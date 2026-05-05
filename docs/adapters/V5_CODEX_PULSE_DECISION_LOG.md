# V5 Codex Pulse Decision Log

## Purpose

Record S7E decisions, non-decisions, blocked decisions, and future architect questions for Pulse bridge identity and read-only event modeling.

## Scope

This decision log is design-only. It does not approve S7B, S8E, S8F, S8G, S8H, S9A, Pulse bridge implementation, Pulse startup, Pulse endpoint calls, existing-local-v5 trial execution, runtime files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, fixtures, harnesses, manifests, audit artifacts, adapter payloads, or Pulse payloads.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CODEX_PULSE_BRIDGE_IDENTITY_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_READ_ONLY_EVENT_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_OBSERVABILITY_AND_AUDIT_SPEC.md`
- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Observability/ObservabilitySystem.md`
- `Releases/v5.0.0/.claude/PAI/PULSE/pulse.ts`

No Pulse endpoint was called and no live Pulse state was read.

## Decisions Made in S7E

S7E decisions preserve these strategic conclusions:

- Codex is not currently proven drop-in for existing local PAI v5 files.
- Codex replacement is plausible only through a designed adapter.
- Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
- `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine.
- `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
- Future Codex `AGENTS.md`, if later authorized, must be a compact router.
- Claude-shaped files must not be copied directly into Codex surfaces.
- Pulse is central v5 infrastructure and S7E does not prove Pulse parity.
- PAI Memory and ISA writes remain blocked.
- Future writes require a single-writer policy, provenance, rollback, and validation.

## Non-Decisions in S7E

S7E does not decide:

- Whether to implement a Pulse bridge.
- Whether any Pulse endpoint may be called in a future trial.
- Whether Codex may submit Pulse events.
- Whether Codex may run Pulse jobs.
- Whether Codex may trigger notifications.
- Whether live Pulse state may be read.
- Whether any Codex config, hook, rule, launcher, wrapper, fixture, harness, manifest, audit artifact, adapter payload, or Pulse payload may be created.
- Whether existing-local-v5 trial execution is approved.

## Blocked Decisions

Blocked decisions:

- Pulse parity claim: blocked until bridge identity, event, audit, failure, rollback, Memory, and ISA proofs exist.
- Live Pulse status observation: blocked until manifest, endpoint classification, identity, permission, audit, and no-write proofs exist.
- Pulse event submission: blocked until a future bridge milestone approves runtime behavior.
- Pulse job or notification behavior: blocked until write and notification policies are approved and tested.
- PAI Memory or ISA integration: blocked until single-writer policy and validation exist.

## Future Architect Questions

Open questions for architect review:

