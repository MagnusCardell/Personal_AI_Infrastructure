# V5 Codex Event Context Envelope Spec

## Purpose

Define the future event/context envelope needed to translate hook-relevant lifecycle signals into safe, auditable Codex-native behavior.

## Scope

The event/context envelope is a future design artifact, not an implementation.

S7D creates no event envelope instance. S7D does not create Codex config, hooks, rules, generated config, runtime files, adapter payloads, manifests, audit artifacts, fixtures, harnesses, or lifecycle adapters.

## Evidence Base

Evidence comes from:

- `Releases/v5.0.0/.claude/settings.json`
- `Releases/v5.0.0/.claude/hooks/README.md`
- `Releases/v5.0.0/.claude/hooks/lib/hook-io.ts`
- `Releases/v5.0.0/.claude/hooks/LoadContext.hook.ts`
- `Releases/v5.0.0/.claude/hooks/PromptProcessing.hook.ts`
- `Releases/v5.0.0/.claude/hooks/SecurityPipeline.hook.ts`
- `Releases/v5.0.0/.claude/hooks/SmartApprover.hook.ts`
- `Releases/v5.0.0/.claude/hooks/ToolActivityTracker.hook.ts`
- `Releases/v5.0.0/.claude/hooks/ISASync.hook.ts`
- `Releases/v5.0.0/.claude/hooks/AgentInvocation.hook.ts`
- `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`

No new Codex capability claim is introduced in S7D. Codex hooks, Codex rules, config, sandbox, and approval facts are inherited from S2 official-source evidence.

## Envelope Problem Statement

Codex is not currently proven drop-in for existing local PAI v5 files.

Claude hooks rely on event names, JSON payloads, stdout shapes, process exits, command hooks, HTTP hook routes, and timeout/async settings that are not automatically equivalent to Codex-native hook or rule behavior.

Codex replacement is plausible only through a designed adapter. The future event/context envelope is the proposed neutral contract for event facts, context sources, policies, denied actions, unsupported surfaces, and provenance.

## Event Source Model

Future event source classes:

- `codex-session`
- `codex-user-prompt`
- `codex-tool-request`
- `codex-tool-result`
- `codex-permission-request`
- `codex-stop`
- `pai-runtime`
- `pulse-event`
- `unknown`

`pulse-event` is a future source class only. S7D does not start Pulse, write Pulse state, call Pulse endpoints, or claim Pulse parity.

## Event Type Model

Future event type classes:

- `context-load`
- `prompt-process`
- `permission-check`
- `pre-tool-observe`
- `post-tool-observe`
- `audit-only`
- `unsupported`
- `prohibited`

Unsupported and prohibited events must be reported explicitly rather than silently allowed.

## Context Input Model

Required future envelope fields:

| Field | Purpose |
| --- | --- |
| `event_id` | Stable event identifier. |
| `engine_id` | Runtime engine identity. |
| `adapter_mode` | Mode such as documentation-only, fixture-read-only, or future controlled mode. |
| `event_source` | Source class for the event. |
| `event_type` | Event type class. |
| `lifecycle_phase` | Lifecycle phase being mapped. |
| `pai_dir` | Explicit PAI root, never inferred from private user-local state without approval. |
| `authority_envelope_id` | Reference to approved authority context. |
| `context_sources` | Allowlisted context sources. |
| `tool_context` | Tool request/result facts, if applicable. |
| `filesystem_policy` | Allowed and denied filesystem posture. |
| `sandbox_policy` | Codex sandbox posture or future equivalent. |
| `permission_policy` | Approval/denial posture. |
| `memory_policy` | PAI Memory and product memory policy. |
| `isa_policy` | ISA read/write/acceptance policy. |
| `pulse_policy` | Pulse no-start/no-call/no-write or future bridge policy. |
| `output_policy` | Allowed advisory outputs. |
| `audit_policy` | Required audit and retention behavior. |
| `unsupported_surfaces` | Unsupported event, payload, or output fields. |
| `denied_actions` | Actions denied by policy. |
| `provenance` | Source, timestamp, and evidence lineage. |

## Authority Context Boundary

`PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.

`CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.

Future Codex `AGENTS.md`, if later authorized, must be a compact router and must not clone `CLAUDE.md` or `PAI_SYSTEM_PROMPT.md`.

Context fields in the event/context envelope must not override PAI doctrine. Product memories, transcripts, SDK threads, Codex memory, Claude Code auto memory, and `/goal` state are not PAI Memory and are not doctrine.

## Tool Event Boundary

Tool event fields must distinguish:

- Tool request.
- Permission request.
- Tool result.
- Tool failure.
- Pre-tool observation.
- Post-tool observation.
- Denied action.
- Unsupported surface.
- Advisory audit.

