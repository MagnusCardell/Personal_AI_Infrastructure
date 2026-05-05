# V5-S8H Execution Plan

## Purpose

Create the design-only V5-S8H Memory and ISA single-writer policy artifacts for the PAI v5 Codex replacement-adapter effort.

S8H does not implement Memory or ISA writes, does not read private user-local Memory or ISA state, and does not create runtime policy files, payloads, fixtures, manifests, harnesses, or adapter material.

## Scope

S8H is limited to non-runtime documentation under the approved write set. It designs future single-writer policy, promotion discipline, ISA workflow boundaries, audit requirements, conflict handling, rollback posture, and decision logging.

S8H preserves the current strategy that Codex is not currently proven drop-in for existing local PAI v5 files and that Codex replacement is plausible only through a designed adapter.

## Approved Write Set

- `docs/adapters/V5_S8H_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_MEMORY_ISA_SINGLE_WRITER_POLICY_SPEC.md`
- `docs/adapters/V5_CODEX_MEMORY_BOUNDARY_AND_PROMOTION_SPEC.md`
- `docs/adapters/V5_CODEX_ISA_WORKFLOW_AND_STATE_POLICY_SPEC.md`
- `docs/adapters/V5_CODEX_MEMORY_ISA_AUDIT_AND_CONFLICT_SPEC.md`
- `docs/adapters/V5_CODEX_MEMORY_ISA_DECISION_LOG.md`

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

1. S0-S7E adapter docs for prior adapter conclusions.
2. Repository-local PAI v5 release files for PAI Memory and ISA facts.
3. Official OpenAI Codex docs only if S8H adds or refreshes a Codex capability claim.
4. Local `codex --version` or `codex --help` only if already available and non-invasive.

Do not use unofficial Codex capability sources. Do not infer current Codex behavior from memory.

## Source Material

Approved read-only sources:

- S0-S7E adapter docs under `docs/adapters/`.
- Repository-local release material under `Releases/v5.0.0/`.
- Repository-local Claude release material under `Releases/v5.0.0/.claude/`.

Discovery outputs are written only to `/tmp` and are not committed into the repository.

## Completion Contract

