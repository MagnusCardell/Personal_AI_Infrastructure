# V5 Codex Pulse Read-Only Event Model Spec

## Purpose

Define future read-only Pulse event interaction classes, boundaries, and denial rules for Codex replacement work without implementing a Pulse bridge.

## Scope

The read-only Pulse event model is future design only. S7E does not call Pulse endpoints, does not read live Pulse state, does not start Pulse, does not create a Pulse bridge, does not create event payloads, does not create audit artifacts, does not create runtime files, does not create Codex hooks or rules, and does not run a read-only trial.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement is plausible only through a designed adapter. Claude-shaped files must not be copied directly into Codex surfaces.

## Evidence Base

Evidence comes from:

- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Observability/ObservabilitySystem.md`
- `Releases/v5.0.0/.claude/PAI/PULSE/pulse.ts`
- `Releases/v5.0.0/.claude/PAI/PULSE/PULSE.toml.example`
- `Releases/v5.0.0/.claude/PAI/PULSE/modules/hooks.ts`
- `Releases/v5.0.0/.claude/PAI/PULSE/modules/wiki.ts`
- `Releases/v5.0.0/.claude/PAI/PULSE/VoiceServer/voice.ts`
- `Releases/v5.0.0/.claude/PAI/PULSE/Observability/observability.ts`
- `docs/adapters/V5_CODEX_PULSE_BRIDGE_IDENTITY_SPEC.md`
- `docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md`
- `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`
- `/tmp/v5-s7e-pulse-files.txt`
- `/tmp/v5-s7e-pulse-search.txt`

No live Pulse state was read. No Pulse endpoint was called.

## Pulse Event Problem Statement

Pulse is central v5 infrastructure. It is a local daemon and dashboard with observability, hook validation, notification, scheduling, Wiki/Knowledge, and state-reporting responsibilities.

Future Codex replacement work needs a read-only event model because Pulse is neither optional nor safely writable by default. Codex-originated activity must be visible as a Codex adapter candidate without starting Pulse, mutating Pulse state, submitting jobs, writing notifications, or claiming Pulse parity.

S7E designs the model only. It does not authorize existing-local-v5 trial execution.

## Pulse Surface Inventory

Release evidence supports these Pulse surfaces:

| Pulse surface | Release evidence | S7E treatment |
| --- | --- | --- |
| daemon | `PULSE/pulse.ts`, `PulseSystem.md`, launchd plist evidence | Static release evidence only. |
| dashboard | Observability static export and Life Dashboard docs | Static release evidence only. |
| hook execution | `modules/hooks.ts`, settings HTTP hook routes, hook docs | Future bridge hazard; no endpoint calls. |
| observability | `Observability/observability.ts`, `ObservabilitySystem.md` | Static API inventory only. |
| voice/notification | `VoiceServer/voice.ts`, `/notify` routes, Pulse docs | Denied in S7E and read-only posture. |
| scheduling/cron/jobs | `PULSE.toml.example`, `pulse.ts`, checks directory | Denied for mutation or execution in S7E. |
| Wiki/Knowledge API | `modules/wiki.ts`, Observability docs | Static source evidence only; no live API reads. |
| logs/status | `state/state.json` docs, `/api/pulse/health`, logs docs | Static release evidence only; no live state reads. |
| optional integrations | Telegram, iMessage, Performance, Syslog, Worker, Assistant imports and docs | Unknown or future-only unless separately proven. |

The release default port evidence includes `31337`.

## Read-Only Event Principles

Principles:

- Use static repository release evidence in S7E.
- Do not call Pulse endpoints.
- Do not read live Pulse state.
- Do not start Pulse.
- Do not submit Pulse events.
- Do not mutate Pulse jobs, schedules, state, logs, notifications, or dashboard data.
- Label any future Codex event as Codex-adapter-originated.
- Report unsupported surfaces with `unsupported_surface_report`.
- Report denied actions with `denied_action_report`.
- Keep PAI Memory and ISA writes blocked.
- Keep read-only posture reversible.

## Event Classification Model

| Class | Meaning |
| --- | --- |
| `PE-0: No interaction` | Pulse is acknowledged but not touched. |
| `PE-1: Static release evidence` | Pulse files/docs are inspected from repository release only. |
| `PE-2: Future read-only status observation` | A future approved adapter may read status without mutation. |
| `PE-3: Future advisory event proposal` | Adapter may propose an event report but not submit it. |
| `PE-4: Future bridge event` | Adapter may submit clearly labeled bridge events after approval and tests. |
| `PE-5: Prohibited in read-only mode` | Startup, writes, jobs, notifications, scheduling, or state mutation. |
| `PE-6: Unknown / evidence gap` | Evidence is insufficient. |
| `PE-7: Drop-in blocker` | Pulse behavior blocks drop-in claims until mapped and tested. |

## Allowed Read-Only Event Classes

Allowed in S7E:

- `PE-0: No interaction`
- `PE-1: Static release evidence`

Potentially allowed in future approved read-only trials:

- `PE-2: Future read-only status observation`, only after explicit manifest, identity, permission, audit, denial, and rollback policy.
- `PE-3: Future advisory event proposal`, only if the proposal is not submitted to Pulse and remains advisory output.

## Denied Event Classes

Denied in S7E:

- Pulse startup or shutdown.
- Pulse endpoint calls.
- `localhost:31337` probing.
- Pulse write/event submission.
- Job scheduling or mutation.
- Notifications or voice dispatch.
- Dashboard mutation.
- Wiki/Knowledge mutation.
- PAI Memory writes.
- ISA writes.
- Product memory promotion into PAI Memory.
- Unsupported Pulse surfaces silently ignored.

Denied in future read-only mode unless a later milestone changes scope:

- `PE-4: Future bridge event`
- `PE-5: Prohibited in read-only mode`

## Event Envelope Fields

Future Pulse event envelopes must include:

| Field | Purpose |
| --- | --- |
| `event_id` | Stable event identifier. |
| `bridge_id` | Future bridge identity or explicit `none`. |
| `engine_id` | Engine identity. |
| `adapter_mode` | Mode controlling read/write posture. |
| `source_kind` | Evidence source class. |
| `pai_version` | PAI release version. |
| `pai_dir` | Explicit PAI root if future approved. |
| `authority_envelope_id` | Authority envelope reference. |
| `event_source` | Future event source class. |
| `event_actor` | Actor label. |
| `pulse_surface` | Pulse surface involved. |
| `pulse_interaction_class` | `PE-*` class. |
| `allowed_in_mode` | Yes/no with rationale. |
| `denied_actions` | Denied action list. |
| `unsupported_surfaces` | Unsupported surface list. |
| `audit_policy` | Audit requirements. |
| `rollback_policy` | Reversibility requirements. |
| `provenance` | Evidence chain. |

Minimum Pulse event model rows:

| Event ID | Pulse surface | Proposed interaction class | Allowed in S7E? | Allowed in future read-only trial? | Main hazard | Required future proof | S7E decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PEV-001 | Pulse daemon status | `PE-2: Future read-only status observation` | No live interaction; static release evidence only. | Candidate only after manifest and no-call/no-write policy. | Status observation can become startup or endpoint probing. | No-start proof, endpoint classification, audit policy, rollback proof. | Design only; no daemon status read. |
| PEV-002 | Life Dashboard availability | `PE-2: Future read-only status observation` | No live interaction; static release evidence only. | Candidate only after dashboard route classification. | Dashboard availability checks can probe `31337` or imply parity. | No-probe proof, dashboard route inventory, unsupported-surface reporting. | Design only; no dashboard call. |
| PEV-003 | Hook execution event | `PE-5: Prohibited in read-only mode` plus `PE-7: Drop-in blocker` | No. | No, unless a later hook/Pulse bridge milestone authorizes it. | Hook execution can mutate context, permissions, Memory, ISA, or Pulse state. | Hook mapping tests, bridge identity, no-write proof. | Denied in S7E. |
| PEV-004 | Tool activity/observability event | `PE-3: Future advisory event proposal` | No live event; static release evidence only. | Candidate as advisory output only before submission. | Tool activity can be mistaken for canonical observability state. | Advisory labeling, non-promotion proof, audit proof. | Design only; no event submission. |
| PEV-005 | Voice notification event | `PE-5: Prohibited in read-only mode` | No. | No in read-only mode. | Voice or notification dispatch is a side effect. | Notification denial proof and user-consent policy for future modes. | Denied in S7E. |
| PEV-006 | Scheduling/cron/job event | `PE-5: Prohibited in read-only mode` plus `PE-7: Drop-in blocker` | No. | No in read-only mode. | Jobs can run commands, call Claude, dispatch notifications, and write state. | Job identity, scheduler denial, no-execution proof, rollback proof. | Denied in S7E. |
| PEV-007 | Wiki/Knowledge API read | `PE-2: Future read-only status observation` | No live API read; static source evidence only. | Candidate only after route-level read/write classification. | Some Wiki/Knowledge routes are mutation-capable. | Method inventory, read-only proof, private-state policy. | Design only; no API call. |
| PEV-008 | Pulse log/status observation | `PE-2: Future read-only status observation` | No live state read; static release evidence only. | Candidate only after manifest and denied-write controls. | Logs/status can expose private state or become endpoint probes. | Privacy review, allowed root proof, no-endpoint-call proof. | Design only. |
| PEV-009 | Pulse write/event submission | `PE-5: Prohibited in read-only mode` | No. | No in read-only mode. | Writes mutate Pulse state and can create false parity. | Single-writer policy, bridge identity, mutation tests, rollback. | Denied in S7E. |
| PEV-010 | Pulse startup/shutdown | `PE-5: Prohibited in read-only mode` | No. | No in read-only mode. | Startup changes process state and can execute jobs/modules. | No-start proof and process-state audit. | Denied in S7E. |
| PEV-011 | Pulse bridge identity event | `PE-3: Future advisory event proposal` or `PE-4: Future bridge event` after approval | No live event. | Advisory-only candidate first; live bridge event requires later approval. | Identity confusion with Claude Code, DA, or official engine. | Bridge identity tests, collision tests, audit proof. | Design only; no bridge event. |
| PEV-012 | Pulse failure/crash report | `PE-2: Future read-only status observation` | No live state read. | Candidate only after safe status source is approved. | Failure checks can probe daemon or read private logs. | Safe source policy, privacy review, no-probe proof. | Design only. |
| PEV-013 | Memory/ISA-related Pulse event | `PE-5: Prohibited in read-only mode` plus `PE-7: Drop-in blocker` | No. | No write-capable behavior in read-only mode. | Event handling can write PAI Memory, ISA, or work state. | Single-writer policy, no-write proof, non-promotion proof. | Denied in S7E. |
| PEV-014 | Pulse optional integration event | `PE-6: Unknown / evidence gap` | No. | Unknown until each integration is inventoried and classified. | Telegram, iMessage, syslog, performance, worker, or DA behavior may have side effects. | Per-integration inventory, privacy review, denial policy. | Unknown / not confirmed for interaction. |
| PEV-015 | Unsupported Pulse surface | `PE-6: Unknown / evidence gap` plus `PE-7: Drop-in blocker` | No. | No unless explicitly classified. | Silent ignore or silent emulation can overclaim Pulse parity. | Unsupported-surface reporting and architect review. | Must report, not emulate. |

## Hook and Lifecycle Event Boundary

Release evidence includes Pulse hook guard routes such as `/hooks/skill-guard` and `/hooks/agent-guard`. S7D records these as bridge-required and prohibited in read-only mode.

Future Codex hook/lifecycle mapping must not call Pulse hook routes by default. It must not treat Codex hooks or rules as Claude hook destinations. It must preserve `PAI_SYSTEM_PROMPT.md` as high-authority doctrine, keep `CLAUDE.md` Claude-facing, and keep future `AGENTS.md` as a compact router only if later authorized.

## Launcher and Inference Event Boundary

S7C records that future launchers must not start Pulse, call Pulse endpoints, emit Pulse events, or claim Pulse parity unless a later Pulse milestone authorizes it.

Future inference must not report Codex output as a Pulse event unless a bridge identity, audit policy, read-only/write policy, and unsupported-surface report are approved.

## Memory and ISA Event Boundary

PAI Memory and ISA artifacts are canonical PAI state. Future Pulse event handling must not write PAI Memory or ISA in read-only mode.

Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory. Product memories must not be silently promoted into PAI Memory.

Any future write-capable Pulse event path requires a single-writer policy, provenance, rollback, and validation.

## Dashboard and Observability Boundary

Release evidence shows the dashboard and observability module serve local pages and APIs through Pulse on port `31337`.

S7E only inventories these surfaces from repository-local release evidence. It does not read live dashboard state, does not call `/api/events/recent`, does not call `/api/pulse/health`, and does not create audit artifacts.

Future read-only observation must report files inspected, files not inspected, endpoint-call status, unsupported surfaces, denied actions, and rollback posture.

## Scheduling and Job Boundary

Release evidence shows Pulse jobs can be scheduled through `PULSE.toml`, can be script or Claude jobs, and can dispatch output. Future Codex work must not overload Claude job identity for Codex.

Read-only posture denies:

- Job creation.
- Job mutation.
- Job execution.
- Schedule changes.
- Startup or shutdown.
- State writes.
- Notification dispatch.

## Voice and Notification Boundary

Release evidence includes voice and notification routes and ElevenLabs-related voice behavior. S7E does not call `/notify`, does not trigger voice, and does not write voice events.

Future Codex advisory output must not become a voice notification unless a later Pulse milestone authorizes identity, permission, user consent, audit, and rollback.

## Wiki and Knowledge API Boundary

Release evidence includes Wiki and Knowledge API routes. Some routes are reads and some routes are writes.

S7E does not call live Wiki/Knowledge APIs. Future read-only trials may only consider read-only Wiki/Knowledge observation after route classification proves no mutation, no private-state access, no PAI Memory write, and no ISA write.

## Candidate Read-Only Event Designs

| Candidate | Summary | Inputs | Outputs | Safety | Reversibility | Drop-in readiness | Main risk | Required future proofs | S7E decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PE-Design-1 | Documentation-only read-only event contract. | S7E specs, release Pulse evidence, S7D event envelope design. | Event classes, denied classes, and future field model. | Safe because no Pulse interaction occurs. | Fully reversible; docs only. | Prerequisite design only. | Too abstract without fixture evidence. | Architect review, event class completeness, no-start/no-call proof. | Design candidate only; no runtime implementation chosen. |
| PE-Design-2 | Future manifest-mediated read-only status observation. | Approved manifest, bridge identity, allowed endpoint inventory, audit policy. | Future status observation plan and denied-action report. | Safer because allowed reads and denied writes are explicit. | Reversible if outputs stay quarantined and advisory. | Candidate for future read-only validation. | Endpoint classification mistake could mutate state. | Endpoint method proof, no-write proof, no-private-state proof, rollback. | Deferred; no runtime implementation chosen. |
| PE-Design-3 | Future bridge event proposal without submission. | Future event envelope, authority envelope, event source, audit policy. | Advisory event report that is not submitted to Pulse. | Safer than live submission because Pulse remains untouched. | Reversible because it is advisory only. | Candidate for later bridge rehearsal. | Advisory output may be mistaken for Pulse state. | Non-promotion proof, audit proof, UI/report labeling tests. | Deferred; no runtime implementation chosen. |

## Required Future Proofs

Future Pulse event work must prove:

- Pulse is not started during read-only modes.
- Pulse endpoints are not called unless explicitly approved.
- Allowed read-only observations cannot mutate state.
- Endpoint method classes are known and tested.
- Codex-originated events have bridge identity and engine identity.
- Unsupported surfaces produce `unsupported_surface_report`.
- Denied actions produce `denied_action_report`.
- PAI Memory and ISA writes are blocked.
- Product memories are not promoted into PAI Memory.
- Rollback and reversible posture are preserved.

## Prohibited Event Designs

Prohibited designs:

- Creating a Pulse bridge in S7E.
- Calling Pulse endpoints in S7E.
- Reading live Pulse state in S7E.
- Starting Pulse or probing `localhost:31337`.
- Submitting Pulse events during read-only posture.
- Mutating jobs, schedules, dashboard state, Wiki/Knowledge content, logs, notifications, PAI Memory, ISA, or Pulse state.
- Treating unsupported Pulse surfaces as successful parity.
- Copying Claude-shaped files directly into Codex surfaces.
- Creating root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, event payloads, runtime files, adapter payloads, or Pulse payloads.

## Non-Goals

S7E does not implement a Pulse bridge, start Pulse, call Pulse endpoints, read live Pulse state, create event payloads, create audit artifacts, create runtime files, create fixtures, create harnesses, create Codex hooks, create Codex rules, authorize PAI Memory writes, authorize ISA writes, authorize Pulse startup, authorize Pulse endpoint calls, authorize Pulse implementation, authorize existing-local-v5 trial execution, claim Pulse parity, claim Codex is drop-in today, or claim Codex is the official upstream engine.
