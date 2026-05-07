# V5 Codex S14 Live Read-Only Trial Gates

## Purpose

Define future S14 live-read-only trial gates for architect review.

S14 is proposed only. S13C does not approve S14 and does not begin S14.

## Scope

These gates define future entry, execution, evidence, and stop boundaries for a possible architect-approved source-selected live-read-only milestone.

S13C does not mark any existing-local-v5, personal-clone, sanitized-user-fixture, or live-read gate as passed.

## Evidence Base

Evidence base:

- S13A clean-clone positive-control trial artifacts.
- S13B negative controls and path-safety hardening.
- S13C clean-clone closeout conclusions.
- S12/S13 consent, source-selection, PAI_DIR, preflight, abort, non-canonical evidence, and no-residue policies.

Codex is not currently proven drop-in for existing local PAI v5 files.

## S14 Gate Problem Statement

A future S14 milestone would be the first possible source-selected live-read-only milestone after clean-clone evidence. It must not proceed without explicit architect approval, explicit source class decision, explicit user consent, explicit source selection, read-only source boundary validation, preflight pass, no writes, non-canonical evidence output, and no drop-in claim.

S14 must not silently read existing-local-v5 state, personal-clone state, product memory, broad home directories, or private user-local paths.

## Gate Model

Each gate includes:

- Required proof.
- Failure signal.
- S13C status.
- Future S14 implication.

S13C status values:

- Future-only: not passed by S13C and requires later architect-approved S14 work.
- Prohibited by default: denied unless a separate architect-approved contract explicitly changes scope.
- Required future evidence: must be proven during S14 if S14 is approved.

## Gate U0: Architect Approval

- Required proof: Explicit architect approval for the exact S14 objective, source class, source root, allowed reads, forbidden reads, approved write set, validation commands, hard failures, stop conditions, and final handoff.
- Failure signal: S14 work begins from S13C proposal docs alone, or S13C is treated as approval.
- S13C status: Future-only; architect approval is required and not granted by S13C.
- Future S14 implication: No S14 source-selected live-read-only command, read, or output may occur until a future architect card approves it.

## Gate U1: Source Class Decision

- Required proof: Explicit architect decision selecting exactly one future source class, such as `existing-local-v5-read-only`, `personal-clone-read-only`, or `sanitized-user-fixture-read-only`.
- Failure signal: Source class is inferred, mixed, ambiguous, switched mid-run, or selected by default.
- S13C status: Future-only; S13C approves no source class.
- Future S14 implication: S14 must abort unless the source class is explicit, architect-approved, and consent-bound.

## Gate U2: Explicit User Consent

- Required proof: Explicit user consent for the selected source class, source root, allowed reads, forbidden reads, forbidden writes, retention, revocation, expiration, no-write policy, and reporting boundary.
- Failure signal: Consent is absent, inferred, stale, expired, revoked, replayed, ambiguous, or overbroad.
- S13C status: Future-only; S13C creates no consent artifact and collects no consent.
- Future S14 implication: S14 must abort before any live-read step if consent is not valid.

## Gate U3: Explicit Source Selection

- Required proof: A future source-selection record identifies the exact source class and source root and binds both to consent.
- Failure signal: Source discovery uses broad home scans, inferred local config, shell history, product memory, subscription state, or any unbounded path traversal.
- S13C status: Future-only; S13C selects no live source.
- Future S14 implication: S14 must fail closed unless every source is explicit and approved.

## Gate U4: PAI_DIR Detection Approval

- Required proof: Future approval that PAI_DIR handling is dry-run, read-only, consent-bound, source-specific, path-bounded, confidence-qualified, and abortable.
- Failure signal: Default live `~/.claude/PAI` reads, automatic PAI_DIR discovery, broad scans, path expansion, or confidence overclaims.
- S13C status: Future-only; S13C does not inspect live PAI_DIR.
- Future S14 implication: PAI_DIR detection cannot run unless the future S14 contract approves the exact read-only method.

## Gate U5: Preflight Report Pass

- Required proof: A future preflight pass proving architect approval, valid consent, source class, source selection, PAI_DIR candidate if applicable, allowed reads, forbidden reads, forbidden writes, runtime prohibitions, non-canonical reporting, retention, and rollback/no-residue expectations.
- Failure signal: Any abort reason, missing evidence, stale consent, unsupported surface silence, write pressure, Pulse pressure, Memory/ISA pressure, product memory pressure, runtime pressure, or source mismatch.
- S13C status: Future-only; S13C creates no preflight report.
- Future S14 implication: S14 source-selected reads cannot proceed without a future preflight pass.

## Gate U6: No Root AGENTS.md

- Required proof: Protected-path validation proves root AGENTS.md is not created, modified, copied, generated, or migrated.
- Failure signal: Root AGENTS.md appears in changed files or is proposed as S14 output.
- S13C status: Prohibited by default.
- Future S14 implication: Future Codex AGENTS.md, if later authorized, must be a compact router in a separate milestone, not S14 live-read output.

## Gate U7: No .codex

- Required proof: Protected-path validation proves `.codex` is not created or modified.
- Failure signal: `.codex` config, hook, rule, skill, memory, command, profile, or generated runtime file appears.
- S13C status: Prohibited by default.
- Future S14 implication: S14 must not create Codex runtime surfaces.

## Gate U8: No Pulse Startup

- Required proof: S14 validation proves Pulse was not started.
- Failure signal: Any command, hook, service, bridge, launcher, or runtime behavior starts Pulse.
- S13C status: Prohibited by default.
- Future S14 implication: Pulse startup remains forbidden unless separately approved.

## Gate U9: No Pulse Endpoint Calls

