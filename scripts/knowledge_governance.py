"""Phase 2: one Markdown contract, explicit authority and scoped context."""
from datetime import date
import csv
import hashlib
import json
from pathlib import Path
import re

if __package__:
    from .check_workspace import LINK, SOURCE_TOKEN, findings, identity_metadata, iso_date, link_path, local_path, metadata, prose, source_pointer
else:
    from check_workspace import LINK, SOURCE_TOKEN, findings, identity_metadata, iso_date, link_path, local_path, metadata, prose, source_pointer

STATES = {"draft", "unverified", "verified", "disputed", "superseded", "archived"}
KINDS = {"external_fact", "interpretation", "hypothesis", "requirement",
         "proposed_decision", "approved_decision", "historical_decision"}
TRANSITIONS = {
    "draft": {"unverified", "archived"},
    "unverified": {"draft", "verified", "disputed", "archived"},
    "verified": {"unverified", "disputed", "superseded", "archived"},
    "disputed": {"unverified", "archived"},
    "superseded": {"archived"},
    "archived": {"draft"},
}
LEGACY = {"DRAFT": "draft", "REVIEWED": "unverified", "STALE": "unverified",
          "PROPOSED": "draft", "APPROVED": "unverified",
          "SUPERSEDED": "superseded", "ARCHIVED": "archived"}
MANAGED = {"kind", "created_at", "updated_at", "effective_at", "reviewed_at",
           "superseded_by", "transitions", "temporal", "review_after", "conflicts",
           "cross_project_refs", "access"}
DYNAMIC = {"status", "updated_at", "reviewed_at", "superseded_by", "transitions"}
FIELD = re.compile(r"^\s*-\s+(?:\*\*)?([A-Za-z][A-Za-z_ ]*):(?:\*\*)?\s*(.*?)\s*$")
MAX_DECISION_DEPTH = 32  # Fail-closed resource bound, not a measured capacity/SLA.


class GovernanceError(ValueError):
    pass


def header(text):
    for line in text.splitlines():
        if re.match(r"^#{2,6}\s", line):
            break
        match = FIELD.match(line)
        if match:
            yield match[1].lower(), match[2]


def content_hash(text):
    """Bind body and stable metadata, excluding only lifecycle bookkeeping."""
    lines = []
    in_header = True
    for line in text.splitlines():
        if re.match(r"^#{2,6}\s", line):
            in_header = False
        match = FIELD.match(line) if in_header else None
        if not match or match[1].lower() not in DYNAMIC:
            lines.append(line)
    return "sha256:" + hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()


def array(meta, name):
    try:
        values = json.loads(meta.get(name, "[]"))
    except ValueError:
        raise GovernanceError("INVALID_" + name.upper()) from None
    if not isinstance(values, list):
        raise GovernanceError("INVALID_" + name.upper())
    return values


def document_path(root, relative):
    path = local_path(root, root, relative)
    if not any(path.is_relative_to(root / folder) for folder in ("wiki", "decisions")):
        raise GovernanceError("INVALID_KNOWLEDGE_PATH")
    if path.suffix != ".md" or path.name in {"index.md", "log.md"}:
        raise GovernanceError("INVALID_KNOWLEDGE_PATH")
    return path


