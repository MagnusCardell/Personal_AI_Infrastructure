# Review Prompt: Current Diff

Review the current diff only. Do not edit files.

Use the PAI project invariants:

1. Claude behavior must remain unchanged by default.
2. Codex support must be adapter-based, not a fork.
3. `~/.codex` must not become PAI_HOME.
4. Installer writes must be idempotent, backed up, and temp-HOME tested.
5. Auth/history/session/log/credential files must not be touched.
6. Hook outputs must match the target platform.
7. Unsupported parity must be documented.
8. Tests must cover schemas and path behavior touched by the diff.
9. Protected governance files must be unchanged unless the task is a `GOVERNANCE-UPDATE`.

Protected governance files:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/README.md`
- `.codex/.gitignore`
- `.codex/agents/**`
- `.codex/prompts/**`
- `.codex/governance/**`

Return:

- Verdict: approve or request changes.
- Blocking issues.
- Non-blocking issues.
- Missing tests.
- Product/development boundary concerns.
- Protected governance files changed: yes/no.
- Exact files/lines to inspect manually.
