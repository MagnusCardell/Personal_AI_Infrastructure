# V5-S10A Execution Plan

## Purpose

Create the first isolated fixture-only validation corpus and read-only harness for the PAI v5 Codex replacement-adapter effort.

S10A implements adapter-test fixtures and a read-only metadata harness only. It does not implement a Codex runtime adapter and does not create runtime adapter files.

## Scope

S10A is limited to the approved execution plan, fixture metadata files, fixture READMEs, harness README, and one read-only Python harness file.

S10A preserves the current conclusion that Codex is not currently proven drop-in for existing local PAI v5 files and that Codex replacement is plausible only through a designed adapter.

## Approved Write Set

- `docs/adapters/V5_S10A_EXEC_PLAN.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-001-release-baseline-static/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-001-release-baseline-static/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-002-authority-doctrine/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-002-authority-doctrine/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-003-compact-router-non-installation/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-003-compact-router-non-installation/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-004-launcher-inference-static/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-004-launcher-inference-static/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-005-hook-lifecycle-static/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-005-hook-lifecycle-static/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-006-pulse-static-no-start/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-006-pulse-static-no-start/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-007-memory-isa-static-no-write/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-007-memory-isa-static-no-write/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-008-denied-path-negative/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-008-denied-path-negative/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-009-product-memory-negative/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-009-product-memory-negative/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-010-unsupported-surface-reporting/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-010-unsupported-surface-reporting/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-011-rollback-no-residue/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-011-rollback-no-residue/fixture.json`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-012-dual-engine-boundary/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/FX-012-dual-engine-boundary/fixture.json`

No other files may be created or modified.

The `fixture.json` files are fixture metadata only. They are not manifest instances, not audit artifacts, not executable schemas, not Codex configuration, and not runtime payload.

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

1. S0-S9B adapter docs for prior adapter conclusions.
2. Repository-local PAI v5 release files for PAI facts.
3. Official OpenAI Codex docs only if S10A adds or refreshes a Codex capability claim.
4. Local `codex --version` or `codex --help` only if already available and non-invasive.

Do not use unofficial Codex capability sources. Do not infer current Codex behavior from memory.

## Source Material

Approved read-only sources:

- S0-S9B adapter docs under `docs/adapters/`.
- Repository-local release material under `Releases/v5.0.0/`.
- Repository-local Claude release material under `Releases/v5.0.0/.claude/`.

Discovery outputs are written only to `/tmp` and are not committed into the repository.

## Completion Contract

> This Completion Contract is the authoritative contract for V5-S10A.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S10A_EXEC_PLAN.md`.
>
> Do not mark S10A complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S10A deliverables must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S10A implements an isolated fixture corpus and read-only harness only.
> * S10A does not implement a Codex runtime adapter.
> * S10A does not create runtime adapter files.
> * S10A does not create root `AGENTS.md`.
> * S10A does not create `.codex/`.
> * S10A does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, trial outputs, manifest instances, audit artifacts, or executable schemas.
> * S10A fixture metadata is not a manifest.
> * S10A harness stdout is not an audit artifact.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
> * Codex config/profile is policy/configuration, not Life OS doctrine.
> * Codex hooks and rules are future native control surfaces, not Claude hook destinations.
> * Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Product memories must not be silently promoted into PAI Memory.
> * Pulse is central v5 infrastructure, but S10A does not start Pulse, call Pulse endpoints, or claim Pulse parity.
> * S10A fixture-only validation must not require uninstalling Claude Code.
> * S10A must prove only fixture metadata and harness boundaries, not Codex drop-in behavior.
> * Future read-only trials against live existing-local-v5 state remain unauthorized.
> * Future writes require a single-writer policy, provenance, rollback, validation, and conflict handling.
> * Controlled write mode must not exist until Memory, ISA, Pulse, authority, launcher/inference, hooks/lifecycle, rollback, audit, and fixture gates pass.
>
> ### Required local discovery commands
>
> Required discovery includes `git status --short`, existence checks for S9B/S9A source docs and release root, an approved `rg` search over `docs/adapters` and `Releases/v5.0.0`, and printing `/tmp/v5-s10a-fixture-harness-search.txt`. Do not write that temporary file into the repository.
>
> ### Required file: `docs/adapters/V5_S10A_EXEC_PLAN.md`
>
> This file must be created first and contain exactly the H1/H2 heading sequence in this execution plan.
>
> ### Required fixture corpus
>
> Create exactly 12 fixture directories under `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/`. Each fixture directory must contain exactly `README.md` and `fixture.json`. The fixture IDs and directories must be exactly `FX-001-release-baseline-static`, `FX-002-authority-doctrine`, `FX-003-compact-router-non-installation`, `FX-004-launcher-inference-static`, `FX-005-hook-lifecycle-static`, `FX-006-pulse-static-no-start`, `FX-007-memory-isa-static-no-write`, `FX-008-denied-path-negative`, `FX-009-product-memory-negative`, `FX-010-unsupported-surface-reporting`, `FX-011-rollback-no-residue`, and `FX-012-dual-engine-boundary`.
>
> ### Required fixture metadata fields
>
> Every `fixture.json` must include `fixture_id`, `fixture_name`, `fixture_source_class`, `pai_version`, `source_paths`, `included_surfaces`, `excluded_surfaces`, `denied_paths`, `expected_denials`, `expected_unsupported_surfaces`, `expected_no_write_proofs`, `expected_audit_fields`, `rollback_expectation`, `privacy_status`, and `s10a_status`. The allowed fixture source classes are `release-derived-fixture`, `synthetic-fixture`, `negative-safety-fixture`, and `unsupported-surface-fixture`. Do not use `sanitized-user-fixture` in S10A. Do not use live existing-local-v5 state as a fixture source. Every fixture must set `s10a_status` to `implemented-fixture-metadata-only`, include all required no-write proof keys, and include all required expected audit field names.
>
> ### Required harness file
>
> Implement a small Python 3 harness using only the Python standard library at `tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py`. The harness must read fixture metadata from the approved fixture root, validate the 12 fixtures, validate metadata fields and safety posture, emit a validation report to stdout only, exit `0` when all checks pass, and exit non-zero when any check fails. It must not write files, create reports on disk, create audit artifacts, create manifests, create schemas, modify fixtures, read release files, read user-local state, start Pulse, call Pulse endpoints, probe `localhost:31337`, invoke Claude Code, invoke Codex, run subprocesses, use network access, or import non-stdlib packages.
>
> ### Required README file
>
> `tests/adapters/v5-codex-readonly-fixture-trial/README.md` must explain S10A is fixture-only, the harness is read-only, the harness validates fixture metadata and safety posture only, the harness does not run Codex or Claude Code, the harness does not start Pulse, the harness does not inspect live user-local state, the harness does not write PAI Memory or ISA, fixture metadata is not a manifest, harness stdout is not an audit artifact, and Codex is not currently proven drop-in for existing local PAI v5 files.
>
> ### Protected paths
>
> Do not modify protected repository paths or inspect private user-local state.
>
> ### Hard failure conditions
>
> S10A fails immediately if any file outside the approved write set is created or modified, any protected file is modified, runtime adapter files or prohibited runtime/config/payload files are created, fixture directories contain files other than `README.md` and `fixture.json`, manifest instances, audit artifacts, schemas, runtime harnesses, or live trials are created or run, private or live existing-local-v5 state is read, PAI Memory or ISA is written, Pulse is started or called, installers, Claude Code, Codex runtime, import/migration tooling, or hook/rule/execpolicy commands are run, the harness imports non-stdlib dependencies, runs subprocesses, uses network access, or writes files, prohibited readiness claims are made, or the goal advances beyond S10A.
>
> ### Required validation commands
>
> Required validation includes `git status --short`, `git diff --name-only | sort`, `git diff --check`, harness execution, changed-file check, exact H1/H2 heading sequence check, fixture corpus metadata check, harness static safety check, content invariant check, no forbidden generated artifact check, and protected-path check.
>
> ### Acceptance criteria
>
> S10A is complete only if exactly the approved S10A files are created or modified, no protected files are changed, no prohibited runtime or state artifacts are created, the fixture corpus contains exactly 12 fixture directories with exactly `README.md` and `fixture.json`, the read-only standard-library harness passes and emits stdout only, no private or live state is read, no Pulse/Memory/ISA writes or calls occur, all validation checks pass, the deliverables make no prohibited claims or authorizations, the execution plan records a scored self-review of at least 94/100 with zero hard failures, and final handoff reports every required validation command.

