# V5-S0 Discovery Report

## Executive Finding

PAI v5.0.0 is a Claude Code-native release whose canonical upstream baseline is `Releases/v5.0.0/.claude/`. The evidence shows a Life OS architecture with Pulse, Algorithm, ISA, Memory, hooks, skills, agents, settings, and `PAI_SYSTEM_PROMPT.md` all wired into Claude Code's home directory and runtime model.

Required S0 conclusions:

1. Codex is not proven drop-in for existing local PAI v5 files at S0.
2. Codex replacement is plausible only as a designed adapter, not by copying Claude files.
3. PAI memory, Claude Code memory, Codex memory, and Codex goal state are separate state surfaces.
4. PAI memory and ISA artifacts must be treated as canonical PAI state.
5. Product memories must not be silently promoted into PAI memory.
6. Future Codex replacement must be reversible and safe for users who already have local v5 files.
7. Future Codex replacement must not require uninstalling Claude Code.
8. Future Codex replacement must have a single-writer policy for PAI state before writes are allowed.
9. Pulse must be treated as central v5 infrastructure, not optional trivia.
10. `PAI_SYSTEM_PROMPT.md` must be treated as high-authority doctrine, not ordinary markdown.

## Repository State

Baseline:

- Initial `git status --short` produced no repository changes.
- `Releases/v5.0.0/.claude` exists.
- `Releases/v5.0.0/README.md` exists.
- Required pre-edit `git diff --name-only`, `git diff --check`, and protected-path status checks produced no output.
- `docs/` did not exist before this S0 task, so `docs/adapters/` was created only to hold the two required files.

Final verification after creating the docs:

- `git status --short` lists only `docs/adapters/V5_S0_DISCOVERY_PLAN.md` and `docs/adapters/V5_S0_DISCOVERY_REPORT.md` as intent-to-add files.
- `git diff --name-only | sort` lists exactly the two required docs.
- `git diff --check` produced no output.
- `test -f` passed for both required docs.
- Protected-path status produced no output.

Release inventory:

- `find Releases/v5.0.0 -type f | wc -l` reported `1552` files.
- `find Releases/v5.0.0 -type d | wc -l` reported `584` directories.
- `find Releases/v5.0.0/.claude -maxdepth 5 -type f | wc -l` reported `1266` files.
- Top-level release files are `README.md`, `algorithm-current-to-ideal.jpg`, `da-at-center.jpg`, `isa-twelve-sections.jpg`, `pai-stack.jpg`, and `skills-constellation.jpg`.
- Top-level release directories are `Releases/v5.0.0/.claude` and `Releases/v5.0.0/.claude/test-results`.

## Files Inspected

Required command evidence was collected from:

- `git status --short`
- `test -d Releases/v5.0.0/.claude`
- `test -f Releases/v5.0.0/README.md || true`
- `find Releases/v5.0.0 -maxdepth 4 -type f | sort | sed -n '1,300p'`
- `find Releases/v5.0.0/.claude -maxdepth 5 -type f | sort > /tmp/pai-v5-files.txt`
- `sed -n '1,300p' /tmp/pai-v5-files.txt`
- Required broad `rg` search over `Releases/v5.0.0`
- `git diff --name-only`
- `git diff --check`
- Protected-path `git status --short -- Releases/ .claude/ PAI/ CLAUDE.md AGENTS.md .codex/ install.sh settings.json hooks/ skills/ subagents/`

Targeted evidence files inspected:

