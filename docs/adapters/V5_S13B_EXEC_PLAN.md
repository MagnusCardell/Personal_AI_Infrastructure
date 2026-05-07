# V5-S13B Execution Plan

## Purpose

Execute V5-S13B Clean-Clone Trial Negative Controls and Path-Safety Hardening as an adapter-test implementation milestone.

S13B proves the S13A clean-clone read-only runner is not a rubber stamp by adding negative controls for consent artifacts, source roots, read scopes, write prohibitions, output paths, runtime prohibitions, Pulse boundaries, PAI Memory boundaries, ISA boundaries, product-memory boundaries, and drop-in claim prevention.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement remains plausible only through a designed adapter and later replacement-grade validation.

## Scope

In scope:

- Create this execution plan first.
- Reread S13A clean-clone trial files and preserve the S13A positive path.
- Add a standard-library-only negative-control self-test for the S13A clean-clone runner.
- Harden the runner only where needed to make negative controls meaningful without weakening S13A guarantees.
- Update the S13A/S13B clean-clone README.
- Deterministically regenerate only the approved S13A preflight and evidence reports through the approved positive-control runner command.
- Run and record all required S13B validation commands.

Out of scope:

- Existing-local-v5 user-state trials.
- Personal-clone trials.
- Live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, arbitrary home-directory, or second personal clone reads.
- Codex runtime adapter implementation.
- Root `AGENTS.md`, `.codex/`, runtime files, runtime payloads, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, committed negative fixtures, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, and migration scripts.
- Pulse startup, Pulse endpoint calls, `localhost:31337` probes, Claude Code invocation, Codex runtime invocation, installers, and Codex import/migration/hook/rule/execpolicy commands.

## Approved Write Set

Create exactly these new files:

- `docs/adapters/V5_S13B_EXEC_PLAN.md`
- `tests/adapters/v5-codex-live-readonly-trial/test_clean_clone_readonly_trial.py`

Modify these existing files only if needed:

- `tests/adapters/v5-codex-live-readonly-trial/README.md`
- `tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py`

These existing S13A report files may be deterministically rewritten only by the approved positive-control runner command:

- `tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json`
- `tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json`

The S13A consent artifact must not be modified unless a defect is found that prevents the approved positive-control trial from passing. If it must be modified, stop and report before modifying it.

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
- Any second or personal clone outside this repository.

## Source Protocol

Allowed sources:

- S0-S13A adapter docs for prior adapter conclusions.
- Existing S10/S11 fixture and evidence files.
- Existing S13A clean-clone trial files.
- Repository-local PAI v5 release files for PAI facts.
- Official OpenAI Codex docs only if S13B adds or refreshes a Codex capability claim.
- Local `codex --version` or `codex --help` only if already available and non-invasive.

Forbidden sources and operations:

- Unofficial Codex capability sources.
- Inferred current Codex behavior from memory.
- Live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, arbitrary home directories, private user-local state, or any second/personal clone outside this repository.
- Live existing-local-v5 state.
- Pulse startup, Pulse endpoint calls, or `localhost:31337` probes.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, and Codex hook/rule/execpolicy commands.

## Source Material

Baseline discovery before S13B file creation:

- `git status --short`: no output.
- Required S13A execution plan and S13 proposal docs existed.
- S13A README, consent artifact, runner, preflight report, and evidence report existed.
- Existing fixture validation passed with `fixture_count: 12`, `case_count: 12`, `coverage_id_count: 25`, `gate_id_count: 20`, and `status: pass`.
- Existing harness negative-control self-test passed with `negative_control_count: 60`.
- Existing no-residue self-test passed with `repository_residue_status: pass`.
- S13A positive-control runner passed with `preflight_status: pass-read-only-clean-clone`, `report_status: pass`, `user_local_access_status: not-accessed`, `personal_clone_access_status: not-accessed`, `pulse_status: not-started-not-called`, `memory_status: no-pai-memory-writes`, `isa_status: no-isa-writes`, `product_memory_status: no-product-memory-read-or-promotion`, `runtime_invocation_status: no-codex-or-claude-runtime-invocation`, and `drop_in_claim_status: not-claimed`.

