# Codex Adapter Adaptation Plan

PR-01 established the inventory and compatibility baseline. PR-02 added the
neutral platform/path primitive for future adapter work. Phase 3 includes
PR-03A platform parsing plus read-only Codex CLI detection, and PR-03B's
first-class Codex-selected installer boundary after detection and prerequisite
reporting. PR-04A begins Phase 4 by adding an unwired target-aware instruction
generation substrate for Claude `CLAUDE.md` compatibility and compact Codex
`AGENTS.md` router generation. PR-04A does not install or generate Codex
runtime files. This document records the evidence base for adapting PAI from a
Claude Code-only release shape into peer Claude and Codex adapters without
changing default Claude behavior.

## Non-Goals Through PR-04A

- No Codex installation path.
- No hook behavior changes.
- No Codex settings, rules, hooks, skills, agents, or runtime instruction
  installation.
- No changes to Claude settings generation output.
- No non-installer release runtime behavior changes.
- No protected governance file edits.
- No claim that Codex support is implemented.
- Existing Claude Code users have no migration action through PR-04A, and the
  default installer path remains Claude.

## Inventory Command

Run the automated inventory from the repository root:

```bash
bun Tools/platform-inventory.ts --format markdown --top 10
```

The default scan excludes development planning files under `.codex/`, root
`AGENTS.md`, the adapter docs, the inventory tool itself, and the inventory
fixtures so counts reflect product and release coupling rather than this PR's
governance text. Use `--include-planning` only when intentionally auditing
development-only files.

For safety, `--root` is confined to this repository. Direct scans of protected
planning roots such as `.codex/` also require `--include-planning`.

For a focused fixture smoke test:

```bash
bun Tools/platform-inventory.ts --root Tools/fixtures/platform-inventory --format json
```

## Evidence Reviewed

- Root governance and phase controls: `AGENTS.md`,
  `.codex/governance/ARCHITECTURE_STEWARD_PROTOCOL.md`, and
  `.codex/governance/PHASE_PLAN.md`.
- Public platform and project docs: `README.md` and `PLATFORM.md`.
- Claude release settings, installer engine files, hooks, transcript tools, and
  session tools under `Releases/*/.claude/`.
- Pack installation and pack README files under `Packs/*/`.
- Existing `Tools/` conventions for Bun TypeScript maintenance tools.

## Ten Deduplicated High-Risk Coupling Themes

The raw inventory output ranks grouped file/pattern findings, which means
repeated release copies can dominate the top 10. This section manually
deduplicates those findings into the highest-risk coupling themes for planning.

1. **PAI application home is currently conflated with `~/.claude`.**
   Current release settings, hook path helpers, transcript/session tools, pack
   installers, and backup tooling assume PAI lives inside Claude Code state.
   Codex must not use `~/.codex` as the PAI application home; later phases need
   a neutral path resolver that preserves Claude defaults and gives Codex a
   default `~/.pai` home.

