# PAI Codex Adapter Development Instructions

This repository is adapting PAI from a Claude Code-only release model into a platform-adapter architecture with Claude Code and Codex CLI as peer adapters.

This file governs development work in this repository. It is not the runtime `AGENTS.md` template that the PAI installer will generate for end users.

## Authority model

The Codex adapter migration is architect-led.

Codex may implement the currently assigned phase or PR-sized task, but Codex must not decide that a phase is complete, advance itself to the next phase, rewrite the governance model, or replace the architecture plan.

The phase loop is:

1. The human/architect supplies the current phase prompt.
2. Codex implements only that phase or the named PR-sized slice.
3. Codex runs its assigned review agents and tests.
4. The user uploads or pastes the review package for architect review.
5. The architect issues the next accepted corrections or the next phase prompt.

Codex final summaries may recommend a next PR, but those recommendations are advisory. Only an architect-issued next prompt is authoritative.

## Governance files are protected

The following files are steward-owned and must not be edited by Codex during normal implementation phases:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/README.md`
- `.codex/.gitignore`
- `.codex/agents/**`
- `.codex/prompts/**`
- `.codex/governance/**`

Codex may read these files freely. Codex may edit them only when the user explicitly supplies a prompt whose first line starts with:

```text
GOVERNANCE-UPDATE:
```

and the prompt names the exact protected files to modify.

If protected files change accidentally, Codex must stop, report the change, and revert it unless the current task is a governance update.

## Non-negotiable architecture

1. Preserve Claude Code behavior by default. Existing Claude users must not be migrated, broken, or forced into Codex.
2. Codex support is an adapter, not a fork and not a replacement.
3. The neutral PAI core owns memory, skills, algorithms, tools, voice, policy abstractions, and installer orchestration.
4. Claude-specific behavior belongs under a Claude adapter.
5. Codex-specific behavior belongs under a Codex adapter.
6. `~/.claude` remains the default Claude adapter home.
7. `~/.codex` is Codex CLI state/config space, not the PAI application home.
8. The default Codex PAI home is `~/.pai`, unless the user explicitly chooses another `PAI_HOME`.
9. `PAI_DIR` remains a compatibility alias and has priority over `PAI_HOME` where legacy behavior requires it.
10. No installer, hook, migration, or test may modify auth/session/history/log files in `~/.codex`, `~/.claude`, or real user homes.

## Canonical implementation phases

The canonical migration plan has ten implementation phases:

1. Inventory and compatibility baseline.
2. Platform core and path abstraction.
3. Installer platform selection and detection.
4. Instruction generation and Codex config merge.
5. Hook adapter and lifecycle mapping.
6. Security policy split: Codex rules plus contextual hooks.
7. Skills and pack conversion.
8. Agents and subagents conversion.
9. Transcript, memory, voice, notify, and status integration.
10. End-to-end install tests, release packaging, documentation, and beta readiness.

Each phase may be split into multiple PR-sized tasks, but no task may skip the architect review gate between phases.

## Codex-specific design constraints

- Use Codex-native surfaces instead of emulating Claude internals.
- Use `AGENTS.md` as a compact context router, not a wholesale port of `CLAUDE.md`.
- Use Codex `config.toml` merging for durable Codex config.
- Use Codex `hooks.json` or inline hooks only through a Codex adapter layer.
- Use Codex rules for static command allow/prompt/forbidden policy.
- Use hooks for contextual validation, lifecycle integration, memory, learning, notifications, and hard blocks where Codex supports them.
- Use Codex skills under `.agents/skills`, `~/.agents/skills`, or admin skill paths; do not assume Claude skill paths.
- Use Codex custom agent TOML files for Codex subagents; do not copy Claude agent markdown directly.
- Treat Claude statusline, `Task`, `Skill`, `AskUserQuestion`, and Claude transcript schemas as Claude-specific until deliberately mapped.

## PR discipline

Each implementation pass must be one PR-sized task. Do not perform broad migrations.

Required sequence for every PR:

1. State the exact task boundary.
2. Inspect relevant files before editing.
3. Run `git status --short` and note whether protected governance files are clean.
4. Add or update tests/fixtures before claiming completion.
5. Preserve Claude defaults unless the task explicitly changes them.
6. Run focused tests and record exact commands/results.
7. Summarize risks and unsupported parity gaps.
8. Leave the repository in a reviewable state with no unrelated formatting churn.

## Reviewer gates

A PR is not acceptable if any answer is no:

- Does Claude Code behavior remain unchanged by default?
- Are Claude-only assumptions isolated under a Claude adapter?
- Are Codex-only assumptions isolated under a Codex adapter?
- Are installer writes idempotent and backed up when touching user config?
- Does the installer avoid treating `~/.codex` as the PAI app home?
- Are auth, history, session, log, credential, and secret files untouched?
- Are hook inputs/outputs valid for the target platform?
- Are unsupported Codex features documented instead of silently claimed?
- Are test fixtures included for any schema, transcript, hook, or config format touched?
- Are protected governance files unchanged unless this is a `GOVERNANCE-UPDATE` task?
- Are product release artifacts free of development-only `.codex` governance files?

## Safe testing rules

- Use temp directories for install and migration tests.
- Never run installer tests against a real home directory.
- Prefer `HOME=$(mktemp -d)` and explicit `PAI_HOME`, `CODEX_HOME`, and `CLAUDE_HOME`/`CLAUDE_DIR` fixtures.
- Do not call real network services from tests unless the task explicitly requires an integration test and the reviewer approves.
- Do not create persistent files outside the workspace or test temp directories.

## Documentation truthfulness

Compatibility claims must be conservative.

Use these labels:

- `full`: tested and equivalent enough for normal use.
- `partial`: implemented with known semantic gaps.
- `claude-only`: intentionally not available in Codex.
- `codex-only`: available only through the Codex adapter.
- `unsupported`: not implemented and not promised.
- `breaking-for-codex`: Claude feature cannot be mapped without changed semantics.
