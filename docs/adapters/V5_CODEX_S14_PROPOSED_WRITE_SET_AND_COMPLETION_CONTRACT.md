# V5 Codex S14 Proposed Write Set and Completion Contract

## Purpose

Propose a future S14 write set and completion contract for architect review without approving S14.

## Scope

S14 is proposed only. S14 is not approved by S13C and must not begin from this document.

Proposed S14 must be read-only unless separately approved. Proposed S14 must not write PAI Memory or ISA, must not start or call Pulse unless separately approved, must not create root AGENTS.md or `.codex`, must not claim drop-in status, must not claim Codex is the official upstream engine, and must not require uninstalling Claude Code.

## Evidence Base

Evidence base:

- S13A clean-clone positive-control trial artifacts.
- S13B clean-clone negative-control and path-safety hardening evidence.
- S13C closeout and S14 gate proposal.
- S12/S13 source-selection, PAI_DIR, preflight, abort, non-canonical evidence, and no-residue policies.

Codex is not currently proven drop-in for existing local PAI v5 files.

## Contract Proposal Status

S14 is proposed only. S14 is not approved by S13C.

Architect approval is required before any future S14 work. This document is not a live-read authorization, not personal-clone authorization, not existing-local-v5 authorization, and not runtime adapter authorization.

## Proposed S14 Objective

Proposed objective:

Run a future architect-approved, explicitly source-class-selected, explicitly consented, read-only source-selected trial after a future preflight pass, producing only approved non-canonical evidence and denied-action reporting, with no writes to live state, PAI Memory, ISA, Pulse, root AGENTS.md, `.codex`, product memory, or runtime adapter surfaces.

## Proposed S14 Source Class Options

Possible future source classes:

- `existing-local-v5-read-only`
- `personal-clone-read-only`
- `sanitized-user-fixture-read-only`

None of these source classes is approved by S13C. A future architect card must explicitly select one source class before S14 can begin.

## Proposed S14 Approved Write Set

Proposed write-set table:

| Proposed path | Proposed artifact type | Purpose | Runtime payload? | Canonical PAI state? | Requires architect approval? |
| --- | --- | --- | --- | --- | --- |
| `docs/adapters/V5_S14A_EXEC_PLAN.md` | Execution plan | Record approved S14A contract and results. | No | No | Yes |
| `docs/adapters/V5_CODEX_S14_SOURCE_SELECTION_AND_CONSENT_RECORD.md` | Non-canonical consent/source record | Record explicit source class, source root, and user consent. | No | No | Yes |
| `docs/adapters/V5_CODEX_S14_PREFLIGHT_RESULT_SUMMARY.md` | Non-canonical preflight summary | Record future preflight pass or abort summary. | No | No | Yes |
| `docs/adapters/V5_CODEX_S14_LIVE_READ_ONLY_TRIAL_REPORT.md` | Non-canonical evidence report | Summarize approved source-selected read-only evidence. | No | No | Yes |
| `docs/adapters/V5_CODEX_S14_DENIED_ACTIONS_AND_UNSUPPORTED_SURFACES.md` | Denied-action report | Record denied actions and unsupported surfaces. | No | No | Yes |
| `docs/adapters/V5_CODEX_S14_ROLLBACK_AND_NO_RESIDUE_REPORT.md` | No-residue report | Record rollback and no-residue evidence. | No | No | Yes |
| `docs/adapters/V5_CODEX_S14_DECISION_LOG.md` | Decision log | Record S14 decisions, non-decisions, and future questions. | No | No | Yes |

No proposed S14 output is PAI Memory, ISA, Pulse state, Claude memory, Codex memory, a manifest, an executable schema, a runtime payload, or proof that Codex is drop-in.

## Proposed S14 Protected Paths

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

Future S14 must not modify protected paths.

## Proposed S14 Allowed Reads

Allowed reads, if future architect approval exists:

- Repository-local S0-S13C adapter docs and evidence.
- Existing repository-local S10/S11 fixture and report files as read-only reference evidence.
- Existing S13A/S13B clean-clone trial files as read-only reference evidence.
- Exactly one explicitly selected source class and source root, only after explicit user consent and preflight pass.
- Read-only PAI_DIR candidate evidence only if explicitly approved, source-bound, and consent-bound.

No live source is allowed by default.

## Proposed S14 Forbidden Reads

