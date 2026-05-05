# V5 Codex Native Surface Evidence

## Purpose

This document records the current official OpenAI Codex surface evidence needed for the V5-S2 compatibility matrix between PAI v5.0.0 and Codex-native surfaces.

S2 is design and evidence only. It does not implement a Codex adapter, create runtime adapter files, modify release files, modify `.codex/`, modify `.claude/`, inspect private user-local state, run migration tooling, or authorize runtime behavior.

## Source Discipline

Codex-native facts in this document come only from official OpenAI Codex documentation.

PAI v5.0.0 facts are taken only from S0/S1 adapter evidence:

- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`
- `docs/adapters/V5_UPSTREAM_RISK_REGISTER.md`
- `docs/adapters/V5_CODEX_GOAL_RUNBOOK.md`

This document does not use observed local Codex runtime behavior as compatibility proof. It also does not inspect `~/.codex/`, `~/.codex/memories/`, `~/.claude/`, or `~/.claude/PAI/`.

## Source Index

| ID | Source | S2 Use |
| --- | --- | --- |
| C-WEB | OpenAI Codex web: `https://developers.openai.com/codex/cloud` | Cloud task and GitHub-connected repository workflow facts. |
| C-CLOUD-ENV | OpenAI Codex cloud environments: `https://developers.openai.com/codex/cloud/environments` | Cloud container, setup script, agent phase, env var, secret, cache, and internet defaults. |
| C-CLOUD-NET | OpenAI Codex agent internet access: `https://developers.openai.com/codex/cloud/internet-access` | Cloud agent internet controls, risk model, allowlist, and HTTP method limits. |
| C-CLI | OpenAI Codex CLI features: `https://developers.openai.com/codex/cli/features` | Local CLI read/edit/run behavior, image input, approvals, diffs, transcript resume. |
| C-CLI-SLASH | OpenAI Codex CLI slash commands: `https://developers.openai.com/codex/cli/slash-commands` | Built-in interactive controls such as permissions, model, agent, MCP, init, status, and plan. |
| C-IDE | OpenAI Codex IDE features: `https://developers.openai.com/codex/ide/features` | IDE local/cloud modes, shared config, approvals, web search, image input, and image generation. |
| C-IDE-SLASH | OpenAI Codex IDE slash commands: `https://developers.openai.com/codex/ide/slash-commands` | IDE slash command controls for local/cloud mode, review, status, and cloud environment. |
| C-CONFIG | OpenAI Codex config basics: `https://developers.openai.com/codex/config-basic` | User/project/system config layers, trust behavior, model, MCP, approval, and sandbox configuration. |
| C-CONFIG-REF | OpenAI Codex config reference: `https://developers.openai.com/codex/config-reference` | Config key space for approvals, sandbox, agents, MCP, tools, history, profiles, and project docs. |
| C-AGENTS | OpenAI Codex AGENTS.md guide: `https://developers.openai.com/codex/guides/agents-md` | Global and project instruction discovery, ordering, overrides, byte limits, and fallback filenames. |
| C-SANDBOX | OpenAI Codex sandbox concept: `https://developers.openai.com/codex/concepts/sandboxing` | Cross-surface sandbox model and command boundary semantics. |
| C-SECURITY | OpenAI Codex agent approvals and security: `https://developers.openai.com/codex/agent-approvals-security` | Local/cloud sandbox defaults, approval policy, workspace write behavior, protected paths, network defaults. |
| C-HOOKS | OpenAI Codex hooks: `https://developers.openai.com/codex/hooks` | Experimental hook framework, event names, matcher behavior, input/output shape, and guardrail limits. |
| C-RULES | OpenAI Codex rules: `https://developers.openai.com/codex/rules` | Experimental rules for commands outside the sandbox and config-layer loading behavior. |
| C-MCP | OpenAI Codex MCP: `https://developers.openai.com/codex/mcp` | MCP support in CLI and IDE, stdio/HTTP transports, shared config, OAuth, allow/deny lists. |
| C-SKILLS | OpenAI Codex skills: `https://developers.openai.com/codex/skills` | Skill format, progressive disclosure, invocation, repository/user/admin/system scan locations. |
| C-SUBAGENTS | OpenAI Codex subagents: `https://developers.openai.com/codex/subagents` | Parallel subagent workflow, built-in agent roles, custom agent TOML, sandbox inheritance. |
| C-MEMORY | OpenAI Codex memories: `https://developers.openai.com/codex/memories` | Optional Codex memory behavior and storage under Codex home. |
| C-NONINTERACTIVE | OpenAI Codex non-interactive mode: `https://developers.openai.com/codex/noninteractive` | `codex exec`, read-only default in automation, sandbox options, stdout/stderr behavior. |
| C-SDK | OpenAI Codex SDK: `https://developers.openai.com/codex/sdk` | Programmatic local Codex control, threads, repeated runs, and thread resume. |
| C-GITHUB | OpenAI Codex GitHub integration: `https://developers.openai.com/codex/integrations/github` | GitHub code review, `@codex review`, cloud task follow-up, PR comments, and AGENTS.md review guidance. |
| P-S0 | `docs/adapters/V5_S0_DISCOVERY_REPORT.md` | PAI v5.0.0 discovery baseline. |
| P-S1-RUNTIME | `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md` | S1 replacement strategy and adapter lanes. |
| P-S1-BOUNDARY | `docs/adapters/V5_ADAPTER_BOUNDARIES.md` | S1 boundary model and protected-state separation. |
| P-S1-RISK | `docs/adapters/V5_UPSTREAM_RISK_REGISTER.md` | S1 risk model and stop conditions. |

