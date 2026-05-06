# V5-S11D Execution Plan

## Purpose

Execute V5-S11D S11 Closeout and S12 Proposed Contract. S11D closes the S11 release-fixture read-only evidence track and proposes the next S12-level contract for architect review.

Codex is not currently proven drop-in for existing local PAI v5 files. S11D is documentation/design only; it does not authorize S12, live trials, existing-local-v5 access, or runtime adapter implementation.

## Scope

In scope:

- Create this S11D execution plan.
- Create the S11 evidence closeout report.
- Create proposed S12 live read-only trial readiness gates.
- Create a proposed S12 write set and completion contract.
- Create the S11-to-S12 decision log.
- Run and record all required validation commands.

Out of scope:

- S12 authorization or execution.
- Live trials or existing-local-v5 access.
- Runtime adapter implementation.
- Test fixture, harness, generator, evaluator, report, or README edits.
- Root `AGENTS.md`, `.codex/`, Pulse startup/calls, PAI Memory writes, ISA writes, product-memory promotion, manifests, schemas, runtime payloads, or audit artifacts.

## Approved Write Set

Create exactly these files:

- `docs/adapters/V5_S11D_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_S11_EVIDENCE_CLOSEOUT_REPORT.md`
- `docs/adapters/V5_CODEX_S12_LIVE_READ_ONLY_TRIAL_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_S12_PROPOSED_WRITE_SET_AND_COMPLETION_CONTRACT.md`
- `docs/adapters/V5_CODEX_S11_TO_S12_DECISION_LOG.md`

No other files may be created or modified.

## Protected Paths

Do not modify:

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