Forbidden reads by default:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`
- Product memory.
- Broad home-directory scans.
- Shell history, inferred local config, subscription state, or prior interaction.
- Personal-clone access unless the `personal-clone-read-only` source class is explicitly selected and consented.
- Existing-local-v5 access unless the `existing-local-v5-read-only` source class is explicitly selected and consented.
- Any source outside the approved source root.

Future S14 must not read product memories by default.

## Proposed S14 Forbidden Writes

Forbidden writes:

- PAI Memory writes.
- ISA writes.
- Pulse state writes.
- Product-memory promotion.
- Root AGENTS.md.
- `.codex/`.
- Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, manifest instances, executable schemas, live-trial artifacts outside the approved write set, runtime payloads, reports outside the approved write set, fixtures, and committed negative fixtures.
- Any live-source write.

## Proposed S14 Consent Requirements

Proposed S14 must require explicit user consent. Consent must identify source class, source root, allowed reads, forbidden reads, forbidden writes, retention, revocation, expiration, rollback/no-residue expectations, reporting output, no official-upstream claim, and no drop-in claim.

Consent must not be inferred from Claude Code installation, Codex installation, dual subscriptions, shell history, product memory, local config, or prior interaction.

## Proposed S14 Source Selection Requirements

Proposed S14 must require explicit source selection. Source selection must bind exactly one source class and one source root to consent.

Source selection must not use default live reads, broad home scans, product memory, shell history, or inferred local config.

## Proposed S14 PAI_DIR Detection Requirements

Proposed S14 PAI_DIR detection, if approved, must remain read-only, dry-run, source-specific, path-bounded, consent-bound, confidence-qualified, abortable, and non-canonical.

PAI_DIR detection must not read live `~/.claude/PAI` by default and must not treat a clean clone as a live PAI install.

## Proposed S14 Preflight Requirements

Proposed S14 must require a future preflight pass before any source-selected read. Preflight must validate architect approval, source class, consent, source root, PAI_DIR candidate if applicable, allowed reads, forbidden reads, forbidden writes, product memory denial, Pulse denial, Memory/ISA write denial, runtime invocation denial, reporting boundaries, retention, rollback/no-residue, no official-upstream claim, and no drop-in claim.

Any failed preflight check must abort.

## Proposed S14 Reporting Requirements

Proposed S14 reporting must be non-canonical, retention-bounded, rollback/no-residue-bounded, and clear about denied actions and unsupported surfaces.

Report output must state it is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.

## Proposed S14 Validation Commands

Future S14 validation commands should include, if architect-approved:

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Changed-file allowlist check for the future S14 approved write set.
- Protected-path check.
- No root AGENTS.md check.
- No `.codex` check.
- Source class validation.
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

These are proposed only and do not approve S14.

## Proposed S14 Acceptance Criteria

S14-AC-001 approved write set only

S14-AC-002 no protected paths changed

S14-AC-003 no root AGENTS.md

S14-AC-004 no .codex

S14-AC-005 explicit architect approval

S14-AC-006 explicit source class selected

S14-AC-007 explicit user consent present

S14-AC-008 explicit source root selected

S14-AC-009 PAI_DIR detection remains read-only

S14-AC-010 preflight pass required

S14-AC-011 no Pulse startup

S14-AC-012 no Pulse endpoint calls

S14-AC-013 no PAI Memory writes

S14-AC-014 no ISA writes

S14-AC-015 no product-memory reads by default

S14-AC-016 no product-memory promotion

S14-AC-017 no Claude file direct-copy

S14-AC-018 no Claude Code invocation

S14-AC-019 no Codex runtime adapter execution

S14-AC-020 no Codex import or migration tooling

S14-AC-021 no installer execution

S14-AC-022 unsupported-surface reporting

S14-AC-023 denied-action reporting

S14-AC-024 non-canonical evidence output

S14-AC-025 rollback/no-residue reporting

S14-AC-026 no drop-in claim

S14-AC-027 no official-upstream claim

S14-AC-028 no dual-engine uncoordinated writes

S14-AC-029 no consent artifact promotion into PAI Memory

S14-AC-030 no report promotion into ISA or Pulse

S14-AC-031 no personal-clone access unless selected and consented

S14-AC-032 no existing-local-v5 access unless selected and consented

S14-AC-033 final architect review required

S14-AC-034 no advance to runtime adapter work

## Proposed S14 Hard Failure Conditions

Future S14 should fail immediately if any file outside the approved write set is created or modified; any protected file is modified; root AGENTS.md or `.codex` is created or modified; PAI Memory or ISA is written; Pulse is started or called; product memory is read by default or promoted; Claude Code is invoked; Codex runtime adapter execution occurs; installers, import/migration tooling, hook/rule/execpolicy commands, runtime payloads, or adapter payloads are created or run; existing-local-v5 access occurs without explicit source selection and consent; personal-clone access occurs without explicit source selection and consent; unsupported surfaces are silently ignored; reports become canonical state; drop-in or official-upstream claims are made; or runtime adapter work begins.

## Proposed S14 Final Handoff Format

Future S14 final handoff should report:

- Files changed.
- Behavior changed.
- Tests run.
- Known risks.
- Protected files changed.
- Goal state.
- Recommended next architect decision.

The handoff must remain advisory and must not begin runtime adapter work.

## Architect Review Required

Architect approval is required before any S14 work. S13C does not approve S14, personal-clone access, existing-local-v5 access, sanitized-user-fixture access, live-read execution, PAI Memory writes, ISA writes, Pulse behavior, root AGENTS.md, `.codex`, or runtime adapter work.

## Prohibited Contract Semantics

This proposal must not be read as approval to run S14, read existing-local-v5 state, read personal-clone state, read product memory, inspect arbitrary home directories, inspect live `~/.claude/PAI`, inspect live `~/.claude/projects`, inspect live `~/.codex`, start Pulse, call Pulse endpoints, probe `localhost:31337`, invoke Claude Code, invoke Codex runtime, create runtime payloads, create root AGENTS.md, create `.codex`, promote product memory, write PAI Memory, write ISA, claim Codex is drop-in, claim Codex is official upstream, or begin runtime adapter work.

## Non-Goals

This proposed contract does not approve S14, begin S14, select a source class, collect consent, select a source root, read existing-local-v5 state, read a personal clone, create consent artifacts, create preflight reports, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, invoke Claude Code, invoke Codex runtime, create root AGENTS.md, create `.codex`, implement a runtime adapter, claim Codex is drop-in today, or claim Codex is the official upstream engine.
