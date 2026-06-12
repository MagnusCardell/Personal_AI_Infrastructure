# PAI Codex Runtime Support

## What This Package Does

This optional package lets Codex operate against a local PAI install. It installs Codex hooks, runtime instructions, safe logging helpers, optional PAI skills, and read-only review agents.

With it enabled, Codex can:

- read live PAI identity, project, and Telos context from `~/.claude/PAI`
- classify prompts into `MINIMAL`, `NATIVE`, or `ALGORITHM`
- follow the PAI Algorithm and create/update canonical ISA files
- write structured observability logs with redaction
- use Codex hook semantics correctly
- add defense-in-depth pre-tool checks for known sink domains, shell-injection forms, and protected paths
- optionally write completion-gated Algorithm learning records
- optionally checkpoint completed ISA criteria into git when explicitly enabled
- optionally regenerate the managed `AGENTS.md` block from live PAI doctrine
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

AGENTS regeneration from live PAI state is manual by default. Use `--generate-agents` with `--global` only when you explicitly want the installer to run the generator during activation.

## What Changes On Disk

PAI-local staging may write:

- `~/.claude/codex/*`
- `~/.claude/codex/tools/*`
- `~/.claude/hooks/codex/*.sh`
- `~/.claude/hooks/codex/lib/*.py`
- `~/.claude/hooks/codex/pulse.env`

Global activation may also write:

- `~/.codex/AGENTS.md`
- `~/.codex/hooks.json`
- `~/.codex/config.toml`
- `~/.codex/pai-config.example.toml`
- `~/.agents/skills/pai-*`
- `~/.codex/agents/pai_*.toml`

Existing `AGENTS.md` receives a managed PAI block. Existing `hooks.json` keeps non-PAI hook groups and receives PAI hook groups. Existing `config.toml` keeps user writable roots and adds required PAI roots if missing.

Before overwriting user files, the installer creates installer-local backups under `~/.claude/codex/backups`. These are install-time backups only. The runtime does not create backups, retention jobs, or hidden maintenance. Existing local `pulse.env` files are preserved unless `--force-replace` is used.

## Install

Dry-run first:

```bash
~/.claude/codex/install-codex.sh --global --dry-run
```

Then activate:

```bash
~/.claude/codex/install-codex.sh --global
```

Preview AGENTS regeneration without writing:

```bash
bun ~/.claude/codex/tools/GenerateAgentsMd.ts --dry-run
```

Activate and regenerate the managed AGENTS block in one explicit step:

```bash
~/.claude/codex/install-codex.sh --global --generate-agents
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

Full package test runner:

```bash
~/.claude/codex/tests/run-all.sh
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
~/.claude/codex/tests/test-learning-runtime.sh
~/.claude/codex/tests/test-generate-agents.sh
~/.claude/codex/tests/test-security-runtime.sh
~/.claude/codex/tests/test-checkpoint-runtime.sh
~/.claude/codex/tests/test-skill-dispatch-runtime.sh
```

These tests use a temporary HOME and do not require a real Codex CLI.

Maintainers should also run `shellcheck` when it is available locally. See `~/.claude/codex/RELEASE_CHECKLIST.md` for the exact release check sequence.

## Optional Pulse Notifications

Pulse notifications are disabled by default and are never required for runtime correctness. When enabled, Stop sends a turn-complete notification and ISA updates may send an `codex.algorithm.isa_updated` notification after ISA detection or sync activity.

Environment variables:

- `PAI_CODEX_PULSE_ENABLED=1` enables notifications.
- `PAI_CODEX_PULSE_URL=http://localhost:31337` sets the Pulse base URL. If unset while enabled, the default is `http://localhost:31337`.

Persistent local enablement can be configured in `~/.claude/hooks/codex/pulse.env`. The packaged default keeps Pulse disabled.

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

Persistent local voice settings can be configured in `~/.claude/hooks/codex/pulse.env`. The packaged default keeps voice disabled and does not include a voice identifier.

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

## Security Guardrails

The pre-tool hook includes defense-in-depth checks for common high-risk tool requests. These checks are guardrails, not complete enforcement. Codex sandboxing and approval policy remain authoritative.

The package checks:

- known exfiltration or sink URL domains in applicable command text
- dangerous shell forms such as command substitution and network input piped into a shell
- detectable Write/Edit/MultiEdit/apply_patch targets outside configured PAI or workspace roots
- protected credential and system paths

Normal local operations, localhost Pulse calls, GitHub API/raw GitHub reads, and ordinary package or git operations are not blocked unless they match a dangerous pattern. Decisions are written to `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-pretool.jsonl` using safe structured logging.

Smoke test:

```bash
~/.claude/codex/tests/test-security-runtime.sh
```

## Skill Invocation

Minimal package skills are available after install through an explicit dispatcher. The runtime does not auto-run skills during install and does not treat skill dispatch as a separate agent surface.

Command pattern:

```bash
~/.claude/hooks/codex/skills/dispatch.sh isa_append <ISA.md> <decisions|changelog|verification> "<content>"
```

`isa_append` appends redacted content to `## Decisions`, `## Changelog`, or `## Verification` in a canonical ISA under `~/.claude/PAI/MEMORY/WORK/*/ISA.md`. It rejects paths outside work memory, non-ISA filenames, symlink escapes, unsupported sections, and empty content.

Additional dispatch routes:

```bash
# Create a deterministic starter task ISA (all twelve sections, refuses overwrite)
~/.claude/hooks/codex/skills/dispatch.sh isa_scaffold --tier E2 "<task>"

# Deterministic multi-lens requirement exploration (candidate criteria, not verified facts)
~/.claude/hooks/codex/skills/dispatch.sh iterative_depth --depth 4 "<problem>"

# Phase-1 scan of prior PAI work (registry, session names, WORK dirs, ISA titles)
~/.claude/hooks/codex/skills/dispatch.sh context_search <term> [term...]

# Run a fabric pattern via the locally installed fabric CLI (input on stdin)
cat input.md | ~/.claude/hooks/codex/skills/dispatch.sh fabric extract_wisdom

# Second-opinion advisor; provider is explicit opt-in configuration
~/.claude/hooks/codex/skills/dispatch.sh advisor "TASK: ..." "QUESTION: ..."
```

`context_search` is read-only and degrades gracefully when registries are missing. `fabric` exits with a clear message when the fabric binary is not installed. `advisor` requires `PAI_CODEX_ADVISOR_PROVIDER` to be set (`claude-inference` routes through the live PAI inference tool; `codex-exec` spawns a read-only Codex subprocess); unset, it fails loudly with exit 4 so an absent review is never mistaken for an approving one. Empty advisor output is reported as inconclusive (exit 5), never as approval.

Execution metadata is written to:

```text
~/.claude/PAI/MEMORY/SKILLS/codex-execution.jsonl
```

The skill does not run git, does not trigger checkpointing directly, and does not perform network calls. Parent Codex remains responsible for deciding when explicit dispatch is appropriate.

Smoke test:

```bash
~/.claude/codex/tests/test-skill-dispatch-runtime.sh
```

## Optional CheckpointPerISC

Checkpointing is disabled by default. The public package does not enable automatic git commits unless the local operator explicitly sets:

```bash
export PAI_CODEX_CHECKPOINT_ENABLED=1
```

When enabled, `post-tool-use.sh` watches canonical task ISA paths under `~/.claude/PAI/MEMORY/WORK/*/ISA.md`. It tracks checkbox state in:

```text
~/.claude/PAI/MEMORY/OBSERVABILITY/codex-isa-state.json
```

Only criterion transitions from `- [ ] ISC-N` to `- [x] ISC-N` are checkpoint candidates. Ordinary ISA writes without a new completed criterion do not create commits.

Checkpoint commits run only inside `~/.claude` when that directory is a git repository. If unrelated local changes are present, checkpointing skips and logs the reason instead of trying to clean or rewrite the working tree. Commit messages use:

```text
ISC checkpoint: {slug} — {ISC ids}
```

Checkpoint attempts are logged to `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-checkpoint.jsonl`. The runtime does not create backups or hidden maintenance jobs.

Smoke test:

```bash
~/.claude/codex/tests/test-checkpoint-runtime.sh
```

## Optional Stop-Gated Learning

Stop-gated learning is disabled by default. When `PAI_CODEX_LEARNING_ENABLED=1`, `stop.sh` scans `~/.claude/PAI/MEMORY/WORK` for `ISA.md` files whose top metadata has `phase: complete` or `phase: learn`. Matching ISAs are passed to `hooks/lib/learning.py`.