Future mapping must not silently emulate Claude tool names, Claude matchers, or Claude hook output fields.

## Filesystem Event Boundary

Filesystem policy must identify allowed reads, denied reads, denied writes, release roots, root `AGENTS.md`, `.codex/`, `.claude/`, PAI Memory, ISA artifacts, Pulse state, generated configs, hook/rule destinations, and user-local private roots.

Read-only mode must deny all writes.

## Memory and ISA Event Boundary

PAI Memory and ISA writes are prohibited in read-only mode.

PAI Memory and ISA artifacts are canonical PAI state. Any future write-capable behavior requires single-writer policy, provenance, rollback, and validation.

Product memory must not be injected as authority or promoted into PAI Memory. Hook-generated advisory output must not become PAI Memory or ISA by default.

## Pulse Event Boundary

Pulse remains central v5 infrastructure, but S7D does not design or implement a Pulse bridge.

Pulse startup, Pulse writes, Pulse endpoint calls, and Pulse parity claims are prohibited in S7D.

Future Pulse event handling requires a later architect-approved Pulse milestone.

## Output and Audit Model

Future event/context envelope output must include:

- Accepted event fields.
- Rejected event fields.
- `unsupported_surface_report`.
- `denied_action_report`.
- Policy decisions.
- Audit classification.
- Provenance.
- Failure reason, if any.

Outputs are advisory unless a future milestone explicitly grants write authority under single-writer policy.

## Unsupported Event Reporting

Unsupported event reporting is mandatory.

Unsupported reports must include:

- Unsupported lifecycle phase.
- Unsupported payload field.
- Unsupported output field.
- Unsupported tool or MCP behavior.
- Unsupported permission behavior.
- Unsupported Pulse behavior.
- Unsupported Memory or ISA behavior.
- S7D decision.

## Candidate Envelope Designs

| Candidate | Summary | Inputs | Outputs | Safety | Reversibility | Drop-in readiness | Main risk | Required future proofs | S7D decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EC-1 | Documentation-only event/context envelope contract. | S7D specs, S2 Codex surface evidence, release hook evidence. | Future field contract and unsupported-event list. | Safe because it creates no runtime artifact. | Fully reversible; docs only. | Prerequisite design only. | Too abstract without fixture replay. | Field completeness, review approval, no-write proof. | Design candidate only; no runtime implementation chosen. |
| EC-2 | Future manifest-mediated event/context envelope. | Approved manifest, source kind, authority envelope, hook event inventory. | Non-executable envelope instances for future fixture/read-only validation. | Safer because roots and policies are explicit. | Reversible if generated outputs stay quarantined and non-runtime. | Candidate for fixture validation. | Manifest drift or path misbinding. | Manifest validation, denied-path proof, no-write proof. | Deferred; no runtime implementation chosen. |
| EC-3 | Future Codex hook dispatcher envelope. | Future Codex hook/rule spec, native hook events, adapter policy. | Runtime dispatcher contract and audit envelope. | Highest risk because it approaches implementation. | Requires rollback and fallback proof before use. | Candidate for later replacement-capable mode. | Dispatcher could become an unreviewed adapter. | Native hook tests, sandbox/approval proof, Memory/ISA/Pulse proof, rollback. | Deferred; no runtime implementation chosen. |

S7D chooses no runtime implementation for `EC-1`, `EC-2`, or `EC-3`.

## Required Future Proofs

Future event/context work must prove:

- Every required field is present or explicitly denied.
- Event source and event type classes are validated.
- Unsupported events are reported.
- Context cannot override authority.
- Tool payloads are bounded.
- Filesystem policy denies protected writes.
- PAI Memory and ISA writes are blocked in read-only mode.
- Pulse startup and Pulse endpoint calls are blocked in S7D posture.
- Product memories are not promoted into PAI Memory.
- Audit and provenance are complete.
- Rollback and reversibility are preserved.

## Prohibited Envelope Designs

Prohibited designs:

- Creating an event envelope instance in S7D.
- Installing an event envelope.
- Copying Claude hook payloads directly into Codex hooks.
- Copying Claude hook files into Codex hook surfaces.
- Treating Codex hooks/rules as complete replacements before validation.
- Using product memory as authority.
- Writing PAI Memory or ISA in read-only mode.
- Starting Pulse or claiming Pulse parity in S7D.
- Creating root `AGENTS.md` or `.codex/`.
- Creating runtime files or adapter payloads.

## Non-Goals

S7D does not implement an event/context envelope, create an event envelope instance, create Codex config, create hooks, create rules, create generated configs, create runtime files, create adapter payloads, create manifests, create audit artifacts, create fixtures, create harnesses, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex hook commands, run Codex rule commands, run `codex execpolicy check`, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, or advance beyond S7D.
