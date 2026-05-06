# V5-S10C Execution Plan

## Purpose

Harden the S10A fixture metadata corpus and read-only harness so validation covers semantic policy ties to the accepted S7A/S7C/S7D/S7E/S8H/S9A safety and coverage model, not just structural metadata shape.

S10C is adapter-test implementation only. It does not implement a Codex runtime adapter and does not create runtime adapter files.

## Scope

S10C is limited to this execution plan, fixture metadata semantic fields, the existing read-only harness, the existing negative-control self-test, and the harness README.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement remains plausible only through a designed adapter.

## Approved Write Set

Create exactly:

- `docs/adapters/V5_S10C_EXEC_PLAN.md`

Modify exactly:

- `tests/adapters/v5-codex-readonly-fixture-trial/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py`
- `tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-001-release-baseline-static/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-002-authority-doctrine/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-003-compact-router-non-installation/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-004-launcher-inference-static/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-005-hook-lifecycle-static/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-006-pulse-static-no-start/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-007-memory-isa-static-no-write/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-008-denied-path-negative/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-009-product-memory-negative/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-010-unsupported-surface-reporting/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-011-rollback-no-residue/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-012-dual-engine-boundary/fixture.json`

No fixture README files may be modified. No fixture directories may be added, removed, or renamed.

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

1. S0-S10B adapter docs for prior adapter conclusions.
2. Existing S10A/S10B fixture corpus and harness files.
3. Repository-local PAI v5 release files for PAI facts only if needed.
4. Official OpenAI Codex docs only if S10C adds or refreshes a Codex capability claim.
5. Local `codex --version` or `codex --help` only if already available and non-invasive.

Do not use unofficial Codex capability sources. Do not infer current Codex behavior from memory.

## Source Material

Approved read-only sources used by S10C:

- `docs/adapters/V5_S10A_EXEC_PLAN.md`
- `docs/adapters/V5_S10B_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_FIXTURE_CORPUS_DESIGN_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_HARNESS_DESIGN_SPEC.md`
- `docs/adapters/V5_CODEX_INTEGRATED_READ_ONLY_FIXTURE_TRIAL_ARCHITECTURE.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_SEQUENCE_AND_GATE_MODEL.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_COVERAGE_MATRIX.md`
- `docs/adapters/V5_CODEX_TRIAL_FAILURE_ROLLBACK_AND_AUDIT_MODEL.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- Existing fixture corpus and harness files under `tests/adapters/v5-codex-readonly-fixture-trial/`

Repository release files remain read-only and were not inspected for live state.

## Completion Contract

This Completion Contract is the authoritative contract for V5-S10C. Before drafting the deliverables, copy this entire Completion Contract section into `docs/adapters/V5_S10C_EXEC_PLAN.md`. Do not mark S10C complete unless every requirement below is satisfied.

Strategic conclusions to preserve: Codex is not currently proven drop-in for existing local PAI v5 files; Codex replacement is plausible only through a designed adapter; S10C hardens fixture metadata and harness policy validation only; S10C does not implement a Codex runtime adapter; S10C does not create runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, trial outputs, manifest instances, audit artifacts, executable schemas, live-trial artifacts, or runtime payloads; S10C fixture metadata is not a manifest; S10C harness stdout is not an audit artifact; S10C self-test temporary data is not a fixture corpus, not a manifest, not an audit artifact, and not runtime payload; Claude-shaped files must not be copied directly into Codex surfaces; Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists; `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown; `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file; future Codex `AGENTS.md`, if later authorized, must be a compact router; Codex config/profile is policy/configuration, not Life OS doctrine; Codex hooks and rules are future native control surfaces, not Claude hook destinations; Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory; PAI Memory and ISA artifacts are canonical PAI state; product memories must not be silently promoted into PAI Memory; Pulse is central v5 infrastructure, but S10C does not start Pulse, call Pulse endpoints, or claim Pulse parity; S10C proves only fixture metadata semantics and harness policy validation, not Codex drop-in behavior; future read-only trials against live existing-local-v5 state remain unauthorized; future writes require a single-writer policy, provenance, rollback, validation, and conflict handling.

Required local discovery commands: run `git status --short`, file-existence checks for S10A/S10B plans and S9A/S10A design sources, existence checks for the harness, self-test, and fixture root, the original harness against the approved fixture corpus, and the S10B negative-control self-test before creating files. Do not inspect live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or user-local state. Do not start Pulse, call `localhost:31337`, run installers, invoke Claude Code, run Codex import or migration tooling, or run Codex hook/rule/execpolicy/runtime commands.

Required execution plan file: `docs/adapters/V5_S10C_EXEC_PLAN.md` must be created first and contain exactly the H1/H2 sequence used by this file. The execution plan must include the required milestones, a 100-point rubric with minimum score 94/100 and hard failures 0, and at least one scored iteration.

Required fixture metadata hardening: every fixture `fixture.json` must continue to include all S10A fields and add `covered_seams`, `coverage_ids`, `gate_ids`, `safety_assertions`, and `semantic_status`. `semantic_status` must be `s10c-semantically-hardened`. `covered_seams` must be a non-empty list using only the allowed seam names from the S10C prompt. `coverage_ids` must be non-empty `CVG-###` IDs from the S9A coverage model. `gate_ids` must be non-empty `TG-###` IDs from the S9A gate model. `safety_assertions` must contain all required boolean keys set to `true`: `fixture_only`, `read_only`, `no_live_user_local_state`, `no_existing_local_v5_access`, `no_root_agents_write`, `no_codex_surface_write`, `no_release_file_write`, `no_claude_file_direct_copy`, `no_codex_runtime_invocation`, `no_claude_code_invocation`, `no_pulse_start`, `no_pulse_endpoint_call`, `no_pai_memory_write`, `no_isa_write`, `no_product_memory_promotion`, `no_drop_in_claim`, `not_manifest`, `not_audit_artifact`, and `not_runtime_payload`. Every fixture must include denied-path coverage for live user-local state, root `AGENTS.md`, `.codex/`, `Releases/ write`, `PAI Memory write`, `ISA write`, `Pulse startup`, `Pulse endpoint call`, product memory promotion, Claude file direct-copy, runtime invocation, and drop-in claim. Every fixture must include unsupported-surface coverage through `expected_unsupported_surfaces`. Every `source_paths` entry must be repository-relative or use an approved synthetic marker prefix: `synthetic:`, `negative:`, or `unsupported:`. Source paths must not start with `/`, `~`, `.codex`, `.claude`, `PAI/`, `AGENTS.md`, or `CLAUDE.md`; must not contain `..`, `/home/`, or `/Users/`; and must use allowed repository-relative prefixes for release, docs, or fixture references.