- `Releases/v5.0.0/README.md`
- `Releases/v5.0.0/.claude/README.md`
- `Releases/v5.0.0/.claude/CLAUDE.md`
- `Releases/v5.0.0/.claude/settings.json`
- `Releases/v5.0.0/.claude/install.sh`
- `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md`
- `Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts`
- `Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts`
- `Releases/v5.0.0/.claude/hooks/README.md`
- `Releases/v5.0.0/.claude/hooks/LoadContext.hook.ts`
- `Releases/v5.0.0/.claude/hooks/PromptProcessing.hook.ts`
- `Releases/v5.0.0/.claude/hooks/lib/paths.ts`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/PAISystemArchitecture.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/ARCHITECTURE_SUMMARY.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Algorithm/AlgorithmSystem.md`
- `Releases/v5.0.0/.claude/PAI/ALGORITHM/LATEST`
- `Releases/v5.0.0/.claude/PAI/ALGORITHM/v6.3.0.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa/IsaSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md`
- `Releases/v5.0.0/.claude/skills/ISA/SKILL.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md`
- `Releases/v5.0.0/.claude/PAI/MEMORY/README.md`
- `Releases/v5.0.0/.claude/PAI/MEMORY/*/README.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Observability/ObservabilitySystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Tools/CliFirstArchitecture.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Tools/Tools.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Config/ConfigSystem.md`
- `Releases/v5.0.0/.claude/PAI/PAI-Install/README.md`
- `Releases/v5.0.0/.claude/PAI/PAI-Install/engine/actions.ts`
- `Releases/v5.0.0/.claude/PAI/PAI-Install/engine/config-gen.ts`
- `Releases/v5.0.0/.claude/PAI/PAI-Install/engine/detect.ts`
- `Releases/v5.0.0/.claude/agents/Engineer.md`
- `Releases/v5.0.0/.claude/commands/context-search.md`

No user-local private state was read.

## V5 Architecture Evidence

The v5 release README names PAI v5.0.0 as a Life Operating System with a unified daemon, Life Dashboard, personalized Digital Assistant, and execution algorithm (`Releases/v5.0.0/README.md:3-5`). The same README lists Skills, Hooks, Workflows, Algorithm v6.3.0, Memory v7.6, and Pulse as release-level components (`Releases/v5.0.0/README.md:7-15`).

The architecture graphic alt text describes a three-layer stack: engines at the bottom, the PAI context-based Life OS in the middle, and the human/life domains at the top (`Releases/v5.0.0/README.md:19`). This is important because it indicates an engine layer exists conceptually, but the shipped implementation is still Claude Code-wired.

`PAISystemArchitecture.md` is explicitly the authoritative architecture reference (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/PAISystemArchitecture.md:1-5`). It gives the installed directory structure under `~/.claude/`, including `CLAUDE.md`, `settings.json`, hooks, skills, agents, commands, and `PAI/` (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/PAISystemArchitecture.md:15-34`). The architecture summary records current versions as PAI 5.0.0, Algorithm v6.3.0, and Memory v7.6 (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/ARCHITECTURE_SUMMARY.md:6-13`).

The main v5 directories observed under `.claude` are:

- `PAI/ALGORITHM`
- `PAI/DOCUMENTATION`
- `PAI/MEMORY`
- `PAI/PAI-Install`
- `PAI/PULSE`
- `PAI/TEMPLATES`
- `PAI/TOOLS`
- `PAI/USER`
- `agents`
- `commands`
- `hooks`
- `skills`
- `test-results`

## Authority Layers

The architecture docs define a four-layer instruction hierarchy:

- Layer 1: `PAI/PAI_SYSTEM_PROMPT.md` as the highest authority system prompt, loaded via `--append-system-prompt-file`.
- Layer 2: `~/.claude/CLAUDE.md` as operational procedures.
- Layer 3: `@` imported identity/project/system files.
- Layer 4: dynamic context from `LoadContext.hook.ts`.

Evidence: `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/PAISystemArchitecture.md:125-148`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/ARCHITECTURE_SUMMARY.md:67-73`.

The v5 README states that `PAI/PAI_SYSTEM_PROMPT.md` is loaded above `CLAUDE.md` and encodes non-negotiable behavioral rules (`Releases/v5.0.0/README.md:86`, `Releases/v5.0.0/README.md:257-268`). `CLAUDE.md` says constitutional rules live in `PAI/PAI_SYSTEM_PROMPT.md`, while `CLAUDE.md` provides operational procedures and templates (`Releases/v5.0.0/.claude/CLAUDE.md:70-83`).

The Algorithm and ISA add state/doctrine authority:

- Algorithm v6.3.0 is the execution doctrine and universal current-state-to-ideal-state engine (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Algorithm/AlgorithmSystem.md:1-13`).
- ISA is the system-of-record primitive for work and projects (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa/IsaSystem.md:15-25`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md:1-10`).

## Runtime Surfaces

The v5 runtime surfaces include:

- Claude Code home and settings: `~/.claude/CLAUDE.md`, `~/.claude/settings.json`, hooks, skills, agents, commands (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/PAISystemArchitecture.md:15-34`).
- `settings.json` permissions, hooks, HTTP hook allowlist, status line, and plugin configuration (`Releases/v5.0.0/.claude/settings.json:1-84`, `Releases/v5.0.0/.claude/settings.json:221-372`).
- Hooks across Claude Code lifecycle events (`Releases/v5.0.0/.claude/hooks/README.md:23-31`, `Releases/v5.0.0/.claude/hooks/README.md:39-90`).
- Pulse daemon on port `31337` for dashboard, observability, voice, hooks, jobs, and event APIs (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md:1-13`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md:34-71`).
- PAI tools under `PAI/TOOLS/`, including `pai.ts` launcher and `Inference.ts` (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Tools/Tools.md:1-16`).

## Claude-Specific Surfaces

The release is Claude-specific in these surfaces:

- Installer requirements and flow verify or install Claude Code (`Releases/v5.0.0/README.md:31`, `Releases/v5.0.0/README.md:302-308`, `Releases/v5.0.0/.claude/PAI/PAI-Install/README.md:31-42`, `Releases/v5.0.0/.claude/PAI/PAI-Install/engine/actions.ts:902-923`).
- Install location is `~/.claude/`; existing `~/.claude/` is backed up and overlaid (`Releases/v5.0.0/README.md:31`, `Releases/v5.0.0/README.md:280-284`, `Releases/v5.0.0/.claude/README.md:29-38`, `Releases/v5.0.0/.claude/PAI/PAI-Install/engine/actions.ts:605-664`).
- `settings.json` declares the Claude Code settings schema and Claude tool permissions such as `Task`, `Skill`, `Agent(...)`, `TodoWrite`, `EnterPlanMode`, and Claude hook events (`Releases/v5.0.0/.claude/settings.json:1-84`, `Releases/v5.0.0/.claude/settings.json:277-360`).
- `pai.ts` launches `claude` and appends `PAI_SYSTEM_PROMPT.md` using Claude Code's `--append-system-prompt-file` flag (`Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts:1-18`, `Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts:391-404`).
- `Inference.ts` shells out to `claude`, uses Claude model names (`haiku`, `sonnet`, `opus`), and intentionally scrubs Anthropic API env vars to route through Claude Code subscription behavior (`Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts:1-36`, `Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts:85-140`).
- `PromptProcessing.hook.ts` emits Claude Code `additionalContext` for `UserPromptSubmit` and classifies modes/tier through a Claude inference path (`Releases/v5.0.0/.claude/hooks/PromptProcessing.hook.ts:58-65`, `Releases/v5.0.0/.claude/hooks/PromptProcessing.hook.ts:734-766`, `Releases/v5.0.0/.claude/hooks/PromptProcessing.hook.ts:923-1068`).
- Agent definitions are Claude-agent format with frontmatter fields such as `model`, `isolation`, `permissions`, and `maxTurns`, and they invoke Pulse voice curls (`Releases/v5.0.0/.claude/agents/Engineer.md:1-34`, `Releases/v5.0.0/.claude/agents/Engineer.md:72-80`).
- Commands reference the Claude Code `Skill(...)` tool directly (`Releases/v5.0.0/.claude/commands/context-search.md:1-19`).
- Pulse `claude` job type spawns Claude CLI for scheduled reasoning jobs (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md:105-119`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md:183-189`).

## Potentially Engine-Neutral Surfaces

The evidence suggests these surfaces may be engine-neutral or adaptable with lower semantic risk:

- PAI doctrine and architecture docs: Life OS, Algorithm, ISA, Memory, Pulse, Tools, Config docs are markdown doctrine rather than Claude runtime code (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/ARCHITECTURE_SUMMARY.md:14-45`).
- ISA format and ISA state model: the ISA is a file-shape contract and system-of-record artifact independent of a specific engine if write semantics are preserved (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md:1-16`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa/IsaSystem.md:108-149`).
- PAI Memory taxonomy: `PAI/MEMORY/` is filesystem-based and typed by directories; it can be read by another engine if access rules and writer policy are defined (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:1-15`, `Releases/v5.0.0/.claude/PAI/MEMORY/README.md:1-7`).
- Pulse HTTP and dashboard surface: Pulse is a Bun daemon with HTTP endpoints and JSONL event sources; parts of the dashboard/event API may be engine-neutral if event schemas are preserved (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Observability/ObservabilitySystem.md:1-31`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Observability/ObservabilitySystem.md:187-220`).
- CLI-first principle: v5 says deterministic CLI tools should be built first, then wrapped by an AI orchestration layer; this principle is engine-neutral even though the current inference tool is Claude-specific (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Tools/CliFirstArchitecture.md:1-24`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Tools/CliFirstArchitecture.md:116-152`).

## Codex-Native Transformation Candidates

These surfaces would require Codex-native transformation before Codex can be a safe runtime engine:

- Launcher: replace or wrap `PAI/TOOLS/pai.ts` behavior that directly spawns `claude` and appends Claude system prompts (`Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts:391-404`).
- Inference: replace `Inference.ts` Claude CLI subprocesses, model names, auth assumptions, and output parsing with Codex-native equivalents (`Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts:85-140`).
- Settings: map Claude Code `settings.json` schema, permissions, hooks, statusLine, HTTP hook allowlists, and plugin fields into Codex-compatible runtime configuration (`Releases/v5.0.0/.claude/settings.json:1-84`, `Releases/v5.0.0/.claude/settings.json:277-372`).
- Hooks: adapt Claude Code hook events, stdin payloads, `additionalContext`, and fail-open/fail-closed semantics to Codex hook or MCP/tool lifecycle semantics (`Releases/v5.0.0/.claude/hooks/README.md:95-130`, `Releases/v5.0.0/.claude/hooks/PromptProcessing.hook.ts:58-65`).
- Skills and commands: translate Claude Code `Skill(...)`, slash-command, and skill-frontmatter routing into Codex skill/plugin semantics without losing activation rules (`Releases/v5.0.0/.claude/commands/context-search.md:7-19`, `Releases/v5.0.0/.claude/skills/ISA/SKILL.md:1-30`).
- Agents: transform Claude Code agent frontmatter, model names, permissions, voice startup routines, and isolation behavior (`Releases/v5.0.0/.claude/agents/Engineer.md:1-34`).
- Pulse jobs: define whether Codex participates in `type = "claude"` jobs, and if so transform scheduled reasoning jobs into an explicit `codex` job type rather than overloading Claude behavior (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md:111-119`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md:183-189`).
- State writes: define a single-writer policy for `PAI/MEMORY`, ISA frontmatter, `work.json`, observability JSONL, and user identity files before any Codex write path is enabled (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:276-300`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md:7-10`).

## Pulse Evidence

Pulse is central v5 infrastructure.

Evidence:

- README: Pulse is the Life Dashboard plus central daemon on port `31337` (`Releases/v5.0.0/README.md:52-55`).
- README headline: Pulse is one Bun process, one port, one launchd service, one log file, and it replaces prior loose services (`Releases/v5.0.0/README.md:92-108`).
- README migration and verification sections instruct users to open and health-check `http://localhost:31337` (`Releases/v5.0.0/README.md:345-369`).
- Pulse docs: Pulse is the visible surface of the Life OS and the unified daemon for cron, voice, hook validation, observability APIs, Telegram, iMessage, and GitHub work polling (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md:1-13`).
- Architecture docs: Pulse absorbs separate daemon services and exposes about 40 endpoints across observability, algorithm, life, security, knowledge, wiki, DA, voice, and hooks (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/PAISystemArchitecture.md:284-298`).
- Observability docs: the HTTP server runs inside Pulse and serves local endpoints on port `31337` (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Observability/ObservabilitySystem.md:1-6`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Observability/ObservabilitySystem.md:187-220`).
- Settings route SkillGuard and AgentGuard through Pulse HTTP hooks (`Releases/v5.0.0/.claude/settings.json:136-151`, `Releases/v5.0.0/.claude/settings.json:364-366`).

Conclusion: Pulse cannot be treated as optional trivia in any Codex replacement design.

## ISA Evidence

ISA is the work/system-of-record primitive.

Evidence:

- README: PRD to ISA migration is one of the top v5 changes, and the Ideal State Artifact replaces PRD as the unit of work (`Releases/v5.0.0/README.md:77-86`, `Releases/v5.0.0/README.md:138-159`).
- ISA system doc: ISA has five identities, including ideal state articulation, test harness, build verification, done condition, and system of record (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa/IsaSystem.md:15-25`).
- ISA format spec: "The ISA is the single source of truth for the thing being articulated" and the AI writes ISA content while hooks read ISAs to sync state (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md:1-10`).
- Algorithm doctrine: every run transitions current state to ideal state through ISCs, and the ISA is the primitive carrying done, tests, verification, and record (`Releases/v5.0.0/.claude/PAI/ALGORITHM/v6.3.0.md:5-23`).
- Two homes are defined: project-root `ISA.md` for persistent things and `MEMORY/WORK/{slug}/ISA.md` for task work (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa/IsaSystem.md:108-117`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md:53-63`).
- Hooks and Pulse read ISA state for dashboard and phase/progress sync (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa/IsaSystem.md:138-149`).

Conclusion: Codex must not create parallel acceptance artifacts or silently mutate ISA format. ISA remains canonical PAI state.

## Memory Evidence

Memory v7.6 is explicit and central.

Evidence:

- README badge and section name Memory v7.6 (`Releases/v5.0.0/README.md:12`, `Releases/v5.0.0/README.md:230-241`).
- Architecture summary current versions include Memory v7.6 (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/ARCHITECTURE_SUMMARY.md:12`).
- MemorySystem doc names version 7.6 and two storage layers: PAI MEMORY at `~/.claude/PAI/MEMORY/` and Claude Code Auto-Memory at `~/.claude/projects/<project>/memory/` (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:1-15`).
- MemorySystem directory structure includes `KNOWLEDGE`, `WORK`, `LEARNING`, `RESEARCH`, `SECURITY`, `STATE`, and `PAISYSTEMUPDATES` (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:51-106`).
- Release tree contains README placeholders for `AUTO`, `BOOKMARKS`, `DATA`, `KNOWLEDGE`, `PAISYSTEMUPDATES`, `PROJECT`, `RAW`, `REFERENCE`, `RELATIONSHIP`, `RESEARCH`, `SCRATCHPAD`, `SKILLS`, `VERIFICATION`, `WISDOM`, and `WORK`.
- `PAI/MEMORY/README.md` says fresh installs are empty by design and content is created as PAI is used (`Releases/v5.0.0/.claude/PAI/MEMORY/README.md:1-7`).
- `WORK/README.md` identifies `WORK/` as the operating record of non-trivial tasks and the home of canonical `ISA.md` artifacts (`Releases/v5.0.0/.claude/PAI/MEMORY/WORK/README.md:1-7`).
- `KNOWLEDGE/README.md` defines curated long-term semantic memory and warns that promotions into it happen only after curation (`Releases/v5.0.0/.claude/PAI/MEMORY/KNOWLEDGE/README.md:1-7`).
- `RELATIONSHIP/README.md`, `WISDOM/README.md`, `RESEARCH/README.md`, and `VERIFICATION/README.md` define major memory categories for interaction patterns, distilled insights, investigations, and proof artifacts.

Conclusion: PAI Memory is canonical PAI state. Product memory from Claude Code or Codex should not be silently promoted into `PAI/MEMORY/KNOWLEDGE` or `PAI/MEMORY/WORK`.

## PAI_SYSTEM_PROMPT Evidence

`PAI_SYSTEM_PROMPT.md` is high-authority doctrine, not ordinary markdown.

Evidence:

- README: v5 adds a top-level system prompt loaded via `--append-system-prompt-file` above `CLAUDE.md` (`Releases/v5.0.0/README.md:86`, `Releases/v5.0.0/README.md:257-268`).
- `PAI_SYSTEM_PROMPT.md` describes PAI as the Life OS and requires reading the philosophy, architecture summary, and Pulse dashboard first (`Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md:1-20`).
- `PAI_SYSTEM_PROMPT.md` states the output format rule has the highest enforcement priority (`Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md:28-44`).
- `PAI_SYSTEM_PROMPT.md` says it defines behavioral non-negotiables and is the highest authority layer, with `CLAUDE.md` below it (`Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md:183-187`).
- Architecture docs place `PAI_SYSTEM_PROMPT.md` at Layer 1 of the model input chain (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/PAISystemArchitecture.md:125-139`).
- `pai.ts` appends this file when launching Claude (`Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts:391-404`).

Conclusion: A Codex adapter must preserve the authority semantics of this file or define an explicit equivalent authority layer.

## PAI_DIR Evidence

`PAI_DIR` points to user-local PAI state, not repo docs.

Evidence:

- `settings.json` sets `PAI_DIR` to `${HOME}/.claude/PAI` and `PAI_CONFIG_DIR` to the same path in the release template (`Releases/v5.0.0/.claude/settings.json:3-10`).
- `hooks/lib/paths.ts` defines two root directories: `PAI_DIR (~/.claude/PAI)` for PAI data and Claude home `~/.claude` for Claude Code settings, skills, hooks, commands, and agents (`Releases/v5.0.0/.claude/hooks/lib/paths.ts:1-10`).
- `getPaiDir()` resolves `PAI_DIR` env first, then falls back to `~/.claude/PAI` (`Releases/v5.0.0/.claude/hooks/lib/paths.ts:28-40`).
- The installer config generator says `PAI_DIR` is the PAI subsystem directory where Memory, Algorithm, USER, TOOLS, and PULSE live, not the install root (`Releases/v5.0.0/.claude/PAI/PAI-Install/engine/config-gen.ts:19-30`).
- `settings.json` docs state `PAI_DIR` is root directory for PAI data and that hooks and skills stay in `~/.claude` (`Releases/v5.0.0/.claude/settings.json:1300-1303`).
- `PAI/statusline-command.sh` defaults `PAI_DIR` to `$HOME/.claude/PAI` and reads runtime caches under `PAI/MEMORY` (`Releases/v5.0.0/.claude/PAI/statusline-command.sh:14-24`).

Conclusion: Future Codex work must treat `PAI_DIR` as installed user-local live state, not as repo documentation.

## Existing Local v5 Trial Implications

Codex must not be run against an existing local v5 install with write privileges at S0.

Reasons:

- The installer copies and clears portions of `~/.claude` during fresh install/upgrade flows (`Releases/v5.0.0/.claude/PAI/PAI-Install/engine/actions.ts:605-664`). A replacement experiment must not replay these semantics accidentally.
- Existing installs may include user-local `PAI/USER`, `PAI/MEMORY`, settings, hooks, credentials, and identity files (`Releases/v5.0.0/.claude/README.md:29-38`, `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md:164-178`).
- Memory and ISA are live canonical PAI state; changes affect dashboard, hooks, learning, relationship memory, and future context (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:276-300`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa/IsaSystem.md:138-149`).
- Claude-specific hooks and tools can write state during lifecycle events; Codex lacks proven compatibility with these event contracts at S0 (`Releases/v5.0.0/.claude/hooks/README.md:39-90`).

Before Codex can safely run against existing local v5 files, an architect should require:

- Read-only inventory mode against a copied fixture.
- No writes to `PAI/MEMORY`, `PAI/USER`, `settings.json`, `CLAUDE.md`, hooks, skills, agents, or Pulse state.
- Explicit mapping from Claude hook payloads to Codex runtime events.
- Explicit mapping from `PAI_SYSTEM_PROMPT.md` into Codex authority semantics.
- Reversible install/uninstall behavior that does not remove Claude Code.
- A single-writer policy for PAI state.
- Rollback proof from backups or a disposable clone.

## Dual Claude/Codex Subscription Memory Implications

The repository establishes at least two memory surfaces:

- PAI Memory: `~/.claude/PAI/MEMORY/`, structured and canonical for PAI state (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:7-15`).
- Claude Code native projects/auto-memory: `~/.claude/projects/<project>/memory/` and transcripts, distinct from PAI memory (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:7-15`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:112-123`).

`PAI_SYSTEM_PROMPT.md` explicitly warns that Claude Code harness auto-memory is not a PAI surface for rules/preferences and says PAI infrastructure should be patched instead (`Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md:115-122`).

Codex memory and Codex goal state were not read because the S0 scope explicitly forbids reading `.codex/` or user-local Codex memory. They must therefore be treated as separate non-PAI state surfaces unless a future adapter explicitly bridges them.

Risks:

- A Claude Code memory note, Codex memory note, or Codex goal state could be mistaken for canonical PAI memory.
- Product memories could be promoted into `PAI/MEMORY/KNOWLEDGE` without the curation contract described by `KNOWLEDGE/README.md`.
- Two engines could write `PAI/MEMORY/WORK/{slug}/ISA.md`, `STATE/work.json`, or relationship memory concurrently.
- Subscription-specific inference behavior differs: current `Inference.ts` is Claude CLI and Anthropic subscription oriented (`Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts:35-36`, `Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts:105-140`).

Conclusion: PAI memory, Claude Code memory, Codex memory, and Codex goal state must remain distinct unless an adapter provides explicit read/write routing and provenance.

## Drop-In Replacement Assessment

Codex is not a drop-in replacement for Claude Code in PAI v5.0.0 at S0.

Blocking evidence:

- v5 installer verifies/installs Claude Code and installs into `~/.claude` (`Releases/v5.0.0/.claude/PAI/PAI-Install/README.md:31-42`, `Releases/v5.0.0/.claude/PAI/PAI-Install/engine/actions.ts:902-923`).
- v5 launcher runs `claude` and uses Claude-specific `--append-system-prompt-file` (`Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts:391-404`).
- v5 inference shells out to `claude`, uses Claude model tiers, and assumes Anthropic credential precedence (`Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts:85-140`).
- v5 settings are Claude Code settings with Claude tool names, hook events, status line, and plugin structures (`Releases/v5.0.0/.claude/settings.json:1-84`, `Releases/v5.0.0/.claude/settings.json:277-384`).
- v5 hooks depend on Claude Code lifecycle events and payloads (`Releases/v5.0.0/.claude/hooks/README.md:95-130`).
- v5 skills, commands, and agents reference Claude Code `Skill`, `Agent`, and slash-command semantics (`Releases/v5.0.0/.claude/commands/context-search.md:7-19`, `Releases/v5.0.0/.claude/agents/Engineer.md:1-34`).
- Pulse contains a Claude job type and scheduled Claude CLI invocation semantics (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md:183-189`).

Assessment:

- Drop-in: not proven and likely unsafe.
- Designed adapter: plausible.
- Copying `.claude` into `.codex`: unsafe and unsupported by S0 evidence.
- Safe replacement path: adapter-first, read-only-first, fixture-tested, reversible, single-writer before writes, and compatible with keeping Claude Code installed.

## Protected Boundary Findings

S0 respected protected boundaries.

Final protected-path command produced no output for:

- `Releases/`
- `.claude/`
- `PAI/`
- `CLAUDE.md`
- `AGENTS.md`
- `.codex/`
- `install.sh`
- `settings.json`
- `hooks/`
- `skills/`
- `subagents/`

Repository evidence supports the sensitivity of live `~/.claude`:

- `PAI_SYSTEM_PROMPT.md` declares `~/.claude` private and says its content must not reach public locations (`Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md:164-178`).
- `.gitignore` identifies private credentials, runtime state, PAI memory handling, Claude runtime directories, project transcripts, and env files (`Releases/v5.0.0/.claude/.gitignore:55-90`, `Releases/v5.0.0/.claude/.gitignore:127-215`).
- Installer docs warn existing `~/.claude` contains settings, hooks, and agents and is overlaid by PAI (`Releases/v5.0.0/.claude/README.md:29-38`).

Protected files for future phases:

- Release baselines: `Releases/`, `Releases/v5.0.0/`, `Releases/v5.0.0/.claude/`
- Installed live roots: `.claude/`, `PAI/`
- High-authority runtime files: `CLAUDE.md`, `PAI_SYSTEM_PROMPT.md`, `settings.json`
- Runtime extension surfaces: `hooks/`, `skills/`, `agents/`, `commands/`, `subagents/` if introduced
- Codex state: `.codex/` and user-local Codex memory
- Root project agent guidance: `AGENTS.md`
- Installer entrypoints: `install.sh`

## Unknowns for Architect Review

- What Codex authority layer should correspond to Claude Code `--append-system-prompt-file`?
- What Codex lifecycle events can accurately replace Claude Code `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `PreCompact`, and `SessionEnd`?
- Should Pulse gain an explicit `codex` job type rather than adapting `type = "claude"`?
- What is the minimum event schema Pulse needs from a Codex runtime for dashboard parity?
- Which PAI tools can be engine-neutralized first, and which should remain Claude-only?
- How should Codex memory and goal state be displayed, if at all, inside PAI without becoming canonical PAI state?
- What is the rollback model for an existing user with both Claude Code and Codex installed?
- What single-writer lock or lease should protect `PAI/MEMORY`, ISA files, and `STATE/work.json`?

## Recommended Next Architect Decision

Approve a V5-S1 adapter design phase, not implementation.

The next architect decision should define:

- Adapter boundaries: launcher, inference, hook/event mapping, settings mapping, skills/agents mapping, Pulse event bridge, and state writer policy.
- Safety model: read-only fixture validation first, no live user writes, no Claude uninstall, reversible setup, and explicit rollback.
- State model: PAI Memory and ISA as canonical PAI state; Claude Code memory, Codex memory, and Codex goal state as separate surfaces.
- Pulse model: Pulse remains central infrastructure and receives Codex-compatible events only through a designed bridge.
- Authority model: `PAI_SYSTEM_PROMPT.md` must retain high-authority doctrine semantics in Codex or have a formally equivalent adapter representation.

No S0 evidence supports letting Codex write existing local v5 files today.
