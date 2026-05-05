# V5 Codex Hook Lifecycle Mapping Spec

## Purpose

Define the future mapping between PAI v5 Claude-shaped hooks/lifecycle behavior and Codex-native hook/rule/control surfaces without copying Claude hook files or implementing Codex hooks.

## Scope

Hook lifecycle mapping is a future adapter design problem, not an implementation.

S7D designs hook, lifecycle, event-context, permission, and safety mappings only. It does not implement hook or lifecycle mapping, create Codex hooks, create Codex rules, create Codex config, create root `AGENTS.md`, create `.codex/`, create runtime files, execute hooks, run Codex hook commands, run Codex rule commands, run `codex execpolicy check`, inspect private user-local state, start Pulse, invoke Claude Code, or invoke Codex as a runtime engine.

Claude hook files must not be copied into Codex hook files. Claude-shaped hook files must not be copied directly into Codex hook surfaces. Claude-shaped files must not be copied directly into Codex surfaces.

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
- `Releases/v5.0.0/.claude/hooks/ToolActivityTracker.hook.ts`
- `Releases/v5.0.0/.claude/hooks/WorkCompletionLearning.hook.ts`
- `Releases/v5.0.0/.claude/hooks/VoiceCompletion.hook.ts`
- `Releases/v5.0.0/.claude/hooks/lib/hook-io.ts`
- `/tmp/v5-s7d-hook-files.txt`
- `/tmp/v5-s7d-hook-lifecycle-search.txt`
- `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`

No new Codex capability claim is introduced in S7D. Codex hooks, Codex rules, config, sandbox, and approval facts are inherited from S2 official-source evidence.

## Hook Problem Statement

Codex is not currently proven drop-in for existing local PAI v5 files.

PAI v5 hook behavior is Claude Code-native. The release hook layer depends on Claude lifecycle event names, Claude settings registration, Claude hook payload shapes, Claude tool names, Claude permission semantics, and Claude-specific stdout/stderr/exit-code behavior.

Codex replacement is plausible only through a designed adapter. Hook lifecycle mapping must preserve PAI intent through native Codex surfaces and explicit unsupported-surface reporting, not by running Claude hooks under Codex or translating files by shape.

Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Existing Claude Hook Inventory

The release contains a large Claude hook payload under `Releases/v5.0.0/.claude/hooks/`.

Observed top-level hook files include:

- `AgentInvocation.hook.ts`
- `CheckpointPerISC.hook.ts`
- `ConfigAudit.hook.ts`
- `ContainmentGuard.hook.ts`
- `ContentScanner.hook.ts`
- `ContextReduction.hook.sh`
- `DocIntegrity.hook.ts`
- `ElicitationHandler.hook.ts`
- `FileChanged.hook.ts`
- `ISASync.hook.ts`
- `InstructionsLoadedHandler.hook.ts`
- `IntegrityCheck.hook.ts`
- `KVSync.hook.ts`
- `KittyEnvPersist.hook.ts`
- `LastResponseCache.hook.ts`
- `LoadContext.hook.ts`
- `PreCompact.hook.ts`
- `PromptGuard.hook.ts`
- `PromptProcessing.hook.ts`
- `QuestionAnswered.hook.ts`
- `RelationshipMemory.hook.ts`
- `RepeatDetection.hook.ts`
- `ResponseTabReset.hook.ts`
- `RestoreContext.hook.ts`
- `SatisfactionCapture.hook.ts`
- `SecurityPipeline.hook.ts`
- `SessionCleanup.hook.ts`
- `SetQuestionTab.hook.ts`
- `SmartApprover.hook.ts`
- `StopFailureHandler.hook.ts`
- `TaskGovernance.hook.ts`
- `TeammateIdle.hook.ts`
- `TelosSummarySync.hook.ts`
- `ToolActivityTracker.hook.ts`
- `ToolFailureTracker.hook.ts`
- `UpdateCounts.hook.ts`
- `VoiceCompletion.hook.ts`
- `WorkCompletionLearning.hook.ts`

Observed shared hook support includes handlers, security inspectors, path utilities, learning utilities, ISA utilities, observability transport, and stdin helpers.

Observed `settings.json` registrations include:

