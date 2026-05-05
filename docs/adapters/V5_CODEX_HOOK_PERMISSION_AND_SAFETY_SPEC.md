# V5 Codex Hook Permission and Safety Spec

## Purpose

Define future safety, sandbox, permission, denial, and audit requirements for any hook/lifecycle mapping.

## Scope

Hook safety is future policy and validation design, not implementation.

S7D creates no hook files, rules files, config files, permission policy files, event envelope instances, runtime files, generated configs, adapter payloads, manifests, audit artifacts, fixtures, or harnesses.

Codex hooks and rules must not be treated as complete replacements for Claude hooks until tested.

Codex hooks/rules must not be treated as complete replacements for Claude hooks until tested.

Codex hooks and Codex rules must not bypass Codex sandbox, approvals, or PAI protected-path policy.

## Evidence Base

Evidence comes from:

- `Releases/v5.0.0/.claude/settings.json`
- `Releases/v5.0.0/.claude/hooks/README.md`
- `Releases/v5.0.0/.claude/hooks/SecurityPipeline.hook.ts`
- `Releases/v5.0.0/.claude/hooks/SmartApprover.hook.ts`
- `Releases/v5.0.0/.claude/hooks/ToolActivityTracker.hook.ts`
- `Releases/v5.0.0/.claude/hooks/ISASync.hook.ts`
- `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`
- `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`

No new Codex capability claim is introduced in S7D. Codex hooks, Codex rules, config, sandbox, and approval facts are inherited from S2 official-source evidence.

## Safety Problem Statement

Codex is not currently proven drop-in for existing local PAI v5 files.

Claude settings grant broad permissions, register command hooks, call Pulse HTTP hook routes, and allow writes under `.claude` and project roots. That safety model cannot be copied directly into Codex config, Codex hooks, or Codex rules.

Codex replacement is plausible only through a designed adapter that maps safety intent into native Codex surfaces with explicit tests, denial reports, unsupported surface reports, and rollback.

## Permission Boundary Model

Future permission mapping must define:

- Allowed read classes.
- Denied read classes.
- Denied write classes.
- Tool permission classes.
- MCP permission classes.
- Network permission classes.
- Human approval behavior.
- Fail-closed behavior.
- Unsupported behavior.

Claude Code permission names and Codex permission controls are not interchangeable. Mapping must be behavior-based.

## Sandbox Boundary Model

Future sandbox mapping must treat Codex sandboxing as a native Codex safety surface, not as a PAI state lock.

Sandbox mapping must be combined with:

- PAI protected-path policy.
- Release-file immutability.
- `.codex/` and root `AGENTS.md` protection.
- No private user-local memory reads.
- No PAI Memory writes.
- No ISA writes.
- No Pulse startup or Pulse writes.
- Audit and provenance.

## Read-Only Enforcement Model

Read-only mode permits advisory inspection of explicitly approved sources only.

Read-only mode denies:

- Writes to release files.
- Writes to `.claude/`.
- Writes to `.codex/`.
- Writes to root `AGENTS.md`.
- Writes to hooks, rules, config, skills, agents, commands, launchers, wrappers, generated configs, manifests, audit artifacts, or adapter payloads.
- Writes to PAI Memory.
- Writes to ISA.
- Writes to Pulse state.
- Local Pulse endpoint calls.
- Installer execution.
- Import or migration tooling.
- Claude Code invocation.
- Codex runtime invocation during design milestones.

## Denied Action Model

Denied actions:

- Modifying release files.
- Modifying root `AGENTS.md`.
- Creating or modifying `.codex/`.
- Reading private user-local memory.
- Writing PAI Memory.
- Writing ISA.
- Starting Pulse.
- Writing Pulse state.
- Running installers.
- Running migration/import tooling.
- Invoking Claude Code.
- Invoking Codex as runtime engine during design milestones.
- Silently allowing unsupported Claude hook behavior.

Denied action reporting must use `denied_action_report`.

## Tool and MCP Safety Model

Tool and MCP safety must be explicit.

Future mapping must distinguish:

- Tool read behavior.
- Tool write behavior.
- Bash or command behavior.
- MCP tool allowlist and denylist behavior.
- HTTP/local service behavior.
- Pulse local endpoint behavior.
- Tool output scanning.
- Permission decisions.
- Unsupported tool behavior.

