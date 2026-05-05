# V5 Codex S10A Write Set and Acceptance Contract

## Purpose

Propose the exact future S10A write set and acceptance contract for architect review, without approving or starting S10A.

## Scope

This is a proposed contract only.

S10A is not approved by S9B. S10A may begin only after architect approval.

S9B does not create fixtures, harnesses, manifests, audit artifacts, executable schemas, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, runtime files, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, fixture files, or harness files.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement is plausible only through a designed adapter. Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CODEX_FIRST_FIXTURE_IMPLEMENTATION_PLAN.md`
- `docs/adapters/V5_CODEX_FIXTURE_CORPUS_DESIGN_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_HARNESS_DESIGN_SPEC.md`
- `docs/adapters/V5_CODEX_INTEGRATED_READ_ONLY_FIXTURE_TRIAL_ARCHITECTURE.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_SEQUENCE_AND_GATE_MODEL.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_COVERAGE_MATRIX.md`
- `docs/adapters/V5_CODEX_TRIAL_FAILURE_ROLLBACK_AND_AUDIT_MODEL.md`

No new Codex capability claim is introduced in S9B.

## Contract Proposal Status

The proposed S10A contract is advisory only. It is not an approval to implement, create files, run harnesses, create fixtures, create manifests, create audit artifacts, create schemas, or run trials.

Required phrase for downstream review: S10A is not approved by S9B.

## Proposed S10A Objective

Proposed future S10A objective:

Create the first fixture-only implementation for the PAI v5 Codex read-only fixture trial by adding an isolated fixture corpus, fixture metadata, a read-only harness, harness documentation, and an S10A execution plan under an architect-approved write set.

Future S10A must not claim Codex is drop-in.

## Proposed S10A Approved Write Set

Proposed future S10A write paths must be under non-runtime adapter-test areas only.

Proposed S10A write paths must not include:

- `Releases/`
- `.claude/`
- `PAI/`
- root `AGENTS.md`
- `.codex/`
- root hooks, skills, agents, commands, settings, or installers.
- Live user-local paths.

Proposed write-set table:

| Proposed path | Proposed artifact type | Purpose | Runtime payload? | Safety rationale | Requires architect approval? |
| --- | --- | --- | --- | --- | --- |
| `docs/adapters/V5_S10A_EXEC_PLAN.md` | S10A execution plan | Record future S10A scope, contract, validation, and outcomes. | No. | Documentation-only control file. | Yes. |
| `docs/adapters/fixture-trial/v5-s10a/fixtures/` | Fixture corpus | Hold isolated fixture files if approved. | No. | Non-runtime adapter-test area, not live PAI state. | Yes. |
| `docs/adapters/fixture-trial/v5-s10a/fixtures/metadata/` | Fixture metadata | Hold fixture metadata if approved. | No. | Declarative test data only. | Yes. |
| `docs/adapters/fixture-trial/v5-s10a/harness/` | Harness script | Hold read-only harness script if approved. | No. | Non-runtime validation tool, not adapter runtime. | Yes. |
| `docs/adapters/fixture-trial/v5-s10a/harness/README.md` | Harness README | Explain future read-only harness operation and constraints. | No. | Documentation in non-runtime adapter-test area. | Yes. |
| `docs/adapters/fixture-trial/v5-s10a/reports/examples/` | Expected report examples | Hold expected report examples only if separately approved. | No. | Advisory examples only, not audit artifacts. | Separate explicit approval. |
| `docs/adapters/fixture-trial/v5-s10a/README.md` | Fixture-trial README | Explain fixture corpus and validation posture. | No. | Documentation in non-runtime adapter-test area. | Yes. |

This proposed write set is not approved by S9B.

## Proposed S10A Protected Paths

Proposed S10A protected paths should include:

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
- Live user-local paths.

## Proposed S10A Allowed Reads

Proposed S10A allowed reads:

- S0-S9B adapter docs.
- Repository-local release files under `Releases/v5.0.0/`, read-only.
- Approved future S10A fixture paths, after creation under approved write set.

## Proposed S10A Forbidden Reads

Proposed S10A forbidden reads:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`
- Live existing-local-v5 state.
- Private user-local state.
- Pulse endpoints.

## Proposed S10A Forbidden Writes

Proposed S10A forbidden writes:

- Protected paths.
- Release files.
- Root `AGENTS.md`.
- `.codex/`.
- Codex runtime surfaces.
- Claude runtime surfaces.
- PAI Memory.
- ISA.
- Pulse state.
- Live user-local state.
- Runtime adapter files.

## Proposed S10A Fixture Files

