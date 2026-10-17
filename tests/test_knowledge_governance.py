"""Synthetic Phase 2 workflows; human approvals here are TEST_ONLY simulations."""
from datetime import date
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts import check_workspace as checker
from scripts import knowledge_governance as governance
from scripts import query_workspace as query
from scripts import source_integrity as integrity

SID1, SID2 = "SRC-20261017-301", "SRC-20261017-302"
DAY = "2026-10-17"


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).absolute().parent
        temporary = tempfile.TemporaryDirectory(prefix="fixture-governance-", dir=parent)
        if not Path(temporary.name).is_relative_to(parent):
            raise AssertionError("fixture escaped tests/")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "workspace"
        self.root.mkdir()
        self.write("sources/manifest.csv", ",".join(checker.MANIFEST_FIELDS) + "\n")
        self.write("wiki/index.md", "# TEST_ONLY Index\n")
        self.write("wiki/log.md", "# TEST_ONLY Log\n")
        self.write("reports/proof.md", "# TEST_ONLY simulated validation evidence\n")
        for sid in (SID1, SID2):
            raw = "sources/raw/" + sid + ".txt"
            integrity.create_raw_snapshot(self.root, raw, ("TEST_ONLY " + sid).encode(), authorized=True)
            row = dict(zip(checker.MANIFEST_FIELDS, (
                sid, "TEST_ONLY source", "synthetic_fixture", raw, "", "", DAY,
                "Synthetic tests only", "Unknown author and publication date.",
            )))
            integrity.register_source(self.root, row, authorized=True)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def page(self, relative="wiki/topic.md", **overrides):
        fields = {
            "Status": "draft", "kind": "external_fact", "Scope": "sample-a",
            "created_at": DAY, "updated_at": DAY, "temporal": "current",
            "review_after": "2099-12-31", "transitions": "[]", "Source IDs": SID1,
            "keywords": '["Fixture policy"]',
        }
        fields.update(overrides)
        text = "# Fixture policy\n" + "".join("- **" + k + ":** " + v + "\n" for k, v in fields.items())
        text += "\n## Summary\nUNKNOWN: TEST_ONLY fixture, never production knowledge.\n"
        text += "\n## Verified findings\n- FACT: TEST_ONLY policy. [" + SID1 + ", section 1]\n"
        self.write(relative, text)
        return relative

    def change(self, relative, name, value):
        path = self.root / relative
        text = governance.replace_field(path.read_text(encoding="utf-8"), name, value)
        path.write_text(text, encoding="utf-8")

    def move(self, relative, target, actor="ai", **kwargs):
        return governance.transition(self.root, relative, target, actor=actor, at=DAY,
                                     reason="TEST_ONLY documented workflow", authorized=True, apply=True, **kwargs)

    def approval(self, relative):
        path = self.root / relative
        ref = "experiments/" + path.stem + "-approval.md"
        self.write(ref, "# TEST_ONLY human approval simulation\n"
                   "- Status: APPROVED\n- authority: human\n- target: " + relative
                   + "\n- content_hash: " + governance.content_hash(path.read_text(encoding="utf-8"))
                   + "\n- validated_at: " + DAY + '\n- evidence: ["reports/proof.md"]\n')
        return ref

    def verified(self, relative="wiki/topic.md", **overrides):
        self.page(relative, **overrides)
        self.move(relative, "unverified")
        self.move(relative, "verified", actor="human", approval_ref=self.approval(relative))
        return relative

    def record(self, relative="wiki/topic.md", **kwargs):
        return governance.read_page(self.root, self.root / relative, **kwargs)

    def errors(self):
        return {s.split()[1] for s in checker.check_workspace(self.root, integrity=True) if s.startswith("ERROR ")}

    def test_01_valid_lifecycle_transitions_are_traceable(self):
        relative = self.verified()
        events = checker.metadata((self.root / relative).read_text(encoding="utf-8"))["transitions"]
        self.assertEqual([e["to"] for e in json.loads(events)], ["unverified", "verified"])
        self.assertEqual(self.record()["status"], "verified")
        self.assertEqual(self.errors(), set())
        self.move(relative, "unverified")
        self.assertEqual(self.record()["status"], "unverified")

    def test_02_invalid_transitions_do_not_write(self):
        relative = self.page()
        before = (self.root / relative).read_bytes()
        for target in ("verified", "superseded", "disputed", "invented"):
            with self.subTest(target=target), self.assertRaises(governance.GovernanceError):
                self.move(relative, target, actor="human")
        self.assertEqual((self.root / relative).read_bytes(), before)

    def test_03_ai_cannot_verify_even_with_approval_or_model_agreement(self):
        relative = self.page()
        self.move(relative, "unverified")
        before = (self.root / relative).read_bytes()
        with self.assertRaisesRegex(governance.GovernanceError, "HUMAN_AUTHORITY_REQUIRED"):
            self.move(relative, "verified", approval_ref=self.approval(relative))
        self.assertEqual((self.root / relative).read_bytes(), before)
        events = json.loads(checker.metadata(before.decode())["transitions"])
        events.append({"from": "unverified", "to": "verified", "actor": "ai", "at": DAY,
                       "reason": "TEST_ONLY two models agree", "approval": None})
        self.change(relative, "transitions", json.dumps(events))
        self.change(relative, "status", "verified")
        self.assertIn("HUMAN_AUTHORITY_REQUIRED", self.errors())
        self.assertEqual(query.search(self.root, "Fixture policy", "sample-a")["status"], "INVALID_DATA")

    def test_04_superseded_decision_is_never_current_truth(self):
        old = self.verified("decisions/old.md", kind="approved_decision")
        new = self.verified("decisions/new.md", kind="approved_decision")
        self.move(old, "superseded", actor="human", superseded_by=new)
        result = query.search(self.root, "Fixture policy", "sample-a")
        self.assertEqual([p["path"] for p in result["matches"]], [new])
        historic = query.search(self.root, "Fixture policy", "sample-a", include_history=True)
        record = next(p for p in historic["matches"] if p["path"] == old)
        self.assertFalse(record["usable_as_current_truth"])
        self.assertEqual(record["decision_authority"], "historical")
        self.assertEqual(record["superseded_by"], new)
        self.assertEqual(self.errors(), set())

    def test_05_historical_fact_retrieval_does_not_expire_by_age(self):
        relative = self.verified(temporal="historical", created_at="2001-01-01", review_after="")
        record = self.record(today=date(2099, 1, 1))
        self.assertNotIn("REVIEW_DUE", record["freshness"])
        result = query.search(self.root, "Fixture policy", "sample-a")
        self.assertEqual(result["status"], "FOUND")
        self.assertFalse(result["matches"][0]["usable_as_current_truth"])
        self.assertEqual(self.record()["status"], "verified")

    def test_06_conflicting_sources_preserved_and_block_verified(self):
        conflicts = json.dumps([{"summary": "TEST_ONLY incompatible results", "source_ids": [SID1, SID2], "resolution": None}])
        relative = self.page(conflicts=conflicts, **{"Source IDs": SID1 + ", " + SID2})
        path = self.root / relative
        path.write_text(path.read_text(encoding="utf-8") + "- FACT: TEST_ONLY alternate policy. [" + SID2 + ", section 2]\n", encoding="utf-8")
        self.move(relative, "unverified")
        self.move(relative, "disputed")
        result = query.search(self.root, "Fixture policy", "sample-a")
        self.assertEqual(result["status"], "DISPUTED")
        self.assertEqual(result["matches"], [])
        self.assertEqual({c["source_id"] for c in result["blocked"][0]["citations"]}, {SID1, SID2})
        self.assertEqual(result["blocked"][0]["conflicts"][0]["source_ids"], [SID1, SID2])
        with self.assertRaises(governance.GovernanceError):
            self.move(relative, "verified", actor="human", approval_ref=self.approval(relative))
        with self.assertRaisesRegex(governance.GovernanceError, "UNRESOLVED_CONFLICT"):
            self.move(relative, "unverified", actor="human", approval_ref=self.approval(relative))

    def test_07_incorrect_project_scope_has_no_fallback_or_alias_leak(self):
        self.verified("wiki/other.md", Scope="arbitrary-project-92", aliases_vi='["chính sách khác"]')
        result = query.search(self.root, "chính sách khác", "sample-a")
        self.assertEqual(result["status"], "NOT_FOUND")
        self.assertEqual(result["expanded_terms"], [])
        self.page("wiki/projects/sample-a/bad.md", Scope="arbitrary-project-92")
        self.assertIn("PROJECT_SCOPE_MISMATCH", self.errors())

    def test_08_explicit_cross_project_lookup_is_context_only(self):
        foreign = self.verified("wiki/other.md", Scope="arbitrary-project-92", aliases_vi='["chính sách khác"]')
        self.page(cross_project_refs=json.dumps([foreign]))
        self.assertEqual(query.search(self.root, "chính sách khác", "sample-a")["status"], "NOT_FOUND")
        result = query.search(self.root, "chính sách khác", "sample-a", cross_refs=[foreign])
        self.assertEqual(result["status"], "FOUND")
        self.assertEqual(result["matches"][0]["scope"], "arbitrary-project-92")
        self.assertTrue(result["matches"][0]["cross_project_context"])
        self.assertFalse(result["matches"][0]["usable_as_current_truth"])
        self.assertEqual(query.search(self.root, "Fixture policy", "not-the-anchor", cross_refs=[foreign])["status"], "ACCESS_DENIED")

    def test_09_proposed_decision_cannot_become_approved_by_citation(self):
        relative = self.page("decisions/proposal.md", kind="proposed_decision")
        self.move(relative, "unverified")
        with self.assertRaisesRegex(governance.GovernanceError, "KIND_CANNOT_BE_VERIFIED"):
            self.move(relative, "verified", actor="human", approval_ref=self.approval(relative))
        proposal = query.search(self.root, "Fixture policy", "sample-a")["matches"][0]
        self.assertEqual(proposal["decision_authority"], "proposed")
        self.assertFalse(proposal["usable_as_current_truth"])
        approved = self.verified("decisions/approved.md", kind="approved_decision")
        self.assertEqual(self.record(approved)["decision_authority"], "approved")

    def test_10_missing_or_inconsistent_metadata_fails_closed(self):
        relative = self.page()
        original = (self.root / relative).read_text(encoding="utf-8")
        for field, value in (("created_at", ""), ("updated_at", "2000-01-01"),
                             ("scope", ""), ("kind", "random"), ("transitions", "{}"),
                             ("status", "verified")):
            with self.subTest(field=field):
                self.write(relative, original)
                self.change(relative, field, value)
                self.assertTrue(self.errors())
                self.assertEqual(query.search(self.root, "Fixture policy", "sample-a")["matches"], [])

    def test_verified_body_or_scope_edit_invalidates_approval(self):
        relative = self.verified()
        path = self.root / relative
        path.write_text(path.read_text(encoding="utf-8").replace("TEST_ONLY policy.", "TEST_ONLY changed."), encoding="utf-8")
        self.assertIn("INVALID_HUMAN_APPROVAL", self.errors())
        self.assertEqual(query.search(self.root, "Fixture policy", "sample-a")["status"], "INVALID_DATA")

    def test_human_label_without_validation_record_is_insufficient(self):
        relative = self.page()
        self.move(relative, "unverified")
        with self.assertRaisesRegex(governance.GovernanceError, "HUMAN_APPROVAL_REQUIRED"):
            self.move(relative, "verified", actor="human")
        approval = self.approval(relative)
        path = self.root / approval
        path.write_text(path.read_text(encoding="utf-8").replace('["reports/proof.md"]', "[]"), encoding="utf-8")
        with self.assertRaisesRegex(governance.GovernanceError, "VALIDATION_EVIDENCE_REQUIRED"):
            self.move(relative, "verified", actor="human", approval_ref=approval)

    def test_restricted_scope_requires_explicit_authorization(self):
        foreign = self.verified("wiki/restricted.md", Scope="sample-b", access="restricted")
        self.page(cross_project_refs=json.dumps([foreign]))
        self.assertEqual(query.search(self.root, "Fixture policy", "sample-b")["status"], "NOT_FOUND")
        self.assertEqual(query.search(self.root, "Fixture policy", "sample-a", cross_refs=[foreign])["status"], "ACCESS_DENIED")
        result = query.search(self.root, "Fixture policy", "sample-b", authorized_scopes=["sample-b"])
        self.assertEqual(result["status"], "FOUND")

    def test_global_knowledge_is_selected_explicitly(self):
        self.verified(Scope="global")
        self.assertEqual(query.search(self.root, "Fixture policy", "sample-a")["status"], "NOT_FOUND")
        self.assertEqual(query.search(self.root, "Fixture policy", "global")["status"], "FOUND")

    def test_review_due_is_warning_not_automatic_obsolescence(self):
        relative = self.verified(review_after="2026-01-01")
        result = query.search(self.root, "Fixture policy", "sample-a")
        self.assertEqual(result["status"], "FOUND")
        self.assertIn("REVIEW_DUE", result["matches"][0]["freshness"])
        self.assertFalse(result["matches"][0]["usable_as_current_truth"])
        self.assertEqual(self.record()["status"], "verified")

    def test_future_effective_policy_is_not_current(self):
        self.verified(effective_at="2099-12-31")
        self.assertEqual(query.search(self.root, "Fixture policy", "sample-a")["status"], "NOT_FOUND")
        result = query.search(self.root, "Fixture policy", "sample-a", include_history=True)
        self.assertIn("NOT_YET_EFFECTIVE", result["matches"][0]["freshness"])
        self.assertFalse(result["matches"][0]["usable_as_current_truth"])

    def test_legacy_reviewed_is_not_verified_and_bytes_are_unchanged(self):
        path = self.write("wiki/legacy.md", "# Legacy policy\n- Status: REVIEWED\n- Updated: " + DAY
                          + "\n- Source IDs: " + SID1 + "\n- Scope: sample-a\n\n## Summary\n"
                          + "- FACT: TEST_ONLY old policy. [" + SID1 + ", section 1]\n")
        before = path.read_bytes()
        record = self.record("wiki/legacy.md")
        self.assertTrue(record["legacy"])
        self.assertEqual(record["status"], "unverified")
        result = query.search(self.root, "Legacy policy", "sample-a")
        self.assertEqual(result["status"], "FOUND")
        self.assertFalse(result["matches"][0]["usable_as_current_truth"])
        self.assertEqual(path.read_bytes(), before)

    def test_interpretation_and_hypothesis_are_not_verified_facts(self):
        for kind in ("interpretation", "hypothesis"):
            with self.subTest(kind=kind):
                relative = self.page(kind=kind)
                self.move(relative, "unverified")
                with self.assertRaisesRegex(governance.GovernanceError, "KIND_CANNOT_BE_VERIFIED"):
                    self.move(relative, "verified", actor="human", approval_ref=self.approval(relative))

    def test_apply_requires_authorization_and_plan_is_read_only(self):
        relative = self.page()
        before = (self.root / relative).read_bytes()
        proposed = governance.transition(self.root, relative, "unverified", actor="ai", at=DAY, reason="TEST_ONLY plan")
        self.assertIn('"to": "unverified"', proposed)
        self.assertEqual((self.root / relative).read_bytes(), before)
        with self.assertRaises(PermissionError):
            governance.transition(self.root, relative, "unverified", actor="ai", at=DAY, reason="TEST_ONLY", apply=True)
        self.assertEqual((self.root / relative).read_bytes(), before)

    def test_archive_requires_human_and_history_is_opt_in(self):
        relative = self.verified()
        with self.assertRaisesRegex(governance.GovernanceError, "HUMAN_AUTHORITY_REQUIRED"):
            self.move(relative, "archived")
        self.move(relative, "archived", actor="human")
        self.assertEqual(query.search(self.root, "Fixture policy", "sample-a")["status"], "NOT_FOUND")
        self.assertEqual(query.search(self.root, "Fixture policy", "sample-a", include_history=True)["status"], "FOUND")
        self.move(relative, "draft", actor="human")
        self.assertEqual(self.record()["status"], "draft")

    def test_foreign_decision_is_context_not_local_configuration(self):
        foreign = self.verified("decisions/foreign.md", Scope="sample-b", kind="approved_decision")
        relative = self.page(cross_project_refs=json.dumps([foreign]))
        path = self.root / relative
        path.write_text(path.read_text(encoding="utf-8").replace(
            "[" + SID1 + ", section 1]", "[Foreign ADR](../" + foreign + ")"), encoding="utf-8")
        self.assertIn("MISSING_CITATION", self.errors())
        self.assertEqual(query.search(self.root, "Fixture policy", "sample-a")["status"], "INVALID_DATA")

    def test_conflict_resolution_needs_human_validation_then_reverification(self):
        conflict = {"summary": "TEST_ONLY conflict", "source_ids": [SID1, SID2], "resolution": None}
        relative = self.page(conflicts=json.dumps([conflict]), **{"Source IDs": SID1 + ", " + SID2})
        self.move(relative, "unverified")
        self.move(relative, "disputed")
        conflict["resolution"] = "TEST_ONLY validation evidence reviewed by the simulated human"
        self.change(relative, "conflicts", json.dumps([conflict]))
        with self.assertRaisesRegex(governance.GovernanceError, "HUMAN_AUTHORITY_REQUIRED"):
            self.move(relative, "unverified", approval_ref=self.approval(relative))
        self.move(relative, "unverified", actor="human", approval_ref=self.approval(relative))
        self.move(relative, "verified", actor="human", approval_ref=self.approval(relative))
        self.assertEqual(self.record()["status"], "verified")
        self.assertEqual(self.record()["conflicts"][0]["source_ids"], [SID1, SID2])

    def test_same_scope_approved_decision_can_support_a_project_choice(self):
        decision = self.verified("decisions/local.md", kind="approved_decision")
        relative = self.page(kind="requirement", **{"Source IDs": "None"})
        path = self.root / relative
        path.write_text(path.read_text(encoding="utf-8").replace(
            "[" + SID1 + ", section 1]", "[Local ADR](../" + decision + ")"), encoding="utf-8")
        self.move(relative, "unverified")
        self.move(relative, "verified", actor="human", approval_ref=self.approval(relative))
        self.assertEqual(self.errors(), set())
        result = query.search(self.root, "Fixture policy", "sample-a")
        wiki = next(p for p in result["matches"] if p["path"] == relative)
        self.assertEqual(wiki["citations"][0]["decision_path"], decision)
        self.assertEqual(wiki["information_type"], "requirement")

    def test_malformed_history_and_mixed_metadata_are_rejected(self):
        relative = self.page()
        original = (self.root / relative).read_text(encoding="utf-8")
        for target in (["verified"], None, {"state": "verified"}):
            with self.subTest(target=target):
                self.write(relative, original)
                self.change(relative, "transitions", json.dumps([{
                    "from": "draft", "to": target, "actor": "ai", "at": DAY,
                    "reason": "TEST_ONLY malformed", "approval": None,
                }]))
                self.assertEqual(query.search(self.root, "Fixture policy", "sample-a")["status"], "INVALID_DATA")
        self.write(relative, original.replace("## Summary", "- Updated: " + DAY + "\n## Summary"))
        self.assertIn("MIXED_METADATA", self.errors())

    def test_unapproved_historical_label_does_not_create_decision_evidence(self):
        relative = self.page(kind="historical_decision", temporal="historical", reviewed_at=DAY)
        self.assertEqual(self.record()["decision_authority"], "unapproved")
        result = query.search(self.root, "Fixture policy", "sample-a", include_history=True)
        self.assertTrue(all(c.get("evidence_type") != "project_decision" for c in result["matches"][0]["citations"]))

    def test_source_tampering_still_blocks_governed_verified_knowledge(self):
        self.verified()
        raw = self.root / ("sources/raw/" + SID1 + ".txt")
        raw.write_bytes(b"TEST_ONLY simulated external tamper")
        result = query.search(self.root, "Fixture policy", "sample-a")
        self.assertEqual(result["status"], "MISSING_EVIDENCE")
        self.assertFalse(result["blocked"][0]["usable_as_current_truth"])

    def test_decision_approval_cannot_bypass_a_tampered_supporting_source(self):
        self.verified("decisions/local.md", kind="approved_decision")
        raw = self.root / ("sources/raw/" + SID1 + ".txt")
        raw.write_bytes(b"TEST_ONLY tampered supporting bytes")
        self.assertEqual(query.search(self.root, "Fixture policy", "sample-a")["status"], "MISSING_EVIDENCE")

    def test_governed_decision_source_references_are_validated(self):
        relative = self.verified("decisions/local.md", kind="approved_decision")
        path = self.root / relative
        path.write_text(path.read_text(encoding="utf-8").replace(SID1, "SRC-20261017-999"), encoding="utf-8")
        self.assertIn("UNKNOWN_SOURCE", self.errors())
        self.assertEqual(query.search(self.root, "Fixture policy", "sample-a")["status"], "INVALID_DATA")

    def test_referenced_decision_cannot_hide_a_changed_supporting_source(self):
        decision = self.verified("decisions/local.md", kind="approved_decision")
        relative = self.page(**{"Source IDs": "None"})
        path = self.root / relative
        path.write_text(path.read_text(encoding="utf-8").replace(
            "[" + SID1 + ", section 1]", "[Local ADR](../" + decision + ")"), encoding="utf-8")
        self.change(relative, "keywords", '["Local project policy"]')
        raw = self.root / ("sources/raw/" + SID1 + ".txt")
        raw.write_bytes(b"TEST_ONLY tampered source of referenced ADR")
        self.assertEqual(query.search(self.root, "Local project policy", "sample-a")["status"], "MISSING_EVIDENCE")

    def test_first_party_choice_without_external_fact_uses_approval_evidence(self):
        relative = self.page("decisions/local.md", kind="approved_decision", **{"Source IDs": "None"})
        path = self.root / relative
        text = path.read_text(encoding="utf-8").replace(
            "- FACT: TEST_ONLY policy. [" + SID1 + ", section 1]",
            "- FACT: TEST_ONLY project chose the documented option.")
        path.write_text(text, encoding="utf-8")
        self.move(relative, "unverified")
        self.move(relative, "verified", actor="human", approval_ref=self.approval(relative))
        self.assertEqual(self.errors(), set())
        result = query.search(self.root, "Fixture policy", "sample-a")
        self.assertEqual(result["matches"][0]["citations"][0]["evidence_type"], "project_decision")

    def test_query_and_audit_are_read_only(self):
        self.verified()
        def snapshot():
            return {p.relative_to(self.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in self.root.rglob("*") if p.is_file()}
        before = snapshot()
        query.search(self.root, "Fixture policy", "sample-a")
        governance.audit_governance(self.root)
        checker.check_workspace(self.root, integrity=True)
        self.assertEqual(snapshot(), before)
