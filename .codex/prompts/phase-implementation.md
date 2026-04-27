# Generic Phase Implementation Prompt

Use this prompt only after replacing the bracketed placeholders.

PHASE: [number and name]
TASK: [one PR-sized task within the phase]
ARCHITECT STATUS: [approved to implement / corrections only]

Implement only the task above.

Before editing:

1. Read `AGENTS.md`.
2. Read `.codex/governance/ARCHITECTURE_STEWARD_PROTOCOL.md`.
3. Read `.codex/governance/PHASE_PLAN.md` for the current phase.
4. Run `git status --short`.
5. State the task boundary and expected files.

Protected governance files are read-only unless this prompt begins with `GOVERNANCE-UPDATE:`:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/README.md`
- `.codex/.gitignore`
- `.codex/agents/**`
- `.codex/prompts/**`
- `.codex/governance/**`

After implementation:

1. Run relevant tests.
2. Run `pai_reviewer`, `pai_security_reviewer`, and `pai_test_engineer` when available.
3. Fix blocking findings that are within scope.
4. Stop and summarize. Do not start the next phase.

Final response must include:

- Files changed.
- Behavior changed.
- Tests run and exact results.
- Review agents run and verdicts.
- Known risks.
- Protected governance files changed: yes/no.
- Advisory next task recommendation.
