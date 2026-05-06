# V5 Codex Consent Failure and Abort Cases

## Purpose

Define future failure and abort cases for consent, source selection, PAI_DIR detection, and live-read preflight.

Codex is not currently proven drop-in for existing local PAI v5 files. S12B defines design-only abort cases and creates no actual consent artifact, validator, report, fixture, or live-trial artifact.

## Scope

This document is documentation/design only. It enumerates future consent and preflight failure cases that must abort before any future live existing-local-v5 read-only trial.

It does not run a live read-only trial, does not read live user-local state, does not create a consent artifact, does not create a consent validator, and does not implement runtime adapter behavior.

## Evidence Base

Evidence base:

- S12A consent model.
- S12A PAI_DIR detection and source selection spec.
- S12A live read-only preflight and abort model.
- S12A live read-only reporting boundary spec.
- S12B consent artifact schema proposal.
- S12B consent validation and revocation spec.

No live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, product memory, or existing-local-v5 state was read.

## Failure Case Philosophy

Future consent validation must fail closed. If consent is absent, ambiguous, expired, revoked, mismatched, replayed, overbroad, or pressured into writes, Pulse behavior, product-memory access, runtime invocation, or drop-in claims, the required response is abort.

Abort is not failure to be worked around. Abort is the correct safety behavior.

## Consent Failure Cases

Consent failure cases include:

- Missing consent.
- Expired consent.
- Revoked consent.
- Ambiguous consent.
- Draft or pending consent treated as live-read approval.
- Consent inferred from Claude Code installation.
- Consent inferred from Codex installation.
- Consent inferred from dual subscriptions.

Every consent failure remains design-only in S12B.

## Source Selection Failure Cases

Source selection failure cases include ambiguous source root, source root mismatch, source kind mismatch, broad home-directory scanning, and selecting `existing-local-v5-read-only` without explicit user consent plus architect approval.

Future source selection must not read live local state by default.

## PAI_DIR Failure Cases

PAI_DIR failure cases include missing `PAI_DIR` confirmation, default live `PAI_DIR` detection, broad `~/.claude/` reads, and treating `~/.claude/PAI` as authorized merely because it exists.

S12B does not inspect `~/.claude/PAI`.

## Read Scope Failure Cases

Read scope failure cases include attempts to read outside allowed scope, product memory by default, `~/.claude/projects/**/memory`, `~/.codex/memories`, arbitrary home directories, or any source not named by a future consent artifact and architect-approved contract.

Any read scope failure must abort.

## Write Pressure Failure Cases

Write pressure includes any attempt or requirement to create, modify, normalize, migrate, promote, import, generate, or persist state outside an approved future write set.

Write pressure must abort even if the user has approved read-only consent.

## Product Memory Failure Cases

Product memory reads remain denied by default. Product-memory promotion into PAI Memory remains denied.

Product memory pressure must abort unless a separate architect-approved product-memory policy exists.

## Pulse Failure Cases

Pulse failure cases include Pulse startup pressure, Pulse endpoint call pressure, `localhost:31337` probe pressure, Pulse payload creation, Pulse bridge creation, and Pulse parity claims.

Pulse pressure must abort.

## Memory and ISA Failure Cases

PAI Memory and ISA are canonical PAI state. Any PAI Memory write pressure or ISA write pressure must abort.

Consent artifacts, validation output, and abort reports are not PAI Memory and not ISA.

## Runtime Invocation Failure Cases

Runtime invocation failure cases include Codex runtime invocation, Codex runtime adapter implementation, Codex import/migration tooling, Codex hook/rule/execpolicy commands, Claude Code invocation, installer execution, launcher creation, wrapper creation, or generated runtime config creation.

Runtime pressure must abort.

## Reporting Failure Cases

Reporting failure cases include reporting output becoming canonical state, reporting output becoming PAI Memory, ISA, Pulse state, Claude memory, Codex memory, a manifest, runtime payload, or proof that Codex is drop-in.

Unsupported surfaces must be reported, not silently ignored.

## Abort Case Table

