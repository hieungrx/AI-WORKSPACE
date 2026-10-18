"""Synthetic V1.1 maintenance rehearsal; never create human approval records."""
from pathlib import Path
import tempfile
import unittest

from scripts.feasibility_evolution import (
    evaluate_evolution, _preservation_checks, SOURCE_A, SOURCE_B, PAGE, UNRELATED_PAGE,
)


class FeasibilityEvolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="fixture-feasibility-unit-",
                                                    dir=Path(__file__).absolute().parent)
        cls.directory = Path(cls.temporary.name)
        cls.result = evaluate_evolution(cls.directory / "evolution")

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_actual_admission_conflict_rollback_retry_and_fresh_reader(self):
        result = self.result
        self.assertTrue(result["passed"], result["failures"])
        self.assertTrue(result["checks"]["failed_existing_update_exact_rollback"])
        self.assertTrue(result["checks"]["conflict_query_disputed_with_both_references"])
        self.assertEqual(result["human_approvals_created"], 0)
        self.assertIsNone(result["human_review_time_seconds"])
        self.assertTrue(all(value >= 0 for value in result["maintenance_elapsed_seconds"].values()))
        fresh = result["subprocess_continuity"]
        self.assertEqual(fresh["exit_code"], 0)
        self.assertEqual(fresh["output"]["status"], "DISPUTED")
        self.assertEqual({citation["source_id"] for citation in fresh["output"]["blocked"][0]["citations"]},
                         {SOURCE_A, SOURCE_B})
        self.assertFalse(fresh["conversation_history_supplied"])
        self.assertTrue(fresh["read_only"])
        self.assertIn(PAGE, result["final_snapshot_hashes"])

    def test_preservation_check_detects_unrelated_mutation(self):
        root = Path(self.result["workspace_path"])
        path = root / UNRELATED_PAGE
        before = path.read_bytes()
        try:
            path.write_bytes(before + b"\nUNKNOWN: TEST_ONLY unauthorized unrelated edit.\n")
            actual = _preservation_checks(root, self.result["preservation_baseline"])
            self.assertFalse(actual[UNRELATED_PAGE])
            self.assertFalse(all(actual.values()))
        finally:
            path.write_bytes(before)

    def test_refuses_live_or_nonempty_fixture_target(self):
        with self.assertRaisesRegex(ValueError, "DISPOSABLE_FEASIBILITY_DIRECTORY_REQUIRED"):
            evaluate_evolution(Path(__file__).absolute().parents[1] / "wiki")
        with self.assertRaisesRegex(FileExistsError, "EMPTY_FEASIBILITY_DIRECTORY_REQUIRED"):
            evaluate_evolution(self.directory / "evolution")


if __name__ == "__main__":
    unittest.main()