- Required proof: S14 validation proves no Pulse endpoint call and no `localhost:31337` probe occurred.
- Failure signal: HTTP call, socket call, curl probe, health check, bridge call, or localhost endpoint access.
- S13C status: Prohibited by default.
- Future S14 implication: Pulse endpoint calls remain forbidden unless separately approved.

## Gate U10: No PAI Memory Writes

- Required proof: Validation proves PAI Memory was not created, modified, migrated, imported, normalized, or promoted into.
- Failure signal: Any PAI Memory mutation or generated Memory payload.
- S13C status: Prohibited by default.
- Future S14 implication: PAI Memory remains canonical PAI state and cannot be written by read-only S14.

## Gate U11: No ISA Writes

- Required proof: Validation proves ISA was not created, modified, migrated, imported, normalized, or updated.
- Failure signal: Any ISA mutation or generated ISA payload.
- S13C status: Prohibited by default.
- Future S14 implication: ISA remains canonical PAI state and cannot be written by read-only S14.

## Gate U12: No Product Memory Reads by Default

- Required proof: Future S14 scope and validation prove product memory is outside default reads.
- Failure signal: Product memory is read, scanned, imported, summarized, inferred from, or used as a source selector by default.
- S13C status: Prohibited by default.
- Future S14 implication: Product memory access requires a separate architect-approved policy.

## Gate U13: No Product Memory Promotion

- Required proof: Validation proves no product memory was promoted, normalized, migrated, imported, or written into PAI Memory.
- Failure signal: Product memory is silently promoted into PAI Memory or used to update canonical PAI state.
- S13C status: Prohibited by default.
- Future S14 implication: Product memories must not be silently promoted into PAI Memory.

## Gate U14: No Claude File Direct-Copy

- Required proof: Review proves `PAI_SYSTEM_PROMPT.md`, `CLAUDE.md`, hooks, commands, skills, and Claude-shaped files are not copied directly into Codex surfaces.
- Failure signal: Claude-facing files are copied into root AGENTS.md, `.codex`, Codex rules, Codex hooks, or Codex runtime config.
- S13C status: Prohibited by default.
- Future S14 implication: Unsupported surfaces must be reported, not copied.

## Gate U15: No Claude Code Invocation

- Required proof: Validation proves Claude Code was not invoked.
- Failure signal: Any command, script, installer, hook, or test invokes Claude Code.
- S13C status: Prohibited by default.
- Future S14 implication: S14 must not depend on Claude Code execution and must not require uninstalling Claude Code.

## Gate U16: No Codex Runtime Adapter Execution

- Required proof: Validation proves Codex was not invoked as a runtime engine and no Codex runtime adapter was executed.
- Failure signal: Codex runtime, adapter command, import/migration tooling, hook/rule/execpolicy command, launcher, wrapper, or generated runtime config executes.
- S13C status: Prohibited by default.
- Future S14 implication: S14 remains read-only evidence, not runtime adapter validation.

## Gate U17: Unsupported Surface Reporting

- Required proof: Future S14 output reports unsupported surfaces explicitly without converting them into runtime payloads.
- Failure signal: Unsupported surfaces are ignored, represented as supported, or materialized as Codex controls.
- S13C status: Required future evidence.
- Future S14 implication: Unsupported-surface reporting is mandatory before any later adapter planning.

## Gate U18: Non-Canonical Evidence Output

- Required proof: Future S14 output states it is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.
- Failure signal: Output is treated as canonical state, runtime payload, manifest, PAI runtime audit artifact, Memory, ISA, Pulse state, or drop-in proof.
- S13C status: Required future evidence.
- Future S14 implication: S14 output must remain advisory evidence unless separately approved.

## Gate U19: Rollback and No-Residue Reporting

- Required proof: Future S14 validation proves no residue outside the approved write set and reports rollback/no-residue expectations.
- Failure signal: New runtime files, report artifacts outside the approved write set, modified fixtures, modified reports, protected path residue, live-source residue, or missing rollback statement.
- S13C status: Required future evidence.
- Future S14 implication: S14 must be able to end without residue in live source roots or protected paths.

## Gate U20: No Drop-In Claim

- Required proof: Future S14 handoff states no drop-in claim and Codex is not currently proven drop-in for existing local PAI v5 files.
- Failure signal: Any claim that Codex is drop-in today, replacement-grade, runtime-compatible, or proven local engine.
- S13C status: Prohibited by default.
- Future S14 implication: No drop-in claim may be made until later replacement-grade validation exists.

## Gate U21: No Official-Upstream Claim

- Required proof: Future S14 handoff states no official-upstream claim and Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
- Failure signal: Any claim that Codex is the official upstream engine for PAI v5 or that Claude Code support has been superseded.
- S13C status: Prohibited by default.
- Future S14 implication: No official-upstream claim may be made by S14.

## Minimum S14 Entry Threshold

Minimum S14 entry threshold:

- Explicit architect approval.
- Explicit source class decision.
- Explicit user consent.
- Explicit source selection.
- Read-only PAI_DIR detection approval if PAI_DIR is in scope.
- Future preflight pass.
- Exact approved write set.
- No root AGENTS.md.
- No `.codex`.
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

S13C does not mark any existing-local-v5, personal-clone, or live-read gate as passed.

## Non-Goals

This gate proposal does not approve S14, begin S14, run live reads, read existing-local-v5 state, inspect private user-local state, inspect live `~/.claude/PAI`, inspect live `~/.claude/projects`, inspect live `~/.codex`, inspect a personal clone, create root AGENTS.md, create `.codex`, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, probe `localhost:31337`, invoke Claude Code, invoke Codex runtime, implement runtime adapter work, create runtime payloads, create consent artifacts, create preflight reports, promote product memory, authorize dual-engine uncoordinated writes, claim Codex is drop-in today, or claim Codex is the official upstream engine.
