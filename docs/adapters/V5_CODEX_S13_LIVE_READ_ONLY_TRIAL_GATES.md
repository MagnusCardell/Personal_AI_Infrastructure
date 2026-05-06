# V5 Codex S13 Live Read-Only Trial Gates

## Purpose

Define future S13 live-read-only trial gates for architect review.

S13 is proposed only. S12E does not approve S13 and does not begin S13.

## Scope

These gates describe future entry, execution, reporting, and stop boundaries for a possible architect-approved S13 live-read-only trial. They do not authorize live reads, runtime adapter work, root `AGENTS.md`, `.codex/`, Pulse startup, Pulse endpoint calls, PAI Memory writes, ISA writes, product memory promotion, Claude Code invocation, Codex runtime invocation, or drop-in claims.

## Evidence Base

Evidence base:

- S11 release-fixture evidence and S11 readiness gate evaluation.
- S12A consent, source-selection, PAI_DIR, preflight, abort, and reporting designs.
- S12B consent artifact proposal and validation/revocation design.
- S12C PAI_DIR dry-run detection and source-root classification design.
- S12D preflight report schema, validation sequence, abort/evidence model, and non-canonical output policy.
- S12E closeout conclusions.

Codex is not currently proven drop-in for existing local PAI v5 files.

## S13 Gate Problem Statement

A future S13 live-read-only trial would be the first milestone that could read explicitly selected live local PAI v5 state. That requires gates that prove architect approval, explicit user consent, explicit source selection, read-only PAI_DIR detection, preflight pass, no writes, no Pulse behavior, non-canonical evidence, and no drop-in claim.

S12E does not mark any live-read gate as passed.

## Gate Model

Each gate below includes:

- Required proof.
- Failure signal.
- S12E status.
- Future S13 implication.

S12E status values:

- Future-only: not passed by S12E and requires later architect-approved S13 work.
- Prohibited by default: denied unless a separate architect-approved contract explicitly changes scope.
- Required future evidence: must be proven during S13 if S13 is approved.

## Gate T0: Architect Approval

- Required proof: Explicit architect approval for the exact S13 objective, source protocol, allowed reads, forbidden reads, approved write set, validation commands, hard failures, stop conditions, and final handoff.
- Failure signal: S13 work begins from S12E documents alone, or S12E is treated as approval.
- S12E status: Future-only; architect approval is required and not granted by S12E.
- Future S13 implication: No S13 command, live read, or output may occur until a future architect card approves it.

## Gate T1: Explicit User Consent

- Required proof: Explicit user consent for the exact source kind, source root, allowed reads, forbidden reads, retention, revocation, expiration, no-write policy, and reporting boundary.
- Failure signal: Consent is absent, ambiguous, inferred, stale, expired, revoked, replayed, or overbroad.
- S12E status: Future-only; S12E creates no consent artifact and collects no consent.
- Future S13 implication: S13 must abort before live reads if consent is not valid.

## Gate T2: Explicit Source Selection

- Required proof: A future source selection record identifies the exact source kind and source root and binds both to consent.
- Failure signal: Source discovery uses broad home scans, inferred local config, subscriptions, product memory, shell history, or any unbounded path traversal.
- S12E status: Future-only; S12E selects no live source.
- Future S13 implication: S13 must fail closed unless every source is explicit and approved.

## Gate T3: PAI_DIR Detection Approval

- Required proof: Future approval that PAI_DIR handling is dry-run, read-only, consent-bound, source-specific, path-bounded, confidence-qualified, and abortable.
- Failure signal: Default live `~/.claude/PAI` reads, automatic PAI_DIR discovery, broad scans, or confidence overclaims.
- S12E status: Future-only; S12E does not inspect live PAI_DIR.
- Future S13 implication: PAI_DIR detection cannot run unless the future S13 contract approves the exact read-only method.

## Gate T4: Preflight Report Pass

- Required proof: A future preflight pass proving architect approval, valid consent, valid source selection, valid PAI_DIR candidate, allowed reads, forbidden reads, forbidden writes, runtime prohibitions, non-canonical reporting, retention, and rollback/no-residue expectations.
- Failure signal: Any abort reason, missing evidence, stale consent, unsupported surface silence, write pressure, Pulse pressure, Memory/ISA pressure, product memory pressure, or runtime pressure.
- S12E status: Future-only; S12E creates no preflight report.
- Future S13 implication: S13 live reads cannot proceed without a future preflight pass.

## Gate T5: No Root AGENTS.md

- Required proof: Protected-path validation proves root `AGENTS.md` is not created, modified, copied, generated, or migrated.
- Failure signal: Root `AGENTS.md` appears in changed files or is proposed as an S13 output.
- S12E status: Prohibited by default.
- Future S13 implication: Future Codex `AGENTS.md`, if later authorized, must be a compact router in a separate milestone, not S13 live-read output.

## Gate T6: No .codex

- Required proof: Protected-path validation proves `.codex/` is not created or modified.
- Failure signal: `.codex` config, hook, rule, skill, memory, command, profile, or generated runtime file appears.
- S12E status: Prohibited by default.
- Future S13 implication: S13 must not create Codex runtime surfaces.

## Gate T7: No Pulse Startup

- Required proof: S13 validation proves Pulse was not started.
- Failure signal: Any command, hook, service, bridge, launcher, or runtime behavior starts Pulse.
- S12E status: Prohibited by default.
- Future S13 implication: Pulse startup remains forbidden unless separately approved.

## Gate T8: No Pulse Endpoint Calls

- Required proof: S13 validation proves no Pulse endpoint call and no `localhost:31337` probe occurred.
- Failure signal: HTTP call, socket call, curl probe, health check, bridge call, or localhost endpoint access.
- S12E status: Prohibited by default.
- Future S13 implication: Pulse endpoint calls remain forbidden unless separately approved.