| Claude lifecycle event | Evidence | Representative behavior |
| --- | --- | --- |
| `PreToolUse` | `settings.json` | Security pipeline, context reduction, tab changes, Pulse HTTP guard routes for `Skill` and `Agent`. |
| `PostToolUse` | `settings.json` | Question reset, Telos sync, tool activity tracking, content scanning. |
| `PreCompact` | `settings.json` | Pre-compact hook. |
| `SessionEnd` | `settings.json` | Work completion learning, cleanup, relationship memory, counts, integrity check, KV sync. |
| `UserPromptSubmit` | `settings.json` | Prompt guard, repeat detection, prompt processing, satisfaction capture. |
| `SessionStart` | `settings.json` | Kitty env persistence, dynamic context loading, KV sync. |
| `Stop` | `settings.json` | Last response cache, tab reset, voice completion, doc integrity. |
| `PermissionRequest` | hook README and `SmartApprover.hook.ts` | Trusted/read approval behavior. Registration in the release settings was not confirmed in the inspected excerpt. |
| `PostToolUseFailure` | hook README | Tool failure tracking. Registration in the release settings was not confirmed in the inspected excerpt. |
| `SubagentStart` / `SubagentStop` | hook README | Release notes say Claude payload gaps pushed PAI to track agent lifecycle through `PreToolUse:Agent` and `PostToolUse:Agent`. |

## Claude Lifecycle Assumptions

The release hook system assumes:

- Hooks are TypeScript or shell scripts called by Claude Code lifecycle events.
- Hooks receive JSON on stdin with fields such as `session_id`, `transcript_path`, `hook_event_name`, `prompt`, `tool_name`, `tool_input`, `tool_response`, and `last_assistant_message`.
- Some hooks emit JSON on stdout using Claude-shaped fields such as `hookSpecificOutput`, `hookEventName`, `additionalContext`, `permissionDecision`, or `decision`.
- Some hooks enforce behavior through exit codes, including `SecurityPipeline.hook.ts` exiting with code `2` on deny.
- Some hooks are blocking, some are async, and some have explicit timeouts in `settings.json`.
- Hook commands are rooted under `$HOME/.claude/hooks/`.
- `PAI_DIR` defaults to `${HOME}/.claude/PAI` in `settings.json`.
- PAI Memory and ISA files are read and sometimes written by hook-adjacent behavior.
- Pulse HTTP routes on `http://localhost:31337/hooks/*` participate in `Skill` and `Agent` guard behavior.
- Claude tool names such as `Bash`, `Write`, `Edit`, `MultiEdit`, `Read`, `Skill`, `Agent`, and `AskUserQuestion` appear in matcher semantics.

## Codex Native Hook and Rule Surfaces

S2 official-source evidence records Codex hooks and Codex rules as native Codex surfaces.

Codex hooks are future native control surfaces, not Claude hook destinations. Codex rules are future native control surfaces, not Claude settings destinations. Codex config/profile is policy/configuration, not Life OS doctrine.

Codex hooks/rules/config are native Codex surfaces, not Claude hook destinations.

S2 records that Codex hooks are experimental, feature-flagged, use JSON stdin, and support some overlapping events such as `SessionStart`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `UserPromptSubmit`, and `Stop`. S2 also records that Codex `PreToolUse` is a guardrail rather than a complete enforcement boundary.

S2 records that Codex rules are experimental and control commands outside the sandbox under active config layers. Codex rules cannot receive copied Claude settings, Claude hook payload assumptions, or Claude command files.

Any future Codex hook/rule mapping requires its own spec and tests.

## Non-Equivalent Lifecycle Semantics

Claude Code hook semantics are not equivalent to Codex hook/rule semantics.

Known non-equivalence areas:

- Event coverage overlaps but is not identical.
- Event order and blocking behavior are not proven equivalent.
- Claude hook payload fields are not Codex payload fields by default.
- Claude `settings.json` matcher semantics are not Codex config/rule syntax.
- Claude hook stdout shapes are not Codex hook output contracts unless proven.
- Claude hook exit-code semantics are not Codex denial semantics unless proven.
- Pulse HTTP hook routes are PAI/Pulse behavior, not Codex hook behavior.
- PAI Memory and ISA writes are canonical PAI state mutations and cannot be inherited from Claude hooks.
- Product memories, transcripts, SDK threads, and `/goal` state are not PAI Memory.

## Mapping Classification Model

