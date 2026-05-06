# V5 Codex S10 to S11 Decision Log

## Purpose

Record the S10G decisions that close the S10 fixture-only validation track and frame S11 as a future, architect-approved read-only milestone proposal.

Codex is not currently proven drop-in for existing local PAI v5 files.

## Scope

This decision log is documentation/design only. It does not authorize S11, live trials, existing-local-v5 access, runtime adapter implementation, root `AGENTS.md`, `.codex`, Pulse startup, Pulse endpoint calls, PAI Memory writes, ISA writes, or product-memory promotion.

## Evidence Base

Evidence comes from S10A through S10F execution plans, the fixture-only corpus, the read-only harness, negative-control self-tests through `NC-060`, global coverage validation, and no-residue determinism validation.

The S10 fixture-only track is ready for architect review, but fixture validation remains necessary and insufficient for drop-in claims.

## Decisions Made in S10G

S10G-D01 Codex remains not drop-in today.

S10G-D02 S10 fixture-only track is closed pending architect review.

S10G-D03 S11 is proposed only and not approved.

S10G-D04 Future S11 must be read-only unless separately approved.

S10G-D05 Existing-local-v5 access remains future-only and explicit.

S10G-D06 Root AGENTS.md remains protected.

S10G-D07 .codex remains protected.

S10G-D08 Pulse startup remains prohibited by default.

S10G-D09 Pulse endpoint calls remain prohibited by default.

S10G-D10 PAI Memory writes remain prohibited.

S10G-D11 ISA writes remain prohibited.

S10G-D12 Product-memory promotion remains prohibited.

S10G-D13 Future S11 must preserve authority, launcher/inference, hook/lifecycle, Pulse, Memory/ISA, rollback, and audit boundaries.

S10G-D14 Future runtime adapter planning remains blocked until S11 readiness is accepted.

S10G-D15 S10G creates no runtime, fixture, harness, schema, manifest, or audit artifact.

S10G-D16 Architect approval is required before any S11 work.

## Non-Decisions in S10G

S10G does not decide to begin S11. S10G does not decide source access for a live trial. S10G does not decide that existing-local-v5 state may be read. S10G does not decide that Codex can become the runtime engine.

S10G does not approve PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, root `AGENTS.md`, `.codex/`, product-memory promotion, manifests, audit artifacts, executable schemas, runtime payloads, or dual-engine uncoordinated writes.

## Blocked Decisions

Blocked until future architect approval:

- Whether to approve S11 as a read-only trial readiness milestone.
- Whether any source beyond repository-local fixture and documentation material may be read.
- Whether any live existing-local-v5 access will ever be permitted.
- Whether Pulse can be started or called in a later controlled milestone.
- Whether runtime adapter planning can begin after S11 readiness review.

## Future Architect Questions

- Should S11 be approved as a read-only readiness milestone?
- Which sources, if any, may S11 inspect beyond S10 fixture-only material?
- Should S11 explicitly prohibit all live user-local state, or allow a later separate card to select a controlled sample?
- What evidence is required before runtime adapter planning may begin?
- What rollback, audit, and provenance model is required before any future write mode?

## Decision Table

| ID | Decision | Status |
| --- | --- | --- |
| S10G-D01 | Codex remains not drop-in today. | Decided |
| S10G-D02 | S10 fixture-only track is closed pending architect review. | Decided |
| S10G-D03 | S11 is proposed only and not approved. | Decided |
| S10G-D04 | Future S11 must be read-only unless separately approved. | Decided |
| S10G-D05 | Existing-local-v5 access remains future-only and explicit. | Decided |
| S10G-D06 | Root AGENTS.md remains protected. | Decided |
| S10G-D07 | .codex remains protected. | Decided |
| S10G-D08 | Pulse startup remains prohibited by default. | Decided |
| S10G-D09 | Pulse endpoint calls remain prohibited by default. | Decided |
| S10G-D10 | PAI Memory writes remain prohibited. | Decided |
| S10G-D11 | ISA writes remain prohibited. | Decided |
| S10G-D12 | Product-memory promotion remains prohibited. | Decided |
| S10G-D13 | Future S11 must preserve authority, launcher/inference, hook/lifecycle, Pulse, Memory/ISA, rollback, and audit boundaries. | Decided |
| S10G-D14 | Future runtime adapter planning remains blocked until S11 readiness is accepted. | Decided |
| S10G-D15 | S10G creates no runtime, fixture, harness, schema, manifest, or audit artifact. | Decided |
| S10G-D16 | Architect approval is required before any S11 work. | Decided |

## Next Milestone Candidates

The next real architect decision should be whether to approve S11 as a read-only trial readiness milestone. S11 is proposed only, not approved, and must preserve no live user-local default access, no PAI Memory writes, no ISA writes, no Pulse startup or calls, no root `AGENTS.md`, no `.codex/`, no product-memory promotion, and no drop-in claim.

Do not begin S11 from this document.

## Non-Goals

This decision log does not authorize S11, runtime adapter implementation, live trials, existing-local-v5 reads, live user-local reads, Claude Code invocation, Codex runtime invocation, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory promotion, root `AGENTS.md`, `.codex`, manifests, audit artifacts, executable schemas, runtime payloads, or dual-engine uncoordinated writes.
