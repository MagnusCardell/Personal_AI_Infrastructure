# V5 Codex S11 Proposed Write Set and Completion Contract

## Purpose

Propose a future S11 read-only trial readiness contract for architect review. S11 is proposed only. S11 is not approved by S10G.

Codex is not currently proven drop-in for existing local PAI v5 files. Proposed S11 must not claim drop-in status.

## Scope

This document proposes a future read-only S11 milestone. It does not authorize S11, does not run live trials, does not read existing-local-v5 state, and does not implement a runtime adapter.

Proposed S11 must be read-only, must not read live user-local state by default, must not write PAI Memory or ISA, must not start or call Pulse unless separately approved, must not create root `AGENTS.md` or `.codex/`, and must not authorize product-memory promotion.

## Evidence Base

Evidence base:

- S10A fixture-only metadata corpus and read-only harness.
- S10B negative-control regression self-tests.
- S10C semantic fixture hardening.
- S10D fixture case data and expected-behavior validation.
- S10E global coverage closure.
- S10F no-residue determinism guard.
- S10G closeout and readiness gate proposal.

## Contract Proposal Status

S11 is proposed only and not approved by S10G. Architect approval is required before any S11 work begins.

This proposal is intentionally conservative: it is read-only by default, denies live user-local state by default, and preserves no live trials unless a future card explicitly approves exact sources and operations.

## Proposed S11 Objective

Proposed objective:

```text
Evaluate whether the S10 fixture-only validation track is sufficient to authorize a future read-only trial readiness report, without implementing a runtime adapter, without writing PAI Memory or ISA, without starting or calling Pulse, without creating root AGENTS.md or .codex/, and without claiming Codex drop-in status.
```

The proposed objective is advisory only and requires architect approval.

## Proposed S11 Approved Write Set

Proposed write-set table:

| Proposed path | Purpose | Status |
| --- | --- | --- |
| `docs/adapters/V5_S11_EXEC_PLAN.md` | Future S11 execution plan with approved contract. | Proposed only |
| `docs/adapters/V5_CODEX_S11_READ_ONLY_TRIAL_PLAN.md` | Read-only trial readiness plan. | Proposed only |
| `docs/adapters/V5_CODEX_S11_SOURCE_SELECTION_REPORT.md` | Explicit source selection and denied-source report. | Proposed only |
| `docs/adapters/V5_CODEX_S11_BOUNDARY_VALIDATION_REPORT.md` | Authority, launcher/inference, hook/lifecycle, Pulse, Memory/ISA, rollback, and audit boundary report. | Proposed only |
| `docs/adapters/V5_CODEX_S11_DECISION_LOG.md` | S11 decision log and architect questions. | Proposed only |

No runtime files, manifests, audit artifacts, executable schemas, live-trial artifacts, Codex config, hooks, rules, skills, agents, commands, launchers, Memory payloads, ISA payloads, or Pulse payloads are proposed.

## Proposed S11 Protected Paths

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

Future S11 must not create root `AGENTS.md` or `.codex/`.

## Proposed S11 Allowed Reads

Allowed reads should be restricted to:

- `docs/adapters/V5_*.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/`
- Repository-local PAI v5 release files only if the future card explicitly names them.
- Future architect-approved read-only sample sources, if any.

Allowed reads must remain repository-relative or explicitly approved. There must be no live user-local reads by default.

## Proposed S11 Forbidden Reads

