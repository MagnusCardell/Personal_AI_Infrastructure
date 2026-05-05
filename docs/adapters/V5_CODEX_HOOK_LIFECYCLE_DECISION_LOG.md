# V5 Codex Hook Lifecycle Decision Log

## Purpose

Record S7D decisions, non-decisions, blocked decisions, and future architect questions for hook/lifecycle mapping.

## Scope

This decision log is design-only. It records decisions for future hook, lifecycle, event-context, permission, and safety mapping.

It does not authorize S7B, S7E, S8D, S8E, S8F, runtime implementation, hook creation, rule creation, config creation, event envelope creation, lifecycle adapter creation, adapter payload creation, root `AGENTS.md`, `.codex/`, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, release edits, Pulse startup, installer execution, Claude Code invocation, Codex runtime invocation, Codex hook commands, Codex rule commands, `codex execpolicy check`, Codex import, or migration tooling.

## Evidence Base

Evidence comes from:

- `Releases/v5.0.0/.claude/settings.json`
- `Releases/v5.0.0/.claude/hooks/README.md`
- `Releases/v5.0.0/.claude/hooks/LoadContext.hook.ts`
- `Releases/v5.0.0/.claude/hooks/PromptProcessing.hook.ts`
- `Releases/v5.0.0/.claude/hooks/SecurityPipeline.hook.ts`
- `Releases/v5.0.0/.claude/hooks/SmartApprover.hook.ts`
- `Releases/v5.0.0/.claude/hooks/ISASync.hook.ts`
- `Releases/v5.0.0/.claude/hooks/AgentInvocation.hook.ts`
- `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md`
- `docs/adapters/V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md`

## Decisions Made in S7D

- Codex remains not drop-in today.
- Claude hook files must not be copied into Codex hook surfaces.
- Hook/lifecycle replacement requires explicit mapping and validation.
- Codex hooks and Codex rules are native surfaces, not Claude hook destinations.
- Context loading must respect the S7A authority seam.
- Prompt processing must not silently mutate PAI doctrine.
- Tool and permission behavior requires explicit sandbox and approval policy.
- PAI Memory and ISA writes remain blocked.
- Pulse bridge remains out of S7D scope.
- Root `AGENTS.md` and `.codex/` remain protected.
- S7D creates no hook, rule, config, or runtime material.
- Future hook validation must precede hook/lifecycle parity claims.
- No user-local state is inspected in S7D.
- No Claude Code or Codex runtime invocation occurs in S7D.

## Non-Decisions in S7D

- No Codex hook file format is selected for PAI.
- No Codex rule policy is selected for PAI.
- No Codex config/profile is authored.
- No event envelope instance format is finalized.
- No Pulse bridge is designed.
- No PAI Memory writer is selected.
- No ISA writer or acceptance mechanism is selected.
- No existing-local-v5 trial is approved.
- No hook/lifecycle parity claim is made.

## Blocked Decisions

- Drop-in hook parity is blocked until native hook/rule event, payload, output, permission, sandbox, Memory, ISA, Pulse, and rollback proofs exist.
- Write-capable hook behavior is blocked until single-writer policy, provenance, rollback, and validation exist.
- Pulse event mapping is blocked until a Pulse bridge milestone defines identity and no-start/read-only behavior.
- Codex project config or `.codex/` creation is blocked until architect-approved write scope exists.
- Root `AGENTS.md` remains blocked until a future router milestone explicitly authorizes it.

## Future Architect Questions

