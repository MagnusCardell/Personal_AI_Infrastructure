# V5 Codex PAI_DIR Detection Failure Cases

## Purpose

Define future failure and abort cases for PAI_DIR detection and source-root selection.

Codex is not currently proven drop-in for existing local PAI v5 files. S12C defines design-only detection failure cases and creates no detector, detector script, report, fixture, consent artifact, or consent validator.

## Scope

This document is documentation/design only. It enumerates future PAI_DIR dry-run detection and source-root selection failure cases that must abort before any live existing-local-v5 read-only trial or personal-clone read could occur.

It does not inspect live `PAI_DIR`, live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, existing-local-v5 state, private user-local state, product memory, or any personal clone.

## Evidence Base

Evidence base:

- S12A PAI_DIR detection and source selection spec.
- S12A consent model.
- S12B consent artifact schema proposal.
- S12B consent validation and revocation spec.
- S12B consent failure and abort cases.

No live source root was read for S12C.

## Failure Case Philosophy

Future PAI_DIR detection must fail closed. If consent, source kind, source root, candidate confidence, read scope, no-write policy, Pulse boundary, product memory boundary, Memory/ISA boundary, runtime boundary, reporting boundary, personal clone boundary, or drop-in claim boundary fails, the required response is abort.

Abort is correct safety behavior. It must not be bypassed through broader discovery or fallback home scans.

## Consent-Related Failures

Consent-related failures include missing consent reference, consent source kind mismatch, consent source root mismatch, expired consent, revoked consent, ambiguous consent, replayed consent, and consent that omits PAI_DIR candidate scope.

Future detection must not proceed without explicit user consent plus architect approval for future live or personal-clone source kinds.

## Source-Root Failures

Source-root failures include ambiguous roots, roots outside allowed scope, arbitrary home-directory roots, unknown roots, source roots inferred from product memory, and personal clones accessed without approval.

A clean clone mistaken for live PAI install is a failure because cloned repository evidence is not live existing-local-v5 state.

## PAI_DIR Candidate Failures

PAI_DIR candidate failures include missing candidate, candidate mismatch, insufficient confidence, forbidden candidate path, default live `~/.claude/PAI` read, and candidate evaluation that would require broad home scanning.

S12C does not inspect live `PAI_DIR`.

## Product Memory Failures

Product memory failures include attempted product memory reads, inferred PAI_DIR from product memory, or product-memory promotion into PAI Memory.

Product memory reads remain denied by default.

## Pulse Failures

Pulse failures include Pulse startup pressure, Pulse endpoint call pressure, `localhost:31337` probes, Pulse payload creation, Pulse bridge creation, and Pulse parity claims.

Pulse pressure must abort.

## Memory and ISA Failures

Memory and ISA failures include PAI Memory write pressure, ISA write pressure, canonical-state promotion, and attempts to store detection output in PAI Memory or ISA.

Future detection output is not PAI Memory and not ISA.

## Runtime Invocation Failures

Runtime invocation failures include detector designs that require runtime adapter execution, Claude Code invocation, Codex runtime invocation, Codex import/migration tooling, Codex hook/rule/execpolicy commands, installer execution, launcher creation, wrapper creation, or generated runtime config creation.

Runtime pressure must abort.

## Reporting Failures

Reporting failures include detection output becoming canonical state, report output becoming PAI Memory, ISA, Pulse state, Claude memory, Codex memory, a manifest, runtime payload, or proof that Codex is drop-in.

Unsupported surfaces must be reported and not silently ignored.

## Detection Failure Table

