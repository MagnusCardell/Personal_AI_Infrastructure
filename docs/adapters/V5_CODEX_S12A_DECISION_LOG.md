# V5 Codex S12A Decision Log

## Purpose

Record S12A decisions, non-decisions, blocked decisions, and future architect questions for live read-only consent, source selection, PAI_DIR detection, preflight, abort, and reporting design.

Codex is not currently proven drop-in for existing local PAI v5 files.

## Scope

This decision log is documentation/design only. S12A does not run a live read-only trial, does not read existing-local-v5 state, does not read live user-local state, does not implement a runtime adapter, does not create root `AGENTS.md`, and does not create `.codex/`. The root AGENTS.md boundary remains protected.

This log does not authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory reads, product-memory promotion, runtime adapter work, live trials, or dual-engine uncoordinated writes.

## Evidence Base

Evidence base:

- S10 fixture-only validation closeout.
- S11 release-fixture evidence closeout.
- S11D S12 live read-only trial readiness gates.
- S11D proposed S12 write set and completion contract.
- S12A consent, PAI_DIR detection, preflight, abort, and reporting boundary specs.

No live user-local state or existing-local-v5 state was read for this decision log.

## Decisions Made in S12A

S12A-D01 Codex remains not drop-in today.

S12A-D02 S12A designs consent and source-selection only.

S12A-D03 S12A does not run a live read-only trial.

S12A-D04 S12A does not read live existing-local-v5 state.

S12A-D05 Future live read requires explicit user consent.

S12A-D06 Consent cannot be inferred from Claude Code installation.

S12A-D07 Consent cannot be inferred from Codex installation.

S12A-D08 Consent cannot be inferred from dual subscriptions.

S12A-D09 PAI_DIR detection remains future-only and read-only.

S12A-D10 No default live local read is allowed.

S12A-D11 Product memory reads remain denied by default.

S12A-D12 Pulse startup and endpoint calls remain denied.

S12A-D13 PAI Memory and ISA writes remain denied.

S12A-D14 Root AGENTS.md and .codex remain protected.

S12A-D15 Future reporting output must be non-canonical.

S12A-D16 Runtime adapter planning remains blocked until live-read-only readiness is approved.

## Non-Decisions in S12A

S12A does not decide to begin a live read-only trial. S12A does not approve live existing-local-v5 access, live user-local reads, live `PAI_DIR` detection, product memory reads, Pulse startup, Pulse endpoint calls, PAI Memory writes, ISA writes, Codex runtime invocation, Claude Code invocation, runtime adapter implementation, root `AGENTS.md`, `.codex/`, manifests, schemas, audit artifacts, live-trial artifacts, runtime payloads, or product-memory promotion.

S12A does not decide that Codex is a drop-in replacement and does not decide that Codex is the official upstream engine.

## Blocked Decisions

Blocked until future architect approval:

- Whether S12B, S12C, S12D, S13A, or S13B should begin.
- Whether any live local source may be read.
- Whether any `existing-local-v5-read-only` source can be selected.
- Whether any future consent artifact may be created.
- Whether `PAI_DIR` detection may run as a dry run.
- Whether any future report may become canonical.
- Whether runtime adapter planning may begin.

## Future Architect Questions

- What exact proof is required before approving a future live read-only trial?
- What consent artifact proposal is acceptable, if any?
- Should PAI_DIR detection be designed as a dry run before any live read?
- What source-selection UX or CLI contract is acceptable?
- How should abort reports be retained without becoming PAI Memory, ISA, Pulse state, a manifest, or runtime payload?
- What evidence would be required before runtime adapter planning can be considered?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S12A-D01 | Codex remains not drop-in today. | S10/S11 evidence is necessary but insufficient for runtime replacement. | S11D closeout and S12 gates. | Decided | Architect accepts later live-read and runtime evidence. |
| S12A-D02 | S12A designs consent and source-selection only. | The approved write set is documentation-only. | S12A contract. | Decided | New architect-approved milestone. |
| S12A-D03 | S12A does not run a live read-only trial. | Live access requires future approval. | S12A hard failures. | Decided | Architect approves a future live-read trial. |
| S12A-D04 | S12A does not read live existing-local-v5 state. | Existing local state is private and future-only. | S12A source protocol. | Decided | Explicit user consent plus architect approval. |
| S12A-D05 | Future live read requires explicit user consent. | Consent must be explicit, bounded, revocable, and source-specific. | Consent model. | Decided | Future consent artifact proposal. |
| S12A-D06 | Consent cannot be inferred from Claude Code installation. | Installation is not source-specific consent. | Consent model. | Decided | None without future contract change. |
| S12A-D07 | Consent cannot be inferred from Codex installation. | Installation is not source-specific consent. | Consent model. | Decided | None without future contract change. |
| S12A-D08 | Consent cannot be inferred from dual subscriptions. | Subscription state is not consent. | Consent model. | Decided | None without future contract change. |
| S12A-D09 | PAI_DIR detection remains future-only and read-only. | S12A does not inspect live `PAI_DIR`. | PAI_DIR spec. | Decided | Architect-approved dry-run design. |
| S12A-D10 | No default live local read is allowed. | Private state must fail closed by default. | PAI_DIR spec and preflight model. | Decided | Explicit source selection and consent approval. |
| S12A-D11 | Product memory reads remain denied by default. | Product memories must not be silently promoted into PAI Memory. | Consent and reporting specs. | Decided | Separate product-memory policy approval. |
| S12A-D12 | Pulse startup and endpoint calls remain denied. | S12A does not start Pulse or call endpoints. | Preflight and reporting specs. | Decided | Separate Pulse-specific approval. |
| S12A-D13 | PAI Memory and ISA writes remain denied. | They are canonical PAI state. | Consent and preflight specs. | Decided | Separate write-mode policy approval. |
| S12A-D14 | Root AGENTS.md and .codex remain protected. | Runtime surfaces are not authorized. | Consent, source, and preflight specs. | Decided | Separate architect-approved runtime surface card. |
| S12A-D15 | Future reporting output must be non-canonical. | Reports must not become memory, manifest, audit, or runtime state by default. | Reporting boundary spec. | Decided | Separate canonical-output approval. |
| S12A-D16 | Runtime adapter planning remains blocked until live-read-only readiness is approved. | Runtime planning requires later evidence. | S11D and S12A scope. | Decided | Architect accepts live-read-only readiness evidence. |

## Next Milestone Candidates

Advisory-only options:

- `V5-S12B`: Consent artifact proposal and validation design.
- `V5-S12C`: PAI_DIR detection dry-run design.
- `V5-S12D`: Live-read-only preflight report design.
- `V5-S13A`: First approved live-read-only trial, only after S12 readiness is accepted.
- `V5-S13B`: Runtime adapter planning, only after live-read-only trial evidence is accepted.

Architect approval is required before any future milestone. This section is not an approval to begin S12B, S12C, S12D, S13A, S13B, or runtime adapter work.

## Non-Goals

S12A does not authorize live trials, live user-local reads, existing-local-v5 access, `PAI_DIR` detection execution, runtime adapter implementation, root `AGENTS.md`, `.codex/`, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory reads, product-memory promotion, Codex runtime invocation, Claude Code invocation, manifests, executable schemas, PAI runtime audit artifacts, runtime payloads, official upstream engine claims, drop-in claims, or dual-engine uncoordinated writes.
