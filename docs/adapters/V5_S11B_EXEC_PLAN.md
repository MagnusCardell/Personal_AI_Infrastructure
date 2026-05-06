# V5-S11B Execution Plan

## Purpose

Execute V5-S11B Evidence Report Generator Negative Controls and Path Safety. S11B proves that the S11A evidence report generator is not a rubber stamp by adding negative controls for unsafe report paths, malformed fixture inputs, report-field invariants, and generator safety boundaries.

Codex is not currently proven drop-in for existing local PAI v5 files. S11B validates evidence-report generator safety only. It does not implement a Codex runtime adapter and does not approve live existing-local-v5 access or runtime adapter work.

## Scope

In scope:

- Create this S11B execution plan.
- Create a standard-library report-generator self-test.
- Update the fixture-trial README with S11B negative-control scope.
- Re-run the approved S11A report generator against the approved report path during validation.
- Run and record all required validation commands.

Out of scope:

- Runtime adapter implementation.
- Live read-only trials.
- Existing-local-v5 access.
- Private user-local reads.
- Pulse startup or calls.
- PAI Memory or ISA writes.
- Root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, runtime files, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures.

## Approved Write Set

Create exactly these new files:

- `docs/adapters/V5_S11B_EXEC_PLAN.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_report_generator.py`

Modify these existing files only if needed:

- `tests/adapters/v5-codex-readonly-fixture-trial/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/generate_readonly_fixture_trial_report.py`

The approved S11A report JSON may be overwritten only by re-running the approved generator command during validation. The final report content must remain valid and bounded to the approved report path.

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

Baseline discovery before S11B edits:

- `git status --short`: no output.
- `docs/adapters/V5_S11A_EXEC_PLAN.md` existed.
- `tests/adapters/v5-codex-readonly-fixture-trial/generate_readonly_fixture_trial_report.py` existed.
- `tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json` existed.
- Approved fixture root existed.
- Existing harness validation passed.
- Existing negative-control self-test passed.
- Existing no-residue self-test passed.
- Existing report generator command passed against the approved fixture root and approved report path.

## Completion Contract

The S11B Completion Contract is copied below in quoted form to preserve the required execution-plan H1/H2 sequence while retaining the contract text.

