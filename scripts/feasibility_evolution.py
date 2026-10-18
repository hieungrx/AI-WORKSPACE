"""Measured TEST_ONLY knowledge evolution through existing bounded V1 APIs.

The retained fixture is for a separate reader; it is never production knowledge.
No human approval, factual verification or model token accounting is simulated.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from time import perf_counter
from unittest.mock import patch

ROOT = Path(__file__).absolute().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import check_workspace as lint
from scripts import ingest_workspace as ingest
from scripts import knowledge_governance as governance
from scripts import query_workspace as query
from scripts import safe_operations as operations
from scripts import source_integrity as integrity
from tests.workflow_support import Workspace

SOURCE_A = "SRC-20261018-801"
SOURCE_B = "SRC-20261018-802"
SOURCE_UNRELATED = "SRC-20261018-803"
PAGE = "wiki/request-budget.md"
UNRELATED_PAGE = "wiki/cache-policy.md"
SCOPE = "synthetic-workbench"
QUESTION = "giới hạn yêu cầu"
CLAIM_A = "TEST_ONLY observation A: Lyra API permits 60 requests per minute."
CLAIM_B = "TEST_ONLY observation B: Lyra API permits 45 requests per minute."


def _hash(data):
    return hashlib.sha256(data).hexdigest()


def _preservation_checks(root, baseline):
    """Re-read protected files and append-only prefixes, rather than trust event labels."""
    checks = {}
    for relative, expected in baseline["files"].items():
        path = root / relative
        checks[relative] = path.is_file() and _hash(path.read_bytes()) == expected
    for relative, expected in baseline["prefixes"].items():
        path = root / relative
        checks[relative + ":old_prefix"] = (path.is_file()
            and _hash(path.read_bytes()[:expected["bytes"]]) == expected["sha256"])
    return checks


def _owned_directory(directory):
    directory = Path(directory).absolute()
    tests = ROOT / "tests"
    try:
        relative = directory.relative_to(tests)
    except ValueError:
        raise ValueError("DISPOSABLE_FEASIBILITY_DIRECTORY_REQUIRED") from None
    if (not relative.parts or not relative.parts[0].startswith("fixture-feasibility-")
            or ".." in relative.parts or directory.resolve() != directory):
        raise ValueError("DISPOSABLE_FEASIBILITY_DIRECTORY_REQUIRED")
    if directory.exists() and any(directory.iterdir()):
        raise FileExistsError("EMPTY_FEASIBILITY_DIRECTORY_REQUIRED")
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def evaluate_evolution(directory: Path):
    """Create and retain a synthetic workspace in the caller's empty fixture directory."""
    directory = _owned_directory(directory)
    result = {"passed": False, "synthetic_only": True,
              "workspace_path": str(directory / "workspace"), "checks": {},
              "observations": [], "maintenance_elapsed_seconds": {},
              "subprocess_continuity": {"status": "NOT RUN"}, "failures": [],
              "human_approvals_created": 0, "human_fact_validation": "NOT RUN",
              "token_usage": None, "api_cost": None, "human_review_time_seconds": None}
    checks = result["checks"]

    def measure(name, operation):
        started = perf_counter()
        try:
            return operation()
        finally:
            result["maintenance_elapsed_seconds"][name] = perf_counter() - started

    def observe(name, value):
        result["observations"].append({"stage": name, "result": value})
        return value

    try:
        w = Workspace(directory / "workspace")
        root = w.root
        # Workspace supplies shared fixture scaffolding. This run never calls verify().
        w.write("reports/validation.md", "# TEST_ONLY fixture\nNo human review or approval occurred.\n")
        measure("unrelated_source_admission", lambda: w.register(
            SOURCE_UNRELATED, "TEST_ONLY cache entries expire after 120 seconds."))
        unrelated = w.page(title="Cache policy", sources=(SOURCE_UNRELATED,), scope=SCOPE,
            claims=[(SOURCE_UNRELATED, "TEST_ONLY cache lifetime is 120 seconds.")],
            page_id="feasibility-cache-policy", keywords='["cache lifetime"]')
        observe("unrelated_draft_ingest", measure("unrelated_draft_ingest", lambda: w.apply(
            UNRELATED_PAGE, unrelated, sid=SOURCE_UNRELATED, scope=SCOPE)))
        row_a = measure("source_a_admission", lambda: w.register(SOURCE_A, CLAIM_A))
        observe("source_a_admission", w.registration_results[-1])
        initial = w.page(title="Lyra API request budget", sources=(SOURCE_A,), scope=SCOPE,
            claims=[(SOURCE_A, CLAIM_A)], page_id="feasibility-request-budget",
            keywords='["Lyra API", "request budget"]', aliases_vi=json.dumps([QUESTION], ensure_ascii=False),
            temporal="current", review_after="2099-12-31")
        observe("initial_draft_ingest", measure("initial_draft_ingest", lambda: w.apply(
            PAGE, initial, sid=SOURCE_A, scope=SCOPE)))
        measure("initial_unverified_transition", lambda: w.move(PAGE, "unverified"))
        before_read = w.snapshot(include_recovery=True)
        initial_query = measure("initial_query", lambda: query.search(root, QUESTION, SCOPE))
        observe("initial_query", initial_query)
        checks["initial_query_found_unverified"] = (initial_query["status"] == "FOUND"
            and len(initial_query["matches"]) == 1
            and initial_query["matches"][0]["knowledge_status"] == "unverified"
            and initial_query["matches"][0]["usable_as_current_truth"] is False)
        checks["initial_query_read_only"] = w.snapshot(include_recovery=True) == before_read

        # The supported edit path explicitly returns unverified knowledge to draft.
        measure("return_to_draft", lambda: w.move(PAGE, "draft"))
        protected_files = (row_a["source_url_or_path"],
                           "sources/raw/" + SOURCE_UNRELATED + ".md", UNRELATED_PAGE)
        baseline = {"files": {relative: _hash((root / relative).read_bytes())
                              for relative in protected_files}, "prefixes": {}}
        for relative in ("sources/manifest.csv", "sources/provenance.jsonl", "wiki/index.md", "wiki/log.md"):
            data = (root / relative).read_bytes()
            baseline["prefixes"][relative] = {"bytes": len(data), "sha256": _hash(data)}
        result["preservation_baseline"] = baseline
        measure("source_b_admission", lambda: w.register(SOURCE_B, CLAIM_B))
        observe("source_b_admission", w.registration_results[-1])
        baseline["files"]["sources/raw/" + SOURCE_B + ".md"] = _hash(
            (root / "sources/raw" / (SOURCE_B + ".md")).read_bytes())
        original_text = (root / PAGE).read_text(encoding="utf-8")
        updated = governance.replace_field(original_text, "Source IDs", SOURCE_A + ", " + SOURCE_B)
        updated = governance.replace_field(updated, "conflicts", json.dumps([{
            "summary": "TEST_ONLY contradictory request budgets; no winner selected.",
            "source_ids": [SOURCE_A, SOURCE_B], "resolution": None}]))
        updated += "\n- FACT: " + CLAIM_B + " [" + SOURCE_B + ", section Evidence]\n"
        changes, expected = w.plan(PAGE, updated)
        before_failed_write = w.snapshot()
        original_replace = operations._replace_file
        attempted_writes = 0

        def fail_second_owned_write(staged, target):
            nonlocal attempted_writes
            if staged.suffix == ".after":
                attempted_writes += 1
                if attempted_writes == 2:
                    raise OSError("TEST_ONLY_FEASIBILITY_WRITE_FAILURE")
            return original_replace(staged, target)

        error_code = None
        started = perf_counter()
        try:
            with patch.object(operations, "_replace_file", fail_second_owned_write):
                ingest.ingest_registered(root, SOURCE_B, changes, expected,
                    scope=SCOPE, authorized=True, apply=True)
        except OSError as error:
            error_code = str(error)
        finally:
            result["maintenance_elapsed_seconds"]["failed_update_and_automatic_rollback"] = perf_counter() - started
        checks["failed_update_injected_after_first_owned_replacement"] = (
            attempted_writes == 2 and error_code == "TEST_ONLY_FEASIBILITY_WRITE_FAILURE")
        checks["failed_existing_update_exact_rollback"] = w.snapshot() == before_failed_write
        checks["failed_update_no_pending_journal_or_lock"] = not any(
            (root / "recovery" / name).exists() for name in ("active.json", "owner.lock"))
        observe("failed_existing_update", {"error": error_code, "owned_replacements_attempted": attempted_writes,
            "before_hashes": before_failed_write, "after_hashes": w.snapshot()})
        retry = measure("retry_conflicting_draft_update", lambda: ingest.ingest_registered(
            root, SOURCE_B, changes, expected, scope=SCOPE, authorized=True, apply=True))
        observe("retry_conflicting_draft_update", retry)
        checks["retry_committed"] = retry["status"] == "COMMITTED"
        measure("updated_unverified_transition", lambda: w.move(PAGE, "unverified"))
        measure("disputed_transition", lambda: w.move(PAGE, "disputed"))
        final_text = (root / PAGE).read_text(encoding="utf-8")
        checks["original_claim_retained_verbatim"] = ("- FACT: " + CLAIM_A + " [" + SOURCE_A
            + ", section Evidence]") in final_text
        checks["both_conflicting_claims_retained"] = CLAIM_A in final_text and CLAIM_B in final_text
        checks["original_transition_prefix_retained"] = governance.array(lint.metadata(final_text), "transitions")[:2] == (
            governance.array(lint.metadata(original_text), "transitions"))
        before_read = w.snapshot(include_recovery=True)
        final_query = measure("disputed_query", lambda: query.search(root, QUESTION, SCOPE))
        observe("disputed_query", final_query)
        blocked = final_query.get("blocked", [])
        checks["conflict_query_disputed_with_both_references"] = (final_query["status"] == "DISPUTED"
            and len(blocked) == 1 and blocked[0]["knowledge_status"] == "disputed"
            and blocked[0]["usable_as_current_truth"] is False
            and {cite.get("source_id") for cite in blocked[0]["citations"]} == {SOURCE_A, SOURCE_B}
            and blocked[0]["conflicts"][0]["resolution"] is None)
        issues = measure("strict_lint", lambda: lint.check_workspace(root, integrity=True, security=True))
        observe("strict_lint", {"issues": issues, "errors": sum(i.startswith("ERROR ") for i in issues),
                                "warnings": sum(i.startswith("WARNING ") for i in issues)})
        checks["strict_lint_no_errors"] = not any(i.startswith("ERROR ") for i in issues)
        checks["query_and_lint_read_only"] = w.snapshot(include_recovery=True) == before_read
        audit = measure("source_integrity_audit", lambda: integrity.audit_sources(root))
        checks["three_sources_intact_and_unverified"] = (set(audit["sources"]) == {
            SOURCE_A, SOURCE_B, SOURCE_UNRELATED} and all(source["integrity_status"] == "MATCH"
            and source["verification_status"] == "UNVERIFIED" for source in audit["sources"].values()))
        result["preservation_results"] = _preservation_checks(root, baseline)
        checks["unrelated_raw_and_append_only_prefixes_preserved"] = all(result["preservation_results"].values())
        checks["no_approval_records_created"] = not (root / "experiments").exists()

        # A fresh Python interpreter receives only root/query/scope, no conversation state.
        command = [sys.executable, "-B", str(ROOT / "scripts/query_workspace.py"),
                   "--root", str(root), "--scope", SCOPE, "--query", QUESTION]
        before_subprocess = w.snapshot(include_recovery=True)
        completed = measure("fresh_python_query", lambda: subprocess.run(command, cwd=ROOT,
            capture_output=True, text=True, encoding="utf-8", timeout=60, check=False))
        try:
            fresh = json.loads(completed.stdout)
        except ValueError:
            fresh = None
        same = fresh == final_query
        readonly = w.snapshot(include_recovery=True) == before_subprocess
        result["subprocess_continuity"] = {"status": "PASS" if completed.returncode == 0 and same and readonly else "FAIL",
            "method": "fresh Python subprocess, not a new agent or human review",
            "conversation_history_supplied": False, "include_history": False,
            "exit_code": completed.returncode, "query": QUESTION, "scope": SCOPE,
            "stderr": completed.stderr, "output": fresh, "same_result": same, "read_only": readonly}
        checks["fresh_python_continuity"] = result["subprocess_continuity"]["status"] == "PASS"
        result["final_snapshot_hashes"] = w.snapshot()
        checks["scenario_completed"] = True
    except Exception as error:
        result["failures"].append({"type": type(error).__name__, "detail": str(error)})
        checks["scenario_completed"] = False
    result["failures"].extend({"check": key} for key, value in checks.items() if value is not True)
    result["passed"] = bool(checks) and all(value is True for value in checks.values()) and not result["failures"]
    return result
