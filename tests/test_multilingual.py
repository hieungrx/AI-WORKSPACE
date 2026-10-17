"""Multilingual readiness tests; all corpus mutations stay in disposable fixtures."""
import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unicodedata
import unittest
from unittest.mock import patch

from scripts import check_workspace as checker
from scripts import query_workspace as query
from scripts import validate_multilingual as validation


class MultilingualTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).absolute().parent
        temporary = tempfile.TemporaryDirectory(prefix="fixture-language-", dir=parent)
        if not Path(temporary.name).absolute().is_relative_to(parent):
            raise AssertionError("temporary fixture escaped tests/")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "workspace"
        shutil.copytree(validation.FIXTURES, self.root)

    def replace(self, relative, old, new):
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def test_all_25_pairs_have_observed_results(self):
        report = validation.evaluate()
        self.assertGreaterEqual(report["pairs"], 20)
        self.assertEqual(report["queries"], report["pairs"] * 2)
        for row in report["results"]:
            with self.subTest(pair=row["pair_id"], language=row["language"]):
                self.assertTrue(row["passed"], row["actual"])
        self.assertEqual(set(report["categories"]), {
            "exact_keyword", "bilingual_aliases", "cross_language", "project_scope", "missing_evidence",
        })

    def test_old_metadata_defaults_and_legacy_retrieval(self):
        fields = checker.multilingual_metadata({})
        self.assertEqual(fields, {"language": "und", "title_vi": "", "keywords": [], "aliases_vi": []})
        result = query.search(self.root, "Giải thích Legacy checksum", "unscoped")
        self.assertEqual(result["status"], "FOUND")
        self.assertEqual(result["matches"][0]["language"], "und")

    def test_underscored_fields_are_parsed(self):
        text = '# Title\n- **title_vi:** Đặt trước\n- **aliases_vi:** ["giữ món"]\n## Summary\n'
        meta = checker.metadata(text)
        self.assertEqual(meta["title_vi"], "Đặt trước")
        self.assertEqual(checker.multilingual_metadata(meta)["aliases_vi"], ["giữ món"])

    def test_optional_metadata_rejects_invalid_types_and_duplicates(self):
        for fields in (
            {"language": "automatic"}, {"keywords": "not JSON"},
            {"keywords": '"keyword"'}, {"aliases_vi": '{"alias":1}'},
            {"keywords": '[null]'}, {"aliases_vi": '[""]'},
            {"keywords": '["API", "API"]'},
        ):
            with self.subTest(fields=fields):
                with self.assertRaises(ValueError):
                    checker.multilingual_metadata(fields)

    def test_linter_and_search_reject_bad_metadata(self):
        self.replace("wiki/cache.md", '["vô hiệu hóa bộ nhớ đệm"]', '"vô hiệu hóa bộ nhớ đệm"')
        issues = checker.check_workspace(self.root)
        self.assertTrue(any("INVALID_MULTILINGUAL_METADATA" in item for item in issues))
        self.assertEqual(query.search(self.root, "cache invalidation", "demo-a")["status"], "INVALID_DATA")

    def test_scope_is_required_and_never_inferred(self):
        for scope in ("", None):
            with self.subTest(scope=scope):
                result = query.search(self.root, "request timeout", scope)
                self.assertEqual(result["status"], "INVALID_QUERY")
                self.assertEqual(result["matches"], [])
        self.assertEqual(query.search(self.root, "request timeout", "demo-c")["status"], "NOT_FOUND")

    def test_aliases_do_not_leak_from_another_project(self):
        a = query.search(self.root, "đổi kích thước ảnh", "demo-a")
        b = query.search(self.root, "đổi kích thước ảnh", "demo-b")
        self.assertEqual(a["status"], "NOT_FOUND")
        self.assertEqual(a["expanded_terms"], [])
        self.assertEqual(b["status"], "FOUND")
        self.assertEqual(b["matches"][0]["path"], "wiki/image-b.md")

    def test_other_project_bad_metadata_does_not_change_selected_scope(self):
        self.replace("wiki/timeout-b.md", '["thời gian chờ"]', "invalid JSON")
        result = query.search(self.root, "thời gian chờ", "demo-a")
        self.assertEqual(result["status"], "FOUND")
        self.assertEqual(result["matches"][0]["path"], "wiki/timeout-a.md")

    def test_alias_and_vietnamese_title_add_only_declared_english_terms(self):
        result = query.search(self.root, "Chính sách thử lại", "demo-a")
        self.assertEqual(result["status"], "FOUND")
        self.assertIn("title_vi", result["matches"][0]["matched_fields"])
        self.assertEqual(result["expanded_terms"], ["retry policy"])
        self.assertEqual(result["query"], "Chính sách thử lại")

    def test_unicode_nfc_nfd_case_and_spacing_match(self):
        original = "  XỬ LÝ   BẾ TẮC THẾ NÀO? "
        result = query.search(self.root, unicodedata.normalize("NFD", original), "demo-a")
        self.assertEqual(result["status"], "FOUND")
        self.assertEqual(result["matches"][0]["path"], "wiki/deadlock.md")
        self.assertEqual(result["query"], unicodedata.normalize("NFD", original))

    def test_accents_are_not_silently_removed_or_synonyms_invented(self):
        for text in ("be tac", "kẹt cứng các tiến trình"):
            with self.subTest(text=text):
                result = query.search(self.root, text, "demo-a")
                self.assertEqual(result["status"], "NOT_FOUND")
                self.assertEqual(result["expanded_terms"], [])

    def test_identifiers_routes_and_filenames_retain_original_spelling(self):
        for term in ("GET /api/listings", "reserveListing()", "checkout.service.ts", "SELECT FOR UPDATE", "HTTP 409"):
            with self.subTest(term=term):
                original = "Giải thích " + term
                result = query.search(self.root, original, "demo-a")
                self.assertEqual(result["status"], "FOUND")
                self.assertEqual(result["query"], original)
                self.assertIn(term, result["matches"][0]["matched_terms"])
        for wrong in ("GET /api/listingsExtra", "checkoutXserviceYts", "reserveListingX"):
            with self.subTest(wrong=wrong):
                self.assertEqual(query.search(self.root, wrong, "demo-a")["status"], "NOT_FOUND")

    def test_punctuation_bearing_technical_keywords_are_literal(self):
        self.replace("wiki/cache.md", '["cache invalidation"]', '["C++"]')
        self.assertEqual(query.search(self.root, "C++", "demo-a")["status"], "FOUND")
        self.assertEqual(query.search(self.root, "C#", "demo-a")["status"], "NOT_FOUND")

    def test_ambiguous_alias_does_not_pick_an_arbitrary_document(self):
        self.replace("wiki/retry.md", '["thử lại", "gửi lại yêu cầu"]', '["phân trang"]')
        result = query.search(self.root, "phân trang", "demo-a")
        self.assertEqual(result["status"], "AMBIGUOUS")
        self.assertEqual(len(result["matches"]), 2)

    def test_missing_evidence_is_not_a_source_backed_answer(self):
        for term in ("payout reconciliation", "refund tracing", "dispute handoff", "audit export"):
            with self.subTest(term=term):
                result = query.search(self.root, term, "demo-a")
                self.assertEqual(result["status"], "MISSING_EVIDENCE")
                self.assertEqual(result["matches"], [])
                self.assertEqual(result["blocked"][0]["citations"], [])
                self.assertIn("UNKNOWN", result["message"])

    def test_raw_bodies_are_not_opened_and_network_is_not_used(self):
        original_open = Path.open

        def guarded(path, *args, **kwargs):
            if path.is_relative_to(self.root / "sources/raw"):
                raise AssertionError("raw body accessed")
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "open", guarded), patch("socket.create_connection", side_effect=AssertionError("network")):
            self.assertEqual(query.search(self.root, "đăng nhập", "demo-a")["status"], "FOUND")

    def test_invalid_registry_fails_closed(self):
        manifest = self.root / "sources/manifest.csv"
        with manifest.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        with manifest.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=checker.MANIFEST_FIELDS)
            writer.writeheader()
            writer.writerows(rows + [rows[0]])
        result = query.search(self.root, "authentication", "demo-a")
        self.assertEqual(result["status"], "INVALID_DATA")
        self.assertEqual(result["matches"], [])

    def test_search_does_not_write_or_translate_any_file(self):
        def snapshot():
            return {p.relative_to(self.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in self.root.rglob("*") if p.is_file()}
        before = snapshot()
        for text in ("đăng nhập", "authentication", "không có tài liệu"):
            query.search(self.root, text, "demo-a")
        self.assertEqual(snapshot(), before)

    def test_report_writer_rejects_existing_or_protected_paths(self):
        for output in (Path("README.md"), Path("sources/raw/report.json"), Path("../report.json")):
            with self.subTest(output=output):
                with self.assertRaises((ValueError, FileExistsError)):
                    validation.save_report({}, output)
        target = self.root / "reports/existing.json"
        target.parent.mkdir()
        target.write_text("existing report", encoding="utf-8")
        with patch.object(validation, "ROOT", self.root):
            with self.assertRaises(FileExistsError):
                validation.save_report({}, Path("reports/existing.json"))
        self.assertEqual(target.read_text(encoding="utf-8"), "existing report")


if __name__ == "__main__":
    unittest.main()
