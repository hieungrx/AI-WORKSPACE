# Phase 5 — Scalability Assessment

**Overall: CONDITIONAL**. Tested correctness: **PASS**.
Correctness is separate from interactive readiness: measured linear scans remain slow at larger sizes, timing samples are small, and production/LLM/host limits remain untested.

Observed UTC: 2026-10-17T18:25:28.540828+00:00; baseline 55e6e1f, branch workspace/initialize.
Fresh regression run: 174 tests; 174 PASS; 0 failures, 0 errors, 0 skips.
Sources: first-party repository implementation/contracts and synthetic load fixtures only. No real source/secret or outside repository was opened.
Read: AGENTS/README/SCHEMA/PROFILE, source/governance/security/workflow reports, prompts, wiki indexes/history, manifest, search/validator/transaction code and tests.
Changed: operation-local registry reuse in governance/Query, Query source-audit scan selection, reproducible load/validation scripts and tests, scalability guide, README/navigation and append-only maintenance history.

## Architecture, bottlenecks and migration

See [architecture review, incremental behavior, Level 1-4 search interface/migration plan, provisional triggers and V1.1 pilot recommendations](../SCALABILITY.md).
Baseline measurements and a separate cProfile identify repeated registry reads and filesystem/path scans. Registry reuse is local to one operation; raw SHA-256, lineage, scope, lifecycle approval, security and recovery checks remain active.
No production index, database, QMD, embedding model, worker service or V2 was added. Source/provenance schema and default full-audit relationships remain compatible.

## Measurement provenance

{"os": "Windows", "release": "11", "machine": "AMD64", "python": "3.13.0", "logical_cpu_count": 8, "free_bytes_at_start": 469595725824}

{"trials": 1, "operation_timeout_seconds": 600, "latency": "Fresh worker process; imports/startup excluded; Path open/stat counters enabled. OS disk cache uncontrolled; not a cold-cache claim.", "memory": "Worker process lifetime peak working set on Windows; imports/checks included.", "setup": "Direct owned fixture provisioning, not production admission throughput.", "cost": "LLM tokens/API charges NOT MEASURED; no LLM API is called by the benchmark.", "selected_operations": ["source_lookup", "query_en", "query_vi", "validation", "incremental_update"]}

[Measured trials and fixture hashes](../reports/scalability-phase5-2026-10-18.json).
[Pre-optimization baseline](../reports/scalability-phase5-baseline-2026-10-18.json).

## 100 wiki documents + 100 raw snapshots

Fixture/navigation/filesystem: {"documents": 100, "raw_snapshots": 100, "fixture_build_seconds": 0.6335244000001694, "fixture_navigation_generation_seconds": 0.00773730000219075, "production_index_generation": "NOT MEASURED (no production generator)", "file_count": 217, "directory_count": 17, "logical_bytes": 451159, "allocated_disk_bytes": "NOT MEASURED", "corpus_sha256": "f32c2cf40a72c58516752e96bafba7e4ad015f34cee28d4bfe11bd843f9bcf6d", "recipe": "TEST_ONLY-scale-v1"}

