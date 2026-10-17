#!/usr/bin/env python3
"""Offline lexical reference search, not answer generation or semantic retrieval."""
import argparse
import csv
import json
from pathlib import Path
import re
import sys
import unicodedata

if __package__:
    from .knowledge_governance import read_page, document_path, GovernanceError
    from .check_workspace import (
        ROOT, MANIFEST_FIELDS, REQUIRED_FIELDS, SOURCE_TOKEN, findings, iso_date,
        linked_path, local_path, metadata, multilingual_metadata, prose, source_id,
    )
else:
    from knowledge_governance import read_page, document_path, GovernanceError
    from check_workspace import (
        ROOT, MANIFEST_FIELDS, REQUIRED_FIELDS, SOURCE_TOKEN, findings, iso_date,
        linked_path, local_path, metadata, multilingual_metadata, prose, source_id,
    )

MESSAGES = {
    "FOUND": "Đã tìm thấy tài liệu có con trỏ nguồn; nội dung claim chưa được tự động xác minh.",
    "NOT_FOUND": "Không tìm thấy tài liệu phù hợp trong scope đã chọn. UNKNOWN.",
    "MISSING_EVIDENCE": "Có tài liệu phù hợp nhưng thiếu bằng chứng nguồn cục bộ hợp lệ. UNKNOWN.",
    "AMBIGUOUS": "Nhiều tài liệu cùng hạng; cần làm rõ truy vấn.",
    "INVALID_DATA": "Không thể tìm kiếm vì metadata hoặc registry không hợp lệ. UNKNOWN.",
    "INVALID_QUERY": "Cần truy vấn và scope tường minh; không tự suy đoán scope.",
    "DISPUTED": "Tài liệu có tranh chấp chưa giải quyết; giữ cả hai nguồn và yêu cầu rà soát.",
    "ACCESS_DENIED": "Tham chiếu chưa được cho phép hoặc scope bị hạn chế; không dùng làm bằng chứng.",
}


def normalize(value):
    return " ".join(unicodedata.normalize("NFC", value).casefold().split())


def contains(text, phrase):
    return bool(phrase) and re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text) is not None


def source_catalog(root):
    """Legacy metadata mode; recorded provenance additionally requires byte hashes."""
    path = local_path(root, root, "sources/manifest.csv")
    catalog = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        if reader.fieldnames != list(MANIFEST_FIELDS):
            raise ValueError("registry header")
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError("registry row")
            row = {key: value.strip() for key, value in row.items()}
            sid = row["source_id"]
            if (not source_id(sid) or sid in catalog
                    or any(not row[field] for field in REQUIRED_FIELDS)
                    or not iso_date(row["retrieved_date"])
                    or row["published_date"] and not iso_date(row["published_date"])):
                raise ValueError("registry value")
            catalog[sid] = None
            try:
                target = local_path(root, root, row["source_url_or_path"])
                if target.is_relative_to(root / "sources/raw") and target.is_file():
                    catalog[sid] = target.relative_to(root).as_posix()
            except (ValueError, OSError):
                pass
    ledger = local_path(root, root, "sources/provenance.jsonl")
    if ledger.exists():
        if __package__:
            from .source_integrity import audit_sources
        else:
            from source_integrity import audit_sources
        audit = audit_sources(root)
        per_source = {"HASH_MISMATCH", "SOURCE_UNAVAILABLE", "MISSING_PROVENANCE", "MISSING_LOCAL_SNAPSHOT"}
        fatal = [issue for issue in audit["issues"] if issue.startswith("ERROR ")
                 and issue.split()[1] not in per_source | {"UNKNOWN_SOURCE_REFERENCE"}]
        if fatal:
            raise ValueError("invalid provenance")
        return {
            sid: {
                "source_path": record["local_path"] if record["integrity_status"] == "MATCH" else None,
                "integrity_status": record["integrity_status"], "source_version": record["source_version"],
                "verification_status": record["verification_status"], "superseded_by": record["superseded_by"],
                "original_uri_status": record["original_uri_status"], "source_uri": record["source_uri"],
            }
            for sid, record in audit["sources"].items()
        }
    return {sid: {"source_path": path, "integrity_status": "LEGACY_UNHASHED", "source_version": None,
                  "verification_status": "UNVERIFIED", "superseded_by": None, "original_uri_status": "UNKNOWN",
                  "source_uri": None}
            for sid, path in catalog.items()}


