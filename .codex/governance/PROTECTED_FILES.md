# Protected Governance Files

These files encode the architect's current project plan and Codex execution harness. They are intentionally versioned in the repository so the implementation agent can read them, but they are not normal implementation files.

## Protected paths

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/README.md`
- `.codex/.gitignore`
- `.codex/agents/**`
- `.codex/prompts/**`
- `.codex/governance/**`

## Normal implementation phases

During normal implementation phases, Codex must not edit these files.

Allowed actions:

- read them
- cite them in summaries
- report conflicts or outdated instructions
- recommend a governance update

Disallowed actions:

- rewrite agent definitions
- modify phase sequencing
- change model/effort settings
- alter root project instructions
- silently adjust prompts to fit an implementation shortcut

## Governance update mode

Codex may edit protected files only when the current prompt begins with:

```text
GOVERNANCE-UPDATE:
```

and explicitly lists the protected files to change.

## Review check

Every final implementation summary must include:

```text
Protected governance files changed: yes/no
```

If the answer is yes outside a governance update, the task is not mergeable until those changes are reverted.
