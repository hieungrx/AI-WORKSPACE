# V1 — Báo cáo khắc phục hai lỗi governance mức High

H-GOV-01: **RESOLVED**. H-GOV-02: **RESOLVED**.

Kết luận giới hạn ở hai lỗi và các đường thực thi đã kiểm tra bằng dữ liệu giả lập. Không tự nâng kết luận toàn workspace thành READY.

Branch: `workspace/initialize`. Baseline: `80d9d67c495aad3443efa06b2b823bae5be8b4a7`. Code/test: `5345a2b`; specification: `a73c638`. HEAD được kiểm thử: `a73c638cd3420d2aa898866fd8b1c54bbab74623`.

## Nguyên nhân và thay đổi

H-GOV-01: Query và Lint có các nhánh kiểm tra ADR không đồng nhất; trạng thái hiện hành chỉ xét trang cha, còn bằng chứng được gộp theo trang. `current_eligibility` và `evaluate_evidence` nay kiểm tra từng finding cùng dependency ADR, effective/review/lifecycle/scope. ADR không đủ điều kiện vẫn là context truy vết được; bằng chứng độc lập hợp lệ cho chính finding đó vẫn được giữ.

H-GOV-02: helper có kiểm tra approval, nhưng direct lifecycle writer và replay có thể bỏ qua. `validate_event_approval` nay dùng chung trong helper, preflight writer và từng event lịch sử. Event mới cần approval dùng policy 2 ràng buộc subject, nội dung, chuyển trạng thái và prefix lịch sử; approval sai không tạo durable event.

## Bằng chứng đã chạy

- Hai lượt full suite riêng đều **219/219 PASS**, không failure/error/skip: 174 test cũ và 45 test mới (21 ADR, 24 approval).
- Validator cuối chạy lại suite mới, không lấy PASS từ báo cáo cũ; hash implementation không đổi trong lượt chạy.
- Đường lỗi H-GOV-01 gốc: cả future/overdue/historical trả `FOUND`, `usable_as_current_truth=false`, citation là context.
- Đường lỗi H-GOV-02 gốc với event legacy sáu trường: helper/writer từ chối approval thiếu bằng `FileNotFoundError`; snapshot không thay đổi; khi chủ động cài lịch sử sai vào fixture, Query trả `INVALID_DATA`, Lint báo `ERROR GOVERNANCE_READ`.
- Strict Lint sau append log: **0 errors**, một `NO_EVIDENCE` có sẵn trên trang draft gốc. Diff whitespace sạch.
- Multilingual: 25 cặp/50 truy vấn lexical đạt 50/50. Benchmark workflow 60 truy vấn giữ Recall@5 0.9375, citation validity 53/53, cross-project leakage 0/60. Không tuyên bố semantic search hoặc dịch tự động.

[Kết quả chi tiết, từng test và original probes](governance-remediation-verification-2026-10-18.md) · [JSON](governance-remediation-verification-2026-10-18.json) · [Workflow/recovery](governance-remediation-workflows-2026-10-18.md) · [Multilingual](governance-remediation-multilingual-2026-10-18.md) · [Baseline trước sửa](governance-remediation-inspection-2026-10-18.md)

## Files đã thay đổi

