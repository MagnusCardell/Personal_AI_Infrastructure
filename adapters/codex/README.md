# Codex Peer Beta Adapter Payload

This directory contains the compact Codex peer beta adapter payload for the V5-S15B-R2 event-attributed runtime work-loop pilot.

The payload installs into `~/.claude/PAI` only through `tools.codex_adapter_installer`. It keeps Claude as the official/full-support upstream adapter and installs Codex as a peer beta router with a contained runtime launcher, not as replacement readiness.

Installed live targets:

- `~/.claude/PAI/AGENTS.md`
- `~/.claude/PAI/adapters/codex/AGENTS.md`
- `~/.claude/PAI/adapters/codex/README.md`
- `~/.claude/PAI/adapters/codex/adapter-manifest.json`
- `~/.claude/PAI/adapters/codex/install-state.json`
- `~/.claude/PAI/adapters/codex/bin/pai-codex`
- `~/.claude/PAI/adapters/codex/runtime-proof.schema.json`
- `~/.claude/PAI/adapters/codex/workloop-once.schema.json`
- `~/.claude/PAI/adapters/codex/runtime-validation.schema.json`
- `~/.claude/PAI/adapters/codex/runtime-state.json`

Approved runtime outputs:

- `~/.claude/PAI/adapters/codex/runs/s15b-r2/runtime-proof.json`
- `~/.claude/PAI/adapters/codex/runs/s15b-r2/workloop-once.json`
- `~/.claude/PAI/adapters/codex/runs/s15b-r2/runtime-events.jsonl`
- `~/.claude/PAI/adapters/codex/runs/s15b-r2/workloop-events.jsonl`
- `~/.claude/PAI/adapters/codex/runs/s15b-r2/runtime-validation.json`

Launcher commands:

- `pai-codex doctor`
- `pai-codex exec-proof`
- `pai-codex workloop-once`
- `pai-codex audit-run`

Event-attributed validation:

- Codex JSONL event streams are the primary write-boundary evidence.
- Filesystem mtime scanning is a secondary detector.
- Known PAI state/cache/log churn may be classified as ambient only when Codex event attribution is clean.

Boundaries:

- No repo root `AGENTS.md`.
- No repo `.codex/`.
- No PAI adapter files under `~/.codex/`.
- No Codex hooks, rules, skills, agents, or commands.
- No Codex launchers outside `~/.claude/PAI/adapters/codex/bin/`.
- No Pulse bridge, Pulse startup, Pulse probe, or local Pulse call.
- No PAI Memory writes.
- No ISA writes.
- No Claude Code invocation.
