# Codex Adapter Adaptation Plan

PR-01 established the inventory and compatibility baseline. PR-02 added the
neutral platform/path primitive for future adapter work. PR-03A adds installer
platform selection state and read-only Codex CLI detection only; it does not
install or generate Codex runtime files. This document records the evidence
base for adapting PAI from a Claude Code-only release shape into peer Claude
and Codex adapters without changing default Claude behavior.

## Non-Goals Through PR-03A

- No Codex installation path.
- No hook behavior changes.
- No Codex settings, rules, hooks, skills, agents, or instruction generation.
- No changes to Claude settings generation output.
- No non-installer release runtime behavior changes.
- No protected governance file edits.
- No claim that Codex support is implemented.
- Existing Claude Code users have no migration action through PR-03A, and the
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
   docs assume Claude Code loads that file. Codex needs compact `AGENTS.md`
   routing plus config merge behavior later; it is not implemented through
   PR-03A.

5. **Transcript and session tools assume Claude JSONL shape and paths.**
   `TranscriptParser.ts`, `SessionHarvester.ts`, `GetTranscript.ts`, and hook
   helpers use `transcript_path`, `.jsonl`, `message.content`, `tool_use`, and
   `~/.claude/projects` assumptions. Codex transcript support needs fixtures
   before memory, learning, voice, or status integration can be labeled beyond
   `unsupported` or `unknown-needs-fixture`.

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
   execution rather than detection. Codex detection can be analogous, but
    prompt execution needs an explicit Codex execution contract before mapping.
    None of this is implemented through PR-03A, and none of it may change
    Claude default detection or require Codex for existing Claude users.

## Adapter Boundary Notes

- Non-installer Claude runtime artifacts under `Releases/*/.claude/`, including
  settings, hooks, skills, agents, transcript tools, and generated instruction
  templates, are treated as Claude adapter evidence and remain out of scope for
  PR-03A. PR-03A mutates only release installer files plus the
  product-consumable platform path primitive needed by those installer files.
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
kept it unwired; PR-03A uses it for read-only installer detection and platform
path planning only.

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

## PR-03A Installer Selection And Detection Primitives

PR-03A adds installer platform option parsing and state for `claude`, `codex`,
and `both`. If no platform is specified, the installer normalizes to
`platform = claude`, preserving the existing default behavior.

Current PR-03A semantics:

- `install.sh` forwards user-supplied arguments to the TypeScript installer and
  still launches GUI mode when no arguments are supplied.
- Codex-containing selections skip bootstrap auto-installs for Git, Bun, and
  Claude Code. Bun must already be present so the TypeScript installer can run
  read-only detection.
- `main.ts` parses `--platform claude`, `--platform codex`, `--platform both`,
  and equals-form variants. Unknown values fail with a clear parser error.
- Installer state records the selected platform and normalized target platform
  list. Legacy saved state without platform fields resumes as Claude-only.
- For Claude writer-facing installer paths, `PAI_DIR` remains the legacy
  combined PAI/Claude home. `PAI_HOME` is retained as neutral PAI planning
  metadata in PR-03A and does not move Claude writer targets.
- Read-only detection checks Codex only when the selected platform includes
  Codex, using `codex --version 2>&1`.
- Missing Codex CLI for `codex` or `both` reports the task-required manual
  install hints:
  `npm install -g @openai/codex` and `brew install codex`.
- Claude-only installs do not require or probe Codex.
- Codex-selected installs skip mutating prerequisite installs and fail closed
  before PAI repository, configuration, Codex runtime, or voice setup writes
  because Codex installation is not implemented in PR-03A.
- `both` is selection and detection state only in PR-03A. It does not mean
  "complete the Claude install and skip Codex"; any Codex-containing selection
  fails before the shared installer writer phases.
- `install.sh --platform codex` is not a full Codex install or a supported dry
  run. It forwards the selected platform into the installer, performs read-only
  platform detection when Bun is available, and stops before unsupported Codex
  PAI writes.
- No `~/.codex`, `~/.pai`, `~/.claude`, `AGENTS.md`, `config.toml`, rules,
  hooks, skills, or agent files are generated for Codex.

## Suggested Evidence For Architect Review

Capture these after PR-03A implementation:

```bash
git status --short
git diff --stat
bun Tools/platform-inventory.ts --format markdown --top 10
bun Tools/platform-inventory.ts --root Tools/fixtures/platform-inventory --format json
bun test Tools/platform/paths.test.ts
bun test Tools/installer-platform.test.ts
bun test Tools/installer-platform-guards.test.ts
```

This package is sufficient to review the installer selection and read-only
detection primitives without advancing into PR-03B or PR-04.
