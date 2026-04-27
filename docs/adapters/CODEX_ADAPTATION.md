# Codex Adapter Adaptation Plan

PR-01 established the inventory and compatibility baseline. PR-02 adds only a
neutral platform/path primitive for future adapter work. This document records
the evidence base for adapting PAI from a Claude Code-only release shape into
peer Claude and Codex adapters without changing current runtime behavior.

## Non-Goals Through PR-02

- No installer behavior changes.
- No hook behavior changes.
- No settings generation changes.
- No release artifact edits under `Releases/*/.claude/`.
- No protected governance file edits.
- No claim that Codex support is implemented.
- Existing Claude Code users have no migration action through PR-02, and current
  Claude defaults remain unchanged.

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
   routing plus config merge behavior later; PR-01 does not implement it.

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
    None of this may change Claude default detection or require Codex for
    existing Claude users.

## Adapter Boundary Notes

- The existing release artifacts under `Releases/*/.claude/` are treated as
  Claude adapter evidence, not files to mutate in this PR.
- `PAI_DIR` remains the legacy compatibility alias and has priority over
  `PAI_HOME` where legacy behavior requires it. Codex's default PAI application
  home is `~/.pai`; `~/.codex` is Codex CLI state/config space, not the PAI app
  home.
- Codex support should be added as new adapter behavior, with neutral core
  abstractions only where they remove duplicated platform assumptions.
- Unsupported or unverified Codex behavior must stay labeled as such in
  `COMPATIBILITY_MATRIX.md`.

## PR-02 Path Resolver Primitive

The shared path primitive lives at `Tools/platform/paths.ts`. It is intentionally
additive and is not wired into the installer, hooks, release packaging, or any
runtime writer in PR-02.

Current tested semantics:

- Supported adapter identifiers are `claude` and `codex`.
- PAI application home precedence is `PAI_DIR`, then `PAI_HOME`, then the
  platform default.
- Claude defaults resolve both the PAI application home and adapter home to
  `~/.claude`, preserving the current Claude shape.
- Codex defaults resolve the PAI application home to `~/.pai` and the Codex
  adapter/config home to `CODEX_HOME` when set, otherwise `~/.codex`.
- `~/.codex` is treated as Codex CLI state/config space, not as the default PAI
  application home.
- Home expansion covers `~`, `$HOME`, and `${HOME}`. Tests use temp-home style
  paths and do not write real user homes.
- Windows path behavior is explicitly rejected as unsupported for this phase.

## Suggested Evidence For Architect Review

Capture these after PR-02 implementation:

```bash
git status --short
git diff --stat
bun Tools/platform-inventory.ts --format markdown --top 10
bun Tools/platform-inventory.ts --root Tools/fixtures/platform-inventory --format json
bun test Tools/platform/paths.test.ts
```

This package is sufficient to review the path abstraction without advancing
into PR-03.
