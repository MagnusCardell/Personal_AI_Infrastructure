# V5-S12A Execution Plan

## Purpose

Execute V5-S12A Live Read-Only Consent, Source Selection, and PAI_DIR Detection Design. S12A defines the documentation/design model required before any future live existing-local-v5 read-only trial can be considered.

Codex is not currently proven drop-in for existing local PAI v5 files. S12A is documentation/design only; it does not run a live read-only trial, read live existing-local-v5 state, or implement a runtime adapter.

## Scope

In scope:

- Create this S12A execution plan.
- Create the live read-only consent model.
- Create the PAI_DIR detection and source selection spec.
- Create the live read-only preflight and abort model.
- Create the live read-only reporting boundary spec.
- Create the S12A decision log.
- Run and record all required validation commands.

Out of scope:

- Live read-only trials or live existing-local-v5 access.
- Runtime adapter implementation.
- Fixture, harness, generator, evaluator, report, README, or release file edits.
- Root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures.

## Approved Write Set

Create exactly these files:

- `docs/adapters/V5_S12A_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_LIVE_READ_ONLY_CONSENT_MODEL.md`
- `docs/adapters/V5_CODEX_PAI_DIR_DETECTION_AND_SOURCE_SELECTION_SPEC.md`
- `docs/adapters/V5_CODEX_LIVE_READ_ONLY_PREFLIGHT_AND_ABORT_MODEL.md`
- `docs/adapters/V5_CODEX_LIVE_READ_ONLY_REPORTING_BOUNDARY_SPEC.md`
- `docs/adapters/V5_CODEX_S12A_DECISION_LOG.md`

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

Allowed sources:

- S0-S11D adapter docs for prior adapter conclusions.
- Existing S10/S11 fixture and evidence files.
- Repository-local PAI v5 release files for PAI facts only if needed.
- Official OpenAI Codex docs only if S12A adds or refreshes a Codex capability claim.
- Local `codex --version` or `codex --help` only if already available and non-invasive.

Forbidden sources and operations:

- Unofficial Codex capability sources.
- Inferred current Codex behavior from memory.
- Live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, or other private user-local state.
- Live existing-local-v5 state.
- Pulse startup, Pulse endpoint calls, or `localhost:31337` probes.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, and Codex hook/rule/execpolicy commands.

## Source Material

Baseline discovery before S12A edits:

- `git status --short`: no output.
- Required S11D closeout docs and S11 reports existed.
- Existing harness validation passed with `fixture_count: 12`, `case_count: 12`, `coverage_id_count: 25`, `gate_id_count: 20`, and `status: pass`.
- Existing harness negative-control self-test passed with `negative_control_count: 60`.
- Existing no-residue self-test passed.
- Existing report-generator negative-control self-test passed with `negative_control_count: 16`.
- S11D closeout documents preserved that S12 is proposed only, live reads remain future-only, explicit user consent design is required, and Codex is not currently proven drop-in for existing local PAI v5 files.

## Completion Contract

The S12A Completion Contract is copied below in quoted form to preserve the required execution-plan H1/H2 sequence while retaining the contract text.

