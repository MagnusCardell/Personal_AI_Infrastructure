# V5 Codex Memory and ISA Decision Log

## Purpose

Record S8H decisions, non-decisions, blocked decisions, and future architect questions for Memory and ISA single-writer policy.

## Scope

This decision log is design-only. It does not approve S7B, S8E, S8F, S8I, S9A, S9B, Memory writes, ISA writes, product-memory promotion, existing-local-v5 trial execution, runtime files, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, fixtures, harnesses, manifests, audit artifacts, adapter payloads, Memory payloads, ISA payloads, or Pulse payloads.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CODEX_MEMORY_ISA_SINGLE_WRITER_POLICY_SPEC.md`
- `docs/adapters/V5_CODEX_MEMORY_BOUNDARY_AND_PROMOTION_SPEC.md`
- `docs/adapters/V5_CODEX_ISA_WORKFLOW_AND_STATE_POLICY_SPEC.md`
- `docs/adapters/V5_CODEX_MEMORY_ISA_AUDIT_AND_CONFLICT_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_PULSE_DECISION_LOG.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa/IsaSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md`

No private user-local Memory or ISA state was inspected.

## Decisions Made in S8H

S8H decisions preserve these conclusions:

- Codex is not currently proven drop-in for existing local PAI v5 files.
- Codex replacement is plausible only through a designed adapter.
- Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
- `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine.
- `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
- Future Codex `AGENTS.md`, if later authorized, must be a compact router.
- Claude-shaped files must not be copied directly into Codex surfaces.
- PAI Memory and ISA artifacts are canonical PAI state.
- Future writes require a single-writer policy, provenance, rollback, validation, and conflict handling.

## Non-Decisions in S8H

S8H does not decide:

- To implement Memory or ISA writes.
- To read existing-local-v5 Memory or ISA.
- To promote product memory.
- To create Memory payloads or ISA payloads.
- To create an audit artifact.
- To run a read-only trial.
- To create root `AGENTS.md` or `.codex/`.
- To create Codex config, hooks, rules, launchers, wrappers, fixtures, harnesses, manifests, or runtime files.
- To start Pulse or call Pulse endpoints.

## Blocked Decisions

Blocked decisions:

- Controlled Memory write mode: blocked until single-writer ownership, provenance, rollback, validation, audit, and conflict proof exist.
- Controlled ISA write mode: blocked until ISA ownership, changelog preservation, verification preservation, rollback, and conflict proof exist.
- Product-memory promotion: blocked until explicit future user and architect approval.
- Existing-local-v5 Memory/ISA reads: blocked until future manifest and private-state approval.
- Dual-engine write coexistence: blocked until surface ownership and conflict tests exist.
- Pulse-related Memory/ISA events: blocked until a future Pulse bridge milestone.

## Future Architect Questions

Open questions:

- What lock or lease mechanism is acceptable for canonical PAI state?
- Which actor can be `pai-native-writer` in future controlled modes?
- Can `codex-adapter-writer` ever write directly, or only prepare reviewed patches?
- What approval record is required for product memory as evidence?
- Should project-root ISAs and task ISAs have different writer policies?
- How should Memory promotion conflicts be reviewed?
- What rollback proof is sufficient before controlled-single-writer mode?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S8H-D01 | Codex remains not drop-in today. | Memory, ISA, Pulse, authority, launcher, inference, hook, rollback, and audit gates remain incomplete. | S6 gates; S7A/S7C/S7D/S7E docs; S8H specs. | Decided for S8H. | All drop-in gates pass or receive architect waiver. |
| S8H-D02 | PAI Memory is canonical PAI state. | Release Memory docs define persistent structured PAI state. | `MemorySystem.md`; Memory boundary spec. | Decided for S8H. | Future Memory architecture revision. |
| S8H-D03 | ISA is canonical PAI work/system-of-record state. | ISA docs define the Ideal State Artifact as system of record. | `IsaSystem.md`; `IsaFormat.md`. | Decided for S8H. | Future ISA doctrine revision. |
| S8H-D04 | Codex memory is not PAI Memory. | Product memory is separate from canonical PAI state. | S1-S7E adapter docs; S8H specs. | Decided for S8H. | Architect-approved promotion policy. |
| S8H-D05 | Claude Code auto memory is not PAI Memory. | Release docs distinguish PAI Memory and Auto-Memory layers. | `MemorySystem.md`; boundary spec. | Decided for S8H. | Future promotion policy. |
| S8H-D06 | `/goal` state is not ISA and not PAI Memory. | Goal state is workflow-control metadata. | Goal runbook; ISA policy spec. | Decided for S8H. | Future advisory patch workflow. |
| S8H-D07 | Product memories must not be silently promoted into PAI Memory. | Silent promotion risks canonical state corruption. | Memory boundary spec; audit/conflict spec. | Decided for S8H. | User and architect approve a promotion design. |
| S8H-D08 | S8H authorizes no Memory writes and no ISA writes. | Milestone is design-only. | User contract; S8H execution plan. | Decided for S8H. | Future controlled-single-writer milestone. |
| S8H-D09 | Future write-capable modes require single-writer ownership. | Concurrent writers can corrupt canonical state. | S6 G9-G12; single-writer spec. | Decided for S8H. | Lock/ownership proof passes review. |
| S8H-D10 | Dual-engine uncoordinated writes are prohibited. | Claude and Codex cannot write the same canonical surface without ownership. | Single-writer spec; readiness gates. | Decided for S8H. | Dual-engine coexistence design with ownership map. |
| S8H-D11 | Existing-local-v5 Memory/ISA reads remain unauthorized in S8H. | Private live state requires explicit future approval. | Source protocol; fixture/path specs. | Decided for S8H. | Manifest and user approval for live read-only scope. |
| S8H-D12 | Pulse bridge remains out of S8H scope. | S8H is Memory/ISA policy only. | S7E Pulse docs; S8H specs. | Decided for S8H. | Future Pulse bridge milestone. |
| S8H-D13 | Root `AGENTS.md` and `.codex/` remain protected. | S8H creates no Codex runtime surfaces. | User contract; execution plan. | Decided for S8H. | Future explicit router/config authorization. |
| S8H-D14 | Future Codex write capability requires audit, provenance, rollback, and conflict proof. | Canonical writes need accountability and reversibility. | Audit/conflict spec; single-writer spec. | Decided for S8H. | Future proof package passes review. |
| S8H-D15 | PRD terminology must not replace ISA terminology in v5 adapter work. | Release ISA docs state PRD fallback was removed and ISA is current. | `IsaFormat.md`; ISA policy spec. | Decided for S8H. | Future v5 doctrine revision. |
| S8H-D16 | No runtime Memory/ISA policy files are created in S8H. | The milestone is documentation/design only. | Approved write set. | Decided for S8H. | Future implementation approval. |

## Next Milestone Candidates

Advisory-only options:

- `V5-S7B`: Fixture-only coupling validation harness design.
- `V5-S8E`: Codex rules and approval policy design.
- `V5-S8F`: Tool/MCP boundary design.
- `V5-S8I`: Memory/ISA fixture validation design, if S8H is accepted.
- `V5-S9A`: Integrated read-only fixture-trial architecture, after S7A/S7C/S7D/S7E/S8H acceptance.
- `V5-S9B`: Controlled single-writer beta architecture, only after read-only fixture validation passes.

Architect approval is required before any future milestone.

## Non-Goals

S8H does not implement a Codex adapter, write PAI Memory, write ISA, read private user-local Memory or ISA state, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create runtime files, create fixtures, create harnesses, create manifests, create audit artifacts, create Memory payloads, create ISA payloads, start Pulse, call Pulse endpoints, authorize product-memory promotion, authorize dual-engine uncoordinated writes, authorize existing-local-v5 trial execution, begin S7B, begin S8E, begin S8F, begin S8I, begin S9A, or begin S9B.
