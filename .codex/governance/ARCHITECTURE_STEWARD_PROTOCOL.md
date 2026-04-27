# Architecture Steward Protocol

This file defines how the PAI Codex adapter migration is controlled.

## Principle

Codex is an implementation and review instrument. The architect is the steward of architecture, phase sequencing, compatibility policy, and release readiness.

Codex may not self-promote a task to complete, self-advance phases, or rewrite the governance model during normal implementation work.

## Phase loop

For each phase:

1. Architect issues a phase prompt or PR-sized implementation prompt.
2. Codex restates scope and expected files before editing.
3. Codex implements only that scope.
4. Codex runs assigned review agents.
5. Codex runs the required tests and captures command output.
6. User packages the repository state for architect review.
7. Architect reviews the actual diff and returns one of:
   - approved, proceed to next phase;
   - request changes within current phase;
   - architectural correction, regenerate phase prompt;
   - stop, reassess plan.

Codex's “recommended next PR” is advisory only.

## Review package

After each phase or PR-sized slice, Codex must leave enough evidence for review:

- `git status --short`
- `git diff --stat`
- `git diff --binary` or patch file
- tests run and outputs
- generated compatibility matrix updates
- any known failures or skipped tests
- whether protected governance files changed

The user should send the changed repository zip plus Codex's final summary to the architect.

## Governance updates

Governance files can be changed only by a deliberate governance update.

A valid governance update prompt starts with:

```text
GOVERNANCE-UPDATE:
```

and names the protected files to modify. Without that marker, Codex must treat governance files as read-only.

## Source of truth hierarchy

1. Human/architect instruction in the current conversation.
2. Root `AGENTS.md`.
3. `.codex/governance/*`.
4. `.codex/prompts/*`.
5. Agent-specific TOML instructions.
6. Codex-generated summaries and recommendations.

If lower levels conflict with higher levels, the higher level wins.
