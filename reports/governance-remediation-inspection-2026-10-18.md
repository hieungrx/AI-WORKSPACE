# Governance remediation - pre-edit inspection

{
  "phase": "High governance remediation - inspection before edits",
  "head": "80d9d67c495aad3443efa06b2b823bae5be8b4a7",
  "branch": "workspace/initialize",
  "root_causes": {
    "H-GOV-01": "ADR eligibility duplicated/incomplete: Query decision_citations and Lint approved set omit dependency freshness/effective/history; current gate only checks parent. Mixed evidence currently uses page-level OR.",
    "H-GOV-02": "Helper validates approval, but event replay checks only truthy resolution ref; writer only checks append/content hash. Required authorization can be skipped through lifecycle transaction."
  },
  "affected_paths": [
    "transition -> approval -> proposed read_page -> transact",
    "transact wiki/lifecycle preflight -> read_page -> validate_update -> journal -> replace",
    "read_page event replay -> audit_governance -> Lint",
    "Query pages -> read_page -> citations OR decision_citations -> current truth",
    "Ingest read_page/update validators -> bounded transaction",
    "recovery restores hash-validated exact before-images; cannot rewrite history"
  ],
  "pre_fix_actual": {
    "ADR_regressions": {
      "tests": 16,
      "failures": 10,
      "errors": 0,
      "exit_code": 1,
      "note": "Includes newly specified behavior, not ten distinct security bugs. Original future/overdue/historical current=true failures reproduced."
    },
    "approval_regressions": {
      "tests": 4,
      "failures": 4,
      "errors": 0,
      "exit_code": 1,
      "note": "Helper rejected nonexistent approval; direct writer committed, reader/Query/Lint accepted legacy invalid history."
    }
  },
  "design_before_implementation": [
    "Canonical per-finding evidence and ADR/current eligibility reused by Query and Lint; preserve context/history and independent valid raw proof.",
    "Shared required-event approval validation in helper, writer preflight, reader and historical audit. New action-bound approval policy with explicit legacy replay; immutable event snapshots; no bulk history rewrite.",
    "Tests only synthetic; preserve raw, source registry, original wiki/decisions and preexisting audit reports."
  ],
  "protected_baseline": {
    ".obsidian/graph.json": {
      "bytes": 502,
      "sha256": "a3aad29bbc1153d8b46cf515d8f0eb994d32b35e87a1e70921fb1db2ac65a8b5"
    },
    "sources/raw/README.md": {
      "bytes": 416,
      "sha256": "c03e0fc22df68048d53bb3d422f302beeed28e395280b711ca44304384775ad8"
    },
    "sources/manifest.csv": {
      "bytes": 109,
      "sha256": "1abd623611abb8760a152154c369c789ebe47b481b6bc1b24690cc27512fb285"
    },
    "sources/provenance.jsonl": {
      "bytes": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "decisions/index.md": {
      "bytes": 165,
      "sha256": "0eb74c8b24c81b746b6fa4c86b983364fe1242d55fd7d2305d51fd07ca8405b2"
    },
    "wiki/concepts/knowledge-system-principles.md": {
      "bytes": 420,
      "sha256": "6f3147ad0c4b4425b9bb7738b47e41eb78c91e8d3a5692840b7eba3408a2bc13"
    },
    "wiki/log.md": {
      "bytes": 23144,
      "sha256": "511a4c3e5711c113d7a7999647b494b67ca4da139f176b8e7323349d12d05424"
    },
    "reports/independent-final-audit-2026-10-18.json": {
      "bytes": 51058,
      "sha256": "b45b49d3736129c97df5a3ecd7b5836960decaf47836af23e5f5f2801e78d73b"
    },
    "reports/independent-final-audit-2026-10-18.md": {
      "bytes": 30042,
      "sha256": "7a25a56727aa48eba9f00a6652e5e34b1a8cd8aac825f1bc8ce40a6d1fd1ac23"
    },
    "reports/independent-final-governance-probes-2026-10-18.json": {
      "bytes": 8086,
      "sha256": "538921f41e6f2b3f3f4e309093387609e2378cd9948732becedda9d367ea32fd"
    },
    "reports/independent-final-governance-probes-2026-10-18.md": {
      "bytes": 7468,
      "sha256": "f38c18de607f50634f2adc5f9dccc3a98c89fefa4150f15298c6401334663435"
    },
    "reports/independent-final-load-2026-10-18.json": {
      "bytes": 14413,
      "sha256": "32d36d13e190088ffd26c3469ffe679e3b86c3965a1b3bce67309c80a2ebc901"
    },
    "reports/independent-final-load-2026-10-18.md": {
      "bytes": 9969,
      "sha256": "7595e1a140c843e18603a4ab0c2358d7d39efd5a581acaaac8631729d64dadc7"
    },
    "reports/independent-final-security-probes-2026-10-18.json": {
      "bytes": 9821,
      "sha256": "5d221a374cb1348efaf1626847540ba4a432ca670984e0c9ceb1432a3e5a7474"
    },
    "reports/independent-final-security-probes-2026-10-18.md": {
      "bytes": 6872,
      "sha256": "baf27576988e784148969f26235731b7574a8b320c053e5991be5c0afa708c7e"
    },
    "reports/independent-final-workflows-2026-10-18.json": {
      "bytes": 200917,
      "sha256": "a2c089395379561770a67ca91337fd074c847b1c475fdc1b2c25f66cdad85ce9"
    },
    "reports/independent-final-workflows-2026-10-18.md": {
      "bytes": 18148,
      "sha256": "21c8a3b5721a83f337f746c4340d303ad2822d1676c870f16276bad01112c90d"
    }
  }
}
