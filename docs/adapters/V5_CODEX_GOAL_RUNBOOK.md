# V5 Codex Goal Runbook

## Purpose

This runbook defines how Codex `/goal` state may be used during PAI v5.0.0 adapter work without confusing Codex task orchestration metadata with canonical PAI state.

This is an S1 design artifact only. It does not authorize reading or writing `.codex/`, Codex memories, `~/.claude/`, live `PAI_DIR`, PAI Memory, ISA files, Pulse state, hooks, skills, agents, commands, settings, or release files.

## Principle

`/goal` is the persistent loop controller.

The milestone plan file is the self-evaluation contract.

The goal text should be short because the plan carries detailed acceptance criteria.

Long-running does not mean unbounded. A goal must have a milestone boundary, approved write set, stop conditions, validation commands, and handoff format.

Codex goal state is not PAI Memory, not ISA, and not Pulse state.

## Goal and Plan Relationship

Use `/goal` for persistence and loop continuity. Use the plan file for detail and self-evaluation.

The plan file should define:

- Purpose.
- Scope.
- Approved write set.
- Protected paths.
- Source material.
- Milestones.
- Self-review rubric.
- Hard failure conditions.
- Validation commands.
- Progress.
- Decision log.
- Retrospective.

The `/goal` objective should name the milestone and point to the plan. It should not duplicate the whole plan.

## Long-Horizon Goal Use

Long-horizon goals are allowed only when bounded by a milestone.

Allowed long-horizon use:

- One goal for one architect-approved milestone.
- A goal that can pause and resume without losing scope.
- A goal that ends with a handoff and a next architect decision.

Forbidden long-horizon use:

- `/goal` must not be used for the entire migration.
- `/goal` must not continue older pre-v5 work.
- `/goal` must not mutate the approved write set.
- `/goal` must not stay open after milestone handoff.

## When /goal Is Allowed

Use `/goal` when:

- The user or milestone explicitly allows it.
- The work needs persistent loop control.
- The scope is bounded.
- The plan file carries acceptance criteria.
- Protected paths are known.
- Validation commands are known.
- Handoff criteria are clear.

## When /goal Is Forbidden

Do not use `/goal` when:

- The user explicitly says not to use `/goal`.
- The task is a small documentation repair that can complete in one turn.
- The goal would cover the entire migration.
- The goal would continue older pre-v5 adapter work.
- The goal would blur design and implementation.
- The work would require reading `.codex/` or user-local Codex memory without explicit approval.
- The work would require writing PAI Memory, ISA, Pulse state, settings, hooks, skills, agents, commands, installers, or release files outside the approved scope.

## Starting a Goal

When starting an approved goal:

- Create exactly one goal.
- Keep the goal text short.
- Name the milestone.
- Reference the plan file.
- Include the approved write set or state that the plan file defines it.
- Include a no-implementation clause when the milestone is design-only.
- Confirm protected paths.

The first repository write should usually be the plan file.

## Working a Goal

While working a goal:

- Keep progress in the plan file.
- Keep edits inside the approved write set.
- Cite evidence from S0 or approved source material.
- Treat Codex goal state as orchestration metadata only.
- Keep PAI Memory and ISA canonical.
- Do not treat goal progress as Pulse progress.
- Do not promote product memories into PAI Memory.
- Update the plan when decisions or validation results change.

## Pausing a Goal

Pause only when:

- The user asks to pause.
- An approval or architect decision is required.
- A hard failure condition is reached.
- Continuing would require protected path modification.

The pause note should record status, files touched, remaining validation, blocker, and next required decision.

## Resuming a Goal

When resuming:

- Re-read the plan file.
- Run `git status --short`.
- Confirm the newest user request still matches the goal.
- Confirm protected paths remain untouched.
- Continue from recorded progress rather than restarting.

If the user changes scope, do not silently mutate the old goal.

## Clearing a Goal

`/goal clear` should be run after milestone handoff when goal tooling is available and clearing is part of the workflow.

Clearing is appropriate when:

- Final handoff has been delivered.
- Validation is complete.
- No follow-up work remains inside the milestone.
- The next step requires a separate architect decision.

Goal clearing does not delete PAI state because Codex goal state is not PAI Memory.

## Evidence Requirements

Every adapter goal must identify its evidence base.

For S1-class work, evidence should come from:

- `docs/adapters/V5_S0_DISCOVERY_PLAN.md`
- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- Upstream release paths cited by S0

Do not inspect:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`

## Self-Evaluation Requirements

Each milestone plan must include a self-review rubric.

The rubric should cover evidence discipline, boundary discipline, design-only scope, protected path hygiene, state separation, authority preservation, Pulse centrality, existing-user safety, reversibility, validation commands, and handoff requirements.

The goal is complete only when the rubric passes or failures are explicitly reported.

## Stop Conditions

Stop and ask for review if goal completion requires:

- Creating runtime adapter files during a design-only milestone.
- Modifying release files.
- Modifying `.codex/`.
- Modifying `.claude/`, `PAI/`, hooks, skills, agents, commands, settings, installers, prompts, or user-local state.
- Running installers or migrations.
- Starting Pulse.
- Invoking Claude Code or Codex import tooling.
- Treating Codex goal state as PAI Memory.
- Treating goal completion as ISA acceptance.
- Treating goal state as Pulse state.
- Continuing older pre-v5 adapter work.

## Required Verification Before Completion

Before completing a documentation milestone:

- Run `git status --short`.
- Run `git diff --name-only | sort`.
- Run `git diff --check`.
- Run any milestone-specific changed-file check.
- Run any milestone-specific heading or content check.
- Run protected-path status checks.
- Confirm that only the approved write set changed.
- Confirm no runtime behavior was authorized.

## Required Milestone Handoff Format

The final handoff for adapter milestones must include these headings:

- `## Files changed`
- `## Behavior changed`
- `## Tests run`
- `## Known risks`
- `## Protected files changed`
- `## Recommended next architect decision`

The handoff must distinguish documentation changes from runtime behavior changes.

## S1 Approved Goal

The approved S1 goal was a bounded documentation strategy milestone. It created the S1 architecture set and did not implement a Codex adapter.

S1R does not use `/goal` because the user explicitly forbade `/goal` for this repair.

S1 establishes these runbook lessons:

- `/goal` is useful for bounded strategy milestones.
- The plan file carries detailed acceptance criteria.
- `/goal` must not be used for the entire migration.
- `/goal` must not continue older pre-v5 work.
- `/goal clear` should be run after milestone handoff when a goal was used.

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
