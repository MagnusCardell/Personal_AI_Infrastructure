# V5 Codex Integrated Trial Decision Log

## Purpose

Record S9A decisions, non-decisions, blocked decisions, and future architect questions for integrated read-only fixture-trial architecture.

## Scope

This document is design-only. S9A creates no fixtures, harnesses, manifests, audit artifacts, executable schemas, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, migration scripts, runtime files, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, or Pulse bridge files.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement is plausible only through a designed adapter. Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Evidence Base

Evidence comes from S0-S8H adapter docs and repository-local PAI v5 release evidence. S9A adds no new Codex capability claim and uses no unofficial Codex capability source.

## Decisions Made in S9A

S9A decisions:

- Integrated architecture is a documentation synthesis layer only.
- Future fixture-trial work must begin with release or sanitized fixture architecture, not live existing-local-v5 state.
- Existing-local-v5 read-only trial remains future-only and separately approved.
- Unsupported surfaces must be reported.
- Future audit output remains advisory and non-canonical.

## Non-Decisions in S9A

S9A does not decide:

- To create fixtures.
- To create a harness.
- To create manifest instances.
- To create audit artifacts.
- To create executable schemas.
- To run a read-only trial.
- To create root `AGENTS.md` or `.codex/`.
- To implement launcher, inference, hook, Pulse, Memory, ISA, or rollback behavior.
- To authorize existing-local-v5 trial execution.
- To authorize controlled write mode.

## Blocked Decisions

Blocked decisions:

- Whether any future fixture corpus may be created.
- Whether any future harness may be created.
- Whether any future manifest or audit artifact may be generated.
- Whether any future executable schema may exist.
- Whether Codex can read live existing-local-v5 state.
- Whether Codex can become drop-in-capable.
- Whether controlled single-writer mode can exist.
- Whether Pulse bridge implementation can begin.

## Future Architect Questions

Questions for architect review:

- Should the next milestone be implementation planning, fixture corpus design, or harness design?
- What future write set would be acceptable for fixture-only work?
- What is the minimum fixture corpus for authority, launcher/inference, hook lifecycle, Pulse, Memory, ISA, rollback, and unsupported-surface coverage?
- Should existing-local-v5 read-only work remain blocked until after fixture validation passes?
- What future audit artifact location, if any, should be approved?
- What proof is required before any controlled single-writer beta architecture?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S9A-D01 | Codex remains not drop-in today. | No integrated fixture validation, live trial, Pulse proof, Memory/ISA proof, or rollback proof exists. | S6 readiness gates, S7A/S7C/S7D/S7E/S8H docs. | Decided for S9A. | All required gates pass or are architect-waived. |
| S9A-D02 | Integrated read-only fixture trial architecture is the next synthesis layer after S7A/S7C/S7D/S7E/S8H. | Individual seam designs now need cross-seam sequencing and coverage. | S7A authority, S7C launcher/inference, S7D hook lifecycle, S7E Pulse, S8H Memory/ISA. | Decided for S9A. | Architect selects next implementation-plan milestone. |
| S9A-D03 | S9A creates no fixtures and runs no trial. | This milestone is design-only. | S9A contract and protected-path discipline. | Decided for S9A. | Architect approves fixture creation under a new bounded write set. |
| S9A-D04 | Future fixture trial must start with release or sanitized fixture, not live existing-local-v5 state. | Live state raises privacy, no-write, rollback, and Pulse hazards. | S6 G11, S8H existing-local-v5 boundary. | Decided for S9A. | Fixture validation succeeds and architect approves live-read scope. |
| S9A-D05 | Existing-local-v5 read-only trial remains future-only and separately approved. | S9A does not read live `~/.claude/PAI` or `~/.codex`. | Source protocol and S8H state boundaries. | Decided for S9A. | Architect issues a separate live-read trial plan. |
| S9A-D06 | Authority, launcher/inference, hooks/lifecycle, Pulse, and Memory/ISA seams must all be covered before drop-in claims. | Any missing seam can corrupt authority, runtime behavior, lifecycle safety, central infrastructure, or canonical state. | S6 drop-in gates and S7/S8H seam docs. | Decided for S9A. | Coverage matrix and future validation show every required seam resolved. |
| S9A-D07 | Root `AGENTS.md` and `.codex/` remain protected. | Router/config creation is outside S9A. | S7A compact router and S9A protected paths. | Decided for S9A. | Maintainer and architect explicitly authorize future router/config work. |
| S9A-D08 | Pulse startup and endpoint calls remain prohibited. | Pulse is central and side-effectful; S9A proves no Pulse parity. | S7E Pulse read-only event model. | Decided for S9A. | Future Pulse milestone authorizes bridge testing. |
| S9A-D09 | PAI Memory and ISA writes remain prohibited. | They are canonical PAI state and require single-writer proof. | S8H Memory/ISA policy. | Decided for S9A. | Controlled single-writer proof passes in a later milestone. |
| S9A-D10 | Product-memory promotion remains prohibited. | Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory. | S7A and S8H memory boundaries. | Decided for S9A. | Future opt-in promotion design is approved and validated. |
| S9A-D11 | Future audit output is advisory and non-canonical. | Audit output must not become PAI Memory, ISA, Pulse state, Claude memory, or Codex memory. | S5, S7E, and S8H audit specs. | Decided for S9A. | Architect approves an audit artifact format and storage path. |
| S9A-D12 | Future rollback/no-residue proof is required. | Read-only fixture trials must leave no protected-path or live-state residue. | S6 G14 and S9A failure model. | Decided for S9A. | Future trial implementation provides residue report. |
| S9A-D13 | Unsupported surfaces must be reported, not silently ignored. | Silent gaps create false drop-in confidence. | S6 readiness gates and all seam specs. | Decided for S9A. | Future validation shows complete unsupported-surface coverage. |
| S9A-D14 | Future fixture-trial implementation requires new architect approval and a bounded write set. | S9A does not authorize implementation, fixtures, harnesses, manifests, audit artifacts, or schemas. | S9A scope and hard failure conditions. | Decided for S9A. | Architect issues a new implementation-plan prompt. |
| S9A-D15 | Controlled write mode remains blocked until read-only fixture validation passes. | Write-capable modes require authority, launcher/inference, hook, Pulse, Memory/ISA, audit, rollback, and conflict proof. | S8H single-writer policy and S6 G12. | Decided for S9A. | Read-only fixture validation passes and architect approves write architecture. |
| S9A-D16 | S9A creates no runtime files, configs, schemas, manifests, audit artifacts, or harnesses. | The milestone is design-only. | S9A approved write set. | Decided for S9A. | New milestone explicitly authorizes those artifacts. |

## Next Milestone Candidates

Advisory-only options, not approvals:

- `V5-S9B`: Fixture-trial implementation plan only, if S9A is accepted.
- `V5-S9C`: Fixture corpus design only, if S9A is accepted.
- `V5-S9D`: Read-only harness design only, if S9A is accepted.
- `V5-S10A`: First fixture-only implementation, only after explicit architect approval.
- `V5-S10B`: Existing-local-v5 read-only trial plan, only after fixture validation succeeds.
- `V5-S10C`: Controlled single-writer beta architecture, only after read-only validation succeeds.

Architect approval is required before any future milestone.

## Non-Goals

S9A does not implement the adapter, create fixtures, create a test harness, create manifests, create audit artifacts, create executable schemas, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create generated configs, create migration scripts, create runtime files, create adapter payloads, create Memory payloads, create ISA payloads, create Pulse payloads, create trial outputs, run a read-only trial, inspect private user-local state, read live existing-local-v5 state, modify release files, start Pulse, call Pulse endpoints, probe `localhost:31337`, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, run Codex hook/rule/execpolicy commands, authorize PAI Memory writes, authorize ISA writes, authorize Pulse startup, authorize Pulse endpoint calls, authorize Pulse implementation, authorize existing-local-v5 trial execution, imply Claude-shaped files can be copied directly into Codex surfaces, authorize product-memory promotion into PAI Memory, authorize dual-engine uncoordinated writes, or advance beyond S9A.
