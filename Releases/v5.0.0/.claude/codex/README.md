# PAI Codex Runtime Support

## What This Package Does

This optional package lets Codex operate against a local PAI install. It installs Codex hooks, runtime instructions, safe logging helpers, optional PAI skills, and read-only review agents.

With it enabled, Codex can:

- read live PAI identity, project, and Telos context from `~/.claude/PAI`
- classify prompts into `MINIMAL`, `NATIVE`, or `ALGORITHM`
- follow the PAI Algorithm and create/update canonical ISA files
- write structured observability logs with redaction
- use Codex hook semantics correctly
- use optional PAI skills and read-only custom agents

## Install Modes

Default mode is PAI-local staging:

```bash
~/.claude/codex/install-codex.sh
```

PAI-local staging installs package files under `~/.claude/codex` and hooks under `~/.claude/hooks/codex`, but does not activate Codex-facing `~/.codex` files.

Global mode activates Codex-facing files:

```bash
~/.claude/codex/install-codex.sh --global
```

Global mode merges into existing `~/.codex/AGENTS.md`, `~/.codex/hooks.json`, and `~/.codex/config.toml`. It does not replace those files by default. Use `--force-replace` only when you explicitly want destructive replacement of managed global files.

## What Changes On Disk

PAI-local staging may write:

- `~/.claude/codex/*`
- `~/.claude/hooks/codex/*.sh`
- `~/.claude/hooks/codex/lib/*.py`

Global activation may also write:

- `~/.codex/AGENTS.md`
- `~/.codex/hooks.json`
- `~/.codex/config.toml`
- `~/.codex/pai-config.example.toml`
- `~/.agents/skills/pai-*`
- `~/.codex/agents/pai_*.toml`

Existing `AGENTS.md` receives a managed PAI block. Existing `hooks.json` keeps non-PAI hook groups and receives PAI hook groups. Existing `config.toml` keeps user writable roots and adds required PAI roots if missing.

Before overwriting user files, the installer creates installer-local backups under `~/.claude/codex/backups`. These are install-time backups only. The runtime does not create backups, retention jobs, or hidden maintenance.

## Install

Dry-run first:

```bash
~/.claude/codex/install-codex.sh --global --dry-run
```

Then activate:

```bash
~/.claude/codex/install-codex.sh --global
```

After the first run, Codex may ask you to review and trust hooks through `/hooks`.

## Post-Install Smoke Test

Run:

```bash
codex exec --json "who am I?"
codex exec --json "what are my active projects?"
codex exec --json "run pwd and explain the result"
```

Expected behavior:

- identity/project prompts use live PAI files
- execution prompts trigger tool hooks
- observability logs are written under `~/.claude/PAI/MEMORY/OBSERVABILITY`

## Verify

Package verification:

```bash
~/.claude/codex/verify-codex.sh --package
```

Installed verification:

```bash
~/.claude/codex/verify-codex.sh --installed
```

The verifier checks JSON syntax, shell syntax, Python syntax, executable bits, read-only agent policy, and common private or secret-like references.

## Uninstall And Restore

Preview uninstall:

```bash
~/.claude/codex/uninstall-codex.sh --dry-run
```

Uninstall managed PAI Codex files:

```bash
~/.claude/codex/uninstall-codex.sh
```

List installer backups:

```bash
~/.claude/codex/uninstall-codex.sh --list-backups
```

Preview restoring the latest backup:

```bash
~/.claude/codex/uninstall-codex.sh --restore-latest --dry-run
```

Restore a backup:

```bash
~/.claude/codex/uninstall-codex.sh --restore-latest
```

Uninstall removes only managed PAI blocks, PAI hook groups, managed hook files, PAI skills, and read-only PAI agents. It does not remove unrelated Codex configuration.

## Known Limitations

- Hooks are guardrails, not a complete security boundary. Codex sandboxing and approval policy remain authoritative.
- Prompt classification is deterministic by default and does not forward raw prompts to another model.
- ISA sync runs only when a supported PAI sync hook or tool is present.
- Pulse/voice support is optional and not full parity yet.
- Custom agents installed by this package are read-only. Parent Codex remains responsible for writes.
