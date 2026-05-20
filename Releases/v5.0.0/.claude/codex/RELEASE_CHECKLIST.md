# PAI Codex Runtime Release Checklist

Use this checklist before publishing or opening a pull request for the Codex runtime package.

## Required Checks

- Run the package verifier:

  ```bash
  Releases/v5.0.0/.claude/codex/verify-codex.sh --package
  ```

- Run the full package test runner:

  ```bash
  Releases/v5.0.0/.claude/codex/tests/run-all.sh
  ```

- Run shell syntax checks:

  ```bash
  bash -n Releases/v5.0.0/.claude/codex/*.sh
  bash -n Releases/v5.0.0/.claude/codex/hooks/*.sh
  bash -n Releases/v5.0.0/.claude/codex/tests/*.sh
  bash -n Releases/v5.0.0/.claude/codex/skills/pai-isa/scripts/*.sh
  bash -n Releases/v5.0.0/.claude/codex/skills/pai-runtime-audit/scripts/*.sh
  ```

- Run Python and JSON syntax checks:

  ```bash
  python3 -m py_compile Releases/v5.0.0/.claude/codex/hooks/lib/*.py
  python3 -m json.tool Releases/v5.0.0/.claude/codex/hooks.json.template >/dev/null
  ```

- Run the AGENTS generator preview when Bun is available:

  ```bash
  bun Releases/v5.0.0/.claude/codex/tools/GenerateAgentsMd.ts --dry-run
  ```

- Run shellcheck when available:

  ```bash
  shellcheck Releases/v5.0.0/.claude/codex/*.sh \
    Releases/v5.0.0/.claude/codex/hooks/*.sh \
    Releases/v5.0.0/.claude/codex/tests/*.sh \
    Releases/v5.0.0/.claude/codex/skills/pai-isa/scripts/*.sh \
    Releases/v5.0.0/.claude/codex/skills/pai-runtime-audit/scripts/*.sh
  ```

- Confirm no generated artifacts are present:

  ```bash
  git status --short
  find Releases/v5.0.0/.claude/codex -name __pycache__ -o -name '*.pyc'
  ```

## Install And Uninstall Checks

- Preview default staging install:

  ```bash
  Releases/v5.0.0/.claude/codex/install-codex.sh --dry-run
  ```

- Preview global activation:

  ```bash
  Releases/v5.0.0/.claude/codex/install-codex.sh --global --dry-run
  ```

- Run clean-HOME acceptance:

  ```bash
  Releases/v5.0.0/.claude/codex/tests/acceptance-clean-home.sh
  ```

- Preview uninstall and restore:

  ```bash
  Releases/v5.0.0/.claude/codex/uninstall-codex.sh --dry-run
  Releases/v5.0.0/.claude/codex/uninstall-codex.sh --restore-latest --dry-run
  ```

## Security And Privacy Scans

- Forbidden/private reference scan: covered by `verify-codex.sh --package`.
- Secret marker scan: covered by `verify-codex.sh --package`.
- Direct provider-call scan: covered by `verify-codex.sh --package`.

Expected result for each built-in scan is no matches.

## Optional Runtime Checks

- Pulse smoke test:

  ```bash
  Releases/v5.0.0/.claude/codex/tests/test-pulse-runtime.sh
  ```

- Voice intent smoke test:

  ```bash
  Releases/v5.0.0/.claude/codex/tests/test-voice-runtime.sh
  ```

- Learning runtime smoke test:

  ```bash
  Releases/v5.0.0/.claude/codex/tests/test-learning-runtime.sh
  ```

- AGENTS generator smoke test:

  ```bash
  Releases/v5.0.0/.claude/codex/tests/test-generate-agents.sh
  ```

- Manual Codex smoke test after global install:

  ```bash
  codex exec --json "who am I?"
  codex exec --json "what are my active projects?"
  codex exec --json "run pwd and explain the result"
  ```

Review hooks through `/hooks` if Codex asks for trust confirmation.

## PR Review Items

- Default install stages files locally and does not activate global Codex config.
- Global install merges `AGENTS.md`, `hooks.json`, and `config.toml` without replacing user content by default.
- Installer backups are install-time only; runtime hooks do not create backups or retention jobs.
- Custom agents are read-only.
- Pulse and voice are optional and disabled by default.
- Hooks are documented as guardrails, not a complete security boundary.