The S11 report-generator self-test was not run during S13B.

## Completion Contract

The authoritative V5-S13B Completion Contract is copied below as an indented block so this file preserves exactly the required H1/H2 heading structure.

    ## Completion Contract
    
    This Completion Contract is the authoritative contract for V5-S13B.
    
    Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S13B_EXEC_PLAN.md`.
    
    Do not mark S13B complete unless every requirement below is satisfied.
    
    ### Strategic conclusions to preserve
    
    The S13B deliverables must preserve these conclusions:
    
    * Codex is not currently proven drop-in for existing local PAI v5 files.
    * Codex replacement is plausible only through a designed adapter.
    * S13B validates clean-clone trial negative controls and path safety only.
    * S13B is not an existing-local-v5 trial.
    * S13B is not a personal-clone trial.
    * S13B does not inspect the user's second personal clone.
    * S13B does not inspect live `~/.claude/PAI`.
    * S13B does not inspect live `~/.claude/projects`.
    * S13B does not inspect live `~/.codex`.
    * S13B does not inspect arbitrary home directories.
    * S13B does not implement a Codex runtime adapter.
    * S13B does not create runtime adapter files.
    * S13B does not create root `AGENTS.md`.
    * S13B does not create `.codex/`.
    * S13B does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, runtime payloads, committed negative fixtures, or live-trial artifacts outside the approved S13B write set.
    * S13B does not modify release files.
    * S13B temporary negative-control data is not a fixture corpus, not a consent artifact for live use, not a manifest, not runtime payload, not PAI Memory, not ISA, not Pulse state, not Claude memory, and not Codex memory.
    * S13B clean-clone reports remain non-canonical adapter-test artifacts only.
    * S13B clean-clone reports are not PAI Memory.
    * S13B clean-clone reports are not ISA.
    * S13B clean-clone reports are not Pulse state.
    * S13B clean-clone reports are not Claude memory.
    * S13B clean-clone reports are not Codex memory.
    * S13B clean-clone reports are not manifests.
    * S13B clean-clone reports are not runtime payloads.
    * S13B clean-clone reports are not proof that Codex is drop-in.
    * Claude-shaped files must not be copied directly into Codex surfaces.
    * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
    * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
    * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
    * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
    * PAI Memory and ISA artifacts are canonical PAI state.
    * Product memories must not be silently promoted into PAI Memory.
    * Pulse is central v5 infrastructure, but S13B does not start Pulse, call Pulse endpoints, or claim Pulse parity.
    * S13B must not require uninstalling Claude Code.
    * S13B must not write PAI Memory or ISA.
    * S13B must not read product memories.
    * S13B must not promote product memories.
    * S13B must not claim Codex is official upstream.
    * S13B must not claim Codex is drop-in.
    
    ### Required local discovery commands
    
    Run these commands from repository root before creating or modifying files:
    
    ```bash
    git status --short
    
    test -f docs/adapters/V5_S13A_EXEC_PLAN.md
    test -f docs/adapters/V5_CODEX_S13_LIVE_READ_ONLY_TRIAL_GATES.md
    test -f docs/adapters/V5_CODEX_S13_PROPOSED_WRITE_SET_AND_COMPLETION_CONTRACT.md
    test -f docs/adapters/V5_CODEX_S13_RISK_REGISTER.md
    test -f tests/adapters/v5-codex-live-readonly-trial/README.md
    test -f tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json
    test -f tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py
    test -f tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json
    test -f tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json
    
    python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py \
      --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures
    
    PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py
    
    PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py
    
    python3 tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py \
      --consent tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json \
      --preflight-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json \
      --evidence-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json
    ```
    
    Do not run `test_readonly_fixture_trial_report_generator.py` during S13B because it may rewrite S11 report artifacts outside the S13B write set.
    
    Do not inspect live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or any user-local state.
    
    Do not inspect any second/personal clone.
    
    Do not start Pulse.
    
    Do not call `localhost:31337`.
    
    Do not run installers.
    
    Do not invoke Claude Code.
    
    Do not invoke Codex runtime.
    
    Do not run Codex import/migration tooling.
    
    Do not run Codex hook, rule, execpolicy, or runtime commands.
    
    ### Required file: `docs/adapters/V5_S13B_EXEC_PLAN.md`
    
    This file must be created first.
    
    It must contain exactly these H1/H2 headings:
    
    ```markdown
    # V5-S13B Execution Plan
    ## Purpose
    ## Scope
    ## Approved Write Set
    ## Protected Paths
    ## Source Protocol
    ## Source Material
    ## Completion Contract
    ## Milestones
    ## Self-Review Rubric
    ## Hard Failure Conditions
    ## Validation Commands
    ## Progress
    ## Iteration Log
    ## Surprises & Discoveries
    ## Decision Log
    ## Outcomes & Retrospective
    ```
    
    The `## Completion Contract` section must contain a verbatim copy of this Completion Contract.
    
    The execution plan must include milestones for baseline status check, S13A reread, S13A positive-control validation, runner importability and validation-surface review, negative-control self-test implementation, runner hardening only if required, README update, positive and negative validation execution, protected-path and no-extra-file validation, self-review and repair, and final handoff and goal-state report.
    
    The self-review rubric must total 100 points with a minimum score of 94/100 and zero hard failures.
    
    ### Required self-test file: `tests/adapters/v5-codex-live-readonly-trial/test_clean_clone_readonly_trial.py`
    
    Implement a Python 3 self-test script using only the Python standard library. The self-test must set `sys.dont_write_bytecode = True`, import the S13A runner in-process, use temporary directories only for negative-control data, automatically clean temporary directories, leave no `__pycache__`, `.pyc`, or temporary artifacts in the repository, not create committed negative fixtures, not use subprocesses, not use network access, not read release files outside the approved repository-local source policy, not read user-local state, not read `~/.claude`, not read `~/.codex`, not inspect the personal clone, not invoke Claude Code, not invoke Codex, not start Pulse, not call Pulse endpoints, not probe `localhost:31337`, emit a self-test report to stdout only, and exit with code `0` only when all positive and negative controls behave correctly.
    
    The self-test must verify the approved S13A clean-clone runner positive path passes.
    
    The self-test must generate temporary negative cases for `S13B-NC-001` through `S13B-NC-036`, covering missing and invalid consent artifacts, required consent fields, consent status and source kind, source root rejection, user-local and protected read roots, required forbidden read and write roots, runtime prohibitions, Memory, ISA, product-memory, drop-in claim, non-canonical statements, output path boundaries, missing clean-clone evidence, personal-clone-like source paths, runtime pressure, Pulse endpoint pressure, and canonical-state report attempts.
    
    For each negative case, the self-test report must include `negative_id`, `description`, `expected_failure_signal`, `observed_failure_signal`, and `status`. The self-test report must include `S13B clean-clone negative-control self-test report`, `positive_control_status`, `negative_control_count`, and `status`. The `negative_control_count` must be `36`.
    
    ### Required runner hardening
    
    Modify `run_clean_clone_readonly_trial.py` only if needed so the self-test can validate negative controls without weakening S13A guarantees. Any runner changes must preserve standard library only, no subprocesses, no network access, no user-local reads, no `~/.claude` reads, no `~/.codex` reads, no personal-clone access, no arbitrary home-directory scans, no Pulse startup, no Pulse endpoint calls, no `localhost:31337` probes, no Claude Code invocation, no Codex runtime invocation, no PAI Memory writes, no ISA writes, no release-file modifications, no root `AGENTS.md` modifications, no `.codex/` modifications, writes only to approved S13A preflight/evidence report paths during positive validation, and deterministic JSON output.
    
    ### Required README update
    
    Update `tests/adapters/v5-codex-live-readonly-trial/README.md` with an S13B section explaining that S13B adds clean-clone runner negative controls, negative controls are generated only in temporary directories, negative controls are not committed fixtures, S13B does not run Codex, S13B does not run Claude Code, S13B does not start Pulse, S13B does not call Pulse endpoints, S13B does not inspect live user-local state, S13B does not inspect the personal clone, S13B does not write PAI Memory or ISA, S13B does not read or promote product memories, S13B reports remain non-canonical adapter-test artifacts, and Codex is not currently proven drop-in for existing local PAI v5 files.
    
    ### Protected paths
    
    Do not modify protected paths including `Releases/`, `.claude/`, `PAI/`, `CLAUDE.md`, `AGENTS.md`, `.codex/`, `install.sh`, `PAI_SYSTEM_PROMPT.md`, `settings.json`, `hooks/`, `skills/`, `subagents/`, `agents/`, `commands/`, `.github/`, and `.agents/`. Do not inspect or modify private user-local state including `~/.claude/`, `~/.claude/PAI/`, `~/.claude/projects/`, `~/.codex/`, and `~/.codex/memories/`.
    
    ### Hard failure conditions
    
    S13B fails immediately if any file outside the approved write set is created or modified; the S13A consent artifact is modified without stopping for architect review; any S10/S11 fixture, harness, generator, evaluator, report, or README file is modified; any release file or protected file is modified; existing-local-v5 state, the user's second personal clone, live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, or arbitrary home-directory paths are inspected; PAI Memory or ISA is written; Pulse is started or called; `localhost:31337` is probed; Claude Code or Codex runtime is invoked; runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, runtime payloads, committed negative fixtures, or live-trial artifacts outside the approved write set are created; the self-test or runner imports non-stdlib dependencies, uses subprocesses, uses network access, writes inside the repository outside approved S13A/S13B paths, leaves `__pycache__`, `.pyc`, or temporary artifacts in the repository, or writes outside approved S13A report paths; any deliverable claims Codex is drop-in today or official upstream or authorizes prohibited writes, Pulse behavior, existing-local-v5 trial execution, personal-clone access, Claude file direct-copy, product-memory promotion, dual-engine uncoordinated writes, or work beyond S13B.
    
    ### Required validation commands
    
    Run `git status --short`, `git diff --name-only | sort`, `git diff --check`, fixture validation, fixture harness negative-control self-test, no-residue self-test, S13A positive-control runner, S13B negative-control self-test, changed-file check, execution-plan heading check, S13A report JSON validation, self-test source check, runner static safety check, content invariant check, no unexpected artifacts and no S10/S11 changes check, and protected-path check.
    
    ### Acceptance criteria
    
    S13B is complete only if only the approved S13B files are created or modified; the S13A consent artifact is not modified; no S10/S11 fixture, harness, generator, evaluator, report, or README file is modified; no release or protected file is modified; no existing-local-v5 state, personal clone, live user-local state, arbitrary home-directory path, PAI Memory write, ISA write, Pulse behavior, Claude Code invocation, Codex runtime invocation, runtime adapter file, root `AGENTS.md`, or `.codex/` occurs; the self-test uses only the Python standard library, no subprocesses, no network access, leaves no generated Python or temporary artifacts in the repository, covers all `S13B-NC-001` through `S13B-NC-036`, and reports `negative_control_count: 36`; the runner still uses only the Python standard library, no subprocesses, no network access, and writes only approved S13A preflight/evidence report paths during positive validation; the S13A positive-control runner command and S13B self-test pass; all required checks pass; this execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures; and final handoff reports every required validation command.
    
    ### Final handoff format
    
    End with exactly these headings: `## Files changed`, `## Behavior changed`, `## Tests run`, `## Known risks`, `## Protected files changed`, `## Goal state`, and `## Recommended next architect decision`.
    
    `Protected files changed` must be exactly `Yes` or `No`, followed by a brief explanation. Expected value: `No — only the approved S13B execution plan, clean-clone trial README, runner, self-test, and deterministically regenerated S13A reports were created or modified.`
    
    `Recommended next architect decision` must be advisory only. Do not begin S13C, S14, personal-clone access, existing-local-v5 trial execution, or runtime adapter work.
    
    ### Stop conditions
    
    Stop and report immediately if any protected file must be edited, any file outside the approved write set is modified, the S13A consent artifact would need to be modified, any S10/S11 fixture, harness, generator, evaluator, report, or README file would need to be modified, any release file would need to be modified, existing-local-v5 state or personal clone state would need to be read, live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, or arbitrary home-directory paths would need to be inspected, PAI Memory or ISA would need to be written, Pulse would need to be started or called, Claude Code or Codex runtime would need to be invoked, runtime implementation seems necessary, root `AGENTS.md` or `.codex/` would need to be modified, forbidden runtime/control artifacts outside the approved write set would need to be created, the runner or self-test would need non-stdlib dependencies, subprocesses, network access, or runner writes outside approved report paths, the goal tries to continue beyond S13B, the Completion Contract cannot be copied into the execution plan, or self-review cannot reach 94/100 without leaving scope.

