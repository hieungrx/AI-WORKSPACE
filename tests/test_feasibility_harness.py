"""Evaluation integrity: gold misses, source cap, bad pointers, fairness and unknowns."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import evaluate_feasibility as evaluation
from tests.workflow_support import Workspace


class FeasibilityHarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix="fixture-feasibility-metrics-", dir=evaluation.ROOT / "tests")
        cls.w = Workspace(Path(cls.directory.name) / "workspace")
        cls.ids = [f"SRC-20261018-{900+n:03d}" for n in range(6)]
        for sid in cls.ids:
            cls.w.register(sid, "TEST_ONLY metric evidence for " + sid)
        cls.w.write("wiki/combined.md", cls.w.page(title="Combined evidence", sources=cls.ids,
                    claims=[(sid, "TEST_ONLY metric evidence.") for sid in cls.ids]))

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def case(self, gold=None):
        return {"case_id": "UNIT", "category": "knowledge", "query": "Combined evidence", "language": "en",
                "relevant_source_ids": self.ids if gold is None else gold, "expected_project_scope": "global"}

    def result(self, pointer="section Evidence", cites=True):
        return {"status": "FOUND", "matches": [{"path": "wiki/combined.md", "scope": "global", "score": 3,
            "usable_as_current_truth": False, "citations": [{"source_id": sid,
                "source_path": f"sources/raw/{sid}.md", "source_pointer": pointer,
                "integrity_status": "MATCH"} for sid in self.ids] if cites else []}], "blocked": []}

    def test_recall_at_five_never_counts_six_sources_from_one_page(self):
        row = evaluation.summarize_trial(self.w, self.case(), "B", self.result(), 0.1)
        self.assertEqual(len(row["retrieved_source_ids_at_5"]), 5)
        self.assertAlmostEqual(row["recall_at_5"], 5 / 6)
        self.assertEqual(row["retrieval_contract"], "MISS")

    def test_blocked_candidate_identity_survives_missing_citations(self):
        result = self.result(cites=False)
        result["blocked"], result["matches"] = result["matches"], []
        result["status"] = "MISSING_EVIDENCE"
        row = evaluation.summarize_trial(self.w, self.case(self.ids[:1]), "B", result, 0.1)
        self.assertEqual(row["recall_at_5"], 1)
        self.assertFalse(row["required_citation_coverage"])
        self.assertEqual(row["citations"], [])

    def test_fake_evidence_pointer_is_not_a_structurally_valid_citation(self):
        for pointer in ("section NoEvidence", "#EvidenceNotPresent", "the evidence elsewhere"):
            with self.subTest(pointer=pointer):
                row = evaluation.summarize_trial(self.w, self.case(), "B", self.result(pointer), 0.1)
                self.assertFalse(any(row["citation_structural_checks"]))

    def test_exact_pointer_and_recorded_bytes_are_valid(self):
        row = evaluation.summarize_trial(self.w, self.case(), "B", self.result(), 0.1)
        self.assertTrue(all(row["citation_structural_checks"]))

    def test_claimed_match_cannot_conceal_actual_raw_tampering(self):
        target = self.w.root / "sources/raw" / (self.ids[0] + ".md")
        before = target.read_bytes()
        try:
            target.write_bytes(before + b"TEST_ONLY tamper\n")
            row = evaluation.summarize_trial(self.w, self.case(), "B", self.result(), 0.1)
            self.assertFalse(row["citation_structural_checks"][0])
        finally:
            target.write_bytes(before)

    def test_gold_miss_is_explicit_and_never_pass(self):
        row = evaluation.summarize_trial(self.w, self.case(), "A", {"status": "NOT_FOUND", "matches": [], "blocked": []}, 0.1)
        self.assertEqual(row["recall_at_5"], 0)
        self.assertEqual(row["retrieval_contract"], "MISS")
        self.assertFalse(row["required_citation_coverage"])

    def test_empty_gold_does_not_create_a_recall_or_answer_score(self):
        row = evaluation.summarize_trial(self.w, self.case([]), "A", {"status": "NOT_FOUND", "matches": [], "blocked": []}, 0.1)
        self.assertIsNone(row["recall_at_5"])
        self.assertEqual(row["retrieval_contract"], "CORRECT_ABSTENTION_SIGNAL")
        self.assertEqual(row["answer_correctness"], "NOT MEASURED")

    def test_unknown_human_cost_and_factual_metrics_are_not_zero_measurements(self):
        values = evaluation.metrics([])
        for name in ("recall_at_5", "API_cost", "token_usage", "human_corrections", "human_review_seconds",
                     "net_productivity", "factual_correctness", "context_continuity_quality"):
            with self.subTest(metric=name):
                self.assertEqual(values[name]["status"], "NOT MEASURED")
                self.assertIsNone(values[name]["value"])

    def test_macro_recall_excludes_zero_gold_and_keeps_actual_misses(self):
        one = evaluation.summarize_trial(self.w, self.case(self.ids[:1]), "B", self.result(), 0.1)
        miss = evaluation.summarize_trial(self.w, self.case(self.ids[:1]), "B", {"status": "NOT_FOUND", "matches": [], "blocked": []}, 0.2)
        empty = evaluation.summarize_trial(self.w, self.case([]), "B", {"status": "NOT_FOUND", "matches": [], "blocked": []}, 0.3)
        result = evaluation.metrics([one, miss, empty])["recall_at_5"]
        self.assertEqual(result["samples"], 2)
        self.assertEqual(result["value"], 0.5)

    def test_raw_baseline_cannot_read_wiki_or_use_wiki_aliases(self):
        packet = [{"source_id": self.ids[0], "title": "Metric evidence", "scope": "global"}]
        original = Path.open
        def guarded(path, *args, **kwargs):
            if path.is_relative_to(self.w.root / "wiki"):
                raise AssertionError("Baseline read maintained wiki")
            return original(path, *args, **kwargs)
        with patch.object(Path, "open", guarded):
            result = evaluation.raw_search(self.w.root, packet, "Metric evidence", "global")
            alias = evaluation.raw_search(self.w.root, packet, "alias absent from raw", "global")
            wrong_scope = evaluation.raw_search(self.w.root, packet, "Metric evidence", "other-project")
        self.assertEqual(result["status"], "FOUND")
        self.assertEqual(alias["status"], "NOT_FOUND")
        self.assertEqual(wrong_scope["status"], "NOT_FOUND")

    def test_counterbalanced_order_is_reproducible_and_balanced(self):
        cases = [{"case_id": str(number)} for number in range(80)]
        order = evaluation.counterbalanced(cases, 1101)
        self.assertEqual(order, evaluation.counterbalanced(cases, 1101))
        self.assertNotEqual(order, evaluation.counterbalanced(cases, 1102))
        self.assertEqual(sum(arms[0] == "A" for _, arms in order), 40)
        self.assertEqual({case["case_id"] for case, _ in order}, {str(n) for n in range(80)})

    def test_dataset_meets_requested_coverage_and_rejects_real_or_duplicate_gold(self):
        data = json.loads(evaluation.DATASET.read_text(encoding="utf-8"))
        coverage = evaluation.validate_dataset(data)
        self.assertEqual(coverage["cases"], 103)
        self.assertEqual(coverage["bilingual_pairs"], 20)
        bad = copy.deepcopy(data)
        bad["synthetic_only"] = False
        with self.assertRaisesRegex(ValueError, "SYNTHETIC"):
            evaluation.validate_dataset(bad)
        bad = copy.deepcopy(data)
        bad["sources"].append(bad["sources"][0])
        with self.assertRaisesRegex(ValueError, "DUPLICATE"):
            evaluation.validate_dataset(bad)
        bad = copy.deepcopy(data)
        bad["cases"][0]["required_citations"] = []
        with self.assertRaisesRegex(ValueError, "GOLD_CITATION"):
            evaluation.validate_dataset(bad)


if __name__ == "__main__":
    unittest.main()
