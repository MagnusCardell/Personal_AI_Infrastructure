# V5 Codex Fixture Trial Sequence and Gate Model

## Purpose

Define the future sequence and gate model for a read-only fixture trial before any implementation, fixture creation, or trial execution.

## Scope

This document is design-only. S9A runs no trial phases and creates no fixture, harness, manifest, audit artifact, executable schema, generated config, runtime file, adapter payload, Memory payload, ISA payload, Pulse payload, or trial output.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement is plausible only through a designed adapter. Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CODEX_INTEGRATED_READ_ONLY_FIXTURE_TRIAL_ARCHITECTURE.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_READ_ONLY_EVENT_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_MEMORY_ISA_SINGLE_WRITER_POLICY_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_SCHEMA_DRY_RUN_VALIDATION_SPEC.md`

No new Codex capability claim is introduced in S9A.

## Sequence Problem Statement

A future read-only fixture trial must sequence checks so unsafe work cannot happen accidentally. Authority must precede router placement, fixture isolation must precede any trial behavior, Pulse no-start/no-call must precede Pulse-related claims, and Memory/ISA no-write proof must precede any state workflow claim.

S9A designs the sequence only. It does not authorize fixture creation, manifest creation, audit artifact creation, schema creation, harness creation, or trial execution.

## Trial Phase Model

Future trial phases:

| Phase | Meaning | S9A status |
| --- | --- | --- |
| `T0: Architect approval` | Architect approves a bounded future milestone and write set. | Not run. |
| `T1: Fixture source selection` | Future source is selected from approved source classes. | Not run. |
| `T2: Fixture isolation verification` | Future fixture isolation and no-live-state boundaries are verified. | Not run. |
| `T3: Manifest dry-run validation` | Future manifest policy is validated without execution. | Not run. |
| `T4: Authority envelope dry-run` | Future authority envelope is checked for order, size, and no-copy behavior. | Not run. |
| `T5: Launcher/inference dry-run` | Future invocation and request/response plans are validated as non-executable. | Not run. |
| `T6: Hook/lifecycle dry-run` | Future event and lifecycle mappings are checked for unsupported surfaces. | Not run. |
| `T7: Pulse no-start/no-call verification` | Future checks prove Pulse is not started or called. | Not run. |
| `T8: Memory/ISA no-write verification` | Future checks prove no PAI Memory or ISA writes occur. | Not run. |
| `T9: Unsupported-surface reporting` | Future unsupported surfaces are reported explicitly. | Not run. |
| `T10: Audit report generation` | Future advisory audit output is generated under approved scope. | Not run. |
| `T11: Rollback/no-residue verification` | Future no-residue and rollback proof is checked. | Not run. |
| `T12: Architect review` | Architect reviews evidence and decides whether to proceed. | Not run. |

S9A runs none of these phases.

## Gate Model

Gate rules:

- Gates fail closed.
- Failed gates block drop-in claims.
- Runtime gates cannot pass in S9A.
- Unsupported surfaces are reported, not silently ignored.
- No fixture, manifest, audit artifact, schema, harness, or trial exists in S9A.
- Future live existing-local-v5 work requires separate approval.

## Preflight Gates

| Gate ID | Phase | Gate | Required evidence | Failure signal | Blocks drop-in? | S9A status |
| --- | --- | --- | --- | --- | --- | --- |
| TG-001 | T0 | Approved write/read scope. | Architect-approved future write set and read set. | Any unapproved file or root touched. | Yes. | Designed only. |
| TG-002 | T2 | Fixture isolation. | Future fixture root is isolated from release, live `.claude`, live `.codex`, and PAI state. | Fixture uses live user-local state or writes outside scope. | Yes. | Designed only. |
| TG-003 | T2 | No live user-local state. | Future run proves no `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or private state reads. | Private-state access. | Yes. | Designed only. |
| TG-004 | T0 | No root `AGENTS.md`. | Future run proves root `AGENTS.md` is absent or untouched unless authorized. | Root `AGENTS.md` created or modified. | Yes. | Designed only. |
| TG-005 | T0 | No `.codex/`. | Future run proves `.codex/` is absent or untouched unless authorized. | `.codex/` created or modified. | Yes. | Designed only. |

## Authority Gates

| Gate ID | Phase | Gate | Required evidence | Failure signal | Blocks drop-in? | S9A status |
| --- | --- | --- | --- | --- | --- | --- |
| TG-006 | T4 | Authority envelope defined. | Future envelope preserves `PAI_SYSTEM_PROMPT.md` as high-authority doctrine. | Doctrine omitted, truncated, or demoted. | Yes. | Designed only. |
| TG-007 | T4 | Compact router non-installable. | Future router remains a non-installed design or approved compact router. | `CLAUDE.md` or `PAI_SYSTEM_PROMPT.md` cloned into `AGENTS.md`. | Yes. | Designed only. |

## Launcher and Inference Gates

| Gate ID | Phase | Gate | Required evidence | Failure signal | Blocks drop-in? | S9A status |
| --- | --- | --- | --- | --- | --- | --- |
| TG-008 | T5 | Launcher plan non-executable. | Future launcher plan has selected engine, denied behaviors, unsupported-surface report, and no process invocation. | Launcher, wrapper, or runtime command created or executed. | Yes. | Designed only. |
| TG-009 | T5 | Inference plan non-executable. | Future request envelope and response envelope are validated without model calls. | Codex runtime or Claude Code invoked. | Yes. | Designed only. |

