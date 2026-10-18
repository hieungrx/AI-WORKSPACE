# V1 Governance Remediation - Verification

First-party local synthetic evidence; no V2 or real intake.

Findings: {"H-GOV-01": "RESOLVED", "H-GOV-02": "RESOLVED"}

Executed test totals: {"run": 219, "passed": 219, "failures": 0, "errors": 0, "skipped": 0}

Tested checkout HEAD: a73c638cd3420d2aa898866fd8b1c54bbab74623; scoped implementation hashes are in JSON.

## Root causes and enforced invariants

H-GOV-01: duplicated, incomplete ADR gates and page-wide evidence fallback. Canonical per-finding evidence now recursively applies own and dependency eligibility; historical/context retrieval is separate from current truth. Independent valid evidence for the same claim is retained.
H-GOV-02: the helper checked approval but writer/replay did not. Shared event approval validation now covers helper, pre-commit writer, replay, Query and Lint. New events bind policy, subject, transition, snapshot hash and prior history; invalid approval cannot commit or be hidden by final unverified/draft status.

## Original public paths rerun

{
  "H-GOV-01": {
    "cases": [
      {
        "case": "future",
        "status": "FOUND",
        "current": [
          false
        ],
        "citations": [
          [
            {
              "decision_path": "decisions/future.md",
              "source_pointer": "documented human approval",
              "evidence_type": "project_decision",
              "scope": "audit-project",
              "eligible_for_current_truth": false,
              "context_only": true,
              "knowledge_status": "verified",
              "temporal": "current",
              "freshness": [
                "NOT_YET_EFFECTIVE"
              ],
              "eligibility_reasons": [
                "NOT_YET_EFFECTIVE"
              ]
            }
          ]
        ]
      },
      {
        "case": "overdue",
        "status": "FOUND",
        "current": [
          false
        ],
        "citations": [
          [
            {
              "decision_path": "decisions/overdue.md",
              "source_pointer": "documented human approval",
              "evidence_type": "project_decision",
              "scope": "audit-project",
              "eligible_for_current_truth": false,
              "context_only": true,
              "knowledge_status": "verified",
              "temporal": "current",
              "freshness": [
                "REVIEW_DUE"
              ],
              "eligibility_reasons": [
                "REVIEW_DUE"
              ]
            }
          ]
        ]
      },
      {
        "case": "historical",
        "status": "FOUND",
        "current": [
          false
        ],
        "citations": [
          [
            {
              "decision_path": "decisions/historical.md",
              "source_pointer": "documented human approval",
              "evidence_type": "project_decision",
              "scope": "audit-project",
              "eligible_for_current_truth": false,
              "context_only": true,
              "knowledge_status": "verified",
              "temporal": "historical",
              "freshness": [],
              "eligibility_reasons": [
                "NOT_CURRENT_KNOWLEDGE"
              ]
            }
          ]
        ]
      }
    ],
    "passed": true
  },
  "H-GOV-02": {
    "outcomes": {
      "helper": "FileNotFoundError",
      "writer": "FileNotFoundError",
      "no_durable_event": true,
      "query": "INVALID_DATA",
      "lint_errors": [
        "ERROR GOVERNANCE_READ wiki/conflict.md: invalid governance metadata or authority."
      ]
    },
    "passed": true
  },
  "owned_fixture_cleaned": true
}

## Regression cases and acceptance evidence

### H-GOV-01

- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_actual_ingest_can_retain_independent_source_and_noncurrent_adr_context
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_adr_lifecycle_change_after_prior_query_is_not_cached_as_current
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_adr_review_deadline_crossing_recomputes_dependencies_without_index_rebuild
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_cyclic_adr_dependencies_never_authorize_current_truth_or_crash
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_derived_adr_chain_propagates_ineligible_support_to_wiki_claim
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_draft_adr_approval_label_does_not_establish_authority
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_future_effective_adr_is_context_not_parent_current_truth
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_historical_decision_kind_is_preserved_in_explicit_history
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_independent_intact_source_for_same_claim_survives_ineligible_adr_context
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_legacy_approved_label_is_not_canonical_current_evidence
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_missing_adr_fails_closed_and_lint_reports_error
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_ordinary_wiki_link_is_not_an_additional_source_of_authority
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_remediation_depth_guard_fails_closed_consistently_in_query_and_lint
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_remediation_ineligible_adr_citation_is_explicit_context_alongside_independent_source
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_remediation_malformed_decision_metadata_is_linted_without_erasing_independent_source
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_review_expired_adr_is_context_not_parent_current_truth
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_source_for_different_claim_does_not_mask_ineligible_adr_only_claim
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_superseded_adr_supports_history_not_current_truth
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_temporally_historical_approved_adr_is_not_parent_current_truth
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_valid_derived_adr_chain_retrieves_traceable_current_evidence
- PASS: test_governance_adr_eligibility.AdrEligibilityTests.test_valid_effective_adr_authorizes_same_scope_current_claim

### H-GOV-02

- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_absent_independent_evidence_is_rejected_everywhere
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_approval_cannot_be_replayed_for_a_later_resolution_cycle
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_bad_approval_rejects_entire_bundle_before_any_publication
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_controlled_revision_keeps_old_approvals_without_rebinding_them
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_duplicate_approval_fields_are_rejected_everywhere
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_expired_or_revoked_before_event_is_rejected_everywhere
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_illegal_history_rejects_helper_writer_reader_query_and_lint
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_invalid_required_approval_remains_invalid_in_prior_history
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_later_expiry_preserves_history_but_blocks_current_truth
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_later_revocation_preserves_history_but_blocks_current_truth
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_legacy_history_still_validates_its_required_approval
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_malformed_or_wrong_event_binding_is_rejected_by_all_consumers
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_missing_approval_helper_and_writer_both_reject_atomically
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_missing_approval_history_is_detected_by_lint
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_missing_approval_history_is_rejected_by_query
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_missing_approval_history_is_rejected_by_reader
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_new_wiki_creation_cannot_import_non_draft_lifecycle_history
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_revoked_pending_and_unauthorized_records_are_rejected_everywhere
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_unauthorized_actor_rejects_helper_writer_reader_query_and_lint
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_unresolved_conflict_cannot_be_cleared_even_with_valid_approval
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_valid_helper_application_matches_direct_transaction
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_valid_resolution_is_consistent_across_public_boundaries
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_wrong_subject_hash_or_date_are_rejected_everywhere
- PASS: test_governance_approval_paths.GovernanceApprovalPathTests.test_wrong_transition_or_history_prefix_is_rejected_everywhere

## Compatibility

Existing source/metadata schema retained; new required events use policy 2. Legacy policy 1 is read-only replay, with missing approvals errors and unavailable historical-content snapshots explicitly unverified.

## Workspace checks

WARNING NO_EVIDENCE wiki/concepts/knowledge-system-principles.md: page has no registered source or approved decision evidence.

## Remaining risks / NOT RUN

- TEST_ONLY approvals are fixtures, not real human approvals or authenticated identities.
- No live knowledge, history or old approval is migrated/deleted/rewritten.
- Graph depth has a 32-node fail-closed bound; dense graphs and new retrieval latency are not benchmarked.
- Host containment, real secrets, real URLs, physical power loss and production intake are not tested.
- Earlier Medium/Low audit findings remain outside this two-High remediation scope.

No real claim/decision approval, source intake, push/merge/deploy or V2 is authorized by these results.
