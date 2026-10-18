"""TEST_ONLY required approvals across every lifecycle public boundary.

Approval files are simulated human assertions in disposable fixtures only.
No production approval, source or lifecycle history is created by these tests.
"""
from datetime import date
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import check_workspace as lint
from scripts import knowledge_governance as governance
from scripts import query_workspace as query
from scripts import safe_operations as operations
from tests.workflow_support import DAY, SID, Workspace


class GovernanceApprovalPathTests(unittest.TestCase):
    def setUp(self):
        class FixtureDate(date):
            @classmethod
            def today(cls):
                return cls(2026, 10, 18)

        clock = patch.object(governance, "date", FixtureDate)
        clock.start()
        self.addCleanup(clock.stop)
        parent = Path(__file__).absolute().parent
        temporary = tempfile.TemporaryDirectory(prefix="fixture-approval-paths-", dir=parent)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "workspace"
        self.workspace = Workspace(self.root)
        self.workspace.register()
        self.other_sid = "SRC-20261018-502"
        self.workspace.register(self.other_sid, body="TEST_ONLY alternate synthetic observation.")
        self.relative = "wiki/approval-boundary.md"
        self.path = self.root / self.relative
        conflict = {"summary": "TEST_ONLY disagreement", "source_ids": [SID, self.other_sid],
                    "resolution": "TEST_ONLY proposed reconciliation awaiting human validation"}
        self.workspace.write(self.relative, self.workspace.page(
            title="Approval boundary", sources=(SID, self.other_sid), conflicts=json.dumps([conflict]),
            temporal="current", review_after="2099-12-31"))
        index = self.root / "wiki/index.md"
        index.write_bytes(index.read_bytes() + b"[TEST_ONLY boundary](approval-boundary.md)\n")
        self.workspace.move(self.relative, "unverified")
        self.workspace.move(self.relative, "disputed")

    def proposal(self, approval_ref, *, actor="human", target="unverified", policy=2):
        """Build untrusted proposed bytes; do not bypass the writer's checks."""
        text = self.path.read_text(encoding="utf-8")
        events = json.loads(lint.metadata(text)["transitions"])
        event = {"from": "disputed", "to": target, "actor": actor, "at": DAY,
                 "reason": "TEST_ONLY boundary transition", "approval": approval_ref}
        if policy == 2:
            event.update(approval_policy=2, approval_content_hash=governance.content_hash(text))
        events.append(event)
        for name, value in (("Status", target), ("updated_at", DAY), ("transitions", json.dumps(events))):
            text = governance.replace_field(text, name, value)
        return text

    def direct_write(self, proposed):
        changes = {self.relative: proposed.encode("utf-8")}
        return operations.transact(self.root, changes,
                                   operations.versions(self.root, changes, operation="lifecycle"),
                                   operation="lifecycle", authorized=True)

    def lint_errors(self):
        return [issue for issue in lint.check_workspace(self.root, integrity=True, security=True)
                if issue.startswith("ERROR ")]

    def assert_metadata_equal(self, left, right):
        left_meta, right_meta = lint.metadata(left), lint.metadata(right)
        self.assertEqual(json.loads(left_meta.pop("transitions")), json.loads(right_meta.pop("transitions")))
        self.assertEqual(left_meta, right_meta)

    def approval(self, relative="experiments/resolution-approval.md", **overrides):
        fields = {"Status": "APPROVED", "authority": "human", "target": self.relative,
                  "content_hash": governance.content_hash(self.path.read_text(encoding="utf-8")),
                  "validated_at": DAY, "evidence": '["reports/validation.md"]',
                  "approval_policy": "2", "from_state": "disputed", "to_state": "unverified",
                  "prior_transitions_hash": governance.history_hash(json.loads(
                      lint.metadata(self.path.read_text(encoding="utf-8"))["transitions"]))}
        fields.update(overrides)
        self.workspace.write(relative, "# TEST_ONLY simulated approval\n" + "".join(
            "- " + key + ": " + value + "\n" for key, value in fields.items()))
        return relative

    def assert_invalid_approval_across_public_boundaries(self, ref):
        original = self.path.read_bytes()
        proposed = self.proposal(ref)
        before = self.workspace.snapshot()
        with self.assertRaises((governance.GovernanceError, OSError)):
            governance.transition(self.root, self.relative, "unverified", actor="human", at=DAY,
                                  reason="TEST_ONLY invalid approval", approval_ref=ref,
                                  authorized=True, apply=True)
        self.assertEqual(self.workspace.snapshot(), before)
        with self.assertRaises((governance.GovernanceError, OSError)):
            self.direct_write(proposed)
        self.assertEqual(self.workspace.snapshot(), before)
        with self.assertRaises((governance.GovernanceError, OSError)):
            governance.read_page(self.root, self.path, proposed)
        try:
            self.workspace.write(self.relative, proposed)
            read_snapshot = self.workspace.snapshot(include_recovery=True)
            result = query.search(self.root, "Approval boundary", "global")
            self.assertEqual(result["status"], "INVALID_DATA")
            self.assertEqual(result["matches"], [])
            self.assertTrue(self.lint_errors())
            self.assertEqual(self.workspace.snapshot(include_recovery=True), read_snapshot)
        finally:
            self.path.write_bytes(original)

    def test_missing_approval_helper_and_writer_both_reject_atomically(self):
        missing = "experiments/does-not-exist.md"
        before = self.workspace.snapshot()
        with self.assertRaises((governance.GovernanceError, OSError)):
            governance.transition(self.root, self.relative, "unverified", actor="human", at=DAY,
                                  reason="TEST_ONLY missing approval", approval_ref=missing,
                                  authorized=True, apply=True)
        self.assertEqual(self.workspace.snapshot(), before)
        with self.assertRaises((governance.GovernanceError, OSError)):
            self.direct_write(self.proposal(missing))
        self.assertEqual(self.workspace.snapshot(), before)

    def test_missing_approval_history_is_rejected_by_reader(self):
        with self.assertRaises((governance.GovernanceError, OSError)):
            governance.read_page(self.root, self.path, self.proposal("experiments/does-not-exist.md"))

    def test_legacy_history_still_validates_its_required_approval(self):
        proposed = self.proposal("experiments/does-not-exist.md", policy=1)
        before = self.workspace.snapshot(include_recovery=True)
        with self.assertRaises((governance.GovernanceError, OSError)):
            self.direct_write(proposed)
        self.assertEqual(self.workspace.snapshot(include_recovery=True), before)
        with self.assertRaises((governance.GovernanceError, OSError)):
            governance.read_page(self.root, self.path, proposed)
        self.workspace.write(self.relative, proposed)
        result = query.search(self.root, "Approval boundary", "global")
        self.assertEqual(result["status"], "INVALID_DATA")
        self.assertEqual(result["matches"], [])
        self.assertTrue(self.lint_errors())

    def test_missing_approval_history_is_rejected_by_query(self):
        self.workspace.write(self.relative, self.proposal("experiments/does-not-exist.md"))
        before = self.workspace.snapshot(include_recovery=True)
        result = query.search(self.root, "Approval boundary", "global")
        self.assertEqual(result["status"], "INVALID_DATA")
        self.assertEqual(result["matches"], [])
        self.assertEqual(self.workspace.snapshot(include_recovery=True), before)

    def test_missing_approval_history_is_detected_by_lint(self):
        self.workspace.write(self.relative, self.proposal("experiments/does-not-exist.md"))
        before = self.workspace.snapshot(include_recovery=True)
        self.assertTrue(self.lint_errors())
        self.assertEqual(self.workspace.snapshot(include_recovery=True), before)

    def test_invalid_required_approval_remains_invalid_in_prior_history(self):
        proposed = self.proposal("experiments/does-not-exist.md")
        events = json.loads(lint.metadata(proposed)["transitions"])
        events.append({"from": "unverified", "to": "draft", "actor": "ai", "at": DAY,
                       "reason": "TEST_ONLY later revision does not erase invalid approval", "approval": None})
        proposed = governance.replace_field(proposed, "transitions", json.dumps(events))
        proposed = governance.replace_field(proposed, "Status", "draft")
        with self.assertRaises((governance.GovernanceError, OSError)):
            governance.read_page(self.root, self.path, proposed)
        self.workspace.write(self.relative, proposed)
        result = query.search(self.root, "Approval boundary", "global")
        self.assertEqual(result["status"], "INVALID_DATA")
        self.assertEqual(result["matches"], [])
        self.assertTrue(self.lint_errors())

    def test_bad_approval_rejects_entire_bundle_before_any_publication(self):
        second = "wiki/other-draft.md"
        original = self.workspace.page(title="Unchanged neighbour")
        self.workspace.write(second, original)
        event = {"from": "draft", "to": "unverified", "actor": "ai", "at": DAY,
                 "reason": "TEST_ONLY valid neighbour transition", "approval": None}
        neighbour = governance.replace_field(original, "transitions", json.dumps([event]))
        neighbour = governance.replace_field(neighbour, "Status", "unverified")
        changes = {second: neighbour.encode("utf-8"),
                   self.relative: self.proposal("experiments/does-not-exist.md").encode("utf-8")}
        before = self.workspace.snapshot(include_recovery=True)
        with self.assertRaises((governance.GovernanceError, OSError)):
            operations.transact(self.root, changes,
                                operations.versions(self.root, changes, operation="lifecycle"),
                                operation="lifecycle", authorized=True)
        self.assertEqual(self.workspace.snapshot(include_recovery=True), before)

    def test_unresolved_conflict_cannot_be_cleared_even_with_valid_approval(self):
        text = self.path.read_text(encoding="utf-8")
        conflicts = json.loads(lint.metadata(text)["conflicts"])
        conflicts[0]["resolution"] = None
        self.workspace.write(self.relative, governance.replace_field(text, "conflicts", json.dumps(conflicts)))
        ref = self.approval()
        self.assert_invalid_approval_across_public_boundaries(ref)

    def test_new_wiki_creation_cannot_import_non_draft_lifecycle_history(self):
        relative = "wiki/imported-history.md"
        ref = self.approval("experiments/imported-history-approval.md", target=relative)
        proposed = self.proposal(ref)
        changes = {relative: proposed.encode("utf-8")}
        before = self.workspace.snapshot(include_recovery=True)
        with self.assertRaisesRegex(governance.GovernanceError, "LIFECYCLE_CREATION_REQUIRES_DRAFT"):
            operations.transact(self.root, changes,
                                operations.versions(self.root, changes, operation="wiki"),
                                operation="wiki", authorized=True)
        self.assertEqual(self.workspace.snapshot(include_recovery=True), before)
        self.assertFalse((self.root / relative).exists())
        with self.assertRaises(governance.GovernanceError):
            operations.transact(self.root, changes,
                                operations.versions(self.root, changes, operation="lifecycle"),
                                operation="lifecycle", authorized=True)
        self.assertEqual(self.workspace.snapshot(include_recovery=True), before)

    def test_revoked_pending_and_unauthorized_records_are_rejected_everywhere(self):
        for overrides in ({"Status": "REVOKED"}, {"Status": "PENDING"}, {"authority": "ai"}):
            with self.subTest(overrides=overrides):
                self.assert_invalid_approval_across_public_boundaries(self.approval(**overrides))

    def test_wrong_subject_hash_or_date_are_rejected_everywhere(self):
        for overrides in ({"target": "wiki/other.md"}, {"content_hash": "sha256:" + "0" * 64},
                          {"validated_at": "2026-10-17"}):
            with self.subTest(overrides=overrides):
                self.assert_invalid_approval_across_public_boundaries(self.approval(**overrides))

    def test_wrong_transition_or_history_prefix_is_rejected_everywhere(self):
        for overrides in ({"from_state": "unverified"}, {"to_state": "verified"},
                          {"prior_transitions_hash": "sha256:" + "0" * 64}):
            with self.subTest(overrides=overrides):
                self.assert_invalid_approval_across_public_boundaries(self.approval(**overrides))

    def test_malformed_or_wrong_event_binding_is_rejected_by_all_consumers(self):
        ref = self.approval()
        original = self.path.read_bytes()
        for change in ({"approval_content_hash": "sha256:" + "0" * 64},
                       {"approval_policy": "2"}, {"approval_content_hash": None}):
            with self.subTest(change=change):
                proposed = self.proposal(ref)
                events = json.loads(lint.metadata(proposed)["transitions"])
                events[-1].update(change)
                proposed = governance.replace_field(proposed, "transitions", json.dumps(events))
                before = self.workspace.snapshot()
                with self.assertRaises((governance.GovernanceError, OSError)):
                    self.direct_write(proposed)
                self.assertEqual(self.workspace.snapshot(), before)
                with self.assertRaises((governance.GovernanceError, OSError)):
                    governance.read_page(self.root, self.path, proposed)
                try:
                    self.workspace.write(self.relative, proposed)
                    result = query.search(self.root, "Approval boundary", "global")
                    self.assertEqual(result["status"], "INVALID_DATA")
                    self.assertEqual(result["matches"], [])
                    self.assertTrue(self.lint_errors())
                finally:
                    self.path.write_bytes(original)

    def test_expired_or_revoked_before_event_is_rejected_everywhere(self):
        for overrides in ({"expires_at": "2026-10-17"}, {"revoked_at": "2026-10-17"}):
            with self.subTest(overrides=overrides):
                self.assert_invalid_approval_across_public_boundaries(self.approval(**overrides))

    def test_valid_resolution_is_consistent_across_public_boundaries(self):
        ref = self.approval()
        proposed = self.proposal(ref)
        record = governance.read_page(self.root, self.path, proposed)
        self.assertEqual(record["status"], "unverified")
        before = self.path.read_bytes()
        planned = governance.transition(self.root, self.relative, "unverified", actor="human", at=DAY,
                                        reason="TEST_ONLY boundary transition", approval_ref=ref)
        self.assertEqual(self.path.read_bytes(), before)
        self.assert_metadata_equal(planned, proposed)
        self.assertEqual(self.direct_write(proposed)["status"], "COMMITTED")
        self.assertEqual(governance.read_page(self.root, self.path)["status"], "unverified")
        result = query.search(self.root, "Approval boundary", "global")
        self.assertEqual(result["status"], "FOUND")
        self.assertEqual(result["matches"][0]["knowledge_status"], "unverified")
        self.assertFalse(result["matches"][0]["usable_as_current_truth"])
        self.assertEqual(self.lint_errors(), [])

    def test_valid_helper_application_matches_direct_transaction(self):
        ref = self.approval()
        proposed = self.proposal(ref)
        actual = governance.transition(self.root, self.relative, "unverified", actor="human", at=DAY,
                                       reason="TEST_ONLY boundary transition", approval_ref=ref,
                                       authorized=True, apply=True)
        self.assert_metadata_equal(actual, proposed)
        self.assertEqual(self.path.read_text(encoding="utf-8"), actual)
        self.assertEqual(self.lint_errors(), [])

    def test_approval_cannot_be_replayed_for_a_later_resolution_cycle(self):
        ref = self.approval()
        self.direct_write(self.proposal(ref))
        self.workspace.move(self.relative, "disputed")
        self.assert_invalid_approval_across_public_boundaries(ref)

    def test_controlled_revision_keeps_old_approvals_without_rebinding_them(self):
        self.direct_write(self.proposal(self.approval()))
        old_ref = self.approval("experiments/first-verification.md", from_state="unverified", to_state="verified")
        self.workspace.move(self.relative, "verified", actor="human", approval_ref=old_ref)
        old_record = (self.root / old_ref).read_bytes()
        self.workspace.move(self.relative, "unverified")
        self.workspace.move(self.relative, "draft")
        revised = self.path.read_text(encoding="utf-8").replace(
            "TEST_ONLY synthetic policy.", "TEST_ONLY revised synthetic policy.")
        self.assertNotEqual(governance.content_hash(revised), governance.content_hash(
            self.path.read_text(encoding="utf-8")))
        changes = {self.relative: revised.encode("utf-8")}
        operations.transact(self.root, changes, operations.versions(self.root, changes), authorized=True)
        self.workspace.move(self.relative, "unverified")
        new_ref = self.approval("experiments/revised-verification.md", from_state="unverified", to_state="verified")
        self.workspace.move(self.relative, "verified", actor="human", approval_ref=new_ref)
        self.assertEqual((self.root / old_ref).read_bytes(), old_record)
        self.assertEqual(governance.read_page(self.root, self.path)["status"], "verified")
        self.assertEqual(self.lint_errors(), [])
        result = query.search(self.root, "Approval boundary", "global")
        self.assertEqual(result["status"], "FOUND")
        self.assertTrue(result["matches"][0]["usable_as_current_truth"])

    def assert_later_restriction_preserves_history_but_blocks_current_truth(self, field):
        self.direct_write(self.proposal(self.approval()))
        ref = self.approval("experiments/verification-approval.md", from_state="unverified",
                            to_state="verified", **{field: "2026-10-19"})
        self.workspace.move(self.relative, "verified", actor="human", approval_ref=ref)
        before = self.workspace.snapshot(include_recovery=True)
        original = query.search(self.root, "Approval boundary", "global")
        self.assertEqual(original["status"], "FOUND")
        self.assertTrue(original["matches"][0]["usable_as_current_truth"])

        class LaterDate(date):
            @classmethod
            def today(cls):
                return cls(2026, 10, 20)

        with patch.object(governance, "date", LaterDate):
            record = governance.read_page(self.root, self.path, today=LaterDate.today())
            self.assertEqual(record["status"], "verified")
            self.assertTrue(record["freshness"])
            result = query.search(self.root, "Approval boundary", "global", include_history=True)
            self.assertEqual(result["status"], "FOUND")
            self.assertFalse(result["matches"][0]["usable_as_current_truth"])
            self.assertEqual(self.lint_errors(), [])
        self.assertEqual(self.workspace.snapshot(include_recovery=True), before)

    def test_later_expiry_preserves_history_but_blocks_current_truth(self):
        self.assert_later_restriction_preserves_history_but_blocks_current_truth("expires_at")

    def test_later_revocation_preserves_history_but_blocks_current_truth(self):
        self.assert_later_restriction_preserves_history_but_blocks_current_truth("revoked_at")

    def test_absent_independent_evidence_is_rejected_everywhere(self):
        for evidence in ("[]", '["reports/missing-proof.md"]',
                         '["experiments/resolution-approval.md"]'):
            with self.subTest(evidence=evidence):
                self.assert_invalid_approval_across_public_boundaries(self.approval(evidence=evidence))

    def test_duplicate_approval_fields_are_rejected_everywhere(self):
        ref = self.approval()
        path = self.root / ref
        path.write_bytes(path.read_bytes() + b"- authority: ai\n")
        self.assert_invalid_approval_across_public_boundaries(ref)

    def test_unauthorized_actor_rejects_helper_writer_reader_query_and_lint(self):
        ref = self.approval()
        proposed = self.proposal(ref, actor="ai")
        before = self.workspace.snapshot()
        with self.assertRaisesRegex(governance.GovernanceError, "HUMAN_AUTHORITY_REQUIRED"):
            governance.transition(self.root, self.relative, "unverified", actor="ai", at=DAY,
                                  reason="TEST_ONLY unauthorized actor", approval_ref=ref,
                                  authorized=True, apply=True)
        with self.assertRaisesRegex(governance.GovernanceError, "HUMAN_AUTHORITY_REQUIRED"):
            self.direct_write(proposed)
        with self.assertRaisesRegex(governance.GovernanceError, "HUMAN_AUTHORITY_REQUIRED"):
            governance.read_page(self.root, self.path, proposed)
        self.assertEqual(self.workspace.snapshot(), before)
        self.workspace.write(self.relative, proposed)
        result = query.search(self.root, "Approval boundary", "global")
        self.assertEqual(result["status"], "INVALID_DATA")
        self.assertEqual(result["matches"], [])
        self.assertTrue(any("HUMAN_AUTHORITY_REQUIRED" in error for error in self.lint_errors()))

    def test_illegal_history_rejects_helper_writer_reader_query_and_lint(self):
        ref = self.approval()
        proposed = self.proposal(ref, target="verified")
        before = self.workspace.snapshot()
        with self.assertRaisesRegex(governance.GovernanceError, "ILLEGAL_TRANSITION"):
            governance.transition(self.root, self.relative, "verified", actor="human", at=DAY,
                                  reason="TEST_ONLY illegal jump", approval_ref=ref,
                                  authorized=True, apply=True)
        with self.assertRaisesRegex(governance.GovernanceError, "ILLEGAL_TRANSITION"):
            self.direct_write(proposed)
        with self.assertRaisesRegex(governance.GovernanceError, "ILLEGAL_TRANSITION"):
            governance.read_page(self.root, self.path, proposed)
        self.assertEqual(self.workspace.snapshot(), before)
        self.workspace.write(self.relative, proposed)
        result = query.search(self.root, "Approval boundary", "global")
        self.assertEqual(result["status"], "INVALID_DATA")
        self.assertEqual(result["matches"], [])
        self.assertTrue(any("ILLEGAL_TRANSITION" in error for error in self.lint_errors()))


if __name__ == "__main__":
    unittest.main()