Proposed fixture files are future-only. They should cover fixture corpus classes `FX-001` through `FX-012` if architect-approved.

S9B creates no fixture files.

## Proposed S10A Harness Files

Proposed harness files are future-only. They should implement read-only checks `HC-001` through `HC-020` if architect-approved.

S9B creates no harness files.

## Proposed S10A Documentation Files

Proposed documentation files:

- S10A execution plan.
- Fixture-trial README.
- Harness README.
- Optional expected report examples documentation only if separately approved.

## Proposed S10A Validation Commands

Proposed future S10A validation should include:

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Proposed changed-file check for approved S10A paths.
- Fixture ID check.
- Fixture metadata field check.
- Harness check ID check.
- Harness read-only static check.
- Protected-path check.
- No live user-local path check.
- No root `AGENTS.md` check.
- No `.codex/` check.
- No Pulse startup/call check.
- PAI Memory no-write check.
- ISA no-write check.
- Unsupported surface report check.
- Denied action report check.
- Rollback/no-residue report check.

## Proposed S10A Acceptance Criteria

Proposed S10A acceptance IDs:

| Acceptance ID | Proposed criterion |
| --- | --- |
| S10A-AC-001 | Approved write set only. |
| S10A-AC-002 | No protected paths changed. |
| S10A-AC-003 | No root `AGENTS.md`. |
| S10A-AC-004 | No `.codex/`. |
| S10A-AC-005 | No live user-local state. |
| S10A-AC-006 | No Pulse startup. |
| S10A-AC-007 | No Pulse endpoint calls. |
| S10A-AC-008 | No PAI Memory writes. |
| S10A-AC-009 | No ISA writes. |
| S10A-AC-010 | No Claude file direct-copy into Codex surfaces. |
| S10A-AC-011 | Fixture metadata exists. |
| S10A-AC-012 | Harness is read-only. |
| S10A-AC-013 | Denied-path checks exist. |
| S10A-AC-014 | Unsupported-surface reporting exists. |
| S10A-AC-015 | Rollback/no-residue reporting exists. |
| S10A-AC-016 | No drop-in claim. |

## Proposed S10A Hard Failure Conditions

Proposed S10A hard failures:

- Any file outside approved S10A write set is created or modified.
- Any protected file is modified.
- Runtime adapter files are created.
- Root `AGENTS.md` is created or modified.
- `.codex/` is created or modified.
- Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, or migration scripts are created.
- Live user-local state is read.
- Live existing-local-v5 state is read.
- Pulse is started.
- Pulse endpoints are called.
- `localhost:31337` is probed.
- PAI Memory is written.
- ISA is written.
- Claude Code is invoked.
- Codex is invoked as runtime unless explicitly approved in the future S10A card.
- Product memories are promoted into PAI Memory.
- Dual-engine uncoordinated writes occur.
- Codex is claimed drop-in.

## Proposed S10A Final Handoff Format

Proposed future S10A final handoff headings:

- Files changed.
- Behavior changed.
- Tests run.
- Known risks.
- Protected files changed.
- Goal state.
- Recommended next architect decision.

## Architect Review Required

Architect review is required before S10A begins. S9B does not authorize S10A implementation, fixture creation, harness creation, manifest creation, audit artifact creation, schema creation, or trial execution.

## Prohibited Contract Semantics

Prohibited semantics:

- Treating this proposed contract as S10A approval.
- Including `Releases/`, `.claude/`, `PAI/`, root `AGENTS.md`, `.codex/`, root hooks/skills/agents/commands/settings/installers, or live user-local paths in the proposed write set.
- Authorizing runtime adapter files.
- Authorizing PAI Memory writes or ISA writes.
- Authorizing Pulse startup, endpoint calls, or implementation.
- Authorizing existing-local-v5 trial execution.
- Authorizing product-memory promotion into PAI Memory.
- Authorizing dual-engine uncoordinated writes.

## Non-Goals

S9B does not implement the adapter, approve S10A, create fixtures, create a test harness, create manifests, create audit artifacts, create executable schemas, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create generated configs, create migration scripts, create runtime files, create adapter payloads, create Memory payloads, create ISA payloads, create Pulse payloads, create trial outputs, create fixture files, create harness files, run a read-only trial, inspect private user-local state, read live existing-local-v5 state, modify release files, start Pulse, call Pulse endpoints, probe `localhost:31337`, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, run Codex hook/rule/execpolicy commands, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, imply Claude-shaped files can be copied directly into Codex surfaces, authorize product-memory promotion into PAI Memory, authorize dual-engine uncoordinated writes, or advance beyond S9B.
