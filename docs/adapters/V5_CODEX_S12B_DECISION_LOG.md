# V5 Codex S12B Decision Log

## Purpose

Record S12B decisions, non-decisions, blocked decisions, and future architect questions for consent artifact schema and validation design.

Codex is not currently proven drop-in for existing local PAI v5 files.

## Scope

This decision log is documentation/design only. S12B designs consent artifact schema and validation boundaries only.

S12B does not create an actual consent artifact, does not implement a consent validator, does not create reports, does not run a live read-only trial, does not read existing-local-v5 state, does not read live user-local state, does not implement a runtime adapter, does not create root AGENTS.md, and does not create `.codex/`.

## Evidence Base

Evidence base:

- S10 fixture-only validation closeout.
- S11 release-fixture evidence closeout.
- S12A consent, source-selection, preflight, abort, reporting, and decision docs.
- S12B schema, validation, failure, abort, and reporting design docs.

No live user-local state or existing-local-v5 state was read.

## Decisions Made in S12B

S12B-D01 Codex remains not drop-in today.

S12B-D02 S12B designs consent artifact schema only.

S12B-D03 S12B creates no actual consent artifact.

S12B-D04 S12B implements no consent validator.

S12B-D05 Future consent must be explicit and source-specific.

S12B-D06 Future consent must be revocable and expiring.

S12B-D07 Consent cannot be inferred from Claude Code installation.

S12B-D08 Consent cannot be inferred from Codex installation.

S12B-D09 Consent cannot be inferred from dual subscriptions.

S12B-D10 Consent does not authorize PAI Memory writes.

S12B-D11 Consent does not authorize ISA writes.

S12B-D12 Consent does not authorize Pulse startup or endpoint calls.

S12B-D13 Consent does not authorize product-memory reads or promotion by default.

S12B-D14 Consent does not authorize root AGENTS.md or .codex writes.

S12B-D15 Consent reporting must be non-canonical.

S12B-D16 Future consent validation must abort on ambiguity, revocation, expiration, write pressure, Pulse pressure, product-memory pressure, runtime pressure, or drop-in claim pressure.

S12B-D17 S12B does not approve live existing-local-v5 reads.

S12B-D18 Runtime adapter planning remains blocked.

## Non-Decisions in S12B

S12B does not decide to approve live read-only trials, live existing-local-v5 reads, actual consent artifacts, actual consent validators, consent reports, PAI_DIR dry-run execution, runtime adapter implementation, root AGENTS.md, `.codex/`, Pulse startup, Pulse endpoint calls, PAI Memory writes, ISA writes, product-memory reads, product-memory promotion, Codex runtime invocation, Claude Code invocation, manifests, executable schemas, runtime payloads, or drop-in claims.

S12B does not decide that Codex is the official upstream engine.

## Blocked Decisions

Blocked until future architect approval:

- Whether to approve `V5-S12C`.
- Whether to approve `V5-S12D`.
- Whether to approve a real consent artifact.
- Whether to approve a real consent validator.
- Whether any live local source may be read.
- Whether `existing-local-v5-read-only` may be used.
- Whether runtime adapter planning may begin.

## Future Architect Questions

- Should S12C design PAI_DIR detection dry-run behavior next?
- Should a future milestone create an actual consent artifact schema file?
- Should a future milestone create a validator, and under what approved write set?
- What negative controls are required before consent validation can be trusted?
- What evidence is required before live-read-only trial approval?
- What evidence would be required before runtime adapter planning can be considered?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S12B-D01 | Codex remains not drop-in today. | Consent design is not runtime proof. | S10-S12A closeout evidence. | Decided | Later replacement-grade validation. |
| S12B-D02 | S12B designs consent artifact schema only. | The milestone is documentation/design. | S12B contract. | Decided | Architect approves implementation milestone. |
| S12B-D03 | S12B creates no actual consent artifact. | Actual artifacts are prohibited. | S12B hard failures. | Decided | Future approved artifact milestone. |
| S12B-D04 | S12B implements no consent validator. | Validator implementation is prohibited. | S12B hard failures. | Decided | Future approved validator milestone. |
| S12B-D05 | Future consent must be explicit and source-specific. | Live local reads require precise authorization. | S12A consent model. | Decided | Future consent artifact review. |
| S12B-D06 | Future consent must be revocable and expiring. | Stale or revoked permission must abort. | Validation and revocation spec. | Decided | Future validator design. |
| S12B-D07 | Consent cannot be inferred from Claude Code installation. | Installation is not consent. | S12A consent model. | Decided | None without contract change. |
| S12B-D08 | Consent cannot be inferred from Codex installation. | Installation is not consent. | S12A consent model. | Decided | None without contract change. |
| S12B-D09 | Consent cannot be inferred from dual subscriptions. | Subscription state is not consent. | S12A consent model. | Decided | None without contract change. |
| S12B-D10 | Consent does not authorize PAI Memory writes. | PAI Memory is canonical PAI state. | Schema and validation specs. | Decided | Future write-mode policy. |
| S12B-D11 | Consent does not authorize ISA writes. | ISA is canonical PAI state. | Schema and validation specs. | Decided | Future write-mode policy. |
| S12B-D12 | Consent does not authorize Pulse startup or endpoint calls. | Pulse remains denied by default. | Schema and reporting specs. | Decided | Separate Pulse approval. |
| S12B-D13 | Consent does not authorize product-memory reads or promotion by default. | Product memories must not be silently promoted into PAI Memory. | Schema and failure cases. | Decided | Separate product-memory policy. |
| S12B-D14 | Consent does not authorize root AGENTS.md or .codex writes. | Runtime surfaces remain protected. | Schema and failure cases. | Decided | Separate runtime surface approval. |
| S12B-D15 | Consent reporting must be non-canonical. | Reports must not become memory, manifest, or runtime state. | Reporting spec. | Decided | Separate canonical-output approval. |
| S12B-D16 | Future consent validation must abort on ambiguity, revocation, expiration, write pressure, Pulse pressure, product-memory pressure, runtime pressure, or drop-in claim pressure. | Fail-closed behavior is required before live reads. | Failure and abort cases. | Decided | Future validator negative controls. |
| S12B-D17 | S12B does not approve live existing-local-v5 reads. | S12B is design only. | S12B scope. | Decided | Future architect-approved live-read milestone. |
| S12B-D18 | Runtime adapter planning remains blocked. | Runtime planning requires accepted live-read-only evidence. | S12A and S12B scope. | Decided | Accepted future live-read-only evidence. |

## Next Milestone Candidates

Advisory-only options:

- `V5-S12C`: PAI_DIR detection dry-run design.
- `V5-S12D`: Live-read-only preflight report design.
- `V5-S12E`: S12 closeout and S13 proposed contract.
- `V5-S13A`: First approved live-read-only trial, only after S12 readiness is accepted.
- `V5-S13B`: Runtime adapter planning, only after live-read-only evidence is accepted.

Architect approval is required before any future milestone. This section is not an approval to begin S12C, S12D, S12E, S13A, S13B, or runtime adapter work.

## Non-Goals

S12B does not authorize actual consent artifacts, consent validators, consent reports, live trials, live user-local reads, existing-local-v5 access, PAI_DIR detection execution, runtime adapter implementation, root AGENTS.md, `.codex/`, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory reads, product-memory promotion, Codex runtime invocation, Claude Code invocation, manifests, executable schemas, PAI runtime audit artifacts, runtime payloads, official upstream engine claims, drop-in claims, or dual-engine uncoordinated writes.