- [scripts/knowledge_governance.py](../scripts/knowledge_governance.py): Canonical own/dependency eligibility; per-finding evidence; shared action-bound approval validation for helper, writer and replay.
- [scripts/query_workspace.py](../scripts/query_workspace.py): Use shared eligibility/evidence, expose context/current reasons and retain historical retrieval.
- [scripts/check_workspace.py](../scripts/check_workspace.py): Use shared evidence evaluator and strict catalog; preserve ERROR diagnostics for invalid records/references.
- [scripts/validate_governance_remediation.py](../scripts/validate_governance_remediation.py): Fresh full-suite validation and original public-path reproductions; scoped evidence export.
- [tests/test_governance_adr_eligibility.py](../tests/test_governance_adr_eligibility.py): 21 new synthetic tests for H-GOV-01, including actual Ingest/Query/Lint and changing dependencies.
- [tests/test_governance_approval_paths.py](../tests/test_governance_approval_paths.py): 24 new synthetic tests across helper, direct writer, stored replay, Query and Lint.
- [tests/test_knowledge_governance.py](../tests/test_knowledge_governance.py): Existing fixtures issue explicit policy-2 approvals; prior assertions retained.
- [tests/workflow_support.py](../tests/workflow_support.py): Unique action-bound TEST_ONLY fixture approval records.
- [tests/test_security_recovery.py](../tests/test_security_recovery.py): Concurrent Query test instruments the new shared evaluation hook; original concurrency expectations retained.
- [KNOWLEDGE_GOVERNANCE.md](../KNOWLEDGE_GOVERNANCE.md): Eligibility, approval policy 2, versioned replay, validity dates and review-in-place quarantine procedure.
- [SCHEMA.md](../SCHEMA.md): Compatible references to canonical eligibility and new action-bound required-approval events.
- [wiki/log.md](../wiki/log.md): Append actual authorized maintenance and test results; preserve the entire 23144-byte prior log.
- [reports/governance-remediation-inspection-2026-10-18.json](../reports/governance-remediation-inspection-2026-10-18.json): New exclusive evidence report; no existing report overwritten.
- [reports/governance-remediation-inspection-2026-10-18.md](../reports/governance-remediation-inspection-2026-10-18.md): New exclusive evidence report; no existing report overwritten.
- [reports/governance-remediation-workflows-2026-10-18.json](../reports/governance-remediation-workflows-2026-10-18.json): New exclusive evidence report; no existing report overwritten.
- [reports/governance-remediation-workflows-2026-10-18.md](../reports/governance-remediation-workflows-2026-10-18.md): New exclusive evidence report; no existing report overwritten.
- [reports/governance-remediation-multilingual-2026-10-18.json](../reports/governance-remediation-multilingual-2026-10-18.json): New exclusive evidence report; no existing report overwritten.
- [reports/governance-remediation-multilingual-2026-10-18.md](../reports/governance-remediation-multilingual-2026-10-18.md): New exclusive evidence report; no existing report overwritten.
- [reports/governance-remediation-verification-2026-10-18.json](../reports/governance-remediation-verification-2026-10-18.json): New exclusive evidence report; no existing report overwritten.
- [reports/governance-remediation-verification-2026-10-18.md](../reports/governance-remediation-verification-2026-10-18.md): New exclusive evidence report; no existing report overwritten.
- [reports/governance-remediation-completion-2026-10-18.json](../reports/governance-remediation-completion-2026-10-18.json): New exclusive evidence report; no existing report overwritten.
- [reports/governance-remediation-completion-2026-10-18.md](../reports/governance-remediation-completion-2026-10-18.md): New exclusive evidence report; no existing report overwritten.

## Invariants và ranh giới thực thi

- One own-record gate and one shared transitive evidence evaluator drive direct ADR, parent wiki/derived claims, Query and strict Lint; no duplicated Query authority implementation.
- Every factual finding needs intact listed source proof or an eligible same-scope canonical decision; proof for a different finding cannot substitute.
- A noncurrent ADR remains traceable context. FOUND is independent of usable_as_current_truth; independent valid evidence for the same finding is retained.
- Effective dates, review deadlines, lifecycle/historical/proposal state, scope and recursive dependencies all gate current authority; missing/unknown evidence fails closed.
- No persistent eligibility cache: changed ADR, approval or date is reevaluated on each operation. Cycles and depth over the resource bound fail closed.
- Every required approval is checked in helper, direct writer before durable publication and every historical replay, including invalid prior events followed by unverified/draft.
- New required-approval writes need policy 2: human authority, valid approval/evidence, exact subject, content hash, from/to transition and prior-history hash. Wrong/reused/revoked/expired approvals cannot commit.
- New wiki creation starts draft with empty lifecycle history; generic wiki writes cannot import fabricated verification events.
- Recorded historical events and approval bytes are never erased or rebound by ordinary edits/recovery; version-specific replay is explicit.
- Source hashing, scope restrictions, expected-version ownership and rollback guards remain in force; citations and model agreement do not prove factual truth.

