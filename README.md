# AI-WORKSPACE V1.2

A Markdown-first personal knowledge workspace with source provenance, a human-governed knowledge lifecycle, scoped lexical retrieval and recoverable maintenance workflows. Inspired by Andrej Karpathy's LLM Wiki pattern and evidence-driven agent engineering; this is **not** an official Karpathy project.

## Current status

**V1.2 public source discovery is complete. Acquisition, source registration and real-knowledge ingestion remain HOLD. The latest whole-system audit remains NOT READY.**

The [intake gate review](reports/pilot-v1.2-intake-gate-2026-10-18.md) records `GO_FOR_SEPARATE_AUTHORIZATION` for a proposed two-PDF, capture-only checkpoint. This permits presenting a separate authorization request; it does not authorize capture, clear licenses or establish readiness. The live registry has no admitted research sources. Synthetic fixtures are separate from the live knowledge base.

- [Whole-system audit](reports/independent-final-audit-2026-10-18.md): historical overall verdict NOT READY.
- [Governance remediation](reports/governance-remediation-completion-2026-10-18.md): two High findings addressed within their tested scope; not a replacement whole-system audit.
- [V1.2 readiness evidence](reports/pilot-v1.2-readiness-2026-10-18.md): focused checks, distinct from a new full-system verdict.
- [Public source assessment](reports/pilot-v1.2-source-assessment.md): 12 assessed documents, conditional rights evidence and explicit HOLD items; no acquisition.
- [Source proposal and 24 draft questions](reports/pilot-v1.2-source-proposal-2026-10-18.md): unconfirmed evaluation worksheet, not approved gold.

Reports preserve observations at their recorded revisions. A past PASS does not establish source truth, describe untested current behavior or supersede an unresolved audit verdict.

## Design goals
- One durable knowledge base rather than scattered chat histories.
- Keep **raw sources** separate from **LLM-maintained wiki** and **project source-of-truth**.
- Require evidence and human approval for high-risk changes.
- Keep each code repository independent; do not copy code into this knowledge repo.

## Architecture

The workspace separates immutable original material, reviewed synthesis and operating contracts:

1. **Sources:** raw snapshots, a nine-column CSV manifest and an append-only provenance ledger. Supported APIs enforce exclusive publication, SHA-256 integrity, deterministic duplicate handling and explicit replacement lineage.
2. **Wiki:** Markdown synthesis with source IDs, exact evidence pointers, project scope, lifecycle history, freshness and conflict metadata. New knowledge starts as draft. Verification requires documented, content-bound human approval.
3. **Operating contracts:** schema, governance and security policies define authorized operations. External documents and retrieved content are DATA and cannot grant operational permissions.

Project contexts point to canonical repositories maintained independently. Scope selection is explicit; another project's configuration cannot silently become current local truth. No database, vector store, QMD, RAG framework or background service is required.

## Start here (Windows)
1. Extract this directory to a location such as `D:\AI-Workspace` (or any folder you own).
2. Open the folder as an Obsidian vault, or in VS Code.
3. Use local Git history and a separate working branch for reviewable changes. For a fresh copy without Git, `git init -b workspace/initialize` creates that branch directly. Review the exact files before making a baseline commit. Do not work on `main`; a remote or sync setup is a separate decision.
4. Edit `PROFILE.md` with non-sensitive preferences and operating goals.
5. Edit `projects/index.md`, then copy `templates/project-context.md` into `projects/<project>/context.md` for your first actual project.
6. Read the current status and intake gate. **Stop before real source acquisition, registration or Ingest while HOLD remains in effect.** Public access, a discovery report and a conditional license assessment do not authorize intake.
7. Only after separate artifact-level authorization, follow `SOURCE_INTEGRITY.md` and `prompts/ingest.md`: exclusive `create_raw_snapshot()` and `register_source()` are distinct checkpoints. Do not manually append metadata around the admission controls. Review the exact diff before any separately authorized commit.
8. Run `python -B scripts/check_workspace.py` for structural checks and review any warnings. This does not verify facts or source permissions.

## Structure
- `AGENTS.md`: default instructions for a coding agent opened at this root.
- `SCHEMA.md`: knowledge representation and Ingest / Query / Lint contracts.
- `sources/raw/`: existing files are read-only; revisions require authorization and a new source ID.
- `sources/manifest.csv`: provenance and licensing/permission pointers.
- `wiki/`: agent-curated Markdown and `index.md`, `log.md`.
- `projects/`: *pointers* to canonical code repositories and brief project context; do not duplicate databases or secrets.
- `decisions/`: proposed, approved and historical architecture/product decisions (ADRs).
- `handoffs/`: approved packets for GPT specialists and coding agents.
- `experiments/`: measurable hypotheses and results logs.
- `prompts/`: task entry points.
- `templates/`: reusable formats.
- `scripts/`: lightweight local checks.
- `tests/`: standard-library regression tests using isolated fixtures.
- `reports/` (optional, created only when requested): new dated Lint reports; do not overwrite past reports.