## Milestones

1. Baseline status check.
2. S0-S9B reread.
3. Fixture corpus implementation.
4. Harness implementation.
5. Harness README implementation.
6. Fixture metadata validation.
7. Harness execution validation.
8. Protected-path and no-extra-file validation.
9. Self-review and repair.
10. Final handoff and goal-state report.

## Self-Review Rubric

| Area                                                                                     | Points |
| ---------------------------------------------------------------------------------------- | -----: |
| Scope and protected-path discipline                                                      |     15 |
| Evidence discipline                                                                      |     10 |
| Fixture corpus completeness                                                              |     20 |
| Fixture metadata quality                                                                 |     15 |
| Read-only harness quality                                                                |     20 |
| No-write, no-private-state, Pulse, Memory, ISA, rollback, and unsupported-surface safety |     15 |
| Verification quality                                                                     |      5 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

- Any file outside the approved write set is created or modified.
- Any protected file is modified.
- Runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, manifest instances, audit artifacts, executable schemas, or Pulse bridge files are created.
- Any fixture directory contains files other than `README.md` and `fixture.json`.
- A live read-only trial is run.
- Private user-local state or live existing-local-v5 state is inspected or modified.
- PAI Memory or ISA is written.
- Pulse is started, Pulse endpoints are called, or `localhost:31337` is probed.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, or Codex hook/rule/execpolicy commands are run.
- The harness imports non-stdlib dependencies, runs subprocesses, uses network access, or writes files.
- The docs or harness claim Codex is drop-in today or the official upstream engine.
- The docs or harness authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, Pulse implementation, existing-local-v5 trial execution, product-memory promotion into PAI Memory, or dual-engine uncoordinated writes.
- The docs or harness imply Claude-shaped files can be copied directly into Codex surfaces.
- The goal advances beyond S10A.

