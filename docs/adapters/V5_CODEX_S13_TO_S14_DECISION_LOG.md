# V5 Codex S13 to S14 Decision Log

## Purpose

Record S13C decisions, non-decisions, blocked decisions, and future architect questions.

## Scope

This decision log closes the S13 clean-clone trial track for architect review and proposes S14 only as a future architect-approved milestone.

It does not approve S14, begin S14, approve personal-clone access, approve existing-local-v5 access, approve sanitized-user-fixture access, or authorize runtime adapter work.

## Evidence Base

Evidence base:

- S13A clean-clone positive-control trial artifacts.
- S13B clean-clone negative controls and path-safety hardening.
- S13C read-only validation of existing S13A artifacts.
- S12/S13 consent, source-selection, PAI_DIR, preflight, abort, non-canonical evidence, and no-residue policies.

Codex is not currently proven drop-in for existing local PAI v5 files.

## Decisions Made in S13C

S13C decisions:

- S13 clean-clone read-only evidence is ready for architect review.
- S13C closes the clean-clone read-only trial track only.
- S14 is proposed only and not approved.
- Future S14 must remain read-only unless separately approved.
- Future S14 requires explicit source class decision, explicit user consent, explicit source selection, read-only PAI_DIR detection if in scope, and a future preflight pass.
- Future S14 output must remain non-canonical.

## Non-Decisions in S13C

S13C does not decide:

- Whether S14 will be approved.
- Which source class S14 should use.
- Whether any existing-local-v5 path may be read.
- Whether any personal clone may be read.
- Whether any sanitized-user-fixture source may be used.
- Whether runtime adapter planning may begin.

## Blocked Decisions

Blocked decisions:

- Runtime adapter planning remains blocked until source-selected live-read-only evidence is accepted.
- Personal-clone access remains blocked until explicit architect approval, explicit user consent, and explicit source selection exist.
- Existing-local-v5 access remains blocked until explicit architect approval, explicit user consent, and explicit source selection exist.
- PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, root AGENTS.md, `.codex`, Codex runtime execution, and runtime adapter work remain blocked.

## Future Architect Questions

Future architect questions:

- Should S14A be approved as the first source-selected live-read-only trial?
- Which source class, if any, should be selected: `existing-local-v5-read-only`, `personal-clone-read-only`, or `sanitized-user-fixture-read-only`?
- What consent artifact shape and retention boundary should S14 require?
- What source root should be selected and how should it be validated?
- Should PAI_DIR detection be in scope, and if so, what read-only method is approved?
- What preflight pass evidence is required before any source-selected read?
- What no-residue proof is required?
- What evidence would be sufficient to unblock later runtime adapter planning?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S13C-D01 | Codex remains not drop-in today. | Clean-clone evidence is necessary but insufficient for replacement-grade validation. | S13A/S13B clean-clone evidence and S13C closeout. | Decided | Replacement-grade validation accepted by architect. |
| S13C-D02 | S13 clean-clone trial track is closed pending architect review. | S13A positive control and S13B negative controls are complete for clean-clone scope. | S13C read-only validation and closeout. | Decided | Architect requests additional clean-clone evidence. |
| S13C-D03 | S14 is proposed only and not approved. | S13C is documentation/design only and cannot authorize S14. | S13C contract and S14 proposal. | Decided | Future architect approval. |
| S13C-D04 | Future S14 must be read-only unless separately approved. | S14 follows clean-clone evidence into source-selected evidence, not runtime writes. | S14 gate proposal. | Decided | Architect explicitly approves writes. |
| S13C-D05 | Future S14 requires explicit source class decision. | Source class controls privacy, consent, and allowed reads. | S14 gates U1 and proposed source class options. | Decided | Future S14 architect card. |
| S13C-D06 | Future S14 requires explicit user consent. | Consent cannot be inferred from installation state or prior interaction. | S14 gates U2 and proposed consent requirements. | Decided | Future S14 consent design. |
| S13C-D07 | Future S14 requires explicit source selection. | Source root must be bound to source class and consent. | S14 gates U3 and proposed source selection requirements. | Decided | Future S14 source selection. |
| S13C-D08 | Future S14 requires read-only PAI_DIR detection. | PAI_DIR confidence must be source-bound, consent-bound, and abortable. | S14 gate U4. | Decided | Architect scopes PAI_DIR detection. |
| S13C-D09 | Future S14 requires preflight pass. | Source-selected reads must fail closed before access. | S14 gate U5. | Decided | Future preflight implementation. |
| S13C-D10 | Future S14 must not start Pulse or call Pulse endpoints. | S13C does not approve Pulse behavior. | S14 gates U8 and U9. | Decided | Separate architect approval for Pulse. |
| S13C-D11 | Future S14 must not write PAI Memory or ISA. | Memory and ISA are canonical PAI state. | S14 gates U10 and U11. | Decided | Separate architect approval for canonical writes. |
| S13C-D12 | Future S14 must not read product memories by default. | Product memory is not a default source selector or evidence source. | S14 gate U12. | Decided | Separate product-memory policy. |
| S13C-D13 | Future S14 must not promote product memories. | Product memory must not silently update PAI Memory. | S14 gate U13. | Decided | Separate architect approval. |
| S13C-D14 | Future S14 must not create root AGENTS.md or .codex. | S14 is read-only evidence, not Codex runtime surface creation. | S14 gates U6 and U7. | Decided | Later adapter-surface milestone. |
| S13C-D15 | Future S14 must not invoke Claude Code or Codex runtime adapter. | S14 is not runtime adapter execution. | S14 gates U15 and U16. | Decided | Later runtime validation approval. |
| S13C-D16 | Future S14 output must be non-canonical. | Evidence must not become PAI Memory, ISA, Pulse, manifest, or runtime payload. | S14 gate U18. | Decided | Architect approves canonical promotion. |
| S13C-D17 | Future S14 must not claim drop-in or official upstream status. | Clean-clone evidence does not prove drop-in or upstream status. | S14 gates U20 and U21. | Decided | Replacement-grade validation accepted. |
| S13C-D18 | Personal-clone access remains unapproved. | S13C does not authorize personal-clone reads. | S14 source class proposal. | Decided | Future architect selects and consents personal-clone source. |
| S13C-D19 | Existing-local-v5 access remains unapproved. | S13C does not authorize existing-local-v5 reads. | S14 source class proposal. | Decided | Future architect selects and consents existing-local-v5 source. |
| S13C-D20 | Runtime adapter planning remains blocked until live-read-only evidence is accepted. | Runtime planning needs source-selected evidence beyond clean clone. | S13C closeout and S14 proposal. | Blocked | Architect accepts future source-selected evidence. |
| S13C-D21 | Architect approval is required before any S14 work. | S13C is proposal-only. | S13C contract and S14 proposed contract. | Decided | Future architect card. |

## Next Milestone Candidates

Advisory-only options, not approvals:

- `V5-S14A`: First approved source-selected live-read-only trial, only after S13 clean-clone evidence is accepted.
- `V5-S14B`: Source-selected live-read-only evidence hardening, only after S14A.
- `V5-S14C`: Runtime adapter planning, only after source-selected live-read-only evidence is accepted.
- `V5-S15A`: Runtime adapter implementation planning, only after architect approval.

Architect approval is required before any future milestone.

## Non-Goals

This decision log does not approve S14, begin S14, approve personal-clone access, approve existing-local-v5 access, approve sanitized-user-fixture access, read live user-local state, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, probe `localhost:31337`, invoke Claude Code, invoke Codex runtime, create root AGENTS.md, create `.codex`, create runtime payloads, authorize product-memory promotion, authorize dual-engine uncoordinated writes, claim Codex is drop-in today, claim Codex is official upstream, or authorize runtime adapter work.