- Which hook lifecycle events are required for minimum read-only validation?
- Should unsupported Claude hook events fail closed, degrade to audit-only, or block the trial?
- Which Codex hook/rule facts need a fresh official-doc refresh before implementation design?
- What event envelope evidence is sufficient before fixture replay?
- What sandbox and approval posture is required before a future hook validation harness?
- Which Pulse hook routes require a separate S7E bridge decision?
- What single-writer primitive will protect PAI Memory and ISA in future write-capable hook modes?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S7D-D01 | Codex remains not drop-in today. | Hook/lifecycle, authority, launcher, inference, Pulse, Memory, ISA, and rollback proofs remain unresolved. | S2 compatibility matrix; S6 readiness gates; S7D specs. | Decided for S7D. | G0-G15 pass or receive explicit architect waiver. |
| S7D-D02 | Claude hook files must not be copied into Codex hook surfaces. | Claude hook files encode Claude payloads, settings, command paths, and event semantics. | Release hooks; S2 non-evidence; S6 seam spec. | Decided for S7D. | Future transformation spec and tests. |
| S7D-D03 | Hook/lifecycle replacement requires explicit mapping and validation. | Event overlap is partial and semantics differ. | S2 hooks matrix; hook README; settings evidence. | Decided for S7D. | Hook fixture validation passes. |
| S7D-D04 | Codex hooks and rules are native surfaces, not Claude hook destinations. | S2 records Codex hooks/rules as native Codex surfaces with their own semantics. | S2 native surface evidence. | Decided for S7D. | Official-doc refresh and native mapping spec. |
| S7D-D05 | Context-loading behavior must respect authority seam decisions. | Dynamic context must not override `PAI_SYSTEM_PROMPT.md`. | `LoadContext.hook.ts`; S7A authority seam. | Decided for S7D. | Authority envelope validation passes. |
| S7D-D06 | Prompt-processing behavior must not silently mutate PAI doctrine. | Prompt processing emits contextual output and telemetry, but doctrine must remain high-authority. | `PromptProcessing.hook.ts`; S7A authority validation. | Decided for S7D. | Event/context tests pass. |
| S7D-D07 | Tool/permission behavior requires explicit sandbox and approval policy. | Security and approval hooks depend on Claude tool names and output shapes. | `SecurityPipeline.hook.ts`; `SmartApprover.hook.ts`; settings permissions. | Decided for S7D. | Safety and permission proof passes. |
| S7D-D08 | PAI Memory and ISA writes remain blocked. | PAI Memory and ISA are canonical PAI state. | S1-S7C memory/ISA boundary docs; `ISASync.hook.ts`. | Decided for S7D. | Single-writer, provenance, rollback, and validation are approved. |
| S7D-D09 | Pulse bridge remains out of S7D scope. | Pulse is central v5 infrastructure, but S7D does not design or implement a Pulse bridge. | Hook README Pulse routes; settings HTTP hook allowlist; S6 Pulse seam. | Decided for S7D. | Architect approves S7E or equivalent Pulse milestone. |
| S7D-D10 | Root `AGENTS.md` and `.codex/` remain protected. | S7D does not create router or Codex project config. | S7D contract; S7A router spec. | Decided for S7D. | Future architect-approved router/config milestone. |
| S7D-D11 | S7D creates no hook, rule, config, or runtime material. | This milestone is documentation-only and design-only. | S7D approved write set. | Decided for S7D. | Future implementation milestone with explicit write set. |
| S7D-D12 | Future hook validation must precede any hook/lifecycle parity claim. | Partial event overlap is not parity. | S2/S6/S7D evidence. | Decided for S7D. | Hook validation harness passes. |
| S7D-D13 | No user-local state is inspected in S7D. | Private user-local roots are protected. | S7D source protocol and protected paths. | Decided for S7D. | Future live-root trial receives explicit approval and guards. |
| S7D-D14 | No Claude Code or Codex runtime invocation occurs in S7D. | Runtime invocation would leave design-only scope. | S7D hard failure conditions. | Decided for S7D. | Future approved validation or implementation milestone. |

## Next Milestone Candidates

Advisory-only options, not approvals:

- `V5-S7B`: Fixture-only coupling validation harness design.
- `V5-S7E`: Pulse bridge identity and read-only event model.
- `V5-S8D`: Hook/lifecycle fixture validation design, if S7D is accepted.
- `V5-S8E`: Codex rules and approval policy design, if S7D is accepted.
- `V5-S8F`: Tool/MCP boundary design, if S7D is accepted.

Architect approval is required before any future milestone.

## Non-Goals

S7D does not implement the adapter, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create migration scripts, create runtime files, create adapter payloads, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, run Codex hook commands, run Codex rule commands, run `codex execpolicy check`, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, imply Claude-shaped files can be copied directly into Codex surfaces, propose installing any hook, rule, config, event envelope, or lifecycle adapter, or advance beyond S7D.