> ## Completion Contract
>
> This Completion Contract is the authoritative contract for V5-S11B.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S11B_EXEC_PLAN.md`.
>
> Do not mark S11B complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S11B deliverables must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * S11B validates evidence-report generator safety only.
> * S11B does not implement a Codex runtime adapter.
> * S11B does not create runtime adapter files.
> * S11B does not create root `AGENTS.md`.
> * S11B does not create `.codex/`.
> * S11B does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures.
> * S11A/S11B evidence output is adapter-test evidence only.
> * S11A/S11B evidence output is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a PAI runtime audit artifact, not a manifest, and not runtime payload.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Product memories must not be silently promoted into PAI Memory.
> * Pulse is central v5 infrastructure, but S11B does not start Pulse, call Pulse endpoints, or claim Pulse parity.
> * S11B proves only report-generator negative-control behavior, not Codex drop-in behavior.
> * S11B does not approve live existing-local-v5 access.
> * S11B does not approve runtime adapter work.
>
> ### Required local discovery commands
>
> Run before creating or modifying files:
>
> ```bash
> git status --short
>
> test -f docs/adapters/V5_S11A_EXEC_PLAN.md
> test -f tests/adapters/v5-codex-readonly-fixture-trial/generate_readonly_fixture_trial_report.py
> test -f tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json
> test -d tests/adapters/v5-codex-readonly-fixture-trial/fixtures
>
> python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py \
>   --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures
>
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py
>
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py
>
> python3 tests/adapters/v5-codex-readonly-fixture-trial/generate_readonly_fixture_trial_report.py \
>   --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures \
>   --report-out tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json
> ```
>
> ### Required file: `docs/adapters/V5_S11B_EXEC_PLAN.md`
>
> This file must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S11B Execution Plan
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
> ### Required generator self-test
>
> Create:
>
> ```text
> tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_report_generator.py
> ```
>
> The self-test must use only the Python standard library.
>
> It must set `sys.dont_write_bytecode = True`; import the report generator in-process; use temporary directories only for negative controls; leave no temporary artifacts in the repository; emit stdout only; exit `0` when all positive and negative controls behave correctly; and exit non-zero on failure.
>
> It must not use subprocesses; use network access; read release files; read user-local state; read `~/.claude`; read `~/.codex`; invoke Claude Code; invoke Codex; start Pulse; call Pulse endpoints; probe `localhost:31337`; or write inside the repository outside the approved report file during positive validation.
>
> The self-test must include these negative controls:
>
> ```text
> RG-001 absolute report path rejected
> RG-002 parent traversal report path rejected
> RG-003 output outside reports directory rejected
> RG-004 unexpected report filename rejected
> RG-005 missing fixture root rejected
> RG-006 fixture root with missing case file rejected
> RG-007 fixture root with malformed fixture metadata rejected
> RG-008 fixture root with malformed case data rejected
> RG-009 report missing required field rejected or impossible by construction
> RG-010 report with wrong status rejected or impossible by construction
> RG-011 report with drop-in claim rejected or impossible by construction
> RG-012 non-canonical output statement omission rejected or impossible by construction
> RG-013 live user-local source reference rejected
> RG-014 Pulse endpoint-call authorization rejected
> RG-015 PAI Memory or ISA write authorization rejected
> RG-016 product-memory promotion authorization rejected
> ```
>
> The self-test report must include:
>
> ```text
> S11B report-generator negative-control self-test report
> positive_control_status
> negative_control_count
> status
> ```
>
> The `negative_control_count` must be `16`.
>
> ### Required README update
>
> Update:
>
> ```text
> tests/adapters/v5-codex-readonly-fixture-trial/README.md
> ```
>
> Add an S11B section explaining that S11B adds report-generator negative controls; negative controls use temporary data only; S11B does not create committed negative fixtures; does not run Codex; does not run Claude Code; does not start Pulse; does not call Pulse endpoints; does not inspect live user-local state; does not write PAI Memory or ISA; S11B evidence reports are not PAI Memory, ISA, Pulse state, Claude memory, Codex memory, runtime audit artifacts, manifests, or runtime payload; and Codex is not currently proven drop-in for existing local PAI v5 files.
>
> ### Hard failure conditions
>
> S11B fails immediately if any file outside the approved write set is created or modified; fixture directories, fixture READMEs, fixture metadata, or fixture case data are modified; any protected file is modified; more than the approved S11A report file is created under `reports/`; runtime adapter files are created; root `AGENTS.md` or `.codex/` is created or modified; a manifest instance, executable schema, PAI runtime audit artifact, live-trial artifact, runtime payload, or committed negative fixture is created; a live read-only trial is run; private user-local state is inspected or modified; live existing-local-v5 state is read; PAI Memory is written; ISA is written; Pulse is started or called; `localhost:31337` is probed; Claude Code or Codex runtime is invoked; the generator or self-test imports non-stdlib dependencies, runs subprocesses, or uses network access; the generator writes outside the approved report path; any deliverable claims Codex is drop-in today or the official upstream engine; or any deliverable authorizes PAI Memory writes, ISA writes, Pulse startup/calls, live existing-local-v5 trial execution, product-memory promotion, or dual-engine uncoordinated writes.
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
> python3 tests/adapters/v5-codex-readonly-fixture-trial/generate_readonly_fixture_trial_report.py \
>   --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures \
>   --report-out tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json
>
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_report_generator.py
> ```
>
> Also run changed-file check, execution-plan heading check, generator self-test source check, protected-path check, and residue check exactly as specified by the S11B card.
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
> Do not begin S11C.

## Milestones

1. Baseline status check.
2. S11A generator and report reread.
3. Existing harness and self-test validation.
4. Report-generator negative-control self-test implementation.
5. README update.
6. Positive and negative validation execution.
7. Protected-path and no-extra-file validation.
8. Self-review and repair.
9. Final handoff and goal-state report.

## Self-Review Rubric

| Area | Points |
| --- | ---: |
| Scope and protected-path discipline | 15 |
| Evidence discipline | 10 |
| Report-generator positive control quality | 15 |
| Negative-control coverage quality | 30 |
| Path safety and temporary-data cleanup | 15 |
| No-live-state, no-Pulse, Memory, ISA, and runtime-invocation safety | 10 |
| Verification quality | 5 |
| Total | 100 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

S11B fails immediately if any file outside the approved write set is created or modified; fixture directories, fixture READMEs, fixture metadata, or fixture case data are modified; any protected file is modified; more than the approved S11A report file is created under `reports/`; runtime adapter files are created; root `AGENTS.md` or `.codex/` is created or modified; a manifest instance, executable schema, PAI runtime audit artifact, live-trial artifact, runtime payload, or committed negative fixture is created; a live read-only trial is run; private user-local state or live existing-local-v5 state is read; PAI Memory or ISA is written; Pulse is started or called; `localhost:31337` is probed; Claude Code or Codex runtime is invoked; the generator or self-test imports non-stdlib dependencies, runs subprocesses, or uses network access; the generator writes outside the approved report path; any deliverable claims Codex is drop-in today or official upstream engine; or any deliverable authorizes PAI Memory writes, ISA writes, Pulse startup/calls, live existing-local-v5 trial execution, product-memory promotion, or dual-engine uncoordinated writes.

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