> ## Completion Contract
>
> This Completion Contract is the authoritative contract for V5-S12A.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S12A_EXEC_PLAN.md`.
>
> Do not mark S12A complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S12A deliverables must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S12A designs consent, source selection, PAI_DIR detection, preflight, abort, and reporting boundaries only.
> * S12A does not run a live read-only trial.
> * S12A does not read live existing-local-v5 state.
> * S12A does not read live user-local state.
> * S12A does not implement a Codex runtime adapter.
> * S12A does not create runtime adapter files.
> * S12A does not create root `AGENTS.md`.
> * S12A does not create `.codex/`.
> * S12A does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures.
> * S12A reporting output is future design only and is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a PAI runtime audit artifact, not a manifest, and not runtime payload.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Product memories must not be silently promoted into PAI Memory.
> * Pulse is central v5 infrastructure, but S12A does not start Pulse, call Pulse endpoints, or claim Pulse parity.
> * Future live read-only access requires explicit user consent design and architect approval.
> * Future live read-only access must not require uninstalling Claude Code.
> * Future live read-only access must not write PAI Memory or ISA.
> * Future live read-only access must not start Pulse or call Pulse endpoints unless separately approved.
> * Future writes require a single-writer policy, provenance, rollback, validation, and conflict handling.
>
> ### Required local discovery commands
>
> Run these commands from repository root before creating files:
>
> ```bash
> git status --short
>
> test -f docs/adapters/V5_CODEX_S11_EVIDENCE_CLOSEOUT_REPORT.md
> test -f docs/adapters/V5_CODEX_S12_LIVE_READ_ONLY_TRIAL_READINESS_GATES.md
> test -f docs/adapters/V5_CODEX_S12_PROPOSED_WRITE_SET_AND_COMPLETION_CONTRACT.md
> test -f docs/adapters/V5_CODEX_S11_TO_S12_DECISION_LOG.md
> test -f tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json
> test -f tests/adapters/v5-codex-readonly-fixture-trial/reports/S11C_READINESS_GATE_EVALUATION.json
>
> python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py \
>   --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures
>
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py
>
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py
>
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_report_generator.py
> ```
>
> Do not inspect live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or any user-local state.
>
> Do not start Pulse.
>
> Do not call `localhost:31337`.
>
> Do not run installers.
>
> Do not invoke Claude Code.
>
> Do not run Codex import/migration tooling.
>
> Do not run Codex hook, rule, execpolicy, or runtime commands.
>
> ### Required file: `docs/adapters/V5_S12A_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S12A Execution Plan
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
> The execution plan must include these milestones:
>
> 1. Baseline status check.
> 2. S10/S11 closeout reread.
> 3. Consent model drafting.
> 4. PAI_DIR detection and source selection spec drafting.
> 5. Preflight and abort model drafting.
> 6. Reporting boundary spec drafting.
> 7. Decision log drafting.
> 8. Protected-path and no-extra-file validation.
> 9. Self-review and repair.
> 10. Final handoff and goal-state report.
>
> The self-review rubric must total 100 points:
>
> | Area                                                        | Points |
> | ----------------------------------------------------------- | -----: |
> | Scope and protected-path discipline                         |     15 |
> | Evidence discipline                                         |     10 |
> | Consent model quality                                       |     20 |
> | PAI_DIR detection and source selection quality              |     20 |
> | Preflight, abort, and reporting boundary quality            |     20 |
> | Memory, ISA, Pulse, product-memory, and no-live-read safety |     10 |
> | Verification quality                                        |      5 |
>
> Pass threshold:
>
> ```text
> Minimum score: 94/100
> Hard failures: 0
> ```
>
> Record at least one scored iteration in `## Iteration Log`.
>
> ### Required file: `docs/adapters/V5_CODEX_LIVE_READ_ONLY_CONSENT_MODEL.md`
>
> Purpose: define the future explicit user consent model required before any live local PAI v5 read-only trial.
>
> It must contain exactly the required consent model headings and state that S12A does not collect user consent. Future consent must be explicit, bounded, revocable, and source-specific. It must not be inferred from having Claude Code installed, Codex installed, or both subscriptions. Future consent must separately identify source root, allowed read scope, forbidden read scope, forbidden writes, reporting output, retention policy, and rollback/no-residue expectation. Consent does not authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory reads, product-memory promotion, root `AGENTS.md`, or `.codex/`. S12A creates no consent artifact.
>
> ### Required file: `docs/adapters/V5_CODEX_PAI_DIR_DETECTION_AND_SOURCE_SELECTION_SPEC.md`
>
> Purpose: define future read-only PAI_DIR detection and source-selection behavior without reading live local state in S12A.
>
> It must contain exactly the required PAI_DIR detection and source selection headings. It must state that S12A does not detect live `PAI_DIR`; that `PAI_DIR` means the PAI subsystem root, usually `~/.claude/PAI`, but S12A does not inspect it; define `release-fixture`, `sanitized-user-fixture`, and `existing-local-v5-read-only`; state that `existing-local-v5-read-only` is future-only and requires explicit consent plus architect approval; define future detection as read-only, path-bounded, and abortable; state no default live local read; no scanning arbitrary home directories; no reading `~/.claude/projects/**/memory`; no reading `~/.codex/memories`; no reading product memories by default; and no writing discovered paths into PAI Memory, ISA, Pulse, Claude memory, or Codex memory.
>
> ### Required file: `docs/adapters/V5_CODEX_LIVE_READ_ONLY_PREFLIGHT_AND_ABORT_MODEL.md`
>
> Purpose: define future preflight checks and abort conditions before any live local PAI v5 read-only trial can run.
>
> It must contain exactly the required preflight and abort headings. It must state that S12A runs no preflight against live local state. It must define future preflight checks for explicit consent present, source root matches consent, no root `AGENTS.md`, no `.codex/`, no write mode, no Pulse startup, no Pulse endpoint calls, no PAI Memory writes, no ISA writes, no product-memory reads by default, no Codex runtime adapter execution, no Claude Code invocation, and no installer execution. It must define abort conditions for missing consent, ambiguous source root, unexpected private state, any write requirement, Pulse startup requirement, Pulse call requirement, Memory/ISA write requirement, product-memory access requirement, runtime adapter requirement, and drop-in claim pressure. It must define abort report as future advisory-only output, not PAI Memory, ISA, Pulse state, manifest, audit artifact, or runtime payload.
>
> ### Required file: `docs/adapters/V5_CODEX_LIVE_READ_ONLY_REPORTING_BOUNDARY_SPEC.md`
>
> Purpose: define future live-read-only reporting boundaries and non-canonical output rules.
>
> It must contain exactly the required reporting boundary headings. It must state that S12A creates no live-read report; define future report types `consent-preflight-report`, `source-selection-report`, `live-read-only-preflight-report`, `abort-report`, and `live-read-only-evidence-report`; state every future report is non-canonical unless separately approved; state future reports are not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not manifest, and not runtime payload; state reports must not be promoted into PAI Memory by default; and define the required future fields listed by the S12A card.
>
> ### Required file: `docs/adapters/V5_CODEX_S12A_DECISION_LOG.md`
>
> Purpose: record S12A decisions, non-decisions, blocked decisions, and future architect questions.
>
> It must contain exactly the required decision-log headings. It must include a decision table with columns `Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger`. It must include decisions `S12A-D01` through `S12A-D16`. The Next Milestone Candidates section must list advisory-only options for `V5-S12B`, `V5-S12C`, `V5-S12D`, `V5-S13A`, and `V5-S13B`, and state that architect approval is required before any future milestone.
>
> ### Protected paths
>
> Do not modify `Releases/`, `Releases/v5.0.0/`, `Releases/v5.0.0/.claude/`, `.claude/`, `PAI/`, `CLAUDE.md`, `AGENTS.md`, `.codex/`, `install.sh`, `PAI_SYSTEM_PROMPT.md`, `settings.json`, `hooks/`, `skills/`, `subagents/`, `agents/`, `commands/`, `.github/`, or `.agents/`.
>
> Do not inspect or modify private user-local state: `~/.claude/`, `~/.claude/PAI/`, `~/.claude/projects/`, `~/.codex/`, or `~/.codex/memories/`.
>
> ### Hard failure conditions
>
> S12A fails immediately if any file outside the approved write set is created or modified; any fixture, harness, generator, evaluator, report, README, or release file is modified; any protected file is modified; runtime adapter files are created; root `AGENTS.md` or `.codex/` is created or modified; Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures are created; a live read-only trial is run; private user-local state is inspected or modified; live existing-local-v5 state is read; `~/.claude/PAI`, `~/.claude/projects`, or `~/.codex` is inspected; PAI Memory is written; ISA is written; Pulse is started; Pulse endpoints are called; `localhost:31337` is probed; installers are run; Claude Code is invoked; Codex is invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available; Codex import or migration tooling is run; Codex hook, rule, or execpolicy commands are run; the docs claim Codex is drop-in today or the official upstream engine; the docs authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, Pulse implementation, existing-local-v5 trial execution, product-memory promotion into PAI Memory, or dual-engine uncoordinated writes; the docs imply Claude-shaped files can be copied directly into Codex surfaces; or the goal advances beyond S12A.
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
> Run changed-file check, heading check, content invariant check, protected-path and no-test-change checks exactly as specified by the S12A card.
>
> ### Acceptance criteria
>
> S12A is complete only if exactly the six approved S12A docs are created or modified; no fixture, harness, generator, evaluator, report, README, release, protected, or runtime file is modified; no root `AGENTS.md` or `.codex/` is created or modified; no runtime, adapter, manifest, schema, audit, live-trial, Memory, ISA, Pulse, or committed negative fixture artifact is created; no live read-only trial is run; no private user-local state or live existing-local-v5 state is read; PAI Memory and ISA are not written; Pulse is not started or called; `localhost:31337` is not probed; installers, Claude Code, Codex runtime, Codex import/migration tooling, and Codex hook/rule/execpolicy commands are not run; the execution plan contains the Completion Contract; the consent model states consent is not inferred from Claude Code installation, Codex installation, or dual subscriptions; the PAI_DIR spec states S12A does not detect live `PAI_DIR`; the preflight model states S12A runs no live preflight; the reporting boundary spec states S12A creates no live-read report; the decision log includes `S12A-D01` through `S12A-D16`; changed-file, heading, content invariant, no-test-change, and protected-path checks pass; and the execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures.
>
> ### Final handoff format
>
> End with exactly these headings:
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
> `Protected files changed` must be exactly `Yes` or `No`, followed by a brief explanation.
>
> Expected value:
>
> ```text
> No — only the six approved S12A documentation files were created or modified.
> ```
>
> `Recommended next architect decision` must be advisory only. Do not begin S12B, S12C, S12D, S13A, or runtime adapter work.
>
> ### Stop conditions
>
> Stop and report immediately if any protected file must be edited; any file outside the approved write set is modified; any test fixture, harness, generator, evaluator, report, README, or release file would need to be modified; runtime implementation seems necessary; root `AGENTS.md` or `.codex/` would need to be modified; any Codex config, hook, rule, skill, subagent, agent, command, launcher, installer, wrapper, generated runtime config, migration script, adapter payload, Memory payload, ISA payload, Pulse payload, Pulse bridge file, manifest instance, executable schema, live-trial artifact, runtime payload, or committed negative fixture would need to be created; a live trial would need to be run; PAI Memory or ISA would need to be written; existing-local-v5 state, `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or private user-local memory would need to be read; Pulse would need to be started; a Pulse endpoint or `localhost:31337` would need to be probed; upstream v5 would need to be patched; Codex import/migration tooling, Claude Code, Codex runtime engine, or Codex hook/rule/execpolicy commands would need to be run; the goal tries to continue beyond S12A; the Completion Contract cannot be copied into the execution plan; or self-review cannot reach 94/100 without leaving scope.

Unabridged contract source retained for audit:

> ## Completion Contract
>
> This Completion Contract is the authoritative contract for V5-S12A.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S12A_EXEC_PLAN.md`.
>
> Do not mark S12A complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S12A deliverables must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S12A designs consent, source selection, PAI_DIR detection, preflight, abort, and reporting boundaries only.
> * S12A does not run a live read-only trial.
> * S12A does not read live existing-local-v5 state.
> * S12A does not read live user-local state.
> * S12A does not implement a Codex runtime adapter.
> * S12A does not create runtime adapter files.
> * S12A does not create root `AGENTS.md`.
> * S12A does not create `.codex/`.
> * S12A does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures.
> * S12A reporting output is future design only and is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a PAI runtime audit artifact, not a manifest, and not runtime payload.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Product memories must not be silently promoted into PAI Memory.
> * Pulse is central v5 infrastructure, but S12A does not start Pulse, call Pulse endpoints, or claim Pulse parity.
> * Future live read-only access requires explicit user consent design and architect approval.
> * Future live read-only access must not require uninstalling Claude Code.
> * Future live read-only access must not write PAI Memory or ISA.
> * Future live read-only access must not start Pulse or call Pulse endpoints unless separately approved.
> * Future writes require a single-writer policy, provenance, rollback, validation, and conflict handling.
>
> ### Required local discovery commands
>
> Run these commands from repository root before creating files:
>
> ```bash
> git status --short
>
> test -f docs/adapters/V5_CODEX_S11_EVIDENCE_CLOSEOUT_REPORT.md
> test -f docs/adapters/V5_CODEX_S12_LIVE_READ_ONLY_TRIAL_READINESS_GATES.md
> test -f docs/adapters/V5_CODEX_S12_PROPOSED_WRITE_SET_AND_COMPLETION_CONTRACT.md
> test -f docs/adapters/V5_CODEX_S11_TO_S12_DECISION_LOG.md
> test -f tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json
> test -f tests/adapters/v5-codex-readonly-fixture-trial/reports/S11C_READINESS_GATE_EVALUATION.json
>
> python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py \
>   --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures
>
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py
>
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py
>
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_report_generator.py
> ```
>
> Do not inspect live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or any user-local state.
>
> Do not start Pulse.
>
> Do not call `localhost:31337`.
>
> Do not run installers.
>
> Do not invoke Claude Code.
>
> Do not run Codex import/migration tooling.
>
> Do not run Codex hook, rule, execpolicy, or runtime commands.
>
> ### Required file: `docs/adapters/V5_S12A_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S12A Execution Plan
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
> The execution plan must include these milestones:
>
> 1. Baseline status check.
> 2. S10/S11 closeout reread.
> 3. Consent model drafting.
> 4. PAI_DIR detection and source selection spec drafting.
> 5. Preflight and abort model drafting.
> 6. Reporting boundary spec drafting.
> 7. Decision log drafting.
> 8. Protected-path and no-extra-file validation.
> 9. Self-review and repair.
> 10. Final handoff and goal-state report.
>
> The self-review rubric must total 100 points:
>
> | Area                                                        | Points |
> | ----------------------------------------------------------- | -----: |
> | Scope and protected-path discipline                         |     15 |
> | Evidence discipline                                         |     10 |
> | Consent model quality                                       |     20 |
> | PAI_DIR detection and source selection quality              |     20 |
> | Preflight, abort, and reporting boundary quality            |     20 |
> | Memory, ISA, Pulse, product-memory, and no-live-read safety |     10 |
> | Verification quality                                        |      5 |
>
> Pass threshold:
>
> ```text
> Minimum score: 94/100
> Hard failures: 0
> ```
>
> Record at least one scored iteration in `## Iteration Log`.
>
> ### Required file: `docs/adapters/V5_CODEX_LIVE_READ_ONLY_CONSENT_MODEL.md`
>
> Purpose: define the future explicit user consent model required before any live local PAI v5 read-only trial.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Live Read-Only Consent Model
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Consent Problem Statement
> ## Consent Principles
> ## Consent Boundary Model
> ## User Disclosure Requirements
> ## Consent Capture Requirements
> ## Consent Scope Model
> ## Consent Expiration and Revocation
> ## Consent and No-Write Policy
> ## Consent and Product Memory Boundary
> ## Consent and Pulse Boundary
> ## Consent and PAI Memory ISA Boundary
> ## Consent Failure Conditions
> ## Required Future Proofs
> ## Prohibited Consent Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * State that S12A does not collect user consent.
> * State that future consent must be explicit, bounded, revocable, and source-specific.
> * State that future consent must not be inferred from having Claude Code installed.
> * State that future consent must not be inferred from having Codex installed.
> * State that future consent must not be inferred from having both subscriptions.
> * State that future consent must separately identify:
>
>   * source root;
>   * allowed read scope;
>   * forbidden read scope;
>   * forbidden writes;
>   * reporting output;
>   * retention policy;
>   * rollback/no-residue expectation.
> * State that consent does not authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory reads, product-memory promotion, root `AGENTS.md`, or `.codex/`.
> * State that S12A creates no consent artifact.
>
> ### Required file: `docs/adapters/V5_CODEX_PAI_DIR_DETECTION_AND_SOURCE_SELECTION_SPEC.md`
>
> Purpose: define future read-only PAI_DIR detection and source-selection behavior without reading live local state in S12A.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex PAI_DIR Detection and Source Selection Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## PAI_DIR Problem Statement
> ## Detection Principles
> ## Source Kind Model
> ## Candidate Source Roots
> ## Allowed Detection Inputs
> ## Forbidden Detection Inputs
> ## PAI_DIR Confirmation Model
> ## Source Selection Workflow
> ## Source Selection Failure Conditions
> ## No-Default-Live-Read Rule
> ## Existing Local v5 Boundary
> ## Product Memory Boundary
> ## Pulse Boundary
> ## Required Future Proofs
> ## Prohibited Detection Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * State that S12A does not detect live `PAI_DIR`.
> * State that `PAI_DIR` means the PAI subsystem root, usually `~/.claude/PAI`, but S12A does not inspect it.
> * Define source kinds:
>
>   * `release-fixture`
>   * `sanitized-user-fixture`
>   * `existing-local-v5-read-only`
> * State that `existing-local-v5-read-only` is future-only and requires explicit consent plus architect approval.
> * Define future detection as read-only, path-bounded, and abortable.
> * State no default live local read.
> * State no scanning of arbitrary home directories.
> * State no reading `~/.claude/projects/**/memory`.
> * State no reading `~/.codex/memories`.
> * State no reading product memories by default.
> * State no writing discovered paths into PAI Memory, ISA, Pulse, Claude memory, or Codex memory.
>
> ### Required file: `docs/adapters/V5_CODEX_LIVE_READ_ONLY_PREFLIGHT_AND_ABORT_MODEL.md`
>
> Purpose: define future preflight checks and abort conditions before any live local PAI v5 read-only trial can run.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Live Read-Only Preflight and Abort Model
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Preflight Problem Statement
> ## Preflight Principles
> ## Required Preflight Checks
> ## Consent Preflight
> ## Source Root Preflight
> ## Protected Path Preflight
> ## No-Write Preflight
> ## Pulse Preflight
> ## Memory and ISA Preflight
> ## Product Memory Preflight
> ## Runtime Invocation Preflight
> ## Abort Condition Model
> ## Abort Report Model
> ## Required Future Proofs
> ## Prohibited Preflight Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * State that S12A runs no preflight against live local state.
> * Define future preflight checks for:
>
>   * explicit consent present;
>   * source root matches consent;
>   * no root `AGENTS.md`;
>   * no `.codex/`;
>   * no write mode;
>   * no Pulse startup;
>   * no Pulse endpoint calls;
>   * no PAI Memory writes;
>   * no ISA writes;
>   * no product-memory reads by default;
>   * no Codex runtime adapter execution;
>   * no Claude Code invocation;
>   * no installer execution.
> * Define abort conditions:
>
>   * missing consent;
>   * ambiguous source root;
>   * unexpected private state;
>   * any write requirement;
>   * Pulse startup requirement;
>   * Pulse call requirement;
>   * Memory/ISA write requirement;
>   * product-memory access requirement;
>   * runtime adapter requirement;
>   * drop-in claim pressure.
> * Define abort report as future advisory-only output, not PAI Memory, ISA, Pulse state, manifest, audit artifact, or runtime payload.
>
> ### Required file: `docs/adapters/V5_CODEX_LIVE_READ_ONLY_REPORTING_BOUNDARY_SPEC.md`
>
> Purpose: define future live-read-only reporting boundaries and non-canonical output rules.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Live Read-Only Reporting Boundary Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Reporting Problem Statement
> ## Reporting Principles
> ## Report Type Model
> ## Required Report Fields
> ## Non-Canonical Output Rules
> ## Privacy and Retention Rules
> ## No-Promotion Rules
> ## Denied Action Reporting
> ## Unsupported Surface Reporting
> ## Pulse Reporting Boundary
> ## Memory and ISA Reporting Boundary
> ## Product Memory Reporting Boundary
> ## Drop-In Claim Reporting
> ## Required Future Proofs
> ## Prohibited Reporting Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * State that S12A creates no live-read report.
> * Define future report types:
>
>   * `consent-preflight-report`
>   * `source-selection-report`
>   * `live-read-only-preflight-report`
>   * `abort-report`
>   * `live-read-only-evidence-report`
> * State every future report is non-canonical unless separately approved.
> * State future reports are not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not manifest, and not runtime payload.
> * State reports must not be promoted into PAI Memory by default.
> * Define required future fields:
>
>   * report ID;
>   * source kind;
>   * consent reference;
>   * source root;
>   * allowed reads;
>   * forbidden reads;
>   * forbidden writes;
>   * denied action report;
>   * unsupported surface report;
>   * Pulse status;
>   * Memory status;
>   * ISA status;
>   * product memory status;
>   * runtime invocation status;
>   * drop-in claim status;
>   * rollback/no-residue status;
>   * non-canonical statement.
>
> ### Required file: `docs/adapters/V5_CODEX_S12A_DECISION_LOG.md`
>
> Purpose: record S12A decisions, non-decisions, blocked decisions, and future architect questions.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex S12A Decision Log
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Decisions Made in S12A
> ## Non-Decisions in S12A
> ## Blocked Decisions
> ## Future Architect Questions
> ## Decision Table
> ## Next Milestone Candidates
> ## Non-Goals
> ```
>
> Required content:
>
> Include a decision table with columns:
>
> ```text
> Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger
> ```
>
> Minimum decisions:
>
> ```text
> S12A-D01 Codex remains not drop-in today.
> S12A-D02 S12A designs consent and source-selection only.
> S12A-D03 S12A does not run a live read-only trial.
> S12A-D04 S12A does not read live existing-local-v5 state.
> S12A-D05 Future live read requires explicit user consent.
> S12A-D06 Consent cannot be inferred from Claude Code installation.
> S12A-D07 Consent cannot be inferred from Codex installation.
> S12A-D08 Consent cannot be inferred from dual subscriptions.
> S12A-D09 PAI_DIR detection remains future-only and read-only.
> S12A-D10 No default live local read is allowed.
> S12A-D11 Product memory reads remain denied by default.
> S12A-D12 Pulse startup and endpoint calls remain denied.
> S12A-D13 PAI Memory and ISA writes remain denied.
> S12A-D14 Root AGENTS.md and .codex remain protected.
> S12A-D15 Future reporting output must be non-canonical.
> S12A-D16 Runtime adapter planning remains blocked until live-read-only readiness is approved.
> ```
>
> The `## Next Milestone Candidates` section must list advisory-only options, not approvals:
>
> * `V5-S12B`: Consent artifact proposal and validation design.
> * `V5-S12C`: PAI_DIR detection dry-run design.
> * `V5-S12D`: Live-read-only preflight report design.
> * `V5-S13A`: First approved live-read-only trial, only after S12 readiness is accepted.
> * `V5-S13B`: Runtime adapter planning, only after live-read-only trial evidence is accepted.
>
> State that architect approval is required before any future milestone.
>
> ### Protected paths
>
> Do not modify:
>
> * `Releases/`
> * `Releases/v5.0.0/`
> * `Releases/v5.0.0/.claude/`
> * `.claude/`
> * `PAI/`
> * `CLAUDE.md`
> * `AGENTS.md`
> * `.codex/`
> * `install.sh`
> * `PAI_SYSTEM_PROMPT.md`
> * `settings.json`
> * `hooks/`
> * `skills/`
> * `subagents/`
> * `agents/`
> * `commands/`
> * `.github/`
> * `.agents/`
>
> Do not inspect or modify private user-local state:
>
> * `~/.claude/`
> * `~/.claude/PAI/`
> * `~/.claude/projects/`
> * `~/.codex/`
> * `~/.codex/memories/`
>
> ### Hard failure conditions
>
> S12A fails immediately if:
>
> * Any file outside the approved write set is created or modified.
> * Any fixture, harness, generator, evaluator, report, README, or release file is modified.
> * Any protected file is modified.
> * Runtime adapter files are created.
> * Root `AGENTS.md` or `.codex/` is created or modified.
> * Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures are created.
> * A live read-only trial is run.
> * Private user-local state is inspected or modified.
> * Live existing-local-v5 state is read.
> * `~/.claude/PAI` is inspected.
> * `~/.claude/projects` is inspected.
> * `~/.codex` is inspected.
> * PAI Memory is written.
> * ISA is written.
> * Pulse is started.
> * Pulse endpoints are called.
> * `localhost:31337` is probed.
> * Installers are run.
> * Claude Code is invoked.
> * Codex is invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available.
> * Codex import or migration tooling is run.
> * Codex hook, rule, or execpolicy commands are run.
> * The docs claim Codex is drop-in today.
> * The docs claim Codex is the official upstream engine.
> * The docs authorize PAI Memory writes.
> * The docs authorize ISA writes.
> * The docs authorize Pulse startup.
> * The docs authorize Pulse endpoint calls.
> * The docs authorize Pulse implementation.
> * The docs authorize existing-local-v5 trial execution.
> * The docs imply Claude-shaped files can be copied directly into Codex surfaces.
> * The docs authorize product-memory promotion into PAI Memory.
> * The docs authorize dual-engine uncoordinated writes.
> * The goal advances beyond S12A.
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
> Run changed-file check, heading check, content invariant check, and protected-path and no-test-change checks as specified by the S12A card.
>
> ### Acceptance criteria
>
> S12A is complete only if:
>
> * Exactly the six approved S12A docs are created or modified.
> * No fixture, harness, generator, evaluator, report, README, release, or runtime file is modified.
> * No protected files are changed.
> * No runtime adapter files are created.
> * No root `AGENTS.md` is created or modified.
> * No `.codex/` files are created or modified.
> * No Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures are created.
> * No live read-only trial is run.
> * No private user-local state is inspected or modified.
> * No live existing-local-v5 state is read.
> * `~/.claude/PAI` is not inspected.
> * `~/.claude/projects` is not inspected.
> * `~/.codex` is not inspected.
> * PAI Memory is not written.
> * ISA is not written.
> * Pulse is not started.
> * Pulse endpoints are not called.
> * `localhost:31337` is not probed.
> * Installers are not run.
> * Claude Code is not invoked.
> * Codex is not invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available.
> * Codex import/migration tooling is not run.
> * Codex hook, rule, or execpolicy commands are not run.
> * `V5_S12A_EXEC_PLAN.md` contains the Completion Contract copied into its `## Completion Contract` section.
> * The consent model states that consent is not inferred from Claude Code installation, Codex installation, or dual subscriptions.
> * The PAI_DIR spec states that S12A does not detect live `PAI_DIR`.
> * The preflight model states that S12A runs no live preflight.
> * The reporting boundary spec states that S12A creates no live-read report.
> * The decision log includes all required `S12A-D01` through `S12A-D16` decisions.
> * Changed-file check passes.
> * Heading check passes.
> * Content invariant check passes.
> * No-test-change check passes.
> * Protected-path check has no output.
> * The deliverables do not claim Codex is drop-in today.
> * The deliverables do not claim Codex is the official upstream engine.
> * The deliverables do not authorize PAI Memory writes.
> * The deliverables do not authorize ISA writes.
> * The deliverables do not authorize Pulse startup.
> * The deliverables do not authorize Pulse endpoint calls.
> * The deliverables do not authorize Pulse implementation.
> * The deliverables do not authorize existing-local-v5 trial execution.
> * The deliverables do not imply Claude-shaped files can be copied directly into Codex surfaces.
> * The deliverables do not authorize product-memory promotion into PAI Memory.
> * The deliverables do not authorize dual-engine uncoordinated writes.
> * The execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures.
> * Final handoff reports every required validation command.
>
> ### Final handoff format
>
> End with exactly these headings:
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
> `Protected files changed` must be exactly `Yes` or `No`, followed by a brief explanation.
>
> Expected value:
>
> ```text
> No — only the six approved S12A documentation files were created or modified.
> ```
>
> `Recommended next architect decision` must be advisory only. Do not begin S12B, S12C, S12D, S13A, or runtime adapter work.
>
> ### Stop conditions
>
> Stop and report immediately if:
>
> * Any protected file must be edited.
> * Any file outside the approved write set is modified.
> * Any test fixture, harness, generator, evaluator, report, README, or release file would need to be modified.
> * Runtime implementation seems necessary.
> * Root `AGENTS.md` or `.codex/` would need to be modified.
> * A Codex config, hook, rule, skill, subagent, agent, command, launcher, installer, wrapper, generated runtime config, migration script, adapter payload, Memory payload, ISA payload, Pulse payload, Pulse bridge file, manifest instance, executable schema, live-trial artifact, runtime payload, or committed negative fixture would need to be created.
> * A live trial would need to be run.
> * PAI Memory would need to be written.
> * ISA would need to be written.
> * Existing-local-v5 state would need to be read.
> * `~/.claude/PAI` would need to be inspected.
> * `~/.claude/projects` would need to be inspected.
> * `~/.codex` would need to be inspected.
> * Pulse would need to be started.
> * A Pulse endpoint would need to be called.
> * `localhost:31337` would need to be probed.
> * Upstream v5 would need to be patched.
> * Private user-local memory would need to be read.
> * Codex import/migration tooling seems necessary.
> * Claude Code would need to be invoked.
> * Codex would need to be invoked as a runtime engine.
> * Codex hook, rule, or execpolicy commands would need to be run.
> * The goal tries to continue beyond S12A.
> * The Completion Contract cannot be copied into the execution plan.
> * The self-review cannot reach 94/100 without leaving scope.

