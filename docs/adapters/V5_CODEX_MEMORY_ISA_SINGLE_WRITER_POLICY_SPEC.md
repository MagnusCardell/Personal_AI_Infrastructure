# V5 Codex Memory and ISA Single-Writer Policy Spec

## Purpose

Define the future single-writer policy required before Codex can write any canonical PAI Memory or ISA state.

## Scope

This document is design-only. S8H designs Memory and ISA single-writer policy only.

S8H does not implement Memory or ISA writes, read private user-local Memory or ISA state, create runtime policy files, create adapter payloads, create Memory payloads, create ISA payloads, create Pulse payloads, run a read-only trial, create root `AGENTS.md`, create `.codex/`, or modify release files.

S8H authorizes only `documentation-only` status.

## Evidence Base

Evidence comes from:

- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa/IsaSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md`
- `Releases/v5.0.0/.claude/PAI/MEMORY/README.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_DECISION_LOG.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `/tmp/v5-s8h-memory-isa-files.txt`
- `/tmp/v5-s8h-memory-isa-search.txt`

No new Codex capability claim is introduced in S8H. Codex memory, Codex config/profile, Codex hooks, Codex rules, and `AGENTS.md` facts are inherited from prior official-source adapter evidence.

## Single-Writer Problem Statement

Codex is not currently proven drop-in for existing local PAI v5 files.

Codex replacement is plausible only through a designed adapter. The highest-risk state boundary is canonical PAI state: PAI Memory and ISA artifacts. The release Memory docs describe a hook-driven, file-system-based memory substrate; ISA docs describe the Ideal State Artifact as the system-of-record primitive for work and projects.

Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists. Future Codex participation in canonical state workflows requires single-writer ownership, provenance, rollback, validation, and conflict handling before any write can exist.

## Canonical PAI State Model

PAI Memory and ISA artifacts are canonical PAI state.

Canonical state classes:

| State class | Release evidence | S8H policy |
| --- | --- | --- |
| PAI Memory `WORK` | `MEMORY/WORK/{slug}/ISA.md` and work tracking docs. | Canonical work state; no S8H writes. |
| PAI Memory `LEARNING` | Learnings, ratings, synthesis, failures, and harvest outputs. | Canonical learning state; no S8H writes. |
| PAI Memory `KNOWLEDGE` | Curated entity-based archive and retrieval source. | Canonical curated knowledge; no S8H writes. |
| ISA artifacts | Project ISAs and task ISAs. | Canonical system-of-record state; no S8H writes. |
| Pulse-derived state | Work/state rendering, observability, and events. | Central v5 infrastructure; out of S8H bridge scope. |

Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are non-PAI state. They are not PAI Memory, not ISA, and not Pulse state.

## Writer Role Model

Writer roles:

| Writer role | Meaning | S8H status |
| --- | --- | --- |
| `no-writer` | No canonical write authority exists. | Required for S8H. |
| `human-approved-writer` | Human-approved future writer applies reviewed changes. | Future only. |
| `pai-native-writer` | Existing PAI mechanism writes canonical state. | Release evidence only; not invoked. |
| `claude-code-writer` | Current Claude Code-native workflow writes canonical state. | Current upstream reality; not invoked. |
| `codex-adapter-writer` | Future Codex adapter writes canonical state under policy. | Blocked until proof. |
| `dual-engine-uncoordinated` | Multiple engines can write without ownership. | Prohibited. |
| `unknown` | Writer cannot be identified. | Prohibited for canonical writes. |

No canonical write may proceed with `dual-engine-uncoordinated` or `unknown` writer status.

## Adapter Mode Write Policy

Adapter modes:

- `documentation-only`
- `release-fixture-read-only`
- `sanitized-user-fixture-read-only`
- `existing-local-v5-read-only`
- `assisted-patch`
- `controlled-single-writer`
- `codex-only-replacement`
- `dual-engine-coexistence`

S8H authorizes only `documentation-only`. Other modes are future design labels, not permissions.

