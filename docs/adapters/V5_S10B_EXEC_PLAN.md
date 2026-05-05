# V5-S10B Execution Plan

## Purpose

Validate the S10A read-only fixture harness with negative controls and regression self-tests that prove unsafe or malformed fixture metadata is rejected.

S10B is adapter-test implementation only. It does not implement a Codex runtime adapter, does not create runtime adapter files, and does not create committed negative fixtures.

## Scope

S10B is limited to this execution plan, a README update for the S10A fixture harness directory, and one new self-test script that generates invalid fixture corpora only in temporary directories.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement remains plausible only through a designed adapter.

## Approved Write Set

Create exactly:

- `docs/adapters/V5_S10B_EXEC_PLAN.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`

Modify exactly:

- `tests/adapters/v5-codex-readonly-fixture-trial/README.md`

Optional only if required:

- `tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py`

No fixture directories or fixture metadata may be modified in S10B.

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

Private user-local paths that must not be inspected or modified:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`

## Source Protocol

Use only:

1. S0-S10A adapter docs for prior adapter conclusions.
2. Existing S10A fixture corpus and harness files.
3. Repository-local PAI v5 release files for PAI facts only if needed.
4. Official OpenAI Codex docs only if S10B adds or refreshes a Codex capability claim.
5. Local `codex --version` or `codex --help` only if already available and non-invasive.

Do not use unofficial Codex capability sources. Do not infer current Codex behavior from memory.

## Source Material

Approved read-only sources used by S10B:

- `docs/adapters/V5_S10A_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_S10A_WRITE_SET_AND_ACCEPTANCE_CONTRACT.md`
- `docs/adapters/V5_CODEX_FIXTURE_CORPUS_DESIGN_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_HARNESS_DESIGN_SPEC.md`
- `docs/adapters/V5_CODEX_INTEGRATED_READ_ONLY_FIXTURE_TRIAL_ARCHITECTURE.md`
- S10A fixture harness files under `tests/adapters/v5-codex-readonly-fixture-trial/`

Repository release files remain read-only and were not needed beyond existing S10A/S9B evidence.

## Completion Contract

```text
This Completion Contract is the authoritative contract for V5-S10B.

Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S10B_EXEC_PLAN.md`.

Do not mark S10B complete unless every requirement below is satisfied.

### Strategic conclusions to preserve

The S10B deliverables must preserve these conclusions:

* Codex is not currently proven drop-in for existing local PAI v5 files.
* Codex replacement is plausible only through a designed adapter.
* S10B validates the S10A fixture harness with negative controls and regression tests only.
* S10B does not implement a Codex runtime adapter.
* S10B does not create runtime adapter files.
* S10B does not create root `AGENTS.md`.
* S10B does not create `.codex/`.
* S10B does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, trial outputs, manifest instances, audit artifacts, executable schemas, live-trial artifacts, or committed negative fixtures.
* S10B self-test temporary data is not a fixture corpus, not a manifest, not an audit artifact, and not runtime payload.
* S10B harness stdout is not an audit artifact.
* Claude-shaped files must not be copied directly into Codex surfaces.
* Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
* `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
* `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
* Future Codex `AGENTS.md`, if later authorized, must be a compact router.
* Codex config/profile is policy/configuration, not Life OS doctrine.
* Codex hooks and rules are future native control surfaces, not Claude hook destinations.
* Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.
* PAI Memory and ISA artifacts are canonical PAI state.
* Product memories must not be silently promoted into PAI Memory.
* Pulse is central v5 infrastructure, but S10B does not start Pulse, call Pulse endpoints, or claim Pulse parity.
* S10B must prove only fixture harness positive/negative behavior, not Codex drop-in behavior.
* Future read-only trials against live existing-local-v5 state remain unauthorized.
* Future writes require a single-writer policy, provenance, rollback, validation, and conflict handling.

### Required local discovery commands

Run these commands from repository root before creating files:

git status --short

test -f docs/adapters/V5_S10A_EXEC_PLAN.md
test -f docs/adapters/V5_CODEX_S10A_WRITE_SET_AND_ACCEPTANCE_CONTRACT.md
test -f tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py
test -d tests/adapters/v5-codex-readonly-fixture-trial/fixtures

python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py \
  --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures

Do not inspect live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or any user-local state.

Do not start Pulse.

Do not call `localhost:31337`.

Do not run installers.

Do not invoke Claude Code.

Do not run Codex import/migration tooling.

Do not run Codex hook, rule, execpolicy, or runtime commands.

### Required file: `docs/adapters/V5_S10B_EXEC_PLAN.md`

This file must be created first.

It must contain exactly these H1/H2 headings: `# V5-S10B Execution Plan`, `## Purpose`, `## Scope`, `## Approved Write Set`, `## Protected Paths`, `## Source Protocol`, `## Source Material`, `## Completion Contract`, `## Milestones`, `## Self-Review Rubric`, `## Hard Failure Conditions`, `## Validation Commands`, `## Progress`, `## Iteration Log`, `## Surprises & Discoveries`, `## Decision Log`, and `## Outcomes & Retrospective`.

