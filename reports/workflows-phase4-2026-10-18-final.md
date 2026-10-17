# Phase 4 — Knowledge Workflow Reliability

**Verdict: CONDITIONAL**. Guarded workflow contract: **PASS**.
The guarded workflow can pass while lexical paraphrase recall, semantic review, full agent answering and host containment remain limited or unmeasured.

Observed at UTC: 2026-10-17T17:27:18.377175+00:00. Baseline: 6097642, branch workspace/initialize.
Executed: 163 tests, 163 PASS, 0 failures, 0 errors, 0 skips.
Only first-party repository files and TEST_ONLY synthetic data were used; no real knowledge or secrets were imported.

## Audit and implemented fixes

Read: AGENTS/README/SCHEMA/PROFILE, security/governance/source reports and contracts, relevant prompts, index/log and actual Python implementation/tests.
- Initial console reproduction on the pre-fix implementation ran 3 new tests: 2 failures and 1 error. A verified page could be reset by Ingest, identical replay raised CONCURRENT_CHANGE, and Lint accepted a bare source ID without a pointer.
- Normal wiki synthesis now protects non-draft knowledge, scope, lifecycle history, prior source pointers and conflicts. Review/transition or a new draft is required for protected updates.
- Exact retries and fresh plans with unchanged pages/index return UNCHANGED without adding duplicate history. Stale changed targets remain conflicts.
- Ingest checks pointer syntax, index retention and appended log before writing; lower-level wiki transactions enforce protected-state updates under ownership.
- Lint adds optional page identity uniqueness, unsupported YAML detection, duplicate index targets, unreviewed status warnings and explicit same-scope current decision slot collisions. Query fails closed on detected identity/slot collisions.
See [workflow specification and reproduction](../WORKFLOW_RELIABILITY.md). No framework, database or new dependency was added.

## Actual benchmark metrics

Pairs: 30; actual queries: 60. Query/Lint read-only: True.
Corpus, hand-authored relevance/expected scopes/states/citations/abstentions and fixture hashes are in the companion JSON and tests/fixtures/workflow.
- retrieval_recall_at_5: {"value": 0.9375, "queries_with_relevance_gold": 48, "definition": "Macro document Recall@5 over actual highest-tier candidates (matches + blocked), ordered by score/path; excludes zero-relevance cases. Retrieval does not imply answerability.", "vi": {"value": 0.9166666666666666, "queries_with_relevance_gold": 24}, "en": {"value": 0.9583333333333334, "queries_with_relevance_gold": 24}}
- citation_validity: {"numerator": 53, "denominator": 53, "value": 1.0}
- cross_project_leakage: {"numerator": 0, "denominator": 60, "value": 0.0}
- duplicate_ingestion_rate: {"numerator": 0, "denominator": 13, "value": 0.0}
- duplicate_registration_rate: {"numerator": 0, "denominator": 17, "value": 0.0}
- schema_validation_pass_rate: {"numerator": 16, "denominator": 16, "value": 1.0}
- workflow_failure_rate: {"numerator": 0, "denominator": 90, "value": 0.0}
- answer_generation_accuracy: "NOT MEASURED"
- cross_language_semantic_search: "NOT MEASURED (not implemented)"
- automatic_translation_accuracy: "NOT MEASURED (not implemented)"
- semantic_factual_verification: "NOT MEASURED"

Observed query outcomes: {"AMBIGUOUS": 2, "DISPUTED": 2, "FOUND": 39, "MISSING_EVIDENCE": 2, "NOT_FOUND": 15}.
Recall includes the negative relevance controls Q25/Q29; a correct NOT_FOUND lexical signal can still be a retrieval miss. Blocked evidence candidates count as retrieved documents, never usable answers.
Citation validity checks identity, local path, recorded SHA-256 and the actual synthetic Evidence heading. It does not verify claim meaning.

## Paired retrieval evidence