- source_lookup: {"completed_trials": 1, "median_seconds": 0.003285499999037711, "max_seconds": 0.003285499999037711}; baseline: {"completed_trials": 1, "median_seconds": 0.004124399998545414, "max_seconds": 0.004124399998545414}
- query_en: {"completed_trials": 1, "median_seconds": 0.8248300999985076, "max_seconds": 0.8248300999985076}; baseline: {"completed_trials": 1, "median_seconds": 1.4150777000031667, "max_seconds": 1.4150777000031667}
- query_vi: {"completed_trials": 1, "median_seconds": 0.8032409999977972, "max_seconds": 0.8032409999977972}; baseline: {"completed_trials": 1, "median_seconds": 1.630455799997435, "max_seconds": 1.630455799997435}
- validation: {"completed_trials": 1, "median_seconds": 2.0034163000018452, "max_seconds": 2.0034163000018452}; baseline: {"completed_trials": 1, "median_seconds": 2.4371589999973367, "max_seconds": 2.4371589999973367}
- incremental_update: {"completed_trials": 1, "median_seconds": 1.6947605999994266, "max_seconds": 1.6947605999994266}; baseline: {"completed_trials": 1, "median_seconds": 1.6733605000008538, "max_seconds": 1.6733605000008538}
- Manifest opens: {"source_lookup": 1, "query_en": 1, "query_vi": 1, "validation": 3, "incremental_update": 7}
- Measured process memory: [{"peak_working_set_bytes": 33103872, "working_set_bytes": 31985664, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 33173504, "working_set_bytes": 32411648, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 33185792, "working_set_bytes": 32018432, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 33198080, "working_set_bytes": 32927744, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 33144832, "working_set_bytes": 32092160, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 33406976, "working_set_bytes": 32706560, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}]
- Quality safeguards: {"status": "MEASURED", "operation": "quality", "correct": true, "observed": {"wrong_scope": "NOT_FOUND", "missing_evidence_abstention": "NOT_FOUND", "same_size_mtime_raw_tamper": "MISSING_EVIDENCE", "injection": "UNTRUSTED_CONTENT", "verified_overwrite": "PROTECTED_KNOWLEDGE_UPDATE", "path_boundary": "WRITE_DENIED", "interrupted_query": "RECOVERY_REQUIRED", "recovery": "ROLLED_BACK", "all_fixture_hashes_restored": true}, "memory": {"peak_working_set_bytes": 33406976, "working_set_bytes": 32706560, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}}

## 1000 wiki documents + 1000 raw snapshots

Fixture/navigation/filesystem: {"documents": 1000, "raw_snapshots": 1000, "fixture_build_seconds": 11.324733500001457, "fixture_navigation_generation_seconds": 0.043021699999371776, "production_index_generation": "NOT MEASURED (no production generator)", "file_count": 2017, "directory_count": 17, "logical_bytes": 4496468, "allocated_disk_bytes": "NOT MEASURED", "corpus_sha256": "7091dd7804edf9c717d531e86d08b91ec3ac031ef41c8d832c9f99ae7c383fbe", "recipe": "TEST_ONLY-scale-v1"}

- source_lookup: {"completed_trials": 1, "median_seconds": 0.015728599999420112, "max_seconds": 0.015728599999420112}; baseline: {"completed_trials": 1, "median_seconds": 0.01526719999674242, "max_seconds": 0.01526719999674242}
- query_en: {"completed_trials": 1, "median_seconds": 12.305914099997608, "max_seconds": 12.305914099997608}; baseline: {"completed_trials": 1, "median_seconds": 15.312296800002514, "max_seconds": 15.312296800002514}
- query_vi: {"completed_trials": 1, "median_seconds": 10.486416799998551, "max_seconds": 10.486416799998551}; baseline: {"completed_trials": 1, "median_seconds": 14.898748700001306, "max_seconds": 14.898748700001306}
- validation: {"completed_trials": 1, "median_seconds": 19.82545780000146, "max_seconds": 19.82545780000146}; baseline: {"completed_trials": 1, "median_seconds": 43.282338599998184, "max_seconds": 43.282338599998184}
- incremental_update: {"completed_trials": 1, "median_seconds": 9.273870699998952, "max_seconds": 9.273870699998952}; baseline: {"completed_trials": 1, "median_seconds": 11.326551299996936, "max_seconds": 11.326551299996936}
- Manifest opens: {"source_lookup": 1, "query_en": 1, "query_vi": 1, "validation": 3, "incremental_update": 7}
- Measured process memory: [{"peak_working_set_bytes": 33484800, "working_set_bytes": 32006144, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 36110336, "working_set_bytes": 35713024, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 35758080, "working_set_bytes": 35524608, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 47026176, "working_set_bytes": 47026176, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 39297024, "working_set_bytes": 38010880, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 37908480, "working_set_bytes": 37908480, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}]
- Quality safeguards: {"status": "MEASURED", "operation": "quality", "correct": true, "observed": {"wrong_scope": "NOT_FOUND", "missing_evidence_abstention": "NOT_FOUND", "same_size_mtime_raw_tamper": "MISSING_EVIDENCE", "injection": "UNTRUSTED_CONTENT", "verified_overwrite": "PROTECTED_KNOWLEDGE_UPDATE", "path_boundary": "WRITE_DENIED", "interrupted_query": "RECOVERY_REQUIRED", "recovery": "ROLLED_BACK", "all_fixture_hashes_restored": true}, "memory": {"peak_working_set_bytes": 37908480, "working_set_bytes": 37908480, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}}

