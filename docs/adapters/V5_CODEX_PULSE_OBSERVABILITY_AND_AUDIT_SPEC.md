# V5 Codex Pulse Observability and Audit Spec

## Purpose

Define future observability, audit, provenance, denied-action reporting, and failure handling for any Codex/Pulse interaction.

## Scope

S7E defines future advisory reporting only. It does not create an audit artifact, does not create a Pulse bridge, does not start Pulse, does not call Pulse endpoints, does not create runtime files, does not create Pulse payloads, and does not run a read-only trial.

Audit output is future advisory reporting only. It is not Pulse state, not PAI Memory, not ISA, not Claude memory, and not Codex memory.

## Evidence Base

Evidence comes from:

- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Observability/ObservabilitySystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md`
- `Releases/v5.0.0/.claude/PAI/PULSE/Observability/observability.ts`
- `Releases/v5.0.0/.claude/PAI/PULSE/pulse.ts`
- `Releases/v5.0.0/.claude/PAI/PULSE/modules/wiki.ts`
- `Releases/v5.0.0/.claude/PAI/PULSE/modules/hooks.ts`
- `docs/adapters/V5_CODEX_PULSE_BRIDGE_IDENTITY_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_READ_ONLY_EVENT_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_OUTPUT_SPEC.md`
- `docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md`
- `/tmp/v5-s7e-pulse-files.txt`
- `/tmp/v5-s7e-pulse-search.txt`

No live observability endpoint was called. No `localhost:31337` probe was run.

## Observability Problem Statement

Pulse observability is an active release surface: it reads local JSONL sources, serves dashboard pages, exposes APIs, reports sessions and events, and includes security and Wiki/Knowledge routes. Some surfaces are read-like, while others are mutation-capable.

Future Codex/Pulse work needs observability and audit boundaries that prevent silent endpoint calls, silent writes, identity confusion, product-memory promotion, and Pulse parity overclaims.

S7E cannot mark Pulse parity as proven.

## Audit Philosophy

Audit output must be:

- Advisory by default.
- Provenance-tagged.
- Explicit about no-start, no-call, and no-write posture.
- Explicit about unsupported surfaces.
- Explicit about denied actions.
- Separate from PAI Memory, ISA, Pulse state, Claude memory, Codex memory, transcripts, SDK threads, and `/goal` state.
- Reversible and reviewable.

Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Provenance Requirements

Future provenance must record:

- Evidence source.
- PAI version.
- Engine identity.
- Bridge identity.
- Adapter mode.
- Authority envelope reference.
- Pulse surface involved.
- Whether interaction was static release evidence, future observation, advisory proposal, or denied.
- Files inspected.
- Files not inspected.
- Denied actions.
- Unsupported surfaces.
- Reviewer or architect approval lineage.

## Read-Only Observation Reporting

Future read-only observation reporting must distinguish:

| Observation class | Required report |
| --- | --- |
| Static release evidence | Files inspected, no live state, no endpoint calls. |
| Future status observation | Approved endpoint, method, identity, no-write proof, rollback statement. |
| Advisory event proposal | Event proposal label, no Pulse submission, non-promotion statement. |
| Denied interaction | Denial reason, protected policy, failure class. |
| Unsupported surface | `unsupported_surface_report`, evidence gap, future proof needed. |

S7E permits only static release evidence and design discussion.

## Denied Action Reporting

Any future report must include `denied_action_report` for attempted or requested actions that policy forbids.

Denied Pulse actions include:

- Pulse startup.
- Pulse endpoint call.
- `localhost:31337` probe.
- Pulse write/event submission.
- Pulse job creation or mutation.
- Pulse notification or voice dispatch.
- Pulse state write.
- Dashboard mutation.
- Wiki/Knowledge mutation.
- PAI Memory write.
- ISA write.
- Private user-local state access.
- Product memory promotion into PAI Memory.
- Unsupported Pulse behavior silently allowed.

## Unsupported Surface Reporting

Any future Pulse observation must report unsupported surfaces rather than silently ignoring them.

`unsupported_surface_report` must include:

- Pulse surface name.
- Evidence source.
- Missing proof.
- Risk class.
- Whether the gap blocks drop-in claims.
- Required future milestone or architect decision.

Unsupported surfaces must not be hidden behind a generic success result.

## Pulse Startup and Call Reporting

Future audit fields must explicitly report:

- `pulse_startup_status`
- `pulse_endpoint_call_status`
- `pulse_write_status`
- `pulse_job_status`
- `pulse_notification_status`

For S7E, each status is `not performed by design`.

Future read-only trials must fail closed if startup, endpoint calls, jobs, notifications, or writes occur outside explicit approval.

## Memory and ISA Reporting

Future audit must report:

- `pulse_memory_isa_event_status`
- PAI Memory write status.
- ISA write status.
- Product memory handling.
- `/goal` boundary.
- Non-promotion status.
- Single-writer status for any future write-capable mode.

PAI Memory and ISA artifacts are canonical PAI state. Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory. Product memories must not be silently promoted into PAI Memory.

## Dashboard and Status Reporting

Future dashboard/status reporting must identify:

- Whether the dashboard was merely described from release evidence or queried live.
- Whether `/api/pulse/health`, `/api/events/recent`, `/api/observability/*`, `/api/wiki/*`, or other endpoints were called.
- Whether any endpoint was read-only, write-capable, or unknown.
- Whether `31337` was contacted.
- Whether dashboard output was advisory or Pulse state.

S7E performs no live dashboard/status calls.

## Failure Classification

Required future failure classes:

| Failure class | Meaning |
| --- | --- |
| `pulse-startup-attempt` | Pulse was started or startup was attempted without approval. |
| `pulse-endpoint-call` | A Pulse endpoint was called without approval. |
| `pulse-write-attempt` | Pulse state, event, dashboard, Wiki, or observability write was attempted. |
| `pulse-job-mutation` | Pulse job, schedule, or automation state was changed or attempted. |
| `pulse-notification-attempt` | Voice, notification, Telegram, iMessage, or push dispatch was attempted. |
| `pulse-identity-confusion` | Codex event identity was confused with Claude Code, DA, or official engine identity. |
| `memory-isa-mutation` | PAI Memory or ISA write was attempted. |
| `private-state-access` | Private user-local state was accessed without approval. |
| `drop-in-overclaim` | Codex or Pulse parity was claimed without required proof. |
| `unsupported-surface-silence` | Unsupported Pulse behavior was ignored instead of reported. |

## Advisory Output Model

Future advisory output must include:

| Output field | Purpose |
| --- | --- |
| `audit_id` | Stable audit identifier. |
| `trial_id` | Future trial identifier or explicit `none`. |
| `engine_id` | Engine identity. |
| `bridge_id` | Bridge identity or explicit `none`. |
| `adapter_mode` | Mode controlling permissions. |
| `source_kind` | Evidence or future trial source class. |
| `pulse_interaction_mode` | Static evidence, future observation, advisory proposal, denied, or unsupported. |
| `pulse_startup_status` | Startup status. |
| `pulse_endpoint_call_status` | Endpoint-call status. |
| `pulse_write_status` | Pulse write status. |
| `pulse_job_status` | Job or schedule status. |
| `pulse_notification_status` | Voice/notification status. |
| `pulse_memory_isa_event_status` | Memory/ISA-related Pulse event status. |
| `denied_action_report` | Denied actions. |
| `unsupported_surface_report` | Unsupported surfaces. |
| `files_inspected` | Static or future approved files inspected. |
| `files_not_inspected` | Denied, private, live, or unapproved files not inspected. |
| `provenance` | Evidence chain. |
| `failure_reason` | Failure reason if any. |
| `rollback_statement` | Reversibility status. |
| `non_promotion_statement` | Statement that advisory output is not promoted into canonical or product memory. |

S7E creates no audit artifact.

## Non-Promotion Rule

Advisory output must not be promoted into PAI Memory, ISA, Pulse, Claude memory, or Codex memory by default.

Any future promotion requires explicit architect approval, user consent where applicable, single-writer policy, provenance, rollback, and validation.

## Required Future Proofs

Future Pulse observability and audit work must prove:

- Pulse startup did not occur unless explicitly authorized.
- Pulse endpoint calls did not occur unless explicitly authorized.
- Read-only observations cannot write state.
- Mutation-capable endpoints are denied in read-only posture.
- Codex identity is explicit and not confused with Claude Code or DA identity.
- `denied_action_report` is complete.
- `unsupported_surface_report` is complete.
- PAI Memory and ISA writes are blocked.
- Advisory output is not promoted into PAI Memory, ISA, Pulse, Claude memory, or Codex memory.
- Rollback is defined and tested.

## Prohibited Audit Designs

Prohibited designs:

- Creating audit artifacts in S7E.
- Treating audit output as Pulse state.
- Treating advisory output as PAI Memory or ISA.
- Calling Pulse endpoints to populate audit.
- Probing `localhost:31337`.
- Starting Pulse.
- Writing Pulse state, jobs, notifications, dashboard data, Wiki/Knowledge content, PAI Memory, or ISA.
- Claiming Pulse parity or Codex drop-in status without proof.
- Copying Claude-shaped files directly into Codex surfaces.

## Non-Goals

S7E does not create an audit artifact, implement a Pulse bridge, start Pulse, call Pulse endpoints, probe `localhost:31337`, write Pulse state, write PAI Memory, write ISA, create event payloads, create runtime files, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, run a trial, inspect private user-local state, authorize Pulse implementation, authorize existing-local-v5 trial execution, claim Codex is drop-in today, or claim Codex is the official upstream engine.