Codex hooks/rules must not bypass Codex sandbox, approvals, or PAI protected-path policy.

## Filesystem Safety Model

Filesystem safety must deny:

- `Releases/`
- `Releases/v5.0.0/`
- `Releases/v5.0.0/.claude/`
- `.claude/`
- `PAI/`
- `CLAUDE.md`
- `AGENTS.md`
- `.codex/`
- `install.sh`
- `PAI_SYSTEM_PROMPT.md`
- `settings.json`
- `hooks/`
- `skills/`
- `subagents/`
- `agents/`
- `commands/`
- `.github/`
- `.agents/`

Future read-only fixture work may allow controlled reads of release evidence, but S7D does not run a trial or create fixtures.

## Memory and ISA Safety Model

PAI Memory and ISA artifacts are canonical PAI state.

Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory. Product memories must not be silently promoted into PAI Memory.

S7D does not authorize PAI Memory writes or ISA writes.

Any future write-capable hook behavior requires single-writer policy, provenance, rollback, and validation.

## Pulse Safety Model

Pulse remains central v5 infrastructure, but S7D does not design or implement a Pulse bridge.

Future hook safety must deny:

- Pulse startup.
- Pulse writes.
- Pulse local endpoint calls.
- Pulse parity claims.
- Pulse job identity reuse without architect approval.

## Product Memory Safety Model

Any future hook-generated advisory output must not be promoted into PAI Memory, ISA, Pulse, Claude memory, or Codex memory by default.

Product memory safety requires:

- No silent promotion.
- Explicit classification.
- Provenance.
- Human/architect review before canonical writes.
- Single-writer control before PAI state writes.

## Audit and Provenance Requirements

Future safety outputs:

- `allowed_action_report`
- `denied_action_report`
- `unsupported_surface_report`
- `sandbox_report`
- `permission_report`
- `memory_write_status`
- `isa_write_status`
- `pulse_action_status`
- `provenance`
- `failure_reason`

Audit and provenance must identify source evidence, event ID, engine ID, adapter mode, denied actions, unsupported surfaces, and future rollback path.

## Failure and Stop Conditions

Stop future hook/lifecycle work if:

- A protected path must be modified.
- Runtime implementation becomes necessary.
- Claude hook files would need to be copied into Codex hook files.
- Claude settings would need to be copied into Codex config.
- PAI Memory or ISA writes are required without single-writer policy.
- Pulse startup, Pulse endpoint calls, or Pulse writes are required.
- Private user-local state must be inspected.
- Codex hook, rule, execpolicy, or runtime commands must be run in a design milestone.
- Existing-local-v5 trial execution becomes necessary.

## Required Future Proofs

Future hook safety work must prove:

- Denied actions are blocked.
- Unsupported surfaces are reported.
- Sandbox posture matches the adapter mode.
- Permission posture is fail-closed.
- Protected paths are not modified.
- Private user-local state is not read.
- PAI Memory and ISA writes are blocked in read-only mode.
- Pulse startup and Pulse writes are blocked.
- Hook-generated advisory output is not promoted into canonical state.
- Rollback and reversibility remain available.

S7D cannot mark hook/lifecycle parity as proven.

## Prohibited Safety Designs

Prohibited designs:

- Treating Codex hooks/rules as complete replacements for Claude hooks before tests.
- Bypassing Codex sandbox, approvals, or PAI protected-path policy.
- Copying Claude hook files into Codex hook surfaces.
- Copying Claude settings into Codex config.
- Creating hook files, rules files, config files, or permission policy files in S7D.
- Creating event envelope instances in S7D.
- Writing PAI Memory or ISA in read-only mode.
- Starting Pulse or writing Pulse state in S7D.
- Running installers, migration/import tooling, Claude Code, Codex runtime commands, Codex hook commands, Codex rule commands, or `codex execpolicy check`.
- Claiming Codex is drop-in today.

## Non-Goals

S7D does not implement hook safety, create hook files, create rules files, create config files, create permission policy files, create root `AGENTS.md`, create `.codex/`, create runtime files, create adapter payloads, create fixtures, create harnesses, create manifests, create audit artifacts, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, run Codex hook commands, run Codex rule commands, run `codex execpolicy check`, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, propose installing hooks/rules/config/event envelopes/lifecycle adapters, or advance beyond S7D.
