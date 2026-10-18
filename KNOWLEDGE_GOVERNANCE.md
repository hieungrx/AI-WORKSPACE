# Phase 2 — Knowledge Governance Specification

First-party V1 operating contract. Extends the existing Markdown metadata, Python checks and Query helper. No database, new dependency, production knowledge or Phase 3.

## Discovery and compatibility

The discovery baseline was a7f387a on workspace/initialize, with a pre-existing Obsidian graph change. The Phase 1 report records PASS; its 81 tests were rerun successfully before this implementation. Source hashing, append-only provenance and source replacement remain authoritative under [Source integrity](SOURCE_INTEGRITY.md).

Existing wiki metadata has DRAFT / REVIEWED / STALE, Updated and Source IDs. Existing ADRs use PROPOSED / APPROVED. Those labels lack a machine-checkable lifecycle history and content-bound validation approval. Existing scope equality already isolates lexical matches, but had no explicit cross-project context or restricted-scope gate.

The read adapter preserves existing files byte-for-byte: DRAFT becomes draft; REVIEWED and STALE become unverified, never verified. STALE retains its existing Lint warning. Missing scope remains unscoped, never global. Legacy ADR approval remains available to the legacy manual workflow; the adapter labels its authority unvalidated, and lexical Query does not resolve legacy ADRs automatically. Governed pages cannot use legacy ADR approval as sufficient authority. Known foreign-scope ADRs cannot establish local choices.

New and explicitly upgraded pages use the single contract below. Mixing Updated / Related project with canonical fields is an error. No schema_version is necessary: presence of the governance fields selects strict validation. There is no automatic bulk migration or history reconstruction.

## Stable metadata

Keep existing Markdown bullets, Source IDs, Decision references and multilingual fields.

- Status: draft / unverified / verified / disputed / superseded / archived.
- kind: external_fact / interpretation / hypothesis / requirement / proposed_decision / approved_decision / historical_decision.
- Scope: one exact identifier. global is explicitly shared knowledge; arbitrary project IDs are data, not core constants. A project query never implicitly includes global.
- created_at and updated_at: required ISO calendar dates. Unknown legacy creation dates stay unknown in compatibility mode; do not invent an old date when upgrading. A newly created governed replacement can use its actual creation date and link its legacy context.
- effective_at: optional date a rule or choice takes effect, independently of publication/review. Future-effective pages require explicit contextual/history lookup.
- reviewed_at: optional last validation date; verified requires the latest verification event's date.
- superseded_by: root-relative wiki/decision path, required for superseded. The successor must have the same kind/scope and a verified or historical lifecycle; self-links and cycles fail validation. Original records remain.
- temporal: historical / current / time_sensitive. This says what the statement describes, not how trustworthy it is.
- review_after: optional explicit review deadline; it does not automatically expire or change knowledge.
- transitions: JSON array, initially empty. Append events; never fabricate earlier transitions.
- conflicts: optional JSON array of objects with summary, source_ids (at least two IDs also listed in Source IDs), and resolution (null until documented). Preserve all references after resolution.
- cross_project_refs: optional JSON array of exact root-relative wiki/decision paths, for context only.
- access: workspace (default) / restricted. Restricted retrieval requires explicit authorization for that exact scope.

Dates are day precision. created_at <= updated_at; reviewed_at lies within those dates. Optional metadata is omitted or empty, never guessed. Invalid types, duplicate metadata keys, missing required values, mixed old/new fields and untraced states fail validation.

Each page is a coherent knowledge unit. Split claims requiring different lifecycles into separate pages; labels and source pointers still apply to each claim. A verified page is not blanket approval of every unstructured sentence.

FACT denotes the type of assertion, not an automatic verification result. Source verification_status from Phase 1 and the wiki lifecycle are separate: validating a claim never rewrites source trust or raw provenance. An approved ADR proves a documented project choice only; its external supporting claims still require intact registered sources, including when another page references that ADR.

## Lifecycle state machine and authority

~~~mermaid
stateDiagram-v2
    [*] --> draft
    draft --> unverified
    draft --> archived
    unverified --> draft
    unverified --> verified
    unverified --> disputed
    unverified --> archived
    verified --> unverified
    verified --> disputed
    verified --> superseded
    verified --> archived
    disputed --> unverified
    disputed --> archived
    superseded --> archived
    archived --> draft
~~~

Every event contains from, to, actor (ai / human), at, reason and approval (path or null). The chain starts at draft, is contiguous/date ordered and ends at Status. New verification and dispute-resolution events additionally carry approval_policy: 2 and approval_content_hash, as specified below. Other transitions retain the six-field format.

