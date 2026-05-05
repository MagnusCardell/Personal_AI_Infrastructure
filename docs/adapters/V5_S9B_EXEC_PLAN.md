# V5-S9B Execution Plan

## Purpose

Create the design-only V5-S9B fixture-trial implementation plan and proposed S10A write-set/acceptance artifacts for the PAI v5 Codex replacement-adapter effort.

S9B converts the accepted S9A integrated read-only fixture-trial architecture into a future implementation plan, fixture corpus design, read-only harness design, and proposed S10A contract for architect review only. It does not implement the plan.

## Scope

S9B is limited to non-runtime documentation under the approved write set. It proposes future implementation boundaries but does not approve or start S10A.

S9B preserves the current strategy that Codex is not currently proven drop-in for existing local PAI v5 files and that Codex replacement is plausible only through a designed adapter.

## Approved Write Set

- `docs/adapters/V5_S9B_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_FIRST_FIXTURE_IMPLEMENTATION_PLAN.md`
- `docs/adapters/V5_CODEX_FIXTURE_CORPUS_DESIGN_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_HARNESS_DESIGN_SPEC.md`
- `docs/adapters/V5_CODEX_S10A_WRITE_SET_AND_ACCEPTANCE_CONTRACT.md`
- `docs/adapters/V5_CODEX_FIXTURE_IMPLEMENTATION_DECISION_LOG.md`

No other files may be created or modified.

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

1. S0-S9A adapter docs for prior adapter conclusions.
2. Repository-local PAI v5 release files for PAI facts.
3. Official OpenAI Codex docs only if S9B adds or refreshes a Codex capability claim.
4. Local `codex --version` or `codex --help` only if already available and non-invasive.

Do not use unofficial Codex capability sources. Do not infer current Codex behavior from memory.

## Source Material

Approved read-only sources:

- S0-S9A adapter docs under `docs/adapters/`.
- Repository-local release material under `Releases/v5.0.0/`.
- Repository-local Claude release material under `Releases/v5.0.0/.claude/`.

Discovery outputs are written only to `/tmp` and are not committed into the repository.

## Completion Contract

