# V5 Codex Live Read-Only Reporting Boundary Spec

## Purpose

Define future live-read-only reporting boundaries and non-canonical output rules.

Codex is not currently proven drop-in for existing local PAI v5 files. S12A creates no live-read report and does not authorize live existing-local-v5 access.

## Scope

This spec applies to future reporting design for possible read-only consent, source selection, preflight, abort, and evidence outputs.

It does not create a live-read report, does not create PAI Memory, does not create ISA, does not create Pulse state, does not create Claude memory, does not create Codex memory, does not create a manifest, does not create a runtime payload, and does not create a PAI runtime audit artifact.

## Evidence Base

Evidence base:

- S10 fixture-only validation closeout.
- S11 release-fixture evidence closeout.
- S11A non-canonical release-fixture evidence report.
- S11B report-generator negative controls.
- S11C readiness gate evaluation.
- S11D proposed S12 reporting and rollback requirements.

S12A creates documentation only and no live-read report.

## Reporting Problem Statement

Future live read-only evidence could be useful for architect review, but reporting must not become a back door into canonical memory, runtime audit artifacts, manifests, or runtime payloads.

The reporting problem is to identify what a future report may say while preserving privacy, no-write behavior, non-promotion, unsupported-surface reporting, denied-action reporting, rollback/no-residue status, and no drop-in claim.

## Reporting Principles

Future reporting must be:

- Non-canonical unless separately approved.
- Read-only in source behavior.
- Bounded to explicit consent and explicit source selection.
- No-residue where required.
- Clear about denied actions and unsupported surfaces.
- Clear that Codex is not currently proven drop-in.

Reports must not authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory promotion, root `AGENTS.md`, `.codex/`, runtime adapter work, live trials beyond the approved scope, or dual-engine uncoordinated writes.

## Report Type Model

Future report types:

- `consent-preflight-report`
- `source-selection-report`
- `live-read-only-preflight-report`
- `abort-report`
- `live-read-only-evidence-report`

S12A creates no live-read report and approves none of these report types for execution.

## Required Report Fields

Required future fields:

- Report ID.
- Source kind.
- Consent reference.
- Source root.
- Allowed reads.
- Forbidden reads.
- Forbidden writes.
- Denied action report.
- Unsupported surface report.
- Pulse status.
- Memory status.
- ISA status.
- Product memory status.
- Runtime invocation status.
- Drop-in claim status.
- Rollback/no-residue status.
- Non-canonical statement.

Any future report must also identify whether it is based on `release-fixture`, `sanitized-user-fixture`, or future-only `existing-local-v5-read-only` sources.

## Non-Canonical Output Rules

Every future report is non-canonical unless separately approved.

Future reports are not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a PAI runtime audit artifact, not a manifest, and not runtime payload.

Future reports must not be promoted into PAI Memory by default and must not be used as runtime payloads, Codex memory, Claude memory, Pulse state, or adapter configuration.

## Privacy and Retention Rules

Future reports must identify retention policy before any live read occurs. Reports must avoid broad private-state capture, must redact or summarize when required by a future contract, and must not include forbidden read content.

Report retention must be consent-bound and revocable where a future contract allows. S12A creates no retained live-read output.

## No-Promotion Rules

No report may be promoted into PAI Memory by default. No report may promote product memory into PAI Memory. No report may write discovered paths or source summaries into PAI Memory, ISA, Pulse, Claude memory, or Codex memory.

Any future promotion would require separate architect approval, single-writer policy, provenance, rollback, validation, and conflict handling.

## Denied Action Reporting

Future reports must state denied actions clearly:

- No root `AGENTS.md`.
- No `.codex/`.
- No PAI Memory writes.
- No ISA writes.
- No Pulse startup.
- No Pulse endpoint calls.
- No product-memory promotion.
- No Claude Code invocation.
- No Codex runtime invocation.
- No runtime adapter implementation.
- No drop-in claim.

Denied action reporting is evidence for architect review only; it does not authorize the denied actions.

## Unsupported Surface Reporting

Future reports must identify unsupported surfaces without converting them into runtime payloads.

Unsupported surfaces may include authority boundaries, compact router boundaries, launcher/inference boundaries, hook/lifecycle boundaries, event/context envelope boundaries, Pulse boundaries, Memory/ISA boundaries, manifest/audit schema boundaries, rollback boundaries, denied paths, and dual-engine boundaries.

Unsupported-surface reporting must not imply support and must not copy Claude-shaped files directly into Codex surfaces.

## Pulse Reporting Boundary

Pulse reporting must preserve no-start and no-call status unless a separate future card explicitly approves otherwise.

Future reports must state Pulse status without starting Pulse, calling Pulse endpoints, probing `localhost:31337`, creating Pulse payloads, or claiming Pulse parity.

## Memory and ISA Reporting Boundary

Future reports must state Memory and ISA status without writing PAI Memory or ISA.

Reports must state that PAI Memory and ISA artifacts are canonical PAI state and that report output is not PAI Memory and not ISA. Reports must not become a Memory payload or ISA payload.

## Product Memory Reporting Boundary

Future reports must state product memory status. Product memory reads are denied by default, and product memories must not be silently promoted into PAI Memory.

Any future report that observes a product-memory boundary must report denial or unsupported status rather than importing, promoting, normalizing, or writing product memory.

## Drop-In Claim Reporting

Future reports must state drop-in claim status as `not-claimed` unless a later architect-approved validation track proves replacement-grade behavior.

S12A and future live read-only readiness reports must not claim Codex is drop-in today and must not claim Codex is the official upstream engine.

## Required Future Proofs

Required future proofs:

- Report path is inside an approved write set.
- Report content is non-canonical.
- Report does not include forbidden reads.
- Report does not write PAI Memory, ISA, Pulse, Claude memory, or Codex memory.
- Report does not create a manifest, runtime payload, PAI runtime audit artifact, root `AGENTS.md`, or `.codex/`.
- Report preserves denied-action and unsupported-surface status.
- Report preserves rollback/no-residue status.

## Prohibited Reporting Designs

Prohibited designs:

- Reports treated as PAI Memory, ISA, Pulse state, Claude memory, Codex memory, manifests, runtime payloads, or PAI runtime audit artifacts by default.
- Reports that authorize live existing-local-v5 access beyond approved consent.
- Reports that promote product memory into PAI Memory.
- Reports that start Pulse, call Pulse endpoints, invoke Claude Code, invoke Codex runtime, or implement a runtime adapter.
- Reports that claim Codex is drop-in today or official upstream engine.

## Non-Goals

S12A creates no live-read report, no PAI Memory, no ISA, no Pulse state, no Claude memory, no Codex memory, no manifest, no runtime payload, no PAI runtime audit artifact, no root `AGENTS.md`, no `.codex/`, no runtime adapter, and no live existing-local-v5 access authorization.