def history_hash(events):
    """Bind an approval to one exact append position, independent of JSON spacing."""
    data = json.dumps(events, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(data.encode("utf-8")).hexdigest()


def approval_required(event):
    return event["to"] == "verified" or (event["from"], event["to"]) == ("disputed", "unverified")


def approval(root, relative, page, text, at, *, event=None, prefix=(), write=False,
             bind_current=True, today=None):
    """Validate a human-authored authorization record, never create one."""
    if not isinstance(relative, str) or not relative:
        raise GovernanceError("HUMAN_APPROVAL_REQUIRED")
    path = local_path(root, root, relative)
    if not path.is_relative_to(root / "experiments") or path.suffix != ".md":
        raise GovernanceError("INVALID_APPROVAL_PATH")
    approval_text = path.read_text(encoding="utf-8-sig")
    pairs = list(header(approval_text))
    if len({key for key, _ in pairs}) != len(pairs):
        raise GovernanceError("DUPLICATE_APPROVAL_METADATA")
    record = metadata(approval_text)
    now = (today or date.today()).isoformat()
    expires, revoked = record.get("expires_at"), record.get("revoked_at")
    if any(value and not iso_date(value) for value in (expires, revoked)):
        raise GovernanceError("INVALID_APPROVAL_DATE")
    if (record.get("authority") != "human" or record.get("status") not in {"APPROVED", "REVOKED"}
            or record.get("target") != page.relative_to(root).as_posix()
            or not re.fullmatch(r"sha256:[0-9a-f]{64}", record.get("content_hash", ""))
            or record.get("validated_at") != at or not iso_date(at)):
        raise GovernanceError("INVALID_HUMAN_APPROVAL")
    if record["status"] == "REVOKED" and (not revoked or revoked <= at) or revoked and revoked <= at:
        raise GovernanceError("APPROVAL_REVOKED")
    if expires and expires < at:
        raise GovernanceError("APPROVAL_EXPIRED")
    flags = []
    if record["status"] == "REVOKED" or revoked and revoked <= now:
        flags.append("APPROVAL_REVOKED")
    if expires and expires < now:
        flags.append("APPROVAL_EXPIRED")
    if write and flags:
        raise GovernanceError(flags[0])
    if event is not None:
        policy = event.get("approval_policy", 1)
        if type(policy) is not int or policy not in {1, 2} or record.get("approval_policy", "1") != str(policy):
            raise GovernanceError("APPROVAL_POLICY_MISMATCH")
        if write and policy != 2:
            raise GovernanceError("APPROVAL_POLICY_REQUIRED")
        if policy == 2:
            if (record.get("from_state") != event["from"] or record.get("to_state") != event["to"]
                    or record.get("prior_transitions_hash") != history_hash(prefix)
                    or event.get("approval_content_hash") != record["content_hash"]):
                raise GovernanceError("APPROVAL_EVENT_MISMATCH")
        elif any(key in record for key in ("from_state", "to_state", "prior_transitions_hash")):
            raise GovernanceError("APPROVAL_POLICY_REQUIRED")
    if bind_current and record["content_hash"] != content_hash(text):
        raise GovernanceError("INVALID_HUMAN_APPROVAL")
    evidence = array(record, "evidence")
    if not evidence:
        raise GovernanceError("VALIDATION_EVIDENCE_REQUIRED")
    for item in evidence:
        if not isinstance(item, str):
            raise GovernanceError("INVALID_VALIDATION_EVIDENCE")
        target = local_path(root, root, item)
        if (target == path or not target.is_file()
                or not any(target.is_relative_to(root / folder)
                           for folder in ("experiments", "reports", "decisions"))):
            raise GovernanceError("INVALID_VALIDATION_EVIDENCE")
    return {"reference": relative, "policy": record.get("approval_policy", "1"),
            "content_hash": record["content_hash"], "current_flags": flags}


def validate_event_approval(root, page, text, event, prefix, *, write=False,
                            bind_current=False, today=None):
    """One authorization check for helper, writer preflight and historical replay."""
    if not approval_required(event):
        if any(key in event for key in ("approval_policy", "approval_content_hash")):
            raise GovernanceError("UNEXPECTED_EVENT_APPROVAL")
        return None
    result = approval(root, event["approval"], page, text, event["at"], event=event,
                      prefix=prefix, write=write, bind_current=bind_current, today=today)
    if (write and event["from"] == "disputed" and event["to"] == "unverified"
            and any(c["resolution"] is None for c in array(metadata(text), "conflicts"))):
        raise GovernanceError("UNRESOLVED_CONFLICT")
    return result


def current_eligibility(record, scope=None):
    """Canonical own-record gate; FOUND is deliberately independent of this."""
    return (not record["legacy"] and record["status"] == "verified"
            and record["temporal"] != "historical" and not record["freshness"]
            and (scope is None or record["scope"] == scope)
            and record["kind"] not in {"proposed_decision", "historical_decision"})


def evaluate_evidence(root, page, catalog, *, text=None, record=None, scope=None,
                      authorized_scopes=(), today=None, _visiting=()):
    """Per-finding proof and transitive ADR eligibility, shared by Query and Lint.

    Raw citations in a finding must all remain intact. An independently supported
    finding may retain an ineligible ADR as context; it cannot support another
    finding. Ordinary wiki links never create a new source of authority.
    """
    root, page = Path(root).absolute(), Path(page).absolute()
    relative = page.relative_to(root).as_posix()
    result = {"citations": [], "complete": True, "current": False, "reasons": [], "issues": []}
    def problem(level, code):
        result["issues"].append((level, code))
        result["reasons"].append(code)
    if relative in _visiting:
        problem("ERROR", "DECISION_EVIDENCE_CYCLE")
        result["complete"] = False
        return result
    if len(_visiting) >= MAX_DECISION_DEPTH:
        problem("ERROR", "DECISION_EVIDENCE_LIMIT")
        result["complete"] = False
        return result
    text = page.read_text(encoding="utf-8-sig") if text is None else text
    meta = metadata(text)
    record = read_page(root, page, text, today=today, _registered_ids=frozenset(catalog)) if record is None else record
    target_scope = record["scope"] if scope is None else scope
    own_current = current_eligibility(record, target_scope)
    blocks = list(findings(prose(text)))
    all_current = bool(blocks)
    listed = set(SOURCE_TOKEN.findall(meta.get("source ids", "")))
    visiting = _visiting + (relative,)

    def decision(target):
        if not target.is_relative_to(root / "decisions") or target.name == "index.md":
            return None
        try:
            child_text = target.read_text(encoding="utf-8-sig")
            child = read_page(root, target, child_text, today=today, _registered_ids=frozenset(catalog))
            if (child["legacy"] or child["scope"] != record["scope"]
                    or child["decision_authority"] not in {"approved", "historical"}
                    or child["access"] == "restricted" and child["scope"] not in authorized_scopes):
                problem("ERROR", "INVALID_DECISION_AUTHORITY")
                return None
            if __package__:
                from .workspace_security import require_safe_data
            else:
                from workspace_security import require_safe_data
            require_safe_data(child_text)
            evaluated = evaluate_evidence(root, target, catalog, text=child_text, record=child,
                                          scope=target_scope, authorized_scopes=authorized_scopes,
                                          today=today, _visiting=visiting)
            for level, code in evaluated["issues"]:
                problem(level, code)
            eligible = evaluated["current"] and child["decision_authority"] == "approved"
            if not eligible:
                problem("WARNING", "INELIGIBLE_DECISION_DEPENDENCY")
            citation = {"decision_path": target.relative_to(root).as_posix(),
                        "source_pointer": "documented human approval", "evidence_type": "project_decision",
                        "scope": child["scope"], "eligible_for_current_truth": eligible,
                        "context_only": not eligible,
                        "knowledge_status": child["status"], "temporal": child["temporal"],
                        "freshness": child["freshness"], "eligibility_reasons": evaluated["reasons"]}
            return evaluated["complete"], eligible, citation
        except (ValueError, OSError, UnicodeError, csv.Error):
            problem("ERROR", "INVALID_DECISION_REFERENCE")
            return None

    for block in blocks:
        required = set(SOURCE_TOKEN.findall(block))
        raw, raw_current = [], True
        for sid in sorted(required):
            source = catalog.get(sid, {})
            path = source.get("source_path") if "source_path" in source else (
                source.get("local_path") if source.get("integrity_status") == "MATCH" else None)
            pointer = source_pointer(block, sid)
            if sid not in listed or not path or not pointer:
                raw_current = False
                continue
            raw.append({"source_id": sid, **source, "source_path": path, "source_pointer": pointer})
            raw_current &= source.get("integrity_status") == "MATCH"
        raw_complete = bool(required) and len(raw) == len(required)
        dependencies = []
        knowledge_link = False
        for match in LINK.finditer(block):
            try:
                target = link_path(root, page, match[1])
                if target is None or not any(target.is_relative_to(root / folder) for folder in ("wiki", "decisions")):
                    continue
                knowledge_link = True
                evaluated = decision(target)
                if evaluated:
                    dependencies.append(evaluated)
            except (ValueError, OSError):
                knowledge_link = True
                problem("ERROR", "INVALID_DECISION_REFERENCE")
        self_choice = (not required and not knowledge_link and not record["legacy"]
                       and page.is_relative_to(root / "decisions")
                       and record["decision_authority"] in {"approved", "historical"})
        if required:
            # A cited missing/tampered raw source is never silently replaced by an ADR.
            supported, eligible = raw_complete, raw_complete and raw_current
        else:
            supported = self_choice or any(dep[0] for dep in dependencies)
            eligible = self_choice or any(dep[1] for dep in dependencies)
        result["complete"] &= supported
        all_current &= eligible
        if raw_complete:
            result["citations"].extend(raw)
        result["citations"].extend(dep[2] for dep in dependencies if dep[0])
        if self_choice:
            result["citations"].append({"decision_path": relative, "source_pointer": "documented human approval",
                                        "evidence_type": "project_decision", "scope": record["scope"],
                                        "eligible_for_current_truth": own_current})
        if not supported:
            problem("ERROR", "MISSING_CLAIM_EVIDENCE")
    # Metadata references are provenance/context, not blanket proof for unlinked findings.
    decision_field = meta.get("decision references", "None")
    if decision_field != "None":
        references = list(LINK.finditer(decision_field))
        if not references:
            problem("ERROR", "UNAPPROVED_DECISION")
        for match in references:
            try:
                target = link_path(root, page, match[1])
                if (target is None or not target.is_relative_to(root / "decisions")
                        or target.name == "index.md" or decision(target) is None):
                    problem("ERROR", "UNAPPROVED_DECISION")
            except (ValueError, OSError):
                problem("ERROR", "INVALID_DECISION_REFERENCE")
    if not blocks:
        result["complete"] = False
    if not own_current:
        result["reasons"].extend(record["freshness"] or ["NOT_CURRENT_KNOWLEDGE"])
    result["current"] = bool(own_current and result["complete"] and all_current)
    result["issues"] = sorted(set(result["issues"]))
    result["reasons"] = sorted(set(result["reasons"]))
    unique = {json.dumps(citation, sort_keys=True): citation for citation in result["citations"]}
    result["citations"] = list(unique.values())
    return result


def check_transition(before, after, actor):
    if any(not isinstance(value, str) for value in (before, after, actor)):
        raise GovernanceError("INVALID_TRANSITION_HISTORY")
    if before not in TRANSITIONS or after not in TRANSITIONS[before]:
        raise GovernanceError("ILLEGAL_TRANSITION")
    if actor not in {"human", "ai"}:
        raise GovernanceError("INVALID_ACTOR")
    if (after in {"verified", "superseded", "archived"} or before in {"archived", "disputed"}) and actor != "human":
        raise GovernanceError("HUMAN_AUTHORITY_REQUIRED")


def read_page(root, page, text=None, today=None, *, _registered_ids=None):
    root, page = Path(root).absolute(), Path(page).absolute()
    text = page.read_text(encoding="utf-8-sig") if text is None else text
    meta = identity_metadata(text)
    legacy = not (MANAGED & meta.keys()) and meta.get("status") in LEGACY
    scope = meta.get("scope", "unscoped")
    if not scope or scope.strip() != scope:
        raise GovernanceError("INVALID_SCOPE")
    if legacy:
        raw_status = meta["status"]
        kind = {"PROPOSED": "proposed_decision", "APPROVED": "approved_decision",
                "SUPERSEDED": "historical_decision", "ARCHIVED": "historical_decision"}.get(raw_status, "unknown")
        return dict(legacy=True, status=LEGACY[raw_status], kind=kind, scope=scope,
                    access="workspace", cross_project_refs=[], conflicts=[], superseded_by=None,
                    created_at=None, updated_at=meta.get("updated"), effective_at=None,
                    reviewed_at=None, temporal="unknown",
                    freshness=["LEGACY_METADATA"] + (["REVIEW_REQUIRED"] if raw_status == "STALE" else []),
                    decision_authority="legacy_unvalidated" if kind.endswith("decision") else None)
    pairs = list(header(text))
    if len({key for key, _ in pairs}) != len(pairs):
        raise GovernanceError("DUPLICATE_METADATA")
    if "updated" in meta or "related project" in meta:
        raise GovernanceError("MIXED_METADATA")
    state, kind = meta.get("status"), meta.get("kind")
    if state not in STATES or kind not in KINDS:
        raise GovernanceError("INVALID_GOVERNANCE_METADATA")
    source_field = meta.get("source ids")
    listed_sources = set(SOURCE_TOKEN.findall(source_field or ""))
    if source_field is None or not listed_sources and source_field != "None":
        raise GovernanceError("INVALID_SOURCE_FIELD")
    if set(SOURCE_TOKEN.findall(prose(text))) - listed_sources:
        raise GovernanceError("UNLISTED_SOURCE")
    if __package__:
        from .source_integrity import read_registry
    else:
        from source_integrity import read_registry
    # An owning read operation may share its already validated registry IDs.
    # Never retain these across operations or use them to skip raw hash checks.
    registered_ids = read_registry(root).keys() if _registered_ids is None else _registered_ids
    if listed_sources - registered_ids:
        raise GovernanceError("UNKNOWN_SOURCE")
    if "scope" not in meta or meta.get("temporal") not in {"historical", "current", "time_sensitive"}:
        raise GovernanceError("MISSING_GOVERNANCE_METADATA")
    if kind == "historical_decision" and meta["temporal"] != "historical":
        raise GovernanceError("HISTORICAL_DECISION_TEMPORAL")
    dates = {}
    for key in ("created_at", "updated_at", "effective_at", "reviewed_at", "review_after"):
        value = meta.get(key) or None
        if value is not None and not iso_date(value) or key in {"created_at", "updated_at"} and value is None:
            raise GovernanceError("INVALID_LIFECYCLE_DATE")
        dates[key] = value
    if (dates["created_at"] > dates["updated_at"]
            or dates["reviewed_at"] and not dates["created_at"] <= dates["reviewed_at"] <= dates["updated_at"]):
        raise GovernanceError("INCONSISTENT_LIFECYCLE_DATES")
    access = meta.get("access", "workspace")
    if access not in {"workspace", "restricted"}:
        raise GovernanceError("INVALID_ACCESS")
    refs = array(meta, "cross_project_refs")
    if any(not isinstance(item, str) for item in refs) or len(set(refs)) != len(refs):
        raise GovernanceError("INVALID_CROSS_PROJECT_REFS")
    for item in refs:
        referenced = document_path(root, item)
        if not referenced.is_file():
            raise GovernanceError("MISSING_CROSS_PROJECT_REF")
        if metadata(referenced.read_text(encoding="utf-8-sig")).get("scope", "unscoped") == scope:
            raise GovernanceError("CROSS_PROJECT_SCOPE_REQUIRED")
    relative = page.relative_to(root)
    if relative.parts[:2] == ("wiki", "projects") and len(relative.parts) >= 4 and relative.parts[2] != scope:
        raise GovernanceError("PROJECT_SCOPE_MISMATCH")
    conflicts = array(meta, "conflicts")
    for conflict in conflicts:
        if (not isinstance(conflict, dict) or set(conflict) != {"summary", "source_ids", "resolution"}
                or not isinstance(conflict["summary"], str) or not conflict["summary"].strip()
                or not isinstance(conflict["source_ids"], list)
                or any(not isinstance(sid, str) for sid in conflict["source_ids"])
                or len(set(conflict["source_ids"])) < 2
                or conflict["resolution"] is not None and
                (not isinstance(conflict["resolution"], str) or not conflict["resolution"].strip())):
            raise GovernanceError("INVALID_CONFLICT")
        listed = set(SOURCE_TOKEN.findall(meta.get("source ids", "")))
        if not set(conflict["source_ids"]) <= listed:
            raise GovernanceError("UNLISTED_CONFLICT_SOURCE")
    unresolved = any(item["resolution"] is None for item in conflicts)
    if state == "verified" and unresolved:
        raise GovernanceError("UNRESOLVED_CONFLICT")
    if state == "disputed" and not conflicts:
        raise GovernanceError("CONFLICT_RECORD_REQUIRED")
    # A foreign page can be context, never a factual statement of this project's choice.
    for block in findings(prose(text)):
        for match in LINK.finditer(block):
            target = link_path(root, page, match[1])
            if (target is not None and target.is_file()
                    and any(target.is_relative_to(root / folder) for folder in ("wiki", "decisions"))
                    and target.name not in {"index.md", "log.md"}
                    and metadata(target.read_text(encoding="utf-8-sig")).get("scope", "unscoped") != scope):
                raise GovernanceError("CROSS_PROJECT_EVIDENCE")
    successor = meta.get("superseded_by") or None
    if state == "superseded" and not successor:
        raise GovernanceError("SUCCESSOR_REQUIRED")
    if successor:
        target = document_path(root, successor)
        other = metadata(target.read_text(encoding="utf-8-sig"))
        if (target == page or other.get("scope") != scope
                or other.get("kind") != kind or other.get("status") not in {"verified", "superseded", "archived"}
                or state not in {"superseded", "archived"}):
            raise GovernanceError("INVALID_SUCCESSOR")
        seen = {relative.as_posix()}
        while target:
            rel = target.relative_to(root).as_posix()
            if rel in seen:
                raise GovernanceError("SUCCESSOR_CYCLE")
            seen.add(rel)
            next_ref = other.get("superseded_by")
            target = document_path(root, next_ref) if next_ref else None
            other = metadata(target.read_text(encoding="utf-8-sig")) if target else {}
    events = array(meta, "transitions")
    previous, last_date, verified_at = "draft", dates["created_at"], None
    approvals, history_warnings = {}, []
    for number, event in enumerate(events):
        base_keys = {"from", "to", "actor", "at", "reason", "approval"}
        if (not isinstance(event, dict) or not base_keys <= event.keys()
                or set(event) - base_keys not in (set(), {"approval_policy"}, {"approval_policy", "approval_content_hash"})
                or event["from"] != previous or not isinstance(event["reason"], str) or not event["reason"].strip()
                or not isinstance(event["at"], str) or not iso_date(event["at"])
                or not last_date <= event["at"] <= dates["updated_at"]):
            raise GovernanceError("INVALID_TRANSITION_HISTORY")
        check_transition(previous, event["to"], event["actor"])
        if event["to"] == "verified":
            if kind in {"interpretation", "hypothesis", "proposed_decision"}:
                raise GovernanceError("KIND_CANNOT_BE_VERIFIED")
            if not isinstance(event["approval"], str) or not event["approval"]:
                raise GovernanceError("HUMAN_APPROVAL_REQUIRED")
            verified_at = event["at"]
        if approval_required(event):
            approvals[number] = validate_event_approval(root, page, text, event, events[:number], today=today)
            if approvals[number]["policy"] == "1" and approvals[number]["content_hash"] != content_hash(text):
                history_warnings.append("LEGACY_APPROVAL_SNAPSHOT_UNAVAILABLE")
        previous, last_date = event["to"], event["at"]
    if previous != state:
        raise GovernanceError("UNTRACED_STATE")
    if (events and (events[-1]["from"], events[-1]["to"]) == ("disputed", "unverified")
            and unresolved):
        raise GovernanceError("UNRESOLVED_CONFLICT")
    if state == "verified" or state in {"superseded", "archived"} and verified_at:
        if dates["reviewed_at"] != verified_at:
            raise GovernanceError("REVIEW_DATE_REQUIRED")
        index = max(i for i, event in enumerate(events) if event["to"] == "verified")
        validate_event_approval(root, page, text, events[index], events[:index], bind_current=True, today=today)
    freshness = []
    now = (today or date.today()).isoformat()
    if unresolved:
        freshness.append("UNRESOLVED_CONFLICT")
    if dates["review_after"] and dates["review_after"] < now:
        freshness.append("REVIEW_DUE")
    elif meta["temporal"] in {"current", "time_sensitive"} and not dates["review_after"]:
        freshness.append("REVIEW_DATE_UNSET")
    if dates["effective_at"] and dates["effective_at"] > now:
        freshness.append("NOT_YET_EFFECTIVE")
    # Historical approvals are evaluated at their event date; current authority
    # additionally loses eligibility after explicit revocation/expiration.
    if state == "verified" and verified_at:
        index = max(i for i, event in enumerate(events) if event["to"] == "verified")
        freshness.extend(approvals[index]["current_flags"])
    authority = None
    if kind.endswith("decision"):
        authority = ("historical" if verified_at and (state in {"superseded", "archived"}
                                                       or kind == "historical_decision" and state == "verified")
                     else "approved" if kind == "approved_decision" and state == "verified"
                     else "proposed" if kind == "proposed_decision" else "unapproved")
    return dict(legacy=False, status=state, kind=kind, scope=scope, access=access,
                cross_project_refs=refs, conflicts=conflicts, superseded_by=successor,
                temporal=meta["temporal"], freshness=freshness, decision_authority=authority,
                history_warnings=sorted(set(history_warnings)), **dates)


def validate_wiki_update(root, page, before, after):
    """Normal synthesis may edit drafts; lifecycle/history and evidence need explicit review."""
    if before is None:
        record = read_page(root, page, after.decode("utf-8-sig"))
        if not record["legacy"] and (record["status"] != "draft"
                                    or array(metadata(after.decode("utf-8-sig")), "transitions")):
            raise GovernanceError("LIFECYCLE_CREATION_REQUIRES_DRAFT")
        return
    if before == after:
        return
    old_text, new_text = before.decode("utf-8-sig"), after.decode("utf-8-sig")
    old, new = read_page(root, page, old_text), read_page(root, page, new_text)
    if old["status"] != "draft":
        raise GovernanceError("PROTECTED_KNOWLEDGE_UPDATE")
    old_meta, new_meta = metadata(old_text), metadata(new_text)
    if (new["status"] != "draft" or old["scope"] != new["scope"]
            or not old["legacy"] and any(old_meta.get(key) != new_meta.get(key) for key in
                ("kind", "created_at", "transitions", "reviewed_at", "effective_at", "superseded_by", "access"))
            or old_meta.get("page_id") and old_meta["page_id"] != new_meta.get("page_id")):
        raise GovernanceError("LIFECYCLE_CHANGE_REQUIRES_TRANSITION")
    old_ids = set(SOURCE_TOKEN.findall(old_meta.get("source ids", "")))
    if not old_ids <= set(SOURCE_TOKEN.findall(new_meta.get("source ids", ""))):
        raise GovernanceError("EVIDENCE_REMOVAL_REQUIRES_REVIEW")
    def pointers(text):
        return {(sid, source_pointer(block, sid)) for block in findings(prose(text))
                for sid in SOURCE_TOKEN.findall(block)}
    if not pointers(old_text) <= pointers(new_text):
        raise GovernanceError("EVIDENCE_REMOVAL_REQUIRES_REVIEW")
    if any(item not in new["conflicts"] for item in old["conflicts"]):
        raise GovernanceError("CONFLICT_REMOVAL_REQUIRES_REVIEW")


def validate_lifecycle_update(root, page, before, after):
    """A lifecycle write appends one event; it cannot rewrite content or reset history."""
    if before is None:
        raise GovernanceError("INVALID_LIFECYCLE_UPDATE")
    old_text, new_text = before.decode("utf-8-sig"), after.decode("utf-8-sig")
    old = read_page(root, page, old_text)
    old_events, new_events = array(metadata(old_text), "transitions"), array(metadata(new_text), "transitions")
    if (old["legacy"] or len(new_events) != len(old_events) + 1 or new_events[:-1] != old_events
            or new_events[-1].get("from") != old["status"] or content_hash(old_text) != content_hash(new_text)):
        raise GovernanceError("INVALID_LIFECYCLE_UPDATE")
    read_page(root, page, new_text)
    validate_event_approval(root, page, new_text, new_events[-1], old_events,
                            write=True, bind_current=True)


def replace_field(text, name, value):
    lines = text.splitlines()
    for number, line in enumerate(lines):
        match = FIELD.match(line)
        if match and match[1].lower() == name.lower():
            lines[number] = f"- **{name}:** {value}"
            return "\n".join(lines) + "\n"
        if re.match(r"^#{2,6}\s", line):
            lines.insert(number, f"- **{name}:** {value}")
            return "\n".join(lines) + "\n"
    raise GovernanceError("MISSING_CONTENT_SECTION")


def transition(root, relative, target, *, actor, at, reason, authorized=False,
               approval_ref=None, superseded_by=None, apply=False):
    """Return a reviewable proposed text; apply only with scoped authorization."""
    root = Path(root).absolute()
    page = document_path(root, relative)
    original = page.read_bytes()
    text = original.decode("utf-8-sig")
    current = read_page(root, page, text)
    if current["legacy"]:
        raise GovernanceError("EXPLICIT_METADATA_MIGRATION_REQUIRED")
    check_transition(current["status"], target, actor)
    if not iso_date(at) or not reason.strip():
        raise GovernanceError("TRANSITION_REASON_DATE_REQUIRED")
    events = array(metadata(text), "transitions")
    event = {"from": current["status"], "to": target, "actor": actor, "at": at,
             "reason": reason, "approval": approval_ref}
    if approval_required(event):
        event.update(approval_policy=2, approval_content_hash=content_hash(text))
        validate_event_approval(root, page, text, event, events, write=True, bind_current=True)
    events.append(event)
    changes = {"status": target, "updated_at": at,
               "transitions": json.dumps(events, ensure_ascii=False)}
    if target == "verified":
        changes["reviewed_at"] = at
    if superseded_by is not None:
        changes["superseded_by"] = superseded_by
    proposed = text
    for key, value in changes.items():
        proposed = replace_field(proposed, key, value)
    read_page(root, page, proposed)
    if apply:
        if not authorized:
            raise PermissionError("MAINTENANCE_AUTHORIZATION_REQUIRED")
        if __package__:
            from .safe_operations import transact, digest
        else:
            from safe_operations import transact, digest
        transact(root, {relative: proposed.encode("utf-8")}, {relative: digest(original)},
                 operation="lifecycle", authorized=True)
    return proposed


def audit_governance(root, today=None):
    root = Path(root).absolute()
    results, issues = {}, []
    if __package__:
        from .source_integrity import read_registry
    else:
        from source_integrity import read_registry
    try:
        registered_ids = frozenset(read_registry(root))
    except (ValueError, OSError, UnicodeError, csv.Error):
        registered_ids = None  # Preserve per-page error handling on invalid registries.
    for folder in ("wiki", "decisions"):
        base = local_path(root, root, folder)
        if not base.is_dir():
            continue
        def visit(directory):
            for child in sorted(directory.iterdir()):
                try:
                    path = local_path(root, root, child.relative_to(root).as_posix())
                except (ValueError, OSError):
                    continue
                if path.is_dir():
                    yield from visit(path)
                elif path.suffix == ".md" and path.name not in {"index.md", "log.md"}:
                    yield path
        for page in visit(base):
            relative = page.relative_to(root).as_posix()
            try:
                record = read_page(root, page, today=today, _registered_ids=registered_ids)
                results[relative] = record
                if not record["legacy"]:
                    for flag in record["freshness"]:
                        issues.append(f"WARNING {flag} {relative}: review required; no automatic state change.")
                    for flag in record.get("history_warnings", []):
                        issues.append(f"WARNING {flag} {relative}: preserve legacy history; review its unavailable snapshot.")
            except (ValueError, OSError, UnicodeError, csv.Error) as error:
                code = str(error) if isinstance(error, GovernanceError) else "GOVERNANCE_READ"
                issues.append(f"ERROR {code} {relative}: invalid governance metadata or authority.")
    return {"pages": results, "issues": issues}
