#!/usr/bin/env python3
"""Observed Phase 3 controls, attack traces and recovery evidence; synthetic only."""
import argparse
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
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, resultclass=RecordedResult, verbosity=0).run(suite)
    module = sys.modules.get("test_security_recovery")
    observations = list(getattr(module, "ATTACK_OBSERVATIONS", []))
    recovery = dict(getattr(module, "RECOVERY_OBSERVATION", {}))
    required = []
    for number in range(1, 11):
        rows = [row for row in result.rows if row["test"].startswith("test_security_recovery.")
                and row["test"].split(".")[-1].startswith(f"test_{number:02d}_")]
        required.append({"scenario": number, "tests": rows,
                         "status": "PASS" if len(rows) == 1 and rows[0]["status"] == "PASS" else "FAIL"})
    expected_attacks = len(json.loads((ROOT / "tests/fixtures/security/attacks.json").read_text(encoding="utf-8"))["samples"]) * 2
    checks = check_workspace(ROOT, integrity=True, security=True)
    errors = [item for item in checks if item.startswith("ERROR ")]
    attack_ok = len(observations) == expected_attacks and all(
        row["observed_status"] == "UNTRUSTED_CONTENT" and row["user_files_unchanged"] for row in observations)
    recovery_ok = (recovery.get("recovery_result", {}).get("status") == "ROLLED_BACK"
                   and recovery.get("all_user_files_preserved") is True
                   and recovery.get("before_hashes") == recovery.get("after_hashes"))
    passed = (result.wasSuccessful() and not result.skipped and not errors and attack_ok and recovery_ok
              and all(item["status"] == "PASS" for item in required))
    return redact({
        "phase": "AI-WORKSPACE V1 Phase 3 only", "discovery_baseline": "309e364",
        "guarded_workflow_verdict": "PASS" if passed else "FAIL",
        "verdict": "CONDITIONAL" if passed else "FAIL",
        "verdict_reason": "Guarded APIs are enforced and tested; broader agent tool permissions remain unchanged and were not proven contained.",
        "synthetic_only": True, "required_scenarios": required,
        "unit_tests": {"run": result.testsRun, "passed": sum(row["status"] == "PASS" for row in result.rows),
                       "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
                       "observed_output": stream.getvalue(), "results": result.rows},
        "workspace_errors": errors, "workspace_warnings": [item for item in checks if item.startswith("WARNING ")],
        "attack_observations": observations, "recovery_demonstration": recovery,
        "compatibility": {
            "baseline_tests": 112,
            "existing_tests_run": sum(not row["test"].startswith("test_security_recovery.") for row in result.rows),
            "existing_tests_passed": sum(not row["test"].startswith("test_security_recovery.") and row["status"] == "PASS" for row in result.rows),
            "changed_failure_contract": "Interrupted registration now restores exact metadata instead of leaving an orphan; its fault-injection regression was updated and run.",
        },
        "residual_risks": [
            "General Codex/editor/shell access can bypass the Python workflow layer; no OS ACL or host permission configuration was changed.",
            "Injection signatures are conservative, incomplete and can have false positives. No complete LLM-agent/model red-team evaluation was run.",
            "Local human/task assertions and journal records are not cryptographically authenticated against a malicious same-user process.",
            "Cooperating writers are serialized; hostile non-cooperating writers and physical power loss require additional external controls.",
            "Secret scanning covers approved public documents and explicit authorized source intake, not every ignored file or all possible personal information.",
            "Source admission and wiki synthesis are separate authorized checkpoints; failed synthesis retains the admitted immutable source.",
            "No real secrets, production knowledge, external targets, deploy/push/merge or Phase 4 work was used.",
        ],
    })


