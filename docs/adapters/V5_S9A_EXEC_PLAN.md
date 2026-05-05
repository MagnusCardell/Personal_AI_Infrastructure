# V5-S9A Execution Plan

## Purpose

Create the design-only V5-S9A integrated read-only fixture-trial architecture artifacts for the PAI v5 Codex replacement-adapter effort.

S9A integrates the already-designed authority/router, launcher/inference, hook/lifecycle, Pulse, Memory/ISA, manifest, audit, schema, rollback, and unsupported-surface seams into one future architecture model. It does not implement a trial and does not create fixtures, harnesses, manifests, schemas, audit artifacts, configs, runtime files, adapter payloads, or trial outputs.

## Scope

S9A is limited to non-runtime documentation under the approved write set. It designs future fixture-trial architecture, sequencing, coverage, failure handling, rollback/no-residue posture, audit reporting, and decision logging.

S9A preserves the current strategy that Codex is not currently proven drop-in for existing local PAI v5 files and that Codex replacement is plausible only through a designed adapter.

## Approved Write Set

- `docs/adapters/V5_S9A_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_INTEGRATED_READ_ONLY_FIXTURE_TRIAL_ARCHITECTURE.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_SEQUENCE_AND_GATE_MODEL.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_COVERAGE_MATRIX.md`
- `docs/adapters/V5_CODEX_TRIAL_FAILURE_ROLLBACK_AND_AUDIT_MODEL.md`
- `docs/adapters/V5_CODEX_INTEGRATED_TRIAL_DECISION_LOG.md`

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

1. S0-S8H adapter docs for prior adapter conclusions.
2. Repository-local PAI v5 release files for PAI facts.
3. Official OpenAI Codex docs only if S9A adds or refreshes a Codex capability claim.
4. Local `codex --version` or `codex --help` only if already available and non-invasive.

Do not use unofficial Codex capability sources. Do not infer current Codex behavior from memory.

## Source Material

Approved read-only sources:

- S0-S8H adapter docs under `docs/adapters/`.
- Repository-local release material under `Releases/v5.0.0/`.
- Repository-local Claude release material under `Releases/v5.0.0/.claude/`.

Discovery outputs are written only to `/tmp` and are not committed into the repository.

## Completion Contract

