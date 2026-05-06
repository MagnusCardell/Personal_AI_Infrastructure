# V5 Codex PAI_DIR Dry-Run Reporting Spec

## Purpose

Define future non-canonical reporting for PAI_DIR dry-run detection.

Codex is not currently proven drop-in for existing local PAI v5 files. S12C designs reporting boundaries only and creates no detection report.

## Scope

This document is documentation/design only. It defines future dry-run reporting fields and non-canonical output boundaries.

S12C creates no detection report, no detector script, no consent artifact, no consent validator, no manifest, no executable schema, no live-trial artifact, no runtime payload, and no runtime adapter file.

## Evidence Base

Evidence base:

- S12A reporting boundary spec.
- S12A PAI_DIR detection and source selection spec.
- S12B consent non-canonical reporting spec.
- S12B consent failure and abort cases.
- S12C dry-run detection and classification designs.

No live user-local state, existing-local-v5 state, product memory, Pulse endpoint, or personal clone was read.

## Reporting Problem Statement

Future PAI_DIR dry-run reporting must communicate candidate, confidence, denial, unsupported surface, and abort evidence without becoming canonical state or implying live-read approval.

Report output must not become PAI Memory, ISA, Pulse state, Claude memory, Codex memory, a manifest, runtime payload, or proof that Codex is drop-in.

## Reporting Principles

Future reports must be:

- Non-canonical unless separately approved.
- Source-specific.
- Consent-bound.
- Privacy-preserving.
- No-write with respect to PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, and `.codex/`.
- Clear about abort and failure conditions.
- Explicit that no default live local read is allowed.

## Report Type Model

Future report types:

- `pai-dir-dry-run-report`
- `source-root-classification-report`
- `pai-dir-abort-report`
- `pai-dir-confidence-report`

S12C creates no detection report of any type.

## Required Report Fields

Required future report fields:

- `report_id`
- `report_type`
- `detection_id`
- `source_kind`
- `declared_source_root`
- `pai_dir_candidate`
- `candidate_status`
- `confidence`
- `consent_reference`
- `allowed_reads`
- `forbidden_reads`
- `forbidden_writes`
- `abort_required`
- `failure_reason`
- `denied_action_report`
- `unsupported_surface_report`
- `pulse_status`
- `memory_status`
- `isa_status`
- `product_memory_status`
- `drop_in_claim_status`
- `non_canonical_statement`
- `provenance`

These fields are future design only. They are not instantiated in S12C.

## Candidate Reporting

Candidate reporting must state the declared source root, `pai_dir_candidate`, candidate status, and whether the candidate was evaluated inside the approved consent and source-selection boundary.

Candidate reporting must not reveal private paths outside the approved reporting policy and must not write discovered paths to canonical memory.

## Confidence Reporting

Confidence reporting must use conservative future values such as:

- `not-evaluated`
- `low`
- `medium`
- `high`
- `insufficient`
- `ambiguous`

Insufficient or ambiguous confidence must set `abort_required` to true. Confidence must not be used to override missing consent, forbidden read scopes, write pressure, Pulse pressure, or runtime pressure.

## Abort Reporting

Abort reporting must include the failure ID, failure reason, denied action report, unsupported surface report when applicable, and non-canonical statement.

Abort reports must not become PAI Memory, ISA, Pulse state, Claude memory, Codex memory, manifests, runtime payloads, or proof that Codex is drop-in.

## Denied Action Reporting

Denied action reporting must cover attempts or pressure to:

- Read live `~/.claude/PAI` by default.
- Read live `~/.claude/projects`.
- Read live `~/.codex`.
- Inspect a personal clone without approval.
- Read product memory by default.
- Write PAI Memory or ISA.
- Start Pulse or call Pulse endpoints.
- Create root `AGENTS.md` or `.codex/`.
- Invoke Claude Code or Codex runtime.
- Claim drop-in behavior.

## Unsupported Surface Reporting

Unsupported surfaces must be reported explicitly and never silently ignored.

Unsupported surfaces may include Claude-shaped files that must not be copied directly into Codex surfaces, future Codex `AGENTS.md` router questions, Codex config/profile policy surfaces, hooks/rules boundaries, and any source-root class that lacks architect approval.

## Non-Canonical Output Rules

Reports are not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.

Reports must not be promoted into PAI Memory by default. Reports must not authorize writes, runtime adapter work, live existing-local-v5 access, personal-clone access, Pulse startup/calls, product-memory promotion, or dual-engine uncoordinated writes.

## Privacy and Retention Rules

Future reports must minimize private path disclosure and must retain only the fields approved by a future contract.

Retention must be bounded by consent, revocation, expiration, and rollback/no-residue expectations. S12C creates no report and no retained detection output.

## Pulse Reporting Boundary

Pulse status must remain `not-started-not-called` unless a separate future architect-approved card changes that boundary.

Reporting must not start Pulse, call endpoints, probe `localhost:31337`, create Pulse payloads, or create Pulse bridge files.

## Memory and ISA Reporting Boundary

Memory status must state no PAI Memory writes. ISA status must state no ISA writes.

Reports must not be stored as PAI Memory or ISA and must not update canonical PAI state.

## Product Memory Reporting Boundary

Product memory status must state product memory reads are denied by default and product-memory promotion is not authorized.

Product memories must not be silently promoted into PAI Memory.

## Drop-In Claim Reporting

Drop-in claim status must remain `not-claimed`.

Future PAI_DIR dry-run reports prove only dry-run detection evidence inside the approved source boundary. They do not prove Codex runtime replacement, official upstream engine status, or drop-in behavior.

## Required Future Proofs

Future reporting approval would require proof that:

- The report is non-canonical.
- The report writes only to an approved future path.
- The report does not read or expose forbidden private state.
- The report includes denied-action and unsupported-surface evidence.
- The report preserves Pulse no-start/no-call, PAI Memory no-write, ISA no-write, product-memory no-promotion, personal-clone future-only, and no drop-in claim boundaries.

## Prohibited Reporting Designs

Prohibited designs:

- Creating a detection report in S12C.
- Treating dry-run reports as PAI Memory, ISA, Pulse state, Claude memory, Codex memory, manifests, runtime payloads, or drop-in proof.
- Writing reports to root `AGENTS.md`, `.codex/`, PAI Memory, ISA, Pulse, Claude memory, or Codex memory.
- Reporting that authorizes live existing-local-v5 access, personal-clone access, Pulse startup/calls, product-memory promotion, runtime adapter work, or dual-engine uncoordinated writes.

## Non-Goals

S12C creates no detection report, creates no detector, creates no detector script, creates no consent artifact, creates no consent validator, runs no live read-only trial, reads no live existing-local-v5 state, inspects no private user-local state, inspects no personal clone, writes no PAI Memory, writes no ISA, starts no Pulse, calls no Pulse endpoints, invokes no Claude Code, invokes no Codex runtime, implements no runtime adapter, and claims no drop-in status.
