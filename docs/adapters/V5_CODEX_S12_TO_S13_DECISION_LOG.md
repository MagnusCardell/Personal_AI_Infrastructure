# V5 Codex S12 to S13 Decision Log

## Purpose

Record S12E decisions, non-decisions, blocked decisions, and future architect questions for the transition from S12 readiness design to a proposed future S13 live-read-only trial.

## Scope

This decision log is documentation/design only. It closes no runtime gap, approves no S13 work, begins no S13 work, runs no live read-only trial, reads no live local state, creates no runtime adapter files, creates no root `AGENTS.md`, and creates no `.codex/`.

## Evidence Base

Evidence base:

- S11 release-fixture evidence closeout and existing S11A/S11C reports.
- S12A consent, source selection, PAI_DIR, preflight, abort, and reporting designs.
- S12B consent artifact schema and validation design.
- S12C PAI_DIR dry-run detection and source-root classification design.
- S12D preflight report schema, validation sequence, abort/evidence, and non-canonical output policies.
- S12E closeout, proposed S13 gates, proposed S13 contract, and proposed S13 risk register.

No live read-only trial has been run. No live local state has been read.

## Decisions Made in S12E

S12E decides that the S12 live-read-only readiness design track is closed pending architect review.

S12E decides that S13 may be proposed only as a future architect-approved milestone.

S12E decides that Codex remains not drop-in today and that runtime adapter planning remains blocked until future live-read-only evidence is accepted.

## Non-Decisions in S12E

S12E does not approve S13, begin S13, approve live existing-local-v5 reads, approve live user-local reads, approve personal-clone access, create consent artifacts, create preflight reports, implement detectors, implement preflight runners, implement live-read runners, implement runtime adapters, create root `AGENTS.md`, create `.codex/`, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, invoke Claude Code, invoke Codex runtime, authorize product-memory promotion, authorize dual-engine uncoordinated writes, claim Codex is drop-in, or claim Codex is the official upstream engine.

## Blocked Decisions

Blocked until future architect approval:

- Whether S12 readiness design is accepted.
- Whether S13A can begin.
- Whether any live local source may be read.
- Whether any consent artifact or record may be created.
- Whether any preflight report may be created.
- Whether PAI_DIR dry-run detection may run.
- Whether personal-clone access may ever be approved.
- Whether runtime adapter planning may begin after live-read-only evidence is accepted.

## Future Architect Questions

- Is S12 readiness design accepted for S13A consideration?
- What exact live source root, if any, may a future S13A read?
- What consent record is acceptable and where may it be written?
- What future preflight pass evidence is required before live reads?
- What no-residue validation is required for live read-only scope?
- What unsupported surfaces must be reported before runtime adapter planning?
- What evidence would be sufficient to unblock runtime adapter planning?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S12E-D01 | Codex remains not drop-in today. | S12 readiness design is not runtime proof. | S11/S12 closeout evidence. | Decided | Later replacement-grade validation. |
| S12E-D02 | S12 readiness design track is closed pending architect review. | S12A-S12D completed readiness design. | S12E closeout report. | Decided | Architect review outcome. |
| S12E-D03 | S13 is proposed only and not approved. | S12E has no approval authority for live reads. | S13 gate and contract docs. | Decided | Future architect-approved S13 card. |
| S12E-D04 | Future S13 must be read-only unless separately approved. | S13 is live-read evidence only. | S12A-S12D no-write boundaries. | Decided | Separate write-mode approval. |
| S12E-D05 | Future S13 requires explicit user consent. | Live local reads require explicit permission. | S12A/S12B consent design. | Decided | Future consent artifact review. |
| S12E-D06 | Future S13 requires explicit source selection. | Source roots must not be inferred. | S12A source-selection design. | Decided | Future source-selection review. |
| S12E-D07 | Future S13 requires read-only PAI_DIR detection. | PAI_DIR confidence must not grant write or broad-read permission. | S12C dry-run model. | Decided | Future PAI_DIR detector approval. |
| S12E-D08 | Future S13 requires preflight pass. | Live reads must fail closed before execution. | S12D validation sequence. | Decided | Future preflight approval. |
| S12E-D09 | Future S13 must not start Pulse or call Pulse endpoints. | Pulse behavior is outside read-only trial scope. | S12A-S12D Pulse boundaries. | Decided | Separate Pulse approval. |
| S12E-D10 | Future S13 must not write PAI Memory or ISA. | PAI Memory and ISA are canonical PAI state. | S12A-S12D Memory/ISA boundaries. | Decided | Separate write-mode approval. |
| S12E-D11 | Future S13 must not read product memories by default. | Product memory is outside default live read scope. | S12A-S12D product memory boundaries. | Decided | Separate product-memory approval. |
| S12E-D12 | Future S13 must not promote product memories. | Product memories must not be silently promoted into PAI Memory. | S12A-S12D non-promotion boundaries. | Decided | Separate promotion policy. |
| S12E-D13 | Future S13 must not create root AGENTS.md or .codex. | Runtime surfaces remain protected. | S12A-S12D protected-path rules. | Decided | Separate runtime surface approval. |
| S12E-D14 | Future S13 must not invoke Claude Code or Codex runtime adapter. | S13 remains read-only evidence, not runtime validation. | S12D runtime prohibition. | Decided | Future runtime validation card. |
| S12E-D15 | Future S13 output must be non-canonical. | Evidence must not become Memory, ISA, Pulse, manifest, or runtime payload. | S12A/S12D reporting policies. | Decided | Separate canonical-output approval. |
| S12E-D16 | Future S13 must not claim drop-in or official upstream status. | No replacement-grade validation exists. | S11/S12 limitations. | Decided | Later replacement-grade validation. |
| S12E-D17 | Runtime adapter planning remains blocked until live-read-only evidence is accepted. | Runtime planning requires accepted live evidence. | S12D and S12E non-goals. | Decided | Architect accepts future live-read-only evidence. |
| S12E-D18 | Architect approval is required before any S13 work. | S13 would read live local state and needs governance. | S13 T0 gate. | Decided | Future architect-approved S13 card. |

## Next Milestone Candidates

Advisory-only options, not approvals:

- `V5-S13A`: First approved live-read-only trial, only after S12 readiness is accepted.
- `V5-S13B`: Live-read-only evidence hardening, only after S13A.
- `V5-S13C`: Runtime adapter planning, only after live-read-only evidence is accepted.
- `V5-S14A`: Runtime adapter implementation planning, only after architect approval.

Architect approval is required before any future milestone.

## Non-Goals

This decision log does not approve S13, begin S13, run live reads, read existing-local-v5 state, inspect private user-local state, inspect live `~/.claude/PAI`, inspect live `~/.claude/projects`, inspect live `~/.codex`, inspect a personal clone, create root `AGENTS.md`, create `.codex/`, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, probe `localhost:31337`, invoke Claude Code, invoke Codex runtime, run installers, run Codex import or migration tooling, implement runtime adapter work, promote product memory, authorize dual-engine uncoordinated writes, claim Codex is drop-in today, or claim Codex is the official upstream engine.