## Milestones

1. Baseline status check.
2. S13A reread.
3. S13A positive-control validation.
4. Runner importability and validation-surface review.
5. Negative-control self-test implementation.
6. Runner hardening only if required.
7. README update.
8. Positive and negative validation execution.
9. Protected-path and no-extra-file validation.
10. Self-review and repair.
11. Final handoff and goal-state report.

## Self-Review Rubric

| Area | Points |
| --- | ---: |
| Scope and protected-path discipline | 15 |
| Evidence discipline | 10 |
| Positive-control preservation | 15 |
| Negative-control coverage quality | 30 |
| Runner path-safety and policy validation quality | 15 |
| No-live-user-state, no-Pulse, Memory, ISA, product-memory, runtime, and no-report-sprawl safety | 10 |
| Verification quality | 5 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

Hard failures for this execution:

- Any file outside the approved S13B write set is created or modified.
- The S13A consent artifact is modified without stopping for architect review.
- Any S10/S11 fixture, harness, generator, evaluator, report, or README file is modified.
- Any release file, protected file, root `AGENTS.md`, or `.codex/` file is modified.
- Existing-local-v5 state, user-local state, arbitrary home-directory state, live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, or a personal clone is inspected.
- PAI Memory or ISA is written.
- Pulse is started, Pulse endpoints are called, or `localhost:31337` is probed.
- Claude Code, Codex runtime, installers, import/migration tooling, hook/rule/execpolicy commands, or runtime adapter work are invoked.
- The runner or self-test imports non-stdlib dependencies, uses subprocesses, uses network access, or writes outside approved paths.
- The self-test leaves `__pycache__`, `.pyc`, temporary repository artifacts, committed negative fixtures, or live-trial artifacts outside the approved write set.
- Deliverables claim Codex is drop-in today or official upstream.
- Deliverables authorize prohibited writes, Pulse behavior, existing-local-v5 trial execution, personal-clone access, Claude file direct-copy, product-memory promotion, dual-engine uncoordinated writes, or work beyond S13B.
- The removed S11 report-generator self-test is run during S13B.
- Self-review cannot reach 94/100 with zero hard failures.

