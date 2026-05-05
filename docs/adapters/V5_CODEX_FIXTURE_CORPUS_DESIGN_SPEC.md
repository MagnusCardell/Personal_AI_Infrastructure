# V5 Codex Fixture Corpus Design Spec

## Purpose

Define the future fixture corpus needed for first read-only validation without creating fixture files.

## Scope

S9B creates no fixtures.

This document is design-only. It does not create fixture files, fixture metadata files, harness files, manifests, audit artifacts, executable schemas, runtime files, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, root `AGENTS.md`, or `.codex/`.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement is plausible only through a designed adapter. Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CODEX_INTEGRATED_READ_ONLY_FIXTURE_TRIAL_ARCHITECTURE.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_SEQUENCE_AND_GATE_MODEL.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_COVERAGE_MATRIX.md`
- `docs/adapters/V5_CODEX_TRIAL_FAILURE_ROLLBACK_AND_AUDIT_MODEL.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_READ_ONLY_EVENT_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_MEMORY_ISA_SINGLE_WRITER_POLICY_SPEC.md`
- Repository-local PAI v5 release evidence under `Releases/v5.0.0/`.

No new Codex capability claim is introduced in S9B.

## Fixture Corpus Status

The fixture corpus is proposed only. S9B does not create fixture files.

Future S10A may create fixture files only after architect approval. S10A is not approved by S9B.

## Fixture Design Principles

Principles:

- Fixture-first, not live existing-local-v5 first.
- Read-only validation only.
- Release-derived and synthetic fixtures first.
- Sanitized user fixtures require later explicit approval.
- No live user-local state.
- No release-file mutation.
- No root `AGENTS.md`.
- No `.codex/`.
- No PAI Memory writes.
- No ISA writes.
- No Pulse startup or endpoint calls.
- No direct Claude-file copying into Codex surfaces.
- Explicit `denied_action_report`.
- Explicit `unsupported_surface_report`.
- Rollback and no-residue reporting.

## Fixture Source Classes

Fixture source classes:

| Source class | Meaning | S9B status |
| --- | --- | --- |
| `release-derived-fixture` | Future isolated copy or excerpt derived from repository-local release evidence. | Proposed only. |
| `synthetic-fixture` | Future minimal synthetic evidence shaped to test safety behavior. | Proposed only. |
| `sanitized-user-fixture` | Future user-approved sanitized copy of selected user material. | Proposed only and requires later explicit approval. |
| `negative-safety-fixture` | Future fixture that intentionally represents denied behavior. | Proposed only. |
| `unsupported-surface-fixture` | Future fixture that requires explicit unsupported-surface reporting. | Proposed only. |

Live existing-local-v5 state is not a fixture source for S10A.

Sanitized user fixtures require later explicit approval and must not be created in S9B.

## Fixture Isolation Rules

Future fixture isolation rules:

- Fixture roots must be under approved non-runtime adapter-test paths.
- Fixture content must not be live `~/.claude/PAI`, live `~/.codex`, or other private user-local state.
- Fixture creation must not modify `Releases/`.
- Fixtures must not install root `AGENTS.md`.
- Fixtures must not create `.codex/`.
- Fixtures must not include executable runtime adapters.
- Fixtures must not include PAI Memory payloads or ISA payloads except isolated static fixture examples approved for testing.
- Fixtures must not include Pulse payloads.
- Fixtures must include expected denials and unsupported surfaces.

## Fixture Metadata Model

Future fixture metadata fields:

- `fixture_id`
- `fixture_name`
- `fixture_source_class`
- `pai_version`
- `source_paths`
- `included_surfaces`
- `excluded_surfaces`
- `denied_paths`
- `expected_denials`
- `expected_unsupported_surfaces`
- `expected_no_write_proofs`
- `expected_audit_fields`
- `rollback_expectation`
- `privacy_status`

S9B creates no metadata files.

## Fixture Corpus Table

| Fixture ID | Fixture name | Source class | Covered seams | Excluded surfaces | Main risk | Future implementation status |
| --- | --- | --- | --- | --- | --- | --- |
| FX-001 | release-baseline-static fixture | `release-derived-fixture` | Baseline release layout, protected paths, release evidence inventory. | Live user-local state, runtime execution, Pulse calls. | Fixture accidentally mutates or mirrors release files. | Proposed / requires architect review. |
| FX-002 | authority-doctrine fixture | `release-derived-fixture` | `PAI_SYSTEM_PROMPT.md` high-authority doctrine and `CLAUDE.md` non-destination boundary. | Full Codex router installation, root `AGENTS.md`. | Doctrine demotion or direct copy into Codex surfaces. | Proposed / requires architect review. |
| FX-003 | compact-router-non-installation fixture | `synthetic-fixture` | Compact router non-installation and no root `AGENTS.md`. | Actual router file, `.codex/`. | Skeleton mistaken for installable guidance. | Proposed / requires architect review. |
| FX-004 | launcher-inference-static fixture | `release-derived-fixture` | Launcher seam and inference seam static coupling evidence. | Runtime invocation, Codex execution, Claude Code execution. | Harness could become launcher implementation. | Proposed / requires architect review. |
| FX-005 | hook-lifecycle-static fixture | `release-derived-fixture` | Hook lifecycle mapping, payload assumptions, event classification. | Hook execution, Codex hook/rule files. | Claude hook files copied into Codex surfaces. | Proposed / requires architect review. |
| FX-006 | Pulse-static-no-start fixture | `release-derived-fixture` | Pulse identity, read-only event, no-start/no-call reporting. | Live Pulse state, endpoint calls, `localhost:31337`. | Static evidence could be mistaken for Pulse parity. | Proposed / requires architect review. |
| FX-007 | Memory-ISA-static-no-write fixture | `release-derived-fixture` | PAI Memory and ISA no-write, single-writer boundary, non-promotion. | Live PAI Memory, live ISA, product memory imports. | Fixture could be mistaken for canonical state. | Proposed / requires architect review. |
| FX-008 | denied-path-negative fixture | `negative-safety-fixture` | Protected path and denied write behavior. | Actual writes to protected paths. | Negative case could cause a real write if harness is unsafe. | Proposed / requires architect review. |
| FX-009 | product-memory-negative fixture | `negative-safety-fixture` | Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` not PAI Memory. | Real product memories. | Product memories silently promoted into PAI Memory. | Proposed / requires architect review. |
| FX-010 | unsupported-surface-reporting fixture | `unsupported-surface-fixture` | `unsupported_surface_report` completeness across all seams. | Silent emulation. | Unsupported gaps hidden as success. | Proposed / requires architect review. |
| FX-011 | rollback-no-residue fixture | `synthetic-fixture` | Rollback and no-residue reporting. | Actual rollback mutations. | Report could miss generated residue. | Proposed / requires architect review. |
| FX-012 | dual-engine-boundary fixture | `synthetic-fixture` | Claude/Codex identity labels, product memory separation, single-writer block. | Dual-engine uncoordinated writes. | Coexistence mistaken for write permission. | Proposed / requires architect review. |