- An authorized AI maintenance task may prepare draft/unverified work, demote verified to unverified or flag a dispute. It cannot verify, supersede, archive, restore or resolve a dispute.
- A human controls verification, supersession, archival, restoration and dispute resolution. Verification and resolution require a documented approval record and validation evidence. A dispute resolves to unverified before a separate verification.
- interpretation, hypothesis and proposed_decision cannot become verified. Evidence-backed external facts and separately authorized decisions use their appropriate kind. A requirement records intent, never proof of implementation.
- approved_decision is only authoritative while verified with documented approval. Superseded/archived approved decisions become historical context. Merely typing approved_decision, historical_decision or reviewed_at does not establish approval.
- Preserve a proposal when an approved decision is authored separately. The agent must not change kind to manufacture decision authority.

The transition function returns proposed Markdown by default. Applying it additionally requires scoped maintenance authorization and checks for concurrent changes. It does not create approvals, infer evidence, fetch URLs or write raw sources.

## Documented verification approval

Only the authorized human may create/approve validation records under experiments/. An agent may prepare an explicitly unapproved proposal; it must never fabricate APPROVED records or human actions. Validation approvals stay separate from decision ADRs. Automated tests simulate approvals solely in disposable TEST_ONLY fixtures.

A validation record uses these Markdown bullets:

~~~text
- Status: APPROVED
- authority: human
- target: wiki/example.md
- content_hash: sha256:<hash from knowledge_governance.content_hash>
- approval_policy: 2
- from_state: unverified
- to_state: verified
- prior_transitions_hash: sha256:<hash from knowledge_governance.history_hash of existing transitions>
- validated_at: YYYY-MM-DD
- evidence: ["reports/existing-validation.md"]
~~~

Evidence must point to existing local reports/experiments/decisions, independently of the approval record. The human must check the claim, actual source pointers, evidence relevance and validation outcome. A file's existence, model agreement, a source citation or a matching hash alone is insufficient.

The approval binds body and stable metadata (including kind, scope, conflicts, deadlines and access), with normalized text line endings. Status, updated_at, reviewed_at, superseded_by and transitions are lifecycle bookkeeping excluded from that hash. Editing verified content invalidates approval. Revert the unauthorized edit, or explicitly demote using the approved snapshot before editing and revalidating; never update an approval hash merely to silence an error.

Records are local human-review assertions, not cryptographic proof of the reviewer's identity. Git review, the task authorization boundary and filesystem permissions remain necessary against someone able to forge both records and content.

### Action binding and historical policy

For every new required approval (verification or disputed → unverified), the approval's exact target, from_state/to_state, validated_at, content_hash and prior_transitions_hash must match the subject and event. The helper records approval_policy: 2 and approval_content_hash in the appended event. Use a distinct human-reviewed approval record for each event; a record bound to one history position cannot authorize a later cycle or a different transition. The public lifecycle writer independently rechecks the same validator under write ownership before publishing any journal or target. New wiki creation starts draft with no imported lifecycle history.

Optional expires_at and revoked_at are ISO dates, with day precision. A new commit rejects a revoked approval or one expired on the event date or commit date. Historical replay evaluates validity on the event date: later expiration/revocation does not erase a valid past event. It does block current eligibility through APPROVAL_EXPIRED/APPROVAL_REVOKED. REVOKED requires a revocation date to establish whether an older event preceded it; unknown validity fails closed. An unchanged APPROVED status does not override a revocation date already reached. Expiration is inclusive through its specified date.

Unversioned historical events/records select legacy approval policy 1. Replay now checks every required approval's existence, human authority, state/validity, target, event date and validation evidence, including dispute resolution. The active last verification must still bind the current content. A legacy event has no historical content snapshot or transition-position binding; when its old hash differs from today's content, Lint reports LEGACY_APPROVAL_SNAPSHOT_UNAVAILABLE. This is an unverified historical-content limitation, not a fabricated reconstruction. A new policy-2 approval can review the current subject and bind the retained legacy prefix; it does not certify unavailable old snapshots. Policy 1 cannot authorize a new required-approval write.

Invalid required approvals produce errors in the reader, Query and integrity Lint even when the page ends unverified or draft. They cannot be repaired by deleting events, rehashing an approval or downgrading an error to a warning. Preserve affected bytes and review the error report as an in-place quarantine: exclude the invalid record from authoritative retrieval. Only a separately authorized reconciliation may restore genuine historical evidence or create a new draft replacement linked to the preserved original. Do not invent an old approval or relabel old events as policy 2. No live event migration is performed by this remediation.

## Isolation and Query rules

Queries require exact scope. No project names are hardcoded. For wiki/projects/<id>/ pages, Scope must agree with <id>. Other layouts use explicit metadata; the tool cannot infer whether a human selected the correct real-world project.

Cross-project access requires both a declared cross_project_refs edge on an accessible anchor-scope page and a user-requested --cross-ref path. Only that target is retrieved; its own references are not recursively followed. Preserve its original scope and mark cross_project_context; it never establishes the anchor project's current configuration. Foreign wiki/ADR links inside structured factual findings fail validation. Put such references in context sections and declare the lookup edge instead.

