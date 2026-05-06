# V5 Codex S12 Live Read-Only Trial Readiness Gates

## Purpose

Define proposed readiness gates for a future S12 live read-only trial readiness milestone.

Codex is not currently proven drop-in for existing local PAI v5 files. S12 is proposed only and requires architect approval before any work begins.

## Scope

These gates are documentation/design only. They do not authorize S12, live trials, existing-local-v5 access, runtime adapter implementation, root `AGENTS.md`, `.codex`, Pulse startup, Pulse endpoint calls, PAI Memory writes, ISA writes, product-memory promotion, or any Codex drop-in claim.

Future S12 must be read-only unless separately approved. Future S12 must not claim Codex is the official upstream engine.

## Evidence Base

Evidence base:

- S10 fixture-only closeout.
- S11A release-fixture read-only evidence report.
- S11B report-generator negative controls.
- S11C readiness gate evaluation report.
- S11D closeout and proposed S12 contract.

S11D does not mark live-read gates as passed. S11D does not read live user-local state or existing-local-v5 state.

## S12 Readiness Problem Statement

The next possible milestone is a live read-only trial readiness design. The problem is to define exact conditions under which a future card could permit strictly bounded live local reads without writes, without Pulse startup or calls, without PAI Memory or ISA writes, and without treating Codex as drop-in.

S12 must not require uninstalling Claude Code. S12 must not create root `AGENTS.md` or `.codex/`. S12 must require explicit user consent design before any live local read.

## Gate Model

Each gate below includes Required proof, Failure signal, S11D status, and Future S12 implication.

S11D status values:

- Proposed only: described for future architect review but not approved.
- Evidence prerequisite available: S10/S11 evidence can support future review but does not authorize S12.
- Future-only: must be designed and approved by a later card before any live-read work.
- Prohibited by default: not allowed unless a later architect-approved card explicitly changes scope.

## Gate L0: Architect Approval

Required proof: explicit architect approval for S12 objective, source protocol, user consent design, allowed reads, forbidden reads, approved write set, validation commands, hard failures, and final handoff.

Failure signal: S12 work begins from S11D documents alone or treats this proposal as authorization.

S11D status: Proposed only; architect approval is required and not granted by S11D.

Future S12 implication: S12 cannot start until a future architect-approved card explicitly authorizes it.

## Gate L1: S10 Fixture Track Accepted

Required proof: architect accepts the S10 fixture-only closeout, harness status, negative controls, global coverage, and no-residue evidence.

Failure signal: S10 fixture evidence is incomplete, rejected, or not reviewed.

S11D status: Evidence prerequisite available.

Future S12 implication: S12 should not start unless S10 fixture evidence is accepted.

## Gate L2: S11 Evidence Track Accepted

Required proof: architect accepts S11A evidence generation, S11B generator controls, and S11C readiness gate evaluation.

Failure signal: S11 evidence is incomplete, rejected, or not reviewed.

S11D status: Evidence prerequisite available; S11 release-fixture evidence is closed pending architect review.

Future S12 implication: S12 should not start unless S11 release-fixture evidence is accepted.

## Gate L3: Explicit User Consent Model

Required proof: a future S12 card defines explicit user consent design before any live local read, including what is read, why it is read, how consent is recorded, and how refusal is handled.

Failure signal: live local reads occur through implicit consent, broad consent, or unclear source scope.

S11D status: Future-only; explicit user consent is required but not designed or approved by S11D.

Future S12 implication: no live local read can occur until explicit user consent design is approved.

## Gate L4: Explicit Source Selection

Required proof: future S12 names exact live read-only sources and repository-local sources, with no discovery through broad home-directory scanning.

Failure signal: source discovery uses private state, default local paths, inferred configuration, or unbounded filesystem traversal.

S11D status: Future-only; source selection is not approved by S11D.

Future S12 implication: S12 must fail closed unless every source is explicitly selected.

## Gate L5: No Default Live User-Local Access

Required proof: future S12 confirms live user-local access is disabled by default and only enabled through explicit user consent design and exact source selection.

Failure signal: any default read of `~/.claude/`, `~/.claude/PAI/`, `~/.claude/projects/`, `~/.codex/`, `~/.codex/memories/`, or equivalent live user-local state.

S11D status: Future-only; no live user-local reads are approved.

Future S12 implication: live user-local access remains blocked unless explicitly approved in a future S12 card.

## Gate L6: PAI_DIR Detection Policy

Required proof: future S12 defines whether `PAI_DIR` detection is allowed, read-only, explicit, and consent-bound.

Failure signal: automatic `PAI_DIR` detection, writes to detected PAI paths, or inferred existing-local-v5 access.

S11D status: Future-only; PAI_DIR detection policy is not approved by S11D.

Future S12 implication: any PAI_DIR detection must be read-only, explicit, and architect-approved before use.

## Gate L7: No Root AGENTS.md

Required proof: protected-path validation confirms root `AGENTS.md` is not created or modified.

Failure signal: root `AGENTS.md` creation, modification, generation, migration, or promotion.

S11D status: Prohibited by default.

Future S12 implication: root `AGENTS.md` remains protected unless a separate future card explicitly approves it.

## Gate L8: No .codex

