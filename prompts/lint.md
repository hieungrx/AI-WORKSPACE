# Prompt: LINT

Audit the current wiki without deleting content. Identify:
- Missing provenance / source IDs
- Broken Markdown links and missing index entries
- Contradictions, stale facts and unresolved questions
- Orphan pages and duplication
- Possible secrets and sensitive data

Run `python scripts/check_workspace.py` if Python is available. Output findings with file paths, severity, proposed corrections and follow-up human decisions. If approved, update wiki and append a dated log entry.