## Hook and Lifecycle Gates

| Gate ID | Phase | Gate | Required evidence | Failure signal | Blocks drop-in? | S9A status |
| --- | --- | --- | --- | --- | --- | --- |
| TG-010 | T6 | Hook/lifecycle mapping non-executable. | Future mapping classifies hook lifecycle behavior without installing hooks, rules, or config. | Claude hooks copied or Codex hook/rule commands run. | Yes. | Designed only. |

## Pulse Gates

| Gate ID | Phase | Gate | Required evidence | Failure signal | Blocks drop-in? | S9A status |
| --- | --- | --- | --- | --- | --- | --- |
| TG-011 | T7 | Pulse no-start. | Future proof shows Pulse is not started. | Pulse process started or startup attempted. | Yes. | Designed only. |
| TG-012 | T7 | Pulse no-call. | Future proof shows no Pulse endpoint call and no `localhost:31337` probe. | Endpoint call, HTTP probe, or `localhost:31337` access. | Yes. | Designed only. |

## Memory and ISA Gates

| Gate ID | Phase | Gate | Required evidence | Failure signal | Blocks drop-in? | S9A status |
| --- | --- | --- | --- | --- | --- | --- |
| TG-013 | T8 | PAI Memory no-write. | Future proof shows `memory_write_status` denied or none. | PAI Memory write or write attempt without denial. | Yes. | Designed only. |
| TG-014 | T8 | ISA no-write. | Future proof shows `isa_write_status` denied or none. | ISA write or write attempt without denial. | Yes. | Designed only. |
| TG-015 | T8 | Product memory non-promotion. | Future proof shows Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory. | Product memories silently promoted. | Yes. | Designed only. |

## Manifest and Audit Gates

| Gate ID | Phase | Gate | Required evidence | Failure signal | Blocks drop-in? | S9A status |
| --- | --- | --- | --- | --- | --- | --- |
| TG-016 | T9 | Unsupported-surface report. | Future `unsupported_surface_report` lists unmapped Claude, Codex, Pulse, Memory, ISA, and hook gaps. | Unsupported surface silently ignored. | Yes. | Designed only. |
| TG-017 | T10 | Audit provenance. | Future advisory audit output includes provenance and source lineage. | Missing provenance or canonical-state promotion. | Yes. | Designed only. |

## No-Write and Denied-Path Gates

Denied-path gates include no release-file writes, no protected-path writes, no root `AGENTS.md`, no `.codex/`, no Memory writes, no ISA writes, no Pulse state, no generated runtime config, and no trial outputs outside future approved paths.

## Rollback Gates

| Gate ID | Phase | Gate | Required evidence | Failure signal | Blocks drop-in? | S9A status |
| --- | --- | --- | --- | --- | --- | --- |
| TG-018 | T11 | Rollback/no-residue. | Future proof shows no repository residue, no live user-local writes, no Pulse state, and no generated runtime material. | Residue detected or rollback missing. | Yes. | Designed only. |

## Trial Completion Gates

| Gate ID | Phase | Gate | Required evidence | Failure signal | Blocks drop-in? | S9A status |
| --- | --- | --- | --- | --- | --- | --- |
| TG-019 | T12 | No drop-in claim. | Future report says Codex is not drop-in unless all gates pass. | Drop-in claim before gates pass. | Yes. | Designed only. |
| TG-020 | T12 | Architect review. | Architect reviews future evidence and decides next milestone. | Automated promotion or unapproved continuation. | Yes. | Designed only. |

## Gate Failure Handling

Any future gate failure must stop the trial, record `failure_reason`, produce or update a future advisory `denied_action_report` or `unsupported_surface_report`, preserve rollback/no-residue posture, and avoid promotion into PAI Memory, ISA, Pulse state, Claude memory, or Codex memory.

## Required Future Proofs

Required future proofs:

- Scope and fixture isolation.
- No live user-local state.
- No root `AGENTS.md`.
- No `.codex/`.
- Authority envelope and compact router safety.
- Non-executable launcher and inference plans.
- Non-executable hook lifecycle mapping.
- Pulse no-start and no-call.
- PAI Memory no-write.
- ISA no-write.
- Product memory non-promotion.
- Unsupported-surface reporting.
- Audit provenance.
- Rollback/no-residue.
- Architect review before any next step.

## Prohibited Sequence Designs

Prohibited designs:

- Running any phase in S9A.
- Creating a fixture, harness, manifest instance, audit artifact, executable schema, or trial output.
- Starting with live existing-local-v5 state.
- Installing root `AGENTS.md` or `.codex/`.
- Invoking Claude Code or Codex runtime.
- Starting Pulse or calling Pulse endpoints.
- Writing PAI Memory or ISA.
- Claiming drop-in readiness.

## Non-Goals

S9A does not implement the adapter, create fixtures, create a test harness, create manifests, create audit artifacts, create executable schemas, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create generated configs, create migration scripts, create runtime files, create adapter payloads, create Memory payloads, create ISA payloads, create Pulse payloads, create trial outputs, run a read-only trial, inspect private user-local state, read live existing-local-v5 state, modify release files, start Pulse, call Pulse endpoints, probe `localhost:31337`, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, run Codex hook/rule/execpolicy commands, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, authorize product-memory promotion into PAI Memory, authorize dual-engine uncoordinated writes, or advance beyond S9A.