## Validation Commands

Discovery commands already run before S13B file creation:

```bash
git status --short
test -f docs/adapters/V5_S13A_EXEC_PLAN.md
test -f docs/adapters/V5_CODEX_S13_LIVE_READ_ONLY_TRIAL_GATES.md
test -f docs/adapters/V5_CODEX_S13_PROPOSED_WRITE_SET_AND_COMPLETION_CONTRACT.md
test -f docs/adapters/V5_CODEX_S13_RISK_REGISTER.md
test -f tests/adapters/v5-codex-live-readonly-trial/README.md
test -f tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json
test -f tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py
test -f tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json
test -f tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json
python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures
PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py
python3 tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py --consent tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json --preflight-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json --evidence-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json
```

Final validation commands to run after implementation:

```bash
git status --short
git diff --name-only | sort
git diff --check
python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures
PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py
python3 tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py --consent tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json --preflight-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json --evidence-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json
PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-live-readonly-trial/test_clean_clone_readonly_trial.py
```

Then run:

- Changed-file check.
- Execution-plan heading check.
- S13A report JSON validation.
- Self-test source check.
- Runner static safety check.
- Content invariant check.
- No unexpected artifacts and no S10/S11 changes check.
- Protected-path check.

## Progress

| Milestone | Status | Evidence |
| --- | --- | --- |
| 1. Baseline status check | Complete | `git status --short` had no output before S13B files. |
| 2. S13A reread | Complete | S13A runner, README, consent artifact, and reports were reviewed. |
| 3. S13A positive-control validation | Complete | Discovery positive-control runner passed. |
| 4. Runner importability and validation-surface review | Complete | Self-test imports the runner in-process with `sys.dont_write_bytecode = True`; static safety checks passed. |
| 5. Negative-control self-test implementation | Complete | `test_clean_clone_readonly_trial.py` covers `S13B-NC-001` through `S13B-NC-036` and reports `negative_control_count: 36`. |
| 6. Runner hardening only if required | Complete | Runner now validates allowed read roots before exact matching, source-root path safety before exact matching, and consent scope/reporting/retention/rollback policy fields. |
| 7. README update | Complete | README includes an S13B negative-controls section and preserves non-canonical, no-runtime, no-Pulse, no-Memory/ISA, and no-drop-in boundaries. |
| 8. Positive and negative validation execution | Complete | S13A positive-control runner passed; S13B negative-control self-test passed. |
| 9. Protected-path and no-extra-file validation | Complete | Changed-file, no unexpected artifacts/S10-S11 changes, and protected-path checks passed. |
| 10. Self-review and repair | Complete | Iteration 2 scored 99/100 with zero hard failures. |
| 11. Final handoff and goal-state report | Pending | Ready after final validation rerun and goal update. |