## Đối chiếu các interface

- **transition helper**: hợp lệ — Proposal/apply succeeds with correct policy-2 approval. Không hợp lệ — Reject before transaction; original missing-ref probe raised FileNotFoundError.
- **direct lifecycle transaction**: hợp lệ — COMMITTED only after shared preflight, under version/ownership guard. Không hợp lệ — Reject before journal/publication; no status downgrade or partial bundle.
- **durable event history**: hợp lệ — Append one bound event; previous event prefix preserved. Không hợp lệ — No durable event, no side effect in snapshot including recovery files.
- **historical read_page replay**: hợp lệ — Version-specific rules retain valid past events and old immutable approvals. Không hợp lệ — ERROR even if final state unverified/draft; no silent historical repair.
- **Query**: hợp lệ — Eligible proof may authorize current; historical/context FOUND is separate. Không hợp lệ — Ineligible ADR-only current=false; malformed approval history INVALID_DATA.
- **strict Lint / integrity audit**: hợp lệ — No authority/integrity ERROR for valid fixtures. Không hợp lệ — Invalid approval/reference ERROR; existing valid but noncurrent ADR support warning with reason.

## Acceptance evidence — H-GOV-01

- **PASS** Valid and effective ADR: `test_governance_adr_eligibility.AdrEligibilityTests.test_valid_effective_adr_authorizes_same_scope_current_claim`.
- **PASS** Not-yet-effective ADR: `test_governance_adr_eligibility.AdrEligibilityTests.test_future_effective_adr_is_context_not_parent_current_truth`.
- **PASS** Expired review requiring reapproval: `test_governance_adr_eligibility.AdrEligibilityTests.test_review_expired_adr_is_context_not_parent_current_truth`.
- **PASS** Historical ADR: `test_governance_adr_eligibility.AdrEligibilityTests.test_temporally_historical_approved_adr_is_not_parent_current_truth`.
- **PASS** Superseded ADR: `test_governance_adr_eligibility.AdrEligibilityTests.test_superseded_adr_supports_history_not_current_truth`.
- **PASS** Missing ADR: `test_governance_adr_eligibility.AdrEligibilityTests.test_missing_adr_fails_closed_and_lint_reports_error`.
- **PASS** Only ineligible support / derived knowledge: `test_governance_adr_eligibility.AdrEligibilityTests.test_derived_adr_chain_propagates_ineligible_support_to_wiki_claim`.
- **PASS** Independent sufficient evidence for the same claim: `test_governance_adr_eligibility.AdrEligibilityTests.test_independent_intact_source_for_same_claim_survives_ineligible_adr_context`.
- **PASS** Validity changes after prior retrieval: `test_governance_adr_eligibility.AdrEligibilityTests.test_adr_lifecycle_change_after_prior_query_is_not_cached_as_current`.
- **PASS** Query and Lint consistency: `test_governance_adr_eligibility.AdrEligibilityTests.test_remediation_depth_guard_fails_closed_consistently_in_query_and_lint`.

## Acceptance evidence — H-GOV-02