- Q01 vi: FOUND; contract PASS; Recall@5 1.0; query khóa chống lặp; paths ["wiki/idempotency.md"]
- Q01 en: FOUND; contract PASS; Recall@5 1.0; query Idempotency-Key; paths ["wiki/idempotency.md"]
- Q02 vi: FOUND; contract PASS; Recall@5 1.0; query Cơ chế khóa chống lặp hoạt động thế nào?; paths ["wiki/idempotency.md"]
- Q02 en: FOUND; contract PASS; Recall@5 1.0; query How is Idempotency-Key handled?; paths ["wiki/idempotency.md"]
- Q03 vi: FOUND; contract PASS; Recall@5 1.0; query khóa hàng; paths ["wiki/locking.md"]
- Q03 en: FOUND; contract PASS; Recall@5 1.0; query row locking; paths ["wiki/locking.md"]
- Q04 vi: FOUND; contract PASS; Recall@5 1.0; query Giải thích SELECT ... FOR UPDATE; paths ["wiki/locking.md"]
- Q04 en: FOUND; contract PASS; Recall@5 1.0; query Explain SELECT ... FOR UPDATE; paths ["wiki/locking.md"]
- Q05 vi: FOUND; contract PASS; Recall@5 1.0; query thử lại có giãn cách; paths ["wiki/backoff.md"]
- Q05 en: FOUND; contract PASS; Recall@5 1.0; query exponential backoff; paths ["wiki/backoff.md"]
- Q06 vi: FOUND; contract PASS; Recall@5 1.0; query nhiễu ngẫu nhiên; paths ["wiki/jitter.md"]
- Q06 en: FOUND; contract PASS; Recall@5 1.0; query full jitter; paths ["wiki/jitter.md"]
- Q07 vi: AMBIGUOUS; contract PASS; Recall@5 1.0; query chính sách thử lại; paths ["wiki/backoff.md", "wiki/jitter.md"]
- Q07 en: AMBIGUOUS; contract PASS; Recall@5 1.0; query retry policy; paths ["wiki/backoff.md", "wiki/jitter.md"]
- Q08 vi: FOUND; contract PASS; Recall@5 1.0; query đọc widget; paths ["wiki/route.md"]
- Q08 en: FOUND; contract PASS; Recall@5 1.0; query /v1/widgets/{widget_id}; paths ["wiki/route.md"]
- Q09 vi: FOUND; contract PASS; Recall@5 1.0; query tệp cấu hình cache; paths ["wiki/file.md"]
- Q09 en: FOUND; contract PASS; Recall@5 1.0; query cache_policy.py; paths ["wiki/file.md"]
- Q10 vi: FOUND; contract PASS; Recall@5 1.0; query kiểm soát đồng thời lạc quan; paths ["wiki/concurrency.md"]
- Q10 en: FOUND; contract PASS; Recall@5 1.0; query optimistic concurrency; paths ["wiki/concurrency.md"]
- Q11 vi: FOUND; contract PASS; Recall@5 1.0; query Giải thích ETag; paths ["wiki/concurrency.md"]
- Q11 en: FOUND; contract PASS; Recall@5 1.0; query Explain ETag; paths ["wiki/concurrency.md"]
- Q12 vi: FOUND; contract PASS; Recall@5 1.0; query Điều kiện If-Match là gì?; paths ["wiki/concurrency.md"]
- Q12 en: FOUND; contract PASS; Recall@5 1.0; query What is If-Match?; paths ["wiki/concurrency.md"]
- Q13 vi: FOUND; contract PASS; Recall@5 1.0; query thời gian chờ yêu cầu; paths ["wiki/projects/demo-orion/timeout.md"]
- Q13 en: FOUND; contract PASS; Recall@5 1.0; query request timeout; paths ["wiki/projects/demo-orion/timeout.md"]
- Q14 vi: FOUND; contract PASS; Recall@5 1.0; query thời gian chờ yêu cầu; paths ["wiki/projects/demo-lyra/timeout.md"]
- Q14 en: FOUND; contract PASS; Recall@5 1.0; query request timeout; paths ["wiki/projects/demo-lyra/timeout.md"]
- Q15 vi: NOT_FOUND; contract PASS; Recall@5 NOT MEASURED; query thời gian chờ yêu cầu; paths []
- Q15 en: NOT_FOUND; contract PASS; Recall@5 NOT MEASURED; query request timeout; paths []
- Q16 vi: NOT_FOUND; contract PASS; Recall@5 NOT MEASURED; query thời gian sống cache; paths []
- Q16 en: NOT_FOUND; contract PASS; Recall@5 NOT MEASURED; query cache TTL; paths []
- Q17 vi: FOUND; contract PASS; Recall@5 1.0; query thời gian sống cache; paths ["wiki/projects/demo-lyra/cache.md"]
- Q17 en: FOUND; contract PASS; Recall@5 1.0; query cache TTL; paths ["wiki/projects/demo-lyra/cache.md"]
- Q18 vi: FOUND; contract PASS; Recall@5 1.0; query lựa chọn giao vận; paths ["decisions/transport-current.md"]
- Q18 en: FOUND; contract PASS; Recall@5 1.0; query transport choice; paths ["decisions/transport-current.md"]
- Q19 vi: FOUND; contract PASS; Recall@5 1.0; query giao vận cũ; paths ["decisions/transport-old.md"]
- Q19 en: FOUND; contract PASS; Recall@5 1.0; query legacy transport; paths ["decisions/transport-old.md"]
- Q20 vi: NOT_FOUND; contract PASS; Recall@5 NOT MEASURED; query giao vận cũ; paths []
- Q20 en: NOT_FOUND; contract PASS; Recall@5 NOT MEASURED; query legacy transport; paths []
- Q21 vi: FOUND; contract PASS; Recall@5 1.0; query đề xuất lưu trữ; paths ["decisions/storage-proposal.md"]
- Q21 en: FOUND; contract PASS; Recall@5 1.0; query storage proposal; paths ["decisions/storage-proposal.md"]
- Q22 vi: DISPUTED; contract PASS; Recall@5 1.0; query cửa sổ tối đa; paths ["wiki/conflict.md"]
- Q22 en: DISPUTED; contract PASS; Recall@5 1.0; query maximum window; paths ["wiki/conflict.md"]
- Q23 vi: MISSING_EVIDENCE; contract PASS; Recall@5 1.0; query sao chép zero-copy; paths ["wiki/missing.md"]
- Q23 en: MISSING_EVIDENCE; contract PASS; Recall@5 1.0; query zero-copy replication; paths ["wiki/missing.md"]
- Q24 vi: NOT_FOUND; contract PASS; Recall@5 NOT MEASURED; query kiến trúc tàu vũ trụ; paths []
- Q24 en: NOT_FOUND; contract PASS; Recall@5 NOT MEASURED; query spaceship architecture; paths []
- Q25 vi: NOT_FOUND; contract PASS; Recall@5 0.0; query sao chép khi ghi; paths []
- Q25 en: FOUND; contract PASS; Recall@5 1.0; query copy-on-write; paths ["wiki/copy.md"]
- Q26 vi: NOT_FOUND; contract PASS; Recall@5 NOT MEASURED; query khóa cấp bảng; paths []
- Q26 en: NOT_FOUND; contract PASS; Recall@5 NOT MEASURED; query table locking; paths []
- Q27 vi: FOUND; contract PASS; Recall@5 1.0; query KHÓA HÀNG; paths ["wiki/locking.md"]
- Q27 en: FOUND; contract PASS; Recall@5 1.0; query ROW LOCKING; paths ["wiki/locking.md"]
- Q28 vi: FOUND; contract PASS; Recall@5 1.0; query Giá trị timeout_ms; paths ["wiki/projects/demo-orion/timeout.md"]
- Q28 en: FOUND; contract PASS; Recall@5 1.0; query Value of timeout_ms; paths ["wiki/projects/demo-orion/timeout.md"]
- Q29 vi: NOT_FOUND; contract PASS; Recall@5 0.0; query giữ bộ đệm gốc khi bản sao thay đổi; paths []
- Q29 en: NOT_FOUND; contract PASS; Recall@5 0.0; query retain the original buffer when mutating its copy; paths []
- Q30 vi: NOT_FOUND; contract PASS; Recall@5 NOT MEASURED; query timeout-ms; paths []
- Q30 en: NOT_FOUND; contract PASS; Recall@5 NOT MEASURED; query timeout.ms; paths []

