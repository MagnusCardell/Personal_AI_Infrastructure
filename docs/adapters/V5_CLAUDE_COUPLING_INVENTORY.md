# V5 Claude Coupling Inventory

## Purpose

Inventory material Claude Code couplings found in the PAI v5.0.0 release and prior adapter docs, then identify the future seams required before Codex can become drop-in-capable.

This document is design-only. S6 does not implement decoupling, does not create runtime adapter seams, and does not authorize read-only trial execution.

## Scope

The inventory covers the release payload under `Releases/v5.0.0/.claude/` and S0-S5 adapter conclusions.

It does not inspect private user-local state, run installers, start Pulse, invoke Claude Code, run Codex import or migration tooling, create root `AGENTS.md`, create `.codex/`, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, or modify release files.

## Evidence Base

Primary evidence:

- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- `docs/adapters/V5_UPSTREAM_RISK_REGISTER.md`
- `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_FIXTURE_AND_PATH_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_MANIFEST_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_SCHEMA_PROPOSAL.md`

Release evidence:

- `Releases/v5.0.0/README.md`
- `Releases/v5.0.0/.claude/CLAUDE.md`
- `Releases/v5.0.0/.claude/settings.json`
- `Releases/v5.0.0/.claude/hooks/README.md`
- `Releases/v5.0.0/.claude/hooks/PromptProcessing.hook.ts`
- `Releases/v5.0.0/.claude/hooks/lib/paths.ts`
- `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md`
- `Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts`
- `Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md`
- `Releases/v5.0.0/.claude/PAI/PAI-Install/README.md`
- `Releases/v5.0.0/.claude/agents/`
- `Releases/v5.0.0/.claude/commands/`
- `Releases/v5.0.0/.claude/skills/`

Required discovery ran to `/tmp/v5-s6-coupling-search.txt`; it was not written into the repository.

## Coupling Classification Model

| Class | Meaning |
| --- | --- |
| `C0: Not a coupling` | Mention/reference only; no adapter impact. |
| `C1: Documentation coupling` | PAI docs assume Claude Code but runtime path is not directly coupled. |
| `C2: Instruction-surface coupling` | Claude-facing instructions or authority path must be mapped to Codex-native authority. |
| `C3: Runtime invocation coupling` | Code or script invokes Claude Code or assumes Claude CLI behavior. |
| `C4: Lifecycle/event coupling` | Hooks, events, or lifecycle semantics assume Claude Code. |
| `C5: State/layout coupling` | PAI state or install layout assumes `.claude`, `PAI_DIR`, or Claude product paths. |
| `C6: Safety/security coupling` | Settings, permissions, sandbox, or trust behavior assumes Claude Code. |
| `C7: Central-system coupling` | Pulse, Memory, ISA, or daemon behavior is coupled to Claude-specific identity or behavior. |
| `C8: Blocker` | Coupling blocks drop-in replacement until a future seam/spec/test exists. |

## Executive Summary

Codex is not currently proven drop-in for existing local PAI v5 files.

PAI v5.0.0 is Claude Code-native in authority, launcher, inference, settings, hooks, skills, agents, commands, local layout, Pulse jobs, and user-local state assumptions. Codex replacement is plausible only through a designed adapter with explicit seams; Claude-shaped files must not be copied directly into Codex surfaces.

Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists. S6 identifies couplings and future seam requirements only.

## Instruction and Authority Couplings

The release uses `PAI_SYSTEM_PROMPT.md` as high-authority doctrine and `CLAUDE.md` as an official Claude-facing instruction surface.

`PAI_SYSTEM_PROMPT.md` states that it is the highest authority layer and that `CLAUDE.md` defines operational procedures and format templates. `CLAUDE.md` references `PAI/PAI_SYSTEM_PROMPT.md`, `PAI_DIR`, Algorithm files, Pulse notifications, Interceptor, skills, subagents, and Claude Code behavior.

A future Codex `AGENTS.md`, if later authorized, must be a compact router. It must not clone `CLAUDE.md` or `PAI_SYSTEM_PROMPT.md`.

## Launcher and Inference Couplings

`PAI/TOOLS/pai.ts` is a Claude launcher. It sets `CLAUDE_DIR` to `~/.claude`, manages MCP profiles under that directory, checks `claude --version`, and launches `claude` with a system-prompt file.

