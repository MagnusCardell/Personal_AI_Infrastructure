# V5-S12B Execution Plan

## Purpose

Execute V5-S12B Consent Artifact Schema and Validation Design. S12B designs the future consent artifact schema, validation rules, revocation/expiration model, consent failure cases, and proposed validation approach required before any future live existing-local-v5 read-only trial can be considered.

Codex is not currently proven drop-in for existing local PAI v5 files. S12B is documentation/design only; it does not create an actual consent artifact, does not create a consent validator, does not run a live read-only trial, and does not implement a runtime adapter.

## Scope

In scope:

- Create this S12B execution plan.
- Create the consent artifact schema proposal.
- Create the consent validation and revocation spec.
- Create the consent failure and abort cases document.
- Create the consent non-canonical reporting spec.
- Create the S12B decision log.
- Run and record all required validation commands.

Out of scope:

- Actual consent artifacts.
- Consent validators.
- Live read-only trials or live existing-local-v5 access.
- Runtime adapter implementation.
- Fixture, harness, generator, evaluator, report, README, release, protected-path, or runtime file edits.
- Root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures.

## Approved Write Set

Create exactly these files:

- `docs/adapters/V5_S12B_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_CONSENT_ARTIFACT_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_CONSENT_VALIDATION_AND_REVOCATION_SPEC.md`
- `docs/adapters/V5_CODEX_CONSENT_FAILURE_AND_ABORT_CASES.md`
- `docs/adapters/V5_CODEX_CONSENT_NON_CANONICAL_REPORTING_SPEC.md`
- `docs/adapters/V5_CODEX_S12B_DECISION_LOG.md`

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

- S0-S12A adapter docs for prior adapter conclusions.
- Existing S10/S11 fixture and evidence files.
- Repository-local PAI v5 release files for PAI facts only if needed.
- Official OpenAI Codex docs only if S12B adds or refreshes a Codex capability claim.
- Local `codex --version` or `codex --help` only if already available and non-invasive.

Forbidden sources and operations:

- Unofficial Codex capability sources.
- Inferred current Codex behavior from memory.
- Live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, or other private user-local state.
- Live existing-local-v5 state.
- Pulse startup, Pulse endpoint calls, or `localhost:31337` probes.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, and Codex hook/rule/execpolicy commands.

## Source Material

Baseline discovery before S12B edits:

- `git status --short`: no output.
- Required S12A consent, PAI_DIR, preflight, reporting, and decision docs existed.
- Required S11 closeout and proposed S12 contract docs existed.
- Existing harness validation passed with `fixture_count: 12`, `case_count: 12`, `coverage_id_count: 25`, `gate_id_count: 20`, and `status: pass`.
- Existing harness negative-control self-test passed with `negative_control_count: 60`.
- Existing no-residue self-test passed.
- Existing report-generator negative-control self-test passed with `negative_control_count: 16`.
- S11A report generation and S11C readiness evaluation commands passed and left the worktree clean.

S12A source reread:

- Consent must be explicit user consent, bounded, revocable, source-specific, and not inferred from Claude Code installation, Codex installation, or dual subscriptions.
- `existing-local-v5-read-only` remains future-only and requires explicit consent plus architect approval.
- Future reports and consent-related outputs are non-canonical unless separately approved.
- PAI Memory, ISA, Pulse, product memory, root `AGENTS.md`, `.codex/`, runtime invocation, and drop-in claim boundaries remain denied by default.

## Completion Contract

The S12B Completion Contract is copied below in quoted form to preserve the required execution-plan H1/H2 sequence while retaining the contract text.