> This Completion Contract is the authoritative contract for V5-S9A.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S9A_EXEC_PLAN.md`.
>
> Do not mark S9A complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S9A docs must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S9A designs an integrated read-only fixture-trial architecture only.
> * S9A does not implement a trial.
> * S9A does not create fixtures.
> * S9A does not create a harness.
> * S9A does not create manifests.
> * S9A does not create audit artifacts.
> * S9A does not create executable schemas.
> * S9A does not create root `AGENTS.md`.
> * S9A does not create `.codex/`.
> * S9A does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, runtime files, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, or trial outputs.
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
> * Pulse is central v5 infrastructure, but S9A does not start Pulse, call Pulse endpoints, or claim Pulse parity.
> * Future read-only trials must not require uninstalling Claude Code.
> * Future read-only fixture trials must prove no writes, no private-state access, no Pulse startup, no Pulse calls, no Memory writes, no ISA writes, and no direct Claude-file copying.
> * Future writes require a single-writer policy, provenance, rollback, validation, and conflict handling.
> * Controlled write mode must not exist until Memory, ISA, Pulse, authority, launcher/inference, hooks/lifecycle, rollback, and audit gates pass.
>
> ### Required local discovery commands
>
> Run these commands from repository root:
>
> ```bash
> git status --short
>
> test -f docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md
> test -f docs/adapters/V5_CODEX_COMPACT_ROUTER_SPEC.md
> test -f docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md
> test -f docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md
> test -f docs/adapters/V5_CODEX_ENGINE_PROFILE_AND_CAPABILITY_CONTRACT.md
> test -f docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md
> test -f docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md
> test -f docs/adapters/V5_CODEX_PULSE_BRIDGE_IDENTITY_SPEC.md
> test -f docs/adapters/V5_CODEX_PULSE_READ_ONLY_EVENT_MODEL_SPEC.md
> test -f docs/adapters/V5_CODEX_MEMORY_ISA_SINGLE_WRITER_POLICY_SPEC.md
> test -f docs/adapters/V5_CODEX_MEMORY_BOUNDARY_AND_PROMOTION_SPEC.md
> test -f docs/adapters/V5_CODEX_ISA_WORKFLOW_AND_STATE_POLICY_SPEC.md
> test -f docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md
>
> rg -n --hidden --glob '!**/.git/**' \
>   'S7A|S7C|S7D|S7E|S8H|authority seam|compact router|launcher seam|inference seam|engine profile|hook lifecycle|event/context|Pulse bridge|read-only event|single-writer|PAI Memory|ISA|fixture|read-only trial|manifest|audit|drop-in|rollback|denied|unsupported|provenance|no-write|no write|no-start|localhost:31337|AGENTS\.md|CLAUDE\.md|PAI_SYSTEM_PROMPT' \
>   docs/adapters Releases/v5.0.0 \
>   > /tmp/v5-s9a-integrated-trial-search.txt || true
>
> sed -n '1,360p' /tmp/v5-s9a-integrated-trial-search.txt
> ```
>
> Do not write `/tmp/v5-s9a-integrated-trial-search.txt` into the repository.
>
> Do not create fixture files.
>
> Do not create manifest files.
>
> Do not create audit files.
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
> ### Required file: `docs/adapters/V5_S9A_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S9A Execution Plan
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
> 2. S0-S8H reread.
> 3. Cross-seam integration synthesis.
> 4. Integrated fixture-trial architecture drafting.
> 5. Trial sequence and gate model drafting.
> 6. Coverage matrix drafting.
> 7. Failure, rollback, and audit model drafting.
> 8. Integrated trial decision log drafting.
> 9. Self-review and repair.
> 10. Final handoff and goal-state report.
>
> The self-review rubric must total 100 points:
>
> | Area                                                          | Points |
> | ------------------------------------------------------------- | -----: |
> | Scope and protected-path discipline                           |     15 |
> | Evidence discipline                                           |     15 |
> | Cross-seam integration quality                                |     20 |
> | Fixture-trial architecture quality                            |     20 |
> | Gate, coverage, failure, rollback, and audit quality          |     20 |
> | Existing-local-v5, Memory, ISA, Pulse, and dual-engine safety |      5 |
> | Verification quality                                          |      5 |
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
> Create only the five S9A design deliverables named in the approved write set. They must contain exactly the required H1/H2 headings, required tables, required seam names, required trial gate IDs, required coverage IDs, required failure classes and audit fields, required decision IDs, and design-only non-goal statements.
>
> ### Protected paths
>
> Do not modify protected repository paths or inspect private user-local state.
>
> ### Hard failure conditions
>
> S9A fails immediately if any file outside the approved write set is created or modified, any protected file is modified, runtime material is created, a fixture, manifest instance, audit artifact, schema file, harness, trial output, or Pulse bridge file is created, a trial is run, private user-local state or live existing-local-v5 state is read, PAI Memory or ISA is written, Pulse is started or called, installer or migration tooling is run, Claude Code or Codex runtime is invoked, the docs overclaim Codex/Pulse/Memory/ISA readiness, product-memory promotion is authorized, dual-engine uncoordinated writes are authorized, or the goal advances beyond S9A.
>
> ### Required validation commands
>
> Required validation includes `git status --short`, `git diff --name-only | sort`, `git diff --check`, changed-file check, exact H1/H2 heading sequence check, content invariant check, seam coverage check, trial gate ID check, coverage ID check, failure/audit field check, decision ID check, and protected-path check.
>
> ### Acceptance criteria
>
> S9A is complete only if exactly the six approved S9A files are created or modified, no protected files are changed, no runtime or trial material is created, no private or live existing-local-v5 state is inspected, PAI Memory and ISA are not written, Pulse is not started or called, the execution plan contains this contract, all required IDs/tables/fields are present, all validation commands pass, the docs remain design-only, no prohibited claims or authorizations appear, and final handoff reports every required validation command.

## Milestones

1. Baseline status check.
2. S0-S8H reread.
3. Cross-seam integration synthesis.
4. Integrated fixture-trial architecture drafting.
5. Trial sequence and gate model drafting.
6. Coverage matrix drafting.
7. Failure, rollback, and audit model drafting.
8. Integrated trial decision log drafting.
9. Self-review and repair.
10. Final handoff and goal-state report.

## Self-Review Rubric

| Area                                                          | Points |
| ------------------------------------------------------------- | -----: |
| Scope and protected-path discipline                           |     15 |
| Evidence discipline                                           |     15 |
| Cross-seam integration quality                                |     20 |
| Fixture-trial architecture quality                            |     20 |
| Gate, coverage, failure, rollback, and audit quality          |     20 |
| Existing-local-v5, Memory, ISA, Pulse, and dual-engine safety |      5 |
| Verification quality                                          |      5 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

- Any file outside the approved write set is created or modified.
- Any protected file is modified.
- Runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, or Pulse bridge files are created.
- Fixtures, harnesses, manifest instances, audit artifacts, or executable schemas are created.
- A trial is run.
- Private user-local state or live existing-local-v5 state is inspected or modified.
- PAI Memory or ISA is written.
- Pulse is started, Pulse endpoints are called, or `localhost:31337` is probed.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, or Codex hook/rule/execpolicy commands are run.
- The docs claim Codex is drop-in today or the official upstream engine.
- The docs authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, Pulse implementation, existing-local-v5 trial execution, fixture creation, manifest creation, audit artifact creation, schema creation, harness creation, trial execution, product-memory promotion into PAI Memory, or dual-engine uncoordinated writes.
- The docs imply Claude-shaped files can be copied directly into Codex surfaces.
- The goal advances beyond S9A.

