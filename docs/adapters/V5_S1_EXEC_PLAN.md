# V5-S1 Execution Plan

## Purpose

Synthesize the V5-S0 discovery evidence into the first coherent Codex replacement-adapter strategy for PAI v5.0.0.

S1 is a design and documentation milestone only. It must not implement a Codex adapter, create runtime adapter files, modify release assets, or touch user-local state.

## Scope

Canonical source evidence:

- `docs/adapters/V5_S0_DISCOVERY_PLAN.md`
- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- Repository paths cited by the S0 report under `Releases/v5.0.0/`

S1 may reason about the upstream v5.0.0 Claude Code-native release, but it may not change it.

## Approved Write Set

Only these repository files may be created or modified during S1:

- `docs/adapters/V5_S1_EXEC_PLAN.md`
- `docs/adapters/V5_UPSTREAM_RISK_REGISTER.md`
- `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
- `docs/adapters/V5_CODEX_GOAL_RUNBOOK.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`

## Protected Paths

Protected from modification during S1:

- `Releases/`
- `.claude/`
- `.codex/`
- `.github/`
- `.agents/`
- `PAI/`
- `CLAUDE.md`
- `AGENTS.md`
- `install.sh`
- `settings.json`
- `hooks/`
- `skills/`
- `agents/`
- `commands/`
- `subagents/`
- Any installer, release, runtime adapter, hook, skill, agent, command, settings, or user-local state file

## Source Material

S1R may read but must not modify:

- `docs/adapters/V5_S0_DISCOVERY_PLAN.md`
- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`

The S0 discovery report is the canonical evidence baseline for this repair. It establishes that PAI v5.0.0 is Claude Code-native, Codex is not currently proven drop-in for existing local PAI v5 files, PAI Memory and ISA artifacts are canonical PAI state, Pulse is central v5 infrastructure, and `PAI_SYSTEM_PROMPT.md` is high-authority doctrine.

The five S1 documents themselves are the only approved repair targets. Release files and user-local state remain evidence-only or protected.

## Milestones

S1R milestones:

1. Normalize the execution plan so it records scope, source material, validation commands, and retrospective sections.
2. Expand the upstream risk register with scoring, risk IDs, existing-local-v5 scenarios, memory/state distinctions, and architect review requirements.
3. Expand the runtime strategy with replacement thesis, explicit drop-in answer, user modes, adapter lanes, and replacement readiness criteria.
4. Expand the goal runbook with bounded `/goal` lifecycle rules and final handoff format.
5. Expand the adapter boundaries document with surface definitions, native surface rules, transformation rules, read/write policy, and review gates.
6. Run the required validation commands.
7. Repair any validation failure without touching files outside the approved write set.

## Non-Goals

S1 must not:

- Implement a Codex adapter.
- Create launcher, runtime, hook, skill, agent, command, installer, settings, or migration files.
- Start Pulse, invoke Claude Code, invoke Codex import or migration tooling, or install dependencies.
- Read or write user-local private state such as `~/.claude/`, `~/.codex/`, or Codex memories.
- Define S1 as permission to run Codex against existing local PAI v5 files with write privileges.
- Advance into S2 implementation planning beyond naming the evidence gates that S2 must satisfy.

## Required Outputs

S1 must produce four strategy documents after this execution plan:

- `V5_UPSTREAM_RISK_REGISTER.md`: risk register for upstream v5.0.0 replacement-adapter work.
- `V5_CODEX_RUNTIME_STRATEGY.md`: runtime strategy for a Codex replacement adapter, with explicit read-only-first posture.
- `V5_CODEX_GOAL_RUNBOOK.md`: runbook for using Codex goal state around PAI without confusing it with canonical PAI state.
- `V5_ADAPTER_BOUNDARIES.md`: boundary contract for engine-neutral PAI state, Claude-specific surfaces, Codex-specific surfaces, and prohibited writes.

## Working Sequence

1. Create this execution plan first.
2. Re-read S0 conclusions and targeted evidence as needed.
3. Draft the risk register.
4. Draft the runtime strategy.
5. Draft the Codex goal runbook.
6. Draft the adapter boundaries.
7. Cross-check all four outputs against the acceptance criteria and self-review rubric below.
8. Update this execution plan with final progress and verification results.

## Acceptance Criteria

