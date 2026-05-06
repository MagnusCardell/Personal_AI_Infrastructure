# V5 Codex S11 to S12 Decision Log

## Purpose

Record S11D decisions that close the S11 release-fixture evidence track and frame S12 as a future, architect-approved proposal only.

Codex is not currently proven drop-in for existing local PAI v5 files.

## Scope

This decision log is documentation/design only. It does not authorize S12, live trials, existing-local-v5 access, runtime adapter implementation, root `AGENTS.md`, `.codex`, Pulse startup, Pulse endpoint calls, PAI Memory writes, ISA writes, product-memory promotion, or dual-engine uncoordinated writes.

## Evidence Base

Evidence comes from:

- S10 fixture-only closeout and S11 readiness gates.
- S11A release-fixture evidence report.
- S11B report-generator negative controls.
- S11C readiness gate evaluation.
- S11D closeout report and proposed S12 contract.

The S11 release-fixture evidence track is closed pending architect review. It remains necessary but insufficient for drop-in claims.

## Decisions Made in S11D

S11D-D01 Codex remains not drop-in today.

S11D-D02 S11 release-fixture evidence track is closed pending architect review.

S11D-D03 S12 is proposed only and not approved.

S11D-D04 Future S12 must be read-only unless separately approved.

S11D-D05 Existing-local-v5 access remains future-only and explicit.

S11D-D06 User consent model is required before any live local read.

S11D-D07 PAI_DIR detection must be read-only.

S11D-D08 Root AGENTS.md remains protected.

S11D-D09 .codex remains protected.

S11D-D10 Pulse startup remains prohibited by default.

S11D-D11 Pulse endpoint calls remain prohibited by default.

S11D-D12 PAI Memory writes remain prohibited.

S11D-D13 ISA writes remain prohibited.

S11D-D14 Product-memory promotion remains prohibited.

S11D-D15 Future S12 must preserve authority, launcher/inference, hook/lifecycle, Pulse, Memory/ISA, rollback, and evidence boundaries.

S11D-D16 Future runtime adapter planning remains blocked until S12 readiness is accepted.

S11D-D17 S11D creates no runtime, fixture, harness, schema, manifest, audit artifact, or live-trial artifact.

S11D-D18 Architect approval is required before any S12 work.

## Non-Decisions in S11D

S11D does not decide to begin S12. S11D does not approve live trials, live existing-local-v5 access, live user-local reads, or `PAI_DIR` detection.

S11D does not approve runtime adapter implementation, Codex runtime invocation, Claude Code invocation, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory promotion, root `AGENTS.md`, `.codex/`, manifests, executable schemas, audit artifacts, runtime payloads, or dual-engine uncoordinated writes.

## Blocked Decisions

Blocked until future architect approval:

- Whether to approve S12 as a live read-only trial readiness milestone.
- Whether any live local source can be read.
- What explicit user consent design is acceptable.
- Whether read-only `PAI_DIR` detection can be used.
- Whether any future Pulse startup or Pulse endpoint call can ever be allowed.
- Whether runtime adapter planning can begin after S12 review.

## Future Architect Questions

- Should S12 be approved as a live read-only trial readiness milestone?
- What exact sources may S12 read, if any?
- What explicit user consent design is required before any live local read?
- Should `PAI_DIR` detection be allowed, and if so, under what read-only constraints?
- What evidence is required before runtime adapter planning may begin?
- What rollback, no-residue, and provenance evidence is required before any future write mode?

## Decision Table

| ID | Decision | Status |
| --- | --- | --- |
| S11D-D01 | Codex remains not drop-in today. | Decided |
| S11D-D02 | S11 release-fixture evidence track is closed pending architect review. | Decided |
| S11D-D03 | S12 is proposed only and not approved. | Decided |
| S11D-D04 | Future S12 must be read-only unless separately approved. | Decided |
| S11D-D05 | Existing-local-v5 access remains future-only and explicit. | Decided |
| S11D-D06 | User consent model is required before any live local read. | Decided |
| S11D-D07 | PAI_DIR detection must be read-only. | Decided |
| S11D-D08 | Root AGENTS.md remains protected. | Decided |
| S11D-D09 | .codex remains protected. | Decided |
| S11D-D10 | Pulse startup remains prohibited by default. | Decided |
| S11D-D11 | Pulse endpoint calls remain prohibited by default. | Decided |
| S11D-D12 | PAI Memory writes remain prohibited. | Decided |
| S11D-D13 | ISA writes remain prohibited. | Decided |
| S11D-D14 | Product-memory promotion remains prohibited. | Decided |
| S11D-D15 | Future S12 must preserve authority, launcher/inference, hook/lifecycle, Pulse, Memory/ISA, rollback, and evidence boundaries. | Decided |
| S11D-D16 | Future runtime adapter planning remains blocked until S12 readiness is accepted. | Decided |
| S11D-D17 | S11D creates no runtime, fixture, harness, schema, manifest, audit artifact, or live-trial artifact. | Decided |
| S11D-D18 | Architect approval is required before any S12 work. | Decided |

## Next Milestone Candidates

The next real architect decision should be whether to review the S11 evidence closeout and decide if S12 should be approved as a future read-only milestone with explicit user consent design.

Do not begin S12 from this document.

## Non-Goals

This decision log does not authorize S12, live trials, live user-local reads, existing-local-v5 access, runtime adapter implementation, root `AGENTS.md`, `.codex`, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory promotion, Codex runtime invocation, Claude Code invocation, manifests, executable schemas, audit artifacts, runtime payloads, official upstream engine claims, drop-in claims, or dual-engine uncoordinated writes.