Required harness update: update the existing harness so it validates all S10C semantic fields while preserving all S10A/S10B guarantees: standard library only, no subprocesses, no network, no writes, reads only the fixture root passed to it, stdout report only, no Pulse startup, no Pulse endpoint calls, no Claude Code invocation, no Codex runtime invocation, no user-local reads, no PAI Memory writes, and no ISA writes. The harness must fail on missing/empty/unknown semantic fields, malformed coverage or gate IDs, missing or false safety assertions, invalid semantic status, forbidden source path pattern, missing denied-path category, and missing unsupported-surface coverage. The harness report must include `S10C semantic validation`, `fixture_count`, `semantic_status`, and `status`.

Required self-test update: preserve `NC-001` through `NC-015` and add `NC-016` through `NC-030` covering missing `covered_seams`, unknown seam value, missing/malformed `coverage_ids`, missing/malformed `gate_ids`, missing/false `safety_assertions`, missing/invalid `semantic_status`, forbidden parent traversal, forbidden absolute source path, missing denied-path category, missing unsupported-surface coverage, and `.codex/` or root `AGENTS.md` source path. The self-test must keep `sys.dont_write_bytecode = True`, use temporary directories only, clean up automatically, leave no Python cache or temp artifacts in the repository, avoid subprocesses, network, release reads, user-local reads, Claude Code, Codex, Pulse startup, and Pulse endpoint calls, and emit stdout only. The self-test report must include `S10C harness semantic negative-control self-test report`, `positive_control_status`, `negative_control_count`, and `status`, with `negative_control_count` equal to `30`.

Required README update: add an S10C section explaining semantic fixture metadata, seam coverage, gate coverage, safety assertions, stronger source-path policy, negative controls `NC-001` through `NC-030`, read-only harness behavior, no Codex, no Claude Code, no Pulse startup or endpoint calls, no live user-local state, no PAI Memory or ISA writes, fixture metadata is not a manifest, harness stdout is not an audit artifact, and Codex is not currently proven drop-in for existing local PAI v5 files.

