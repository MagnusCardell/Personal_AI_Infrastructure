# V5 Codex Consent Validation and Revocation Spec

## Purpose

Define future consent validation, revocation, expiration, and replay-protection rules before live local reads.

Codex is not currently proven drop-in for existing local PAI v5 files. S12B implements no validator and approves no live use of any consent status.

## Scope

This spec is documentation/design only. It describes how a future architect-approved validator could evaluate a future consent artifact before preflight or live read-only access.

It does not create a consent validator, does not create an actual consent artifact, does not read live local state, does not run a live read-only trial, and does not implement runtime adapter behavior.

## Evidence Base

Evidence base:

- S12A consent model.
- S12A source-selection and PAI_DIR detection design.
- S12A preflight and abort model.
- S12A reporting boundary spec.
- S12B consent artifact schema proposal.

No live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, product memory, or existing-local-v5 state was read.

## Validation Problem Statement

A future consent artifact must not become a rubber stamp. Future validation must reject missing, revoked, expired, ambiguous, mismatched, replayed, overbroad, write-authorizing, Pulse-authorizing, Memory/ISA-authorizing, product-memory-authorizing, runtime-authorizing, or drop-in-claiming consent.

Validation must not read live local state by itself. Validation checks the proposed consent record and approved contract boundaries.

## Validation Principles

Future validation must be:

- Read-only.
- Deterministic.
- Fail-closed.
- Source-specific.
- Revocation-aware.
- Expiration-aware.
- Replay-protected.
- Non-canonical in its reporting.

Validation must not write PAI Memory, ISA, Pulse, Claude memory, Codex memory, root AGENTS.md, or `.codex/`.

## Consent Status Model

Future consent statuses:

- `draft`
- `pending-user-approval`
- `approved-for-preflight-only`
- `approved-for-live-read-only`
- `revoked`
- `expired`
- `invalid`
- `aborted`

S12B approves none of these statuses for live use. They are proposed future values only.

## Validation Input Model

Future validation inputs:

- Proposed consent artifact.
- Architect approval reference.
- Source selection record.
- Approved source kind.
- Approved source root.
- Approved allowed reads.
- Approved forbidden reads.
- Approved forbidden writes.
- Runtime prohibitions.
- Reporting boundary policy.

Validation must not discover sources, scan home directories, read live `PAI_DIR`, or inspect product memory by itself.

## Validation Output Model

Proposed validation outputs:

- `consent_valid`
- `consent_scope`
- `allowed_reads`
- `forbidden_reads`
- `forbidden_writes`
- `runtime_prohibitions`
- `abort_required`
- `failure_reason`
- `reporting_boundary`
- `non_canonical_statement`

These outputs are not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, and not runtime payload.

## Revocation Model

Revoked consent must abort. Any non-null `consent_revoked_at` must make future live reads invalid.

Revocation must not write to PAI Memory, ISA, Pulse, Claude memory, Codex memory, root AGENTS.md, or `.codex/`. Revocation reporting must remain non-canonical unless separately approved.

## Expiration Model

Expired consent must abort. Consent whose expiration cannot be parsed, compared, or trusted must be treated as invalid.

Future validation must reject an `approved-for-live-read-only` status after `consent_expires_at`. Expiration must be checked before any future live local read.

## Replay Protection Model

Replayed consent must abort. Consent cannot be reused after expiration, revocation, source-root change, source-kind change, or architect approval change.

Future replay protection should bind `consent_id`, `source_kind`, `source_root`, `architect_approval_reference`, creation time, expiration time, and revocation state.

## Source Root Consistency Checks

Future validation must confirm:

- `source_root` is explicit.
- `source_root_confirmation` matches `source_root`.
- `source_kind` is one allowed value.
- `existing-local-v5-read-only` has explicit user consent plus architect approval.
- `pai_dir_candidate` is future-only and read-only.

Ambiguous or mismatched source root consent must abort.

## Allowed Read Scope Checks

Future validation must confirm allowed reads are:

- Path-bounded.
- Source-specific.
- Within the selected root.
- Not broader than the approved contract.
- Not overlapping forbidden reads.

Allowed reads cannot include product memory by default, `~/.claude/projects/**/memory`, `~/.codex/memories`, broad home scans, or unbounded `~/.claude/` reads.

## Forbidden Read Scope Checks

Future validation must require forbidden reads for:

- Product memory by default.
- `~/.claude/projects/**/memory`.
- `~/.codex/memories`.
- Broad home-directory scans.
- Any source outside the selected source root.
- Any live user-local path not explicitly consented and architect-approved.

If a requested read overlaps a forbidden read, validation must set `abort_required` to true.

## Forbidden Write Checks

Future validation must require forbidden writes for:

- PAI Memory.
- ISA.
- Pulse.
- Product-memory promotion.
- Root AGENTS.md.
- `.codex/`.
- Runtime adapter files.
- Reports, fixtures, manifests, schemas, live-trial artifacts, runtime payloads, Memory payloads, ISA payloads, Pulse payloads, and committed negative fixtures outside an approved write set.

Any write pressure must abort.

## Product Memory Checks

Future validation must reject product-memory reads by default and reject product-memory promotion into PAI Memory.

Product memories must not be silently promoted into PAI Memory. Any product memory exception requires a separate architect-approved policy.

## Pulse Checks

Future validation must require:

- No Pulse startup.
- No Pulse endpoint calls.
- No `localhost:31337` probe.
- No Pulse payloads.
- No Pulse bridge files.
- No Pulse parity claim.

Pulse pressure must abort.

## Memory and ISA Checks

Future validation must require no PAI Memory writes and no ISA writes.

Consent validation output must not become PAI Memory or ISA. It must not update canonical PAI state.

## Runtime Invocation Checks

Future validation must reject:

- Codex runtime invocation.
- Codex runtime adapter execution.
- Codex import or migration tooling.
- Codex hook, rule, or execpolicy commands.
- Claude Code invocation.
- Installer execution.
- Runtime adapter implementation pressure.

Runtime pressure must abort.

## Failure and Abort Rules

Revoked, expired, ambiguous, mismatched, or replayed consent must abort.

Validation must also abort on missing consent, invalid status, source kind mismatch, source root mismatch, overbroad reads, forbidden read overlap, any write requirement, Pulse pressure, PAI Memory pressure, ISA pressure, product-memory pressure, runtime pressure, or drop-in claim pressure.

## Required Future Proofs

Future validation implementation would need proof that:

- It uses only approved inputs.
- It does not read live local state by itself.
- It does not write files outside an approved write set.
- It rejects revoked and expired consent.
- It rejects replayed consent.
- It preserves no Pulse, no PAI Memory, no ISA, no product-memory promotion, no root AGENTS.md, no `.codex/`, no runtime invocation, and no drop-in claim boundaries.

## Prohibited Validation Designs

Prohibited designs:

- A validator created by S12B.
- Validation that reads live local state by itself.
- Validation that writes PAI Memory, ISA, Pulse, Claude memory, Codex memory, root AGENTS.md, or `.codex/`.
- Validation that treats consent as proof Codex is drop-in.
- Validation that starts Pulse, calls endpoints, invokes Claude Code, invokes Codex runtime, runs installers, creates runtime payloads, or promotes product memory.

## Non-Goals

S12B implements no validator, creates no actual consent artifact, runs no live read-only trial, reads no live existing-local-v5 state, inspects no private user-local state, writes no PAI Memory, writes no ISA, starts no Pulse, calls no Pulse endpoints, invokes no Claude Code, invokes no Codex runtime, creates no root AGENTS.md, creates no `.codex/`, and authorizes no product-memory promotion.
