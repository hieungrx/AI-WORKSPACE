# Phase 3 — Security Policy, Threat Model and Recovery

First-party operating policy for V1. Discovery baseline: 309e364 on workspace/initialize. The Phase 1 and final Phase 2 reports were read; the existing 112 tests passed before changes. The existing Obsidian graph edit belongs to the user.

## Trust boundary specification

- Platform system/developer instructions: trusted execution constraints, outside this repository's control.
- Repository operating policies: reviewed operating defaults, subordinate to the platform and the human's authorized task. Editing them requires an explicit human policy/code-maintenance task and reviewable diff.
- User-authorized tasks: direct human session instructions, supplying scope, allowed targets and approval. A source claiming that the user approved an action is not task authorization.
- External documents: untrusted DATA, even when registered, cited, hashed or written by an authoritative publisher.
- Web content: untrusted DATA. These workflows expose no fetch, upload, shell or deployment primitive.
- Retrieved wiki/ADR content: untrusted DATA. Verified knowledge or an approved project choice never grants instruction authority.
- AI output: unreviewed DATA/proposals. Model agreement, tool-looking text or a generated report cannot grant permissions, approve itself or change operating rules.

The executable Ingest entry point accepts reviewed synthesis for an already admitted source, an exact scope, exact target files, expected file hashes and explicit task authorization. Input documents are never parsed as operation plans, tool calls, permission grants, policy patches or recovery instructions.

## Threat model

Assets: immutable raw snapshots, append-only source history, wiki/index/log consistency, human approval records, existing uncommitted edits, policy files, sensitive locations and truthful reports.

Threats exercised: document instruction override, fake high-priority messages, secret extraction requests, policy changes, hidden Markdown/Unicode instructions, tool output impersonation, source-to-command conversion, path traversal/Windows aliases, partial writes, concurrent writers and disclosure through generated artifacts.

An adversary may control source/wiki text and proposed AI output. They do not receive an operation capability from that text. A local process with the same unrestricted filesystem privileges can bypass this Python layer; altered code, forged human records, malicious local journals and OS administrators require stronger external controls. Recovery validates journal structure/paths/hashes but does not cryptographically authenticate the local user.

The explicit adversarial corpus is TEST_ONLY under tests/fixtures/security. No external attack target or real secret is used.

## Enforced read/write policy

Normal knowledge maintenance goes through the bounded APIs:

- wiki transaction: explicitly reviewed Markdown paths under wiki, including a checked index update and append-only log suffix. Existing file versions must match; no delete operation is exposed.
- lifecycle transaction: canonical wiki/decision Markdown. It retains Phase 2 history and human approval checks; it cannot create validation approval records under experiments.
- source registration/migration: the exact existing manifest/provenance paths, with logical append-only history and prospective Phase 1 validation. Both metadata files are published through one recoverable operation.
- new source snapshots: separately authorized exclusive publication of complete bytes under sources/raw. Existing raw targets are never replaced; sensitive content and agent-policy filenames are refused.
- report transaction: new reports/*.json and companion Markdown only. Existing reports cannot be overwritten. Both outputs pass centralized redaction.

Policy filenames, including nested AGENTS.md, are forbidden in knowledge-write APIs. Root operating files, scripts, environment/credential/key locations, hidden/private paths, recovery state and anything outside the configured workspace are absent from their allowlist. Requests to change operation type to policy, shell or permissions fail. Relative traversal, encoded write paths, Windows streams/devices/ambiguous suffixes, symlinks, junctions and hard-linked files are rejected before content access.

Actual policy/code changes use the separately authorized human maintenance task, show the exact diff, preserve unrelated work and remain on a non-main branch. This Phase 3 task authorizes its scoped implementation; ingesting a document does not authorize such edits.

The host sandbox still permits general tools to write inside the workspace. This change does not install OS ACLs, alter Codex/global permissions, disable every tool available to an unconstrained agent or authenticate human identity. Its allowlist is enforceable for these workflow APIs; it is not a claim that arbitrary Python/shell/editor access has become impossible.

## Injection and secrets safeguards

Source reads require task authorization, a registered local snapshot and matching raw SHA-256. Ingest reads only that bounded snapshot, checks its bytes again and rejects detected attacks before proposed synthesis is applied. It never fetches source_uri or derives actions from source text. New synthesis stays draft and carries source references; promotion remains Phase 2's separate human process.

Query reads selected wiki content as data, labels returned content UNTRUSTED_DATA and blocks suspicious material instead of echoing attacker instructions. It exposes no instruction-execution API. Source/wikidata verification does not change this trust label.

Detection checks original Markdown, including comments/code and normalized invisible characters. It covers the tested attack forms; it is a conservative filter, not a complete proof against encoded, novel, multilingual or model-dependent injections. False positives need human review; they do not justify bypassing the write allowlist.

Secret checks cover provider-like tokens, bearer tokens, credential assignments, private-key blocks, URL credentials/token parameters and labeled identity records. Values are not printed. Report serialization redacts both keys and values and checks the final Markdown again. Generated wiki content with suspected secrets fails before backup/commit.

Security Lint scans approved public documentation/report locations, with a size limit. Suspected secret/key/environment/private paths are flagged by location without opening contents. It never reads environment-variable values or sends content to an external service. This is bounded preventive scanning, not complete personal-data discovery or a scan of unknown raw bodies/ignored files.

## Atomicity, ownership and recovery

Each reviewed file needs its expected SHA-256 (or null for a genuinely new target). A local exclusive owner lock prevents cooperating writers from interleaving. Versions are checked under ownership and immediately before replacement; stale edits fail without silent overwrites.

Before changing a target, the operation writes/fsyncs before-images and complete staged bytes, then publishes a prepared journal. File replacement is atomic; the multi-file operation is recoverable rather than a filesystem-wide atomic transaction. Query returns RECOVERY_REQUIRED while a write or unresolved journal exists. It checks the operation generation at both read boundaries, so a completed concurrent write/rollback also invalidates an in-flight mixed snapshot.

On a normal error, rollback checks every affected target against its recorded old/new hashes before restoring. It removes only an operation-created new file whose complete bytes still match; unrelated files or new user edits are never automatically removed. A mismatch blocks recovery and retains snapshots for human reconciliation.

A simulated process interruption leaves the journal. Explicit authorized recovery rolls back prepared state; if commit was recorded, it verifies/retains the complete result instead. Receipts and before-images remain under ignored recovery/. Do not publish this folder or automatically delete another operation's lock.

Source admission is a complete, separately authorized checkpoint. Failed wiki synthesis retains that immutable admitted source while rolling back only the wiki/index/log operation; it does not erase source history. Legacy orphan records from older versions still require human reconciliation; they are never silently rehashed or truncated.

On Windows, new raw publication uses rename that refuses an existing destination; other platforms use exclusive linking. Transient Windows sharing failures receive bounded retries with a target-version check, then fail safely. Temporary raw bytes are never exposed as a completed snapshot.

## Recovery procedure

1. Stop the affected workflow; retain the journal and current diff.
2. Verify that the recorded owner is no longer running. Recovery never guesses that a lock is stale. A legacy source registration lock also needs explicit human review.
3. Review the affected paths/hashes and authorize recover(root, authorized=True). If a genuinely stale owner lock remains, acknowledge_stale_lock=True additionally requires direct human confirmation of step 2.
4. On RECOVERY_CONFLICT or BACKUP_MISMATCH, preserve the user's newer bytes separately and reconcile them. Do not reset the checkout, delete arbitrary files, truncate historical metadata or replace raw.
5. Run strict source/security Lint, review the resulting diff and commit the accepted repair.

Directory/power-loss durability and hostile non-cooperating editors are not fully guaranteed by portable standard-library file APIs. Tests inject exceptions and simulated interruption; no physical power-loss test or complete agent/model sandbox evaluation was performed.

## Checks and verdict scope

~~~text
python -B scripts/check_workspace.py --integrity --security
python -B scripts/validate_security.py
python -B -m unittest discover -s tests -v
~~~

The security report separates automated guarded-workflow results from the whole-agent verdict. A passing test suite does not establish containment of an agent that can directly use broader filesystem/shell tools. No deploy, push, merge, global-permission modification, real ingestion or Phase 4 is part of this phase.