| Class | Meaning |
| --- | --- |
| `M0: Not applicable` | No hook/lifecycle mapping is needed. |
| `M1: Documentation-only reference` | Source informs future design but does not map to a live Codex surface. |
| `M2: Authority/context candidate` | Behavior may be represented through authority envelope or compact router design. |
| `M3: Codex hook candidate` | Behavior may map to future Codex-native hook configuration after spec and tests. |
| `M4: Codex rule/policy candidate` | Behavior may map to future Codex rules, sandbox, approval, or permission policy after spec and tests. |
| `M5: Bridge required` | Behavior requires an adapter bridge or dispatcher, not only native hooks/rules. |
| `M6: Prohibited in read-only mode` | Behavior would write state, invoke runtime side effects, or access private state. |
| `M7: Unknown / evidence gap` | Evidence is insufficient and must be reviewed later. |
| `M8: Drop-in blocker` | Behavior blocks drop-in claims until mapped, tested, and validated. |

## Hook Mapping Table

| Mapping ID | Evidence source | Claude hook/lifecycle behavior | Current Codex-native candidate | Mapping class | Main hazard | Required future proof | S7D decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HM-001 | `settings.json` | Hook registration, permissions allowlist, HTTP hook URL allowlist, env defaults, status line, plugin config. | Codex config, rules, sandbox, approvals, and future hook config. | `M4: Codex rule/policy candidate` plus `M8: Drop-in blocker` | Direct translation can overgrant writes or misbind live `.claude` paths. | Settings/security mapping, denied-path tests, least-privilege proof. | Design only; do not copy `settings.json`. |
| HM-002 | `LoadContext.hook.ts` | `SessionStart` dynamic context loading from relationship, learning, work, opinions, and ISA-linked files. | Authority/context envelope candidate plus future hook candidate. | `M2: Authority/context candidate` plus `M3: Codex hook candidate` | Dynamic context could override PAI doctrine or read private state. | Authority ordering, source allowlist, truncation, and no-private-read proof. | Design only; no context hook created. |
| HM-003 | `PromptProcessing.hook.ts` | `UserPromptSubmit` mode/tier classification, tab/session naming, telemetry, and additional context output. | Event/context envelope plus future hook candidate. | `M3: Codex hook candidate` plus `M5: Bridge required` | Claude `additionalContext` behavior may not map directly. | Payload/output contract, ordering, and prompt-processing fixture proof. | Design only; no prompt hook created. |
| HM-004 | `SecurityPipeline.hook.ts`, `SmartApprover.hook.ts`, `settings.json` | Pre-tool security checks and permission decisions for Bash/write/read classes. | Codex rules, sandbox, approvals, and future hook guardrail. | `M4: Codex rule/policy candidate` plus `M8: Drop-in blocker` | Fail-open or overbroad allow could bypass protected paths. | Fail-closed tests, denied-action proof, sandbox/approval validation. | Design only; no policy installed. |
| HM-005 | `ToolActivityTracker.hook.ts`, `ISASync.hook.ts`, `ContentScanner.hook.ts`, settings `PostToolUse` | Post-tool observation, ground-truth audit, ISA sync, content scanning, state pushes. | Audit envelope plus future hook candidate; some behavior requires bridge. | `M3: Codex hook candidate`, `M5: Bridge required`, `M6: Prohibited in read-only mode` | Observation can become write behavior to PAI Memory, ISA, Pulse, or KV. | Audit-only proof, no-write proof, single-writer gate for future writes. | Design only; no post-tool mapping installed. |
| HM-006 | settings `UserPromptSubmit`, `PromptGuard.hook.ts`, `RepeatDetection.hook.ts`, `PromptProcessing.hook.ts`, `SatisfactionCapture.hook.ts` | User prompt guard, repeat detection, prompt processing, satisfaction capture. | Future Codex hook plus authority/event envelope. | `M3: Codex hook candidate` plus `M2: Authority/context candidate` | Prompt hooks may mutate context or advisory outputs without audit. | Event envelope, context ordering, advisory output, and no-promotion proof. | Design only. |
| HM-007 | settings `SessionStart`, `LoadContext.hook.ts`, `KittyEnvPersist.hook.ts`, `KVSync.hook.ts` | Session start context loading, terminal state, and KV sync. | Authority envelope plus future hook candidate; KV sync requires bridge. | `M2: Authority/context candidate`, `M3: Codex hook candidate`, `M6: Prohibited in read-only mode` | Startup could read live PAI state or write remote state. | Source allowlist, no-private-read, no-remote-write, and rollback proof. | Design only. |
| HM-008 | settings `Stop`, `SessionEnd`, `VoiceCompletion.hook.ts`, `WorkCompletionLearning.hook.ts`, `SessionCleanup.hook.ts` | Completion voice, doc integrity, response cache, learning capture, cleanup. | Audit-only envelope; bridge required for voice/Pulse/learning. | `M5: Bridge required`, `M6: Prohibited in read-only mode`, `M8: Drop-in blocker` | Completion hooks write canonical or product state and may call services. | No-write proof, Pulse no-start proof, single-writer gate, bridge tests. | Design only. |
| HM-009 | hook README, `hook-io.ts`, representative hooks | JSON stdin payload assumptions and stdout/stderr conventions. | Event/context envelope. | `M5: Bridge required` | Payload mismatch can silently drop context, denials, or audit fields. | Envelope schema, fixture payload replay, unsupported field reporting. | Design only. |
| HM-010 | `settings.json`, hook files | Command hook execution, async flags, timeouts, shell/TypeScript runtime assumptions. | Codex hook candidate only after native execution semantics are tested. | `M3: Codex hook candidate`, `M7: Unknown / evidence gap` | Timeout, async, exit, and runtime differences can change behavior. | Native hook execution fixture tests and fail-mode matrix. | Design only; do not execute hooks. |
| HM-011 | `LoadContext.hook.ts`, `ISASync.hook.ts`, `WorkCompletionLearning.hook.ts`, S1-S7C docs | PAI Memory and ISA read/write boundary behavior. | Memory/ISA policy in event envelope; write-capable mode requires single-writer. | `M6: Prohibited in read-only mode`, `M8: Drop-in blocker` | Product memories or advisory outputs could be promoted into PAI Memory or ISA. | No-write proof, non-promotion proof, single-writer validation. | Writes remain blocked. |
| HM-012 | `settings.json`, hook README, Pulse HTTP hook routes, voice hooks | Pulse event/job/HTTP boundary behavior on port `31337`. | Future Pulse bridge only; not a hook-only mapping. | `M5: Bridge required`, `M6: Prohibited in read-only mode`, `M8: Drop-in blocker` | Pulse parity overclaim or accidental local endpoint calls. | Pulse bridge identity and no-start proof. | S7D does not design or implement Pulse bridge. |
| HM-013 | `AgentInvocation.hook.ts`, settings Agent matchers, hook README | Agent/subagent lifecycle tracking through `PreToolUse:Agent` and `PostToolUse:Agent`. | Future Codex subagent/event envelope mapping. | `M5: Bridge required`, `M8: Drop-in blocker` | Claude Agent payload and Codex subagent metadata are not equivalent. | Subagent identity, prompt, duration, and audit mapping tests. | Design only. |
| HM-014 | S2 Codex native surface evidence | Codex rules as possible policy/control surface. | Codex rules. | `M4: Codex rule/policy candidate` | Rules may be mistaken for complete hook parity or PAI state ownership. | Rule scope, sandbox, approval, and protected-path tests. | Design only; no rules files created. |
| HM-015 | S2 Codex native surface evidence | Codex hooks as possible event/control surface. | Codex hooks. | `M3: Codex hook candidate` | Experimental hooks may not cover all PAI lifecycle semantics. | Native hook event, payload, output, ordering, and guardrail tests. | Design only; no Codex hooks created. |