- **PASS** Valid approval: `test_governance_approval_paths.GovernanceApprovalPathTests.test_valid_resolution_is_consistent_across_public_boundaries`.
- **PASS** Nonexistent approval: `test_governance_approval_paths.GovernanceApprovalPathTests.test_missing_approval_helper_and_writer_both_reject_atomically`.
- **PASS** Revoked approval: `test_governance_approval_paths.GovernanceApprovalPathTests.test_revoked_pending_and_unauthorized_records_are_rejected_everywhere`.
- **PASS** Expired approval: `test_governance_approval_paths.GovernanceApprovalPathTests.test_expired_or_revoked_before_event_is_rejected_everywhere`.
- **PASS** Different subject: `test_governance_approval_paths.GovernanceApprovalPathTests.test_wrong_subject_hash_or_date_are_rejected_everywhere`.
- **PASS** Different transition: `test_governance_approval_paths.GovernanceApprovalPathTests.test_wrong_transition_or_history_prefix_is_rejected_everywhere`.
- **PASS** Unauthorized approver: `test_governance_approval_paths.GovernanceApprovalPathTests.test_unauthorized_actor_rejects_helper_writer_reader_query_and_lint`.
- **PASS** Duplicate/replayed approval: `test_governance_approval_paths.GovernanceApprovalPathTests.test_approval_cannot_be_replayed_for_a_later_resolution_cycle`.
- **PASS** Failed commit atomicity: `test_governance_approval_paths.GovernanceApprovalPathTests.test_bad_approval_rejects_entire_bundle_before_any_publication`.
- **PASS** Invalid historical event: `test_governance_approval_paths.GovernanceApprovalPathTests.test_invalid_required_approval_remains_invalid_in_prior_history`.

Các ca bổ sung bao gồm nguồn của finding khác không bù cho claim thiếu proof, chuỗi ADR, cycle/depth guard, dữ liệu Decision sai, actual Ingest, thay đổi deadline, import history qua wiki writer, unresolved conflict, approval hết hạn/thu hồi sau event và snapshot legacy. Danh sách đủ 45 test nằm trong báo cáo verification/JSON.

## Lệnh đã chạy và kết quả

- `python -B scripts/validate_workflows.py --output reports/governance-remediation-workflows-2026-10-18.json` — exit 0: 219/219 tests; existing 60-query independent synthetic workflow benchmark and recovery demonstrations executed.
- `python -B scripts/validate_multilingual.py --output reports/governance-remediation-multilingual-2026-10-18.json` — exit 0: 25 pairs / 50 queries, 50 passed; scoped lexical matching and curated aliases only.
- `python -B scripts/validate_governance_remediation.py --output reports/governance-remediation-verification-2026-10-18.json` — exit 0: Fresh second full suite 219/219 plus the original public-path probes; both findings RESOLVED; core hashes unchanged.
- `python -B scripts/check_workspace.py --integrity --security` — exit 0: 0 errors, existing 1 NO_EVIDENCE warning; repeated after log append.
- `git diff 80d9d67 --check` — exit 0: No whitespace errors across remediation code/docs and appended log.
- `git show --stat --oneline 5345a2b` — exit 0: Reviewed explicit code/test checkpoint; no unrelated data included.
- `Python standard-library SHA-256 comparison against inspection report` — exit 0: 16 complete files plus original log prefix match all 17 protected baselines.
- `Ad hoc TEST_ONLY compatibility fixture via python -B -` — exit 0: Policy-1 active read, controlled content revision and new policy-2 validation; old approval bytes/event prefix preserved; strict Lint has no errors; owned fixture removed.

## Tương thích và lịch sử

- CSV/provenance contract, Markdown metadata and legacy read adapter remain; no global schema_version or competing metadata standard added.
- Unversioned six-field events replay under policy 1. Their required approvals are validated; policy 1 cannot authorize a new required-approval write.
- Policy 2 adds approval_policy / approval_content_hash to required events and binds the approval record to from_state / to_state / prior_transitions_hash. Approval templates/process must use these fields for future authorized required transitions.
- Later expiry/revocation preserves a valid prior event evaluated on its event date, while blocking current authority. New commits also check commit-date validity.
- Policy-1 historical content snapshots are unavailable if content has changed. LEGACY_APPROVAL_SNAPSHOT_UNAVAILABLE is an explicit unverified limitation; new validation does not retroactively certify absent old content.
- Invalid historical approval data is quarantined in place by ERROR / INVALID_DATA. Preserve bytes for human review; separately authorized reconciliation may restore genuine evidence or create a draft replacement linked to the original. Never invent an old approval, drop events or relabel policy versions.
- Recovery restores exact validated snapshots, not silently edited history; restored invalid history remains rejected by Query/Lint. No live migration/reapproval took place.

