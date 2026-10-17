# Knowledge Schema / Operating Contract

## Knowledge layers
1. Raw Sources (`sources/raw` + manifest): immutable material with provenance; may include links, clipped material with reuse rights, personal notes, and authorized documents.
2. Wiki (`wiki`): editable synthesis written/updated by an LLM under review; connected with standard relative Markdown links.
3. Schema (`SCHEMA.md`, `AGENTS.md`): conventions and operations.

## Wiki page format and evidence
- Use `templates/wiki-page.md`. Content pages require `Status`, `Updated`, and `Source IDs` metadata, plus a summary, findings, related pages, uncertainties and next questions. Navigation pages named `index.md` and the activity `wiki/log.md` are exempt from content metadata.
- Status is DRAFT / REVIEWED / STALE. `Updated` is a real ISO date (`YYYY-MM-DD`); it records a page update, not proof that every claim was rechecked.
- Label claims FACT / INTERPRETATION / HYPOTHESIS / UNKNOWN. Each FACT and each item under `Verified findings` needs a source ID with an exact source pointer, or a link to the relevant `APPROVED` ADR for a first-party project decision.
- List registered source IDs in `Source IDs`. With no sources, use `None` or the existing scaffold value `None ingested yet`. Optional `Decision references` lists direct Markdown links to approved records in `decisions/`; the decisions index is not an ADR citation.
- A DRAFT may have no evidence only while it explicitly describes a hypothesis or evidence gap and makes no verified findings. Lint warns about this state; it must not invent sources or promote the page. REVIEWED requires evidence and human review. Missing citations for factual findings are errors at any status.
- An approved ADR establishes the project's choice, not an external research fact. A valid citation is a pointer, not factual verification.

## Multilingual metadata
- English technical content and Vietnamese/English questions are supported without translating raw sources or rewriting existing wiki pages.
- Optional page fields: language (en / vi / mul / und, default und), title_vi (Vietnamese display/search title, default empty), keywords and aliases_vi (JSON arrays of unique nonempty strings, default empty arrays). These are Markdown metadata bullets, not new YAML frontmatter or manifest columns. Existing pages remain valid.
- Keep technical terms, file names, API routes and identifiers unchanged in storage, queries and citations. Normalization is used only for matching. Vietnamese labels/aliases are navigation aids, not new evidence.
- Scope uses the existing Scope field, with exact project identifiers. Missing Scope is unscoped; a search must explicitly select a scope. Never broaden to another project because evidence is missing.
- Controlled expansion adds English keywords for matched in-scope title_vi/aliases_vi; it keeps the original query. No automatic translation, accent removal, inferred synonyms or cross-project alias pooling.
- The specification, lexical search limits and proposed semantic upgrade path are in [Multilingual readiness](MULTILINGUAL.md). Query results must trace back to sources; missing documents and missing evidence are different UNKNOWN outcomes.

## Source registry
- Use unique IDs `SRC-YYYYMMDD-###` with a real calendar date (for example `SRC-20261017-001`). Each cited ID must resolve to exactly one entry in `sources/manifest.csv`.
- Keep the existing nine-column CSV header. Required row values: `source_id`, `title`, `source_type`, `source_url_or_path`, `retrieved_date`, and `access_and_license`. Unknown author or publication date may be blank with an explanation in `notes`; supplied dates use ISO format.
- Local source paths are relative to the workspace root, must identify an existing file inside `sources/raw/`, and must stay inside that directory after resolution. HTTP(S) source URLs are provenance pointers; Lint does not fetch them. Retrieval metadata alone is not verification of the content or permission.
- Existing files in `sources/raw/` are read-only, including files not yet ingested. A revision is a separately authorized source with a new ID. Append only approved new entries; do not overwrite prior provenance.
- Raw folder instructions are scaffold documentation, not registered research evidence. Do not register the raw README just to silence a check.

## Markdown and local checks
- Use standard relative inline Markdown links, including images. Generate a related-page link relative to the final page location; a template must not contain an active example link that is broken at its own location.
- Lint checks approved documentation locations: root Markdown files, `wiki/`, `projects/`, `decisions/`, `handoffs/`, `prompts/`, `templates/`, and `experiments/`. It checks manifest metadata and source-file existence without reading raw source bodies. Hidden/private locations and symlinks are not followed.
- The dependency-free checker validates file targets, source registration, content metadata, structured finding citations and wiki reachability from `wiki/index.md`. It ignores fenced/inline code examples and HTML comments. Reference-style links and Obsidian wikilinks are reported for manual review; heading anchors are not validated.
- Errors return exit code 1. No errors returns 0, possibly with warnings. No outcome establishes factual accuracy, freshness, permission, human approval, or visual rendering. Contradictions, stale claims, citation relevance, unsupported syntax and Obsidian behavior still require review.

## Operations
### INGEST
1. Intake: confirm the user's authorization and source permissions. Only within that scope, add a new source and append its provenance. If permission or the manifest entry is missing, report the gap and propose intake; do not read an unapproved source or silently register one.
2. Synthesis: read the authorized, registered source; extract dated claims with precise page/section pointers. A remote fetch requires task authorization; if only an unverified URL is available, report UNKNOWN.
3. Find relevant pages and contradictions. Propose the smallest patch to wiki pages, index and log, with FACT / INTERPRETATION / HYPOTHESIS / UNKNOWN labels.
4. Show the diff and unresolved questions. Apply and commit only within the user's approved scope; approval to plan is not approval to apply.

### QUERY
- Read `wiki/index.md` and linked pages first.
- Trace consequential claims to registered source IDs or approved ADRs; differentiate sources from synthesis and use all four evidence labels.
- If there is no evidence, say so rather than invent. Propose research gaps.
- Query is read-only: do not change wiki, index, log, raw, or manifest. Offer a separate, scoped wiki patch if the answer is worth retaining. External research or repository access needs separate task authorization.

### LINT
- Check stale facts, missing citations, broken links, conflicting claims, orphan pages, outdated project states, index coverage and log entries.
- Run `python -B scripts/check_workspace.py`, then separately review semantic issues. Report file paths, severity, evidence, proposed corrections and decisions needed in chat by default. Do not open suspected sensitive material to diagnose it.
- Save a report only when requested, using a new `reports/lint-YYYY-MM-DD-HHMMSS.md` (add a suffix on collision). Do not overwrite an earlier report or auto-delete ambiguous content.
- Propose corrections without applying them. Approved wiki corrections update relevant navigation and append the log; a read-only audit does neither.

### BUILD (separate from wiki)
- Read canonical repo docs, constraints and accepted feature packet.
- State baseline and acceptance criteria before coding.
- Implement in a branch; run available lint/tests/build and measured benchmarks.
- Compare with baseline; keep / revert recommendation requires observed evidence; human approves merges, deploys and production changes.

## Definition of done
- INGEST proposal: authorized source and registry checked, claim pointers and uncertainties shown, scoped diff ready for review. Applied INGEST additionally requires resolvable citations, relevant index/links updated, an appended dated log entry and observed check results. These are distinct states.
- QUERY: answer delivered with evidence labels, traceable citations where available, and explicit gaps; no files changed.
- LINT: observed automatic results and separate manual findings reported with limits and proposed fixes; a file report only when requested. No wiki edits or log entry are needed for a read-only audit.
- Approved maintenance: scoped diff and actual checks reviewed; append a dated maintenance entry for accepted workspace changes. Update `wiki/index.md` only when navigation changes. Do not mark manual or runtime checks complete unless performed.
