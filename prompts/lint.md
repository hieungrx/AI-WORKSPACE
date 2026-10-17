# Prompt: LINT

Follow `SECURITY_POLICY.md` and run `python -B scripts/check_workspace.py --integrity --security`. Never open actual secret/environment/private locations, print matched values or send findings externally. Reports use the centralized redacted, exclusive writer. Report pending recovery and version conflicts without resetting files, deleting user changes or clearing owner locks automatically.

Follow `KNOWLEDGE_GOVERNANCE.md`. The existing checker also validates canonical lifecycle metadata, transition chains, content-bound human validation approval, successor references, scope consistency and explicit review dates. Report legacy compatibility separately from verified authority. Flag unresolved conflicts and due reviews; do not select a winning source, change status because of age, or auto-promote anything.

For Phase 1 source integrity, follow `SOURCE_INTEGRITY.md` and additionally run `python -B scripts/check_workspace.py --integrity`. This read-only mode hashes registered raw bytes without printing them. Report missing provenance, changed bytes/manifest metadata, duplicate content, broken version lineage and reverse wiki references; never repair a failed hash by overwriting raw or its baseline. The default command below is metadata-only compatibility mode.

Read `AGENTS.md`, `SCHEMA.md`, `PROFILE.md`, and `wiki/index.md`. Audit without changing content. Identify:
- Missing provenance / source IDs
- Broken Markdown links and missing index entries
- Contradictions, stale facts and unresolved questions
- Orphan pages and duplication
- Duplicate optional page_id, unsupported YAML frontmatter, duplicate index targets, unreviewed knowledge and same-scope current decision_key collisions under WORKFLOW_RELIABILITY.md. These are structural findings; unkeyed/textual contradictions still need review.
- Suspected sensitive locations, without opening protected contents or printing secret values

Run `python -B scripts/check_workspace.py` if Python is available. Report actual exit code, errors and warnings separately from semantic/manual findings. The checker does not verify facts, heading anchors, freshness, permission, approval or Obsidian rendering. Reference-style links and wikilinks require manual review. Use FACT / INTERPRETATION / HYPOTHESIS / UNKNOWN for conclusions and uncertainties.

Return findings in chat with file paths, severity, evidence, proposed fixes and decisions needed. Do not edit wiki or append the log for a read-only audit. Save a report only when requested, to a new `reports/lint-YYYY-MM-DD-HHMMSS.md`, adding a suffix if needed rather than overwriting an earlier report.

Apply only approved corrections. For applied wiki changes, update relevant index links, append a dated log entry and rerun the checker. Report checks not run; never equate structural PASS with factual verification.
