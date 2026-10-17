# Wiki activity log (append-only)

## [2026-10-17] scaffold | Initialize AI-Workspace
- Added empty source registry, wiki skeleton, and governance files.
- No external sources ingested; no code tests or experiments claimed.

## [2026-10-17] maintenance | Stabilize Ingest / Query / Lint
- First-party maintenance observed under the user's approved implementation plan; this entry is not external research evidence.
- Local branch: `workspace/initialize`. Baseline: `6a2d37f`; operation contracts: `003bad2`; prompts/template: `97c4b2b`; validator/tests: `da93750`. Each checkpoint is independently reviewable.
- Updated `AGENTS.md`, `SCHEMA.md`, `README.md`, the three knowledge prompts, `templates/wiki-page.md`, and `scripts/check_workspace.py`; added `tests/test_check_workspace.py`.
- Observed: `python -B -m unittest discover -s tests -v` ran 36 tests, all OK, exit 0. Fixtures include a registered-source synthesis, invalid citations/metadata, approved/proposed ADRs, navigation, path boundaries, protected-content guards and read-only behavior. These are isolated tests, not a real source ingest or an agent workflow execution.
- Observed: the checker ran from both the workspace root and `scripts/`, exit 0, with 0 structural errors and 1 `NO_EVIDENCE` warning for the existing DRAFT principles page. No source was invented to clear the warning.
- Observed: Git diff whitespace checks passed. SHA-256 comparisons confirmed raw README, manifest, decisions index and Obsidian app configuration were unchanged; earlier log entries are retained.
- Manual contract review: Query remains read-only; missing source authorization/registration stops Ingest at the intake proposal; read-only Lint reports in chat. No source bodies were ingested and no external repositories or URLs were opened.
- NOT_RUN: real-source Ingest (no source registered/approved for this task), Obsidian visual rendering/link clicks, and external-source verification. Structural checks do not establish factual accuracy or human approval.

## [2026-10-17] maintenance | Multilingual readiness V1
- First-party implementation under the user's multilingual-readiness task. Metadata/specification checkpoint: `aecf6ce`; lexical retrieval, synthetic fixtures and regression tests: `22602ee`.
- Added optional language, title_vi, keywords and aliases_vi metadata without changing existing page requirements or manifest columns. Updated the template, Query/Ingest prompts, schema, README and wiki navigation; the specification and proposed semantic upgrade path are in [MULTILINGUAL.md](../MULTILINGUAL.md).
- Added read-only lexical retrieval with explicit project scope, curated Vietnamese-to-English expansion, preserved identifiers and a local source-citation gate. It returns NOT_FOUND or MISSING_EVIDENCE rather than guessing. This is not semantic retrieval or answer generation.
- Observed: `python -B -m unittest discover -s tests -v` ran 55 tests, all OK, exit 0. These include the previous 36 tests and multilingual compatibility, Unicode, ambiguity, identifier preservation, scope isolation, evidence and read-only checks.
- Observed: `python -B scripts/validate_multilingual.py --output reports/multilingual-2026-10-17.json` executed 25 Vietnamese-English pairs / 50 queries on 23 synthetic documents; 50 expected outcomes met, 0 failed. Actual outcomes: 36 FOUND, 6 NOT_FOUND and 8 MISSING_EVIDENCE. Each of the five requested categories met 10/10 expected query outcomes; negative outcomes are intentional, not successful document retrievals.
- Detailed actual queries, expansions, paths, scopes and fixture citations: [readable report](../reports/multilingual-2026-10-17.md) and [JSON results](../reports/multilingual-2026-10-17.json). Artificial source IDs and evidence belong only to the separate test fixture registry, not live knowledge.
- Observed: live-workspace query for “nguồn đã được kiểm chứng” in unscoped returned NOT_FOUND. The live linter reported 0 structural errors and the existing DRAFT NO_EVIDENCE warning. Diff whitespace checks passed; live raw, manifest and decisions-index hashes were unchanged.
- NOT_RUN: real knowledge ingest, semantic retrieval quality on unseen paraphrases, and Obsidian visual checks. No QMD, RAG, vector database, new dependency or external-repository access was introduced.

## [2026-10-17] maintenance | Phase 1 source integrity and provenance
- First-party implementation and audit under the user's Phase 1 task; no real source intake or external research. Discovery baseline: b2acfef on workspace/initialize. Integrity/test checkpoint: b92094c; contract/migration checkpoint: 371c56d.
- Extended existing validators instead of duplicating their metadata, citation and path checks. Kept the nine-column manifest and added a separate append-only provenance ledger; controlled new snapshots/admission, SHA-256 for raw and manifest metadata, deterministic duplicates, explicit replacement lineage, reverse source-to-wiki relationships, and fail-closed Query evidence checks.
- Contract, compatibility, unknown metadata handling, migration and limits: [SOURCE_INTEGRITY.md](../SOURCE_INTEGRITY.md). Unknown source metadata stays unknown; a matching hash or citation never certifies factual correctness.
- Observed: python -B scripts/validate_source_integrity.py --output reports/source-integrity-phase1-2026-10-17.json ran 81 tests, 81 PASS, 0 failures/errors/skips. These include 26 new integrity tests with all ten requested synthetic scenarios, plus the existing 55 compatibility tests. The live registry has 0 sources and the new ledger is empty.
- Observed: python -B scripts/check_workspace.py --integrity returned exit 0, 0 errors and the existing DRAFT NO_EVIDENCE warning. The separate multilingual validator met all 50 expected query outcomes: 36 FOUND, 6 NOT_FOUND, 8 MISSING_EVIDENCE; those negative outcomes remain intentional.
- Actual audit/results: [readable report](../reports/source-integrity-phase1-2026-10-17.md) and [JSON evidence](../reports/source-integrity-phase1-2026-10-17.json). Phase 1 verdict is PASS for the implemented contract, current empty registry and synthetic tests only.
- Observed: staged/working diff whitespace checks passed. Baseline SHA-256 comparisons preserved live raw README, manifest, decisions index and the user's existing Obsidian graph change; earlier log bytes were retained before this append.
- Remaining limits: URL availability was not checked over the network; legacy migration establishes a current-byte baseline, not historical immutability. Interrupted two-file registration fails closed and requires human reconciliation. Trusted history is still needed against edits to both raw and provenance.
- NOT_RUN: real knowledge ingestion, real-source migration, Obsidian visual checks, factual verification, Phase 2 or V2. Future real intake/migration requires its own task authorization.
