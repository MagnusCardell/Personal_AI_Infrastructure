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

## DA/Runtime Parity

Session start loads bounded runtime context from live PAI files so Codex can answer identity and status questions in PAI-native form. The context includes principal identity, DA identity, Telos, active projects, the active Algorithm pointer, and any missing-file notes.

## Runtime Context Files

The runtime context helper reads:

- `~/.claude/PAI/USER/PRINCIPAL_IDENTITY.md`
- `~/.claude/PAI/USER/DA_IDENTITY.md`
- `~/.claude/PAI/USER/PROJECTS/PROJECTS.md`
- `~/.claude/PAI/USER/TELOS/PRINCIPAL_TELOS.md`
- `~/.claude/PAI/ALGORITHM/LATEST`
- `~/.claude/PAI/MEMORY/WORK`
- `~/.claude/PAI/MEMORY/OBSERVABILITY`
- `~/.claude/PAI/MEMORY/LEARNING`

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

Runtime parity tests in the release package:

```bash
~/.claude/codex/tests/test-da-runtime-context.sh
~/.claude/codex/tests/test-algorithm-isa-runtime.sh
~/.claude/codex/tests/test-pulse-runtime.sh
~/.claude/codex/tests/test-voice-runtime.sh
```

These tests use a temporary HOME and do not require a real Codex CLI.

## Optional Pulse Notifications

Pulse notifications are disabled by default and are never required for runtime correctness. When enabled, Stop sends a turn-complete notification and ISA updates may send an `codex.algorithm.isa_updated` notification after ISA detection or sync activity.

Environment variables:

- `PAI_CODEX_PULSE_ENABLED=1` enables notifications.
- `PAI_CODEX_PULSE_URL=http://localhost:31337` sets the Pulse base URL. If unset while enabled, the default is `http://localhost:31337`.

Example:

```bash
PAI_CODEX_PULSE_ENABLED=1 codex exec --json "run pwd and explain the result"
```

Smoke test:

```bash
~/.claude/codex/tests/test-pulse-runtime.sh
```

If Pulse is unavailable, hooks still emit valid JSON and continue. Voice intent is configured separately and remains disabled by default.

## Optional Voice Notifications

Voice notifications are disabled by default and require Pulse. Codex emits voice intent through the Pulse `/notify` payload only; Codex hooks do not render speech or call speech providers directly.

The local Pulse contract is flat JSON: `message`, `voice_enabled`, and optional `voice_id`. Because local Pulse may treat an omitted `voice_enabled` field as enabled, Codex sends `voice_enabled: false` unless voice is explicitly enabled for the event.

Environment variables:

- `PAI_CODEX_PULSE_ENABLED=1` enables Pulse delivery.
- `PAI_CODEX_VOICE_ENABLED=1` enables voice intent.
- `PAI_CODEX_VOICE_EVENTS=turn_complete,algorithm_isa_updated` selects voice events. If unset while voice is enabled, only `turn_complete` is selected.
- `PAI_CODEX_VOICE_ID=<id>` adds a voice identifier when explicitly set.
- `PAI_CODEX_VOICE_MESSAGE_TURN_COMPLETE=<message>` overrides the turn-complete speech message.
- `PAI_CODEX_VOICE_MESSAGE_ISA_UPDATED=<message>` overrides the ISA-updated speech message.

Example:

```bash
PAI_CODEX_PULSE_ENABLED=1 PAI_CODEX_VOICE_ENABLED=1 codex exec --json "run pwd"
```

Smoke test:

```bash
~/.claude/codex/tests/test-voice-runtime.sh
```

Known limitations:

- Voice rendering depends on the local Pulse implementation.
- Codex does not perform direct speech rendering.
- Phase-transition voice is not emitted by Codex unless future Pulse events are added.

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

## What Is Not Included Yet

- Pulse features beyond basic optional notifications.
- Voice features beyond Pulse intent payloads.
- Write-capable custom agents.
- Private user state.

## Known Limitations

- Hooks are guardrails, not a complete security boundary. Codex sandboxing and approval policy remain authoritative.
- Prompt classification is deterministic by default and does not forward raw prompts to another model.
- ISA sync runs only when a supported PAI sync hook or tool is present.
- Pulse notifications are optional and disabled by default.
- Voice notifications are optional, disabled by default, and require Pulse.
- Custom agents installed by this package are read-only. Parent Codex remains responsible for writes.
- Private user state is not included in this package.
