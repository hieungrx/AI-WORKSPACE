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
