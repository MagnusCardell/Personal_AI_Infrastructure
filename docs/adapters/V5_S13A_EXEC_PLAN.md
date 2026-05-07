# V5-S13A Execution Plan

## Purpose

Execute V5-S13A First Clean-Clone Live Read-Only Trial as an adapter-test implementation milestone.

S13A is the first approved live-read-only trial, but only against the current clean cloned repository. It is not an existing-local-v5 user-state trial, not a personal-clone trial, and not runtime adapter implementation.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement remains plausible only through a designed adapter and later replacement-grade validation.

## Scope

In scope:

- Create this execution plan first.
- Create the clean-clone S13A README.
- Create the adapter-test consent artifact.
- Implement the standard-library-only clean-clone read-only runner.
- Generate the S13A preflight report.
- Generate the S13A clean-clone evidence report.
- Run and record all amended validation commands.

Out of scope:

- Existing-local-v5 user-state trials.
- Personal-clone trials.
- Live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, arbitrary home-directory, or second personal clone reads.
- Codex runtime adapter implementation.
- Root `AGENTS.md`, `.codex/`, runtime files, runtime payloads, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, committed negative fixtures, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, and migration scripts.
- Pulse startup, Pulse endpoint calls, `localhost:31337` probes, Claude Code invocation, Codex runtime invocation, installers, and Codex import/migration/hook/rule/execpolicy commands.

## Approved Write Set

Create exactly these files:

- `docs/adapters/V5_S13A_EXEC_PLAN.md`
- `tests/adapters/v5-codex-live-readonly-trial/README.md`
- `tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json`
- `tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py`
- `tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json`
- `tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json`

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

- S0-S12E adapter docs for prior adapter conclusions.
- Existing S10/S11 fixture and evidence files.
- Repository-local PAI v5 release files for PAI facts.
- Official OpenAI Codex docs only if S13A adds or refreshes a Codex capability claim.
- Local `codex --version` or `codex --help` only if already available and non-invasive.

Forbidden sources and operations:

- Unofficial Codex capability sources.
- Inferred current Codex behavior from memory.
- Live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, arbitrary home directories, private user-local state, or any second/personal clone outside this repository.
- Live existing-local-v5 state.
- Pulse startup, Pulse endpoint calls, or `localhost:31337` probes.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, and Codex hook/rule/execpolicy commands.

## Source Material

Baseline amended discovery before S13A file creation:

- `git status --short`: no output.
- Required S12E closeout and S13 proposal docs existed.
- `Releases/v5.0.0/.claude` existed.
- `Releases/v5.0.0/.claude/CLAUDE.md` existed.
- `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md` existed.
- Existing S11A and S11C report files existed.
- Existing S11 evidence closeout and S12 readiness closeout docs existed.
- Existing fixture validation passed with `fixture_count: 12`, `case_count: 12`, `coverage_id_count: 25`, `gate_id_count: 20`, and `status: pass`.
- Existing harness negative-control self-test passed with `negative_control_count: 60`.
- Existing no-residue self-test passed.
- S13A Contract Amendment 1 read-only S11A/S11C report validation passed with `existing S11 evidence reports ok`.

No S11 report generator was run under S13A.

## Completion Contract