def pages(root, scope, *, cross_refs=(), include_history=False, authorized_scopes=()):
    selected = []

    def visit(folder):
        if not folder.is_dir():
            return
        for child in sorted(folder.iterdir()):
            try:
                child = local_path(root, root, child.relative_to(root).as_posix())
            except (ValueError, OSError):
                continue
            if child.is_dir():
                yield from visit(child)
            elif child.suffix.lower() == ".md" and child.name not in {"index.md", "log.md"}:
                text = child.read_text(encoding="utf-8-sig")
                meta = metadata(text)
                if meta.get("scope", "unscoped") == scope:
                    # Legacy ADR retrieval remains an agent workflow, as in Phase 1.
                    if child.is_relative_to(root / "decisions") and meta.get("status", "").isupper():
                        continue
                    governed = read_page(root, child, text)
                    if governed["access"] == "restricted" and scope not in authorized_scopes:
                        continue
                    yield child, text, meta, governed

    for folder in ("wiki", "decisions"):
        selected.extend(visit(local_path(root, root, folder)))
    allowed = {ref for _, _, _, governed in selected for ref in governed["cross_project_refs"]}
    for ref in cross_refs:
        if ref not in allowed:
            raise PermissionError("undeclared cross-project reference")
        target = document_path(root, ref)
        text = target.read_text(encoding="utf-8-sig")
        meta = metadata(text)
        governed = read_page(root, target, text)
        if governed["access"] == "restricted" and governed["scope"] not in authorized_scopes:
            raise PermissionError("restricted target scope")
        selected.append((target, text, meta, governed))
    for child, text, meta, governed in selected:
        if governed["status"] in {"superseded", "archived"} and not include_history:
            continue
        if "NOT_YET_EFFECTIVE" in governed["freshness"] and not include_history:
            continue
        fields = multilingual_metadata(meta)
        title = re.search(r"(?m)^#\s+(.+)$", text)
        yield {
            "path": child.relative_to(root).as_posix(), "title": title[1] if title else child.stem,
            "meta": meta, "text": text, "governance": governed, **fields,
        }


def citations(page, catalog):
    listed = set(SOURCE_TOKEN.findall(page["meta"].get("source ids", "")))
    result = []
    seen = set()
    for block in findings(prose(page["text"])):
        required = set(SOURCE_TOKEN.findall(block))
        if not required or not required <= listed:
            return []
        for sid in sorted(required):
            pointer = re.search(r"\[" + re.escape(sid) + r",\s*([^\]\n]+)\]", block)
            record = catalog.get(sid)
            if not record or not record["source_path"] or not pointer:
                return []
            if pointer:
                key = (sid, pointer[1].strip())
                if key not in seen:
                    seen.add(key)
                    result.append({
                        "source_id": sid, **record,
                        "source_pointer": pointer[1].strip(),
                    })
    return result


def decision_citations(root, page, catalog, include_history, authorized_scopes):
    """First-party decisions are evidence of a choice, never external facts."""
    record = page["governance"]
    if record["legacy"]:
        return []
    if any(SOURCE_TOKEN.search(block) for block in findings(prose(page["text"]))):
        return []  # Never use decision approval to bypass an unavailable cited source.
    if record["decision_authority"] == "approved" or (
            include_history and record["decision_authority"] == "historical"
            and record["reviewed_at"]):
        return [{"decision_path": page["path"], "source_pointer": "documented human approval",
                 "evidence_type": "project_decision", "scope": record["scope"]}]
    result = []
    for block in findings(prose(page["text"])):
        if SOURCE_TOKEN.search(block):
            return []
        found = []
        for match in re.finditer(r'\[[^\]\n]+\]\(([^)\s]+)\)', block):
            target = local_path(root, (root / page["path"]).parent, match[1])
            if not target.is_relative_to(root / "decisions") or target.name == "index.md":
                continue
            other_text = target.read_text(encoding="utf-8-sig")
            other = read_page(root, target, other_text)
            if (other["legacy"] or other["scope"] != record["scope"]
                    or other["decision_authority"] != "approved"
                    or other["access"] == "restricted" and other["scope"] not in authorized_scopes):
                return []
            if any(SOURCE_TOKEN.search(block) for block in findings(prose(other_text))):
                node = {"text": other_text, "meta": metadata(other_text)}
                if not citations(node, catalog):
                    return []
            found.append({"decision_path": target.relative_to(root).as_posix(),
                          "source_pointer": "documented human approval", "evidence_type": "project_decision",
                          "scope": other["scope"]})
        if not found:
            return []
        result.extend(found)
    return result


