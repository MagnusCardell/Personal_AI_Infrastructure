# PAI Codex Development Harness

This `.codex` directory is for developing the PAI Codex adapter in this repository.

It is not part of the PAI runtime, not part of a user installation, and not the generated Codex adapter payload. The PAI installer must not copy this directory into `~/.codex`, `~/.pai`, or `~/.claude`.

## Authority model

This harness is architect-governed. Codex uses these files to execute a phase, but Codex does not own or advance the phase plan.

The accepted loop is:

1. Architect/human supplies a phase or PR-sized prompt.
2. Codex implements only that scope.
3. Codex runs reviewers and tests.
4. User packages the diff and Codex summary.
5. Architect reviews the actual repository state and issues corrections or the next phase.

Codex may recommend a next task. That recommendation is not authoritative until the architect accepts or revises it.

## Protected files

These governance files are steward-owned:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/README.md`
- `.codex/.gitignore`
- `.codex/agents/**`
- `.codex/prompts/**`
- `.codex/governance/**`

Codex may edit them only under a prompt beginning with `GOVERNANCE-UPDATE:` that names the files to change.

## What belongs here

- Project-scoped Codex configuration for this repository.
- Custom Codex subagent definitions used during implementation and review.
- Reusable prompts for PR-sized implementation and review tasks.
- Steward protocol, phase plan, and protected-file rules.

## What does not belong here

- Product hooks for end-user Codex installations.
- Product rules for end-user Codex installations.
- Generated end-user Codex adapter templates.
- Any auth, session, history, log, API key, token, or private user state.
- Generated release payloads.

## Packaging rule

Release artifacts must exclude `.codex/` unless a future release process explicitly documents and tests a reason to include a specific file.

Product Codex templates should live under an adapter/release path such as `adapters/codex/`, `PAI-Install/templates/codex/`, or `Releases/<version>/.../adapters/codex/`, not in this development harness.