## Executive Evidence Summary

Official OpenAI documentation establishes Codex as a coding agent available through cloud, CLI, IDE extension, and automation surfaces. Codex has native surfaces for local repository work, cloud task execution, configuration, instruction discovery, sandboxing, approvals, MCP, hooks, rules, skills, subagents, memories, slash commands, non-interactive execution, SDK control, GitHub integration, web search, and image input/generation.

That evidence does not establish Codex as a drop-in runtime for PAI v5.0.0. The official Codex surfaces are native Codex surfaces, not Claude Code surfaces. They do not natively define PAI Memory, ISA, Pulse, Claude Code `settings.json`, Claude Code hook payloads, Claude Code skills, Claude Code agents, Claude Code commands, or PAI's current `pai.ts` and `Inference.ts` Claude launcher behavior.

S2 conclusion: Codex has enough native surface area to support future adapter design, but Codex is not currently proven drop-in for existing local PAI v5 files.

## Codex Client Surfaces

| Surface | Official Evidence | Native Facts | S2 Compatibility Consequence |
| --- | --- | --- | --- |
| Codex web/cloud | C-WEB, C-CLOUD-ENV, C-CLOUD-NET | Codex can run coding tasks in OpenAI-managed cloud environments, work in the background, use connected GitHub repositories, run setup scripts, edit code, run checks, show diffs, and open PRs. | Useful for repo-governance and cloud validation workflows, but not a local PAI runtime replacement by itself. |
| Codex CLI | C-CLI | The CLI can run in an interactive terminal UI, read a repository, make edits, run commands, show diffs, accept screenshots, queue follow-ups, and resume local transcripts. | Native local engine surface for future adapter trials, but current PAI launcher and inference paths still invoke Claude Code. |
| Codex IDE extension | C-IDE, C-IDE-SLASH | The IDE extension uses the same agent as the CLI, shares configuration, supports local and cloud modes, can reference editor files, adjust approval mode, use web search, accept images, and generate or edit images. | Useful for developer workflow and review, not a substitute for PAI runtime semantics. |
| Non-interactive CLI | C-NONINTERACTIVE | `codex exec` runs Codex from scripts and CI; by default it runs in a read-only sandbox and can be configured with explicit sandbox and approval settings. | Promising future surface for read-only trial, fixture validation, or advisory analysis, not current adapter implementation. |
| SDK | C-SDK | The SDK can programmatically start local Codex threads, run prompts, continue the same thread, and resume past threads. | Future automation lane, but any adapter use would need architect approval and tests. |

## Configuration and Instruction Surfaces

