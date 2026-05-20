# PAI Codex Runtime Support

This optional package installs Codex runtime support for PAI. It lets Codex read live PAI context, classify prompts into PAI modes, follow the Algorithm, write ISA work files, and record safe observability logs through Codex hooks.

## Install

From the PAI release directory:

```bash
cd ~/.claude/codex
./install-codex.sh --global
```

Use `./install-codex.sh` without `--global` to stage PAI-local files only. Global activation writes Codex-facing files under `~/.codex`, `~/.agents`, and `~/.claude/hooks/codex`.

The installer creates timestamped backups before replacing user files. These are installer backups only; no runtime backup behavior is added.

## Verify

```bash
~/.claude/codex/verify-codex.sh --installed
```

The verifier checks installed files, hook JSON, executable bits, helper Python syntax, and common private-reference leaks.

## Uninstall

```bash
~/.claude/codex/uninstall-codex.sh --dry-run
~/.claude/codex/uninstall-codex.sh
```

The uninstaller removes known PAI Codex files and does not remove unrelated Codex configuration.

## Installed Files

Global activation installs:

- `~/.codex/AGENTS.md`
- `~/.codex/hooks.json`
- `~/.codex/pai-config.example.toml`
- `~/.claude/hooks/codex/*.sh`
- `~/.claude/hooks/codex/lib/*.py`
- `~/.agents/skills/pai-*`
- `~/.codex/agents/pai_*.toml`

PAI-local staging installs the same runtime package under `~/.claude/codex` and hooks under `~/.claude/hooks/codex`, without replacing global Codex instruction or hook config files.

## Known Limitations

- Codex hooks are guardrails, not a complete security boundary. Codex sandboxing and approval policy remain authoritative.
- Prompt classification is deterministic by default and does not forward raw prompts to another model.
- ISA sync runs only when a supported PAI sync hook or tool is present.
- Pulse and voice notifications are optional and are only used when reachable and enabled.
- Custom agents installed by this package are read-only review/exploration helpers. Parent Codex remains responsible for writes.