## Recovery and failure evidence

- register_ingest_query_lint: {"lint_issues": ["WARNING UNREVIEWED_KNOWLEDGE wiki/topic.md: knowledge awaits authorized validation; citations are not factual verification."], "query_status": "FOUND", "scenario": "register_ingest_query_lint", "source_integrity": "MATCH"}
- duplicate_admission: {"attempts": 2, "new_registry_entries": 0, "raw_unchanged": true, "scenario": "duplicate_admission"}
- draft_update: {"changed_paths": ["wiki/log.md", "wiki/topic.md"], "existing_citation_retained": true, "scenario": "draft_update"}
- conflict_preservation: {"observed_status": "DISPUTED", "preserved_source_ids": ["SRC-20261018-501", "SRC-20261018-502"], "scenario": "conflict_preservation"}
- write_failure_and_retry: {"exact_rollback_observed": true, "injected_error": "TEST_ONLY_WRITE_FAILURE", "retry": "COMMITTED", "rollback_hashes": {"reports/validation.md": "108007af2e1a45c6f4489c0b9f637fa2ae85a34b38b3f292c74e772fe97ee9a8", "sources/manifest.csv": "ffd1452546e6ee2cb04633a3ede35cb12f5b69093c66e2b5a6fe4f94ed4e8a63", "sources/provenance.jsonl": "ef962249973b56b07583e6e213c4432ef7060497293ddea47e87b53720a6a8da", "sources/raw/SRC-20261018-501.md": "9f6592730233ef13ead4cc897ab12a6b61f84d302369c8cfaa1e57d9c32ad5d2", "wiki/index.md": "b24ee391281501b5c5d70f21e86731ce0d1a5dd49dd84d35bd97a55d82a1808e", "wiki/log.md": "ae76caaed9fd320e76633875b54b634023ff768084f769dd1bec025b8e3f5e15"}, "scenario": "write_failure_and_retry"}
- interruption_recovery_and_retry: {"after_hashes": {"reports/validation.md": "108007af2e1a45c6f4489c0b9f637fa2ae85a34b38b3f292c74e772fe97ee9a8", "sources/manifest.csv": "ffd1452546e6ee2cb04633a3ede35cb12f5b69093c66e2b5a6fe4f94ed4e8a63", "sources/provenance.jsonl": "ef962249973b56b07583e6e213c4432ef7060497293ddea47e87b53720a6a8da", "sources/raw/SRC-20261018-501.md": "9f6592730233ef13ead4cc897ab12a6b61f84d302369c8cfaa1e57d9c32ad5d2", "wiki/index.md": "b24ee391281501b5c5d70f21e86731ce0d1a5dd49dd84d35bd97a55d82a1808e", "wiki/log.md": "ae76caaed9fd320e76633875b54b634023ff768084f769dd1bec025b8e3f5e15"}, "before_hashes": {"reports/validation.md": "108007af2e1a45c6f4489c0b9f637fa2ae85a34b38b3f292c74e772fe97ee9a8", "sources/manifest.csv": "ffd1452546e6ee2cb04633a3ede35cb12f5b69093c66e2b5a6fe4f94ed4e8a63", "sources/provenance.jsonl": "ef962249973b56b07583e6e213c4432ef7060497293ddea47e87b53720a6a8da", "sources/raw/SRC-20261018-501.md": "9f6592730233ef13ead4cc897ab12a6b61f84d302369c8cfaa1e57d9c32ad5d2", "wiki/index.md": "b24ee391281501b5c5d70f21e86731ce0d1a5dd49dd84d35bd97a55d82a1808e", "wiki/log.md": "ae76caaed9fd320e76633875b54b634023ff768084f769dd1bec025b8e3f5e15"}, "query_during_recovery": "RECOVERY_REQUIRED", "recovery_status": "ROLLED_BACK", "retry_status": "COMMITTED", "scenario": "interruption_recovery_and_retry"}

