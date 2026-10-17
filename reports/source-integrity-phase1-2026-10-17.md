# Phase 1 — Source Integrity Audit

First-party observed repository audit and synthetic test results. No real source ingestion.

## Final verdict

**PASS** — Source-integrity contract, current registry and synthetic fixtures; not factual correctness or Phase 2.

Observed: 81 automated tests; 81 PASS, 0 failures, 0 errors, 0 skipped.
Live registered sources: 0; hash-matched live sources: 0.
Strict workspace errors: 0; warnings: 1.

## Discovery and inconsistencies

- Discovery baseline b2acfef already had unique ID/date validation, CSV checks, wiki references, structured citations, path guards and bilingual lexical search. Existing features were extended.
- The old citation gate checked file existence: a recorded synthetic baseline experiment changed raw bytes but still returned FOUND. Hash-backed sources now fail closed on that change.
- Old documentation said Query never opened raw. The current contract explicitly distinguishes legacy metadata-only retrieval from binary hash verification for recorded provenance.
- Immutability and source revisions previously had written rules but no admission/version guard. Exclusive snapshots, append-only admission, duplicate policy and lineage validation now implement them.
- A pre-existing .obsidian/graph.json working change was excluded from the implementation scope.

## Contract and compatibility

See [provenance contract and migration notes](../SOURCE_INTEGRITY.md). The nine-column CSV is unchanged; new metadata is an append-only ledger. Missing author/publisher/date/origin stays unknown. A matching hash does not set VERIFIED.
Existing compatibility tests, including paired bilingual retrieval, are included in the run below. The legacy migration test verifies raw/CSV preservation and explicit baseline creation.

## Requested synthetic scenarios

- PASS: test_01_valid_registration_and_unknown_metadata
- PASS: test_02_duplicate_ingestion_is_idempotent_and_content_deduplicated
- PASS: test_03_duplicate_id_with_different_content_is_rejected
- PASS: test_04_hash_mismatch_blocks_source_and_query
- PASS: test_05_missing_source_file_is_detected
- PASS: test_06_invalid_wiki_reference_is_detected
- PASS: test_07_missing_required_metadata_is_rejected_before_writes
- PASS: test_08_unavailable_original_url_retains_local_evidence_without_network
- PASS: test_09_attempted_raw_modification_is_refused
- PASS: test_10_source_version_replacement_preserves_old_snapshot_and_references

## Acceptance evidence

- PASS: Unambiguous identity and deterministic duplicates.
- PASS: Validated source references and multi-source traceability.
- PASS: Detectable raw and manifest tampering.
- PASS: Controlled source replacement.
- PASS: Backward compatibility or tested migration.

## All observed test cases

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
- PASS: test_source_integrity.SourceIntegrityTests.test_interrupted_registration_is_an_orphan_not_a_trusted_source
- PASS: test_source_integrity.SourceIntegrityTests.test_known_origin_revision_needs_explicit_version_link
- PASS: test_source_integrity.SourceIntegrityTests.test_legacy_migration_is_explicit_readonly_planning_and_append_only_apply
- PASS: test_source_integrity.SourceIntegrityTests.test_manifest_metadata_tampering_is_detected
- PASS: test_source_integrity.SourceIntegrityTests.test_manually_duplicated_content_is_detected
- PASS: test_source_integrity.SourceIntegrityTests.test_metadata_only_replacement_can_reuse_immutable_bytes
- PASS: test_source_integrity.SourceIntegrityTests.test_migration_detects_changed_bytes_since_proposal
- PASS: test_source_integrity.SourceIntegrityTests.test_multiple_sources_support_one_claim_and_one_bad_source_blocks_it
- PASS: test_source_integrity.SourceIntegrityTests.test_remote_only_legacy_record_requires_an_authorized_snapshot
- PASS: test_source_integrity.SourceIntegrityTests.test_stale_lock_is_not_deleted_or_ignored

## Remaining risks and checks not run

- No real knowledge was ingested; an empty live registry is explicitly reported.
- Original URL availability is recorded metadata, never a live network verification here.
- Legacy sources without a baseline remain LEGACY_UNHASHED and fail strict admission until migration.
- Migration records current bytes, not proof of historical immutability.
- Two metadata appends are not an atomic transaction; an interruption fails closed as an orphan.
- Hashes and citations do not prove factual correctness; trusted Git history protects the baseline.
- No external URL requests, real-source ingestion, Obsidian visual check, Phase 2 or V2 work was performed.
- Interrupted registration requires human reconciliation against the surviving record and raw hash; the tool never truncates provenance or automatically removes an existing lock.

## Reproduce

~~~text
python -B scripts/validate_source_integrity.py
python -B scripts/check_workspace.py --integrity
~~~

The runner uses standard-library unittest discovery and writes reports only with an explicit new output path.
