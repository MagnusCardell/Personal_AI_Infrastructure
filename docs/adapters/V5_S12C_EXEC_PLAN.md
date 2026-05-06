# V5-S12C Execution Plan

## Purpose

Execute V5-S12C PAI_DIR Detection Dry-Run Design. S12C designs the future PAI_DIR detection dry-run model, source-root classification rules, no-default-live-read guarantees, and dry-run evidence requirements.

Codex is not currently proven drop-in for existing local PAI v5 files. S12C is documentation/design only. It does not implement a detector, create a detector script, create a consent artifact, create a consent validator, run a live read-only trial, read live existing-local-v5 state, inspect private user-local state, or implement runtime adapter behavior.

## Scope

In scope:

- Create this S12C execution plan.
- Create the PAI_DIR dry-run detection model.
- Create the source-root classification and guardrail spec.
- Create the PAI_DIR detection failure cases document.
- Create the PAI_DIR dry-run reporting spec.
- Create the S12C decision log.
- Run and record all required validation commands.

Out of scope:

- Detector implementation or detector scripts.
- Consent artifacts or consent validators.
- Live read-only trials or live existing-local-v5 access.
- Inspection of live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, private user-local state, or the user's second personal clone.
- Fixture, harness, generator, evaluator, report, README, release, protected-path, runtime, or adapter file edits.
- Root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures.

## Approved Write Set

Create exactly these files:

- `docs/adapters/V5_S12C_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_DETECTION_MODEL.md`
- `docs/adapters/V5_CODEX_SOURCE_ROOT_CLASSIFICATION_AND_GUARDRAIL_SPEC.md`
- `docs/adapters/V5_CODEX_PAI_DIR_DETECTION_FAILURE_CASES.md`
- `docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_REPORTING_SPEC.md`
- `docs/adapters/V5_CODEX_S12C_DECISION_LOG.md`

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
- Any second/personal clone outside this repository.

## Source Protocol

Allowed sources:

- S0-S12B adapter docs for prior adapter conclusions.
- Existing S10/S11 fixture and evidence files.
- Repository-local PAI v5 release files for PAI facts only if needed.
- Official OpenAI Codex docs only if S12C adds or refreshes a Codex capability claim.
- Local `codex --version` or `codex --help` only if already available and non-invasive.

Forbidden sources and operations:

- Unofficial Codex capability sources.
- Inferred current Codex behavior from memory.
- Live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, private user-local state, or any second/personal clone outside this repository.
- Live existing-local-v5 state.
- Pulse startup, Pulse endpoint calls, or `localhost:31337` probes.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, and Codex hook/rule/execpolicy commands.

## Source Material

Baseline discovery before S12C edits:

- `git status --short`: no output.
- Required S12A consent, PAI_DIR/source-selection, S12B schema, validation, failure, and decision docs existed.
- `Releases/v5.0.0/.claude` existed as repository-local release fixture material.
- Existing harness validation passed with `fixture_count: 12`, `case_count: 12`, `coverage_id_count: 25`, `gate_id_count: 20`, and `status: pass`.
- Existing harness negative-control self-test passed with `negative_control_count: 60`.
- Existing no-residue self-test passed.
- Existing report-generator negative-control self-test passed with `negative_control_count: 16`.

S12A/S12B source reread:

- Future PAI_DIR detection must be read-only, dry-run, path-bounded, abortable, consent-bound, and architect-approved.
- No default live local read is allowed.
- `existing-local-v5-read-only` remains future-only and requires explicit user consent plus architect approval.
- Consent validation must abort on missing, revoked, expired, ambiguous, mismatched, replayed, overbroad, write-authorizing, Pulse-authorizing, Memory/ISA-authorizing, product-memory-authorizing, runtime-authorizing, or drop-in-claiming consent.
- Product memory reads remain denied by default, Pulse startup/calls remain denied, and PAI Memory and ISA writes remain denied.

## Completion Contract

