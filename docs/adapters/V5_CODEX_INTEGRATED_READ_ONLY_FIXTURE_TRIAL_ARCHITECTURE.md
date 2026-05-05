# V5 Codex Integrated Read-Only Fixture-Trial Architecture

## Purpose

Define the future integrated architecture for a read-only fixture trial of Codex against PAI v5 semantics without touching live user state or creating runtime artifacts.

## Scope

S9A is an integrated architecture design only. It does not implement a trial.

S9A creates no fixtures, harnesses, manifests, executable schemas, audit artifacts, configs, runtime files, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, generated configs, migration scripts, trial outputs, root `AGENTS.md`, or `.codex/`.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement is plausible only through a designed adapter. Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_COMPACT_ROUTER_SPEC.md`
- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_ENGINE_PROFILE_AND_CAPABILITY_CONTRACT.md`
- `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md`
- `docs/adapters/V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_BRIDGE_IDENTITY_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_READ_ONLY_EVENT_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_OBSERVABILITY_AND_AUDIT_SPEC.md`
- `docs/adapters/V5_CODEX_MEMORY_ISA_SINGLE_WRITER_POLICY_SPEC.md`
- `docs/adapters/V5_CODEX_MEMORY_BOUNDARY_AND_PROMOTION_SPEC.md`
- `docs/adapters/V5_CODEX_ISA_WORKFLOW_AND_STATE_POLICY_SPEC.md`
- `docs/adapters/V5_CODEX_MEMORY_ISA_AUDIT_AND_CONFLICT_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_MANIFEST_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_SCHEMA_DRY_RUN_VALIDATION_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- Repository-local PAI v5 release evidence under `Releases/v5.0.0/`.

No new Codex capability claim is introduced in S9A.

## Architecture Problem Statement

Prior milestones defined individual seams, but a future read-only fixture trial needs one integrated architecture that shows how those seams are evaluated together without creating runtime material.

The architecture must prove design coherence before implementation. It must keep live `~/.claude/PAI`, live `~/.codex`, private user-local state, Pulse, PAI Memory, ISA, release files, root `AGENTS.md`, and `.codex/` protected. It must also preserve the rule that Claude-shaped files must not be copied directly into Codex surfaces.

## Trial Architecture Principles

Principles:

- Design first; no fixture creation in S9A.
- Static repository evidence only.
- Read-only fixture posture before any live existing-local-v5 posture.
- No root `AGENTS.md` creation.
- No `.codex/` creation.
- No manifest instance creation.
- No audit artifact creation.
- No executable schema creation.
- No harness creation.
- No trial execution.
- No Pulse startup or endpoint call.
- No PAI Memory writes.
- No ISA writes.
- No product memories promoted into PAI Memory.
- Explicit `denied_action_report`.
- Explicit `unsupported_surface_report`.
- Reversible by default with rollback and no-residue proof as future gates.

## Trial Source Model

Future trial source classes:

| Source class | Meaning | S9A status |
| --- | --- | --- |
| `release-fixture` | Future isolated fixture derived from repository-local release evidence. | Designed only; no fixture is created. |
| `sanitized-user-fixture` | Future user-approved sanitized copy of selected user material. | Designed only; no user state is read. |
| `existing-local-v5-read-only` | Future live local PAI v5 read-only source. | Future-only and separately approved; not authorized in S9A. |

S9A can only design `release-fixture` and `sanitized-user-fixture` architecture. Live `existing-local-v5-read-only` remains future-only and requires separate approval.

## Integrated Seam Model

Integrated seams:

- Authority/router.
- Launcher/inference.
- Hook/lifecycle.
- Pulse.
- Memory/ISA.
- Manifest/audit/schema.
- Rollback.
- Unsupported-surface reporting.

| Seam | Source spec | Trial responsibility | Forbidden behavior | Required future proof | S9A status |
| --- | --- | --- | --- | --- | --- |
| Authority seam | `V5_CODEX_AUTHORITY_SEAM_SPEC.md` | Preserve `PAI_SYSTEM_PROMPT.md` as high-authority doctrine and report authority loss. | Demoting doctrine or treating memory as authority. | Authority ordering, conflict, truncation, and no-copy proof. | Designed only. |
| Compact router seam | `V5_CODEX_COMPACT_ROUTER_SPEC.md` | Keep future Codex `AGENTS.md`, if authorized, as a compact router. | Creating root `AGENTS.md` or cloning `CLAUDE.md`. | Router minimality and non-installation proof. | Designed only. |
| Launcher seam | `V5_CODEX_LAUNCHER_SEAM_SPEC.md` | Model engine selection and invocation planning without execution. | Creating a launcher, wrapper, or invoking Codex runtime. | Invocation plan, denied behavior, exit-code, and rollback proof. | Designed only. |
| Inference seam | `V5_CODEX_INFERENCE_SEAM_SPEC.md` | Model request/response envelopes without model calls. | Assuming Claude CLI behavior or silently emulating unsupported surfaces. | Request envelope, response envelope, unsupported-surface proof. | Designed only. |
| Engine profile/capability seam | `V5_CODEX_ENGINE_PROFILE_AND_CAPABILITY_CONTRACT.md` | Classify capabilities before mode eligibility. | Creating an engine profile instance or claiming drop-in capability. | Capability declaration and evidence proof. | Designed only. |
| Hook/lifecycle seam | `V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md` | Map Claude hook behavior to future Codex-native candidates or unsupported reports. | Copying Claude hook files or executing hooks. | Event, payload, order, output, and deny proof. | Designed only. |
| Event/context envelope seam | `V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md` | Carry hook-relevant lifecycle context safely. | Creating event envelope instances or accessing private state. | Envelope field completeness and no-write proof. | Designed only. |
| Hook permission/safety seam | `V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md` | Enforce future denied actions and sandbox posture. | Installing Codex rules, hooks, config, or bypassing approvals. | Denied action, sandbox, permission, and audit proof. | Designed only. |
| Pulse identity seam | `V5_CODEX_PULSE_BRIDGE_IDENTITY_SPEC.md` | Label any future Codex/Pulse activity distinctly. | Impersonating Claude Code, DA identity, or official engine identity. | Bridge identity collision and audit proof. | Designed only. |
| Pulse read-only event seam | `V5_CODEX_PULSE_READ_ONLY_EVENT_MODEL_SPEC.md` | Prove Pulse no-start/no-call posture and classify future events. | Starting Pulse, calling endpoints, probing `localhost:31337`. | No-start, no-call, and event class proof. | Designed only. |
| Pulse observability/audit seam | `V5_CODEX_PULSE_OBSERVABILITY_AND_AUDIT_SPEC.md` | Report Pulse status without creating Pulse state. | Creating audit artifacts or writing Pulse state. | Pulse audit field and non-promotion proof. | Designed only. |
| Memory/ISA single-writer seam | `V5_CODEX_MEMORY_ISA_SINGLE_WRITER_POLICY_SPEC.md` | Keep canonical state writes blocked. | PAI Memory writes, ISA writes, or dual-engine uncoordinated writes. | Single-writer, lock, provenance, rollback, conflict proof. | Designed only. |
| Memory boundary/promotion seam | `V5_CODEX_MEMORY_BOUNDARY_AND_PROMOTION_SPEC.md` | Keep product memories outside PAI Memory. | Silent product-memory promotion. | Source classification, review, provenance, and dedupe proof. | Designed only. |
| ISA workflow/state seam | `V5_CODEX_ISA_WORKFLOW_AND_STATE_POLICY_SPEC.md` | Preserve ISA as the system-of-record primitive. | Treating `/goal`, transcripts, or PRD terminology as ISA. | ISA read/write, changelog, criteria, and ownership proof. | Designed only. |
| Memory/ISA audit/conflict seam | `V5_CODEX_MEMORY_ISA_AUDIT_AND_CONFLICT_SPEC.md` | Report Memory/ISA access, write attempts, conflict, and rollback status. | Creating audit artifacts or canonical state payloads. | Audit fields, conflict classes, and no-promotion proof. | Designed only. |
| Manifest schema seam | `V5_CODEX_TRIAL_MANIFEST_SCHEMA_PROPOSAL.md` | Describe future trial policy fields without creating a manifest. | Creating manifest instances or executable schemas. | Non-executable manifest proposal review and future schema gate. | Designed only. |
| Audit schema seam | `V5_CODEX_TRIAL_AUDIT_SCHEMA_PROPOSAL.md` | Describe future audit fields without creating audit output. | Creating audit artifacts or promoting audit output to PAI state. | Non-executable audit proposal review and future schema gate. | Designed only. |
| Dry-run validation seam | `V5_CODEX_SCHEMA_DRY_RUN_VALIDATION_SPEC.md` | Define future validation ordering before runtime trials. | Running a dry-run or creating validators/harnesses in S9A. | Future dry-run design and no-write proof. | Designed only. |
| Rollback seam | S6/S7C/S8H readiness and rollback sections | Prove no-residue and fallback posture before live work. | Mutating live roots or leaving generated state. | Rollback/no-residue validation. | Designed only. |

## Authority and Router Integration

`PAI_SYSTEM_PROMPT.md` remains high-authority PAI doctrine. `CLAUDE.md` remains an official Claude-facing surface, not a Codex destination file. Future Codex `AGENTS.md`, if later authorized, must be a compact router and must not clone `CLAUDE.md` or `PAI_SYSTEM_PROMPT.md`.

A future read-only fixture trial must prove that the authority seam can reference or envelope doctrine without copying Claude-shaped files directly into Codex surfaces.

## Launcher and Inference Integration

Launcher and inference integration is non-executable in S9A.

A future trial architecture must carry engine selection, request envelope, response envelope, denied tools, unsupported surfaces, output policy, audit policy, and rollback policy without invoking Codex as a runtime engine during S9A.

The future launcher seam and inference seam must report unsupported surfaces rather than silently emulating Claude Code behavior.

## Hook and Lifecycle Integration

Hook lifecycle behavior must be tested only after future approval. S9A does not create Codex hooks, Codex rules, hook payloads, event envelope instances, or lifecycle adapter payloads.

Future fixture-trial architecture must classify hook/lifecycle behavior as mapped, denied, unsupported, or blocked. It must not copy Claude hook files into Codex hook surfaces.

## Pulse Integration Boundary

Pulse is central v5 infrastructure, but S9A does not start Pulse, call Pulse endpoints, probe `localhost:31337`, create a Pulse bridge, create Pulse payloads, or claim Pulse parity.

Future read-only fixture architecture may only prove no-start/no-call behavior and unsupported-surface reporting until an architect-approved Pulse milestone authorizes more.

## Memory and ISA Integration Boundary

PAI Memory and ISA artifacts are canonical PAI state. Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.

Product memories must not be silently promoted into PAI Memory. Future writes require a single-writer policy, provenance, rollback, validation, and conflict handling.

S9A does not authorize PAI Memory writes, ISA writes, existing-local-v5 reads, or controlled single-writer mode.

## Manifest, Audit, and Schema Integration

Manifest, audit, and schema integration is non-executable in S9A.

The future architecture may refer to non-executable manifest schema proposal, non-executable audit schema proposal, and dry-run validation design. It does not create manifest files, manifest instances, audit files, audit artifacts, executable schemas, validators, or harnesses.

## Fixture Isolation Boundary

Future fixture isolation must prove:

- No live user-local state.
- No live `~/.claude/PAI`.
- No live `~/.codex`.
- No release-file mutation.
- No root `AGENTS.md`.
- No `.codex/`.
- No PAI Memory writes.
- No ISA writes.
- No Pulse startup or endpoint calls.
- No generated runtime config.
- No hidden repository residue.

S9A creates no fixture.

## Existing Local v5 Boundary

Existing-local-v5 read-only trial execution is not authorized in S9A.

Future live local work requires separate architect approval, explicit manifest, allowed read roots, denied read roots, denied write roots, privacy review, rollback proof, and no-write proof. It must not require uninstalling Claude Code.

## Dual-Engine Boundary

Future read-only trials must not require uninstalling Claude Code.

Dual-engine uncoordinated writes are prohibited. Future dual-engine coexistence requires explicit engine labels, product memory separation, single-writer ownership for each canonical surface, audit, provenance, rollback, and conflict handling.

## Trial Output Model

S9A creates no trial outputs.

Future trial output may be advisory only and must not be PAI Memory, ISA, Pulse state, Claude memory, or Codex memory. Future outputs must include `denied_action_report`, `unsupported_surface_report`, provenance, rollback status, no-residue status, and non-promotion statement.

## Required Future Proofs

Required future proofs:

- Authority envelope preserves high-authority doctrine.
- Compact router remains non-installable until authorized.
- Launcher plan and inference plan remain non-executable during design phases.
- Hook lifecycle mapping reports unsupported surfaces.
- Pulse no-start and no-call proof exists.
- PAI Memory no-write proof exists.
- ISA no-write proof exists.
- Product memories are not promoted.
- Manifest, audit, and schema artifacts are created only under a future approved write set.
- Rollback/no-residue proof exists.
- No drop-in claim is made before gates pass.

## Prohibited Architecture Designs

Prohibited designs:

- Creating fixtures in S9A.
- Creating a harness in S9A.
- Creating manifest instances in S9A.
- Creating audit artifacts in S9A.
- Creating executable schemas in S9A.
- Creating root `AGENTS.md` or `.codex/`.
- Creating Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, runtime files, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, or trial outputs.
- Running a read-only trial in S9A.
- Reading private user-local state or live existing-local-v5 state.
- Starting Pulse or calling Pulse endpoints.
- Authorizing PAI Memory writes or ISA writes.
- Authorizing product-memory promotion into PAI Memory.
- Authorizing dual-engine uncoordinated writes.
- Claiming Codex is drop-in today.

## Non-Goals

S9A does not implement the adapter, create fixtures, create a test harness, create manifests, create audit artifacts, create executable schemas, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create generated configs, create migration scripts, create runtime files, create adapter payloads, create Memory payloads, create ISA payloads, create Pulse payloads, create trial outputs, run a read-only trial, inspect private user-local state, read live `~/.claude/PAI`, read live `~/.codex`, modify release files, start Pulse, call Pulse endpoints, probe `localhost:31337`, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, run Codex hook/rule/execpolicy commands, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, imply Claude-shaped files can be copied directly into Codex surfaces, authorize product-memory promotion into PAI Memory, authorize dual-engine uncoordinated writes, or advance beyond S9A.