> This Completion Contract is the authoritative contract for V5-S8H.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S8H_EXEC_PLAN.md`.
>
> Do not mark S8H complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S8H docs must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S8H designs Memory and ISA single-writer policy only.
> * S8H does not implement Memory or ISA writes.
> * S8H does not read private user-local Memory or ISA state.
> * S8H does not create root `AGENTS.md`.
> * S8H does not create `.codex/`.
> * S8H does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, migration scripts, runtime files, adapter payloads, Memory payloads, ISA payloads, or Pulse payloads.
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
> * Pulse is central v5 infrastructure, but S8H does not design or implement a Pulse bridge.
> * Future read-only trials must not require uninstalling Claude Code.
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
> test -d Releases/v5.0.0/.claude/PAI/MEMORY || true
> test -d Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory || true
> test -d Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa || true
> test -f docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md
> test -f docs/adapters/V5_CODEX_PULSE_DECISION_LOG.md
> test -f docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md
> test -f docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md
> test -f docs/adapters/V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md
>
> find Releases/v5.0.0/.claude/PAI -maxdepth 5 -type f \( -ipath '*memory*' -o -ipath '*isa*' -o -iname '*ISA*' \) | sort > /tmp/v5-s8h-memory-isa-files.txt
> sed -n '1,260p' /tmp/v5-s8h-memory-isa-files.txt
>
> rg -n --hidden --glob '!**/.git/**' \
>   'Memory|MEMORY|WORK|LEARNING|KNOWLEDGE|ISA|Ideal State Artifact|Ideal State|PRD|system of record|single-writer|writer|write|promotion|promote|canonical|provenance|rollback|conflict|merge|audit|changelog|verification|criteria|PAI_DIR|PAI_SYSTEM_PROMPT|CLAUDE\.md|AGENTS\.md|Codex memory|Claude Code auto memory|goal|Pulse|PULSE|31337|read-only|controlled|single writer|dual-engine|product memory' \
>   Releases/v5.0.0 docs/adapters \
>   > /tmp/v5-s8h-memory-isa-search.txt || true
>
> sed -n '1,340p' /tmp/v5-s8h-memory-isa-search.txt
> ```
>
> Do not write `/tmp/v5-s8h-memory-isa-files.txt` or `/tmp/v5-s8h-memory-isa-search.txt` into the repository.
>
> Do not inspect live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or any user-local memory state.
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
> ### Required file: `docs/adapters/V5_S8H_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S8H Execution Plan
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
> 2. S0-S7E reread.
> 3. Memory and ISA release evidence reread.
> 4. Canonical state boundary synthesis.
> 5. Single-writer policy spec drafting.
> 6. Memory boundary and promotion spec drafting.
> 7. ISA workflow and state policy spec drafting.
> 8. Memory/ISA audit and conflict spec drafting.
> 9. Memory/ISA decision log drafting.
> 10. Self-review and repair.
> 11. Final handoff and goal-state report.
>
> The self-review rubric must total 100 points:
>
> | Area                                                                | Points |
> | ------------------------------------------------------------------- | -----: |
> | Scope and protected-path discipline                                 |     15 |
> | Evidence discipline                                                 |     15 |
> | PAI Memory model accuracy                                           |     15 |
> | ISA model accuracy                                                  |     15 |
> | Single-writer policy quality                                        |     20 |
> | Promotion, audit, conflict, rollback, Pulse, and dual-engine safety |     15 |
> | Verification quality                                                |      5 |
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
> ### Required file: `docs/adapters/V5_CODEX_MEMORY_ISA_SINGLE_WRITER_POLICY_SPEC.md`
>
> Purpose: define the future single-writer policy required before Codex can write any canonical PAI Memory or ISA state.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Memory and ISA Single-Writer Policy Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Single-Writer Problem Statement
> ## Canonical PAI State Model
> ## Writer Role Model
> ## Adapter Mode Write Policy
> ## Read-Only Mode Policy
> ## Assisted Patch Mode Policy
> ## Controlled Single-Writer Mode Policy
> ## Codex-Only Replacement Mode Policy
> ## Dual-Engine Coexistence Policy
> ## Lock and Ownership Model
> ## Provenance Requirements
> ## Rollback Requirements
> ## Pulse Boundary Requirements
> ## Failure and Stop Conditions
> ## Required Future Proofs
> ## Prohibited Write Policies
> ## Non-Goals
> ```
>
> Required content includes PAI Memory and ISA canonicality, writer roles, adapter modes, documentation-only status, no writes in read-only modes, advisory-only assisted patch mode, future controlled-single-writer proof requirements, prohibition of `dual-engine-uncoordinated`, and no silent product-memory promotion.
>
> ### Required file: `docs/adapters/V5_CODEX_MEMORY_BOUNDARY_AND_PROMOTION_SPEC.md`
>
> Purpose: define the boundary between PAI Memory and product memory surfaces, and define future promotion discipline without authorizing promotion.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Memory Boundary and Promotion Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Memory Boundary Problem Statement
> ## PAI Memory Model
> ## Product Memory Model
> ## Non-Memory State Surfaces
> ## Boundary Rules
> ## Promotion Philosophy
> ## WORK Promotion Policy
> ## LEARNING Promotion Policy
> ## KNOWLEDGE Promotion Policy
> ## Product Memory Non-Promotion Rule
> ## Provenance and Attribution Requirements
> ## Review and Approval Requirements
> ## Conflict and Duplication Risks
> ## Required Future Proofs
> ## Prohibited Promotion Designs
> ## Non-Goals
> ```
>
> Required content includes PAI Memory categories `WORK`, `LEARNING`, and `KNOWLEDGE`; product memory surfaces; non-memory PAI state surfaces; explicit future approvals; and opt-in, provenance-tagged, reviewable, reversible, deduplicated, conflict-checked promotion discipline.
>
> ### Required file: `docs/adapters/V5_CODEX_ISA_WORKFLOW_AND_STATE_POLICY_SPEC.md`
>
> Purpose: define how future Codex workflows must treat ISA as the PAI system-of-record primitive without replacing it with `/goal`, task notes, transcripts, or product memory.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex ISA Workflow and State Policy Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## ISA Problem Statement
> ## ISA Role Model
> ## ISA and PRD Boundary
> ## ISA and Codex Goal Boundary
> ## ISA and Transcript Boundary
> ## ISA Read Policy
> ## ISA Advisory Patch Policy
> ## ISA Write Policy
> ## ISA Changelog and Verification Policy
> ## ISA Conflict Model
> ## ISA Ownership Model
> ## ISA and Pulse Boundary
> ## Required Future Proofs
> ## Prohibited ISA Designs
> ## Non-Goals
> ```
>
> Required content includes ISA as the v5 work/system-of-record primitive, PRD terminology not replacing ISA terminology, `/goal` not being ISA, no private user-local ISA reads, no ISA writes, future read policies, advisory patch policy, and future write prerequisites.
>
> ### Required file: `docs/adapters/V5_CODEX_MEMORY_ISA_AUDIT_AND_CONFLICT_SPEC.md`
>
> Purpose: define future audit, conflict, failure, and rollback requirements for any Codex-related Memory or ISA interaction.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Memory and ISA Audit and Conflict Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Audit Problem Statement
> ## Audit Philosophy
> ## Audit Field Model
> ## Memory Access Reporting
> ## ISA Access Reporting
> ## Write Attempt Reporting
> ## Promotion Reporting
> ## Conflict Detection Model
> ## Conflict Classification
> ## Rollback Reporting
> ## Pulse Reporting Boundary
> ## Failure Classification
> ## Advisory Output Model
> ## Non-Promotion Rule
> ## Required Future Proofs
> ## Prohibited Audit Designs
> ## Non-Goals
> ```
>
> Required content includes future advisory audit fields, conflict classes, failure classes, rollback reporting, Pulse boundary, and advisory output non-promotion.
>
> ### Required file: `docs/adapters/V5_CODEX_MEMORY_ISA_DECISION_LOG.md`
>
> Purpose: record S8H decisions, non-decisions, blocked decisions, and future architect questions for Memory and ISA single-writer policy.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Memory and ISA Decision Log
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Decisions Made in S8H
> ## Non-Decisions in S8H
> ## Blocked Decisions
> ## Future Architect Questions
> ## Decision Table
> ## Next Milestone Candidates
> ## Non-Goals
> ```
>
> Required content includes decisions `S8H-D01` through `S8H-D16`, advisory-only next milestone candidates, and architect approval requirements.
>
> ### Protected paths
>
> Do not modify protected repository paths or inspect private user-local state.
>
> ### Hard failure conditions
>
> S8H fails immediately if any file outside the approved write set is created or modified, any protected file is modified, runtime material is created, private user-local Memory or ISA state is inspected, PAI Memory or ISA is written, Pulse is started, Pulse endpoints are called, installer or migration tooling is run, Claude Code or Codex runtime is invoked, the docs overclaim Codex/Pulse/Memory/ISA readiness, product-memory promotion is authorized, dual-engine uncoordinated writes are authorized, or the goal advances beyond S8H.
>
> ### Required validation commands
>
> Required validation includes `git status --short`, `git diff --name-only | sort`, `git diff --check`, changed-file check, exact H1/H2 heading sequence check, content invariant check, writer role and mode check, Memory source table check, ISA operation check, audit field and conflict class check, decision ID check, and protected-path check.
>
> ### Acceptance criteria
>
> S8H is complete only if exactly the six approved S8H files are created or modified, no protected files are changed, no runtime material is created, no private user-local state is inspected, PAI Memory and ISA are not written, Pulse is not started or called, the execution plan contains this contract, all required IDs/tables/fields are present, all validation commands pass, the docs remain design-only, no prohibited claims or authorizations appear, and final handoff reports every required validation command.

## Milestones

1. Baseline status check.
2. S0-S7E reread.
3. Memory and ISA release evidence reread.
4. Canonical state boundary synthesis.
5. Single-writer policy spec drafting.
6. Memory boundary and promotion spec drafting.
7. ISA workflow and state policy spec drafting.
8. Memory/ISA audit and conflict spec drafting.
9. Memory/ISA decision log drafting.
10. Self-review and repair.
11. Final handoff and goal-state report.

## Self-Review Rubric

| Area                                                                | Points |
| ------------------------------------------------------------------- | -----: |
| Scope and protected-path discipline                                 |     15 |
| Evidence discipline                                                 |     15 |
| PAI Memory model accuracy                                           |     15 |
| ISA model accuracy                                                  |     15 |
| Single-writer policy quality                                        |     20 |
| Promotion, audit, conflict, rollback, Pulse, and dual-engine safety |     15 |
| Verification quality                                                |      5 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

- Any file outside the approved write set is created or modified.
- Any protected file is modified.
- Runtime adapter files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, or Pulse payloads are created.
- Private user-local Memory or ISA state is inspected or modified.
- PAI Memory or ISA is written.
- Pulse is started, Pulse endpoints are called, or `localhost:31337` is probed.
- Installers, Claude Code, Codex runtime, Codex import/migration tooling, or Codex hook/rule/execpolicy commands are run.
- The docs claim Codex is drop-in today or the official upstream engine.
- The docs authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, Pulse implementation, existing-local-v5 trial execution, product-memory promotion into PAI Memory, or dual-engine uncoordinated writes.
- The docs imply Claude-shaped files can be copied directly into Codex surfaces.
- The goal advances beyond S8H.

## Validation Commands

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Changed-file check for the six approved S8H files.
- Exact H1/H2 heading sequence check.
- Content invariant check.
- Writer role and mode check.
- Memory source table check.
- ISA operation check.
- Audit field and conflict class check.
- Decision ID check.
- Protected-path check.

## Progress

- Baseline status check: complete. Initial status showed no pre-existing repository changes before S8H files were created.
- S0-S7E reread: complete. Prior adapter conclusions preserved Codex as not currently proven drop-in and required designed seams before replacement claims.
- Memory and ISA release evidence reread: complete. Release-local PAI Memory, ISA, MemoryRetriever, hook, and documentation evidence was read only from approved repository paths.
- Canonical state boundary synthesis: complete. PAI Memory and ISA are treated as canonical PAI state; Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are treated as non-PAI state.
- Single-writer policy spec drafting: complete.
- Memory boundary and promotion spec drafting: complete.
- ISA workflow and state policy spec drafting: complete.
- Memory/ISA audit and conflict spec drafting: complete.
- Memory/ISA decision log drafting: complete.
- Self-review and repair: complete. Required checks passed after the approved S8H files were drafted.
- Final handoff and goal-state report: ready after final validation rerun.

## Iteration Log

| Iteration | Scope and protected-path discipline | Evidence discipline | PAI Memory model accuracy | ISA model accuracy | Single-writer policy quality | Promotion, audit, conflict, rollback, Pulse, and dual-engine safety | Verification quality | Score | Hard failures | Notes |
| --------- | ----------------------------------: | ------------------: | ------------------------: | -----------------: | ---------------------------: | ------------------------------------------------------------------: | -------------------: | ----: | ------------: | ----- |
| 1 | 15 | 15 | 15 | 15 | 19 | 15 | 5 | 99/100 | 0 | S8H stayed design-only, used approved repository-local evidence only, created only the six approved docs, preserved no-write/no-promotion boundaries, and passed the required validation suite. One point reserved because future controlled single-writer behavior remains intentionally unimplemented and unproven. |

## Surprises & Discoveries

- Release documentation distinguishes structured PAI Memory categories from product/runtime memory behavior; S8H therefore treats PAI Memory as canonical state and treats Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state as non-PAI state.
- Release ISA documentation frames ISA as the Ideal State Artifact and work/system-of-record primitive. S8H therefore blocks replacement of ISA terminology with PRD, task notes, transcripts, or product memory.
- Release-local evidence includes Memory/ISA-related hook and tool paths, but S8H did not execute hooks, tools, installers, Pulse, Claude Code, Codex runtime commands, or any migration/import tooling.

## Decision Log

- S8H goal started after the previous S7E goal was completed.
- Execution plan created before the five S8H deliverables.
- No official Codex documentation refresh was required because S8H added no new Codex capability claim.
- S8H authorizes only `documentation-only` status. Future read-only, assisted, controlled-write, dual-engine, or replacement modes remain blocked pending architect-approved proof.
- Product-memory promotion into PAI Memory remains unauthorized by default and requires future explicit approval, provenance, conflict checks, and rollback.
- Existing-local-v5 Memory/ISA reads remain unauthorized in S8H.

## Outcomes & Retrospective

- Created exactly the six approved S8H documentation artifacts.
- No protected paths were modified.
- No runtime adapter files, root `AGENTS.md`, `.codex/`, fixtures, harnesses, schemas, manifests, audit artifacts, generated configs, migration scripts, Memory payloads, ISA payloads, or Pulse payloads were created.
- PAI Memory and ISA were not written.
- Private user-local Memory/ISA state was not inspected.
- Pulse was not started and Pulse endpoints were not called.
- Validation results recorded before final handoff:
  - `git status --short`: only the six approved S8H docs are shown as added.
  - `git diff --name-only | sort`: lists exactly the six approved S8H docs.
  - `git diff --check`: passed.
  - Changed-file check: passed.
  - Exact H1/H2 heading sequence check: passed.
  - Content invariant check: passed.
  - Writer role and mode check: passed.
  - Memory source table check: passed.
  - ISA operation check: passed.
  - Audit field and conflict class check: passed.
  - Decision ID check: passed.
  - Protected-path check: passed with no output.
