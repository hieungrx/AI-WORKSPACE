#!/usr/bin/env python3
"""Phase 1: append-only provenance, immutable snapshots and offline integrity."""
from contextlib import contextmanager
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
from urllib.parse import urlsplit

if __package__:
    from .safe_operations import atomic_snapshot, digest, transact, versions
else:
    from safe_operations import atomic_snapshot, digest, transact, versions

if __package__:
    from .check_workspace import (
        MANIFEST_FIELDS, REQUIRED_FIELDS, SOURCE_TOKEN, findings, iso_date,
        linked_path, local_path, prose, source_id,
    )
else:
    from check_workspace import (
        MANIFEST_FIELDS, REQUIRED_FIELDS, SOURCE_TOKEN, findings, iso_date,
        linked_path, local_path, prose, source_id,
    )

LEDGER = "sources/provenance.jsonl"
FIELDS = {
    "source_id", "source_uri", "local_path", "content_hash", "manifest_hash", "language", "publisher",
    "verification_status", "verification_note", "source_version", "replaces",
    "original_uri_status", "original_uri_checked_at",
}


class IntegrityError(ValueError):
    """The message is a stable error code, never raw source contents."""


def _root(root):
    root = Path(root).absolute()
    if linked_path(root):
        raise IntegrityError("LINKED_ROOT")
    return root


def _row(row):
    if set(row) != set(MANIFEST_FIELDS) or any(not isinstance(v, str) for v in row.values()):
        raise IntegrityError("MANIFEST_ROW")
    row = {key: value.strip() for key, value in row.items()}
    if any(not row[key] for key in REQUIRED_FIELDS):
        raise IntegrityError("MISSING_SOURCE_VALUE")
    if not source_id(row["source_id"]):
        raise IntegrityError("INVALID_SOURCE_ID")
    if any(row[key] and not iso_date(row[key]) for key in ("published_date", "retrieved_date")):
        raise IntegrityError("INVALID_SOURCE_DATE")
    return row


def read_registry(root):
    path = local_path(root, root, "sources/manifest.csv")
    rows = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        if reader.fieldnames != list(MANIFEST_FIELDS):
            raise IntegrityError("MANIFEST_HEADER")
        for values in reader:
            row = _row(values)
            sid = row["source_id"]
            if sid in rows:
                raise IntegrityError("DUPLICATE_SOURCE_ID")
            rows[sid] = row
    return rows


