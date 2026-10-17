"""Disposable TEST_ONLY workspaces. No production knowledge or approvals are created."""
import hashlib
import json
from pathlib import Path

from scripts import check_workspace as lint
from scripts import ingest_workspace as ingest
from scripts import knowledge_governance as governance
from scripts import safe_operations as operations
from scripts import source_integrity as integrity

DAY = "2026-10-18"
SID = "SRC-20261018-501"
FIXTURES = Path(__file__).absolute().parent / "fixtures/workflow"


class Workspace:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True)
        self.registration_results = []
        self.write("sources/manifest.csv", ",".join(lint.MANIFEST_FIELDS) + "\n")
        self.write("wiki/index.md", "# TEST_ONLY index\n")
        self.write("wiki/log.md", "# TEST_ONLY history\n")
        self.write("reports/validation.md", "# TEST_ONLY simulated human validation evidence\n")

    def write(self, relative, text):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8"))
        return target

    def register(self, sid=SID, body="TEST_ONLY: synthetic policy evidence.", **provenance):
        relative = "sources/raw/" + sid + ".md"
        integrity.create_raw_snapshot(self.root, relative,
                                      ("# TEST_ONLY " + sid + "\n\n## Evidence\n" + body + "\n").encode(),
                                      authorized=True)
        row = dict(zip(lint.MANIFEST_FIELDS, (sid, "TEST_ONLY " + sid, "synthetic_fixture",
                       relative, "", "", DAY, "Synthetic benchmark only",
                       "Unknown author, publisher and publication date; synthetic local origin.")))
        result = integrity.register_source(self.root, row, authorized=True, language="en", **provenance)
        self.registration_results.append(result)
        return row

    def page(self, title="Fixture policy", sources=(SID,), scope="global", claims=None, **extra):
        fields = {"Status": "draft", "kind": "external_fact", "Scope": scope,
                  "created_at": DAY, "updated_at": DAY, "temporal": "historical",
                  "transitions": "[]", "Source IDs": ", ".join(sources) if sources else "None",
                  "language": "en", "keywords": json.dumps([title]), "aliases_vi": "[]"}
        fields.update(extra)
        text = "# " + title + "\n\n" + "".join("- " + key + ": " + str(value) + "\n" for key, value in fields.items())
        text += "\n## Summary\nUNKNOWN: TEST_ONLY synthesis pending review.\n\n## Verified findings\n"
        if claims is None:
            claims = [(SID, "TEST_ONLY synthetic policy.")]
        text += "".join("- FACT: " + claim + " [" + sid + ", section Evidence]\n" for sid, claim in claims)
        return text

    def plan(self, relative="wiki/topic.md", text=None):
        target = relative.removeprefix("wiki/")
        index = (self.root / "wiki/index.md").read_bytes()
        link = ("[TEST_ONLY " + target + "](" + target + ")\n").encode()
        if link not in index:
            index += link
        changes = {relative: (text if text is not None else self.page()).encode(),
                   "wiki/index.md": index,
                   "wiki/log.md": (self.root / "wiki/log.md").read_bytes()
                                  + ("\n[" + DAY + "] TEST_ONLY reviewed synthesis: " + relative + "\n").encode()}
        return changes, operations.versions(self.root, changes)

    def apply(self, relative="wiki/topic.md", text=None, sid=SID, scope="global"):
        changes, expected = self.plan(relative, text)
        return ingest.ingest_registered(self.root, sid, changes, expected, scope=scope, authorized=True, apply=True)

    def move(self, relative, target, actor="ai", **kwargs):
        return governance.transition(self.root, relative, target, actor=actor, at=DAY,
                                     reason="TEST_ONLY documented transition", authorized=True, apply=True, **kwargs)

    def verify(self, relative):
        self.move(relative, "unverified")
        target = self.root / relative
        approval = "experiments/" + target.stem + "-approval.md"
        self.write(approval, "# TEST_ONLY human approval simulation\n- Status: APPROVED\n- authority: human\n"
                   "- target: " + relative + "\n- content_hash: "
                   + governance.content_hash(target.read_text(encoding="utf-8"))
                   + "\n- validated_at: " + DAY + '\n- evidence: ["reports/validation.md"]\n')
        self.move(relative, "verified", actor="human", approval_ref=approval)

    def snapshot(self, include_recovery=False):
        return {path.relative_to(self.root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in self.root.rglob("*") if path.is_file()
                and (include_recovery or not path.is_relative_to(self.root / "recovery"))}


def build_corpus(workspace):
    """The fixture adapter performs actual authorized calls; expectations live separately."""
    corpus = json.loads((FIXTURES / "corpus.json").read_text(encoding="utf-8"))
    admissions, synthesis = [], []
    for source in corpus["sources"]:
        row = workspace.register(source["id"], source["body"])
        first = workspace.registration_results[-1]
        retry = integrity.register_source(workspace.root, row, authorized=True, language="en")
        admissions.append({"source_id": row["source_id"], "first": first["status"], "retry": retry["status"]})
    # Linked targets are ordered before their anchor; no external lookup or fetch is used.
    for spec in corpus["pages"]:
        extra = {"kind": spec.get("kind", "external_fact"), "page_id": "test-" + Path(spec["path"]).stem,
                 "keywords": json.dumps(spec["keywords"], ensure_ascii=False),
                 "aliases_vi": json.dumps(spec["aliases_vi"], ensure_ascii=False)}
        # Timeout filenames are intentionally identical across scopes; page identities are not.
        extra["page_id"] = "test-" + spec["path"].removesuffix(".md").replace("/", ".")
        for name in ("conflicts", "cross_project_refs"):
            if name in spec:
                extra[name] = json.dumps(spec[name], ensure_ascii=False)
        if "decision_key" in spec:
            extra["decision_key"] = spec["decision_key"]
        if spec.get("kind") == "approved_decision":
            extra.update(temporal="current", review_after="2099-12-31")
        text = workspace.page(title=spec["title"], sources=spec["sources"], scope=spec["scope"],
                              claims=spec["claims"], **extra)
        if spec["path"].startswith("wiki/"):
            changes, expected = workspace.plan(spec["path"], text)
            first = ingest.ingest_registered(workspace.root, spec["sources"][0], changes, expected,
                                             scope=spec["scope"], authorized=True, apply=True)
            before = workspace.snapshot()
            retry = ingest.ingest_registered(workspace.root, spec["sources"][0], changes, expected,
                                             scope=spec["scope"], authorized=True, apply=True)
            synthesis.append({"path": spec["path"], "first": first["status"], "retry": retry["status"],
                              "retry_preserved_bytes": workspace.snapshot() == before})
        else:
            # Synthetic ADR provisioning is test setup, not an automated decision approval workflow.
            workspace.write(spec["path"], text)
            index = workspace.root / "wiki/index.md"
            index.write_bytes(index.read_bytes() + ("[TEST_ONLY ADR](../" + spec["path"] + ")\n").encode())
        state = spec["status"]
        if state in {"verified", "superseded"}:
            workspace.verify(spec["path"])
        elif state in {"unverified", "disputed"}:
            workspace.move(spec["path"], "unverified")
        if state == "disputed":
            workspace.move(spec["path"], "disputed")
        if state == "superseded":
            workspace.move(spec["path"], "superseded", actor="human", superseded_by=spec["superseded_by"])
    return {"admissions": admissions, "synthesis": synthesis,
            "source_count": len(corpus["sources"]), "page_count": len(corpus["pages"])}
