# Prompt: QUERY

Read `AGENTS.md`, `SCHEMA.md`, and `PROFILE.md`; start knowledge navigation at `wiki/index.md`. Question: `[QUESTION]`.

Use relevant wiki pages and trace material claims to registered sources or direct APPROVED ADRs. Read the authorized primary evidence when the claim is consequential or time-sensitive; if evidence is unavailable, report UNKNOWN. Do not fetch external URLs or inspect other repositories without task authorization.

Distinguish FACT / INTERPRETATION / HYPOTHESIS / UNKNOWN and give precise source pointers, dates where relevant, and unresolved research gaps. A PROPOSED ADR is a proposal, not an approved choice.

This operation is read-only: do not change wiki, index, log, raw sources, manifest, or save an answer file. A useful synthesis may be offered as a separate scoped patch. Query is complete when the answer and evidence gaps are delivered; no log entry is required.
