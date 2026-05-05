# V5 Codex Fixture Trial Coverage Matrix

## Purpose

Define the future coverage matrix showing how a read-only fixture trial would cover the accepted seams and drop-in readiness gates without implementing the trial.

## Scope

This document is design-only. It does not create a fixture, harness, manifest, executable schema, audit artifact, generated config, runtime file, adapter payload, trial output, root `AGENTS.md`, or `.codex/`.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement is plausible only through a designed adapter. Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Evidence Base

Evidence comes from S0-S8H adapter docs, especially authority seam, launcher seam, inference seam, hook lifecycle, Pulse read-only event, Memory/ISA single-writer, manifest schema proposal, audit schema proposal, dry-run validation, and drop-in readiness gate docs.

No new Codex capability claim is introduced in S9A.

## Coverage Problem Statement

A future fixture-trial must show what is covered, what is blocked, what remains documentation-only, and what is prohibited. Without a coverage matrix, a future read-only fixture could accidentally overclaim drop-in readiness while leaving authority, Pulse, Memory, ISA, hook lifecycle, rollback, or unsupported-surface gaps untested.

## Coverage Classification Model

| Class | Meaning |
| --- | --- |
| `CV-0: Not covered` | No future trial coverage is defined. |
| `CV-1: Documentation coverage` | Coverage is documented but not executable. |
| `CV-2: Dry-run design coverage` | Coverage is designed for future dry-run validation. |
| `CV-3: Fixture-read-only candidate` | Coverage may be validated against a future isolated fixture. |
| `CV-4: Existing-local-v5 future candidate` | Coverage may be validated against live local PAI only after separate approval. |
| `CV-5: Blocked` | Coverage is blocked by unresolved safety or authority issues. |
| `CV-6: Prohibited` | Coverage must not be attempted in read-only mode. |

## Seam Coverage Matrix

| Coverage ID | Surface or gate | Source spec | Coverage class | Future fixture evidence | Main gap | Blocks drop-in? | S9A status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CVG-001 | PAI_SYSTEM_PROMPT authority | Authority seam | `CV-3: Fixture-read-only candidate` | Future authority envelope references doctrine priority. | No behavioral proof yet. | Yes. | Designed only. |
| CVG-002 | CLAUDE.md non-copy boundary | Authority seam and compact router | `CV-3: Fixture-read-only candidate` | Future scan proves `CLAUDE.md` is not copied into Codex surfaces. | No future scan exists. | Yes. | Designed only. |
| CVG-003 | Compact router sketch non-installation | Compact router | `CV-2: Dry-run design coverage` | Future proof shows router remains non-installed unless authorized. | Root `AGENTS.md` remains protected. | Yes. | Designed only. |
| CVG-004 | Launcher seam | Launcher seam | `CV-3: Fixture-read-only candidate` | Future launcher plan has selected engine, denied behaviors, rollback path. | No executable launcher exists. | Yes. | Designed only. |
| CVG-005 | Inference seam | Inference seam | `CV-3: Fixture-read-only candidate` | Future request envelope and response envelope validate unsupported surfaces. | No model call proof exists. | Yes. | Designed only. |
| CVG-006 | Engine profile capability contract | Engine profile contract | `CV-2: Dry-run design coverage` | Future capability declaration reports unsupported surfaces. | No engine profile instance exists. | Yes. | Designed only. |
| CVG-007 | Hook lifecycle mapping | Hook lifecycle mapping | `CV-3: Fixture-read-only candidate` | Future payload/event matrix maps or rejects Claude hook behavior. | No hook execution proof exists. | Yes. | Designed only. |
| CVG-008 | Event/context envelope | Event/context envelope | `CV-3: Fixture-read-only candidate` | Future event fields prove no private reads and no writes. | No envelope instance exists. | Yes. | Designed only. |
| CVG-009 | Hook permission/safety | Hook permission/safety | `CV-3: Fixture-read-only candidate` | Future denied action and sandbox reports prove fail-closed behavior. | No Codex rules or hooks installed. | Yes. | Designed only. |
| CVG-010 | Pulse identity | Pulse bridge identity | `CV-2: Dry-run design coverage` | Future identity report labels Codex as adapter candidate. | No Pulse bridge exists. | Yes. | Designed only. |
| CVG-011 | Pulse read-only event model | Pulse read-only event model | `CV-3: Fixture-read-only candidate` | Future event class table proves no-start/no-call posture. | No live Pulse observation allowed. | Yes. | Designed only. |
| CVG-012 | Pulse no-start/no-call | Pulse read-only event and audit specs | `CV-3: Fixture-read-only candidate` | Future proof records startup and endpoint call status as denied/none. | No process or endpoint proof yet. | Yes. | Designed only. |
| CVG-013 | Memory single-writer no-write | Memory/ISA single-writer | `CV-3: Fixture-read-only candidate` | Future no-write report for PAI Memory. | No fixture validation exists. | Yes. | Designed only. |
| CVG-014 | Memory boundary/non-promotion | Memory boundary/promotion | `CV-3: Fixture-read-only candidate` | Future source classification proves product memories are not PAI Memory. | No promotion validation exists. | Yes. | Designed only. |
| CVG-015 | ISA workflow no-write | ISA workflow/state | `CV-3: Fixture-read-only candidate` | Future no-write report for ISA operations. | No fixture validation exists. | Yes. | Designed only. |
| CVG-016 | Memory/ISA audit/conflict | Memory/ISA audit/conflict | `CV-2: Dry-run design coverage` | Future audit fields classify read/write/promotion/conflict status. | No audit artifact created. | Yes. | Designed only. |
| CVG-017 | Manifest schema proposal | Manifest schema proposal | `CV-2: Dry-run design coverage` | Future non-executable manifest field coverage. | No manifest instance exists. | Yes. | Designed only. |
| CVG-018 | Audit schema proposal | Audit schema proposal | `CV-2: Dry-run design coverage` | Future non-executable audit field coverage. | No audit artifact exists. | Yes. | Designed only. |
| CVG-019 | Dry-run validation | Dry-run validation spec | `CV-2: Dry-run design coverage` | Future validation order and invariant checks. | No validator or harness exists. | Yes. | Designed only. |
| CVG-020 | Rollback/no-residue | Readiness gates and failure model | `CV-3: Fixture-read-only candidate` | Future residue report and rollback statement. | No future output path exists. | Yes. | Designed only. |
| CVG-021 | Existing-local-v5 boundary | Read-only trial and S8H policies | `CV-4: Existing-local-v5 future candidate` | Future separate approval, manifest, privacy, no-write proof. | Live state access is not authorized. | Yes. | Designed only. |
| CVG-022 | Dual-engine boundary | S6/S8H readiness and single-writer policy | `CV-5: Blocked` | Future engine labels and single-writer ownership map. | Dual-engine uncoordinated writes prohibited. | Yes. | Designed only. |
| CVG-023 | Product memory boundary | S7A and S8H memory policy | `CV-3: Fixture-read-only candidate` | Future report keeps Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state outside PAI Memory. | No promotion proof exists. | Yes. | Designed only. |
| CVG-024 | Unsupported surface reporting | All seam specs | `CV-3: Fixture-read-only candidate` | Future `unsupported_surface_report` lists every unmapped surface. | No fixture report exists. | Yes. | Designed only. |
| CVG-025 | Drop-in claim prevention | Drop-in readiness gates | `CV-2: Dry-run design coverage` | Future audit states Codex is not drop-in unless gates pass. | No gate has runtime proof. | Yes. | Designed only. |

