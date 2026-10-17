"""Scale recipe and operation-local reuse must preserve V1's trust/evidence rules."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts import benchmark_scalability as benchmark
from scripts import check_workspace as lint
from scripts import knowledge_governance as governance
from scripts import query_workspace as query
from scripts import source_integrity as integrity
from scripts import validate_scalability as validator
from workflow_support import Workspace, SID


class ScaleSafetyTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).absolute().parent
        temporary = tempfile.TemporaryDirectory(prefix="fixture-scale-unit-", dir=parent)
        self.addCleanup(temporary.cleanup)
        self.w = Workspace(Path(temporary.name) / "workspace")
        self.root = self.w.root
        self.w.register()
        self.w.apply()
        self.w.apply("wiki/second.md", self.w.page(title="Second protocol"))

    def test_query_reuses_validated_ids_only_within_one_operation(self):
        with patch.object(integrity, "read_registry", wraps=integrity.read_registry) as reads:
            result = query.search(self.root, "Fixture policy", "global")
            self.assertEqual(result["status"], "FOUND")
            self.assertEqual(reads.call_count, 1)
        # A subsequent query must discover the newly introduced unknown reference.
        self.w.write("wiki/unknown.md", self.w.page(title="Unknown source").replace(SID, "SRC-20261018-999"))
        self.assertEqual(query.search(self.root, "Unknown source", "global")["status"], "INVALID_DATA")

    def test_governance_batch_parses_registry_once(self):
        with patch.object(integrity, "read_registry", wraps=integrity.read_registry) as reads:
            result = governance.audit_governance(self.root)
            self.assertEqual(len(result["pages"]), 2)
            self.assertEqual(reads.call_count, 1)
        manifest = self.root / "sources/manifest.csv"
        manifest.write_bytes(manifest.read_bytes().replace(b"synthetic_fixture", b""))
        result = governance.audit_governance(self.root)
        self.assertTrue(result["issues"])
        self.assertEqual(query.search(self.root, "Fixture policy", "global")["status"], "INVALID_DATA")

    def test_registry_metadata_hash_is_not_cached_between_queries(self):
        self.assertEqual(query.search(self.root, "Fixture policy", "global")["status"], "FOUND")
        manifest = self.root / "sources/manifest.csv"
        manifest.write_bytes(manifest.read_bytes().replace(b"Unknown author", b"Altered author"))
        self.assertEqual(query.search(self.root, "Fixture policy", "global")["status"], "INVALID_DATA")

    def test_query_skips_only_the_redundant_reverse_wiki_scan(self):
        with patch.object(integrity, "wiki_relationships", side_effect=AssertionError("reverse scan repeated")):
            self.assertEqual(query.search(self.root, "Fixture policy", "global")["status"], "FOUND")
        full = integrity.audit_sources(self.root)
        self.assertEqual(set(full["source_to_wiki"][SID]), {"wiki/topic.md", "wiki/second.md"})
        source_only = integrity.audit_sources(self.root, include_relationships=False)
        self.assertEqual(source_only["sources"], full["sources"])
        self.assertEqual(source_only["issues"], full["issues"])

    def test_raw_same_size_mtime_edit_remains_detectable(self):
        self.assertEqual(query.search(self.root, "Fixture policy", "global")["status"], "FOUND")
        raw = self.root / ("sources/raw/" + SID + ".md")
        data, attributes = raw.read_bytes(), raw.stat()
        raw.write_bytes(data.replace(b"TEST_ONLY", b"TEST_0NLY", 1))
        import os
        os.utime(raw, ns=(attributes.st_atime_ns, attributes.st_mtime_ns))
        self.assertEqual(query.search(self.root, "Fixture policy", "global")["status"], "MISSING_EVIDENCE")

    def test_10000_source_ids_are_valid_and_unique(self):
        ids = [benchmark.identity(number) for number in range(1, 10001)]
        self.assertEqual(len(set(ids)), 10000)
        self.assertTrue(all(lint.source_id(sid) for sid in ids))

    def test_fixture_root_cannot_target_live_knowledge(self):
        for target in (benchmark.ROOT, benchmark.ROOT / "sources/raw/workspace", benchmark.ROOT / "tests/workspace"):
            with self.subTest(target=str(target)), self.assertRaisesRegex(ValueError, "LOAD_FIXTURE_PATH_REQUIRED"):
                benchmark.fixture_root(target)

    def test_timeout_is_not_a_completed_latency_or_pass(self):
        with patch.object(subprocess, "run", side_effect=subprocess.TimeoutExpired("TEST_ONLY", 5)):
            observed = benchmark.run_child(self.root, "query_en", 0, 5)
        self.assertEqual(observed["status"], "NOT RUN")
        self.assertNotIn("seconds", observed)
        self.assertNotIn("correct", observed)

    def test_measurement_data_cannot_select_files_to_read(self):
        with self.assertRaisesRegex(ValueError, "INVALID_IMPLEMENTATION_MANIFEST"):
            validator.implementation_mismatches({"implementation_sha256": {"../../.env": "TEST_ONLY"}})

    def test_profile_only_results_cannot_claim_full_load_correctness(self):
        measured = {"datasets": [{"setup": {"documents": size},
                     "operations": [{"operation": "profile_query", "status": "MEASURED", "correct": True}],
                     "quality": {"status": "MEASURED", "correct": True}}
                    for size in (100, 1000, 10000)]}
        self.assertFalse(validator.complete_load_probes(measured))

    def test_recipe_and_hierarchical_index_are_reproducible(self):
        parent = Path(__file__).absolute().parent
        hashes = []
        for _ in range(2):
            with tempfile.TemporaryDirectory(prefix="fixture-scale-recipe-", dir=parent) as directory:
                root = Path(directory) / "workspace"
                setup = benchmark.build_fixture(root, 3)
                hashes.append(setup["corpus_sha256"])
                issues = lint.check_workspace(root, integrity=True, security=True)
                self.assertFalse(any(issue.startswith("ERROR ") for issue in issues), issues)
                self.assertEqual(len(integrity.read_registry(root)), 3)
                self.assertEqual(json.loads((root / "fixture.json").read_text())["recipe"], benchmark.RECIPE)
        self.assertEqual(hashes[0], hashes[1])
