---
name: pai-memory
description: Use when reading, summarizing, or safely writing PAI Memory under live ~/.claude/PAI paths.
---

# PAI Memory Skill

Use this skill for live PAI memory reads, summaries, evidence writes, or explicitly requested safe memory updates.

## Memory Map

- User state: `~/.claude/PAI/USER`
- Work memory: `~/.claude/PAI/MEMORY/WORK`
- Learning memory: `~/.claude/PAI/MEMORY/LEARNING`
- Observability memory: `~/.claude/PAI/MEMORY/OBSERVABILITY`

Read live files when they exist. Do not answer from recollection when the live file is available.

## Write Rules

- `MEMORY/WORK`: write for execution-oriented tasks and Algorithm work artifacts.
- `MEMORY/OBSERVABILITY`: write evidence, logs, manifests, and verification records.
- `MEMORY/LEARNING`: write only when completion is explicit or clearly evidenced.
- `USER`: do not mutate identity, projects, Telos, or preferences unless the user explicitly asks.

## Secret Boundaries

Never read or write auth material, private keys, cloud credentials, environment files, tokens, passwords, API keys, or credential URLs unless explicitly instructed and approved.

If logs include previews, redact sensitive values first. Prefer hashes, summaries, and risk flags over raw prompt or command text.

## Runtime Safety

Memory writes are live runtime behavior. They are not installer backups. Runtime hooks must not create hidden backup jobs or hidden maintenance.
