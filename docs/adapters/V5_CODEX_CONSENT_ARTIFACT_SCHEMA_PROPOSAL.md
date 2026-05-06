# V5 Codex Consent Artifact Schema Proposal

## Purpose

Define the future consent artifact schema proposal required before any live local PAI v5 read-only trial.

Codex is not currently proven drop-in for existing local PAI v5 files. This is a schema proposal in markdown only. S12B does not create an actual consent artifact and does not create a consent validator.

## Scope

This document proposes future fields, semantics, and validation boundaries for an architect-approved consent artifact that could be considered by a later milestone.

It does not create a consent artifact, does not create a JSON schema file, does not create a validator, does not run a live read-only trial, does not read live existing-local-v5 state, does not read live user-local state, and does not authorize runtime adapter work.

## Evidence Base

Evidence base:

- S10 fixture-only validation closeout.
- S11 release-fixture evidence closeout.
- S12A live read-only consent model.
- S12A PAI_DIR detection and source selection spec.
- S12A preflight and abort model.
- S12A reporting boundary spec.

No live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, product memory, or existing-local-v5 state was read for S12B.

## Schema Proposal Status

This is a schema proposal in markdown only. It is not an executable schema, not a manifest, not runtime payload, not a validator, and not an implementation artifact.

S12B does not create an actual consent artifact. Any future artifact would require explicit architect approval, explicit user consent design, approved write set, validation commands, and hard failure conditions.

## Consent Artifact Role

A future consent artifact would record explicit user consent for a specific future source kind and source root. It would not grant general access to user-local state.

The artifact role is to bind source selection, allowed reads, forbidden reads, forbidden writes, runtime prohibitions, retention, revocation, expiration, and abort behavior into a future non-canonical record.

## Non-Canonical Artifact Rules

A future consent artifact is non-canonical unless separately approved.

A future consent artifact is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, not a runtime adapter payload, and not proof that Codex is drop-in.

It must not be promoted into PAI Memory by default and must not authorize Pulse startup, Pulse endpoint calls, PAI Memory writes, ISA writes, product-memory reads by default, product-memory promotion, root AGENTS.md, or `.codex/`.

## Top-Level Field Model

Proposed top-level fields:

- `schema_id`
- `schema_version`
- `consent_id`
- `consent_status`
- `consent_created_at`
- `consent_expires_at`
- `consent_revoked_at`
- `principal_acknowledgement`
- `source_kind`
- `source_root`
- `source_root_confirmation`
- `pai_dir_candidate`
- `allowed_read_scope`
- `forbidden_read_scope`
- `forbidden_write_scope`
- `runtime_prohibitions`
- `product_memory_policy`
- `pulse_policy`
- `memory_policy`
- `isa_policy`
- `reporting_policy`
- `retention_policy`
- `rollback_no_residue_policy`
- `drop_in_claim_policy`
- `architect_approval_reference`
- `stop_conditions`

Every field remains proposed only. S12B creates no artifact containing these fields.

## Identity and Version Fields

Proposed identity and version fields:

- `schema_id`: identifies the future consent schema family.
- `schema_version`: identifies the proposed schema version.
- `consent_id`: unique identifier for a future consent decision.
- `consent_status`: future validation status such as draft, approved-for-preflight-only, revoked, expired, invalid, or aborted.
- `consent_created_at`: proposed creation timestamp.
- `consent_expires_at`: proposed expiration timestamp.
- `consent_revoked_at`: proposed revocation timestamp, null unless revoked.

These fields do not make the artifact canonical and do not authorize live reads by themselves.

## User Disclosure Fields

`principal_acknowledgement` must prove the user acknowledged:

- Codex is not currently proven drop-in for existing local PAI v5 files.
- The future trial is read-only unless separately approved.
- Consent is explicit user consent and source-specific.
- Consent is revocable and expiring.
- Consent is not inferred from Claude Code installation, Codex installation, or dual subscriptions.
- Consent does not authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory reads or promotion, root AGENTS.md, `.codex/`, runtime adapter work, or drop-in claims.

## Source Selection Fields

`source_kind` allowed future values:

- `release-fixture`
- `sanitized-user-fixture`
- `existing-local-v5-read-only`

`existing-local-v5-read-only` is future-only and requires explicit user consent plus architect approval.

`source_root` must be explicit and source-specific. `source_root_confirmation` must bind the selected source root to user acknowledgement. `pai_dir_candidate` may only be used in a future read-only, path-bounded, architect-approved PAI_DIR detection design.

## Allowed Read Scope Fields

`allowed_read_scope` must define exactly what may be read under the approved future source root.

It must be path-bounded, read-only, and narrower than the source root when possible. It must not imply product memory reads, arbitrary home-directory scans, broad `~/.claude/` reads, `~/.claude/projects/**/memory` reads, or `~/.codex/memories` reads.

## Forbidden Read Scope Fields

`forbidden_read_scope` must include default denials for:

- Live `~/.claude/` unless explicitly approved by a future card.
- Live `~/.claude/PAI` unless explicitly approved by a future card.
- `~/.claude/projects/**/memory`.
- `~/.codex/memories`.
- Product memory by default.
- Broad home-directory scans.
- Any source outside the consented root.

Forbidden reads must fail closed and trigger abort behavior.

## Forbidden Write Scope Fields

`forbidden_write_scope` must include:

- PAI Memory writes.
- ISA writes.
- Pulse state writes.
- Product-memory promotion.
- Root AGENTS.md writes.
- `.codex/` writes.
- Codex config, hooks, rules, skills, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, and committed negative fixtures.

Consent is not a write authorization.

## Runtime Prohibition Fields

`runtime_prohibitions` must deny:

- Codex runtime adapter implementation.
- Codex runtime invocation.
- Codex import or migration tooling.
- Codex hook, rule, or execpolicy commands.
- Claude Code invocation.
- Installer execution.
- Launcher or wrapper creation.

The artifact must not claim Codex is drop-in today or official upstream engine.

## Product Memory Boundary Fields

`product_memory_policy` must state:

- Product memory reads are denied by default.
- Product memories must not be silently promoted into PAI Memory.
- Product-memory promotion requires separate architect approval, single-writer policy, provenance, rollback, validation, and conflict handling.

## Pulse Boundary Fields

`pulse_policy` must state:

- No Pulse startup.
- No Pulse endpoint calls.
- No `localhost:31337` probe.
- No Pulse payloads.
- No Pulse bridge files.
- No Pulse parity claim.

Pulse status remains not-started-not-called unless separately approved.

## Memory and ISA Boundary Fields

`memory_policy` must state no PAI Memory writes. `isa_policy` must state no ISA writes.

The future artifact must state that PAI Memory and ISA artifacts are canonical PAI state and that consent does not authorize writing either one.

## Reporting and Retention Fields

`reporting_policy` must identify future non-canonical report outputs and denied-action reporting requirements.

`retention_policy` must define how long future consent and reports may be retained, how revocation affects retention, and whether no-residue handling is required.

Reporting must not create PAI Memory, ISA, Pulse state, Claude memory, Codex memory, a manifest, runtime payload, or PAI runtime audit artifact by default.

## Revocation and Expiration Fields

`consent_expires_at` and `consent_revoked_at` must be first-class proposed fields.

Revoked consent must abort. Expired consent must abort. Ambiguous revocation or expiration must abort. A future consent artifact must not be replayed after expiration or revocation.

## Cross-Field Validation Rules

Proposed cross-field rules:

- `existing-local-v5-read-only` requires explicit user consent plus architect approval.
- `approved-for-live-read-only` cannot be valid if `consent_expires_at` is in the past.
- Any non-null `consent_revoked_at` makes live read invalid.
- `source_root` must match `source_root_confirmation`.
- `allowed_read_scope` must not overlap forbidden reads.
- `forbidden_write_scope` must include PAI Memory, ISA, Pulse, root AGENTS.md, `.codex/`, runtime payloads, and product-memory promotion.
- Runtime prohibitions must include Claude Code invocation and Codex runtime invocation.
- `drop_in_claim_policy` must remain `not-claimed`.

## Example Non-Executable Consent Artifact

The following block is a documentation sketch only.

```json
{
  "label": "NON-EXECUTABLE DESIGN SKETCH — DO NOT USE AS CONSENT",
  "schema_id": "v5-codex-consent-artifact-proposal",
  "schema_version": "proposal-only-s12b",
  "consent_id": "example-only-not-valid",
  "consent_status": "draft",
  "consent_created_at": "future-timestamp-required",
  "consent_expires_at": "future-expiration-required",
  "consent_revoked_at": null,
  "principal_acknowledgement": {
    "codex_drop_in_claim": "not-claimed",
    "explicit_user_consent": "required",
    "source_specific": true,
    "revocable": true
  },
  "source_kind": "existing-local-v5-read-only",
  "source_root": "future-explicit-source-root-required",
  "source_root_confirmation": "must-match-source-root",
  "pai_dir_candidate": "future-only-read-only-detection",
  "allowed_read_scope": ["future-explicit-path-bounded-read-scope"],
  "forbidden_read_scope": ["~/.claude/projects/**/memory", "~/.codex/memories", "product memory by default"],
  "forbidden_write_scope": ["PAI Memory", "ISA", "Pulse", "root AGENTS.md", ".codex/"],
  "runtime_prohibitions": ["Codex runtime invocation", "Claude Code invocation", "runtime adapter implementation"],
  "product_memory_policy": "no-product-memory-reads-or-promotion-by-default",
  "pulse_policy": "not-started-not-called",
  "memory_policy": "no-pai-memory-writes",
  "isa_policy": "no-isa-writes",
  "reporting_policy": "non-canonical-reporting-only",
  "retention_policy": "future-policy-required",
  "rollback_no_residue_policy": "future-policy-required",
  "drop_in_claim_policy": "not-claimed",
  "architect_approval_reference": "future-architect-approval-required",
  "stop_conditions": ["revoked", "expired", "write pressure", "Pulse pressure", "runtime pressure"]
}
```

This example is not consent, not a manifest, not runtime payload, and not an executable schema.

## Prohibited Schema Semantics

Prohibited semantics:

- Treating the proposal as an actual consent artifact.
- Treating any future artifact as PAI Memory, ISA, Pulse state, Claude memory, Codex memory, a manifest, runtime payload, or proof that Codex is drop-in.
- Inferring consent from Claude Code installation, Codex installation, or dual subscriptions.
- Authorizing PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory promotion, root AGENTS.md, `.codex/`, runtime adapter work, live trials, or dual-engine uncoordinated writes.

## Future Implementation Gates

Future implementation would require:

- Architect approval.
- Explicit user consent design.
- Approved write set.
- A real schema file only if separately authorized.
- A real validator only if separately authorized.
- Negative controls for missing, expired, revoked, ambiguous, mismatched, replayed, and overbroad consent.
- Protected-path, no-write, no-Pulse, no-Memory, no-ISA, and no-runtime validation.

## Non-Goals

S12B does not create an actual consent artifact, create a consent validator, run a live read-only trial, read existing-local-v5 state, inspect live user-local state, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, probe `localhost:31337`, invoke Claude Code, invoke Codex runtime, implement a runtime adapter, create root `AGENTS.md`, create `.codex/`, create a manifest, create runtime payload, create a report, create fixtures, or authorize product-memory promotion.
