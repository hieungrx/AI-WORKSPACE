"""Adversarial inputs and recovery run only in disposable TEST_ONLY workspaces."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from scripts import check_workspace as checker
from scripts import ingest_workspace as ingest
from scripts import query_workspace as query
from scripts import safe_operations as operations
from scripts import source_integrity as integrity
from scripts import workspace_security as security

SID = "SRC-20261017-401"
ATTACKS = Path(__file__).absolute().parent / "fixtures/security/attacks.json"
ATTACK_OBSERVATIONS = []
RECOVERY_OBSERVATION = {}


class SimulatedCrash(BaseException):
    pass


class SecurityRecoveryTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).absolute().parent
        temporary = tempfile.TemporaryDirectory(prefix="fixture-security-", dir=parent)
        if not Path(temporary.name).is_relative_to(parent):
            raise AssertionError("fixture escaped tests/")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "workspace"
        self.root.mkdir()
        self.write("sources/manifest.csv", ",".join(checker.MANIFEST_FIELDS) + "\n")
        self.write("AGENTS.md", "# TEST_ONLY trusted operating policy\n")
        self.write("SCHEMA.md", "# TEST_ONLY trusted schema\n")
        self.write(".env", "TEST_ONLY_DO_NOT_OPEN\n")
        self.write("wiki/index.md", "# TEST_ONLY Index\n[Existing](existing.md)\n")
        self.write("wiki/log.md", "# TEST_ONLY append-only log\n")
        self.write("wiki/existing.md", "# Existing policy\n- Status: DRAFT\n- Updated: 2026-10-17\n"
                   "- Source IDs: None\n- Scope: security-demo\n\n## Summary\nUNKNOWN: TEST_ONLY evidence gap.\n")
        self.write("wiki/unrelated.md", "# User notes\n- Status: DRAFT\n- Updated: 2026-10-17\n"
                   "- Source IDs: None\n- Scope: security-demo\n\n## Summary\nUNKNOWN: TEST_ONLY user work.\n")
        self.register(SID, "# TEST_ONLY safe source\nBenign synthetic technical evidence.\n")

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def register(self, sid, text):
        raw = "sources/raw/" + sid + ".md"
        integrity.create_raw_snapshot(self.root, raw, text.encode("utf-8"), authorized=True)
        row = dict(zip(checker.MANIFEST_FIELDS, (
            sid, "TEST_ONLY source", "synthetic_fixture", raw, "", "", "2026-10-17",
            "Synthetic tests only", "Unknown author and publication date.",
        )))
        integrity.register_source(self.root, row, authorized=True)

    def plan(self, sid=SID):
        text = ("# Safe synthesis\n- Status: draft\n- kind: external_fact\n- Scope: security-demo\n"
                "- created_at: 2026-10-17\n- updated_at: 2026-10-17\n- temporal: historical\n"
                "- transitions: []\n- Source IDs: " + sid
                + "\n\n## Summary\nUNKNOWN: TEST_ONLY synthesis pending human review.\n"
                "\n## Verified findings\n- FACT: TEST_ONLY synthetic claim. [" + sid + ", section 1]\n")
        changes = {"wiki/new.md": text.encode(),
                   "wiki/index.md": (self.root / "wiki/index.md").read_bytes() + b"[New](new.md)\n",
                   "wiki/log.md": (self.root / "wiki/log.md").read_bytes() + b"\nTEST_ONLY approved synthesis.\n"}
        return changes, operations.versions(self.root, changes)

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*")
                if p.is_file() and not p.is_relative_to(self.root / "recovery")}

    def fail_second_replace(self, exception):
        original = operations._replace_file
        counter = 0

        def replace(staged, target):
            nonlocal counter
            if staged.suffix == ".after":
                counter += 1
                if counter == 2:
                    raise exception
            return original(staged, target)
        return replace

    def test_01_prompt_injection_in_source_is_blocked_on_actual_ingest_path(self):
        samples = json.loads(ATTACKS.read_text(encoding="utf-8"))["samples"]
        for number, sample in enumerate(samples, 410):
            with self.subTest(sample=sample["id"]):
                sid = "SRC-20261017-" + str(number)
                self.register(sid, sample["markdown"])
                changes, expected = self.plan(sid)
                before = self.snapshot()
                with patch("subprocess.run", side_effect=AssertionError("shell forbidden")), patch(
                        "socket.create_connection", side_effect=AssertionError("network forbidden")):
                    with self.assertRaisesRegex(security.SecurityError, "UNTRUSTED_CONTENT") as blocked:
                        ingest.ingest_registered(self.root, sid, changes, expected, scope="security-demo",
                                                 authorized=True, apply=True)
                ATTACK_OBSERVATIONS.append({"sample": sample["id"], "path": "ingest_registered",
                                            "observed_status": str(blocked.exception),
                                            "user_files_unchanged": self.snapshot() == before})
                self.assertEqual(self.snapshot(), before)

    def test_02_fake_priority_and_hidden_instructions_block_actual_query(self):
        original = (self.root / "wiki/existing.md").read_text(encoding="utf-8")
        samples = json.loads(ATTACKS.read_text(encoding="utf-8"))["samples"]
        for sample in samples:
            with self.subTest(sample=sample["id"]):
                self.write("wiki/existing.md", original + "\n" + sample["markdown"])
                before = self.snapshot()
                with patch("subprocess.run", side_effect=AssertionError("shell forbidden")):
                    result = query.search(self.root, "Existing policy", "security-demo")
                ATTACK_OBSERVATIONS.append({"sample": sample["id"], "path": "query.search",
                                            "observed_status": result["status"],
                                            "user_files_unchanged": self.snapshot() == before})
                self.assertEqual(result["status"], "UNTRUSTED_CONTENT")
                self.assertEqual(result["matches"], [])
                self.assertNotIn(sample["markdown"], json.dumps(result))
                self.assertEqual(self.snapshot(), before)

    def test_03_unauthorized_policy_modification_has_no_write_capability(self):
        before = self.snapshot()
        for path in ("AGENTS.md", "SCHEMA.md", "wiki/AGENTS.md", "sources/raw/AGENTS.md", ".gitignore"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                operations.transact(self.root, {path: b"TEST_ONLY forbidden change"}, {path: None}, authorized=True)
        changes, expected = self.plan()
        changes["AGENTS.md"], expected["AGENTS.md"] = b"TEST_ONLY source-supplied policy", None
        with self.assertRaisesRegex(security.SecurityError, "POLICY_WRITE_DENIED"):
            ingest.ingest_registered(self.root, SID, changes, expected, scope="security-demo", authorized=True, apply=True)
        self.assertEqual(self.snapshot(), before)

    def test_04_path_traversal_and_windows_aliases_are_rejected(self):
        for path in ("../outside.md", "wiki/../AGENTS.md", "wiki/%2e%2e/AGENTS.md",
                     "C:/outside.md", "//server/share/file.md", "wiki/page.md:stream",
                     "wiki/NUL.md", "wiki/page.md."):
            with self.subTest(path=path), self.assertRaises(ValueError):
                operations.transact(self.root, {path: b"TEST_ONLY"}, {path: None}, authorized=True)

    def test_05_sensitive_locations_are_rejected_before_open(self):
        guarded = self.root / ".env"
        original_open = Path.open
        def no_secret(path, *args, **kwargs):
            if path == guarded:
                raise AssertionError("sensitive contents opened")
            return original_open(path, *args, **kwargs)
        with patch.object(Path, "open", no_secret):
            with self.assertRaises(ValueError):
                security.read_data(self.root, ".env")
            issues = security.audit_security(self.root)
        self.assertTrue(any("SENSITIVE_LOCATION" in issue for issue in issues))
        self.assertNotIn("TEST_ONLY_DO_NOT_OPEN", json.dumps(issues))

    def test_06_failed_write_midway_restores_all_owned_resources(self):
        changes, expected = self.plan()
        before = self.snapshot()
        with patch.object(operations, "_replace_file", self.fail_second_replace(OSError("TEST_ONLY disk failure"))):
            with self.assertRaises(OSError):
                operations.transact(self.root, changes, expected, authorized=True)
        self.assertEqual(self.snapshot(), before)
        operations.ensure_idle(self.root)

    def test_07_failed_ingestion_rolls_back_without_removing_approved_source(self):
        changes, expected = self.plan()
        before = self.snapshot()
        with patch.object(operations, "_replace_file", self.fail_second_replace(OSError("TEST_ONLY failed ingest"))):
            with self.assertRaises(OSError):
                ingest.ingest_registered(self.root, SID, changes, expected, scope="security-demo",
                                         authorized=True, apply=True)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(integrity.audit_sources(self.root)["sources"][SID]["integrity_status"], "MATCH")
        self.assertFalse((self.root / "wiki/new.md").exists())

    def test_08_concurrent_writers_cannot_silently_lose_updates(self):
        relative = "wiki/existing.md"
        original = (self.root / relative).read_bytes()
        expected = operations.versions(self.root, [relative])
        barrier = threading.Barrier(2)
        def writer(label):
            data = original + ("\nTEST_ONLY writer " + label + "\n").encode()
            barrier.wait(timeout=10)
            try:
                operations.transact(self.root, {relative: data}, expected, authorized=True)
                return label, "COMMITTED", data
            except (ValueError, OSError):
                return label, "CONFLICT", data
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(writer, ("A", "B")))
        winners = [item for item in results if item[1] == "COMMITTED"]
        self.assertEqual(len(winners), 1)
        self.assertEqual((self.root / relative).read_bytes(), winners[0][2])

    def test_09_generated_report_redacts_secret_keys_and_values(self):
        fake = "sk-proj-" + "TESTONLY0123456789" * 3
        report = {fake: fake, "detail": "Bearer " + "TESTONLYTOKEN" * 3}
        operations.save_reports(self.root, report, "reports/redacted.json", lambda data: json.dumps(data))
        for relative in ("reports/redacted.json", "reports/redacted.md"):
            text = (self.root / relative).read_text(encoding="utf-8")
            self.assertNotIn(fake, text)
            self.assertIn("[REDACTED]", text)

    def test_10_crash_recovery_preserves_every_unrelated_user_file(self):
        changes, expected = self.plan()
        before = self.snapshot()
        with patch.object(operations, "_replace_file", self.fail_second_replace(SimulatedCrash())):
            with self.assertRaises(SimulatedCrash):
                ingest.ingest_registered(self.root, SID, changes, expected, scope="security-demo",
                                         authorized=True, apply=True)
        pending_status = query.search(self.root, "Existing policy", "security-demo")["status"]
        self.assertEqual(pending_status, "RECOVERY_REQUIRED")
        result = operations.recover(self.root, authorized=True)
        RECOVERY_OBSERVATION.update({
            "fixture_only": True, "failure_after_resource_replacements": 1,
            "query_before_recovery": pending_status, "recovery_result": result,
            "before_hashes": {key: operations.digest(value) for key, value in before.items()
                              if key.startswith("wiki/") or key.startswith("sources/")},
            "after_hashes": {key: operations.digest(value) for key, value in self.snapshot().items()
                             if key.startswith("wiki/") or key.startswith("sources/")},
            "all_user_files_preserved": self.snapshot() == before,
        })
        self.assertEqual(result["status"], "ROLLED_BACK")
        self.assertEqual(self.snapshot(), before)
        operations.ensure_idle(self.root)

    def test_successful_ingestion_is_atomic_draft_and_query_remains_data(self):
        changes, expected = self.plan()
        result = ingest.ingest_registered(self.root, SID, changes, expected, scope="security-demo",
                                          authorized=True, apply=True)
        self.assertEqual(result["status"], "COMMITTED")
        found = query.search(self.root, "Safe synthesis", "security-demo")
        self.assertEqual(found["status"], "FOUND")
        self.assertEqual(found["matches"][0]["content_trust"], "UNTRUSTED_DATA")
        self.assertEqual(found["matches"][0]["knowledge_status"], "draft")
        self.assertFalse(found["matches"][0]["usable_as_current_truth"])

    def test_recovery_refuses_to_overwrite_edits_made_after_interruption(self):
        changes, expected = self.plan()
        with patch.object(operations, "_replace_file", self.fail_second_replace(SimulatedCrash())):
            with self.assertRaises(SimulatedCrash):
                operations.transact(self.root, changes, expected, authorized=True)
        self.write("wiki/new.md", "TEST_ONLY user edit after interruption\n")
        before = self.snapshot()
        with self.assertRaisesRegex(security.SecurityError, "RECOVERY_CONFLICT"):
            operations.recover(self.root, authorized=True)
        self.assertEqual(self.snapshot(), before)

    def test_tampered_journal_cannot_target_operating_policy(self):
        changes, expected = self.plan()
        with patch.object(operations, "_replace_file", self.fail_second_replace(SimulatedCrash())):
            with self.assertRaises(SimulatedCrash):
                operations.transact(self.root, changes, expected, authorized=True)
        journal = self.root / "recovery/active.json"
        record = json.loads(journal.read_text(encoding="utf-8"))
        record["files"][0]["path"] = "AGENTS.md"
        journal.write_text(json.dumps(record), encoding="utf-8")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            operations.recover(self.root, authorized=True)
        self.assertEqual(self.snapshot(), before)

    def test_new_raw_snapshot_never_publishes_partial_bytes(self):
        original = operations._sync
        def fail(path, data):
            if path.suffix == ".snapshot":
                original(path, b"TEST_ONLY incomplete")
                raise OSError("TEST_ONLY partial temporary write")
            return original(path, data)
        with patch.object(operations, "_sync", fail):
            with self.assertRaises(OSError):
                integrity.create_raw_snapshot(self.root, "sources/raw/new.md", b"TEST_ONLY complete", authorized=True)
        self.assertFalse((self.root / "sources/raw/new.md").exists())

    def test_approval_and_source_command_cannot_expand_the_write_allowlist(self):
        for operation in ("policy", "shell", "external", "permissions"):
            with self.subTest(operation=operation), self.assertRaisesRegex(security.SecurityError, "WRITE_DENIED"):
                operations.transact(self.root, {"AGENTS.md": b"TEST_ONLY"}, {"AGENTS.md": None},
                                    operation=operation, authorized=True)

    def test_sensitive_generated_wiki_is_blocked_before_backup_or_commit(self):
        changes, expected = self.plan()
        changes["wiki/new.md"] += ("\napi_key=" + "TESTONLY0123456789" * 2).encode()
        before = self.snapshot()
        with self.assertRaisesRegex(security.SecurityError, "SENSITIVE_CONTENT"):
            ingest.ingest_registered(self.root, SID, changes, expected, scope="security-demo",
                                     authorized=True, apply=True)
        self.assertEqual(self.snapshot(), before)

    def test_stale_owner_requires_explicit_human_recovery_acknowledgement(self):
        lock = self.write("recovery/owner.lock", "a" * 32)
        with self.assertRaisesRegex(security.SecurityError, "OWNER_REVIEW_REQUIRED"):
            operations.recover(self.root, authorized=True)
        self.assertTrue(lock.exists())
        result = operations.recover(self.root, authorized=True, acknowledge_stale_lock=True)
        self.assertEqual(result["status"], "NOTHING_TO_RECOVER")

    def test_old_report_writers_use_the_redaction_boundary(self):
        from scripts import validate_source_integrity, validate_knowledge_governance, validate_multilingual
        fake = "sk-proj-" + "TESTONLY0123456789" * 3
        for number, module in enumerate((validate_source_integrity, validate_knowledge_governance, validate_multilingual)):
            name = "save_report" if module is validate_multilingual else "save"
            renderer = "markdown_report" if module is validate_multilingual else "markdown"
            with patch.object(module, "ROOT", self.root), patch.object(module, renderer, lambda data: json.dumps(data)):
                getattr(module, name)({"details": fake}, Path(f"reports/legacy-writer-{number}.json"))
            self.assertNotIn(fake, (self.root / f"reports/legacy-writer-{number}.json").read_text(encoding="utf-8"))

    def test_committed_operation_recovery_keeps_complete_result(self):
        changes, expected = self.plan()
        original = operations._finish
        with patch.object(operations, "_finish", side_effect=SimulatedCrash()):
            with self.assertRaises(SimulatedCrash):
                operations.transact(self.root, changes, expected, authorized=True)
        after = self.snapshot()
        result = operations.recover(self.root, authorized=True)
        self.assertEqual(result["status"], "COMMITTED")
        self.assertEqual(self.snapshot(), after)
        self.assertEqual((self.root / "wiki/new.md").read_bytes(), changes["wiki/new.md"])

    def test_fake_labeled_identity_is_flagged_without_value_in_output(self):
        fake = "TEST_ONLY_IDENTITY_00000"
        self.write("wiki/accidental.md", "national_id=" + fake)
        issues = security.audit_security(self.root)
        self.assertTrue(any("LABELED_IDENTITY" in issue for issue in issues))
        self.assertNotIn(fake, json.dumps(issues))

    def test_raw_policy_filename_is_blocked_before_publication(self):
        with self.assertRaisesRegex(security.SecurityError, "POLICY_WRITE_DENIED"):
            integrity.create_raw_snapshot(self.root, "sources/raw/AGENTS.md", b"TEST_ONLY", authorized=True)
        self.assertFalse((self.root / "sources/raw/AGENTS.md").exists())

    def test_query_rejects_a_generation_changed_during_retrieval(self):
        changes, expected = self.plan()
        ingest.ingest_registered(self.root, SID, changes, expected, scope="security-demo", authorized=True, apply=True)
        original = query.evaluate_evidence
        changed = False
        def concurrent_writer(*args, **kwargs):
            nonlocal changed
            if not changed:
                changed = True
                relative = "wiki/new.md"
                before = (self.root / relative).read_bytes()
                operations.transact(self.root, {relative: before + b"\nTEST_ONLY concurrent edit\n"},
                                    {relative: operations.digest(before)}, authorized=True)
            return original(*args, **kwargs)
        with patch.object(query, "evaluate_evidence", concurrent_writer):
            result = query.search(self.root, "Safe synthesis", "security-demo")
        self.assertEqual(result["status"], "RECOVERY_REQUIRED")
        self.assertEqual(result["matches"], [])

    def test_synthetic_private_key_block_is_redacted_as_a_whole(self):
        text = "-----BEGIN ENCRYPTED PRIVATE KEY-----\nTEST_ONLY_NOT_A_KEY\n-----END ENCRYPTED PRIVATE KEY-----"
        self.assertEqual(security.secret_codes(text), ["PRIVATE_KEY"])
        safe = security.redact(text)
        self.assertEqual(safe, "[REDACTED]")
        self.assertNotIn("TEST_ONLY_NOT_A_KEY", safe)
