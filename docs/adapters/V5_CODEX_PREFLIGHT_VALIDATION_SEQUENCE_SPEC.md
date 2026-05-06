# V5 Codex Preflight Validation Sequence Spec

## Purpose

Define future live-read-only preflight validation sequence without implementing it.

Codex is not currently proven drop-in for existing local PAI v5 files. S12D implements no validation sequence.

## Scope

This document is documentation/design only. It defines a future validation sequence that could be considered before a future live existing-local-v5 read-only trial.

S12D does not implement a preflight runner, create a preflight report, create a detector script, create a consent artifact, create a consent validator, read live local state, run a live read-only trial, or implement runtime adapter behavior.

## Evidence Base

Evidence base:

- S12A preflight and abort model.
- S12B consent validation and revocation spec.
- S12C PAI_DIR dry-run detection model.
- S12C PAI_DIR detection failure cases.
- S12D preflight report schema proposal.

No live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, existing-local-v5 state, product memory, or personal clone was read.

## Validation Sequence Problem Statement

A future preflight sequence must prove the candidate read-only trial is inside the approved consent, source, no-write, Pulse, Memory/ISA, product-memory, runtime, and reporting boundaries before any live local read can proceed.

The sequence must fail closed. Any failed step must abort.

## Validation Principles

Future validation must be:

- Architect-approved.
- Read-only.
- Consent-bound.
- Source-specific.
- Path-bounded.
- Deterministic.
- Fail closed.
- Abortable.
- Non-runtime.
- Non-canonical in output.

Validation must not read live local state by itself. Validation must not write PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, or `.codex/`. Validation must not start Pulse or call Pulse endpoints. Validation must not invoke Claude Code or Codex runtime.

## Sequence Input Model

Future sequence inputs:

- Architect approval reference.
- Consent artifact reference.
- Consent validation result.
- Declared source kind.
- Declared source root.
- PAI_DIR candidate.
- Allowed reads.
- Forbidden reads.
- Forbidden writes.
- Runtime prohibitions.
- Product memory policy.
- Pulse policy.
- Memory policy.
- ISA policy.
- Reporting policy.

S12D creates none of these as artifacts.

## Sequence Output Model

Future sequence outputs:

- `preflight_status`
- `abort_required`
- `abort_reasons`
- `denied_action_report`
- `unsupported_surface_report`
- `non_canonical_statement`

Output is advisory and non-canonical by default. It is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.

## Step P0: Architect Approval Check

Future-only step. Confirm an architect-approved card exists for the exact preflight milestone, write set, read set, validation commands, source kind, and stop conditions.

If approval is missing, invalid, ambiguous, or stale, fail closed and abort.

## Step P1: Consent Validation

Future-only step. Confirm consent exists, is explicit, source-specific, not expired, not revoked, not replayed, and matches the proposed source root.

If consent is missing, expired, revoked, mismatched, ambiguous, overbroad, or inferred from installation/subscription state, fail closed and abort.

## Step P2: Source Kind Validation

Future-only step. Confirm the source kind is approved and matches consent.

`existing-local-v5-read-only` and `personal-clone-read-only` remain future-only and require explicit architect approval plus explicit user consent.

If the source kind is unsupported or mismatched, fail closed and abort.

## Step P3: Source Root Validation

Future-only step. Confirm the source root is explicit, source-specific, path-bounded, and matches consent.

No default live local read is allowed. No arbitrary home-directory scan is allowed. If the source root is ambiguous, outside scope, a personal clone without approval, or a clean clone mistaken for live PAI install, fail closed and abort.

## Step P4: PAI_DIR Candidate Validation

Future-only step. Confirm the PAI_DIR candidate is declared, consent-bound, source-specific, and confidence-qualified.

The step must not inspect live `~/.claude/PAI` by default. If the candidate is missing, forbidden, ambiguous, insufficient confidence, or requires live PAI_DIR reads outside approval, fail closed and abort.

## Step P5: Allowed Read Scope Validation

Future-only step. Confirm allowed reads are path-bounded, read-only, inside the selected source root, and no broader than the future contract.

