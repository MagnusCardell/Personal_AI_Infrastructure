# V5 Codex Goal Runbook

## Purpose

This runbook defines how Codex `/goal` state may be used during PAI v5.0.0 adapter work without confusing Codex task orchestration metadata with canonical PAI state.

This is an S1 design artifact only. It does not authorize reading or writing `.codex/`, Codex memories, `~/.claude/`, live `PAI_DIR`, PAI Memory, ISA files, Pulse state, hooks, skills, agents, commands, settings, or release files.

## Evidence Baseline

S0 established the required state separation:

- PAI Memory at `~/.claude/PAI/MEMORY/` is canonical PAI state (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:1-15`).
- ISA is the system-of-record primitive and single source of truth for the work being articulated (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md:1-10`).
- Claude Code native project memory is separate from PAI Memory (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:7-15`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:112-123`).
- Codex memory and Codex goal state were not read in S0 and must be treated as separate non-PAI state surfaces unless a future adapter explicitly bridges them (`docs/adapters/V5_S0_DISCOVERY_REPORT.md`, "Dual Claude/Codex Subscription Memory Implications").
- Product memories must not be silently promoted into `PAI/MEMORY/KNOWLEDGE` or `PAI/MEMORY/WORK` (`Releases/v5.0.0/.claude/PAI/MEMORY/KNOWLEDGE/README.md:1-7`, `Releases/v5.0.0/.claude/PAI/MEMORY/WORK/README.md:1-7`).

## Core Rule

Codex `/goal` state is orchestration metadata. It is not PAI Memory, not an ISA, not Pulse state, not Claude Code memory, and not proof that canonical PAI state has changed.

Goal state may describe work being done by Codex. It must not become the place where PAI stores project truth, done conditions, durable memory, relationship learning, user identity, or system doctrine.

## State Classification

| Surface | Classification | S1 Handling |
| --- | --- | --- |
| Codex `/goal` objective and progress | Codex task metadata | Allowed for managing this S1 task. Do not export to PAI Memory automatically. |
| `docs/adapters/V5_S1_EXEC_PLAN.md` progress | S1 repository documentation | Allowed because it is in the approved write set. |
| `docs/adapters/*.md` strategy outputs | S1 repository documentation | Allowed because these are approved docs. |
| `PAI/MEMORY/WORK/{slug}/ISA.md` | Canonical PAI work state | No read/write in S1 except release evidence already cited by S0. Future writes require single-writer policy. |
| `PAI/MEMORY/KNOWLEDGE` | Curated PAI long-term semantic memory | No promotion from Codex goal state. |
| Claude Code project memory | Claude product memory | Separate from PAI Memory. No bridging in S1. |
| Codex memory | Codex product memory | Not read or written in S1. Separate from PAI Memory. |
| Pulse observability and jobs | PAI runtime infrastructure | No live calls or writes in S1. Future bridge requires provenance. |

## When To Start A Codex Goal

Use a Codex goal only for bounded work where the objective, write set, stop conditions, and completion proof can be stated upfront.

For adapter work, the goal objective should include:

- The exact milestone name.
- The approved write set.
- Explicit protected paths.
- A no-implementation clause if the milestone is design-only.
- Required verification before closure.

The current S1 goal fits that model because it is limited to five docs under `docs/adapters/` and explicitly forbids runtime adapter implementation.

## Goal Startup Checklist

Before doing work inside a Codex goal:

- Confirm whether the goal is design-only or implementation-capable.
- Record the approved write set.
- Record protected paths and user-local paths.
- Identify canonical PAI state surfaces that must not be touched.
- Identify whether release files are evidence-only.
- Decide where progress should be recorded. For S1, progress belongs in `V5_S1_EXEC_PLAN.md`, not PAI Memory.
- Confirm that no `.codex/`, `~/.codex/`, `~/.claude/`, or live `PAI_DIR` inspection is needed.

## During-Goal Rules

