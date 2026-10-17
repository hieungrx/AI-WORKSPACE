#!/usr/bin/env python3
"""Observed Phase 1 audit plus the existing and synthetic regression suites."""
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
from scripts.source_integrity import audit_sources


class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.rows.append({"test": test.id(), "status": "PASS"})

    def addFailure(self, test, error):
        super().addFailure(test, error)
        self.rows.append({"test": test.id(), "status": "FAIL", "detail": self._exc_info_to_string(error, test)})

    def addError(self, test, error):
        super().addError(test, error)
        self.rows.append({"test": test.id(), "status": "ERROR", "detail": self._exc_info_to_string(error, test)})

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.rows.append({"test": test.id(), "status": "SKIP", "reason": reason})

    def addSubTest(self, test, subtest, error):
        super().addSubTest(test, subtest, error)
        if error is not None:
            self.rows.append({"test": subtest.id(), "status": "FAIL", "detail": self._exc_info_to_string(error, test)})

    def addExpectedFailure(self, test, error):
        super().addExpectedFailure(test, error)
        self.rows.append({"test": test.id(), "status": "EXPECTED_FAILURE"})

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self.rows.append({"test": test.id(), "status": "UNEXPECTED_SUCCESS"})


def evaluate():
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, resultclass=RecordedResult, verbosity=0).run(suite)
    audit = audit_sources(ROOT)
    workspace_issues = check_workspace(ROOT, integrity=True)
    errors = [item for item in workspace_issues if item.startswith("ERROR ")]
    skipped = any(row["status"] != "PASS" for row in result.rows)
    verdict = "FAIL" if errors or not result.wasSuccessful() else "CONDITIONAL" if skipped else "PASS"
    return {
        "phase": "AI-WORKSPACE V1 Phase 1 only",
        "verdict": verdict,
        "verdict_scope": "Source-integrity contract, current registry and synthetic fixtures; not factual correctness or Phase 2.",
        "synthetic_tests_only": True,
        "live_registered_sources": len(audit["sources"]),
        "live_hash_matches": sum(item["integrity_status"] == "MATCH" for item in audit["sources"].values()),
        "workspace_errors": errors,
        "workspace_warnings": [item for item in workspace_issues if item.startswith("WARNING ")],
        "source_audit": audit,
        "unit_tests": {
            "run": result.testsRun,
            "passed": sum(row["status"] == "PASS" for row in result.rows),
            "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
            "observed_output": stream.getvalue(), "results": result.rows,
        },
        "limits": [
            "No real knowledge was ingested; an empty live registry is explicitly reported.",
            "Original URL availability is recorded metadata, never a live network verification here.",
            "Legacy sources without a baseline remain LEGACY_UNHASHED and fail strict admission until migration.",
            "Migration records current bytes, not proof of historical immutability.",
            "Phase 3 journals metadata publication and rollback; unresolved recovery blocks queries. Legacy orphan records need human reconciliation.",
            "Hashes and citations do not prove factual correctness; trusted Git history protects the baseline.",
        ],
    }


def markdown(report):
    unit = report["unit_tests"]
    lines = [
        "# Phase 1 — Source Integrity Audit", "",
        "First-party observed repository audit and synthetic test results. No real source ingestion.", "",
        "## Final verdict", "",
        f"**{report['verdict']}** — {report['verdict_scope']}", "",
        f"Observed: {unit['run']} automated tests; {unit['passed']} PASS, "
        f"{unit['failures']} failures, {unit['errors']} errors, {unit['skipped']} skipped.",
        f"Live registered sources: {report['live_registered_sources']}; "
        f"hash-matched live sources: {report['live_hash_matches']}.",
        f"Strict workspace errors: {len(report['workspace_errors'])}; "
        f"warnings: {len(report['workspace_warnings'])}.", "",
        "## Discovery and inconsistencies", "",
        "- Discovery baseline b2acfef already had unique ID/date validation, CSV checks, wiki references, "
        "structured citations, path guards and bilingual lexical search. Existing features were extended.",
        "- The old citation gate checked file existence: a recorded synthetic baseline experiment changed "
        "raw bytes but still returned FOUND. Hash-backed sources now fail closed on that change.",
        "- Old documentation said Query never opened raw. The current contract explicitly distinguishes "
        "legacy metadata-only retrieval from binary hash verification for recorded provenance.",
        "- Immutability and source revisions previously had written rules but no admission/version guard. "
        "Exclusive snapshots, append-only admission, duplicate policy and lineage validation now implement them.",
        "- A pre-existing .obsidian/graph.json working change was excluded from the implementation scope.", "",
        "## Contract and compatibility", "",
        "See [provenance contract and migration notes](../SOURCE_INTEGRITY.md). The nine-column CSV is unchanged; "
        "new metadata is an append-only ledger. Missing author/publisher/date/origin stays unknown. "
        "A matching hash does not set VERIFIED.",
        "Existing compatibility tests, including paired bilingual retrieval, are included in the run below. "
        "The legacy migration test verifies raw/CSV preservation and explicit baseline creation.", "",
        "## Requested synthetic scenarios", "",
    ]
    for row in unit["results"]:
        if ".test_0" in row["test"] or ".test_10_" in row["test"]:
            lines.append(f"- {row['status']}: {row['test'].split('.')[-1]}")
    lines += ["", "## Acceptance evidence", ""]
    links = {
        "Unambiguous identity and deterministic duplicates": ("test_01_", "test_02_", "test_03_"),
        "Validated source references and multi-source traceability": ("test_06_", "test_multiple_sources_"),
        "Detectable raw and manifest tampering": ("test_04_", "test_manifest_metadata_", "test_09_"),
        "Controlled source replacement": ("test_10_", "test_forked_", "test_metadata_only_replacement_"),
        "Backward compatibility or tested migration": ("test_legacy_migration_", "test_all_25_pairs_"),
    }
    for label, prefixes in links.items():
        rows = [row for row in unit["results"] if any(row["test"].split(".")[-1].startswith(p) for p in prefixes)]
        status = "PASS" if len(rows) >= len(prefixes) and all(row["status"] == "PASS" for row in rows) else "FAIL"
        lines.append(f"- {status}: {label}.")
    lines += ["", "## All observed test cases", ""]
    for row in unit["results"]:
        lines.append(f"- {row['status']}: {row['test']}")
    lines += ["", "## Remaining risks and checks not run", ""]
    lines.extend("- " + item for item in report["limits"])
    lines += [
        "- No external URL requests, real-source ingestion, Obsidian visual check, Phase 2 or V2 work was performed.",
        "- Phase 3 uses recoverable metadata publication. Legacy orphan records require human reconciliation; "
        "the tool never truncates committed provenance or automatically removes an existing lock.", "",
        "## Reproduce", "",
        "~~~text", "python -B scripts/validate_source_integrity.py",
        "python -B scripts/check_workspace.py --integrity", "~~~", "",
        "The runner uses standard-library unittest discovery and writes reports only with an explicit new output path.",
        "",
    ]
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
    print(json.dumps({
        "verdict": report["verdict"], "tests_run": report["unit_tests"]["run"],
        "tests_passed": report["unit_tests"]["passed"],
        "live_registered_sources": report["live_registered_sources"],
        "strict_errors": len(report["workspace_errors"]), "warnings": len(report["workspace_warnings"]),
    }, indent=2))
    return 1 if report["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