S1 passes only if all criteria below are satisfied:

- Exactly the five S1 approved files are created or modified relative to the pre-S1 clean state.
- No protected path is modified.
- No runtime adapter files, installer files, release files, root `AGENTS.md`, `.codex/`, `.claude/`, `PAI/`, hooks, skills, agents, commands, settings, or user-local state are created or modified.
- Each S1 strategy document cites S0 evidence or release paths rather than relying on undocumented assumptions.
- The strategy preserves the S0 conclusion that Codex is not a drop-in replacement for PAI v5.0.0.
- The strategy treats `PAI_SYSTEM_PROMPT.md` as high-authority doctrine requiring equivalent Codex authority semantics.
- The strategy treats Pulse as central v5 infrastructure and requires an explicit event bridge before dashboard or job parity is claimed.
- The strategy treats ISA and PAI Memory as canonical PAI state.
- The strategy keeps PAI Memory, Claude Code memory, Codex memory, and Codex goal state distinct unless a future adapter explicitly bridges them with provenance.
- The strategy requires read-only fixture validation before any live local v5 write path.
- The strategy requires reversible setup and rollback behavior that does not uninstall Claude Code.
- The strategy requires a single-writer policy before any Codex adapter writes to `PAI/MEMORY`, ISA files, `STATE/work.json`, observability JSONL, user identity files, or Pulse state.
- The risk register includes risk identifiers, affected surfaces, severity, mitigation, verification gates, and S2 decision implications.
- The runtime strategy defines adapter lanes for authority, launcher/inference, hooks/events, Pulse, skills/commands/agents, settings, and state access.
- The goal runbook defines how Codex `/goal` state may be used as task orchestration metadata without becoming canonical PAI memory or ISA truth.
- The adapter boundaries document distinguishes allowed S1 design claims, future adapter responsibilities, prohibited behavior, and phase gates.
- Open unknowns are explicitly recorded rather than hidden as implementation certainty.

## Self-Review Rubric

Before completion, mark each item as pass/fail in the final progress section:

- Evidence discipline: every major claim traces to S0 or cited upstream v5 release evidence.
- Boundary discipline: S1 does not create implementation pressure or implied permission to write live PAI state.
- State discipline: canonical PAI state is separate from product memory and goal metadata.
- Authority discipline: high-authority doctrine is preserved as a first-class adapter problem.
- Pulse discipline: Pulse remains central, with no unsupported claim of Codex dashboard or job parity.
- Existing-user safety: the strategy is safe for users who already have local v5 files and does not require uninstalling Claude Code.
- Reversibility: rollback, fixture testing, and no-live-write gates are explicit.
- S2 readiness: the docs create a clear next review target without advancing beyond S1.
- Scope hygiene: final changed-file verification names only the S1 approved write set.

## Hard Failure Conditions

Stop and report a failure if completion requires:

- Creating runtime adapter files.
- Modifying release files.
- Modifying root `AGENTS.md`.
- Modifying `.codex/`.
- Modifying `.claude/`, `PAI/`, hooks, skills, agents, commands, settings, installers, prompts, or user-local state.
- Reading private user-local state under `~/.claude/`, `~/.claude/PAI/`, `~/.claude/projects/`, `~/.codex/`, or `~/.codex/memories/`.
- Starting Pulse or calling local Pulse endpoints.
- Running installers, migrations, Claude Code, Codex import tooling, or dependency installation.
- Claiming Codex is drop-in today.
- Claiming Codex is the official upstream engine today.
- Claiming Claude-shaped files can be copied directly into Codex native surfaces.
- Authorizing PAI Memory, ISA, Pulse, settings, hook, skill, agent, command, or installer writes.

## Validation Commands

Required commands from repository root:

```bash
git status --short
git diff --name-only | sort
git diff --check
```

Required changed-file check:

```bash
python3 - <<'PY'
import subprocess

expected = [
    "docs/adapters/V5_ADAPTER_BOUNDARIES.md",
    "docs/adapters/V5_CODEX_GOAL_RUNBOOK.md",
    "docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md",
    "docs/adapters/V5_S1_EXEC_PLAN.md",
    "docs/adapters/V5_UPSTREAM_RISK_REGISTER.md",
]

actual = sorted(subprocess.check_output(
    ["git", "diff", "--name-only"],
    text=True,
).splitlines())

if actual != expected:
    print("unexpected changed files")
    print("expected:")
    print("\n".join(expected))
    print("actual:")
    print("\n".join(actual))
    raise SystemExit(1)

print("changed files ok")
PY
```