- Should a future Codex/Pulse bridge exist at all, or should Codex remain Pulse-advisory only?
- Which Pulse endpoints, if any, are eligible for future read-only observation?
- How should Codex adapter identity appear in Pulse without impersonating Claude Code or the DA?
- Should future Codex events be proposed as audit output only before live submission is considered?
- What identity policy is required before Codex can be visible in dashboard or observability output?
- What single-writer mechanism is acceptable for Pulse-adjacent Memory and ISA state?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S7E-D01 | Codex remains not drop-in today. | Pulse, Memory, ISA, authority, launcher, inference, and hook proofs remain incomplete. | S6 gates; S7A/S7C/S7D docs; S7E specs. | Decided for S7E. | All drop-in gates pass or receive architect waiver. |
| S7E-D02 | Pulse is central v5 infrastructure and must not be treated as optional trivia. | Release docs identify Pulse as the Life Dashboard and unified local runtime. | `PulseSystem.md`; `pulse.ts`; Observability docs. | Decided for S7E. | Future architecture changes Pulse role. |
| S7E-D03 | S7E does not start Pulse or call Pulse endpoints. | S7E is design-only and endpoint calls would violate scope. | User contract; S7E execution plan; no-call validation posture. | Decided for S7E. | Future architect-approved Pulse observation milestone. |
| S7E-D04 | Future Codex/Pulse interaction requires explicit bridge identity. | Codex activity must not be confused with Claude Code, DA, or canonical PAI state. | Pulse identity spec; S6 `CC-012`; S6 `CC-013`. | Decided for S7E. | Architect approves a future bridge identity design. |
| S7E-D05 | Codex must not impersonate Claude Code in Pulse events. | Claude Code remains the official/full-support upstream engine. | S1-S7 adapter strategy; Pulse Claude job evidence. | Decided for S7E. | Replacement-grade validation and support posture decision. |
| S7E-D06 | Codex must not claim official/full-support Pulse identity. | S7E provides no runtime Pulse proof. | S6 G8; S7E specs. | Decided for S7E. | Future Pulse bridge validation passes. |
| S7E-D07 | Read-only Pulse posture must deny startup, writes, jobs, notifications, and state mutation. | These actions mutate runtime state or produce side effects. | Pulse event spec; Pulse audit spec; release Pulse docs. | Decided for S7E. | Future write-capable milestone with single-writer policy. |
| S7E-D08 | Pulse bridge work must preserve authority, launcher, inference, and hook seam decisions. | Pulse interaction crosses those boundaries. | S7A, S7C, and S7D specs. | Decided for S7E. | Integrated read-only architecture review. |
| S7E-D09 | PAI Memory and ISA writes remain blocked. | They are canonical PAI state and require single-writer policy. | S1-S7D adapter docs; S7E specs. | Decided for S7E. | Single-writer milestone and write validation. |
| S7E-D10 | Product memories, `/goal`, transcripts, and SDK threads are not Pulse state and not PAI Memory. | Product/session state cannot be promoted silently. | S7A authority spec; S7E identity and audit specs. | Decided for S7E. | Architect-approved memory promotion policy. |
| S7E-D11 | Root `AGENTS.md` and `.codex/` remain protected. | S7E creates no Codex runtime guidance or config. | User contract; S7E execution plan. | Decided for S7E. | Future explicit router/config authorization. |
| S7E-D12 | Future Pulse parity claims require bridge identity, event, audit, failure, rollback, Memory, and ISA proofs. | Pulse centrality makes partial parity claims unsafe. | S6 G8-G14; S7E specs. | Decided for S7E. | Future proof package passes review. |
| S7E-D13 | No user-local state is inspected in S7E. | S7E uses repository-local release evidence only. | Source protocol; discovery commands. | Decided for S7E. | Future manifest authorizes live local read-only scope. |
| S7E-D14 | S7E creates no bridge, event payload, audit artifact, config, hook, or runtime material. | The milestone is design-only. | Approved write set; validation checks. | Decided for S7E. | Future implementation milestone approval. |

## Next Milestone Candidates

Advisory-only options:

- `V5-S7B`: Fixture-only coupling validation harness design.
- `V5-S8E`: Codex rules and approval policy design.
- `V5-S8F`: Tool/MCP boundary design.
- `V5-S8G`: Pulse fixture validation design, if S7E is accepted.
- `V5-S8H`: Memory and ISA single-writer policy design.
- `V5-S9A`: Integrated read-only fixture-trial architecture, after S7A/S7C/S7D/S7E acceptance.

Architect approval is required before any future milestone.

## Non-Goals

S7E does not implement a Pulse bridge, start Pulse, call Pulse endpoints, probe `localhost:31337`, create Pulse payloads, create event payloads, create audit artifacts, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create runtime files, run installers, run Codex import or migration tooling, invoke Claude Code, invoke Codex as a runtime engine, inspect private user-local state, authorize PAI Memory writes, authorize ISA writes, authorize Pulse startup, authorize Pulse endpoint calls, authorize Pulse implementation, authorize existing-local-v5 trial execution, begin S7B, begin S8E, begin S8F, begin S8G, begin S8H, or begin S9A.
