# V5 Codex Consent Non-Canonical Reporting Spec

## Purpose

Define future reporting boundaries for consent validation and abort reports.

Codex is not currently proven drop-in for existing local PAI v5 files. S12B creates no consent report and creates no actual consent artifact or validator.

## Scope

This spec is documentation/design only. It describes possible future report types and fields for consent schema review, validation, revocation, expiration, and abort reporting.

It does not create reports, fixtures, live-trial artifacts, manifests, runtime payloads, PAI Memory, ISA, Pulse state, Claude memory, or Codex memory.

## Evidence Base

Evidence base:

- S12A reporting boundary spec.
- S12A consent model.
- S12B consent artifact schema proposal.
- S12B consent validation and revocation spec.
- S12B consent failure and abort cases.

No live user-local state or existing-local-v5 state was read.

## Reporting Problem Statement

Consent validation may need future evidence, but consent reports must not become canonical state or runtime payloads. They must not become proof that Codex is drop-in.

The problem is to define report boundaries that preserve privacy, non-promotion, no-write behavior, denied-action reporting, unsupported-surface reporting, and abort evidence without authorizing live reads.

## Reporting Principles

Future consent reporting must be:

- Non-canonical unless separately approved.
- Source-specific.
- Consent-status aware.
- Revocation-aware.
- Expiration-aware.
- Abort-aware.
- No-write by default.
- Clear that Codex is not currently proven drop-in.

Reports must not authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory reads or promotion, root AGENTS.md, `.codex/`, runtime adapter implementation, or dual-engine uncoordinated writes.

## Consent Report Type Model

Future report types:

- `consent-schema-review-report`
- `consent-validation-report`
- `consent-revocation-report`
- `consent-expiration-report`
- `consent-abort-report`

S12B creates no consent report and approves none of these report types for live use.

## Required Consent Report Fields

Required future report fields:

- `report_id`
- `report_type`
- `consent_id`
- `source_kind`
- `source_root`
- `pai_dir_candidate`
- `allowed_reads`
- `forbidden_reads`
- `forbidden_writes`
- `runtime_prohibitions`
- `consent_status`
- `validation_status`
- `abort_required`
- `failure_reason`
- `denied_action_report`
- `unsupported_surface_report`
- `pulse_status`
- `memory_status`
- `isa_status`
- `product_memory_status`
- `drop_in_claim_status`
- `non_canonical_statement`
- `retention_policy`
- `provenance`

These fields are proposed only.

## Abort Report Fields

Future abort reports must include:

- Abort ID.
- Failure class.
- Trigger.
- Required response.
- Reported evidence.
- Future proof required.
- Consent status.
- Source kind.
- Source root.
- Non-canonical statement.

Abort reports must not write PAI Memory, ISA, Pulse state, Claude memory, Codex memory, root AGENTS.md, or `.codex/`.

## Non-Canonical Output Rules

Reports are not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not manifests, not runtime payloads, and not proof that Codex is drop-in.

Reports must not be promoted into PAI Memory by default and must not be used as runtime adapter payloads, Codex config, Codex memory, Claude memory, Pulse state, or executable schemas.

## Privacy and Retention Rules

Future reports must avoid storing forbidden read content. Retention must be explicit, source-specific, revocation-aware, and expiration-aware.

If consent is revoked or expired, future reporting must preserve only the minimum non-canonical evidence required by the approved contract and must not continue live reads.

## No-Promotion Rules

No consent report may promote product memory into PAI Memory. No consent report may write discovered paths, source summaries, or consent summaries into PAI Memory, ISA, Pulse, Claude memory, or Codex memory.

Any promotion would require separate architect approval and is outside S12B.

## Denied Action Reporting

Denied action reporting must state:

- No PAI Memory writes.
- No ISA writes.
- No Pulse startup.
- No Pulse endpoint calls.
- No product-memory promotion.
- No product memory reads by default.
- No root AGENTS.md writes.
- No `.codex/` writes.
- No Claude Code invocation.
- No Codex runtime invocation.
- No runtime adapter implementation.
- No drop-in claim.

Denied action reporting is evidence only and does not authorize denied actions.

## Unsupported Surface Reporting

Future reports must identify unsupported surfaces instead of silently ignoring them.

Unsupported surfaces must not be converted into runtime payloads, manifests, executable schemas, Codex config, hooks, rules, skills, agents, commands, launchers, installers, wrappers, Memory payloads, ISA payloads, Pulse payloads, or Pulse bridge files.

## Pulse Reporting Boundary

Pulse reporting must state Pulse status without starting Pulse, calling Pulse endpoints, probing `localhost:31337`, creating Pulse payloads, creating Pulse bridge files, or claiming Pulse parity.

Pulse status remains not-started-not-called unless separately approved.

## Memory and ISA Reporting Boundary

Memory and ISA reporting must state no PAI Memory writes and no ISA writes.

Consent reports are not PAI Memory and not ISA. They must not become Memory payloads or ISA payloads.

## Product Memory Reporting Boundary

Product memory reporting must state that product memory reads are denied by default and product-memory promotion is prohibited by default.

Product memories must not be silently promoted into PAI Memory.

## Drop-In Claim Reporting

Drop-in claim reporting must state not-claimed. A consent artifact, consent validation output, or consent report is not proof that Codex is drop-in.

Reports must not claim Codex is the official upstream engine.

## Required Future Proofs

Future implementation must prove:

- Reports are created only inside an approved write set.
- Reports are non-canonical.
- Reports contain no forbidden read content.
- Reports do not write PAI Memory, ISA, Pulse, Claude memory, or Codex memory.
- Reports preserve denied-action and unsupported-surface evidence.
- Reports do not authorize live reads, runtime adapter work, Pulse behavior, Memory/ISA writes, product-memory promotion, or drop-in claims.

## Prohibited Reporting Designs

Prohibited designs:

- Creating a consent report in S12B.
- Treating a report as PAI Memory, ISA, Pulse state, Claude memory, Codex memory, a manifest, runtime payload, or proof that Codex is drop-in.
- Reporting that starts Pulse, calls endpoints, invokes Claude Code, invokes Codex runtime, implements an adapter, or promotes product memory.
- Reporting that authorizes existing-local-v5 trial execution.

## Non-Goals

S12B creates no consent report, no actual consent artifact, no consent validator, no manifest, no runtime payload, no fixture, no live-trial artifact, no PAI Memory, no ISA, no Pulse state, no Claude memory, no Codex memory, no runtime adapter, no root AGENTS.md, and no `.codex/`.