def search(root, query, scope, *, cross_refs=(), include_history=False, authorized_scopes=()):
    """Require explicit scope; only curated, same-scope aliases expand a query."""
    root = Path(root).absolute()
    outcome = {
        "query": query, "scope": scope, "retrieval_only": True,
        "expanded_terms": [], "matches": [], "blocked": [],
    }

    def finish(status):
        outcome.update(status=status, message=MESSAGES[status])
        return outcome

    if not isinstance(query, str) or not isinstance(scope, str) or not query.strip() or not scope.strip():
        return finish("INVALID_QUERY")
    if (not isinstance(cross_refs, (tuple, list)) or any(not isinstance(ref, str) for ref in cross_refs)
            or not isinstance(authorized_scopes, (tuple, list, set))
            or any(not isinstance(item, str) for item in authorized_scopes)):
        return finish("INVALID_QUERY")
    if linked_path(root):
        return finish("INVALID_DATA")
    q = normalize(query)
    candidates = []
    try:
        catalog = source_catalog(root)
        for page in pages(root, scope, cross_refs=cross_refs, include_history=include_history,
                          authorized_scopes=authorized_scopes):
            terms = (
                [("title", page["title"]), ("title_vi", page["title_vi"])]
                + [("keywords", term) for term in page["keywords"]]
                + [("aliases_vi", term) for term in page["aliases_vi"]]
            )
            matched = []
            for field, term in terms:
                n = normalize(term)
                score = 3 if n and q == n else 2 if n and contains(q, n) else 0
                if score:
                    matched.append((score, field, term))
            body = page["text"].split("\n## ", 1)[-1]
            score = max((item[0] for item in matched), default=0)
            if not score and contains(normalize(body), q):
                score = 1
                matched = [(1, "body", query)]
            if not score:
                continue
            additions = []
            if any(item[1] in {"title_vi", "aliases_vi"} for item in matched):
                additions = page["keywords"] or ([page["title"]] if page["language"] == "en" else [])
            governed = page["governance"]
            evidence = citations(page, catalog) or decision_citations(root, page, catalog, include_history, authorized_scopes)
            current = (not governed["legacy"] and governed["status"] == "verified"
                       and governed["temporal"] != "historical" and not governed["freshness"]
                       and governed["scope"] == scope
                       and governed["kind"] not in {"proposed_decision", "historical_decision"}
                       and bool(evidence) and all(c.get("integrity_status") == "MATCH"
                                                 or c.get("evidence_type") == "project_decision" for c in evidence))
            candidates.append({
                "path": page["path"], "title": page["title"],
                "title_vi": page["title_vi"], "language": page["language"],
                "scope": governed["scope"], "page_status": page["meta"].get("status", "UNKNOWN"),
                "knowledge_status": governed["status"], "information_type": governed["kind"],
                "created_at": governed["created_at"], "updated_at": governed["updated_at"],
                "effective_at": governed["effective_at"], "reviewed_at": governed["reviewed_at"],
                "temporal": governed["temporal"],
                "decision_authority": governed["decision_authority"],
                "freshness": governed["freshness"], "conflicts": governed["conflicts"],
                "superseded_by": governed["superseded_by"], "usable_as_current_truth": current,
                "cross_project_context": governed["scope"] != scope,
                "score": score, "matched_fields": sorted({item[1] for item in matched}),
                "matched_terms": list(dict.fromkeys(item[2] for item in matched)),
                "expansion_terms": additions,
                "citations": evidence,
            })
    except PermissionError:
        return finish("ACCESS_DENIED")
    except (OSError, UnicodeError, ValueError, csv.Error):
        return finish("INVALID_DATA")
    if not candidates:
        return finish("NOT_FOUND")
    best = max(page["score"] for page in candidates)
    top = sorted((page for page in candidates if page["score"] == best), key=lambda page: page["path"])
    for page in top:
        for term in page["expansion_terms"]:
            if normalize(term) not in {normalize(item) for item in outcome["expanded_terms"]}:
                outcome["expanded_terms"].append(term)
        outcome["matches" if page["citations"] and page["knowledge_status"] != "disputed"
                and "UNRESOLVED_CONFLICT" not in page["freshness"] else "blocked"].append(page)
    if outcome["blocked"]:
        if any(page["knowledge_status"] == "disputed" or "UNRESOLVED_CONFLICT" in page["freshness"]
               for page in outcome["blocked"]):
            return finish("DISPUTED")
        return finish("MISSING_EVIDENCE")
    return finish("AMBIGUOUS" if len(top) > 1 else "FOUND")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--scope", required=True, help="Exact Scope; missing page Scope is unscoped.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Workspace or explicitly selected test fixture root.")
    parser.add_argument("--cross-ref", action="append", default=[], help="Explicit declared wiki/decision path; context only.")
    parser.add_argument("--include-history", action="store_true")
    parser.add_argument("--allow-restricted-scope", action="append", default=[], help="Use only with task authorization.")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    result = search(args.root, args.query, args.scope, cross_refs=args.cross_ref,
                    include_history=args.include_history, authorized_scopes=args.allow_restricted_scope)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["status"] in {"INVALID_QUERY", "INVALID_DATA"} else 0


if __name__ == "__main__":
    sys.exit(main())
