# V5-S4 Execution Plan

## Purpose

Design the non-runtime artifacts required before any future read-only Codex trial can be run against PAI v5 fixture material or existing local PAI v5 files.

S4 is a design milestone only. It does not run a read-only trial, create fixtures, implement a Codex adapter, create root `AGENTS.md`, create `.codex/`, create hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, runtime files, or test harnesses.

## Scope

S4 is limited to designing:

- A read-only trial manifest specification.
- A fixture and path model specification.
- An authority-equivalence test specification.
- A trial audit output specification.

S4 may use S0/S1/S2/S3 adapter docs, read-only PAI v5 release evidence, and official OpenAI Codex documentation only if new Codex capability claims are needed.

S4 does not create the manifest instance, fixture material, tests, runtime config, harness, adapter, installer, launcher, wrapper, Codex project files, or trial output.

## Approved Write Set

Only these files may be created or modified during S4:

- `docs/adapters/V5_S4_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_MANIFEST_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_FIXTURE_AND_PATH_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_EQUIVALENCE_TEST_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_OUTPUT_SPEC.md`

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

PAI and prior adapter evidence:

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
- `docs/adapters/V5_S3_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`

Read-only PAI v5 release evidence may be used only for targeted facts already relevant to S4.

Official OpenAI Codex documentation may be used only if S4 needs a new current Codex capability claim not already captured in S2/S3.

## Required Outputs

S4 must create:

- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_MANIFEST_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_FIXTURE_AND_PATH_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_EQUIVALENCE_TEST_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_OUTPUT_SPEC.md`

The docs must be design-only. They must describe future artifact contracts without creating those artifacts.

## Design Questions

S4 must answer:

- What fields must a future read-only trial manifest contain?
- How should fixture material, sanitized fixture material, and existing local v5 roots be classified?
- What paths must be readable, denied, or write-denied before any future trial?
- What authority-equivalence cases must be evaluated before a future trial?
- What should future trial audit output contain?
- How should a future audit prove no writes, no denied reads, no Pulse startup, no installer execution, no migration tooling, and no state promotion?
- What stops a future trial before execution?
- What artifacts are explicitly not created in S4?

## Milestones

1. Create this execution plan first.
2. Read S0/S1/S2/S3 evidence needed for S4.
3. Draft the read-only trial manifest spec.
4. Draft the fixture and path model spec.
5. Draft the authority-equivalence test spec.
6. Draft the trial audit output spec.
7. Self-review all S4 specs against the approved write set and non-runtime boundary.
8. Run validation commands.
9. Update this plan with progress, validation, decisions, and retrospective.

## Self-Review Rubric

S4 passes only if:

- Exactly the five approved S4 files are created or modified.
- No protected path is modified.
- No read-only trial is run.
- No fixture material is created.
- No runtime adapter file is created.
- No root `AGENTS.md` is created.
- No `.codex/` directory or config is created.
- No hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, runtime files, test harnesses, or migration scripts are created.
- No release file is modified.
- No private user-local state is inspected or modified.
- Pulse is not started.
- Installers are not run.
- Codex import or migration tooling is not run.
- Codex-native claims are limited to S2/S3 evidence unless official OpenAI Codex documentation is cited.
- PAI facts cite S0/S1/S2/S3 evidence or read-only release evidence.
- The docs preserve the S1/S2/S3 conclusion that Codex is not currently proven drop-in for existing local PAI v5 files.
- The docs do not claim Codex is the official upstream PAI engine.
- The docs do not imply Claude-shaped files can be copied directly into Codex-native surfaces.
- The docs do not authorize PAI Memory, ISA, Pulse, settings, hook, installer, fixture, or trial writes.

## Hard Failure Conditions

Stop and report a blocker if S4 requires:

- Running a read-only trial.
- Creating fixtures.
- Implementing a Codex adapter.
- Creating runtime adapter surfaces.
- Creating root `AGENTS.md`.
- Creating `.codex/`.
- Creating hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, runtime files, test harnesses, or migration scripts.
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
    "docs/adapters/V5_CODEX_AUTHORITY_EQUIVALENCE_TEST_SPEC.md",
    "docs/adapters/V5_CODEX_READ_ONLY_TRIAL_MANIFEST_SPEC.md",
    "docs/adapters/V5_CODEX_TRIAL_AUDIT_OUTPUT_SPEC.md",
    "docs/adapters/V5_CODEX_TRIAL_FIXTURE_AND_PATH_MODEL_SPEC.md",
    "docs/adapters/V5_S4_EXEC_PLAN.md",
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

- Started the bounded S4 goal.
- Confirmed the repository was clean before S4 edits.
- Created this execution plan as the first S4 file and living self-evaluation contract.
- Read S1/S2/S3 adapter evidence needed for S4.
- Determined no new Codex capability claims were needed beyond S2/S3, so no new OpenAI documentation lookup was required.
- Created `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_MANIFEST_SPEC.md`.
- Created `docs/adapters/V5_CODEX_TRIAL_FIXTURE_AND_PATH_MODEL_SPEC.md`.
- Created `docs/adapters/V5_CODEX_AUTHORITY_EQUIVALENCE_TEST_SPEC.md`.
- Created `docs/adapters/V5_CODEX_TRIAL_AUDIT_OUTPUT_SPEC.md`.
- Marked the five approved S4 docs as intent-to-add so `git diff --name-only` validates the approved write set.
- Ran S4 validation commands and confirmed only the five approved S4 files are changed.

## Decision Log

- Treat S0/S1/S2/S3 adapter docs as the main evidence base.
- Avoid new OpenAI documentation lookup unless a new current Codex capability claim is needed.
- Keep S4 as artifact contract design only, not artifact creation or trial execution.
- Preserve the read-only-first, adapter-first, reversible posture from S1 through S3.
- Treat manifest, fixture/path, authority-equivalence, and audit output as future contract specs, not runtime files.
- Keep fixture creation, schema implementation, hash inventory, trial execution, audit artifact writing, and harness work blocked for later architect-approved milestones.
- Require future manifests to deny by default, make write-deny dominate all read roots, and keep generated audit output outside live PAI, Claude, Codex, release, and runtime roots.

## Outcomes & Retrospective

Created the S4 manifest, fixture/path model, authority-equivalence test, and audit output specs as design-only documentation.

Validation results:

- `git status --short` listed only the five approved S4 docs as intent-to-add files.
- `git diff --name-only | sort` listed exactly the five approved S4 docs.
- `git diff --check` passed.
- The explicit changed-file Python check printed `changed files ok`.
- Protected-path status produced no output.

S4 did not run a read-only trial, create fixtures, implement a Codex adapter, create root `AGENTS.md`, create `.codex/`, create hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, runtime files, test harnesses, or migration scripts. S4 did not modify release files, inspect private user-local state, start Pulse, run installers, run Codex import or migration tooling, authorize PAI Memory writes, authorize ISA writes, authorize Pulse writes, claim Codex is drop-in today, or advance beyond S4.