Failures were injected only into disposable fixture operations. Actual hashes, blocked codes, authorized recovery and successful retry are recorded; source admission remains intact after failed synthesis.

## Lint evidence and semantic boundary

- Expected BROKEN_LINK: ["ERROR BROKEN_LINK wiki/topic.md: an inline link/image file target does not exist.", "WARNING UNREVIEWED_KNOWLEDGE wiki/topic.md: knowledge awaits authorized validation; citations are not factual verification.", "ERROR MISSING_CITATION wiki/topic.md: a structured factual finding needs a registered source or APPROVED ADR."]
- Expected CURRENT_DECISION_COLLISION: ["ERROR CURRENT_DECISION_COLLISION decisions/second.md: multiple current approved decisions share scope and decision_key; review and supersede explicitly."]
- Expected DUPLICATE_INDEX_ENTRY: ["WARNING DUPLICATE_INDEX_ENTRY wiki/index.md: a Markdown target is listed more than once.", "WARNING UNREVIEWED_KNOWLEDGE wiki/topic.md: knowledge awaits authorized validation; citations are not factual verification."]
- Expected DUPLICATE_PAGE_ID: ["WARNING UNREVIEWED_KNOWLEDGE wiki/other.md: knowledge awaits authorized validation; citations are not factual verification.", "ERROR DUPLICATE_PAGE_ID wiki/topic.md: page_id must be unique across wiki and canonical decisions.", "WARNING UNREVIEWED_KNOWLEDGE wiki/topic.md: knowledge awaits authorized validation; citations are not factual verification.", "WARNING ORPHAN_PAGE wiki/other.md: not reachable through checked links from wiki/index.md.", "WARNING ORPHAN_PAGE wiki/topic.md: not reachable through checked links from wiki/index.md."]
- Expected UNSUPPORTED_FRONTMATTER: ["ERROR GOVERNANCE_READ wiki/topic.md: invalid governance metadata or authority.", "ERROR UNSUPPORTED_FRONTMATTER wiki/topic.md: use canonical Markdown metadata and valid optional identifiers.", "WARNING ORPHAN_PAGE wiki/topic.md: not reachable through checked links from wiki/index.md."]
- Expected UNTRACED_STATE: ["ERROR UNTRACED_STATE wiki/topic.md: invalid governance metadata or authority.", "WARNING ORPHAN_PAGE wiki/topic.md: not reachable through checked links from wiki/index.md."]
- Expected UNKNOWN_SOURCE: ["ERROR UNKNOWN_SOURCE wiki/topic.md: invalid governance metadata or authority.", "ERROR UNKNOWN_SOURCE wiki/topic.md: SRC-20261018-999 is not registered.", "ERROR MISSING_CITATION wiki/topic.md: a structured factual finding needs a registered source or APPROVED ADR.", "WARNING NO_EVIDENCE wiki/topic.md: page has no registered source or approved decision evidence.", "WARNING ORPHAN_PAGE wiki/topic.md: not reachable through checked links from wiki/index.md.", "ERROR UNKNOWN_SOURCE_REFERENCE sources/provenance.jsonl: SRC-20261018-999."]
- Expected ORPHAN_PAGE: ["WARNING UNREVIEWED_KNOWLEDGE wiki/topic.md: knowledge awaits authorized validation; citations are not factual verification.", "WARNING ORPHAN_PAGE wiki/topic.md: not reachable through checked links from wiki/index.md."]
- Expected REVIEW_DUE: ["WARNING REVIEW_DUE wiki/topic.md: review required; no automatic state change.", "WARNING UNREVIEWED_KNOWLEDGE wiki/topic.md: knowledge awaits authorized validation; citations are not factual verification.", "WARNING ORPHAN_PAGE wiki/topic.md: not reachable through checked links from wiki/index.md."]
- Expected UNREVIEWED_KNOWLEDGE: ["WARNING UNREVIEWED_KNOWLEDGE wiki/topic.md: knowledge awaits authorized validation; citations are not factual verification."]