2. **Claude settings hook schema drives lifecycle integration.**
   `settings.json` uses Claude event names such as `SessionStart`,
   `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, and `SessionEnd`,
   with matchers for Claude tool names. Codex hook support must be mapped
   through an adapter instead of copying this schema.

3. **Hook decision outputs are Claude-specific.**
   Security and guard hooks emit Claude decision objects such as
   `{ "continue": true }`, `{ "decision": "ask" }`, or hard blocks via
   `exit(2)`. Codex enforcement must use Codex-native rules and supported hook
   contracts, with fixtures before any parity claim.

4. **Instruction generation is named and shaped around `CLAUDE.md`.**
   Release hooks call `BuildCLAUDE.ts`, settings reference `CLAUDE.md`, and
   docs assume Claude Code loads that file. PR-04A adds an unwired compact
   Codex `AGENTS.md` router generator and keeps config merge behavior for a
   later PR.

5. **Transcript and session tools assume Claude JSONL shape and paths.**
   `TranscriptParser.ts`, `SessionHarvester.ts`, `GetTranscript.ts`, and hook
   helpers use `transcript_path`, `.jsonl`, `message.content`, `tool_use`, and
   `~/.claude/projects` assumptions. Codex transcript support needs fixtures
   before memory, learning, voice, or status integration can be claimed beyond
   `unsupported`; inventory findings should remain `unknown-needs-fixture`
   until those fixtures exist.

6. **Permissions and hooks depend on Claude tool names.**
   Tool names such as `Read`, `Write`, `Edit`, `MultiEdit`, `Task`, `Skill`,
   `AskUserQuestion`, and `Stop` appear in settings, hooks, pack docs, and
   agent workflows. Codex equivalents are not a one-for-one port, especially
   for subagents, skills, and user questions.

7. **Pack installers write to Claude skill and command locations.**
   Pack install docs create and copy into `~/.claude/skills`,
   `~/.claude/commands`, and `~/.claude/PAI/USER/...`. Codex pack support will
   need Codex skill locations and an honest compatibility label per pack.

8. **Agent workflows assume Claude `Task` and Claude subagent environment.**
   Hooks and skills reference `Task`, `CLAUDE_PROJECT_DIR`, `CLAUDE_AGENT_TYPE`,
   `subagent_type`, and `.claude/Agents`. Codex custom-agent TOML semantics
   need a separate adapter and should not reuse Claude agent markdown directly.

9. **Statusline, tab state, and terminal UI behavior are Claude-specific.**
   Release settings define `statusLine`, hooks mutate terminal/tab state, and
   transcript parsing extracts completion text for voice/status UX. Codex parity
   is unproven and should remain `unsupported` unless later implemented with
   known gaps.

10. **Claude CLI detection, prompt execution, and update checks are embedded in installer/hooks.**
    Installer detection calls `claude --version`; older update checks reference
    `@anthropic-ai/claude-code`, and any `claude -p` use is Claude prompt
    execution rather than detection. Phase 3 implements read-only Codex CLI
    detection, but Codex prompt execution and update-check mapping still need
    explicit contracts before mapping. None of that later mapping may change
    Claude default detection or require Codex for existing Claude users.

## Adapter Boundary Notes

- Non-installer Claude runtime artifacts under `Releases/*/.claude/`, including
  settings, hooks, skills, agents, transcript tools, and generated instruction
  templates, are treated as Claude adapter evidence. PR-04A touches only the
  instruction-generation tool surface and adds an explicit Codex adapter
  template; it does not wire installer runtime writes.
- `PAI_DIR` remains the legacy compatibility alias and has priority over
  `PAI_HOME` where legacy behavior requires it. Codex's default PAI application
  home is `~/.pai`; `~/.codex` is Codex CLI state/config space, not the PAI app
  home.
- Codex support should be added as new adapter behavior, with neutral core
  abstractions only where they remove duplicated platform assumptions.
- Unsupported or unverified Codex behavior must stay labeled as such in
  `COMPATIBILITY_MATRIX.md`.

## PR-02 Path Resolver Primitive

The canonical path primitive lives in the product-consumable release tree at
`Releases/v4.0.3/.claude/PAI/Tools/platform/paths.ts`, with
`Tools/platform/paths.ts` kept as a repository-tooling re-export shim. PR-02
kept it unwired; Phase 3 uses it for read-only installer detection, platform
path planning, and boundary reporting only.

Current tested semantics:

- Supported adapter identifiers are `claude` and `codex`.
- PAI application home precedence is `PAI_DIR`, then `PAI_HOME`, then the
  platform default.
- Claude defaults resolve both the PAI application home and adapter home to
  `~/.claude`, preserving the current Claude shape. If `PAI_DIR` is set for
  Claude, it preserves the legacy combined PAI/Claude home. If `PAI_HOME` is
  set without `PAI_DIR`, it moves only the neutral PAI application home; the
  Claude adapter home remains `~/.claude`.
- Codex defaults resolve the PAI application home to `~/.pai` and the Codex
  adapter/config home to `CODEX_HOME` when set, otherwise `~/.codex`.
- `~/.codex` is treated as Codex CLI state/config space, not as the default PAI
  application home.
- Home expansion covers `~`, `$HOME`, and `${HOME}`. Tests use temp-home style
  paths and do not write real user homes.
- Windows path behavior is explicitly rejected as unsupported for this phase.

## Phase 3 Installer Selection, Detection, And Boundary

PR-03A adds installer platform option parsing and state for `claude`, `codex`,
and `both`. If no platform is specified, the installer normalizes to
`platform = claude`, preserving the existing default behavior.

PR-03A selection and detection semantics:

- The outer release `install.sh` forwards user-supplied arguments to the
  TypeScript installer and still launches GUI mode when no arguments are
  supplied. The nested installer script keeps its existing headless fallback.
- Codex-containing selections skip bootstrap auto-installs for Git, Bun, and
  Claude Code. Bun must already be present so the TypeScript installer can run
  read-only detection and boundary reporting.
- `main.ts` parses `--platform claude`, `--platform codex`, `--platform both`,
  and equals-form variants. Unknown values fail with a clear parser error.
- Installer state records the selected platform and normalized target platform
  list. Legacy saved state without platform fields resumes as Claude-only.
- For Claude writer-facing installer paths, `PAI_DIR` remains the legacy
  combined PAI/Claude home. `PAI_HOME` is retained as neutral PAI planning
  metadata and does not move Claude writer targets.
- Read-only detection checks Codex only when the selected platform includes
  Codex, using `codex --version 2>&1`.
- Missing Codex CLI for `codex` or `both` reports the task-required manual
  install hints:
  `npm install -g @openai/codex` and `brew install codex`.
- Claude-only installs do not require or probe Codex.

PR-03B boundary semantics:

- Codex-selected CLI and web installs run system detection and read-only
  prerequisites, then stop at a first-class platform boundary before API key,
  identity, repository, configuration, voice, or validation steps are reached.
- `both` mode is not a partial Claude install. It runs detection and read-only
  prerequisite reporting, then stops at the same boundary with an explicit
  both-mode not-implemented message.
- Deliberate Codex boundary stops do not save resumable installer state. If a
  Claude saved state already exists, Codex-selected runs ignore it without
  clearing or overwriting it.
- Existing Claude saved-state resume and cleanup behavior remains Claude-only.
- Writer-phase fail-closed guards remain in place as a second line of defense:
  Codex-selected runs still throw before repository, configuration, or voice
  writes if those paths are reached unexpectedly.
- `install.sh --platform codex` is not a full Codex install or a supported dry
  run. It forwards the selected platform into the installer, performs read-only
  platform detection when Bun is available, and stops before unsupported Codex
  PAI writes.
- No `~/.codex`, `~/.pai`, `~/.claude`, `AGENTS.md`, `config.toml`, rules,
  hooks, skills, or agent files are generated for Codex.
- Codex installer support remains unimplemented beyond selection, detection,
  prerequisite reporting, and the not-implemented boundary.

## PR-04A Target-Aware Instruction Generation

PR-04A adds a product-consumable instruction builder at
`Releases/v4.0.3/.claude/PAI/Tools/BuildInstructions.ts`. The existing
`BuildCLAUDE.ts` file remains a compatibility entrypoint for the Claude
SessionStart hook and manual `bun PAI/Tools/BuildCLAUDE.ts` usage.

Current tested PR-04A semantics:

- The Claude target renders the same `CLAUDE.md` content as the legacy
  `BuildCLAUDE.ts` algorithm for the same `CLAUDE.md.template`,
  `settings.json`, and `PAI/Algorithm/LATEST` inputs.
- The Codex target renders a compact `AGENTS.md` router from
  `Releases/v4.0.3/.claude/PAI/Adapters/codex/AGENTS.md.template`.
- The Codex router records PAI version, algorithm version/path, PAI home,
  Codex adapter/config home, and context-routing path. It tells Codex to load
  the routing file only when task-specific PAI context is needed and to load
  the algorithm file for substantial work.
- The Codex router is intentionally not a copy of `CLAUDE.md`. It avoids
  Claude-only tool names, Claude settings semantics, Claude hook semantics, and
  Claude transcript assumptions.
- Codex `AGENTS.md` generation is unwired after PR-04A. The installer does not
  write `~/.codex/AGENTS.md`, `~/.pai/AGENTS.md`, or any Codex runtime
  instruction file.
- Non-dry-run Codex generation requires an explicit output path inside an
  explicit PAI home containment root. It rejects repository governance paths,
  default runtime homes, Codex adapter/config home paths, traversal outside the
  containment root, non-`AGENTS.md` outputs, reserved `.agents`, `.codex`,
  `agents`, `hooks`, `rules`, and `skills` subpaths, symlink output paths, and
  symlink path components.
- Codex config merge remains unauthorized in PR-04A. No `config.toml`, rules,
  hooks, skills, agents, transcript, memory, voice, or status behavior is
  generated.

The compact router shape is deliberate. Codex should receive a small routing
file that points to PAI context and algorithm sources when needed, instead of a
large Claude-specific instruction corpus that embeds Claude tool and lifecycle
assumptions.

## Suggested Evidence For Architect Review

Capture these after PR-04A implementation:

```bash
git status --short
git diff --stat
bun Tools/platform-inventory.ts --format markdown --top 10
bun Tools/platform-inventory.ts --root Tools/fixtures/platform-inventory --format json
bun test Tools/instruction-generation.test.ts
bun test Tools/platform/paths.test.ts
bun test Tools/installer-platform.test.ts
bun test Tools/installer-platform-guards.test.ts
bun test Tools/installer-boundary.test.ts
bun test Tools/installer-entrypoints.test.ts
```

This package is sufficient to review PR-04A target-aware instruction generation
without advancing into Codex config merge or any PR-04B work.
