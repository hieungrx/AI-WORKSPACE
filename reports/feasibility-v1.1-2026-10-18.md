# V1.1 — Synthetic feasibility harness

**Real-world feasibility: NOT YET MEASURED. Verdict: INCONCLUSIVE.**

Harness: PASS. No AI model was invoked; no independent human score was produced.

Dataset: {"sources": 30, "cases": 103, "by_category": {"knowledge": 30, "bilingual": 40, "evolution": 10, "scope": 10, "continuity": 5, "task": 8}, "bilingual_pairs": 20}

Paired retrieval cases: 80; actual arm executions: 160. Seed: 1101. Runtime HEAD: 457a9bf6db7bb2476117200f76586032ca1e432b.

The 23 protocol-only gold cases (10 evolution, 5 AI-session continuity, 8 research/coding tasks) remain NOT RUN. The generic evolution demonstration below does not replace running those case-specific rubrics.

## Baseline A and wiki B — component diagnostics only

A reads all permitted raw bytes and independent title/scope metadata. B uses actual wiki Query plus those same raw sources. Both are deterministic helpers, not equivalent AI workflows. Wiki aliases/curation are the intended extra artifact; the raw adapter cannot demonstrate how a competent AI would use raw materials.

Retrieval quality outcomes (separate from infrastructure): {"A": {"HIT": 40, "MISS": 32, "CORRECT_ABSTENTION_SIGNAL": 8}, "B": {"HIT": 54, "MISS": 18, "CORRECT_ABSTENTION_SIGNAL": 8}}

### A