## Milestones

1. Baseline status check.
2. S10/S11 closeout reread.
3. Consent model drafting.
4. PAI_DIR detection and source selection spec drafting.
5. Preflight and abort model drafting.
6. Reporting boundary spec drafting.
7. Decision log drafting.
8. Protected-path and no-extra-file validation.
9. Self-review and repair.
10. Final handoff and goal-state report.

## Self-Review Rubric

| Area | Points |
| --- | ---: |
| Scope and protected-path discipline | 15 |
| Evidence discipline | 10 |
| Consent model quality | 20 |
| PAI_DIR detection and source selection quality | 20 |
| Preflight, abort, and reporting boundary quality | 20 |
| Memory, ISA, Pulse, product-memory, and no-live-read safety | 10 |
| Verification quality | 5 |
| Total | 100 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

Hard failures:

- Any file outside the approved S12A write set changes.
- Any fixture, harness, generator, evaluator, report, README, or release file changes.
- Any protected path changes.
- Any live read-only trial, live existing-local-v5 read, private user-local read, Pulse start/call, PAI Memory write, ISA write, Claude Code invocation, or Codex runtime invocation occurs.
- Any runtime adapter file, root `AGENTS.md`, `.codex/`, manifest, schema, audit artifact, live-trial artifact, runtime payload, Memory payload, ISA payload, Pulse payload, or committed negative fixture is created.
- Any deliverable claims Codex is drop-in today or official upstream engine, or authorizes live trials, runtime adapter work, Pulse startup/calls, PAI Memory writes, ISA writes, existing-local-v5 access, product-memory promotion, or dual-engine uncoordinated writes.

