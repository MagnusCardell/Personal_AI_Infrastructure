# V5 Codex Preflight Abort and Evidence Model

## Purpose

Define future abort reasons, evidence records, denied-action evidence, unsupported-surface evidence, and failure classification for live-read-only preflight.

Codex is not currently proven drop-in for existing local PAI v5 files. S12D defines design-only abort evidence and creates no preflight report.

## Scope

This document is documentation/design only. It enumerates future preflight abort evidence that must stop before any future live existing-local-v5 read-only trial can proceed.

It does not implement a preflight runner, create a preflight report, create a detector script, create a consent artifact, create a consent validator, run a live read-only trial, inspect live `~/.claude/PAI`, inspect live `~/.claude/projects`, inspect live `~/.codex`, inspect any personal clone, or implement runtime adapter behavior.

## Evidence Base

Evidence base:

- S12A preflight and abort model.
- S12A reporting boundary spec.
- S12B consent validation and failure cases.
- S12C PAI_DIR dry-run detection failure cases.
- S12D preflight report schema proposal.

No live source root, private user-local state, product memory, Pulse endpoint, Claude Code runtime, or Codex runtime was used.

## Abort Evidence Problem Statement

Future preflight must explain why it aborts without reading forbidden state, writing canonical state, invoking runtimes, or treating abort as a recoverable warning.

Abort evidence must support architect review, not live access, runtime implementation, or drop-in claims.

## Abort Principles

Abort principles:

- Fail closed.
- Abort before forbidden reads or writes.
- Preserve no default live local read.
- Preserve no Pulse startup/calls.
- Preserve no PAI Memory or ISA writes.
- Preserve product memory denial by default.
- Preserve runtime invocation denial.
- Produce only non-canonical advisory evidence under a future approved write set.

## Abort Reason Model

Future abort reasons must be explicit, stable, and tied to evidence IDs.

Abort reasons must include missing approval, invalid consent, invalid source, invalid PAI_DIR candidate, forbidden read pressure, forbidden write pressure, product-memory pressure, Pulse pressure, Memory/ISA pressure, runtime pressure, unsupported-surface silence, canonical-output pressure, personal-clone pressure, clean-clone confusion, missing rollback/no-residue expectation, missing retention policy, and drop-in claim pressure.

## Evidence Record Model

Future evidence records should include:

- Evidence ID.
- Evidence class.
- Trigger.
- Required preflight response.
- Required report field.
- Future proof required.
- Status.

Evidence records are not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.

## Consent Evidence

Consent evidence must prove architect approval and explicit user consent are present, valid, not expired, not revoked, source-specific, and not replayed.

Missing, expired, revoked, mismatched, or ambiguous consent must abort.

## Source Root Evidence

Source root evidence must prove the declared source root is explicit, matches consent, is inside allowed scope, and is not an arbitrary home directory, unapproved personal clone, or clean clone mistaken for live PAI install.

Source root evidence must not authorize writes.

## PAI_DIR Evidence

PAI_DIR evidence must prove the future candidate is declared, source-specific, consent-bound, and confidence-qualified.

Attempted default reads of live `~/.claude/PAI` must abort. Insufficient confidence must abort.

## Read Scope Evidence

Read scope evidence must prove allowed reads are path-bounded and forbidden reads remain denied.

Attempted reads of live `~/.claude/projects`, live `~/.codex`, product memory by default, arbitrary home directories, or unapproved personal clones must abort.

## Write Pressure Evidence

Write pressure evidence must capture any attempt or requirement to write, create, modify, import, migrate, normalize, promote, persist, or generate state.

Any write pressure must abort even if consent is otherwise valid.

## Product Memory Evidence

Product memory evidence must prove product memory reads are denied by default and product-memory promotion into PAI Memory is not authorized.

Product memory pressure must abort.

## Pulse Evidence

Pulse evidence must prove no Pulse startup, no Pulse endpoint calls, no `localhost:31337` probe, no Pulse payloads, no Pulse bridge files, and no Pulse parity claim.

Pulse pressure must abort.

## Memory and ISA Evidence

Memory and ISA evidence must prove no PAI Memory writes and no ISA writes.

Future preflight evidence must not become PAI Memory or ISA.

## Runtime Invocation Evidence

Runtime invocation evidence must prove no Claude Code invocation, no Codex runtime invocation, no Codex runtime adapter execution, no Codex import/migration tooling, no Codex hook/rule/execpolicy commands, and no installer execution.

Runtime pressure must abort.

## Reporting Evidence

Reporting evidence must prove future output remains non-canonical, advisory, retention-bounded, rollback/no-residue-bounded, and not a manifest, runtime payload, PAI runtime audit artifact, Memory, ISA, Pulse state, Claude memory, Codex memory, or drop-in proof.

Unsupported surfaces must be reported and not silently ignored.

## Abort Evidence Table

