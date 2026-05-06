# V5-S12D Execution Plan

## Purpose

Execute V5-S12D Live Read-Only Preflight Report Design. S12D designs the future live-read-only preflight report contract, validation sequence, abort evidence model, and non-canonical output policy required before any future live existing-local-v5 read-only trial can be considered.

Codex is not currently proven drop-in for existing local PAI v5 files. S12D is documentation/design only. It does not implement a preflight runner, create a preflight report, create a detector script, create a consent artifact, create a consent validator, run a live read-only trial, read live existing-local-v5 state, inspect private user-local state, or implement runtime adapter behavior.

## Scope

In scope:

- Create this S12D execution plan.
- Create the preflight report schema proposal.
- Create the preflight validation sequence spec.
- Create the preflight abort and evidence model.
- Create the preflight non-canonical output policy.
- Create the S12D decision log.
- Run and record all required validation commands.

Out of scope:

- Preflight runners, actual preflight reports, detector scripts, consent artifacts, and consent validators.
- Live read-only trials or live existing-local-v5 access.
- Inspection of live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, private user-local state, or the user's second personal clone.
- Fixture, harness, generator, evaluator, report, README, release, protected-path, runtime, adapter, or detector file edits.
- Root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, preflight reports, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures.

## Approved Write Set

Create exactly these files:

- `docs/adapters/V5_S12D_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_LIVE_READ_ONLY_PREFLIGHT_REPORT_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_PREFLIGHT_VALIDATION_SEQUENCE_SPEC.md`
- `docs/adapters/V5_CODEX_PREFLIGHT_ABORT_AND_EVIDENCE_MODEL.md`
- `docs/adapters/V5_CODEX_PREFLIGHT_NON_CANONICAL_OUTPUT_POLICY.md`
- `docs/adapters/V5_CODEX_S12D_DECISION_LOG.md`

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

- S0-S12C adapter docs for prior adapter conclusions.
- Existing S10/S11 fixture and evidence files.
- Repository-local PAI v5 release files for PAI facts only if needed.
- Official OpenAI Codex docs only if S12D adds or refreshes a Codex capability claim.
- Local `codex --version` or `codex --help` only if already available and non-invasive.

Forbidden sources and operations:

- Unofficial Codex capability sources.
- Inferred current Codex behavior from memory.
- Live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, private user-local state, or any second/personal clone outside this repository.
- Live existing-local-v5 state.
- Pulse startup, Pulse endpoint calls, or `localhost:31337` probes.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, and Codex hook/rule/execpolicy commands.

## Source Material

Baseline discovery before S12D edits:

- `git status --short`: no output.
- Required S12A preflight/reporting docs, S12B consent docs, and S12C PAI_DIR detection/reporting docs existed.
- `Releases/v5.0.0/.claude` existed as repository-local release fixture material.
- Existing harness validation passed with `fixture_count: 12`, `case_count: 12`, `coverage_id_count: 25`, `gate_id_count: 20`, and `status: pass`.
- Existing harness negative-control self-test passed with `negative_control_count: 60`.
- Existing no-residue self-test passed.
- Existing report-generator negative-control self-test passed with `negative_control_count: 16`.

S12A/S12B/S12C source reread:

- Future preflight must be read-only, explicitly consent-bound, path-bounded, deterministic, no-write, abortable, and non-runtime.
- Future consent validation must reject missing, revoked, expired, ambiguous, mismatched, replayed, overbroad, write-authorizing, Pulse-authorizing, Memory/ISA-authorizing, product-memory-authorizing, runtime-authorizing, or drop-in-claiming consent.
- Future PAI_DIR dry-run detection output remains non-canonical and not proof that Codex is drop-in.
- Product memory reads remain denied by default, Pulse startup/calls remain denied, and PAI Memory and ISA writes remain denied.

## Completion Contract

