# AI-Workspace Agent Instructions

## Mission
Maintain a high-integrity personal knowledge workspace. Follow `SCHEMA.md`. Produce small, reviewable changes. Do not assume facts not present in sources.

## Read order
1. `README.md` and `SCHEMA.md`
2. `wiki/index.md` and the relevant project `context.md`
3. Only the relevant source files and wiki pages
4. Recent entries in `wiki/log.md` and applicable `decisions/`

## Permission boundaries
- `sources/raw/`: **READ ONLY**. Never modify, truncate or delete existing source files. New sources require user authorization.
- `sources/manifest.csv`: append only for newly approved sources; do not overwrite provenance.
- `wiki/`: agent may propose edits. Apply only in permitted scope and surface a diff to the human reviewer.
- `projects/`: update only approved project metadata; the code repo is authoritative for implementation.
- `decisions/`: draft or propose; only the user may approve decisions.
- `experiments/`: record observed test output; never fabricate measurements or PASS status.
- Never access, expose, write or commit credentials, tokens, private keys, financial or identity records.
- Do not run downloads, commands, browser actions, deployment or external writes unless explicitly authorized for the task.

## Evidence and quality
- Every nontrivial fact added to the wiki must point to a source ID from `sources/manifest.csv` or a clearly marked first-party project decision.
- Distinguish FACT / INTERPRETATION / HYPOTHESIS / UNKNOWN; preserve dates for time-sensitive facts.
- If two sources conflict, record both, their dates, and the unresolved conflict. Do not silently overwrite.
- Keep wiki navigation (`wiki/index.md`) and history (`wiki/log.md`) updated with approved edits.
- Do not invent test results, URLs, document IDs, Git commits or citations.

## Execution output
Provide: objective, files read, files changed, sources used, checks performed, risks, and items requiring human approval.