> # V5-S12C PAI_DIR Detection Dry-Run Design
>
> ## Role
>
> You are implementing an architect-issued documentation/design milestone for adapting PAI v5.0.0 so Codex can eventually become a drop-in-capable local runtime engine.
>
> S12A designed consent, source-selection, PAI_DIR detection constraints, preflight, abort, and reporting boundaries.
>
> S12B designed future consent artifact schema, validation, revocation, expiration, and abort cases.
>
> S12C designs the future PAI_DIR detection dry-run model, source-root classification rules, no-default-live-read guarantees, and dry-run evidence requirements.
>
> This is documentation/design only.
>
> This is not a live read-only trial.
>
> This is not runtime adapter implementation.
>
> Do not implement a detector.
>
> Do not create a detector script.
>
> Do not create a consent artifact.
>
> Do not create a consent validator.
>
> Do not inspect live `~/.claude/PAI`.
>
> Do not inspect live `~/.claude/projects`.
>
> Do not inspect live `~/.codex`.
>
> Do not inspect the user's second personal clone unless it is explicitly provided inside this repository and approved by a future architect card.
>
> Do not run a live read-only trial.
>
> Do not implement the Codex adapter.
>
> Do not create root `AGENTS.md`.
>
> Do not create `.codex/`.
>
> Do not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, runtime files, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures.
>
> Do not modify release files.
>
> Do not start Pulse.
>
> Do not call Pulse endpoints.
>
> Do not probe `localhost:31337`.
>
> Do not run installers.
>
> Do not run Codex import or migration tooling.
>
> Do not invoke Claude Code.
>
> Do not invoke Codex as a runtime engine except for non-invasive `codex --version` or `codex --help` if already available.
>
> Do not run Codex hook, rule, execpolicy, or runtime commands.
>
> ## Start the goal
>
> Start exactly one bounded goal:
>
> ```text
> /goal Execute V5-S12C PAI_DIR Detection Dry-Run Design. Treat the Completion Contract in this prompt as the authoritative self-evaluation contract. First create docs/adapters/V5_S12C_EXEC_PLAN.md and copy the Completion Contract into it verbatim. Then create only docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_DETECTION_MODEL.md, docs/adapters/V5_CODEX_SOURCE_ROOT_CLASSIFICATION_AND_GUARDRAIL_SPEC.md, docs/adapters/V5_CODEX_PAI_DIR_DETECTION_FAILURE_CASES.md, docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_REPORTING_SPEC.md, and docs/adapters/V5_CODEX_S12C_DECISION_LOG.md. Do not mark the goal complete until every validation command in the Completion Contract passes, the execution plan records the results, and the final handoff reports the same checks. Do not modify files outside the approved write set. Do not advance beyond V5-S12C.
> ```
>
> After final handoff, report whether `/goal clear` was completed, unavailable, or not applicable.
>
> ## Approved write set
>
> Create exactly these files:
>
> * `docs/adapters/V5_S12C_EXEC_PLAN.md`
> * `docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_DETECTION_MODEL.md`
> * `docs/adapters/V5_CODEX_SOURCE_ROOT_CLASSIFICATION_AND_GUARDRAIL_SPEC.md`
> * `docs/adapters/V5_CODEX_PAI_DIR_DETECTION_FAILURE_CASES.md`
> * `docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_REPORTING_SPEC.md`
> * `docs/adapters/V5_CODEX_S12C_DECISION_LOG.md`
>
> No other files may be created or modified.
>
> ## Approved read set
>
> Read but do not modify:
>
> * all `docs/adapters/V5_*.md`
> * `tests/adapters/v5-codex-readonly-fixture-trial/`
> * `Releases/v5.0.0/`
> * `Releases/v5.0.0/.claude/`
>
> Do not read:
>
> * `~/.claude/`
> * `~/.claude/PAI/`
> * `~/.claude/projects/`
> * `~/.codex/`
> * `~/.codex/memories/`
> * any second/personal clone outside this repository
>
> ## Source protocol
>
> Use only:
>
> 1. S0-S12B adapter docs for prior adapter conclusions.
> 2. Existing S10/S11 fixture and evidence files.
> 3. Repository-local PAI v5 release files for PAI facts only if needed.
> 4. Official OpenAI Codex docs only if S12C adds or refreshes a Codex capability claim.
> 5. Local `codex --version` or `codex --help` only if already available and non-invasive.
>
> Do not use unofficial Codex capability sources.
>
> Do not infer current Codex behavior from memory.
>
> ## Completion Contract
>
> This Completion Contract is the authoritative contract for V5-S12C.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S12C_EXEC_PLAN.md`.
>
> Do not mark S12C complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S12C deliverables must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S12C designs future PAI_DIR detection dry-run behavior only.
> * S12C does not implement a detector.
> * S12C does not create a detector script.
> * S12C does not create a consent artifact.
> * S12C does not create a consent validator.
> * S12C does not run a live read-only trial.
> * S12C does not read live existing-local-v5 state.
> * S12C does not read live user-local state.
> * S12C does not inspect live `~/.claude/PAI`.
> * S12C does not inspect live `~/.claude/projects`.
> * S12C does not inspect live `~/.codex`.
> * S12C does not inspect the user's second personal clone.
> * S12C does not implement a Codex runtime adapter.
> * S12C does not create runtime adapter files.
> * S12C does not create root `AGENTS.md`.
> * S12C does not create `.codex/`.
> * S12C does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures.
> * Future dry-run detection output is not PAI Memory.
> * Future dry-run detection output is not ISA.
> * Future dry-run detection output is not Pulse state.
> * Future dry-run detection output is not Claude memory.
> * Future dry-run detection output is not Codex memory.
> * Future dry-run detection output is not a manifest.
> * Future dry-run detection output is not runtime payload.
> * Future dry-run detection output is not proof that Codex is drop-in.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Product memories must not be silently promoted into PAI Memory.
> * Pulse is central v5 infrastructure, but S12C does not start Pulse, call Pulse endpoints, or claim Pulse parity.
> * Future live read-only access requires explicit user consent design and architect approval.
> * Future live read-only access must not require uninstalling Claude Code.
> * Future live read-only access must not write PAI Memory or ISA.
> * Future live read-only access must not start Pulse or call Pulse endpoints unless separately approved.
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
> test -f docs/adapters/V5_CODEX_CONSENT_ARTIFACT_SCHEMA_PROPOSAL.md
> test -f docs/adapters/V5_CODEX_CONSENT_VALIDATION_AND_REVOCATION_SPEC.md
> test -f docs/adapters/V5_CODEX_CONSENT_FAILURE_AND_ABORT_CASES.md
> test -f docs/adapters/V5_CODEX_S12B_DECISION_LOG.md
> test -d Releases/v5.0.0/.claude
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
> Do not inspect any second/personal clone.
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
> ### Required file: `docs/adapters/V5_S12C_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S12C Execution Plan
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
> 2. S12A/S12B reread.
> 3. PAI_DIR dry-run detection model drafting.
> 4. Source-root classification and guardrail spec drafting.
> 5. Detection failure cases drafting.
> 6. Dry-run reporting spec drafting.
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
> | PAI_DIR dry-run model quality                               |     25 |
> | Source-root classification and guardrail quality            |     20 |
> | Failure cases and reporting boundary quality                |     15 |
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
> ### Required file: `docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_DETECTION_MODEL.md`
>
> Purpose: define future PAI_DIR dry-run detection behavior without implementing or executing detection.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex PAI_DIR Dry-Run Detection Model
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Detection Problem Statement
> ## Dry-Run Detection Principles
> ## Detection Input Model
> ## Detection Output Model
> ## PAI_DIR Candidate Model
> ## Consent Dependency Model
> ## Source Selection Dependency Model
> ## No-Default-Live-Read Model
> ## No-Write Detection Model
> ## Product Memory Boundary
> ## Pulse Boundary
> ## Memory and ISA Boundary
> ## Abort and Failure Model
> ## Required Future Proofs
> ## Prohibited Detection Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * State that S12C does not implement detection.
> * State that S12C does not inspect live `PAI_DIR`.
> * State that future detection is dry-run, read-only, consent-bound, source-specific, path-bounded, abortable, and non-canonical.
> * Define future detection inputs:
>
>   * consent artifact reference;
>   * declared source kind;
>   * declared source root;
>   * expected `PAI_DIR` candidate;
>   * allowed read scope;
>   * forbidden read scope;
>   * forbidden write scope;
>   * runtime prohibition policy;
>   * product memory policy;
>   * Pulse policy;
>   * Memory policy;
>   * ISA policy.
> * Define future detection outputs:
>
>   * `detection_id`
>   * `source_kind`
>   * `declared_source_root`
>   * `pai_dir_candidate`
>   * `candidate_status`
>   * `confidence`
>   * `allowed_reads`
>   * `forbidden_reads`
>   * `forbidden_writes`
>   * `abort_required`
>   * `failure_reason`
>   * `non_canonical_statement`
> * State that detection output is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.
>
> ### Required file: `docs/adapters/V5_CODEX_SOURCE_ROOT_CLASSIFICATION_AND_GUARDRAIL_SPEC.md`
>
> Purpose: define future source-root classes, allowed/denied root behavior, and guardrails.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Source Root Classification and Guardrail Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Classification Problem Statement
> ## Source Root Classification Model
> ## Release Fixture Source Rules
> ## Sanitized User Fixture Source Rules
> ## Existing Local v5 Source Rules
> ## Personal Clone Boundary Rules
> ## Allowed Root Patterns
> ## Forbidden Root Patterns
> ## Guardrail Model
> ## Product Memory Guardrails
> ## Pulse Guardrails
> ## Memory and ISA Guardrails
> ## Runtime Guardrails
> ## Required Future Proofs
> ## Prohibited Classification Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * Define source root classes:
>
>   * `release-fixture`
>   * `sanitized-user-fixture`
>   * `existing-local-v5-read-only`
>   * `personal-clone-read-only`
>   * `unknown`
> * State that `existing-local-v5-read-only` and `personal-clone-read-only` are future-only and require explicit architect approval plus explicit user consent.
> * State that S12C does not inspect any personal clone.
> * State that a clean cloned repo without installer-run PAI state can be classified only from repository-local evidence in S12C.
> * Define forbidden root patterns:
>
>   * `~/.claude`
>   * `~/.claude/PAI`
>   * `~/.claude/projects`
>   * `~/.codex`
>   * `~/.codex/memories`
>   * arbitrary home-directory scans
>   * root `AGENTS.md`
>   * `.codex/`
>   * `Releases/` writes
> * State no root is read by default.
> * State no source-root classification may imply permission to write.
>
> ### Required file: `docs/adapters/V5_CODEX_PAI_DIR_DETECTION_FAILURE_CASES.md`
>
> Purpose: define future failure and abort cases for PAI_DIR detection and source-root selection.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex PAI_DIR Detection Failure Cases
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Failure Case Philosophy
> ## Consent-Related Failures
> ## Source-Root Failures
> ## PAI_DIR Candidate Failures
> ## Product Memory Failures
> ## Pulse Failures
> ## Memory and ISA Failures
> ## Runtime Invocation Failures
> ## Reporting Failures
> ## Detection Failure Table
> ## Required Future Proofs
> ## Prohibited Failure Handling Designs
> ## Non-Goals
> ```
>
> Required content:
>
> Include a detection failure table with columns:
>
> ```text
> Failure ID | Failure class | Trigger | Required response | Reported evidence | Future proof required | S12C status
> ```
>
> Minimum failure IDs:
>
> * `PD-001`: missing consent reference.
> * `PD-002`: consent source kind mismatch.
> * `PD-003`: consent source root mismatch.
> * `PD-004`: source root ambiguous.
> * `PD-005`: source root outside allowed scope.
> * `PD-006`: source root is arbitrary home directory.
> * `PD-007`: attempted default read of `~/.claude/PAI`.
> * `PD-008`: attempted read of `~/.claude/projects`.
> * `PD-009`: attempted read of `~/.codex`.
> * `PD-010`: attempted product memory read.
> * `PD-011`: attempted Pulse startup.
> * `PD-012`: attempted Pulse endpoint call.
> * `PD-013`: PAI Memory write pressure.
> * `PD-014`: ISA write pressure.
> * `PD-015`: root `AGENTS.md` write pressure.
> * `PD-016`: `.codex/` write pressure.
> * `PD-017`: personal clone accessed without approval.
> * `PD-018`: clean clone mistaken for live PAI install.
> * `PD-019`: `PAI_DIR` confidence insufficient.
> * `PD-020`: detector would need runtime adapter execution.
> * `PD-021`: detector would need Claude Code invocation.
> * `PD-022`: detector would need Codex runtime invocation.
> * `PD-023`: detector output would become canonical state.
> * `PD-024`: unsupported surface silently ignored.
> * `PD-025`: drop-in claim pressure.
>
> S12C must mark every case as design-only.
>
> ### Required file: `docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_REPORTING_SPEC.md`
>
> Purpose: define future non-canonical reporting for PAI_DIR dry-run detection.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex PAI_DIR Dry-Run Reporting Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Reporting Problem Statement
> ## Reporting Principles
> ## Report Type Model
> ## Required Report Fields
> ## Candidate Reporting
> ## Confidence Reporting
> ## Abort Reporting
> ## Denied Action Reporting
> ## Unsupported Surface Reporting
> ## Non-Canonical Output Rules
> ## Privacy and Retention Rules
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
> * State that S12C creates no detection report.
> * Define future report types:
>
>   * `pai-dir-dry-run-report`
>   * `source-root-classification-report`
>   * `pai-dir-abort-report`
>   * `pai-dir-confidence-report`
> * Define required future report fields:
>
>   * `report_id`
>   * `report_type`
>   * `detection_id`
>   * `source_kind`
>   * `declared_source_root`
>   * `pai_dir_candidate`
>   * `candidate_status`
>   * `confidence`
>   * `consent_reference`
>   * `allowed_reads`
>   * `forbidden_reads`
>   * `forbidden_writes`
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
>   * `provenance`
> * State reports are not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.
>
> ### Required file: `docs/adapters/V5_CODEX_S12C_DECISION_LOG.md`
>
> Purpose: record S12C decisions, non-decisions, blocked decisions, and future architect questions.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex S12C Decision Log
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Decisions Made in S12C
> ## Non-Decisions in S12C
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
> S12C-D01 Codex remains not drop-in today.
> S12C-D02 S12C designs PAI_DIR dry-run detection only.
> S12C-D03 S12C implements no detector.
> S12C-D04 S12C reads no live PAI_DIR.
> S12C-D05 S12C does not inspect the personal clone.
> S12C-D06 Clean clone status does not imply live PAI install.
> S12C-D07 Future detection must be consent-bound.
> S12C-D08 Future detection must be source-specific.
> S12C-D09 Future detection must be abortable.
> S12C-D10 Future detection output is non-canonical.
> S12C-D11 Existing-local-v5-read-only remains future-only.
> S12C-D12 Personal-clone-read-only remains future-only.
> S12C-D13 Product memory reads remain denied by default.
> S12C-D14 Pulse startup and endpoint calls remain denied.
> S12C-D15 PAI Memory and ISA writes remain denied.
> S12C-D16 Root AGENTS.md and .codex remain protected.
> S12C-D17 Future detector validation must prove no default home scan.
> S12C-D18 Runtime adapter planning remains blocked.
> ```
>
> The `## Next Milestone Candidates` section must list advisory-only options, not approvals:
>
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
> S12C fails immediately if:
>
> * Any file outside the approved write set is created or modified.
> * Any fixture, harness, generator, evaluator, report, README, or release file is modified.
> * Any protected file is modified.
> * Runtime adapter files are created.
> * A detector script is created.
> * Root `AGENTS.md` is created or modified.
> * `.codex/` is created or modified.
> * Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures are created.
> * A live read-only trial is run.
> * Private user-local state is inspected or modified.
> * Live existing-local-v5 state is read.
> * `~/.claude/PAI` is inspected.
> * `~/.claude/projects` is inspected.
> * `~/.codex` is inspected.
> * The user's second personal clone is inspected.
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
> * The docs authorize personal-clone access.
> * The docs imply Claude-shaped files can be copied directly into Codex surfaces.
> * The docs authorize product-memory promotion into PAI Memory.
> * The docs authorize dual-engine uncoordinated writes.
> * The goal advances beyond S12C.
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
> Run changed-file check, heading check, content invariant check, no-test-change check, and protected-path check exactly as specified by the S12C card.
>
> ### Acceptance criteria
>
> S12C is complete only if exactly the six approved S12C docs are created or modified; no fixture, harness, generator, evaluator, report, README, release, or runtime file is modified; no protected files are changed; no detector script is created; no runtime adapter files are created; no root `AGENTS.md` or `.codex/` files are created or modified; no Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures are created; no live read-only trial is run; no private user-local state or live existing-local-v5 state is read; `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, and the user's second personal clone are not inspected; PAI Memory and ISA are not written; Pulse is not started or called; `localhost:31337` is not probed; installers, Claude Code, Codex runtime, Codex import/migration tooling, and Codex hook/rule/execpolicy commands are not run; the execution plan contains the Completion Contract; the detection model states S12C does not implement detection or inspect live `PAI_DIR`; the source-root spec states S12C does not inspect any personal clone; the failure cases doc includes `PD-001` through `PD-025`; the reporting spec states S12C creates no detection report; the decision log includes `S12C-D01` through `S12C-D18`; changed-file, heading, content invariant, no-test-change, and protected-path checks pass; deliverables do not claim Codex is drop-in today or official upstream engine; deliverables do not authorize PAI Memory writes, ISA writes, Pulse startup/calls, Pulse implementation, existing-local-v5 trial execution, personal-clone access, product-memory promotion, or dual-engine uncoordinated writes; deliverables do not imply Claude-shaped files can be copied directly into Codex surfaces; and the execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures.
>
> ## Final handoff format
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
> No — only the six approved S12C documentation files were created or modified.
> ```
>
> `Recommended next architect decision` must be advisory only. Do not begin S12D, S12E, S13A, or runtime adapter work.
>
> ## Stop conditions
>
> Stop and report immediately if:
>
> * Any protected file must be edited.
> * Any file outside the approved write set is modified.
> * Any test fixture, harness, generator, evaluator, report, README, or release file would need to be modified.
> * Runtime implementation seems necessary.
> * A detector script would need to be created.
> * A consent artifact would need to be created.
> * A consent validator would need to be created.
> * Root `AGENTS.md` or `.codex/` would need to be modified.
> * A Codex config, hook, rule, skill, subagent, agent, command, launcher, installer, wrapper, generated runtime config, migration script, adapter payload, Memory payload, ISA payload, Pulse payload, Pulse bridge file, consent artifact, manifest instance, executable schema, live-trial artifact, runtime payload, report, fixture, or committed negative fixture would need to be created.
> * A live trial would need to be run.
> * PAI Memory would need to be written.
> * ISA would need to be written.
> * Existing-local-v5 state would need to be read.
> * `~/.claude/PAI` would need to be inspected.
> * `~/.claude/projects` would need to be inspected.
> * `~/.codex` would need to be inspected.
> * The user's second personal clone would need to be inspected.
> * Pulse would need to be started.
> * A Pulse endpoint would need to be called.
> * `localhost:31337` would need to be probed.
> * Upstream v5 would need to be patched.
> * Private user-local memory would need to be read.
> * Codex import/migration tooling seems necessary.
> * Claude Code would need to be invoked.
> * Codex would need to be invoked as a runtime engine.
> * Codex hook, rule, or execpolicy commands would need to be run.
> * The goal tries to continue beyond S12C.
> * The Completion Contract cannot be copied into the execution plan.
> * The self-review cannot reach 94/100 without leaving scope.

