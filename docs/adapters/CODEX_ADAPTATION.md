# Codex Adapter Adaptation Plan

PR-01 established the inventory and compatibility baseline. PR-02 added the
neutral platform/path primitive for future adapter work. Phase 3 includes
PR-03A platform parsing plus read-only Codex CLI detection, and PR-03B's
first-class Codex-selected installer boundary after detection and prerequisite
reporting. PR-04A begins Phase 4 by adding an unwired target-aware instruction
generation substrate for Claude `CLAUDE.md` compatibility and compact Codex
`AGENTS.md` router generation. PR-04B adds an unwired, explicit-path Codex
`config.toml` merge primitive with conflict detection, backup, idempotency, and
path-safety tests. PR-04C adds an unwired Codex adapter install-plan and
temp-HOME writer primitive for `AGENTS.md`, plus optional test-only integration
with the PR-04B config merge helper. These PRs do not install or generate Codex
runtime files through installer flows. This
document records the evidence base for adapting PAI from a Claude Code-only
release shape into peer Claude and Codex adapters without changing default
Claude behavior.

## Non-Goals Through PR-04C

- No Codex installation path.
- No hook behavior changes.
- No Codex runtime config, rules, hooks, skills, agents, or runtime
  instruction installation.
- No changes to Claude settings generation output.
- No non-installer release runtime behavior changes.
- No protected governance file edits.
- No claim that Codex support is implemented.
- Existing Claude Code users have no migration action through PR-04C, and the
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

## PR-04B Codex Config Merge Primitive

PR-04B adds an unwired Codex `config.toml` merge primitive at
`Releases/v4.0.3/.claude/PAI-Install/engine/codex-config-merge.ts`. It is a
small conservative helper for later installer phases and is not called by CLI,
web, or install actions in PR-04B.

Current tested PR-04B semantics:

- Merging requires an explicit `configPath` and explicit `allowedRoot`
  containment path for dry runs and writes.
- The primitive supports only a small TOML subset for PAI-managed fragments:
  top-level scalar assignments, simple table headers, nested table headers such
  as `[mcp_servers.example]`, comments, blank lines, and scalar values retained
  as raw TOML text.
- Existing user config is preserved. User model, provider, profile, feature,
  MCP, agent, and unrelated table settings are not rewritten or removed.
- Inserted PAI values are wrapped in clear PAI-managed markers inside the
  relevant table. Existing PAI-managed blocks for the same target table are
  replaced; running the same merge again is idempotent and reports no change.
- Existing user-owned table/key conflicts are reported with table, key, line,
  and reason. Conflicts do not write by default.
- Dotted-key or array-of-table TOML that overlaps the target table fails closed
  instead of being rewritten or merged by guesswork.
- Merged output is validated as TOML before the primitive reports a changed
  result or writes content.
- Non-dry-run writes create deterministic backups when `backup: true`,
  `now` is injected, the target already exists, and content changes. No backup
  is created for dry runs or no-op merges. Backup path collisions fail closed
  instead of overwriting earlier backups.
- Writes use a temporary file in the same target directory and rename over the
  target. Temp and backup files are created with exclusive semantics. Tests
  verify no temporary file remains after a successful write.
- Path safety rejects root repository `.codex/config.toml`, real user
  `~/.codex/config.toml`, `~/.pai/config.toml`, and
  `~/.claude/config.toml`, symlink config paths, symlink parent directories,
  symlink path components, symlink `allowedRoot` paths, non-`config.toml`
  basenames unless explicitly allowed for tests, and traversal outside an
  explicit `allowedRoot`.
- A temp-home `.codex/config.toml` path is accepted only when tests pass an
  explicit temp `HOME` and matching `allowedRoot`. Temp-home `.pai` and
  `.claude` paths remain rejected.
- Replacing an existing file preserves its mode; creating a new config uses
  restrictive `0600` permissions.

PR-04B does not create a product config fragment, does not enable Codex runtime
configuration, and does not write `~/.codex/config.toml`. Product config
fragments, runtime config writes, hooks, rules, skills, agents, MCP enablement,
model/provider/profile defaults, approval policy, and sandbox defaults remain
unauthorized for this PR.

## PR-04C Codex Adapter Install-Plan And Temp-HOME Writer

PR-04C adds an unwired installer-engine primitive at
`Releases/v4.0.3/.claude/PAI-Install/engine/codex-adapter-plan.ts`. It is a
product-consumable helper for later installer phases, but no CLI, web, shell,
or installer action imports or calls it in PR-04C.

