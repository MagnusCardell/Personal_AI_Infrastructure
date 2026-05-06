# V5 Codex Live Read-Only Preflight Report Schema Proposal

## Purpose

Define the future preflight report schema proposal required before any live local PAI v5 read-only trial.

Codex is not currently proven drop-in for existing local PAI v5 files. This is a schema proposal in markdown only.

## Scope

S12D does not create an actual preflight report, does not implement a preflight runner, does not create a detector script, does not create a consent artifact, does not create a consent validator, and does not run a live read-only trial.

This document proposes future preflight report fields and semantics only. It does not read live existing-local-v5 state, inspect live `~/.claude/PAI`, inspect live `~/.claude/projects`, inspect live `~/.codex`, inspect private user-local state, inspect the user's second personal clone, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, or create runtime adapter files.

## Evidence Base

Evidence base:

- S12A live read-only preflight and abort model.
- S12A live read-only reporting boundary spec.
- S12B consent artifact schema proposal.
- S12B consent validation and revocation spec.
- S12C PAI_DIR dry-run detection model.
- S12C PAI_DIR dry-run reporting spec.

No live local state was read for S12D.

## Schema Proposal Status

This is a schema proposal in markdown only. It is not an executable schema, not a manifest, not runtime payload, not a validator, not a preflight runner, and not an implementation artifact.

S12D does not create an actual preflight report. Any future report would require explicit architect approval, explicit user consent design, an approved write set, validation commands, and hard failure conditions.

## Preflight Report Role

A future preflight report would summarize whether a future read-only trial is eligible to proceed to a separately architect-approved read-only trial boundary.

The report role is to bind consent validation, source selection, PAI_DIR candidate checks, allowed reads, forbidden reads, forbidden writes, runtime prohibitions, product memory boundaries, Pulse boundaries, Memory/ISA boundaries, abort reasons, retention, rollback/no-residue, and drop-in claim status into a non-canonical advisory record.

## Non-Canonical Report Rules

The future preflight report is non-canonical unless separately approved.

The future preflight report is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.

It must not be promoted into PAI Memory by default and must not authorize Pulse startup, Pulse endpoint calls, PAI Memory writes, ISA writes, product-memory reads by default, product-memory promotion, root `AGENTS.md`, `.codex/`, runtime adapter work, or live existing-local-v5 trial execution.

## Top-Level Field Model

Proposed top-level fields:

- `schema_id`
- `schema_version`
- `preflight_report_id`
- `preflight_status`
- `consent_id`
- `consent_status`
- `source_kind`
- `source_root`
- `source_root_status`
- `pai_dir_candidate`
- `pai_dir_candidate_status`
- `allowed_reads`
- `forbidden_reads`
- `forbidden_writes`
- `runtime_prohibitions`
- `product_memory_policy`
- `pulse_policy`
- `memory_policy`
- `isa_policy`
- `abort_required`
- `abort_reasons`
- `denied_action_report`
- `unsupported_surface_report`
- `non_canonical_statement`
- `retention_policy`
- `rollback_no_residue_policy`
- `drop_in_claim_policy`
- `architect_approval_reference`

Every field remains proposed only. S12D creates no report containing these fields.

## Identity and Version Fields

Proposed identity and version fields:

- `schema_id`: identifies the future preflight report schema family.
- `schema_version`: identifies the proposed schema version.
- `preflight_report_id`: unique identifier for a future preflight report.
- `preflight_status`: proposed outcome status.
- `architect_approval_reference`: future reference proving the preflight boundary was approved by an architect.

These fields do not make the report canonical and do not authorize live reads by themselves.

## Consent Validation Fields

`consent_id` and `consent_status` must reference a future consent artifact and validation result.

Consent status must prove consent is explicit, source-specific, not expired, not revoked, not replayed, and not inferred from Claude Code installation, Codex installation, dual subscriptions, local config, shell history, product memory, or prior interaction.

Invalid consent must set `abort_required` to true.

## Source Selection Fields

`source_kind`, `source_root`, and `source_root_status` must bind the future report to a single source root and source class.

`existing-local-v5-read-only` and `personal-clone-read-only` remain future-only and require explicit architect approval plus explicit user consent. Source selection does not authorize writes.

## PAI_DIR Detection Fields

`pai_dir_candidate` and `pai_dir_candidate_status` must record only future dry-run evidence.

PAI_DIR candidate status must not imply permission to read live `~/.claude/PAI` by default and must not imply that a clean clone is a live PAI install.

## Allowed Read Fields

`allowed_reads` must be path-bounded, source-specific, consent-bound, and no broader than a future architect-approved contract.

Allowed reads do not include product memory by default, `~/.claude/projects/**/memory`, `~/.codex/memories`, arbitrary home-directory scans, or any source outside the selected root.

## Forbidden Read Fields

`forbidden_reads` must include default denials for live `~/.claude/PAI` absent future approval, live `~/.claude/projects`, live `~/.codex`, product memory by default, arbitrary home-directory scans, personal clones without approval, and any source outside the approved read scope.

Any forbidden read pressure must abort.

## Forbidden Write Fields

`forbidden_writes` must include PAI Memory, ISA, Pulse state, product-memory promotion, root `AGENTS.md`, `.codex/`, runtime adapter files, Codex config, hooks, rules, skills, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, preflight reports outside an approved write set, manifests, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, and committed negative fixtures.

Read-only consent and preflight status do not authorize writes.

## Runtime Prohibition Fields

`runtime_prohibitions` must deny Codex runtime adapter implementation, Codex runtime invocation, Codex import or migration tooling, Codex hook/rule/execpolicy commands, Claude Code invocation, installer execution, launcher creation, wrapper creation, generated runtime config creation, and drop-in claims.

