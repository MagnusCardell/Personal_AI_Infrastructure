# Codex Peer Beta Adapter Payload

This directory contains the compact Codex peer beta adapter payload for the V5-S15A live activation pilot.

The payload installs into `~/.claude/PAI` only through `tools.codex_adapter_installer`. It keeps Claude as the official/full-support upstream adapter and installs Codex as a peer beta router, not a replacement-grade adapter.

Installed live targets:

- `~/.claude/PAI/AGENTS.md`
- `~/.claude/PAI/adapters/codex/AGENTS.md`
- `~/.claude/PAI/adapters/codex/README.md`
- `~/.claude/PAI/adapters/codex/adapter-manifest.json`
- `~/.claude/PAI/adapters/codex/install-state.json`

Boundaries:

- No repo root `AGENTS.md`.
- No repo `.codex/`.
- No `~/.codex/` writes.
- No Codex hooks, rules, skills, agents, commands, launchers, or runtime files.
- No Pulse bridge, Pulse startup, Pulse probe, or `localhost:31337` call.
- No PAI Memory writes.
- No ISA writes.
- No Claude Code invocation.
- No Codex runtime invocation.
