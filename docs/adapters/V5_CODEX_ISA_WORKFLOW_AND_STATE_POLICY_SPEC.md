# V5 Codex ISA Workflow and State Policy Spec

## Purpose

Define how future Codex workflows must treat ISA as the PAI system-of-record primitive without replacing it with `/goal`, task notes, transcripts, or product memory.

## Scope

This document is design-only. It does not read private user-local ISA state, write ISA artifacts, create ISA payloads, create advisory patches, create audit artifacts, create runtime files, run a read-only trial, or implement a Codex adapter.

## Evidence Base

Evidence comes from:

- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa/IsaSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md`
- `docs/adapters/V5_CODEX_MEMORY_ISA_SINGLE_WRITER_POLICY_SPEC.md`
- `docs/adapters/V5_CODEX_GOAL_RUNBOOK.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_DECISION_LOG.md`
- `/tmp/v5-s8h-memory-isa-files.txt`
- `/tmp/v5-s8h-memory-isa-search.txt`

No private user-local ISA state was read.

## ISA Problem Statement

The ISA is the Ideal State Artifact and the v5 work/system-of-record primitive. Release docs describe it as ideal state articulation, test harness, build verification, done condition, and system of record.

Codex `/goal`, transcripts, SDK threads, product memory, task notes, and advisory output can support workflow control or evidence in future reviewed contexts, but they are not ISA and must not replace ISA.

## ISA Role Model

ISA roles:

- Articulates ideal state.
- Holds Ideal State Criteria.
- Serves as test harness.
- Records verification.
- Records decisions.
- Records changelog.
- Acts as system-of-record for the thing being pursued.

Task ISAs live under `MEMORY/WORK/{slug}/ISA.md`. Project ISAs can live at project root as long-lived system-of-record artifacts. S8H reads only repository-local release evidence.

## ISA and PRD Boundary

PRD terminology must not replace ISA terminology for v5 adapter work.

Release ISA format docs state that `PRD.md` fallback was removed and that legacy `PRD.md` files are inert. S8H therefore treats PRD as historical vocabulary only.

Future Codex docs must use ISA terminology for v5 canonical work state.

## ISA and Codex Goal Boundary

Codex `/goal` is workflow-control state, not ISA.

`/goal` completion does not create ISA acceptance, does not update ISA criteria, does not update ISA changelog, does not write PAI Memory, and does not write Pulse state.

Any future proposal to reflect `/goal` output in ISA requires advisory patch review and single-writer ownership.

## ISA and Transcript Boundary

Transcripts are not ISA.

Codex transcripts, Claude Code transcripts, SDK threads, and product memory may not be treated as ISA sections, ISA changelog, ISA verification, or ISA acceptance without future explicit approval and writer policy.

## ISA Read Policy

Future ISA read policy:

| Source class | Future read posture | S8H status |
| --- | --- | --- |
| release fixture | Read repository-local or copied release examples only. | Repository-local evidence read only. |
| sanitized user fixture | Future sanitized fixture with user and architect approval. | Not created or read in S8H. |
| existing-local-v5 read-only | Future explicit live-root approval and technical read-only enforcement. | Unauthorized in S8H. |
| controlled single-writer | Future read under ownership and write policy. | Blocked in S8H. |

S8H authorizes no ISA reads from private user-local state and no ISA writes.

## ISA Advisory Patch Policy

Future ISA advisory patch policy:

- Patch proposal only.
- No automatic application.
- Provenance required.
- Human or PAI-native writer approval required.
- Single-writer ownership required before application.
- Conflict detection required.
- Changelog preservation required.
- Verification criteria preservation required.
- Rollback required.
- Audit output required.

S8H creates no advisory ISA patch.

## ISA Write Policy

Future ISA write policy requires:

- Single-writer ownership.
- Writer role not `unknown`.
- No `dual-engine-uncoordinated` writes.
- Conflict detection.
- Changelog preservation.
- Verification criteria preservation.
- Pulse boundary handling.
- Audit output.
- Rollback.
- Validation.

S8H authorizes no ISA writes.

## ISA Changelog and Verification Policy

Future ISA writes must preserve:

- Stable ISC IDs.
- Criteria state.
- Verification evidence.
- Decisions.
- Changelog entries.
- Refined goal and criteria rationale.
- Project/task ISA distinction.
- Audit and provenance lineage.

Changelog and verification must not be reconstructed from product memory without review.

## ISA Conflict Model

ISA conflicts include:

- Stale ISA base.
- Concurrent writer.
- Unowned write.
- Criteria renumbering.
- Changelog loss.
- Verification evidence loss.
- `/goal` overpromotion.
- Transcript overpromotion.
- Pulse state confusion.
- PRD terminology replacing ISA terminology.

Any conflict must fail closed until resolved by the future approved owner.

## ISA Ownership Model

Future ownership model must identify:

- ISA path.
- ISA type: project or task.
- Writer role.
- Lock or lease.
- Allowed operation.
- Approval source.
- Conflict status.
- Rollback path.
- Audit ID.

S8H implements no ownership mechanism.

## ISA and Pulse Boundary

Pulse is central v5 infrastructure, but S8H does not design or implement a Pulse bridge.

Future ISA operations must not emit Pulse events, update Pulse state, call Pulse endpoints, start Pulse, or claim Pulse parity unless a later Pulse milestone authorizes it.

## Required Future Proofs

Future ISA work must prove:

- ISA remains the Ideal State Artifact and system-of-record primitive.
- PRD terminology does not replace ISA terminology.
- `/goal` is not ISA.
- Transcripts are not ISA.
- Product memory is not ISA.
- Reads are explicitly authorized.
- Writes have single-writer ownership.
- Changelog and verification are preserved.
- Conflicts fail closed.
- Pulse boundaries are preserved.
- Rollback is proven.

ISA operation policy table:

| ISA operation | Allowed in S8H? | Future allowed mode | Required writer | Required proof | Main hazard |
| --- | --- | --- | --- | --- | --- |
| Read release ISA examples | Yes, repository-local release evidence only. | `documentation-only` or `release-fixture-read-only`. | `no-writer` | Approved source and no-write proof. | Release examples mistaken for live state. |
| Read sanitized fixture ISA | No. | `sanitized-user-fixture-read-only`. | `no-writer` | User approval, sanitization, provenance. | Sanitization misses private state. |
| Read existing local ISA | No. | `existing-local-v5-read-only`. | `no-writer` | Manifest, user approval, technical read-only proof. | Private live state exposure. |
| Propose advisory ISA patch | No. | `assisted-patch`. | `human-approved-writer` or `pai-native-writer` for application. | Patch quarantine, provenance, review, rollback. | Proposal mistaken for applied ISA state. |
| Apply ISA patch | No. | `controlled-single-writer`. | Approved single writer. | Lock/ownership, conflict detection, changelog preservation. | Unowned write or concurrent writer. |
| Create new ISA | No. | `controlled-single-writer` or future approved fixture work. | Approved single writer. | Source approval, ownership, rollback, audit. | Shadow ISA outside canonical workflow. |
| Update ISA criteria | No. | `controlled-single-writer`. | Approved single writer. | Stable ID proof, conflict detection, verification preservation. | Criteria renumbering or test loss. |
| Update ISA changelog | No. | `controlled-single-writer`. | Approved single writer. | Changelog format proof and provenance. | Changelog drift or missing learning chain. |
| Reconcile conflicting ISA edits | No. | `controlled-single-writer`. | Approved single writer or human-approved reconciler. | Conflict report, merge proof, rollback. | Silent conflict resolution. |
| Promote /goal result into ISA | No. | Future advisory patch only. | Human-approved or PAI-native writer for application. | Goal/ISA separation proof, review, audit. | `/goal` becomes ISA. |
| Promote transcript into ISA | No. | Future advisory patch only. | Human-approved or PAI-native writer for application. | Transcript approval, summary review, provenance. | Transcript becomes canonical without curation. |
| Emit Pulse event about ISA | No. | Future Pulse bridge milestone only. | Future bridge identity, not ISA writer by default. | Pulse identity, event, audit, no-write proof. | Pulse mutation or parity overclaim. |

## Prohibited ISA Designs

Prohibited designs:

- Authorizing ISA writes in S8H.
- Reading private user-local ISA state in S8H.
- Treating `/goal` as ISA.
- Treating transcripts as ISA.
- Treating product memory as ISA.
- Treating PRD as current v5 canonical terminology.
- Applying advisory patches automatically.
- Allowing concurrent or unowned ISA writes.
- Emitting Pulse events from ISA policy in S8H.
- Creating ISA payloads, runtime files, or adapter payloads.

## Non-Goals

S8H does not write ISA artifacts, read private user-local ISA state, create ISA payloads, create advisory patches, run a trial, implement a Codex adapter, start Pulse, call Pulse endpoints, authorize existing-local-v5 trial execution, authorize product-memory promotion into ISA, claim Codex is drop-in today, or claim Codex is the official upstream engine.
