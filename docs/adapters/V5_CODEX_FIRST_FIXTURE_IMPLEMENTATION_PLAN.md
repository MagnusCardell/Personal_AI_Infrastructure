# V5 Codex First Fixture Implementation Plan

## Purpose

Define the future first implementation milestone for a read-only fixture trial without authorizing implementation in S9B.

## Scope

S9B creates a future implementation plan and proposed write-set only. S9B does not implement the plan.

This document does not create fixtures, a test harness, manifests, audit artifacts, executable schemas, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, runtime files, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, fixture files, or harness files.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement is plausible only through a designed adapter. Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

Claude-shaped files must not be copied directly into Codex surfaces.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CODEX_INTEGRATED_READ_ONLY_FIXTURE_TRIAL_ARCHITECTURE.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_SEQUENCE_AND_GATE_MODEL.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_COVERAGE_MATRIX.md`
- `docs/adapters/V5_CODEX_TRIAL_FAILURE_ROLLBACK_AND_AUDIT_MODEL.md`
- `docs/adapters/V5_CODEX_INTEGRATED_TRIAL_DECISION_LOG.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- Repository-local PAI v5 release evidence under `Releases/v5.0.0/`.

No new Codex capability claim is introduced in S9B.

## Implementation Planning Status

S9B does not approve or perform S10A implementation.

This plan is a proposal for architect review. Future S10A may begin only after explicit architect approval with a bounded write set, read set, validation contract, and hard failure conditions.

## Future S10A Objective

Future S10A is proposed as the first possible fixture-only implementation milestone.

The proposed objective is to create an isolated read-only fixture corpus and a read-only harness that validates fixture metadata, protected-path denial, unsupported-surface reporting, no-write posture, no-private-state posture, Pulse no-start/no-call posture, Memory/ISA no-write posture, and rollback/no-residue reporting.

Future S10A must not claim Codex is drop-in.

## Future S10A Non-Goals

Future S10A non-goals should include:

- No adapter implementation.
- No runtime adapter files.
- No root `AGENTS.md`.
- No `.codex/`.
- No Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, or migration scripts.
- No live existing-local-v5 trial.
- No live user-local state reads.
- No Pulse startup or Pulse endpoint calls.
- No PAI Memory writes.
- No ISA writes.
- No Claude Code invocation.
- No Codex runtime invocation unless explicitly approved in the future S10A card.
- No product-memory promotion into PAI Memory.
- No dual-engine uncoordinated writes.

## Future S10A Write-Set Philosophy

Future S10A should use isolated repository fixture paths only. It should keep all future write paths under non-runtime adapter-test areas and should not modify `Releases/`, `.claude/`, `PAI/`, root `AGENTS.md`, `.codex/`, root hooks, root skills, root agents, root commands, root settings, root installers, or live user-local paths.

The future write set must separate:

- Fixture files.
- Fixture metadata.
- Read-only harness script.
- Harness documentation.
- Expected-report examples only if separately approved later.
- S10A execution plan and design notes.

S9B creates none of these artifacts.

## Future S10A Fixture Strategy

Future S10A fixture strategy should start with release-derived and synthetic fixtures only. Sanitized user fixtures require later explicit user approval and architect approval. Live existing-local-v5 state is not a fixture source for S10A.

Future fixture selection must cover authority, launcher/inference, hook lifecycle, Pulse, Memory/ISA, denied paths, unsupported surfaces, product memory boundaries, dual-engine boundaries, rollback, and no-residue behavior.

## Future S10A Harness Strategy

Future S10A harness strategy should be read-only.

The harness should inspect approved fixture files and metadata only. It should not invoke Claude Code, should not invoke Codex as a runtime engine unless separately approved, should not start Pulse, should not call Pulse endpoints, should not write PAI Memory, and should not write ISA.

The harness should produce validation output only in future approved paths.

## Future S10A Validation Strategy

Future validation should fail closed on:

- Unapproved write paths.
- Protected-path changes.
- Root `AGENTS.md` or `.codex/`.
- Live user-local paths.
- Release file writes.
- Direct Claude-file copy into Codex surfaces.
- Runtime invocation.
- Pulse startup or endpoint calls.
- PAI Memory writes.
- ISA writes.
- Product-memory promotion.
- Missing `denied_action_report`.
- Missing `unsupported_surface_report`.
- Missing rollback/no-residue report.
- Drop-in overclaim.

## Future S10A No-Write Strategy

Future S10A must prove no writes outside approved future S10A paths. It must also prove no PAI Memory writes, no ISA writes, no Pulse state writes, no release mutations, no root `AGENTS.md`, no `.codex/`, and no generated runtime config.

## Future S10A No-Private-State Strategy

Future S10A must operate only on approved fixtures, not live user-local state.

Future S10A must not read live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, `~/.codex/memories`, or other private user-local state.

Required future wording: no live user-local state is read.

## Future S10A Pulse Strategy

Pulse is central v5 infrastructure, but future S10A must not start Pulse, call Pulse endpoints, probe `localhost:31337`, create Pulse payloads, create a Pulse bridge, or claim Pulse parity.

