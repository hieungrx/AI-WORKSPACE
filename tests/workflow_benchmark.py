"""Reference adapter/metrics for the independent TEST_ONLY corpus and query contracts."""
import hashlib
import json

from scripts import check_workspace as lint
from scripts import query_workspace as query
from scripts import source_integrity as integrity
from workflow_support import FIXTURES, build_corpus


def fraction(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator,
            "value": numerator / denominator if denominator else "NOT MEASURED"}


def run_benchmark(workspace):
    setup = build_corpus(workspace)
    contract = json.loads((FIXTURES / "queries.json").read_text(encoding="utf-8"))
    sources = integrity.audit_sources(workspace.root)["sources"]
    before = workspace.snapshot(include_recovery=True)
    rows, citation_checks = [], []
    for pair in contract["pairs"]:
        for language in ("vi", "en"):
            expected = contract["expectations"][pair.get("expect_" + language, pair["expect"]) ]
            actual = query.search(workspace.root, pair[language], pair["scope"],
                                  cross_refs=pair.get("cross_refs", ()), include_history=pair.get("include_history", False))
            documents = actual["matches"] + actual["blocked"]
            ranked = sorted(documents, key=lambda doc: (-doc["score"], doc["path"]))[:5]
            relevant = set(pair["relevant"])
            retrieved = {doc["path"] for doc in ranked}
            mismatches = []
            if actual["status"] != expected["status"]:
                mismatches.append("status")
            if {doc["path"] for doc in documents} != {doc["path"] for doc in expected["documents"]}:
                mismatches.append("documents")
            allowed = {doc["path"]: doc for doc in expected["documents"]}
            for doc in documents:
                gold = allowed.get(doc["path"], {})
                for field, gold_field in (("scope", "scope"), ("knowledge_status", "status")):
                    if doc[field] != gold.get(gold_field):
                        mismatches.append(field)
                if "decision_authority" in gold and doc["decision_authority"] != gold["decision_authority"]:
                    mismatches.append("decision_authority")
                if doc["cross_project_context"] != gold.get("cross_project_context", False):
                    mismatches.append("cross_project_context")
                if "usable_as_current_truth" in gold and doc["usable_as_current_truth"] != gold["usable_as_current_truth"]:
                    mismatches.append("current_truth_authority")
                if (doc in actual["blocked"]) != gold.get("blocked", False):
                    mismatches.append("evidence_gate")
                if {cite.get("source_id") for cite in doc["citations"]} != set(gold.get("source_ids", [])):
                    mismatches.append("source_ids")
                if doc["knowledge_status"] in {"draft", "unverified", "disputed", "superseded"} and doc["usable_as_current_truth"]:
                    mismatches.append("current_truth_authority")
                for cite in doc["citations"]:
                    source = sources.get(cite.get("source_id"), {})
                    raw_path = source.get("local_path")
                    raw = (workspace.root / raw_path).read_bytes() if raw_path else b""
                    valid = bool(raw_path and cite.get("source_path") == raw_path
                                 and source["integrity_status"] == cite.get("integrity_status") == "MATCH"
                                 and cite.get("source_pointer") == contract["citation_pointer"]
                                 and b"\n## Evidence\n" in raw
                                 and source["content_hash"] == "sha256:" + hashlib.sha256(raw).hexdigest())
                    citation_checks.append({"pair": pair["id"], "language": language, "path": doc["path"],
                                            "source_id": cite.get("source_id"), "valid": valid})
                    if not valid:
                        mismatches.append("citation")
            if actual["query"] != pair[language]:
                mismatches.append("query_mutation")
            preserve = pair.get("preserve_both", []) + (pair.get("preserve_en", []) if language == "en" else [])
            if any(term not in actual["query"] for term in preserve):
                mismatches.append("terminology")
            if pair["id"] in {"Q25", "Q26", "Q29", "Q30"} and not documents and actual["expanded_terms"]:
                mismatches.append("unapproved_expansion")
            leakage = [doc["path"] for doc in documents if doc["scope"] != pair["scope"]
                       and not (doc["path"] in pair.get("cross_refs", []) and doc.get("cross_project_context"))]
            if leakage:
                mismatches.append("scope_leakage")
            rows.append({"pair": pair["id"], "language": language, "category": pair["category"],
                         "query": pair[language], "scope": pair["scope"], "expected": expected,
                         "actual": actual, "relevant_paths": sorted(relevant),
                         "recall_at_5": len(relevant & retrieved) / len(relevant) if relevant else "NOT MEASURED",
                         "scope_leakage": leakage, "expected_abstention_signal": expected["abstain"],
                         "contract_result": "FAIL" if mismatches else "PASS", "mismatches": sorted(set(mismatches))})
    issues = lint.check_workspace(workspace.root, integrity=True, security=True)
    error_pages = {issue.split()[2].rstrip(":") for issue in issues if issue.startswith("ERROR ")}
    corpus_paths = {page["path"] for page in json.loads((FIXTURES / "corpus.json").read_text(encoding="utf-8"))["pages"]}
    recalls = [row["recall_at_5"] for row in rows if row["recall_at_5"] != "NOT MEASURED"]
    metrics = {
        "retrieval_recall_at_5": {"value": sum(recalls) / len(recalls) if recalls else "NOT MEASURED",
                                  "queries_with_relevance_gold": len(recalls),
                                  "definition": "Macro document Recall@5 over actual highest-tier candidates (matches + blocked), ordered by score/path; excludes zero-relevance cases. Retrieval does not imply answerability."},
        "citation_validity": fraction(sum(row["valid"] for row in citation_checks), len(citation_checks)),
        "cross_project_leakage": fraction(sum(bool(row["scope_leakage"]) for row in rows), len(rows)),
        "duplicate_ingestion_rate": fraction(sum(row["retry"] != "UNCHANGED" or not row["retry_preserved_bytes"] for row in setup["synthesis"]), len(setup["synthesis"])),
        "duplicate_registration_rate": fraction(sum(row["retry"] != "DUPLICATE" for row in setup["admissions"]), len(setup["admissions"])),
        "schema_validation_pass_rate": fraction(len(corpus_paths - error_pages) if not error_pages - corpus_paths else 0, len(corpus_paths)),
        "workflow_failure_rate": fraction(sum(row["contract_result"] != "PASS" for row in rows)
                                           + sum(row["first"] != "COMMITTED" for row in setup["synthesis"])
                                           + sum(row["first"] != "REGISTERED" for row in setup["admissions"]),
                                           len(rows) + len(setup["synthesis"]) + len(setup["admissions"])),
        "answer_generation_accuracy": "NOT MEASURED",
        "cross_language_semantic_search": "NOT MEASURED (not implemented)",
        "automatic_translation_accuracy": "NOT MEASURED (not implemented)",
        "semantic_factual_verification": "NOT MEASURED",
    }
    for language in ("vi", "en"):
        language_recalls = [row["recall_at_5"] for row in rows if row["language"] == language and row["recall_at_5"] != "NOT MEASURED"]
        metrics["retrieval_recall_at_5"][language] = {
            "value": sum(language_recalls) / len(language_recalls) if language_recalls else "NOT MEASURED",
            "queries_with_relevance_gold": len(language_recalls)}
    return {"dataset_id": contract["dataset_id"], "pairs": len(contract["pairs"]), "queries": len(rows),
            "fixture_sha256": {name: hashlib.sha256((FIXTURES / name).read_bytes()).hexdigest()
                               for name in ("corpus.json", "queries.json")},
            "setup": setup, "results": rows, "citation_checks": citation_checks, "metrics": metrics,
            "lint_issues": issues, "query_and_lint_read_only": workspace.snapshot(include_recovery=True) == before,
            "unexpected_failures": [row for row in rows if row["contract_result"] == "FAIL"]}