Do not inspect or modify private user-local state:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`

## Source Protocol

Allowed reads:

- `docs/adapters/V5_*.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/`
- `Releases/v5.0.0/`
- `Releases/v5.0.0/.claude/`

Forbidden reads and operations:

- Live `~/.claude/PAI`, live `~/.codex`, `~/.claude/projects`, or other private user-local state.
- Live existing-local-v5 state.
- Pulse startup, Pulse endpoint calls, or `localhost:31337` probes.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, and Codex hook/rule/execpolicy commands.

## Source Material

Baseline discovery before S11D edits:

- `git status --short`: no output.
- S11C execution plan, S11A evidence report, S11B report-generator controls, and S11C readiness report existed.
- S10-to-S11 decision log and S11 readiness gates were read from repository-local docs.
- S11 evidence report status showed pass.
- S11C readiness report showed `gate_count: 18`, `R0: requires-architect-approval`, and `s12_approval_status: not-approved`.

## Completion Contract

The S11D Completion Contract is copied below in quoted form to preserve the required execution-plan H1/H2 sequence while retaining the contract text.

> ## Completion Contract
>
> This Completion Contract is the authoritative contract for V5-S11D.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S11D_EXEC_PLAN.md`.
>
> Do not mark S11D complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> S11D must preserve:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * S11D closes the S11 release-fixture evidence track only.
> * S11D does not authorize S12.
> * S11D does not run live trials.
> * S11D does not read existing-local-v5 state.
> * S11D does not create runtime adapter files.
> * S11D does not create root `AGENTS.md` or `.codex/`.
> * S12 may be proposed only as a future architect-approved milestone.
> * Future S12 must remain read-only unless separately approved.
> * Future S12 must not write PAI Memory or ISA.
> * Future S12 must not start Pulse or call Pulse endpoints unless explicitly approved by a future card.
> * Future S12 must not require uninstalling Claude Code.
> * Product memories must not be silently promoted into PAI Memory.
> * S12 must not claim Codex is drop-in.
> * S12 must not claim Codex is the official upstream engine.
>
> ### Required file: `docs/adapters/V5_S11D_EXEC_PLAN.md`
>
> This file must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S11D Execution Plan
> ## Purpose
> ## Scope
> ## Approved Write Set
> ## Protected Paths
> ## Source Protocol
> ## Source Material
> ## Completion Contract
> ## Milestones
> ## Self-Review Rubric
> ## Hard Failure Conditions
> ## Validation Commands
> ## Progress
> ## Iteration Log
> ## Surprises & Discoveries
> ## Decision Log
> ## Outcomes & Retrospective
> ```
>
> The `## Completion Contract` section must contain a verbatim copy of this Completion Contract.
>
> The execution plan must record at least one scored self-review iteration with score at least `94/100` and zero hard failures.
>
> ### Required file: `docs/adapters/V5_CODEX_S11_EVIDENCE_CLOSEOUT_REPORT.md`
>
> Must contain exactly the required closeout report headings and summarize S11A, S11B, and S11C. It must state whether the release-fixture evidence track is ready for architect review; that no live trial has been run; that no runtime adapter has been implemented; that Codex is not drop-in today; and that release-fixture evidence is necessary but insufficient for drop-in claims.
>
> ### Required file: `docs/adapters/V5_CODEX_S12_LIVE_READ_ONLY_TRIAL_READINESS_GATES.md`
>
> Must contain exactly the required S12 gate headings. Each gate must include `Required proof`, `Failure signal`, `S11D status`, and `Future S12 implication`. S11D must not mark live-read gates as passed. `L0` must require architect approval. `L3` through `L6` must remain future-only. S12 entry threshold must require explicit architect approval and explicit user consent design.
>
> ### Required file: `docs/adapters/V5_CODEX_S12_PROPOSED_WRITE_SET_AND_COMPLETION_CONTRACT.md`
>
> Must contain exactly the required proposed contract headings. It must state S12 is proposed only and not approved by S11D; proposed S12 must be read-only; must not read live user-local state by default; must require explicit user consent design before any live local read; must not write PAI Memory or ISA; must not start or call Pulse unless separately approved; must not create root `AGENTS.md` or `.codex/`; and must not claim drop-in status. It must include a proposed write-set table and acceptance IDs `S12-AC-001` through `S12-AC-024`.
>
> ### Required file: `docs/adapters/V5_CODEX_S11_TO_S12_DECISION_LOG.md`
>
> Must contain exactly the required decision-log headings and decisions `S11D-D01` through `S11D-D18`.
>
> ### Hard failure conditions
>
> S11D fails if any file outside the approved write set is created or modified; any test fixture, harness, generator, evaluator, report, or README file changes; any protected path changes; runtime adapter files are created; root `AGENTS.md` or `.codex/` is created or modified; live user-local state is read; Pulse is started or called; PAI Memory or ISA is written; Claude Code or Codex runtime is invoked; S12 is authorized rather than proposed; any deliverable claims Codex is drop-in today or official upstream engine; or any deliverable authorizes live trials, runtime adapter work, PAI Memory writes, ISA writes, Pulse startup/calls, existing-local-v5 access, product-memory promotion, or dual-engine uncoordinated writes.
>
> ### Required validation commands
>
> Run:
>
> ```bash
> git status --short
> git diff --name-only | sort
> git diff --check
>
> python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py \
>   --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures
>
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py
>
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py
>
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_report_generator.py
>
> python3 tests/adapters/v5-codex-readonly-fixture-trial/generate_readonly_fixture_trial_report.py \
>   --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures \
>   --report-out tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json
>
> python3 tests/adapters/v5-codex-readonly-fixture-trial/evaluate_readiness_gates.py \
>   --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures \
>   --evidence-report tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json \
>   --report-out tests/adapters/v5-codex-readonly-fixture-trial/reports/S11C_READINESS_GATE_EVALUATION.json
> ```
>
> Run changed-file check, heading check, content checks, and protected-path check exactly as specified by the S11D card.
>
> ### Final handoff format
>
> End with exactly:
>
> ```markdown
> ## Files changed
>
> ## Behavior changed
>
> ## Tests run
>
> ## Known risks
>
> ## Protected files changed
>
> ## Goal state
>
> ## Recommended next architect decision
> ```
>
> Do not begin S12.

## Milestones

1. Baseline status check.
2. S10 closeout and S11A/S11B/S11C reread.
3. S11 evidence closeout report creation.
4. S12 readiness gate proposal creation.
5. S12 proposed write set and completion contract creation.
6. S11-to-S12 decision log creation.
7. Validation execution.
8. Protected-path and no-extra-file validation.
9. Self-review and repair.
10. Final handoff and goal-state report.

## Self-Review Rubric

| Area | Points |
| --- | ---: |
| Scope and protected-path discipline | 15 |
| Evidence discipline | 15 |
| S11 closeout quality | 20 |
| S12 proposed gate quality | 20 |
| S12 proposed contract quality | 15 |
| Decision log quality | 10 |
| Verification quality | 5 |
| Total | 100 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