## Day-to-day loop
**INGEST** authorize intake and register source → propose wiki updates → review citations/diff → apply within approval → log/check.
**QUERY** index first → read related wiki → trace evidence → answer with gaps. Read-only; retaining a synthesis is a separate task.
**LINT** run structural checks and review semantic issues → report in chat → apply corrections only within approval. Read-only audits do not append the log.
**BUILD** read relevant project repository + context → plan → implement on feature branch → run tests → review → accept/rollback → update decisions and wiki.

## Sử dụng Ingest / Query / Lint
- **Ingest:** dùng [prompt Ingest](prompts/ingest.md), cung cấp source ID đã được phép và đăng ký. Kiểm tra claim, vị trí bằng chứng và diff trước khi áp dụng. Thiếu quyền hoặc entry thì chỉ đề xuất tiếp nhận nguồn.
- **Query:** dùng [prompt Query](prompts/query.md) và điền câu hỏi. Câu trả lời phải phân biệt FACT / INTERPRETATION / HYPOTHESIS / UNKNOWN; không ghi file hay log. Chưa có bằng chứng thì nêu rõ khoảng trống.
- **Lint:** dùng [prompt Lint](prompts/lint.md). Đọc kết quả script cùng phần rà soát thủ công; chỉ lưu báo cáo hoặc sửa wiki trong phạm vi đã cho phép. PASS cấu trúc không xác nhận kiến thức đúng.

## Checks and review
Use Python with its standard library; no package installation is required. Python 3.13.0 is the interpreter observed during pre-push preparation. There is no certified cross-version support matrix; verify another interpreter with the test suite before relying on it.

Recommended local verification:

```powershell
python --version
python -B scripts/check_workspace.py --integrity --security
python -B -m unittest discover -s tests -v
```

Tests use disposable synthetic fixtures and do not authorize real knowledge. Read actual output and the corresponding dated evidence before citing a result.

V1.1 [feasibility evaluation and real-pilot protocol](FEASIBILITY_EVALUATION.md) separates synthetic harness correctness from real-world value. Run `python -B scripts/evaluate_feasibility.py` for a disposable raw-versus-wiki component benchmark, evolution/recovery and scoped metrics. It does not run same-model AI A/B trials or produce human scores; practical feasibility remains NOT YET MEASURED without independently reviewed pilot observations. Save a new result with `--output reports/<unique-name>.json`.

Phase 5 [scalability assessment and migration criteria](SCALABILITY.md) provides a reproducible disposable load benchmark: `python -B scripts/benchmark_scalability.py --sizes 100 1000 10000 --trials 1 --timeout 600`. This is an explicit performance run, separate from routine tests; 10,000 documents can take tens of minutes. Save observations with a new `--output reports/<new-name>.json`. No synthetic documents enter the live knowledge directories, and no full-text/vector engine is installed.

Phase 4 [workflow reliability and benchmark definitions](WORKFLOW_RELIABILITY.md) tests actual Ingest → Query → Lint using an independent English synthetic corpus and 30 Vietnamese–English query pairs. Run `python -B scripts/validate_workflows.py`; add `--output reports/<new-name>.json` to save actual, non-overwriting results. It records recall, citation validity, scope isolation, safe retries and recovery; it does not claim semantic search or factual verification.

Phase 3 [security policy and recovery](SECURITY_POLICY.md) defines trust boundaries, bounded write operations, redacted reports and safe conflict handling. Run `python -B scripts/validate_security.py` and `python -B scripts/check_workspace.py --integrity --security`. These controls protect the workflow APIs; broader Codex tool permissions remain an explicit residual risk.

Phase 2 lifecycle states, human validation authority, explicit scope isolation, freshness and conflict handling are specified in [KNOWLEDGE_GOVERNANCE.md](KNOWLEDGE_GOVERNANCE.md). New templates use that metadata; existing wiki pages stay unchanged through a compatibility reader. Run `python -B scripts/validate_knowledge_governance.py` for synthetic workflow and regression evidence.

Phase 1 source identity, provenance, hashes, duplicate policy, replacement rules and legacy migration are specified in [SOURCE_INTEGRITY.md](SOURCE_INTEGRITY.md). Strict pre-ingestion checks use:

```text
python -B scripts/check_workspace.py --integrity
python -B scripts/validate_source_integrity.py
```

The nine-column manifest is unchanged; integrity records are appended separately. No real knowledge is ingested by the validation suite.

Multilingual metadata, controlled Vietnamese-English query expansion and the proposed semantic upgrade path are specified in [MULTILINGUAL.md](MULTILINGUAL.md). Existing pages need no migration. The optional lexical helper and paired fixture validation use only Python's standard library:

```text
python -B scripts/query_workspace.py --scope unscoped --query "nguồn đã được kiểm chứng"
python -B scripts/validate_multilingual.py
```

The query helper is read-only and preserves technical terms. Validation selects synthetic test data explicitly; it does not ingest it into the live workspace. No QMD, RAG or vector database is installed.