## 10000 wiki documents + 10000 raw snapshots

Fixture/navigation/filesystem: {"documents": 10000, "raw_snapshots": 10000, "fixture_build_seconds": 178.8921902000002, "fixture_navigation_generation_seconds": 0.28592660000140313, "production_index_generation": "NOT MEASURED (no production generator)", "file_count": 20017, "directory_count": 26, "logical_bytes": 44949915, "allocated_disk_bytes": "NOT MEASURED", "corpus_sha256": "483ffc3871b4a5215b1b58dd5f2a0436eb301e691aeb1610234a98dd96a3272f", "recipe": "TEST_ONLY-scale-v1"}

- source_lookup: {"completed_trials": 1, "median_seconds": 0.27427170000009937, "max_seconds": 0.27427170000009937}; baseline: "NOT RUN"
- query_en: {"completed_trials": 1, "median_seconds": 280.2969895999995, "max_seconds": 280.2969895999995}; baseline: "NOT RUN"
- query_vi: {"completed_trials": 1, "median_seconds": 103.08347560000038, "max_seconds": 103.08347560000038}; baseline: "NOT RUN"
- validation: {"completed_trials": 1, "median_seconds": 282.1866344000009, "max_seconds": 282.1866344000009}; baseline: "NOT RUN"
- incremental_update: {"completed_trials": 1, "median_seconds": 110.82470530000137, "max_seconds": 110.82470530000137}; baseline: "NOT RUN"
- Manifest opens: {"source_lookup": 1, "query_en": 1, "query_vi": 1, "validation": 3, "incremental_update": 7}
- Measured process memory: [{"peak_working_set_bytes": 39231488, "working_set_bytes": 34414592, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 70242304, "working_set_bytes": 61415424, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 70189056, "working_set_bytes": 61300736, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 178671616, "working_set_bytes": 132358144, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 88756224, "working_set_bytes": 77520896, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}, {"peak_working_set_bytes": 81960960, "working_set_bytes": 77852672, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}]
- Quality safeguards: {"status": "MEASURED", "operation": "quality", "correct": true, "observed": {"wrong_scope": "NOT_FOUND", "missing_evidence_abstention": "NOT_FOUND", "same_size_mtime_raw_tamper": "MISSING_EVIDENCE", "injection": "UNTRUSTED_CONTENT", "verified_overwrite": "PROTECTED_KNOWLEDGE_UPDATE", "path_boundary": "WRITE_DENIED", "interrupted_query": "RECOVERY_REQUIRED", "recovery": "ROLLED_BACK", "all_fixture_hashes_restored": true}, "memory": {"peak_working_set_bytes": 81960960, "working_set_bytes": 77852672, "definition": "Current worker process lifetime counters, including imports and checks; not operation-only allocations."}}

## Correctness and compatibility

{"run": 163, "passed": 163}

Measurement implementation mismatches: []

Every timed Query validates expected document/source/pointer/scope. Incremental probes compare all fixture hashes, observe a new keyword without rebuild and verify UNCHANGED retries. Separate per-size probes check wrong scope, missing documents, source tamper with unchanged size/mtime, injection, verified overwrite, path traversal, interrupted reads and exact recovery.
Default full Lint/source admission keep reverse relationships; only Query's redundant scan is omitted. Invalid registry/manifest edits are rediscovered on the next operation. Existing legacy readers and source/approval hashes remain regression-tested.

## Live workspace checks

- WARNING NO_EVIDENCE wiki/concepts/knowledge-system-principles.md: page has no registered source or approved decision evidence.
Live registered sources: 0. Synthetic corpora stay in owned temporary test directories.

## Cost and untested limits

{"LLM_tokens": "NOT MEASURED", "API_charges": "NOT MEASURED", "monetary_CPU_storage_cost": "NOT MEASURED", "note": "No LLM API is invoked by this benchmark. This is not a bill estimate for the chat or future pilot."}
- NOT MEASURED: P95, throughput or concurrent capacity
- NOT MEASURED: Cold OS-cache behavior
- NOT MEASURED: Physical disk allocation and wear
- NOT MEASURED: Real production corpus and human ingestion/approval throughput
- NOT MEASURED: Full-text incremental-index throughput (not implemented)
- NOT MEASURED: Semantic retrieval/reranking and LLM answer correctness
- NOT MEASURED: Obsidian UI performance
- NOT MEASURED: Host containment and physical power-loss recovery

