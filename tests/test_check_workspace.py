"""Regression tests with disposable fixtures; never modify real raw sources."""
from contextlib import redirect_stdout
import csv
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import check_workspace as checker


SID = "SRC-20261017-001"
REPO = Path(__file__).absolute().parents[1]


def page(status="DRAFT", sources="None", decision="None", findings="", summary="UNKNOWN: evidence gap."):
    return (
        f"# Fixture page\n\n- **Status:** {status}\n- **Updated:** 2026-10-17\n"
        f"- **Source IDs:** {sources}\n- **Decision references:** {decision}\n\n"
        f"## Summary\n{summary}\n\n## Verified findings\n{findings}\n\n"
        "## Related pages\n[Index](index.md)\n"
    )


class WorkspaceChecks(unittest.TestCase):
    def setUp(self):
        fixture_parent = Path(__file__).absolute().parent
        temporary = tempfile.TemporaryDirectory(prefix="fixture-", dir=fixture_parent)
        if not Path(temporary.name).absolute().is_relative_to(fixture_parent):
            raise AssertionError("fixture must remain inside tests/")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "workspace"
        self.root.mkdir()
        self.manifest([])
        self.write("wiki/index.md", "# Index\n[Topic](topic.md)\n")
        self.write("wiki/log.md", "# Fixture activity log\n")
        self.write("wiki/topic.md", page())

    def write(self, relative, content):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def manifest(self, rows):
        target = self.root / "sources/manifest.csv"
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=checker.MANIFEST_FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

    def source(self, **overrides):
        row = dict(zip(checker.MANIFEST_FIELDS, (
            SID, "Disposable fixture", "note", "sources/raw/reference.md",
            "Fixture author", "2026-10-17", "2026-10-17", "test fixture only", "",
        )))
        row.update(overrides)
        self.write("sources/raw/reference.md", "# Source\nSection 1: fixture claim.\n")
        self.manifest([row])
        return row

    def codes(self, level=None):
        return {item.split()[1] for item in checker.check_workspace(self.root)
                if level is None or item.startswith(level + " ")}

    def reviewed(self, **overrides):
        values = dict(status="REVIEWED", sources=SID, findings=f"- FACT: Fixture claim. [{SID}, section 1]")
        values.update(overrides)
        self.write("wiki/topic.md", page(**values))

    def test_empty_registry_allows_explicit_unverified_draft(self):
        self.assertEqual(self.codes("ERROR"), set())
        self.assertEqual(self.codes("WARNING"), {"NO_EVIDENCE"})

    def test_existing_starter_hypothesis_remains_valid(self):
        text = (REPO / "wiki/concepts/knowledge-system-principles.md").read_text(encoding="utf-8-sig")
        self.write("wiki/concepts/knowledge-system-principles.md", text)
        self.write("wiki/index.md", "# Index\n[Principles](concepts/knowledge-system-principles.md)\n")
        self.write("SCHEMA.md", "# Fixture schema\n")
        self.assertEqual(self.codes("ERROR"), set())

    def test_registered_source_and_finding_pass(self):
        self.source()
        self.reviewed()
        self.assertEqual(checker.check_workspace(self.root), [])

    def test_citations_can_continue_on_the_next_line(self):
        self.source()
        self.reviewed(findings=f"- FACT: Fixture claim.\n  [{SID}, section 1]")
        self.assertNotIn("MISSING_CITATION", self.codes())

    def test_structured_facts_require_citations_even_in_drafts(self):
        for finding in ("- FACT: Unsupported claim.", "- Unsupported verified finding."):
            with self.subTest(finding=finding):
                self.write("wiki/topic.md", page(findings=finding))
                self.assertIn("MISSING_CITATION", self.codes("ERROR"))

    def test_unknown_and_malformed_source_ids_are_reported(self):
        for sid, code in ((SID, "UNKNOWN_SOURCE"), ("SRC-20260230-001", "INVALID_SOURCE_ID"),
                          ("SRC-20261017-ABC", "INVALID_SOURCE_ID")):
            with self.subTest(sid=sid):
                self.write("wiki/topic.md", page(sources=sid))
                self.assertIn(code, self.codes("ERROR"))

    def test_cited_source_must_be_listed_in_page_metadata(self):
        self.source()
        self.reviewed(sources="None")
        self.assertIn("UNLISTED_SOURCE", self.codes("ERROR"))

    def test_each_finding_needs_its_own_citation(self):
        self.source()
        self.reviewed(findings=f"- FACT: Supported claim. [{SID}, section 1]\n\n- FACT: Unsupported claim.")
        self.assertIn("MISSING_CITATION", self.codes("ERROR"))

    def test_duplicate_manifest_ids_are_errors(self):
        row = self.source()
        self.manifest([row, row])
        self.assertIn("DUPLICATE_SOURCE", self.codes("ERROR"))

    def test_all_required_manifest_values_are_checked(self):
        for field in checker.REQUIRED_FIELDS:
            with self.subTest(field=field):
                self.source(**{field: ""})
                self.assertIn("MISSING_SOURCE_VALUE", self.codes("ERROR"))

    def test_bad_manifest_header_and_row_shape_are_errors(self):
        for content, code in (
            ("source_id,title\n", "MANIFEST_HEADER"),
            (",".join(checker.MANIFEST_FIELDS) + "\nonly,two\n", "MANIFEST_ROW"),
            (",".join(checker.MANIFEST_FIELDS) + "\n" + ",".join(["x"] * 10) + "\n", "MANIFEST_ROW"),
        ):
            with self.subTest(code=code, content=content):
                self.write("sources/manifest.csv", content)
                self.assertIn(code, self.codes("ERROR"))

    def test_missing_and_unreadable_manifests_are_reported_without_tracebacks(self):
        target = self.root / "sources/manifest.csv"
        target.unlink()
        self.assertIn("MANIFEST_READ", self.codes("ERROR"))
        target.write_bytes(b"\xff\xfe")
        self.assertIn("MANIFEST_READ", self.codes("ERROR"))

    def test_source_dates_and_id_dates_are_real_calendar_dates(self):
        for field, value, code in (
            ("source_id", "SRC-20260230-001", "INVALID_SOURCE_ID"),
            ("retrieved_date", "2026-02-30", "INVALID_SOURCE_DATE"),
            ("published_date", "20261017", "INVALID_SOURCE_DATE"),
        ):
            with self.subTest(field=field):
                self.source(**{field: value})
                self.assertIn(code, self.codes("ERROR"))

    def test_unknown_author_or_publication_date_needs_an_explanatory_note(self):
        self.source(author="", published_date="")
        self.assertIn("SOURCE_GAP", self.codes("WARNING"))
        self.source(author="", published_date="", notes="Author and publication date unknown.")
        self.assertNotIn("SOURCE_GAP", self.codes())

    def test_missing_raw_file_and_directory_targets_are_errors(self):
        self.source(source_url_or_path="sources/raw/missing.md")
        self.assertIn("MISSING_RAW_SOURCE", self.codes("ERROR"))
        self.source(source_url_or_path="sources/raw")
        self.assertIn("MISSING_RAW_SOURCE", self.codes("ERROR"))

    def test_source_paths_cannot_escape_raw_or_workspace(self):
        for location in ("README.md", "../foreign-repo/source.md", "E:/foreign-repo/source.md"):
            with self.subTest(location=location):
                self.source(source_url_or_path=location)
                self.assertIn("INVALID_SOURCE_PATH", self.codes("ERROR"))

    def test_http_sources_are_metadata_only_and_no_network_is_used(self):
        self.source(source_url_or_path="https://example.invalid/source")
        self.reviewed()
        with patch("socket.create_connection", side_effect=AssertionError("network access")):
            self.assertEqual(checker.check_workspace(self.root), [])

    def test_source_paths_cannot_hide_linked_components_before_parent_segments(self):
        self.source(source_url_or_path="sources/raw/linked/../reference.md")
        linked = self.root / "sources/raw/linked"
        original_linked = checker.linked_path
        with patch.object(checker, "linked_path", lambda path: path == linked or original_linked(path)):
            self.assertIn("INVALID_SOURCE_PATH", self.codes("ERROR"))

    def test_raw_bodies_and_protected_documents_are_never_opened(self):
        self.source()
        self.reviewed()
        self.write("wiki/private/note.md", "Disposable protected fixture.")
        self.write("credentials.md", "Disposable protected fixture.")
        original_open = Path.open

        def guarded_open(target, *args, **kwargs):
            relative = target.relative_to(self.root).as_posix()
            if relative.startswith(("sources/raw/", "wiki/private/")) or relative == "credentials.md":
                raise AssertionError("protected contents opened")
            return original_open(target, *args, **kwargs)

        with patch.object(Path, "open", guarded_open):
            codes = self.codes()
        self.assertIn("PROTECTED_PATH", codes)
        self.assertNotIn("DOCUMENT_READ", codes)

    def test_content_metadata_values_are_validated(self):
        for old, new, code in (
            ("- **Status:** DRAFT", "", "INVALID_STATUS"),
            ("DRAFT", "BANANA", "INVALID_STATUS"),
            ("- **Updated:** 2026-10-17", "", "INVALID_UPDATED"),
            ("2026-10-17", "2026-02-30", "INVALID_UPDATED"),
            ("- **Source IDs:** None", "", "INVALID_SOURCE_FIELD"),
        ):
            with self.subTest(code=code, old=old):
                self.write("wiki/topic.md", page().replace(old, new))
                self.assertIn(code, self.codes("ERROR"))

    def test_unverified_draft_and_reviewed_without_evidence_are_distinct(self):
        self.write("wiki/topic.md", page(summary="General overview."))
        self.assertIn("UNMARKED_DRAFT", self.codes("ERROR"))
        self.write("wiki/topic.md", page(status="REVIEWED"))
        self.assertIn("REVIEWED_WITHOUT_EVIDENCE", self.codes("ERROR"))
        self.write("wiki/topic.md", page(status="STALE"))
        self.assertIn("STALE_PAGE", self.codes("WARNING"))

    def test_approved_adr_can_support_a_first_party_project_decision(self):
        self.write("decisions/ADR-001.md", "# Fixture choice\n- Status: APPROVED\n")
        decision = "[ADR-001](../decisions/ADR-001.md)"
        self.reviewed(sources="None", decision=decision, findings=f"- FACT: Project chose an option. {decision}")
        self.assertEqual(checker.check_workspace(self.root), [])
        self.reviewed(sources="None", findings=f"- FACT: Project chose an option. {decision}")
        self.assertEqual(checker.check_workspace(self.root), [])

    def test_proposed_adr_and_decision_index_are_not_approved_evidence(self):
        for filename, text in (
            ("ADR-001.md", "# Fixture choice\n- Status: PROPOSED\n"),
            ("index.md", "# Decisions index\n- Status: APPROVED\n"),
        ):
            with self.subTest(filename=filename):
                self.write("decisions/" + filename, text)
                decision = f"[Choice](../decisions/{filename})"
                self.reviewed(sources="None", decision=decision, findings=f"- FACT: Chosen option. {decision}")
                codes = self.codes("ERROR")
                self.assertTrue({"UNAPPROVED_DECISION", "MISSING_CITATION"} <= codes)

    def test_proposed_adr_can_be_linked_as_context_without_claiming_approval(self):
        self.write("decisions/ADR-001.md", "# Fixture choice\n- Status: PROPOSED\n")
        self.write("wiki/topic.md", page() + "\n[Proposal context](../decisions/ADR-001.md)\n")
        self.assertEqual(self.codes("ERROR"), set())
        self.assertIn("NO_EVIDENCE", self.codes("WARNING"))

    def test_inline_links_are_checked_across_documentation_locations(self):
        for directory in ("",) + checker.DOC_DIRS:
            with self.subTest(directory=directory):
                relative = (directory + "/" if directory else "") + "broken.md"
                target = self.write(relative, "# Fixture\n[Missing](absent.md)\n")
                self.assertIn("BROKEN_LINK", self.codes("ERROR"))
                target.unlink()

    def test_images_and_encoded_or_angle_bracket_targets(self):
        self.write("wiki/topic.md", page() + "\n![Missing image](absent.png)\n")
        self.assertIn("BROKEN_LINK", self.codes("ERROR"))
        self.write("wiki/figure one.png", "Disposable image filename fixture.")
        self.write("wiki/topic.md", page() + "\n![A](figure%20one.png)\n![B](<figure one.png>)\n")
        self.assertEqual(self.codes("ERROR"), set())

    def test_examples_and_comments_do_not_create_citations_or_links(self):
        tick = chr(96)
        example = "[Missing](absent.md) SRC-20261017-999"
        examples = (
            f"\n{tick * 3}markdown\n{example}\n{tick * 3}\n"
            f"\n~~~text\n{example}\n~~~\n\n{tick}{example}{tick}\n"
            f"\n<!--\n{example}\n-->\n"
        )
        self.write("wiki/topic.md", page() + examples)
        self.assertEqual(self.codes("ERROR"), set())

    def test_unsupported_links_warn_and_heading_anchor_limit_is_explicit(self):
        for link in ("[Missing][ref]\n[ref]: absent.md", "[[Absent]]", "[Nested](file(name).md)"):
            with self.subTest(link=link):
                self.write("wiki/topic.md", page() + "\n" + link + "\n")
                self.assertIn("UNSUPPORTED_MARKDOWN", self.codes("WARNING"))
        self.write("wiki/topic.md", page() + "\n[Heading](topic.md#unknown-heading)\n")
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(checker.main(self.root), 0)
        self.assertIn("heading anchors", output.getvalue())

    def test_orphans_are_reported_and_indirect_navigation_is_followed(self):
        self.write("wiki/index.md", "# Index\n")
        self.assertIn("ORPHAN_PAGE", self.codes("WARNING"))
        self.write("wiki/index.md", "# Index\n[Section](nested/index.md)\n")
        self.write("wiki/nested/index.md", "# Section\n[Topic](../topic.md)\n")
        self.assertNotIn("ORPHAN_PAGE", self.codes())

    def test_missing_wiki_entrypoints_are_reported(self):
        for filename, code in (("index.md", "MISSING_INDEX"), ("log.md", "MISSING_LOG")):
            with self.subTest(filename=filename):
                target = self.root / "wiki" / filename
                original = target.read_text(encoding="utf-8")
                target.unlink()
                self.assertIn(code, self.codes("ERROR"))
                self.write("wiki/" + filename, original)

    def test_escaped_links_are_rejected_without_accessing_outside_paths(self):
        original_exists = Path.exists

        def guarded_exists(target, *args, **kwargs):
            if not target.is_relative_to(self.root):
                raise AssertionError("outside path accessed")
            return original_exists(target, *args, **kwargs)

        for link in ("../../foreign-repo/README.md", "E:/foreign-repo/README.md",
                     "..%2F..%2Fforeign-repo%2FREADME.md"):
            with self.subTest(link=link):
                self.write("wiki/topic.md", page() + f"\n[Outside]({link})\n")
                with patch.object(Path, "exists", guarded_exists):
                    self.assertIn("OUTSIDE_WORKSPACE", self.codes("ERROR"))

    def test_linked_paths_are_not_followed(self):
        target = self.write("wiki/linked.md", "Disposable unread fixture.")
        original_linked = checker.linked_path
        original_open = Path.open

        def pretend_link(path):
            return path == target or original_linked(path)

        def guarded_open(path, *args, **kwargs):
            if path == target:
                raise AssertionError("linked file opened")
            return original_open(path, *args, **kwargs)

        self.write("wiki/topic.md", page() + "\n[Linked](linked.md)\n")
        with patch.object(checker, "linked_path", pretend_link), patch.object(Path, "open", guarded_open):
            self.assertIn("LINKED_PATH", self.codes("WARNING"))

    def test_checker_does_not_modify_or_create_workspace_files(self):
        self.source()
        self.reviewed()

        def snapshot():
            return {p.relative_to(self.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in self.root.rglob("*") if p.is_file()}

        before = snapshot()
        checker.check_workspace(self.root)
        with redirect_stdout(io.StringIO()):
            checker.main(self.root)
        self.assertEqual(snapshot(), before)

    def test_exit_codes_and_output_distinguish_pass_warning_and_error(self):
        self.source()
        self.reviewed()
        for state, expected_exit, expected_text in (
            ("clean", 0, "PASS: structural"),
            ("warning", 0, "CHECKS COMPLETED:"),
            ("error", 1, "FAIL:"),
        ):
            with self.subTest(state=state):
                if state == "warning":
                    self.write("wiki/topic.md", page())
                elif state == "error":
                    self.write("wiki/topic.md", page() + "\n[Broken](missing.md)\n")
                output = io.StringIO()
                with redirect_stdout(output):
                    self.assertEqual(checker.main(self.root), expected_exit)
                self.assertIn(expected_text, output.getvalue())
                self.assertIn("MANUAL REVIEW:", output.getvalue())
                if state != "clean":
                    self.assertNotIn("PASS:", output.getvalue())

    def test_template_can_be_copied_at_two_wiki_depths_without_broken_examples(self):
        template = (REPO / "templates/wiki-page.md").read_text(encoding="utf-8-sig")
        template = template.replace("YYYY-MM-DD", "2026-10-17")
        self.write("wiki/new-topic.md", template)
        self.write("wiki/concepts/nested-topic.md", template)
        self.write("wiki/index.md", "# Index\n[One](new-topic.md)\n[Two](concepts/nested-topic.md)\n")
        self.assertEqual(self.codes("ERROR"), set())

    def test_utf8_bom_and_windows_newlines_are_supported(self):
        target = self.root / "sources/manifest.csv"
        target.write_bytes(b"\xef\xbb\xbf" + target.read_bytes().replace(b"\n", b"\r\n"))
        target = self.root / "wiki/topic.md"
        target.write_bytes(b"\xef\xbb\xbf" + target.read_bytes().replace(b"\n", b"\r\n"))
        self.assertEqual(self.codes("ERROR"), set())


if __name__ == "__main__":
    unittest.main()
