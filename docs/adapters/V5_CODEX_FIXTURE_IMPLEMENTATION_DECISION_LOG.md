# V5 Codex Fixture Implementation Decision Log

## Purpose

Record S9B decisions, non-decisions, blocked decisions, and future architect questions for first fixture implementation planning.

## Scope

This document is design-only. S9B creates no fixtures, harnesses, manifests, audit artifacts, executable schemas, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, runtime files, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, fixture files, harness files, or Pulse bridge files.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement is plausible only through a designed adapter. Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Evidence Base

Evidence comes from S0-S9A adapter docs and repository-local PAI v5 release evidence. S9B adds no new Codex capability claim and uses no unofficial Codex capability source.

## Decisions Made in S9B

S9B decisions:

- S10A is proposed only.
- First implementation should be fixture-only, not live existing-local-v5.
- Future harness design must be read-only.
- Future S10A must avoid runtime and protected surfaces.
- Architect approval is required before any future implementation.

## Non-Decisions in S9B

S9B does not decide:

- To approve S10A.
- To create fixtures.
- To create a harness.
- To create manifests.
- To create audit artifacts.
- To create executable schemas.
- To run a read-only trial.
- To create root `AGENTS.md` or `.codex/`.
- To implement any runtime adapter.
- To authorize existing-local-v5 trial execution.

## Blocked Decisions

Blocked decisions:

- Whether the proposed S10A write set is accepted.
- Whether fixture files may be created.
- Whether harness files may be created.
- Whether expected report examples may be created.
- Whether any manifest, audit artifact, or executable schema may be generated.
- Whether Codex may be invoked as runtime in fixture trials.
- Whether live existing-local-v5 state can be read.
- Whether controlled single-writer beta work can begin.

## Future Architect Questions

Questions for architect review:

- Is the proposed S10A write set acceptable?
- Should expected report examples be included in S10A or deferred?
- Should fixture corpus and harness work happen in one milestone or split milestones?
- Should S10A permit Codex runtime invocation, or remain static/read-only only?
- What future proof is required before existing-local-v5 read-only planning?
- What future proof is required before controlled single-writer beta architecture?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S9B-D01 | Codex remains not drop-in today. | No fixture validation, live trial, Pulse proof, Memory/ISA proof, or rollback proof exists. | S6 readiness gates and S9A architecture. | Decided for S9B. | All required gates pass or are architect-waived. |
| S9B-D02 | S9B proposes but does not approve S10A. | S9B is design-only and cannot authorize implementation. | S9B scope and proposed S10A contract. | Decided for S9B. | Architect approves a future S10A card. |
| S9B-D03 | First implementation should be fixture-only, not existing-local-v5. | Fixture-only work avoids private-state and live-state risks. | S9A source model and S8H state boundaries. | Decided for S9B. | Fixture validation succeeds and architect approves live-read planning. |
| S9B-D04 | Future fixture harness must be read-only. | The goal is no-write validation, not runtime behavior. | S9A gate model and S9B harness design. | Decided for S9B. | Architect approves a different future mode. |
| S9B-D05 | Future S10A must avoid root `AGENTS.md` and `.codex/`. | Router/config surfaces remain protected. | S7A compact router and S9A architecture. | Decided for S9B. | Maintainer and architect authorize router/config work. |
| S9B-D06 | Future S10A must avoid `Releases/` mutation. | Release files are source evidence and protected. | S9A fixture isolation boundary. | Decided for S9B. | Architect explicitly approves a separate release-change milestone. |
| S9B-D07 | Future S10A must not start Pulse or call Pulse endpoints. | Pulse is central and side-effectful; S10A should be static no-start/no-call validation. | S7E Pulse model and S9A gates. | Decided for S9B. | Future Pulse bridge milestone is approved. |
| S9B-D08 | Future S10A must not write PAI Memory or ISA. | PAI Memory and ISA are canonical PAI state. | S8H single-writer policy. | Decided for S9B. | Controlled single-writer proof exists. |
| S9B-D09 | Future S10A must not read private user-local state. | S10A is fixture-only and no live user-local state is allowed. | S9A existing-local-v5 boundary. | Decided for S9B. | Architect approves sanitized or live-state scope. |
| S9B-D10 | Future S10A must not invoke Claude Code. | Claude Code invocation would be runtime behavior and outside fixture-only static validation. | S9A no-runtime constraints. | Decided for S9B. | Architect approves explicit runtime comparison work. |
| S9B-D11 | Future S10A must not claim drop-in readiness. | Fixture-only implementation cannot prove replacement-grade validation. | S6 readiness gates. | Decided for S9B. | All drop-in gates pass or are architect-waived. |
| S9B-D12 | Future S10A must report unsupported surfaces. | Silent gaps create false confidence. | S9A coverage matrix and failure model. | Decided for S9B. | Future validation proves all unsupported surfaces resolved. |
| S9B-D13 | Future S10A must include rollback/no-residue proof. | Fixture work must not leave protected or live residue. | S9A rollback/no-residue model. | Decided for S9B. | Future S10A completes residue reporting. |
| S9B-D14 | Fixture corpus design must cover authority, launcher/inference, hooks/lifecycle, Pulse, Memory/ISA, denied paths, unsupported surfaces, and rollback. | Drop-in confidence requires cross-seam coverage. | S9A integrated architecture and coverage matrix. | Decided for S9B. | Architect narrows or expands S10A fixture scope. |
| S9B-D15 | Harness design must not become runtime adapter implementation. | Harness checks fixtures; it must not launch engines or mutate state. | S9B harness design. | Decided for S9B. | Architect approves runtime adapter planning after fixture validation. |
| S9B-D16 | Architect approval is required before any future implementation. | S9B proposes only and cannot authorize S10A. | S9B contract. | Decided for S9B. | Future architect-approved S10A prompt exists. |

## Next Milestone Candidates

Advisory-only options, not approvals:

- `V5-S10A`: First fixture-only implementation, only after explicit architect approval.
- `V5-S10B`: Existing-local-v5 read-only trial plan, only after fixture validation succeeds.
- `V5-S10C`: Controlled single-writer beta architecture, only after read-only validation succeeds.
- `V5-S10D`: Runtime adapter implementation plan, only after fixture validation succeeds and architect approves runtime surfaces.

Architect approval is required before any future milestone.

## Non-Goals

S9B does not implement the adapter, approve S10A, create fixtures, create a test harness, create manifests, create audit artifacts, create executable schemas, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create generated configs, create migration scripts, create runtime files, create adapter payloads, create Memory payloads, create ISA payloads, create Pulse payloads, create trial outputs, create fixture files, create harness files, run a read-only trial, inspect private user-local state, read live existing-local-v5 state, modify release files, start Pulse, call Pulse endpoints, probe `localhost:31337`, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, run Codex hook/rule/execpolicy commands, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse startup, authorize Pulse endpoint calls, authorize Pulse implementation, authorize existing-local-v5 trial execution, imply Claude-shaped files can be copied directly into Codex surfaces, authorize product-memory promotion into PAI Memory, authorize dual-engine uncoordinated writes, or advance beyond S9B.
