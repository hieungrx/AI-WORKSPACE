"""Apply reviewed synthesis for an already admitted source; never execute source text."""
from pathlib import Path

if __package__:
    from .check_workspace import LINK, SOURCE_TOKEN, findings, link_path, metadata, prose, source_pointer, source_id as valid_id
    from .source_integrity import audit_sources
    from .knowledge_governance import read_page, validate_wiki_update
    from .safe_operations import allowed_path, ensure_idle, transact
    from .workspace_security import SecurityError, TRUST, read_data, require_safe_data
else:
    from check_workspace import LINK, SOURCE_TOKEN, findings, link_path, metadata, prose, source_pointer, source_id as valid_id
    from source_integrity import audit_sources
    from knowledge_governance import read_page, validate_wiki_update
    from safe_operations import allowed_path, ensure_idle, transact
    from workspace_security import SecurityError, TRUST, read_data, require_safe_data


def ingest_registered(root, source_id, changes, expected, *, scope, authorized=False, apply=False):
    """Task inputs are explicit arguments; source data cannot supply operations or grants."""
    if not authorized:
        raise PermissionError("SOURCE_AUTHORIZATION_REQUIRED")
    root = Path(root).absolute()
    ensure_idle(root)
    if not isinstance(source_id, str) or not valid_id(source_id) or not isinstance(scope, str) or not scope.strip():
        raise SecurityError("INVALID_INGEST_REQUEST")
    audit = audit_sources(root)
    if any(issue.startswith("ERROR ") for issue in audit["issues"]):
        raise SecurityError("SOURCE_INTEGRITY_REQUIRED")
    source = audit["sources"].get(source_id)
    if not source or source["integrity_status"] != "MATCH":
        raise SecurityError("SOURCE_INTEGRITY_REQUIRED")
    # Reads only the explicitly authorized, hash-validated snapshot; never a URL.
    data = read_data(root, source["local_path"])
    if data["content_hash"] != source["content_hash"]:
        raise SecurityError("SOURCE_CHANGED_DURING_INGEST")
    if not isinstance(changes, dict) or len(changes) < 3 or not {"wiki/index.md", "wiki/log.md"} <= changes.keys():
        raise SecurityError("INCOMPLETE_INGEST_PLAN")
    if not isinstance(expected, dict) or set(changes) != set(expected):
        raise SecurityError("INVALID_WRITE_PLAN")
    if any(not isinstance(value, bytes) for value in changes.values()):
        raise SecurityError("INVALID_WRITE_PLAN")
    index_path = allowed_path(root, "wiki/index.md", "wiki")
    index_text = changes["wiki/index.md"].decode("utf-8-sig")
    links = {link_path(root, index_path, match[1]) for match in LINK.finditer(prose(index_text))}
    old_links = {link_path(root, index_path, match[1]) for match in
                 LINK.finditer(prose(index_path.read_text(encoding="utf-8-sig")))} if index_path.exists() else set()
    if not old_links <= links:
        raise SecurityError("INDEX_REMOVAL_REQUIRES_REVIEW")
    log_path = allowed_path(root, "wiki/log.md", "wiki")
    old_log = log_path.read_bytes() if log_path.exists() else b""
    if not changes["wiki/log.md"].startswith(old_log):
        raise SecurityError("APPEND_ONLY")
    changed_content = any(relative not in {"wiki/index.md", "wiki/log.md"}
                          and (not (target := allowed_path(root, relative, "wiki")).exists()
                               or target.read_bytes() != value) for relative, value in changes.items())
    if changed_content and len(changes["wiki/log.md"]) <= len(old_log):
        raise SecurityError("MISSING_CHANGE_LOG_ENTRY")
    for relative, proposed in changes.items():
        target = allowed_path(root, relative, "wiki")
        if not isinstance(proposed, bytes):
            raise SecurityError("INVALID_WRITE_PLAN")
        text = proposed.decode("utf-8-sig")
        require_safe_data(text)
        if target.name in {"index.md", "log.md"}:
            continue
        meta = metadata(text)
        if (meta.get("status") != "draft" or meta.get("scope") != scope
                or meta.get("kind") not in {"external_fact", "interpretation", "hypothesis"}
                or source_id not in SOURCE_TOKEN.findall(meta.get("source ids", ""))):
            raise SecurityError("INGEST_DRAFT_REQUIRED")
        read_page(root, target, text)
        validate_wiki_update(root, target, target.read_bytes() if target.exists() else None, proposed)
        if target not in links:
            raise SecurityError("MISSING_INDEX_ENTRY")
        for block in findings(prose(text)):
            cited = set(SOURCE_TOKEN.findall(block))
            if not cited or not cited <= audit["sources"].keys():
                raise SecurityError("INGEST_EVIDENCE_REQUIRED")
            if any(not source_pointer(block, sid) for sid in cited):
                raise SecurityError("MISSING_CITATION_POINTER")
    result = {"status": "PROPOSED", "source_id": source_id, "input_trust": data["trust"],
              "output_trust": TRUST, "paths": sorted(changes), "source_data_executed": False}
    if apply:
        result.update(transact(root, changes, expected, operation="wiki", authorized=True, allow_unchanged=True))
    return result
