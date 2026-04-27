# PR-01 Prompt: Inventory and Compatibility Matrix Only

Implement PR-01 only.

Goal:
Create adaptation planning docs and an automated inventory of Claude-specific coupling. Make zero runtime behavior changes.

Read at minimum:

- `AGENTS.md`
- `.codex/governance/ARCHITECTURE_STEWARD_PROTOCOL.md`
- `.codex/governance/PHASE_PLAN.md`
- README.md
- PLATFORM.md
- Releases/*/.claude/settings.json where present
- Releases/*/.claude/PAI-Install/engine/* where present
- Releases/*/.claude/hooks/* where present
- Releases/*/.claude/PAI/Tools/*Transcript* where present
- Releases/*/.claude/PAI/Tools/*Session* where present
- Packs/*/INSTALL.md
- Packs/*/README.md

Create or update:

- docs/adapters/CODEX_ADAPTATION.md
- docs/adapters/COMPATIBILITY_MATRIX.md
- Tools/platform-inventory.ts or the nearest existing tools location if the repo already has a tool convention

Inventory these references:

- `~/.claude`
- `.claude`
- `CLAUDE_DIR`
- `PAI_DIR`
- `CLAUDE.md`
- `BuildCLAUDE`
- `claude --version`
- `claude -p`
- `@anthropic-ai/claude-code`
- `Claude Code`
- Claude settings hook events
- Claude hook decision outputs
- Claude transcript assumptions
- Claude tool names such as `Read`, `Write`, `Edit`, `MultiEdit`, `Task`, `Skill`, `AskUserQuestion`, `Stop`
- Claude statusline assumptions
- Claude skills and agents paths

Classify each occurrence as:

- claude-only
- platform-neutralizable
- codex-equivalent
- breaking-for-codex
- docs-only
- unknown-needs-fixture

Protected governance files are read-only for this task:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/README.md`
- `.codex/.gitignore`
- `.codex/agents/**`
- `.codex/prompts/**`
- `.codex/governance/**`

If any protected file changes accidentally, stop and report.

Do not modify:

- Installer behavior
- Hook behavior
- Settings generation
- README messaging outside the new adapter docs
- Runtime source files unless needed only for the inventory tool
- Protected governance files

Acceptance criteria:

1. Inventory command runs successfully.
2. Top 10 highest-risk Claude couplings are summarized.
3. Compatibility matrix exists and marks unknown/partial honestly.
4. Git diff contains no runtime behavior changes.
5. Claude release artifacts are untouched.
6. Protected governance files are unchanged.

End with:

- Files changed
- Inventory command run
- Tests/checks run
- Known limitations
- Protected governance files changed: yes/no
- Recommended PR-02 scope, advisory only