The `## Completion Contract` section must contain a verbatim copy of this Completion Contract.

The execution plan must include these milestones:

1. Baseline status check.
2. S10A reread.
3. Existing harness positive-path verification.
4. Negative-control self-test implementation.
5. README update.
6. Harness importability repair only if required.
7. Positive and negative validation execution.
8. Protected-path and no-extra-file validation.
9. Self-review and repair.
10. Final handoff and goal-state report.

The self-review rubric must total 100 points:

| Area                                                                          | Points |
| ----------------------------------------------------------------------------- | -----: |
| Scope and protected-path discipline                                           |     15 |
| Evidence discipline                                                           |     10 |
| Positive-path fixture validation coverage                                     |     15 |
| Negative-control coverage quality                                             |     30 |
| Self-test safety and cleanup quality                                          |     15 |
| No-write, no-private-state, Pulse, Memory, ISA, and runtime-invocation safety |     10 |
| Verification quality                                                          |      5 |

Pass threshold:

Minimum score: 94/100
Hard failures: 0

Record at least one scored iteration in `## Iteration Log`.

### Required self-test file: `tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`

Implement a Python 3 self-test script using only the Python standard library.

The self-test script must set `sys.dont_write_bytecode = True` before importing the harness, import the existing harness module, use temporary directories only for generated negative-control fixture corpora, automatically clean up temporary directories, avoid committed negative fixtures, avoid repository writes outside the approved self-test file, avoid subprocesses, avoid network access, avoid non-stdlib dependencies, avoid release reads, avoid user-local reads, avoid Pulse startup and endpoint calls, avoid Claude Code and Codex invocation, emit stdout only, exit `0` when all expected positive and negative cases behave correctly, and exit non-zero on failure.

The self-test must verify the approved S10A fixture corpus passes.

The self-test must generate temporary negative cases for at least these IDs and required failure behaviors:

NC-001 missing fixture directory.
NC-002 extra file inside a fixture directory.
NC-003 missing required metadata field.
NC-004 invalid `fixture_source_class`.
NC-005 forbidden `sanitized-user-fixture`.
NC-006 forbidden live/private source path such as `~/.claude/PAI`.
NC-007 missing `expected_no_write_proofs` key.
NC-008 false `expected_no_write_proofs` value.
NC-009 missing `expected_audit_fields` value.
NC-010 missing denied-path coverage for Pulse endpoint calls.
NC-011 invalid `privacy_status`.
NC-012 invalid `s10a_status`.
NC-013 invalid JSON in `fixture.json`.
NC-014 unexpected fixture directory.
NC-015 missing README.

For each negative case, the self-test must verify `negative_id`, `description`, `expected_failure_signal`, `observed_failure_signal`, and `status`.

The self-test report must include `S10B harness negative-control self-test report`, `positive_control_status`, `negative_control_count`, and `status`.

### Required README update

Update `tests/adapters/v5-codex-readonly-fixture-trial/README.md` with an S10B section explaining negative-control self-tests, temporary-only negative controls, no committed negative fixtures, no Codex, no Claude Code, no Pulse, no live user-local state, no PAI Memory or ISA writes, no manifests, audit artifacts, schemas, configs, or runtime files, and no Codex drop-in proof.

### Optional harness modification rule

The existing harness file may be modified only if S10B discovers it is not importable or cannot support the required negative-control self-tests. Any modification must preserve all S10A guarantees.

