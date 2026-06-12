---
name: pai-runtime-audit
description: Use when auditing PAI Codex runtime hooks, sandbox settings, permissions, logs, hashes, or installation health.
---

# PAI Runtime Audit Skill

Use this skill for bounded audits of installed Codex runtime support and DA/runtime parity.

## Check Surfaces

- `~/.codex/AGENTS.md`
- `~/.codex/hooks.json`
- `~/.codex/config.toml`
- `~/.claude/hooks/codex/*.sh`
- `~/.claude/hooks/codex/lib/*.py`
- `~/.claude/PAI/USER/PRINCIPAL_IDENTITY.md`
- `~/.claude/PAI/USER/DA_IDENTITY.md`
- `~/.claude/PAI/USER/PROJECTS/PROJECTS.md`
- `~/.claude/PAI/USER/TELOS/PRINCIPAL_TELOS.md`
- `~/.claude/PAI/ALGORITHM/LATEST`
- `~/.claude/PAI/MEMORY/WORK`
- `~/.claude/PAI/MEMORY/OBSERVABILITY`
- `~/.claude/PAI/MEMORY/LEARNING`
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
- Report missing PAI identity, DA, project, Telos, Algorithm, and Memory paths without mutating state.
- Resolve `ALGORITHM/LATEST` when it points to a file inside `~/.claude/PAI/ALGORITHM`.

## Script

Run `scripts/runtime-audit.sh` for a quick local audit. It emits concise `OK|WARN|FAIL` lines and does not modify files.