> This Completion Contract is the authoritative contract for V5-S9B.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S9B_EXEC_PLAN.md`.
>
> Do not mark S9B complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S9B docs must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S9B creates a future implementation plan and proposed write-set only.
> * S9B does not implement the plan.
> * S9B does not create fixtures.
> * S9B does not create a harness.
> * S9B does not create manifests.
> * S9B does not create audit artifacts.
> * S9B does not create executable schemas.
> * S9B does not create root `AGENTS.md`.
> * S9B does not create `.codex/`.
> * S9B does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, runtime files, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, fixture files, or harness files.
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
> * Pulse is central v5 infrastructure, but S9B does not start Pulse, call Pulse endpoints, or claim Pulse parity.
> * Future read-only fixture trials must not require uninstalling Claude Code.
> * Future read-only fixture trials must prove no writes, no private-state access, no Pulse startup, no Pulse calls, no Memory writes, no ISA writes, no direct Claude-file copying, and no product-memory promotion.
> * Future writes require a single-writer policy, provenance, rollback, validation, and conflict handling.
> * Controlled write mode must not exist until Memory, ISA, Pulse, authority, launcher/inference, hooks/lifecycle, rollback, and audit gates pass.
> * S10A is not approved by S9B. S9B may propose the S10A write set and acceptance contract for architect review only.
>
> ### Required local discovery commands
>
> Run these commands from repository root:
>
> ```bash
> git status --short
>
> test -f docs/adapters/V5_CODEX_INTEGRATED_READ_ONLY_FIXTURE_TRIAL_ARCHITECTURE.md
> test -f docs/adapters/V5_CODEX_FIXTURE_TRIAL_SEQUENCE_AND_GATE_MODEL.md
> test -f docs/adapters/V5_CODEX_FIXTURE_TRIAL_COVERAGE_MATRIX.md
> test -f docs/adapters/V5_CODEX_TRIAL_FAILURE_ROLLBACK_AND_AUDIT_MODEL.md
> test -f docs/adapters/V5_CODEX_INTEGRATED_TRIAL_DECISION_LOG.md
> test -f docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md
> test -d Releases/v5.0.0/.claude
>
> find Releases/v5.0.0/.claude -maxdepth 3 -type f | sort | sed -n '1,260p'
>
> rg -n --hidden --glob '!**/.git/**' \
>   'fixture|fixture-trial|read-only fixture|harness|manifest|audit|schema|dry-run|coverage|gate|TG-|CVG-|rollback|no-residue|denied_action_report|unsupported_surface_report|PAI_SYSTEM_PROMPT|CLAUDE\.md|AGENTS\.md|PAI Memory|ISA|Pulse|31337|single-writer|product memories|drop-in|runtime files|protected path|write set|S10A' \
>   docs/adapters Releases/v5.0.0 \
>   > /tmp/v5-s9b-fixture-implementation-plan-search.txt || true
>
> sed -n '1,360p' /tmp/v5-s9b-fixture-implementation-plan-search.txt
> ```
>
> Do not write `/tmp/v5-s9b-fixture-implementation-plan-search.txt` into the repository.
>
> Do not create fixture files.
>
> Do not create manifest files.
>
> Do not create audit files.
>
> Do not create schema files.
>
> Do not create harness files.
>
> Do not run trial commands.
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
> ### Required file: `docs/adapters/V5_S9B_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S9B Execution Plan
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
> 2. S0-S9A reread.
> 3. First fixture implementation plan drafting.
> 4. Fixture corpus design drafting.
> 5. Read-only harness design drafting.
> 6. S10A proposed write-set and acceptance contract drafting.
> 7. Fixture implementation decision log drafting.
> 8. Self-review and repair.
> 9. Final handoff and goal-state report.
>
> The self-review rubric must total 100 points:
>
> | Area                                                        | Points |
> | ----------------------------------------------------------- | -----: |
> | Scope and protected-path discipline                         |     15 |
> | Evidence discipline                                         |     15 |
> | S10A write-set precision                                    |     20 |
> | Fixture corpus design quality                               |     20 |
> | Harness design quality                                      |     15 |
> | Safety, rollback, no-write, and no-private-state guarantees |     10 |
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
> ### Required deliverables
>
> Create only the five S9B design deliverables named in the approved write set. They must contain exactly the required H1/H2 headings, required tables, required fixture IDs, required harness check IDs, required proposed S10A acceptance IDs, required decision IDs, and design-only non-goal statements.
>
> ### Protected paths
>
> Do not modify protected repository paths or inspect private user-local state.
>
> ### Hard failure conditions
>
> S9B fails immediately if any file outside the approved write set is created or modified, any protected file is modified, runtime material is created, a fixture, manifest instance, audit artifact, schema file, harness, trial output, fixture file, harness file, or Pulse bridge file is created, a trial is run, private user-local state or live existing-local-v5 state is read, PAI Memory or ISA is written, Pulse is started or called, installer or migration tooling is run, Claude Code or Codex runtime is invoked, S10A implementation is authorized, the docs overclaim Codex/Pulse/Memory/ISA readiness, product-memory promotion is authorized, dual-engine uncoordinated writes are authorized, or the goal advances beyond S9B.
>
> ### Required validation commands
>
> Required validation includes `git status --short`, `git diff --name-only | sort`, `git diff --check`, changed-file check, exact H1/H2 heading sequence check, content invariant check, fixture ID check, harness check ID check, proposed S10A acceptance ID check, decision ID check, and protected-path check.
>
> ### Acceptance criteria
>
> S9B is complete only if exactly the six approved S9B files are created or modified, no protected files are changed, no runtime or trial material is created, no private or live existing-local-v5 state is inspected, PAI Memory and ISA are not written, Pulse is not started or called, the execution plan contains this contract, all required IDs/tables/fields are present, all validation commands pass, the docs remain design-only, no prohibited claims or authorizations appear, and final handoff reports every required validation command.

## Milestones

1. Baseline status check.
2. S0-S9A reread.
3. First fixture implementation plan drafting.
4. Fixture corpus design drafting.
5. Read-only harness design drafting.
6. S10A proposed write-set and acceptance contract drafting.
7. Fixture implementation decision log drafting.
8. Self-review and repair.
9. Final handoff and goal-state report.

## Self-Review Rubric

| Area                                                        | Points |
| ----------------------------------------------------------- | -----: |
| Scope and protected-path discipline                         |     15 |
| Evidence discipline                                         |     15 |
| S10A write-set precision                                    |     20 |
| Fixture corpus design quality                               |     20 |
| Harness design quality                                      |     15 |
| Safety, rollback, no-write, and no-private-state guarantees |     10 |
| Verification quality                                        |      5 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