python3 tests/adapters/v5-codex-readonly-fixture-trial/generate_readonly_fixture_trial_report.py \
  --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures \
  --report-out tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json

PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_report_generator.py
```

Additional required checks:

- Changed-file check.
- Execution-plan heading check.
- Generator self-test source check.
- Generated-artifact residue check.
- Protected-path check.

## Progress

- Baseline status check: complete; `git status --short` produced no output before edits.
- S11A generator and report existence checks: complete.
- Existing harness validation: complete; passed.
- Existing negative-control self-test validation: complete; passed.
- Existing no-residue self-test validation: complete; passed.
- Existing report generator validation: complete; passed.
- S11B execution plan creation: complete.
- Report-generator self-test implementation: complete; `RG-001` through `RG-016` are covered.
- README update: complete.
- Generator hardening: complete; the generator now runs approved fixture harness validation before building report content.
- Final validation execution: complete; all required commands and checks passed.
- Final handoff and goal-state report: pending.

## Iteration Log

Iteration 1 target score before implementation: 94/100 minimum, hard failures 0. Baseline scope is feasible without modifying fixtures, protected paths, runtime files, Codex surfaces, Pulse surfaces, PAI Memory, ISA, release files, or private user-local state.

Iteration 1 scored self-review after validation:

| Area | Points | Score |
| --- | ---: | ---: |
| Scope and protected-path discipline | 15 | 15 |
| Evidence discipline | 10 | 10 |
| Report-generator positive control quality | 15 | 15 |
| Negative-control coverage quality | 30 | 30 |
| Path safety and temporary-data cleanup | 15 | 15 |
| No-live-state, no-Pulse, Memory, ISA, and runtime-invocation safety | 10 | 10 |
| Verification quality | 5 | 5 |
| Total | 100 | 100 |

Result: `100/100`, hard failures `0`.

## Surprises & Discoveries

No scope blocker was found during baseline discovery. The S11A generator already rejects unsafe output paths by exact approved-path matching, and the existing harness rejects malformed temporary fixture corpora when called in-process by the generator.

One generator ordering issue was hardened inside the approved S11B write set: report generation now invokes the approved fixture harness validation before extracting report counts or version fields, so malformed temporary fixture roots fail through the intended validation boundary.

## Decision Log

- S11B-D01: Keep S11B limited to report-generator safety and negative controls.
- S11B-D02: Use temporary directories for malformed fixture-input controls and avoid committed negative fixtures.
- S11B-D03: Preserve S11A report output as adapter-test evidence only, not PAI Memory, ISA, Pulse state, Claude memory, Codex memory, a PAI runtime audit artifact, a manifest, or runtime payload.
- S11B-D04: Do not modify fixtures or existing harness/self-test files unless a validation defect requires it.
- S11B-D05: Preserve no Codex runtime, no Claude Code, no Pulse startup/calls, no live user-local reads, no PAI Memory writes, no ISA writes, and no product-memory promotion.

## Outcomes & Retrospective

Validation results:

- `git status --short`: passed; changed files were limited to the S11B execution plan, fixture-trial README, report generator, and report-generator self-test.
- `git diff --name-only | sort`: passed; output stayed within the approved S11B write set.
- `git diff --check`: passed with no output.
- Positive fixture harness command: passed with `fixture_count: 12`, `case_count: 12`, `coverage_id_count: 25`, `gate_id_count: 20`, `denied_category_count: 13`, and `status: pass`.
- Existing negative-control self-test: passed with `negative_control_count: 60` and `status: pass`.
- Existing no-residue self-test: passed with stable fixture digest, stable stdout shape, and `status: pass`.
- S11A report generator command: passed and wrote only the approved S11A report path.
- S11B report-generator self-test: passed with `positive_control_status: pass`, `negative_control_count: 16`, and `status: pass`.
- Changed-file check: passed.
- Execution-plan heading check: passed.
- Generator self-test source check: passed.
- Generated-artifact residue check: passed.
- Protected-path check: passed with no output.

S11B remains adapter-test implementation only. It proves report-generator negative-control behavior and path safety for the approved fixture evidence flow; it does not prove Codex drop-in behavior, approve live existing-local-v5 access, or authorize runtime adapter work.