## Drop-In Gate Coverage Matrix

S9A maps future fixture coverage to drop-in gates G0-G15, but no runtime gate passes in S9A. Authority, router, launcher, inference, hook lifecycle, Pulse, Memory, ISA, existing-local-v5, single-writer, dual-engine, rollback, and support posture remain future proof areas.

## Fixture Source Coverage Matrix

| Source kind | Future coverage class | S9A posture | Main restriction |
| --- | --- | --- | --- |
| `release-fixture` | `CV-3: Fixture-read-only candidate` | Designed only. | No fixture is created. |
| `sanitized-user-fixture` | `CV-3: Fixture-read-only candidate` | Designed only. | No user state is read. |
| `existing-local-v5-read-only` | `CV-4: Existing-local-v5 future candidate` | Future-only. | Separate approval required. |

## Denied Behavior Coverage Matrix

Denied behavior coverage must include protected-path modification, root `AGENTS.md`, `.codex/`, release-file writes, Codex surface writes, Pulse startup, Pulse endpoint calls, Memory writes, ISA writes, product memory promotion, fixture residue, harness execution, manifest creation, audit artifact creation, executable schema creation, and drop-in overclaim.

## Memory ISA Pulse Coverage Matrix

PAI Memory, ISA, and Pulse are central safety surfaces. Future fixture coverage must prove:

- `PAI Memory` no-write.
- `ISA` no-write.
- `single-writer` mode not entered.
- `Pulse is central` and not optional.
- Pulse no-start and no-call.
- Product memories are not PAI Memory.
- `/goal` state is not ISA.
- Advisory output is not canonical state.

## Unsupported Surface Coverage Matrix

Every unsupported Claude, Codex, Pulse, Memory, ISA, hook lifecycle, launcher, inference, manifest, audit, schema, rollback, or product-memory surface must be reported through `unsupported_surface_report`.

Unsupported surfaces must be reported, not silently emulated.

## Coverage Gaps After S9A

Remaining gaps:

- No fixture exists.
- No harness exists.
- No manifest instance exists.
- No audit artifact exists.
- No executable schema exists.
- No trial has run.
- No authority behavior is proven.
- No launcher or inference behavior is proven.
- No hook lifecycle behavior is proven.
- No Pulse behavior is proven.
- No Memory/ISA no-write behavior is proven.
- No rollback/no-residue proof exists.
- No existing-local-v5 approval exists.

## Required Future Proofs

Required future proofs:

- Future coverage matrix is tied to a bounded write set.
- Future fixture source is isolated.
- Future denied behavior checks fail closed.
- Future output includes `denied_action_report` and `unsupported_surface_report`.
- Future audit is advisory only.
- Future rollback/no-residue proof exists.
- Future drop-in claim remains blocked unless gates pass.

## Prohibited Coverage Claims

Prohibited claims:

- S9A proves fixture readiness.
- S9A creates a read-only fixture.
- S9A creates a manifest, audit artifact, schema, or harness.
- S9A proves Codex is drop-in.
- S9A proves Pulse parity.
- S9A authorizes Memory writes or ISA writes.
- S9A authorizes existing-local-v5 trial execution.
- S9A authorizes product-memory promotion into PAI Memory.
- S9A authorizes dual-engine uncoordinated writes.

## Non-Goals

S9A does not implement the adapter, create fixtures, create a test harness, create manifests, create audit artifacts, create executable schemas, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create generated configs, create migration scripts, create runtime files, create adapter payloads, create Memory payloads, create ISA payloads, create Pulse payloads, create trial outputs, run a read-only trial, inspect private user-local state, read live existing-local-v5 state, modify release files, start Pulse, call Pulse endpoints, probe `localhost:31337`, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, run Codex hook/rule/execpolicy commands, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, authorize product-memory promotion into PAI Memory, authorize dual-engine uncoordinated writes, or advance beyond S9A.