| Evidence ID | Evidence class | Trigger | Required preflight response | Required report field | Future proof required | S12D status |
| --- | --- | --- | --- | --- | --- | --- |
| PE-001 | Architect approval | Architect approval missing. | Abort before any live preflight. | `abort_reasons` | Approval reference validation. | Design-only |
| PE-002 | Consent | Missing consent. | Abort before source validation. | `consent_status` | Consent reference required. | Design-only |
| PE-003 | Consent | Expired consent. | Abort. | `consent_status` | Expiration validation. | Design-only |
| PE-004 | Consent | Revoked consent. | Abort. | `consent_status` | Revocation validation. | Design-only |
| PE-005 | Consent | Consent source root mismatch. | Abort before source read. | `source_root_status` | Source root consistency check. | Design-only |
| PE-006 | Source kind | Source kind mismatch. | Abort. | `source_kind` | Source kind consistency check. | Design-only |
| PE-007 | Source root | Ambiguous source root. | Abort. | `source_root_status` | Ambiguity fails closed. | Design-only |
| PE-008 | Source root | Source root outside allowed scope. | Abort and deny read. | `denied_action_report` | Path-bounded scope check. | Design-only |
| PE-009 | PAI_DIR | Missing `PAI_DIR` candidate. | Abort. | `pai_dir_candidate_status` | Candidate presence check. | Design-only |
| PE-010 | PAI_DIR | Insufficient `PAI_DIR` confidence. | Abort. | `pai_dir_candidate_status` | Confidence threshold check. | Design-only |
| PE-011 | Read scope | Attempted default read of `~/.claude/PAI`. | Abort and deny read. | `denied_action_report` | No default live PAI_DIR read proof. | Design-only |
| PE-012 | Read scope | Attempted read of `~/.claude/projects`. | Abort and deny read. | `denied_action_report` | Forbidden read check. | Design-only |
| PE-013 | Read scope | Attempted read of `~/.codex`. | Abort and deny read. | `denied_action_report` | Forbidden read check. | Design-only |
| PE-014 | Product memory | Attempted product memory read. | Abort and deny read. | `product_memory_policy` | Product memory denied by default. | Design-only |
| PE-015 | Write pressure | Write pressure detected. | Abort. | `forbidden_writes` | No-write check. | Design-only |
| PE-016 | Memory | PAI Memory write pressure. | Abort. | `memory_policy` | PAI Memory write denial. | Design-only |
| PE-017 | ISA | ISA write pressure. | Abort. | `isa_policy` | ISA write denial. | Design-only |
| PE-018 | Pulse | Pulse startup pressure. | Abort. | `pulse_policy` | Pulse no-start proof. | Design-only |
| PE-019 | Pulse | Pulse endpoint call pressure. | Abort. | `pulse_policy` | Pulse no-call proof. | Design-only |
| PE-020 | Protected path | Root `AGENTS.md` write pressure. | Abort. | `forbidden_writes` | Protected-path proof. | Design-only |
| PE-021 | Protected path | `.codex/` write pressure. | Abort. | `forbidden_writes` | Protected-path proof. | Design-only |
| PE-022 | Runtime | Claude Code invocation pressure. | Abort. | `runtime_prohibitions` | No Claude Code invocation proof. | Design-only |
| PE-023 | Runtime | Codex runtime invocation pressure. | Abort. | `runtime_prohibitions` | No Codex runtime invocation proof. | Design-only |
| PE-024 | Unsupported surface | Unsupported surface would be silently ignored. | Abort or report unsupported surface. | `unsupported_surface_report` | Unsupported-surface reporting proof. | Design-only |
| PE-025 | Drop-in claim | Drop-in claim pressure. | Abort or fail validation. | `drop_in_claim_policy` | Drop-in status remains not-claimed. | Design-only |
| PE-026 | Reporting | Report output would become canonical state. | Abort report creation or fail validation. | `non_canonical_statement` | Non-canonical output proof. | Design-only |
| PE-027 | Personal clone | Personal clone access without approval. | Abort and deny access. | `denied_action_report` | Architect approval plus explicit consent required. | Design-only |
| PE-028 | Clone classification | Clean clone mistaken for live PAI install. | Abort or classify as non-live evidence only. | `source_root_status` | Clean clone is not live PAI install. | Design-only |
| PE-029 | Rollback/no-residue | Rollback/no-residue expectation missing. | Abort or fail preflight validation. | `rollback_no_residue_policy` | Rollback/no-residue boundary required. | Design-only |
| PE-030 | Retention | Retention policy missing. | Abort or fail preflight validation. | `retention_policy` | Retention policy required. | Design-only |

## Required Future Proofs

Future implementation must prove:

- Every `PE-001` through `PE-030` evidence ID has a corresponding validation check.
- Every failed evidence check aborts before live local reads.
- Abort evidence remains non-canonical.
- Abort evidence does not write PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, or `.codex/`.
- Abort evidence preserves no Pulse, no product-memory promotion, no runtime invocation, no personal-clone access without approval, and no drop-in claim boundaries.

## Prohibited Abort Evidence Designs

Prohibited designs:

- Treating abort evidence as a warning and continuing.
- Writing abort evidence to PAI Memory, ISA, Pulse, Claude memory, or Codex memory.
- Starting Pulse or invoking runtime tools to collect abort evidence.
- Reading forbidden live paths to explain aborts.
- Treating preflight abort evidence as a manifest, runtime payload, or drop-in proof.

## Non-Goals

S12D creates no preflight report, creates no preflight runner, creates no detector script, creates no consent artifact, creates no consent validator, runs no live read-only trial, reads no live existing-local-v5 state, inspects no private user-local state, inspects no personal clone, writes no PAI Memory, writes no ISA, starts no Pulse, calls no Pulse endpoints, invokes no Claude Code, invokes no Codex runtime, implements no runtime adapter, creates no root `AGENTS.md`, creates no `.codex/`, and authorizes no product-memory promotion.
