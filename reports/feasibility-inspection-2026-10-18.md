# V1.1 evaluation: inspection and plan

{
  "objective": "V1.1 evaluation harness first; real-world feasibility NOT YET MEASURED",
  "observed_at_utc": "2026-10-18T06:47:27.481037+00:00",
  "head": "457a9bf6db7bb2476117200f76586032ca1e432b",
  "branch": "workspace/initialize",
  "initial_uncommitted_status": [
    " M .obsidian/graph.json",
    "?? reports/independent-final-audit-2026-10-18.json",
    "?? reports/independent-final-audit-2026-10-18.md",
    "?? reports/independent-final-governance-probes-2026-10-18.json",
    "?? reports/independent-final-governance-probes-2026-10-18.md",
    "?? reports/independent-final-load-2026-10-18.json",
    "?? reports/independent-final-load-2026-10-18.md",
    "?? reports/independent-final-security-probes-2026-10-18.json",
    "?? reports/independent-final-security-probes-2026-10-18.md",
    "?? reports/independent-final-workflows-2026-10-18.json",
    "?? reports/independent-final-workflows-2026-10-18.md"
  ],
  "protected_baseline": {
    ".obsidian/graph.json": {
      "bytes": 511,
      "sha256": "9101fb93e2fefb6266c38a1fe7cf7c33fa5b2a33487dbb27e4171d971e686806"
    },
    "decisions/index.md": {
      "bytes": 165,
      "sha256": "0eb74c8b24c81b746b6fa4c86b983364fe1242d55fd7d2305d51fd07ca8405b2"
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
    },
    "sources/manifest.csv": {
      "bytes": 109,
      "sha256": "1abd623611abb8760a152154c369c789ebe47b481b6bc1b24690cc27512fb285"
    },
    "sources/provenance.jsonl": {
      "bytes": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "sources/raw/README.md": {
      "bytes": 416,
      "sha256": "c03e0fc22df68048d53bb3d422f302beeed28e395280b711ca44304384775ad8"
    },
    "wiki/concepts/knowledge-system-principles.md": {
      "bytes": 420,
      "sha256": "6f3147ad0c4b4425b9bb7738b47e41eb78c91e8d3a5692840b7eba3408a2bc13"
    },
    "wiki/log.md": {
      "bytes": 27166,
      "sha256": "b258643720bf0f0fb6bdc643fd0a6de61e74ba0513bb5240ba259bd145cf6da8"
    }
  },
  "core_implementation_sha256": {
    "ingest_workspace.py": "c98a95afe039b643205250a1acf888ce6771b09294fdf71cf53ab4f5f110f5d3",
    "query_workspace.py": "2d3884fd180711a7d63808d33fb3450ced9bd616bd5a80ac72c87511732cf14a",
    "check_workspace.py": "4b9c51045ede39596125af367146dffc2fc437e5b082b05224dd0468f0f2462a",
    "knowledge_governance.py": "b1e9339c39b022f00256036e9ef40fad376a1c4ae7ed67fdf796398c6ce7c9f6",
    "source_integrity.py": "2df48ff29a5e41057b18703c8d7fa20009e06d2afa1ef73ed110b8cb0b8b2468",
    "safe_operations.py": "2a97bc6d198627aa8cf69c2bf33528b7c16ce831bb5bea28b87ab0610c4d050e",
    "workspace_security.py": "03a35cb6524de3a4fb2c7b1b994c8d6d9ad88d4f0607341b1d8d92ec175f80ad"
  },
  "plan": [
    "Independent raw-grounded synthetic specification and gold format",
    "Counterbalanced raw-only versus wiki deterministic retrieval diagnostics; no model A/B inference",
    "Actual Ingest/Query/Lint evolution and rollback; fresh process and independent agent continuity observation",
    "Fresh regression, scoped metrics and real-pilot guide; stop before real intake/V2"
  ],
  "audit_premise": "No newer whole-system READY audit found. Two High findings resolved in last remediation; earlier Medium/Low limitations remain. Do not treat task premise as measurement.",
  "real_pilot_inputs": "Curated real documents, human-confirmed gold, independent human scores and observable model usage unavailable."
}
