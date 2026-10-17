"""Apply reviewed synthesis for an already admitted source; never execute source text."""
import json
from pathlib import Path

if __package__:
    from .check_workspace import LINK, SOURCE_TOKEN, link_path, metadata, prose, source_id as valid_id
    from .source_integrity import audit_sources
    from .safe_operations import allowed_path, ensure_idle, transact
    from .workspace_security import SecurityError, TRUST, read_data, require_safe_data
else:
    from check_workspace import LINK, SOURCE_TOKEN, link_path, metadata, prose, source_id as valid_id
    from source_integrity import audit_sources
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
        index_text = changes["wiki/index.md"].decode("utf-8-sig")
        links = {link_path(root, root / "wiki/index.md", match[1]) for match in LINK.finditer(prose(index_text))}
        if target not in links:
            raise SecurityError("MISSING_INDEX_ENTRY")
    result = {"status": "PROPOSED", "source_id": source_id, "input_trust": data["trust"],
              "output_trust": TRUST, "paths": sorted(changes), "source_data_executed": False}
    if apply:
        result.update(transact(root, changes, expected, operation="wiki", authorized=True))
    return result
