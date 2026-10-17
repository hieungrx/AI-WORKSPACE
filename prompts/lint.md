# Prompt: LINT

Read `AGENTS.md`, `SCHEMA.md`, `PROFILE.md`, and `wiki/index.md`. Audit without changing content. Identify:
- Missing provenance / source IDs
- Broken Markdown links and missing index entries
- Contradictions, stale facts and unresolved questions
- Orphan pages and duplication
- Suspected sensitive locations, without opening protected contents or printing secret values

Run `python -B scripts/check_workspace.py` if Python is available. Report actual exit code, errors and warnings separately from semantic/manual findings. The checker does not verify facts, heading anchors, freshness, permission, approval or Obsidian rendering. Reference-style links and wikilinks require manual review. Use FACT / INTERPRETATION / HYPOTHESIS / UNKNOWN for conclusions and uncertainties.

Return findings in chat with file paths, severity, evidence, proposed fixes and decisions needed. Do not edit wiki or append the log for a read-only audit. Save a report only when requested, to a new `reports/lint-YYYY-MM-DD-HHMMSS.md`, adding a suffix if needed rather than overwriting an earlier report.

Apply only approved corrections. For applied wiki changes, update relevant index links, append a dated log entry and rerun the checker. Report checks not run; never equate structural PASS with factual verification.