## Validation Commands

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Harness execution:
  - `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures`
- Changed-file check.
- Exact H1/H2 heading sequence check for this execution plan.
- Fixture corpus metadata check.
- Harness static safety check.
- Content invariant check.
- No forbidden runtime-surface files check.
- Protected-path check.

## Progress

- Baseline status check: complete. The initial `git status --short` before S10A file creation was clean; after execution-plan creation, status showed only the approved S10A execution plan.
- S0-S9B reread: complete. Required file-existence checks passed and the required `rg` discovery ran over `docs/adapters` and `Releases/v5.0.0`, with output kept in `/tmp/v5-s10a-fixture-harness-search.txt`.
- Fixture corpus implementation: complete. Exactly 12 approved fixture directories were created under `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/`.
- Harness implementation: complete. The read-only standard-library harness was created at the approved path and validates fixture metadata only.
- Harness README implementation: complete. The README states fixture-only scope, read-only behavior, no Codex/Claude/Pulse runtime action, no live user-local state, no PAI Memory or ISA writes, and no drop-in claim.
- Fixture metadata validation: complete. All 12 `fixture.json` files include the required fields, allowed source classes, allowed privacy values, required no-write proof keys, required audit field names, denied paths, and S10A metadata-only status.
- Harness execution validation: complete. The harness passed against the approved fixture root and emitted stdout only.
- Protected-path and no-extra-file validation: complete. Protected-path status produced no output, changed-file scope matched the approved write set, and the generated-artifact scan passed.
- Self-review and repair: complete. One whitespace repair removed trailing blank lines; final self-review scored 99/100 with zero hard failures.
- Final handoff and goal-state report: pending final response.

## Iteration Log

| Iteration | Scope and protected-path discipline | Evidence discipline | Fixture corpus completeness | Fixture metadata quality | Read-only harness quality | No-write, no-private-state, Pulse, Memory, ISA, rollback, and unsupported-surface safety | Verification quality | Score | Hard failures | Notes |
| --------- | ----------------------------------: | ------------------: | --------------------------: | -----------------------: | ------------------------: | -------------------------------------------------------------------------------------: | -------------------: | ----: | ------------: | ----- |
| 1 | 15/15 | 10/10 | 20/20 | 15/15 | 19/20 | 15/15 | 5/5 | 99/100 | 0 | Scope stayed within the approved S10A files. Fixture metadata and the harness passed validation. One point reserved because S10A proves metadata/harness boundaries only, not any future adapter behavior. |

## Surprises & Discoveries

- The repository-local discovery reiterated the S9A/S9B safety posture: S10A should stay fixture-only, avoid live existing-local-v5 state, avoid root `AGENTS.md` and `.codex/`, avoid Pulse startup and endpoint calls, and avoid PAI Memory or ISA writes.
- `git diff --check` initially reported trailing blank lines at EOF in the newly added approved files. A mechanical cleanup removed those whitespace defects before final validation.
- Running the harness did not create `__pycache__` or other generated artifacts.

## Decision Log

- S10A goal started after the S9B goal was completed.
- Execution plan created before the fixture corpus, harness README, and harness file.
- Fixture metadata stays metadata-only and is not a manifest instance, audit artifact, executable schema, Codex config, hook, rule, runtime file, or adapter payload.
- Harness stdout stays validation output only and is not an audit artifact or trial output.
- Fixture source paths use repository-relative release/docs paths or synthetic design references only; no live user-local paths are used.
- The harness reads only the supplied fixture root, uses only Python standard library modules, runs no subprocesses, performs no network access, writes no files, and invokes neither Codex nor Claude Code.
- S10A does not prove Codex drop-in behavior, Pulse parity, PAI Memory write safety, ISA write safety, or existing-local-v5 trial readiness.

## Outcomes & Retrospective

Validation results recorded for S10A:

- `git status --short`: passed; output listed only the approved S10A intent-to-add files.
- `git diff --name-only | sort`: passed; output listed the approved S10A execution plan, harness README, read-only harness, and 12 fixture README/metadata pairs.
- `git diff --check`: passed after trailing blank-line cleanup.
- Harness execution passed:
  - `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures`
- Changed-file check: passed.
- Exact H1/H2 heading sequence check for this execution plan: passed.
- Fixture corpus metadata check: passed.
- Harness static safety check: passed.
- Content invariant check: passed.
- No forbidden runtime-surface files check: passed.
- Protected-path check: passed with no output.

No protected files were changed. No root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, trial outputs, manifest instances, audit artifacts, executable schemas, or runtime adapter files were created.

S10A remains limited to fixture metadata, fixture READMEs, a harness README, and a read-only fixture metadata harness. The deliverables do not claim Codex is drop-in today, do not claim Codex is the official upstream engine, do not authorize PAI Memory writes, do not authorize ISA writes, do not authorize Pulse startup or endpoint calls, do not authorize existing-local-v5 trial execution, and do not authorize product-memory promotion into PAI Memory.