> ## Completion Contract
>
> This Completion Contract is the authoritative contract for V5-S12B.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S12B_EXEC_PLAN.md`.
>
> Do not mark S12B complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S12B deliverables must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S12B designs future consent artifact schema and validation only.
> * S12B does not create an actual consent artifact.
> * S12B does not create a consent validator.
> * S12B does not run a live read-only trial.
> * S12B does not read live existing-local-v5 state.
> * S12B does not read live user-local state.
> * S12B does not implement a Codex runtime adapter.
> * S12B does not create runtime adapter files.
> * S12B does not create root `AGENTS.md`.
> * S12B does not create `.codex/`.
> * S12B does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures.
> * A future consent artifact is not PAI Memory.
> * A future consent artifact is not ISA.
> * A future consent artifact is not Pulse state.
> * A future consent artifact is not Claude memory.
> * A future consent artifact is not Codex memory.
> * A future consent artifact is not a runtime adapter payload.
> * A future consent artifact is not proof that Codex is drop-in.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Product memories must not be silently promoted into PAI Memory.
> * Pulse is central v5 infrastructure, but S12B does not start Pulse, call Pulse endpoints, or claim Pulse parity.
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
> test -f docs/adapters/V5_CODEX_LIVE_READ_ONLY_CONSENT_MODEL.md
> test -f docs/adapters/V5_CODEX_PAI_DIR_DETECTION_AND_SOURCE_SELECTION_SPEC.md
> test -f docs/adapters/V5_CODEX_LIVE_READ_ONLY_PREFLIGHT_AND_ABORT_MODEL.md
> test -f docs/adapters/V5_CODEX_LIVE_READ_ONLY_REPORTING_BOUNDARY_SPEC.md
> test -f docs/adapters/V5_CODEX_S12A_DECISION_LOG.md
> test -f docs/adapters/V5_CODEX_S11_EVIDENCE_CLOSEOUT_REPORT.md
> test -f docs/adapters/V5_CODEX_S12_PROPOSED_WRITE_SET_AND_COMPLETION_CONTRACT.md
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
> ### Required file: `docs/adapters/V5_S12B_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S12B Execution Plan
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
> 2. S11/S12A reread.
> 3. Consent artifact schema proposal drafting.
> 4. Consent validation and revocation spec drafting.
> 5. Consent failure and abort case drafting.
> 6. Consent non-canonical reporting spec drafting.
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
> | Consent artifact schema quality                             |     25 |
> | Validation, revocation, and expiration quality              |     20 |
> | Failure, abort, and reporting boundary quality              |     15 |
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
> ### Required file: `docs/adapters/V5_CODEX_CONSENT_ARTIFACT_SCHEMA_PROPOSAL.md`
>
> Purpose: define the future consent artifact schema proposal required before any live local PAI v5 read-only trial.
>
> It must contain exactly the required consent artifact schema proposal headings. It must state that this is a schema proposal in markdown only; S12B does not create an actual consent artifact; the future consent artifact is non-canonical unless separately approved; the future consent artifact is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in; define the required top-level proposed fields; define allowed future `source_kind` values `release-fixture`, `sanitized-user-fixture`, and `existing-local-v5-read-only`; mark `existing-local-v5-read-only` as future-only and requiring explicit user consent plus architect approval; include one non-executable example consent artifact inside a markdown fenced block; and label the example `NON-EXECUTABLE DESIGN SKETCH — DO NOT USE AS CONSENT`.
>
> ### Required file: `docs/adapters/V5_CODEX_CONSENT_VALIDATION_AND_REVOCATION_SPEC.md`
>
> Purpose: define future consent validation, revocation, expiration, and replay-protection rules before live local reads.
>
> It must contain exactly the required validation and revocation headings. It must state that S12B implements no validator; define future consent statuses `draft`, `pending-user-approval`, `approved-for-preflight-only`, `approved-for-live-read-only`, `revoked`, `expired`, `invalid`, and `aborted`; state S12B approves none of these statuses for live use; define validation outputs `consent_valid`, `consent_scope`, `allowed_reads`, `forbidden_reads`, `forbidden_writes`, `runtime_prohibitions`, `abort_required`, `failure_reason`, `reporting_boundary`, and `non_canonical_statement`; state revoked, expired, ambiguous, mismatched, or replayed consent must abort; state validation must not read live local state by itself; and state validation must not write PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, or `.codex/`.
>
> ### Required file: `docs/adapters/V5_CODEX_CONSENT_FAILURE_AND_ABORT_CASES.md`
>
> Purpose: define future failure and abort cases for consent, source selection, PAI_DIR detection, and live-read preflight.
>
> It must contain exactly the required failure and abort headings. It must include an abort case table with columns `Abort ID | Failure class | Trigger | Required response | Reported evidence | Future proof required | S12B status`, include `CA-001` through `CA-025`, and mark every case as design-only.
>
> ### Required file: `docs/adapters/V5_CODEX_CONSENT_NON_CANONICAL_REPORTING_SPEC.md`
>
> Purpose: define future reporting boundaries for consent validation and abort reports.
>
> It must contain exactly the required reporting headings. It must state that S12B creates no consent report; define future report types `consent-schema-review-report`, `consent-validation-report`, `consent-revocation-report`, `consent-expiration-report`, and `consent-abort-report`; state that reports are not PAI Memory, ISA, Pulse state, Claude memory, Codex memory, manifests, runtime payloads, or proof that Codex is drop-in; and define the required future report fields.
>
> ### Required file: `docs/adapters/V5_CODEX_S12B_DECISION_LOG.md`
>
> Purpose: record S12B decisions, non-decisions, blocked decisions, and future architect questions.
>
> It must contain exactly the required decision-log headings. It must include a decision table with columns `Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger`. It must include decisions `S12B-D01` through `S12B-D18`. The Next Milestone Candidates section must list advisory-only options for `V5-S12C`, `V5-S12D`, `V5-S12E`, `V5-S13A`, and `V5-S13B`, and state that architect approval is required before any future milestone.
>
> ### Protected paths
>
> Do not modify `Releases/`, `Releases/v5.0.0/`, `Releases/v5.0.0/.claude/`, `.claude/`, `PAI/`, `CLAUDE.md`, `AGENTS.md`, `.codex/`, `install.sh`, `PAI_SYSTEM_PROMPT.md`, `settings.json`, `hooks/`, `skills/`, `subagents/`, `agents/`, `commands/`, `.github/`, or `.agents/`.
>
> Do not inspect or modify private user-local state: `~/.claude/`, `~/.claude/PAI/`, `~/.claude/projects/`, `~/.codex/`, or `~/.codex/memories/`.
>
> ### Hard failure conditions
>
> S12B fails immediately if any file outside the approved write set is created or modified; any fixture, harness, generator, evaluator, report, README, or release file is modified; any protected file is modified; runtime adapter files are created; root `AGENTS.md` is created or modified; `.codex/` is created or modified; Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, manifest instances, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures are created; a live read-only trial is run; private user-local state is inspected or modified; live existing-local-v5 state is read; `~/.claude/PAI`, `~/.claude/projects`, or `~/.codex` is inspected; PAI Memory is written; ISA is written; Pulse is started; Pulse endpoints are called; `localhost:31337` is probed; installers are run; Claude Code is invoked; Codex is invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available; Codex import or migration tooling is run; Codex hook, rule, or execpolicy commands are run; the docs claim Codex is drop-in today or the official upstream engine; the docs authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, Pulse implementation, existing-local-v5 trial execution, product-memory promotion into PAI Memory, or dual-engine uncoordinated writes; the docs imply Claude-shaped files can be copied directly into Codex surfaces; or the goal advances beyond S12B.
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
> Run changed-file check, heading check, content invariant check, no-test-change check, and protected-path check exactly as specified by the S12B card.
>
> ### Acceptance criteria
>
> S12B is complete only if exactly the six approved S12B docs are created or modified; no fixture, harness, generator, evaluator, report, README, release, or runtime file is modified; no protected files are changed; no runtime adapter files are created; no root `AGENTS.md` or `.codex/` files are created or modified; no Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, manifest instances, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures are created; no live read-only trial is run; no private user-local state or live existing-local-v5 state is read; `~/.claude/PAI`, `~/.claude/projects`, and `~/.codex` are not inspected; PAI Memory and ISA are not written; Pulse is not started or called; `localhost:31337` is not probed; installers, Claude Code, Codex runtime, Codex import/migration tooling, and Codex hook/rule/execpolicy commands are not run; the execution plan contains the Completion Contract; the schema proposal states S12B creates no actual consent artifact; the validation spec states S12B implements no validator; the failure cases doc includes `CA-001` through `CA-025`; the reporting spec states S12B creates no consent report; the decision log includes `S12B-D01` through `S12B-D18`; changed-file, heading, content invariant, no-test-change, and protected-path checks pass; and the execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures.
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
> No — only the six approved S12B documentation files were created or modified.
> ```
>
> `Recommended next architect decision` must be advisory only. Do not begin S12C, S12D, S13A, or runtime adapter work.
>
> ### Stop conditions
>
> Stop and report immediately if any protected file must be edited; any file outside the approved write set is modified; any test fixture, harness, generator, evaluator, report, README, or release file would need to be modified; runtime implementation seems necessary; a consent artifact or consent validator would need to be created; root `AGENTS.md` or `.codex/` would need to be modified; a Codex config, hook, rule, skill, subagent, agent, command, launcher, installer, wrapper, generated runtime config, migration script, adapter payload, Memory payload, ISA payload, Pulse payload, Pulse bridge file, consent artifact, manifest instance, executable schema, live-trial artifact, runtime payload, or committed negative fixture would need to be created; a live trial would need to be run; PAI Memory or ISA would need to be written; existing-local-v5 state, `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or private user-local memory would need to be read; Pulse would need to be started; a Pulse endpoint or `localhost:31337` would need to be probed; upstream v5 would need to be patched; Codex import/migration tooling, Claude Code, Codex runtime engine, or Codex hook/rule/execpolicy commands would need to be run; the goal tries to continue beyond S12B; the Completion Contract cannot be copied into the execution plan; or self-review cannot reach 94/100 without leaving scope.