| Mode | Allowed PAI Memory reads | Allowed PAI Memory writes | Allowed ISA reads | Allowed ISA writes | Required writer | Required proof | S8H status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `documentation-only` | Repository-local release evidence and adapter docs only. | No. | Repository-local release evidence and adapter docs only. | No. | `no-writer` | Approved write set and protected-path proof. | Active S8H status. |
| `release-fixture-read-only` | Future copied release fixture only. | No. | Future copied release fixture only. | No. | `no-writer` | Fixture integrity, read-only mount, no-write proof. | Future only. |
| `sanitized-user-fixture-read-only` | Future sanitized fixture only. | No. | Future sanitized fixture only. | No. | `no-writer` | User approval, sanitization, provenance, no-write proof. | Future only. |
| `existing-local-v5-read-only` | Future explicitly approved live roots only. | No. | Future explicitly approved live roots only. | No. | `no-writer` | Manifest, private-state approval, read-only proof, rollback. | Future only; not authorized in S8H. |
| `assisted-patch` | Future approved sources only. | No direct write; advisory patch proposal only. | Future approved sources only. | No direct write; advisory patch proposal only. | `human-approved-writer` or `pai-native-writer` for application. | Patch quarantine, human/PAI approval, provenance, rollback. | Future only. |
| `controlled-single-writer` | Future approved sources only. | Future possible only after proof. | Future approved sources only. | Future possible only after proof. | Exactly one approved writer, never `dual-engine-uncoordinated`. | Lock/ownership, provenance, rollback, conflict handling, audit. | Future blocked. |
| `codex-only-replacement` | Future approved sources only. | Future possible only after all replacement gates pass. | Future approved sources only. | Future possible only after all replacement gates pass. | `codex-adapter-writer` only after proof. | Authority, launcher, inference, hooks, Pulse, Memory, ISA, rollback, audit gates. | Future blocked. |
| `dual-engine-coexistence` | Future approved sources only. | Only surfaces explicitly owned by one writer. | Future approved sources only. | Only surfaces explicitly owned by one writer. | Surface-specific single writer. | Engine labels, ownership map, conflict tests, rollback. | Future blocked. |

## Read-Only Mode Policy

All read-only modes allow no Memory writes and no ISA writes.

Read-only policy requires:

- Explicit source kind.
- Explicit allowed reads.
- Explicit denied reads.
- Explicit denied writes.
- No private user-local Memory or ISA reads unless future manifest and user approval allow them.
- No PAI Memory writes.
- No ISA writes.
- No Pulse startup or endpoint calls.
- No product-memory promotion.
- `denied_action_report` for any requested write.

## Assisted Patch Mode Policy

`assisted-patch` may propose advisory patches only in future approved work. It must not apply patches automatically.

Future assisted patch constraints:

- Patch proposal only.
- No direct write to PAI Memory.
- No direct write to ISA.
- Human or PAI-native writer approval required before any application.
- Provenance required.
- Conflict check required.
- Rollback plan required.
- Audit output required.

S8H creates no advisory patch proposal.

## Controlled Single-Writer Mode Policy

`controlled-single-writer` requires explicit future proof of:

- Lock or lease ownership.
- Writer identity.
- Surface ownership.
- PAI Memory category ownership.
- ISA ownership.
- Provenance.
- Rollback.
- Conflict handling.
- Audit.
- Pulse boundary handling.
- Validation before and after write.

Controlled write mode must not exist until Memory, ISA, Pulse, authority, launcher/inference, hooks/lifecycle, rollback, and audit gates pass.

## Codex-Only Replacement Mode Policy

`codex-only-replacement` is future-only and blocked in S8H.

It cannot be considered until:

- Codex is replacement-grade validated.
- Claude Code fallback and rollback policy are resolved.
- PAI Memory and ISA single-writer ownership is proven.
- Pulse bridge and event boundaries are proven or explicitly waived.
- No product-memory promotion occurs silently.
- User-facing support posture is approved.

## Dual-Engine Coexistence Policy

