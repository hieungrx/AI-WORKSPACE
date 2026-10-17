# Prompt: INGEST

Read `AGENTS.md`, `SCHEMA.md`, `PROFILE.md`, and `wiki/index.md`. Source to ingest: `[SOURCE_ID / LOCAL_PATH]`.

1. Check existing task authorization, permissions and the source's unique entry in `sources/manifest.csv`. If intake is not authorized or registered, stop before reading the unapproved source: propose the new source/append-only entry and explain what is missing. Do not ask again for steps already authorized.
2. Read only the authorized source. Do not fetch a URL or open another repository without task authorization. Extract claims with precise section/page pointers and dates; use FACT / INTERPRETATION / HYPOTHESIS / UNKNOWN. An unverified URL alone is UNKNOWN.
3. Identify affected wiki pages and contradictions. Preserve both sides and their dates when sources conflict. For project choices, cite the direct APPROVED ADR; a PROPOSED ADR is not approval evidence.
   English technical content may stay English. When approved, add optional `language`, `title_vi`, `keywords`, `aliases_vi` and the exact project Scope to synthesized pages under `MULTILINGUAL.md`. These are navigation aids, not new evidence. Never translate or rewrite raw sources or translate technical identifiers.
4. Propose the smallest patch to wiki pages, relevant index links and an appended log entry. Do not change any existing raw file or overwrite provenance. Distinguish the proposal from applied changes.
5. Show the diff, source pointers, unverified claims and remaining decisions. Apply only within approved scope, then run `python -B scripts/check_workspace.py` and report actual results. Commit only when authorized.