Probe bổ sung đã đọc approval policy 1 đang active, thực hiện revision có kiểm soát rồi approval policy 2 mới: approval cũ và prefix event giữ nguyên; Lint không có lỗi. Warning `LEGACY_APPROVAL_SNAPSHOT_UNAVAILABLE` giữ đúng giới hạn chưa xác minh nội dung cũ.

Quy tắc cụ thể: [KNOWLEDGE_GOVERNANCE.md](../KNOWLEDGE_GOVERNANCE.md), [SCHEMA.md](../SCHEMA.md). Chưa migrate dữ liệu/approval thực tế.

## Bảo toàn dữ liệu và Git

16 entire baseline files plus the exact 23144-byte old log prefix preserved. User Obsidian change and ten prior audit reports remain excluded from remediation commits.

Live registered sources: **0**. Raw/manifest/provenance, trang gốc, decisions index và báo cáo audit cũ không đổi. `wiki/log.md` được append qua transaction có expected hash; 23144 byte cũ giữ nguyên. JSON ghi đầy đủ expected/observed SHA-256 của từng tệp.

Diff code/docs đã review theo checkpoint; không thêm dependency, database, framework hoặc thay đổi permission/AGENTS. Báo cáo này và log có checkpoint riêng sau khi sinh; xem Git history để lấy commit thực tế. Không ghi trước một ID commit chưa tồn tại.

## Ghi chú quá trình kiểm thử

- Pre-fix focused ADR set: 10 failures / 16 tests; approval set: 4 failures / 4 tests. These are regression observations, not counts of distinct vulnerabilities.
- Fixture approval generators were upgraded to action-bound records; the existing concurrent-Query test follows the shared evaluator hook. No benchmark gold or prior safety assertions were relaxed.
- An initial ad hoc legacy compatibility probe placed a new interpretation inside the factual Findings section: strict Lint correctly rejected missing evidence. Moving that synthetic line to its own Interpretations section made the corrected fixture pass; implementation rules were not weakened.

## Rủi ro và phần chưa đo

- Local approval records/caller authorization flags do not authenticate human identity or validate evidence relevance; direct host tools outside the bounded API remain outside this guarantee.
- Shared deterministic checks do not prove source truth, semantic citation relevance, conflict correctness or LLM answer accuracy.
- Depth 32 is a fail-closed resource bound, not measured capacity. Dense dependency graph latency, concurrency capacity and post-change 100/1000/10000 load are NOT RUN; old Phase 5 flat-corpus timings are not evidence for this new recursive path.
- Legacy missing snapshots cannot be reconstructed; no real legacy reconciliation or reviewer authentication was tested.
- Other Medium/Low findings in the retained independent audit, including detector coverage and historical wrapper/version drift, are outside this two-High task and remain outstanding.

NOT RUN / NOT MEASURED: Production knowledge or approval ingestion; Live legacy migration/reapproval; Semantic retrieval / automatic translation / factual truth evaluation; Real secrets or real URL availability; OS/host containment and hostile same-user editors; Physical power loss; Obsidian UI rendering; New dependency-graph performance benchmark; API tokens/charges; Push / merge / deployment / V2.

Các yêu cầu cần phê duyệt riêng: real human validation, live legacy reconciliation, pilot intake, thay đổi kiến trúc hoặc permission. Không thực hiện các bước này trong remediation.

## Kết luận

**H-GOV-01 — RESOLVED. H-GOV-02 — RESOLVED.** Cả hai đường lỗi gốc đã được chạy lại thành công qua cùng public paths. Không sửa kết luận audit cũ, không bắt đầu Knowledge Pilot hoặc V2.
