---
name: pai-algorithm
description: Use when a user asks Codex to run, structure, verify, or complete a PAI Algorithm task using live PAI state.
---

# PAI Algorithm Skill

Use this skill for Algorithm-shaped work: execution, implementation, design, investigation, verification, or work that creates or updates a PAI ISA.

## Live State

- PAI root: `~/.claude/PAI`
- Algorithm pointer: `~/.claude/PAI/ALGORITHM/LATEST`
- Algorithm files: `~/.claude/PAI/ALGORITHM`
- Work memory: `~/.claude/PAI/MEMORY/WORK`
- Learning memory: `~/.claude/PAI/MEMORY/LEARNING`
- Observability memory: `~/.claude/PAI/MEMORY/OBSERVABILITY`

Read `~/.claude/PAI/ALGORITHM/LATEST` before claiming the active Algorithm version. If the pointer is a version, resolve `~/.claude/PAI/ALGORITHM/v<version>.md`.

## Required Phase Names

Use these phase names for full Algorithm runs:

- OBSERVE
- THINK
- PLAN
- BUILD
- EXECUTE
- VERIFY
- LEARN

Do not claim a full Algorithm run unless all seven phases are present in the answer or work artifact.

## Runtime Rules

- Read live PAI state directly.
- Use `MEMORY/WORK/{slug}/ISA.md` for one-shot task state.
- Write `MEMORY/LEARNING` only when completion is explicit or clearly evidenced.
- Do not mutate `USER` state unless the user explicitly asks for that state change.
- Logs and evidence belong in `MEMORY/OBSERVABILITY`.
- Preserve Codex sandbox and approval semantics.
- Do not add runtime backup behavior.
