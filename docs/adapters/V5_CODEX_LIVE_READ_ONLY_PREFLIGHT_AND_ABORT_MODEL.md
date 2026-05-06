# V5 Codex Live Read-Only Preflight and Abort Model

## Purpose

Define future preflight checks and abort conditions before any live local PAI v5 read-only trial can run.

Codex is not currently proven drop-in for existing local PAI v5 files. S12A defines a model only; it runs no live preflight and performs no live existing-local-v5 access.

## Scope

This document describes future preflight, abort, and advisory reporting behavior for a possible later architect-approved read-only trial.

It does not run a live read-only trial, inspect live user-local state, read `~/.claude/PAI`, read `~/.claude/projects`, read `~/.codex`, start Pulse, call Pulse endpoints, write PAI Memory, write ISA, invoke Claude Code, invoke Codex runtime, implement a runtime adapter, create root `AGENTS.md`, create `.codex/`, or create manifests, executable schemas, audit artifacts, live-trial artifacts, or runtime payloads.

## Evidence Base

Evidence base:

- S10 fixture-only validation closeout.
- S11 release-fixture evidence closeout.
- S11D S12 readiness gates.
- S11D proposed S12 write set and consent requirements.
- S12A consent and source-selection model.

No live local state was read for this model.

## Preflight Problem Statement

A future live read-only trial must fail closed before reading live state if consent, source selection, protected path, no-write, Pulse, Memory, ISA, product memory, runtime invocation, or drop-in claim boundaries are not satisfied.

Preflight must be a boundary check, not a migration, adapter implementation, installer, launcher, or runtime bridge.

## Preflight Principles

Future preflight must be:

- Read-only.
- Explicitly consent-bound.
- Path-bounded.
- Deterministic.
- No-write.
- Abortable.
- Non-runtime.
- Evidence-producing only inside an approved future write set.

Preflight must not assume Codex is drop-in and must not claim Codex is the official upstream engine.

## Required Preflight Checks

Future preflight checks must include:

- Explicit consent present.
- Source root matches consent.
- No root `AGENTS.md` creation or modification.
- No `.codex/` creation or modification.
- No write mode.
- No Pulse startup.
- No Pulse endpoint calls.
- No PAI Memory writes.
- No ISA writes.
- No product-memory reads by default.
- No Codex runtime adapter execution.
- No Claude Code invocation.
- No installer execution.

S12A runs none of these checks against live local state; it defines the future requirements only.

## Consent Preflight

Future consent preflight must confirm that consent exists, is explicit, is bounded to the selected source root, is source-specific, is not expired, and is not revoked.

Consent must not be inferred from Claude Code installation, Codex installation, dual subscriptions, local config, product memory, shell history, or past interaction. Missing, ambiguous, expired, or revoked consent must abort before any live read.

## Source Root Preflight

Future source root preflight must confirm that the selected root exactly matches the consent record and approved source-selection record.

It must abort on ambiguous source roots, parent traversal, default live local reads, arbitrary home-directory scans, `~/.claude/projects/**/memory`, `~/.codex/memories`, product memory by default, root `AGENTS.md`, `.codex/`, or any path outside the approved read scope.

## Protected Path Preflight

Future protected path preflight must prove that the trial will not create or modify protected paths:

- `Releases/`
- `.claude/`
- `PAI/`
- `CLAUDE.md`
- `AGENTS.md`
- `.codex/`
- `install.sh`
- `PAI_SYSTEM_PROMPT.md`
- `settings.json`
- `hooks/`
- `skills/`
- `subagents/`
- `agents/`
- `commands/`
- `.github/`
- `.agents/`

Root `AGENTS.md` and `.codex/` remain protected by default.

## No-Write Preflight

Future no-write preflight must prove the trial can run without any repository or live-source write. It must reject write modes, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, manifest instances, executable schemas, live-trial artifacts outside an approved write set, runtime payloads, committed negative fixtures, and any direct mutation of the selected source.

Read-only consent does not authorize writes.

## Pulse Preflight

Future Pulse preflight must prove:

- No Pulse startup.
- No Pulse endpoint calls.
- No `localhost:31337` probe.
- No Pulse payloads.
- No Pulse bridge files.
- No claim of Pulse parity.

Pulse status must remain `not-started-not-called` unless a separate architect-approved card changes scope.

## Memory and ISA Preflight

Future Memory and ISA preflight must prove:

- No PAI Memory writes.
- No ISA writes.
- No product-memory promotion into PAI Memory.
- No report output is treated as PAI Memory or ISA.
- No discovered path is written into PAI Memory, ISA, Pulse, Claude memory, or Codex memory.

PAI Memory and ISA artifacts remain canonical PAI state. Future read-only trials cannot write them.

## Product Memory Preflight

Future product memory preflight must prove product memory reads are denied by default and product-memory promotion is not performed.

Any product memory access requirement must abort unless a separate future architect-approved policy explicitly changes the scope.

## Runtime Invocation Preflight

Future runtime invocation preflight must prove:

- No Codex runtime adapter execution.
- No Codex hook, rule, or execpolicy commands.
- No Codex import or migration tooling.
- No Claude Code invocation.
- No installer execution.
- No launcher, wrapper, runtime config, generated config, or runtime file creation.

The trial must remain adapter-test evidence generation or design only until a later validation track separately authorizes runtime planning.

## Abort Condition Model

Future preflight must abort on:

- Missing consent.
- Ambiguous source root.
- Unexpected private state.
- Any write requirement.
- Pulse startup requirement.
- Pulse call requirement.
- Memory/ISA write requirement.
- Product-memory access requirement.
- Runtime adapter requirement.
- Drop-in claim pressure.

Abort means no live read proceeds beyond the allowed preflight boundary and no canonical PAI state is written.

## Abort Report Model

A future abort report is advisory-only output. It must be non-canonical unless separately approved.

An abort report is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not a PAI runtime audit artifact, and not runtime payload. It must not be promoted into PAI Memory by default.

## Required Future Proofs

Required future proofs:

- Preflight checks are read-only and path-bounded.
- Missing or ambiguous consent aborts.
- Ambiguous source roots abort.
- Protected paths remain unchanged.
- No write mode exists.
- Pulse is not started or called.
- PAI Memory and ISA are not written.
- Product memory is not read by default and is not promoted.
- Claude Code and Codex runtime are not invoked.
- Abort reports are non-canonical and no-residue by design.

## Prohibited Preflight Designs

Prohibited designs:

- Live preflight without explicit consent.
- Broad discovery before source selection.
- Preflight that writes consent, discovered paths, or reports to PAI Memory, ISA, Pulse, Claude memory, or Codex memory.
- Preflight that creates root `AGENTS.md`, `.codex/`, runtime adapter files, generated configs, manifests, executable schemas, audit artifacts, live-trial artifacts, or runtime payloads.
- Preflight that starts Pulse, calls Pulse endpoints, invokes Claude Code, invokes Codex runtime, runs installers, or claims Codex is drop-in.

## Non-Goals

S12A runs no preflight against live local state, runs no live read-only trial, reads no existing-local-v5 state, reads no private user-local state, writes no PAI Memory, writes no ISA, starts no Pulse, calls no Pulse endpoints, probes no `localhost:31337`, invokes no Claude Code, invokes no Codex runtime, implements no runtime adapter, creates no root `AGENTS.md`, creates no `.codex/`, and authorizes no product-memory promotion or dual-engine uncoordinated writes.
