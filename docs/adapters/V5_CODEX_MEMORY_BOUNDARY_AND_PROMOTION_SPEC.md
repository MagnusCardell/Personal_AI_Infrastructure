# V5 Codex Memory Boundary and Promotion Spec

## Purpose

Define the boundary between PAI Memory and product memory surfaces, and define future promotion discipline without authorizing promotion.

## Scope

This document is design-only. It does not create Memory payloads, write PAI Memory, inspect private user-local Memory, create fixtures, create audit artifacts, create runtime files, authorize promotion, or implement any adapter behavior.

## Evidence Base

Evidence comes from:

- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md`
- `Releases/v5.0.0/.claude/PAI/MEMORY/README.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa/IsaSystem.md`
- `docs/adapters/V5_CODEX_MEMORY_ISA_SINGLE_WRITER_POLICY_SPEC.md`
- `docs/adapters/V5_CODEX_GOAL_RUNBOOK.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_DECISION_LOG.md`
- `/tmp/v5-s8h-memory-isa-files.txt`
- `/tmp/v5-s8h-memory-isa-search.txt`

No private user-local Memory was read.

## Memory Boundary Problem Statement

Codex is not currently proven drop-in for existing local PAI v5 files.

The release Memory docs describe PAI Memory as broad, persistent, structured state. They also describe Claude Code auto memory and transcripts as adjacent product surfaces. S8H must keep these boundaries crisp because product memories can be useful evidence but are not canonical PAI Memory.

Product memories must not be silently promoted into PAI Memory.

## PAI Memory Model

PAI Memory categories relevant to S8H:

| PAI Memory category | Release role | S8H policy |
| --- | --- | --- |
| `WORK` | Primary work tracking, including task ISAs under `MEMORY/WORK/{slug}/ISA.md`. | Canonical PAI state; no S8H writes. |
| `LEARNING` | Learnings, failures, signals, reflections, and synthesis. | Canonical PAI state; no S8H writes. |
| `KNOWLEDGE` | Curated entity-based archive and retrieval source. | Canonical PAI state; no S8H writes. |

The broader release tree also includes state, research, security, bookmarks, raw, reference, relationship, skills, verification, and other directories. S8H focuses policy on `WORK`, `LEARNING`, and `KNOWLEDGE` because they are central to work, learning, and promotion decisions.

## Product Memory Model

Product memory surfaces:

- Claude Code auto memory.
- Codex memory.
- Codex transcripts.
- SDK threads.
- `/goal` state.

These surfaces are not PAI Memory. They are not ISA. They are not Pulse state. They may be evidence sources only after explicit future user approval and architect approval.

## Non-Memory State Surfaces

Non-memory PAI state surfaces:

- ISA artifacts.
- Pulse events/state.
- audit reports.
- advisory findings.

These surfaces must not be collapsed into PAI Memory. Audit reports and advisory findings are governance output, not PAI Memory. Pulse events/state are central runtime infrastructure, not Memory promotion targets in S8H. ISA artifacts are canonical work/system-of-record state, not product memory.

## Boundary Rules

Boundary rules:

- PAI Memory is canonical PAI state.
- Product memory is non-PAI state.
- ISA is canonical work/system-of-record state and is not product memory.
- `/goal` state is workflow-control state and not PAI Memory.
- Transcripts are not PAI Memory.
- SDK threads are not PAI Memory.
- Audit output is not PAI Memory.
- Advisory patches are not PAI Memory.
- Pulse events are not PAI Memory.
- No product memory may be promoted silently.
- No S8H document authorizes promotion.

## Promotion Philosophy

Promotion is a future reviewed act, not an automatic pipeline.

Any future promotion must be:

- opt-in;
- provenance-tagged;
- human-reviewable;
- reversible;
- deduplicated;
- conflict-checked;
- consistent with PAI Memory category semantics.

Promotion requires explicit future user approval and architect approval before any product memory may be used as evidence.

## WORK Promotion Policy

`WORK` is for discrete work tracking and task artifacts.

Future promotion into `WORK` requires:

- A concrete work unit.
- ISA relationship or work state relationship.
- Human or PAI-native writer approval.
- No automatic import from product memory.
- No `/goal` to ISA conversion without review.
- Single-writer ownership.
- Rollback.

S8H authorizes no `WORK` writes.

## LEARNING Promotion Policy

`LEARNING` is for learnings, failures, ratings, reflections, and synthesis.

Future promotion into `LEARNING` requires:

- Clear learning category.
- Evidence source.
- Provenance.
- Human-reviewable summary.
- Conflict and duplication check.
- No raw transcript dump unless explicitly approved.
- No silent import from Codex memory or Claude Code auto memory.

S8H authorizes no `LEARNING` writes.

## KNOWLEDGE Promotion Policy

`KNOWLEDGE` is for curated entity-based knowledge.

Future promotion into `KNOWLEDGE` requires:

- Entity category fit.
- Schema fit.
- Source attribution.
- Deduplication.
- Validity or uncertainty notes when needed.
- Human or PAI-native approval.
- No automatic promotion from product memory.

S8H authorizes no `KNOWLEDGE` writes.

## Product Memory Non-Promotion Rule

Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.

Product memories must not be silently promoted into PAI Memory.

Product memory may not override `PAI_SYSTEM_PROMPT.md`, ISA, PAI Memory, Pulse policy, or protected-path policy.

## Provenance and Attribution Requirements

Future promotion provenance must include:

- Source surface.
- Source owner or engine.
- Human approval record.
- Architect approval record.
- Target PAI Memory category.
- Summary of transformation.
- Conflict check result.
- Deduplication result.
- Rollback path.
- Audit ID.

## Review and Approval Requirements

Future promotion requires:

- User approval to inspect source product memory.
- Architect approval for the promotion path.
- Human-reviewable proposed content.
- Single-writer policy for the target.
- Category-specific validation.
- Rollback statement.
- Audit output.

S8H grants none of these approvals.

## Conflict and Duplication Risks

Risks:

- Duplicate Memory entries.
- Category mismatch between `WORK`, `LEARNING`, and `KNOWLEDGE`.
- Product memory leak into canonical state.
- Stale transcript facts.
- `/goal` state mistaken for ISA.
- Audit output mistaken for Memory.
- Pulse events mistaken for Memory.
- Missing provenance.
- Irreversible promotion.

## Required Future Proofs

Future promotion work must prove:

- Source inspection was approved.
- Target category is correct.
- Promotion is opt-in.
- Promotion is provenance-tagged.
- Promotion is human-reviewable.
- Promotion is reversible.
- Promotion is deduplicated.
- Promotion is conflict-checked.
- Promotion respects PAI Memory category semantics.
- No product-memory promotion occurs silently.

## Prohibited Promotion Designs

Prohibited designs:

- Authorizing promotion in S8H.
- Auto-promoting Codex memory into PAI Memory.
- Auto-promoting Claude Code auto memory into PAI Memory.
- Treating Codex transcripts as PAI Memory.
- Treating SDK threads as PAI Memory.
- Treating `/goal` state as PAI Memory.
- Treating audit reports or advisory findings as PAI Memory.
- Treating Pulse events as PAI Memory.
- Promoting without provenance, review, conflict checks, deduplication, rollback, or single-writer ownership.

Promotion source policy table:

| Source surface | Target PAI Memory category | Promotion allowed in S8H? | Future approval required | Main hazard | Required future proof |
| --- | --- | --- | --- | --- | --- |
| Claude Code auto memory | `WORK`, `LEARNING`, or `KNOWLEDGE` only by reviewed category fit. | No. | User and architect approval. | Claude product memory mistaken for canonical PAI Memory. | Source approval, category fit, provenance, deduplication, rollback. |
| Codex memory | `WORK`, `LEARNING`, or `KNOWLEDGE` only by reviewed category fit. | No. | User and architect approval. | Codex memory overrules PAI doctrine or becomes hidden canonical state. | Non-authority proof, provenance, conflict check, rollback. |
| Codex transcript | Usually `LEARNING` or `WORK` only after review. | No. | User and architect approval. | Raw session continuity becomes Memory without curation. | Transcript approval, summary review, PII review, rollback. |
| SDK thread | Usually none; possible evidence only after review. | No. | User and architect approval. | Programmatic thread treated as PAI state. | Source approval, non-memory classification, audit. |
| `/goal state` | Usually none; possible `WORK` note only after review. | No. | Architect and human approval. | `/goal` becomes ISA or PAI Memory. | Goal/ISA separation proof and no automatic promotion. |
| audit report | None by default; possible governance reference after review. | No. | Architect approval. | Audit output becomes canonical Memory. | Non-promotion statement and approved governance path. |
| advisory patch proposal | `WORK` only if separately accepted by a writer. | No. | Human or PAI-native writer approval. | Proposal is treated as applied state. | Patch acceptance proof and rollback. |
| Pulse event | None by default; possible `LEARNING` after approved bridge review. | No. | Architect approval plus Pulse policy. | Pulse runtime event becomes Memory without consent. | Bridge identity, event audit, non-promotion proof. |
| ISA changelog entry | `WORK` or ISA-owned state only through ISA writer policy. | No. | Single-writer approval. | Changelog duplicated or detached from ISA. | ISA ownership, changelog preservation, conflict check. |
| human-authored note | `WORK`, `LEARNING`, or `KNOWLEDGE` by reviewed category fit. | No. | Human approval and category review. | Unstructured note misfiled or duplicated. | Attribution, category fit, deduplication, rollback. |

## Non-Goals

S8H does not write PAI Memory, create promotion tooling, create Memory payloads, inspect private user-local Memory, inspect product memory, authorize product-memory promotion, create audit artifacts, create runtime files, run a trial, claim Codex is drop-in today, or claim Codex is the official upstream engine.