Protected paths and hard failures: do not modify protected paths; do not inspect private user-local state; do not modify fixture README files; do not add/remove/rename fixture directories; do not create runtime adapter files or prohibited Codex/runtime/state/trial artifacts; do not create committed negative fixtures, manifest instances, audit artifacts, schemas, live trials, private-state reads, PAI Memory writes, ISA writes, Pulse startup/calls/probes, installers, Claude Code invocation, Codex runtime/import/migration/hook/rule/execpolicy commands, non-stdlib harness or self-test dependencies, subprocesses, network access, harness writes, self-test repository writes outside approved files, Python cache/temp artifacts, prohibited drop-in/official-engine claims, PAI Memory or ISA write authorization, Pulse authorization, existing-local-v5 trial authorization, direct Claude-file copy authorization, product-memory promotion authorization, dual-engine uncoordinated write authorization, or advancement beyond S10C.

Required validation commands: run `git status --short`, `git diff --name-only | sort`, `git diff --check`, the original harness against the approved fixture corpus, the S10C negative-control self-test, changed-file check, execution-plan heading sequence check, fixture semantic metadata check, self-test source check, harness static safety check, no committed negative fixtures or generated artifacts check, content invariant check, and protected-path check.

Acceptance criteria: S10C is complete only if only approved files are created or modified, fixture READMEs are not modified, fixture directories are unchanged, no protected/prohibited files are changed or created, no committed negative fixtures or live trials exist, no private or live state is read, Memory/ISA/Pulse remain untouched, all semantic fields and checks pass, the original harness passes, the self-test passes and covers `NC-001` through `NC-030`, harness and self-test remain standard-library/no-subprocess/no-network/no-write safe, all required validation checks pass, deliverables make no prohibited claims or authorizations, the execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures, and final handoff reports every required validation command.

## Milestones

1. Baseline status check.
2. S10A/S10B reread.
3. Fixture semantic-field design.
4. Fixture metadata update.
5. Harness semantic validation update.
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
| Fixture semantic metadata quality                                             |     25 |
| Harness semantic validation quality                                           |     25 |
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
- Any protected file is modified.
- Runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, manifest instances, audit artifacts, executable schemas, live-trial artifacts, runtime payloads, or Pulse bridge files are created.
- Committed negative fixture directories or files are created.
- A live read-only trial is run.
- Private user-local state or live existing-local-v5 state is inspected or modified.
- PAI Memory or ISA is written.
- Pulse is started, Pulse endpoints are called, or `localhost:31337` is probed.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, or Codex hook/rule/execpolicy commands are run.
- The harness or self-test imports non-stdlib dependencies, runs subprocesses, uses network access, writes outside approved behavior, or leaves `__pycache__`, `.pyc`, or temporary artifacts in the repository.
- The docs, harness, self-test, or fixture metadata claim Codex is drop-in today or the official upstream engine.
- The docs, harness, self-test, or fixture metadata authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, Pulse implementation, existing-local-v5 trial execution, product-memory promotion into PAI Memory, or dual-engine uncoordinated writes.
- The docs, harness, self-test, or fixture metadata imply Claude-shaped files can be copied directly into Codex surfaces.
- The goal advances beyond S10C.

## Validation Commands

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Original harness:
  - `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures`
- S10C negative-control self-test:
  - `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`
- Changed-file check.
- Exact H1/H2 heading sequence check for this execution plan.
- Fixture semantic metadata check.
- Self-test source check.
- Harness static safety check.
- No committed negative fixtures or generated artifacts check.
- Content invariant check.
- Protected-path check.

## Progress

