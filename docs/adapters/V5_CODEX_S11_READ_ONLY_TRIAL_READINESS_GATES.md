# V5 Codex S11 Read-Only Trial Readiness Gates

## Purpose

Define proposed readiness gates for a future S11 read-only trial milestone. S11 is proposed only and requires architect approval before any work begins.

Codex is not currently proven drop-in for existing local PAI v5 files. S10G closes the fixture-only track and proposes gates only; it does not authorize S11, live trials, existing-local-v5 access, or runtime adapter implementation.

## Scope

These gates describe what a future architect-approved S11 would need to prove before any read-only trial can proceed. They are not an implementation plan and do not create runtime adapter files, root `AGENTS.md`, `.codex`, Codex config, hooks, rules, skills, agents, commands, launchers, manifests, audit artifacts, executable schemas, Memory payloads, ISA payloads, or Pulse payloads.

Future S11 must remain read-only unless separately approved. It must preserve no live user-local access by default, no PAI Memory writes, no ISA writes, no Pulse startup, no Pulse endpoint calls, no product-memory promotion, and no drop-in claim.

## Evidence Base

Evidence base:

- S10A fixture-only metadata corpus and read-only harness.
- S10B negative-control regression self-tests.
- S10C semantic fixture metadata and harness policy validation.
- S10D fixture case data and expected-behavior validation.
- S10E global coverage validation.
- S10F no-residue determinism validation.

The S10 fixture-only track is ready for architect review, but S10G must not mark live-trial gates as passed.

## S11 Readiness Problem Statement

The next decision is whether to approve S11 as a read-only trial readiness milestone. The problem is to move from isolated fixture validation toward carefully bounded trial planning without reading existing-local-v5 state by default and without implying Codex is drop-in today.

S11 must not require uninstalling Claude Code. S11 must not write PAI Memory or ISA. S11 must not start Pulse or call Pulse endpoints unless a future card explicitly approves those actions.

## Gate Model

Each gate below includes Required proof, Failure signal, S10G status, and Future S11 implication.

S10G status values:

- Proposed: a future proof is described but not satisfied by S10G.
- Fixture-track evidence available: S10 provides supporting fixture-only evidence, but not live-trial evidence.
- Blocked pending architect approval: the gate cannot pass until a future card approves S11 scope.

## Gate R0: Architect Approval

Required proof: explicit architect approval for S11 objective, source protocol, allowed reads, forbidden reads, approved write set, final handoff, and hard failure conditions.

Failure signal: any S11 work begins from S10G documents alone or treats this proposal as authorization.

S10G status: Blocked pending architect approval.

Future S11 implication: S11 cannot start until architect approval is granted.

## Gate R1: Fixture Track Accepted

Required proof: architect accepts the S10 fixture-only closeout report, harness status, negative-control status, global coverage status, and no-residue status.

Failure signal: fixture-only evidence is incomplete, rejected, or not reviewed.

S10G status: Fixture-track evidence available.

Future S11 implication: S11 should not start until the S10 fixture-only track is accepted.

## Gate R2: Approved S11 Write Set

Required proof: future S11 card lists exact documents or reports that may be created, and confirms no runtime, manifest, audit artifact, schema, Memory payload, ISA payload, Pulse payload, root `AGENTS.md`, or `.codex` write is allowed.

Failure signal: an open-ended write set, generated runtime files, or any write outside approved docs.

S10G status: Proposed.

Future S11 implication: S11 needs a strict write-set contract before any command or edit.

## Gate R3: No Live User-Local State By Default

Required proof: future S11 source protocol forbids live user-local reads by default and explicitly forbids `~/.claude/`, `~/.claude/PAI/`, `~/.claude/projects/`, `~/.codex/`, and `~/.codex/memories/` unless a later card names a specific controlled source.

Failure signal: implicit live user-local reads, broad home-directory reads, or existing-local-v5 access without explicit approval.

S10G status: Proposed.

Future S11 implication: S11 must preserve no live user-local default behavior and must fail closed on private paths.

## Gate R4: Explicit Source Selection

Required proof: future S11 defines source selection with repository-relative fixtures, approved release files, or explicitly named read-only sample sources.

Failure signal: source discovery through private state, live default paths, or inferred local configuration.

S10G status: Proposed.

Future S11 implication: S11 can only inspect approved sources and must report denied sources.

## Gate R5: No Root AGENTS.md

Required proof: future S11 protected-path check confirms root `AGENTS.md` is not created or modified.

Failure signal: any root `AGENTS.md` creation, modification, generation, or migration.

S10G status: Proposed.

Future S11 implication: future Codex `AGENTS.md`, if later authorized, remains outside S11 unless explicitly approved.

## Gate R6: No .codex

Required proof: future S11 protected-path check confirms `.codex` is not created or modified.

Failure signal: any `.codex` config, profile, hook, rule, memory, or generated file.

S10G status: Proposed.

Future S11 implication: S11 must not create Codex runtime surfaces.

