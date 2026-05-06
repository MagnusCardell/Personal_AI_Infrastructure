# V5 Codex S12D Decision Log

## Purpose

Record S12D decisions, non-decisions, blocked decisions, and future architect questions for live-read-only preflight report design.

Codex is not currently proven drop-in for existing local PAI v5 files.

## Scope

This decision log is documentation/design only. S12D designs preflight report contract, validation sequence, abort evidence, and non-canonical output policy only.

S12D creates no actual preflight report, implements no preflight runner, creates no detector script, creates no consent artifact, creates no consent validator, runs no live read-only trial, reads no live existing-local-v5 state, inspects no private user-local state, inspects no personal clone, implements no runtime adapter, creates no root AGENTS.md, and creates no `.codex/`.

## Evidence Base

Evidence base:

- S10 fixture-only validation closeout.
- S11 release-fixture evidence closeout.
- S12A consent, PAI_DIR source-selection, preflight, abort, reporting, and decision docs.
- S12B consent schema, validation, failure, abort, reporting, and decision docs.
- S12C PAI_DIR dry-run detection, classification, failure, reporting, and decision docs.
- S12D schema, validation sequence, abort evidence, and output policy docs.

No live user-local state, existing-local-v5 state, live `PAI_DIR`, live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, product memory, or personal clone was read.

## Decisions Made in S12D

S12D-D01 Codex remains not drop-in today.

S12D-D02 S12D designs preflight report contract only.

S12D-D03 S12D creates no actual preflight report.

S12D-D04 S12D implements no preflight runner.

S12D-D05 S12D reads no live PAI_DIR.

S12D-D06 S12D reads no live user-local state.

S12D-D07 Future preflight must require architect approval.

S12D-D08 Future preflight must require valid consent.

S12D-D09 Future preflight must fail closed.

S12D-D10 Future preflight proceed does not mean drop-in.

S12D-D11 Product memory reads remain denied by default.

S12D-D12 Pulse startup and endpoint calls remain denied.

S12D-D13 PAI Memory and ISA writes remain denied.

S12D-D14 Root AGENTS.md and .codex remain protected.

S12D-D15 Future preflight output is non-canonical.

S12D-D16 Personal-clone access remains future-only.

S12D-D17 Existing-local-v5 read remains future-only.

S12D-D18 Runtime adapter planning remains blocked.

## Non-Decisions in S12D

S12D does not decide to approve live read-only trials, live existing-local-v5 reads, live PAI_DIR detection, personal-clone access, preflight runner implementation, detector scripts, consent artifacts, consent validators, actual preflight reports, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, root AGENTS.md, `.codex/`, runtime adapter implementation, Codex runtime invocation, Claude Code invocation, manifests, executable schemas, runtime payloads, or drop-in claims.

S12D does not decide that Codex is the official upstream engine.

## Blocked Decisions

Blocked until future architect approval:

- Whether to approve `V5-S12E`.
- Whether to create an actual preflight report.
- Whether to implement a preflight runner.
- Whether to create a consent artifact.
- Whether to create a consent validator.
- Whether to implement a detector script.
- Whether any live local source may be read.
- Whether a personal clone may be inspected.
- Whether runtime adapter planning may begin.

## Future Architect Questions

- Should S12E close S12 and propose the S13 live-read-only trial contract?
- What negative controls would prove every preflight step fails closed?
- What approved write set would be acceptable for a future actual preflight report?
- What consent artifact state is required before any preflight runner can execute?
- What proof is needed before `Proceed` can lead to a live read-only trial?
- What evidence is required before runtime adapter planning can be considered?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S12D-D01 | Codex remains not drop-in today. | Preflight design is not runtime proof. | S10-S12C closeout evidence. | Decided | Later replacement-grade validation. |
| S12D-D02 | S12D designs preflight report contract only. | The milestone is documentation/design. | S12D contract. | Decided | Architect approves implementation milestone. |
| S12D-D03 | S12D creates no actual preflight report. | Actual reports are prohibited. | S12D hard failures. | Decided | Future approved report milestone. |
| S12D-D04 | S12D implements no preflight runner. | Runner implementation is prohibited. | S12D hard failures. | Decided | Future approved runner milestone. |
| S12D-D05 | S12D reads no live PAI_DIR. | Live PAI_DIR reads are prohibited. | S12D scope and source protocol. | Decided | Future approved live-read milestone. |
| S12D-D06 | S12D reads no live user-local state. | Private state reads are prohibited. | S12D source protocol. | Decided | Future explicit consent plus approval. |
| S12D-D07 | Future preflight must require architect approval. | Live-read eligibility requires explicit governance. | Validation sequence step P0. | Decided | Future preflight runner review. |
| S12D-D08 | Future preflight must require valid consent. | Consent is the access boundary. | Validation sequence step P1. | Decided | Future consent artifact approval. |
| S12D-D09 | Future preflight must fail closed. | Unsafe ambiguity must abort. | Validation sequence and evidence model. | Decided | Future negative controls. |
| S12D-D10 | Future preflight proceed does not mean drop-in. | Proceed is only read-only trial eligibility. | Validation sequence step P13. | Decided | Later replacement-grade validation. |
| S12D-D11 | Product memory reads remain denied by default. | Product memories must not be silently promoted into PAI Memory. | Output policy and evidence model. | Decided | Separate product-memory policy. |
| S12D-D12 | Pulse startup and endpoint calls remain denied. | Pulse remains outside preflight by default. | Pulse boundary checks. | Decided | Separate Pulse approval. |
| S12D-D13 | PAI Memory and ISA writes remain denied. | PAI Memory and ISA are canonical PAI state. | Memory/ISA output policy. | Decided | Future write-mode policy. |
| S12D-D14 | Root AGENTS.md and .codex remain protected. | Runtime surfaces remain protected. | Protected path rules. | Decided | Separate runtime surface approval. |
| S12D-D15 | Future preflight output is non-canonical. | Output must not become memory, manifest, or runtime state. | Non-canonical output policy. | Decided | Separate canonical-output approval. |
| S12D-D16 | Personal-clone access remains future-only. | Personal clone access needs explicit approval and consent. | S12C and S12D boundaries. | Decided | Future personal-clone approval. |
| S12D-D17 | Existing-local-v5 read remains future-only. | Live local PAI state is not approved for S12D. | S12D non-goals. | Decided | Architect-approved live-read milestone. |
| S12D-D18 | Runtime adapter planning remains blocked. | Runtime planning requires accepted live-read-only evidence. | S12D non-goals. | Decided | Accepted future live-read-only evidence. |

## Next Milestone Candidates

Advisory-only options:

- `V5-S12E`: S12 closeout and S13 proposed contract.
- `V5-S13A`: First approved live-read-only trial, only after S12 readiness is accepted.
- `V5-S13B`: Runtime adapter planning, only after live-read-only evidence is accepted.

Architect approval is required before any future milestone. This section is not an approval to begin S12E, S13A, S13B, or runtime adapter work.

## Non-Goals

S12D does not authorize preflight runner implementation, actual preflight reports, detector scripts, consent artifacts, consent validators, live trials, live user-local reads, existing-local-v5 access, personal-clone access, runtime adapter implementation, root AGENTS.md, `.codex/`, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, product-memory reads, product-memory promotion, Codex runtime invocation, Claude Code invocation, manifests, executable schemas, PAI runtime audit artifacts, runtime payloads, official upstream engine claims, drop-in claims, or dual-engine uncoordinated writes.
