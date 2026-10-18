# V1.1 independent synthetic agent readback

One fork_turns=none agent, given only fixture/query/scope and operating policies, reported DISPUTED, both raw claims, unresolved conflict and current=false. Root reran the same public Query and independently compared saved knowledge hashes. No human score, model A/B advantage or production continuity is claimed.

{
  "phase": "V1.1 independent synthetic agent readback",
  "observed_at_utc": "2026-10-18T11:46:18.263059+00:00",
  "preparation": {
    "passed": true,
    "synthetic_only": true,
    "workspace_path": "E:\\AI-Workspace-Starter-v1\\AI-Workspace-Starter\\tests\\fixture-feasibility-fresh-agent-cmtz3hql\\evolution\\workspace",
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
          "operation_id": "80330a88220742a48d725149495b3a38",
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
          "operation_id": "da82262f1b1b486a83752f70eb7a6843",
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
          "operation_id": "84359bd3b5ba43afa24ef2d294b61aa5",
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
      "unrelated_source_admission": 1.507665299999644,
      "unrelated_draft_ingest": 1.4692340999972657,
      "source_a_admission": 1.4890258999985235,
      "initial_draft_ingest": 1.3210720999995829,
      "initial_unverified_transition": 0.8200721999965026,
      "initial_query": 0.1158878000023833,
      "return_to_draft": 0.6415271000005305,
      "source_b_admission": 1.3830519000002823,
      "failed_update_and_automatic_rollback": 0.7281270999992557,
      "retry_conflicting_draft_update": 1.5795700999988185,
      "updated_unverified_transition": 0.5066079999996873,
      "disputed_transition": 0.5312869999979739,
      "disputed_query": 0.0619842999985849,
      "strict_lint": 0.11019070000111242,
      "source_integrity_audit": 0.02551840000160155,
      "fresh_python_query": 0.4936457000003429
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
  },
  "agent_observation": {
    "agent_task": "/root/feasibility_fresh_reader",
    "history_mode": "fork_turns=none",
    "answer_key_provided": false,
    "receipt_or_reports_authorized": false,
    "human_review": false,
    "model_id_version_settings": "NOT OBSERVED",
    "reported_command": [
      "D:\\laragon\\bin\\python\\python-3.13\\python.exe",
      "-B",
      "E:\\AI-Workspace-Starter-v1\\AI-Workspace-Starter\\scripts\\query_workspace.py",
      "--root",
      "E:\\AI-Workspace-Starter-v1\\AI-Workspace-Starter\\tests\\fixture-feasibility-fresh-agent-cmtz3hql\\evolution\\workspace",
      "--scope",
      "synthetic-workbench",
      "--query",
      "giới hạn yêu cầu"
    ],
    "reported_exit_code": 0,
    "reported_status": "DISPUTED",
    "reported_source_claims": {
      "SRC-20261018-801": "60 requests/minute",
      "SRC-20261018-802": "45 requests/minute"
    },
    "reported_current_truth": false,
    "reported_unresolved_conflict": true,
    "answer_summary": "The two raw statements disagree; no winner or currently applicable limit is established. Human review of scope/version/effective dates is required. Source hashes show byte integrity, not truth.",
    "scope": "Single synthetic readback observation; not the five gold continuity cases or a real A/B pilot."
  },
  "corroborating_root_query": {
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
  "corroborating_exit_code": 0,
  "corroborating_stderr": "",
  "readback_preserved_all_workspace_bytes": true,
  "prepared_knowledge_hashes_preserved": true,
  "raw_evidence_snapshots": {
    "SRC-20261018-801": {
      "trust": "UNTRUSTED_DATA",
      "origin": "sources/raw/SRC-20261018-801.md",
      "text": "# TEST_ONLY SRC-20261018-801\n\n## Evidence\nTEST_ONLY observation A: Lyra API permits 60 requests per minute.\n",
      "content_hash": "sha256:720ab214bdad9adaa235c8bcebaab8b0f942daf1f0892493080a884a28d1580c"
    },
    "SRC-20261018-802": {
      "trust": "UNTRUSTED_DATA",
      "origin": "sources/raw/SRC-20261018-802.md",
      "text": "# TEST_ONLY SRC-20261018-802\n\n## Evidence\nTEST_ONLY observation B: Lyra API permits 45 requests per minute.\n",
      "content_hash": "sha256:f881fa364b090738205d5f52033ee41584eeba32850b851dec6b4d84638c4f60"
    }
  },
  "agent_answer_semantic_human_score": "NOT MEASURED",
  "agent_AI_tokens_cost_elapsed": "NOT OBSERVED",
  "synthetic_continuity_observed": true,
  "real_world_feasibility": "NOT YET MEASURED",
  "ephemeral_fixture_note": "The owned workspace is removed after archiving these synthetic bytes/hashes. Paths in tool output describe the executed fixture, not durable source locations."
}