- Baseline status check: complete. Initial `git status --short` had no output.
- S10A/S10B reread: complete. Required S10A/S10B plans, S9A/S10A design docs, harness, self-test, and fixture root exist.
- Fixture semantic-field design: complete. The fields `covered_seams`, `coverage_ids`, `gate_ids`, `safety_assertions`, and `semantic_status` were mapped to S9A coverage and gate semantics.
- Fixture metadata update: complete. The 12 approved fixture metadata files were updated; fixture README files and fixture directories were not modified.
- Harness semantic validation update: complete. The harness now validates S10C semantic fields, source-path policy, denied-path categories, unsupported-surface coverage, and semantic report fields.
- Negative-control self-test update: complete. The self-test preserves `NC-001` through `NC-015` and adds `NC-016` through `NC-030`, with `negative_control_count: 30`.
- README update: complete. The harness README now documents S10C semantic hardening and safety boundaries.
- Positive and negative validation execution: complete. The positive harness passed and the S10C negative-control self-test passed.
- Protected-path and no-extra-file validation: complete. Changed-file scope, protected-path status, fixture directory checks, generated-artifact checks, and no committed negative fixture checks passed.
- Self-review and repair: complete. No hard failures were found; validation score is 100/100.
- Final handoff and goal-state report: pending final response.

## Iteration Log

| Iteration | Scope and protected-path discipline | Evidence discipline | Fixture semantic metadata quality | Harness semantic validation quality | Negative-control coverage quality | No-write, no-private-state, Pulse, Memory, ISA, and runtime-invocation safety | Verification quality | Score | Hard failures | Notes |
| --------- | ----------------------------------: | ------------------: | --------------------------------: | ----------------------------------: | --------------------------------: | --------------------------------------------------------------------------: | -------------------: | ----: | ------------: | ----- |
| 1 | 15/15 | 10/10 | 25/25 | 25/25 | 10/10 | 10/10 | 5/5 | 100/100 | 0 | S10C stayed within the approved write set, kept fixture READMEs and directories unchanged, added semantic metadata to all 12 fixtures, extended harness validation, and passed 30 negative controls. |

## Surprises & Discoveries

- The S10A/S10B harness structure was already suitable for import-based semantic testing; no runtime or subprocess execution was needed.
- The S10B temporary negative-control pattern extended cleanly to semantic policy cases without committed negative fixtures.
- The S10C semantic source-path policy required keeping release and adapter-doc references repository-relative while denying absolute, home, parent traversal, `.codex`, `.claude`, root `AGENTS.md`, root `CLAUDE.md`, and `PAI/` paths.

## Decision Log

- S10C will modify fixture metadata JSON only, not fixture README files or fixture directory structure.
- The harness and self-test will stay standard-library-only and continue to avoid subprocess, network, release-file reads, user-local reads, Codex invocation, Claude Code invocation, Pulse startup, and Pulse endpoint calls.
- The 12 fixture metadata files now use `semantic_status: s10c-semantically-hardened`.
- Every fixture uses S9A-style `CVG-###` coverage IDs and `TG-###` gate IDs.
- Every fixture includes S10C safety assertions requiring fixture-only, read-only, no live user-local state, no existing-local-v5 access, no root `AGENTS.md`, no `.codex/`, no release writes, no direct Claude-file copy, no Codex or Claude runtime invocation, no Pulse startup or endpoint calls, no PAI Memory writes, no ISA writes, no product-memory promotion, no drop-in claim, not a manifest, not an audit artifact, and not runtime payload.
- The self-test report was upgraded to `S10C harness semantic negative-control self-test report`.

## Outcomes & Retrospective

Validation results recorded for S10C:

- `git status --short`: passed; output listed only the approved S10C files.
- `git diff --name-only | sort`: passed; output listed the approved S10C execution plan, harness README, harness, self-test, and 12 approved fixture metadata files.
- `git diff --check`: passed.
- Original harness execution passed:
  - `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures`
- S10C negative-control self-test passed:
  - `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`
- Changed-file check: passed.
- Exact H1/H2 heading sequence check for this execution plan: passed.
- Fixture semantic metadata check: passed.
- Self-test source check: passed.
- Harness static safety check: passed.
- No committed negative fixtures or generated artifacts check: passed.
- Content invariant check: passed.
- Protected-path check: passed with no output.

No fixture README files were modified. No fixture directories were added, removed, or renamed. No protected files were changed. No runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, manifest instances, audit artifacts, executable schemas, live-trial artifacts, runtime payloads, Pulse bridge files, or committed negative fixtures were created.

S10C proves only fixture metadata semantics and harness policy validation. It does not prove Codex drop-in behavior, official upstream engine status, Pulse parity, existing-local-v5 trial readiness, Memory/ISA write safety, or runtime adapter correctness.
