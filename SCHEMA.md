# Knowledge Schema / Operating Contract

## Knowledge layers
1. Raw Sources (`sources/raw` + manifest): immutable material with provenance; may include links, clipped material with reuse rights, personal notes, and authorized documents.
2. Wiki (`wiki`): editable synthesis written/updated by an LLM under review; connected with standard relative Markdown links.
3. Schema (`SCHEMA.md`, `AGENTS.md`): conventions and operations.

## Wiki page format
Use `templates/wiki-page.md`. Each page contains title, updated date, status, summary, findings, citations using SOURCE_ID values, connections, uncertainties and next questions.
Status one of: DRAFT / REVIEWED / STALE.

## Source ID
Use `SRC-YYYYMMDD-###` (e.g. `SRC-20261017-001`). Each ID must have an entry in `sources/manifest.csv`. A URL without retrieval/verification data is not conclusive evidence.

## Operations
### INGEST
- Confirm source license/permissions and register provenance.
- Read source; extract claims with precise page/section/URL anchors where available.
- Identify existing relevant wiki pages. Propose a minimal patch: add/update page(s), cross-links, index, log.
- Mark contradictions, unclear claims and gaps. Ask for human review before committing.

### QUERY
- Read `wiki/index.md` and linked pages first.
- Trace consequential claims to raw-source IDs; differentiate sources from synthesis.
- If there is no evidence, say so rather than invent. Propose research gaps.
- Offer to file durable, properly sourced synthesis back into wiki, not directly into raw.

### LINT
- Check stale facts, missing citations, broken links, conflicting claims, orphan pages, outdated project states, index coverage and log entries.
- Generate `reports/lint-YYYY-MM-DD.md` and a proposed patch; do not auto-delete ambiguous content.

### BUILD (separate from wiki)
- Read canonical repo docs, constraints and accepted feature packet.
- State baseline and acceptance criteria before coding.
- Implement in a branch; run available lint/tests/build and measured benchmarks.
- Compare with baseline; keep / revert recommendation requires observed evidence; human approves merges, deploys and production changes.

## Definition of done
A knowledge operation is DONE when source IDs resolve, index and links are up to date, dated log entry is appended, and any unresolved uncertainty is flagged.
