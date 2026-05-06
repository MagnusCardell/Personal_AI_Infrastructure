# V5 Codex S12C Decision Log

## Purpose

Record S12C decisions, non-decisions, blocked decisions, and future architect questions for PAI_DIR detection dry-run design.

Codex is not currently proven drop-in for existing local PAI v5 files.

## Scope

This decision log is documentation/design only. S12C designs PAI_DIR dry-run detection, source-root classification, failure, and reporting boundaries only.

S12C implements no detector, creates no detector script, creates no consent artifact, creates no consent validator, creates no reports, runs no live read-only trial, reads no live existing-local-v5 state, inspects no private user-local state, inspects no personal clone, implements no runtime adapter, creates no root AGENTS.md, and creates no `.codex/`.

## Evidence Base

Evidence base:

- S10 fixture-only validation closeout.
- S11 release-fixture evidence closeout.
- S12A consent, PAI_DIR source-selection, preflight, abort, reporting, and decision docs.
- S12B consent schema, validation, failure, abort, reporting, and decision docs.
- S12C dry-run detection, classification, failure, and reporting design docs.

No live user-local state, existing-local-v5 state, live `PAI_DIR`, live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, product memory, or personal clone was read.

## Decisions Made in S12C

S12C-D01 Codex remains not drop-in today.

S12C-D02 S12C designs PAI_DIR dry-run detection only.

S12C-D03 S12C implements no detector.

S12C-D04 S12C reads no live PAI_DIR.

S12C-D05 S12C does not inspect the personal clone.

S12C-D06 Clean clone status does not imply live PAI install.

S12C-D07 Future detection must be consent-bound.

S12C-D08 Future detection must be source-specific.

S12C-D09 Future detection must be abortable.

S12C-D10 Future detection output is non-canonical.

S12C-D11 Existing-local-v5-read-only remains future-only.

S12C-D12 Personal-clone-read-only remains future-only.

S12C-D13 Product memory reads remain denied by default.

S12C-D14 Pulse startup and endpoint calls remain denied.

S12C-D15 PAI Memory and ISA writes remain denied.

S12C-D16 Root AGENTS.md and .codex remain protected.

S12C-D17 Future detector validation must prove no default home scan.

S12C-D18 Runtime adapter planning remains blocked.

## Non-Decisions in S12C

S12C does not decide to approve live read-only trials, live existing-local-v5 reads, live PAI_DIR detection, personal-clone access, detector implementation, detector scripts, consent artifacts, consent validators, detection reports, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, root AGENTS.md, `.codex/`, runtime adapter implementation, Codex runtime invocation, Claude Code invocation, manifests, executable schemas, runtime payloads, or drop-in claims.

S12C does not decide that Codex is the official upstream engine.

## Blocked Decisions

Blocked until future architect approval:

- Whether to approve `V5-S12D`.
- Whether to approve actual PAI_DIR dry-run detector implementation.
- Whether to approve a real consent artifact.
- Whether to approve a real consent validator.
- Whether any live local source may be read.
- Whether a personal clone may be inspected.
- Whether `existing-local-v5-read-only` may be used.
- Whether runtime adapter planning may begin.

## Future Architect Questions

- Should S12D design live-read-only preflight report behavior next?
- What proof would be required before any detector implementation is permitted?
- What negative controls would prove no default home scan?
- What consent artifact state would be acceptable before any dry-run detector reads live paths?
- How should a future contract distinguish clean clone evidence from live PAI install evidence?
- What evidence is required before live-read-only trial approval?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S12C-D01 | Codex remains not drop-in today. | Dry-run detection design is not runtime proof. | S10-S12B closeout evidence. | Decided | Later replacement-grade validation. |
| S12C-D02 | S12C designs PAI_DIR dry-run detection only. | The milestone is documentation/design. | S12C contract. | Decided | Architect approves implementation milestone. |
| S12C-D03 | S12C implements no detector. | Detector implementation is prohibited. | S12C hard failures. | Decided | Future approved detector milestone. |
| S12C-D04 | S12C reads no live PAI_DIR. | Live PAI_DIR reads are prohibited. | S12C scope and source protocol. | Decided | Future approved live-read milestone. |
| S12C-D05 | S12C does not inspect the personal clone. | Personal clone access is prohibited. | S12C source-root spec. | Decided | Future approval plus explicit user consent. |
| S12C-D06 | Clean clone status does not imply live PAI install. | Clone evidence is not existing-local-v5 state. | Source-root classification spec. | Decided | Future source classification validation. |
| S12C-D07 | Future detection must be consent-bound. | Live or personal sources require explicit user consent. | S12A/S12B consent docs. | Decided | Future consent artifact approval. |
| S12C-D08 | Future detection must be source-specific. | Detection cannot scan arbitrary roots. | PAI_DIR dry-run model. | Decided | Future detector design review. |
| S12C-D09 | Future detection must be abortable. | Ambiguity and pressure must fail closed. | Detection failure cases. | Decided | Future negative-control implementation. |
| S12C-D10 | Future detection output is non-canonical. | Output must not become memory, manifest, or runtime state. | Reporting spec. | Decided | Separate canonical-output approval. |
| S12C-D11 | Existing-local-v5-read-only remains future-only. | Live local PAI state is not approved for S12C. | S12A/S12B source model. | Decided | Architect-approved live-read milestone. |
| S12C-D12 | Personal-clone-read-only remains future-only. | Personal clone access needs explicit approval and consent. | Source-root classification spec. | Decided | Future personal-clone approval. |
| S12C-D13 | Product memory reads remain denied by default. | Product memories must not be silently promoted into PAI Memory. | S12A/S12B/S12C boundaries. | Decided | Separate product-memory policy. |
| S12C-D14 | Pulse startup and endpoint calls remain denied. | Pulse remains outside dry-run detection. | Pulse boundaries. | Decided | Separate Pulse approval. |
| S12C-D15 | PAI Memory and ISA writes remain denied. | PAI Memory and ISA are canonical PAI state. | Memory/ISA boundaries. | Decided | Future write-mode policy. |
| S12C-D16 | Root AGENTS.md and .codex remain protected. | Runtime surfaces remain protected. | Protected path rules. | Decided | Separate runtime surface approval. |
| S12C-D17 | Future detector validation must prove no default home scan. | No default live local read is a hard boundary. | Dry-run model and failure cases. | Decided | Future detector negative controls. |
| S12C-D18 | Runtime adapter planning remains blocked. | Runtime planning requires accepted live-read-only evidence. | S12C non-goals. | Decided | Accepted future live-read-only evidence. |

## Next Milestone Candidates

Advisory-only options:

- `V5-S12D`: Live-read-only preflight report design.
- `V5-S12E`: S12 closeout and S13 proposed contract.
- `V5-S13A`: First approved live-read-only trial, only after S12 readiness is accepted.
- `V5-S13B`: Runtime adapter planning, only after live-read-only evidence is accepted.

Architect approval is required before any future milestone. This section is not an approval to begin S12D, S12E, S13A, S13B, or runtime adapter work.

## Non-Goals

S12C does not authorize detector implementation, detector scripts, consent artifacts, consent validators, detection reports, live trials, live user-local reads, existing-local-v5 access, personal-clone access, runtime adapter implementation, root AGENTS.md, `.codex/`, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory reads, product-memory promotion, Codex runtime invocation, Claude Code invocation, manifests, executable schemas, PAI runtime audit artifacts, runtime payloads, official upstream engine claims, drop-in claims, or dual-engine uncoordinated writes.