Forbidden reads by default:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`
- Any live existing-local-v5 state.
- Any private user-local state.

No live user-local state may be read by default. Existing-local-v5 access remains future-only and explicit.

## Proposed S11 Forbidden Writes

Forbidden writes:

- PAI Memory writes.
- ISA writes.
- Pulse payloads.
- Memory payloads.
- Runtime adapter files.
- Codex config, hooks, rules, skills, agents, commands, launchers, wrappers, installers, generated configs, or migration scripts.
- Root `AGENTS.md`.
- `.codex/`.
- Manifests, audit artifacts, executable schemas, and live-trial artifacts unless separately approved by a future card.
- Product-memory promotion into PAI Memory.

## Proposed S11 Validation Commands

Proposed validation commands:

```bash
git status --short
git diff --name-only | sort
git diff --check
python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures
PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py
git status --short -- Releases/ .claude/ PAI/ CLAUDE.md AGENTS.md .codex/ install.sh settings.json hooks/ skills/ subagents/ agents/ commands/ .github/ .agents/
```

Future S11 may add document heading, content invariant, and changed-file checks matching its approved write set.

## Proposed S11 Acceptance Criteria

- S11-AC-001: S11 is explicitly approved by an architect before work begins.
- S11-AC-002: S11 is proposed only by S10G and not approved by S10G.
- S11-AC-003: S11 remains read-only unless separately approved.
- S11-AC-004: S11 approved write set is exact and document-only unless separately approved.
- S11-AC-005: No file outside the approved S11 write set changes.
- S11-AC-006: No live user-local state is read by default.
- S11-AC-007: Existing-local-v5 access remains future-only and explicit.
- S11-AC-008: Root `AGENTS.md` is not created or modified.
- S11-AC-009: `.codex/` is not created or modified.
- S11-AC-010: PAI Memory is not written.
- S11-AC-011: ISA is not written.
- S11-AC-012: Pulse is not started.
- S11-AC-013: Pulse endpoints are not called and `localhost:31337` is not probed.
- S11-AC-014: Product memories are not promoted into PAI Memory.
- S11-AC-015: Claude-shaped files are not copied directly into Codex surfaces.
- S11-AC-016: Fixture-only evidence is referenced as necessary but insufficient for drop-in claims.
- S11-AC-017: Unsupported surfaces are reported, not silently treated as supported.
- S11-AC-018: Audit and rollback posture remains report-only unless separately approved.
- S11-AC-019: Final handoff includes no drop-in claim.
- S11-AC-020: Final handoff states Codex is not currently proven drop-in for existing local PAI v5 files.

## Proposed S11 Hard Failure Conditions

Proposed S11 fails if:

- S11 begins without architect approval.
- Any file outside the approved write set changes.
- Root `AGENTS.md` or `.codex/` is created or modified.
- Runtime adapter files are created.
- Live user-local state is read without explicit future approval.
- Existing-local-v5 state is read by default.
- Pulse is started or called.
- PAI Memory or ISA is written.
- Product-memory promotion occurs.
- Claude Code or Codex runtime is invoked.
- Any deliverable claims Codex is drop-in today or the official upstream engine.
- Any deliverable authorizes live trials, runtime adapter work, Memory writes, ISA writes, Pulse implementation, product-memory promotion, or dual-engine uncoordinated writes outside the approved card.

## Proposed S11 Final Handoff Format

Proposed final handoff sections:

- Files changed.
- Behavior changed.
- Tests run.
- Known risks.
- Protected files changed.
- Goal state.
- Recommended next architect decision.

The final handoff must state S11 is read-only, no live user-local state was read by default, no PAI Memory or ISA writes occurred, Pulse was not started or called, root `AGENTS.md` and `.codex/` were not created or modified, and no drop-in claim is made.

## Architect Review Required

Architect approval is required before any S11 work. S10G does not approve S11 and does not authorize live trials, existing-local-v5 access, runtime adapter implementation, root `AGENTS.md`, `.codex/`, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, or product-memory promotion.

## Prohibited Contract Semantics

Future S11 must not imply that Codex is drop-in today, must not imply Codex is the official upstream engine, must not authorize runtime adapter implementation, must not authorize live user-local reads by default, must not authorize PAI Memory or ISA writes, must not authorize Pulse implementation, and must not authorize dual-engine uncoordinated writes.

S11 must preserve no live user-local default behavior and no drop-in claim.

## Non-Goals

This proposal does not begin S11, approve S11, run live trials, inspect existing-local-v5 state, implement runtime adapter behavior, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, create root `AGENTS.md`, create `.codex/`, create manifests, create audit artifacts, create executable schemas, create runtime payloads, invoke Claude Code, or invoke Codex runtime.
