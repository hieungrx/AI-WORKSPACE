# AI-Workspace Starter (v1.0)

A lightweight, Markdown-first personal AI workspace inspired by Andrej Karpathy's LLM Wiki pattern and evidence-driven agent workflows. This is **not** an official Karpathy project.

## Design goals
- One durable knowledge base rather than scattered chat histories.
- Keep **raw sources** separate from **LLM-maintained wiki** and **project source-of-truth**.
- Require evidence and human approval for high-risk changes.
- Keep each code repository independent; do not copy code into this knowledge repo.

## Start here (Windows)
1. Extract this directory to a location such as `D:\AI-Workspace` (or any folder you own).
2. Open the folder as an Obsidian vault, or in VS Code.
3. Use local Git history and a separate working branch for reviewable changes. For a fresh copy without Git, `git init -b workspace/initialize` creates that branch directly. Review the exact files before making a baseline commit. Do not work on `main`; a remote or sync setup is a separate decision.
4. Edit `PROFILE.md` with non-sensitive preferences and operating goals.
5. Edit `projects/index.md`, then copy `templates/project-context.md` into `projects/<project>/context.md` for your first actual project.
6. Authorize the first source and its processing permissions. Then store it (or a permitted URL record) in `sources/raw/` and append its unique entry in `sources/manifest.csv`. Existing raw files and provenance remain unchanged.
7. Ask a coding agent to **ingest** it using `prompts/ingest.md`, then review the diff. Commit only after review.
8. Run `python -B scripts/check_workspace.py` for structural checks and review any warnings. This does not verify facts or source permissions.

## Structure
- `AGENTS.md`: default instructions for a coding agent opened at this root.
- `SCHEMA.md`: knowledge representation and Ingest / Query / Lint contracts.
- `sources/raw/`: existing files are read-only; revisions require authorization and a new source ID.
- `sources/manifest.csv`: provenance and licensing/permission pointers.
- `wiki/`: agent-curated Markdown and `index.md`, `log.md`.
- `projects/`: *pointers* to canonical code repositories and brief project context; do not duplicate databases or secrets.
- `decisions/`: approved architecture/product decisions (ADRs).
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
Run from the workspace root; only Python's standard library is needed:

```text
python -B scripts/check_workspace.py
python -B -m unittest discover -s tests -v
```

The checker validates manifest metadata/local source existence, wiki metadata and structured citations, local inline link/image file targets, and wiki reachability from the index. It does not read raw source bodies or fetch URLs. It reports unsupported reference links/wikilinks for manual review and does not validate heading anchors or factual meaning. Exit 0 means no structural errors, possibly with warnings; exit 1 means errors need attention.

Keep each accepted checkpoint in a separate local commit and review its diff before continuing. Rollback can target that checkpoint without rewriting earlier history. Tests use isolated temporary fixtures under `tests/`, removed by the test runner, not real sources or approved decisions.

## Codex and Obsidian
Open the workspace root as the vault. The checked-in `.obsidian/app.json` selects Markdown links and relative paths, matching `SCHEMA.md`. Generate links from the final page location. Opening a page and following its links in Obsidian is a separate visual check; the script cannot certify that behavior. No additional plugin is required by this workspace contract.

## Boundaries
- Never assume this directory can automatically synchronize with ChatGPT Custom GPTs, Google Drive, or Gemini Spark. Manual export/import or separately authorized connectors are required.
- This repository stores **knowledge**, not application source or real secret values.
- Raw sources are not automatically legally shareable. Check copyright and privacy.
- `wiki` content is a synthesis, never a substitute for verified source documents.

## Sources
- [Karpathy's LLM Wiki idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Karpathy's AutoResearch](https://github.com/karpathy/autoresearch)
- [OpenAI Codex workflows](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex)