S11D fails if any file outside the approved write set is created or modified; any test fixture, harness, generator, evaluator, report, or README file changes; any protected path changes; runtime adapter files are created; root `AGENTS.md` or `.codex/` is created or modified; live user-local state or existing-local-v5 state is read; Pulse is started or called; PAI Memory or ISA is written; Claude Code or Codex runtime is invoked; S12 is authorized rather than proposed; any deliverable claims Codex is drop-in today or official upstream engine; or any deliverable authorizes live trials, runtime adapter work, PAI Memory writes, ISA writes, Pulse startup/calls, existing-local-v5 access, product-memory promotion, or dual-engine uncoordinated writes.

## Validation Commands

Required commands:

```bash
git status --short
git diff --name-only | sort
git diff --check

python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py \
  --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures

PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py

PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py

PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_report_generator.py

python3 tests/adapters/v5-codex-readonly-fixture-trial/generate_readonly_fixture_trial_report.py \
  --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures \
  --report-out tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json

python3 tests/adapters/v5-codex-readonly-fixture-trial/evaluate_readiness_gates.py \
  --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures \
  --evidence-report tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json \
  --report-out tests/adapters/v5-codex-readonly-fixture-trial/reports/S11C_READINESS_GATE_EVALUATION.json
```

Additional required checks:

- Changed-file check.
- Heading check.
- Content checks.
- Protected-path check.

## Progress

- Baseline status check: complete; `git status --short` produced no output before edits.
- S10 closeout and S11A/S11B/S11C reread: complete.
- S11 evidence closeout report creation: complete.
- S12 readiness gate proposal creation: complete.
- S12 proposed write set and completion contract creation: complete.
- S11-to-S12 decision log creation: complete.
- Validation execution: complete; all required commands and checks passed.
- Final handoff and goal-state report: pending.

## Iteration Log

Iteration 1 target score before implementation: 94/100 minimum, hard failures 0. Baseline scope is feasible with documentation-only changes and without modifying tests, fixtures, harnesses, generators, evaluators, reports, READMEs, protected paths, runtime files, Pulse, PAI Memory, ISA, or private user-local state.

Iteration 1 scored self-review after validation:

| Area | Points | Score |
| --- | ---: | ---: |
| Scope and protected-path discipline | 15 | 15 |
| Evidence discipline | 15 | 15 |
| S11 closeout quality | 20 | 20 |
| S12 proposed gate quality | 20 | 20 |
| S12 proposed contract quality | 15 | 15 |
| Decision log quality | 10 | 10 |
| Verification quality | 5 | 5 |
| Total | 100 | 100 |

Result: `100/100`, hard failures `0`.

## Surprises & Discoveries

No scope blocker was found during baseline discovery. S11C already records `R0` as requiring architect approval and `s12_approval_status` as `not-approved`, which directly supports S11D closeout without creating new evidence artifacts.

## Decision Log

- S11D-D01: Keep S11D documentation/design only.
- S11D-D02: Close the S11 release-fixture evidence track pending architect review.
- S11D-D03: Propose S12 only; do not approve it.
- S11D-D04: Preserve read-only, no default live user-local access, explicit user consent design, no Pulse, no PAI Memory writes, no ISA writes, no product-memory promotion, and no drop-in claim as S12 constraints.

## Outcomes & Retrospective

Validation results:

- `git status --short`: passed; changed files were limited to the five approved S11D documents.
- `git diff --name-only | sort`: passed; output stayed within the approved S11D write set.
- `git diff --check`: passed with no output.
- Positive fixture harness command: passed with `fixture_count: 12`, `case_count: 12`, `coverage_id_count: 25`, `gate_id_count: 20`, `denied_category_count: 13`, and `status: pass`.
- Existing negative-control self-test: passed with `negative_control_count: 60` and `status: pass`.
- Existing no-residue self-test: passed with stable fixture digest, stable stdout shape, and `status: pass`.
- S11B report-generator negative-control self-test: passed with `negative_control_count: 16` and `status: pass`.
- S11A report generator command: passed and produced no final report diff.
- S11C readiness evaluator command: passed and produced no final report diff.
- Changed-file check: passed.
- Heading check: passed.
- Content checks: passed.
- Protected-path check: passed with no output.

S11D remains documentation/design only. It closes S11 pending architect review, proposes S12 only, does not authorize S12, does not run live trials, does not read existing-local-v5 state, does not implement runtime adapter work, does not start or call Pulse, does not write PAI Memory or ISA, and does not claim Codex is drop-in today.