Run from the workspace root; only Python's standard library is needed:

```text
python -B scripts/check_workspace.py
python -B -m unittest discover -s tests -v
```

The checker validates manifest metadata/local source existence, wiki metadata and structured citations, local inline link/image file targets, and wiki reachability from the index. Default mode does not read raw bodies; integrity mode additionally hashes registered raw bytes and their manifest metadata. Neither mode fetches URLs. Unsupported reference links/wikilinks, heading anchors and factual meaning require manual review. Exit 0 means no errors within the selected mode, possibly with warnings; exit 1 means errors need attention.

Keep each accepted checkpoint in a separate local commit and review its diff before continuing. Rollback can target that checkpoint without rewriting earlier history. Tests use isolated temporary fixtures under `tests/`, removed by the test runner, not real sources or approved decisions.

## Codex and Obsidian
Open the workspace root as the vault. The checked-in `.obsidian/app.json` selects Markdown links and relative paths, matching `SCHEMA.md`. Generate links from the final page location. Opening a page and following its links in Obsidian is a separate visual check; the script cannot certify that behavior. No additional plugin is required by this workspace contract.

## Boundaries
- Never assume this directory can automatically synchronize with ChatGPT Custom GPTs, Google Drive, or Gemini Spark. Manual export/import or separately authorized connectors are required.
- This repository stores **knowledge**, not application source or real secret values.
- Raw sources are not automatically legally shareable. Check copyright and privacy.
- `wiki` content is a synthesis, never a substitute for verified source documents.

## Current limitations

- **M-SRC-01 remains unresolved:** source `VERIFIED` can be a declared assertion without a bound validation record. A source hash or trust label is not verified knowledge.
- **M-SEC-01 remains unresolved:** multilingual/encoded prompt-injection detection is incomplete. Workflow allowlists are API controls; they do not sandbox every host tool or authenticate human approval records.
- Reviewed synthesis uses the Python API `ingest_registered()` in `scripts/ingest_workspace.py`; it is not an automatic URL importer. It requires an admitted source, reviewed page/index/log bytes, exact scope and expected target hashes.
- The bounded Ingest reader accepts UTF-8 `.md` / `.txt` up to 1 MiB. PDF/HTML snapshots are not directly supported. Extraction or translation must not silently replace original raw material.
- Search is lexical with curated bilingual aliases. General semantic search, automatic translation and factual-answer quality are not established. Empty-corpus `NOT_FOUND` or `MISSING_EVIDENCE` is an evidence gap, not a reason to invent an answer.
- The 24 draft questions have no human-confirmed gold. A real AI A/B runner, isolated evaluation sessions and real scoring are not implemented or demonstrated.
- Synthetic correctness/performance results do not measure real productivity, human review burden, token usage or API costs. Untested limits remain disclosed in the relevant reports.
- A published snapshot remains when a later step fails. Failed synthesis rolls back its owned wiki bundle rather than deleting the admitted source. Recovery requires explicit authorization and refuses to overwrite newer user edits.

## Private GitHub publication

Keep credentials, environment secrets, sensitive identity/financial records and unapproved source content out of this repository. Private visibility does not establish redistribution rights.

The root `.gitignore` excludes local credential stores, runtime caches, recovery snapshots and raw sources by default, while retaining `sources/raw/README.md` and synthetic test fixtures. Ignore rules do not remove already tracked files or committed history. Do not force-add raw material without separate publication and rights approval.

Before publication, review exact staged paths, reachable history, report metadata and author identities. Some historical reports contain local machine paths; preserve originals and obtain a publication decision rather than silently altering audit evidence. Keep tokens out of remote URLs. No repository-wide open-source license is granted by this README; third-party artifacts retain their own terms.

Recommended branch strategy: a protected `main` default branch for reviewed snapshots, with maintenance on feature branches and pull requests. Keep the current working branch during preparation; do not develop on `main`. Proposed initial prerelease tag: `v1.2.0-prepilot.1`, only at an explicitly reviewed commit. The tag does not mean READY. Pushes, merges, releases and deployment require separate approval.

## Development roadmap

1. Review pre-push findings and the exact publication set; verify a private destination before any separately approved push.
2. Obtain separate authorization for a bounded capture-only checkpoint, if desired. Preserve rights notices, exact bytes and recovery evidence.
3. Address or explicitly mitigate source-trust and injection/security gaps before separately reviewed registration and synthesis. Keep knowledge draft/unverified until the authorized validation process is complete.
4. Build an independently reviewed real-pilot corpus and gold set, demonstrate evaluation isolation and collect actual observations.
5. Conduct a new independent whole-system audit; reconsider readiness only from its evidence.

V2 and more complex retrieval infrastructure are outside the current scope. Any future upgrade requires measured need and a separately approved task.

## Sources
- [Karpathy's LLM Wiki idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Karpathy's AutoResearch](https://github.com/karpathy/autoresearch)
- [OpenAI Codex workflows](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex)