`PAI/TOOLS/Inference.ts` shells out to `claude`, uses Claude model names (`haiku`, `sonnet`, `opus`), deletes Anthropic API environment variables to preserve Claude Code subscription routing, and uses Claude CLI flags such as `--print`, `--model`, `--tools`, `--setting-sources`, and `--system-prompt`.

These are direct runtime invocation couplings and are blockers for drop-in replacement until launcher and inference seams are specified and tested.

## Settings and Permission Couplings

`settings.json` uses the Claude Code settings schema. It grants Claude tool permissions such as `Task`, `Skill`, `Agent(...)`, `TodoWrite`, `EnterPlanMode`, `Bash`, `Write(~/.claude/**)`, and `Edit(~/.claude/**)`.

The same file defines Claude lifecycle hooks, HTTP hook routes, trusted local service rules, PAI identity fields, and `PAI_DIR` as `${HOME}/.claude/PAI`.

This is a safety/security coupling. A Codex adapter must map security intent to native Codex controls, not translate the JSON shape directly.

## Hook and Lifecycle Couplings

The hook system is explicitly described as lifecycle event handlers that extend Claude Code. It depends on events such as `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `ConfigChange`, and `SessionEnd`.

Hook payloads include Claude Code fields such as `session_id`, `transcript_path`, `hook_event_name`, `tool_name`, `tool_input`, and `stop_hook_active`. `PromptProcessing.hook.ts` writes `additionalContext` for Claude Code and uses Claude inference to select mode and tier.

Codex hook behavior must be designed natively. Unsupported events, payload gaps, ordering differences, and fail-open or fail-closed differences must remain visible.

## Skill Couplings

The release ships Claude-facing skill directories under `.claude/skills/`, with `SKILL.md`, workflows, tools, references, templates, and skill-specific assumptions. S0/S2 already classify skills as a transformation surface, not portable files.

Skills must be transformed by semantics. Direct copying into Codex skill surfaces would risk wrong activation behavior, hidden tool assumptions, state writes, and prompt-authority drift.

## Agent and Command Couplings

The release ships Claude agent definitions under `.claude/agents/` and command files under `.claude/commands/`.

Settings grant `Agent(...)` permissions, `CLAUDE.md` references `Agent(subagent_type=...)`, and command files are Claude-facing slash-command material. S0/S2 identify agents and commands as high-risk transformation surfaces.

Codex agents, subagents, or command-like behavior must be designed as native Codex material with tests. The names `agent` and `command` are not evidence of compatibility.

## Pulse Couplings

Pulse is central v5 infrastructure. It is a local daemon on port `31337` with dashboard, observability, voice, hook validation, scheduled jobs, and state.

Pulse docs define `type = "claude"` jobs and describe spawning Claude headless through the `PAI/TOOLS/Inference.ts` flag pattern. Settings route SkillGuard and AgentGuard through Pulse HTTP routes. `CLAUDE.md` and the system prompt include Pulse notification behavior.

S6 does not design or implement a Pulse bridge. Pulse parity cannot be claimed until a future event and job identity seam exists.

## Memory and ISA Couplings

PAI Memory and ISA artifacts are canonical PAI state.

Memory docs define PAI Memory under `~/.claude/PAI/MEMORY/` and Auto-Memory under Claude Code project memory paths. ISA docs define the ISA as the single source of truth, test harness, build verification, done condition, and system of record.

Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory. Product memories must not be silently promoted into PAI Memory.

## Installer and Local Layout Couplings

The release installs to `~/.claude/`, backs up existing `~/.claude/`, verifies or installs Claude Code, generates or merges `settings.json`, creates `.env`, configures shell aliases, and optionally installs Pulse and the Pulse menu bar.

The installer model is not a Codex adapter model. Future read-only trials must not require uninstalling Claude Code and must be reversible.

## Product Memory Couplings

Claude Code product memory and project transcripts are adjacent to PAI Memory in the current local layout, but they are not canonical PAI state by adapter policy.

Codex memory is also product memory. It must not be read as PAI Memory, silently merged into PAI Memory, or used as hidden authority. Any future promotion path requires explicit curation, provenance, and single-writer policy.

## User-Local State Couplings

The release assumes live user-local roots such as `~/.claude/`, `~/.claude/PAI/`, and `~/.claude/projects/`.

S6 reads only repository-local release files, not private user-local state. Existing-local-v5 future trials require explicit read-only manifests, denied-path controls, no write ability, rollback, and no Pulse startup.

## Coupling Inventory Table

| Coupling ID | Release path or evidence source | Coupling class | Coupled surface | Observed Claude assumption | Codex replacement hazard | Required seam | Drop-in impact | S6 decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CC-001 | `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md`; S0/S3 | `C2`, `C8` | Authority | System prompt is loaded above `CLAUDE.md` and treated as highest authority. | Codex may not preserve equivalent authority ordering without explicit design. | Authority seam | Blocks drop-in claim. | Confirmed; future authority-equivalence gate required. |
| CC-002 | `Releases/v5.0.0/.claude/CLAUDE.md`; S0/S2 | `C2`, `C8` | Claude instruction router | `CLAUDE.md` is the official Claude-facing operational surface. | Copying it into `AGENTS.md` would clone Claude assumptions. | Router seam | Blocks direct surface reuse. | Confirmed; Codex router must be compact and native. |
| CC-003 | `settings.json`; `hooks/lib/paths.ts`; PAI-Install docs | `C5`, `C8` | Local layout and `PAI_DIR` | PAI data lives under `~/.claude/PAI`; Claude home holds settings, hooks, skills, agents, commands. | Codex could bind to live user state or write into Claude-owned roots. | Installer/local layout seam | Blocks existing-local-v5 mode. | Confirmed; read-only path model remains required. |
| CC-004 | `Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts` | `C3`, `C8` | Launcher | Launcher manages `.claude` MCPs and spawns `claude`. | Codex cannot replace launcher by file copy or flag substitution. | Launcher seam | Blocks local engine substitution. | Confirmed; future native launcher contract needed. |
| CC-005 | `Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts` | `C3`, `C8` | Inference | Inference shells out to `claude` with Claude model names and auth behavior. | Codex output, auth, model, timeout, and JSON parsing behavior are unproven. | Inference seam | Blocks inference parity. | Confirmed; future provider contract needed. |
| CC-006 | `Releases/v5.0.0/.claude/settings.json` | `C6`, `C8` | Settings and permissions | Claude settings schema grants Claude tools, hooks, and write permissions. | Direct translation could weaken sandbox or overgrant writes. | Settings and permission seam | Blocks safe runtime mode. | Confirmed; map behavior, not syntax. |
| CC-007 | `settings.json`; `hooks/README.md` | `C4`, `C8` | Lifecycle hooks | Hook events are Claude Code lifecycle events. | Codex event support may differ in timing, payload, and enforcement. | Hook and lifecycle seam | Blocks lifecycle parity. | Confirmed; compatibility matrix required. |
| CC-008 | `hooks/README.md`; `PromptProcessing.hook.ts` | `C4`, `C8` | Hook payload/context | Hook stdin payloads and `additionalContext` are Claude Code-specific. | Codex may lose mode/tier injection, tab naming, and guard context. | Hook and lifecycle seam | Blocks authority and behavior parity. | Confirmed; payload fixture tests required. |
| CC-009 | `.claude/skills/`; S0/S2 | `C2`, `C6`, `C8` | Skills | Skills are authored for Claude-facing skill semantics. | Copying skills could misroute activation and tool/state assumptions. | Skill seam | Blocks workflow parity. | Confirmed; semantic transformation required. |
| CC-010 | `.claude/agents/`; `settings.json`; S0/S2 | `C2`, `C6`, `C8` | Agents/subagents | Agents use Claude agent names, permissions, models, and invocation semantics. | Codex subagents are adjacent, not equivalent. | Agent and command seam | Blocks delegation parity. | Confirmed; role and permission mapping required. |
| CC-011 | `.claude/commands/`; S0/S2 | `C2`, `C8` | Slash commands | Commands are Claude-facing command files and reference Claude tools. | Codex built-in slash commands are not PAI command files. | Agent and command seam | Blocks command parity. | Confirmed; command strategy required. |
| CC-012 | Pulse docs; `settings.json` HTTP hooks | `C7`, `C8` | Pulse daemon/dashboard | Pulse centrality includes hooks, voice, dashboard, observability, and local endpoints. | Codex activity is invisible or mislabeled without a bridge. | Pulse seam | Blocks Pulse safety gate. | Confirmed; S6 does not implement bridge. |
| CC-013 | `PulseSystem.md` Claude job sections | `C7`, `C8` | Pulse jobs | Pulse supports `type = "claude"` jobs and Claude CLI spawning. | Overloading Claude job type for Codex would corrupt provenance. | Pulse seam | Blocks job parity. | Confirmed; future job identity required. |
| CC-014 | `MemorySystem.md`; S0/S5 | `C7`, `C8` | PAI Memory | PAI Memory is canonical PAI state; hooks and harvesters write structured memory. | Codex memory or outputs could be mistaken for PAI Memory. | Memory seam | Blocks write-capable mode. | Confirmed; writes blocked until single-writer. |
| CC-015 | `IsaFormat.md`; S0/S5 | `C7`, `C8` | ISA | ISA is system of record and done condition. | Codex plans, transcripts, or `/goal` could create shadow acceptance. | ISA seam | Blocks acceptance parity. | Confirmed; writes blocked until single-writer. |
| CC-016 | `README.md`; `PAI-Install/README.md`; PAI-Install engine docs | `C5`, `C8` | Installer/local layout | Install clones or overlays `~/.claude`, verifies Claude Code, and installs Pulse. | Codex replacement could overwrite Claude fallback or live state. | Installer/local layout seam and rollback seam | Blocks existing-user safety. | Confirmed; no installer edits in S6. |
| CC-017 | `PAI_SYSTEM_PROMPT.md`; `MemorySystem.md`; S0 | `C5`, `C7` | Claude Code product memory | Claude Code projects and auto-memory are not PAI authority by adapter policy. | Product memories could be silently promoted into PAI Memory. | Product-memory boundary seam | Blocks memory safety. | Confirmed; no promotion without provenance. |
| CC-018 | S2/S3/S4/S5 adapter docs | `C5`, `C7` | Codex memory | Codex memory is product state, not PAI Memory. | Codex recall could be treated as canonical state or authority. | Product-memory boundary seam | Blocks dual-engine safety. | Confirmed from adapter evidence; not release evidence. |
| CC-019 | `V5_ADAPTER_BOUNDARIES.md`; S1-S5 docs | `C1`, `C8` | Governance boundary | Repo governance and product payload are distinct from engine runtime surfaces. | Adapter work could mutate protected governance or runtime paths. | Rollback seam and governance gate | Blocks scope integrity. | Confirmed; docs-only area remains separate. |
| CC-020 | S1-S5 adapter docs; absence of S6 runtime files | `C8` | Future Codex native surfaces | Codex-native adapter surfaces are absent by design in S6. | Absence prevents any drop-in claim and prevents runtime validation. | All seams | Blocks replacement readiness. | Confirmed; S6 designs only. |

## Highest-Risk Couplings

Highest-risk blockers:

- `CC-001` authority handling for `PAI_SYSTEM_PROMPT.md`.
- `CC-004` and `CC-005` direct Claude launcher and inference invocation.
- `CC-006` settings and permission semantics.
- `CC-007` and `CC-008` lifecycle and hook payload behavior.
- `CC-012` and `CC-013` Pulse centrality and Claude job identity.
- `CC-014` and `CC-015` PAI Memory and ISA state writes.
- `CC-016` installer/local layout and rollback risk.

## Non-Couplings and False Positives

Not every mention of Claude or Codex is a material coupling.

False positives:

- Documentation references to Claude Code as current engine are evidence, not adapter behavior by themselves.
- A `CodexResearcher` agent name in the Claude release does not prove Codex runtime support.
- Generic mentions of MCP, Bun, shell commands, or local services are not automatically Claude couplings unless they assume Claude Code behavior.
- PAI doctrine markdown can be engine-neutral if authority and state semantics are preserved.
- Pulse as Life Dashboard is not inherently Claude-specific; its current job identity and hook routes are coupled.

## Unknowns for Architect Review

Open questions:

- Which future Codex-native authority surface should carry `PAI_SYSTEM_PROMPT.md` doctrine without demotion?
- Whether a future compact Codex `AGENTS.md` should exist at all, and where.
- How to represent Codex-originated Pulse events without overloading `type = "claude"`.
- Whether PAI commands should become Codex skills, MCP tools, plugin material, docs, or a future native command surface.
- Which parts of the skills and agents tree are behaviorally reusable after semantic transformation.
- What single-writer mechanism is acceptable for PAI Memory, ISA, Pulse state, and work state.

## Non-Goals

S6 does not implement decoupling, create runtime adapter seams, create root `AGENTS.md`, create `.codex/`, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create migration scripts, inspect private user-local state, start Pulse, run installers, run Codex import or migration tooling, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, claim Codex is drop-in today, or claim Codex is the official upstream engine.
