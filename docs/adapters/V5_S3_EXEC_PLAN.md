# V5-S3 Execution Plan

## Purpose

Design the non-runtime authority-mapping and read-only trial posture required before Codex can safely be tested against existing local PAI v5 files.

S3 is a design milestone only. It does not implement a Codex adapter, create runtime adapter files, create root `AGENTS.md`, create `.codex/`, modify release files, inspect private user-local state, start Pulse, run installers, or run Codex import or migration tooling.

## Scope

S3 is limited to:

- Defining how PAI v5 authority layers should be mapped into future Codex-native authority surfaces.
- Defining a future read-only trial posture for existing local PAI v5 files.
- Using S0/S1/S2 adapter docs, read-only PAI v5 release evidence, and official OpenAI Codex documentation only.
- Creating design docs under `docs/adapters/`.

S3 may not create runtime surfaces, root `AGENTS.md`, `.codex/`, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixture harnesses, tests, generated config, or migration scripts.

## Approved Write Set

Only these files may be created or modified during S3:

- `docs/adapters/V5_S3_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`

## Protected Paths

Protected repository paths:

- `Releases/`
- `Releases/v5.0.0/`
- `Releases/v5.0.0/.claude/`
- `.claude/`
- `PAI/`
- `CLAUDE.md`
- `AGENTS.md`
- `.codex/`
- `install.sh`
- `PAI_SYSTEM_PROMPT.md`
- `settings.json`
- `hooks/`
- `skills/`
- `subagents/`
- `agents/`
- `commands/`
- `.github/`
- `.agents/`

Protected user-local paths:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`

## Source Material

PAI evidence sources:

- `docs/adapters/V5_S0_DISCOVERY_PLAN.md`
- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- `docs/adapters/V5_S1_EXEC_PLAN.md`
- `docs/adapters/V5_UPSTREAM_RISK_REGISTER.md`
- `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
- `docs/adapters/V5_CODEX_GOAL_RUNBOOK.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`
- `docs/adapters/V5_S2_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- Read-only release evidence under `Releases/v5.0.0/` when needed.

Codex evidence sources:

- Official OpenAI Codex documentation only.

The OpenAI developer-docs MCP tooling is not available in this session, and installing it would modify Codex configuration. Because `.codex/` and user-local Codex state are protected for S3, official OpenAI web documentation is the approved fallback source for current Codex-native facts.

## Required Outputs

S3 must create:

- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`

The authority mapping spec must define the future authority stack, Codex-native target surfaces, prohibited direct copies, conflict handling, doctrine boundaries, and readiness gates.

The read-only trial spec must define a future trial posture for existing local PAI v5 files that prevents writes, avoids private-state inspection during S3, preserves Claude Code fallback, labels state provenance, and blocks promotion into live write modes until later architect approval.

## Design Questions

S3 must answer:

- What are the current PAI v5 authority layers?
- Which Codex-native authority surfaces are documented by OpenAI?
- How should `PAI_SYSTEM_PROMPT.md` be treated in a future Codex design?
- What must a future Codex `AGENTS.md` do if later authorized?
- What must never be copied directly from Claude-shaped surfaces into Codex?
- How should authority conflicts be evaluated without creating runtime files?
- What are the phases of a read-only trial against existing local PAI v5 files?
- What filesystem and state boundaries must prevent accidental live writes?
- How should PAI Memory, ISA, Pulse state, Codex memory, Codex goal state, and transcripts be labeled?
- What evidence must exist before a future milestone can test against existing local v5 files?

## Milestones

1. Create this execution plan first.
2. Collect S0/S1/S2 adapter evidence and targeted read-only release evidence.
3. Collect official OpenAI Codex documentation evidence for authority and read-only trial controls.
4. Draft `V5_CODEX_AUTHORITY_MAPPING_SPEC.md`.
5. Draft `V5_CODEX_READ_ONLY_TRIAL_SPEC.md`.
6. Self-review both specs against S3 boundaries.
7. Run validation commands.
8. Update this plan with final progress, validation, decisions, and retrospective.

## Self-Review Rubric

S3 passes only if:

- Exactly the three approved S3 files are created or modified.
- No protected path is modified.
- No runtime adapter file is created.
- No root `AGENTS.md` is created.
- No `.codex/` directory or config is created.
- No hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixture harnesses, tests, or migration scripts are created.
- No release file is modified.
- No private user-local state is inspected or modified.
- Pulse is not started.
- Installers are not run.
- Codex import or migration tooling is not run.
- Codex-native facts cite official OpenAI Codex documentation.
- PAI facts cite S0/S1/S2 evidence or read-only release evidence.
- The docs preserve the S1/S2 conclusion that Codex is not currently proven drop-in for existing local PAI v5 files.
- The docs do not claim Codex is the official upstream PAI engine.
- The docs do not imply Claude-shaped files can be copied directly into Codex-native surfaces.
- The docs do not authorize PAI Memory, ISA, Pulse, settings, hook, or installer writes.

## Hard Failure Conditions

Stop and report a blocker if S3 requires:

- Implementing a Codex adapter.
- Creating runtime adapter surfaces.
- Creating root `AGENTS.md`.
- Creating `.codex/`.
- Creating hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixture harnesses, tests, generated config, or migration scripts.
- Modifying protected paths.
- Inspecting private user-local state.
- Starting Pulse.
- Running installers.
- Running Codex import or migration tooling.
- Claiming Codex drop-in compatibility.
- Claiming Codex is the official upstream PAI engine.
- Claiming undocumented Codex behavior as fact.

## Validation Commands

Run from repository root:

```bash
git status --short
git diff --name-only | sort
git diff --check
git status --short -- Releases/ .claude/ PAI/ CLAUDE.md AGENTS.md .codex/ install.sh settings.json hooks/ skills/ subagents/ agents/ commands/ .github/ .agents/
```

Run this changed-file check:

```bash
python3 - <<'PY'
import subprocess

expected = [
    "docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md",
    "docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md",
    "docs/adapters/V5_S3_EXEC_PLAN.md",
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

## Progress

- Started the bounded S3 goal.
- Confirmed the repository was clean before S3 edits.
- Created this execution plan as the first S3 file and living self-evaluation contract.
- Collected S0/S1/S2 adapter evidence.
- Collected targeted read-only release evidence for the PAI instruction hierarchy, `PAI_SYSTEM_PROMPT.md`, `CLAUDE.md`, `PAI_DIR`, and settings boundaries.
- Collected official OpenAI Codex documentation evidence for `AGENTS.md`, config precedence, sandbox modes, approval policy, non-interactive read-only behavior, hooks, memories, and CLI behavior.
- Created `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`.
- Created `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`.
- Marked the three approved S3 docs as intent-to-add so `git diff --name-only` validates the approved write set.
- Ran S3 validation commands and confirmed only the three approved S3 files are changed.

## Decision Log

- Use official OpenAI web documentation for Codex-native facts because installing the OpenAI docs MCP would modify protected Codex configuration.
- Treat S0/S1/S2 adapter docs as the main PAI evidence baseline.
- Use read-only release evidence only for targeted authority and trial facts.
- Keep S3 design-only and non-runtime.
- Treat a future Codex `AGENTS.md`, if later authorized, as a compact router rather than a clone of `CLAUDE.md` or `PAI_SYSTEM_PROMPT.md`.
- Treat Codex hooks as possible dynamic context or guardrail surfaces, not a complete enforcement boundary and not constitutional authority.
- Treat Codex memories, transcripts, plans, SDK threads, and `/goal` state as product/session state, not PAI Memory, ISA, or Pulse state.
- Require explicit manifest, consent, read-only enforcement, denied-path handling, no Pulse startup, no installer calls, and no migration tooling before any future existing-local-v5 read-only trial.

## Outcomes & Retrospective

Created the S3 authority mapping and read-only trial specs as design-only documentation.

Validation results:

- `git status --short` listed only the three approved S3 docs as intent-to-add files.
- `git diff --name-only | sort` listed exactly the three approved S3 docs.
- `git diff --check` passed.
- The explicit changed-file Python check printed `changed files ok`.
- Protected-path status produced no output.

S3 did not implement a Codex adapter, create root `AGENTS.md`, create `.codex/`, create hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixture harnesses, tests, generated config, or runtime files. S3 did not modify release files, inspect private user-local state, start Pulse, run installers, run Codex import or migration tooling, authorize PAI Memory writes, authorize ISA writes, authorize Pulse writes, claim Codex is drop-in today, or advance beyond S3.