Unabridged contract source retained for audit:

> ## Completion Contract
>
> This Completion Contract is the authoritative contract for V5-S12B.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S12B_EXEC_PLAN.md`.
>
> Do not mark S12B complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S12B deliverables must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S12B designs future consent artifact schema and validation only.
> * S12B does not create an actual consent artifact.
> * S12B does not create a consent validator.
> * S12B does not run a live read-only trial.
> * S12B does not read live existing-local-v5 state.
> * S12B does not read live user-local state.
> * S12B does not implement a Codex runtime adapter.
> * S12B does not create runtime adapter files.
> * S12B does not create root `AGENTS.md`.
> * S12B does not create `.codex/`.
> * S12B does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures.
> * A future consent artifact is not PAI Memory.
> * A future consent artifact is not ISA.
> * A future consent artifact is not Pulse state.
> * A future consent artifact is not Claude memory.
> * A future consent artifact is not Codex memory.
> * A future consent artifact is not a runtime adapter payload.
> * A future consent artifact is not proof that Codex is drop-in.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Product memories must not be silently promoted into PAI Memory.
> * Pulse is central v5 infrastructure, but S12B does not start Pulse, call Pulse endpoints, or claim Pulse parity.
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
> test -f docs/adapters/V5_CODEX_LIVE_READ_ONLY_CONSENT_MODEL.md
> test -f docs/adapters/V5_CODEX_PAI_DIR_DETECTION_AND_SOURCE_SELECTION_SPEC.md
> test -f docs/adapters/V5_CODEX_LIVE_READ_ONLY_PREFLIGHT_AND_ABORT_MODEL.md
> test -f docs/adapters/V5_CODEX_LIVE_READ_ONLY_REPORTING_BOUNDARY_SPEC.md
> test -f docs/adapters/V5_CODEX_S12A_DECISION_LOG.md
> test -f docs/adapters/V5_CODEX_S11_EVIDENCE_CLOSEOUT_REPORT.md
> test -f docs/adapters/V5_CODEX_S12_PROPOSED_WRITE_SET_AND_COMPLETION_CONTRACT.md
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
> ### Required file: `docs/adapters/V5_S12B_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S12B Execution Plan
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
> 2. S11/S12A reread.
> 3. Consent artifact schema proposal drafting.
> 4. Consent validation and revocation spec drafting.
> 5. Consent failure and abort case drafting.
> 6. Consent non-canonical reporting spec drafting.
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
> | Consent artifact schema quality                             |     25 |
> | Validation, revocation, and expiration quality              |     20 |
> | Failure, abort, and reporting boundary quality              |     15 |
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
> ### Required file: `docs/adapters/V5_CODEX_CONSENT_ARTIFACT_SCHEMA_PROPOSAL.md`
>
> Purpose: define the future consent artifact schema proposal required before any live local PAI v5 read-only trial.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Consent Artifact Schema Proposal
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Schema Proposal Status
> ## Consent Artifact Role
> ## Non-Canonical Artifact Rules
> ## Top-Level Field Model
> ## Identity and Version Fields
> ## User Disclosure Fields
> ## Source Selection Fields
> ## Allowed Read Scope Fields
> ## Forbidden Read Scope Fields
> ## Forbidden Write Scope Fields
> ## Runtime Prohibition Fields
> ## Product Memory Boundary Fields
> ## Pulse Boundary Fields
> ## Memory and ISA Boundary Fields
> ## Reporting and Retention Fields
> ## Revocation and Expiration Fields
> ## Cross-Field Validation Rules
> ## Example Non-Executable Consent Artifact
> ## Prohibited Schema Semantics
> ## Future Implementation Gates
> ## Non-Goals
> ```
>
> Required content:
>
> * State that this is a schema proposal in markdown only.
> * State that S12B does not create an actual consent artifact.
> * State that the future consent artifact is non-canonical unless separately approved.
> * State that the future consent artifact is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.
> * Define top-level proposed fields:
>
>   * `schema_id`
>   * `schema_version`
>   * `consent_id`
>   * `consent_status`
>   * `consent_created_at`
>   * `consent_expires_at`
>   * `consent_revoked_at`
>   * `principal_acknowledgement`
>   * `source_kind`
>   * `source_root`
>   * `source_root_confirmation`
>   * `pai_dir_candidate`
>   * `allowed_read_scope`
>   * `forbidden_read_scope`
>   * `forbidden_write_scope`
>   * `runtime_prohibitions`
>   * `product_memory_policy`
>   * `pulse_policy`
>   * `memory_policy`
>   * `isa_policy`
>   * `reporting_policy`
>   * `retention_policy`
>   * `rollback_no_residue_policy`
>   * `drop_in_claim_policy`
>   * `architect_approval_reference`
>   * `stop_conditions`
> * Define allowed future `source_kind` values:
>
>   * `release-fixture`
>   * `sanitized-user-fixture`
>   * `existing-local-v5-read-only`
> * Mark `existing-local-v5-read-only` as future-only and requiring explicit user consent plus architect approval.
> * Include one non-executable example consent artifact inside a markdown fenced block.
> * The example must be labeled `NON-EXECUTABLE DESIGN SKETCH — DO NOT USE AS CONSENT`.
>
> ### Required file: `docs/adapters/V5_CODEX_CONSENT_VALIDATION_AND_REVOCATION_SPEC.md`
>
> Purpose: define future consent validation, revocation, expiration, and replay-protection rules before live local reads.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Consent Validation and Revocation Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Validation Problem Statement
> ## Validation Principles
> ## Consent Status Model
> ## Validation Input Model
> ## Validation Output Model
> ## Revocation Model
> ## Expiration Model
> ## Replay Protection Model
> ## Source Root Consistency Checks
> ## Allowed Read Scope Checks
> ## Forbidden Read Scope Checks
> ## Forbidden Write Checks
> ## Product Memory Checks
> ## Pulse Checks
> ## Memory and ISA Checks
> ## Runtime Invocation Checks
> ## Failure and Abort Rules
> ## Required Future Proofs
> ## Prohibited Validation Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * State that S12B implements no validator.
> * Define future consent statuses:
>
>   * `draft`
>   * `pending-user-approval`
>   * `approved-for-preflight-only`
>   * `approved-for-live-read-only`
>   * `revoked`
>   * `expired`
>   * `invalid`
>   * `aborted`
> * State that S12B approves none of these statuses for live use.
> * Define validation outputs:
>
>   * `consent_valid`
>   * `consent_scope`
>   * `allowed_reads`
>   * `forbidden_reads`
>   * `forbidden_writes`
>   * `runtime_prohibitions`
>   * `abort_required`
>   * `failure_reason`
>   * `reporting_boundary`
>   * `non_canonical_statement`
> * State that revoked, expired, ambiguous, mismatched, or replayed consent must abort.
> * State that validation must not read live local state by itself.
> * State that validation must not write PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, or `.codex/`.
>
> ### Required file: `docs/adapters/V5_CODEX_CONSENT_FAILURE_AND_ABORT_CASES.md`
>
> Purpose: define future failure and abort cases for consent, source selection, PAI_DIR detection, and live-read preflight.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Consent Failure and Abort Cases
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Failure Case Philosophy
> ## Consent Failure Cases
> ## Source Selection Failure Cases
> ## PAI_DIR Failure Cases
> ## Read Scope Failure Cases
> ## Write Pressure Failure Cases
> ## Product Memory Failure Cases
> ## Pulse Failure Cases
> ## Memory and ISA Failure Cases
> ## Runtime Invocation Failure Cases
> ## Reporting Failure Cases
> ## Abort Case Table
> ## Required Future Proofs
> ## Prohibited Failure Handling Designs
> ## Non-Goals
> ```
>
> Required content:
>
> Include an abort case table with columns:
>
> ```text
> Abort ID | Failure class | Trigger | Required response | Reported evidence | Future proof required | S12B status
> ```
>
> Minimum abort IDs:
>
> * `CA-001`: missing consent.
> * `CA-002`: expired consent.
> * `CA-003`: revoked consent.
> * `CA-004`: ambiguous source root.
> * `CA-005`: source root mismatch.
> * `CA-006`: source kind mismatch.
> * `CA-007`: missing `PAI_DIR` confirmation.
> * `CA-008`: attempt to read outside allowed scope.
> * `CA-009`: attempt to read product memory by default.
> * `CA-010`: attempt to read `~/.claude/projects/**/memory`.
> * `CA-011`: attempt to read `~/.codex/memories`.
> * `CA-012`: write requirement detected.
> * `CA-013`: PAI Memory write pressure.
> * `CA-014`: ISA write pressure.
> * `CA-015`: Pulse startup pressure.
> * `CA-016`: Pulse endpoint call pressure.
> * `CA-017`: root `AGENTS.md` write pressure.
> * `CA-018`: `.codex/` write pressure.
> * `CA-019`: runtime adapter implementation pressure.
> * `CA-020`: Claude Code invocation pressure.
> * `CA-021`: Codex runtime invocation pressure.
> * `CA-022`: drop-in claim pressure.
> * `CA-023`: product-memory promotion pressure.
> * `CA-024`: reporting output would become canonical state.
> * `CA-025`: unsupported surface would be silently ignored.
>
> S12B must mark every case as design-only.
>
> ### Required file: `docs/adapters/V5_CODEX_CONSENT_NON_CANONICAL_REPORTING_SPEC.md`
>
> Purpose: define future reporting boundaries for consent validation and abort reports.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Consent Non-Canonical Reporting Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Reporting Problem Statement
> ## Reporting Principles
> ## Consent Report Type Model
> ## Required Consent Report Fields
> ## Abort Report Fields
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
> * State that S12B creates no consent report.
> * Define future report types:
>
>   * `consent-schema-review-report`
>   * `consent-validation-report`
>   * `consent-revocation-report`
>   * `consent-expiration-report`
>   * `consent-abort-report`
> * State that reports are not PAI Memory, ISA, Pulse state, Claude memory, Codex memory, manifests, runtime payloads, or proof that Codex is drop-in.
> * Define required future report fields:
>
>   * `report_id`
>   * `report_type`
>   * `consent_id`
>   * `source_kind`
>   * `source_root`
>   * `pai_dir_candidate`
>   * `allowed_reads`
>   * `forbidden_reads`
>   * `forbidden_writes`
>   * `runtime_prohibitions`
>   * `consent_status`
>   * `validation_status`
>   * `abort_required`
>   * `failure_reason`
>   * `denied_action_report`
>   * `unsupported_surface_report`
>   * `pulse_status`
>   * `memory_status`
>   * `isa_status`
>   * `product_memory_status`
>   * `drop_in_claim_status`
>   * `non_canonical_statement`
>   * `retention_policy`
>   * `provenance`
>
> ### Required file: `docs/adapters/V5_CODEX_S12B_DECISION_LOG.md`
>
> Purpose: record S12B decisions, non-decisions, blocked decisions, and future architect questions.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex S12B Decision Log
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Decisions Made in S12B
> ## Non-Decisions in S12B
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
> S12B-D01 Codex remains not drop-in today.
> S12B-D02 S12B designs consent artifact schema only.
> S12B-D03 S12B creates no actual consent artifact.
> S12B-D04 S12B implements no consent validator.
> S12B-D05 Future consent must be explicit and source-specific.
> S12B-D06 Future consent must be revocable and expiring.
> S12B-D07 Consent cannot be inferred from Claude Code installation.
> S12B-D08 Consent cannot be inferred from Codex installation.
> S12B-D09 Consent cannot be inferred from dual subscriptions.
> S12B-D10 Consent does not authorize PAI Memory writes.
> S12B-D11 Consent does not authorize ISA writes.
> S12B-D12 Consent does not authorize Pulse startup or endpoint calls.
> S12B-D13 Consent does not authorize product-memory reads or promotion by default.
> S12B-D14 Consent does not authorize root AGENTS.md or .codex writes.
> S12B-D15 Consent reporting must be non-canonical.
> S12B-D16 Future consent validation must abort on ambiguity, revocation, expiration, write pressure, Pulse pressure, product-memory pressure, runtime pressure, or drop-in claim pressure.
> S12B-D17 S12B does not approve live existing-local-v5 reads.
> S12B-D18 Runtime adapter planning remains blocked.
> ```
>
> The `## Next Milestone Candidates` section must list advisory-only options, not approvals:
>
> * `V5-S12C`: PAI_DIR detection dry-run design.
> * `V5-S12D`: Live-read-only preflight report design.
> * `V5-S12E`: S12 closeout and S13 proposed contract.
> * `V5-S13A`: First approved live-read-only trial, only after S12 readiness is accepted.
> * `V5-S13B`: Runtime adapter planning, only after live-read-only evidence is accepted.
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
> S12B fails immediately if:
>
> * Any file outside the approved write set is created or modified.
> * Any fixture, harness, generator, evaluator, report, README, or release file is modified.
> * Any protected file is modified.
> * Runtime adapter files are created.
> * Root `AGENTS.md` is created or modified.
> * `.codex/` is created or modified.
> * Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, manifest instances, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures are created.
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
> * The goal advances beyond S12B.
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
> Run changed-file check, heading check, content invariant check, no-test-change check, and protected-path check as specified by the S12B card.
>
> ### Acceptance criteria
>
> S12B is complete only if:
>
> * Exactly the six approved S12B docs are created or modified.
> * No fixture, harness, generator, evaluator, report, README, release, or runtime file is modified.
> * No protected files are changed.
> * No runtime adapter files are created.
> * No root `AGENTS.md` is created or modified.
> * No `.codex/` files are created or modified.
> * No Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, manifest instances, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures are created.
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
> * `V5_S12B_EXEC_PLAN.md` contains the Completion Contract copied into its `## Completion Contract` section.
> * The schema proposal states that S12B creates no actual consent artifact.
> * The validation spec states that S12B implements no validator.
> * The failure cases doc includes all required `CA-001` through `CA-025` abort IDs.
> * The reporting spec states that S12B creates no consent report.
> * The decision log includes all required `S12B-D01` through `S12B-D18` decisions.
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
> No — only the six approved S12B documentation files were created or modified.
> ```
>
> `Recommended next architect decision` must be advisory only. Do not begin S12C, S12D, S13A, or runtime adapter work.
>
> ### Stop conditions
>
> Stop and report immediately if:
>
> * Any protected file must be edited.
> * Any file outside the approved write set is modified.
> * Any test fixture, harness, generator, evaluator, report, README, or release file would need to be modified.
> * Runtime implementation seems necessary.
> * A consent artifact would need to be created.
> * A consent validator would need to be created.
> * Root `AGENTS.md` or `.codex/` would need to be modified.
> * A Codex config, hook, rule, skill, subagent, agent, command, launcher, installer, wrapper, generated runtime config, migration script, adapter payload, Memory payload, ISA payload, Pulse payload, Pulse bridge file, consent artifact, manifest instance, executable schema, live-trial artifact, runtime payload, or committed negative fixture would need to be created.
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
> * The goal tries to continue beyond S12B.
> * The Completion Contract cannot be copied into the execution plan.
> * The self-review cannot reach 94/100 without leaving scope.

## Milestones

1. Baseline status check.
2. S11/S12A reread.
3. Consent artifact schema proposal drafting.
4. Consent validation and revocation spec drafting.
5. Consent failure and abort case drafting.
6. Consent non-canonical reporting spec drafting.
7. Decision log drafting.
8. Protected-path and no-extra-file validation.
9. Self-review and repair.
10. Final handoff and goal-state report.

## Self-Review Rubric

| Area | Points |
| --- | ---: |
| Scope and protected-path discipline | 15 |
| Evidence discipline | 10 |
| Consent artifact schema quality | 25 |
| Validation, revocation, and expiration quality | 20 |
| Failure, abort, and reporting boundary quality | 15 |
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

- Any file outside the approved S12B write set changes.
- Any fixture, harness, generator, evaluator, report, README, release, protected, or runtime file changes.
- Any actual consent artifact or consent validator is created.
- Any live read-only trial, live existing-local-v5 read, private user-local read, Pulse start/call, PAI Memory write, ISA write, Claude Code invocation, or Codex runtime invocation occurs.
- Any runtime adapter file, root `AGENTS.md`, `.codex/`, manifest, schema, audit artifact, live-trial artifact, runtime payload, Memory payload, ISA payload, Pulse payload, report, fixture, or committed negative fixture is created.
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

- Baseline status check: completed before S12B file creation; worktree was clean.
- Required source existence checks: completed before S12B file creation.
- Existing S10/S11 validations: completed before S12B file creation; harness, negative-control self-test, no-residue self-test, report-generator self-test, S11A report generation, and S11C readiness evaluation passed.
- S11/S12A reread: completed using repository-local S12A consent, PAI_DIR/source-selection, reporting, and decision docs.
- Consent artifact schema proposal drafting: completed in `docs/adapters/V5_CODEX_CONSENT_ARTIFACT_SCHEMA_PROPOSAL.md`.
- Consent validation and revocation spec drafting: completed in `docs/adapters/V5_CODEX_CONSENT_VALIDATION_AND_REVOCATION_SPEC.md`.
- Consent failure and abort case drafting: completed in `docs/adapters/V5_CODEX_CONSENT_FAILURE_AND_ABORT_CASES.md`.
- Consent non-canonical reporting spec drafting: completed in `docs/adapters/V5_CODEX_CONSENT_NON_CANONICAL_REPORTING_SPEC.md`.
- Decision log drafting: completed in `docs/adapters/V5_CODEX_S12B_DECISION_LOG.md`.
- Final validation execution: completed; all required validation commands and content checks passed.

## Iteration Log

Iteration 1 self-review score: 100/100. Hard failures: 0.

| Area | Points | Result |
| --- | ---: | --- |
| Scope and protected-path discipline | 15/15 | Only the six approved S12B docs are changed; protected-path check has no output. |
| Evidence discipline | 10/10 | Source material is limited to repository-local S10/S11/S12A docs and fixture evidence. |
| Consent artifact schema quality | 25/25 | Schema proposal is markdown-only, includes all required fields, source kinds, non-canonical rules, and non-executable example. |
| Validation, revocation, and expiration quality | 20/20 | Validation spec covers statuses, outputs, revocation, expiration, replay protection, consistency checks, and abort rules. |
| Failure, abort, and reporting boundary quality | 15/15 | Failure cases include `CA-001` through `CA-025`; reporting spec preserves non-canonical boundaries. |
| Memory, ISA, Pulse, product-memory, and no-live-read safety | 10/10 | PAI Memory, ISA, Pulse, product memory, live user-local, and existing-local-v5 boundaries are denied by default. |
| Verification quality | 5/5 | Required validation commands, changed-file, heading, content invariant, no-test-change, and protected-path checks pass. |

## Surprises & Discoveries

- The local sandbox wrapper may return `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; repository-local validation commands were rerun outside the broken sandbox using explicit escalations when needed.
- S12A already preserved consent as explicit, source-specific, revocable, and no-write; S12B narrows that design into future schema and validation documentation only.

## Decision Log

- Use documentation-only S12B deliverables and do not create actual consent artifacts, validators, reports, fixtures, schemas, manifests, or runtime payloads.
- Treat any future consent artifact as non-canonical and not proof that Codex is drop-in.
- Treat validation, revocation, expiration, replay protection, and abort behavior as future design only.

## Outcomes & Retrospective

Validation results recorded:

- `git status --short`: only the six approved S12B docs.
- `git diff --name-only | sort`: only the six approved S12B docs.
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

S12B remains documentation/design only. It does not create an actual consent artifact, create a consent validator, create a consent report, run a live read-only trial, read live existing-local-v5 state, inspect private user-local state, implement a runtime adapter, create root `AGENTS.md`, create `.codex/`, start or call Pulse, write PAI Memory, write ISA, authorize product-memory promotion, or claim Codex is drop-in today.
