# V5-S10D Execution Plan

## Purpose

Add non-runtime fixture case data and extend the read-only harness so it validates expected behaviors, denied behaviors, unsupported-surface expectations, no-write expectations, rollback/no-residue expectations, and non-drop-in posture.

S10D is adapter-test implementation only. It does not implement a Codex runtime adapter and does not create runtime adapter files.

## Scope

S10D is limited to this execution plan, the approved new `case.json` fixture case files, the existing read-only harness, the existing negative-control self-test, and the harness README.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement remains plausible only through a designed adapter.

## Approved Write Set

Create exactly:

- `docs/adapters/V5_S10D_EXEC_PLAN.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-001-release-baseline-static/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-002-authority-doctrine/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-003-compact-router-non-installation/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-004-launcher-inference-static/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-005-hook-lifecycle-static/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-006-pulse-static-no-start/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-007-memory-isa-static-no-write/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-008-denied-path-negative/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-009-product-memory-negative/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-010-unsupported-surface-reporting/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-011-rollback-no-residue/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-012-dual-engine-boundary/case.json`

Modify exactly:

- `tests/adapters/v5-codex-readonly-fixture-trial/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py`
- `tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`

Do not modify fixture `README.md` files. Do not modify fixture `fixture.json` files. Do not add, remove, or rename fixture directories.

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

1. S0-S10C adapter docs for prior adapter conclusions.
2. Existing S10A/S10B/S10C fixture corpus and harness files.
3. Repository-local PAI v5 release files for PAI facts only if needed.
4. Official OpenAI Codex docs only if S10D adds or refreshes a Codex capability claim.
5. Local `codex --version` or `codex --help` only if already available and non-invasive.

Do not use unofficial Codex capability sources. Do not infer current Codex behavior from memory.

## Source Material

Approved read-only sources used by S10D:

- `docs/adapters/V5_S10A_EXEC_PLAN.md`
- `docs/adapters/V5_S10B_EXEC_PLAN.md`
- `docs/adapters/V5_S10C_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_FIXTURE_CORPUS_DESIGN_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_HARNESS_DESIGN_SPEC.md`
- `docs/adapters/V5_CODEX_INTEGRATED_READ_ONLY_FIXTURE_TRIAL_ARCHITECTURE.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_SEQUENCE_AND_GATE_MODEL.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_COVERAGE_MATRIX.md`
- `docs/adapters/V5_CODEX_TRIAL_FAILURE_ROLLBACK_AND_AUDIT_MODEL.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- Existing fixture corpus and harness files under `tests/adapters/v5-codex-readonly-fixture-trial/`

Repository release files remain read-only and were not needed for S10D edits.

## Completion Contract

This Completion Contract is the authoritative contract for V5-S10D. Before drafting the deliverables, copy this entire Completion Contract section into `docs/adapters/V5_S10D_EXEC_PLAN.md`. Do not mark S10D complete unless every requirement below is satisfied.

Strategic conclusions to preserve: Codex is not currently proven drop-in for existing local PAI v5 files; Codex replacement is plausible only through a designed adapter; S10D adds fixture case data and expected-behavior validation only; S10D does not implement a Codex runtime adapter; S10D does not create runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, trial outputs, manifest instances, audit artifacts, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures; S10D fixture case data is not a manifest, not an audit artifact, and not runtime payload; S10D harness stdout is not an audit artifact; S10D self-test temporary data is not a fixture corpus, not a manifest, not an audit artifact, and not runtime payload; Claude-shaped files must not be copied directly into Codex surfaces; Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists; `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown; `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file; future Codex `AGENTS.md`, if later authorized, must be a compact router; Codex config/profile is policy/configuration, not Life OS doctrine; Codex hooks and rules are future native control surfaces, not Claude hook destinations; Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory; PAI Memory and ISA artifacts are canonical PAI state; product memories must not be silently promoted into PAI Memory; Pulse is central v5 infrastructure, but S10D does not start Pulse, call Pulse endpoints, or claim Pulse parity; S10D proves only fixture case validation and harness policy behavior, not Codex drop-in behavior; future read-only trials against live existing-local-v5 state remain unauthorized; future writes require a single-writer policy, provenance, rollback, validation, and conflict handling.

Required local discovery commands: run `git status --short`, file-existence checks for S10C and S9A/S10C design sources, existence checks for the harness, self-test, and fixture root, the harness against the approved fixture corpus, and the S10C negative-control self-test before creating files. Do not inspect live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or user-local state. Do not start Pulse, call `localhost:31337`, run installers, invoke Claude Code, run Codex import or migration tooling, or run Codex hook/rule/execpolicy/runtime commands.

Required execution plan file: `docs/adapters/V5_S10D_EXEC_PLAN.md` must be created first and contain exactly the H1/H2 sequence used by this file. The execution plan must include the required milestones, a 100-point rubric with minimum score 94/100 and hard failures 0, and at least one scored iteration.

Required fixture case files: each fixture directory must contain exactly `README.md`, `fixture.json`, and `case.json` after S10D. Each `case.json` file must include `case_id`, `fixture_id`, `case_name`, `case_type`, `case_status`, `input_symbols`, `source_references`, `expected_behaviors`, `denied_behaviors`, `unsupported_surface_expectations`, `no_write_expectations`, `audit_expectations`, `rollback_expectations`, `prohibited_actions`, `source_policy`, `drop_in_claim_allowed`, `codex_runtime_invocation_allowed`, `claude_code_invocation_allowed`, `pulse_start_allowed`, `pulse_endpoint_call_allowed`, `pai_memory_write_allowed`, `isa_write_allowed`, `product_memory_promotion_allowed`, and `existing_local_v5_access_allowed`. `case_status` must be `s10d-fixture-case-data-only`. `case_type` must be one of the allowed S10D boundary types: release baseline, authority, router non-installation, launcher/inference, hook/lifecycle, Pulse, Memory/ISA, denied path, product memory, unsupported surface, rollback, or dual engine. All prohibited boolean fields must be `false`. Required list fields must be non-empty. `source_policy` must contain every required key set to `true`: `repository_relative_only`, `synthetic_markers_allowed`, `no_absolute_paths`, `no_home_paths`, `no_parent_traversal`, `no_protected_root_paths`, `no_live_user_local_paths`, and `no_release_file_writes`.

Required denied behavior coverage: every `case.json` must include denied behaviors for root `AGENTS.md` write, `.codex/` write, release file write, Claude file direct-copy, Codex runtime invocation, Claude Code invocation, Pulse startup, Pulse endpoint call, PAI Memory write, ISA write, product memory promotion, existing-local-v5 access, and drop-in claim. Every `case.json` must include unsupported-surface expectations for at least one relevant seam or surface. Every `source_references` entry must be repository-relative or use an approved synthetic marker prefix: `synthetic:`, `negative:`, or `unsupported:`. Source references must not start with `/`, `~`, `.codex`, `.claude`, `PAI/`, `AGENTS.md`, or `CLAUDE.md`; must not contain `..`, `/home/`, or `/Users/`; and must use allowed repository-relative prefixes for release, docs, or fixture references.

Required harness update: update the existing harness so it validates all S10D case files while preserving all S10A/S10B/S10C guarantees: standard library only, no subprocesses, no network, no writes, reads only the fixture root passed to it, stdout report only, no Pulse startup, no Pulse endpoint calls, no Claude Code invocation, no Codex runtime invocation, no user-local reads, no PAI Memory writes, and no ISA writes. The harness must fail on missing `case.json`, invalid case JSON, missing required case field, fixture ID mismatch between directory, `fixture.json`, and `case.json`, invalid `case_type`, invalid `case_status`, empty required case lists, missing denied behavior category, missing or false `source_policy` key, forbidden `source_references` pattern, any prohibited boolean set to `true`, and fixture directory file-set violations. The harness report must include `S10D fixture case validation`, `fixture_count`, `case_count`, `case_status`, and `status`.

Required self-test update: preserve `NC-001` through `NC-030` and add `NC-031` through `NC-045` covering missing `case.json`, invalid case JSON, case fixture ID mismatch, missing required case field, invalid `case_type`, invalid `case_status`, empty `input_symbols`, empty `expected_behaviors`, missing denied behavior category, empty unsupported-surface expectations, empty no-write expectations, false or missing `source_policy` key, forbidden source reference such as `~/.claude/PAI`, prohibited action boolean set to `true`, and extra unexpected file after S10D file-set rules. The self-test must keep `sys.dont_write_bytecode = True`, use temporary directories only, clean up automatically, leave no Python cache or temp artifacts in the repository, avoid subprocesses, network, release reads, user-local reads, Claude Code, Codex, Pulse startup, and Pulse endpoint calls, and emit stdout only. The self-test report must include `S10D fixture case negative-control self-test report`, `positive_control_status`, `negative_control_count`, and `status`, with `negative_control_count` equal to `45`.

Required README update: add an S10D section explaining `case.json` fixture case data, that `case.json` is fixture case data only, not a manifest, not an audit artifact, and not runtime payload, expected-behavior and denied-behavior validation, negative controls `NC-001` through `NC-045`, read-only harness behavior, no Codex, no Claude Code, no Pulse startup or endpoint calls, no live user-local state, no PAI Memory or ISA writes, and Codex is not currently proven drop-in for existing local PAI v5 files.

Protected paths and hard failures: do not modify protected paths; do not inspect private user-local state; do not modify fixture README files or fixture metadata files; do not add/remove/rename fixture directories; do not create runtime adapter files or prohibited Codex/runtime/state/trial artifacts; do not create committed negative fixtures, manifest instances, audit artifacts, schemas, live trials, private-state reads, PAI Memory writes, ISA writes, Pulse startup/calls/probes, installers, Claude Code invocation, Codex runtime/import/migration/hook/rule/execpolicy commands, non-stdlib harness or self-test dependencies, subprocesses, network access, harness writes, self-test repository writes outside approved files, Python cache/temp artifacts, prohibited drop-in/official-engine claims, PAI Memory or ISA write authorization, Pulse authorization, existing-local-v5 trial authorization, direct Claude-file copy authorization, product-memory promotion authorization, dual-engine uncoordinated write authorization, or advancement beyond S10D.

Required validation commands: run `git status --short`, `git diff --name-only | sort`, `git diff --check`, the harness against the approved fixture corpus, the S10D negative-control self-test, changed-file check, execution-plan heading sequence check, fixture case validation check, self-test source check, harness static safety check, no committed negative fixtures or generated artifacts check, content invariant check, and protected-path check.

Acceptance criteria: S10D is complete only if only approved files are created or modified, fixture READMEs and fixture metadata are not modified, fixture directories are unchanged, each fixture directory contains exactly `README.md`, `fixture.json`, and `case.json`, no protected/prohibited files are changed or created, no committed negative fixtures or live trials exist, no private or live state is read, Memory/ISA/Pulse remain untouched, every `case.json` exists and passes validation, the harness passes, the self-test passes and covers `NC-001` through `NC-045`, harness and self-test remain standard-library/no-subprocess/no-network/no-write safe, all required validation checks pass, deliverables make no prohibited claims or authorizations, the execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures, and final handoff reports every required validation command.

## Milestones

1. Baseline status check.
2. S10A/S10B/S10C reread.
3. Fixture case-data model implementation.
4. Case file creation for all twelve fixtures.
5. Harness case validation update.
6. Negative-control self-test update.
7. README update.
8. Positive and negative validation execution.
9. Protected-path and no-extra-file validation.
10. Self-review and repair.
11. Final handoff and goal-state report.

## Self-Review Rubric

| Area                                                                          | Points |
| ----------------------------------------------------------------------------- | -----: |
| Scope and protected-path discipline                                           |     15 |
| Evidence discipline                                                           |     10 |
| Fixture case-data quality                                                     |     25 |
| Harness expected-behavior validation quality                                  |     25 |
| Negative-control coverage quality                                             |     10 |
| No-write, no-private-state, Pulse, Memory, ISA, and runtime-invocation safety |     10 |
| Verification quality                                                          |      5 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

- Any file outside the approved write set is created or modified.
- Fixture README files or fixture metadata files are modified.
- Fixture directories are added, removed, or renamed.
- Any protected file is modified.
- Runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, manifest instances, audit artifacts, executable schemas, live-trial artifacts, runtime payloads, or Pulse bridge files are created.
- Committed negative fixture directories or files are created.
- A live read-only trial is run.
- Private user-local state or live existing-local-v5 state is inspected or modified.
- PAI Memory or ISA is written.
- Pulse is started, Pulse endpoints are called, or `localhost:31337` is probed.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, or Codex hook/rule/execpolicy commands are run.
- The harness or self-test imports non-stdlib dependencies, runs subprocesses, uses network access, writes outside approved behavior, or leaves `__pycache__`, `.pyc`, or temporary artifacts in the repository.
- The docs, harness, self-test, fixture metadata, or fixture case data claim Codex is drop-in today or the official upstream engine.
- The docs, harness, self-test, fixture metadata, or fixture case data authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, Pulse implementation, existing-local-v5 trial execution, product-memory promotion into PAI Memory, or dual-engine uncoordinated writes.
- The docs, harness, self-test, fixture metadata, or fixture case data imply Claude-shaped files can be copied directly into Codex surfaces.
- The goal advances beyond S10D.

## Validation Commands

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Harness:
  - `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures`
- S10D negative-control self-test:
  - `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`
- Changed-file check.
- Exact H1/H2 heading sequence check for this execution plan.
- Fixture case validation check.
- Self-test source check.
- Harness static safety check.
- No committed negative fixtures or generated artifacts check.
- Content invariant check.
- Protected-path check.

## Progress

- Baseline status check: complete. Initial `git status --short` had no output.
- S10A/S10B/S10C reread: complete. Required S10C plan, S9A/S10C design docs, harness, self-test, and fixture root exist.
- Fixture case-data model implementation: complete. The S10D `case.json` model validates expected behaviors, denied behaviors, unsupported-surface expectations, no-write expectations, audit expectations, rollback expectations, prohibited actions, source policy, and false authorization booleans.
- Case file creation for all twelve fixtures: complete. Each fixture directory now has one approved `case.json`; fixture README files and fixture metadata files were not modified.
- Harness case validation update: complete. The harness validates S10A metadata, S10C semantic fields, and S10D fixture case data while remaining read-only.
- Negative-control self-test update: complete. The self-test preserves `NC-001` through `NC-030` and adds `NC-031` through `NC-045`, with `negative_control_count: 45`.
- README update: complete. The harness README now documents S10D fixture case data and safety boundaries.
- Positive and negative validation execution: complete. The harness passed against the approved fixture corpus, and the S10D negative-control self-test passed.
- Protected-path and no-extra-file validation: complete. Changed-file scope, protected-path status, fixture directory checks, generated-artifact checks, and no committed negative fixture checks passed.
- Self-review and repair: complete. No hard failures were found; validation score is 100/100.
- Final handoff and goal-state report: pending final response.

## Iteration Log

| Iteration | Scope and protected-path discipline | Evidence discipline | Fixture case-data quality | Harness expected-behavior validation quality | Negative-control coverage quality | No-write, no-private-state, Pulse, Memory, ISA, and runtime-invocation safety | Verification quality | Score | Hard failures | Notes |
| --------- | ----------------------------------: | ------------------: | ------------------------: | -------------------------------------------: | --------------------------------: | --------------------------------------------------------------------------: | -------------------: | ----: | ------------: | ----- |
| 1 | 15/15 | 10/10 | 25/25 | 25/25 | 10/10 | 10/10 | 5/5 | 100/100 | 0 | S10D stayed within the approved write set, left fixture READMEs and fixture metadata unchanged, added all 12 case files, extended harness validation, and passed 45 negative controls. |

## Surprises & Discoveries

- The S10C metadata validation structure extended cleanly to case-file validation without requiring subprocesses, network access, or runtime invocation.
- The S10B/S10C temporary negative-control corpus pattern remained sufficient after adding `case.json`; no committed negative fixtures were needed.
- S10D file-set validation required updating the positive fixture directory rule from exactly `README.md` and `fixture.json` to exactly `README.md`, `fixture.json`, and `case.json`.

## Decision Log

- S10D will add `case.json` files only as non-runtime fixture case data, not manifests, audit artifacts, executable schemas, trial outputs, or runtime payloads.
- S10D will not modify fixture README files or fixture metadata files.
- The read-only harness and self-test will continue to use only the Python standard library and will not run subprocesses, network calls, Codex, Claude Code, Pulse, live trials, user-local reads, PAI Memory writes, or ISA writes.
- Every S10D `case.json` sets drop-in, Codex runtime invocation, Claude Code invocation, Pulse startup, Pulse endpoint call, PAI Memory write, ISA write, product memory promotion, and existing-local-v5 access booleans to `false`.
- The self-test report was upgraded to `S10D fixture case negative-control self-test report`.

## Outcomes & Retrospective

Validation results recorded for S10D:

- `git status --short`: passed; output listed only the approved S10D files.
- `git diff --name-only | sort`: passed; output listed the approved S10D execution plan, harness README, harness, self-test, and 12 approved fixture case files.
- `git diff --check`: passed.
- Harness execution passed:
  - `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures`
- S10D negative-control self-test passed:
  - `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`
- Changed-file check: passed.
- Exact H1/H2 heading sequence check for this execution plan: passed.
- Fixture case validation check: passed.
- Self-test source check: passed.
- Harness static safety check: passed.
- No committed negative fixtures or generated artifacts check: passed.
- Content invariant check: passed.
- Protected-path check: passed with no output.

S10D remains fixture-only adapter-test implementation. It does not implement a runtime adapter, does not create manifests or audit artifacts, does not run a live trial, does not read private user-local state, does not start or call Pulse, and does not write PAI Memory or ISA.