## Gate T9: No PAI Memory Writes

- Required proof: Validation proves PAI Memory was not created, modified, migrated, imported, normalized, or promoted into.
- Failure signal: Any PAI Memory file mutation or generated Memory payload.
- S12E status: Prohibited by default.
- Future S13 implication: PAI Memory remains canonical PAI state and cannot be written by read-only S13.

## Gate T10: No ISA Writes

- Required proof: Validation proves ISA was not created, modified, migrated, imported, normalized, or updated.
- Failure signal: Any ISA mutation or generated ISA payload.
- S12E status: Prohibited by default.
- Future S13 implication: ISA remains canonical PAI state and cannot be written by read-only S13.

## Gate T11: No Product Memory Reads by Default

- Required proof: Future S13 scope and validation prove product memory is outside default reads.
- Failure signal: Product memory is read, scanned, imported, summarized, inferred from, or used as a source selector by default.
- S12E status: Prohibited by default.
- Future S13 implication: Product memory access requires a separate architect-approved policy.

## Gate T12: No Product Memory Promotion

- Required proof: Validation proves no product memory was promoted, normalized, migrated, imported, or written into PAI Memory.
- Failure signal: Product memory is silently promoted into PAI Memory or used to update canonical PAI state.
- S12E status: Prohibited by default.
- Future S13 implication: Product memories must not be silently promoted into PAI Memory.

## Gate T13: No Claude File Direct-Copy

- Required proof: Review proves `PAI_SYSTEM_PROMPT.md`, `CLAUDE.md`, hooks, commands, skills, and Claude-shaped files are not copied directly into Codex surfaces.
- Failure signal: Claude-facing files are copied into root `AGENTS.md`, `.codex/`, Codex rules, Codex hooks, or Codex runtime config.
- S12E status: Prohibited by default.
- Future S13 implication: Unsupported surfaces must be reported, not copied.

## Gate T14: No Claude Code Invocation

- Required proof: Validation proves Claude Code was not invoked.
- Failure signal: Any command, script, installer, hook, or test invokes Claude Code.
- S12E status: Prohibited by default.
- Future S13 implication: S13 must not depend on Claude Code execution and must not require uninstalling Claude Code.

## Gate T15: No Codex Runtime Adapter Execution

- Required proof: Validation proves Codex was not invoked as a runtime engine and no Codex runtime adapter was executed.
- Failure signal: Codex runtime, adapter command, import/migration tooling, hook/rule/execpolicy command, launcher, wrapper, or generated runtime config executes.
- S12E status: Prohibited by default.
- Future S13 implication: S13 remains read-only evidence, not runtime adapter validation.

## Gate T16: Unsupported Surface Reporting

- Required proof: Future S13 output reports unsupported surfaces explicitly without converting them into runtime payloads.
- Failure signal: Unsupported surfaces are ignored, represented as supported, or materialized as Codex controls.
- S12E status: Required future evidence.
- Future S13 implication: Unsupported-surface reporting is mandatory before any later adapter planning.

## Gate T17: Non-Canonical Evidence Output

- Required proof: Future S13 output states it is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.
- Failure signal: Output is treated as canonical state, runtime payload, manifest, PAI runtime audit artifact, Memory, ISA, Pulse state, or drop-in proof.
- S12E status: Required future evidence.
- Future S13 implication: S13 output must remain advisory evidence unless separately approved.

## Gate T18: Rollback and No-Residue Reporting

- Required proof: Future S13 validation proves no residue outside the approved write set and reports rollback/no-residue expectations.
- Failure signal: New runtime files, report artifacts outside the approved write set, modified fixtures, modified reports, protected path residue, live-source residue, or missing rollback statement.
- S12E status: Required future evidence.
- Future S13 implication: S13 must be able to end without residue in live source roots or protected paths.

## Gate T19: No Drop-In Claim

- Required proof: Future S13 handoff states no drop-in claim, no official-upstream claim, and Codex is not currently proven drop-in for existing local PAI v5 files.
- Failure signal: Any claim that Codex is drop-in today, official upstream, replacement-grade, runtime-compatible, or proven local engine.
- S12E status: Prohibited by default.
- Future S13 implication: No drop-in claim may be made until later replacement-grade validation exists.

## Minimum S13 Entry Threshold

Minimum S13 entry threshold:

- Explicit architect approval.
- Explicit user consent design and valid future consent.
- Explicit source selection.
- Read-only PAI_DIR detection approval if PAI_DIR is in scope.
- Future preflight pass.
- Exact approved write set.
- No root `AGENTS.md`.
- No `.codex/`.
- No Pulse startup.
- No Pulse endpoint calls.
- No PAI Memory writes.
- No ISA writes.
- No product memory reads by default.
- No product memory promotion.
- No Claude file direct-copy.
- No Claude Code invocation.
- No Codex runtime adapter execution.
- Non-canonical evidence output.
- Rollback/no-residue reporting.
- No drop-in claim.
- No official-upstream claim.

S12E does not mark any live-read gate as passed.

## Non-Goals

This gate proposal does not approve S13, begin S13, run live reads, read existing-local-v5 state, inspect private user-local state, inspect live `~/.claude/PAI`, inspect live `~/.claude/projects`, inspect live `~/.codex`, inspect a personal clone, create root `AGENTS.md`, create `.codex/`, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, probe `localhost:31337`, invoke Claude Code, invoke Codex runtime, implement runtime adapter work, create runtime payloads, create consent artifacts, create preflight reports, promote product memory, authorize dual-engine uncoordinated writes, claim Codex is drop-in today, or claim Codex is the official upstream engine.
