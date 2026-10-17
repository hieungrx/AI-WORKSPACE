# Phase 4 — Knowledge Workflow Reliability

First-party specification for testing V1's guarded Ingest → Query → Lint APIs. Discovery baseline: 6097642 on workspace/initialize. Phase 1/2 PASS reports and Phase 3's guarded PASS / overall CONDITIONAL report were inspected. The inherited host-permission limitation remains; this phase does not change host settings or claim full agent containment.

## Reproducible synthetic benchmark

Run from this workspace using Python's standard library:

~~~text
python -B scripts/validate_workflows.py
python -B -m unittest discover -s tests -p test_workflow_reliability.py -v
python -B scripts/check_workspace.py --integrity --security
~~~

To retain observed evidence, add --output reports/<new-name>.json to validate_workflows.py. The redacted, exclusive report writer also creates companion Markdown and refuses to overwrite past results. Console-only evaluation does not change the live wiki/log, sources or registry. Temporary test workspaces are created under tests and cleaned up by the runner.

- tests/fixtures/workflow/corpus.json: independent English synthetic evidence, pages, scopes, declared conflicts and decision history. It contains no production fact, real URL or external project configuration.
- tests/fixtures/workflow/queries.json: 30 hand-authored Vietnamese–English pairs; expected document paths, source IDs, scope, lifecycle, citation pointer, abstention signal and separate document relevance gold. Gold is never derived from retrieval output.
- tests/workflow_support.py: adapter that admits immutable raw snapshots, registers sources and calls actual ingest_registered; it retries every wiki plan, then applies synthetic lifecycle transitions. ADR files and TEST_ONLY approval assertions are fixture setup, not an implemented auto-approval feature.
- tests/workflow_benchmark.py: executes actual Query and strict Lint, verifies citations against fixture raw bytes/headings and computes metrics. Alternative retrieval can reuse the corpus/gold without changing expected results.
- tests/test_workflow_reliability.py: actual-path failure injection, retry/recovery, protected updates and deliberate Lint faults; includes the paired benchmark.

English technical material is retained as written. Vietnamese aliases are curated navigation metadata. Q25 and Q29 deliberately test meaningful unlisted paraphrases, so correct lexical abstention can coexist with a recall miss. Q26 tests an incorrect translation; the helper must not invent a row-locking expansion for table locking. Technical spelling, punctuation, routes, headers, filenames and identifiers remain unchanged.

## Ingest contract and recovery

1. Authorize the synthetic/local intake explicitly. Use create_raw_snapshot and register_source; existing raw and provenance are immutable. Equal registered bytes deterministically reuse the original source identity. Source admission is its own durable checkpoint.
2. Review exact draft page bytes, index, append-only log and expected target SHA-256 values. Call ingest_registered with exact scope, authorized=True and apply=False for a proposal; apply=True uses the owned/recoverable wiki transaction.
3. New synthesis stays draft. Existing draft edits must preserve scope, lifecycle history, identity, existing source IDs/pointers and recorded conflicts. Important findings need registered [source_id, exact pointer] citations. Index links must retain prior targets and include changed pages. A changed page requires an appended log entry; review entry dates/content manually.
4. Changed non-draft knowledge returns PROTECTED_KNOWLEDGE_UPDATE. Create a separately reviewed draft or use the authorized lifecycle process before changing protected content. Ingest cannot reset verified history or resolve disputes. General maintenance exceptions still require direct human task scope and diff review.
5. Replay of an identical plan, or a fresh plan with identical page/index content, returns UNCHANGED and writes no duplicate log entry. Reuse the reviewed plan when retrying. Changed stale versions return CONCURRENT_CHANGE; do not regenerate hashes to overwrite newer user changes.
6. Normal write failures restore the exact wiki/index/log before-images and retain admitted sources. A process interruption blocks Query with RECOVERY_REQUIRED. Follow [authorized recovery](SECURITY_POLICY.md), reconcile newer user changes if any, then retry the reviewed plan. Never clear another owner's lock or delete source history.

Synthesis does not execute source text, fetch URLs, approve claims or create model-generated decisions. Authorization and source permissions still come from the human task, not from the input document. See [source integrity](SOURCE_INTEGRITY.md) and [governance](KNOWLEDGE_GOVERNANCE.md).

## Query contract and measurement

