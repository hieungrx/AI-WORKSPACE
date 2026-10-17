# Phase 5 — Scalability and V1.1 Pilot Readiness

First-party engineering assessment. Discovery baseline: 55e6e1f on workspace/initialize. Read current AGENTS, README, SCHEMA, PROFILE, source/governance/security contracts, prompts, wiki navigation/history, implementation and Phase 4 results. Prior 163-test/60-query results were observed in their report; they are not new performance measurements. No production source is authorized by this task.

## Architecture assessment

- Markdown pages remain authoritative, with immutable raw snapshots and append-only CSV/provenance. No schema or manifest-column migration is needed for this phase.
- Navigation supports directory indexes through ordinary relative links. The current Ingest contract additionally requires a direct root-index link to each changed page; the load recipe keeps one explicitly active review target. Sharding all future maintenance behind indirect links would require a separately reviewed Ingest contract change, not an assumption that it already works.
- Queries scan selected-scope wiki metadata, validate lifecycle/approval/citations and hash the source registry's raw snapshots. Exact scope and explicit cross-project context remain mandatory. They perform lexical matching only; no persistent full-text index exists.
- Strict Lint traverses approved documentation, builds link reachability, checks page identities/lifecycle/current decision slots, validates source relationships and hashes raw bytes. Full Lint is intentionally workspace-wide. Warning counts on synthetic drafts are expected and do not imply verified knowledge.
- Ingest writes an explicit page/index/log bundle, guarded by target hashes, ownership and recovery. One-page updates do not regenerate all wiki files. Source admission remains a separate immutable checkpoint. Its auditing/read cost still grows with corpus size.
- CSV/JSONL registries, Markdown navigation and append-only history grow linearly. Before this phase, per-page registry parsing multiplied validation work by the number of pages. Duplicate source/path and reverse-wiki scans also repeated work during Query. These are code-derived complexity observations; actual timings and call counts belong to the measured reports.
- Registration logically appends but physically journals/replaces complete CSV/ledger files and retains before-images. Many sequential admissions can accumulate quadratic copying/backup volume. Long source-revision chains can also repeat lineage traversal. These are inferred risks, not measured admission throughput or storage costs; the load recipe uses independent version-1 sources and does not simulate 10,000 sequential admissions. Backup retention requires separate human review; this phase deletes no retained recovery history.

## Reproducible measurements

~~~text
python -B scripts/benchmark_scalability.py --sizes 100 1000 10000 --trials 1 --timeout 600 --output reports/<new-name>.json
python -B scripts/benchmark_scalability.py --sizes 100 --trials 1 --profile --skip-quality --output reports/<new-profile-name>.json
python -B scripts/validate_scalability.py --benchmark reports/<measured-name>.json --baseline reports/<baseline-name>.json --output reports/<new-assessment-name>.json
python -B -m unittest discover -s tests -v
python -B scripts/check_workspace.py --integrity --security
~~~

Use a new output basename. Existing reports are never overwritten. The benchmark creates only owned tests/fixture-scale-*/workspace trees and deletes only those temporary trees after the run. The production raw/manifest/wiki and user Obsidian work are excluded. The dataset is deterministic for its recipe, size and date; reports include its aggregate SHA-256 and logical file/byte counts.

Each size means N wiki knowledge documents plus N unique immutable-style synthetic raw snapshots, ten scope indexes and small metadata/TEST_ONLY validation records. Text uses invented English protocol/queue observations, Vietnamese aliases, registered source IDs and precise Evidence-section citations. IDs span dates after 999 per day; 10,000 entries do not violate the existing format.

The three-digit suffix has 1,000 possible strings (000–999) per encoded date; this recipe uses positive counters 001–999 and advances dates. The synthetic corpus spans eleven dates; it does not prove 10,000 same-day admissions with genuine date assignment. Dense linking, deep directories/revision chains, large PDFs/binary inputs, very long logs, simultaneous production writers and corpora above 10,000 are untested operating shapes.

Fixture construction publishes complete synthetic registries directly. It is test provisioning, not a claim that 10,000 production admissions or per-source approval operations were benchmarked. Navigation generation measures the fixture's hierarchical index renderer; a production index generator does not exist and its throughput is NOT MEASURED.

Metrics distinguish:

- Fresh-process operation time, excluding interpreter startup/imports. Path.open/Path.stat instrumentation counts some filesystem calls; it is not a complete OS syscall/physical-I/O trace. OS disk cache is uncontrolled, so no cold-cache or production-SLA claim is made.
- Manifest lookup includes reading/validating CSV and selecting one ID. Query includes integrity, scope, metadata, security and citation gates, not just string matching.
- Strict validation includes security/source checks. Incremental cost measures one actual Ingest commit; hashing all fixture resources before/after verifies only the selected page and appended log changed. The reviewed unchanged root index is still republished as part of the current bundle.
- The retry returns UNCHANGED. A newly added keyword becomes visible without a full index rebuild. Raw tamper with unchanged size/mtime still returns MISSING_EVIDENCE. Interruption returns RECOVERY_REQUIRED, and authorized recovery restores exact fixture hashes.
- Windows process-lifetime peak working set includes imports and correctness checks, not just timed-operation allocations. Logical bytes/file/directory counts are measured; physical allocation, disk wear, memory under other workloads and filesystem cache memory are NOT MEASURED.
- Median/max use only completed trials; with one trial these equal the single observation. No p95, throughput, concurrency capacity or confidence interval is inferred. Timed-out attempts are NOT RUN for completed latency/correctness, with the actual attempt duration retained.
- The timeout bounds the complete worker, including imports, snapshots, retries and post-write evidence checks. A timed function may have returned before a later check exhausts that budget; without a complete verified worker result, its latency/correctness is still NOT RUN. English/Vietnamese runs occur in order with uncontrolled OS cache/I/O, so their timing difference is not evidence of a language-specific algorithm effect.
- LLM tokens, model latency, API billing and monetary local CPU/storage costs are NOT MEASURED. The benchmark calls no LLM API; this does not establish the cost of this chat or a future pilot.

## Observed results — 2026-10-18

Overall verdict: **CONDITIONAL**; correctness within the executed probes: **PASS**. The fresh regression run passed 174/174 tests, including all 163 earlier tests. The live workspace has zero registered sources and only its existing draft NO_EVIDENCE warning. These are structural/workflow results, not factual verification.

Each timing below is one completed observation on Windows 11 / Python 3.13.0, with uncontrolled OS cache:

- 100 documents: English Query 0.825s; Vietnamese Query 0.803s; strict Lint 2.003s; one-page Ingest 1.695s.
- 1,000 documents: English Query 12.306s; Vietnamese Query 10.486s; strict Lint 19.825s; one-page Ingest 9.274s.
- 10,000 documents: English Query 280.297s; Vietnamese Query 103.083s; strict Lint 282.187s; one-page Ingest 110.825s. Its unchanged retry still took 113.846s because auditing remains necessary.

At 1,000 documents the pre-change strict Lint took 43.282s and English Query 15.312s. Manifest opens fell from 1,002 to 3 per Lint and from 102 to 1 per Query. This supports removing redundant reads; it does not establish a stable speedup distribution. No 10,000-document baseline was run or extrapolated.

Source lookup took 3.29ms / 15.73ms / 274.27ms at the three sizes. Fixture navigation generation took 7.74ms / 43.02ms / 285.93ms. At 10,000 documents the corpus contained 20,017 files, 26 directories and 44,949,915 logical bytes; strict Lint's worker peak working set was 178,671,616 bytes (170.39 MiB). CSV lookup is not the observed dominant delay; raw hashing and path/filesystem scans remain material. A new database alone is not justified by these measurements.

All three sizes rejected wrong-scope lookup, detected same-size/mtime source tampering, blocked injection/protected overwrites/path traversal, and recovered an interrupted write with every fixture content hash restored. Every incremental run changed only its selected page and appended log, exposed the new keyword without rebuilding, and returned UNCHANGED on retry. Large-corpus correctness does not establish acceptable interactive latency.

The measured 100-document case is the only tested size meeting the provisional 2-second Query budget. Recommend a separately authorized **25–100-page V1.1 pilot**, starting small and measuring the actual content mix; the lower starting point is a conservative proposal, not a separately measured capacity. No real ingestion begins in this phase.

Evidence: [final assessment and individual test results](reports/scalability-phase5-assessment-2026-10-18.md), [raw measured trials](reports/scalability-phase5-2026-10-18.json), [pre-change baseline](reports/scalability-phase5-baseline-2026-10-18.json), and [separate baseline profile](reports/scalability-phase5-profile-2026-10-18.json). Profile overhead is excluded from the ordinary latency comparison. API cost, tokens, p95, concurrent capacity, Obsidian UI and real admission throughput remain NOT MEASURED.

## Minimal measured improvements

The saved baseline and profile identify repeated manifest reads plus filesystem/path checks. Changes remain inside existing functions:

1. Share a validated immutable source-ID set within one governance audit or Query. No result is cached between operations. A subsequent registry/metadata edit is read again.
2. For hash-backed Query, use the complete source audit once instead of first repeating the legacy CSV/raw-path scan. Legacy unbaselined sources keep the original compatibility path.
3. Skip only Query's redundant reverse-wiki relationship scan, since selected pages are subsequently validated for source membership, lifecycle, scope and citations. Full source audit/Lint/registration retain relationship checking by default.

Raw hashes, provenance, version lineage, source errors, approval hashes, restricted scopes, suspicious-content rejection, generation checks and rollback are retained. No mtime-only source-integrity shortcut, persistent metadata cache, full-text engine or worker service is introduced. New regression tests specifically check operation-local reuse, registry invalidation, default source relationships and same-size/mtime tamper.

## Search migration interface — specification only

Keep the existing Query contract as the compatibility boundary. A future adapter receives original query, exact scope, requested top_k, include_history, explicit cross_refs and authorized scopes. It returns status/message, preserved query/scope, declared expansions, ordered matches and blocked candidates. Every candidate retains path/page_id, actual scope, lifecycle/kind, decision authority, freshness/conflicts, trust label and source/ADR citations with pointers/integrity/version lineage. Report backend/version, snapshot generation and measured timing separately.

No adapter may return stale-index content as current truth, broaden scope to improve recall, treat a rank as verification or bypass live evidence/security/approval gates. If the snapshot changes or recovery is pending, fail closed. If evidence is absent, abstain. The current helper returns its highest lexical tier; the proposed top_k interface does not mean top-k ranking is now implemented.

Level 1: current Markdown navigation + exact metadata/source lookup. Keep Git diffs, explicit ownership and human review.

Level 2: optional local full-text derived index, only after a separately approved experiment. Build from permitted wiki fields; bind every record to content SHA-256 and source/approval dependencies. Detect additions/deletions/renames and policy changes, apply deltas atomically, and invalidate on generation/permission/scope/schema mismatch. Rebuild is a recovery fallback; ordinary updates should touch affected records. Live citation/hash checks still apply, so a full-text index alone cannot remove integrity-scan overhead.

Level 3: optional multilingual embedding/hybrid experiment if independent Vietnamese paraphrase recall remains inadequate after reviewed alias improvements. Preserve English originals/technical identifiers and measure recall/citation validity/isolation/abstention against the unchanged Phase 4 gold plus unseen questions. Do not install embeddings/vector storage in this phase.

Level 4: reranking/evaluation only if Level 2/3 measured relevance errors justify it. Keep deterministic gates before answer use; report model usage and actual cost only if observed. Test failure/degraded behavior as well as successful ranking.

## Upgrade triggers and V1.1 recommendations

All user-experience thresholds below are **PROVISIONAL**, because the user has supplied no latency SLA, concurrency target or real corpus. They are experiment/pilot gates, not observed system limits.

- Full-text indexing: consider an isolated experiment when pilot questions repeatedly exceed a provisional 2-second interactive budget and profiling attributes a material share to lexical scanning. Present hash/path auditing costs separately; adding an index is not evidence those disappear.
- QMD: require an explicit product choice, a reproducible comparison with the standard-library baseline and measured improvement on the same independent workload without citation/scope/regression losses. No document-count threshold alone justifies QMD.
- Multilingual embeddings: use the observed Phase 4 unlisted-paraphrase misses as research motivation, not evidence of model quality. A provisional recall target of 95% on a larger independent paraphrase set needs human agreement; test against the current 93.75% synthetic document Recall@5 definition without changing gold to suit the retriever.
- Database metadata store: require measured CSV/JSONL parsing or concurrent write conflicts to dominate latency/operations after operation-local reuse. Compare a bounded prototype before choosing a database; file count alone is insufficient. No database is introduced here.
- Background processing: consider only when measured authorized intake/review queues or full validation exceed an agreed foreground budget. Provisional 30-second maintenance budget is for discussion; preserve exclusive write ownership, explicit cancellation, journal recovery and visible stale-index state.
- V1.1 pilot: use the largest actually measured size meeting the agreed interactive budget; do not infer capacity above 10,000 or from generated bytes alone. Begin with a small, separately authorized source batch, human-reviewed permissions and explicit project scopes. Reuse Phase 4 gold, capture actual operation latencies/abstentions and periodically run full integrity/security Lint. Define rollback and stop on hash, scope, approval or recovery errors.

The final measured assessment/report determines the practical recommendation. These are proposals, not approved architectural decisions, automatic source authorization or V2 implementation. Broader host permissions, real LLM answering and Obsidian visual behavior retain their prior limitations.
