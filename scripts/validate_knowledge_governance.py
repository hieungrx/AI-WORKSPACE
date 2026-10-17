#!/usr/bin/env python3
"""Run Phase 2 synthetic workflows and existing regressions; save only new reports."""
import argparse
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).absolute().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.check_workspace import check_workspace, local_path
from scripts.knowledge_governance import audit_governance
from scripts.validate_source_integrity import RecordedResult


def evaluate():
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(stream=stream, resultclass=RecordedResult, verbosity=0).run(suite)
    checks = check_workspace(ROOT, integrity=True)
    errors = [item for item in checks if item.startswith("ERROR ")]
    requested = []
    for number in range(1, 11):
        rows = [row for row in result.rows if row["test"].startswith("test_knowledge_governance.")
                and row["test"].split(".")[-1].startswith(f"test_{number:02d}_")]
        requested.append({"scenario": number, "status": "PASS" if len(rows) == 1 and rows[0]["status"] == "PASS" else "FAIL",
                          "observed_tests": rows})
    accepted = all(row["status"] == "PASS" for row in requested)
    verdict = ("FAIL" if errors or not result.wasSuccessful() or not accepted else
               "CONDITIONAL" if any(row["status"] != "PASS" for row in result.rows) else "PASS")
    old = [row for row in result.rows if not row["test"].startswith("test_knowledge_governance.")]
    return {
        "phase": "AI-WORKSPACE V1 Phase 2 only", "verdict": verdict,
        "verdict_scope": "Observed synthetic lifecycle/authority/isolation workflows and current scaffold; not human authentication or factual verification.",
        "discovery_baseline": "a7f387a", "prerequisite": "Phase 1 PASS report read; 81 tests rerun successfully before changes.",
        "requested_scenarios": requested,
        "unit_tests": {"run": result.testsRun, "passed": sum(row["status"] == "PASS" for row in result.rows),
                       "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
                       "observed_output": stream.getvalue(), "results": result.rows},
        "compatibility": {"existing_tests_run": len(old), "existing_tests_passed": sum(row["status"] == "PASS" for row in old),
                          "bulk_migration": False, "legacy_reviewed_promoted": False},
        "workspace_errors": errors,
        "workspace_warnings": [item for item in checks if item.startswith("WARNING ")],
        "governance_audit": audit_governance(ROOT),
        "limits": [
            "All approval and source workflow fixtures are TEST_ONLY; no production knowledge or real human claim approval was created.",
            "A local human approval record is a review assertion, not cryptographic identity authentication; trusted Git review and task authorization remain required.",
            "Semantic conflict discovery, evidence relevance, actual implementation, correct real-world project assignment and human identity require manual review.",
            "Restricted-scope gates isolate retrieval, not OS file access; Lint and source integrity remain workspace-wide.",
            "Legacy pages stay readable but cannot acquire verified authority through the adapter; no historical dates or events are inferred.",
            "Review deadlines trigger warnings, never automatic status changes, deletion or a claim that old knowledge is obsolete.",
            "No external repository, URL fetch, real ingestion, Obsidian visual validation or Phase 3 work was performed.",
        ],
    }


def markdown(report):
    unit = report["unit_tests"]
    lines = ["# Phase 2 — Knowledge Lifecycle and Isolation Audit", "",
             f"**{report['verdict']}** — {report['verdict_scope']}", "",
             f"Observed: {unit['run']} tests, {unit['passed']} PASS, {unit['failures']} failures, "
             f"{unit['errors']} errors, {unit['skipped']} skipped.",
             f"Strict workspace checks: {len(report['workspace_errors'])} errors, "
             f"{len(report['workspace_warnings'])} warnings.", "",
             "## Objective and discovery", "",
             "- Extend V1 governance while retaining Phase 1 raw/provenance controls and existing work.",
             "- Baseline a7f387a; Phase 1 PASS and its 81 tests were checked before implementation.",
             "- Existing DRAFT/REVIEWED/STALE and ADR APPROVED labels had no content-bound lifecycle approval history.",
             "- Existing exact-scope lexical search was preserved and extended with declared cross-project context, history and restricted-scope gates.",
             "- Existing user Obsidian graph changes are outside this implementation.", "",
             "## Files inspected and changed", "",
             "- Read: AGENTS.md, README.md, SCHEMA.md, PROFILE.md, wiki index/log and scaffold, project contexts/index, ADR template/index, relevant prompts, Phase 1 report and existing validation/query/test implementations.",
             "- Core changes: scripts/knowledge_governance.py, check_workspace.py, query_workspace.py, test_knowledge_governance.py and this observed validation runner.",
             "- Contract/template changes: KNOWLEDGE_GOVERNANCE.md, SCHEMA.md, AGENTS.md, README.md, MULTILINGUAL.md, wiki/ADR templates, three prompts, wiki operating navigation and append-only maintenance log.",
             "- Sources used: first-party repository files and disposable synthetic fixtures only; no external factual knowledge.", "",
             "## Specification and compatibility", "",
             "See [governance specification, state machine and scope rules](../KNOWLEDGE_GOVERNANCE.md).",
             f"Compatibility regressions: {report['compatibility']['existing_tests_passed']} / "
             f"{report['compatibility']['existing_tests_run']} existing tests passed.",
             "Canonical metadata uses the existing Markdown bullet parser; no schema_version, database or competing serialization standard.",
             "Legacy REVIEWED maps to unverified; existing wiki/source files are not bulk rewritten. Governed templates are checked at two wiki depths.",
             "Historical decisions remain retrievable explicitly, while old facts do not expire by age.", "",
             "## Required observed scenarios", ""]
    for row in report["requested_scenarios"]:
        names = ", ".join(test["test"].split(".")[-1] for test in row["observed_tests"]) or "NOT_RUN"
        lines.append(f"- {row['status']}: {row['scenario']}. {names}")
    lines += ["", "## All observed test results", ""]
    lines.extend(f"- {row['status']}: {row['test']}" for row in unit["results"])
    lines += ["", "## Remaining risks and checks not run", ""]
    lines.extend("- " + value for value in report["limits"])
    lines += ["", "## Reproduce", "", "~~~text",
              "python -B scripts/validate_knowledge_governance.py",
              "python -B scripts/check_workspace.py --integrity", "~~~", "",
              "Human approval is still required for actual knowledge verification, decision approval and real ingestion; the implementation task approves none of those actions.", ""]
    return "\n".join(lines)


def save(report, output):
    if __package__:
        from .safe_operations import save_reports
    else:
        from safe_operations import save_reports
    return save_reports(ROOT, report, output, markdown)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = evaluate()
    if args.output:
        save(report, args.output)
    print(json.dumps({"verdict": report["verdict"], "tests": report["unit_tests"]["run"],
                      "passed": report["unit_tests"]["passed"], "required_scenarios": report["requested_scenarios"]},
                     ensure_ascii=False, indent=2))
    return 1 if report["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