Dual-engine coexistence is allowed only as a future controlled mode with surface-specific single-writer ownership.

`dual-engine-uncoordinated` is prohibited.

Future dual-engine coexistence requires:

- Explicit engine labels.
- Separate product memory boundaries.
- No silent product-memory merge.
- Surface ownership map.
- Conflict detection.
- Rollback plan.
- Audit report.

## Lock and Ownership Model

Future lock and ownership model must define:

| Requirement | Purpose |
| --- | --- |
| Owner identity | Names the only writer for a canonical surface. |
| Surface scope | Identifies exact PAI Memory category, ISA file, or derived state target. |
| Lock/lease duration | Prevents concurrent write ambiguity. |
| Acquisition proof | Shows how writer obtained authority. |
| Release proof | Shows how writer released authority. |
| Conflict fallback | Defines behavior if lock cannot be obtained. |
| Audit reference | Links every write decision to provenance. |

No lock model is implemented in S8H.

## Provenance Requirements

Future canonical writes require provenance that includes:

- Engine identity.
- Writer role.
- Adapter mode.
- Source kind.
- Human or PAI-native approval.
- Input sources.
- Product memory use status.
- Conflict status.
- Rollback reference.
- Audit ID.
- Timestamp.

Product memories must not be silently promoted into PAI Memory.

## Rollback Requirements

Future rollback requirements:

- Pre-write snapshot or reversible patch.
- Writer identity.
- Affected files.
- Affected Memory category.
- Affected ISA IDs or sections.
- Changelog preservation.
- Failure recovery path.
- Human-readable rollback statement.
- Audit reference.

Rollback must be proven before any write-capable mode.

## Pulse Boundary Requirements

Pulse is central v5 infrastructure, but S8H does not design or implement a Pulse bridge.

Future Memory or ISA writes must not emit Pulse events, update Pulse state, call `localhost:31337`, start Pulse, or claim Pulse parity unless a later Pulse milestone approves the bridge identity, event model, audit model, and rollback path.

## Failure and Stop Conditions

Stop future Memory/ISA write work if:

- Writer identity is unknown.
- More than one writer can write the same surface.
- Lock or ownership cannot be proven.
- Provenance is missing.
- Rollback is missing.
- Conflict status is unknown.
- Product memory would be promoted silently.
- Pulse startup or endpoint calls are required without approval.
- Claude-shaped files would be copied directly into Codex surfaces.

## Required Future Proofs

Future write-capable work must prove:

- PAI Memory and ISA canonicality is preserved.
- `single-writer` ownership exists for each surface.
- `dual-engine-uncoordinated` writes are impossible.
- Product memories are not PAI Memory.
- `/goal` is not ISA.
- Read-only modes cannot write.
- Assisted patches cannot self-apply.
- Controlled writes have provenance, rollback, validation, audit, and conflict handling.
- Pulse boundaries are preserved.

## Prohibited Write Policies

Prohibited policies:

- Authorizing PAI Memory writes in S8H.
- Authorizing ISA writes in S8H.
- Authorizing product-memory promotion into PAI Memory.
- Allowing `dual-engine-uncoordinated` writes.
- Treating Codex memory as PAI Memory.
- Treating Claude Code auto memory as PAI Memory.
- Treating transcripts, SDK threads, or `/goal` state as canonical PAI state.
- Writing Pulse state from Memory/ISA policy.
- Creating runtime policy files, Memory payloads, ISA payloads, or adapter payloads.

## Non-Goals

S8H does not implement a Codex adapter, write PAI Memory, write ISA artifacts, read private user-local Memory or ISA state, create root `AGENTS.md`, create `.codex/`, create runtime files, create audit artifacts, create fixtures, create manifests, create Memory payloads, create ISA payloads, start Pulse, call Pulse endpoints, authorize existing-local-v5 trial execution, authorize product-memory promotion, authorize dual-engine uncoordinated writes, claim Codex is drop-in today, or claim Codex is the official upstream engine.