Future S10A may validate only static fixture evidence and no-start/no-call reporting.

## Future S10A Memory and ISA Strategy

PAI Memory and ISA artifacts are canonical PAI state.

Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory. Product memories must not be silently promoted into PAI Memory.

Future S10A must not write PAI Memory or ISA. Future writes require a single-writer policy, provenance, rollback, validation, and conflict handling.

## Future S10A Rollback and No-Residue Strategy

Future S10A should include rollback/no-residue reporting that proves:

- No protected paths changed.
- No live user-local writes occurred.
- No Pulse state exists.
- No PAI Memory writes occurred.
- No ISA writes occurred.
- No root `AGENTS.md` or `.codex/` was created.
- No generated runtime config was created.
- No hidden temp artifacts were committed to the repository.

## Future S10A Audit Strategy

Future S10A audit output, if approved, must be advisory only. It must not be PAI Memory, ISA, Pulse state, Claude memory, or Codex memory.

Future audit fields should include provenance, denied action report, unsupported surface report, no-write status, no-private-state status, Pulse no-start/no-call status, Memory/ISA no-write status, rollback status, no-residue status, and drop-in claim status.

## Future S10A Completion Criteria

Future S10A completion criteria should include:

- Approved write set only.
- Fixture metadata exists.
- Harness is read-only.
- Protected-path checks exist.
- Denied-path checks exist.
- Unsupported-surface reporting exists.
- No live user-local state is read.
- Pulse no-start/no-call reporting exists.
- PAI Memory no-write reporting exists.
- ISA no-write reporting exists.
- Product-memory non-promotion reporting exists.
- Rollback/no-residue reporting exists.
- No drop-in claim appears.

| Future component | Proposed purpose | Proposed path class | Writes allowed in S9B? | Future approval required | Main hazard | Required future proof |
| --- | --- | --- | --- | --- | --- | --- |
| Fixture files | Hold isolated release-derived, synthetic, negative, and unsupported-surface evidence. | Future non-runtime adapter-test fixture corpus path. | No. | Yes. | Fixture drift, live-state leakage, or release mutation. | Fixture source provenance and isolation proof. |
| Fixture metadata | Describe fixture IDs, sources, included/excluded surfaces, expected denials, and no-write proofs. | Future fixture metadata path. | No. | Yes. | Metadata can understate denied paths or unsupported surfaces. | Metadata completeness and validation proof. |
| Read-only harness script | Check fixture metadata, protected paths, denied paths, unsupported surfaces, and no-write reports. | Future non-runtime adapter-test harness path. | No. | Yes. | Harness can become runtime adapter implementation. | Read-only proof and command-denial proof. |
| Harness documentation | Explain future harness operation and constraints. | Future adapter-test docs path. | No. | Yes. | Docs may imply S10A is already approved. | Explicit approval boundary and non-runtime wording. |
| Expected-report examples | Illustrate future advisory reports if separately approved later. | Future examples path. | No. | Separate explicit approval. | Examples can be mistaken for audit artifacts. | Non-canonical advisory labeling and no-promotion proof. |
| S10A execution plan | Record future S10A task contract and validation results. | Future docs/adapters execution plan path. | No. | Yes. | Scope creep into implementation without gates. | Architect-approved contract and changed-file check. |

## Blockers Before S10A

Blockers before S10A:

- Architect approval is required.
- S10A write set must be explicit.
- Fixture path classes must be approved.
- Harness path classes must be approved.
- Expected report examples require separate explicit approval if included.
- Protected paths must remain blocked.
- Live existing-local-v5 reads remain blocked.
- Runtime surfaces remain blocked.
- Drop-in claims remain blocked.

## Prohibited Implementation Plan Semantics

Prohibited semantics:

- S9B approves S10A.
- S9B creates fixture files.
- S9B creates harness files.
- S9B creates manifest instances.
- S9B creates audit artifacts.
- S9B creates executable schemas.
- S9B creates runtime files.
- S9B authorizes live existing-local-v5 trial execution.
- S9B authorizes PAI Memory writes or ISA writes.
- S9B authorizes Pulse startup, Pulse endpoint calls, or Pulse implementation.
- S9B implies Claude-shaped files may be copied directly into Codex surfaces.
- S9B authorizes product-memory promotion into PAI Memory.
- S9B authorizes dual-engine uncoordinated writes.

## Non-Goals

S9B does not implement the adapter, implement S10A, approve S10A, create fixtures, create a test harness, create manifests, create audit artifacts, create executable schemas, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create generated configs, create migration scripts, create runtime files, create adapter payloads, create Memory payloads, create ISA payloads, create Pulse payloads, create trial outputs, create fixture files, create harness files, run a read-only trial, inspect private user-local state, read live `~/.claude/PAI`, read live `~/.codex`, modify release files, start Pulse, call Pulse endpoints, probe `localhost:31337`, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, run Codex hook/rule/execpolicy commands, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, imply Claude-shaped files can be copied directly into Codex surfaces, authorize product-memory promotion into PAI Memory, authorize dual-engine uncoordinated writes, or advance beyond S9B.