The helper writes only explicit learning material already present in `## Changelog`, `## Learning`, or compatible learning-marked ISA sections. It does not invent learnings. Records are JSONL under:

```text
~/.claude/PAI/MEMORY/LEARNING/ALGORITHM/YYYY-MM/session.jsonl
```

Each record includes timestamp, source, ISA slug, ISA path, phase, entries, and a content hash. Existing hashes are skipped so repeated Stop events do not duplicate the same ISA learning record. Learning failures are non-blocking and Stop still returns `{}`.

Persistent local enablement can be configured in `~/.claude/hooks/codex/pulse.env`:

```bash
export PAI_CODEX_LEARNING_ENABLED=1
```

Smoke test:

```bash
~/.claude/codex/tests/test-learning-runtime.sh
```

## AGENTS.md Regeneration

`tools/GenerateAgentsMd.ts` regenerates only the managed block between:

```text
<!-- PAI-CODEX:BEGIN managed by Personal_AI_Infrastructure -->
<!-- PAI-CODEX:END managed by Personal_AI_Infrastructure -->
```

Content outside the managed block is preserved. The generator reads bounded PAI identity, runtime assistant identity, the Algorithm pointer and resolved Algorithm file, plus the packaged `AGENTS.md.template`. It does not read private project detail directories, logs, learning files, or broad PAI Memory.

Dry-run writes nothing and prints a summary:

```bash
bun ~/.claude/codex/tools/GenerateAgentsMd.ts --dry-run
```

Write the default target:

```bash
bun ~/.claude/codex/tools/GenerateAgentsMd.ts
```

Use a custom PAI root or output:

```bash
bun ~/.claude/codex/tools/GenerateAgentsMd.ts --pai-dir /path/to/PAI --output /path/to/AGENTS.md
```

The installer does not run this generator unless `--generate-agents` is supplied. Uninstall never removes user `AGENTS.md`; it only removes the managed block when present.

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

If `pulse.env` still matches the packaged disabled defaults, uninstall removes it. If it appears locally modified, uninstall preserves it and prints a notice.

## Optional Diagnostic Probe

The package includes `~/.claude/hooks/codex/probe.sh` as a passive diagnostic hook for hook-event troubleshooting. It is not enabled by default in `hooks.json.template`. If you enable it manually, it writes redacted event summaries to `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-runtime-probe.jsonl` and avoids raw prompt or command logging.

## Classifier Decision (Accepted Design)

The prompt classifier in `prompt-processing.sh` is local, deterministic keyword matching. This is an accepted design decision, not a temporary gap:

- **Privacy:** raw prompts are never logged or forwarded to another model (`PAI_PRIVACY=raw_prompt_not_logged_or_forwarded`).
- **Latency:** classification is effectively instant; a model-inference classifier adds seconds to every prompt.
- **Cost:** no external billing surface in the hook path.
- **Known weakness:** context-dependent escalation (a short approval like "yes" after a multi-step proposal) is misclassified in isolation. This is mitigated executor-side: the generated AGENTS.md `Context Override Escalation` section instructs the runtime to inherit mode and tier from conversation context and record the override in the active ISA.

**Revisit trigger:** audit `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-prompt-classification.jsonl` periodically; if observed misclassification materially affects tier selection beyond what executor-side escalation corrects, reopen this decision.

## What Is Not Included Yet

- Pulse features beyond basic optional notifications.
- Voice features beyond Pulse intent payloads.
- Write-capable custom agents.
- Private user state.

## Known Limitations

- Hooks are guardrails, not a complete security boundary. Codex sandboxing and approval policy remain authoritative.
- Prompt classification is deterministic by default and does not forward raw prompts to another model (see Classifier Decision above).
- The advisor skill is opt-in and inert until `PAI_CODEX_ADVISOR_PROVIDER` is configured.
- ISA sync runs only when a supported PAI sync hook or tool is present.
- Pulse notifications are optional and disabled by default.
- Voice notifications are optional, disabled by default, and require Pulse.
- Custom agents installed by this package are read-only. Parent Codex remains responsible for writes.
- Private user state is not included in this package.