## Validation Commands

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Changed-file check for the six approved S9A files.
- Exact H1/H2 heading sequence check.
- Content invariant check.
- Seam coverage check.
- Trial gate ID check.
- Coverage ID check.
- Failure/audit field check.
- Decision ID check.
- Protected-path check.

## Progress

- Baseline status check: complete. Initial status before S9A file creation had no output.
- S0-S8H reread: complete. Prior authority, launcher/inference, hook/lifecycle, Pulse, Memory/ISA, manifest, audit, schema, and readiness gate docs were synthesized.
- Cross-seam integration synthesis: complete.
- Integrated fixture-trial architecture drafting: complete.
- Trial sequence and gate model drafting: complete.
- Coverage matrix drafting: complete.
- Failure, rollback, and audit model drafting: complete.
- Integrated trial decision log drafting: complete.
- Self-review and repair: complete. Required checks passed after the approved S9A files were drafted.
- Final handoff and goal-state report: ready after final validation rerun.

## Iteration Log

| Iteration | Scope and protected-path discipline | Evidence discipline | Cross-seam integration quality | Fixture-trial architecture quality | Gate, coverage, failure, rollback, and audit quality | Existing-local-v5, Memory, ISA, Pulse, and dual-engine safety | Verification quality | Score | Hard failures | Notes |
| --------- | ----------------------------------: | ------------------: | -----------------------------: | ---------------------------------: | ---------------------------------------------------: | ------------------------------------------------------------: | -------------------: | ----: | ------------: | ----- |
| 1 | 15 | 15 | 20 | 19 | 20 | 5 | 5 | 99/100 | 0 | S9A stayed design-only, created only the six approved docs, integrated the S7A/S7C/S7D/S7E/S8H seams, preserved fixture/no-trial/no-runtime boundaries, and passed the required validation suite. One point reserved because future fixture-trial behavior remains intentionally unimplemented and unproven. |

## Surprises & Discoveries

- The prior seam stack is now coherent enough for an integrated architecture, but every runtime-like object remains blocked: fixture, harness, manifest instance, audit artifact, executable schema, router file, Codex config, hook/rule material, launcher, wrapper, adapter payload, Memory payload, ISA payload, Pulse payload, and trial output.
- The safest sequence starts with release-fixture or sanitized-user-fixture architecture. Live existing-local-v5 read-only work remains future-only because it would require separate approval, privacy scope, allowed/denied roots, rollback proof, and no-write proof.
- Pulse remains central v5 infrastructure, but S9A can only design no-start/no-call and reporting gates. It cannot prove Pulse parity.
- The cross-seam blocker pattern is consistent: authority, launcher/inference, hook lifecycle, Pulse, Memory/ISA, manifest/audit/schema, unsupported-surface reporting, and rollback all have to pass before drop-in claims.

## Decision Log

- S9A goal started after the S8H goal was completed.
- Execution plan created before the five S9A deliverables.
- No official Codex documentation refresh was required because S9A added no new Codex capability claim.
- S9A preserves `release-fixture` and `sanitized-user-fixture` as future architecture classes only; it creates no fixture.
- S9A preserves `existing-local-v5-read-only` as future-only and separately approved.
- S9A keeps controlled write mode blocked until read-only fixture validation, single-writer, provenance, rollback, validation, conflict, Pulse, Memory, ISA, authority, launcher/inference, hook/lifecycle, and audit gates pass.

## Outcomes & Retrospective

- Created exactly the six approved S9A documentation artifacts.
- No protected paths were modified.
- No runtime adapter files, root `AGENTS.md`, `.codex/`, fixtures, harnesses, manifest instances, audit artifacts, executable schemas, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, or trial outputs were created.
- No trial was run.
- Private user-local state and live existing-local-v5 state were not inspected.
- PAI Memory and ISA were not written.
- Pulse was not started, Pulse endpoints were not called, and `localhost:31337` was not probed.
- Validation results recorded before final handoff:
  - `git status --short`: only the six approved S9A docs are shown as added.
  - `git diff --name-only | sort`: lists exactly the six approved S9A docs.
  - `git diff --check`: passed.
  - Changed-file check: passed.
  - Exact H1/H2 heading sequence check: passed.
  - Content invariant check: passed.
  - Seam coverage check: passed.
  - Trial gate ID check: passed.
  - Coverage ID check: passed.
  - Failure/audit field check: passed.
  - Decision ID check: passed.
  - Protected-path check: passed with no output.
