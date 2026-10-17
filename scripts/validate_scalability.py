#!/usr/bin/env python3
"""Combine completed Phase 5 measurements with fresh V1 safety regressions."""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).absolute().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.check_workspace import check_workspace, local_path
from scripts.safe_operations import save_reports
from scripts.source_integrity import read_registry
from scripts.validate_source_integrity import RecordedResult

IMPLEMENTATION_FILES = {"query_workspace.py", "source_integrity.py", "knowledge_governance.py", "check_workspace.py", "safe_operations.py"}
REQUIRED_OPERATIONS = {"source_lookup", "query_en", "query_vi", "validation", "incremental_update"}


def complete_load_probes(measured):
    datasets = measured["datasets"]
    return (len(datasets) == 3 and {data["setup"]["documents"] for data in datasets} == {100, 1000, 10000}
            and all({row["operation"] for row in data["operations"]} == REQUIRED_OPERATIONS
                    and all(row["status"] == "MEASURED" and row.get("correct") is True
                            for row in data["operations"] + [data["quality"]]) for data in datasets))


def implementation_mismatches(measured):
    recorded = measured.get("implementation_sha256")
    if not isinstance(recorded, dict) or set(recorded) != IMPLEMENTATION_FILES:
        raise ValueError("INVALID_IMPLEMENTATION_MANIFEST")
    return [name for name in sorted(IMPLEMENTATION_FILES)
            if hashlib.sha256(local_path(ROOT, ROOT, "scripts/" + name).read_bytes()).hexdigest() != recorded[name]]


def read_measurements(relative):
    path = local_path(ROOT, ROOT, str(relative))
    if not path.is_relative_to(ROOT / "reports") or path.suffix != ".json":
        raise ValueError("BENCHMARK_REPORT_REQUIRED")
    report = json.loads(path.read_text(encoding="utf-8"))
    if report.get("phase") != "V1 Phase 5" or report.get("synthetic_only") is not True:
        raise ValueError("PHASE5_SYNTHETIC_REPORT_REQUIRED")
    return report


def evaluate(benchmark_path, baseline_path=None):
    measured = read_measurements(benchmark_path)
    baseline = read_measurements(baseline_path) if baseline_path else None
    stale = implementation_mismatches(measured)
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output, resultclass=RecordedResult, verbosity=0).run(suite)
    checks = check_workspace(ROOT, integrity=True, security=True)
    failed = not result.wasSuccessful() or bool(result.skipped) or bool(stale) or any(issue.startswith("ERROR ") for issue in checks)
    failed |= any(row["status"] == "FAIL" for data in measured["datasets"] for row in data["operations"] + [data["quality"]])
    sizes = {data["setup"]["documents"] for data in measured["datasets"]}
    complete = complete_load_probes(measured)
    correctness = "FAIL" if failed else "PASS" if complete else "CONDITIONAL"
    rows = []
    for data in measured["datasets"]:
        old = next((item for item in baseline["datasets"] if item["setup"]["documents"] == data["setup"]["documents"]), None) if baseline else None
        rows.append({"documents": data["setup"]["documents"], "setup": data["setup"],
                     "summary": data["summary"], "baseline_summary": old["summary"] if old else "NOT RUN",
                     "quality": data["quality"], "memory": [row.get("memory", {}) for row in data["operations"] + [data["quality"]]],
                     "manifest_opens": {row["operation"]: row.get("io_calls", {}).get("manifest_open_calls", "NOT MEASURED") for row in data["operations"]}})
    return {"phase": "V1 Phase 5 assessment", "discovery_baseline": "55e6e1f",
            "observed_at_utc": datetime.now(timezone.utc).isoformat(), "correctness_verdict": correctness,
            "verdict": "FAIL" if failed else "CONDITIONAL",
            "verdict_reason": "Correctness is separate from interactive readiness: measured linear scans remain slow at larger sizes, timing samples are small, and production/LLM/host limits remain untested.",
            "benchmark_path": str(benchmark_path).replace("\\", "/"), "baseline_path": str(baseline_path).replace("\\", "/") if baseline else None,
            "environment": measured["environment"], "method": measured["method"], "sizes_tested": sorted(sizes),
            "measurement_implementation_mismatch": stale, "datasets": rows,
            "unit_tests": {"run": result.testsRun, "passed": sum(row["status"] == "PASS" for row in result.rows),
                           "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
                           "observed_output": output.getvalue(), "results": result.rows},
            "previous_regressions": {"run": sum(not row["test"].startswith("test_scalability.") for row in result.rows),
                                     "passed": sum(not row["test"].startswith("test_scalability.") and row["status"] == "PASS" for row in result.rows)},
            "workspace_checks": checks, "live_registered_sources": len(read_registry(ROOT)),
            "cost": {"LLM_tokens": "NOT MEASURED", "API_charges": "NOT MEASURED", "monetary_CPU_storage_cost": "NOT MEASURED",
                     "note": "No LLM API is invoked by this benchmark. This is not a bill estimate for the chat or future pilot."},
            "not_measured": ["P95, throughput or concurrent capacity", "Cold OS-cache behavior", "Physical disk allocation and wear",
                             "Real production corpus and human ingestion/approval throughput", "Full-text incremental-index throughput (not implemented)",
                             "Semantic retrieval/reranking and LLM answer correctness", "Obsidian UI performance", "Host containment and physical power-loss recovery"],
            "pilot_recommendation": "Start with a separately authorized 25-100 page knowledge pilot; 2s interaction and 30s foreground maintenance budgets are PROVISIONAL. Larger measured sizes require accepting their observed delays or a separate index experiment; do not claim untested scale.",
            "specification": "SCALABILITY.md"}


