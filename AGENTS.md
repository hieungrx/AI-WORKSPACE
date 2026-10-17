# AI-Workspace Agent Instructions

## Mission
Maintain a high-integrity personal knowledge workspace. Follow `SCHEMA.md`. Produce small, reviewable changes. Do not assume facts not present in sources.

Respond in Vietnamese and follow the non-sensitive preferences in `PROFILE.md`. Inspect current files before proposing changes, work in small checkpoints, and prefer the existing architecture and Python standard library. Do not work on `main`.

## Read order
1. `README.md`, `SCHEMA.md`, and `PROFILE.md`
2. `wiki/index.md` and the relevant project `context.md`
3. Only the relevant source files and wiki pages
4. Recent entries in `wiki/log.md` and applicable `decisions/`

## Permission boundaries
- `sources/raw/`: **READ ONLY**. Never modify, truncate or delete existing source files. New sources require user authorization.
- `sources/manifest.csv`: append only for newly approved sources; do not overwrite provenance.
- `wiki/`: agent may propose edits. Apply only in permitted scope and surface a diff to the human reviewer.
- `wiki/log.md`: append approved changes and actual check results; never rewrite prior entries. Query and read-only Lint do not append entries.
- `projects/`: update only approved project metadata; the code repo is authoritative for implementation.
- `decisions/`: draft or propose; only the user may approve decisions.
- `experiments/`: record observed test output; never fabricate measurements or PASS status.
- Never access, expose, write or commit credentials, tokens, private keys, financial or identity records.
- Lint may flag a suspected sensitive location without opening its contents or printing secret values. Do not treat a secret scan as permission to read protected material.
- Do not run downloads, commands, browser actions, deployment or external writes unless explicitly authorized for the task.

## Evidence and quality
- Every nontrivial fact added to the wiki must point to a source ID from `sources/manifest.csv` or a clearly marked first-party project decision.
- A decision is evidence of a project's approved choice only when its linked ADR is `APPROVED`; `PROPOSED` records are not approved evidence. Source IDs and ADR links do not by themselves verify a claim.
- Distinguish FACT / INTERPRETATION / HYPOTHESIS / UNKNOWN; preserve dates for time-sensitive facts.
- If two sources conflict, record both, their dates, and the unresolved conflict. Do not silently overwrite.
- Keep wiki navigation (`wiki/index.md`) and history (`wiki/log.md`) updated with approved edits.
- Do not invent test results, URLs, document IDs, Git commits or citations.

## Execution output
Provide: objective, files read, files changed, sources used, checks performed, risks, and items requiring human approval.
Separate observed checks from interpretations, checks not run, and manual review still needed. Follow the operation-specific completion rules in `SCHEMA.md`.