> ## Completion Contract
>
> This Completion Contract is the authoritative contract for V5-S12D.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S12D_EXEC_PLAN.md`.
>
> Do not mark S12D complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S12D deliverables must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S12D designs future live-read-only preflight report behavior only.
> * S12D does not implement a preflight runner.
> * S12D does not create a preflight report.
> * S12D does not create a detector script.
> * S12D does not create a consent artifact.
> * S12D does not create a consent validator.
> * S12D does not run a live read-only trial.
> * S12D does not read live existing-local-v5 state.
> * S12D does not read live user-local state.
> * S12D does not inspect live `~/.claude/PAI`.
> * S12D does not inspect live `~/.claude/projects`.
> * S12D does not inspect live `~/.codex`.
> * S12D does not inspect the user’s second personal clone.
> * S12D does not implement a Codex runtime adapter.
> * S12D does not create runtime adapter files.
> * S12D does not create root `AGENTS.md`.
> * S12D does not create `.codex/`.
> * S12D does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures.
> * Future preflight report output is not PAI Memory.
> * Future preflight report output is not ISA.
> * Future preflight report output is not Pulse state.
> * Future preflight report output is not Claude memory.
> * Future preflight report output is not Codex memory.
> * Future preflight report output is not a manifest.
> * Future preflight report output is not runtime payload.
> * Future preflight report output is not proof that Codex is drop-in.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Product memories must not be silently promoted into PAI Memory.
> * Pulse is central v5 infrastructure, but S12D does not start Pulse, call Pulse endpoints, or claim Pulse parity.
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
> test -f docs/adapters/V5_CODEX_LIVE_READ_ONLY_PREFLIGHT_AND_ABORT_MODEL.md
> test -f docs/adapters/V5_CODEX_LIVE_READ_ONLY_REPORTING_BOUNDARY_SPEC.md
> test -f docs/adapters/V5_CODEX_CONSENT_ARTIFACT_SCHEMA_PROPOSAL.md
> test -f docs/adapters/V5_CODEX_CONSENT_VALIDATION_AND_REVOCATION_SPEC.md
> test -f docs/adapters/V5_CODEX_CONSENT_FAILURE_AND_ABORT_CASES.md
> test -f docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_DETECTION_MODEL.md
> test -f docs/adapters/V5_CODEX_SOURCE_ROOT_CLASSIFICATION_AND_GUARDRAIL_SPEC.md
> test -f docs/adapters/V5_CODEX_PAI_DIR_DETECTION_FAILURE_CASES.md
> test -f docs/adapters/V5_CODEX_PAI_DIR_DRY_RUN_REPORTING_SPEC.md
> test -f docs/adapters/V5_CODEX_S12C_DECISION_LOG.md
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
> ### Required file: `docs/adapters/V5_S12D_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S12D Execution Plan
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
> 2. S12A/S12B/S12C reread.
> 3. Preflight report schema proposal drafting.
> 4. Preflight validation sequence drafting.
> 5. Abort and evidence model drafting.
> 6. Non-canonical output policy drafting.
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
> | Preflight report schema quality                             |     25 |
> | Validation sequence quality                                 |     20 |
> | Abort/evidence and non-canonical output quality             |     15 |
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
> ### Required file: `docs/adapters/V5_CODEX_LIVE_READ_ONLY_PREFLIGHT_REPORT_SCHEMA_PROPOSAL.md`
>
> Purpose: define the future preflight report schema proposal required before any live local PAI v5 read-only trial.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Live Read-Only Preflight Report Schema Proposal
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Schema Proposal Status
> ## Preflight Report Role
> ## Non-Canonical Report Rules
> ## Top-Level Field Model
> ## Identity and Version Fields
> ## Consent Validation Fields
> ## Source Selection Fields
> ## PAI_DIR Detection Fields
> ## Allowed Read Fields
> ## Forbidden Read Fields
> ## Forbidden Write Fields
> ## Runtime Prohibition Fields
> ## Product Memory Boundary Fields
> ## Pulse Boundary Fields
> ## Memory and ISA Boundary Fields
> ## Abort and Failure Fields
> ## Reporting and Retention Fields
> ## Cross-Field Validation Rules
> ## Example Non-Executable Preflight Report
> ## Prohibited Schema Semantics
> ## Future Implementation Gates
> ## Non-Goals
> ```
>
> Required content:
>
> * State that this is a schema proposal in markdown only.
> * State that S12D does not create an actual preflight report.
> * State that the future preflight report is non-canonical unless separately approved.
> * State that the future preflight report is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.
> * Define top-level proposed fields:
>
>   * `schema_id`
>   * `schema_version`
>   * `preflight_report_id`
>   * `preflight_status`
>   * `consent_id`
>   * `consent_status`
>   * `source_kind`
>   * `source_root`
>   * `source_root_status`
>   * `pai_dir_candidate`
>   * `pai_dir_candidate_status`
>   * `allowed_reads`
>   * `forbidden_reads`
>   * `forbidden_writes`
>   * `runtime_prohibitions`
>   * `product_memory_policy`
>   * `pulse_policy`
>   * `memory_policy`
>   * `isa_policy`
>   * `abort_required`
>   * `abort_reasons`
>   * `denied_action_report`
>   * `unsupported_surface_report`
>   * `non_canonical_statement`
>   * `retention_policy`
>   * `rollback_no_residue_policy`
>   * `drop_in_claim_policy`
>   * `architect_approval_reference`
> * Define allowed future `preflight_status` values:
>
>   * `not-run`
>   * `pass-read-only`
>   * `abort-required`
>   * `invalid-consent`
>   * `invalid-source`
>   * `invalid-pai-dir`
>   * `blocked-by-policy`
> * State that S12D approves none of these statuses for live use.
> * Include one non-executable example preflight report inside a markdown fenced block.
> * The example must be labeled `NON-EXECUTABLE DESIGN SKETCH — DO NOT USE AS PREFLIGHT REPORT`.
>
> ### Required file: `docs/adapters/V5_CODEX_PREFLIGHT_VALIDATION_SEQUENCE_SPEC.md`
>
> Purpose: define future live-read-only preflight validation sequence without implementing it.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Preflight Validation Sequence Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Validation Sequence Problem Statement
> ## Validation Principles
> ## Sequence Input Model
> ## Sequence Output Model
> ## Step P0: Architect Approval Check
> ## Step P1: Consent Validation
> ## Step P2: Source Kind Validation
> ## Step P3: Source Root Validation
> ## Step P4: PAI_DIR Candidate Validation
> ## Step P5: Allowed Read Scope Validation
> ## Step P6: Forbidden Read Scope Validation
> ## Step P7: Forbidden Write Scope Validation
> ## Step P8: Product Memory Boundary Validation
> ## Step P9: Pulse Boundary Validation
> ## Step P10: Memory and ISA Boundary Validation
> ## Step P11: Runtime Invocation Boundary Validation
> ## Step P12: Reporting Boundary Validation
> ## Step P13: Abort or Proceed Decision
> ## Required Future Proofs
> ## Prohibited Validation Sequences
> ## Non-Goals
> ```
>
> Required content:
>
> * State that S12D implements no validation sequence.
> * Define each step as future-only.
> * State that every step must fail closed.
> * State that any failed step must abort.
> * State that `Proceed` in future preflight means only “eligible for architect-approved read-only trial,” not drop-in status.
> * State that validation must not read live local state by itself.
> * State that validation must not write PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, or `.codex/`.
> * State that validation must not start Pulse or call Pulse endpoints.
> * State that validation must not invoke Claude Code or Codex runtime.
>
> ### Required file: `docs/adapters/V5_CODEX_PREFLIGHT_ABORT_AND_EVIDENCE_MODEL.md`
>
> Purpose: define future abort reasons, evidence records, denied-action evidence, unsupported-surface evidence, and failure classification for live-read-only preflight.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Preflight Abort and Evidence Model
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Abort Evidence Problem Statement
> ## Abort Principles
> ## Abort Reason Model
> ## Evidence Record Model
> ## Consent Evidence
> ## Source Root Evidence
> ## PAI_DIR Evidence
> ## Read Scope Evidence
> ## Write Pressure Evidence
> ## Product Memory Evidence
> ## Pulse Evidence
> ## Memory and ISA Evidence
> ## Runtime Invocation Evidence
> ## Reporting Evidence
> ## Abort Evidence Table
> ## Required Future Proofs
> ## Prohibited Abort Evidence Designs
> ## Non-Goals
> ```
>
> Required content:
>
> Include an abort evidence table with columns:
>
> ```text
> Evidence ID | Evidence class | Trigger | Required preflight response | Required report field | Future proof required | S12D status
> ```
>
> Minimum evidence IDs:
>
> * `PE-001`: architect approval missing.
> * `PE-002`: missing consent.
> * `PE-003`: expired consent.
> * `PE-004`: revoked consent.
> * `PE-005`: consent source root mismatch.
> * `PE-006`: source kind mismatch.
> * `PE-007`: ambiguous source root.
> * `PE-008`: source root outside allowed scope.
> * `PE-009`: missing `PAI_DIR` candidate.
> * `PE-010`: insufficient `PAI_DIR` confidence.
> * `PE-011`: attempted default read of `~/.claude/PAI`.
> * `PE-012`: attempted read of `~/.claude/projects`.
> * `PE-013`: attempted read of `~/.codex`.
> * `PE-014`: attempted product memory read.
> * `PE-015`: write pressure detected.
> * `PE-016`: PAI Memory write pressure.
> * `PE-017`: ISA write pressure.
> * `PE-018`: Pulse startup pressure.
> * `PE-019`: Pulse endpoint call pressure.
> * `PE-020`: root `AGENTS.md` write pressure.
> * `PE-021`: `.codex/` write pressure.
> * `PE-022`: Claude Code invocation pressure.
> * `PE-023`: Codex runtime invocation pressure.
> * `PE-024`: unsupported surface would be silently ignored.
> * `PE-025`: drop-in claim pressure.
> * `PE-026`: report output would become canonical state.
> * `PE-027`: personal clone access without approval.
> * `PE-028`: clean clone mistaken for live PAI install.
> * `PE-029`: rollback/no-residue expectation missing.
> * `PE-030`: retention policy missing.
>
> S12D must mark every case as design-only.
>
> ### Required file: `docs/adapters/V5_CODEX_PREFLIGHT_NON_CANONICAL_OUTPUT_POLICY.md`
>
> Purpose: define future non-canonical output policy for preflight reports.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Preflight Non-Canonical Output Policy
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Output Policy Problem Statement
> ## Output Principles
> ## Non-Canonical Output Model
> ## Retention Policy Model
> ## Privacy Policy Model
> ## No-Promotion Policy
> ## PAI Memory Boundary
> ## ISA Boundary
> ## Pulse Boundary
> ## Claude Memory Boundary
> ## Codex Memory Boundary
> ## Manifest Boundary
> ## Runtime Payload Boundary
> ## Drop-In Claim Boundary
> ## Required Future Proofs
> ## Prohibited Output Policies
> ## Non-Goals
> ```
>
> Required content:
>
> * State that S12D creates no preflight report.
> * State that future preflight output must be advisory and non-canonical by default.
> * State future output is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.
> * State future output must not be promoted into PAI Memory by default.
> * State future output must not be used to update ISA by default.
> * State future output must not be submitted to Pulse by default.
> * State future output must not be stored in Claude memory or Codex memory by default.
> * State future output must not create root `AGENTS.md` or `.codex/`.
> * State future output must include rollback/no-residue and retention boundaries.
>
> ### Required file: `docs/adapters/V5_CODEX_S12D_DECISION_LOG.md`
>
> Purpose: record S12D decisions, non-decisions, blocked decisions, and future architect questions.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex S12D Decision Log
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Decisions Made in S12D
> ## Non-Decisions in S12D
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
> S12D-D01 Codex remains not drop-in today.
> S12D-D02 S12D designs preflight report contract only.
> S12D-D03 S12D creates no actual preflight report.
> S12D-D04 S12D implements no preflight runner.
> S12D-D05 S12D reads no live PAI_DIR.
> S12D-D06 S12D reads no live user-local state.
> S12D-D07 Future preflight must require architect approval.
> S12D-D08 Future preflight must require valid consent.
> S12D-D09 Future preflight must fail closed.
> S12D-D10 Future preflight proceed does not mean drop-in.
> S12D-D11 Product memory reads remain denied by default.
> S12D-D12 Pulse startup and endpoint calls remain denied.
> S12D-D13 PAI Memory and ISA writes remain denied.
> S12D-D14 Root AGENTS.md and .codex remain protected.
> S12D-D15 Future preflight output is non-canonical.
> S12D-D16 Personal-clone access remains future-only.
> S12D-D17 Existing-local-v5 read remains future-only.
> S12D-D18 Runtime adapter planning remains blocked.
> ```
>
> The `## Next Milestone Candidates` section must list advisory-only options, not approvals:
>
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
> S12D fails immediately if:
>
> * Any file outside the approved write set is created or modified.
> * Any fixture, harness, generator, evaluator, report, README, or release file is modified.
> * Any protected file is modified.
> * Any actual preflight report is created.
> * Any preflight runner is created.
> * Any detector script is created.
> * Any consent artifact is created.
> * Any consent validator is created.
> * Runtime adapter files are created.
> * Root `AGENTS.md` is created or modified.
> * `.codex/` is created or modified.
> * Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, preflight reports, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures are created.
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
> * The goal advances beyond S12D.
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
>     "docs/adapters/V5_S12D_EXEC_PLAN.md",
>     "docs/adapters/V5_CODEX_LIVE_READ_ONLY_PREFLIGHT_REPORT_SCHEMA_PROPOSAL.md",
>     "docs/adapters/V5_CODEX_PREFLIGHT_VALIDATION_SEQUENCE_SPEC.md",
>     "docs/adapters/V5_CODEX_PREFLIGHT_ABORT_AND_EVIDENCE_MODEL.md",
>     "docs/adapters/V5_CODEX_PREFLIGHT_NON_CANONICAL_OUTPUT_POLICY.md",
>     "docs/adapters/V5_CODEX_S12D_DECISION_LOG.md",
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
>     "docs/adapters/V5_S12D_EXEC_PLAN.md": [
>         "# V5-S12D Execution Plan",
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
>     "docs/adapters/V5_CODEX_LIVE_READ_ONLY_PREFLIGHT_REPORT_SCHEMA_PROPOSAL.md": [
>         "# V5 Codex Live Read-Only Preflight Report Schema Proposal",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Schema Proposal Status",
>         "## Preflight Report Role",
>         "## Non-Canonical Report Rules",
>         "## Top-Level Field Model",
>         "## Identity and Version Fields",
>         "## Consent Validation Fields",
>         "## Source Selection Fields",
>         "## PAI_DIR Detection Fields",
>         "## Allowed Read Fields",
>         "## Forbidden Read Fields",
>         "## Forbidden Write Fields",
>         "## Runtime Prohibition Fields",
>         "## Product Memory Boundary Fields",
>         "## Pulse Boundary Fields",
>         "## Memory and ISA Boundary Fields",
>         "## Abort and Failure Fields",
>         "## Reporting and Retention Fields",
>         "## Cross-Field Validation Rules",
>         "## Example Non-Executable Preflight Report",
>         "## Prohibited Schema Semantics",
>         "## Future Implementation Gates",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_PREFLIGHT_VALIDATION_SEQUENCE_SPEC.md": [
>         "# V5 Codex Preflight Validation Sequence Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Validation Sequence Problem Statement",
>         "## Validation Principles",
>         "## Sequence Input Model",
>         "## Sequence Output Model",
>         "## Step P0: Architect Approval Check",
>         "## Step P1: Consent Validation",
>         "## Step P2: Source Kind Validation",
>         "## Step P3: Source Root Validation",
>         "## Step P4: PAI_DIR Candidate Validation",
>         "## Step P5: Allowed Read Scope Validation",
>         "## Step P6: Forbidden Read Scope Validation",
>         "## Step P7: Forbidden Write Scope Validation",
>         "## Step P8: Product Memory Boundary Validation",
>         "## Step P9: Pulse Boundary Validation",
>         "## Step P10: Memory and ISA Boundary Validation",
>         "## Step P11: Runtime Invocation Boundary Validation",
>         "## Step P12: Reporting Boundary Validation",
>         "## Step P13: Abort or Proceed Decision",
>         "## Required Future Proofs",
>         "## Prohibited Validation Sequences",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_PREFLIGHT_ABORT_AND_EVIDENCE_MODEL.md": [
>         "# V5 Codex Preflight Abort and Evidence Model",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Abort Evidence Problem Statement",
>         "## Abort Principles",
>         "## Abort Reason Model",
>         "## Evidence Record Model",
>         "## Consent Evidence",
>         "## Source Root Evidence",
>         "## PAI_DIR Evidence",
>         "## Read Scope Evidence",
>         "## Write Pressure Evidence",
>         "## Product Memory Evidence",
>         "## Pulse Evidence",
>         "## Memory and ISA Evidence",
>         "## Runtime Invocation Evidence",
>         "## Reporting Evidence",
>         "## Abort Evidence Table",
>         "## Required Future Proofs",
>         "## Prohibited Abort Evidence Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_PREFLIGHT_NON_CANONICAL_OUTPUT_POLICY.md": [
>         "# V5 Codex Preflight Non-Canonical Output Policy",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Output Policy Problem Statement",
>         "## Output Principles",
>         "## Non-Canonical Output Model",
>         "## Retention Policy Model",
>         "## Privacy Policy Model",
>         "## No-Promotion Policy",
>         "## PAI Memory Boundary",
>         "## ISA Boundary",
>         "## Pulse Boundary",
>         "## Claude Memory Boundary",
>         "## Codex Memory Boundary",
>         "## Manifest Boundary",
>         "## Runtime Payload Boundary",
>         "## Drop-In Claim Boundary",
>         "## Required Future Proofs",
>         "## Prohibited Output Policies",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_S12D_DECISION_LOG.md": [
>         "# V5 Codex S12D Decision Log",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Decisions Made in S12D",
>         "## Non-Decisions in S12D",
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
>     "docs/adapters/V5_CODEX_LIVE_READ_ONLY_PREFLIGHT_REPORT_SCHEMA_PROPOSAL.md",
>     "docs/adapters/V5_CODEX_PREFLIGHT_VALIDATION_SEQUENCE_SPEC.md",
>     "docs/adapters/V5_CODEX_PREFLIGHT_ABORT_AND_EVIDENCE_MODEL.md",
>     "docs/adapters/V5_CODEX_PREFLIGHT_NON_CANONICAL_OUTPUT_POLICY.md",
>     "docs/adapters/V5_CODEX_S12D_DECISION_LOG.md",
> ])
>
> required = [
>     "Codex is not currently proven drop-in",
>     "preflight",
>     "PAI_DIR",
>     "consent",
>     "fail closed",
>     "abort",
>     "future-only",
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
>     "NON-EXECUTABLE DESIGN SKETCH",
> ]
>
> for term in required:
>     if term not in combined:
>         print(f"missing content invariant: {term}")
>         raise SystemExit(1)
>
> for i in range(1, 31):
>     term = f"PE-{i:03d}"
>     if term not in combined:
>         print(f"missing preflight evidence ID: {term}")
>         raise SystemExit(1)
>
> for i in range(1, 19):
>     term = f"S12D-D{i:02d}"
>     if term not in combined:
>         print(f"missing S12D decision ID: {term}")
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
> S12D is complete only if:
>
> * Exactly the six approved S12D docs are created or modified.
> * No fixture, harness, generator, evaluator, report, README, release, or runtime file is modified.
> * No protected files are changed.
> * No actual preflight report is created.
> * No preflight runner is created.
> * No detector script is created.
> * No consent artifact is created.
> * No consent validator is created.
> * No runtime adapter files are created.
> * No root `AGENTS.md` is created or modified.
> * No `.codex/` files are created or modified.
> * No Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, consent artifacts, preflight reports, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures are created.
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
> * `V5_S12D_EXEC_PLAN.md` contains the Completion Contract copied into its `## Completion Contract` section.
> * The schema proposal states that S12D creates no actual preflight report.
> * The validation sequence spec states that S12D implements no validation sequence.
> * The abort/evidence model includes all required `PE-001` through `PE-030` evidence IDs.
> * The output policy states that S12D creates no preflight report.
> * The decision log includes all required `S12D-D01` through `S12D-D18` decisions.
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
> No — only the six approved S12D documentation files were created or modified.
> ```
>
> `Recommended next architect decision` must be advisory only. Do not begin S12E, S13A, or runtime adapter work.
>
> ## Stop conditions
>
> Stop and report immediately if:
>
> * Any protected file must be edited.
> * Any file outside the approved write set is modified.
> * Any test fixture, harness, generator, evaluator, report, README, or release file would need to be modified.
> * Runtime implementation seems necessary.
> * A preflight runner would need to be created.
> * A preflight report would need to be created.
> * A detector script would need to be created.
> * A consent artifact would need to be created.
> * A consent validator would need to be created.
> * Root `AGENTS.md` or `.codex/` would need to be modified.
> * A Codex config, hook, rule, skill, subagent, agent, command, launcher, installer, wrapper, generated runtime config, migration script, adapter payload, Memory payload, ISA payload, Pulse payload, Pulse bridge file, consent artifact, preflight report, manifest instance, executable schema, live-trial artifact, runtime payload, report, fixture, or committed negative fixture would need to be created.
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
> * The goal tries to continue beyond S12D.
> * The Completion Contract cannot be copied into the execution plan.
> * The self-review cannot reach 94/100 without leaving scope.

## Milestones

1. Baseline status check.
2. S12A/S12B/S12C reread.
3. Preflight report schema proposal drafting.
4. Preflight validation sequence drafting.
5. Abort and evidence model drafting.
6. Non-canonical output policy drafting.
7. Decision log drafting.
8. Protected-path and no-extra-file validation.
9. Self-review and repair.
10. Final handoff and goal-state report.

## Self-Review Rubric

| Area | Points |
| --- | ---: |
| Scope and protected-path discipline | 15 |
| Evidence discipline | 10 |
| Preflight report schema quality | 25 |
| Validation sequence quality | 20 |
| Abort/evidence and non-canonical output quality | 15 |
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

- Any file outside the approved S12D write set changes.
- Any fixture, harness, generator, evaluator, report, README, release, protected, runtime, detector, preflight runner, preflight report, consent artifact, or consent validator file changes or is created.
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

- Baseline status check: completed before S12D file creation; worktree was clean.
- Required source existence checks: completed before S12D file creation.
- Existing S10/S11 validations: completed before S12D file creation; harness, negative-control self-test, no-residue self-test, and report-generator self-test passed.
- S12A/S12B/S12C reread: completed using repository-local preflight, reporting, consent validation, PAI_DIR detection, failure, reporting, and decision docs.
- Preflight report schema proposal drafting: completed in `docs/adapters/V5_CODEX_LIVE_READ_ONLY_PREFLIGHT_REPORT_SCHEMA_PROPOSAL.md`.
- Preflight validation sequence drafting: completed in `docs/adapters/V5_CODEX_PREFLIGHT_VALIDATION_SEQUENCE_SPEC.md`.
- Abort and evidence model drafting: completed in `docs/adapters/V5_CODEX_PREFLIGHT_ABORT_AND_EVIDENCE_MODEL.md`.
- Non-canonical output policy drafting: completed in `docs/adapters/V5_CODEX_PREFLIGHT_NON_CANONICAL_OUTPUT_POLICY.md`.
- Decision log drafting: completed in `docs/adapters/V5_CODEX_S12D_DECISION_LOG.md`.
- Final validation execution: completed. Required git checks, fixture harness checks, report-generator checks, changed-file check, heading check, content invariant check, no-test-change check, and protected-path check passed.

## Iteration Log

Iteration 1 self-review score: 100/100. Hard failures: 0.

| Area | Points | Result |
| --- | ---: | --- |
| Scope and protected-path discipline | 15/15 | Only the six approved S12D docs are intended to change. |
| Evidence discipline | 10/10 | Source material is limited to repository-local S12A/S12B/S12C docs and existing fixture evidence. |
| Preflight report schema quality | 25/25 | Schema proposal states no actual preflight report and includes required fields, statuses, non-canonical rules, and non-executable example. |
| Validation sequence quality | 20/20 | Validation sequence defines future-only `P0` through `P13` and fail-closed abort behavior. |
| Abort/evidence and non-canonical output quality | 15/15 | Abort evidence includes `PE-001` through `PE-030`; output policy preserves non-canonical boundaries. |
| Memory, ISA, Pulse, product-memory, and no-live-read safety | 10/10 | PAI Memory, ISA, Pulse, product memory, live user-local, personal clone, and existing-local-v5 boundaries remain denied by default. |
| Verification quality | 5/5 | All required validation commands and S12D-specific checks passed. |

## Surprises & Discoveries

- The local sandbox wrapper may return `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; repository-local validation commands may need explicit escalation when the wrapper fails.
- S12A/S12B/S12C already establish fail-closed preflight and dry-run boundaries; S12D narrows that into future report schema, validation sequence, abort evidence, and output policy documentation only.

## Decision Log

- Use documentation-only S12D deliverables and do not create preflight runners, actual preflight reports, detector scripts, consent artifacts, consent validators, schemas, manifests, runtime payloads, reports, fixtures, or committed negative fixtures.
- Treat future preflight output as advisory, non-canonical, and not proof that Codex is drop-in.
- Treat `Proceed` in a future preflight only as eligibility for a separately architect-approved read-only trial, not runtime parity or drop-in status.

## Outcomes & Retrospective

S12D produced only the six approved documentation files. It created no preflight runner, actual preflight report, detector script, consent artifact, consent validator, runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts, runtime payloads, reports, fixtures, or committed negative fixtures.

Validation results:

- `git status --short`: passed; only the six approved S12D docs are new.
- `git diff --name-only | sort`: passed; listed only the six approved S12D docs.
- `git diff --check`: passed with no whitespace errors.
- `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures`: passed with `fixture_count: 12`, `case_count: 12`, `coverage_id_count: 25`, `gate_id_count: 20`, and `status: pass`.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`: passed with `negative_control_count: 60` and `status: pass`.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py`: passed with stable fixture digest, stable stdout shape, repository residue pass, and `status: pass`.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_report_generator.py`: passed with `negative_control_count: 16` and `status: pass`.
- `python3 tests/adapters/v5-codex-readonly-fixture-trial/generate_readonly_fixture_trial_report.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures --report-out tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json`: passed; regenerated the approved S11A report path without introducing an additional changed file.
- `python3 tests/adapters/v5-codex-readonly-fixture-trial/evaluate_readiness_gates.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures --evidence-report tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json --report-out tests/adapters/v5-codex-readonly-fixture-trial/reports/S11C_READINESS_GATE_EVALUATION.json`: passed; regenerated the approved S11C report path without introducing an additional changed file.
- Changed-file check: passed; actual changed file set exactly matched the six approved S12D docs.
- Heading check: passed.
- Content invariant check: passed.
- No-test-change check: passed.
- Protected-path check: passed with no output.

No live read-only trial was run. No live existing-local-v5 state, live user-local state, live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, or personal clone was inspected. Pulse was not started or called, `localhost:31337` was not probed, installers were not run, Claude Code and Codex runtime were not invoked, and PAI Memory and ISA were not written.