Required heading and content checks are the Python checks supplied by the S1R request.

Required protected-path check:

```bash
git status --short -- Releases/ .claude/ PAI/ CLAUDE.md AGENTS.md .codex/ install.sh settings.json hooks/ skills/ subagents/ agents/ commands/ .github/ .agents/
```

Expected protected-path result: no output.

## Progress

- Created this S1 execution plan as the living self-evaluation contract.
- Created `docs/adapters/V5_UPSTREAM_RISK_REGISTER.md`.
- Created `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`.
- Created `docs/adapters/V5_CODEX_GOAL_RUNBOOK.md`.
- Created `docs/adapters/V5_ADAPTER_BOUNDARIES.md`.
- Completed final self-review against the S1 acceptance criteria and rubric.
- Completed final changed-file and protected-path verification.

## Final Verification

Commands run from repository root:

- `git status --short`
- `git ls-files --others --exclude-standard docs/adapters`
- `git diff --check`
- `git status --short -- Releases/ .claude/ PAI/ CLAUDE.md AGENTS.md .codex/ install.sh settings.json hooks/ skills/ agents/ commands/ subagents/ .github/ .agents/`

Results:

- `git status --short` lists exactly the five S1 files:
  - `docs/adapters/V5_ADAPTER_BOUNDARIES.md`
  - `docs/adapters/V5_CODEX_GOAL_RUNBOOK.md`
  - `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
  - `docs/adapters/V5_S1_EXEC_PLAN.md`
  - `docs/adapters/V5_UPSTREAM_RISK_REGISTER.md`
- `git ls-files --others --exclude-standard docs/adapters` lists the same five S1 files.
- `git diff --check` produced no output.
- Protected-path status produced no output.

## Self-Review Results

- Evidence discipline: pass. Major claims cite S0 or upstream v5 release evidence.
- Boundary discipline: pass. S1 docs remain design-only and do not authorize live PAI writes.
- State discipline: pass. Canonical PAI state is separated from product memory and goal metadata.
- Authority discipline: pass. `PAI_SYSTEM_PROMPT.md` authority equivalence is a blocking adapter lane.
- Pulse discipline: pass. Pulse remains central and parity requires an explicit event bridge.
- Existing-user safety: pass. The strategy does not require uninstalling Claude Code and forbids live install/migration trials during S1.
- Reversibility: pass. Rollback, fixture testing, and no-live-write gates are explicit.
- S2 readiness: pass. Future gates are named without authorizing implementation or advancing beyond S1.
- Scope hygiene: pass. Final verification names only the S1 approved write set and no protected paths.

## Iteration Log

- S1 created the initial safe strategy set.
- S1R repairs structure and expands missing required sections without changing the safety posture.
- S1R does not use `/goal`; the user explicitly forbade `/goal` for this repair.
- S1R keeps all edits inside the five approved existing files.

## Surprises & Discoveries

- The five S1 files were tracked and the worktree was clean at S1R start, so the requested `git diff --name-only` validation can be used directly.
- The S1 output was safe but compressed. The repair normalizes structure and adds missing scenario, readiness, memory, and boundary detail.
- The strategy requires a clear distinction between replacement-capable Codex beta design and official/full-support upstream status.

## Decision Log

- Preserve S0 as the evidence baseline.
- Treat Claude Code as the current official/full-support upstream engine for PAI v5.0.0.
- Treat Codex as a replacement-capable beta local engine candidate only behind a designed adapter.
- Define replacement as user-selectable local engine substitution, not overwriting Claude files and not turning PAI into an OpenAI project.
- Require future read-only trial, reversibility, and single-writer policy before any live state writes.
- Require native Codex surfaces rather than direct copying of Claude-shaped files.

## Outcomes & Retrospective

S1R normalizes the five S1 documents into a canonical architecture set while preserving the original S1 conclusions. The repaired set remains design-only and does not authorize implementation, runtime behavior, PAI Memory writes, Pulse implementation, Codex as drop-in today, Codex as official upstream engine, or direct copying of Claude files into Codex surfaces.

## Current Status

Complete.
