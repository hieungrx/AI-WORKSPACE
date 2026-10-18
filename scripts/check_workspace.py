#!/usr/bin/env python3
"""Read-only, offline structural checks. Uses only the Python standard library."""
import csv
import argparse
from datetime import date
import json
from pathlib import Path, PureWindowsPath
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).absolute().parents[1]
DOC_DIRS = ("wiki", "projects", "decisions", "handoffs", "prompts", "templates", "experiments")
MANIFEST_FIELDS = (
    "source_id", "title", "source_type", "source_url_or_path", "author",
    "published_date", "retrieved_date", "access_and_license", "notes",
)
REQUIRED_FIELDS = (
    "source_id", "title", "source_type", "source_url_or_path",
    "retrieved_date", "access_and_license",
)
SOURCE_TOKEN = re.compile(r"\bSRC-[\w-]+\b")
LINK = re.compile(r'!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^()\s]+)(?:\s+"[^"\n]*")?\s*\)')
REFERENCE_LINK = re.compile(r"(?m)^\s{0,3}\[[^\]\n]+\]:|!?\[[^\]\n]+\]\[[^\]\n]*\]")
MANUAL_LIMITS = (
    "MANUAL REVIEW: facts, freshness, exact source pointers, permission, human approval, "
    "heading anchors, unsupported Markdown and Obsidian rendering are not verified."
)


def iso_date(value):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def source_id(value):
    return bool(re.fullmatch(r"SRC-\d{8}-\d{3}", value)) and iso_date(
        f"{value[4:8]}-{value[8:10]}-{value[10:12]}"
    )


def protected(path):
    reserved = {"private", "secret", "secrets", "credential", "credentials", "env", "environment",
                "token", "tokens", "identity", "financial"}
    return any(part.startswith(".") or Path(part).stem.lower() in reserved
               or part.lower().startswith(("id_rsa", "id_ed25519", "id_ecdsa"))
               or Path(part).suffix.lower() in {".pem", ".key", ".p12", ".pfx", ".kdbx", ".env"}
               or re.search(r"(?i)(?:^|[_.-])(?:passwords?|credentials?|secrets?|tokens?)(?:[_.-]|$)", part)
               for part in path.parts)


def linked_path(path):
    return path.is_symlink() or getattr(path, "is_junction", lambda: False)()


def local_path(root, base, target):
    """Reject escapes and links before checking target existence or reading it."""
    if not isinstance(target, str) or any(ord(c) < 32 for c in target):
        raise ValueError("INVALID_PATH")
    target = target.replace("\\", "/")
    if Path(target).is_absolute() or PureWindowsPath(target).drive:
        raise ValueError("OUTSIDE_WORKSPACE")
    current = base
    for part in target.split("/"):
        if part in ("", "."):
            continue
        if part != ".." and (":" in part or part.endswith((" ", "."))
                             or re.fullmatch(r"(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?", part)):
            raise ValueError("INVALID_PATH")
        current = current.parent if part == ".." else current / part
        if not current.is_relative_to(root):
            raise ValueError("OUTSIDE_WORKSPACE")
        if protected(current.relative_to(root)):
            raise ValueError("PROTECTED_PATH")
        if linked_path(current):
            raise ValueError("LINKED_PATH")
        if current.is_file() and current.stat().st_nlink > 1:
            raise ValueError("LINKED_PATH")
    return current


def link_path(root, page, target):
    parsed = urlsplit(target.strip("<>"))
    if parsed.scheme.lower() in ("http", "https", "mailto"):
        return None
    if parsed.netloc or PureWindowsPath(target).drive:
        raise ValueError("OUTSIDE_WORKSPACE")
    if parsed.scheme or parsed.query:
        raise ValueError("UNSUPPORTED_LINK")
    return local_path(root, page.parent, unquote(parsed.path)) if parsed.path else page


def prose(text):
    """Remove comments and code examples while preserving line boundaries."""
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m[0].count("\n"), text, flags=re.S)
    lines = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(\x60{3,}|~{3,})", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = None
            lines.append("")
        elif marker:
            fence = marker[1]
            lines.append("")
        else:
            lines.append(re.sub(r"(\x60+).*?\1", "", line))
    return "\n".join(lines)


