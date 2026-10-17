"""Phase 4 actual Ingest -> Query -> Lint paths, entirely TEST_ONLY."""
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from scripts import check_workspace as lint
from scripts import ingest_workspace as ingest
from scripts import knowledge_governance as governance
from scripts import query_workspace as query
from scripts import safe_operations as operations
from scripts import source_integrity as integrity
from workflow_benchmark import run_benchmark
from workflow_support import Workspace, DAY, SID

BENCHMARK_OBSERVATION = {}
WORKFLOW_OBSERVATIONS = []
LINT_OBSERVATIONS = []


class SimulatedInterruption(BaseException):
    pass


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).absolute().parent
        temporary = tempfile.TemporaryDirectory(prefix="fixture-workflow-", dir=parent)
        self.addCleanup(temporary.cleanup)
        self.w = Workspace(Path(temporary.name) / "workspace")
        self.root = self.w.root
        self.row = self.w.register()

    def test_ingest_cannot_reset_verified_knowledge_to_draft(self):
        self.w.apply()
        self.w.verify("wiki/topic.md")
        changes, expected = self.w.plan(text=self.w.page().replace("synthetic policy.", "changed policy."))
        before = self.w.snapshot()
        with self.assertRaisesRegex(ValueError, "PROTECTED_KNOWLEDGE_UPDATE"):
            ingest.ingest_registered(self.root, SID, changes, expected, scope="global", authorized=True, apply=True)
        self.assertEqual(self.w.snapshot(), before)

    def test_identical_ingest_retry_is_a_read_only_noop(self):
        changes, expected = self.w.plan()
        first = ingest.ingest_registered(self.root, SID, changes, expected, scope="global", authorized=True, apply=True)
        before, token = self.w.snapshot(), operations.read_version(self.root)
        retry = ingest.ingest_registered(self.root, SID, changes, expected, scope="global", authorized=True, apply=True)
        self.assertEqual(first["status"], "COMMITTED")
        self.assertEqual(retry["status"], "UNCHANGED")
        self.assertEqual(self.w.snapshot(), before)
        self.assertEqual(operations.read_version(self.root), token)

    def test_lint_rejects_a_source_id_without_an_exact_pointer(self):
        self.w.write("wiki/topic.md", self.w.page().replace(", section Evidence]", "]"))
        codes = {item.split()[1] for item in lint.check_workspace(self.root, integrity=True)}
        self.assertIn("MISSING_CITATION_POINTER", codes)
        self.assertEqual(query.search(self.root, "Fixture policy", "global")["status"], "MISSING_EVIDENCE")

    def test_01_registration_provenance_ingest_query_lint(self):
        raw_before = (self.root / self.row["source_url_or_path"]).read_bytes()
        applied = self.w.apply()
        audit = integrity.audit_sources(self.root)
        result = query.search(self.root, "Fixture policy", "global")
        issues = lint.check_workspace(self.root, integrity=True, security=True)
        self.assertEqual(applied["status"], "COMMITTED")
        self.assertEqual(result["status"], "FOUND")
        self.assertEqual(result["matches"][0]["citations"][0]["source_id"], SID)
        self.assertEqual(audit["sources"][SID]["integrity_status"], "MATCH")
        self.assertIsNone(audit["sources"][SID]["author"])
        self.assertIsNone(audit["sources"][SID]["published_at"])
        self.assertIn("wiki/topic.md", audit["source_to_wiki"][SID])
        self.assertFalse(any(issue.startswith("ERROR ") for issue in issues), issues)
        self.assertEqual(raw_before, (self.root / self.row["source_url_or_path"]).read_bytes())
        WORKFLOW_OBSERVATIONS.append({"scenario": "register_ingest_query_lint", "source_integrity": "MATCH",
                                      "query_status": result["status"], "lint_issues": issues})

    def test_02_duplicate_registration_reuses_identity_and_bytes(self):
        before = self.w.snapshot()
        for row in (self.row, {**self.row, "source_id": "SRC-20261018-599"}):
            actual = integrity.register_source(self.root, row, authorized=True, language="en")
            self.assertEqual(actual, {"status": "DUPLICATE", "source_id": SID})
        self.assertEqual(len(integrity.read_registry(self.root)), 1)
        self.assertEqual(self.w.snapshot(), before)
        WORKFLOW_OBSERVATIONS.append({"scenario": "duplicate_admission", "attempts": 2,
                                      "new_registry_entries": 0, "raw_unchanged": True})

    def test_03_fresh_plan_for_identical_content_does_not_duplicate_log(self):
        self.w.apply()
        before = self.w.snapshot()
        actual = self.w.apply()
        self.assertEqual(actual["status"], "UNCHANGED")
        self.assertEqual(self.w.snapshot(), before)

    def test_04_existing_draft_update_retains_old_evidence(self):
        self.w.apply()
        before = self.w.snapshot()
        updated = self.w.page() + "\n- FACT: TEST_ONLY second observation. [" + SID + ", section Evidence]\n"
        self.assertEqual(self.w.apply(text=updated)["status"], "COMMITTED")
        after = self.w.snapshot()
        changed = {path for path in before if before[path] != after[path]}
        self.assertEqual(changed, {"wiki/topic.md", "wiki/log.md"})
        self.assertEqual(query.search(self.root, "Fixture policy", "global")["status"], "FOUND")
        self.assertFalse(any(issue.startswith("ERROR ") for issue in lint.check_workspace(self.root, integrity=True)))
        WORKFLOW_OBSERVATIONS.append({"scenario": "draft_update", "changed_paths": sorted(changed),
                                      "existing_citation_retained": True})

    def test_05_bounded_wiki_transaction_cannot_bypass_verified_guard(self):
        self.w.apply()
        self.w.verify("wiki/topic.md")
        changes, expected = self.w.plan()
        before = self.w.snapshot()
        with self.assertRaisesRegex(ValueError, "PROTECTED_KNOWLEDGE_UPDATE"):
            operations.transact(self.root, changes, expected, authorized=True)
        self.assertEqual(self.w.snapshot(), before)

    def test_06_scope_and_transition_history_cannot_be_reset_by_ingest(self):
        self.w.apply()
        self.w.move("wiki/topic.md", "unverified")
        self.w.move("wiki/topic.md", "draft")
        before = self.w.snapshot()
        with self.assertRaisesRegex(ValueError, "LIFECYCLE_CHANGE_REQUIRES_TRANSITION"):
            self.w.apply()
        self.assertEqual(self.w.snapshot(), before)

    def test_lifecycle_operation_cannot_reset_verified_history(self):
        self.w.apply()
        self.w.verify("wiki/topic.md")
        relative = "wiki/topic.md"
        before = self.w.snapshot()
        with self.assertRaisesRegex(ValueError, "INVALID_LIFECYCLE_UPDATE"):
            operations.transact(self.root, {relative: self.w.page().encode()},
                                operations.versions(self.root, [relative], operation="lifecycle"),
                                operation="lifecycle", authorized=True)
        self.assertEqual(self.w.snapshot(), before)

    def test_07_conflicting_information_and_pointers_are_preserved(self):
        other = "SRC-20261018-502"
        self.w.register(other, "TEST_ONLY: another observation disagrees with the first.")
        conflicts = [{"summary": "TEST_ONLY incompatible observations", "source_ids": [SID, other], "resolution": None}]
        text = self.w.page(sources=(SID, other), conflicts=json.dumps(conflicts),
                           claims=[(SID, "TEST_ONLY observation A."), (other, "TEST_ONLY observation B.")])
        self.w.apply(text=text)
        before = self.w.snapshot()
        removed_conflict = governance.replace_field(text, "conflicts", "[]")
        with self.assertRaisesRegex(ValueError, "CONFLICT_REMOVAL_REQUIRES_REVIEW"):
            self.w.apply(text=removed_conflict)
        with self.assertRaisesRegex(ValueError, "EVIDENCE_REMOVAL_REQUIRES_REVIEW"):
            self.w.apply(text=self.w.page())
        self.assertEqual(self.w.snapshot(), before)
        actual = query.search(self.root, "Fixture policy", "global")
        self.assertEqual(actual["status"], "DISPUTED")
        self.assertEqual({cite["source_id"] for cite in actual["blocked"][0]["citations"]}, {SID, other})
        WORKFLOW_OBSERVATIONS.append({"scenario": "conflict_preservation", "observed_status": actual["status"],
                                      "preserved_source_ids": [SID, other]})

    def test_08_missing_index_and_missing_log_are_rejected_before_write(self):
        changes, expected = self.w.plan()
        before = self.w.snapshot()
        for target, code in (("wiki/index.md", "MISSING_INDEX_ENTRY"), ("wiki/log.md", "MISSING_CHANGE_LOG_ENTRY")):
            with self.subTest(target=target):
                invalid = {**changes, target: (self.root / target).read_bytes()}
                with self.assertRaisesRegex(ValueError, code):
                    ingest.ingest_registered(self.root, SID, invalid, expected, scope="global", authorized=True, apply=True)
                self.assertEqual(self.w.snapshot(), before)

    def test_09_ingest_cannot_remove_existing_index_links(self):
        self.w.apply()
        changes, expected = self.w.plan("wiki/second.md")
        changes["wiki/index.md"] = b"# TEST_ONLY index\n[Second](second.md)\n"
        before = self.w.snapshot()
        with self.assertRaisesRegex(ValueError, "INDEX_REMOVAL_REQUIRES_REVIEW"):
            ingest.ingest_registered(self.root, SID, changes, expected, scope="global", authorized=True, apply=True)
        self.assertEqual(self.w.snapshot(), before)

    def failure_after_one_write(self, exception):
        original = operations._replace_file
        writes = 0
        def replace(staged, target):
            nonlocal writes
            if staged.suffix == ".after":
                writes += 1
                if writes == 2:
                    raise exception
            return original(staged, target)
        return replace

    def test_10_failed_ingest_rolls_back_and_retry_succeeds(self):
        changes, expected = self.w.plan()
        before = self.w.snapshot()
        with patch.object(operations, "_replace_file", self.failure_after_one_write(OSError("TEST_ONLY_WRITE_FAILURE"))):
            with self.assertRaisesRegex(OSError, "TEST_ONLY_WRITE_FAILURE"):
                ingest.ingest_registered(self.root, SID, changes, expected, scope="global", authorized=True, apply=True)
        self.assertEqual(self.w.snapshot(), before)
        self.assertEqual(len(integrity.read_registry(self.root)), 1)
        self.assertEqual(query.search(self.root, "Fixture policy", "global")["status"], "NOT_FOUND")
        actual = ingest.ingest_registered(self.root, SID, changes, expected, scope="global", authorized=True, apply=True)
        self.assertEqual(actual["status"], "COMMITTED")
        self.assertEqual(query.search(self.root, "Fixture policy", "global")["status"], "FOUND")
        WORKFLOW_OBSERVATIONS.append({"scenario": "write_failure_and_retry", "injected_error": "TEST_ONLY_WRITE_FAILURE",
                                      "rollback_hashes": before, "exact_rollback_observed": True, "retry": actual["status"]})

    def test_11_interrupted_ingest_requires_recovery_then_retry(self):
        changes, expected = self.w.plan()
        before = self.w.snapshot()
        with patch.object(operations, "_replace_file", self.failure_after_one_write(SimulatedInterruption())):
            with self.assertRaises(SimulatedInterruption):
                ingest.ingest_registered(self.root, SID, changes, expected, scope="global", authorized=True, apply=True)
        blocked = query.search(self.root, "Fixture policy", "global")
        self.assertEqual(blocked["status"], "RECOVERY_REQUIRED")
        recovered = operations.recover(self.root, authorized=True)
        self.assertEqual(recovered["status"], "ROLLED_BACK")
        after = self.w.snapshot()
        self.assertEqual(after, before)
        retry = ingest.ingest_registered(self.root, SID, changes, expected, scope="global", authorized=True, apply=True)
        self.assertEqual(retry["status"], "COMMITTED")
        WORKFLOW_OBSERVATIONS.append({"scenario": "interruption_recovery_and_retry", "query_during_recovery": blocked["status"],
                                      "recovery_status": recovered["status"], "before_hashes": before,
                                      "after_hashes": after, "retry_status": retry["status"]})

    def test_12_stale_update_does_not_overwrite_newer_user_work(self):
        self.w.apply()
        proposed = self.w.page() + "\n## Next questions\nUNKNOWN: TEST_ONLY queued update.\n"
        changes, expected = self.w.plan(text=proposed)
        target = self.root / "wiki/topic.md"
        target.write_bytes(target.read_bytes() + b"\n## Next questions\nUNKNOWN: TEST_ONLY newer user note.\n")
        before = self.w.snapshot()
        with self.assertRaisesRegex(ValueError, "CONCURRENT_CHANGE"):
            ingest.ingest_registered(self.root, SID, changes, expected, scope="global", authorized=True, apply=True)
        self.assertEqual(self.w.snapshot(), before)

    def test_13_invalid_citation_plan_does_not_leave_partial_files(self):
        changes, expected = self.w.plan(text=self.w.page().replace(", section Evidence]", "]"))
        before = self.w.snapshot()
        with self.assertRaisesRegex(ValueError, "MISSING_CITATION_POINTER"):
            ingest.ingest_registered(self.root, SID, changes, expected, scope="global", authorized=True, apply=True)
        self.assertEqual(self.w.snapshot(), before)

    def fault(self, code):
        issues = lint.check_workspace(self.root, integrity=True)
        LINT_OBSERVATIONS.append({"expected_code": code, "observed_issues": issues})
        self.assertIn(code, {issue.split()[1] for issue in issues}, issues)

    def test_lint_broken_markdown_link(self):
        self.w.apply(text=self.w.page())
        target = self.root / "wiki/topic.md"
        target.write_bytes(target.read_bytes() + b"\n[Broken](absent.md)\n")
        self.fault("BROKEN_LINK")

    def test_lint_missing_source_reference(self):
        self.w.write("wiki/topic.md", self.w.page().replace(SID, "SRC-20261018-999"))
        self.fault("UNKNOWN_SOURCE")

    def test_lint_orphan_and_missing_index_entry(self):
        self.w.write("wiki/topic.md", self.w.page())
        self.fault("ORPHAN_PAGE")

    def test_lint_duplicate_page_identity(self):
        text = self.w.page(page_id="fixture.topic")
        self.w.write("wiki/topic.md", text)
        self.w.write("wiki/other.md", text)
        self.fault("DUPLICATE_PAGE_ID")
        self.assertEqual(query.search(self.root, "Fixture policy", "global")["status"], "INVALID_DATA")

    def test_lint_invalid_frontmatter_does_not_ignore_yaml(self):
        self.w.write("wiki/topic.md", "---\nstatus: [\n---\n" + self.w.page())
        self.fault("UNSUPPORTED_FRONTMATTER")
        self.assertEqual(query.search(self.root, "Fixture policy", "global")["status"], "INVALID_DATA")

    def test_lint_invalid_lifecycle_transition(self):
        self.w.write("wiki/topic.md", governance.replace_field(self.w.page(), "Status", "verified"))
        self.fault("UNTRACED_STATE")

    def test_lint_contradictory_current_decision_slots_require_review(self):
        for name, claim in (("first", "TEST_ONLY use red channel."), ("second", "TEST_ONLY use blue channel.")):
            relative = "decisions/" + name + ".md"
            self.w.write(relative, self.w.page(title=name, kind="approved_decision", temporal="current",
                                              decision_key="channel", review_after="2099-12-31", claims=[(SID, claim)]))
            self.w.verify(relative)
        self.fault("CURRENT_DECISION_COLLISION")
        self.assertEqual(query.search(self.root, "first", "global")["status"], "INVALID_DATA")

    def test_lint_unreviewed_knowledge_is_not_verified(self):
        self.w.apply()
        self.fault("UNREVIEWED_KNOWLEDGE")
        self.assertFalse(query.search(self.root, "Fixture policy", "global")["matches"][0]["usable_as_current_truth"])

    def test_lint_potentially_stale_does_not_change_status(self):
        text = self.w.page(created_at="2000-01-01", updated_at="2000-01-01", temporal="current", review_after="2001-01-01")
        target = self.w.write("wiki/topic.md", text)
        before = target.read_bytes()
        self.fault("REVIEW_DUE")
        self.assertEqual(target.read_bytes(), before)
        historical = governance.replace_field(text, "temporal", "historical")
        historical = historical.replace("- review_after: 2001-01-01\n", "")
        self.w.write("wiki/topic.md", historical)
        self.assertNotIn("REVIEW_DUE", {issue.split()[1] for issue in lint.check_workspace(self.root)})

    def test_lint_duplicate_index_target(self):
        self.w.apply()
        index = self.root / "wiki/index.md"
        index.write_bytes(index.read_bytes() + b"[Duplicate label](./topic.md)\n")
        self.fault("DUPLICATE_INDEX_ENTRY")


class BenchmarkTests(unittest.TestCase):
    def test_independent_corpus_and_thirty_query_pairs(self):
        parent = Path(__file__).absolute().parent
        with tempfile.TemporaryDirectory(prefix="fixture-workflow-benchmark-", dir=parent) as directory:
            observed = run_benchmark(Workspace(Path(directory) / "workspace"))
        BENCHMARK_OBSERVATION.clear()
        BENCHMARK_OBSERVATION.update(observed)
        self.assertGreaterEqual(observed["pairs"], 20)
        self.assertEqual(observed["unexpected_failures"], [],
                         [(row["pair"], row["language"], row["mismatches"], row["actual"]["status"])
                          for row in observed["unexpected_failures"]])
        self.assertTrue(observed["query_and_lint_read_only"])
        self.assertFalse(any(issue.startswith("ERROR ") for issue in observed["lint_issues"]), observed["lint_issues"])
        for metric in ("cross_project_leakage", "duplicate_ingestion_rate", "workflow_failure_rate"):
            self.assertEqual(observed["metrics"][metric]["numerator"], 0, observed["metrics"][metric])
        self.assertTrue(all(row["valid"] for row in observed["citation_checks"]))