Unabridged Completion Contract source retained for audit:

> ## Completion Contract
>
> This Completion Contract is the authoritative contract for V5-S12C.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S12C_EXEC_PLAN.md`.
>
> Do not mark S12C complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S12C deliverables must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S12C designs future PAI_DIR detection dry-run behavior only.
> * S12C does not implement a detector.
> * S12C does not create a detector script.
> * S12C does not create a consent artifact.
> * S12C does not create a consent validator.
> * S12C does not run a live read-only trial.
> * S12C does not read live existing-local-v5 state.
> * S12C does not read live user-local state.
> * S12C does not inspect live `~/.claude/PAI`.
> * S12C does not inspect live `~/.claude/projects`.
> * S12C does not inspect live `~/.codex`.
> * S12C does not inspect the user’s second personal clone.
> * S12C does not implement a Codex runtime adapter.
> * S12C does not create runtime adapter files.
> * S12C does not create root `AGENTS.md`.
> * S12C does not create `.codex/`.
> * S12C does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures.
> * Future dry-run detection output is not PAI Memory.
> * Future dry-run detection output is not ISA.
> * Future dry-run detection output is not Pulse state.
> * Future dry-run detection output is not Claude memory.
> * Future dry-run detection output is not Codex memory.
> * Future dry-run detection output is not a manifest.
> * Future dry-run detection output is not runtime payload.
> * Future dry-run detection output is not proof that Codex is drop-in.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Product memories must not be silently promoted into PAI Memory.
> * Pulse is central v5 infrastructure, but S12C does not start Pulse, call Pulse endpoints, or claim Pulse parity.
> * Future live read-only access requires explicit user consent design and architect approval.
> * Future live read-only access must not require uninstalling Claude Code.
> * Future live read-only access must not write PAI Memory or ISA.
> * Future live read-only access must not start Pulse or call Pulse endpoints unless separately approved.
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
> test -f docs/adapters/V5_CODEX_CONSENT_ARTIFACT_SCHEMA_PROPOSAL.md
> test -f docs/adapters/V5_CODEX_CONSENT_VALIDATION_AND_REVOCATION_SPEC.md
> test -f docs/adapters/V5_CODEX_CONSENT_FAILURE_AND_ABORT_CASES.md
> test -f docs/adapters/V5_CODEX_S12B_DECISION_LOG.md
> test -d Releases/v5.0.0/.claude
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
> Do not inspect any second/personal clone.
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
> ### Required file: `docs/adapters/V5_S12C_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S12C Execution Plan
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
> 2. S12A/S12B reread.
> 3. PAI_DIR dry-run detection model drafting.
> 4. Source-root classification and guardrail spec drafting.
> 5. Detection failure cases drafting.
> 6. Dry-run reporting spec drafting.
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
> | PAI_DIR dry-run model quality                               |     25 |
> | Source-root classification and guardrail quality            |     20 |
> | Failure cases and reporting boundary quality                |     15 |
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
> ### Required file: `docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_DETECTION_MODEL.md`
>
> Purpose: define future PAI_DIR dry-run detection behavior without implementing or executing detection.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex PAI_DIR Dry-Run Detection Model
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Detection Problem Statement
> ## Dry-Run Detection Principles
> ## Detection Input Model
> ## Detection Output Model
> ## PAI_DIR Candidate Model
> ## Consent Dependency Model
> ## Source Selection Dependency Model
> ## No-Default-Live-Read Model
> ## No-Write Detection Model
> ## Product Memory Boundary
> ## Pulse Boundary
> ## Memory and ISA Boundary
> ## Abort and Failure Model
> ## Required Future Proofs
> ## Prohibited Detection Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * State that S12C does not implement detection.
> * State that S12C does not inspect live `PAI_DIR`.
> * State that future detection is dry-run, read-only, consent-bound, source-specific, path-bounded, abortable, and non-canonical.
> * Define future detection inputs:
>
>   * consent artifact reference;
>   * declared source kind;
>   * declared source root;
>   * expected `PAI_DIR` candidate;
>   * allowed read scope;
>   * forbidden read scope;
>   * forbidden write scope;
>   * runtime prohibition policy;
>   * product memory policy;
>   * Pulse policy;
>   * Memory policy;
>   * ISA policy.
> * Define future detection outputs:
>
>   * `detection_id`
>   * `source_kind`
>   * `declared_source_root`
>   * `pai_dir_candidate`
>   * `candidate_status`
>   * `confidence`
>   * `allowed_reads`
>   * `forbidden_reads`
>   * `forbidden_writes`
>   * `abort_required`
>   * `failure_reason`
>   * `non_canonical_statement`
> * State that detection output is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.
>
> ### Required file: `docs/adapters/V5_CODEX_SOURCE_ROOT_CLASSIFICATION_AND_GUARDRAIL_SPEC.md`
>
> Purpose: define future source-root classes, allowed/denied root behavior, and guardrails.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Source Root Classification and Guardrail Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Classification Problem Statement
> ## Source Root Classification Model
> ## Release Fixture Source Rules
> ## Sanitized User Fixture Source Rules
> ## Existing Local v5 Source Rules
> ## Personal Clone Boundary Rules
> ## Allowed Root Patterns
> ## Forbidden Root Patterns
> ## Guardrail Model
> ## Product Memory Guardrails
> ## Pulse Guardrails
> ## Memory and ISA Guardrails
> ## Runtime Guardrails
> ## Required Future Proofs
> ## Prohibited Classification Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * Define source root classes:
>
>   * `release-fixture`
>   * `sanitized-user-fixture`
>   * `existing-local-v5-read-only`
>   * `personal-clone-read-only`
>   * `unknown`
> * State that `existing-local-v5-read-only` and `personal-clone-read-only` are future-only and require explicit architect approval plus explicit user consent.
> * State that S12C does not inspect any personal clone.
> * State that a clean cloned repo without installer-run PAI state can be classified only from repository-local evidence in S12C.
> * Define forbidden root patterns:
>
>   * `~/.claude`
>   * `~/.claude/PAI`
>   * `~/.claude/projects`
>   * `~/.codex`
>   * `~/.codex/memories`
>   * arbitrary home-directory scans
>   * root `AGENTS.md`
>   * `.codex/`
>   * `Releases/` writes
> * State no root is read by default.
> * State no source-root classification may imply permission to write.
>
> ### Required file: `docs/adapters/V5_CODEX_PAI_DIR_DETECTION_FAILURE_CASES.md`
>
> Purpose: define future failure and abort cases for PAI_DIR detection and source-root selection.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex PAI_DIR Detection Failure Cases
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Failure Case Philosophy
> ## Consent-Related Failures
> ## Source-Root Failures
> ## PAI_DIR Candidate Failures
> ## Product Memory Failures
> ## Pulse Failures
> ## Memory and ISA Failures
> ## Runtime Invocation Failures
> ## Reporting Failures
> ## Detection Failure Table
> ## Required Future Proofs
> ## Prohibited Failure Handling Designs
> ## Non-Goals
> ```
>
> Required content:
>
> Include a detection failure table with columns:
>
> ```text
> Failure ID | Failure class | Trigger | Required response | Reported evidence | Future proof required | S12C status
> ```
>
> Minimum failure IDs:
>
> * `PD-001`: missing consent reference.
> * `PD-002`: consent source kind mismatch.
> * `PD-003`: consent source root mismatch.
> * `PD-004`: source root ambiguous.
> * `PD-005`: source root outside allowed scope.
> * `PD-006`: source root is arbitrary home directory.
> * `PD-007`: attempted default read of `~/.claude/PAI`.
> * `PD-008`: attempted read of `~/.claude/projects`.
> * `PD-009`: attempted read of `~/.codex`.
> * `PD-010`: attempted product memory read.
> * `PD-011`: attempted Pulse startup.
> * `PD-012`: attempted Pulse endpoint call.
> * `PD-013`: PAI Memory write pressure.
> * `PD-014`: ISA write pressure.
> * `PD-015`: root `AGENTS.md` write pressure.
> * `PD-016`: `.codex/` write pressure.
> * `PD-017`: personal clone accessed without approval.
> * `PD-018`: clean clone mistaken for live PAI install.
> * `PD-019`: `PAI_DIR` confidence insufficient.
> * `PD-020`: detector would need runtime adapter execution.
> * `PD-021`: detector would need Claude Code invocation.
> * `PD-022`: detector would need Codex runtime invocation.
> * `PD-023`: detector output would become canonical state.
> * `PD-024`: unsupported surface silently ignored.
> * `PD-025`: drop-in claim pressure.
>
> S12C must mark every case as design-only.
>
> ### Required file: `docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_REPORTING_SPEC.md`
>
> Purpose: define future non-canonical reporting for PAI_DIR dry-run detection.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex PAI_DIR Dry-Run Reporting Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Reporting Problem Statement
> ## Reporting Principles
> ## Report Type Model
> ## Required Report Fields
> ## Candidate Reporting
> ## Confidence Reporting
> ## Abort Reporting
> ## Denied Action Reporting
> ## Unsupported Surface Reporting
> ## Non-Canonical Output Rules
> ## Privacy and Retention Rules
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
> * State that S12C creates no detection report.
> * Define future report types:
>
>   * `pai-dir-dry-run-report`
>   * `source-root-classification-report`
>   * `pai-dir-abort-report`
>   * `pai-dir-confidence-report`
> * Define required future report fields:
>
>   * `report_id`
>   * `report_type`
>   * `detection_id`
>   * `source_kind`
>   * `declared_source_root`
>   * `pai_dir_candidate`
>   * `candidate_status`
>   * `confidence`
>   * `consent_reference`
>   * `allowed_reads`
>   * `forbidden_reads`
>   * `forbidden_writes`
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
>   * `provenance`
> * State reports are not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.
>
> ### Required file: `docs/adapters/V5_CODEX_S12C_DECISION_LOG.md`
>
> Purpose: record S12C decisions, non-decisions, blocked decisions, and future architect questions.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex S12C Decision Log
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Decisions Made in S12C
> ## Non-Decisions in S12C
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
> S12C-D01 Codex remains not drop-in today.
> S12C-D02 S12C designs PAI_DIR dry-run detection only.
> S12C-D03 S12C implements no detector.
> S12C-D04 S12C reads no live PAI_DIR.
> S12C-D05 S12C does not inspect the personal clone.
> S12C-D06 Clean clone status does not imply live PAI install.
> S12C-D07 Future detection must be consent-bound.
> S12C-D08 Future detection must be source-specific.
> S12C-D09 Future detection must be abortable.
> S12C-D10 Future detection output is non-canonical.
> S12C-D11 Existing-local-v5-read-only remains future-only.
> S12C-D12 Personal-clone-read-only remains future-only.
> S12C-D13 Product memory reads remain denied by default.
> S12C-D14 Pulse startup and endpoint calls remain denied.
> S12C-D15 PAI Memory and ISA writes remain denied.
> S12C-D16 Root AGENTS.md and .codex remain protected.
> S12C-D17 Future detector validation must prove no default home scan.
> S12C-D18 Runtime adapter planning remains blocked.
> ```
>
> The `## Next Milestone Candidates` section must list advisory-only options, not approvals:
>
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
> S12C fails immediately if:
>
> * Any file outside the approved write set is created or modified.
> * Any fixture, harness, generator, evaluator, report, README, or release file is modified.
> * Any protected file is modified.
> * Runtime adapter files are created.
> * A detector script is created.
> * Root `AGENTS.md` is created or modified.
> * `.codex/` is created or modified.
> * Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures are created.
> * A live read-only trial is run.
> * Private user-local state is inspected or modified.
> * Live existing-local-v5 state is read.
> * `~/.claude/PAI` is inspected.
> * `~/.claude/projects` is inspected.
> * `~/.codex` is inspected.
> * The user’s second personal clone is inspected.
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
> * The docs authorize personal-clone access.
> * The docs imply Claude-shaped files can be copied directly into Codex surfaces.
> * The docs authorize product-memory promotion into PAI Memory.
> * The docs authorize dual-engine uncoordinated writes.
> * The goal advances beyond S12C.
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
> Run changed-file check:
>
> ```bash
> python3 - <<'PY'
> import subprocess
>
> expected = {
>     "docs/adapters/V5_S12C_EXEC_PLAN.md",
>     "docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_DETECTION_MODEL.md",
>     "docs/adapters/V5_CODEX_SOURCE_ROOT_CLASSIFICATION_AND_GUARDRAIL_SPEC.md",
>     "docs/adapters/V5_CODEX_PAI_DIR_DETECTION_FAILURE_CASES.md",
>     "docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_REPORTING_SPEC.md",
>     "docs/adapters/V5_CODEX_S12C_DECISION_LOG.md",
> }
>
> actual = set(subprocess.check_output(["git", "diff", "--name-only"], text=True).splitlines())
> actual |= set(subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], text=True).splitlines())
>
> if actual != expected:
>     print("unexpected changed files")
>     print("expected:")
>     print("\n".join(sorted(expected)))
>     print("actual:")
>     print("\n".join(sorted(actual)))
>     raise SystemExit(1)
>
> print("changed files ok")
> PY
> ```
>
> Run heading check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
> import re
>
> required = {
>     "docs/adapters/V5_S12C_EXEC_PLAN.md": [
>         "# V5-S12C Execution Plan",
>         "## Purpose",
>         "## Scope",
>         "## Approved Write Set",
>         "## Protected Paths",
>         "## Source Protocol",
>         "## Source Material",
>         "## Completion Contract",
>         "## Milestones",
>         "## Self-Review Rubric",
>         "## Hard Failure Conditions",
>         "## Validation Commands",
>         "## Progress",
>         "## Iteration Log",
>         "## Surprises & Discoveries",
>         "## Decision Log",
>         "## Outcomes & Retrospective",
>     ],
>     "docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_DETECTION_MODEL.md": [
>         "# V5 Codex PAI_DIR Dry-Run Detection Model",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Detection Problem Statement",
>         "## Dry-Run Detection Principles",
>         "## Detection Input Model",
>         "## Detection Output Model",
>         "## PAI_DIR Candidate Model",
>         "## Consent Dependency Model",
>         "## Source Selection Dependency Model",
>         "## No-Default-Live-Read Model",
>         "## No-Write Detection Model",
>         "## Product Memory Boundary",
>         "## Pulse Boundary",
>         "## Memory and ISA Boundary",
>         "## Abort and Failure Model",
>         "## Required Future Proofs",
>         "## Prohibited Detection Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_SOURCE_ROOT_CLASSIFICATION_AND_GUARDRAIL_SPEC.md": [
>         "# V5 Codex Source Root Classification and Guardrail Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Classification Problem Statement",
>         "## Source Root Classification Model",
>         "## Release Fixture Source Rules",
>         "## Sanitized User Fixture Source Rules",
>         "## Existing Local v5 Source Rules",
>         "## Personal Clone Boundary Rules",
>         "## Allowed Root Patterns",
>         "## Forbidden Root Patterns",
>         "## Guardrail Model",
>         "## Product Memory Guardrails",
>         "## Pulse Guardrails",
>         "## Memory and ISA Guardrails",
>         "## Runtime Guardrails",
>         "## Required Future Proofs",
>         "## Prohibited Classification Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_PAI_DIR_DETECTION_FAILURE_CASES.md": [
>         "# V5 Codex PAI_DIR Detection Failure Cases",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Failure Case Philosophy",
>         "## Consent-Related Failures",
>         "## Source-Root Failures",
>         "## PAI_DIR Candidate Failures",
>         "## Product Memory Failures",
>         "## Pulse Failures",
>         "## Memory and ISA Failures",
>         "## Runtime Invocation Failures",
>         "## Reporting Failures",
>         "## Detection Failure Table",
>         "## Required Future Proofs",
>         "## Prohibited Failure Handling Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_REPORTING_SPEC.md": [
>         "# V5 Codex PAI_DIR Dry-Run Reporting Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Reporting Problem Statement",
>         "## Reporting Principles",
>         "## Report Type Model",
>         "## Required Report Fields",
>         "## Candidate Reporting",
>         "## Confidence Reporting",
>         "## Abort Reporting",
>         "## Denied Action Reporting",
>         "## Unsupported Surface Reporting",
>         "## Non-Canonical Output Rules",
>         "## Privacy and Retention Rules",
>         "## Pulse Reporting Boundary",
>         "## Memory and ISA Reporting Boundary",
>         "## Product Memory Reporting Boundary",
>         "## Drop-In Claim Reporting",
>         "## Required Future Proofs",
>         "## Prohibited Reporting Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_S12C_DECISION_LOG.md": [
>         "# V5 Codex S12C Decision Log",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Decisions Made in S12C",
>         "## Non-Decisions in S12C",
>         "## Blocked Decisions",
>         "## Future Architect Questions",
>         "## Decision Table",
>         "## Next Milestone Candidates",
>         "## Non-Goals",
>     ],
> }
>
> for file, expected in required.items():
>     lines = [line.rstrip() for line in Path(file).read_text(encoding="utf-8").splitlines()]
>     actual = [line for line in lines if re.match(r"^(#|##) [^#]", line)]
>
>     if actual != expected:
>         print(f"{file}: heading mismatch")
>         print("expected:")
>         print("\n".join(expected))
>         print("actual:")
>         print("\n".join(actual))
>         raise SystemExit(1)
>
> print("heading structure ok")
> PY
> ```
>
> Run content invariant check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> combined = "\n".join(Path(p).read_text(encoding="utf-8") for p in [
>     "docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_DETECTION_MODEL.md",
>     "docs/adapters/V5_CODEX_SOURCE_ROOT_CLASSIFICATION_AND_GUARDRAIL_SPEC.md",
>     "docs/adapters/V5_CODEX_PAI_DIR_DETECTION_FAILURE_CASES.md",
>     "docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_REPORTING_SPEC.md",
>     "docs/adapters/V5_CODEX_S12C_DECISION_LOG.md",
> ])
>
> required = [
>     "Codex is not currently proven drop-in",
>     "PAI_DIR",
>     "dry-run",
>     "consent-bound",
>     "source-specific",
>     "no default live",
>     "existing-local-v5-read-only",
>     "personal-clone-read-only",
>     "future-only",
>     "clean clone",
>     "not PAI Memory",
>     "not ISA",
>     "not Pulse state",
>     "not a manifest",
>     "not runtime payload",
>     "PAI Memory",
>     "ISA",
>     "Pulse",
>     "product memory",
>     "root AGENTS.md",
>     ".codex",
>     "architect approval",
> ]
>
> for term in required:
>     if term not in combined:
>         print(f"missing content invariant: {term}")
>         raise SystemExit(1)
>
> for i in range(1, 26):
>     term = f"PD-{i:03d}"
>     if term not in combined:
>         print(f"missing PAI_DIR detection failure ID: {term}")
>         raise SystemExit(1)
>
> for i in range(1, 19):
>     term = f"S12C-D{i:02d}"
>     if term not in combined:
>         print(f"missing S12C decision ID: {term}")
>         raise SystemExit(1)
>
> print("content invariants ok")
> PY
> ```
>
> Run no-test-change and protected-path checks:
>
> ```bash
> python3 - <<'PY'
> import subprocess
>
> changed = set(subprocess.check_output(["git", "diff", "--name-only"], text=True).splitlines())
> changed |= set(subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], text=True).splitlines())
>
> for path in changed:
>     if path.startswith("tests/adapters/"):
>         print(f"unexpected test artifact change: {path}")
>         raise SystemExit(1)
>
> print("no test artifact changes ok")
> PY
>
> git status --short -- Releases/ .claude/ PAI/ CLAUDE.md AGENTS.md .codex/ install.sh settings.json hooks/ skills/ subagents/ agents/ commands/ .github/ .agents/
> ```
>
> Expected protected-path result: no output.
>
> ### Acceptance criteria
>
> S12C is complete only if:
>
> * Exactly the six approved S12C docs are created or modified.
> * No fixture, harness, generator, evaluator, report, README, release, or runtime file is modified.
> * No protected files are changed.
> * No detector script is created.
> * No runtime adapter files are created.
> * No root `AGENTS.md` is created or modified.
> * No `.codex/` files are created or modified.
> * No Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures are created.
> * No live read-only trial is run.
> * No private user-local state is inspected or modified.
> * No live existing-local-v5 state is read.
> * `~/.claude/PAI` is not inspected.
> * `~/.claude/projects` is not inspected.
> * `~/.codex` is not inspected.
> * The user’s second personal clone is not inspected.
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
> * `V5_S12C_EXEC_PLAN.md` contains the Completion Contract copied into its `## Completion Contract` section.
> * The detection model states that S12C does not implement detection or inspect live `PAI_DIR`.
> * The source-root spec states that S12C does not inspect any personal clone.
> * The failure cases doc includes all required `PD-001` through `PD-025` failure IDs.
> * The reporting spec states that S12C creates no detection report.
> * The decision log includes all required `S12C-D01` through `S12C-D18` decisions.
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
> * The deliverables do not authorize personal-clone access.
> * The deliverables do not imply Claude-shaped files can be copied directly into Codex surfaces.
> * The deliverables do not authorize product-memory promotion into PAI Memory.
> * The deliverables do not authorize dual-engine uncoordinated writes.
> * The execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures.
> * Final handoff reports every required validation command.
>
> ## Final handoff format
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
> No — only the six approved S12C documentation files were created or modified.
> ```
>
> `Recommended next architect decision` must be advisory only. Do not begin S12D, S12E, S13A, or runtime adapter work.
>
> ## Stop conditions
>
> Stop and report immediately if:
>
> * Any protected file must be edited.
> * Any file outside the approved write set is modified.
> * Any test fixture, harness, generator, evaluator, report, README, or release file would need to be modified.
> * Runtime implementation seems necessary.
> * A detector script would need to be created.
> * A consent artifact would need to be created.
> * A consent validator would need to be created.
> * Root `AGENTS.md` or `.codex/` would need to be modified.
> * A Codex config, hook, rule, skill, subagent, agent, command, launcher, installer, wrapper, generated runtime config, migration script, adapter payload, Memory payload, ISA payload, Pulse payload, Pulse bridge file, consent artifact, manifest instance, executable schema, live-trial artifact, runtime payload, report, fixture, or committed negative fixture would need to be created.
> * A live trial would need to be run.
> * PAI Memory would need to be written.
> * ISA would need to be written.
> * Existing-local-v5 state would need to be read.
> * `~/.claude/PAI` would need to be inspected.
> * `~/.claude/projects` would need to be inspected.
> * `~/.codex` would need to be inspected.
> * The user’s second personal clone would need to be inspected.
> * Pulse would need to be started.
> * A Pulse endpoint would need to be called.
> * `localhost:31337` would need to be probed.
> * Upstream v5 would need to be patched.
> * Private user-local memory would need to be read.
> * Codex import/migration tooling seems necessary.
> * Claude Code would need to be invoked.
> * Codex would need to be invoked as a runtime engine.
> * Codex hook, rule, or execpolicy commands would need to be run.
> * The goal tries to continue beyond S12C.
> * The Completion Contract cannot be copied into the execution plan.
> * The self-review cannot reach 94/100 without leaving scope.

## Milestones

1. Baseline status check.
2. S12A/S12B reread.
3. PAI_DIR dry-run detection model drafting.
4. Source-root classification and guardrail spec drafting.
5. Detection failure cases drafting.
6. Dry-run reporting spec drafting.
7. Decision log drafting.
8. Protected-path and no-extra-file validation.
9. Self-review and repair.
10. Final handoff and goal-state report.

## Self-Review Rubric

| Area | Points |
| --- | ---: |
| Scope and protected-path discipline | 15 |
| Evidence discipline | 10 |
| PAI_DIR dry-run model quality | 25 |
| Source-root classification and guardrail quality | 20 |
| Failure cases and reporting boundary quality | 15 |
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

- Any file outside the approved S12C write set changes.
- Any fixture, harness, generator, evaluator, report, README, release, protected, runtime, detector, consent artifact, or consent validator file changes or is created.
- Any live read-only trial, live existing-local-v5 read, private user-local read, personal clone inspection, Pulse start/call, PAI Memory write, ISA write, Claude Code invocation, or Codex runtime invocation occurs.
- Any deliverable claims Codex is drop-in today or official upstream engine, or authorizes live trials, runtime adapter work, personal-clone access, Pulse startup/calls, PAI Memory writes, ISA writes, existing-local-v5 access, product-memory promotion, or dual-engine uncoordinated writes.

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

- Baseline status check: completed before S12C file creation; worktree was clean.
- Required source existence checks: completed before S12C file creation.
- Existing S10/S11 validations: completed before S12C file creation; harness, negative-control self-test, no-residue self-test, and report-generator self-test passed.
- S12A/S12B reread: completed using repository-local S12A consent and PAI_DIR docs plus S12B schema, validation, failure, and decision docs.
- PAI_DIR dry-run detection model drafting: completed in `docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_DETECTION_MODEL.md`.
- Source-root classification and guardrail spec drafting: completed in `docs/adapters/V5_CODEX_SOURCE_ROOT_CLASSIFICATION_AND_GUARDRAIL_SPEC.md`.
- Detection failure cases drafting: completed in `docs/adapters/V5_CODEX_PAI_DIR_DETECTION_FAILURE_CASES.md`.
- Dry-run reporting spec drafting: completed in `docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_REPORTING_SPEC.md`.
- Decision log drafting: completed in `docs/adapters/V5_CODEX_S12C_DECISION_LOG.md`.
- Final validation execution: completed; all required validation commands and content checks passed.

## Iteration Log

Iteration 1 self-review score: 100/100. Hard failures: 0.

| Area | Points | Result |
| --- | ---: | --- |
| Scope and protected-path discipline | 15/15 | Only the six approved S12C docs are intended to change. |
| Evidence discipline | 10/10 | Source material is limited to repository-local S12A/S12B docs and existing fixture evidence. |
| PAI_DIR dry-run model quality | 25/25 | Dry-run model states no detector, no live PAI_DIR inspection, and defines required inputs/outputs. |
| Source-root classification and guardrail quality | 20/20 | Classification spec covers required source classes, future-only live/personal clone rules, and forbidden root patterns. |
| Failure cases and reporting boundary quality | 15/15 | Failure cases include `PD-001` through `PD-025`; reporting spec preserves non-canonical boundaries. |
| Memory, ISA, Pulse, product-memory, and no-live-read safety | 10/10 | PAI Memory, ISA, Pulse, product memory, live user-local, personal clone, and existing-local-v5 boundaries remain denied by default. |
| Verification quality | 5/5 | Required validation commands, changed-file, heading, content invariant, no-test-change, and protected-path checks pass. |

## Surprises & Discoveries

- The local sandbox wrapper may return `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; repository-local validation commands may need explicit escalation when the wrapper fails.
- S12A already establishes no default live local read; S12C narrows that into design-only PAI_DIR dry-run behavior and source-root classification guardrails.

## Decision Log

- Use documentation-only S12C deliverables and do not create detector scripts, reports, fixtures, schemas, manifests, runtime payloads, consent artifacts, or validators.
- Treat future PAI_DIR dry-run output as non-canonical and not proof that Codex is drop-in.
- Treat `existing-local-v5-read-only` and `personal-clone-read-only` as future-only classes requiring explicit architect approval plus explicit user consent.

## Outcomes & Retrospective

Validation results recorded:

- `git status --short`: only the six approved S12C docs.
- `git diff --name-only | sort`: only the six approved S12C docs.
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
- Python cache residue check: pass.

S12C remains documentation/design only. It does not implement a detector, create a detector script, create a consent artifact, create a consent validator, create a detection report, run a live read-only trial, read live existing-local-v5 state, inspect private user-local state, inspect live `~/.claude/PAI`, inspect live `~/.claude/projects`, inspect live `~/.codex`, inspect the user's second personal clone, implement a runtime adapter, create root `AGENTS.md`, create `.codex/`, start or call Pulse, write PAI Memory, write ISA, authorize product-memory promotion, authorize personal-clone access, or claim Codex is drop-in today.
