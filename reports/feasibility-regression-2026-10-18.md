# V1.1 fresh regression evidence

{
  "phase": "V1.1 fresh regression validation",
  "observed_at_utc": "2026-10-18T07:02:46.481226+00:00",
  "tested_head": "457a9bf6db7bb2476117200f76586032ca1e432b",
  "branch": "workspace/initialize",
  "code_sha256": {
    "scripts/benchmark_scalability.py": "adaa62aadb6a3e7c6a638dd834f15f384a6576080cee84f8e8d31ebf08e7d04c",
    "scripts/check_workspace.py": "4b9c51045ede39596125af367146dffc2fc437e5b082b05224dd0468f0f2462a",
    "scripts/evaluate_feasibility.py": "49b11301dd9b8c206e298c1aa7f159df3f87651d48abdd588c702d7b6406612a",
    "scripts/feasibility_evolution.py": "8baa1cdaa0f2d646b6882c48a8df8e8802b9a6fcda52ae731f763e1bee06c3d9",
    "scripts/ingest_workspace.py": "c98a95afe039b643205250a1acf888ce6771b09294fdf71cf53ab4f5f110f5d3",
    "scripts/knowledge_governance.py": "b1e9339c39b022f00256036e9ef40fad376a1c4ae7ed67fdf796398c6ce7c9f6",
    "scripts/query_workspace.py": "2d3884fd180711a7d63808d33fb3450ced9bd616bd5a80ac72c87511732cf14a",
    "scripts/safe_operations.py": "2a97bc6d198627aa8cf69c2bf33528b7c16ce831bb5bea28b87ab0610c4d050e",
    "scripts/source_integrity.py": "2df48ff29a5e41057b18703c8d7fa20009e06d2afa1ef73ed110b8cb0b8b2468",
    "scripts/validate_governance_remediation.py": "f4cea4c1fc41bf95be06fa4adf14a06238074fdf1b420422694d6c7954e9cd76",
    "scripts/validate_knowledge_governance.py": "f213ac2469248afc8a596f6a5117b05e73667d0515f1063ec25deac44ff199f3",
    "scripts/validate_multilingual.py": "41c875ecd40190a85e46fce29bc947dc444e98263c9eb2b3a111bf45b5d8e134",
    "scripts/validate_scalability.py": "de1dcf6aba63151f663b69f7fb52c9a278c4b15814da9e853d6c586b905320b3",
    "scripts/validate_security.py": "ed79324a9d34aed9314a94712a6d6f566ae1a80caa88a0eddcb9360bc6b40f7a",
    "scripts/validate_source_integrity.py": "d6c001e3382a57a3d578a88a82d638c7aa69d0ea80d89aad78d92face1eb7c63",
    "scripts/validate_workflows.py": "32bff4f845759e9c28c9163ca3c0236dd433c37ad74ac96f1e4d3494e9f3c9b0",
    "scripts/workspace_security.py": "03a35cb6524de3a4fb2c7b1b994c8d6d9ad88d4f0607341b1d8d92ec175f80ad",
    "tests/test_check_workspace.py": "09c3e825c0e1064da4043cb2e9b46f5ba7e848dddc79bf6b35379d576f0a364f",
    "tests/test_feasibility_evolution.py": "3b6f297983cac9f590b833a4e1a00e0124d7d37142e8fcda68f507244b91437f",
    "tests/test_feasibility_harness.py": "536be6d60cfe02385c5540dc1e2b74a0d25cbd6e6b7069682f9a8e22589a410f",
    "tests/test_governance_adr_eligibility.py": "fab8745bd45fd203f40032683844a085bd25bb310ad3362925ca345301021280",
    "tests/test_governance_approval_paths.py": "8ec9ce54f386dd438b1f4befdea84aeccd950d0ebf0b5a922343cb708c742880",
    "tests/test_knowledge_governance.py": "10a3e0f499b9c320fe2eb43f872db327e87f39fca22ef97fc0cdc486865ccf5a",
    "tests/test_multilingual.py": "183f7da34345114d1d5dc79bd15249458712fb0897f07ef773448342903b2d66",
    "tests/test_scalability.py": "1f5ea5fb68164b2b16cf6ba26a44785d97882fd7b007e155627060fd3467981a",
    "tests/test_security_recovery.py": "3bfa4a48b73d2fa8cd95aa2a39b1c4bc3f60bbe9221482412ebae4178fb51f1b",
    "tests/test_source_integrity.py": "6cc5536aa0525fb89c071e5f30ae9422399a62e51dcc5ade1840a6f5968017cd",
    "tests/test_workflow_reliability.py": "6343a662265773ef957ede18660aac32168ba1049262a163e9975c3f65bdac43",
    "tests/workflow_benchmark.py": "d118b5c50500fd164fe740d6ea03634eaeab5d71daf8fa73cb42cdde41732293",
    "tests/workflow_support.py": "e8d968fdac6f444aceef0749f208e4d9e7ee0e04210910449f605844134083d1"
  },
  "code_unchanged_during_tests": true,
  "legacy_wrapper_phase_origin": "6097642",
  "origin_note": "The old wrapper labels its historical Phase4 origin; tested_head and hashes above identify this actual execution.",
  "unit_tests": {
    "run": 234,
    "passed": 234,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "observed_output": "----------------------------------------------------------------------\nRan 234 tests in 576.418s\n\nOK\n",
    "results": [
      {
        "test": "test_check_workspace.WorkspaceChecks.test_all_required_manifest_values_are_checked",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_approved_adr_can_support_a_first_party_project_decision",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_bad_manifest_header_and_row_shape_are_errors",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_checker_does_not_modify_or_create_workspace_files",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_citations_can_continue_on_the_next_line",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_cited_source_must_be_listed_in_page_metadata",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_content_metadata_values_are_validated",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_duplicate_manifest_ids_are_errors",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_each_finding_needs_its_own_citation",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_empty_registry_allows_explicit_unverified_draft",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_escaped_links_are_rejected_without_accessing_outside_paths",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_examples_and_comments_do_not_create_citations_or_links",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_existing_starter_hypothesis_remains_valid",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_exit_codes_and_output_distinguish_pass_warning_and_error",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_http_sources_are_metadata_only_and_no_network_is_used",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_images_and_encoded_or_angle_bracket_targets",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_inline_links_are_checked_across_documentation_locations",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_linked_paths_are_not_followed",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_missing_and_unreadable_manifests_are_reported_without_tracebacks",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_missing_raw_file_and_directory_targets_are_errors",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_missing_wiki_entrypoints_are_reported",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_orphans_are_reported_and_indirect_navigation_is_followed",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_proposed_adr_and_decision_index_are_not_approved_evidence",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_proposed_adr_can_be_linked_as_context_without_claiming_approval",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_raw_bodies_and_protected_documents_are_never_opened",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_registered_source_and_finding_pass",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_source_dates_and_id_dates_are_real_calendar_dates",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_source_paths_cannot_escape_raw_or_workspace",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_source_paths_cannot_hide_linked_components_before_parent_segments",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_structured_facts_require_citations_even_in_drafts",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_template_can_be_copied_at_two_wiki_depths_without_broken_examples",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_unknown_and_malformed_source_ids_are_reported",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_unknown_author_or_publication_date_needs_an_explanatory_note",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_unsupported_links_warn_and_heading_anchor_limit_is_explicit",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_unverified_draft_and_reviewed_without_evidence_are_distinct",
        "status": "PASS"
      },
      {
        "test": "test_check_workspace.WorkspaceChecks.test_utf8_bom_and_windows_newlines_are_supported",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_evolution.FeasibilityEvolutionTests.test_actual_admission_conflict_rollback_retry_and_fresh_reader",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_evolution.FeasibilityEvolutionTests.test_preservation_check_detects_unrelated_mutation",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_evolution.FeasibilityEvolutionTests.test_refuses_live_or_nonempty_fixture_target",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_harness.FeasibilityHarnessTests.test_blocked_candidate_identity_survives_missing_citations",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_harness.FeasibilityHarnessTests.test_claimed_match_cannot_conceal_actual_raw_tampering",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_harness.FeasibilityHarnessTests.test_counterbalanced_order_is_reproducible_and_balanced",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_harness.FeasibilityHarnessTests.test_dataset_meets_requested_coverage_and_rejects_real_or_duplicate_gold",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_harness.FeasibilityHarnessTests.test_empty_gold_does_not_create_a_recall_or_answer_score",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_harness.FeasibilityHarnessTests.test_exact_pointer_and_recorded_bytes_are_valid",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_harness.FeasibilityHarnessTests.test_fake_evidence_pointer_is_not_a_structurally_valid_citation",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_harness.FeasibilityHarnessTests.test_gold_miss_is_explicit_and_never_pass",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_harness.FeasibilityHarnessTests.test_macro_recall_excludes_zero_gold_and_keeps_actual_misses",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_harness.FeasibilityHarnessTests.test_raw_baseline_cannot_read_wiki_or_use_wiki_aliases",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_harness.FeasibilityHarnessTests.test_recall_at_five_never_counts_six_sources_from_one_page",
        "status": "PASS"
      },
      {
        "test": "test_feasibility_harness.FeasibilityHarnessTests.test_unknown_human_cost_and_factual_metrics_are_not_zero_measurements",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_actual_ingest_can_retain_independent_source_and_noncurrent_adr_context",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_adr_lifecycle_change_after_prior_query_is_not_cached_as_current",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_adr_review_deadline_crossing_recomputes_dependencies_without_index_rebuild",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_cyclic_adr_dependencies_never_authorize_current_truth_or_crash",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_derived_adr_chain_propagates_ineligible_support_to_wiki_claim",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_draft_adr_approval_label_does_not_establish_authority",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_future_effective_adr_is_context_not_parent_current_truth",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_historical_decision_kind_is_preserved_in_explicit_history",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_independent_intact_source_for_same_claim_survives_ineligible_adr_context",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_legacy_approved_label_is_not_canonical_current_evidence",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_missing_adr_fails_closed_and_lint_reports_error",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_ordinary_wiki_link_is_not_an_additional_source_of_authority",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_remediation_depth_guard_fails_closed_consistently_in_query_and_lint",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_remediation_ineligible_adr_citation_is_explicit_context_alongside_independent_source",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_remediation_malformed_decision_metadata_is_linted_without_erasing_independent_source",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_review_expired_adr_is_context_not_parent_current_truth",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_source_for_different_claim_does_not_mask_ineligible_adr_only_claim",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_superseded_adr_supports_history_not_current_truth",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_temporally_historical_approved_adr_is_not_parent_current_truth",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_valid_derived_adr_chain_retrieves_traceable_current_evidence",
        "status": "PASS"
      },
      {
        "test": "test_governance_adr_eligibility.AdrEligibilityTests.test_valid_effective_adr_authorizes_same_scope_current_claim",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_absent_independent_evidence_is_rejected_everywhere",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_approval_cannot_be_replayed_for_a_later_resolution_cycle",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_bad_approval_rejects_entire_bundle_before_any_publication",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_controlled_revision_keeps_old_approvals_without_rebinding_them",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_duplicate_approval_fields_are_rejected_everywhere",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_expired_or_revoked_before_event_is_rejected_everywhere",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_illegal_history_rejects_helper_writer_reader_query_and_lint",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_invalid_required_approval_remains_invalid_in_prior_history",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_later_expiry_preserves_history_but_blocks_current_truth",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_later_revocation_preserves_history_but_blocks_current_truth",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_legacy_history_still_validates_its_required_approval",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_malformed_or_wrong_event_binding_is_rejected_by_all_consumers",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_missing_approval_helper_and_writer_both_reject_atomically",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_missing_approval_history_is_detected_by_lint",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_missing_approval_history_is_rejected_by_query",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_missing_approval_history_is_rejected_by_reader",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_new_wiki_creation_cannot_import_non_draft_lifecycle_history",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_revoked_pending_and_unauthorized_records_are_rejected_everywhere",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_unauthorized_actor_rejects_helper_writer_reader_query_and_lint",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_unresolved_conflict_cannot_be_cleared_even_with_valid_approval",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_valid_helper_application_matches_direct_transaction",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_valid_resolution_is_consistent_across_public_boundaries",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_wrong_subject_hash_or_date_are_rejected_everywhere",
        "status": "PASS"
      },
      {
        "test": "test_governance_approval_paths.GovernanceApprovalPathTests.test_wrong_transition_or_history_prefix_is_rejected_everywhere",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_01_valid_lifecycle_transitions_are_traceable",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_02_invalid_transitions_do_not_write",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_03_ai_cannot_verify_even_with_approval_or_model_agreement",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_04_superseded_decision_is_never_current_truth",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_05_historical_fact_retrieval_does_not_expire_by_age",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_06_conflicting_sources_preserved_and_block_verified",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_07_incorrect_project_scope_has_no_fallback_or_alias_leak",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_08_explicit_cross_project_lookup_is_context_only",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_09_proposed_decision_cannot_become_approved_by_citation",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_10_missing_or_inconsistent_metadata_fails_closed",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_apply_requires_authorization_and_plan_is_read_only",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_archive_requires_human_and_history_is_opt_in",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_conflict_resolution_needs_human_validation_then_reverification",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_decision_approval_cannot_bypass_a_tampered_supporting_source",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_first_party_choice_without_external_fact_uses_approval_evidence",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_foreign_decision_is_context_not_local_configuration",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_future_effective_policy_is_not_current",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_global_knowledge_is_selected_explicitly",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_governed_decision_source_references_are_validated",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_human_label_without_validation_record_is_insufficient",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_interpretation_and_hypothesis_are_not_verified_facts",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_legacy_reviewed_is_not_verified_and_bytes_are_unchanged",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_malformed_history_and_mixed_metadata_are_rejected",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_query_and_audit_are_read_only",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_referenced_decision_cannot_hide_a_changed_supporting_source",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_restricted_scope_requires_explicit_authorization",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_review_due_is_warning_not_automatic_obsolescence",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_same_scope_approved_decision_can_support_a_project_choice",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_source_tampering_still_blocks_governed_verified_knowledge",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_unapproved_historical_label_does_not_create_decision_evidence",
        "status": "PASS"
      },
      {
        "test": "test_knowledge_governance.GovernanceTests.test_verified_body_or_scope_edit_invalidates_approval",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_accents_are_not_silently_removed_or_synonyms_invented",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_alias_and_vietnamese_title_add_only_declared_english_terms",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_aliases_do_not_leak_from_another_project",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_all_25_pairs_have_observed_results",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_ambiguous_alias_does_not_pick_an_arbitrary_document",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_identifiers_routes_and_filenames_retain_original_spelling",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_invalid_registry_fails_closed",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_linter_and_search_reject_bad_metadata",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_missing_evidence_is_not_a_source_backed_answer",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_old_metadata_defaults_and_legacy_retrieval",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_optional_metadata_rejects_invalid_types_and_duplicates",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_other_project_bad_metadata_does_not_change_selected_scope",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_punctuation_bearing_technical_keywords_are_literal",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_raw_bodies_are_not_opened_and_network_is_not_used",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_report_writer_rejects_existing_or_protected_paths",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_scope_is_required_and_never_inferred",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_search_does_not_write_or_translate_any_file",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_underscored_fields_are_parsed",
        "status": "PASS"
      },
      {
        "test": "test_multilingual.MultilingualTests.test_unicode_nfc_nfd_case_and_spacing_match",
        "status": "PASS"
      },
      {
        "test": "test_scalability.ScaleSafetyTests.test_10000_source_ids_are_valid_and_unique",
        "status": "PASS"
      },
      {
        "test": "test_scalability.ScaleSafetyTests.test_fixture_root_cannot_target_live_knowledge",
        "status": "PASS"
      },
      {
        "test": "test_scalability.ScaleSafetyTests.test_governance_batch_parses_registry_once",
        "status": "PASS"
      },
      {
        "test": "test_scalability.ScaleSafetyTests.test_measurement_data_cannot_select_files_to_read",
        "status": "PASS"
      },
      {
        "test": "test_scalability.ScaleSafetyTests.test_profile_only_results_cannot_claim_full_load_correctness",
        "status": "PASS"
      },
      {
        "test": "test_scalability.ScaleSafetyTests.test_query_reuses_validated_ids_only_within_one_operation",
        "status": "PASS"
      },
      {
        "test": "test_scalability.ScaleSafetyTests.test_query_skips_only_the_redundant_reverse_wiki_scan",
        "status": "PASS"
      },
      {
        "test": "test_scalability.ScaleSafetyTests.test_raw_same_size_mtime_edit_remains_detectable",
        "status": "PASS"
      },
      {
        "test": "test_scalability.ScaleSafetyTests.test_recipe_and_hierarchical_index_are_reproducible",
        "status": "PASS"
      },
      {
        "test": "test_scalability.ScaleSafetyTests.test_registry_metadata_hash_is_not_cached_between_queries",
        "status": "PASS"
      },
      {
        "test": "test_scalability.ScaleSafetyTests.test_timeout_is_not_a_completed_latency_or_pass",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_01_prompt_injection_in_source_is_blocked_on_actual_ingest_path",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_02_fake_priority_and_hidden_instructions_block_actual_query",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_03_unauthorized_policy_modification_has_no_write_capability",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_04_path_traversal_and_windows_aliases_are_rejected",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_05_sensitive_locations_are_rejected_before_open",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_06_failed_write_midway_restores_all_owned_resources",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_07_failed_ingestion_rolls_back_without_removing_approved_source",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_08_concurrent_writers_cannot_silently_lose_updates",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_09_generated_report_redacts_secret_keys_and_values",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_10_crash_recovery_preserves_every_unrelated_user_file",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_approval_and_source_command_cannot_expand_the_write_allowlist",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_committed_operation_recovery_keeps_complete_result",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_fake_labeled_identity_is_flagged_without_value_in_output",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_new_raw_snapshot_never_publishes_partial_bytes",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_old_report_writers_use_the_redaction_boundary",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_query_rejects_a_generation_changed_during_retrieval",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_raw_policy_filename_is_blocked_before_publication",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_recovery_refuses_to_overwrite_edits_made_after_interruption",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_sensitive_generated_wiki_is_blocked_before_backup_or_commit",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_stale_owner_requires_explicit_human_recovery_acknowledgement",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_successful_ingestion_is_atomic_draft_and_query_remains_data",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_synthetic_private_key_block_is_redacted_as_a_whole",
        "status": "PASS"
      },
      {
        "test": "test_security_recovery.SecurityRecoveryTests.test_tampered_journal_cannot_target_operating_policy",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_01_valid_registration_and_unknown_metadata",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_02_duplicate_ingestion_is_idempotent_and_content_deduplicated",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_03_duplicate_id_with_different_content_is_rejected",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_04_hash_mismatch_blocks_source_and_query",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_05_missing_source_file_is_detected",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_06_invalid_wiki_reference_is_detected",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_07_missing_required_metadata_is_rejected_before_writes",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_08_unavailable_original_url_retains_local_evidence_without_network",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_09_attempted_raw_modification_is_refused",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_10_source_version_replacement_preserves_old_snapshot_and_references",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_audit_and_query_are_read_only_and_only_hash_raw_bytes",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_binary_sources_are_hashed_without_text_decoding",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_claim_with_no_evidence_stays_unknown",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_corrupt_duplicate_and_orphan_provenance_fail_closed",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_forked_and_out_of_sequence_versions_are_rejected_before_append",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_hash_matching_never_promotes_verification_status",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_interrupted_registration_rolls_back_metadata_without_touching_raw",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_known_origin_revision_needs_explicit_version_link",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_legacy_migration_is_explicit_readonly_planning_and_append_only_apply",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_manifest_metadata_tampering_is_detected",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_manually_duplicated_content_is_detected",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_metadata_only_replacement_can_reuse_immutable_bytes",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_migration_detects_changed_bytes_since_proposal",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_multiple_sources_support_one_claim_and_one_bad_source_blocks_it",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_remote_only_legacy_record_requires_an_authorized_snapshot",
        "status": "PASS"
      },
      {
        "test": "test_source_integrity.SourceIntegrityTests.test_stale_lock_is_not_deleted_or_ignored",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.BenchmarkTests.test_independent_corpus_and_thirty_query_pairs",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_01_registration_provenance_ingest_query_lint",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_02_duplicate_registration_reuses_identity_and_bytes",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_03_fresh_plan_for_identical_content_does_not_duplicate_log",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_04_existing_draft_update_retains_old_evidence",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_05_bounded_wiki_transaction_cannot_bypass_verified_guard",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_06_scope_and_transition_history_cannot_be_reset_by_ingest",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_07_conflicting_information_and_pointers_are_preserved",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_08_missing_index_and_missing_log_are_rejected_before_write",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_09_ingest_cannot_remove_existing_index_links",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_10_failed_ingest_rolls_back_and_retry_succeeds",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_11_interrupted_ingest_requires_recovery_then_retry",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_12_stale_update_does_not_overwrite_newer_user_work",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_13_invalid_citation_plan_does_not_leave_partial_files",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_identical_ingest_retry_is_a_read_only_noop",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_ingest_cannot_reset_verified_knowledge_to_draft",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_lifecycle_operation_cannot_reset_verified_history",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_lint_broken_markdown_link",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_lint_contradictory_current_decision_slots_require_review",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_lint_duplicate_index_target",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_lint_duplicate_page_identity",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_lint_invalid_frontmatter_does_not_ignore_yaml",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_lint_invalid_lifecycle_transition",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_lint_missing_source_reference",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_lint_orphan_and_missing_index_entry",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_lint_potentially_stale_does_not_change_status",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_lint_rejects_a_source_id_without_an_exact_pointer",
        "status": "PASS"
      },
      {
        "test": "test_workflow_reliability.WorkflowTests.test_lint_unreviewed_knowledge_is_not_verified",
        "status": "PASS"
      }
    ]
  },
  "workspace_issues": [
    "WARNING NO_EVIDENCE wiki/concepts/knowledge-system-principles.md: page has no registered source or approved decision evidence."
  ],
  "workflow_metrics": {
    "retrieval_recall_at_5": {
      "value": 0.9375,
      "queries_with_relevance_gold": 48,
      "definition": "Macro document Recall@5 over actual highest-tier candidates (matches + blocked), ordered by score/path; excludes zero-relevance cases. Retrieval does not imply answerability.",
      "vi": {
        "value": 0.9166666666666666,
        "queries_with_relevance_gold": 24
      },
      "en": {
        "value": 0.9583333333333334,
        "queries_with_relevance_gold": 24
      }
    },
    "citation_validity": {
      "numerator": 53,
      "denominator": 53,
      "value": 1.0
    },
    "cross_project_leakage": {
      "numerator": 0,
      "denominator": 60,
      "value": 0.0
    },
    "duplicate_ingestion_rate": {
      "numerator": 0,
      "denominator": 13,
      "value": 0.0
    },
    "duplicate_registration_rate": {
      "numerator": 0,
      "denominator": 17,
      "value": 0.0
    },
    "schema_validation_pass_rate": {
      "numerator": 16,
      "denominator": 16,
      "value": 1.0
    },
    "workflow_failure_rate": {
      "numerator": 0,
      "denominator": 90,
      "value": 0.0
    },
    "answer_generation_accuracy": "NOT MEASURED",
    "cross_language_semantic_search": "NOT MEASURED (not implemented)",
    "automatic_translation_accuracy": "NOT MEASURED (not implemented)",
    "semantic_factual_verification": "NOT MEASURED"
  },
  "passed": true
}
