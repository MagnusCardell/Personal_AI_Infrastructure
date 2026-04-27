# PAI Codex Adapter Phase Plan

This is the canonical ten-phase implementation plan. Phases may contain multiple PR-sized tasks, but phase progression requires architect review.

## Phase 1 — Inventory and compatibility baseline

Goal: establish an evidence-based map of Claude-specific coupling with no runtime behavior changes.

Deliverables:

- `docs/adapters/CODEX_ADAPTATION.md`
- `docs/adapters/COMPATIBILITY_MATRIX.md`
- inventory tool for hardcoded Claude assumptions
- top-risk coupling list

Review gate:

- No runtime behavior changes.
- Existing Claude release artifacts untouched.
- Inventory classifications are specific enough to drive implementation.

## Phase 2 — Platform core and path abstraction

Goal: introduce neutral platform/path primitives while preserving Claude defaults exactly.

Deliverables:

- `PaiPlatform` and `PlatformPaths` concepts
- centralized path resolution for `PAI_DIR`, `PAI_HOME`, `CODEX_HOME`, Claude home, and platform defaults
- tests for env-var precedence and temp homes

Review gate:

- Claude path behavior remains unchanged by default.
- No Codex files are written.
- No new scattered hardcoded home paths.

## Phase 3 — Installer platform selection and detection

Goal: add explicit install modes without changing the existing Claude default path.

Deliverables:

- installer platform flags: `claude`, `codex`, `both`
- Codex CLI detection
- temp-HOME dry-run harness
- clear failure modes when Codex is missing

Review gate:

- `claude` mode remains default-compatible.
- `codex` mode does not treat `~/.codex` as `PAI_HOME`.
- all installer tests use temp homes.

## Phase 4 — Instruction generation and Codex config merge

Goal: split instruction generation and add safe Codex config merge behavior.

Deliverables:

- `BuildInstructions` abstraction
- Claude `CLAUDE.md` compatibility shim
- compact Codex `AGENTS.md` generator
- `~/.codex/config.toml` merge logic with backup and idempotency tests

Review gate:

- generated Codex `AGENTS.md` is a router, not a giant Claude dump.
- config merge preserves user settings and makes backups.
- Claude `CLAUDE.md` output remains compatible.

## Phase 5 — Hook adapter and lifecycle mapping

Goal: normalize hook inputs/outputs while respecting each platform's native hook schema.

Deliverables:

- normalized hook input/output model
- Claude adapter preserving current behavior
- Codex hook wrappers and fixtures for supported events
- remapping plan for `SessionEnd` to Codex `Stop` or explicit finalization

Review gate:

- Codex hooks do not emit Claude decision shapes.
- every touched schema has fixtures.
- unsupported hook parity is documented.

## Phase 6 — Security policy split

Goal: separate static command policy from contextual security and prevent fail-open migrations.

Deliverables:

- Codex rules generation for static allow/prompt/forbidden policy
- contextual `SecurityValidator` behavior through hook adapter where supported
- tests for destructive command patterns and config-rule output

Review gate:

- Claude `ask` behavior is not blindly copied to Codex.
- generated Codex rules are testable.
- hooks are not relied on for unsupported enforcement paths.

## Phase 7 — Skills and pack conversion

Goal: expose PAI skills to Codex through Codex skill conventions while preserving Claude skills.

Deliverables:

- skill converter or wrapper generator
- Codex `SKILL.md` metadata validation
- pack metadata with platform compatibility labels
- symlink/copy strategy for `~/.agents/skills`

Review gate:

- no Claude skill is declared Codex-full without validation.
- pack docs clearly distinguish Claude and Codex install paths.

## Phase 8 — Agents and subagents conversion

Goal: convert relevant PAI/Claude agents into Codex custom-agent TOML without conflating Claude `Task` semantics.

Deliverables:

- Codex agent TOML generator or curated agent files
- sandbox and model settings per agent role
- docs explaining semantic differences

Review gate:

- generated TOML validates.
- Claude agents remain intact.
- no product code depends on root `.codex/agents` governance files.

## Phase 9 — Transcript, memory, voice, notify, and status integration

Goal: make session/memory features platform-neutral and provide Codex-native alternatives for Claude-only UI hooks.

Deliverables:

- transcript parser interface
- Claude parser preserving current behavior
- Codex parser based on fixtures and hook-provided paths
- voice/notify integration via Codex-native surfaces
- statusline compatibility notes

Review gate:

- no direct `~/.claude/projects` assumption outside Claude parser/provider.
- Codex transcript format is fixture-tested.
- Claude dynamic statusline is not overclaimed as supported.

## Phase 10 — E2E install tests, release packaging, documentation, and beta readiness

Goal: prepare a safe beta release with honest compatibility claims and reversible install behavior.

Deliverables:

- temp-HOME E2E install tests for Claude, Codex, and both
- packaging exclusion tests for root `.codex`
- migration/rollback docs
- release notes and compatibility matrix
- beta support label for Codex

Review gate:

- existing Claude users have a no-action path.
- release artifacts exclude development governance files.
- all known non-parity is documented.
