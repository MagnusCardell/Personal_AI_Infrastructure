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

## Current Status

Complete.