def _provenance(entry):
    if not isinstance(entry, dict) or set(entry) != FIELDS:
        raise IntegrityError("PROVENANCE_FIELDS")
    if not isinstance(entry["source_id"], str) or not source_id(entry["source_id"]):
        raise IntegrityError("INVALID_SOURCE_ID")
    for key in ("content_hash", "manifest_hash"):
        if not isinstance(entry[key], str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", entry[key]):
            raise IntegrityError("INVALID_" + key.upper())
    if not isinstance(entry["local_path"], str) or not entry["local_path"]:
        raise IntegrityError("MISSING_LOCAL_SNAPSHOT")
    if entry["language"] not in ("en", "vi", "mul", "und"):
        raise IntegrityError("INVALID_SOURCE_LANGUAGE")
    if type(entry["source_version"]) is not int or entry["source_version"] < 1:
        raise IntegrityError("INVALID_SOURCE_VERSION")
    for key in ("source_uri", "publisher", "verification_note"):
        if entry[key] is not None and (not isinstance(entry[key], str) or not entry[key].strip()):
            raise IntegrityError("INVALID_PROVENANCE_VALUE")
    predecessor = entry["replaces"]
    if predecessor is not None and (not isinstance(predecessor, str) or not source_id(predecessor)):
        raise IntegrityError("INVALID_REPLACEMENT")
    status = entry["verification_status"]
    if status not in ("UNVERIFIED", "VERIFIED", "DISPUTED"):
        raise IntegrityError("INVALID_VERIFICATION_STATUS")
    if status != "UNVERIFIED" and not entry["verification_note"]:
        raise IntegrityError("VERIFICATION_NOTE_REQUIRED")
    uri_status = entry["original_uri_status"]
    checked = entry["original_uri_checked_at"]
    if uri_status not in ("UNKNOWN", "AVAILABLE", "UNAVAILABLE"):
        raise IntegrityError("INVALID_URI_STATUS")
    if uri_status == "UNKNOWN":
        if checked is not None:
            raise IntegrityError("UNKNOWN_URI_CHECK_DATE")
    elif not entry["source_uri"] or not isinstance(checked, str) or not iso_date(checked):
        raise IntegrityError("URI_CHECK_METADATA_REQUIRED")
    return entry


def read_provenance(root):
    path = local_path(root, root, LEDGER)
    if not path.exists():
        return {}
    entries = {}
    with path.open(encoding="utf-8-sig") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                def unique_fields(pairs):
                    values = {}
                    for key, value in pairs:
                        if key in values:
                            raise IntegrityError("DUPLICATE_PROVENANCE_FIELD")
                        values[key] = value
                    return values
                entry = _provenance(json.loads(line, object_pairs_hook=unique_fields))
            except (TypeError, ValueError) as error:
                if isinstance(error, IntegrityError):
                    raise
                raise IntegrityError("PROVENANCE_FORMAT") from None
            sid = entry["source_id"]
            if sid in entries:
                raise IntegrityError("DUPLICATE_PROVENANCE_ID")
            entries[sid] = entry
    return entries


def raw_path(root, location):
    path = local_path(root, root, location)
    if not path.is_relative_to(root / "sources/raw") or path == root / "sources/raw":
        raise IntegrityError("OUTSIDE_RAW")
    return path


def content_hash(root, location):
    path = raw_path(root, location)
    if not path.is_file():
        raise IntegrityError("MISSING_RAW_SOURCE")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        before = os.fstat(handle.fileno())
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
        after = os.fstat(handle.fileno())
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise IntegrityError("SOURCE_CHANGED_DURING_HASH")
    return "sha256:" + digest.hexdigest()


def manifest_hash(row):
    data = json.dumps(_row(row), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical(row, entry=None):
    entry = entry or {}
    location = row["source_url_or_path"]
    parsed = urlsplit(location)
    remote = parsed.scheme.lower() in ("http", "https") and bool(parsed.netloc)
    if entry:
        if entry["manifest_hash"] != manifest_hash(row):
            raise IntegrityError("MANIFEST_HASH_MISMATCH")
        if remote and entry["source_uri"] != location:
            raise IntegrityError("ORIGINAL_URI_MISMATCH")
        if not remote and entry["local_path"] != location:
            raise IntegrityError("SOURCE_LOCATION_MISMATCH")
    return {
        "source_id": row["source_id"], "source_type": row["source_type"], "title": row["title"],
        "author": row["author"] or None, "publisher": entry.get("publisher"),
        "published_at": row["published_date"] or None, "retrieved_at": row["retrieved_date"],
        "source_uri": entry.get("source_uri", location if remote else None),
        "local_path": entry.get("local_path", None if remote else location),
        "content_hash": entry.get("content_hash"), "manifest_hash": entry.get("manifest_hash"),
        "language": entry.get("language", "und"),
        "verification_status": entry.get("verification_status", "UNVERIFIED"),
        "verification_note": entry.get("verification_note"),
        "source_version": entry.get("source_version"), "replaces": entry.get("replaces"),
        "original_uri_status": entry.get("original_uri_status", "UNKNOWN"),
        "original_uri_checked_at": entry.get("original_uri_checked_at"),
    }


def wiki_relationships(root):
    usage = {}
    claims = []
    wiki = local_path(root, root, "wiki")

    def visit(folder):
        if not folder.is_dir():
            return
        for child in sorted(folder.iterdir()):
            try:
                child = local_path(root, root, child.relative_to(root).as_posix())
            except (ValueError, OSError):
                continue
            if child.is_dir():
                visit(child)
            elif child.suffix.lower() == ".md":
                text = prose(child.read_text(encoding="utf-8-sig"))
                relative = child.relative_to(root).as_posix()
                for sid in sorted(set(SOURCE_TOKEN.findall(text))):
                    usage.setdefault(sid, []).append(relative)
                for number, block in enumerate(findings(text), 1):
                    claims.append({"wiki_path": relative, "finding": number,
                                   "source_ids": sorted(set(SOURCE_TOKEN.findall(block)))})

    visit(wiki)
    return usage, claims


def audit_sources(root, require_complete=True, verify_hashes=True, *, _new_rows=(), _new_entries=()):
    root = _root(root)
    result = {"issues": [], "sources": {}, "source_to_wiki": {}, "claims": []}

    def issue(level, code, sid="registry"):
        result["issues"].append(f"{level} {code} {LEDGER}: {sid}.")

    try:
        rows = read_registry(root)
        ledger = read_provenance(root)
        for row in _new_rows:
            row = _row(row)
            if row["source_id"] in rows:
                raise IntegrityError("DUPLICATE_SOURCE_ID")
            rows[row["source_id"]] = row
        for entry in _new_entries:
            _provenance(entry)
            if entry["source_id"] in ledger:
                raise IntegrityError("DUPLICATE_PROVENANCE_ID")
            ledger[entry["source_id"]] = entry
    except (ValueError, OSError, UnicodeError, csv.Error) as error:
        issue("ERROR", str(error) if isinstance(error, IntegrityError) else "REGISTRY_READ")
        return result
    for sid in ledger.keys() - rows.keys():
        issue("ERROR", "ORPHAN_PROVENANCE", sid)
    digests = {}
    parents = {}
    for sid, row in rows.items():
        entry = ledger.get(sid)
        try:
            record = canonical(row, entry)
        except ValueError as error:
            issue("ERROR", str(error) if isinstance(error, IntegrityError) else "PROVENANCE_LOCATION_MISMATCH", sid)
            continue
        record["integrity_status"] = "LEGACY_UNHASHED" if not entry else "UNCHECKED"
        record["superseded_by"] = None
        result["sources"][sid] = record
        if not entry and require_complete:
            issue("ERROR", "MISSING_PROVENANCE", sid)
        location = record["local_path"]
        if not location:
            record["integrity_status"] = "MISSING_SNAPSHOT"
            if require_complete:
                issue("ERROR", "MISSING_LOCAL_SNAPSHOT", sid)
        else:
            try:
                target = raw_path(root, location)
                if not target.is_file():
                    raise IntegrityError("MISSING_RAW_SOURCE")
                if verify_hashes:
                    actual = content_hash(root, location)
                    digests[sid] = actual
                    if entry:
                        record["integrity_status"] = "MATCH" if actual == record["content_hash"] else "HASH_MISMATCH"
                        if actual != record["content_hash"]:
                            issue("ERROR", "HASH_MISMATCH", sid)
            except (ValueError, OSError):
                record["integrity_status"] = "UNAVAILABLE"
                issue("ERROR", "SOURCE_UNAVAILABLE", sid)
        if record["source_uri"] and record["original_uri_status"] != "AVAILABLE":
            issue("WARNING", "ORIGINAL_URI_" + record["original_uri_status"], sid)
        previous = record["replaces"]
        parents[sid] = previous
        if previous:
            if previous not in ledger or previous not in rows:
                issue("ERROR", "REPLACEMENT_SOURCE_MISSING", sid)
            elif record["source_version"] != ledger[previous]["source_version"] + 1:
                issue("ERROR", "SOURCE_VERSION_SEQUENCE", sid)
        elif entry and record["source_version"] != 1:
            issue("ERROR", "SOURCE_VERSION_SEQUENCE", sid)
    children = {}
    for sid, previous in parents.items():
        if previous:
            if previous in children:
                issue("ERROR", "BRANCHED_SOURCE_VERSION", previous)
            children[previous] = sid
            if previous in result["sources"]:
                result["sources"][previous]["superseded_by"] = sid

    def lineage(sid):
        seen = set()
        while sid:
            if sid in seen:
                issue("ERROR", "SOURCE_VERSION_CYCLE", sid)
                return None
            seen.add(sid)
            previous = parents.get(sid)
            if not previous:
                return sid
            sid = previous

    identities = {sid: lineage(sid) for sid in rows}
    seen_hashes = {}
    seen_uris = {}
    for sid, record in result["sources"].items():
        digest = digests.get(sid) if verify_hashes else record["content_hash"]
        if digest:
            previous = seen_hashes.setdefault(digest, sid)
            if previous != sid and identities.get(previous) != identities.get(sid):
                issue("ERROR", "DUPLICATE_CONTENT", sid)
        uri = record["source_uri"]
        if uri:
            previous = seen_uris.setdefault(uri, sid)
            if previous != sid and identities.get(previous) != identities.get(sid):
                issue("ERROR", "UNLINKED_SOURCE_REVISION", sid)
    try:
        usage, claims = wiki_relationships(root)
        result["source_to_wiki"], result["claims"] = usage, claims
        for sid in usage.keys() - rows.keys():
            issue("ERROR", "UNKNOWN_SOURCE_REFERENCE", sid)
        for sid in usage.keys() & result["sources"].keys():
            if result["sources"][sid]["superseded_by"]:
                issue("WARNING", "SUPERSEDED_SOURCE_REFERENCE", sid)
    except (ValueError, OSError, UnicodeError):
        issue("ERROR", "SOURCE_REFERENCE_READ")
    return result


def _entry(root, row, *, source_uri=None, local_snapshot=None, language="und",
           publisher=None, verification_status="UNVERIFIED", verification_note=None,
           source_version=1, replaces=None, original_uri_status="UNKNOWN",
           original_uri_checked_at=None):
    location = row["source_url_or_path"]
    parsed = urlsplit(location)
    remote = parsed.scheme.lower() in ("http", "https") and bool(parsed.netloc)
    snapshot = local_snapshot or (None if remote else location)
    if not snapshot:
        raise IntegrityError("MISSING_LOCAL_SNAPSHOT")
    entry = {
        "source_id": row["source_id"], "source_uri": source_uri or (location if remote else None),
        "local_path": snapshot, "content_hash": content_hash(root, snapshot),
        "manifest_hash": manifest_hash(row), "language": language,
        "publisher": publisher, "verification_status": verification_status,
        "verification_note": verification_note, "source_version": source_version, "replaces": replaces,
        "original_uri_status": original_uri_status, "original_uri_checked_at": original_uri_checked_at,
    }
    _provenance(entry)
    canonical(row, entry)
    return entry


@contextmanager
def _registration_lock(root, authorized):
    if not authorized:
        raise PermissionError("SOURCE_AUTHORIZATION_REQUIRED")
    root = _root(root)
    lock = local_path(root, root, "sources/registration.lock")
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        yield
    finally:
        os.close(descriptor)
        lock.unlink()  # Only the exclusive lock created by this operation.


def _append_json(root, entries):
    path = local_path(root, root, LEDGER)
    if path.exists() and path.stat().st_size and not path.read_bytes().endswith(b"\n"):
        raise IntegrityError("PROVENANCE_FINAL_NEWLINE")
    previous = path.read_bytes() if path.exists() else b""
    data = previous + "".join(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n" for entry in entries).encode("utf-8")
    transact(root, {LEDGER: data}, {LEDGER: digest(previous) if path.exists() else None},
             operation="registry", authorized=True)


def create_raw_snapshot(root, location, data, *, authorized=False):
    if not authorized:
        raise PermissionError("SOURCE_AUTHORIZATION_REQUIRED")
    if not isinstance(data, bytes):
        raise IntegrityError("RAW_BYTES_REQUIRED")
    root = _root(root)
    path = raw_path(root, location)
    try:
        atomic_snapshot(root, location, data)
    except FileExistsError:
        raise IntegrityError("RAW_SOURCE_IMMUTABLE") from None
    return location


def register_source(root, row, *, authorized=False, **metadata_values):
    root = _root(root)
    row = _row(row)
    with _registration_lock(root, authorized):
        expected = versions(root, ("sources/manifest.csv", LEDGER), operation="registry")
        rows = read_registry(root)
        ledger = read_provenance(root)
        entry = _entry(root, row, **metadata_values)
        sid = row["source_id"]
        current = audit_sources(root)
        # Unknown wiki IDs may be resolved by this very registration.
        fatal = [i for i in current["issues"] if i.startswith("ERROR ") and " UNKNOWN_SOURCE_REFERENCE " not in i]
        if fatal:
            raise IntegrityError("EXISTING_INTEGRITY_ERRORS")
        if sid in rows:
            if row == rows[sid] and entry == ledger.get(sid):
                return {"status": "DUPLICATE", "source_id": sid}
            raise IntegrityError("SOURCE_ID_CONFLICT")
        previous = entry["replaces"]
        if not previous and entry["source_version"] != 1:
            raise IntegrityError("SOURCE_VERSION_SEQUENCE")
        for old_id, old in ledger.items():
            if old["content_hash"] == entry["content_hash"] and not previous:
                return {"status": "DUPLICATE", "source_id": old_id}
            if entry["source_uri"] and old["source_uri"] == entry["source_uri"] and not previous:
                raise IntegrityError("SOURCE_REVISION_REQUIRED")
        proposed = audit_sources(root, _new_rows=[row], _new_entries=[entry])
        fatal = [i for i in proposed["issues"] if i.startswith("ERROR ") and " UNKNOWN_SOURCE_REFERENCE " not in i]
        if fatal:
            raise IntegrityError(fatal[0].split()[1])
        text = io.StringIO(newline="")
        writer = csv.DictWriter(text, fieldnames=MANIFEST_FIELDS, lineterminator="\n")
        writer.writerow(row)
        manifest = local_path(root, root, "sources/manifest.csv")
        if not manifest.read_bytes().endswith(b"\n"):
            raise IntegrityError("MANIFEST_FINAL_NEWLINE")
        if content_hash(root, entry["local_path"]) != entry["content_hash"]:
            raise IntegrityError("SOURCE_CHANGED_BEFORE_REGISTRATION")
        ledger_path = local_path(root, root, LEDGER)
        prior_ledger = ledger_path.read_bytes() if ledger_path.exists() else b""
        if prior_ledger and not prior_ledger.endswith(b"\n"):
            raise IntegrityError("PROVENANCE_FINAL_NEWLINE")
        # Logical append-only history; physical replacement is journaled and recoverable.
        transact(root, {
            LEDGER: prior_ledger + (json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8"),
            "sources/manifest.csv": manifest.read_bytes() + text.getvalue().encode("utf-8"),
        }, expected, operation="registry", authorized=True)
        return {"status": "REGISTERED", "source_id": sid}


def plan_migration(root):
    """Read-only proposal: baseline current bytes, never certify historical integrity."""
    root = _root(root)
    rows, ledger = read_registry(root), read_provenance(root)
    entries = []
    for sid, row in rows.items():
        if sid not in ledger:
            entries.append(_entry(root, row))
    return entries


def apply_migration(root, proposal, *, authorized=False):
    root = _root(root)
    with _registration_lock(root, authorized):
        if not isinstance(proposal, list) or any(not isinstance(entry, dict) for entry in proposal):
            raise IntegrityError("MIGRATION_PROPOSAL_CHANGED")
        rows, ledger = read_registry(root), read_provenance(root)
        ids = [entry.get("source_id") for entry in proposal]
        if len(set(ids)) != len(ids) or set(ids) != rows.keys() - ledger.keys():
            raise IntegrityError("MIGRATION_PROPOSAL_CHANGED")
        for entry in proposal:
            _provenance(entry)
            canonical(rows[entry["source_id"]], entry)
            if content_hash(root, entry["local_path"]) != entry["content_hash"]:
                raise IntegrityError("MIGRATION_PROPOSAL_CHANGED")
        proposed = audit_sources(root, _new_entries=proposal)
        fatal = [i for i in proposed["issues"] if i.startswith("ERROR ") and " UNKNOWN_SOURCE_REFERENCE " not in i]
        if fatal:
            raise IntegrityError(fatal[0].split()[1])
        if proposal:
            _append_json(root, proposal)
    return {"status": "MIGRATED", "sources": len(proposal)}