def metadata(text):
    result = {}
    for line in text.splitlines():
        if re.match(r"^#{2,6}\s", line):
            break
        match = re.match(r"^\s*-\s+(?:\*\*)?([A-Za-z][A-Za-z_ ]*):(?:\*\*)?\s*(.*?)\s*$", line)
        if match:
            result[match[1].lower()] = match[2]
    return result


def identity_metadata(text):
    """Optional IDs, one format. Canonical metadata is Markdown bullets, never YAML."""
    if text.lstrip("\ufeff\r\n ").startswith("---"):
        raise ValueError("UNSUPPORTED_FRONTMATTER")
    meta = metadata(text)
    for field in ("page_id", "decision_key"):
        if field in meta and not re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,95}", meta[field]):
            raise ValueError("INVALID_" + field.upper())
    return meta


def source_pointer(block, sid):
    match = re.search(r"\[" + re.escape(sid) + r",\s*([^\]\n]+)\]", block)
    return match[1].strip() if match and match[1].strip() else None


def multilingual_metadata(meta):
    """Optional additive fields; older pages keep their original meaning."""
    language = meta.get("language", "und")
    if language not in {"en", "vi", "mul", "und"}:
        raise ValueError("language")
    fields = {"language": language, "title_vi": meta.get("title_vi", "")}
    for name in ("keywords", "aliases_vi"):
        try:
            values = json.loads(meta.get(name, "[]"))
        except (ValueError, TypeError):
            raise ValueError(name) from None
        if (not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values)
                or len(set(values)) != len(values)):
            raise ValueError(name)
        fields[name] = values
    return fields


def findings(text):
    """Yield structured FACT blocks and items in the canonical findings section."""
    block = []
    verified = False
    for line in text.splitlines() + [""]:
        heading = re.match(r"^(#{1,6})\s+(.+)", line)
        item = re.match(r"^\s*(?:[-*+]|\d+\.)\s+", line)
        fact = re.search(r"\bFACT(?:\*\*)?\s*:", line)
        if heading or not line.strip() or item:
            if block:
                yield "\n".join(block)
                block = []
        if heading:
            if len(heading[1]) <= 2:
                verified = heading[2].strip().lower() == "verified findings"
        elif line.strip() and (verified or fact or block):
            block.append(line)


