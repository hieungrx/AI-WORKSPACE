# TEST_ONLY V1.1 feasibility dataset

`dataset.json` is an AI-authored synthetic specification, **not human-confirmed real-world gold**. It contains 30 invented English Markdown source documents and 103 independent case specifications: 30 knowledge questions, 40 bilingual questions in 20 Vietnamese-English pairs, 10 evolution/conflict cases, 10 scope cases, 5 new-session continuity cases and 8 research/coding tasks.

All evidence concerns an invented widget protocol and the arbitrary scopes `global`, `pilot-cedar`, `pilot-marlin`; negative scope cases also use `pilot-kestrel`. These identifiers are fixture data, not names to hardcode into core logic. No document describes a real project configuration or real benchmark measurement.

## Independence and provenance

The source `body` values are the raw synthetic evidence. The `cases` gold is declared from their literal `## Evidence` sections, never generated from a wiki page, retriever output, implementation-specific ranking or an executed answer. `required_citations` identifies those raw sections. No external source, author, URL, publication metadata or real human approval is invented. Every expected decision validity remains `unverified`.

The `keywords` and `aliases_vi` properties are **navigation metadata for disposable wiki pages only**. They must not be appended to, translated into, or otherwise change source `body` bytes. There are 29 alias-bearing source specifications (25 distinct Vietnamese labels). Technical names, filenames, API paths, case and punctuation remain literal. The copy-on-write document intentionally has no Vietnamese alias: B20-vi and K27 retain source relevance gold even if lexical retrieval misses them. K28 is an unlisted English paraphrase. Missing retrieval for these cases counts as a recall miss, not fabricated semantic support or a changed empty gold set.

## Execution and scoring

`execution=retrieval` covers 80 cases (knowledge30 + bilingual40 + scope10). This permits observed ranking, recall, valid-citation and scope measurements. A correct retrieved source alone does not establish factual answer correctness, claim-level citation sufficiency, ambiguity resolution, or approved current truth. All returned evidence must remain unverified.

The 23 `protocol_only` cases (evolution10 + continuity5 + task8) specify expected answers and rubrics for a separate real execution. They must be reported **NOT RUN** until the corresponding independent agent/session/human evaluation is actually performed and a transcript is retained. A retrieval probe, subprocess, template, or one model's self-scoring does not establish those capabilities. In particular a new Python process is not an independently continued AI session, and a coding-task outline is not an implemented and tested change.

Negative cases have empty relevant sources and explicit abstention rules. Unlisted paraphrases retain nonempty relevance gold. Source disagreement requires both references and no invented winner. Source dates, former-state wording, agreement between observations, or a newer proposal do not authorize lifecycle promotion. Current settings from another project may not silently fill an evidence gap.

Do not copy any synthetic source into live `sources/raw/`, the live manifest, or production wiki pages. A runner may construct disposable hash-backed workspaces under `tests/` using existing bounded APIs, preserve raw bytes and clean up only its own temporary directory. The dataset contains specifications, **no PASS results**. Real source intake and human-confirmed gold require a separately approved pilot.