## Iteration Log

Iteration 1 initial self-review after execution plan creation:

| Area | Score | Notes |
| --- | ---: | --- |
| Scope and protected-path discipline | 15/15 | Only the approved execution plan created so far. |
| Evidence discipline | 10/10 | Discovery used repository-local S13A docs/files, S10/S11 fixture validation, and the S13A positive-control runner only. |
| Positive-control preservation | 15/15 | S13A positive-control runner passed before S13B edits. |
| Negative-control coverage quality | 0/30 | Self-test not yet implemented. |
| Runner path-safety and policy validation quality | 0/15 | Runner hardening review pending. |
| No-live-user-state, no-Pulse, Memory, ISA, product-memory, runtime, and no-report-sprawl safety | 10/10 | No forbidden reads, Pulse behavior, Memory/ISA writes, product memory reads, runtime commands, or report sprawl occurred. |
| Verification quality | 2/5 | Discovery passed; final validation pending. |
| Total | 52/100 | Below pass threshold because implementation remains pending. |

Hard failures: 0.

Iteration 2 final self-review after validation:

| Area | Score | Notes |
| --- | ---: | --- |
| Scope and protected-path discipline | 15/15 | Changed-file and no-unexpected-artifact checks passed; only approved S13B/S13A report paths are changed or allowed. |
| Evidence discipline | 10/10 | Evidence remains repository-local clean-clone adapter-test evidence only. |
| Positive-control preservation | 15/15 | S13A positive-control runner still passes after hardening. |
| Negative-control coverage quality | 30/30 | Self-test covers all `S13B-NC-001` through `S13B-NC-036` and reports `negative_control_count: 36`. |
| Runner path-safety and policy validation quality | 15/15 | Runner validates consent scope, read-root path safety, source-root path safety, output path boundaries, runtime prohibitions, Memory/ISA/product-memory/Pulse policies, drop-in prevention, and non-canonical statements. |
| No-live-user-state, no-Pulse, Memory, ISA, product-memory, runtime, and no-report-sprawl safety | 10/10 | No forbidden reads, Pulse behavior, Memory/ISA writes, product-memory reads, runtime commands, committed negative fixtures, or report sprawl occurred. |
| Verification quality | 4/5 | All required validation commands passed; the S11 report-generator self-test was intentionally not run per S13B contract. |
| Total | 99/100 | Pass threshold met. |