Required proof: protected-path validation confirms `.codex/` is not created or modified.

Failure signal: `.codex` config, profile, hook, rule, memory, or generated file creation or mutation.

S11D status: Prohibited by default.

Future S12 implication: Codex runtime surfaces remain unauthorized unless separately approved.

## Gate L9: No Pulse Startup

Required proof: validation proves Pulse is not started.

Failure signal: any command, service, script, hook, or trial behavior starts Pulse.

S11D status: Prohibited by default.

Future S12 implication: Pulse startup remains prohibited unless a future card explicitly approves it.

## Gate L10: No Pulse Endpoint Calls

Required proof: validation proves Pulse endpoints are not called and `localhost:31337` is not probed.

Failure signal: HTTP call, socket call, curl probe, health check, or localhost endpoint access.

S11D status: Prohibited by default.

Future S12 implication: Pulse endpoint calls remain prohibited unless a future card explicitly approves them.

## Gate L11: No PAI Memory Writes

Required proof: validation proves PAI Memory is not written.

Failure signal: PAI Memory file creation, mutation, migration, import, promotion, or generated update.

S11D status: Prohibited by default.

Future S12 implication: PAI Memory remains canonical PAI state and cannot be written by read-only trials.

## Gate L12: No ISA Writes

Required proof: validation proves ISA is not written.

Failure signal: ISA file creation, mutation, migration, import, or generated update.

S11D status: Prohibited by default.

Future S12 implication: ISA remains canonical PAI state and cannot be written by read-only trials.

## Gate L13: No Product Memory Promotion

Required proof: validation proves product memories are not silently promoted into PAI Memory.

Failure signal: product-memory promotion, normalization, migration, or import into PAI Memory.

S11D status: Prohibited by default.

Future S12 implication: product-memory promotion remains prohibited without a separate architect-approved policy.

## Gate L14: Authority Boundary Preserved

Required proof: future S12 preserves boundaries among `PAI_SYSTEM_PROMPT.md`, `CLAUDE.md`, future compact router surfaces, and Codex policy/config.

Failure signal: Claude-shaped files are copied directly into Codex surfaces or authority levels are flattened.

S11D status: Evidence prerequisite available.

Future S12 implication: authority boundary preservation must be reported before any future runtime adapter planning.

## Gate L15: Launcher and Inference Boundary Preserved

Required proof: future S12 preserves launcher and inference boundaries without invoking Codex as a runtime engine.

Failure signal: launcher, wrapper, installer, migration, inference profile, or runtime invocation is created or executed.

S11D status: Evidence prerequisite available.

Future S12 implication: S12 must remain read-only and non-runtime unless separately approved.

## Gate L16: Hook and Lifecycle Boundary Preserved

Required proof: future S12 preserves hook/lifecycle and event/context envelope boundaries without creating Codex hooks, rules, commands, agents, or skills.

Failure signal: hook, rule, skill, agent, command, lifecycle payload, or generated Codex control surface is created.

S11D status: Evidence prerequisite available.

Future S12 implication: unsupported hook and lifecycle surfaces must be reported, not implemented.

## Gate L17: Unsupported Surface Reporting

Required proof: future S12 reports unsupported surfaces without treating them as supported or converting them into runtime payloads.

Failure signal: unsupported surfaces are ignored, represented as supported, or materialized as adapter payloads.

S11D status: Evidence prerequisite available.

Future S12 implication: unsupported-surface reporting remains mandatory before any future compatibility claim.

## Gate L18: Evidence Report and Rollback Reporting

Required proof: future S12 creates only approved non-canonical evidence reports and rollback/no-residue reporting.

Failure signal: created PAI runtime audit artifact, manifest, executable schema, live-trial artifact outside approved set, runtime payload, or missing rollback/no-residue evidence.

S11D status: Proposed only.

Future S12 implication: evidence and rollback reporting must remain non-canonical unless separately approved.

## Gate L19: No Drop-In Claim

Required proof: future S12 final handoff states no drop-in claim and confirms Codex is not currently proven drop-in for existing local PAI v5 files.

Failure signal: any claim that Codex is drop-in today, official upstream engine, replacement-grade, or runtime-compatible without future validation.

S11D status: Prohibited by default.

Future S12 implication: no drop-in claim is allowed until a later architect-approved validation track proves it.

## Minimum S12 Entry Threshold

Minimum entry threshold:

- Explicit architect approval is required.
- Explicit user consent design is required before any live local read.
- S10 fixture track must be accepted.
- S11 evidence track must be accepted.
- S12 write set must be exact.
- S12 must be read-only unless separately approved.
- S12 must preserve no default live user-local reads.
- S12 must preserve no PAI Memory writes, no ISA writes, no Pulse startup, no Pulse endpoint calls, no root `AGENTS.md`, no `.codex`, no product-memory promotion, and no drop-in claim.

S11D does not mark live-read gates as passed.

## Non-Goals

This gate proposal does not authorize S12, live trials, existing-local-v5 access, live user-local reads, runtime adapter work, root `AGENTS.md`, `.codex`, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory promotion, Codex runtime invocation, Claude Code invocation, manifests, executable schemas, audit artifacts, runtime payloads, official upstream engine claims, or drop-in claims.
