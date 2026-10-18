#!/usr/bin/env python3
"""Run fresh regressions and reproduce both original governance public paths."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).absolute().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts import check_workspace as lint
from scripts import knowledge_governance as governance
from scripts import query_workspace as query
from scripts import safe_operations as operations
from scripts.source_integrity import read_registry
from scripts.validate_workflows import evaluate as run_workflow_validation
from tests.workflow_support import Workspace, DAY, SID


IMPLEMENTATION = ("knowledge_governance.py", "query_workspace.py", "check_workspace.py", "safe_operations.py")


def code_hashes():
    return {name: hashlib.sha256((ROOT / "scripts" / name).read_bytes()).hexdigest() for name in IMPLEMENTATION}


def original_paths():
    observations = {}
    with tempfile.TemporaryDirectory(prefix="fixture-governance-remediation-", dir=ROOT / "tests") as directory:
        w = Workspace(Path(directory) / "workspace")
        cases = []
        for name, extra in (("future", {"effective_at": "2099-01-01"}),
                            ("overdue", {"review_after": "2020-01-01"}),
                            ("historical", {"temporal": "historical"})):
            adr, page = f"decisions/{name}.md", f"wiki/current-{name}.md"
            fields = {"kind": "approved_decision", "temporal": "current", "review_after": "2099-12-31"}
            fields.update(extra)
            w.write(adr, w.page(title="ADR " + name, sources=(), claims=[], scope="audit-project", **fields)
                    + "- FACT: TEST_ONLY project chose option A.\n")
            w.verify(adr)
            w.write(page, w.page(title="Current " + name, sources=(), claims=[], scope="audit-project",
                                temporal="current", review_after="2099-12-31")
                    + f"- FACT: TEST_ONLY current configuration uses A. [ADR](../{adr})\n")
            w.verify(page)
            index = w.root / "wiki/index.md"
            index.write_bytes(index.read_bytes() + f"[page](current-{name}.md)\n[decision](../{adr})\n".encode())
            result = query.search(w.root, "Current " + name, "audit-project")
            cases.append({"case": name, "status": result["status"],
                          "current": [p["usable_as_current_truth"] for p in result["matches"]],
                          "citations": [p["citations"] for p in result["matches"]]})
        observations["H-GOV-01"] = {"cases": cases, "passed": all(
            row["status"] == "FOUND" and row["current"] == [False] for row in cases)}
        w.register()
        other = "SRC-20261018-502"
        w.register(other, body="TEST_ONLY alternate evidence")
        conflicts = [{"summary": "TEST_ONLY disagreement", "source_ids": [SID, other],
                      "resolution": "TEST_ONLY proposed reconciliation awaiting validation"}]
        page = "wiki/conflict.md"
        w.write(page, w.page(title="Conflict probe", sources=(SID, other), conflicts=json.dumps(conflicts)))
        w.move(page, "unverified")
        w.move(page, "disputed")
        before = w.snapshot(include_recovery=True)
        original = (w.root / page).read_text(encoding="utf-8")
        events = governance.array(lint.metadata(original), "transitions")
        # Exact legacy six-key event from the original audit, not just a v2 test.
        events.append({"from": "disputed", "to": "unverified", "actor": "human", "at": DAY,
                       "reason": "TEST_ONLY missing approval probe", "approval": "experiments/does-not-exist.md"})
        proposed = governance.replace_field(governance.replace_field(original, "status", "unverified"),
                                            "transitions", json.dumps(events))
        outcomes = {}
        try:
            governance.transition(w.root, page, "unverified", actor="human", at=DAY, reason="TEST_ONLY audit",
                                  approval_ref="experiments/does-not-exist.md", authorized=True, apply=True)
            outcomes["helper"] = "UNEXPECTED_ALLOW"
        except (ValueError, OSError) as error:
            outcomes["helper"] = type(error).__name__
        try:
            operations.transact(w.root, {page: proposed.encode()},
                                operations.versions(w.root, [page], operation="lifecycle"),
                                operation="lifecycle", authorized=True)
            outcomes["writer"] = "UNEXPECTED_COMMITTED"
        except (ValueError, OSError) as error:
            outcomes["writer"] = type(error).__name__
        outcomes["no_durable_event"] = before == w.snapshot(include_recovery=True)
        w.write(page, proposed)  # Deliberate invalid historical fixture, never live data.
        outcomes["query"] = query.search(w.root, "Conflict probe", "global")["status"]
        outcomes["lint_errors"] = [i for i in lint.check_workspace(w.root, integrity=True, security=True)
                                   if i.startswith("ERROR ")]
        observations["H-GOV-02"] = {"outcomes": outcomes, "passed": (
            outcomes["helper"] != "UNEXPECTED_ALLOW" and outcomes["writer"] != "UNEXPECTED_COMMITTED"
            and outcomes["no_durable_event"] and outcomes["query"] == "INVALID_DATA"
            and bool(outcomes["lint_errors"]))}
    observations["owned_fixture_cleaned"] = not Path(directory).exists()
    return observations


def evaluate():
    before_code = code_hashes()
    tests = run_workflow_validation()
    unit = tests["unit_tests"]
    rows = unit["results"]
    adr = [r for r in rows if r["test"].startswith("test_governance_adr_eligibility.")]
    approvals = [r for r in rows if r["test"].startswith("test_governance_approval_paths.")]
    full_ok = (before_code == code_hashes() and unit["run"] >= 219 and unit["run"] == unit["passed"] and not unit["skipped"]
               and not unit["failures"] and not unit["errors"] and len(adr) >= 21 and len(approvals) >= 24)
    observed = original_paths()
    checks = lint.check_workspace(ROOT, integrity=True, security=True)
    return {"phase": "V1 high governance remediation only", "observed_at_utc": datetime.now(timezone.utc).isoformat(),
            "tested_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "validation_entry_point": "Fresh scripts.validate_workflows.evaluate() plus original-path probes; no imported PASS reports.",
            "unit_tests": unit,
            "focused_cases": {"H-GOV-01": adr, "H-GOV-02": approvals}, "original_paths": observed,
            "findings": {name: "RESOLVED" if full_ok and observed[name]["passed"]
                         and not any(i.startswith("ERROR ") for i in checks) else "PARTIALLY RESOLVED"
                         for name in ("H-GOV-01", "H-GOV-02")},
            "workspace_checks": checks, "live_registered_sources": len(read_registry(ROOT)),
            "code_sha256": before_code, "code_unchanged_during_validation": before_code == code_hashes(),
            "workflow_metrics": tests.get("benchmark", {}).get("metrics", {}),
            "compatibility": "Existing source/metadata schema retained; new required events use policy 2. Legacy policy 1 is read-only replay, with missing approvals errors and unavailable historical-content snapshots explicitly unverified.",
            "limits": ["TEST_ONLY approvals are fixtures, not real human approvals or authenticated identities.",
                       "No live knowledge, history or old approval is migrated/deleted/rewritten.",
                       "Graph depth has a 32-node fail-closed bound; dense graphs and new retrieval latency are not benchmarked.",
                       "Host containment, real secrets, real URLs, physical power loss and production intake are not tested.",
                       "Earlier Medium/Low audit findings remain outside this two-High remediation scope."]}


def markdown(r):
    lines = ["# V1 Governance Remediation - Verification", "", "First-party local synthetic evidence; no V2 or real intake.", "",
             "Findings: " + json.dumps(r["findings"]), "", "Executed test totals: " + json.dumps({k: v for k, v in r["unit_tests"].items() if k not in {"results", "observed_output"}}),
             "", "Tested checkout HEAD: " + r["tested_head"] + "; scoped implementation hashes are in JSON.",
             "", "## Root causes and enforced invariants", "",
             "H-GOV-01: duplicated, incomplete ADR gates and page-wide evidence fallback. Canonical per-finding evidence now recursively applies own and dependency eligibility; historical/context retrieval is separate from current truth. Independent valid evidence for the same claim is retained.",
             "H-GOV-02: the helper checked approval but writer/replay did not. Shared event approval validation now covers helper, pre-commit writer, replay, Query and Lint. New events bind policy, subject, transition, snapshot hash and prior history; invalid approval cannot commit or be hidden by final unverified/draft status.",
             "", "## Original public paths rerun", "", json.dumps(r["original_paths"], ensure_ascii=False, indent=2),
             "", "## Regression cases and acceptance evidence", ""]
    for finding, rows in r["focused_cases"].items():
        lines += ["### " + finding, ""] + ["- " + row["status"] + ": " + row["test"] for row in rows] + [""]
    lines += ["## Compatibility", "", r["compatibility"], "", "## Workspace checks", ""] + r["workspace_checks"]
    lines += ["", "## Remaining risks / NOT RUN", ""] + ["- " + item for item in r["limits"]]
    lines += ["", "No real claim/decision approval, source intake, push/merge/deploy or V2 is authorized by these results.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    result = evaluate()
    if args.output:
        operations.save_reports(ROOT, result, args.output, markdown)
    print(json.dumps({"findings": result["findings"], "unit_tests": {k: v for k, v in result["unit_tests"].items()
                                                                   if k not in {"results", "observed_output"}}}, indent=2))
    return 0 if all(value == "RESOLVED" for value in result["findings"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