def markdown(report):
    unit = report["unit_tests"]
    lines = ["# Phase 5 — Scalability Assessment", "", f"**Overall: {report['verdict']}**. Tested correctness: **{report['correctness_verdict']}**.",
             report["verdict_reason"], "", f"Observed UTC: {report['observed_at_utc']}; baseline 55e6e1f, branch workspace/initialize.",
             f"Fresh regression run: {unit['run']} tests; {unit['passed']} PASS; {unit['failures']} failures, {unit['errors']} errors, {unit['skipped']} skips.",
             "Sources: first-party repository implementation/contracts and synthetic load fixtures only. No real source/secret or outside repository was opened.",
             "Read: AGENTS/README/SCHEMA/PROFILE, source/governance/security/workflow reports, prompts, wiki indexes/history, manifest, search/validator/transaction code and tests.",
             "Changed: operation-local registry reuse in governance/Query, Query source-audit scan selection, reproducible load/validation scripts and tests, scalability guide, README/navigation and append-only maintenance history.",
             "", "## Architecture, bottlenecks and migration", "",
             "See [architecture review, incremental behavior, Level 1-4 search interface/migration plan, provisional triggers and V1.1 pilot recommendations](../SCALABILITY.md).",
             "Baseline measurements and a separate cProfile identify repeated registry reads and filesystem/path scans. Registry reuse is local to one operation; raw SHA-256, lineage, scope, lifecycle approval, security and recovery checks remain active.",
             "No production index, database, QMD, embedding model, worker service or V2 was added. Source/provenance schema and default full-audit relationships remain compatible.", "",
             "## Measurement provenance", "", json.dumps(report["environment"], ensure_ascii=False), "", json.dumps(report["method"], ensure_ascii=False),
             "", f"[Measured trials and fixture hashes](../{report['benchmark_path']})."]
    if report["baseline_path"]:
        lines.append(f"[Pre-optimization baseline](../{report['baseline_path']}).")
    for data in report["datasets"]:
        lines += ["", f"## {data['documents']} wiki documents + {data['documents']} raw snapshots", "",
                  "Fixture/navigation/filesystem: " + json.dumps(data["setup"], ensure_ascii=False), ""]
        for name, value in data["summary"].items():
            old = data["baseline_summary"].get(name, "NOT RUN") if isinstance(data["baseline_summary"], dict) else "NOT RUN"
            lines.append("- " + name + ": " + json.dumps(value) + "; baseline: " + json.dumps(old))
        lines += ["- Manifest opens: " + json.dumps(data["manifest_opens"]),
                  "- Measured process memory: " + json.dumps(data["memory"]),
                  "- Quality safeguards: " + json.dumps(data["quality"], ensure_ascii=False)]
    lines += ["", "## Correctness and compatibility", "", json.dumps(report["previous_regressions"]),
              "", "Measurement implementation mismatches: " + json.dumps(report["measurement_implementation_mismatch"]),
              "", "Every timed Query validates expected document/source/pointer/scope. Incremental probes compare all fixture hashes, observe a new keyword without rebuild and verify UNCHANGED retries. Separate per-size probes check wrong scope, missing documents, source tamper with unchanged size/mtime, injection, verified overwrite, path traversal, interrupted reads and exact recovery.",
              "Default full Lint/source admission keep reverse relationships; only Query's redundant scan is omitted. Invalid registry/manifest edits are rediscovered on the next operation. Existing legacy readers and source/approval hashes remain regression-tested.",
              "", "## Live workspace checks", ""]
    lines.extend("- " + issue for issue in report["workspace_checks"])
    lines += [f"Live registered sources: {report['live_registered_sources']}. Synthetic corpora stay in owned temporary test directories.",
              "", "## Cost and untested limits", "", json.dumps(report["cost"], ensure_ascii=False)]
    lines.extend("- NOT MEASURED: " + item for item in report["not_measured"])
    lines += ["", "No baseline 10,000-document timing was run: the smaller-size profile already justified eliminating redundant scans before that larger run. No baseline number is extrapolated as a measurement.",
              "", "Single observations are not latency distributions or production limits. File/corpus counts and logical bytes do not measure allocated disk overhead. Source lookup does not by itself validate factual content.",
              "The worker timeout includes imports, snapshots, retries and post-checks; incomplete workers have no completed verified latency. English/Vietnamese timing differences cannot be attributed to language because OS cache/I/O and order are uncontrolled.",
              "", "## V1.1 pilot recommendation", "", report["pilot_recommendation"],
              "", "Proposed thresholds require human agreement. Actual source intake, retrieval backend choice and architecture approvals remain separate user decisions; this task authorizes none of them.",
              "", "## Fresh automated test results", ""]
    lines.extend("- " + row["status"] + ": " + row["test"] for row in unit["results"])
    lines += ["", "No deployment, push, merge or V2 implementation was performed."]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", type=Path, required=True)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    report = evaluate(args.benchmark, args.baseline)
    if args.output:
        save_reports(ROOT, report, args.output, markdown)
    print(json.dumps({"verdict": report["verdict"], "correctness_verdict": report["correctness_verdict"],
                      "sizes_tested": report["sizes_tested"],
                      "tests": {key: value for key, value in report["unit_tests"].items() if key not in {"results", "observed_output"}},
                      "workspace_checks": report["workspace_checks"]}, ensure_ascii=False, indent=2))
    if report["correctness_verdict"] == "FAIL":
        print(report["unit_tests"]["observed_output"])
    return 1 if report["correctness_verdict"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