## Product Memory Boundary Fields

`product_memory_policy` must state that product memory reads are denied by default and product memories must not be silently promoted into PAI Memory.

Product-memory access or promotion pressure must set `abort_required` to true unless a separate future architect-approved policy explicitly changes the boundary.

## Pulse Boundary Fields

`pulse_policy` must state:

- No Pulse startup.
- No Pulse endpoint calls.
- No `localhost:31337` probes.
- No Pulse payloads.
- No Pulse bridge files.
- No Pulse parity claim.

Pulse pressure must abort.

## Memory and ISA Boundary Fields

`memory_policy` must state no PAI Memory writes. `isa_policy` must state no ISA writes.

The future report must state that PAI Memory and ISA artifacts are canonical PAI state and that preflight output is neither PAI Memory nor ISA.

## Abort and Failure Fields

`abort_required`, `abort_reasons`, `denied_action_report`, and `unsupported_surface_report` must capture future fail-closed evidence.

Abort reasons must be explicit and machine-checkable in a future implementation. Unsupported surfaces must be reported and not silently ignored.

## Reporting and Retention Fields

`non_canonical_statement` must state the report is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.

`retention_policy` and `rollback_no_residue_policy` must define future retention and cleanup boundaries. S12D creates no retained output.

## Cross-Field Validation Rules

Proposed cross-field rules:

- `preflight_status` cannot be `pass-read-only` if `abort_required` is true.
- `pass-read-only` requires valid architect approval and valid consent.
- `pass-read-only` means only eligible for an architect-approved read-only trial, not drop-in status.
- `existing-local-v5-read-only` and `personal-clone-read-only` require explicit architect approval plus explicit user consent.
- `allowed_reads` must not overlap `forbidden_reads`.
- `forbidden_writes` must include PAI Memory, ISA, Pulse, root `AGENTS.md`, `.codex/`, runtime payloads, and product-memory promotion.
- `drop_in_claim_policy` must remain `not-claimed`.

Allowed future `preflight_status` values:

- `not-run`
- `pass-read-only`
- `abort-required`
- `invalid-consent`
- `invalid-source`
- `invalid-pai-dir`
- `blocked-by-policy`

S12D approves none of these statuses for live use. They are proposed future values only.

## Example Non-Executable Preflight Report

The following block is a documentation sketch only.

```json
{
  "label": "NON-EXECUTABLE DESIGN SKETCH — DO NOT USE AS PREFLIGHT REPORT",
  "schema_id": "v5-codex-preflight-report-proposal",
  "schema_version": "proposal-only-s12d",
  "preflight_report_id": "example-only-not-valid",
  "preflight_status": "not-run",
  "consent_id": "future-consent-required",
  "consent_status": "not-validated",
  "source_kind": "existing-local-v5-read-only",
  "source_root": "future-explicit-source-root-required",
  "source_root_status": "not-validated",
  "pai_dir_candidate": "future-pai-dir-candidate-required",
  "pai_dir_candidate_status": "not-validated",
  "allowed_reads": ["future-path-bounded-read-scope"],
  "forbidden_reads": ["~/.claude/projects", "~/.codex", "product memory by default"],
  "forbidden_writes": ["PAI Memory", "ISA", "Pulse", "root AGENTS.md", ".codex/"],
  "runtime_prohibitions": ["Claude Code invocation", "Codex runtime invocation", "runtime adapter implementation"],
  "product_memory_policy": "no-product-memory-reads-or-promotion-by-default",
  "pulse_policy": "not-started-not-called",
  "memory_policy": "no-pai-memory-writes",
  "isa_policy": "no-isa-writes",
  "abort_required": true,
  "abort_reasons": ["not-run-design-sketch"],
  "denied_action_report": ["no runtime invocation", "no Pulse calls", "no Memory or ISA writes"],
  "unsupported_surface_report": ["future unsupported surfaces must be reported"],
  "non_canonical_statement": "not PAI Memory; not ISA; not Pulse state; not Claude memory; not Codex memory; not a manifest; not runtime payload; not proof that Codex is drop-in",
  "retention_policy": "future-policy-required",
  "rollback_no_residue_policy": "future-policy-required",
  "drop_in_claim_policy": "not-claimed",
  "architect_approval_reference": "future-architect-approval-required"
}
```

## Prohibited Schema Semantics

Prohibited semantics:

- Treating schema proposal as an executable schema.
- Treating `pass-read-only` as drop-in status.
- Treating preflight output as PAI Memory, ISA, Pulse state, Claude memory, Codex memory, a manifest, runtime payload, or replacement proof.
- Authorizing live existing-local-v5 access, personal-clone access, writes, Pulse startup/calls, runtime adapter work, product-memory promotion, or dual-engine uncoordinated writes.

## Future Implementation Gates

Future implementation would require:

- Separate architect approval.
- Explicit user consent.
- Approved write set.
- A real validator design.
- Negative controls for every abort evidence ID.
- No live reads before consent and source checks pass.
- No PAI Memory writes, ISA writes, Pulse startup/calls, product-memory promotion, personal-clone access without approval, or runtime invocation.

## Non-Goals

S12D creates no actual preflight report, creates no preflight runner, creates no detector script, creates no consent artifact, creates no consent validator, runs no live read-only trial, reads no live existing-local-v5 state, inspects no private user-local state, inspects no personal clone, writes no PAI Memory, writes no ISA, starts no Pulse, calls no Pulse endpoints, invokes no Claude Code, invokes no Codex runtime, implements no runtime adapter, creates no root `AGENTS.md`, creates no `.codex/`, and authorizes no product-memory promotion.