- Any file outside the approved write set is created or modified.
- Any protected file is modified.
- Runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, fixture files, harness files, or Pulse bridge files are created.
- Fixtures, harnesses, manifest instances, audit artifacts, or executable schemas are created.
- A trial is run.
- Private user-local state or live existing-local-v5 state is inspected or modified.
- PAI Memory or ISA is written.
- Pulse is started, Pulse endpoints are called, or `localhost:31337` is probed.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, or Codex hook/rule/execpolicy commands are run.
- The docs claim Codex is drop-in today or the official upstream engine.
- The docs authorize S10A implementation, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, Pulse implementation, existing-local-v5 trial execution, fixture creation, manifest creation, audit artifact creation, schema creation, harness creation, trial execution, product-memory promotion into PAI Memory, or dual-engine uncoordinated writes.
- The docs imply Claude-shaped files can be copied directly into Codex surfaces.
- The goal advances beyond S9B.

## Validation Commands

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Changed-file check for the six approved S9B files.
- Exact H1/H2 heading sequence check.
- Content invariant check.
- Fixture ID check.
- Harness check ID check.
- Proposed S10A acceptance ID check.
- Decision ID check.
- Protected-path check.

## Progress

- Baseline status check: complete. Initial status before S9B file creation had no output.
- S0-S9A reread: complete. Prior integrated architecture, sequence/gate, coverage, failure/audit, readiness, and seam docs were synthesized.
- First fixture implementation plan drafting: complete.
- Fixture corpus design drafting: complete.
- Read-only harness design drafting: complete.
- S10A proposed write-set and acceptance contract drafting: complete.
- Fixture implementation decision log drafting: complete.
- Self-review and repair: complete. One exact content-invariant phrase was repaired, then required checks passed.
- Final handoff and goal-state report: ready after final validation rerun.

## Iteration Log

| Iteration | Scope and protected-path discipline | Evidence discipline | S10A write-set precision | Fixture corpus design quality | Harness design quality | Safety, rollback, no-write, and no-private-state guarantees | Verification quality | Score | Hard failures | Notes |
| --------- | ----------------------------------: | ------------------: | -----------------------: | ----------------------------: | ---------------------: | ----------------------------------------------------------: | -------------------: | ----: | ------------: | ----- |
| 1 | 15 | 15 | 20 | 20 | 15 | 10 | 5 | 100/100 | 0 | S9B stayed design-only, created only the six approved docs, proposed S10A without approving it, preserved no-fixture/no-harness/no-runtime boundaries, and passed the required validation suite after adding one exact invariant phrase. |

## Surprises & Discoveries

- The release file inventory confirms future fixture scope can be broad without reading live state, but S9B keeps all fixture and harness paths proposed only.
- The S9A architecture already established the right sequencing: fixture-only implementation must precede existing-local-v5 read-only planning, and controlled write mode must remain blocked until read-only validation succeeds.
- The future S10A contract needs especially precise wording because it can propose fixture and harness paths without authorizing their creation in S9B.
- No official Codex documentation refresh was required because S9B added no new Codex capability claim.

## Decision Log

- S9B goal started after the S9A goal was completed.
- Execution plan created before the five S9B deliverables.
- Future S10A is proposed only and is not approved by S9B.
- Future S10A should be fixture-only, not existing-local-v5.
- Future harness behavior must be read-only and must not become runtime adapter implementation.
- Future expected report examples require separate explicit approval if included.

## Outcomes & Retrospective

- Created exactly the six approved S9B documentation artifacts.
- No protected paths were modified.
- No runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, fixture files, harness files, or Pulse bridge files were created.
- No fixture was created.
- No harness was created.
- No manifest instance, audit artifact, or executable schema was created.
- No trial was run.
- Private user-local state and live existing-local-v5 state were not inspected.
- PAI Memory and ISA were not written.
- Pulse was not started, Pulse endpoints were not called, and `localhost:31337` was not probed.
- Validation results recorded before final handoff:
  - `git status --short`: only the six approved S9B docs are shown as added.
  - `git diff --name-only | sort`: lists exactly the six approved S9B docs.
  - `git diff --check`: passed.
  - Changed-file check: passed.
  - Exact H1/H2 heading sequence check: passed.
  - Content invariant check: passed.
  - Fixture ID check: passed.
  - Harness check ID check: passed.
  - Proposed S10A acceptance ID check: passed.
  - Decision ID check: passed.
  - Protected-path check: passed with no output.