| Failure ID | Failure class | Trigger | Required response | Reported evidence | Future proof required | S12C status |
| --- | --- | --- | --- | --- | --- | --- |
| PD-001 | Consent | Missing consent reference. | Abort before detection. | Missing consent reference. | Future detector rejects absent consent reference. | Design-only |
| PD-002 | Consent | Consent source kind mismatch. | Abort before source-root classification. | Expected and declared source kind mismatch. | Source kind consistency check. | Design-only |
| PD-003 | Consent | Consent source root mismatch. | Abort before source read. | Expected and declared source root mismatch. | Source root consistency check. | Design-only |
| PD-004 | Source root | Source root ambiguous. | Abort and report ambiguity. | Ambiguous candidate roots. | Ambiguous roots fail closed. | Design-only |
| PD-005 | Source root | Source root outside allowed scope. | Abort and deny read. | Out-of-scope root path. | Allowed scope is path-bounded. | Design-only |
| PD-006 | Source root | Source root is arbitrary home directory. | Abort and deny broad scan. | Home-directory root signal. | No arbitrary home scan proof. | Design-only |
| PD-007 | PAI_DIR | Attempted default read of `~/.claude/PAI`. | Abort and deny read. | Forbidden live PAI_DIR path. | No default live PAI_DIR read proof. | Design-only |
| PD-008 | Read scope | Attempted read of `~/.claude/projects`. | Abort and deny read. | Forbidden projects path. | Forbidden read pattern enforced. | Design-only |
| PD-009 | Read scope | Attempted read of `~/.codex`. | Abort and deny read. | Forbidden Codex path. | Forbidden read pattern enforced. | Design-only |
| PD-010 | Product memory | Attempted product memory read. | Abort and deny read. | Product memory boundary signal. | Product memory denied by default. | Design-only |
| PD-011 | Pulse | Attempted Pulse startup. | Abort. | Pulse startup pressure. | Pulse no-start proof. | Design-only |
| PD-012 | Pulse | Attempted Pulse endpoint call. | Abort. | Endpoint/probe pressure. | Pulse no-call proof. | Design-only |
| PD-013 | Memory | PAI Memory write pressure. | Abort. | PAI Memory write signal. | PAI Memory write denial enforced. | Design-only |
| PD-014 | ISA | ISA write pressure. | Abort. | ISA write signal. | ISA write denial enforced. | Design-only |
| PD-015 | Protected path | Root `AGENTS.md` write pressure. | Abort. | Root AGENTS.md write signal. | Protected-path proof. | Design-only |
| PD-016 | Protected path | `.codex/` write pressure. | Abort. | `.codex/` write signal. | Protected-path proof. | Design-only |
| PD-017 | Personal clone | Personal clone accessed without approval. | Abort and deny access. | Missing personal-clone approval/consent. | Architect approval plus explicit user consent required. | Design-only |
| PD-018 | Clone classification | Clean clone mistaken for live PAI install. | Abort or classify as non-live evidence only. | Clean clone evidence mismatch. | Clean clone status does not imply live PAI install. | Design-only |
| PD-019 | PAI_DIR confidence | `PAI_DIR` confidence insufficient. | Abort and report insufficient confidence. | Low or ambiguous confidence. | Confidence threshold and abort proof. | Design-only |
| PD-020 | Runtime | Detector would need runtime adapter execution. | Abort. | Runtime adapter requirement. | Detector is non-runtime. | Design-only |
| PD-021 | Runtime | Detector would need Claude Code invocation. | Abort. | Claude Code invocation requirement. | No Claude Code invocation proof. | Design-only |
| PD-022 | Runtime | Detector would need Codex runtime invocation. | Abort. | Codex runtime invocation requirement. | No Codex runtime invocation proof. | Design-only |
| PD-023 | Reporting | Detector output would become canonical state. | Abort report creation or fail validation. | Canonical-output pressure. | Non-canonical output proof. | Design-only |
| PD-024 | Unsupported surface | Unsupported surface silently ignored. | Abort or report unsupported surface. | Missing unsupported-surface report. | Unsupported-surface reporting proof. | Design-only |
| PD-025 | Drop-in claim | Drop-in claim pressure. | Abort or fail validation. | Drop-in claim signal. | Drop-in status remains not-claimed. | Design-only |

## Required Future Proofs

Future implementation must prove:

- Every `PD-001` through `PD-025` failure ID has a corresponding validation check.
- Every failure aborts before live local reads or personal-clone reads.
- Abort output is non-canonical.
- No broad home scan occurs.
- No default read of live `~/.claude/PAI`, `~/.claude/projects`, or `~/.codex` occurs.
- No PAI Memory write, ISA write, Pulse startup, Pulse call, product-memory read by default, runtime invocation, personal-clone access without approval, or drop-in claim occurs.

## Prohibited Failure Handling Designs

Prohibited designs:

- Treating abort as a warning and continuing.
- Falling back to broad home scans.
- Reading live `~/.claude/PAI` after consent failure.
- Inspecting personal clones without architect approval plus explicit user consent.
- Starting Pulse or calling Pulse endpoints to diagnose detection failures.
- Invoking Claude Code or Codex runtime to classify roots.
- Writing detection output to PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, or `.codex/`.
- Claiming Codex is drop-in after any failure.

## Non-Goals

S12C creates no detector, creates no detector script, creates no consent artifact, creates no consent validator, creates no detection report, runs no live read-only trial, reads no live existing-local-v5 state, inspects no live user-local state, inspects no live `~/.claude/PAI`, inspects no live `~/.claude/projects`, inspects no live `~/.codex`, inspects no personal clone, writes no PAI Memory, writes no ISA, starts no Pulse, calls no Pulse endpoints, invokes no Claude Code, invokes no Codex runtime, implements no runtime adapter, creates no root `AGENTS.md`, creates no `.codex/`, and authorizes no product-memory promotion.