## Load Context Mapping

`LoadContext.hook.ts` treats `PAI_SYSTEM_PROMPT.md` as constitutional doctrine, `CLAUDE.md` as Claude operational guidance, and dynamic context as session-specific supplemental information.

Future Codex mapping must preserve:

- `PAI_SYSTEM_PROMPT.md` as high-authority PAI doctrine.
- `CLAUDE.md` as an official Claude-facing surface, not a Codex destination file.
- Future Codex `AGENTS.md`, if later authorized, as a compact router.
- Dynamic context as bounded context, not doctrine.
- Product memories as non-authority and not PAI Memory.
- `/goal` state as workflow-control state, not PAI Memory and not ISA.

## Prompt Processing Mapping

`PromptProcessing.hook.ts` handles prompt classification, session naming, tab state, telemetry, and Claude-shaped additional context.

Future mapping must report:

- Prompt event source.
- Prompt event type.
- Authority envelope used.
- Context additions requested.
- Unsupported output fields.
- Denied mutations.
- Audit and provenance.

Prompt-processing behavior must not silently mutate PAI doctrine.

## Tool Permission and Observation Mapping

Tool permission and observation behavior spans `SecurityPipeline.hook.ts`, `SmartApprover.hook.ts`, `ToolActivityTracker.hook.ts`, `ISASync.hook.ts`, content scanning, Pulse HTTP guards, and settings matchers.

