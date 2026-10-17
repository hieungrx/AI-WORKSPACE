"""Bounded local writes with optimistic versions, ownership and recoverable snapshots."""
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import time
import uuid

if __package__:
    from .check_workspace import local_path, linked_path
    from .workspace_security import SecurityError, secret_codes
else:
    from check_workspace import local_path, linked_path
    from workspace_security import SecurityError, secret_codes

RUNTIME = "recovery"
REGISTRY = {"sources/manifest.csv", "sources/provenance.jsonl"}
POLICY_NAMES = {"agents.md", "schema.md", "security.md", "security_policy.md", "claude.md", "gemini.md"}


def digest(data):
    return None if data is None else hashlib.sha256(data).hexdigest()


def _root(root):
    root = Path(root).absolute()
    if linked_path(root):
        raise SecurityError("LINKED_ROOT")
    return root


def _runtime(root, name):
    return local_path(root, root, RUNTIME + "/" + name)


def ensure_idle(root):
    root = _root(root)
    if _runtime(root, "active.json").exists() or _runtime(root, "owner.lock").exists():
        raise SecurityError("RECOVERY_REQUIRED")


def read_version(root):
    """A reader must see the same operation generation at both boundaries."""
    root = _root(root)
    ensure_idle(root)
    path = _runtime(root, "generation")
    value = path.read_bytes() if path.exists() else None
    if value is not None and not re.fullmatch(rb"[0-9a-f]{32}", value):
        raise SecurityError("RECOVERY_REQUIRED")
    return value


def allowed_path(root, relative, operation):
    if not isinstance(relative, str) or "%" in relative or ".." in relative.replace("\\", "/").split("/"):
        raise SecurityError("WRITE_DENIED")
    path = local_path(root, root, relative)
    if path.name.casefold() in POLICY_NAMES:
        raise SecurityError("POLICY_WRITE_DENIED")
    rel = path.relative_to(root).as_posix()
    if operation == "wiki":
        allowed = path.is_relative_to(root / "wiki") and path.suffix == ".md"
    elif operation == "lifecycle":
        allowed = (any(path.is_relative_to(root / folder) for folder in ("wiki", "decisions"))
                   and path.suffix == ".md" and path.name not in {"index.md", "log.md"})
    elif operation == "registry":
        allowed = rel in REGISTRY
    elif operation == "report":
        allowed = path.is_relative_to(root / "reports") and path.suffix in {".md", ".json"}
    else:
        allowed = False
    if not allowed:
        raise SecurityError("WRITE_DENIED")
    return path


def versions(root, paths, operation="wiki"):
    root = _root(root)
    result = {}
    for relative in paths:
        path = allowed_path(root, relative, operation)
        result[relative] = digest(path.read_bytes()) if path.exists() else None
    return result


def _sync(path, data):
    with path.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def _replace_file(staged, target):
    original = digest(target.read_bytes()) if target.exists() else None
    for attempt in range(4):
        try:
            os.replace(staged, target)
            return
        except PermissionError as error:
            if os.name != "nt" or getattr(error, "winerror", None) not in {5, 32, 33} or attempt == 3:
                raise
            time.sleep(0.02 * (2 ** attempt))
            current = digest(target.read_bytes()) if target.exists() else None
            if current != original:
                raise SecurityError("CONCURRENT_CHANGE") from None


@contextmanager
def ownership(root):
    folder = _runtime(root, "owner.lock").parent
    folder.mkdir(parents=True, exist_ok=True)
    lock = _runtime(root, "owner.lock")
    owner = uuid.uuid4().hex.encode("ascii")
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.write(descriptor, owner)
        os.fsync(descriptor)
        yield
    finally:
        os.close(descriptor)
        # Never remove a lock replaced by an unrelated owner.
        if lock.is_file() and lock.read_bytes() == owner:
            lock.unlink()


def _journal(root, record):
    temporary = _runtime(root, uuid.uuid4().hex + ".journal")
    _sync(temporary, (json.dumps(record, sort_keys=True) + "\n").encode("utf-8"))
    _replace_file(temporary, _runtime(root, "active.json"))