- Keep repository edits inside the approved write set.
- Treat Codex goal progress as local orchestration, not as canonical memory.
- Cite S0 or upstream release evidence for strategy claims.
- Do not write an ISA unless a future phase explicitly makes ISA the approved write target and establishes single-writer control.
- Do not create a "goal summary" under PAI Memory.
- Do not promote observations into `PAI/MEMORY/KNOWLEDGE` without a future explicit curation workflow.
- Do not treat a completed Codex goal as Pulse job completion unless a future Pulse bridge has emitted a provenance-labeled event.
- Do not let goal status replace test evidence, review evidence, or rollback evidence.

## Goal Closure Checklist

Before closing a Codex goal for adapter work:

- Verify changed files are exactly within the approved write set.
- Verify protected paths are not modified.
- Verify no runtime adapter files were created.
- Verify all stated acceptance criteria are satisfied or list failures explicitly.
- Verify the final answer distinguishes repository docs from canonical PAI state.
- If any information should become PAI Memory in a future phase, record it as a proposed curation item only. Do not write it directly.

## Promotion Policy

Codex goal state can be promoted into canonical PAI state only in a future phase that has all of the following:

- An explicit user or architect decision to promote.
- A single-writer policy for the target PAI state.
- A provenance record linking source goal, reviewer, adapter version, and target state path.
- A curation rule appropriate to the target memory class.
- Rollback behavior.
- Verification that the target is not product memory or private Codex state.

Without those conditions, Codex goals remain non-canonical.

## Relationship To ISA

ISA is the PAI system-of-record primitive. A Codex goal may help execute a task, but it must not become a shadow ISA.

Future adapter behavior should follow these rules:

- If an ISA exists, the goal may reference it but does not supersede it.
- If no ISA exists, the goal may not silently create a replacement acceptance artifact.
- Done conditions belong in ISA or approved project documentation, not only in Codex goal metadata.
- Goal closure is not equivalent to ISA acceptance unless a future bridge records that relationship explicitly.

## Relationship To PAI Memory

PAI Memory is curated canonical state. Codex goals are operational metadata.

Allowed:

- Use a goal to track S1 progress.
- Summarize goal results in approved repository docs.
- Record proposed future memory curation items in docs when the milestone permits it.

Prohibited:

- Writing Codex goal summaries into `PAI/MEMORY`.
- Treating Codex memory as `PAI/MEMORY/KNOWLEDGE`.
- Treating Claude Code memory as PAI Memory.
- Treating goal progress as relationship memory, learning memory, or work memory.

## Relationship To Pulse

Pulse is central v5 runtime infrastructure. Codex goals are outside Pulse unless a future adapter bridge proves otherwise.

Future bridge requirements:

- A goal-start event must identify Codex as the source engine and state whether the run is fixture, read-only, shadow, or live.
- A goal-progress event must avoid writing canonical state unless single-writer gates are satisfied.
- A goal-complete event must not imply ISA acceptance unless linked to canonical verification evidence.
- A goal-failed event must include rollback or no-write status.

S1 does not emit Pulse events or call Pulse endpoints.

## Abort Conditions

Stop a goal and report the blocker if completion requires:

- Reading or writing `.codex/`, `~/.codex/`, or Codex memories.
- Reading or writing `~/.claude/` or live `PAI_DIR`.
- Starting Pulse or invoking local dashboard endpoints.
- Running installers, migrations, or import tools.
- Creating runtime adapter files during a design-only milestone.
- Writing PAI Memory, ISA, settings, hooks, skills, agents, commands, or release files outside the approved scope.

## S1 Application

For V5-S1, this runbook means:

- The Codex goal is a bounded project-management control for the documentation task.
- The living contract is `docs/adapters/V5_S1_EXEC_PLAN.md`.
- The strategy outputs are repository docs only.
- No canonical PAI state changes are made.
- Completing the goal proves only that the S1 docs and checks are complete. It does not prove Codex runtime compatibility.