Current tested PR-04C semantics:

- `runCodexAdapterPlan` requires explicit `paiHome`, `adapterHome`, and
  `allowedRoot` inputs.
- Codex `AGENTS.md` content is rendered by calling `BuildInstructions` with
  `target = "codex"` and `dryRun = true`. The plan exposes the rendered
  content in its result.
- The product Codex `AGENTS.md.template` from PR-04A is used by default.
  Explicit test template paths are allowed only when they are the product
  template or are contained by an explicit temp `allowedRoot`; root repository
  `.codex/` is rejected as a template source, including through symlinks.
- The dedicated PR-04C writer owns `adapterHome/AGENTS.md` writes. It does not
  use the PR-04A temporary output write path for adapter-home writes.
- Dry-run plans render content, report a skipped write, and do not create
  `AGENTS.md`, `config.toml`, or backups.
- Non-dry-run test calls can write `adapterHome/AGENTS.md` under a temp
  `HOME/.codex` only when `env.HOME` points at that temp home and
  `allowedRoot` contains the target path.
- `PAI_HOME` must remain separate from the Codex adapter/config home. The plan
  rejects `PAI_HOME` equal to or overlapping `adapterHome`, and rejects
  repository, configured-home, or real-home `.codex` paths as the PAI
  application home.
- Writer path safety rejects root repository `AGENTS.md`, root repository
  `.codex/**`, real process-home `~/.codex`, `~/.pai`, and `~/.claude`
  targets, configured temp-home `.pai` and `.claude` targets, traversal outside
  `allowedRoot`, broad roots such as `/` and the repository root, symlink
  adapter homes, symlink parents, symlink `AGENTS.md` paths, and symlink path
  components.
- Existing `AGENTS.md` mode is preserved when content changes. New
  `AGENTS.md` files are created with restrictive `0600` permissions.
- Backups are created only when `backup: true`, the target exists, content
  changes, and the run is not a dry run. Backup timestamps are deterministic
  when `now` is injected, using
  `AGENTS.md.pai-backup-YYYYMMDD-HHMMSS`. Backup collisions fail closed.
- Writes use a temporary file in the same directory and rename over the target.
  Tests verify no successful write leaves `.pai-tmp-*` files behind.
- If `configFragment` is absent, the plan returns a `skip-config` operation
  with an explicit reason. PR-04C does not define any product Codex config
  fragment.
- If a test supplies `configFragment`, the plan calls the PR-04B
  `mergeCodexConfig` primitive with the explicit `configPath`, `allowedRoot`,
  `env`, `backup`, `now`, and `sourceLabel`. This is test-only integration
  coverage and does not introduce PAI Codex runtime defaults. The plan narrows
  this integration to `adapterHome/config.toml` so PR-04C does not become a
  generic config writer.
- Config merge preflight runs before the `AGENTS.md` writer mutates content,
  including deterministic config backup collision checks, so expected config
  failures do not leave a partial `AGENTS.md` write.
- The config merge integration preserves user config, preserves PR-04B conflict
  behavior, and is idempotent on a second identical merge.

PR-04C still does not write real `~/.codex/AGENTS.md`,
`~/.codex/config.toml`, `~/.pai`, or `~/.claude`. It does not generate Codex
hooks, rules, skills, agents, MCP config, transcript integration, memory,
voice, status, model/provider/profile defaults, approval policy, or sandbox
defaults. Codex runtime support remains unimplemented.

## Suggested Evidence For Architect Review

Capture these after PR-04C implementation:

```bash
git status --short
git diff --stat
bun test Tools/codex-adapter-plan.test.ts
bun Tools/platform-inventory.ts --format markdown --top 10
bun Tools/platform-inventory.ts --root Tools/fixtures/platform-inventory --format json
bun test Tools/codex-config-merge.test.ts
bun test Tools/instruction-generation.test.ts
bun test Tools/platform/paths.test.ts
bun test Tools/installer-platform.test.ts
bun test Tools/installer-platform-guards.test.ts
bun test Tools/installer-boundary.test.ts
bun test Tools/installer-entrypoints.test.ts
```

This package is sufficient to review PR-04C's unwired install-plan and
temp-HOME writer primitive without advancing into runtime config writes,
installer wiring, or any later Phase 4/5 work.