## Validation Commands

Required validation commands:

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

Additional checks:

- Changed-file check.
- Heading check.
- Content invariant check.
- No-test-change check.
- Protected-path check.

## Progress

- Baseline status check: completed before S12A file creation; worktree was clean.
- S10/S11 closeout reread: completed using repository-local S11D closeout, S12 gate proposal, proposed contract, and decision log.
- Existing S10/S11 validations: completed before S12A file creation; harness, negative-control self-test, no-residue self-test, and report-generator self-test passed.
- Consent model drafting: completed in `docs/adapters/V5_CODEX_LIVE_READ_ONLY_CONSENT_MODEL.md`.
- PAI_DIR detection and source selection spec drafting: completed in `docs/adapters/V5_CODEX_PAI_DIR_DETECTION_AND_SOURCE_SELECTION_SPEC.md`.
- Preflight and abort model drafting: completed in `docs/adapters/V5_CODEX_LIVE_READ_ONLY_PREFLIGHT_AND_ABORT_MODEL.md`.
- Reporting boundary spec drafting: completed in `docs/adapters/V5_CODEX_LIVE_READ_ONLY_REPORTING_BOUNDARY_SPEC.md`.
- Decision log drafting: completed in `docs/adapters/V5_CODEX_S12A_DECISION_LOG.md`.
- Final validation execution: completed; all required validation commands and content checks passed.