> ## Completion Contract
>
> This Completion Contract is the authoritative contract for V5-S13A.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S13A_EXEC_PLAN.md`.
>
> Do not mark S13A complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S13A deliverables must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S13A is the first clean-clone live read-only trial only.
> * S13A is not an existing-local-v5 trial.
> * S13A is not a personal-clone trial.
> * S13A does not inspect the user's second personal clone.
> * S13A does not inspect live `~/.claude/PAI`.
> * S13A does not inspect live `~/.claude/projects`.
> * S13A does not inspect live `~/.codex`.
> * S13A does not inspect arbitrary home directories.
> * S13A does not implement a Codex runtime adapter.
> * S13A does not create runtime adapter files.
> * S13A does not create root `AGENTS.md`.
> * S13A does not create `.codex/`.
> * S13A does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, runtime payloads, or committed negative fixtures.
> * S13A does not modify release files.
> * S13A consent, preflight, and evidence artifacts are non-canonical adapter-test artifacts only.
> * S13A consent, preflight, and evidence artifacts are not PAI Memory.
> * S13A consent, preflight, and evidence artifacts are not ISA.
> * S13A consent, preflight, and evidence artifacts are not Pulse state.
> * S13A consent, preflight, and evidence artifacts are not Claude memory.
> * S13A consent, preflight, and evidence artifacts are not Codex memory.
> * S13A consent, preflight, and evidence artifacts are not manifests.
> * S13A consent, preflight, and evidence artifacts are not runtime payloads.
> * S13A consent, preflight, and evidence artifacts are not proof that Codex is drop-in.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Product memories must not be silently promoted into PAI Memory.
> * Pulse is central v5 infrastructure, but S13A does not start Pulse, call Pulse endpoints, or claim Pulse parity.
> * S13A must not require uninstalling Claude Code.
> * S13A must not write PAI Memory or ISA.
> * S13A must not read product memories.
> * S13A must not promote product memories.
> * S13A must not claim Codex is official upstream.
> * S13A must not claim Codex is drop-in.
>
> ### Required local discovery commands
>
> Run from repository root before creating files: `git status --short`; required S12E/S13 proposal doc existence checks; release fixture existence checks for `Releases/v5.0.0/.claude`, `Releases/v5.0.0/.claude/CLAUDE.md`, and `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md`; fixture harness validation; fixture harness negative controls; no-residue validation; and, after S13A Contract Amendment 1, read-only validation of existing S11A and S11C reports.
>
> Do not inspect live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or any user-local state. Do not inspect any second/personal clone. Do not start Pulse. Do not call `localhost:31337`. Do not run installers. Do not invoke Claude Code. Do not run Codex import/migration tooling. Do not run Codex hook, rule, execpolicy, or runtime commands.
>
> ### Required file: `docs/adapters/V5_S13A_EXEC_PLAN.md`
>
> This file must be created first. It must contain exactly these H1/H2 headings: `# V5-S13A Execution Plan`, `## Purpose`, `## Scope`, `## Approved Write Set`, `## Protected Paths`, `## Source Protocol`, `## Source Material`, `## Completion Contract`, `## Milestones`, `## Self-Review Rubric`, `## Hard Failure Conditions`, `## Validation Commands`, `## Progress`, `## Iteration Log`, `## Surprises & Discoveries`, `## Decision Log`, and `## Outcomes & Retrospective`.
>
> The execution plan must include milestones for baseline status check, S12 closeout reread, clean-clone consent artifact creation, read-only trial runner implementation, preflight report generation, clean-clone evidence report generation, protected-path and no-extra-file validation, self-review and repair, and final handoff and goal-state report.
>
> The self-review rubric must total 100 points with a minimum score of 94/100 and zero hard failures.
>
> ### Required S13A files
>
> Create only the approved S13A execution plan, clean-clone trial README, clean-clone consent artifact, standard-library-only runner, preflight report, and evidence report.
>
> The README must state S13A is a clean-clone read-only trial only, not an existing-local-v5 trial, not a personal-clone trial, does not inspect live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or arbitrary home directories, does not run Codex or Claude Code, does not start or call Pulse, does not write PAI Memory or ISA, does not read or promote product memories, and does not prove Codex is drop-in.
>
> The consent artifact must include the required consent, source, read-root, forbidden-root, runtime prohibition, product memory, Pulse, Memory, ISA, reporting, retention, rollback/no-residue, drop-in, non-canonical, and limitation fields with `consent_status: approved-for-clean-clone-preflight-only`, `source_kind: clean-clone-read-only`, `source_root: .`, and `drop_in_claim_policy: not-allowed`.
>
> The runner must be Python 3 standard-library-only, set `sys.dont_write_bytecode = True`, validate consent, read only approved repository-local roots, refuse unsafe source roots and forbidden paths, inspect only lightweight repository-local evidence, write exactly the two approved S13A report paths, emit stdout summary only, and exit non-zero on failure. It must not use subprocesses, network access, non-stdlib dependencies, user-local state, Pulse, Claude Code, Codex runtime, release modifications, root `AGENTS.md`, `.codex/`, or runtime files.
>
> The preflight report and evidence report must include the required fields and required values, must be non-canonical adapter-test evidence only, and must state they are not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.
>
> ### Protected paths
>
> Do not modify protected paths including `Releases/`, `.claude/`, `PAI/`, `CLAUDE.md`, `AGENTS.md`, `.codex/`, `install.sh`, `PAI_SYSTEM_PROMPT.md`, `settings.json`, `hooks/`, `skills/`, `subagents/`, `agents/`, `commands/`, `.github/`, and `.agents/`. Do not inspect or modify private user-local state including `~/.claude/`, `~/.claude/PAI/`, `~/.claude/projects/`, `~/.codex/`, and `~/.codex/memories/`.
>
> ### Hard failure conditions
>
> S13A fails if any file outside the approved write set is created or modified; any S10/S11 fixture, harness, generator, evaluator, report, README outside the S13A directory, or release file is modified; any protected file is modified; existing-local-v5 state or personal clone state is read; live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or arbitrary home directories are inspected; PAI Memory or ISA is written; Pulse is started or called; `localhost:31337` is probed; Claude Code or Codex runtime is invoked; runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, runtime payloads, or committed negative fixtures are created; the runner imports non-stdlib dependencies, uses subprocesses, uses network access, or writes outside approved S13A report paths; any deliverable claims Codex is drop-in today or official upstream or authorizes prohibited writes, Pulse behavior, existing-local-v5 trial execution, personal-clone access, Claude file direct-copy, product-memory promotion, dual-engine uncoordinated writes, or work beyond S13A.
>
> ### Required validation commands
>
> Run the amended S13A validation commands: `git status --short`, `git diff --name-only | sort`, `git diff --check`, fixture harness validation, fixture harness negative controls, no-residue validation, clean-clone runner execution, read-only S11A/S11C report validation, changed-file check, execution-plan heading check, JSON artifact validation, runner static safety check, content invariant check, no unexpected S13A/generated artifact check, no S10/S11 report artifact change check, S13A write-set check, and protected-path check.
>
> ### Acceptance criteria
>
> S13A is complete only if exactly the six approved files are created or modified; no S10/S11 fixture, harness, generator, evaluator, report, README outside the S13A directory, or release file is modified; no protected files are changed; no existing-local-v5 state, personal clone, live user-local state, arbitrary home-directory path, PAI Memory write, ISA write, Pulse behavior, Claude Code invocation, Codex runtime invocation, runtime adapter file, root `AGENTS.md`, or `.codex/` occurs; the runner uses only the Python standard library, no subprocesses, no network access, and writes only the two approved S13A reports; all artifacts validate; all checks pass; this execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures; and final handoff reports every required validation command.
>
> ### Final handoff format
>
> End with exactly these headings: `## Files changed`, `## Behavior changed`, `## Tests run`, `## Known risks`, `## Protected files changed`, `## Goal state`, and `## Recommended next architect decision`.
>
> ### Stop conditions
>
> Stop and report immediately if any protected file must be edited, any file outside the approved write set is modified, any S10/S11 fixture, harness, generator, evaluator, report, README, or release file would need to be modified, existing-local-v5 state or personal clone state would need to be read, live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or arbitrary home-directory paths would need to be inspected, PAI Memory or ISA would need to be written, Pulse would need to be started or called, Claude Code or Codex runtime would need to be invoked, runtime implementation seems necessary, root `AGENTS.md` or `.codex/` would need to be modified, forbidden runtime/control artifacts would need to be created, the runner would need non-stdlib dependencies, subprocesses, network access, or writes outside approved report paths, the goal tries to continue beyond S13A, the Completion Contract cannot be copied, or self-review cannot reach 94/100 without leaving scope.