## Gate R7: No Pulse Startup

Required proof: future S11 validation proves Pulse is not started.

Failure signal: command, service, script, or harness behavior starts Pulse.

S10G status: Proposed.

Future S11 implication: Pulse startup remains prohibited unless a future card explicitly approves it.

## Gate R8: No Pulse Endpoint Calls

Required proof: future S11 validation proves Pulse endpoints are not called and `localhost:31337` is not probed.

Failure signal: HTTP call, socket call, curl probe, health check, or localhost endpoint access.

S10G status: Proposed.

Future S11 implication: Pulse endpoint calls remain prohibited unless explicitly approved later.

## Gate R9: No PAI Memory Writes

Required proof: future S11 confirms PAI Memory is not written and any Memory path is either forbidden or read-only if explicitly approved.

Failure signal: Memory file creation, mutation, migration, or promotion.

S10G status: Proposed.

Future S11 implication: PAI Memory remains canonical PAI state and cannot be written by read-only trials.

## Gate R10: No ISA Writes

Required proof: future S11 confirms ISA is not written and any ISA path is either forbidden or read-only if explicitly approved.

Failure signal: ISA file creation, mutation, migration, or generated state update.

S10G status: Proposed.

Future S11 implication: ISA remains canonical PAI state and cannot be written by read-only trials.

## Gate R11: No Product Memory Promotion

Required proof: future S11 confirms product memories are not silently promoted into PAI Memory and are reported as non-PAI Memory.

Failure signal: product-memory promotion, normalization, migration, or import into PAI Memory.

S10G status: Proposed.

Future S11 implication: product-memory promotion remains prohibited without a separate architect-approved policy.

## Gate R12: Authority Boundary Preserved

Required proof: future S11 report preserves the authority distinction between `PAI_SYSTEM_PROMPT.md`, `CLAUDE.md`, future compact router surfaces, and Codex policy/config.

Failure signal: Claude-shaped files are copied directly into Codex surfaces or authority levels are flattened.

S10G status: Fixture-track evidence available.

Future S11 implication: S11 must report authority boundary preservation before any later adapter work.

## Gate R13: Launcher and Inference Boundary Preserved

Required proof: future S11 report preserves launcher and inference boundaries without invoking Codex as a runtime engine.

Failure signal: launcher, wrapper, installer, migration, inference profile, or runtime invocation is created or executed.

S10G status: Fixture-track evidence available.

Future S11 implication: S11 remains read-only and must not implement launcher or inference behavior.

## Gate R14: Hook and Lifecycle Boundary Preserved

Required proof: future S11 report preserves hook/lifecycle and event/context envelope boundaries without creating Codex hooks, rules, commands, agents, or skills.

Failure signal: any hook, rule, skill, agent, command, lifecycle payload, or generated Codex control surface.

S10G status: Fixture-track evidence available.

Future S11 implication: S11 can report unsupported surfaces but cannot implement hooks or lifecycle mapping.

## Gate R15: Unsupported Surface Reporting

Required proof: future S11 produces read-only unsupported-surface reporting for surfaces not covered by Codex adapter evidence.

Failure signal: unsupported surfaces are ignored, treated as supported, or converted into runtime payloads.

S10G status: Fixture-track evidence available.

Future S11 implication: unsupported-surface reporting is mandatory before any drop-in readiness claim.

## Gate R16: Audit and Rollback Reporting

Required proof: future S11 defines report-only audit and rollback posture without creating audit artifacts, manifests, schemas, or trial outputs unless explicitly approved.

Failure signal: missing rollback/no-residue report, created audit artifact, created manifest, or created executable schema.

S10G status: Proposed.

Future S11 implication: S11 must preserve report-only audit/rollback semantics unless the future card approves concrete artifacts.

## Gate R17: No Drop-In Claim

Required proof: future S11 final handoff states no drop-in claim and confirms Codex is not currently proven drop-in for existing local PAI v5 files.

Failure signal: any claim that Codex is drop-in today, official upstream engine, replacement-grade, or runtime-compatible without future validation.

S10G status: Proposed.

Future S11 implication: no drop-in claim is allowed until a later architect-approved validation track proves it.

## Minimum S11 Entry Threshold

Minimum entry threshold:

- Explicit architect approval is required.
- S10 fixture-only track must be accepted.
- S11 write set must be exact.
- S11 must be read-only unless separately approved.
- S11 must preserve no live user-local reads by default.
- S11 must preserve no PAI Memory writes, no ISA writes, no Pulse startup, no Pulse endpoint calls, no root `AGENTS.md`, no `.codex`, no product-memory promotion, and no drop-in claim.

S10G does not mark live-trial gates as passed.

## Non-Goals

This gate document does not authorize S11, live trials, existing-local-v5 access, runtime adapter implementation, root `AGENTS.md`, `.codex`, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory promotion, manifests, audit artifacts, executable schemas, runtime payloads, Claude Code invocation, or Codex runtime invocation.
