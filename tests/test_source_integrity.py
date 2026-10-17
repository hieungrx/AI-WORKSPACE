"""Synthetic Phase 1 tests. External corruption is simulated only in temp fixtures."""
import csv
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import check_workspace as checker
from scripts import query_workspace as query
from scripts import source_integrity as integrity

SID1 = "SRC-20261017-201"
SID2 = "SRC-20261017-202"
SID3 = "SRC-20261017-203"


class SourceIntegrityTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).absolute().parent
        temporary = tempfile.TemporaryDirectory(prefix="fixture-provenance-", dir=parent)
        if not Path(temporary.name).absolute().is_relative_to(parent):
            raise AssertionError("unsafe fixture path")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "workspace"
        self.root.mkdir()
        self.write("sources/manifest.csv", ",".join(checker.MANIFEST_FIELDS) + "\n")
        self.write("wiki/index.md", "# Index\n[Fixture](fixture.md)\n")
        self.write("wiki/log.md", "# Synthetic log\n")
        self.wiki([])

    def write(self, location, text):
        target = self.root / location
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def row(self, sid=SID1, filename="one.md"):
        return dict(zip(checker.MANIFEST_FIELDS, (
            sid, "TEST_ONLY synthetic source", "synthetic_fixture", "sources/raw/" + filename,
            "", "", "2026-10-17", "Synthetic test fixture", "Author and publication date unknown.",
        )))

    def snapshot(self, row, data=b"TEST_ONLY original bytes\n"):
        integrity.create_raw_snapshot(self.root, row["source_url_or_path"], data, authorized=True)

    def register(self, row=None, data=b"TEST_ONLY original bytes\n", **values):
        row = row or self.row()
        self.snapshot(row, data)
        integrity.register_source(self.root, row, authorized=True, **values)
        return row

    def wiki(self, ids):
        source_ids = ", ".join(ids) or "None"
        citations = " ".join("[" + sid + ", section 1]" for sid in ids)
        text = (
            "# Fixture claim\n- **Status:** DRAFT\n- **Updated:** 2026-10-17\n"
            "- **Source IDs:** " + source_ids + "\n- **Scope:** demo\n\n## Summary\n"
            "UNKNOWN: synthetic fixture only.\n\n## Verified findings\n"
        )
        if ids:
            text += "- FACT: TEST_ONLY claim. " + citations + "\n"
        self.write("wiki/fixture.md", text)

    def append_row(self, row):
        with (self.root / "sources/manifest.csv").open("a", encoding="utf-8", newline="") as handle:
            csv.DictWriter(handle, fieldnames=checker.MANIFEST_FIELDS, lineterminator="\n").writerow(row)

    def append_entry(self, entry):
        with (self.root / integrity.LEDGER).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")

    def errors(self):
        return {item.split()[1] for item in integrity.audit_sources(self.root)["issues"] if item.startswith("ERROR ")}

    def metadata_bytes(self):
        return {p: (self.root / p).read_bytes() if (self.root / p).exists() else None
                for p in ("sources/manifest.csv", integrity.LEDGER)}

    def test_01_valid_registration_and_unknown_metadata(self):
        original = self.metadata_bytes()["sources/manifest.csv"]
        self.register(language="en")
        self.wiki([SID1])
        audit = integrity.audit_sources(self.root)
        record = audit["sources"][SID1]
        self.assertEqual(self.errors(), set())
        self.assertEqual(record["integrity_status"], "MATCH")
        self.assertIsNone(record["author"])
        self.assertIsNone(record["publisher"])
        self.assertIsNone(record["published_at"])
        self.assertIsNone(record["source_uri"])
        self.assertEqual(record["verification_status"], "UNVERIFIED")
        self.assertEqual(record["content_hash"], "sha256:" + hashlib.sha256(b"TEST_ONLY original bytes\n").hexdigest())
        self.assertTrue(self.metadata_bytes()["sources/manifest.csv"].startswith(original))
        self.assertEqual(audit["source_to_wiki"][SID1], ["wiki/fixture.md"])
        self.assertEqual(query.search(self.root, "Fixture claim", "demo")["matches"][0]["citations"][0]["integrity_status"], "MATCH")

    def test_02_duplicate_ingestion_is_idempotent_and_content_deduplicated(self):
        row = self.register()
        before = self.metadata_bytes()
        self.assertEqual(integrity.register_source(self.root, row, authorized=True),
                         {"status": "DUPLICATE", "source_id": SID1})
        duplicate = self.row(SID2, "duplicate.md")
        self.snapshot(duplicate)
        self.assertEqual(integrity.register_source(self.root, duplicate, authorized=True),
                         {"status": "DUPLICATE", "source_id": SID1})
        self.assertEqual(self.metadata_bytes(), before)
        self.assertTrue((self.root / duplicate["source_url_or_path"]).exists())

    def test_03_duplicate_id_with_different_content_is_rejected(self):
        self.register()
        before = self.metadata_bytes()
        other = self.row(SID1, "different.md")
        self.snapshot(other, b"TEST_ONLY different content")
        with self.assertRaisesRegex(integrity.IntegrityError, "SOURCE_ID_CONFLICT"):
            integrity.register_source(self.root, other, authorized=True)
        self.assertEqual(self.metadata_bytes(), before)
        self.assertEqual((self.root / "sources/raw/one.md").read_bytes(), b"TEST_ONLY original bytes\n")

    def test_04_hash_mismatch_blocks_source_and_query(self):
        self.register()
        self.wiki([SID1])
        # Simulated external tampering; normal maintenance APIs never do this.
        (self.root / "sources/raw/one.md").write_bytes(b"TEST_ONLY corrupted bytes")
        self.assertIn("HASH_MISMATCH", self.errors())
        self.assertTrue(any("HASH_MISMATCH" in item for item in checker.check_workspace(self.root, integrity=True)))
        result = query.search(self.root, "Fixture claim", "demo")
        self.assertEqual(result["status"], "MISSING_EVIDENCE")
        self.assertEqual(result["matches"], [])

    def test_05_missing_source_file_is_detected(self):
        self.register()
        self.wiki([SID1])
        (self.root / "sources/raw/one.md").unlink()  # Synthetic loss only.
        self.assertIn("SOURCE_UNAVAILABLE", self.errors())
        self.assertEqual(query.search(self.root, "Fixture claim", "demo")["status"], "MISSING_EVIDENCE")

    def test_06_invalid_wiki_reference_is_detected(self):
        self.wiki([SID1])
        self.assertIn("UNKNOWN_SOURCE_REFERENCE", self.errors())
        self.assertTrue(any("UNKNOWN_SOURCE" in issue for issue in checker.check_workspace(self.root, integrity=True)))

    def test_07_missing_required_metadata_is_rejected_before_writes(self):
        row = self.row()
        self.snapshot(row)
        before = self.metadata_bytes()
        for field in checker.REQUIRED_FIELDS:
            with self.subTest(field=field):
                invalid = dict(row, **{field: ""})
                with self.assertRaisesRegex(integrity.IntegrityError, "MISSING_SOURCE_VALUE"):
                    integrity.register_source(self.root, invalid, authorized=True)
        self.assertEqual(self.metadata_bytes(), before)

    def test_08_unavailable_original_url_retains_local_evidence_without_network(self):
        with patch("socket.create_connection", side_effect=AssertionError("network")):
            self.register(source_uri="https://example.invalid/fixture", original_uri_status="UNAVAILABLE",
                          original_uri_checked_at="2026-10-17")
            audit = integrity.audit_sources(self.root)
        self.assertEqual(self.errors(), set())
        self.assertEqual(audit["sources"][SID1]["integrity_status"], "MATCH")
        self.assertTrue(any("ORIGINAL_URI_UNAVAILABLE" in issue for issue in audit["issues"]))
        self.assertEqual(audit["sources"][SID1]["verification_status"], "UNVERIFIED")

    def test_09_attempted_raw_modification_is_refused(self):
        row = self.row()
        self.snapshot(row)
        path = self.root / row["source_url_or_path"]
        before = path.read_bytes()
        with self.assertRaisesRegex(integrity.IntegrityError, "RAW_SOURCE_IMMUTABLE"):
            integrity.create_raw_snapshot(self.root, row["source_url_or_path"], b"replacement", authorized=True)
        self.assertEqual(path.read_bytes(), before)
        with self.assertRaises(PermissionError):
            integrity.create_raw_snapshot(self.root, "sources/raw/new.md", b"new")
        self.assertFalse((self.root / "sources/raw/new.md").exists())

    def test_10_source_version_replacement_preserves_old_snapshot_and_references(self):
        self.register(source_uri="https://example.invalid/versioned")
        self.wiki([SID1])
        before = self.metadata_bytes()
        second = self.row(SID2, "two.md")
        self.snapshot(second, b"TEST_ONLY revision two")
        integrity.register_source(self.root, second, authorized=True, source_uri="https://example.invalid/versioned",
                                  source_version=2, replaces=SID1)
        audit = integrity.audit_sources(self.root)
        self.assertEqual(self.errors(), set())
        self.assertEqual(audit["sources"][SID1]["superseded_by"], SID2)
        self.assertEqual(audit["sources"][SID2]["source_version"], 2)
        self.assertTrue(any("SUPERSEDED_SOURCE_REFERENCE" in issue for issue in audit["issues"]))
        self.assertEqual((self.root / "sources/raw/one.md").read_bytes(), b"TEST_ONLY original bytes\n")
        for path, data in before.items():
            self.assertTrue((self.root / path).read_bytes().startswith(data))
        citation = query.search(self.root, "Fixture claim", "demo")["matches"][0]["citations"][0]
        self.assertEqual(citation["source_id"], SID1)
        self.assertEqual(citation["source_version"], 1)
        self.assertEqual(citation["superseded_by"], SID2)

    def test_legacy_migration_is_explicit_readonly_planning_and_append_only_apply(self):
        row = self.row()
        self.snapshot(row)
        self.append_row(row)
        self.wiki([SID1])
        before = self.metadata_bytes()
        raw_before = (self.root / row["source_url_or_path"]).read_bytes()
        self.assertIn("MISSING_PROVENANCE", self.errors())
        self.assertFalse(any(item.startswith("ERROR ") for item in checker.check_workspace(self.root)))
        legacy = query.search(self.root, "Fixture claim", "demo")["matches"][0]["citations"][0]
        self.assertEqual(legacy["integrity_status"], "LEGACY_UNHASHED")
        proposal = integrity.plan_migration(self.root)
        self.assertEqual(self.metadata_bytes(), before)
        with self.assertRaises(PermissionError):
            integrity.apply_migration(self.root, proposal)
        integrity.apply_migration(self.root, proposal, authorized=True)
        self.assertEqual(self.errors(), set())
        self.assertEqual((self.root / "sources/manifest.csv").read_bytes(), before["sources/manifest.csv"])
        self.assertEqual((self.root / row["source_url_or_path"]).read_bytes(), raw_before)
        self.assertEqual(integrity.audit_sources(self.root)["sources"][SID1]["language"], "und")

    def test_migration_detects_changed_bytes_since_proposal(self):
        row = self.row()
        self.snapshot(row)
        self.append_row(row)
        proposal = integrity.plan_migration(self.root)
        (self.root / row["source_url_or_path"]).write_bytes(b"TEST_ONLY changed after planning")
        before = self.metadata_bytes()
        with self.assertRaisesRegex(integrity.IntegrityError, "MIGRATION_PROPOSAL_CHANGED"):
            integrity.apply_migration(self.root, proposal, authorized=True)
        self.assertEqual(self.metadata_bytes(), before)

    def test_remote_only_legacy_record_requires_an_authorized_snapshot(self):
        row = dict(self.row(), source_url_or_path="https://example.invalid/unavailable")
        self.append_row(row)
        with patch("socket.create_connection", side_effect=AssertionError("network")):
            with self.assertRaisesRegex(integrity.IntegrityError, "MISSING_LOCAL_SNAPSHOT"):
                integrity.plan_migration(self.root)
        self.assertIn("MISSING_LOCAL_SNAPSHOT", self.errors())

    def test_multiple_sources_support_one_claim_and_one_bad_source_blocks_it(self):
        self.register()
        self.register(self.row(SID2, "two.md"), data=b"TEST_ONLY second independent source")
        self.wiki([SID1, SID2])
        audit = integrity.audit_sources(self.root)
        self.assertEqual(self.errors(), set())
        self.assertEqual(audit["claims"][0]["source_ids"], [SID1, SID2])
        result = query.search(self.root, "Fixture claim", "demo")
        self.assertEqual({c["source_id"] for c in result["matches"][0]["citations"]}, {SID1, SID2})
        (self.root / "sources/raw/two.md").write_bytes(b"TEST_ONLY bit flip")
        self.assertEqual(query.search(self.root, "Fixture claim", "demo")["status"], "MISSING_EVIDENCE")

    def test_claim_with_no_evidence_stays_unknown(self):
        self.register()
        self.wiki([SID1])
        with (self.root / "wiki/fixture.md").open("a", encoding="utf-8") as handle:
            handle.write("\n- FACT: TEST_ONLY unsupported additional claim.\n")
        self.assertTrue(any("MISSING_CITATION" in item for item in checker.check_workspace(self.root, integrity=True)))
        self.assertEqual(query.search(self.root, "Fixture claim", "demo")["status"], "MISSING_EVIDENCE")

    def test_corrupt_duplicate_and_orphan_provenance_fail_closed(self):
        for text, code in (
            ("not JSON\n", "PROVENANCE_FORMAT"),
            ('{"source_id":"x","source_id":"y"}\n', "DUPLICATE_PROVENANCE_FIELD"),
            ('{"source_id":"x"}\n', "PROVENANCE_FIELDS"),
        ):
            with self.subTest(code=code):
                self.write(integrity.LEDGER, text)
                self.assertIn(code, self.errors())
        (self.root / integrity.LEDGER).unlink()
        self.register()
        entry = integrity.read_provenance(self.root)[SID1]
        self.append_entry(entry)
        self.assertIn("DUPLICATE_PROVENANCE_ID", self.errors())

    def test_manually_duplicated_content_is_detected(self):
        row = self.register()
        entry = integrity.read_provenance(self.root)[SID1]
        duplicate = dict(row, source_id=SID2)
        self.append_row(duplicate)
        self.append_entry(dict(entry, source_id=SID2, manifest_hash=integrity.manifest_hash(duplicate)))
        self.assertIn("DUPLICATE_CONTENT", self.errors())

    def test_manifest_metadata_tampering_is_detected(self):
        self.register()
        self.wiki([SID1])
        path = self.root / "sources/manifest.csv"
        # Simulated unauthorized metadata edit, not a normal maintenance operation.
        text = path.read_text(encoding="utf-8").replace("TEST_ONLY synthetic source", "TEST_ONLY altered title")
        path.write_text(text, encoding="utf-8")
        self.assertIn("MANIFEST_HASH_MISMATCH", self.errors())
        self.assertEqual(query.search(self.root, "Fixture claim", "demo")["status"], "INVALID_DATA")
    def test_known_origin_revision_needs_explicit_version_link(self):
        self.register(source_uri="https://example.invalid/origin")
        second = self.row(SID2, "two.md")
        self.snapshot(second, b"TEST_ONLY changed revision")
        before = self.metadata_bytes()
        with self.assertRaisesRegex(integrity.IntegrityError, "SOURCE_REVISION_REQUIRED"):
            integrity.register_source(self.root, second, authorized=True, source_uri="https://example.invalid/origin")
        self.assertEqual(self.metadata_bytes(), before)

    def test_forked_and_out_of_sequence_versions_are_rejected_before_append(self):
        self.register()
        second = self.register(self.row(SID2, "two.md"), data=b"TEST_ONLY second",
                               source_version=2, replaces=SID1)
        third = self.row(SID3, "three.md")
        self.snapshot(third, b"TEST_ONLY third")
        before = self.metadata_bytes()
        with self.assertRaisesRegex(integrity.IntegrityError, "BRANCHED_SOURCE_VERSION"):
            integrity.register_source(self.root, third, authorized=True, source_version=2, replaces=SID1)
        with self.assertRaisesRegex(integrity.IntegrityError, "SOURCE_VERSION_SEQUENCE"):
            integrity.register_source(self.root, third, authorized=True, source_version=4, replaces=second["source_id"])
        self.assertEqual(self.metadata_bytes(), before)

    def test_metadata_only_replacement_can_reuse_immutable_bytes(self):
        row = self.register()
        corrected = dict(row, source_id=SID2, title="TEST_ONLY corrected title")
        integrity.register_source(self.root, corrected, authorized=True, source_version=2, replaces=SID1)
        self.assertEqual(self.errors(), set())
        audit = integrity.audit_sources(self.root)
        self.assertEqual(audit["sources"][SID1]["content_hash"], audit["sources"][SID2]["content_hash"])

    def test_binary_sources_are_hashed_without_text_decoding(self):
        self.register(data=b"\x00\xff\xfeTEST_ONLY binary")
        self.assertEqual(self.errors(), set())

    def test_stale_lock_is_not_deleted_or_ignored(self):
        lock = self.write("sources/registration.lock", "TEST_ONLY existing lock")
        row = self.row()
        self.snapshot(row)
        with self.assertRaises(FileExistsError):
            integrity.register_source(self.root, row, authorized=True)
        self.assertEqual(lock.read_text(encoding="utf-8"), "TEST_ONLY existing lock")

    def test_interrupted_registration_is_an_orphan_not_a_trusted_source(self):
        row = self.row()
        self.snapshot(row)
        manifest = self.root / "sources/manifest.csv"
        original_open = Path.open

        def fail_append(path, mode="r", *args, **kwargs):
            if path == manifest and mode == "a":
                raise OSError("TEST_ONLY simulated interrupted manifest append")
            return original_open(path, mode, *args, **kwargs)

        with patch.object(Path, "open", fail_append):
            with self.assertRaises(OSError):
                integrity.register_source(self.root, row, authorized=True)
        self.assertIn("ORPHAN_PROVENANCE", self.errors())
        self.assertEqual(query.search(self.root, "Fixture claim", "demo")["status"], "INVALID_DATA")
        self.assertEqual((self.root / row["source_url_or_path"]).read_bytes(), b"TEST_ONLY original bytes\n")

    def test_hash_matching_never_promotes_verification_status(self):
        self.register()
        record = integrity.audit_sources(self.root)["sources"][SID1]
        self.assertEqual(record["integrity_status"], "MATCH")
        self.assertEqual(record["verification_status"], "UNVERIFIED")
        second = self.row(SID2, "two.md")
        self.snapshot(second, b"TEST_ONLY another source")
        with self.assertRaisesRegex(integrity.IntegrityError, "VERIFICATION_NOTE_REQUIRED"):
            integrity.register_source(self.root, second, authorized=True, verification_status="VERIFIED")

    def test_audit_and_query_are_read_only_and_only_hash_raw_bytes(self):
        row = self.register()
        self.wiki([SID1])
        before = self.metadata_bytes()
        raw_before = (self.root / row["source_url_or_path"]).read_bytes()
        original_open = Path.open

        def binary_only(path, mode="r", *args, **kwargs):
            if path.is_relative_to(self.root / "sources/raw") and mode != "rb":
                raise AssertionError("raw source must only be opened for binary hashing")
            return original_open(path, mode, *args, **kwargs)

        with patch.object(Path, "open", binary_only):
            self.assertEqual(self.errors(), set())
            self.assertEqual(query.search(self.root, "Fixture claim", "demo")["status"], "FOUND")
        self.assertEqual(self.metadata_bytes(), before)
        self.assertEqual((self.root / row["source_url_or_path"]).read_bytes(), raw_before)


if __name__ == "__main__":
    unittest.main()
