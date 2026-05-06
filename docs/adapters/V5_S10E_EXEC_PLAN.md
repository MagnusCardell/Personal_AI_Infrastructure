# V5-S10E Execution Plan

## Purpose

Validate that the existing S10 fixture corpus globally covers the accepted seam, gate, and coverage model, and make the read-only harness report deterministic global coverage counts.

S10E is adapter-test implementation only. It does not implement a runtime adapter.

## Scope

S10E is limited to this execution plan, the read-only fixture harness, the harness self-test, the harness README, and fixture metadata or case data only if needed for global coverage closure.

Codex is not currently proven drop-in for existing local PAI v5 files. S10E validates fixture coverage only.

## Approved Write Set

Create exactly:

- `docs/adapters/V5_S10E_EXEC_PLAN.md`

Modify exactly if needed:

- `tests/adapters/v5-codex-readonly-fixture-trial/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py`
- `tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`

Allowed fixture metadata and case-data modifications, only if needed for coverage closure:

- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-001-release-baseline-static/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-001-release-baseline-static/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-002-authority-doctrine/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-002-authority-doctrine/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-003-compact-router-non-installation/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-003-compact-router-non-installation/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-004-launcher-inference-static/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-004-launcher-inference-static/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-005-hook-lifecycle-static/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-005-hook-lifecycle-static/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-006-pulse-static-no-start/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-006-pulse-static-no-start/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-007-memory-isa-static-no-write/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-007-memory-isa-static-no-write/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-008-denied-path-negative/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-008-denied-path-negative/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-009-product-memory-negative/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-009-product-memory-negative/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-010-unsupported-surface-reporting/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-010-unsupported-surface-reporting/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-011-rollback-no-residue/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-011-rollback-no-residue/case.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-012-dual-engine-boundary/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-012-dual-engine-boundary/case.json`

Do not modify fixture `README.md` files. Do not add, remove, or rename fixture directories.

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

1. S0-S10D adapter docs for prior adapter conclusions.
2. Existing S10A/S10B/S10C/S10D fixture corpus and harness files.
3. Repository-local PAI v5 release files for PAI facts only if needed.
4. Official OpenAI Codex docs only if S10E adds or refreshes a Codex capability claim.
5. Local `codex --version` or `codex --help` only if already available and non-invasive.

Do not use unofficial Codex capability sources. Do not infer current Codex behavior from memory.

## Source Material

Approved read-only sources used by S10E:

- `docs/adapters/V5_S10D_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_COVERAGE_MATRIX.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_SEQUENCE_AND_GATE_MODEL.md`
- `docs/adapters/V5_CODEX_TRIAL_FAILURE_ROLLBACK_AND_AUDIT_MODEL.md`
- Existing fixture corpus and harness files under `tests/adapters/v5-codex-readonly-fixture-trial/`

Repository release files remain read-only and were not needed for S10E edits.

## Completion Contract

This Completion Contract is the authoritative contract for V5-S10E. Copy this entire Completion Contract into `docs/adapters/V5_S10E_EXEC_PLAN.md`.

Required conclusions: Codex is not currently proven drop-in for existing local PAI v5 files; S10E validates fixture coverage only; S10E does not implement a runtime adapter; S10E does not create root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, agents, commands, launchers, installers, manifests, audit artifacts, executable schemas, live-trial artifacts, runtime payloads, Memory payloads, ISA payloads, or Pulse payloads; fixture metadata and case data are not manifests, audit artifacts, or runtime payload; harness stdout is not an audit artifact; Pulse is not started or called; PAI Memory and ISA are not written; existing-local-v5 state is not read; product memories must not be silently promoted into PAI Memory; Claude-shaped files must not be copied directly into Codex surfaces.

Required execution-plan headings: `docs/adapters/V5_S10E_EXEC_PLAN.md` must contain exactly the H1/H2 sequence used by this file: title, Purpose, Scope, Approved Write Set, Protected Paths, Source Protocol, Source Material, Completion Contract, Milestones, Self-Review Rubric, Hard Failure Conditions, Validation Commands, Progress, Iteration Log, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective.

Required harness behavior: update the harness so it validates global corpus coverage. Every required fixture ID `FX-001` through `FX-012` must exist. Every required seam must appear at least once across `covered_seams`: authority seam, compact router seam, launcher seam, inference seam, engine profile/capability seam, hook/lifecycle seam, event/context envelope seam, hook permission/safety seam, Pulse identity seam, Pulse read-only event seam, Pulse observability/audit seam, Memory/ISA single-writer seam, Memory boundary/promotion seam, ISA workflow/state seam, Memory/ISA audit/conflict seam, manifest schema seam, audit schema seam, dry-run validation seam, rollback seam, fixture isolation seam, denied-path seam, unsupported-surface seam, and dual-engine boundary seam. Every coverage ID `CVG-001` through `CVG-025` must appear at least once across `coverage_ids`. Every gate ID `TG-001` through `TG-020` must appear at least once across `gate_ids`. Every required denied category must appear at least once across corpus denial data. Every required no-write proof must be asserted in every fixture. Every fixture must have at least one unsupported-surface expectation. The harness report must include `S10E global coverage validation`, `fixture_count`, `case_count`, `seam_count`, `coverage_id_count`, `gate_id_count`, `denied_category_count`, and `status`.

Required self-test update: preserve `NC-001` through `NC-045` and add `NC-046` through `NC-060`: missing global seam coverage, missing global coverage ID, missing global gate ID, duplicate fixture ID, duplicate case ID, case references coverage not present in fixture metadata, fixture metadata references coverage not present in case expectations, missing global denied category, missing global unsupported-surface expectation, missing rollback/no-residue expectation, missing drop-in claim denial, missing Pulse no-start/no-call coverage, missing Memory/ISA no-write coverage, missing product-memory non-promotion coverage, and missing Claude file direct-copy denial. The self-test report must include `S10E global coverage negative-control self-test report`, `positive_control_status`, `negative_control_count`, and `status`, with `negative_control_count` equal to `60`.

Required README update: add an S10E section explaining that S10E validates global fixture coverage; checks global seam, gate, coverage, denial, unsupported-surface, rollback, Pulse, Memory, ISA, product-memory, and drop-in denial coverage; extends negative controls to `NC-001` through `NC-060`; keeps the harness read-only; does not run Codex, Claude Code, Pulse, or live trials; keeps fixture metadata and case data out of manifests and audit artifacts; and preserves that Codex is not currently proven drop-in for existing local PAI v5 files.

Hard failures: S10E fails if any file outside the approved write set changes; fixture README files change; fixture directories are added, removed, or renamed; any protected path changes; the harness or self-test uses non-stdlib dependencies, subprocesses, or network access; the harness writes files; the self-test leaves `__pycache__`, `.pyc`, or temporary artifacts in the repository; Pulse is started or called; `localhost:31337` is probed; Claude Code or Codex runtime is invoked; live user-local state is read; PAI Memory or ISA is written; any deliverable claims Codex is drop-in today or official upstream engine; or any deliverable authorizes live trials, runtime adapter work, Memory writes, ISA writes, Pulse implementation, product-memory promotion, or dual-engine uncoordinated writes.

Required validation commands: run `git status --short`, `git diff --name-only | sort`, `git diff --check`, the harness against the approved fixture corpus, the S10E negative-control self-test, changed-file check, execution-plan heading check, global coverage source check, static safety check, generated-artifact check, and protected-path check.

Final handoff format: end with exactly `Files changed`, `Behavior changed`, `Tests run`, `Known risks`, `Protected files changed`, `Goal state`, and `Recommended next architect decision` headings.

## Milestones

1. Baseline status check.
2. S10D reread and global coverage inventory.
3. Fixture coverage closure assessment.
4. Harness global coverage validation update.
5. Negative-control self-test update.
6. README update.
7. Positive and negative validation execution.
8. Protected-path and no-extra-file validation.
9. Self-review and repair.
10. Final handoff and goal-state report.

## Self-Review Rubric

| Area                                                                          | Points |
| ----------------------------------------------------------------------------- | -----: |
| Scope and protected-path discipline                                           |     15 |
| Evidence discipline                                                           |     10 |
| Global fixture coverage quality                                               |     25 |
| Harness summary determinism and validation quality                            |     25 |
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
- Fixture README files are modified.
- Fixture directories are added, removed, or renamed.
- Any protected path is modified.
- Runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, agents, commands, launchers, installers, manifests, audit artifacts, executable schemas, live-trial artifacts, runtime payloads, Memory payloads, ISA payloads, or Pulse payloads are created.
- The harness or self-test imports non-stdlib dependencies, runs subprocesses, uses network access, or writes outside approved behavior.
- The self-test leaves `__pycache__`, `.pyc`, or temporary artifacts in the repository.
- Pulse is started or called, `localhost:31337` is probed, Claude Code or Codex runtime is invoked, live user-local state is read, or PAI Memory or ISA is written.
- Any deliverable claims Codex is drop-in today or the official upstream engine.
- Any deliverable authorizes live trials, runtime adapter work, Memory writes, ISA writes, Pulse implementation, product-memory promotion, or dual-engine uncoordinated writes.
- The goal advances beyond S10E.

## Validation Commands

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Harness:
  - `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures`
- S10E negative-control self-test:
  - `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`
- Changed-file check.
- Execution-plan heading check.
- Global coverage source check.
- Static safety check.
- Generated-artifact check.
- Protected-path check.

## Progress

- Baseline status check: complete. Initial `git status --short` had no output.
- S10D reread and global coverage inventory: complete. Current fixture metadata already covers all required seams, all `CVG-001` through `CVG-025`, and all `TG-001` through `TG-020`.
- Fixture coverage closure assessment: complete. Global coverage closure did not require fixture metadata changes; case data was hardened with `coverage_expectations` matching fixture metadata coverage IDs.
- Harness global coverage validation update: complete. The harness validates global seam, coverage ID, gate ID, denied category, unsupported-surface, rollback/no-residue, Pulse, Memory/ISA, product-memory, Claude direct-copy, duplicate ID, and fixture/case coverage alignment.
- Negative-control self-test update: complete. The self-test preserves `NC-001` through `NC-045` and adds `NC-046` through `NC-060`, with `negative_control_count: 60`.
- README update: complete. The harness README now documents S10E global coverage validation and safety boundaries.
- Positive and negative validation execution: complete. The harness passed against the approved fixture corpus, and the S10E negative-control self-test passed.
- Protected-path and no-extra-file validation: complete. Changed-file scope, protected-path status, generated-artifact checks, and no fixture README/directory changes passed.
- Self-review and repair: complete. One self-test mismatch was repaired by tightening global denied-category aggregation to denied behavior data. No hard failures remain; validation score is 100/100.
- Final handoff and goal-state report: pending final response.

## Iteration Log

| Iteration | Scope and protected-path discipline | Evidence discipline | Global fixture coverage quality | Harness summary determinism and validation quality | Negative-control coverage quality | No-write, no-private-state, Pulse, Memory, ISA, and runtime-invocation safety | Verification quality | Score | Hard failures | Notes |
| --------- | ----------------------------------: | ------------------: | ------------------------------: | -------------------------------------------------: | --------------------------------: | --------------------------------------------------------------------------: | -------------------: | ----: | ------------: | ----- |
| 1 | 15/15 | 10/10 | 25/25 | 24/25 | 9/10 | 10/10 | 5/5 | 98/100 | 0 | Initial S10E implementation passed the positive harness but one negative-control expected signal used broader no-write text as denied coverage. |
| 2 | 15/15 | 10/10 | 25/25 | 25/25 | 10/10 | 10/10 | 5/5 | 100/100 | 0 | Global denied-category aggregation was tightened to denied behavior data; the harness and all 60 negative controls passed. |

## Surprises & Discoveries

- The existing S10D corpus already covered all 23 required seams, all 25 coverage IDs, and all 20 gate IDs before S10E edits.
- S10E coverage closure did not require fixture metadata changes.
- Global denied-category validation needed to count denied behavior data separately from no-write expectation text so the dedicated missing-denial negative control proved the intended policy.

## Decision Log

- S10E will not modify fixture README files or fixture directories.
- S10E will keep the harness and self-test standard-library-only and free of subprocesses, network access, Codex invocation, Claude Code invocation, Pulse startup, Pulse endpoint calls, live trials, user-local reads, PAI Memory writes, and ISA writes.
- S10E will treat fixture metadata and case data as non-runtime adapter-test inputs, not manifests, audit artifacts, or runtime payload.
- S10E will add `coverage_expectations` to approved case data so each case can be checked against its fixture metadata coverage IDs.
- S10E will report deterministic global counts for fixtures, cases, seams, coverage IDs, gate IDs, and denied categories.

## Outcomes & Retrospective

Validation results recorded for S10E:

- `git status --short`: passed; output listed only the approved S10E files.
- `git diff --name-only | sort`: passed; output listed the approved S10E execution plan, harness README, harness, self-test, and 12 approved fixture case files.
- `git diff --check`: passed.
- Harness execution passed:
  - `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures`
- S10E negative-control self-test passed:
  - `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`
- Changed-file check: passed.
- Execution-plan heading check: passed.
- Global coverage source check: passed.
- Static safety check: passed.
- Generated-artifact check: passed.
- Protected-path check: passed with no output.

The final harness report includes `S10E global coverage validation`, `fixture_count: 12`, `case_count: 12`, `seam_count: 23`, `coverage_id_count: 25`, `gate_id_count: 20`, `denied_category_count: 13`, and `status: pass`.

S10E remains fixture coverage validation only. It does not implement a runtime adapter, does not create manifests or audit artifacts, does not run live trials, does not read existing-local-v5 state, does not start or call Pulse, and does not write PAI Memory or ISA.
