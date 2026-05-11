# Codex Peer Beta Adapter Payload

This directory contains the compact Codex peer beta adapter payload for the V5-S15A live activation pilot and the V5-S15B runtime end-to-end pilot.

The payload installs into `~/.claude/PAI` only through `tools.codex_adapter_installer`. It keeps Claude as the official/full-support upstream adapter and installs Codex as a peer beta router and bounded runtime pilot, not replacement readiness.

Installed live targets:

- `~/.claude/PAI/AGENTS.md`
- `~/.claude/PAI/adapters/codex/AGENTS.md`
- `~/.claude/PAI/adapters/codex/README.md`
- `~/.claude/PAI/adapters/codex/adapter-manifest.json`
- `~/.claude/PAI/adapters/codex/install-state.json`
- `~/.claude/PAI/adapters/codex/bin/pai-codex`
- `~/.claude/PAI/adapters/codex/runtime-proof.schema.json`
- `~/.claude/PAI/adapters/codex/runtime-state.json`

Runtime proof target:

- `~/.claude/PAI/adapters/codex/runs/s15b/runtime-proof.json`

Boundaries:

- No repo root `AGENTS.md`.
- No repo `.codex/`.
- No `~/.codex/` writes.
- No Codex hooks, rules, skills, agents, commands, launchers outside `~/.claude/PAI/adapters/codex/bin/`, or runtime files outside approved adapter targets.
- No Pulse bridge, Pulse startup, Pulse probe, or `localhost:31337` call.
- No PAI Memory writes.
- No ISA writes.
- No Claude Code invocation.
- Codex runtime invocation is approved only for the S15B bounded proof path.
