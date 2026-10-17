# AI-WORKSPACE V1 — Multilingual Readiness

This is a first-party operating specification. It does not assert external research findings. English documents remain English; questions may be Vietnamese or English. Raw sources and the existing nine-column source manifest are unchanged.

## Metadata specification

Use the existing Markdown metadata bullets before the first level-two heading. Four optional additions:

- language: en (English), vi (Vietnamese), mul (mixed), or und (unknown/default).
- title_vi: optional Vietnamese display/search title. Default: empty string. It is not a translation of the full page or independent evidence.
- keywords: JSON array of unique nonempty strings. Prefer canonical English technical phrases and exact identifiers.
- aliases_vi: JSON array of unique nonempty Vietnamese navigation phrases. Include alternate wording only when explicitly curated.

Keep Scope as the exact project identifier. Missing Scope means unscoped, never an inferred project. Missing new fields default to und, empty title and empty arrays; no migration or wiki-wide translation is required. Source IDs, dates, page status and citation rules remain in force. The linter checks new fields only when provided.

Example metadata only; not a real knowledge entry:

~~~text
- **Scope:** demo-a
- **language:** en
- **title_vi:** Đặt trước sản phẩm
- **keywords:** ["reservation", "reserveListing()", "GET /api/listings"]
- **aliases_vi:** ["đặt trước sản phẩm", "giữ món"]
~~~

JSON arrays avoid ambiguous comma-separated lists. Values retain their original spelling, punctuation and technical identifiers. This V1 format does not add YAML frontmatter or a dependency on Obsidian properties.

## Controlled query expansion

1. Require an explicit scope. If a question has no project context, clarify the scope; do not search another project as a fallback. Global and unscoped are explicit scopes, not additions to every search.
2. Preserve the complete original question. Normalize a matching copy with Unicode NFC, casefold and collapsed whitespace. Keep accents; do not stem words, strip punctuation, translate identifiers or rewrite the stored question.
3. Inspect only the selected scope's terms for matching/expansion. Match whole phrases with word boundaries, including exact filenames, API routes and identifiers. A curated aliases_vi or title_vi match adds that page's English keywords, or its English title if keywords are empty.
4. Expansion is additive and local to the matched document. Do not pool synonyms across projects, recursively expand aliases or invent English terms. Unlisted paraphrases may legitimately return NOT_FOUND.
5. Rank exact metadata matches above metadata phrases contained in the question, then exact query phrases in the body. Scores are ordinal lexical ranks 3/2/1, not probabilities. Return only the highest rank; ties are AMBIGUOUS and require refinement.
6. Return source pointers, not generated answers. A result needs a source ID listed in page metadata, cited in a structured factual finding as [SOURCE_ID, exact pointer], and registered against an available local raw file. Metadata-only citations, unknown IDs, missing source files and unavailable remote evidence yield MISSING_EVIDENCE. Phase 1 provenance records additionally require matching raw SHA-256; Query reads bytes for this check without decoding, translating or printing them. Legacy citations are marked LEGACY_UNHASHED. URLs are never fetched. See [Source integrity](SOURCE_INTEGRITY.md).
7. NOT_FOUND means no matching document in that scope; MISSING_EVIDENCE means a document matched without adequate local source pointers. Report UNKNOWN in both cases, without guessing or silently widening the search.

The lexical tool reports page status and does not certify source relevance, source-pointer accuracy, human review, factual correctness or freshness. It currently resolves registered local source citations; approved ADR reasoning remains part of the agent Query workflow and is not automatically verified by this tool. Scope filtering is retrieval isolation, not a filesystem authorization system.

## Usage and validation

~~~text
python -B scripts/query_workspace.py --scope demo-a --query "đặt trước sản phẩm"
python -B -m unittest discover -s tests -v
python -B scripts/validate_multilingual.py
~~~

The first command searches the live workspace read-only. It may return NOT_FOUND while the wiki is still a scaffold. The validation runner explicitly selects synthetic fixtures under tests/fixtures/multilingual; they are not real ingested knowledge. The runner prints actual outcomes; saving a report uses an explicitly supplied new output path and refuses to overwrite an existing report.

The paired suite covers exact technical keywords, bilingual aliases, cross-language matching, project isolation and missing evidence. Unit tests additionally cover metadata compatibility, Unicode, ambiguity, identifier preservation and read-only behavior. Test counts and measured results belong in the generated report, not in an assumed PASS statement here.

## Proposed upgrade path — not implemented

1. Keep the lexical reference baseline and paired queries as a repeatable evaluation set. Add reviewed terminology and natural, previously unseen paraphrases before changing the search method.
2. After user approval and an actual corpus, evaluate better lexical ranking against this baseline. Measure per-language retrieval, scope leakage, missing-evidence handling and citation availability; do not optimize only successful examples.
3. If paraphrase misses justify semantic retrieval, separately propose a multilingual embedding or hybrid experiment with model, privacy, cost and rollback criteria. QMD, RAG and vector storage are not prerequisites for this V1 and are not installed here.
4. Preserve scope filtering before retrieval/ranking, immutable raw sources, stable source IDs, exact technical identifiers and the citation gate under any later method. A semantic similarity score must not manufacture evidence.
5. Approve migration only after measured gains on held-out queries without cross-project leaks or weakened missing-evidence behavior. No semantic implementation or architecture decision is approved by this specification.