Hard failures: 0.

## Surprises & Discoveries

- The local sandbox may fail repository-local commands with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; when that occurs, required validation commands must be rerun with explicit escalation.
- The S11 report-generator self-test remains forbidden during S13B because it may rewrite S11 report artifacts outside the S13B write set.
- The S13A runner already failed closed for many negative controls; S13B hardening improved signal quality for allowed read roots, source roots, and consent policy fields.

## Decision Log

- S13B remains clean-clone negative-control and path-safety hardening only.
- S13B will not modify the S13A consent artifact.
- S13B will not create committed negative fixtures; negative cases must be temporary data only.
- S13B will not begin S13C, S14, personal-clone access, existing-local-v5 trial execution, or runtime adapter work.
- S13B clean-clone reports remain non-canonical adapter-test artifacts only.
- Runner hardening is limited to validation logic and does not add runtime adapter behavior.

## Outcomes & Retrospective

Final validation outcomes:

| Command or check | Result |
| --- | --- |
| `git status --short` | Passed; changed files were scoped to approved S13B paths and approved S13A runner/README paths. |
| `git diff --name-only | sort` | Passed; tracked diffs are `README.md` and `run_clean_clone_readonly_trial.py`. |
| `git diff --check` | Passed with no output. |
| `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures` | Passed with `status: pass`, `fixture_count: 12`, `case_count: 12`, `coverage_id_count: 25`, and `gate_id_count: 20`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py` | Passed with `positive_control_status: pass` and `negative_control_count: 60`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py` | Passed with `repository_residue_status: pass`. |
| `python3 tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py --consent tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json --preflight-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json --evidence-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json` | Passed with `preflight_status: pass-read-only-clean-clone`, `report_status: pass`, and no user-local or personal-clone access. |
| `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-live-readonly-trial/test_clean_clone_readonly_trial.py` | Passed with `positive_control_status: pass`, `negative_control_count: 36`, and `status: pass`. |
| Changed-file check | Passed with `changed files ok`. |
| Execution-plan heading check | Passed with `heading structure ok`. |
| S13A report JSON validation | Passed with `S13A report json ok`. |
| Self-test source check | Passed with `S13B self-test source ok`. |
| Runner static safety check | Passed with `runner static safety ok`. |
| Content invariant check | Passed with `S13B content invariants ok`. |
| No unexpected artifacts and no S10/S11 changes check | Passed with `no unexpected artifacts or S10/S11 changes ok`. |
| Protected-path check | Passed with no output. |

Outcome:

- S13B created the approved execution plan and self-test.
- S13B updated only the approved README and runner files.
- S13B did not modify the S13A consent artifact.
- S13B did not modify S10/S11 fixture, harness, generator, evaluator, report, or README files.
- S13B did not modify release files or protected paths.
- S13B negative-control data was temporary only and was not committed as fixtures.
- S13B did not inspect existing-local-v5 state, personal clone state, live user-local state, arbitrary home directories, live `~/.claude/PAI`, live `~/.claude/projects`, or live `~/.codex`.
- S13B did not start Pulse, call Pulse endpoints, probe `localhost:31337`, invoke Claude Code, invoke Codex runtime, run installers, run Codex import/migration/hook/rule/execpolicy commands, or implement runtime adapter work.
- S13B did not write PAI Memory, ISA, Pulse state, product memory, runtime payloads, or protected paths.