def _load(root):
    path = _runtime(root, "active.json")
    if path.stat().st_size > 1024 * 1024:
        raise SecurityError("INVALID_RECOVERY_RECORD")
    try:
        def unique(pairs):
            values = {}
            for key, value in pairs:
                if key in values:
                    raise SecurityError("INVALID_RECOVERY_RECORD")
                values[key] = value
            return values
        record = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)
        if (set(record) != {"id", "operation", "status", "files"}
                or not re.fullmatch(r"[0-9a-f]{32}", record["id"])
                or record["status"] not in {"prepared", "committed"}
                or not isinstance(record["files"], list) or not 1 <= len(record["files"]) <= 64):
            raise ValueError()
        seen = set()
        for item in record["files"]:
            if set(item) != {"path", "before", "after"}:
                raise ValueError()
            path = allowed_path(root, item["path"], record["operation"])
            canonical = str(path).casefold()
            if canonical in seen:
                raise ValueError()
            seen.add(canonical)
            for key in ("before", "after"):
                value = item[key]
                if not (key == "before" and value is None) and not (
                        isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value)):
                    raise ValueError()
        return record
    except (ValueError, TypeError, KeyError):
        raise SecurityError("INVALID_RECOVERY_RECORD") from None


def _finish(root, record, status):
    record["status"] = status
    receipt = _runtime(root, record["id"] + "/receipt.json")
    staged = _runtime(root, record["id"] + "/" + uuid.uuid4().hex + ".receipt")
    _sync(staged, (json.dumps(record, sort_keys=True) + "\n").encode("utf-8"))
    _replace_file(staged, receipt)
    generation = _runtime(root, record["id"] + "/" + uuid.uuid4().hex + ".generation")
    _sync(generation, record["id"].encode("ascii"))
    _replace_file(generation, _runtime(root, "generation"))
    _runtime(root, "active.json").unlink()
    return {"status": status.upper(), "operation_id": record["id"], "files": len(record["files"])}


def _restore(root, record):
    # Preflight ALL resources and snapshots before touching even the first target.
    snapshots = []
    for number, item in enumerate(record["files"]):
        target = allowed_path(root, item["path"], record["operation"])
        current = target.read_bytes() if target.exists() else None
        if digest(current) not in {item["before"], item["after"]}:
            raise SecurityError("RECOVERY_CONFLICT")
        backup = _runtime(root, record["id"] + f"/{number}.before")
        data = backup.read_bytes() if item["before"] is not None else None
        if digest(data) != item["before"]:
            raise SecurityError("BACKUP_MISMATCH")
        snapshots.append((target, current, data))
    for number, (target, current, data) in enumerate(snapshots):
        if current == data:
            continue
        if (target.read_bytes() if target.exists() else None) != current:
            raise SecurityError("RECOVERY_CONFLICT")
        if data is None:
            # Only remove a new file whose complete bytes still match this operation.
            if digest(target.read_bytes()) != record["files"][number]["after"]:
                raise SecurityError("RECOVERY_CONFLICT")
            target.unlink()
        else:
            staged = _runtime(root, record["id"] + "/" + uuid.uuid4().hex + ".restore")
            _sync(staged, data)
            _replace_file(staged, target)
    return _finish(root, record, "rolled_back")


def transact(root, changes, expected, *, operation="wiki", authorized=False):
    """Every target needs its reviewed version; no inferred write/delete/command."""
    if not authorized:
        raise PermissionError("MAINTENANCE_AUTHORIZATION_REQUIRED")
    root = _root(root)
    if (not isinstance(changes, dict) or not changes or len(changes) > 64
            or not isinstance(expected, dict) or set(changes) != set(expected)):
        raise SecurityError("INVALID_WRITE_PLAN")
    ensure_idle(root)
    with ownership(root):
        if _runtime(root, "active.json").exists():
            raise SecurityError("RECOVERY_REQUIRED")
        records, bodies, seen = [], [], set()
        for relative, after in changes.items():
            target = allowed_path(root, relative, operation)
            canonical = str(target).casefold()
            if canonical in seen or not isinstance(after, bytes) or len(after) > 4 * 1024 * 1024:
                raise SecurityError("INVALID_WRITE_PLAN")
            seen.add(canonical)
            before = target.read_bytes() if target.exists() else None
            if digest(before) != expected[relative]:
                if operation == "report" and expected[relative] is None:
                    raise FileExistsError("REPORT_EXISTS")
                raise SecurityError("CONCURRENT_CHANGE")
            if operation == "registry" or relative.replace("\\", "/") == "wiki/log.md":
                if before is not None and not after.startswith(before):
                    raise SecurityError("APPEND_ONLY")
            if operation == "report" and before is not None:
                raise FileExistsError("REPORT_EXISTS")
            if secret_codes(after.decode("utf-8", errors="ignore")) or (
                    before and secret_codes(before.decode("utf-8", errors="ignore"))):
                raise SecurityError("SENSITIVE_CONTENT")
            records.append({"path": relative, "before": digest(before), "after": digest(after)})
            bodies.append((before, after, target))
        if operation in {"wiki", "lifecycle"}:
            if __package__:
                from .knowledge_governance import read_page
                from .check_workspace import LINK, link_path, prose
                from .workspace_security import require_safe_data
            else:
                from knowledge_governance import read_page
                from check_workspace import LINK, link_path, prose
                from workspace_security import require_safe_data
            destinations = {target for _, _, target in bodies}
            for _, after, target in bodies:
                text = after.decode("utf-8-sig")
                require_safe_data(text)
                if target.name not in {"index.md", "log.md"}:
                    governed = read_page(root, target, text)
                    if governed["legacy"] and governed["kind"].endswith("decision"):
                        raise SecurityError("LEGACY_DECISION_MIGRATION_REQUIRED")
                for match in LINK.finditer(prose(text)):
                    linked = link_path(root, target, match[1])
                    if linked is not None and not linked.exists() and linked not in destinations:
                        raise SecurityError("BROKEN_PROPOSED_LINK")
        record = {"id": uuid.uuid4().hex, "operation": operation, "status": "prepared", "files": records}
        job = _runtime(root, record["id"])
        job.mkdir()
        for number, (before, after, _) in enumerate(bodies):
            if before is not None:
                _sync(job / f"{number}.before", before)
            _sync(job / f"{number}.after", after)
        _journal(root, record)
        try:
            for number, (_, _, target) in enumerate(bodies):
                # Recheck immediately before replacement as well as under ownership.
                existing = target.read_bytes() if target.exists() else None
                if digest(existing) != records[number]["before"]:
                    raise SecurityError("CONCURRENT_CHANGE")
                target.parent.mkdir(parents=True, exist_ok=True)
                _replace_file(job / f"{number}.after", target)
            record["status"] = "committed"
            _journal(root, record)
        except Exception:
            _restore(root, record)
            raise
        return _finish(root, record, "committed")