## Iteration Log

Iteration 1 self-review score: 100/100. Hard failures: 0.

| Area | Points | Result |
| --- | ---: | --- |
| Scope and protected-path discipline | 15/15 | Only the six approved S12A docs are changed; protected-path check has no output. |
| Evidence discipline | 10/10 | Source material is limited to repository-local S10/S11 docs and fixture evidence. |
| Consent model quality | 20/20 | Consent is explicit, bounded, revocable, source-specific, not inferred, and does not authorize writes or runtime surfaces. |
| PAI_DIR detection and source selection quality | 20/20 | `PAI_DIR` detection is future-only, read-only, consent-bound, path-bounded, and no-default-live-read. |
| Preflight, abort, and reporting boundary quality | 20/20 | Future preflight, abort, and reporting boundaries preserve no-write, no-runtime, non-canonical output, and fail-closed behavior. |
| Memory, ISA, Pulse, product-memory, and no-live-read safety | 10/10 | PAI Memory, ISA, Pulse, product memory, live user-local, and existing-local-v5 boundaries are denied by default. |
| Verification quality | 5/5 | Required validation commands, changed-file, heading, content invariant, no-test-change, and protected-path checks pass. |

## Surprises & Discoveries

- The local sandbox wrapper returned `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; repository-local validation commands were rerun outside the broken sandbox using explicit escalations.
- The S11D closeout keeps S12 proposed only and requires explicit user consent design before any future live local read.

## Decision Log

- Use documentation-only S12A deliverables and do not alter fixture, harness, generator, evaluator, report, README, release, or protected files.
- Treat `existing-local-v5-read-only` as future-only and unavailable in S12A.
- Treat all future S12A reporting outputs as non-canonical design outputs unless separately approved.
- Repair one literal content invariant by adding the exact phrase `root AGENTS.md` while preserving the protected-path meaning.

## Outcomes & Retrospective

Validation results recorded:

- `git status --short`: only the six approved S12A docs.
- `git diff --name-only | sort`: only the six approved S12A docs.
- `git diff --check`: pass.
- Fixture harness: pass.
- Harness negative-control self-test: pass with `negative_control_count: 60`.
- No-residue self-test: pass.
- Report-generator negative-control self-test: pass with `negative_control_count: 16`.
- S11A report generation command: pass and did not add changed report files.
- S11C readiness evaluator command: pass and did not add changed report files.
- Changed-file check: pass.
- Heading check: pass.
- Content invariant check: pass.
- No-test-change check: pass.
- Protected-path check: no output.

S12A remains documentation/design only. It does not run a live read-only trial, read live existing-local-v5 state, inspect private user-local state, implement a runtime adapter, create root `AGENTS.md`, create `.codex/`, start or call Pulse, write PAI Memory, write ISA, authorize product-memory promotion, or claim Codex is drop-in today.