Allowed reads do not include product memory by default, `~/.claude/projects`, `~/.codex`, arbitrary home scans, or personal clones without approval. Any overbroad read scope must abort.

## Step P6: Forbidden Read Scope Validation

Future-only step. Confirm forbidden reads include live `~/.claude/PAI` absent approval, live `~/.claude/projects`, live `~/.codex`, product memory by default, arbitrary home scans, personal clones without approval, and any source outside allowed scope.

Any requested read that overlaps forbidden reads must fail closed and abort.

## Step P7: Forbidden Write Scope Validation

Future-only step. Confirm forbidden writes include PAI Memory, ISA, Pulse, product-memory promotion, root `AGENTS.md`, `.codex/`, runtime adapter files, generated configs, migration scripts, adapter payloads, manifests, schemas, live-trial artifacts, runtime payloads, reports, fixtures, and committed negative fixtures outside an approved write set.

Any write pressure must fail closed and abort.

## Step P8: Product Memory Boundary Validation

Future-only step. Confirm product memory reads are denied by default and product-memory promotion is not authorized.

Any product-memory access or promotion pressure must abort unless a separate future architect-approved policy explicitly changes the boundary.

## Step P9: Pulse Boundary Validation

Future-only step. Confirm no Pulse startup, no Pulse endpoint calls, no `localhost:31337` probe, no Pulse payloads, no Pulse bridge files, and no Pulse parity claim.

Any Pulse pressure must fail closed and abort.

## Step P10: Memory and ISA Boundary Validation

Future-only step. Confirm no PAI Memory writes and no ISA writes.

Future preflight output must not become PAI Memory or ISA. Any Memory/ISA write pressure must abort.

## Step P11: Runtime Invocation Boundary Validation

Future-only step. Confirm no Codex runtime adapter execution, no Codex runtime invocation, no Codex import/migration tooling, no Codex hook/rule/execpolicy commands, no Claude Code invocation, and no installer execution.

Any runtime pressure must fail closed and abort.

## Step P12: Reporting Boundary Validation

Future-only step. Confirm reporting is non-canonical, retention is defined, rollback/no-residue expectations are defined, denied-action reporting is present, unsupported-surface reporting is present, and drop-in claim status is `not-claimed`.

If report output would become canonical state, manifest, runtime payload, Memory, ISA, Pulse state, Claude memory, Codex memory, or drop-in proof, fail closed and abort.

## Step P13: Abort or Proceed Decision

Future-only step. If any prior step fails, abort. If every prior step passes under a future architect-approved card, `Proceed` means only eligible for architect-approved read-only trial.

`Proceed` does not mean Codex is drop-in. `Proceed` does not authorize runtime adapter implementation, writes, Pulse startup/calls, PAI Memory writes, ISA writes, product-memory promotion, personal-clone access beyond the approved scope, or dual-engine uncoordinated writes.

## Required Future Proofs

Future implementation would need proof that:

- Every step `P0` through `P13` is implemented and covered by negative controls.
- Every step fails closed.
- Any failed step aborts before live local reads.
- Validation does not read live local state by itself.
- Validation does not write canonical state.
- Validation does not start Pulse, call endpoints, invoke Claude Code, invoke Codex runtime, or run installers.
- `Proceed` is not a drop-in claim.

## Prohibited Validation Sequences

Prohibited sequences:

- Preflight that runs without architect approval.
- Preflight that reads live local state before consent and source checks.
- Preflight that treats warnings as pass.
- Preflight that falls back to home scans.
- Preflight that writes to PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, or `.codex/`.
- Preflight that starts Pulse, invokes runtime tools, creates runtime payloads, or claims Codex is drop-in.

## Non-Goals

S12D implements no validation sequence, creates no preflight runner, creates no preflight report, creates no detector script, creates no consent artifact, creates no consent validator, runs no live read-only trial, reads no live existing-local-v5 state, inspects no private user-local state, inspects no personal clone, writes no PAI Memory, writes no ISA, starts no Pulse, calls no Pulse endpoints, invokes no Claude Code, invokes no Codex runtime, implements no runtime adapter, creates no root `AGENTS.md`, creates no `.codex/`, and authorizes no product-memory promotion.