Deterministic checks do not establish factual truth. A shared decision_key identifies an exclusive slot collision; textual contradictions without this declaration require human/LLM review. No semantic review or full answer-generation score is claimed.

## Live workspace and compatibility

- WARNING NO_EVIDENCE wiki/concepts/knowledge-system-principles.md: page has no registered source or approved decision evidence.
{"prior_tests_run": 135, "prior_tests_passed": 135, "schema": "Optional page_id / decision_key; Markdown bullets retained; no CSV changes or bulk migration.", "stricter_contract": "Bare source IDs, YAML metadata, conflicting explicit decision slots and unsafe synthesis now fail closed; old valid fixtures remain compatible."}
Existing raw, registry, decision history and original wiki pages were not migrated or overwritten. Existing Obsidian user edits are excluded from the checkpoint.

## Known limitations and recommended fixes

- LLM answer correctness and actual model abstention
- Cross-language semantic search and automatic translation (not implemented)
- Factual truth, semantic contradiction discovery and source relevance
- Obsidian visual rendering
- Physical power-loss recovery and complete host/agent containment
- Review curated aliases for the observed unlisted paraphrases before any real intake.
- Retain independent relevance gold and add unseen natural questions when expanding evaluation.
- Review unkeyed or textual contradictions manually; deterministic collisions cannot choose a winning decision.
- Constrain broader agent tools separately before treating workflow API controls as host security.

## Reproduce

~~~text
python -B scripts/validate_workflows.py
python -B scripts/check_workspace.py --integrity --security
~~~

Use a new --output reports/<unique-name>.json to save redacted evidence without replacing past reports. No Phase 5, real intake, external access, push, merge or deployment was performed.