def markdown(report):
    unit = report["unit_tests"]
    lines = ["# Phase 3 — Security and Recovery Audit", "",
             f"**Overall: {report['verdict']}**. Guarded workflow controls: **{report['guarded_workflow_verdict']}**.",
             report["verdict_reason"], "",
             f"Observed: {unit['run']} tests; {unit['passed']} PASS, {unit['failures']} failures, "
             f"{unit['errors']} errors, {unit['skipped']} skipped.",
             f"Strict source/security Lint: {len(report['workspace_errors'])} errors, {len(report['workspace_warnings'])} warnings.", "",
             "## Threat model and policy", "",
             "See [trust boundaries, allowlist, safeguards and recovery procedure](../SECURITY_POLICY.md).",
             "Read: repository AGENTS/README/SCHEMA/PROFILE, wiki index/log, relevant prompts, prior phase reports, "
             "source/governance/query/report implementations and validation tests.",
             "Sources used: first-party repository state and TEST_ONLY synthetic attack fixtures. No real secret was opened.",
             "Changed: bounded transaction/security/Ingest modules; registration, lifecycle, Query and report writers; "
             "path guards, security Lint, operating docs/prompts, adversarial tests and append-only maintenance history.", "",
             "## Compatibility and implementation findings", "",
             "- Existing source hashes, lifecycle approval, citations and exact-scope matching were retained.",
             "- Earlier raw publication/direct wiki writes and two-file append registration had incomplete-operation windows.",
             "- Writes now use expected versions, ownership, staged bytes, before-images and validated recovery; "
             "source history remains logically append-only.",
             "- The old interrupted-registration orphan test now injects failure during replacement and verifies exact restoration.",
             f"- Existing regressions passed: {report['compatibility']['existing_tests_passed']} / "
             f"{report['compatibility']['existing_tests_run']}. Historical phase reports were preserved.", "",
             "## Required observed scenarios", ""]
    for row in report["required_scenarios"]:
        names = ", ".join(item["test"].split(".")[-1] for item in row["tests"]) or "NOT_RUN"
        lines.append(f"- {row['status']}: {row['scenario']}. {names}")
    lines += ["", "## Actual adversarial handling paths", ""]
    for row in report["attack_observations"]:
        lines.append(f"- {row['sample']} / {row['path']}: {row['observed_status']}; "
                     f"user files unchanged: {row['user_files_unchanged']}.")
    demo = report["recovery_demonstration"]
    lines += ["", "## Recovery demonstration on disposable fixtures", "",
              f"- Injected interruption after {demo.get('failure_after_resource_replacements', 'NOT_RUN')} target replacement.",
              f"- Query before recovery: {demo.get('query_before_recovery', 'NOT_RUN')}.",
              f"- Actual recovery result: {demo.get('recovery_result', {}).get('status', 'NOT_RUN')}.",
              f"- Exact user-file preservation: {demo.get('all_user_files_preserved', False)}.",
              f"- Before/after resource hashes equal: {demo.get('before_hashes') == demo.get('after_hashes') if demo else False}.",
              "- The JSON companion contains the observed operation ID and before/after hashes; it contains no source bodies or secret values.",
              "- Additional tests cover recovery conflicts, journal tampering, committed-state recovery and stale-owner acknowledgement.", "",
              "## All observed tests", ""]
    lines.extend(f"- {row['status']}: {row['test']}" for row in unit["results"])
    lines += ["", "## Residual risks and checks not run", ""]
    lines.extend("- " + item for item in report["residual_risks"])
    lines += ["", "## Reproduce", "", "~~~text", "python -B scripts/validate_security.py",
              "python -B scripts/check_workspace.py --integrity --security", "~~~", "",
              "The whole-agent verdict remains CONDITIONAL until broader host permissions are independently constrained and tested. "
              "This phase did not change global settings or begin Phase 4.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = evaluate()
    if args.output:
        save_reports(ROOT, report, args.output, markdown)
    print(json.dumps({"verdict": report["verdict"], "guarded_workflows": report["guarded_workflow_verdict"],
                      "tests": report["unit_tests"]["run"], "passed": report["unit_tests"]["passed"],
                      "attack_observations": len(report["attack_observations"]),
                      "recovery": report["recovery_demonstration"].get("recovery_result", {}).get("status")}, indent=2))
    return 1 if report["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