### Protected paths

Do not modify protected paths and do not inspect or modify private user-local state.

### Hard failure conditions

S10B fails immediately if any file outside the approved write set is created or modified, fixture files or metadata are modified, protected files are modified, runtime adapter/config/payload/trial artifacts are created, committed negative fixtures are created, live trials are run, private or live existing-local-v5 state is read, PAI Memory or ISA is written, Pulse is started or called, installers, Claude Code, Codex runtime, import/migration tooling, or hook/rule/execpolicy commands are run, the harness or self-test uses forbidden dependencies, subprocesses, network access, repository writes, or leaves Python cache/temp artifacts, prohibited readiness claims are made, or the goal advances beyond S10B.

### Required validation commands

Run `git status --short`, `git diff --name-only | sort`, `git diff --check`, the original S10A harness, the S10B negative-control self-test, changed-file check, exact H1/H2 heading sequence check, self-test source check, harness static safety check, no committed negative fixtures or generated artifacts check, content invariant check, and protected-path check.

### Acceptance criteria

S10B is complete only if only approved files are created or modified, fixture files and metadata are not modified, no protected files are changed, no prohibited runtime/state/trial artifacts are created, no committed negative fixtures are created, no private or live state is read, PAI Memory and ISA are not written, Pulse is not started or called, the execution plan contains this contract, the original harness passes, the S10B self-test passes, self-test covers NC-001 through NC-015, self-test and harness remain standard-library/no-subprocess/no-network/no-write-safe, no Python cache or temp artifacts remain, all required checks pass, deliverables make no prohibited claims or authorizations, the execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures, and final handoff reports every required validation command.
```

## Milestones

1. Baseline status check.
2. S10A reread.
3. Existing harness positive-path verification.
4. Negative-control self-test implementation.
5. README update.
6. Harness importability repair only if required.
7. Positive and negative validation execution.
8. Protected-path and no-extra-file validation.
9. Self-review and repair.
10. Final handoff and goal-state report.

## Self-Review Rubric

| Area                                                                          | Points |
| ----------------------------------------------------------------------------- | -----: |
| Scope and protected-path discipline                                           |     15 |
| Evidence discipline                                                           |     10 |
| Positive-path fixture validation coverage                                     |     15 |
| Negative-control coverage quality                                             |     30 |
| Self-test safety and cleanup quality                                          |     15 |
| No-write, no-private-state, Pulse, Memory, ISA, and runtime-invocation safety |     10 |
| Verification quality                                                          |      5 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

- Any file outside the approved write set is created or modified.
- Fixture files or fixture metadata are modified.
- Any protected file is modified.
- Runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, manifest instances, audit artifacts, executable schemas, live-trial artifacts, or Pulse bridge files are created.
- Committed negative fixture directories or files are created.
- A live read-only trial is run.
- Private user-local state or live existing-local-v5 state is inspected or modified.
- PAI Memory or ISA is written.
- Pulse is started, Pulse endpoints are called, or `localhost:31337` is probed.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, or Codex hook/rule/execpolicy commands are run.
- The harness or self-test imports non-stdlib dependencies, runs subprocesses, uses network access, writes outside allowed temporary/self-test scope, or leaves `__pycache__`, `.pyc`, or temporary artifacts in the repository.
- The docs, harness, or self-test claim Codex is drop-in today or the official upstream engine.
- The docs, harness, or self-test authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, Pulse implementation, existing-local-v5 trial execution, product-memory promotion into PAI Memory, or dual-engine uncoordinated writes.
- The docs, harness, or self-test imply Claude-shaped files can be copied directly into Codex surfaces.
- The goal advances beyond S10B.

## Validation Commands

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Original S10A harness:
  - `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures`
- S10B negative-control self-test:
  - `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`
- Changed-file check.
- Exact H1/H2 heading sequence check for this execution plan.
- Self-test source check.
- Harness static safety check.
- No committed negative fixtures or generated artifacts check.
- Content invariant check.
- Protected-path check.

## Progress

- Baseline status check: complete. Initial `git status --short` had no output.
- S10A reread: complete. Required S10A execution plan, S10A write-set contract, harness, and fixture root exist.
- Existing harness positive-path verification: complete. The S10A harness passed against the approved fixture corpus before S10B edits.
- Negative-control self-test implementation: complete. The self-test imports the S10A harness with `sys.dont_write_bytecode = True`, generates temporary invalid fixture corpora, and covers `NC-001` through `NC-015`.
- README update: complete. The S10A harness README now documents the S10B negative-control scope and exclusions.
- Harness importability repair only if required: complete. No harness modification was required.
- Positive and negative validation execution: complete. The original S10A harness passed, and the S10B negative-control self-test passed with 15/15 expected failures detected.
- Protected-path and no-extra-file validation: complete. Changed-file scope, protected-path status, generated-artifact checks, and no committed negative fixture checks passed.
- Self-review and repair: complete. One trailing blank line in the new self-test was removed; one embedded contract heading list was reformatted so the execution-plan heading validator sees only the required H1/H2 sequence.
- Final handoff and goal-state report: pending final response.

## Iteration Log

| Iteration | Scope and protected-path discipline | Evidence discipline | Positive-path fixture validation coverage | Negative-control coverage quality | Self-test safety and cleanup quality | No-write, no-private-state, Pulse, Memory, ISA, and runtime-invocation safety | Verification quality | Score | Hard failures | Notes |
| --------- | ----------------------------------: | ------------------: | ----------------------------------------: | --------------------------------: | -----------------------------------: | --------------------------------------------------------------------------: | -------------------: | ----: | ------------: | ----- |
| 1 | 15/15 | 10/10 | 15/15 | 30/30 | 15/15 | 10/10 | 5/5 | 100/100 | 0 | S10B stayed within the approved write set, left fixture metadata untouched, validated the positive S10A corpus, and proved all 15 required negative controls fail as expected. |

## Surprises & Discoveries

- The S10A harness was already importable without modification because its CLI entrypoint is guarded by `if __name__ == "__main__"`.
- `TemporaryDirectory` cleanup left no `__pycache__`, `.pyc`, committed negative fixture, report, manifest, audit artifact, schema, or runtime artifact in the repository.
- The first heading check caught copied contract heading names inside the execution plan body. The executable plan headings were left unchanged, and the embedded list was reformatted to avoid false heading detection.

## Decision Log

- S10B will not modify fixture metadata or fixture directories.
- The existing S10A harness appears importable through `importlib` without changing the harness file.
- Negative controls will be generated only under temporary directories and cleaned automatically.
- The self-test verifies the approved S10A corpus as a positive control before negative controls.
- The negative controls exercise missing directory, extra file, missing metadata field, invalid source class, forbidden sanitized fixture class, private source path, missing no-write proof key, false no-write proof value, missing audit field, missing Pulse endpoint denial, invalid privacy status, invalid S10A status, invalid JSON, unexpected directory, and missing README.
- Harness stdout and self-test stdout remain validation output only and are not audit artifacts.

## Outcomes & Retrospective

Validation results recorded for S10B:

- `git status --short`: passed; output listed only `docs/adapters/V5_S10B_EXEC_PLAN.md`, `tests/adapters/v5-codex-readonly-fixture-trial/README.md`, and `tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`.
- `git diff --name-only | sort`: passed; output listed exactly the approved S10B files.
- `git diff --check`: passed after trailing blank-line cleanup.
- Original S10A harness execution passed:
  - `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures`
- S10B negative-control self-test passed:
  - `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`
- Changed-file check: passed.
- Exact H1/H2 heading sequence check for this execution plan: passed.
- Self-test source check: passed.
- Harness static safety check: passed.
- No committed negative fixtures or generated artifacts check: passed.
- Content invariant check: passed.
- Protected-path check: passed with no output.

No fixture directory or fixture metadata was modified. No protected files were changed. No committed negative fixture, manifest instance, audit artifact, schema, runtime adapter file, root `AGENTS.md`, `.codex/`, Codex config, hook, rule, skill, subagent, agent, command, launcher, installer, wrapper, generated config, migration script, adapter payload, Memory payload, ISA payload, Pulse payload, trial output, live-trial artifact, or Pulse bridge file was created.

S10B proves only positive and negative harness behavior for fixture metadata. It does not prove Codex drop-in behavior, official upstream engine status, Pulse parity, Memory/ISA write safety, existing-local-v5 trial readiness, or runtime adapter correctness.