- recall_at_5: {"status": "MEASURED", "value": 0.5555555555555556, "samples": 72, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": "Macro source Recall@5: first 5 distinct source IDs projected from ranked candidates; nonempty gold, blocked identities included; no answer score."}
- citation_structural_validity: {"status": "MEASURED", "value": 1.0, "samples": 45, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": "Recorded source ID/path/hash status and Evidence heading; not factual truth.", "numerator": 45, "denominator": 45}
- citation_gold_agreement: {"status": "MEASURED", "value": 0.9333333333333333, "samples": 45, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": "Cited source IDs present in the independent relevance gold; meaning NOT assessed.", "numerator": 42, "denominator": 45}
- cross_project_leakage: {"status": "MEASURED", "value": 0.0, "samples": 80, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": "Trials returning an out-of-scope candidate.", "numerator": 0, "denominator": 80}
- unauthorized_current_flags: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": "Returned wiki flags for this unverified-only corpus; NOT AI factual assertions.", "numerator": 0, "denominator": 0}
- query_elapsed_mean_seconds: {"status": "MEASURED", "value": 0.5334771649999936, "samples": 80, "unit": "seconds", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": "Actual adapter elapsed time, uncontrolled OS cache; not human/AI task time."}
- task_correctness: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- factual_correctness: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- citation_semantic_accuracy: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- context_continuity_quality: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- unsupported_AI_current_truth_assertions: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- human_corrections: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- human_review_seconds: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- AI_task_elapsed_seconds: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- context_tokens: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- token_usage: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- API_cost: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- net_productivity: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- repeated_research_steps: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
### B

- recall_at_5: {"status": "MEASURED", "value": 0.75, "samples": 72, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": "Macro source Recall@5: first 5 distinct source IDs projected from ranked candidates; nonempty gold, blocked identities included; no answer score."}
- citation_structural_validity: {"status": "MEASURED", "value": 1.0, "samples": 57, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": "Recorded source ID/path/hash status and Evidence heading; not factual truth.", "numerator": 57, "denominator": 57}
- citation_gold_agreement: {"status": "MEASURED", "value": 0.9824561403508771, "samples": 57, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": "Cited source IDs present in the independent relevance gold; meaning NOT assessed.", "numerator": 56, "denominator": 57}
- cross_project_leakage: {"status": "MEASURED", "value": 0.0, "samples": 80, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": "Trials returning an out-of-scope candidate.", "numerator": 0, "denominator": 80}
- unauthorized_current_flags: {"status": "MEASURED", "value": 0.0, "samples": 57, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": "Returned wiki flags for this unverified-only corpus; NOT AI factual assertions.", "numerator": 0, "denominator": 57}
- query_elapsed_mean_seconds: {"status": "MEASURED", "value": 0.6332434675000173, "samples": 80, "unit": "seconds", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": "Actual adapter elapsed time, uncontrolled OS cache; not human/AI task time."}
- task_correctness: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- factual_correctness: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- citation_semantic_accuracy: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- context_continuity_quality: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- unsupported_AI_current_truth_assertions: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- human_corrections: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- human_review_seconds: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- AI_task_elapsed_seconds: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- context_tokens: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- token_usage: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- API_cost: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- net_productivity: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}
- repeated_research_steps: {"status": "NOT MEASURED", "value": null, "samples": 0, "unit": "ratio", "scope": "synthetic deterministic component; no AI model, human score or real pilot", "definition": ""}

## Knowledge evolution and recovery

{
  "passed": true,
  "synthetic_only": true,
  "checks": {
    "initial_query_found_unverified": true,
    "initial_query_read_only": true,
    "failed_update_injected_after_first_owned_replacement": true,
    "failed_existing_update_exact_rollback": true,
    "failed_update_no_pending_journal_or_lock": true,
    "retry_committed": true,
    "original_claim_retained_verbatim": true,
    "both_conflicting_claims_retained": true,
    "original_transition_prefix_retained": true,
    "conflict_query_disputed_with_both_references": true,
    "strict_lint_no_errors": true,
    "query_and_lint_read_only": true,
    "three_sources_intact_and_unverified": true,
    "unrelated_raw_and_append_only_prefixes_preserved": true,
    "no_approval_records_created": true,
    "fresh_python_continuity": true,
    "scenario_completed": true
  },
  "observations": [
    {
      "stage": "unrelated_draft_ingest",
      "result": {
        "status": "COMMITTED",
        "source_id": "SRC-20261018-803",
        "input_trust": "UNTRUSTED_DATA",
        "output_trust": "UNTRUSTED_DATA",
        "paths": [
          "wiki/cache-policy.md",
          "wiki/index.md",
          "wiki/log.md"
        ],
        "source_data_executed": false,
        "operation_id": "da29de38582645568aa95e9f89f39baa",
        "files": 3
      }
    },
    {
      "stage": "source_a_admission",
      "result": {
        "status": "REGISTERED",
        "source_id": "SRC-20261018-801"
      }
    },
    {
      "stage": "initial_draft_ingest",
      "result": {
        "status": "COMMITTED",
        "source_id": "SRC-20261018-801",
        "input_trust": "UNTRUSTED_DATA",
        "output_trust": "UNTRUSTED_DATA",
        "paths": [
          "wiki/index.md",
          "wiki/log.md",
          "wiki/request-budget.md"
        ],
        "source_data_executed": false,
        "operation_id": "65cda144a6914a62b6da9048092f9c45",
        "files": 3
      }
    },
    {
      "stage": "initial_query",
      "result": {
        "query": "giới hạn yêu cầu",
        "scope": "synthetic-workbench",
        "retrieval_only": true,
        "expanded_terms": [
          "Lyra API",
          "request budget"
        ],
        "matches": [
          {
            "content_trust": "UNTRUSTED_DATA",
            "path": "wiki/request-budget.md",
            "title": "Lyra API request budget",
            "title_vi": "",
            "language": "en",
            "scope": "synthetic-workbench",
            "page_status": "unverified",
            "knowledge_status": "unverified",
            "information_type": "external_fact",
            "created_at": "2026-10-18",
            "updated_at": "2026-10-18",
            "effective_at": null,
            "reviewed_at": null,
            "temporal": "current",
            "decision_authority": null,
            "freshness": [],
            "conflicts": [],
            "superseded_by": null,
            "usable_as_current_truth": false,
            "eligibility_reasons": [
              "NOT_CURRENT_KNOWLEDGE"
            ],
            "evidence_issues": [],
            "cross_project_context": false,
            "score": 3,
            "matched_fields": [
              "aliases_vi"
            ],
            "matched_terms": [
              "giới hạn yêu cầu"
            ],
            "expansion_terms": [
              "Lyra API",
              "request budget"
            ],
            "citations": [
              {
                "source_id": "SRC-20261018-801",
                "source_path": "sources/raw/SRC-20261018-801.md",
                "integrity_status": "MATCH",
                "source_version": 1,
                "verification_status": "UNVERIFIED",
                "superseded_by": null,
                "original_uri_status": "UNKNOWN",
                "source_uri": null,
                "source_pointer": "section Evidence"
              }
            ]
          }
        ],
        "blocked": [],
        "status": "FOUND",
        "message": "Đã tìm thấy tài liệu có con trỏ nguồn; nội dung claim chưa được tự động xác minh."
      }
    },
    {
      "stage": "source_b_admission",
      "result": {
        "status": "REGISTERED",
        "source_id": "SRC-20261018-802"
      }
    },
    {
      "stage": "failed_existing_update",
      "result": {
        "error": "TEST_ONLY_FEASIBILITY_WRITE_FAILURE",
        "owned_replacements_attempted": 2,
        "before_hashes": {
          "reports/validation.md": "94cf28ffa7c8a4cb130af51b0e219da0c6a28ac2546adc892bc492d51b5c796e",
          "sources/manifest.csv": "538bc78e5e1cda40a6c21af754a16c2c06595392b23b440c602f50df6657b78e",
          "sources/provenance.jsonl": "7e9b7614c3f4b5c4d033fe88b719ef7482a920ce652db254bfc753ecc6365668",
          "wiki/cache-policy.md": "58ecc5c4a32fccd3b7a71238e85675a52e4d9ec893537a8566a650370fa18909",
          "wiki/index.md": "abe2b93405e0a1f92f9b36fb8a2b40bda247854861eeeb903c9c54e77a1dddc2",
          "wiki/log.md": "40834fe84f0bc57cd358d2016a42ef4559543c6e137532eae4af2e0d6d0dcebd",
          "wiki/request-budget.md": "da90ce1d40ca7d7d7248be0d64e053f8ee790f8b0316c4b5596a7c7e8cc72839",
          "sources/raw/SRC-20261018-801.md": "720ab214bdad9adaa235c8bcebaab8b0f942daf1f0892493080a884a28d1580c",
          "sources/raw/SRC-20261018-802.md": "f881fa364b090738205d5f52033ee41584eeba32850b851dec6b4d84638c4f60",
          "sources/raw/SRC-20261018-803.md": "aa86692d36c5d70d308b4700e2c827b8f8485d33586f4b97a6d70151b3372c18"
        },
        "after_hashes": {
          "reports/validation.md": "94cf28ffa7c8a4cb130af51b0e219da0c6a28ac2546adc892bc492d51b5c796e",
          "sources/manifest.csv": "538bc78e5e1cda40a6c21af754a16c2c06595392b23b440c602f50df6657b78e",
          "sources/provenance.jsonl": "7e9b7614c3f4b5c4d033fe88b719ef7482a920ce652db254bfc753ecc6365668",
          "wiki/cache-policy.md": "58ecc5c4a32fccd3b7a71238e85675a52e4d9ec893537a8566a650370fa18909",
          "wiki/index.md": "abe2b93405e0a1f92f9b36fb8a2b40bda247854861eeeb903c9c54e77a1dddc2",
          "wiki/log.md": "40834fe84f0bc57cd358d2016a42ef4559543c6e137532eae4af2e0d6d0dcebd",
          "wiki/request-budget.md": "da90ce1d40ca7d7d7248be0d64e053f8ee790f8b0316c4b5596a7c7e8cc72839",
          "sources/raw/SRC-20261018-801.md": "720ab214bdad9adaa235c8bcebaab8b0f942daf1f0892493080a884a28d1580c",
          "sources/raw/SRC-20261018-802.md": "f881fa364b090738205d5f52033ee41584eeba32850b851dec6b4d84638c4f60",
          "sources/raw/SRC-20261018-803.md": "aa86692d36c5d70d308b4700e2c827b8f8485d33586f4b97a6d70151b3372c18"
        }
      }
    },
    {
      "stage": "retry_conflicting_draft_update",
      "result": {
        "status": "COMMITTED",
        "source_id": "SRC-20261018-802",
        "input_trust": "UNTRUSTED_DATA",
        "output_trust": "UNTRUSTED_DATA",
        "paths": [
          "wiki/index.md",
          "wiki/log.md",
          "wiki/request-budget.md"
        ],
        "source_data_executed": false,
        "operation_id": "642da06595be48868a35bf0ac3f5f163",
        "files": 3
      }
    },
    {
      "stage": "disputed_query",
      "result": {
        "query": "giới hạn yêu cầu",
        "scope": "synthetic-workbench",
        "retrieval_only": true,
        "expanded_terms": [
          "Lyra API",
          "request budget"
        ],
        "matches": [],
        "blocked": [
          {
            "content_trust": "UNTRUSTED_DATA",
            "path": "wiki/request-budget.md",
            "title": "Lyra API request budget",
            "title_vi": "",
            "language": "en",
            "scope": "synthetic-workbench",
            "page_status": "disputed",
            "knowledge_status": "disputed",
            "information_type": "external_fact",
            "created_at": "2026-10-18",
            "updated_at": "2026-10-18",
            "effective_at": null,
            "reviewed_at": null,
            "temporal": "current",
            "decision_authority": null,
            "freshness": [
              "UNRESOLVED_CONFLICT"
            ],
            "conflicts": [
              {
                "summary": "TEST_ONLY contradictory request budgets; no winner selected.",
                "source_ids": [
                  "SRC-20261018-801",
                  "SRC-20261018-802"
                ],
                "resolution": null
              }
            ],
            "superseded_by": null,
            "usable_as_current_truth": false,
            "eligibility_reasons": [
              "UNRESOLVED_CONFLICT"
            ],
            "evidence_issues": [],
            "cross_project_context": false,
            "score": 3,
            "matched_fields": [
              "aliases_vi"
            ],
            "matched_terms": [
              "giới hạn yêu cầu"
            ],
            "expansion_terms": [
              "Lyra API",
              "request budget"
            ],
            "citations": [
              {
                "source_id": "SRC-20261018-801",
                "source_path": "sources/raw/SRC-20261018-801.md",
                "integrity_status": "MATCH",
                "source_version": 1,
                "verification_status": "UNVERIFIED",
                "superseded_by": null,
                "original_uri_status": "UNKNOWN",
                "source_uri": null,
                "source_pointer": "section Evidence"
              },
              {
                "source_id": "SRC-20261018-802",
                "source_path": "sources/raw/SRC-20261018-802.md",
                "integrity_status": "MATCH",
                "source_version": 1,
                "verification_status": "UNVERIFIED",
                "superseded_by": null,
                "original_uri_status": "UNKNOWN",
                "source_uri": null,
                "source_pointer": "section Evidence"
              }
            ]
          }
        ],
        "status": "DISPUTED",
        "message": "Tài liệu có tranh chấp chưa giải quyết; giữ cả hai nguồn và yêu cầu rà soát."
      }
    },
    {
      "stage": "strict_lint",
      "result": {
        "issues": [
          "WARNING UNRESOLVED_CONFLICT wiki/request-budget.md: review required; no automatic state change.",
          "WARNING UNREVIEWED_KNOWLEDGE wiki/cache-policy.md: knowledge awaits authorized validation; citations are not factual verification."
        ],
        "errors": 0,
        "warnings": 2
      }
    }
  ],
  "maintenance_elapsed_seconds": {
    "unrelated_source_admission": 1.0327290000000175,
    "unrelated_draft_ingest": 0.840538800000104,
    "source_a_admission": 1.2780842999995912,
    "initial_draft_ingest": 0.8712676999998621,
    "initial_unverified_transition": 0.6009578000002875,
    "initial_query": 0.06657809999978781,
    "return_to_draft": 0.5275550000001203,
    "source_b_admission": 1.1044468000000052,
    "failed_update_and_automatic_rollback": 0.896277000000282,
    "retry_conflicting_draft_update": 0.9599342999999863,
    "updated_unverified_transition": 0.48310940000010305,
    "disputed_transition": 0.5541215000002921,
    "disputed_query": 0.07930390000001353,
    "strict_lint": 0.15007520000017394,
    "source_integrity_audit": 0.04413269999986369,
    "fresh_python_query": 0.830797099999927
  },
  "subprocess_continuity": {
    "status": "PASS",
    "method": "fresh Python subprocess, not a new agent or human review",
    "conversation_history_supplied": false,
    "include_history": false,
    "exit_code": 0,
    "query": "giới hạn yêu cầu",
    "scope": "synthetic-workbench",
    "stderr": "",
    "output": {
      "query": "giới hạn yêu cầu",
      "scope": "synthetic-workbench",
      "retrieval_only": true,
      "expanded_terms": [
        "Lyra API",
        "request budget"
      ],
      "matches": [],
      "blocked": [
        {
          "content_trust": "UNTRUSTED_DATA",
          "path": "wiki/request-budget.md",
          "title": "Lyra API request budget",
          "title_vi": "",
          "language": "en",
          "scope": "synthetic-workbench",
          "page_status": "disputed",
          "knowledge_status": "disputed",
          "information_type": "external_fact",
          "created_at": "2026-10-18",
          "updated_at": "2026-10-18",
          "effective_at": null,
          "reviewed_at": null,
          "temporal": "current",
          "decision_authority": null,
          "freshness": [
            "UNRESOLVED_CONFLICT"
          ],
          "conflicts": [
            {
              "summary": "TEST_ONLY contradictory request budgets; no winner selected.",
              "source_ids": [
                "SRC-20261018-801",
                "SRC-20261018-802"
              ],
              "resolution": null
            }
          ],
          "superseded_by": null,
          "usable_as_current_truth": false,
          "eligibility_reasons": [
            "UNRESOLVED_CONFLICT"
          ],
          "evidence_issues": [],
          "cross_project_context": false,
          "score": 3,
          "matched_fields": [
            "aliases_vi"
          ],
          "matched_terms": [
            "giới hạn yêu cầu"
          ],
          "expansion_terms": [
            "Lyra API",
            "request budget"
          ],
          "citations": [
            {
              "source_id": "SRC-20261018-801",
              "source_path": "sources/raw/SRC-20261018-801.md",
              "integrity_status": "MATCH",
              "source_version": 1,
              "verification_status": "UNVERIFIED",
              "superseded_by": null,
              "original_uri_status": "UNKNOWN",
              "source_uri": null,
              "source_pointer": "section Evidence"
            },
            {
              "source_id": "SRC-20261018-802",
              "source_path": "sources/raw/SRC-20261018-802.md",
              "integrity_status": "MATCH",
              "source_version": 1,
              "verification_status": "UNVERIFIED",
              "superseded_by": null,
              "original_uri_status": "UNKNOWN",
              "source_uri": null,
              "source_pointer": "section Evidence"
            }
          ]
        }
      ],
      "status": "DISPUTED",
      "message": "Tài liệu có tranh chấp chưa giải quyết; giữ cả hai nguồn và yêu cầu rà soát."
    },
    "same_result": true,
    "read_only": true
  },
  "failures": [],
  "human_approvals_created": 0,
  "human_fact_validation": "NOT RUN",
  "token_usage": null,
  "api_cost": null,
  "human_review_time_seconds": null,
  "preservation_baseline": {
    "files": {
      "sources/raw/SRC-20261018-801.md": "720ab214bdad9adaa235c8bcebaab8b0f942daf1f0892493080a884a28d1580c",
      "sources/raw/SRC-20261018-803.md": "aa86692d36c5d70d308b4700e2c827b8f8485d33586f4b97a6d70151b3372c18",
      "wiki/cache-policy.md": "58ecc5c4a32fccd3b7a71238e85675a52e4d9ec893537a8566a650370fa18909",
      "sources/raw/SRC-20261018-802.md": "f881fa364b090738205d5f52033ee41584eeba32850b851dec6b4d84638c4f60"
    },
    "prefixes": {
      "sources/manifest.csv": {
        "bytes": 521,
        "sha256": "509306d146b87d9bf513dcb93e96c3d81c8e8caeaabbc20738115bbedbb3ac7a"
      },
      "sources/provenance.jsonl": {
        "bytes": 986,
        "sha256": "078a697a9469314a04215e1679297d5f2406485deaac72cdc0862d40858af42f"
      },
      "wiki/index.md": {
        "bytes": 112,
        "sha256": "abe2b93405e0a1f92f9b36fb8a2b40bda247854861eeeb903c9c54e77a1dddc2"
      },
      "wiki/log.md": {
        "bytes": 152,
        "sha256": "40834fe84f0bc57cd358d2016a42ef4559543c6e137532eae4af2e0d6d0dcebd"
      }
    }
  },
  "preservation_results": {
    "sources/raw/SRC-20261018-801.md": true,
    "sources/raw/SRC-20261018-803.md": true,
    "wiki/cache-policy.md": true,
    "sources/raw/SRC-20261018-802.md": true,
    "sources/manifest.csv:old_prefix": true,
    "sources/provenance.jsonl:old_prefix": true,
    "wiki/index.md:old_prefix": true,
    "wiki/log.md:old_prefix": true
  },
  "final_snapshot_hashes": {
    "reports/validation.md": "94cf28ffa7c8a4cb130af51b0e219da0c6a28ac2546adc892bc492d51b5c796e",
    "sources/manifest.csv": "538bc78e5e1cda40a6c21af754a16c2c06595392b23b440c602f50df6657b78e",
    "sources/provenance.jsonl": "7e9b7614c3f4b5c4d033fe88b719ef7482a920ce652db254bfc753ecc6365668",
    "wiki/cache-policy.md": "58ecc5c4a32fccd3b7a71238e85675a52e4d9ec893537a8566a650370fa18909",
    "wiki/index.md": "abe2b93405e0a1f92f9b36fb8a2b40bda247854861eeeb903c9c54e77a1dddc2",
    "wiki/log.md": "4a764f64de57460ebec662c91640870d86195ae7e016818bf4345d71442e97a3",
    "wiki/request-budget.md": "3a6a9d66a51179b377b48f662d9ef7ee88804b03776f8d1ad775c72827c2811c",
    "sources/raw/SRC-20261018-801.md": "720ab214bdad9adaa235c8bcebaab8b0f942daf1f0892493080a884a28d1580c",
    "sources/raw/SRC-20261018-802.md": "f881fa364b090738205d5f52033ee41584eeba32850b851dec6b4d84638c4f60",
    "sources/raw/SRC-20261018-803.md": "aa86692d36c5d70d308b4700e2c827b8f8485d33586f4b97a6d70151b3372c18"
  }
}

## Accumulating source batches

- 10 sources: fixed panel ['K01', 'K02', 'K03', 'K04']; actual batch machine time 34.46264220000057 seconds; A/B source Recall@5 1.0/1.0.
- 20 sources: fixed panel ['K01', 'K02', 'K03', 'K04']; actual batch machine time 38.18853299999955 seconds; A/B source Recall@5 1.0/1.0.
- 30 sources: fixed panel ['K01', 'K02', 'K03', 'K04']; actual batch machine time 41.48731939999925 seconds; A/B source Recall@5 1.0/1.0.

Repeated research steps, answer quality, human maintenance/review burden and practical compounding value remain NOT MEASURED. Fixed-panel retrieval can stay flat as files accumulate; it is not evidence of increasing practical value.

## Limits and next action

- NOT MEASURED: Real curated/human-confirmed gold
- NOT MEASURED: Same-model independent AI A/B trials
- NOT MEASURED: Semantic/factual answer correctness
- NOT MEASURED: Human review/correction/maintenance time
- NOT MEASURED: AI context/token/API cost
- NOT MEASURED: Net productivity/compounding practical value
- Use the reviewed real-pilot protocol only in a separately authorized task; do not infer V2 readiness from synthetic PASS.

Gold, cases, actual per-arm outputs, seeds, timings and file hashes are retained in companion JSON. No real intake, network, other project repository or V2 was used.

See [evaluation protocol](../FEASIBILITY_EVALUATION.md) and [dataset contract](../tests/fixtures/feasibility/README.md).
