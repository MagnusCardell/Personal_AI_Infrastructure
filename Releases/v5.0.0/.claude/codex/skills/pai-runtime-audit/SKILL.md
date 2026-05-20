---
name: pai-runtime-audit
description: Use when auditing PAI Codex runtime hooks, sandbox settings, permissions, logs, hashes, or installation health.
---

# PAI Runtime Audit Skill

Use this skill for bounded audits of installed Codex runtime support.

## Check Surfaces

- `~/.codex/AGENTS.md`
- `~/.codex/hooks.json`
- `~/.codex/config.toml`
- `~/.claude/hooks/codex/*.sh`
- `~/.claude/hooks/codex/lib/*.py`
- `~/.agents/skills/pai-*`
- `~/.codex/agents/pai_*.toml`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-*.jsonl`

## Audit Rules

- Treat hooks as guardrails, not complete enforcement.
- Verify `workspace-write` and `on-request` when the user wants normal contained operation.
- Verify unknown permission requests fall back to Codex approval.
- Verify runtime hooks do not create hidden backup behavior.
- Verify logs use structured safe logging and do not store raw prompts or raw commands by default.
- Verify custom agents are read-only.

## Script

Run `scripts/runtime-audit.sh` for a quick local audit. It reports findings and does not modify files.
