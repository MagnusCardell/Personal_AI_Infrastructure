# V5 Codex S13 Proposed Write Set and Completion Contract

## Purpose

Propose a future S13 write set and completion contract for architect review without approving S13.

## Scope

This is a proposal only. S13 is not approved by S12E and must not begin from this document.

Proposed S13 must be read-only unless separately approved. It must not write PAI Memory or ISA, must not start Pulse or call Pulse endpoints unless separately approved, must not create root `AGENTS.md` or `.codex/`, must not claim drop-in status, must not claim Codex is the official upstream engine, and must not require uninstalling Claude Code.

## Evidence Base

Evidence base:

- S11 release-fixture evidence and readiness gates.
- S12A live-read-only consent, source-selection, preflight, abort, and reporting designs.
- S12B consent artifact schema and validation design.
- S12C PAI_DIR dry-run detection design.
- S12D preflight report schema, validation sequence, abort/evidence, and non-canonical output policies.
- S12E closeout and S13 gate proposal.

Codex is not currently proven drop-in for existing local PAI v5 files.

## Contract Proposal Status

S13 is proposed only. S13 is not approved by S12E.

Architect approval is required before any future S13 work. This document is not a live-read authorization and not runtime adapter authorization.

## Proposed S13 Objective

Proposed objective:

Run a future architect-approved, explicitly consented, read-only live local PAI v5 trial against an explicitly selected source root, after a future preflight pass, producing only approved non-canonical evidence and denied-action reporting, with no writes to live state, PAI Memory, ISA, Pulse, root `AGENTS.md`, `.codex/`, product memory, or runtime adapter surfaces.

## Proposed S13 Approved Write Set

Proposed write-set table:

| Proposed path | Proposed artifact type | Purpose | Runtime payload? | Canonical PAI state? | Requires architect approval? |
| --- | --- | --- | --- | --- | --- |
| `docs/adapters/V5_S13A_EXEC_PLAN.md` | Execution plan | Record approved S13A contract and results. | No | No | Yes |
| `docs/adapters/V5_CODEX_S13_LIVE_READ_ONLY_TRIAL_REPORT.md` | Non-canonical evidence report | Summarize approved read-only live trial evidence. | No | No | Yes |
| `docs/adapters/V5_CODEX_S13_SOURCE_SELECTION_AND_CONSENT_RECORD.md` | Non-canonical consent/source record | Record explicit consent and explicit source selection for review. | No | No | Yes |
| `docs/adapters/V5_CODEX_S13_PREFLIGHT_RESULT_SUMMARY.md` | Non-canonical preflight summary | Record future preflight pass or abort summary. | No | No | Yes |
| `docs/adapters/V5_CODEX_S13_DENIED_ACTIONS_AND_UNSUPPORTED_SURFACES.md` | Denied-action report | Record denied actions and unsupported surfaces. | No | No | Yes |
| `docs/adapters/V5_CODEX_S13_ROLLBACK_AND_NO_RESIDUE_REPORT.md` | No-residue report | Record rollback and no-residue evidence. | No | No | Yes |
| `docs/adapters/V5_CODEX_S13_DECISION_LOG.md` | Decision log | Record S13 decisions, non-decisions, and future questions. | No | No | Yes |

No proposed S13 output is PAI Memory, ISA, Pulse state, Claude memory, Codex memory, a manifest, an executable schema, a runtime payload, or proof that Codex is drop-in.

## Proposed S13 Protected Paths

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

Future S13 must not modify protected paths.

## Proposed S13 Allowed Reads

Allowed reads, if future architect approval exists:

- Repository-local S10/S11/S12/S12E adapter docs and evidence.
- Existing repository-local S10/S11 fixture and report files as read-only reference evidence.
- Exactly one explicitly selected live source root, only after explicit user consent and preflight pass.
- Read-only PAI_DIR candidate evidence only if explicitly approved, source-bound, and consent-bound.

No live source is allowed by default.

## Proposed S13 Forbidden Reads

