---
name: pai-isa
description: Use when creating or updating PAI ISA.md files, Ideal State Criteria, status markers, verification, or ISASync behavior.
---

# PAI ISA Skill

Use this skill when a task touches an ISA file, Ideal State Criteria, status markers, verification evidence, or ISASync behavior.

## Canonical Pathing

For one-shot PAI work, use:

`~/.claude/PAI/MEMORY/WORK/{slug}/ISA.md`

Use a clear slug such as `YYYYMMDD-HHMMSS_short-purpose`. Do not place task ISAs in arbitrary memory paths.

## Minimum Shape

An E1 task ISA may be minimal, but it must include:

- frontmatter with `task`, `slug`, `effort`, `phase`, `progress`, `mode`, `started`, `updated`
- `## Goal`
- `## Criteria`
- verification evidence before criteria are marked complete

Higher-tier work should follow the active Algorithm's tier rules.

## Status Markers

- Mark criteria `[x]` only after verification exists.
- Keep `phase` honest.
- Keep `progress` consistent with checked criteria.
- Do not fabricate passing verification.

## ISASync

PostToolUse may run an available PAI sync tool when it detects a canonical live ISA path. Supported locations:

- `~/.claude/PAI/TOOLS/ISASync.ts`
- `~/.claude/hooks/ISASync.hook.ts`

If sync is absent or fails, log the result honestly.

## Validation

Use `scripts/validate-isa.sh <path-to-ISA.md>` for a basic structural check. It is not a substitute for verification tied to the actual task.
