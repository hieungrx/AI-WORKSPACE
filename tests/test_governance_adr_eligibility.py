"""H-GOV-01 regression through public APIs; only disposable TEST_ONLY data."""
import json
from datetime import date
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import check_workspace as lint
from scripts import knowledge_governance as governance
from scripts import query_workspace as query
from workflow_support import DAY, SID, Workspace


class AdrEligibilityTests(unittest.TestCase):
    scope = "synthetic-governance-project"

    def setUp(self):
        parent = Path(__file__).absolute().parent
        temporary = tempfile.TemporaryDirectory(prefix="fixture-adr-eligibility-", dir=parent)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "workspace"
        self.w = Workspace(self.root)

    def indexed(self, relative):
        index = self.root / "wiki/index.md"
        href = relative.removeprefix("wiki/") if relative.startswith("wiki/") else "../" + relative
        index.write_bytes(index.read_bytes() + ("[TEST_ONLY fixture](" + href + ")\n").encode())

    def adr(self, relative="decisions/choice.md", title="Fixture choice", *, dependency=None, **extra):
        fields = {"kind": "approved_decision", "temporal": "current", "review_after": "2099-12-31"}
        fields.update(extra)
        text = self.w.page(title=title, sources=(), claims=[], scope=self.scope, **fields)
        context = ""
        if dependency:
            href = Path(os.path.relpath(self.root / dependency, (self.root / relative).parent)).as_posix()
            context = " [Supporting decision](" + href + ")"
        self.w.write(relative, text + "- FACT: TEST_ONLY the project chose option A." + context + "\n")
        self.indexed(relative)
        self.w.verify(relative)
        return relative

    def claim(self, relative="wiki/claim.md", title="Fixture dependent", target="decisions/choice.md",
              *, source=False, separate_source_claim=False):
        sources = (SID,) if source or separate_source_claim else ()
        text = self.w.page(title=title, sources=sources, claims=[], scope=self.scope,
                           temporal="current", review_after="2099-12-31")
        base = self.root / relative
        href = Path(os.path.relpath(self.root / target, base.parent)).as_posix()
        pointer = " [" + SID + ", section Evidence]" if source else ""
        text += "- FACT: TEST_ONLY the active configuration uses option A." + pointer + " [Context](" + href + ")\n"
        if separate_source_claim:
            text += "- FACT: TEST_ONLY an independent observation about option B. [" + SID + ", section Evidence]\n"
        self.w.write(relative, text)
        self.indexed(relative)
        self.w.verify(relative)
        return relative

    def search(self, title="Fixture dependent", **kwargs):
        return query.search(self.root, title, self.scope, **kwargs)

    def record(self, result, relative):
        values = result["matches"] + result["blocked"]
        return next((item for item in values if item["path"] == relative), None)

    def issues(self):
        return lint.check_workspace(self.root, integrity=True, security=True)

    def assert_not_current(self, result):
        self.assertFalse(any(item["usable_as_current_truth"] for item in result["matches"] + result["blocked"]), result)

    def assert_dependency_flag(self, relative):
        self.assertTrue(any(relative + ":" in issue and issue.startswith(("WARNING ", "ERROR "))
                            for issue in self.issues()), "Lint did not expose the dependent record's ineligible evidence")

    def test_valid_effective_adr_authorizes_same_scope_current_claim(self):
        self.adr()
        relative = self.claim()
        result = self.search()
        self.assertEqual(result["status"], "FOUND")
        self.assertTrue(self.record(result, relative)["usable_as_current_truth"])
        self.assertEqual([issue for issue in self.issues() if issue.startswith("ERROR ")], [])
        direct = self.search("Fixture choice")
        self.assertEqual(direct["status"], "FOUND")
        self.assertTrue(direct["matches"][0]["usable_as_current_truth"])

    def test_future_effective_adr_is_context_not_parent_current_truth(self):
        self.adr(effective_at="2099-01-01")
        relative = self.claim()
        result = self.search()
        self.assertEqual(result["status"], "FOUND")
        self.assert_not_current(result)
        self.assert_dependency_flag(relative)
        self.assertEqual(self.search("Fixture choice")["status"], "NOT_FOUND")
        history = self.search("Fixture choice", include_history=True)
        self.assertEqual(history["status"], "FOUND")
        self.assert_not_current(history)

    def test_review_expired_adr_is_context_not_parent_current_truth(self):
        self.adr(review_after="2020-01-01")
        relative = self.claim()
        result = self.search()
        self.assertEqual(result["status"], "FOUND")
        self.assert_not_current(result)
        self.assert_dependency_flag(relative)
        direct = self.search("Fixture choice")
        self.assertEqual(direct["status"], "FOUND")
        self.assert_not_current(direct)
        self.assertEqual(governance.read_page(self.root, self.root / "decisions/choice.md")["status"], "verified")

    def test_temporally_historical_approved_adr_is_not_parent_current_truth(self):
        self.adr(temporal="historical")
        relative = self.claim()
        result = self.search()
        self.assertEqual(result["status"], "FOUND")
        self.assert_not_current(result)
        self.assert_dependency_flag(relative)
        self.assertEqual(self.search("Fixture choice")["status"], "FOUND")

    def test_historical_decision_kind_is_preserved_in_explicit_history(self):
        self.adr(kind="historical_decision", temporal="historical")
        self.claim()
        result = self.search(include_history=True)
        self.assertEqual(result["status"], "FOUND")
        self.assert_not_current(result)
        direct = self.search("Fixture choice", include_history=True)
        self.assertEqual(direct["status"], "FOUND")
        self.assert_not_current(direct)

    def test_superseded_adr_supports_history_not_current_truth(self):
        old = self.adr()
        successor = self.adr("decisions/new-choice.md", title="Fixture successor")
        self.w.move(old, "superseded", actor="human", superseded_by=successor)
        relative = self.claim()
        history = self.search(include_history=True)
        self.assertEqual(history["status"], "FOUND")
        self.assert_not_current(history)
        self.assert_dependency_flag(relative)
        direct = self.search("Fixture choice", include_history=True)
        self.assertEqual(direct["status"], "FOUND")
        self.assertEqual(self.record(direct, old)["superseded_by"], successor)
        self.assert_not_current(direct)

    def test_missing_adr_fails_closed_and_lint_reports_error(self):
        self.adr()
        relative = self.claim()
        (self.root / "decisions/choice.md").unlink()  # Disposable synthetic fixture, never a workspace source.
        result = self.search()
        self.assert_not_current(result)
        self.assertNotEqual(result["status"], "FOUND")
        self.assertTrue(any(issue.startswith("ERROR ") and relative in issue for issue in self.issues()))

    def test_draft_adr_approval_label_does_not_establish_authority(self):
        self.adr()
        self.w.move("decisions/choice.md", "unverified")
        self.claim()
        result = self.search()
        self.assert_not_current(result)
        self.assertNotEqual(result["status"], "FOUND")

    def test_legacy_approved_label_is_not_canonical_current_evidence(self):
        self.w.write("decisions/legacy.md", "# TEST_ONLY legacy choice\n- Status: APPROVED\n"
                     "- Updated: " + DAY + "\n- Scope: " + self.scope + "\n- Source IDs: None\n"
                     "\n## Summary\nUNKNOWN: TEST_ONLY retained manual decision.\n")
        self.indexed("decisions/legacy.md")
        relative = self.claim(target="decisions/legacy.md")
        self.assert_not_current(self.search())
        self.assertTrue(any(issue.startswith("ERROR ") and relative in issue for issue in self.issues()))

    def test_independent_intact_source_for_same_claim_survives_ineligible_adr_context(self):
        self.w.register(body="TEST_ONLY independently validates configuration option A.")
        self.adr(effective_at="2099-01-01")
        relative = self.claim(source=True)
        result = self.search()
        self.assertEqual(result["status"], "FOUND")
        page = self.record(result, relative)
        self.assertTrue(page["usable_as_current_truth"])
        self.assertIn(SID, {item.get("source_id") for item in page["citations"]})

    def test_remediation_malformed_decision_metadata_is_linted_without_erasing_independent_source(self):
        self.w.register(body="TEST_ONLY independent source validates configuration option A.")
        variants = (("garbage", "TEST_ONLY invalid decision text"),
                    ("wiki", "[TEST_ONLY ordinary wiki](index.md)"),
                    ("http", "[TEST_ONLY remote pointer](https://example.invalid/decision)"))
        for label, references in variants:
            with self.subTest(metadata=label):
                relative = "wiki/metadata-" + label + ".md"
                title = "Fixture malformed metadata " + label
                text = self.w.page(title=title, scope=self.scope, temporal="current", review_after="2099-12-31",
                                   claims=[(SID, "TEST_ONLY configuration option A is independently supported.")])
                text = governance.replace_field(text, "Decision references", references)
                self.w.write(relative, text)
                self.indexed(relative)
                self.w.verify(relative)
                result = self.search(title)
                self.assertEqual(result["status"], "FOUND")
                page = self.record(result, relative)
                self.assertTrue(page["usable_as_current_truth"])
                self.assertIn(SID, {citation.get("source_id") for citation in page["citations"]})
                self.assertIn("UNAPPROVED_DECISION", page["eligibility_reasons"])
                self.assertTrue(any(issue.startswith("ERROR UNAPPROVED_DECISION ") and relative + ":" in issue
                                    for issue in self.issues()))

    def test_remediation_ineligible_adr_citation_is_explicit_context_alongside_independent_source(self):
        self.w.register(body="TEST_ONLY independently validates configuration option A.")
        adr = self.adr(effective_at="2099-01-01")
        relative = self.claim(source=True)
        result = self.search()
        self.assertEqual(result["status"], "FOUND")
        page = self.record(result, relative)
        self.assertTrue(page["usable_as_current_truth"])
        self.assertIn(SID, {citation.get("source_id") for citation in page["citations"]})
        context = next(citation for citation in page["citations"] if citation.get("decision_path") == adr)
        self.assertIs(context["context_only"], True)
        self.assertIs(context["eligible_for_current_truth"], False)
        self.assertIn("NOT_YET_EFFECTIVE", context["freshness"])
        self.assertIn("INELIGIBLE_DECISION_DEPENDENCY", page["eligibility_reasons"])

    def test_remediation_depth_guard_fails_closed_consistently_in_query_and_lint(self):
        leaf = self.adr()
        derived = self.adr("decisions/derived.md", title="Fixture derived ADR", dependency=leaf)
        relative = self.claim(target=derived)
        self.assertTrue(self.search()["matches"][0]["usable_as_current_truth"])
        # A deliberately tiny resource bound exercises the guard without constructing a large corpus.
        # This verifies fail-closed behavior, not the performance capacity of the default depth limit.
        with patch.object(governance, "MAX_DECISION_DEPTH", 2):
            result = self.search()
            self.assertEqual(result["status"], "MISSING_EVIDENCE")
            self.assert_not_current(result)
            self.assertIn("DECISION_EVIDENCE_LIMIT", self.record(result, relative)["eligibility_reasons"])
            self.assertTrue(any(issue.startswith("ERROR DECISION_EVIDENCE_LIMIT ") and relative + ":" in issue
                                for issue in self.issues()))

    def test_source_for_different_claim_does_not_mask_ineligible_adr_only_claim(self):
        self.w.register(body="TEST_ONLY observation of option B only, not option A.")
        self.adr(effective_at="2099-01-01")
        relative = self.claim(separate_source_claim=True)
        self.assert_not_current(self.search())
        self.assert_dependency_flag(relative)

    def test_adr_lifecycle_change_after_prior_query_is_not_cached_as_current(self):
        self.adr()
        successor = self.adr("decisions/new-choice.md", title="Fixture successor")
        self.claim()
        self.assertTrue(self.search()["matches"][0]["usable_as_current_truth"])
        self.w.move("decisions/choice.md", "superseded", actor="human", superseded_by=successor)
        result = self.search(include_history=True)
        self.assertEqual(result["status"], "FOUND")
        self.assert_not_current(result)

    def test_adr_review_deadline_crossing_recomputes_dependencies_without_index_rebuild(self):
        self.adr(review_after="2026-10-19")
        self.claim()
        with patch.object(governance, "date") as calendar:
            calendar.today.return_value = date(2026, 10, 18)
            self.assertTrue(self.search()["matches"][0]["usable_as_current_truth"])
            calendar.today.return_value = date(2026, 10, 20)
            self.assert_not_current(self.search())

    def test_ordinary_wiki_link_is_not_an_additional_source_of_authority(self):
        self.adr(effective_at="2099-01-01")
        middle = self.claim("wiki/middle.md", title="Fixture middle")
        derived = self.claim("wiki/derived.md", title="Fixture derived", target=middle)
        result = self.search("Fixture derived")
        self.assert_not_current(result)
        self.assertNotEqual(result["status"], "FOUND")
        self.assertTrue(any(issue.startswith("ERROR ") and derived in issue for issue in self.issues()))

    def test_derived_adr_chain_propagates_ineligible_support_to_wiki_claim(self):
        leaf = self.adr(effective_at="2099-01-01")
        derived_adr = self.adr("decisions/derived.md", title="Fixture derived ADR", dependency=leaf)
        relative = self.claim(target=derived_adr)
        result = self.search()
        self.assertEqual(result["status"], "FOUND")
        self.assert_not_current(result)
        self.assert_dependency_flag(relative)
        direct = self.search("Fixture derived ADR")
        self.assertEqual(direct["status"], "FOUND")
        self.assert_not_current(direct)

    def test_valid_derived_adr_chain_retrieves_traceable_current_evidence(self):
        leaf = self.adr()
        derived_adr = self.adr("decisions/derived.md", title="Fixture derived ADR", dependency=leaf)
        derived = self.claim("wiki/derived-claim.md", title="Fixture derived", target=derived_adr)
        result = self.search("Fixture derived")
        self.assertEqual(result["status"], "FOUND")
        page = self.record(result, derived)
        self.assertTrue(page["usable_as_current_truth"])
        self.assertTrue(page["citations"])
        self.assertEqual([issue for issue in self.issues() if issue.startswith("ERROR ")], [])

    def test_cyclic_adr_dependencies_never_authorize_current_truth_or_crash(self):
        # Provision both complete TEST_ONLY approval simulations at the fixture boundary.
        # This intentionally bypasses write-time checks to exercise hostile historical data.
        for relative, other, title in (("decisions/cycle-a.md", "cycle-b.md", "Cycle alpha"),
                                       ("decisions/cycle-b.md", "cycle-a.md", "Cycle beta")):
            events = [{"from": "draft", "to": "unverified", "actor": "ai", "at": DAY,
                       "reason": "TEST_ONLY initial state", "approval": None},
                      {"from": "unverified", "to": "verified", "actor": "human", "at": DAY,
                       "reason": "TEST_ONLY approval simulation", "approval": "experiments/" + Path(relative).stem + "-approval.md"}]
            text = self.w.page(title=title, sources=(), claims=[], scope=self.scope,
                               Status="verified", kind="approved_decision", temporal="current", review_after="2099-12-31",
                               reviewed_at=DAY, transitions=json.dumps(events))
            text += "- FACT: TEST_ONLY derived option A. [dependency](" + other + ")\n"
            self.w.write(relative, text)
            self.w.write(events[-1]["approval"], "# TEST_ONLY simulated approval\n- Status: APPROVED\n- authority: human\n"
                         "- target: " + relative + "\n- content_hash: " + governance.content_hash(text)
                         + "\n- validated_at: " + DAY + '\n- evidence: ["reports/validation.md"]\n')
            self.indexed(relative)
        result = self.search("Cycle alpha")
        self.assert_not_current(result)
        self.assertTrue(any(issue.startswith("ERROR ") and "cycle-a.md" in issue for issue in self.issues()))

    def test_actual_ingest_can_retain_independent_source_and_noncurrent_adr_context(self):
        self.w.register(body="TEST_ONLY independent source confirms queue size eight.")
        self.adr(effective_at="2099-01-01")
        text = self.w.page(title="Fixture ingested", scope=self.scope, temporal="current", review_after="2099-12-31",
                           claims=[(SID, "TEST_ONLY queue size is eight. [ADR context](../decisions/choice.md)")])
        result = self.w.apply("wiki/ingested.md", text=text, scope=self.scope)
        self.assertEqual(result["status"], "COMMITTED")
        self.w.verify("wiki/ingested.md")
        observed = self.search("Fixture ingested")
        self.assertEqual(observed["status"], "FOUND")
        self.assertTrue(observed["matches"][0]["usable_as_current_truth"])


if __name__ == "__main__":
    unittest.main()
