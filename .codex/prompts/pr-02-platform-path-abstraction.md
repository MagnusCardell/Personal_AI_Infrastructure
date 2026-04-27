# PR-02 Prompt: Platform Path and Type Abstraction

Implement PR-02 only.

Goal:
Add platform path/type abstraction with tests while preserving Claude defaults exactly. Do not change installer output or Codex install behavior yet.

Read first:

- `AGENTS.md`
- `.codex/governance/ARCHITECTURE_STEWARD_PROTOCOL.md`
- `.codex/governance/PHASE_PLAN.md`

Required design:

- Platform type: `claude | codex`.
- Neutral preferred env var: `PAI_HOME`.
- Legacy env var: `PAI_DIR`, preserved and prioritized where existing behavior depends on it.
- Claude adapter home default: `~/.claude`.
- Codex adapter home default: `$CODEX_HOME` or `~/.codex`.
- Codex PAI home default: `~/.pai`.
- Do not use `~/.codex` as PAI_HOME.

Create a small platform library in the existing project style. Suggested concepts:

- `PaiPlatform`
- `PlatformPaths`
- `resolvePaiHome()`
- `resolveAdapterHome()`
- `resolvePlatformPaths()`
- `detectPlatformAvailability()` if needed, but avoid changing installer behavior in this PR

Protected governance files are read-only for this task:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/README.md`
- `.codex/.gitignore`
- `.codex/agents/**`
- `.codex/prompts/**`
- `.codex/governance/**`

If any protected file changes accidentally, stop and report.

Acceptance criteria:

1. Existing Claude defaults resolve exactly as before.
2. `PAI_DIR` compatibility is tested.
3. `PAI_HOME` behavior is tested.
4. `CODEX_HOME` behavior is tested.
5. No Codex files are written.
6. No installer behavior changes.
7. No direct new hardcoded `~/.claude` or `~/.codex` references outside path/adapters/tests.
8. Tests use temp directories and do not touch real homes.
9. Protected governance files are unchanged.

End with:

- Files changed
- Tests run
- Behavior confirmed unchanged for Claude defaults
- Any remaining hardcoded path references intentionally left for later PRs
- Protected governance files changed: yes/no
- Recommended next task, advisory only