| Surface | Official Evidence | Native Facts | S2 Compatibility Consequence |
| --- | --- | --- | --- |
| Config layers | C-CONFIG, C-CONFIG-REF | Codex reads user config from `~/.codex/config.toml`, can load trusted project `.codex/config.toml` layers, and resolves values by CLI/config overrides, profiles, project config, user config, system config, and defaults. | Native config exists, but S2 may not create `.codex/` config. Claude Code `settings.json` cannot be copied into Codex config. |
| Project trust | C-CONFIG | Project `.codex/` layers load only when the project is trusted. If untrusted, Codex skips project-scoped config, hooks, and rules while user/system config still load. | Future adapter must explicitly model trusted versus untrusted local PAI trials. |
| AGENTS.md | C-AGENTS | Codex reads global and project `AGENTS.md` or `AGENTS.override.md` guidance, walks from project root to current directory, concatenates root-to-leaf, and applies byte limits and fallback filenames. | Native instruction routing exists, but a future PAI Codex `AGENTS.md` must be a compact router, not a clone of `CLAUDE.md` or `PAI_SYSTEM_PROMPT.md`. |
| Slash commands | C-CLI-SLASH, C-IDE-SLASH | CLI slash commands control the interactive session; IDE slash commands control status, local/cloud mode, review, and cloud environment. | Codex slash commands are client controls, not proven replacements for PAI's Claude command files. |
| Prompting | C-CLI, C-IDE | Official docs emphasize giving context, constraints, desired outcome, and verification commands; clients can attach files, code, screenshots, and editor context. | Useful for operator practice; does not encode PAI doctrine by itself. |

## Sandbox, Approval, and Security Surfaces

| Surface | Official Evidence | Native Facts | S2 Compatibility Consequence |
| --- | --- | --- | --- |
| Sandbox | C-SANDBOX, C-SECURITY | Codex uses a constrained environment for local commands; sandbox and approval policy work together; spawned commands inherit sandbox boundaries. | Strong candidate for future read-only trial and fixture containment, but live PAI writes still require a single-writer policy. |
| Default local security posture | C-SECURITY | Local CLI/IDE defaults include no network access and workspace-limited writes, with approvals required outside the workspace or for network access. | Native safety controls exist, but they do not automatically understand PAI Memory, ISA, or Pulse state ownership. |
| Protected paths | C-SECURITY | In workspace-write mode, protected paths include `.git`, `.agents`, and `.codex` under writable roots as read-only. | Helpful for repository safety, but PAI-specific protected paths require adapter policy and tests. |
| Rules | C-RULES | Codex rules are experimental and control which commands can run outside the sandbox; rules load under active config layers, including project `.codex/rules/` only when trusted. | Adjacent to Claude Code permissions, but syntax and lifecycle are native Codex and cannot receive copied Claude settings. |
| Internet access | C-SECURITY, C-CLOUD-NET, C-IDE | Local network is off by default unless configured; cloud agent internet is off by default during the agent phase; cloud environments can allow all domains or allowlisted domains and restrict HTTP methods. | Future Pulse or package-access behavior must be explicit. Internet access is not evidence of Pulse parity. |

## Tooling and Extension Surfaces

| Surface | Official Evidence | Native Facts | S2 Compatibility Consequence |
| --- | --- | --- | --- |
| MCP | C-MCP | Codex supports MCP servers in CLI and IDE, with stdio and streamable HTTP servers, env vars, OAuth, bearer tokens, tool allowlists, and tool denylists in config. | Candidate bridge lane for external tools, but PAI Pulse and PAI tools need explicit adapter contracts. |
| Hooks | C-HOOKS | Codex hooks are experimental, feature-flagged, and support events including `SessionStart`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `UserPromptSubmit`, and `Stop`. They receive JSON stdin. `PreToolUse` can intercept some Bash, `apply_patch`, and MCP calls but is a guardrail rather than a complete enforcement boundary. | Partial lifecycle overlap with Claude Code hooks, not drop-in parity. Event payloads and enforcement semantics require a compatibility spec. |
| Skills | C-SKILLS | Codex skills package instructions, resources, and optional scripts under a `SKILL.md`; Codex uses progressive disclosure and can invoke skills explicitly or by matching descriptions. | Native skill concept exists, but Claude skills must be transformed by semantics, not copied by file shape. |
| Subagents | C-SUBAGENTS | Codex can spawn explicit subagents, has built-in `default`, `worker`, and `explorer` roles, and can load custom agents from TOML under user or project Codex locations. Subagents inherit sandbox policy. | Adjacent to Claude Code agents, but model names, permissions, isolation, turn limits, and Pulse routines require transformation. |
| Images and multimodal input | C-CLI, C-IDE | Codex clients can accept screenshots/images as context; the IDE can generate or edit images through an image generation skill. | Useful for UX/design tasks and evidence capture, not central to PAI runtime replacement. |
| Web search | C-IDE, C-SECURITY | Codex has a first-party web search tool; cached mode is used for local IDE tasks by default, with caution about prompt injection. | Useful for research tasks when allowed, but not a PAI runtime state surface. |