## Authority Fixtures

Authority fixtures must preserve `PAI_SYSTEM_PROMPT.md` as high-authority PAI doctrine, keep `CLAUDE.md` as an official Claude-facing surface, and keep future Codex `AGENTS.md`, if later authorized, as a compact router. They must not copy Claude-shaped files directly into Codex surfaces.

## Launcher and Inference Fixtures

Launcher and inference fixtures must remain static. They may cover source evidence for launcher seam and inference seam behavior but must not create launchers, wrappers, runtime files, request executors, or model-call adapters.

## Hook and Lifecycle Fixtures

Hook lifecycle fixtures must cover Claude hook registrations, event names, payload assumptions, permission behavior, and lifecycle hazards. They must not execute hooks, create Codex hooks, create Codex rules, or create Codex config.

## Pulse Fixtures

Pulse fixtures must treat Pulse as central v5 infrastructure while proving only no-start/no-call posture. They must not start Pulse, call Pulse endpoints, probe `localhost:31337`, create Pulse payloads, or claim Pulse parity.

## Memory and ISA Fixtures

Memory and ISA fixtures must prove no-write and non-promotion expectations. PAI Memory and ISA artifacts are canonical PAI state. Product memories are not PAI Memory, and future writes require a single-writer policy, provenance, rollback, validation, and conflict handling.

## Negative Safety Fixtures

Negative safety fixtures intentionally represent denied actions such as protected-path writes, root `AGENTS.md`, `.codex/`, Pulse endpoint calls, PAI Memory writes, ISA writes, product-memory promotion, and drop-in overclaim.

They must be inert data in future fixture files, never executable behavior.

## Unsupported Surface Fixtures

Unsupported surface fixtures must require `unsupported_surface_report` output for unmapped Claude hooks, settings, skills, agents, commands, Pulse surfaces, Memory/ISA behaviors, launcher flags, inference assumptions, and router gaps.

## Rollback and No-Residue Fixtures

Rollback and no-residue fixtures must validate future reporting that no protected paths, live user-local state, release files, root `AGENTS.md`, `.codex/`, Pulse state, PAI Memory, ISA, runtime configs, or hidden temp artifacts were created or modified.

## Required Future Proofs

Required future proofs:

- Fixture provenance.
- Fixture isolation.
- Metadata completeness.
- No live user-local state.
- No release mutation.
- No protected-path writes.
- No runtime execution.
- No Pulse startup or endpoint calls.
- No PAI Memory or ISA writes.
- No product-memory promotion.
- Rollback/no-residue reporting.

## Prohibited Fixture Designs

Prohibited designs:

- Using live existing-local-v5 state as S10A fixture source.
- Creating sanitized user fixtures without later explicit approval.
- Copying `CLAUDE.md` into Codex surfaces.
- Installing root `AGENTS.md`.
- Creating `.codex/`.
- Creating executable runtime adapter fixtures.
- Creating Pulse payloads.
- Creating Memory payloads or ISA payloads as canonical state.
- Creating fixtures in S9B.

## Non-Goals

S9B does not implement the adapter, approve S10A, create fixtures, create a test harness, create manifests, create audit artifacts, create executable schemas, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create generated configs, create migration scripts, create runtime files, create adapter payloads, create Memory payloads, create ISA payloads, create Pulse payloads, create trial outputs, create fixture files, create harness files, run a read-only trial, inspect private user-local state, read live existing-local-v5 state, modify release files, start Pulse, call Pulse endpoints, probe `localhost:31337`, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, run Codex hook/rule/execpolicy commands, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, imply Claude-shaped files can be copied directly into Codex surfaces, authorize product-memory promotion into PAI Memory, authorize dual-engine uncoordinated writes, or advance beyond S9B.
