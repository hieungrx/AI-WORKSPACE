#!/usr/bin/env python3
"""Run Phase 4 synthetic E2E, independent retrieval benchmark and all regressions."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).absolute().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.check_workspace import check_workspace
from scripts.safe_operations import save_reports
from scripts.validate_source_integrity import RecordedResult
from scripts.workspace_security import redact


def evaluate():
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    module = sys.modules.get("test_workflow_reliability")
    if module:
        module.BENCHMARK_OBSERVATION.clear()
        module.WORKFLOW_OBSERVATIONS.clear()
        module.LINT_OBSERVATIONS.clear()
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output, resultclass=RecordedResult, verbosity=0).run(suite)
    module = sys.modules.get("test_workflow_reliability")
    benchmark = dict(getattr(module, "BENCHMARK_OBSERVATION", {}))
    workflow = list(getattr(module, "WORKFLOW_OBSERVATIONS", []))
    lint = list(getattr(module, "LINT_OBSERVATIONS", []))
    issues = check_workspace(ROOT, integrity=True, security=True)
    passed = (result.wasSuccessful() and not result.skipped and benchmark.get("queries", 0) >= 40
              and not benchmark.get("unexpected_failures", ["not run"])
              and benchmark.get("query_and_lint_read_only") is True
              and not any(issue.startswith("ERROR ") for issue in issues))
    return redact({
        "phase": "AI-WORKSPACE V1 Phase 4 only", "discovery_baseline": "6097642",
        "observed_at_utc": datetime.now(timezone.utc).isoformat(), "synthetic_only": True,
        "workflow_verdict": "PASS" if passed else "FAIL", "verdict": "CONDITIONAL" if passed else "FAIL",
        "verdict_reason": "The guarded workflow can pass while lexical paraphrase recall, semantic review, full agent answering and host containment remain limited or unmeasured.",
        "unit_tests": {"run": result.testsRun, "passed": sum(row["status"] == "PASS" for row in result.rows),
                       "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
                       "observed_output": output.getvalue(), "results": result.rows},
        "workspace_issues": issues, "benchmark": benchmark, "workflow_observations": workflow,
        "lint_fault_observations": lint,
        "compatibility": {"prior_tests_run": sum(not row["test"].startswith("test_workflow_reliability.") for row in result.rows),
                          "prior_tests_passed": sum(not row["test"].startswith("test_workflow_reliability.")
                                                    and row["status"] == "PASS" for row in result.rows),
                          "schema": "Optional page_id / decision_key; Markdown bullets retained; no CSV changes or bulk migration.",
                          "stricter_contract": "Bare source IDs, YAML metadata, conflicting explicit decision slots and unsafe synthesis now fail closed; old valid fixtures remain compatible."},
        "not_measured": ["LLM answer correctness and actual model abstention", "Cross-language semantic search and automatic translation (not implemented)",
                         "Factual truth, semantic contradiction discovery and source relevance", "Obsidian visual rendering", "Physical power-loss recovery and complete host/agent containment"],
        "recommended_fixes": ["Review curated aliases for the observed unlisted paraphrases before any real intake.",
                              "Retain independent relevance gold and add unseen natural questions when expanding evaluation.",
                              "Review unkeyed or textual contradictions manually; deterministic collisions cannot choose a winning decision.",
                              "Constrain broader agent tools separately before treating workflow API controls as host security."],
    })


def markdown(report):
    unit, benchmark = report["unit_tests"], report["benchmark"]
    metrics = benchmark.get("metrics", {})
    lines = ["# Phase 4 — Knowledge Workflow Reliability", "",
             f"**Verdict: {report['verdict']}**. Guarded workflow contract: **{report['workflow_verdict']}**.",
             report["verdict_reason"], "",
             f"Observed at UTC: {report['observed_at_utc']}. Baseline: 6097642, branch workspace/initialize.",
             f"Executed: {unit['run']} tests, {unit['passed']} PASS, {unit['failures']} failures, {unit['errors']} errors, {unit['skipped']} skips.",
             "Only first-party repository files and TEST_ONLY synthetic data were used; no real knowledge or secrets were imported.", "",
             "## Audit and implemented fixes", "",
             "Read: AGENTS/README/SCHEMA/PROFILE, security/governance/source reports and contracts, relevant prompts, index/log and actual Python implementation/tests.",
             "- Initial console reproduction on the pre-fix implementation ran 3 new tests: 2 failures and 1 error. A verified page could be reset by Ingest, identical replay raised CONCURRENT_CHANGE, and Lint accepted a bare source ID without a pointer.",
             "- Normal wiki synthesis now protects non-draft knowledge, scope, lifecycle history, prior source pointers and conflicts. Review/transition or a new draft is required for protected updates.",
             "- Exact retries and fresh plans with unchanged pages/index return UNCHANGED without adding duplicate history. Stale changed targets remain conflicts.",
             "- Ingest checks pointer syntax, index retention and appended log before writing; lower-level wiki transactions enforce protected-state updates under ownership.",
             "- Lint adds optional page identity uniqueness, unsupported YAML detection, duplicate index targets, unreviewed status warnings and explicit same-scope current decision slot collisions. Query fails closed on detected identity/slot collisions.",
             "See [workflow specification and reproduction](../WORKFLOW_RELIABILITY.md). No framework, database or new dependency was added.", "",
             "## Actual benchmark metrics", "",
             f"Pairs: {benchmark.get('pairs', 'NOT RUN')}; actual queries: {benchmark.get('queries', 'NOT RUN')}. Query/Lint read-only: {benchmark.get('query_and_lint_read_only', 'NOT RUN')}.",
             "Corpus, hand-authored relevance/expected scopes/states/citations/abstentions and fixture hashes are in the companion JSON and tests/fixtures/workflow."]
    for name, value in metrics.items():
        lines.append("- " + name + ": " + json.dumps(value, ensure_ascii=False))
    counts = Counter(row["actual"]["status"] for row in benchmark.get("results", []))
    lines += ["", "Observed query outcomes: " + json.dumps(dict(sorted(counts.items())), ensure_ascii=False) + ".",
              "Recall includes the negative relevance controls Q25/Q29; a correct NOT_FOUND lexical signal can still be a retrieval miss. Blocked evidence candidates count as retrieved documents, never usable answers.",
              "Citation validity checks identity, local path, recorded SHA-256 and the actual synthetic Evidence heading. It does not verify claim meaning.", "",
              "## Paired retrieval evidence", ""]
    for row in benchmark.get("results", []):
        paths = [doc["path"] for doc in row["actual"]["matches"] + row["actual"]["blocked"]]
        lines.append(f"- {row['pair']} {row['language']}: {row['actual']['status']}; contract {row['contract_result']}; Recall@5 {row['recall_at_5']}; query {row['query']}; paths " + json.dumps(paths, ensure_ascii=False))
    lines += ["", "## Recovery and failure evidence", ""]
    for row in report["workflow_observations"]:
        lines.append("- " + row["scenario"] + ": " + json.dumps(row, ensure_ascii=False, sort_keys=True))
    lines += ["", "Failures were injected only into disposable fixture operations. Actual hashes, blocked codes, authorized recovery and successful retry are recorded; source admission remains intact after failed synthesis.",
              "", "## Lint evidence and semantic boundary", ""]
    for row in report["lint_fault_observations"]:
        lines.append("- Expected " + row["expected_code"] + ": " + json.dumps(row["observed_issues"], ensure_ascii=False))
    lines += ["", "Deterministic checks do not establish factual truth. A shared decision_key identifies an exclusive slot collision; textual contradictions without this declaration require human/LLM review. No semantic review or full answer-generation score is claimed.",
              "", "## Live workspace and compatibility", ""]
    lines.extend("- " + issue for issue in report["workspace_issues"])
    lines += [json.dumps(report["compatibility"], ensure_ascii=False),
              "Existing raw, registry, decision history and original wiki pages were not migrated or overwritten. Existing Obsidian user edits are excluded from the checkpoint.",
              "", "## Known limitations and recommended fixes", ""]
    lines.extend("- " + item for item in report["not_measured"])
    lines.extend("- " + item for item in report["recommended_fixes"])
    lines += ["", "## Reproduce", "", "~~~text", "python -B scripts/validate_workflows.py",
              "python -B scripts/check_workspace.py --integrity --security", "~~~", "",
              "Use a new --output reports/<unique-name>.json to save redacted evidence without replacing past reports. No Phase 5, real intake, external access, push, merge or deployment was performed."]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="New reports/*.json plus companion Markdown; never overwrite.")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = evaluate()
    if args.output:
        save_reports(ROOT, report, args.output, markdown)
    print(json.dumps({"verdict": report["verdict"], "workflow_verdict": report["workflow_verdict"],
                      "tests": {key: value for key, value in report["unit_tests"].items() if key not in {"results", "observed_output"}},
                      "benchmark_queries": report["benchmark"].get("queries", "NOT RUN"),
                      "metrics": report["benchmark"].get("metrics", {}), "workspace_issues": report["workspace_issues"]},
                     ensure_ascii=False, indent=2))
    if report["workflow_verdict"] != "PASS":
        print(report["unit_tests"]["observed_output"])
    return 0 if report["workflow_verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