Future mapping must separate:

- Permission decision behavior.
- Sandbox enforcement behavior.
- Tool observation behavior.
- Audit-only behavior.
- State-write behavior.
- Pulse interaction behavior.

Read-only mode must deny PAI Memory writes, ISA writes, Pulse startup, Pulse writes, release writes, root `AGENTS.md` edits, `.codex/` creation, and private user-local state access.

## Session and Completion Mapping

Session and completion behavior includes `SessionStart`, `Stop`, and `SessionEnd` hooks.

Future mapping must not treat completion hooks as permission to:

- Capture product memories into PAI Memory.
- Accept ISA state.
- Start Pulse.
- Write learning files.
- Write relationship memory.
- Clear or mutate live PAI state.
- Call external services.

Any future completion bridge requires explicit single-writer policy, provenance, rollback, and validation.

## Subagent and Agent Boundary Mapping

`AgentInvocation.hook.ts` documents that Claude built-in `SubagentStart` and `SubagentStop` payloads were insufficient for PAI, so release behavior tracks agent lifecycle at `PreToolUse:Agent` and `PostToolUse:Agent`.

Future Codex mapping must not assume Codex subagent lifecycle metadata is equivalent. It must define native fields for agent type, description, prompt preview, start, stop, duration, sandbox inheritance, permissions, and Pulse/reporting boundaries.

## Memory and ISA Boundary Mapping

PAI Memory and ISA artifacts are canonical PAI state.

Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory. Product memories must not be silently promoted into PAI Memory.

Read-only hook lifecycle mapping may produce advisory reports only. It may not write PAI Memory, write ISA, accept ISA, or create shadow ISA state.

Future writes require a single-writer policy, provenance, rollback, and validation.

## Pulse Boundary Mapping

Pulse remains central v5 infrastructure, but S7D does not design or implement a Pulse bridge.

Release evidence shows Pulse-related hook behavior through local HTTP hook routes, voice behavior, observability transport, and references to port `31337`.

Future hook lifecycle mapping must deny Pulse startup, Pulse writes, Pulse endpoint calls, and Pulse parity claims unless a later Pulse milestone explicitly approves a bridge.

## Required Future Proofs

Future hook/lifecycle work must prove:

- Claude hook files are not copied into Codex hook surfaces.
- Claude `settings.json` is not copied into Codex config.
- Codex hooks and Codex rules are mapped natively.
- Event coverage is explicit.
- Unsupported events are reported.
- Payload fields are mapped or rejected.
- Output fields are mapped or rejected.
- Blocking, async, timeout, and exit-code behavior are validated.
- Permission and sandbox behavior is fail-closed.
- PAI Memory and ISA writes are denied in read-only mode.
- Pulse startup and endpoint calls are denied in S7D posture.
- Rollback remains available.

## Prohibited Hook Mappings

Prohibited designs:

- Copy Claude hook files into Codex hook files.
- Copy Claude-shaped files directly into Codex surfaces.
- Copy Claude `settings.json` into Codex config.
- Treat Codex hooks/rules as complete replacements for Claude hooks before tests.
- Run Claude hooks directly under Codex without payload mapping.
- Use hooks to bypass Codex sandbox, approvals, or PAI protected-path policy.
- Promote product memories, transcripts, SDK threads, or `/goal` state into PAI Memory.
- Write ISA or PAI Memory in read-only mode.
- Start Pulse or call Pulse endpoints in S7D.
- Claim Codex is drop-in today.

## Non-Goals

S7D does not implement hook or lifecycle mapping, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create migration scripts, create runtime files, create adapter payloads, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, run Codex hook commands, run Codex rule commands, run `codex execpolicy check`, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, imply Claude-shaped files can be copied directly into Codex surfaces, propose installing hooks/rules/config/event envelopes/lifecycle adapters, or advance beyond S7D.