def recover(root, *, authorized=False, acknowledge_stale_lock=False):
    if not authorized:
        raise PermissionError("RECOVERY_AUTHORIZATION_REQUIRED")
    root = _root(root)
    lock = _runtime(root, "owner.lock")
    if lock.exists():
        if not acknowledge_stale_lock:
            raise SecurityError("OWNER_REVIEW_REQUIRED")
        # This acknowledgement must come from the human after verifying the owner stopped.
        if not re.fullmatch(rb"[0-9a-f]{32}", lock.read_bytes()):
            raise SecurityError("INVALID_OWNER")
        lock.unlink()
    with ownership(root):
        if not _runtime(root, "active.json").exists():
            return {"status": "NOTHING_TO_RECOVER"}
        record = _load(root)
        if record["status"] == "committed":
            for item in record["files"]:
                target = allowed_path(root, item["path"], record["operation"])
                if not target.exists() or digest(target.read_bytes()) != item["after"]:
                    raise SecurityError("RECOVERY_CONFLICT")
            return _finish(root, record, "committed")
        return _restore(root, record)


def atomic_snapshot(root, relative, data):
    """Publish a complete NEW raw snapshot exclusively; never replace raw."""
    root = _root(root)
    target = local_path(root, root, relative)
    if target.name.casefold() in POLICY_NAMES:
        raise SecurityError("POLICY_WRITE_DENIED")
    if not target.is_relative_to(root / "sources/raw"):
        raise SecurityError("WRITE_DENIED")
    if secret_codes(data.decode("utf-8", errors="ignore")):
        raise SecurityError("SENSITIVE_CONTENT")
    target.parent.mkdir(parents=True, exist_ok=True)
    ensure_idle(root)
    with ownership(root):
        staged = _runtime(root, uuid.uuid4().hex + ".snapshot")
        try:
            _sync(staged, data)
            if os.name == "nt":
                os.rename(staged, target)  # Windows rename refuses an existing destination.
            else:
                os.link(staged, target)  # POSIX rename would overwrite; link is exclusive.
        finally:
            if staged.exists():
                staged.unlink()


def save_reports(root, report, output, renderer):
    if __package__:
        from .workspace_security import redact
    else:
        from workspace_security import redact
    root = _root(root)
    path = allowed_path(root, str(output), "report")
    if path.suffix != ".json":
        raise ValueError("REPORT_JSON_REQUIRED")
    companion = path.with_suffix(".md")
    if path.exists() or companion.exists():
        raise FileExistsError("REPORT_EXISTS")
    safe = redact(report)
    changes = {
        path.relative_to(root).as_posix(): (json.dumps(safe, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
        companion.relative_to(root).as_posix(): redact(renderer(safe)).encode("utf-8"),
    }
    return transact(root, changes, {key: None for key in changes}, operation="report", authorized=True)