No baseline 10,000-document timing was run: the smaller-size profile already justified eliminating redundant scans before that larger run. No baseline number is extrapolated as a measurement.

Single observations are not latency distributions or production limits. File/corpus counts and logical bytes do not measure allocated disk overhead. Source lookup does not by itself validate factual content.
The worker timeout includes imports, snapshots, retries and post-checks; incomplete workers have no completed verified latency. English/Vietnamese timing differences cannot be attributed to language because OS cache/I/O and order are uncontrolled.

## V1.1 pilot recommendation

Start with a separately authorized 25-100 page knowledge pilot; 2s interaction and 30s foreground maintenance budgets are PROVISIONAL. Larger measured sizes require accepting their observed delays or a separate index experiment; do not claim untested scale.

Proposed thresholds require human agreement. Actual source intake, retrieval backend choice and architecture approvals remain separate user decisions; this task authorizes none of them.

## Fresh automated test results

- PASS: test_check_workspace.WorkspaceChecks.test_all_required_manifest_values_are_checked
- PASS: test_check_workspace.WorkspaceChecks.test_approved_adr_can_support_a_first_party_project_decision
- PASS: test_check_workspace.WorkspaceChecks.test_bad_manifest_header_and_row_shape_are_errors
- PASS: test_check_workspace.WorkspaceChecks.test_checker_does_not_modify_or_create_workspace_files
- PASS: test_check_workspace.WorkspaceChecks.test_citations_can_continue_on_the_next_line
- PASS: test_check_workspace.WorkspaceChecks.test_cited_source_must_be_listed_in_page_metadata
- PASS: test_check_workspace.WorkspaceChecks.test_content_metadata_values_are_validated
- PASS: test_check_workspace.WorkspaceChecks.test_duplicate_manifest_ids_are_errors
- PASS: test_check_workspace.WorkspaceChecks.test_each_finding_needs_its_own_citation
- PASS: test_check_workspace.WorkspaceChecks.test_empty_registry_allows_explicit_unverified_draft
- PASS: test_check_workspace.WorkspaceChecks.test_escaped_links_are_rejected_without_accessing_outside_paths
- PASS: test_check_workspace.WorkspaceChecks.test_examples_and_comments_do_not_create_citations_or_links
- PASS: test_check_workspace.WorkspaceChecks.test_existing_starter_hypothesis_remains_valid
- PASS: test_check_workspace.WorkspaceChecks.test_exit_codes_and_output_distinguish_pass_warning_and_error
- PASS: test_check_workspace.WorkspaceChecks.test_http_sources_are_metadata_only_and_no_network_is_used
- PASS: test_check_workspace.WorkspaceChecks.test_images_and_encoded_or_angle_bracket_targets
- PASS: test_check_workspace.WorkspaceChecks.test_inline_links_are_checked_across_documentation_locations
- PASS: test_check_workspace.WorkspaceChecks.test_linked_paths_are_not_followed
- PASS: test_check_workspace.WorkspaceChecks.test_missing_and_unreadable_manifests_are_reported_without_tracebacks
- PASS: test_check_workspace.WorkspaceChecks.test_missing_raw_file_and_directory_targets_are_errors
- PASS: test_check_workspace.WorkspaceChecks.test_missing_wiki_entrypoints_are_reported
- PASS: test_check_workspace.WorkspaceChecks.test_orphans_are_reported_and_indirect_navigation_is_followed
- PASS: test_check_workspace.WorkspaceChecks.test_proposed_adr_and_decision_index_are_not_approved_evidence
- PASS: test_check_workspace.WorkspaceChecks.test_proposed_adr_can_be_linked_as_context_without_claiming_approval
- PASS: test_check_workspace.WorkspaceChecks.test_raw_bodies_and_protected_documents_are_never_opened
- PASS: test_check_workspace.WorkspaceChecks.test_registered_source_and_finding_pass
- PASS: test_check_workspace.WorkspaceChecks.test_source_dates_and_id_dates_are_real_calendar_dates
- PASS: test_check_workspace.WorkspaceChecks.test_source_paths_cannot_escape_raw_or_workspace
- PASS: test_check_workspace.WorkspaceChecks.test_source_paths_cannot_hide_linked_components_before_parent_segments
- PASS: test_check_workspace.WorkspaceChecks.test_structured_facts_require_citations_even_in_drafts
- PASS: test_check_workspace.WorkspaceChecks.test_template_can_be_copied_at_two_wiki_depths_without_broken_examples
- PASS: test_check_workspace.WorkspaceChecks.test_unknown_and_malformed_source_ids_are_reported
- PASS: test_check_workspace.WorkspaceChecks.test_unknown_author_or_publication_date_needs_an_explanatory_note
- PASS: test_check_workspace.WorkspaceChecks.test_unsupported_links_warn_and_heading_anchor_limit_is_explicit
- PASS: test_check_workspace.WorkspaceChecks.test_unverified_draft_and_reviewed_without_evidence_are_distinct
- PASS: test_check_workspace.WorkspaceChecks.test_utf8_bom_and_windows_newlines_are_supported
- PASS: test_knowledge_governance.GovernanceTests.test_01_valid_lifecycle_transitions_are_traceable
- PASS: test_knowledge_governance.GovernanceTests.test_02_invalid_transitions_do_not_write
- PASS: test_knowledge_governance.GovernanceTests.test_03_ai_cannot_verify_even_with_approval_or_model_agreement
- PASS: test_knowledge_governance.GovernanceTests.test_04_superseded_decision_is_never_current_truth
- PASS: test_knowledge_governance.GovernanceTests.test_05_historical_fact_retrieval_does_not_expire_by_age
- PASS: test_knowledge_governance.GovernanceTests.test_06_conflicting_sources_preserved_and_block_verified
- PASS: test_knowledge_governance.GovernanceTests.test_07_incorrect_project_scope_has_no_fallback_or_alias_leak
- PASS: test_knowledge_governance.GovernanceTests.test_08_explicit_cross_project_lookup_is_context_only
- PASS: test_knowledge_governance.GovernanceTests.test_09_proposed_decision_cannot_become_approved_by_citation
- PASS: test_knowledge_governance.GovernanceTests.test_10_missing_or_inconsistent_metadata_fails_closed
- PASS: test_knowledge_governance.GovernanceTests.test_apply_requires_authorization_and_plan_is_read_only
- PASS: test_knowledge_governance.GovernanceTests.test_archive_requires_human_and_history_is_opt_in
- PASS: test_knowledge_governance.GovernanceTests.test_conflict_resolution_needs_human_validation_then_reverification
- PASS: test_knowledge_governance.GovernanceTests.test_decision_approval_cannot_bypass_a_tampered_supporting_source
- PASS: test_knowledge_governance.GovernanceTests.test_first_party_choice_without_external_fact_uses_approval_evidence
- PASS: test_knowledge_governance.GovernanceTests.test_foreign_decision_is_context_not_local_configuration
- PASS: test_knowledge_governance.GovernanceTests.test_future_effective_policy_is_not_current
- PASS: test_knowledge_governance.GovernanceTests.test_global_knowledge_is_selected_explicitly
- PASS: test_knowledge_governance.GovernanceTests.test_governed_decision_source_references_are_validated
- PASS: test_knowledge_governance.GovernanceTests.test_human_label_without_validation_record_is_insufficient
- PASS: test_knowledge_governance.GovernanceTests.test_interpretation_and_hypothesis_are_not_verified_facts
- PASS: test_knowledge_governance.GovernanceTests.test_legacy_reviewed_is_not_verified_and_bytes_are_unchanged
- PASS: test_knowledge_governance.GovernanceTests.test_malformed_history_and_mixed_metadata_are_rejected
- PASS: test_knowledge_governance.GovernanceTests.test_query_and_audit_are_read_only
- PASS: test_knowledge_governance.GovernanceTests.test_referenced_decision_cannot_hide_a_changed_supporting_source
- PASS: test_knowledge_governance.GovernanceTests.test_restricted_scope_requires_explicit_authorization
- PASS: test_knowledge_governance.GovernanceTests.test_review_due_is_warning_not_automatic_obsolescence
- PASS: test_knowledge_governance.GovernanceTests.test_same_scope_approved_decision_can_support_a_project_choice
- PASS: test_knowledge_governance.GovernanceTests.test_source_tampering_still_blocks_governed_verified_knowledge
- PASS: test_knowledge_governance.GovernanceTests.test_unapproved_historical_label_does_not_create_decision_evidence
- PASS: test_knowledge_governance.GovernanceTests.test_verified_body_or_scope_edit_invalidates_approval
- PASS: test_multilingual.MultilingualTests.test_accents_are_not_silently_removed_or_synonyms_invented
- PASS: test_multilingual.MultilingualTests.test_alias_and_vietnamese_title_add_only_declared_english_terms
- PASS: test_multilingual.MultilingualTests.test_aliases_do_not_leak_from_another_project
- PASS: test_multilingual.MultilingualTests.test_all_25_pairs_have_observed_results
- PASS: test_multilingual.MultilingualTests.test_ambiguous_alias_does_not_pick_an_arbitrary_document
- PASS: test_multilingual.MultilingualTests.test_identifiers_routes_and_filenames_retain_original_spelling
- PASS: test_multilingual.MultilingualTests.test_invalid_registry_fails_closed
- PASS: test_multilingual.MultilingualTests.test_linter_and_search_reject_bad_metadata
- PASS: test_multilingual.MultilingualTests.test_missing_evidence_is_not_a_source_backed_answer
- PASS: test_multilingual.MultilingualTests.test_old_metadata_defaults_and_legacy_retrieval
- PASS: test_multilingual.MultilingualTests.test_optional_metadata_rejects_invalid_types_and_duplicates
- PASS: test_multilingual.MultilingualTests.test_other_project_bad_metadata_does_not_change_selected_scope
- PASS: test_multilingual.MultilingualTests.test_punctuation_bearing_technical_keywords_are_literal
- PASS: test_multilingual.MultilingualTests.test_raw_bodies_are_not_opened_and_network_is_not_used
- PASS: test_multilingual.MultilingualTests.test_report_writer_rejects_existing_or_protected_paths
- PASS: test_multilingual.MultilingualTests.test_scope_is_required_and_never_inferred
- PASS: test_multilingual.MultilingualTests.test_search_does_not_write_or_translate_any_file
- PASS: test_multilingual.MultilingualTests.test_underscored_fields_are_parsed
- PASS: test_multilingual.MultilingualTests.test_unicode_nfc_nfd_case_and_spacing_match
- PASS: test_scalability.ScaleSafetyTests.test_10000_source_ids_are_valid_and_unique
- PASS: test_scalability.ScaleSafetyTests.test_fixture_root_cannot_target_live_knowledge
- PASS: test_scalability.ScaleSafetyTests.test_governance_batch_parses_registry_once
- PASS: test_scalability.ScaleSafetyTests.test_measurement_data_cannot_select_files_to_read
- PASS: test_scalability.ScaleSafetyTests.test_profile_only_results_cannot_claim_full_load_correctness
- PASS: test_scalability.ScaleSafetyTests.test_query_reuses_validated_ids_only_within_one_operation
- PASS: test_scalability.ScaleSafetyTests.test_query_skips_only_the_redundant_reverse_wiki_scan
- PASS: test_scalability.ScaleSafetyTests.test_raw_same_size_mtime_edit_remains_detectable
- PASS: test_scalability.ScaleSafetyTests.test_recipe_and_hierarchical_index_are_reproducible
- PASS: test_scalability.ScaleSafetyTests.test_registry_metadata_hash_is_not_cached_between_queries
- PASS: test_scalability.ScaleSafetyTests.test_timeout_is_not_a_completed_latency_or_pass
- PASS: test_security_recovery.SecurityRecoveryTests.test_01_prompt_injection_in_source_is_blocked_on_actual_ingest_path
- PASS: test_security_recovery.SecurityRecoveryTests.test_02_fake_priority_and_hidden_instructions_block_actual_query
- PASS: test_security_recovery.SecurityRecoveryTests.test_03_unauthorized_policy_modification_has_no_write_capability
- PASS: test_security_recovery.SecurityRecoveryTests.test_04_path_traversal_and_windows_aliases_are_rejected
- PASS: test_security_recovery.SecurityRecoveryTests.test_05_sensitive_locations_are_rejected_before_open
- PASS: test_security_recovery.SecurityRecoveryTests.test_06_failed_write_midway_restores_all_owned_resources
- PASS: test_security_recovery.SecurityRecoveryTests.test_07_failed_ingestion_rolls_back_without_removing_approved_source
- PASS: test_security_recovery.SecurityRecoveryTests.test_08_concurrent_writers_cannot_silently_lose_updates
- PASS: test_security_recovery.SecurityRecoveryTests.test_09_generated_report_redacts_secret_keys_and_values
- PASS: test_security_recovery.SecurityRecoveryTests.test_10_crash_recovery_preserves_every_unrelated_user_file
- PASS: test_security_recovery.SecurityRecoveryTests.test_approval_and_source_command_cannot_expand_the_write_allowlist
- PASS: test_security_recovery.SecurityRecoveryTests.test_committed_operation_recovery_keeps_complete_result
- PASS: test_security_recovery.SecurityRecoveryTests.test_fake_labeled_identity_is_flagged_without_value_in_output
- PASS: test_security_recovery.SecurityRecoveryTests.test_new_raw_snapshot_never_publishes_partial_bytes
- PASS: test_security_recovery.SecurityRecoveryTests.test_old_report_writers_use_the_redaction_boundary
- PASS: test_security_recovery.SecurityRecoveryTests.test_query_rejects_a_generation_changed_during_retrieval
- PASS: test_security_recovery.SecurityRecoveryTests.test_raw_policy_filename_is_blocked_before_publication
- PASS: test_security_recovery.SecurityRecoveryTests.test_recovery_refuses_to_overwrite_edits_made_after_interruption
- PASS: test_security_recovery.SecurityRecoveryTests.test_sensitive_generated_wiki_is_blocked_before_backup_or_commit
- PASS: test_security_recovery.SecurityRecoveryTests.test_stale_owner_requires_explicit_human_recovery_acknowledgement
- PASS: test_security_recovery.SecurityRecoveryTests.test_successful_ingestion_is_atomic_draft_and_query_remains_data
- PASS: test_security_recovery.SecurityRecoveryTests.test_synthetic_private_key_block_is_redacted_as_a_whole
- PASS: test_security_recovery.SecurityRecoveryTests.test_tampered_journal_cannot_target_operating_policy
- PASS: test_source_integrity.SourceIntegrityTests.test_01_valid_registration_and_unknown_metadata
- PASS: test_source_integrity.SourceIntegrityTests.test_02_duplicate_ingestion_is_idempotent_and_content_deduplicated
- PASS: test_source_integrity.SourceIntegrityTests.test_03_duplicate_id_with_different_content_is_rejected
- PASS: test_source_integrity.SourceIntegrityTests.test_04_hash_mismatch_blocks_source_and_query
- PASS: test_source_integrity.SourceIntegrityTests.test_05_missing_source_file_is_detected
- PASS: test_source_integrity.SourceIntegrityTests.test_06_invalid_wiki_reference_is_detected
- PASS: test_source_integrity.SourceIntegrityTests.test_07_missing_required_metadata_is_rejected_before_writes
- PASS: test_source_integrity.SourceIntegrityTests.test_08_unavailable_original_url_retains_local_evidence_without_network
- PASS: test_source_integrity.SourceIntegrityTests.test_09_attempted_raw_modification_is_refused
- PASS: test_source_integrity.SourceIntegrityTests.test_10_source_version_replacement_preserves_old_snapshot_and_references
- PASS: test_source_integrity.SourceIntegrityTests.test_audit_and_query_are_read_only_and_only_hash_raw_bytes
- PASS: test_source_integrity.SourceIntegrityTests.test_binary_sources_are_hashed_without_text_decoding
- PASS: test_source_integrity.SourceIntegrityTests.test_claim_with_no_evidence_stays_unknown
- PASS: test_source_integrity.SourceIntegrityTests.test_corrupt_duplicate_and_orphan_provenance_fail_closed
- PASS: test_source_integrity.SourceIntegrityTests.test_forked_and_out_of_sequence_versions_are_rejected_before_append
- PASS: test_source_integrity.SourceIntegrityTests.test_hash_matching_never_promotes_verification_status
- PASS: test_source_integrity.SourceIntegrityTests.test_interrupted_registration_rolls_back_metadata_without_touching_raw
- PASS: test_source_integrity.SourceIntegrityTests.test_known_origin_revision_needs_explicit_version_link
- PASS: test_source_integrity.SourceIntegrityTests.test_legacy_migration_is_explicit_readonly_planning_and_append_only_apply
- PASS: test_source_integrity.SourceIntegrityTests.test_manifest_metadata_tampering_is_detected
- PASS: test_source_integrity.SourceIntegrityTests.test_manually_duplicated_content_is_detected
- PASS: test_source_integrity.SourceIntegrityTests.test_metadata_only_replacement_can_reuse_immutable_bytes
- PASS: test_source_integrity.SourceIntegrityTests.test_migration_detects_changed_bytes_since_proposal
- PASS: test_source_integrity.SourceIntegrityTests.test_multiple_sources_support_one_claim_and_one_bad_source_blocks_it
- PASS: test_source_integrity.SourceIntegrityTests.test_remote_only_legacy_record_requires_an_authorized_snapshot
- PASS: test_source_integrity.SourceIntegrityTests.test_stale_lock_is_not_deleted_or_ignored
- PASS: test_workflow_reliability.BenchmarkTests.test_independent_corpus_and_thirty_query_pairs
- PASS: test_workflow_reliability.WorkflowTests.test_01_registration_provenance_ingest_query_lint
- PASS: test_workflow_reliability.WorkflowTests.test_02_duplicate_registration_reuses_identity_and_bytes
- PASS: test_workflow_reliability.WorkflowTests.test_03_fresh_plan_for_identical_content_does_not_duplicate_log
- PASS: test_workflow_reliability.WorkflowTests.test_04_existing_draft_update_retains_old_evidence
- PASS: test_workflow_reliability.WorkflowTests.test_05_bounded_wiki_transaction_cannot_bypass_verified_guard
- PASS: test_workflow_reliability.WorkflowTests.test_06_scope_and_transition_history_cannot_be_reset_by_ingest
- PASS: test_workflow_reliability.WorkflowTests.test_07_conflicting_information_and_pointers_are_preserved
- PASS: test_workflow_reliability.WorkflowTests.test_08_missing_index_and_missing_log_are_rejected_before_write
- PASS: test_workflow_reliability.WorkflowTests.test_09_ingest_cannot_remove_existing_index_links
- PASS: test_workflow_reliability.WorkflowTests.test_10_failed_ingest_rolls_back_and_retry_succeeds
- PASS: test_workflow_reliability.WorkflowTests.test_11_interrupted_ingest_requires_recovery_then_retry
- PASS: test_workflow_reliability.WorkflowTests.test_12_stale_update_does_not_overwrite_newer_user_work
- PASS: test_workflow_reliability.WorkflowTests.test_13_invalid_citation_plan_does_not_leave_partial_files
- PASS: test_workflow_reliability.WorkflowTests.test_identical_ingest_retry_is_a_read_only_noop
- PASS: test_workflow_reliability.WorkflowTests.test_ingest_cannot_reset_verified_knowledge_to_draft
- PASS: test_workflow_reliability.WorkflowTests.test_lifecycle_operation_cannot_reset_verified_history
- PASS: test_workflow_reliability.WorkflowTests.test_lint_broken_markdown_link
- PASS: test_workflow_reliability.WorkflowTests.test_lint_contradictory_current_decision_slots_require_review
- PASS: test_workflow_reliability.WorkflowTests.test_lint_duplicate_index_target
- PASS: test_workflow_reliability.WorkflowTests.test_lint_duplicate_page_identity
- PASS: test_workflow_reliability.WorkflowTests.test_lint_invalid_frontmatter_does_not_ignore_yaml
- PASS: test_workflow_reliability.WorkflowTests.test_lint_invalid_lifecycle_transition
- PASS: test_workflow_reliability.WorkflowTests.test_lint_missing_source_reference
- PASS: test_workflow_reliability.WorkflowTests.test_lint_orphan_and_missing_index_entry
- PASS: test_workflow_reliability.WorkflowTests.test_lint_potentially_stale_does_not_change_status
- PASS: test_workflow_reliability.WorkflowTests.test_lint_rejects_a_source_id_without_an_exact_pointer
- PASS: test_workflow_reliability.WorkflowTests.test_lint_unreviewed_knowledge_is_not_verified

No deployment, push, merge or V2 implementation was performed.
