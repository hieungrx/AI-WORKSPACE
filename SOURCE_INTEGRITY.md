# Phase 1 — Source Integrity and Provenance

First-party operating contract for the existing V1 workspace. This phase adds integrity controls, not real knowledge, a database, semantic retrieval or Phase 2.

## Discovery and compatibility

The discovery baseline was b2acfef. Existing code already checked the nine-column CSV header, ID/date validity, required values, duplicate IDs, permitted local paths, wiki source IDs, structured citations and multilingual metadata. It did not hash raw contents, deduplicate bytes, record source-version links or provide an executable admission guard.

An observed synthetic baseline probe changed raw bytes and still received FOUND from the old existence-only Query gate. Immutability in the old documentation was a policy rather than byte-integrity enforcement. No real raw source was modified in that experiment.

The existing CSV remains authoritative for its nine columns. It is not rewritten or extended. New integrity metadata lives in sources/provenance.jsonl, one immutable JSON object per registered ID. Empty ledger + empty manifest is valid. Append-only admission and migration never remove earlier provenance. Older files without this ledger retain explicitly labelled LEGACY_UNHASHED retrieval; strict integrity validation requires migration first.

## Minimal provenance contract

The normalized view joins a CSV row with its ledger record:

- source_id: unchanged SRC-YYYYMMDD-### scheme; unique, with a real date.
- source_type and title: required existing CSV values.
- source_uri: exact known original URL/location supplied by the user, or null. No redirect discovery, URL invention or inferred publisher.
- local_path: immutable snapshot inside sources/raw, relative to the workspace root. A CSV URL may coexist with this cached path in the ledger; a CSV local path must agree with it.
- author: existing CSV author or null; publisher: optional explicitly known ledger value or null.
- published_at: existing publication date or null. retrieved_at: required existing retrieval date. Existing day precision remains day precision; no fabricated time or timezone.
- content_hash: sha256: followed by 64 lowercase hexadecimal characters, over exact raw bytes. No text decoding, newline conversion or translation.
- manifest_hash: SHA-256 of the nine trimmed CSV values serialized as sorted, compact UTF-8 JSON. This binds identity, title and provenance metadata without duplicating those fields.
- language: en / vi / mul / und; unknown is und, never automatically inferred.
- verification_status: UNVERIFIED by default; VERIFIED or DISPUTED requires an explicit verification_note. A matching hash never promotes this status or proves correctness.
- source_version: positive integer for this registry's version sequence, not an inferred publisher release number. Initial recorded snapshot is 1.
- replaces: predecessor source ID or null; a replacement uses a new ID and the next version number.
- original_uri_status: UNKNOWN by default, or an explicitly recorded AVAILABLE / UNAVAILABLE observation. Known observations require original_uri_checked_at at recorded date precision. These are metadata assertions; validators do not make HTTP requests.

Unknown author, publisher, publication date, original URI or verification must stay unknown. Missing required title, type, retrieval date, permission metadata or local snapshot cannot be repaired by guessing.

## Identity, duplicates and revisions

- Same ID + identical CSV and provenance: DUPLICATE, no metadata write.
- Same ID + different bytes or metadata: conflict, no silent overwrite.
- New ID + identical bytes without an explicit replacement: return the first registered matching ID deterministically; append nothing. The unregistered candidate file is retained, not deleted.
- A changed snapshot for the same known origin requires a new ID, new raw file, source_version + 1 and replaces. No fork, missing predecessor or cycle is accepted.
- A metadata-only correction may reuse unchanged bytes/path under a new ID and explicit replacement. Old records and references remain resolvable.
- Unrelated duplicate hashes or unlinked revisions inserted outside the admission API fail strict validation.
- Superseded sources stay available. Existing wiki references are reported for review, never silently changed to a newer source.

## Authorized admission and immutable raw

The source_integrity module exposes small standard-library functions for separately authorized future intake:

1. create_raw_snapshot(root, location, bytes, authorized=True): creates a new snapshot exclusively; an existing target is never opened for writing. No implicit authorization, source download or translation.
2. register_source(root, reviewed_row, authorized=True, ...): validates metadata, computes hashes, checks duplicates and version lineage, then appends ledger/CSV metadata. It never writes raw contents. The reviewed row must contain the exact existing nine fields.
3. audit_sources(root): strict read-only audit, normalized source view and reverse wiki relationships.

All paths reuse the existing workspace/private/symlink/junction guards. Hashing reads registered raw files as binary chunks; it never prints source bodies. Audit and Query do not modify raw or provenance.

Registration uses an exclusive lock and persists the ledger first, then appends the CSV row. A stale lock is not automatically removed. If an interruption leaves an orphan ledger record, validation and Query fail closed. Human reconciliation must verify the surviving record and bytes before appending the exact missing CSV row; do not truncate history or rehash altered raw just to clear an error.

These controls enforce immutability through these maintenance APIs and detect later byte changes. They do not make files unwritable to every editor/OS process. Trusted Git history and human review are needed against an actor able to alter both raw data and the ledger.

## Traceability and Query

Wiki Source IDs metadata remains compatible. One finding may cite several sources using separate source-pointer citations. Source-to-wiki relationships and structured finding source lists are included in the integrity audit. Missing IDs, missing files and changed hashes remain errors, not evidence.

The existing source-based lexical Query gate now requires every source cited by a returned structured finding to be available. With a ledger present, cited snapshots must match their recorded hashes. Citations include source_version, verification_status, integrity_status, original URI status and superseded_by. Query does not silently omit a bad supporting source and return the remainder as complete evidence.

Legacy workspaces without a ledger keep metadata-only retrieval, visibly labelled LEGACY_UNHASHED. This does not establish byte integrity. An empty/partial ledger is not a waiver for missing entries: strict admission requires complete provenance, and Query blocks those missing entries. Approved ADR reasoning remains the separate existing agent workflow.

## Validation modes

~~~text
python -B scripts/check_workspace.py
python -B scripts/check_workspace.py --integrity
python -B -m unittest discover -s tests -v
python -B scripts/validate_source_integrity.py
~~~

Default Lint keeps its metadata-only compatibility behavior and explicitly says hash checks were not run. The integrity flag additionally requires complete provenance, verifies raw/manifest hashes, detects duplicate bytes and broken version chains, and reports source relationships. Neither mode verifies factual claims, permission assertions or original URL availability.

Tests are synthetic and disposable under tests/. They cover the ten requested scenarios, legacy migration, multiple-source claims, metadata tampering, binary data, stale locks, interrupted registration and trust-status separation. Saved reports must use a new path; prior test reports are not rewritten.

## Migration notes

1. Run strict validation first. Missing ledger records are MISSING_PROVENANCE, not proof that the old source was modified.
2. For local legacy sources, plan_migration(root) produces a read-only proposal with current byte/manifest hashes and explicitly unknown optional metadata. It establishes a baseline now, not proof of historical immutability.
3. Review the proposal. The user may supply known language/publisher/origin or justified version links; do not invent them. Duplicate legacy content needs explicit human reconciliation. URL-only records require a separately authorized local snapshot; there is no automatic download.
4. apply_migration(root, proposal, authorized=True) rechecks current bytes, metadata, IDs and the prospective version graph before appending records. A stale/invalid proposal writes nothing. Existing raw and CSV bytes remain unchanged.
5. Run strict validation again. Only after it passes should new real knowledge intake proceed under its own authorization.

The live manifest was empty at discovery, so no live data migration or source ingestion was needed or performed. Existing multilingual fixtures remain a deliberate legacy compatibility corpus, including intentional negative cases; they are not asserted to pass strict source admission unchanged.
