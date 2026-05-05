# V5 Codex Memory and ISA Audit and Conflict Spec

## Purpose

Define future audit, conflict, failure, and rollback requirements for any Codex-related Memory or ISA interaction.

## Scope

This document is design-only. It does not create an audit artifact, write PAI Memory, write ISA, create Memory payloads, create ISA payloads, create runtime files, inspect private user-local state, start Pulse, or call Pulse endpoints.

Audit output is future advisory reporting only, not PAI Memory and not ISA.

## Evidence Base

Evidence comes from:

- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa/IsaSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md`
- `docs/adapters/V5_CODEX_MEMORY_ISA_SINGLE_WRITER_POLICY_SPEC.md`
- `docs/adapters/V5_CODEX_MEMORY_BOUNDARY_AND_PROMOTION_SPEC.md`
- `docs/adapters/V5_CODEX_ISA_WORKFLOW_AND_STATE_POLICY_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_OBSERVABILITY_AND_AUDIT_SPEC.md`
- `docs/adapters/V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md`
- `/tmp/v5-s8h-memory-isa-files.txt`
- `/tmp/v5-s8h-memory-isa-search.txt`

## Audit Problem Statement

Future Codex-related Memory or ISA interaction must be provable. Without explicit audit, a future adapter could silently read private state, promote product memory, create shadow ISA state, write canonical Memory, conflict with Claude Code, mutate Pulse state, or overclaim drop-in readiness.

## Audit Philosophy

Audit must be:

- Advisory by default.
- Separate from PAI Memory.
- Separate from ISA.
- Separate from Pulse.
- Provenance-tagged.
- Conflict-aware.
- Rollback-aware.
- Explicit about denied actions.
- Explicit about unsupported surfaces.

S8H creates no audit artifact.

## Audit Field Model

Required future audit fields:

| Field | Purpose |
| --- | --- |
| `audit_id` | Stable audit identifier. |
| `trial_id` | Future trial identifier or explicit `none`. |
| `engine_id` | Engine identity. |
| `adapter_mode` | Adapter mode such as `documentation-only` or future controlled mode. |
| `source_kind` | Evidence, fixture, sanitized fixture, or future live source. |
| `memory_access_mode` | Memory read/write posture. |
| `isa_access_mode` | ISA read/write posture. |
| `writer_role` | Writer role for canonical state. |
| `single_writer_status` | Whether single-writer ownership is proven. |
| `memory_read_status` | Memory read result or denial. |
| `memory_write_status` | Memory write result or denial. |
| `isa_read_status` | ISA read result or denial. |
| `isa_write_status` | ISA write result or denial. |
| `promotion_status` | Product-memory promotion status. |
| `conflict_status` | Conflict status. |
| `rollback_status` | Rollback readiness. |
| `pulse_action_status` | Pulse action status. |
| `denied_action_report` | Denied actions. |
| `unsupported_surface_report` | Unsupported surfaces. |
| `files_inspected` | Files inspected. |
| `files_not_inspected` | Files intentionally not inspected. |
| `provenance` | Evidence chain. |
| `failure_reason` | Failure reason if any. |
| `non_promotion_statement` | Statement that advisory output is not promoted into canonical or product memory. |

## Memory Access Reporting

Future Memory access reporting must distinguish:

- Static release evidence read.
- Sanitized fixture read.
- Existing-local-v5 read-only access.
- Denied private-state access.
- Denied Memory write.
- Unsupported Memory category.
- Product memory evidence request.
- Promotion request.

S8H reads no private user-local Memory and writes no PAI Memory.

## ISA Access Reporting

Future ISA access reporting must distinguish:

- Release ISA evidence read.
- Sanitized fixture ISA read.
- Existing local ISA read.
- Advisory ISA patch proposal.
- Denied ISA write.
- Denied ISA creation.
- Denied ISA changelog update.
- Unsupported ISA operation.

S8H reads no private user-local ISA and writes no ISA.

## Write Attempt Reporting

Any future write attempt must report:

- Requested writer role.
- Target surface.
- Adapter mode.
- Lock/ownership status.
- Conflict status.
- Denial or approval basis.
- Rollback status.
- Audit ID.

In S8H, all PAI Memory write attempts and ISA write attempts are denied by design.

## Promotion Reporting

Future promotion reporting must include:

- Source surface.
- Target category.
- User approval status.
- Architect approval status.
- Human-review status.
- Provenance.
- Deduplication.
- Conflict check.
- Rollback.
- Non-promotion statement.

Product memories must not be silently promoted into PAI Memory.

## Conflict Detection Model

Future conflict detection must evaluate:

- Existing target content.
- Duplicate Memory candidates.
- Category fit.
- ISA freshness.
- Writer ownership.
- Lock state.
- Provenance.
- Pulse side effects.
- Product-memory leakage.
- Rollback readiness.

Unknown conflict status must fail closed.

## Conflict Classification

Conflict classes:

| Conflict class | Meaning |
| --- | --- |
| `no-conflict` | No conflict detected. |
| `duplicate-memory` | Proposed Memory content duplicates existing Memory. |
| `category-mismatch` | Proposed Memory target category is wrong. |
| `stale-isa` | ISA proposal is based on stale state. |
| `concurrent-writer` | Another writer can write the same canonical surface. |
| `unowned-write` | No approved owner exists. |
| `promotion-without-provenance` | Promotion lacks source and approval chain. |
| `product-memory-leak` | Product memory would enter canonical state silently. |
| `pulse-state-conflict` | Pulse state or event behavior conflicts with Memory/ISA policy. |
| `unknown-conflict` | Evidence is insufficient. |

## Rollback Reporting

Future rollback reporting must include:

- Affected target.
- Prior state reference.
- Reversible patch or snapshot.
- Writer role.
- Conflict class.
- Failure reason.
- Recovery steps.
- Human-readable rollback statement.
- Audit ID.

Rollback must exist before any write-capable mode.

## Pulse Reporting Boundary

Pulse is central v5 infrastructure, but S8H does not design or implement a Pulse bridge.

Future Memory/ISA audit must report `pulse_action_status`. In S8H, Pulse status is `no startup, no endpoint call, no Pulse write, no Pulse payload`.

## Failure Classification

Failure classes:

| Failure class | Meaning |
| --- | --- |
| `private-state-access` | Private user-local state was read or attempted. |
| `memory-write-attempt` | PAI Memory write was attempted without authorization. |
| `isa-write-attempt` | ISA write was attempted without authorization. |
| `single-writer-violation` | More than one writer can write a canonical surface. |
| `promotion-violation` | Product memory promotion was attempted without approval. |
| `rollback-missing` | Rollback is absent or unproven. |
| `pulse-mutation` | Pulse state, event, endpoint, or startup mutation occurred. |
| `drop-in-overclaim` | Codex was claimed drop-in without proof. |
| `unsupported-surface-silence` | Unsupported surface was ignored instead of reported. |

## Advisory Output Model

Future advisory output may report findings, proposed patches, conflicts, and denial reasons, but it is not canonical state.

Advisory output must include:

- Audit fields.
- Denied action report.
- Unsupported surface report.
- Conflict classification.
- Rollback statement.
- Non-promotion statement.

## Non-Promotion Rule

Advisory output must not be promoted into PAI Memory, ISA, Pulse, Claude memory, or Codex memory by default.

Any future promotion requires explicit approval, single-writer ownership, provenance, rollback, validation, and conflict handling.

## Required Future Proofs

Future Memory/ISA audit work must prove:

- Audit fields are complete.
- No private-state access occurs without approval.
- No write occurs in read-only modes.
- Single-writer status is known.
- Conflicts are classified.
- Rollback exists.
- Promotion is opt-in and provenance-tagged.
- Pulse actions are denied or explicitly approved in a later milestone.
- Unsupported surfaces are reported.

## Prohibited Audit Designs

Prohibited designs:

- Creating audit artifacts in S8H.
- Treating audit output as PAI Memory.
- Treating audit output as ISA.
- Writing PAI Memory or ISA from audit.
- Promoting product memory from audit output.
- Hiding conflicts.
- Ignoring rollback.
- Starting Pulse or calling Pulse endpoints.
- Creating runtime audit files, Memory payloads, ISA payloads, or Pulse payloads.

## Non-Goals

S8H does not create audit artifacts, write PAI Memory, write ISA, inspect private user-local state, create Memory payloads, create ISA payloads, create runtime files, start Pulse, call Pulse endpoints, authorize product-memory promotion, authorize dual-engine uncoordinated writes, claim Codex is drop-in today, or claim Codex is the official upstream engine.