## Persistence and Memory Surfaces

| Surface | Official Evidence | Native Facts | S2 Compatibility Consequence |
| --- | --- | --- | --- |
| Local transcripts and resume | C-CLI | Codex stores transcripts locally and supports `codex resume`, `codex resume --all`, `codex resume --last`, and `codex resume <SESSION_ID>`. Resumed runs keep original transcript, plan history, and approvals. | This is Codex product/session state. It is not PAI Memory, ISA, or Pulse state. |
| SDK threads | C-SDK | SDK threads can be continued with another `run()` or resumed by thread ID. | Programmatic continuity exists, but not as canonical PAI state. |
| Codex memories | C-MEMORY | Codex memories are off by default, not available in the EEA, UK, or Switzerland at launch, and can store useful context under Codex home, with main files under `~/.codex/memories/`. | Codex memory is not PAI Memory. Product memories must not be silently promoted into PAI Memory. |
| Goal-like persistence | C-CLI, C-SDK, P-S1-RUNTIME, P-S1-BOUNDARY | Official docs consulted show transcript/thread resume and optional memories. S1 separately treats Codex `/goal` state as orchestration metadata, not PAI Memory, not ISA, and not Pulse state. | Any future goal or resume state must remain non-canonical unless an explicit adapter bridge is designed and approved. |

## GitHub and Review Surfaces

| Surface | Official Evidence | Native Facts | S2 Compatibility Consequence |
| --- | --- | --- | --- |
| GitHub code review | C-GITHUB | Codex can review GitHub PR diffs, follow repository guidance, post GitHub code reviews, respond to `@codex review`, and start cloud tasks from PR comments. | Useful for repository maintenance and adapter review, but it is not a local PAI runtime engine. |
| Cloud PR workflow | C-WEB, C-GITHUB | Codex cloud can work with connected repositories and create pull requests from its work. | Useful for future implementation governance only after S2; S2 does not create PR automation or runtime code. |

## PAI v5 Evidence Summary

S0/S1 establish these PAI facts:

- PAI v5.0.0 is Claude Code-native, with canonical upstream baseline under `Releases/v5.0.0/.claude/`.
- Claude Code remains the current official/full-support upstream engine for v5.0.0 until replacement-grade validation exists.
- The current launcher and inference surfaces invoke `claude`.
- Current settings, hooks, skills, agents, and commands are Claude-shaped.
- Pulse is central v5 infrastructure, not optional background trivia.
- `PAI_SYSTEM_PROMPT.md` is high-authority doctrine, not ordinary markdown.
- PAI Memory and ISA artifacts are canonical PAI state.
- Claude Code memory, Codex memory, and Codex `/goal` or resume state are not PAI Memory.
- Future Codex replacement must be reversible, must not require uninstalling Claude Code, and must support read-only trial before writes.
- Future writes to canonical PAI state require a single-writer policy.

## Non-Evidence and Explicit Gaps

Official Codex documentation consulted for S2 does not prove:

- Codex can directly consume Claude Code `settings.json`.
- Codex can directly consume Claude Code hooks.
- Codex can directly consume Claude Code skill, agent, or command files.
- Codex can directly preserve `PAI_SYSTEM_PROMPT.md` authority ordering without an adapter.
- Codex can natively operate PAI Pulse jobs, dashboard state, or hook validation.
- Codex can natively write PAI Memory or ISA safely.
- Codex memory, Codex transcripts, Codex SDK threads, or Codex `/goal` state are PAI Memory.
- Existing local PAI v5 files can be safely modified by Codex without a read-only trial, single-writer policy, provenance, and rollback.

## S2 Evidence Judgment

Codex has substantial native surfaces for future adapter design:

- Local CLI and IDE agent execution.
- Non-interactive execution.
- SDK-driven local threads.
- Config, approval, sandbox, rules, and hooks.
- AGENTS.md instruction routing.
- MCP, skills, subagents, GitHub integration, web search, and image input.
- Optional memory and resumable session/thread state.

However, these surfaces are not Claude Code surfaces and are not PAI state surfaces. They support future adapter lanes, but they do not authorize implementation and do not establish drop-in compatibility for PAI v5.0.0.
