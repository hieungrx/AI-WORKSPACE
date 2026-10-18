#!/usr/bin/env python3
"""Validate V1.1 evaluation plumbing on synthetic data, not AI productivity."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import random
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).absolute().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts import check_workspace as lint
from scripts import query_workspace as query
from scripts.safe_operations import save_reports
from scripts.source_integrity import audit_sources
from scripts.workspace_security import read_data, require_safe_data
from tests.workflow_support import Workspace

DATASET = ROOT / "tests/fixtures/feasibility/dataset.json"
SCOPE = "synthetic deterministic component; no AI model, human score or real pilot"
CORE = ("ingest_workspace.py", "query_workspace.py", "check_workspace.py", "knowledge_governance.py",
        "source_integrity.py", "safe_operations.py", "workspace_security.py")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def measured(value, *, n, unit="ratio", definition=""):
    return {"status": "MEASURED" if value is not None else "NOT MEASURED", "value": value,
            "samples": n, "unit": unit, "scope": SCOPE, "definition": definition}


def fraction(numerator, denominator, definition):
    result = measured(numerator / denominator if denominator else None, n=denominator, definition=definition)
    result.update(numerator=numerator, denominator=denominator)
    return result


def validate_dataset(data):
    """Gold is supplied by the independent source specification, never Query output."""
    if data.get("synthetic_only") is not True or not data.get("gold_origin") or not data.get("dataset_id"):
        raise ValueError("SYNTHETIC_DATASET_REQUIRED")
    sources, cases = data["sources"], data["cases"]
    ids = [s["source_id"] for s in sources]
    if len(set(ids)) != len(ids) or any(not lint.source_id(sid) for sid in ids):
        raise ValueError("DUPLICATE_OR_INVALID_SOURCE")
    catalog = {s["source_id"]: s for s in sources}
    for source in sources:
        if not all(source.get(k) for k in ("title", "scope", "body")) or "## Evidence\n" not in source["body"]:
            raise ValueError("SOURCE_EVIDENCE_REQUIRED")
        if not all(isinstance(source.get(k), list) for k in ("keywords", "aliases_vi")):
            raise ValueError("NAVIGATION_METADATA_REQUIRED")
    seen, pairs = set(), {}
    required = {"case_id", "category", "input_prompt", "query", "language", "relevant_source_ids",
                "required_citations", "expected_project_scope", "expected_decision_validity", "expected_answer",
                "scoring_rubric", "abstention_rules", "severity", "execution"}
    for case in cases:
        if not required <= case.keys() or case["case_id"] in seen:
            raise ValueError("INVALID_OR_DUPLICATE_CASE")
        seen.add(case["case_id"])
        gold = case["relevant_source_ids"]
        if (len(set(gold)) != len(gold) or not set(gold) <= catalog.keys()
                or case["expected_decision_validity"] != "unverified"
                or case["execution"] not in {"retrieval", "protocol_only"}
                or not case["expected_project_scope"] or not case["scoring_rubric"] or not case["abstention_rules"]):
            raise ValueError("INVALID_GOLD_CONTRACT")
        if {c["source_id"] for c in case["required_citations"]} != set(gold):
            raise ValueError("GOLD_CITATION_MISMATCH")
        if any(c["pointer"] != "#Evidence" for c in case["required_citations"]):
            raise ValueError("UNSUPPORTED_SYNTHETIC_POINTER")
        if case["category"] == "bilingual":
            pairs.setdefault(case["pair_id"], []).append(case)
    counts = Counter(c["category"] for c in cases)
    if any(counts[k] < n for k, n in {"knowledge": 30, "bilingual": 40, "evolution": 10,
                                      "scope": 10, "continuity": 5, "task": 8}.items()):
        raise ValueError("DATASET_COVERAGE_INCOMPLETE")
    if len(pairs) < 20 or any(len(p) != 2 or {c["language"] for c in p} != {"vi", "en"}
                              or p[0]["relevant_source_ids"] != p[1]["relevant_source_ids"]
                              or p[0]["expected_project_scope"] != p[1]["expected_project_scope"]
                              for p in pairs.values()):
        raise ValueError("BILINGUAL_PAIR_MISMATCH")
    return {"sources": len(sources), "cases": len(cases), "by_category": dict(counts), "bilingual_pairs": len(pairs)}


def counterbalanced(cases, seed):
    ordered = list(cases)
    random.Random(seed).shuffle(ordered)
    return [(case, ("A", "B") if number % 2 == 0 else ("B", "A"))
            for number, case in enumerate(ordered)]


def raw_search(root, packet, text, scope):
    """Baseline-only adapter: reads raw and scope/title packet, never wiki/aliases."""
    require_safe_data(text)
    q = query.normalize(text)
    catalog = query.source_catalog(root)  # Same recorded byte integrity as B, no reverse wiki scan.
    candidates = []
    for source in packet:
        if source["scope"] != scope:
            continue
        sid = source["source_id"]
        record = catalog[sid]
        if record["integrity_status"] != "MATCH":
            raise ValueError("BASELINE_SOURCE_INTEGRITY")
        raw = read_data(root, record["source_path"])["text"]
        title = query.normalize(source["title"])
        score = 3 if title == q else 2 if query.contains(q, title) else 1 if query.contains(query.normalize(raw), q) else 0
        if score:
            candidates.append({"path": record["source_path"], "score": score, "scope": scope,
                "citations": [{"source_id": sid, "source_path": record["source_path"],
                               "source_pointer": "section Evidence", "integrity_status": "MATCH"}]})
    best = max((row["score"] for row in candidates), default=0)
    top = sorted((row for row in candidates if row["score"] == best), key=lambda r: r["path"])
    return {"status": "AMBIGUOUS" if len(top) > 1 else "FOUND" if top else "NOT_FOUND",
            "matches": top, "blocked": [], "retrieval_only": True}


def summarize_trial(w, case, arm, result, elapsed, catalog=None):
    ranked = sorted(result["matches"] + result["blocked"], key=lambda row: (-row["score"], row["path"]))
    catalog = catalog if catalog is not None else audit_sources(w.root, include_relationships=False)["sources"]
    # Retrieval identity must survive missing citations, while evidence quality is separate.
    identities = []
    for row in ranked:
        target = lint.local_path(w.root, w.root, row["path"])
        if row["path"].startswith("wiki/"):
            identities.extend(sorted(set(lint.SOURCE_TOKEN.findall(lint.metadata(
                target.read_text(encoding="utf-8")).get("source ids", "")))))
        else:
            identities.extend(c["source_id"] for c in row["citations"] if "source_id" in c)
    found = list(dict.fromkeys(identities))[:5]
    citations = [cite for row in ranked[:5] for cite in row["citations"] if "source_id" in cite]
    gold = set(case["relevant_source_ids"])
    structural = []
    for citation in citations:
        sid = citation["source_id"]
        record = catalog.get(sid)
        target = w.root / "sources/raw" / (sid + ".md") if lint.source_id(sid) else None
        valid = bool(record and target and record["integrity_status"] == "MATCH" and target.is_file()
                 and citation.get("source_path") == record["local_path"] == target.relative_to(w.root).as_posix()
                 and citation.get("integrity_status") == "MATCH"
                 and "sha256:" + sha(target.read_bytes()) == record["content_hash"]
                 and "## Evidence\n" in target.read_text(encoding="utf-8")
                 and citation.get("source_pointer", "").casefold() in {"section evidence", "#evidence"})
        structural.append(valid)
    quality = ("HIT" if gold <= set(found) else "MISS") if gold else (
        "CORRECT_ABSTENTION_SIGNAL" if not ranked and result["status"] == "NOT_FOUND" else "UNEXPECTED_RETRIEVAL")
    return {"case_id": case["case_id"], "category": case["category"], "arm": arm,
            "language": case["language"], "query": case["query"], "scope": case["expected_project_scope"],
            "expected_source_ids": sorted(gold), "status": result["status"], "retrieved_source_ids_at_5": found,
            "recall_at_5": len(gold & set(found)) / len(gold) if gold else None,
            "retrieval_contract": quality,
            "required_citation_coverage": gold <= {c["source_id"] for c in citations},
            "ranked_paths": [row["path"] for row in ranked[:5]], "citations": citations,
            "citation_structural_checks": structural, "citation_gold_agreement": [c["source_id"] in gold for c in citations],
            "cross_project_leaks": sum(row["scope"] != case["expected_project_scope"] for row in ranked),
            "current_flags": [row["usable_as_current_truth"] for row in ranked if "usable_as_current_truth" in row],
            "expected_current_authority": False, "elapsed_seconds": elapsed,
            "answer_correctness": "NOT MEASURED", "human_review": None}


def run_pairs(w, data, cases, seed):
    rows, order = [], []
    catalog = audit_sources(w.root, include_relationships=False)["sources"]
    packet = [{key: source[key] for key in ("source_id", "title", "scope")} for source in data["sources"]]
    for case, arms in counterbalanced(cases, seed):
        order.append({"case_id": case["case_id"], "arms": arms})
        for arm in arms:
            start = time.perf_counter()
            result = (raw_search(w.root, packet, case["query"], case["expected_project_scope"]) if arm == "A"
                      else query.search(w.root, case["query"], case["expected_project_scope"]))
            elapsed = time.perf_counter() - start
            rows.append(summarize_trial(w, case, arm, result, elapsed, catalog))
    return rows, order


def metrics(rows):
    recalls = [r["recall_at_5"] for r in rows if r["recall_at_5"] is not None]
    citations = [v for r in rows for v in r["citation_structural_checks"]]
    agreements = [v for r in rows for v in r["citation_gold_agreement"]]
    flags = [v for r in rows for v in r["current_flags"]]
    return {"recall_at_5": measured(sum(recalls) / len(recalls) if recalls else None, n=len(recalls),
                                    definition="Macro source Recall@5: first 5 distinct source IDs projected from ranked candidates; nonempty gold, blocked identities included; no answer score."),
            "citation_structural_validity": fraction(sum(citations), len(citations), "Recorded source ID/path/hash status and Evidence heading; not factual truth."),
            "citation_gold_agreement": fraction(sum(agreements), len(agreements), "Cited source IDs present in the independent relevance gold; meaning NOT assessed."),
            "cross_project_leakage": fraction(sum(r["cross_project_leaks"] > 0 for r in rows), len(rows), "Trials returning an out-of-scope candidate."),
            "unauthorized_current_flags": fraction(sum(flags), len(flags), "Returned wiki flags for this unverified-only corpus; NOT AI factual assertions."),
            "query_elapsed_mean_seconds": measured(sum(r["elapsed_seconds"] for r in rows) / len(rows) if rows else None,
                                                   n=len(rows), unit="seconds", definition="Actual adapter elapsed time, uncontrolled OS cache; not human/AI task time."),
            "task_correctness": measured(None, n=0), "factual_correctness": measured(None, n=0),
            "citation_semantic_accuracy": measured(None, n=0), "context_continuity_quality": measured(None, n=0),
            "unsupported_AI_current_truth_assertions": measured(None, n=0),
            "human_corrections": measured(None, n=0), "human_review_seconds": measured(None, n=0),
            "AI_task_elapsed_seconds": measured(None, n=0), "context_tokens": measured(None, n=0),
            "token_usage": measured(None, n=0), "API_cost": measured(None, n=0),
            "net_productivity": measured(None, n=0), "repeated_research_steps": measured(None, n=0)}


def add_batch(w, sources):
    times, admissions = [], []
    for source in sources:
        start = time.perf_counter()
        sid = source["source_id"]
        w.register(sid, source["body"])
        admissions.append(w.registration_results[-1]["status"])
        pointer = source["body"].split("## Evidence\n", 1)[1].strip().replace("\n", " ")
        relative = f"wiki/{sid}.md"
        text = w.page(title=source["title"], scope=source["scope"], sources=(sid,), claims=[(sid, pointer)],
                      temporal="current", review_after="2099-12-31", keywords=json.dumps(source["keywords"], ensure_ascii=False),
                      aliases_vi=json.dumps(source["aliases_vi"], ensure_ascii=False))
        result = w.apply(relative, text, sid=sid, scope=source["scope"])
        w.move(relative, "unverified")
        times.append({"source_id": sid, "admission": admissions[-1], "synthesis": result["status"],
                      "elapsed_seconds": time.perf_counter() - start})
    return times


def evaluate(seed=1101):
    from scripts.feasibility_evolution import evaluate_evolution
    data_bytes = DATASET.read_bytes()
    data = json.loads(data_bytes)
    characteristics = validate_dataset(data)
    initial_hashes = {name: sha((ROOT / "scripts" / name).read_bytes()) for name in CORE}
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="fixture-feasibility-", dir=ROOT / "tests") as directory:
        base = Path(directory)
        w = Workspace(base / "paired")
        w.write("reports/validation.md", "# TEST_ONLY fixture\nNo human validation or approval occurred.\n")
        batch_observations, rounds = [], []
        # Same small query panel on each growing corpus; no simulated future-round scores.
        panel = [c for c in data["cases"] if c["execution"] == "retrieval"][:4]
        admitted = 0
        sizes = sorted({min(10, len(data["sources"])), min(20, len(data["sources"])), len(data["sources"])})
        for size in sizes:
            batch = add_batch(w, data["sources"][admitted:size])
            batch_observations.extend(batch)
            partial = dict(data, sources=data["sources"][:size])
            rows, order = run_pairs(w, partial, panel, seed)
            rounds.append({"source_count": size, "query_panel_case_ids": [c["case_id"] for c in panel],
                           "batch_operations": batch, "rows": rows, "execution_order": order,
                           "A": metrics([r for r in rows if r["arm"] == "A"]),
                           "B": metrics([r for r in rows if r["arm"] == "B"])})
            admitted = size
        before = w.snapshot(include_recovery=True)
        executable = [c for c in data["cases"] if c["execution"] == "retrieval"]
        rows, order = run_pairs(w, data, executable, seed)
        lint_issues = lint.check_workspace(w.root, integrity=True, security=True)
        read_only = before == w.snapshot(include_recovery=True)
        evolution = evaluate_evolution(base / "evolution")
        # Temporary absolute paths are not reusable evidence locations.
        evolution.pop("workspace_path", None)
        arms = {arm: metrics([r for r in rows if r["arm"] == arm]) for arm in ("A", "B")}
        delta = arms["B"]["recall_at_5"]["value"] - arms["A"]["recall_at_5"]["value"]
        technical = (len(rows) == 2 * len(executable) and any(r["citations"] for r in rows if r["arm"] == "B")
                     and read_only and evolution["passed"] and not any(i.startswith("ERROR ") for i in lint_issues)
                     and all(row["admission"] == "REGISTERED" and row["synthesis"] == "COMMITTED" for row in batch_observations)
                     and not any(r["cross_project_leaks"] or any(r["current_flags"])
                                 or not all(r["citation_structural_checks"]) for r in rows)
                     and not any(r["status"] in {"INVALID_DATA", "RECOVERY_REQUIRED", "UNTRUSTED_CONTENT"} for r in rows))
        observation = {"dataset": characteristics, "paired_cases": len(executable), "arm_executions": len(rows),
                       "protocol_only_cases": [{"case_id": c["case_id"], "category": c["category"], "status": "NOT RUN"}
                                               for c in data["cases"] if c["execution"] == "protocol_only"],
                       "rows": rows, "execution_order": order,
                       "retrieval_quality_outcomes": {arm: dict(Counter(r["retrieval_contract"] for r in rows if r["arm"] == arm)) for arm in ("A", "B")},
                       "harness_verdict_definition": "Execution, preservation and integrity plumbing only. MISS/unexpected retrieval rows remain explicit quality failures, never converted to PASS.",
                       "A": arms["A"], "B": arms["B"], "proxy_recall_delta_B_minus_A": measured(delta, n=len(executable),
                          definition="Paired raw adapter versus wiki helper on curated synthetic queries; NOT AI A/B value."),
                       "compounding_rounds": rounds, "maintenance_operations": batch_observations,
                       "maintenance_elapsed_seconds": measured(sum(r["elapsed_seconds"] for r in batch_observations),
                                                              n=len(batch_observations), unit="seconds", definition="Actual synthetic admission/synthesis/lifecycle machine time; excludes human review."),
                       "query_and_lint_read_only": read_only, "lint_issues": lint_issues,
                       "knowledge_evolution": evolution, "harness_verdict": "PASS" if technical else "FAIL"}
    unchanged = all(sha((ROOT / "scripts" / name).read_bytes()) == value for name, value in initial_hashes.items())
    observation.update({"phase": "V1.1 feasibility harness", "synthetic_only": True,
        "observed_at_utc": datetime.now(timezone.utc).isoformat(), "seed": seed,
        "runtime": {"python": platform.python_version(), "platform": platform.platform(),
                    "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                    "dirty_status": subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines()},
        "dataset_sha256": sha(data_bytes), "core_implementation_sha256": initial_hashes,
        "harness_sha256": {name: sha((ROOT / "scripts" / name).read_bytes())
                           for name in ("evaluate_feasibility.py", "feasibility_evolution.py")},
        "core_unchanged": unchanged, "owned_fixture_cleaned": not base.exists(),
        "total_harness_elapsed_seconds": time.perf_counter() - started,
        "real_world_feasibility": "NOT YET MEASURED", "verdict": "INCONCLUSIVE",
        "model": None, "settings": None, "model_sessions": 0, "human_evaluations": 0,
        "experimental_controls": {"same_raw_bytes_and_scopes": True, "A_wiki_access": False,
            "B_maintained_metadata": True, "order": "seeded shuffle, alternating AB/BA", "independent_AI_sessions": False,
            "engine": "same normalization/phrase boundaries/rank tiers; A raw title/body, B actual wiki keywords/aliases",
            "source_access": "A receives all raw sources and independent title/scope packet; B has identical raw access plus maintained wiki.",
            "information_limit": "Raw adapter is NOT a competent raw-searching AI; no model comparison or productivity conclusion.",
            "cache_control": "No persistent eligibility cache; OS cache and sequential process effects uncontrolled."},
        "not_measured": ["Real curated/human-confirmed gold", "Same-model independent AI A/B trials", "Semantic/factual answer correctness",
                         "Human review/correction/maintenance time", "AI context/token/API cost", "Net productivity/compounding practical value"],
        "recommendation": "Use the reviewed real-pilot protocol only in a separately authorized task; do not infer V2 readiness from synthetic PASS."})
    if not unchanged or not observation["owned_fixture_cleaned"]:
        observation["harness_verdict"] = "FAIL"
    return observation


def markdown(r):
    lines = ["# V1.1 — Synthetic feasibility harness", "", "**Real-world feasibility: NOT YET MEASURED. Verdict: INCONCLUSIVE.**", "",
             "Harness: " + r["harness_verdict"] + ". No AI model was invoked; no independent human score was produced.", "",
             "Dataset: " + json.dumps(r["dataset"], ensure_ascii=False), "",
             f"Paired retrieval cases: {r['paired_cases']}; actual arm executions: {r['arm_executions']}. Seed: {r['seed']}. Runtime HEAD: {r['runtime']['head']}.", "",
             "The 23 protocol-only gold cases (10 evolution, 5 AI-session continuity, 8 research/coding tasks) remain NOT RUN. The generic evolution demonstration below does not replace running those case-specific rubrics.", "",
             "## Baseline A and wiki B — component diagnostics only", "",
             "A reads all permitted raw bytes and independent title/scope metadata. B uses actual wiki Query plus those same raw sources. Both are deterministic helpers, not equivalent AI workflows. Wiki aliases/curation are the intended extra artifact; the raw adapter cannot demonstrate how a competent AI would use raw materials.", ""]
    lines += ["Retrieval quality outcomes (separate from infrastructure): " + json.dumps(r["retrieval_quality_outcomes"]), ""]
    for arm in ("A", "B"):
        lines += ["### " + arm, ""]
        lines += ["- " + key + ": " + json.dumps(value, ensure_ascii=False) for key, value in r[arm].items()]
    lines += ["", "## Knowledge evolution and recovery", "", json.dumps(r["knowledge_evolution"], ensure_ascii=False, indent=2), "",
              "## Accumulating source batches", ""]
    for batch in r["compounding_rounds"]:
        lines.append(f"- {batch['source_count']} sources: fixed panel {batch['query_panel_case_ids']}; actual batch machine time "
                     + str(sum(op["elapsed_seconds"] for op in batch["batch_operations"]))
                     + " seconds; A/B source Recall@5 " + str(batch["A"]["recall_at_5"]["value"]) + "/" + str(batch["B"]["recall_at_5"]["value"]) + ".")
    lines += ["", "Repeated research steps, answer quality, human maintenance/review burden and practical compounding value remain NOT MEASURED. Fixed-panel retrieval can stay flat as files accumulate; it is not evidence of increasing practical value.", "",
              "## Limits and next action", ""]
    lines += ["- NOT MEASURED: " + item for item in r["not_measured"]]
    lines += ["- " + r["recommendation"], "", "Gold, cases, actual per-arm outputs, seeds, timings and file hashes are retained in companion JSON. No real intake, network, other project repository or V2 was used.", "",
              "See [evaluation protocol](../FEASIBILITY_EVALUATION.md) and [dataset contract](../tests/fixtures/feasibility/README.md).", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seed", type=int, default=1101)
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    result = evaluate(args.seed)
    if args.output:
        save_reports(ROOT, result, args.output, markdown)
    print(json.dumps({k: result[k] for k in ("harness_verdict", "verdict", "real_world_feasibility", "paired_cases", "arm_executions", "dataset")}))
    return 0 if result["harness_verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