Forbidden reads by default:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`
- Product memory.
- Broad home-directory scans.
- Shell history, inferred local config, subscription state, or prior interaction.
- Any personal clone without explicit architect approval and explicit user consent.
- Any source outside the approved source root.

Future S13 must not read product memories by default.

## Proposed S13 Forbidden Writes

Forbidden writes:

- PAI Memory writes.
- ISA writes.
- Pulse state writes.
- Product-memory promotion.
- Root `AGENTS.md`.
- `.codex/`.
- Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts outside the approved write set, runtime payloads, reports outside the approved write set, fixtures, and committed negative fixtures.
- Any live-source write.

## Proposed S13 Consent Requirements

Proposed S13 must require explicit user consent. Consent must identify source kind, source root, allowed reads, forbidden reads, forbidden writes, retention, revocation, expiration, rollback/no-residue expectations, reporting output, and the no drop-in claim.

Consent must not be inferred from Claude Code installation, Codex installation, dual subscriptions, shell history, product memory, local config, or prior interaction.

## Proposed S13 Source Selection Requirements

Proposed S13 must require explicit source selection. Source selection must bind exactly one source kind and one source root to consent.

Source selection must not use default live reads, broad home scans, product memory, shell history, or inferred local config.

## Proposed S13 PAI_DIR Detection Requirements

Proposed S13 PAI_DIR detection, if approved, must remain read-only, dry-run, source-specific, path-bounded, consent-bound, confidence-qualified, abortable, and non-canonical.

PAI_DIR detection must not read live `~/.claude/PAI` by default and must not treat a clean clone as a live PAI install.

## Proposed S13 Preflight Requirements

Proposed S13 must require a future preflight pass before any live read. Preflight must validate architect approval, consent, source kind, source root, PAI_DIR candidate, allowed reads, forbidden reads, forbidden writes, product memory denial, Pulse denial, Memory/ISA write denial, runtime invocation denial, reporting boundaries, retention, rollback/no-residue, and no drop-in claim.

Any failed preflight check must abort.

## Proposed S13 Reporting Requirements

Proposed S13 reporting must be non-canonical, retention-bounded, rollback/no-residue-bounded, and clear about denied actions and unsupported surfaces.

Report output must state it is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.

## Proposed S13 Validation Commands

Future S13 validation commands should include, if architect-approved:

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Changed-file allowlist check for the future S13 approved write set.
- Protected-path check.
- No root `AGENTS.md` check.
- No `.codex/` check.
- Consent record validation.
- Source selection validation.
- PAI_DIR read-only detection validation if approved.
- Preflight pass validation.
- No Pulse startup and no Pulse endpoint call validation.
- No PAI Memory write and no ISA write validation.
- No product memory read by default and no product memory promotion validation.
- No Claude Code invocation validation.
- No Codex runtime adapter execution validation.
- Unsupported-surface and denied-action content validation.
- Non-canonical evidence output validation.
- Rollback/no-residue validation.
- No drop-in claim and no official-upstream claim content validation.

These are proposed only and do not approve S13.

## Proposed S13 Acceptance Criteria

S13-AC-001 approved write set only

S13-AC-002 no protected paths changed

S13-AC-003 no root AGENTS.md

S13-AC-004 no .codex

S13-AC-005 explicit user consent present

S13-AC-006 explicit source selection present

S13-AC-007 PAI_DIR detection remains read-only

S13-AC-008 preflight pass required

S13-AC-009 no Pulse startup

S13-AC-010 no Pulse endpoint calls

S13-AC-011 no PAI Memory writes

S13-AC-012 no ISA writes

S13-AC-013 no product-memory reads by default

S13-AC-014 no product-memory promotion

S13-AC-015 no Claude file direct-copy

S13-AC-016 no Claude Code invocation

S13-AC-017 no Codex runtime adapter execution

S13-AC-018 no Codex import or migration tooling

S13-AC-019 no installer execution

S13-AC-020 unsupported-surface reporting

S13-AC-021 denied-action reporting

S13-AC-022 non-canonical evidence output

S13-AC-023 rollback/no-residue reporting

S13-AC-024 no drop-in claim

S13-AC-025 no official-upstream claim

S13-AC-026 no dual-engine uncoordinated writes

S13-AC-027 no consent artifact promotion into PAI Memory

S13-AC-028 no report promotion into ISA or Pulse

S13-AC-029 final architect review required

S13-AC-030 no advance to runtime adapter work

## Proposed S13 Hard Failure Conditions

Future S13 fails if any file outside its approved write set changes; any protected path changes; root `AGENTS.md` or `.codex/` is created or modified; explicit user consent is absent; source selection is absent; preflight does not pass; PAI_DIR detection writes or overclaims; Pulse is started or called; PAI Memory or ISA is written; product memory is read by default or promoted; Claude files are copied directly into Codex surfaces; Claude Code or Codex runtime adapter execution occurs; Codex import or migration tooling runs; installers run; unsupported surfaces are silently ignored; evidence output becomes canonical; rollback/no-residue reporting is missing; a no drop-in claim is missing; a no official-upstream claim is missing; dual-engine uncoordinated writes are authorized; or runtime adapter work begins.

## Proposed S13 Final Handoff Format

Future S13 final handoff should report:

- Files changed.
- Behavior changed.
- Tests run.
- Known risks.
- Protected files changed.
- Goal state.
- Recommended next architect decision.

The final handoff must be advisory only and must not approve runtime adapter work.

## Architect Review Required

Architect review is required before any S13 work. S12E does not approve S13.

The architect must approve the objective, write set, protected paths, allowed reads, forbidden reads, forbidden writes, explicit user consent requirements, source selection requirements, PAI_DIR detection rules, preflight requirements, validation commands, hard failures, and final handoff.

## Prohibited Contract Semantics

The proposed S13 contract must not authorize drop-in status, official upstream status, runtime adapter work, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, Pulse implementation, product-memory promotion, direct copying of Claude-shaped files into Codex surfaces, existing-local-v5 access without explicit consent and approval, personal-clone access without explicit consent and approval, dual-engine uncoordinated writes, or uninstalling Claude Code.

## Non-Goals

This proposal does not approve S13, begin S13, run a live read-only trial, read live state, create root `AGENTS.md`, create `.codex/`, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, probe `localhost:31337`, invoke Claude Code, invoke Codex runtime, run installers, run Codex import or migration tooling, implement a runtime adapter, promote product memory, claim Codex is drop-in today, or claim Codex is the official upstream engine.
