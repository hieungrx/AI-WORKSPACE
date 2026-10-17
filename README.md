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
3. Create a **private** Git repository if you want version history and sync. Do not upload secrets, private documents, or sensitive datasets without reviewing them.
4. Edit `PROFILE.md` with non-sensitive preferences and operating goals.
5. Edit `projects/index.md`, then copy `templates/project-context.md` into `projects/<project>/context.md` for your first actual project.
6. Store one permitted source document (or a note with its verified URL) in `sources/raw/`; register it in `sources/manifest.csv`.
7. Ask a coding agent to **ingest** it using `prompts/ingest.md`, then review the diff. Commit only after review.
8. Run `python scripts/check_workspace.py` to identify missing wiki links and missing source references.

## Structure
- `AGENTS.md`: default instructions for a coding agent opened at this root.
- `SCHEMA.md`: knowledge representation and Ingest / Query / Lint contracts.
- `sources/raw/`: read-only references (content immutable after ingest; revisions become separate sources).
- `sources/manifest.csv`: provenance and licensing/permission pointers.
- `wiki/`: agent-curated Markdown and `index.md`, `log.md`.
- `projects/`: *pointers* to canonical code repositories and brief project context; do not duplicate databases or secrets.
- `decisions/`: approved architecture/product decisions (ADRs).
- `handoffs/`: approved packets for GPT specialists and coding agents.
- `experiments/`: measurable hypotheses and results logs.
- `prompts/`: task entry points.
- `templates/`: reusable formats.
- `scripts/`: lightweight local checks.

## Day-to-day loop
**INGEST** source → propose wiki updates → review citations/diff → accept → log.
**QUERY** index first → read related wiki → verify claims against source → answer → optionally file a useful synthesis.
**LINT** check stale claims, contradictions, orphan pages, citations, broken links → report → apply approved edits.
**BUILD** read relevant project repository + context → plan → implement on feature branch → run tests → review → accept/rollback → update decisions and wiki.

## Boundaries
- Never assume this directory can automatically synchronize with ChatGPT Custom GPTs, Google Drive, or Gemini Spark. Manual export/import or separately authorized connectors are required.
- This repository stores **knowledge**, not application source or real secret values.
- Raw sources are not automatically legally shareable. Check copyright and privacy.
- `wiki` content is a synthesis, never a substitute for verified source documents.

## Sources
- [Karpathy's LLM Wiki idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Karpathy's AutoResearch](https://github.com/karpathy/autoresearch)
- [OpenAI Codex workflows](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex)
