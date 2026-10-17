#!/usr/bin/env python3
"""Run paired retrieval against TEST_ONLY fixtures and optionally save new reports."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

if __package__:
    from .check_workspace import ROOT, local_path
    from .query_workspace import search
else:
    from check_workspace import ROOT, local_path
    from query_workspace import search

FIXTURES = ROOT / "tests/fixtures/multilingual"


def evaluate():
    pairs = json.loads((FIXTURES / "pairs.json").read_text(encoding="utf-8"))["pairs"]
    rows = []
    categories = {}
    for pair in pairs:
        group = categories.setdefault(pair["category"], {"queries": 0, "passed": 0})
        for language in ("vi", "en"):
            result = search(FIXTURES, pair[language], pair["scope"])
            actual_paths = sorted(item["path"] for item in result["matches"] + result["blocked"])
            checks = {
                "status": result["status"] == pair["expected_status"],
                "paths": actual_paths == sorted(pair["expected_paths"]),
                "scope_isolation": all(item["scope"] == pair["scope"] for item in result["matches"] + result["blocked"]),
                "original_query": result["query"] == pair[language],
                "expansion": language != "vi" or set(pair["expected_expansion_vi"]) <= set(result["expanded_terms"]),
                "citations": True,
            }
            for item in result["matches"]:
                if not item["citations"]:
                    checks["citations"] = False
                for citation in item["citations"]:
                    source = local_path(FIXTURES, FIXTURES, citation["source_path"])
                    pointer = citation["source_pointer"]
                    # Only the explicitly synthetic fixture bodies are read here.
                    headings = source.read_text(encoding="utf-8").splitlines()
                    if not pointer.startswith("#") or "## " + pointer[1:] not in headings:
                        checks["citations"] = False
            passed = all(checks.values())
            rows.append({
                "pair_id": pair["id"], "category": pair["category"], "language": language,
                "expected_status": pair["expected_status"], "expected_paths": pair["expected_paths"],
                "checks": checks, "passed": passed, "actual": result,
            })
            group["queries"] += 1
            group["passed"] += int(passed)
    passed = sum(item["passed"] for item in rows)
    return {
        "fixture_only": True, "fixture_root": FIXTURES.relative_to(ROOT).as_posix(),
        "method": "scoped deterministic lexical matching with curated aliases; no semantic retrieval",
        "python": sys.version.split()[0],
        "pairs": len(pairs), "queries": len(rows), "passed": passed, "failed": len(rows) - passed,
        "categories": categories,
        "actual_outcomes": dict(Counter(row["actual"]["status"] for row in rows)),
        "results": rows,
    }


def markdown_report(report):
    lines = [
        "# Multilingual readiness — observed synthetic retrieval results", "",
        "TEST_ONLY: these results concern artificial fixtures, not real project knowledge.",
        f"Method: {report['method']}. Python: {report['python']}.", "",
        f"Observed: {report['pairs']} pairs / {report['queries']} queries; "
        f"{report['passed']} met expected outcomes, {report['failed']} failed.", "",
        "Passing a negative case means NOT_FOUND or MISSING_EVIDENCE was returned as expected; "
        "it does not mean every query found a source.", "",
        "## Observed categories", "",
    ]
    for name, group in report["categories"].items():
        lines.append(f"- {name}: {group['passed']}/{group['queries']} expected outcomes.")
    lines += ["", "## Actual search outcomes", ""]
    for name, count in report["actual_outcomes"].items():
        lines.append(f"- {name}: {count}")
    lines += ["", "## Pair details", ""]
    for offset in range(0, len(report["results"]), 2):
        vi, en = report["results"][offset:offset + 2]
        lines.append(f"### {vi['pair_id']} — {vi['category']}")
        lines.append("")
        for row in (vi, en):
            actual = row["actual"]
            paths = [item["path"] for item in actual["matches"] + actual["blocked"]]
            lines.append(f"- {row['language']}: {actual['query']} → {actual['status']}; "
                         f"scope={actual['scope']}; paths={', '.join(paths) or 'none'}; "
                         f"expected={row['expected_status']}; checks={'PASS' if row['passed'] else 'FAIL'}.")
            if actual["expanded_terms"]:
                lines.append("- Added terms: " + ", ".join(actual["expanded_terms"]))
        citations = [c for hit in vi["actual"]["matches"] for c in hit["citations"]]
        for citation in citations:
            target = "../" + report["fixture_root"] + "/" + citation["source_path"] + citation["source_pointer"]
            lines.append(f"- Fixture evidence: [{citation['source_id']}]({target}).")
        lines.append("")
    lines += [
        "## Limits and next step", "",
        "This measures the declared lexical rules on curated examples. It does not establish semantic "
        "recall, performance on unseen paraphrases, factual correctness, approval or live Obsidian behavior. "
        "No live raw source was added, read, translated or rewritten by the retrieval runner. "
        "The proposed upgrade path remains in MULTILINGUAL.md; no QMD, RAG or vector store was implemented.", "",
    ]
    return "\n".join(lines)


def save_report(report, output):
    output = local_path(ROOT, ROOT, str(output))
    if not output.is_relative_to(ROOT / "reports") or output.suffix != ".json":
        raise ValueError("report output must be a relative reports/*.json path")
    companion = output.with_suffix(".md")
    if output.exists() or companion.exists():
        raise FileExistsError("refusing to overwrite an existing report")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    with companion.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(markdown_report(report))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="New relative reports/*.json path; also writes a Markdown companion.")
    args = parser.parse_args()
    report = evaluate()
    if args.output:
        save_report(report, args.output)
    print(json.dumps({key: value for key, value in report.items() if key != "results"}, indent=2))
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