Full original S13A Completion Contract copy, preserved as a blockquote so this execution plan still has exactly the required H1/H2 heading structure:

> ## Completion Contract
>
> This Completion Contract is the authoritative contract for V5-S13A.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S13A_EXEC_PLAN.md`.
>
> Do not mark S13A complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S13A deliverables must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S13A is the first clean-clone live read-only trial only.
> * S13A is not an existing-local-v5 trial.
> * S13A is not a personal-clone trial.
> * S13A does not inspect the user's second personal clone.
> * S13A does not inspect live `~/.claude/PAI`.
> * S13A does not inspect live `~/.claude/projects`.
> * S13A does not inspect live `~/.codex`.
> * S13A does not inspect arbitrary home directories.
> * S13A does not implement a Codex runtime adapter.
> * S13A does not create runtime adapter files.
> * S13A does not create root `AGENTS.md`.
> * S13A does not create `.codex/`.
> * S13A does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, runtime payloads, or committed negative fixtures.
> * S13A does not modify release files.
> * S13A consent, preflight, and evidence artifacts are non-canonical adapter-test artifacts only.
> * S13A consent, preflight, and evidence artifacts are not PAI Memory.
> * S13A consent, preflight, and evidence artifacts are not ISA.
> * S13A consent, preflight, and evidence artifacts are not Pulse state.
> * S13A consent, preflight, and evidence artifacts are not Claude memory.
> * S13A consent, preflight, and evidence artifacts are not Codex memory.
> * S13A consent, preflight, and evidence artifacts are not manifests.
> * S13A consent, preflight, and evidence artifacts are not runtime payloads.
> * S13A consent, preflight, and evidence artifacts are not proof that Codex is drop-in.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Product memories must not be silently promoted into PAI Memory.
> * Pulse is central v5 infrastructure, but S13A does not start Pulse, call Pulse endpoints, or claim Pulse parity.
> * S13A must not require uninstalling Claude Code.
> * S13A must not write PAI Memory or ISA.
> * S13A must not read product memories.
> * S13A must not promote product memories.
> * S13A must not claim Codex is official upstream.
> * S13A must not claim Codex is drop-in.
>
> ### Required local discovery commands
>
> Run these commands from repository root before creating files:
>
> ```bash
> git status --short
>
> test -f docs/adapters/V5_CODEX_S12_READINESS_CLOSEOUT_REPORT.md
> test -f docs/adapters/V5_CODEX_S13_LIVE_READ_ONLY_TRIAL_GATES.md
> test -f docs/adapters/V5_CODEX_S13_PROPOSED_WRITE_SET_AND_COMPLETION_CONTRACT.md
> test -f docs/adapters/V5_CODEX_S13_RISK_REGISTER.md
> test -f docs/adapters/V5_CODEX_S12_TO_S13_DECISION_LOG.md
> test -d Releases/v5.0.0/.claude
> test -f Releases/v5.0.0/.claude/CLAUDE.md
> test -f Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md
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
> ### Required file: `docs/adapters/V5_S13A_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S13A Execution Plan
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
> 2. S12 closeout reread.
> 3. Clean-clone consent artifact creation.
> 4. Read-only trial runner implementation.
> 5. Preflight report generation.
> 6. Clean-clone evidence report generation.
> 7. Protected-path and no-extra-file validation.
> 8. Self-review and repair.
> 9. Final handoff and goal-state report.
>
> The self-review rubric must total 100 points:
>
> | Area                                                                          | Points |
> | ----------------------------------------------------------------------------- | -----: |
> | Scope and protected-path discipline                                           |     15 |
> | Evidence discipline                                                           |     10 |
> | Consent artifact quality                                                      |     15 |
> | Preflight report quality                                                      |     20 |
> | Clean-clone evidence report quality                                           |     20 |
> | No-live-user-state, no-Pulse, Memory, ISA, product-memory, and runtime safety |     15 |
> | Verification quality                                                          |      5 |
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
> ### Required file: `tests/adapters/v5-codex-live-readonly-trial/README.md`
>
> This README must explain:
>
> * S13A is a clean-clone read-only trial only.
> * S13A is not an existing-local-v5 trial.
> * S13A is not a personal-clone trial.
> * S13A does not inspect `~/.claude/PAI`.
> * S13A does not inspect `~/.claude/projects`.
> * S13A does not inspect `~/.codex`.
> * S13A does not inspect arbitrary home directories.
> * S13A does not run Codex.
> * S13A does not run Claude Code.
> * S13A does not start Pulse.
> * S13A does not call Pulse endpoints.
> * S13A does not write PAI Memory or ISA.
> * S13A does not read or promote product memories.
> * S13A artifacts are non-canonical adapter-test artifacts only.
> * S13A does not prove Codex is drop-in.
> * Codex is not currently proven drop-in for existing local PAI v5 files.
>
> ### Required file: `tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json`
>
> Create a JSON consent artifact for this clean-clone-only S13A trial.
>
> It must include:
>
> ```text
> consent_id
> consent_status
> consent_scope
> source_kind
> source_root
> allowed_read_roots
> forbidden_read_roots
> forbidden_write_roots
> runtime_prohibitions
> product_memory_policy
> pulse_policy
> memory_policy
> isa_policy
> reporting_policy
> retention_policy
> rollback_no_residue_policy
> drop_in_claim_policy
> non_canonical_statement
> limitations
> ```
>
> Required values:
>
> ```text
> consent_status: approved-for-clean-clone-preflight-only
> source_kind: clean-clone-read-only
> source_root: .
> drop_in_claim_policy: not-allowed
> ```
>
> Allowed read roots must be exactly:
>
> ```text
> docs/adapters
> tests/adapters/v5-codex-readonly-fixture-trial
> Releases/v5.0.0
> ```
>
> Forbidden read roots must include:
>
> ```text
> ~/.claude
> ~/.claude/PAI
> ~/.claude/projects
> ~/.codex
> ~/.codex/memories
> /home
> /Users
> ```
>
> Forbidden write roots must include:
>
> ```text
> Releases
> .claude
> PAI
> CLAUDE.md
> AGENTS.md
> .codex
> install.sh
> settings.json
> hooks
> skills
> subagents
> agents
> commands
> .github
> .agents
> ```
>
> Runtime prohibitions must include:
>
> ```text
> no_codex_runtime_invocation
> no_claude_code_invocation
> no_pulse_start
> no_pulse_endpoint_calls
> no_installers
> no_import_or_migration_tooling
> no_hook_rule_or_execpolicy_commands
> ```
>
> The non-canonical statement must explicitly say the artifact is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.
>
> ### Required file: `tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py`
>
> Implement a Python 3 standard-library-only runner.
>
> The runner must:
>
> * set `sys.dont_write_bytecode = True`;
> * read the approved consent artifact;
> * validate consent fields;
> * read only the approved repository-local read roots;
> * refuse absolute source roots except the normalized current repository root derived from `.`;
> * refuse parent traversal;
> * refuse user-local paths;
> * refuse arbitrary `/home` or `/Users` paths;
> * refuse `.codex`, `.claude`, `PAI`, root `AGENTS.md`, root `CLAUDE.md`, and protected write surfaces as read roots;
> * inspect only lightweight repository-local evidence:
>
>   * existence of S12E closeout docs;
>   * existence of S11 reports;
>   * existence of `Releases/v5.0.0/.claude/CLAUDE.md`;
>   * existence of `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md`;
>   * existence of fixture-trial harness files;
> * produce exactly:
>
>   * `reports/S13A_PREFLIGHT_REPORT.json`
>   * `reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json`
> * write only those two approved report paths;
> * emit stdout summary only;
> * exit with code `0` when all checks pass;
> * exit non-zero on failure.
>
> The runner must not:
>
> * use subprocesses;
> * use network access;
> * import non-stdlib dependencies;
> * read user-local state;
> * read `~/.claude`;
> * read `~/.codex`;
> * inspect the personal clone;
> * start Pulse;
> * call Pulse endpoints;
> * probe `localhost:31337`;
> * invoke Claude Code;
> * invoke Codex;
> * write PAI Memory;
> * write ISA;
> * modify release files;
> * modify root `AGENTS.md`;
> * modify `.codex/`;
> * create runtime files.
>
> The runner CLI must support:
>
> ```bash
> python3 tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py \
>   --consent tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json \
>   --preflight-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json \
>   --evidence-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json
> ```
>
> ### Required preflight report
>
> Create:
>
> ```text
> tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json
> ```
>
> It must include:
>
> ```text
> report_id
> report_type
> report_status
> source_kind
> source_root
> consent_status
> allowed_read_roots
> forbidden_read_roots
> forbidden_write_roots
> preflight_status
> abort_required
> abort_reasons
> pulse_status
> memory_status
> isa_status
> product_memory_status
> runtime_invocation_status
> drop_in_claim_status
> protected_path_status
> non_canonical_statement
> limitations
> ```
>
> Required values:
>
> ```text
> report_type: clean-clone-read-only-preflight
> report_status: pass
> source_kind: clean-clone-read-only
> consent_status: approved-for-clean-clone-preflight-only
> preflight_status: pass-read-only-clean-clone
> abort_required: false
> pulse_status: not-started-not-called
> memory_status: no-pai-memory-writes
> isa_status: no-isa-writes
> product_memory_status: no-product-memory-read-or-promotion
> runtime_invocation_status: no-codex-or-claude-runtime-invocation
> drop_in_claim_status: not-claimed
> protected_path_status: no-protected-path-writes
> ```
>
> The non-canonical statement must explicitly say the report is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.
>
> ### Required evidence report
>
> Create:
>
> ```text
> tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json
> ```
>
> It must include:
>
> ```text
> report_id
> report_type
> report_status
> source_kind
> source_root
> files_checked
> required_evidence
> missing_evidence
> pulse_status
> memory_status
> isa_status
> product_memory_status
> runtime_invocation_status
> drop_in_claim_status
> release_files_modified
> protected_paths_modified
> personal_clone_access_status
> user_local_access_status
> non_canonical_statement
> limitations
> ```
>
> Required values:
>
> ```text
> report_type: clean-clone-read-only-evidence
> report_status: pass
> source_kind: clean-clone-read-only
> pulse_status: not-started-not-called
> memory_status: no-pai-memory-writes
> isa_status: no-isa-writes
> product_memory_status: no-product-memory-read-or-promotion
> runtime_invocation_status: no-codex-or-claude-runtime-invocation
> drop_in_claim_status: not-claimed
> release_files_modified: false
> protected_paths_modified: false
> personal_clone_access_status: not-accessed
> user_local_access_status: not-accessed
> ```
>
> `missing_evidence` must be an empty list.
>
> The non-canonical statement must explicitly say the report is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.
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
> S13A fails immediately if:
>
> * Any file outside the approved write set is created or modified.
> * Any fixture, harness, generator, evaluator, S10/S11 report, README outside the S13A directory, or release file is modified.
> * Any protected file is modified.
> * Existing-local-v5 state is read.
> * The user's second personal clone is inspected.
> * `~/.claude/PAI` is inspected.
> * `~/.claude/projects` is inspected.
> * `~/.codex` is inspected.
> * Arbitrary home-directory paths are scanned.
> * PAI Memory is written.
> * ISA is written.
> * Pulse is started.
> * Pulse endpoints are called.
> * `localhost:31337` is probed.
> * Claude Code is invoked.
> * Codex is invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available.
> * Runtime adapter files are created.
> * Root `AGENTS.md` is created or modified.
> * `.codex/` is created or modified.
> * Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, runtime payloads, or committed negative fixtures are created.
> * The runner imports non-stdlib dependencies.
> * The runner uses subprocesses.
> * The runner uses network access.
> * The runner writes outside approved S13A report paths.
> * The docs, runner, consent artifact, preflight report, or evidence report claim Codex is drop-in today.
> * The docs, runner, consent artifact, preflight report, or evidence report claim Codex is the official upstream engine.
> * The docs, runner, consent artifact, preflight report, or evidence report authorize PAI Memory writes.
> * The docs, runner, consent artifact, preflight report, or evidence report authorize ISA writes.
> * The docs, runner, consent artifact, preflight report, or evidence report authorize Pulse startup.
> * The docs, runner, consent artifact, preflight report, or evidence report authorize Pulse endpoint calls.
> * The docs, runner, consent artifact, preflight report, or evidence report authorize Pulse implementation.
> * The docs, runner, consent artifact, preflight report, or evidence report authorize existing-local-v5 trial execution.
> * The docs, runner, consent artifact, preflight report, or evidence report authorize personal-clone access.
> * The docs, runner, consent artifact, preflight report, or evidence report imply Claude-shaped files can be copied directly into Codex surfaces.
> * The docs, runner, consent artifact, preflight report, or evidence report authorize product-memory promotion into PAI Memory.
> * The docs, runner, consent artifact, preflight report, or evidence report authorize dual-engine uncoordinated writes.
> * The goal advances beyond S13A.
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
> python3 tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py \
>   --consent tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json \
>   --preflight-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json \
>   --evidence-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json
> ```
>
> Run changed-file check:
>
> ```bash
> python3 - <<'PY'
> import subprocess
>
> expected = {
>     "docs/adapters/V5_S13A_EXEC_PLAN.md",
>     "tests/adapters/v5-codex-live-readonly-trial/README.md",
>     "tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json",
>     "tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py",
>     "tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json",
>     "tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json",
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
> Run execution-plan heading check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
> import re
>
> file = Path("docs/adapters/V5_S13A_EXEC_PLAN.md")
> expected = [
>     "# V5-S13A Execution Plan",
>     "## Purpose",
>     "## Scope",
>     "## Approved Write Set",
>     "## Protected Paths",
>     "## Source Protocol",
>     "## Source Material",
>     "## Completion Contract",
>     "## Milestones",
>     "## Self-Review Rubric",
>     "## Hard Failure Conditions",
>     "## Validation Commands",
>     "## Progress",
>     "## Iteration Log",
>     "## Surprises & Discoveries",
>     "## Decision Log",
>     "## Outcomes & Retrospective",
> ]
>
> lines = [line.rstrip() for line in file.read_text(encoding="utf-8").splitlines()]
> actual = [line for line in lines if re.match(r"^(#|##) [^#]", line)]
>
> if actual != expected:
>     print("heading mismatch")
>     print("expected:")
>     print("\n".join(expected))
>     print("actual:")
>     print("\n".join(actual))
>     raise SystemExit(1)
>
> print("heading structure ok")
> PY
> ```
>
> Run JSON artifact validation:
>
> ```bash
> python3 - <<'PY'
> import json
> from pathlib import Path
>
> consent = json.loads(Path("tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json").read_text(encoding="utf-8"))
> preflight = json.loads(Path("tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json").read_text(encoding="utf-8"))
> evidence = json.loads(Path("tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json").read_text(encoding="utf-8"))
>
> failures = []
>
> if consent.get("consent_status") != "approved-for-clean-clone-preflight-only":
>     failures.append("consent_status mismatch")
>
> if consent.get("source_kind") != "clean-clone-read-only":
>     failures.append("consent source_kind mismatch")
>
> if consent.get("source_root") != ".":
>     failures.append("consent source_root must be .")
>
> if preflight.get("report_type") != "clean-clone-read-only-preflight":
>     failures.append("preflight report_type mismatch")
>
> if preflight.get("report_status") != "pass":
>     failures.append("preflight report_status mismatch")
>
> if preflight.get("preflight_status") != "pass-read-only-clean-clone":
>     failures.append("preflight_status mismatch")
>
> if preflight.get("abort_required") is not False:
>     failures.append("preflight abort_required must be false")
>
> if evidence.get("report_type") != "clean-clone-read-only-evidence":
>     failures.append("evidence report_type mismatch")
>
> if evidence.get("report_status") != "pass":
>     failures.append("evidence report_status mismatch")
>
> if evidence.get("missing_evidence") != []:
>     failures.append("missing_evidence must be empty")
>
> required_status = {
>     "pulse_status": "not-started-not-called",
>     "memory_status": "no-pai-memory-writes",
>     "isa_status": "no-isa-writes",
>     "product_memory_status": "no-product-memory-read-or-promotion",
>     "runtime_invocation_status": "no-codex-or-claude-runtime-invocation",
>     "drop_in_claim_status": "not-claimed",
> }
>
> for data_name, data in [("preflight", preflight), ("evidence", evidence)]:
>     for key, value in required_status.items():
>         if data.get(key) != value:
>             failures.append(f"{data_name} {key}: expected {value!r}, got {data.get(key)!r}")
>
> statement_blob = " ".join([
>     str(consent.get("non_canonical_statement", "")),
>     str(preflight.get("non_canonical_statement", "")),
>     str(evidence.get("non_canonical_statement", "")),
> ])
>
> for term in [
>     "not PAI Memory",
>     "not ISA",
>     "not Pulse state",
>     "not Claude memory",
>     "not Codex memory",
>     "not a manifest",
>     "not runtime payload",
>     "not proof that Codex is drop-in",
> ]:
>     if term not in statement_blob:
>         failures.append(f"missing non-canonical term: {term}")
>
> if evidence.get("personal_clone_access_status") != "not-accessed":
>     failures.append("personal_clone_access_status must be not-accessed")
>
> if evidence.get("user_local_access_status") != "not-accessed":
>     failures.append("user_local_access_status must be not-accessed")
>
> if evidence.get("release_files_modified") is not False:
>     failures.append("release_files_modified must be false")
>
> if evidence.get("protected_paths_modified") is not False:
>     failures.append("protected_paths_modified must be false")
>
> if failures:
>     print("\n".join(failures))
>     raise SystemExit(1)
>
> print("S13A json artifacts ok")
> PY
> ```
>
> Run runner static safety check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
> import ast
>
> script = Path("tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py")
> text = script.read_text(encoding="utf-8")
> tree = ast.parse(text)
>
> required_terms = [
>     "dont_write_bytecode",
>     "clean-clone-read-only",
>     "not-accessed",
>     "not-started-not-called",
>     "no-pai-memory-writes",
>     "no-isa-writes",
>     "no-product-memory-read-or-promotion",
>     "no-codex-or-claude-runtime-invocation",
> ]
>
> for term in required_terms:
>     if term not in text:
>         print(f"missing runner term: {term}")
>         raise SystemExit(1)
>
> forbidden_imports = {
>     "subprocess",
>     "requests",
>     "http",
>     "http.client",
>     "urllib",
>     "urllib.request",
>     "socket",
>     "webbrowser",
>     "shutil",
> }
>
> for node in ast.walk(tree):
>     if isinstance(node, ast.Import):
>         for alias in node.names:
>             if alias.name.split(".")[0] in forbidden_imports:
>                 print(f"forbidden import: {alias.name}")
>                 raise SystemExit(1)
>     if isinstance(node, ast.ImportFrom):
>         if (node.module or "").split(".")[0] in forbidden_imports:
>             print(f"forbidden import from: {node.module}")
>             raise SystemExit(1)
>     if isinstance(node, ast.Call):
>         if isinstance(node.func, ast.Attribute) and node.func.attr in {"system", "popen"}:
>             print("runtime command call detected")
>             raise SystemExit(1)
>
> print("runner static safety ok")
> PY
> ```
>
> Run no forbidden access string check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> paths = [
>     Path("docs/adapters/V5_S13A_EXEC_PLAN.md"),
>     Path("tests/adapters/v5-codex-live-readonly-trial/README.md"),
>     Path("tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json"),
>     Path("tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py"),
>     Path("tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json"),
>     Path("tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json"),
> ]
>
> combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
>
> required = [
>     "Codex is not currently proven drop-in",
>     "clean-clone",
>     "not an existing-local-v5 trial",
>     "not a personal-clone trial",
>     "not PAI Memory",
>     "not ISA",
>     "not Pulse state",
>     "not a manifest",
>     "not runtime payload",
>     "not proof that Codex is drop-in",
>     "no-product-memory-read-or-promotion",
>     "not-started-not-called",
>     "no-pai-memory-writes",
>     "no-isa-writes",
> ]
>
> for term in required:
>     if term not in combined:
>         print(f"missing content invariant: {term}")
>         raise SystemExit(1)
>
> print("S13A content invariants ok")
> PY
> ```
>
> Run no unexpected report/test artifacts check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> failures = []
>
> allowed_live = {
>     Path("tests/adapters/v5-codex-live-readonly-trial/README.md"),
>     Path("tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json"),
>     Path("tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py"),
>     Path("tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json"),
>     Path("tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json"),
> }
>
> root = Path("tests/adapters/v5-codex-live-readonly-trial")
> if root.exists():
>     for path in root.rglob("*"):
>         if path.is_file() and path not in allowed_live:
>             failures.append(f"unexpected S13A live-readonly artifact: {path}")
>
> for path in Path(".").rglob("*"):
>     s = str(path)
>     if "__pycache__" in s or path.suffix == ".pyc":
>         failures.append(f"unexpected generated Python artifact: {path}")
>
> if failures:
>     print("\n".join(failures))
>     raise SystemExit(1)
>
> print("no unexpected S13A/generated artifacts ok")
> PY
> ```
>
> Run protected-path check:
>
> ```bash
> git status --short -- Releases/ .claude/ PAI/ CLAUDE.md AGENTS.md .codex/ install.sh settings.json hooks/ skills/ subagents/ agents/ commands/ .github/ .agents/
> ```
>
> Expected protected-path result: no output.
>
> ### Acceptance criteria
>
> S13A is complete only if:
>
> * Exactly the six approved S13A files are created or modified.
> * No fixture, harness, generator, evaluator, S10/S11 report, README outside the S13A directory, or release file is modified.
> * No protected files are changed.
> * No existing-local-v5 state is read.
> * The user's second personal clone is not inspected.
> * `~/.claude/PAI` is not inspected.
> * `~/.claude/projects` is not inspected.
> * `~/.codex` is not inspected.
> * Arbitrary home-directory paths are not scanned.
> * PAI Memory is not written.
> * ISA is not written.
> * Pulse is not started.
> * Pulse endpoints are not called.
> * `localhost:31337` is not probed.
> * Claude Code is not invoked.
> * Codex is not invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available.
> * Runtime adapter files are not created.
> * Root `AGENTS.md` is not created or modified.
> * `.codex/` is not created or modified.
> * The runner uses only the Python standard library.
> * The runner does not use subprocesses.
> * The runner does not use network access.
> * The runner writes only the two approved S13A reports.
> * The consent artifact validates.
> * The preflight report validates.
> * The evidence report validates.
> * The runner static safety check passes.
> * The changed-file check passes.
> * The heading check passes.
> * JSON artifact validation passes.
> * Content invariant check passes.
> * No unexpected artifact check passes.
> * Protected-path check has no output.
> * `V5_S13A_EXEC_PLAN.md` contains the Completion Contract copied into its `## Completion Contract` section.
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
> No — only the approved S13A execution plan, clean-clone trial README, consent artifact, runner, preflight report, and evidence report were created or modified.
> ```
>
> `Recommended next architect decision` must be advisory only. Do not begin S13B, S14, personal-clone access, existing-local-v5 trial execution, or runtime adapter work.
>
> ### Stop conditions
>
> Stop and report immediately if:
>
> * Any protected file must be edited.
> * Any file outside the approved write set is modified.
> * Any S10/S11 fixture, harness, generator, evaluator, report, README, or release file would need to be modified.
> * Existing-local-v5 state would need to be read.
> * The user's second personal clone would need to be inspected.
> * `~/.claude/PAI` would need to be inspected.
> * `~/.claude/projects` would need to be inspected.
> * `~/.codex` would need to be inspected.
> * Arbitrary home-directory paths would need to be scanned.
> * PAI Memory would need to be written.
> * ISA would need to be written.
> * Pulse would need to be started.
> * A Pulse endpoint would need to be called.
> * `localhost:31337` would need to be probed.
> * Claude Code would need to be invoked.
> * Codex would need to be invoked as a runtime engine.
> * Runtime implementation seems necessary.
> * Root `AGENTS.md` or `.codex/` would need to be modified.
> * A Codex config, hook, rule, skill, subagent, agent, command, launcher, installer, wrapper, generated runtime config, migration script, adapter payload, Memory payload, ISA payload, Pulse payload, Pulse bridge file, runtime payload, or committed negative fixture would need to be created.
> * The runner would need non-stdlib dependencies.
> * The runner would need subprocesses.
> * The runner would need network access.
> * The runner would need to write outside approved report paths.
> * The goal tries to continue beyond S13A.
> * The Completion Contract cannot be copied into the execution plan.
> * The self-review cannot reach 94/100 without leaving scope.

S13A Contract Amendment 1 removed the S11 report-generator self-test from discovery and validation because it may rewrite S11 report artifacts outside the S13A write set. The command was replaced with read-only validation of existing S11A and S11C reports.

Under Amendment 1, this command must not be run during S13A:

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_report_generator.py`

Replacement read-only checks:

- `test -f tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json`
- `test -f tests/adapters/v5-codex-readonly-fixture-trial/reports/S11C_READINESS_GATE_EVALUATION.json`
- `test -f docs/adapters/V5_CODEX_S11_EVIDENCE_CLOSEOUT_REPORT.md`
- `test -f docs/adapters/V5_CODEX_S12_READINESS_CLOSEOUT_REPORT.md`
- Existing-report JSON invariant validation prints `existing S11 evidence reports ok`.

## Milestones

1. Baseline status check.
2. S12 closeout reread.
3. Clean-clone consent artifact creation.
4. Read-only trial runner implementation.
5. Preflight report generation.
6. Clean-clone evidence report generation.
7. Protected-path and no-extra-file validation.
8. Self-review and repair.
9. Final handoff and goal-state report.

## Self-Review Rubric

| Area | Points |
| --- | ---: |
| Scope and protected-path discipline | 15 |
| Evidence discipline | 10 |
| Consent artifact quality | 15 |
| Preflight report quality | 20 |
| Clean-clone evidence report quality | 20 |
| No-live-user-state, no-Pulse, Memory, ISA, product-memory, and runtime safety | 15 |
| Verification quality | 5 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

Hard failures for this execution:

- Any file outside the six approved S13A files is created or modified.
- Any S10/S11 fixture, harness, generator, evaluator, report, README outside the S13A directory, release file, protected file, root `AGENTS.md`, or `.codex/` file is modified.
- Existing-local-v5 state, user-local state, arbitrary home-directory state, live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, or a personal clone is inspected.
- PAI Memory or ISA is written.
- Pulse is started, Pulse endpoints are called, or `localhost:31337` is probed.
- Claude Code, Codex runtime, installers, import/migration tooling, hook/rule/execpolicy commands, or runtime adapter work are invoked.
- The runner imports non-stdlib dependencies, uses subprocesses, uses network access, or writes outside the two approved S13A report paths.
- Deliverables claim Codex is drop-in today or official upstream.
- Deliverables authorize prohibited writes, Pulse behavior, existing-local-v5 trial execution, personal-clone access, Claude file direct-copy, product-memory promotion, dual-engine uncoordinated writes, or work beyond S13A.
- The removed S11 report-generator self-test is run during S13A.
- Self-review cannot reach 94/100 with zero hard failures.

## Validation Commands

Amended discovery commands already run before S13A file creation:

```bash
git status --short
test -f docs/adapters/V5_CODEX_S12_READINESS_CLOSEOUT_REPORT.md
test -f docs/adapters/V5_CODEX_S13_LIVE_READ_ONLY_TRIAL_GATES.md
test -f docs/adapters/V5_CODEX_S13_PROPOSED_WRITE_SET_AND_COMPLETION_CONTRACT.md
test -f docs/adapters/V5_CODEX_S13_RISK_REGISTER.md
test -f docs/adapters/V5_CODEX_S12_TO_S13_DECISION_LOG.md
test -d Releases/v5.0.0/.claude
test -f Releases/v5.0.0/.claude/CLAUDE.md
test -f Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md
python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures
PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py
test -f tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json
test -f tests/adapters/v5-codex-readonly-fixture-trial/reports/S11C_READINESS_GATE_EVALUATION.json
test -f docs/adapters/V5_CODEX_S11_EVIDENCE_CLOSEOUT_REPORT.md
test -f docs/adapters/V5_CODEX_S12_READINESS_CLOSEOUT_REPORT.md
```

Amended final validation commands to run after drafting:

```bash
git status --short
git diff --name-only | sort
git diff --check
python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures
PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py
python3 tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py --consent tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json --preflight-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json --evidence-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json
```

Then run:

- Read-only existing S11 report validation block.
- Changed-file check.
- Execution-plan heading check.
- JSON artifact validation.
- Runner static safety check.
- Content invariant check.
- Unexpected-artifact check.
- No S10/S11 report artifact change check.
- S13A write-set check.
- Protected-path check.

## Progress

| Milestone | Status | Evidence |
| --- | --- | --- |
| 1. Baseline status check | Complete | `git status --short` had no output before S13A files. |
| 2. S12 closeout reread | Complete | Required S12E/S13 proposal docs existed; S11/S12 evidence checks passed. |
| 3. Clean-clone consent artifact creation | Complete | `tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json` created. |
| 4. Read-only trial runner implementation | Complete | `tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py` created and static safety check passed. |
| 5. Preflight report generation | Complete | Runner generated `reports/S13A_PREFLIGHT_REPORT.json` with `report_status: pass`. |
| 6. Clean-clone evidence report generation | Complete | Runner generated `reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json` with `report_status: pass` and empty `missing_evidence`. |
| 7. Protected-path and no-extra-file validation | Complete | Changed-file, no unexpected artifact, no S10/S11 report artifact, S13A write-set, and protected-path checks passed. |
| 8. Self-review and repair | Complete | Iteration 2 scored 98/100 with zero hard failures. |
| 9. Final handoff and goal-state report | Pending | Ready after final validation rerun and goal update. |

## Iteration Log

Iteration 1 initial self-review after execution plan creation:

| Area | Score | Notes |
| --- | ---: | --- |
| Scope and protected-path discipline | 15/15 | Only the approved execution plan created so far. |
| Evidence discipline | 10/10 | Amended discovery used repository-local S12E docs, release fixture paths, S10/S11 fixture validation, and read-only S11 report validation only. |
| Consent artifact quality | 0/15 | Consent artifact not yet created. |
| Preflight report quality | 0/20 | Preflight report not yet generated. |
| Clean-clone evidence report quality | 0/20 | Evidence report not yet generated. |
| No-live-user-state, no-Pulse, Memory, ISA, product-memory, and runtime safety | 15/15 | No forbidden reads, Pulse behavior, Memory/ISA writes, product memory reads, or runtime commands used. |
| Verification quality | 2/5 | Amended discovery passed; final validation pending. |
| Total | 42/100 | Below pass threshold because deliverables remain pending. |

Hard failures: 0.

Iteration 2 final self-review after validation:

| Area | Score | Notes |
| --- | ---: | --- |
| Scope and protected-path discipline | 15/15 | Changed-file and S13A write-set checks passed with exactly the six approved files; protected-path check had no output. |
| Evidence discipline | 10/10 | Evidence is repository-local clean-clone evidence only; no existing-local-v5, personal clone, user-local, arbitrary home-directory, Pulse, Claude Code, or Codex runtime access occurred. |
| Consent artifact quality | 15/15 | Consent artifact includes required fields and required values, with approved read roots exactly matching the contract. |
| Preflight report quality | 19/20 | Preflight report validates with required statuses and non-canonical statement. |
| Clean-clone evidence report quality | 20/20 | Evidence report validates with required statuses, checked evidence list, and empty `missing_evidence`. |
| No-live-user-state, no-Pulse, Memory, ISA, product-memory, and runtime safety | 15/15 | Runner and artifacts preserve no user-local access, no Pulse, no Memory/ISA writes, no product memory reads or promotion, and no runtime invocation. |
| Verification quality | 4/5 | All amended validation commands passed; S11 report-generator self-test was intentionally not run per Amendment 1. |
| Total | 98/100 | Pass threshold met. |

Hard failures: 0.

## Surprises & Discoveries

- The original S13A contract included the S11 report-generator self-test, which may rewrite existing S11 report artifacts outside the S13A write set.
- S13A Contract Amendment 1 removed that command and replaced it with read-only validation of existing S11A and S11C reports.
- The local sandbox continues to fail many commands with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; repository-local commands were run with explicit escalation where needed.

## Decision Log

- S13A uses Contract Amendment 1 as the controlling validation adjustment.
- S13A will not run the S11 report-generator self-test.
- S13A remains clean-clone read-only only.
- S13A does not approve or begin S13B, S14, personal-clone access, existing-local-v5 trial execution, or runtime adapter work.
- S13A consent, preflight, and evidence outputs remain non-canonical adapter-test artifacts only.

## Outcomes & Retrospective

Final validation outcomes:

| Command or check | Result |
| --- | --- |
| `git status --short` | Passed; only S13A approved path group is untracked. |
| `git diff --name-only | sort` | Passed; no output because S13A files are untracked. |
| `git diff --check` | Passed; no output. |
| `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures` | Passed with `status: pass`, `fixture_count: 12`, `case_count: 12`, `coverage_id_count: 25`, and `gate_id_count: 20`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py` | Passed with `positive_control_status: pass` and `negative_control_count: 60`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py` | Passed with `repository_residue_status: pass`. |
| `python3 tests/adapters/v5-codex-live-readonly-trial/run_clean_clone_readonly_trial.py --consent tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json --preflight-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json --evidence-out tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json` | Passed with `preflight_status: pass-read-only-clean-clone`, `report_status: pass`, and no user-local or personal-clone access. |
| Read-only existing S11 report validation block | Passed with `existing S11 evidence reports ok`. |
| Changed-file check | Passed with `changed files ok`. |
| Execution-plan heading check | Passed with `heading structure ok`. |
| JSON artifact validation | Passed with `S13A json artifacts ok`. |
| Runner static safety check | Passed with `runner static safety ok`. |
| Content invariant check | Passed with `S13A content invariants ok`. |
| Unexpected-artifact check | Passed with `no unexpected S13A/generated artifacts ok`. |
| No S10/S11 report artifact change check | Passed with `no S10/S11 report artifact changes ok`. |
| S13A write-set check | Passed with `S13A write set ok`. |
| Protected-path check | Passed with no output. |

Outcome:

- Exactly the six approved S13A files were created.
- No S10/S11 report artifact changed.
- No S10/S11 fixture, harness, generator, evaluator, README outside S13A, release file, protected path, root `AGENTS.md`, or `.codex/` file changed.
- S13A remained a clean-clone read-only adapter-test trial only.
- S13A did not inspect existing-local-v5 state, personal clone state, live user-local state, arbitrary home directories, live `~/.claude/PAI`, live `~/.claude/projects`, or live `~/.codex`.
- S13A did not start Pulse, call Pulse endpoints, probe `localhost:31337`, invoke Claude Code, invoke Codex runtime, run installers, run Codex import/migration/hook/rule/execpolicy commands, or implement runtime adapter work.
- S13A did not write PAI Memory, ISA, Pulse state, product memory, runtime payloads, or protected paths.
