# Prompt: QUERY

Read `AGENTS.md`, `SCHEMA.md`, and `PROFILE.md`; start knowledge navigation at `wiki/index.md`. Question: `[QUESTION]`.

Accept Vietnamese or English questions over English technical pages. Follow `MULTILINGUAL.md`: preserve the original question and all technical terms, filenames, APIs and identifiers. Establish the exact project Scope first; ask for clarification if it is unknown. Expand Vietnamese only through in-scope `title_vi` / `aliases_vi` and their declared English `keywords`. Keep added terms visible; do not invent synonyms, translate raw sources, or fall back to another project.

When useful, run the read-only lexical helper with `python -B scripts/query_workspace.py --scope <scope> --query "<question>"`. It reports matches and source pointers, not a generated answer. Distinguish NOT_FOUND, MISSING_EVIDENCE and AMBIGUOUS; do not treat a matched page, metadata-only source ID or lexical rank as factual verification. Unlisted paraphrases can be UNKNOWN.

Use relevant wiki pages and trace material claims to registered sources or direct APPROVED ADRs. Read the authorized primary evidence when the claim is consequential or time-sensitive; if evidence is unavailable, report UNKNOWN. Do not fetch external URLs or inspect other repositories without task authorization.

Follow `SOURCE_INTEGRITY.md`: a matching hash proves recorded bytes, not correctness. Legacy citations marked LEGACY_UNHASHED have no byte-integrity baseline. Do not conceal missing/tampered supporting sources, infer URL availability, or silently retarget superseded IDs; report source versions and evidence gaps.

Distinguish FACT / INTERPRETATION / HYPOTHESIS / UNKNOWN and give precise source pointers, dates where relevant, and unresolved research gaps. A PROPOSED ADR is a proposal, not an approved choice.

This operation is read-only: do not change wiki, index, log, raw sources, manifest, or save an answer file. A useful synthesis may be offered as a separate scoped patch. Query is complete when the answer and evidence gaps are delivered; no log entry is required.