| Abort ID | Failure class | Trigger | Required response | Reported evidence | Future proof required | S12B status |
| --- | --- | --- | --- | --- | --- | --- |
| CA-001 | Consent | Missing consent. | Abort before preflight or live read. | Missing consent signal. | Validator rejects absent consent. | Design-only |
| CA-002 | Consent | Expired consent. | Abort before preflight or live read. | Expiration timestamp/status. | Validator rejects expired consent. | Design-only |
| CA-003 | Consent | Revoked consent. | Abort before preflight or live read. | Revocation timestamp/status. | Validator rejects revoked consent. | Design-only |
| CA-004 | Source selection | Ambiguous source root. | Abort before any source read. | Ambiguity detail. | Source root must be explicit. | Design-only |
| CA-005 | Source selection | Source root mismatch. | Abort before any source read. | Expected and observed root mismatch. | Source root confirmation check. | Design-only |
| CA-006 | Source selection | Source kind mismatch. | Abort before any source read. | Expected and observed source kind mismatch. | Source kind consistency check. | Design-only |
| CA-007 | PAI_DIR | Missing `PAI_DIR` confirmation. | Abort before PAI_DIR use. | Missing confirmation. | PAI_DIR confirmation is explicit and read-only. | Design-only |
| CA-008 | Read scope | Attempt to read outside allowed scope. | Abort and deny read. | Forbidden path or selector. | Allowed reads are path-bounded. | Design-only |
| CA-009 | Product memory | Attempt to read product memory by default. | Abort and deny read. | Product memory boundary signal. | Product memory denied by default. | Design-only |
| CA-010 | Read scope | Attempt to read `~/.claude/projects/**/memory`. | Abort and deny read. | Protected product-memory-like path. | Forbidden read pattern enforced. | Design-only |
| CA-011 | Read scope | Attempt to read `~/.codex/memories`. | Abort and deny read. | Codex memory path. | Forbidden read pattern enforced. | Design-only |
| CA-012 | Write pressure | Write requirement detected. | Abort. | Write requirement detail. | No-write validation covers every path. | Design-only |
| CA-013 | Memory | PAI Memory write pressure. | Abort. | PAI Memory write signal. | PAI Memory write denial enforced. | Design-only |
| CA-014 | ISA | ISA write pressure. | Abort. | ISA write signal. | ISA write denial enforced. | Design-only |
| CA-015 | Pulse | Pulse startup pressure. | Abort. | Startup requirement detail. | Pulse no-start proof. | Design-only |
| CA-016 | Pulse | Pulse endpoint call pressure. | Abort. | Endpoint/probe detail. | Pulse no-call proof. | Design-only |
| CA-017 | Protected path | Root `AGENTS.md` write pressure. | Abort. | Root AGENTS.md write signal. | Protected-path proof. | Design-only |
| CA-018 | Protected path | `.codex/` write pressure. | Abort. | `.codex/` write signal. | Protected-path proof. | Design-only |
| CA-019 | Runtime | Runtime adapter implementation pressure. | Abort. | Runtime adapter requirement. | Non-runtime proof. | Design-only |
| CA-020 | Runtime | Claude Code invocation pressure. | Abort. | Claude Code invocation requirement. | No Claude Code invocation proof. | Design-only |
| CA-021 | Runtime | Codex runtime invocation pressure. | Abort. | Codex runtime invocation requirement. | No Codex runtime invocation proof. | Design-only |
| CA-022 | Drop-in claim | Drop-in claim pressure. | Abort or fail validation. | Claim text or status. | Drop-in status remains not-claimed. | Design-only |
| CA-023 | Product memory | Product-memory promotion pressure. | Abort. | Promotion requirement detail. | No-promotion proof. | Design-only |
| CA-024 | Reporting | Reporting output would become canonical state. | Abort report creation or fail validation. | Canonical-output pressure. | Non-canonical reporting proof. | Design-only |
| CA-025 | Unsupported surface | Unsupported surface would be silently ignored. | Abort or report unsupported surface. | Missing unsupported-surface report. | Unsupported surfaces reported explicitly. | Design-only |

## Required Future Proofs

Future implementation must prove:

- Every abort ID has a corresponding validation check.
- Every abort response happens before live local reads.
- Abort reporting is non-canonical.
- Abort behavior leaves no residue outside an approved write set.
- Abort does not write PAI Memory, ISA, Pulse, Claude memory, Codex memory, root AGENTS.md, or `.codex/`.

## Prohibited Failure Handling Designs

Prohibited designs:

- Treating abort as a warning and continuing.
- Creating fallback broad reads after consent failure.
- Writing abort state to PAI Memory, ISA, Pulse, Claude memory, or Codex memory.
- Promoting product memory into PAI Memory.
- Starting Pulse or calling Pulse endpoints to diagnose failure.
- Invoking Claude Code or Codex runtime to repair failure.
- Claiming Codex is drop-in after any abort case.

## Non-Goals

S12B creates no actual consent artifact, creates no validator, creates no abort report, runs no live trial, reads no live existing-local-v5 state, inspects no private user-local state, writes no PAI Memory, writes no ISA, starts no Pulse, calls no Pulse endpoints, creates no root AGENTS.md, creates no `.codex/`, invokes no Claude Code, invokes no Codex runtime, implements no runtime adapter, and authorizes no product-memory promotion.
