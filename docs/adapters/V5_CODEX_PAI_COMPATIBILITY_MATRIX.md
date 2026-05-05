# V5 Codex PAI Compatibility Matrix

## Purpose

This document maps PAI v5.0.0 runtime surfaces to current Codex-native surfaces using the S2 evidence set.

This is design and evidence only. It does not implement a Codex adapter, create runtime adapter files, modify release files, modify `.codex/`, modify `.claude/`, inspect private user-local state, run Codex import or migration tooling, or authorize runtime behavior.

## Executive Answer

Is Codex a drop-in replacement today for existing local PAI v5 files?

No. Codex is not currently proven drop-in for existing local PAI v5 files.

S2 finds that Codex has native surfaces that can support a future designed adapter: local CLI, IDE, cloud tasks, `codex exec`, SDK threads, config, AGENTS.md, sandboxing, approvals, rules, hooks, MCP, skills, subagents, GitHub integration, optional memories, and resumable sessions.

S2 also finds that PAI v5.0.0 is currently Claude Code-native. The current PAI launcher, inference path, settings, hooks, skills, agents, commands, Pulse job semantics, and instruction authority stack are not Codex-native. Replacement remains plausible only through a designed adapter, not by copying Claude-shaped files.

## Compatibility Labels

| Label | Meaning |
| --- | --- |
| `native` | Codex has an official native surface that can plausibly carry the responsibility, subject to later adapter tests. |
| `partial` | Codex has an adjacent native surface, but behavior-preserving transformation or missing semantics remain. |
| `gap` | Official Codex docs consulted for S2 do not document a native counterpart for the PAI surface. |
| `blocked` | Surface cannot be treated as compatible until an architect-approved gate is satisfied. |
| `out-of-scope` | Not evaluated in S2 because it would require implementation, private state, migration tooling, or non-official evidence. |

No label authorizes implementation.

## Evidence Key

Codex evidence is recorded in `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`.

PAI evidence comes from:

- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`
- `docs/adapters/V5_UPSTREAM_RISK_REGISTER.md`
- `docs/adapters/V5_CODEX_GOAL_RUNBOOK.md`

## Matrix Summary

| Area | S2 Label | Summary |
| --- | --- | --- |
| Local execution client | `partial` | Codex CLI/IDE/exec/SDK are native, but PAI launcher and inference still target Claude Code. |
| Instruction authority | `partial` | Codex AGENTS.md exists, but PAI_SYSTEM_PROMPT.md authority ordering needs an explicit equivalent. |
| Settings and permissions | `partial` | Codex config, sandbox, approvals, and rules exist, but Claude `settings.json` is not portable. |
| Hooks and lifecycle | `partial` | Codex hooks overlap some lifecycle needs, but event payloads and enforcement semantics differ. |
| Pulse | `blocked` | Codex has no documented native PAI Pulse equivalent; Pulse bridge and job identity are required. |
| PAI Memory and ISA | `blocked` | PAI Memory and ISA are canonical PAI state; Codex memory/session state is separate. |
| Skills and agents | `partial` | Codex skills and subagents exist, but Claude-shaped files require transformation and tests. |
| Commands | `gap` | Codex has built-in slash commands, not a proven native equivalent for PAI command files. |
| Existing local v5 safety | `blocked` | Read-only trial, single-writer policy, provenance, and rollback are required before live writes. |

## Detailed Compatibility Matrix

| ID | PAI v5 Surface | PAI Evidence | Codex-Native Surface | Codex Evidence | Label | Compatibility Judgment | Required Future Gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M-001 | Canonical v5 runtime payload | S0 identifies `Releases/v5.0.0/.claude/` as the canonical upstream baseline and current Claude Code-native payload. | Codex has local and cloud agent clients, but no documented PAI v5 payload loader. | S2 evidence: C-CLI, C-IDE, C-WEB. | `blocked` | Codex cannot be treated as a drop-in consumer of the release payload. | Architect-approved adapter spec and fixture validation. |
| M-002 | Official engine identity | S1 states Claude Code remains the current official/full-support upstream engine. | Codex is a replacement-capable beta candidate only in the S1 strategy. | S2 evidence: native Codex clients exist, but OpenAI docs do not define PAI official engine status. | `blocked` | Codex is not the official upstream PAI engine today. | Explicit maintainer decision after replacement-grade validation. |
| M-003 | `PAI/TOOLS/pai.ts` launcher | S0 reports `pai.ts` launches `claude` and appends `PAI_SYSTEM_PROMPT.md` with a Claude Code flag. | Codex CLI, `codex exec`, and SDK can launch local Codex work. | S2 evidence: C-CLI, C-NONINTERACTIVE, C-SDK. | `partial` | Native Codex launch surfaces exist, but current PAI launcher behavior is Claude-specific. | Launcher adapter design, authority mapping, and no live install edits. |
| M-004 | `PAI/TOOLS/Inference.ts` | S0 reports `Inference.ts` shells out to `claude`, uses Claude model names, and assumes Claude Code subscription routing. | Codex has CLI, non-interactive execution, SDK threads, and configurable models. | S2 evidence: C-CLI, C-NONINTERACTIVE, C-SDK, C-CONFIG. | `partial` | Codex has execution surfaces, but PAI inference semantics, model mapping, auth, output parsing, and routing require a native provider contract. | Inference adapter contract and regression tests. |
| M-005 | `PAI_SYSTEM_PROMPT.md` authority layer | S0/S1 identify it as high-authority doctrine above `CLAUDE.md`, not ordinary markdown. | Codex reads global and project AGENTS.md guidance and config-defined project docs. | S2 evidence: C-AGENTS, C-CONFIG, C-CONFIG-REF. | `partial` | Codex has instruction routing, but no S2 proof of equivalent high-authority ordering for PAI doctrine. | Authority-equivalence spec with conflict tests. |
| M-006 | `CLAUDE.md` operational procedures | S0 identifies `CLAUDE.md` as Claude Code operational procedures below `PAI_SYSTEM_PROMPT.md`. | Codex AGENTS.md can hold project guidance and layered overrides. | S2 evidence: C-AGENTS. | `partial` | A future Codex AGENTS.md can route to PAI doctrine, but must not clone `CLAUDE.md`. | Native instruction router spec. |
| M-007 | Claude Code `settings.json` | S0 reports Claude Code settings schema, permissions, hooks, HTTP hook allowlists, status line, and plugin config. | Codex `config.toml`, approvals, sandbox, rules, hooks, MCP, and profiles. | S2 evidence: C-CONFIG, C-CONFIG-REF, C-SECURITY, C-RULES, C-HOOKS, C-MCP. | `partial` | Codex has native configuration and security controls, but Claude settings cannot be copied or syntactically translated without semantics. | Settings/security mapping spec and fail-closed tests. |
| M-008 | Claude Code permissions | S0 reports permissions for Claude tools such as Task, Skill, Agent, TodoWrite, and hook-related behavior. | Codex sandbox modes, approval policies, rules, protected paths, MCP tool allow/deny lists. | S2 evidence: C-SECURITY, C-SANDBOX, C-RULES, C-MCP. | `partial` | Security intent can be mapped only by behavior, not by copying permission names. | Least-privilege policy and protected-path tests. |
| M-009 | Claude hooks | S0 reports Claude lifecycle hooks, including prompt processing and context-loading behavior. | Codex hooks support `SessionStart`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `UserPromptSubmit`, and `Stop`, behind a feature flag. | S2 evidence: C-HOOKS. | `partial` | Codex hook events overlap some lifecycle points, but payloads, ordering, concurrency, and enforcement differ. | Hook event compatibility matrix and unsupported-event list. |
| M-010 | Hook `additionalContext` behavior | S0 reports PAI prompt processing emits Claude Code `additionalContext` for `UserPromptSubmit`. | Codex hooks can add extra developer context for selected events; `PreToolUse` is a guardrail, not complete enforcement. | S2 evidence: C-HOOKS. | `partial` | Some context-injection behavior may be possible, but exact behavior must be tested natively. | Context-injection spec and fixture proof. |
| M-011 | Pulse daemon and dashboard | S0 states Pulse is central v5 infrastructure on port `31337` for dashboard, observability, voice, hooks, jobs, and event APIs. | Codex clients produce agent output, diffs, transcripts, hooks, and cloud task logs; no PAI Pulse equivalent is documented. | S2 evidence: C-CLI, C-CLOUD-ENV, C-HOOKS. | `blocked` | Pulse parity cannot be claimed from Codex native surfaces. | Pulse bridge schema, event identity, and dashboard parity tests. |
| M-012 | Pulse job identity | S0 reports Pulse has Claude job semantics. | Codex has cloud tasks, CLI runs, non-interactive runs, SDK threads, and subagents. | S2 evidence: C-WEB, C-NONINTERACTIVE, C-SDK, C-SUBAGENTS. | `blocked` | Codex activity needs explicit PAI adapter job identity; it must not overload Claude job identity. | Architect-approved Codex or adapter job type. |
| M-013 | PAI Memory | S0 states PAI Memory under PAI state is canonical PAI state. | Codex memories are optional product memory under Codex home and are off by default. | S2 evidence: C-MEMORY; PAI evidence: P-S0, P-S1-BOUNDARY. | `blocked` | Codex memory is not PAI Memory. Product memories must not be silently promoted into PAI Memory. | Memory boundary, provenance, curation, and single-writer policy. |
| M-014 | ISA artifacts | S0 states ISA is the system-of-record primitive and canonical PAI state. | Codex has plans, transcripts, thread resume, and goal-like orchestration state, but no native ISA surface. | S2 evidence: C-CLI, C-SDK; PAI evidence: P-S0, P-S1-RUNTIME. | `blocked` | Codex plans or `/goal` completion are not ISA acceptance. | ISA read/write policy and single-writer gate. |
| M-015 | Algorithm doctrine | S0 identifies Algorithm v6.3.0 as execution doctrine. | Codex can read project instructions and repository docs when included in context. | S2 evidence: C-AGENTS, C-CLI, C-IDE. | `partial` | Doctrine can be surfaced to Codex, but authority and ordering need a native design. | Doctrine routing and conflict-resolution tests. |
| M-016 | Skills | S0 reports Claude-shaped skills under `.claude/skills/`. | Codex skills use `SKILL.md`, progressive disclosure, explicit `$skill` invocation, implicit matching by description, and repository/user/admin/system locations. | S2 evidence: C-SKILLS. | `partial` | Codex has a native skill system, but Claude skills must be transformed semantically and cannot be copied directly. | Skill transformation spec and activation tests. |
| M-017 | Agents | S0 reports Claude agent frontmatter with model, isolation, permissions, max turns, and Pulse voice calls. | Codex supports explicit subagents, built-in roles, and custom agent TOML under Codex locations. | S2 evidence: C-SUBAGENTS. | `partial` | Codex subagents are adjacent but not equivalent to Claude agents. | Agent role, permission, isolation, and Pulse-call mapping tests. |
| M-018 | Commands | S0 reports Claude command files and references to Claude tools such as `Skill(...)`. | Codex has built-in CLI and IDE slash commands for client control. | S2 evidence: C-CLI-SLASH, C-IDE-SLASH. | `gap` | Official Codex docs consulted do not prove a native equivalent for PAI's repository command files. | Command surface decision: transform into skills, docs, MCP, plugin, or future native command format. |
| M-019 | MCP and external tools | S0 reports PAI CLI-first tools and Pulse HTTP surfaces. | Codex supports MCP servers in CLI and IDE, stdio and HTTP transports, env vars, OAuth, and allow/deny lists. | S2 evidence: C-MCP. | `partial` | MCP is a plausible future tool bridge, but PAI tools and Pulse endpoints need explicit contracts. | MCP/tool bridge spec, side-effect annotations, and approval tests. |
| M-020 | Web search and internet | PAI S0 does not identify web search as a replacement-critical state surface; Pulse and tools may need network behavior later. | Codex has web search and configurable local/cloud network access. | S2 evidence: C-IDE, C-SECURITY, C-CLOUD-NET. | `partial` | Native network/web surfaces exist but increase prompt-injection and exfiltration risk. They do not imply Pulse parity. | Network policy with allowlist and threat model. |
| M-021 | Multimodal/image input | PAI release includes visual assets, but S0 does not make them a core runtime compatibility blocker. | Codex CLI/IDE can accept screenshots/images; IDE can generate or edit images. | S2 evidence: C-CLI, C-IDE. | `out-of-scope` | Useful for future design work, not a central PAI replacement lane in S2. | None for S2. |
| M-022 | GitHub and review workflow | PAI S0 notes repo governance separately from runtime state. | Codex can review PRs, respond to `@codex review`, and start cloud tasks from GitHub comments. | S2 evidence: C-GITHUB, C-WEB. | `native` | Native Codex GitHub review is useful for adapter development governance, not local PAI runtime substitution. | Use only in future implementation/review milestones. |
| M-023 | Existing local v5 read-only trial | S1 requires safe read-only trial before live writes. | Codex has read-only sandbox modes and `codex exec` defaults to read-only in automation. | S2 evidence: C-NONINTERACTIVE, C-SECURITY, C-SANDBOX. | `partial` | Read-only trial is plausible, but S2 does not inspect live local state and does not create a harness. | Fixture-root guard, live-root denylist, and read-only proof. |
| M-024 | Assisted patch mode | S1 describes Codex proposing changes while another approved actor applies them. | Codex can produce diffs and PRs in CLI/cloud/GitHub workflows. | S2 evidence: C-CLI, C-WEB, C-GITHUB. | `partial` | Proposal-only workflows are plausible, but PAI acceptance must remain external and explicit. | Provenance and human-acceptance workflow. |
| M-025 | Controlled single-writer mode | S1 requires a single-writer policy before Codex writes canonical PAI state. | Codex has sandbox and approval controls but no PAI-specific writer ownership model. | S2 evidence: C-SECURITY, C-SANDBOX. | `blocked` | Native sandboxing is not a PAI state lock. | Single-writer lock or lease design with rollback. |
| M-026 | Codex-only replacement mode | S1 permits only future replacement-grade validation. | Codex has local clients and automation surfaces. | S2 evidence: all Codex client evidence. | `blocked` | Codex-only replacement is not supported by S2 evidence. | Full replacement readiness criteria and architect approval. |
| M-027 | Dual-engine coexistence | S1 requires one writer per canonical PAI state surface and separate product memories. | Codex config and memory are separate from Claude, and Claude can remain installed. | S2 evidence: C-CONFIG, C-MEMORY; PAI evidence: P-S1-BOUNDARY. | `partial` | Coexistence is plausible if state ownership is explicit; memory does not merge. | Engine provenance labels and owner map. |
| M-028 | Rollback and reversibility | S1 requires future Codex replacement to be reversible and not require uninstalling Claude Code. | Codex native docs show separate Codex home/config, but no PAI rollback feature. | S2 evidence: C-CONFIG; PAI evidence: P-S1-RUNTIME, P-S1-BOUNDARY. | `blocked` | Separate Codex config helps, but rollback is an adapter obligation. | Reversible installer/launcher proof and restore tests. |
| M-029 | Installer behavior | S0 reports current installer overlays Claude Code home and verifies/installs Claude Code. | Codex docs describe configuring Codex clients, not installing PAI. | S2 evidence: C-CONFIG, C-CLI, C-IDE. | `blocked` | No Codex adapter installer can be inferred from Codex docs. | Future installer design; no release or protected-path edits in S2. |
| M-030 | User-local private state | S0/S1 protect `~/.claude/`, `~/.claude/PAI/`, `~/.claude/projects/`, `~/.codex/`, and `~/.codex/memories/`. | Codex stores config, sessions, and optional memories under Codex home. | S2 evidence: C-CONFIG, C-CLI, C-MEMORY. | `blocked` | S2 does not inspect private user-local state. Future trials must deny accidental reads and writes. | Privacy policy, explicit consent model, and fixture-first validation. |

## Existing Local v5 User Mode Matrix

| Mode | S1 Definition | S2 Codex Evidence | S2 Label | S2 Judgment |
| --- | --- | --- | --- | --- |
| Read-only trial mode | Codex reasons over copied or explicitly read-only existing local v5 files. | Codex has read-only sandbox modes and `codex exec` defaults to read-only in automation. | `partial` | Plausible future first live mode, but blocked until fixture-root and live-root guards exist. |
| Assisted patch mode | Codex proposes changes while another approved actor applies them. | Codex can produce diffs, PRs, and final outputs. | `partial` | Plausible for advisory workflows, but accepted PAI writes must remain outside Codex until policy exists. |
| Controlled single-writer mode | Codex writes selected PAI state under lock or lease. | Codex sandboxing and approvals do not define PAI writer ownership. | `blocked` | Requires a single-writer policy, provenance, rollback, and tests. |
| Codex-only replacement mode | Codex is selected as local engine after replacement-grade validation. | Codex has local clients but no drop-in PAI runtime proof. | `blocked` | Not S2-ready. Requires all replacement readiness criteria. |
| Dual-engine coexistence mode | Claude Code and Codex are both available with one writer per canonical state surface. | Codex memory/config/session state are separate from PAI state. | `partial` | Plausible only with owner labels and no silent memory promotion. |

## Adapter Lane Matrix

| Adapter Lane | Current PAI Need | Closest Codex Native Surface | S2 Label | Primary Gap |
| --- | --- | --- | --- | --- |
| Authority | Preserve `PAI_SYSTEM_PROMPT.md` as high-authority doctrine. | AGENTS.md and project instruction discovery. | `partial` | Need proven high-authority ordering and conflict handling. |
| Launcher | Replace Claude launcher behavior safely. | CLI, `codex exec`, SDK. | `partial` | Need native launch contract without modifying release or live install. |
| Inference | Replace Claude model/auth/output path. | CLI/SDK/model config. | `partial` | Need provider contract and output compatibility tests. |
| Hooks/events | Preserve context, guards, and lifecycle behavior. | Codex hooks. | `partial` | Need payload/event semantics and enforcement proof. |
| Pulse | Maintain central daemon observability and jobs. | No native Pulse counterpart. | `blocked` | Need Pulse bridge and job identity. |
| Memory | Protect PAI Memory as canonical state. | Codex optional memories and session state. | `blocked` | Codex memory is not PAI Memory; writes require single-writer policy. |
| ISA | Preserve ISA as system of record. | No native ISA counterpart. | `blocked` | Need no-shadow-ISA policy and writer control. |
| Skills | Preserve workflow activation semantics. | Codex skills. | `partial` | Need semantic transformation and tests. |
| Agents | Preserve role, model, permissions, isolation, max-turn behavior. | Codex subagents/custom agents. | `partial` | Need role and permission mapping. |
| Commands | Preserve PAI command behavior. | Built-in Codex slash commands. | `gap` | Need future command strategy; built-ins are not PAI command files. |
| Settings/security | Preserve security intent. | Config, sandbox, approvals, rules. | `partial` | Need native policy mapping and fail-closed behavior. |
| Installer/rollback | Preserve Claude fallback and reversibility. | Separate Codex config/home. | `blocked` | Need reversible installer/launcher design. |

## Unsupported or Unproven Direct Mappings

The following direct mappings are not supported by S2 evidence:

- `Releases/v5.0.0/.claude/` to `.codex/`
- `CLAUDE.md` to `AGENTS.md` as a direct clone
- Claude Code `settings.json` to Codex `config.toml` as a direct translation
- Claude hooks to Codex hooks without event and payload tests
- Claude skills to Codex skills by copying file shape
- Claude agents to Codex custom agents or subagents by copying frontmatter
- Claude commands to Codex slash commands by name matching
- Pulse Claude jobs to Codex tasks without explicit job identity
- PAI Memory to Codex memory
- ISA acceptance to Codex plan, transcript, resume, or `/goal` completion

## Replacement Readiness Criteria

Codex replacement readiness remains unproven until all of these gates pass:

- Authority-equivalence gate for `PAI_SYSTEM_PROMPT.md`.
- Launcher and inference adapter contract.
- Settings/security mapping with fail-closed permissions.
- Hook event compatibility matrix and unsupported-event disclosure.
- Pulse bridge with engine identity, mode labels, and job identity.
- PAI Memory read/write boundary with no silent product-memory promotion.
- ISA read/write boundary with no shadow acceptance artifacts.
- Skill, agent, and command transformation specs with tests.
- Existing local v5 read-only trial harness.
- Single-writer policy for all canonical PAI state writes.
- Rollback and reversibility proof that keeps Claude Code usable.
- Architect approval that Codex may move from candidate evidence to implementation.

## S2 Final Judgment

Codex is replacement-capable only as a future adapter target. It is not currently proven drop-in for existing local PAI v5 files, and it is not the official upstream engine for PAI v5.0.0.

The correct next posture is native-surface adapter design: map behavior into Codex-native surfaces with explicit evidence, tests, single-writer controls, Pulse bridge design, and rollback proof. Claude-shaped files must not be copied directly into Codex surfaces.
