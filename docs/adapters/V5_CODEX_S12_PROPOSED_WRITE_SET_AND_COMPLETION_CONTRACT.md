# V5 Codex S12 Proposed Write Set and Completion Contract

## Purpose

Propose a future S12 live read-only trial readiness contract for architect review.

Codex is not currently proven drop-in for existing local PAI v5 files. S12 is proposed only and not approved by S11D.

## Scope

This document is a proposal only. It does not authorize S12, live trials, live existing-local-v5 access, runtime adapter implementation, root `AGENTS.md`, `.codex/`, Pulse startup, Pulse endpoint calls, PAI Memory writes, ISA writes, product-memory promotion, or Codex drop-in claims.

Proposed S12 must be read-only unless separately approved.

## Evidence Base

Evidence base:

- S10 fixture-only closeout.
- S11A release-fixture evidence report.
- S11B report-generator negative controls.
- S11C readiness gate evaluation report.
- S11D S11 evidence closeout and S12 readiness gate proposal.

Release-fixture evidence is necessary but insufficient for any drop-in claim.

## Contract Proposal Status

S12 is proposed only. S12 is not approved by S11D.

Architect approval is required before any S12 work. Explicit user consent design is required before any live local read.

## Proposed S12 Objective

Proposed objective:

Create a future architect-approved, read-only live trial readiness evidence report that evaluates explicitly selected local sources under explicit user consent design, without writes, without runtime adapter implementation, without Pulse startup or calls, without PAI Memory or ISA writes, and without any drop-in claim.

## Proposed S12 Approved Write Set

Proposed write-set table:

| Proposed path | Purpose | Status |
| --- | --- | --- |
| `docs/adapters/V5_S12_EXEC_PLAN.md` | Execution plan with architect-approved S12 contract. | Proposed only |
| `docs/adapters/V5_CODEX_S12_LIVE_READ_ONLY_TRIAL_REPORT.md` | Non-canonical S12 evidence report. | Proposed only |
| `docs/adapters/V5_CODEX_S12_SOURCE_SELECTION_RECORD.md` | Explicit source selection and explicit user consent design record. | Proposed only |
| `docs/adapters/V5_CODEX_S12_DENIED_ACTIONS_AND_UNSUPPORTED_SURFACES.md` | Denied-action and unsupported-surface report. | Proposed only |
| `docs/adapters/V5_CODEX_S12_ROLLBACK_AND_NO_RESIDUE_REPORT.md` | Rollback and no-residue evidence report. | Proposed only |

No root `AGENTS.md`, `.codex/`, runtime adapter file, manifest, executable schema, PAI runtime audit artifact, live-trial artifact outside the approved write set, runtime payload, Memory payload, ISA payload, or Pulse payload is proposed.

## Proposed S12 Protected Paths

Protected paths:

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

Future S12 must not modify protected paths.

## Proposed S12 Allowed Reads

Allowed reads, if architect-approved:

- Repository-local S10/S11 docs and evidence.
- Repository-local S10/S11 fixture corpus and harness files.
- Explicitly selected local read-only sources named in the approved S12 card and consent record.
- Read-only `PAI_DIR` detection only if explicitly approved and consent-bound.

No live source is allowed by default.

## Proposed S12 Forbidden Reads

Forbidden reads by default:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`
- live existing-local-v5 state
- broad home-directory scans
- inferred local configuration
- implicit `PAI_DIR` discovery

Any exception requires explicit architect approval and explicit user consent design.

## Proposed S12 Forbidden Writes

Forbidden writes:

- PAI Memory writes.
- ISA writes.
- Product-memory promotion into PAI Memory.
- Pulse state writes.
- Root `AGENTS.md`.
- `.codex/`.
- Runtime adapter files.
- Codex config, hooks, rules, skills, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts outside the approved write set, runtime payloads, and committed negative fixtures.

## Proposed S12 Consent Requirements

Proposed S12 must require explicit user consent design before any live local read.

The consent design must state:

- exact source paths or source selectors;
- why each source is needed;
- whether `PAI_DIR` detection is allowed;
- how consent is recorded in non-canonical evidence;
- how refusal is handled;
- how no-write behavior is verified;
- how no live user-local default behavior is preserved.

No live local read may occur without explicit architect approval and explicit user consent.

## Proposed S12 Validation Commands

Proposed validation commands must include:

```bash
git status --short
git diff --name-only | sort
git diff --check
```

Future S12 must also include source-selection validation, consent-record validation, protected-path validation, no generated artifact validation, no Pulse startup/call validation, no PAI Memory write validation, no ISA write validation, and no drop-in claim content validation.

## Proposed S12 Acceptance Criteria

S12-AC-001 approved write set only

S12-AC-002 no protected paths changed

S12-AC-003 no root AGENTS.md

S12-AC-004 no .codex

S12-AC-005 no default live user-local state

S12-AC-006 explicit source selection

S12-AC-007 explicit user consent model

S12-AC-008 PAI_DIR detection is read-only

S12-AC-009 no Pulse startup

S12-AC-010 no Pulse endpoint calls

S12-AC-011 no PAI Memory writes

S12-AC-012 no ISA writes

S12-AC-013 no product-memory promotion

S12-AC-014 no Claude file direct-copy

S12-AC-015 authority boundary preserved

S12-AC-016 launcher/inference boundary preserved

S12-AC-017 hook/lifecycle boundary preserved

S12-AC-018 unsupported-surface reporting

S12-AC-019 evidence report is non-canonical

S12-AC-020 rollback/no-residue reporting

S12-AC-021 no Codex runtime adapter implementation

S12-AC-022 no Claude Code invocation

S12-AC-023 no drop-in claim

S12-AC-024 architect review required

## Proposed S12 Hard Failure Conditions

S12 must fail if any file outside its approved write set changes; protected paths change; root `AGENTS.md` or `.codex/` is created or modified; default live user-local state is read; explicit user consent design is missing; unapproved existing-local-v5 access occurs; PAI Memory or ISA is written; Pulse is started or called; product-memory promotion occurs; Claude Code or Codex runtime is invoked; runtime adapter work begins; or any deliverable claims Codex is drop-in today or official upstream engine.

## Proposed S12 Final Handoff Format

Proposed final handoff headings are: Files changed; Behavior changed; Tests run; Known risks; Protected files changed; Goal state; Recommended next architect decision.

## Architect Review Required

Architect review is required before any S12 work. S11D does not approve S12.

The architect must approve the objective, approved write set, protected paths, allowed reads, forbidden reads, explicit user consent design, validation commands, hard failures, and final handoff.

## Prohibited Contract Semantics

The proposed S12 contract must not authorize live trials by implication, runtime adapter work, PAI Memory writes, ISA writes, Pulse startup/calls, existing-local-v5 access without explicit approval, product-memory promotion, dual-engine uncoordinated writes, Codex drop-in claims, or official upstream engine claims.

## Non-Goals

This proposal does not authorize S12, live trials, live user-local reads, existing-local-v5 access, runtime adapter implementation, root `AGENTS.md`, `.codex/`, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory promotion, Codex runtime invocation, Claude Code invocation, manifests, executable schemas, audit artifacts, runtime payloads, or drop-in claims.