Use query_workspace.py with an explicit --scope and --query; --cross-ref requires a declared edge and explicit task scope; --include-history is opt-in. Query and Lint are read-only. Keep draft/proposed/unverified results separate from current verified decisions. Conflicts retain both citations and return DISPUTED. NOT_FOUND and MISSING_EVIDENCE signal UNKNOWN, never permission to invent an answer or broaden project scope.

The current helper performs literal keyword/alias matching, returns the highest lexical score tier and reports controlled English expansion terms. It does not translate arbitrary questions, run a second semantic search with expansions or generate answers. A tie is AMBIGUOUS. The benchmark records retrieval abstention signals; actual LLM answering/abstention is NOT MEASURED.

- Retrieval Recall@5: per-query fraction of independently relevant document paths found among the first five actual highest-tier candidates (matches plus blocked, ordered score descending/path ascending), macro-averaged over nonempty relevance gold. Negative no-relevance controls are excluded; Q25/Q29 remain in the denominator. Also report Vietnamese/English separately. This metric measures retrieval, not usable evidence or factual truth.
- Citation validity: valid returned references / references checked. Check source ID, registered local path, raw SHA-256, expected pointer and actual fixture heading. Pointer syntax or a hash alone cannot establish semantic relevance or correctness.
- Cross-project leakage: queries with an undeclared/unrequested foreign-scope result / all executed queries. Explicit cross-project context is allowed only for the expected target and remains context.
- Duplicate ingestion rate: repeated synthesis plans that write again or change page/index/log bytes / repeat attempts. Source registration deduplication is recorded separately. These controlled retries are not a production traffic estimate.
- Schema pass rate: valid corpus content pages / corpus content pages under strict deterministic Lint. Deliberately malformed negative fixtures are separate fault-detection tests, not valid-corpus failures. Warnings do not equal schema errors or verified truth.
- Workflow failure rate: unexpected admission/synthesis/query-contract outcomes / executed first admissions, first wiki synthesis operations and queries. Expected adversarial/failure-injection errors are reported separately; do not count successful rejection as accidental failure. Recovery and deduplication have their own observations.
- Automatic translation quality, semantic retrieval, generated answer accuracy, factual verification and real production rates: NOT MEASURED.

No expected or actual PASS is inferred from an implementation plan. Each report includes observed statuses, metrics with denominators, unit results, warnings and fixture hashes.

## Lint boundary and compatible metadata additions

Metadata remains Markdown bullets; YAML frontmatter is unsupported and rejected for knowledge pages, including malformed YAML that would otherwise be silently ignored. No YAML dependency or schema_version is introduced. Existing valid metadata and nine-column manifests remain unchanged.

- Optional page_id: globally unique lowercase identifier across wiki content and canonical ADRs, matching `[a-z0-9][a-z0-9._-]{0,95}`. Missing IDs retain path-based identity for old pages. Duplicate IDs are errors; normal synthesis cannot silently change an existing ID.
- Optional decision_key: the same identifier syntax, naming an exclusive decision slot. Two human-approved, effective, current/non-historical records with the same exact scope and key produce CURRENT_DECISION_COLLISION. Superseded/history, proposed, future-effective or other-scope records are not current collisions. Query fails closed for a selected scope with such a collision. Lint cannot infer decision domains from prose or choose a winner.
- UNREVIEWED_KNOWLEDGE warns on canonical draft/unverified content even when cited. REVIEW_DUE flags explicit elapsed review deadlines; age alone never changes lifecycle or deletes history.
- Broken links, unknown/unlisted sources, missing finding pointers, lifecycle errors, orphan pages and duplicate index targets are deterministic structural findings. Heading anchors, exact pointer meaning, unlabelled claims, textual contradictions, unkeyed decisions and actual Obsidian rendering still require manual/LLM review.

New optional fields require no bulk migration. If an existing page uses bare finding IDs or unsupported YAML, propose a reviewed correction using known evidence; never invent a pointer or silently rewrite a raw source. Preserve prior reports and historical decisions.

## Remaining limits and recommended follow-up

The corpus is deliberately small and synthetic. Results do not predict production recall or model behavior. Curated aliases handle tested cross-language cases; arbitrary paraphrases and semantic search are unsupported. First extend reviewed terminology and unseen independent questions if more coverage is needed. Any semantic retrieval experiment remains a separately authorized future proposal; no QMD/RAG/vector store is installed.

The Phase 3 API/host boundary, human identity assertion, incomplete injection patterns, unsupported Markdown and physical power-loss limitations remain. No real sources, external repository, secret file, deployment, push or merge are part of this validation. No Phase 5 work is authorized by a passing or conditional Phase 4 result.