def check_workspace(root=ROOT, integrity=False, security=False):
    root = Path(root).absolute()
    issues = []

    def report(level, code, page, message):
        issues.append(f"{level} {code} {page.relative_to(root).as_posix()}: {message}")

    if linked_path(root):
        return ["ERROR LINKED_ROOT .: workspace root must not be a symlink or junction."]

    ids = set()
    source_catalog = {}
    manifest = root / "sources/manifest.csv"
    try:
        manifest = local_path(root, root, "sources/manifest.csv")
        with manifest.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, strict=True)
            if reader.fieldnames != list(MANIFEST_FIELDS):
                report("ERROR", "MANIFEST_HEADER", manifest, "expected the nine schema columns in order.")
            else:
                for row_number, row in enumerate(reader, 2):
                    prefix = f"row {row_number}"
                    if None in row or any(value is None for value in row.values()):
                        report("ERROR", "MANIFEST_ROW", manifest, f"{prefix} has the wrong number of values.")
                        continue
                    row = {key: value.strip() for key, value in row.items()}
                    for field in REQUIRED_FIELDS:
                        if not row[field]:
                            report("ERROR", "MISSING_SOURCE_VALUE", manifest, f"{prefix} is missing {field}.")
                    sid = row["source_id"]
                    if not source_id(sid):
                        report("ERROR", "INVALID_SOURCE_ID", manifest, f"{prefix} has an invalid source ID/date.")
                    elif sid in ids:
                        report("ERROR", "DUPLICATE_SOURCE", manifest, f"{prefix} repeats a source ID.")
                    else:
                        ids.add(sid)
                    source_catalog[sid] = {"source_path": None, "integrity_status": "NOT_CHECKED"}
                    for field in ("published_date", "retrieved_date"):
                        if row[field] and not iso_date(row[field]):
                            report("ERROR", "INVALID_SOURCE_DATE", manifest, f"{prefix} has an invalid {field}.")
                    if (not row["author"] or not row["published_date"]) and not row["notes"]:
                        report("WARNING", "SOURCE_GAP", manifest, f"{prefix} needs a note explaining unknown metadata.")
                    location = row["source_url_or_path"]
                    if not location:
                        continue
                    try:
                        parsed = urlsplit(location)
                        if parsed.scheme.lower() in ("http", "https") and parsed.netloc:
                            continue
                        target = local_path(root, root, location)
                        if not target.is_relative_to(root / "sources/raw"):
                            raise ValueError("OUTSIDE_RAW")
                        if not target.is_file():
                            report("ERROR", "MISSING_RAW_SOURCE", manifest, f"{prefix} points to no local source file.")
                        else:
                            source_catalog[sid]["source_path"] = target.relative_to(root).as_posix()
                    except (ValueError, OSError):
                        report("ERROR", "INVALID_SOURCE_PATH", manifest, f"{prefix} must use a permitted raw path or HTTP(S) URL.")
    except (OSError, UnicodeError, csv.Error, ValueError):
        report("ERROR", "MANIFEST_READ", manifest, "cannot safely read a valid UTF-8 CSV manifest.")

    documents = {}

    def collect(path):
        relative = path.relative_to(root)
        if protected(relative):
            report("WARNING", "PROTECTED_PATH", path, "contents skipped; review the location manually.")
        elif linked_path(path):
            report("WARNING", "LINKED_PATH", path, "symlink/junction skipped without following it.")
        elif path.is_dir():
            for child in sorted(path.iterdir()):
                collect(child)
        elif path.suffix.lower() == ".md":
            try:
                documents[path] = prose(path.read_text(encoding="utf-8-sig"))
            except (OSError, UnicodeError):
                report("ERROR", "DOCUMENT_READ", path, "cannot read UTF-8 Markdown.")

    try:
        for page in sorted(root.glob("*.md")):
            collect(page)
        for folder in DOC_DIRS:
            path = root / folder
            if linked_path(path) or path.exists():
                collect(path)
    except OSError:
        return issues + ["ERROR DOCUMENT_SCAN .: cannot enumerate permitted documentation."]

    graph = {page: set() for page in documents}
    for page, text in documents.items():
        index_targets = set()
        starts = len(re.findall(r"!?\[[^\]\n]*\]\(", text))
        if (REFERENCE_LINK.search(text) or re.search(r"!?\[\[[^\]\n]+\]\]", text)
                or starts > len(list(LINK.finditer(text)))):
            report("WARNING", "UNSUPPORTED_MARKDOWN", page, "unsupported link syntax needs manual review.")
        for match in LINK.finditer(text):
            try:
                target = link_path(root, page, match[1])
                if target is not None:
                    if page.name == "index.md" and target.suffix == ".md":
                        if target in index_targets:
                            report("WARNING", "DUPLICATE_INDEX_ENTRY", page, "a Markdown target is listed more than once.")
                        index_targets.add(target)
                    if target.exists():
                        graph[page].add(target)
                    else:
                        report("ERROR", "BROKEN_LINK", page, "an inline link/image file target does not exist.")
            except (ValueError, OSError) as error:
                code = str(error) if str(error) in {
                    "OUTSIDE_WORKSPACE", "PROTECTED_PATH", "LINKED_PATH", "UNSUPPORTED_LINK"
                } else "INVALID_LINK"
                level = "WARNING" if code in {"PROTECTED_PATH", "LINKED_PATH", "UNSUPPORTED_LINK"} else "ERROR"
                report(level, code, page, "target was not accessed; review the link manually.")

    def adr_targets(page, text):
        targets = set()
        for match in LINK.finditer(text):
            try:
                target = link_path(root, page, match[1])
                if target in documents and target.is_relative_to(root / "decisions") and target.name != "index.md":
                    targets.add(target)
            except (ValueError, OSError):
                continue
        return targets

    if __package__:
        from .knowledge_governance import STATES, audit_governance, current_eligibility, evaluate_evidence
    else:
        from knowledge_governance import STATES, audit_governance, current_eligibility, evaluate_evidence
    source_audit = None
    if integrity:
        if __package__:
            from .source_integrity import audit_sources
        else:
            from source_integrity import audit_sources
        source_audit = audit_sources(root)
        source_catalog = {sid: {**record, "source_path": record["local_path"]
                               if record["integrity_status"] == "MATCH" else None}
                          for sid, record in source_audit["sources"].items()}
    governance = audit_governance(root)
    issues.extend(governance["issues"])
    approved = {page for page, text in documents.items()
                if page.is_relative_to(root / "decisions") and page.name != "index.md"
                and metadata(text).get("status") == "APPROVED"}
    approved |= {root / path for path, record in governance["pages"].items()
                 if path.startswith("decisions/") and record["decision_authority"] == "approved"}
    wiki = {page for page in documents if page.is_relative_to(root / "wiki")}
    canonical_decisions = {root / path for path, record in governance["pages"].items()
                           if path.startswith("decisions/") and not record["legacy"]}
    page_ids, current_decisions = {}, {}
    for page in sorted(wiki | canonical_decisions):
        text = documents[page]
        tokens = set(SOURCE_TOKEN.findall(text))
        for sid in sorted(tokens):
            if not source_id(sid):
                report("ERROR", "INVALID_SOURCE_ID", page, "a source token has an invalid ID/date.")
            elif sid not in ids:
                report("ERROR", "UNKNOWN_SOURCE", page, f"{sid} is not registered.")
        if page.name == "index.md" or page == root / "wiki/log.md":
            continue
        meta = metadata(text)
        try:
            identity_metadata(text)
        except ValueError as error:
            report("ERROR", str(error), page, "use canonical Markdown metadata and valid optional identifiers.")
        if page_id := meta.get("page_id"):
            if page_id in page_ids:
                report("ERROR", "DUPLICATE_PAGE_ID", page, "page_id must be unique across wiki and canonical decisions.")
            page_ids[page_id] = page
        try:
            multilingual_metadata(meta)
        except ValueError as error:
            report("ERROR", "INVALID_MULTILINGUAL_METADATA", page, f"invalid optional {error} field.")
        status = meta.get("status")
        governed = governance["pages"].get(page.relative_to(root).as_posix(), {})
        modern = not governed.get("legacy", True)
        if modern and governed.get("status") in {"draft", "unverified"}:
            report("WARNING", "UNREVIEWED_KNOWLEDGE", page, "knowledge awaits authorized validation; citations are not factual verification.")
        if (modern and governed.get("decision_authority") == "approved" and current_eligibility(governed)
                and meta.get("decision_key")):
            key = (governed["scope"], meta["decision_key"])
            if key in current_decisions:
                report("ERROR", "CURRENT_DECISION_COLLISION", page, "multiple current approved decisions share scope and decision_key; review and supersede explicitly.")
            current_decisions[key] = page
        if status not in {"DRAFT", "REVIEWED", "STALE"} | STATES:
            report("ERROR", "INVALID_STATUS", page, "invalid legacy or lifecycle status.")
        if not iso_date(meta.get("updated_at", meta.get("updated", ""))):
            report("ERROR", "INVALID_UPDATED", page, "Updated must be a real ISO date.")
        source_field = meta.get("source ids")
        listed = set(SOURCE_TOKEN.findall(source_field or ""))
        if source_field is None or (not listed and source_field not in {"None", "None ingested yet"}):
            report("ERROR", "INVALID_SOURCE_FIELD", page, "Source IDs must list IDs or an explicit None value.")
        if tokens - listed:
            report("ERROR", "UNLISTED_SOURCE", page, "cited source IDs must also appear in Source IDs metadata.")
        decision_field = meta.get("decision references", "None")
        if modern:
            proof = evaluate_evidence(root, page, source_catalog, text=text, record=governed,
                                      scope=governed["scope"], authorized_scopes=(governed["scope"],))
            for level, code in proof["issues"]:
                report(level, code, page, "claim evidence or decision dependency needs review; current truth is separately gated.")
            for block in findings(text):
                for sid in set(SOURCE_TOKEN.findall(block)) & ids:
                    if not source_pointer(block, sid):
                        report("ERROR", "MISSING_CITATION_POINTER", page, "each cited source needs an exact pointer.")
            if status == "verified" and not proof["complete"]:
                report("ERROR", "VERIFIED_WITHOUT_EVIDENCE", page, "verified requires complete per-finding evidence.")
            elif not proof["citations"]:
                report("WARNING", "NO_EVIDENCE", page, "page has no registered source or approved decision evidence.")
            continue
        eligible = approved
        if not modern and meta.get("scope"):
            eligible = {target for target in approved
                        if metadata(documents[target]).get("scope") == meta["scope"]}
        decisions = adr_targets(page, decision_field)
        if decision_field != "None" and (not decisions or decisions - eligible):
            report("ERROR", "UNAPPROVED_DECISION", page, "Decision references must link directly to APPROVED ADRs.")
        decision_evidence = decisions & eligible
        for block in findings(text):
            block_decisions = adr_targets(page, block) & eligible
            if page in canonical_decisions and governed.get("decision_authority") == "approved":
                block_decisions.add(page)  # A first-party choice is supported by its own human-approved ADR.
            decision_evidence |= block_decisions
            if not (set(SOURCE_TOKEN.findall(block)) & ids or block_decisions):
                report("ERROR", "MISSING_CITATION", page, "a structured factual finding needs a registered source or APPROVED ADR.")
            for sid in set(SOURCE_TOKEN.findall(block)) & ids:
                if not source_pointer(block, sid):
                    report("ERROR", "MISSING_CITATION_POINTER", page, "each cited source in a finding needs [source_id, exact pointer].")
        has_evidence = bool(listed & ids or decision_evidence)
        if status == "verified" and not has_evidence and governed.get("decision_authority") != "approved":
            report("ERROR", "VERIFIED_WITHOUT_EVIDENCE", page, "verified requires traceable source or same-scope approved decision.")
        if status == "REVIEWED" and not has_evidence:
            report("ERROR", "REVIEWED_WITHOUT_EVIDENCE", page, "REVIEWED requires source or approved decision evidence.")
        elif not has_evidence:
            report("WARNING", "NO_EVIDENCE", page, "page has no registered source or approved decision evidence.")
            if status == "DRAFT" and not re.search(
                r"\b(?:HYPOTHESIS|UNKNOWN|unverified|not source-verified|evidence gap|None ingested yet)\b",
                text, re.I,
            ):
                report("ERROR", "UNMARKED_DRAFT", page, "mark the hypothesis or evidence gap explicitly.")
        if status == "STALE":
            report("WARNING", "STALE_PAGE", page, "freshness needs human review.")

    index = root / "wiki/index.md"
    if index not in documents:
        report("ERROR", "MISSING_INDEX", index, "wiki entry point is missing or unreadable.")
    if root / "wiki/log.md" not in documents:
        report("ERROR", "MISSING_LOG", root / "wiki/log.md", "activity log is missing or unreadable.")
    reachable = set()
    pending = [index]
    while pending:
        page = pending.pop()
        if page not in reachable:
            reachable.add(page)
            pending.extend(graph.get(page, set()) - reachable)
    for page in sorted(wiki - reachable):
        if page.name != "index.md" and page != root / "wiki/log.md":
            report("WARNING", "ORPHAN_PAGE", page, "not reachable through checked links from wiki/index.md.")
    if source_audit is not None:
        for issue in source_audit["issues"]:
            if issue not in issues:
                issues.append(issue)
    if security:
        if __package__:
            from .workspace_security import audit_security
            from .safe_operations import ensure_idle
        else:
            from workspace_security import audit_security
            from safe_operations import ensure_idle
        issues.extend(audit_security(root))
        try:
            ensure_idle(root)
        except ValueError:
            issues.append("ERROR RECOVERY_REQUIRED recovery/: writes or recovery need review.")
    return issues


def main(root=ROOT, integrity=False, security=False):
    issues = check_workspace(root, integrity=integrity, security=security)
    for issue in issues:
        print(issue)
    errors = sum(issue.startswith("ERROR ") for issue in issues)
    warnings = sum(issue.startswith("WARNING ") for issue in issues)
    if errors:
        print(f"FAIL: {errors} structural error(s), {warnings} warning(s).")
    elif warnings:
        print(f"CHECKS COMPLETED: 0 structural errors, {warnings} warning(s).")
    else:
        print("PASS: structural checks only; NOT a factual verification.")
    print(MANUAL_LIMITS)
    if not integrity:
        print("HASH CHECKS: not run; use --integrity for required provenance and SHA-256 checks.")
    return 1 if errors else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--integrity", action="store_true", help="Require provenance and verify local raw bytes read-only.")
    parser.add_argument("--security", action="store_true", help="Scan approved public documents without opening sensitive files.")
    args = parser.parse_args()
    sys.exit(main(integrity=args.integrity, security=args.security))