Restricted scopes also require --allow-restricted-scope with task authorization. These are retrieval gates in a local single-user workspace, not OS ACLs or a multi-user security boundary. Lint and source-integrity auditing remain workspace-wide; never store secrets here.

Query outputs include knowledge_status, information_type, decision_authority, freshness, conflicts and superseded_by. usable_as_current_truth only indicates eligibility for the selected scope after those gates, source integrity and approval checks; it does not certify factual correctness or implementation. Legacy, proposed, historical, disputed, future-effective, overdue or cross-project content is never eligible.

Default retrieval excludes superseded/archived and future-effective records. --include-history returns them as context, preserving dates and successor pointers. Historical facts remain retrievable in ordinary queries when relevant, without implying current project configuration.

### Canonical evidence and ADR eligibility

knowledge_governance.evaluate_evidence is the shared evaluator for Query and Lint. It applies current_eligibility to the subject and every supporting ADR: verified approval, exact scope, current temporal context, effective date, explicit review deadline and approval validity must all permit current use. REVIEW_DUE and REVIEW_DATE_UNSET require review/reapproval for current eligibility; they never automatically change lifecycle status. A referenced historical, superseded, future-effective or overdue ADR can remain traceable context with eligible_for_current_truth=false and context_only=true. FOUND does not imply usable_as_current_truth.

Evidence is evaluated per structured finding. Every finding needs sufficient valid evidence before the coherent page can be current. An intact registered source with its exact pointer can independently support the same finding even if an accompanying ADR is ineligible. A source cited by a different finding cannot cover an unsupported claim. Explicitly cited missing/tampered raw evidence is never silently replaced by an ADR. Ordinary wiki links do not introduce another source of authority; synthesized/derived pages must retain original source IDs or direct first-party ADR proof.

First-party ADR choices can use their own documented approval, but explicit dependent ADRs must be evaluated transitively; a self-link or cycle cannot bootstrap authorization. Missing/invalid/foreign/restricted references fail closed. Decision references metadata is validated as direct ADR links and retained as context; it is not blanket evidence for unlinked claims. Lint reports broken, unsupported or cyclic evidence as errors and valid-but-ineligible dependencies as warnings on their consumers. An independent valid source is not discarded merely because an optional context reference needs review.

There is no persistent eligibility cache or full-text index. Each operation rereads current records/approvals; date and lifecycle changes are evaluated without rebuilding wiki pages. Dependency depth is capped at 32 as an explicit fail-closed resource guard (DECISION_EVIDENCE_LIMIT), not measured capacity or an SLA. Dense DAG cost and larger/deeper graph workloads remain unmeasured; no Phase 5 flat-corpus timing is claimed to cover this evaluator.

~~~text
python -B scripts/query_workspace.py --scope global --query "<question>"
python -B scripts/query_workspace.py --scope <project-id> --query "<question>"
python -B scripts/query_workspace.py --scope <project-id> --query "<question>" --cross-ref wiki/other.md
python -B scripts/query_workspace.py --scope <project-id> --query "<question>" --include-history
~~~

## Freshness and conflicts

Age alone never changes status. Historical facts do not expire because their creation date is old. Current/time-sensitive content without a review_after gets a review warning; an exceeded deadline produces REVIEW_DUE. Both require review, not automatic obsolescence. Future effective_at is NOT_YET_EFFECTIVE. No background scheduler or deletion is introduced.

Conflicts retain source IDs, summary and any resolution. Unresolved conflicts produce warnings and DISPUTED Query output with both source citations, never a verified answer. A disputed page requires a conflict record. Verification is blocked while any conflict remains unresolved. A human documents resolution and validation before moving to unverified, then separately verifies. The checker cannot discover all semantic disagreements by itself.

## Operations and compatibility checks
Phase 3 [security policy](SECURITY_POLICY.md) routes applied transitions through the shared version-checked, journaled writer. Verified wiki content still has DATA trust; it cannot issue commands, create human approvals or change permissions. A pending operation blocks Query until recovery completes.


Ingest retains Phase 1 admission/hashing, starts new synthesis at draft and proposes governance metadata within task authorization. Query stays read-only. Lint reports lifecycle/authority/scope/freshness failures; it never promotes, resolves or deletes content.

~~~text
python -B scripts/check_workspace.py --integrity
python -B -m unittest discover -s tests -v
python -B scripts/validate_knowledge_governance.py
python -B scripts/validate_governance_remediation.py --output reports/<new-remediation-name>.json
~~~

Compatibility is exercised by the unchanged Phase 1 and multilingual tests, legacy read-only retrieval, template copying at two depths, and the new authority/scope workflows. The live starter wiki is not rewritten. Real ingestion, legacy upgrades and human approval of actual claims remain separate tasks.

The remediation validator runs the complete existing suite fresh, records scoped code hashes before/after, and repeats the original ADR-parent Query and six-field missing-approval lifecycle transaction. It does not import PASS assertions from previous reports. Use a new output basename; previous audit findings remain immutable historical evidence.
