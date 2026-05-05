# V5 Codex Drop-In Readiness Gates

## Purpose

Define the gates that must pass before Codex can be described as drop-in-capable for PAI v5.

S6 does not claim the drop-in threshold is met.

## Scope

This document defines readiness gates only. It does not implement decoupling, run a read-only trial, create runtime adapter seams, create root `AGENTS.md`, create `.codex/`, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, or create migration scripts.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_MANIFEST_SCHEMA_PROPOSAL.md`
- Repository-local PAI v5 release files.

## Drop-In Definition

A future state where a user with an existing local PAI v5 installation can choose Codex as the local runtime engine for PAI workflows without uninstalling Claude Code, overwriting Claude-facing files, corrupting PAI Memory/ISA/Pulse state, or losing rollback to the official Claude Code engine.

S6 does not claim this threshold is met.

## Non-Drop-In Conditions

Codex is not currently proven drop-in for existing local PAI v5 files.

Claude-shaped files must not be copied directly into Codex surfaces.

Non-drop-in conditions include:

- Codex is claimed as the official upstream engine.
- Claude Code is removed or must be uninstalled.
- Claude-shaped files are copied directly into Codex surfaces.
- `CLAUDE.md` is cloned into `AGENTS.md`.
- `PAI_SYSTEM_PROMPT.md` high-authority doctrine is demoted.
- PAI Memory writes occur without single-writer policy.
- ISA writes or acceptance occur without writer ownership.
- Pulse implementation or Pulse parity is claimed without a bridge.
- Existing-local-v5 trial execution occurs before read-only gates.
- Rollback is unproven.

## Gate Model

Gate status values:

| Status | Meaning |
| --- | --- |
| Not started | Gate has not been designed or evaluated. |
| Designed only | S6 describes the gate, but no runtime validation exists. |
| Evidence partial | Some evidence exists, but required proof is incomplete. |
| Blocked | Gate cannot proceed until prerequisite design, approval, or test evidence exists. |
| Candidate for future implementation | Gate is scoped enough for an architect to approve a future milestone. |
| Passed | Required proof has passed. |

S6 should not mark any runtime gate as `Passed`.

## Gate G0: Scope and Boundary Integrity

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G0 | Approved write set only; protected paths unchanged; no runtime files created. | Any protected or unapproved file changed. | Designed only | Every future milestone must keep an explicit boundary check. |

## Gate G1: Authority Equivalence

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G1 | `PAI_SYSTEM_PROMPT.md` remains high-authority doctrine in a Codex-native authority envelope. | Doctrine is ordinary markdown, product memory, transcript, or hidden prompt. | Blocked | V5-S7A authority seam and compact router design. |

## Gate G2: Router Safety

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G2 | Future Codex `AGENTS.md`, if authorized, is a compact router and not a clone. | `CLAUDE.md` or Claude-shaped instructions are copied directly. | Blocked | V5-S7A compact router design after authority seam. |

## Gate G3: Launcher and Inference Replacement

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G3 | Native Codex launcher and inference provider contract preserves PAI behavior without release mutation. | `pai.ts` or `Inference.ts` Claude behavior is assumed compatible. | Evidence partial | V5-S7C launcher and inference seam design. |

## Gate G4: Settings and Permission Parity

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G4 | Native Codex settings, sandbox, approvals, rules, and denied paths preserve Claude settings security intent. | Claude `settings.json` is copied or writes are overgranted. | Evidence partial | Settings/security mapping milestone. |

## Gate G5: Hook and Lifecycle Mapping

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G5 | Claude lifecycle events, payloads, additional context, and enforcement behavior are mapped or marked unsupported. | Hooks are invoked without event and payload compatibility. | Evidence partial | V5-S7D hook/lifecycle mapping design. |

## Gate G6: Skill Mapping

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G6 | Claude-facing skill semantics are transformed into native Codex skill behavior with activation tests. | Skill directories are copied directly or activation assumptions are untested. | Evidence partial | Skill transformation design and fixture tests. |

## Gate G7: Agent and Command Mapping

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G7 | Agent roles, permissions, isolation, max-turns, and command routing are mapped natively. | Claude agent frontmatter or command files are copied directly. | Evidence partial | Agent/command transformation design. |

## Gate G8: Pulse Safety

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G8 | Pulse is not started during trials; future Codex events have explicit engine identity and no parity overclaim. | Pulse startup, endpoint calls, `type = "claude"` overload, or parity claim. | Blocked | V5-S7E Pulse bridge identity and read-only event model. |

## Gate G9: Memory Safety

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G9 | PAI Memory remains canonical PAI state; product memories are not silently promoted; writes require single-writer control. | Codex memory, Claude Code auto memory, transcripts, SDK threads, or `/goal` state treated as PAI Memory. | Blocked | Memory boundary and single-writer design. |

## Gate G10: ISA Safety

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G10 | ISA remains canonical system of record; Codex plans and goal state do not equal ISA acceptance. | Shadow acceptance artifacts or ISA writes without writer ownership. | Blocked | ISA writer policy and acceptance tests. |

## Gate G11: Existing Local v5 Read-Only Trial

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G11 | Explicit manifest, allowed reads, denied reads, denied writes, no private-state escape, no Pulse startup, advisory output only. | Live local roots are inspected or written without approval. | Blocked | Fixture/harness design followed by architect-approved read-only trial. |

## Gate G12: Single-Writer Controlled Write Mode

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G12 | Lock or lease policy, writer owner map, provenance, rollback, and validation for each PAI state surface. | Claude and Codex can both write the same canonical state surface. | Blocked | Single-writer controlled write design. |

## Gate G13: Dual-Engine Coexistence

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G13 | Claude Code and Codex coexist with visible engine labels, product memory separation, and one writer per canonical surface. | Product memories merge silently or ownership is hidden. | Designed only | Dual-engine coexistence policy and audit tests. |

## Gate G14: Rollback and Reversibility

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G14 | Failed Codex trial leaves Claude Code usable and restores generated adapter state. | No restore path, release mutation, `.claude` overwrite, or missing audit trail. | Blocked | Rollback proof milestone before live modes. |

## Gate G15: User-Facing Support Posture

| Gate | Required proof | Failure signal | Current S6 status | Future milestone needed |
| --- | --- | --- | --- | --- |
| G15 | Docs clearly state Codex candidate status, Claude fallback, no drop-in claim, and known unsupported surfaces. | User-facing docs imply official Codex support or replacement readiness. | Designed only | Support posture review after technical gates. |

## Readiness Scoring Model

Readiness scoring is gate-based, not percentage-based.

Drop-in claims are prohibited unless:

- All G0-G15 gates are either `Passed` or explicitly waived by architect review.
- No write-safety gate is unresolved.
- No Pulse/Memory/ISA safety gate is unresolved.
- Rollback has passed.
- Existing-local-v5 read-only trial has passed.
- Controlled-write validation has passed if write capability is claimed.

No S6 gate result authorizes implementation.

## Minimum Drop-In Claim Threshold

Minimum threshold:

- G0-G15 resolved as `Passed` or architect-waived.
- G1, G8, G9, G10, G11, G12, and G14 cannot be waived without explicit written risk acceptance.
- No active hard failure condition.
- Claude Code remains recoverable unless a later official upstream decision changes support posture.
- Docs state exactly what is unsupported.

S6 does not meet this threshold.

## Blockers Remaining After S6

Remaining blockers:

- Authority equivalence is not implemented or tested.
- Router is not created.
- Launcher and inference replacement are not implemented or tested.
- Settings and permission parity is not proven.
- Hook and lifecycle mapping is not proven.
- Skill, agent, and command mapping is not proven.
- Pulse bridge is not designed or implemented.
- PAI Memory and ISA writes remain blocked.
- Existing-local-v5 read-only trial has not run.
- Single-writer controlled write mode is not designed.
- Rollback proof has not passed.

## Non-Goals

S6 does not implement a Codex adapter, claim Codex is drop-in today, claim Codex is the official upstream engine, create runtime files, create root `AGENTS.md`, create `.codex/`, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create migration scripts, inspect user-local private state, start Pulse, run installers, run Codex import or migration tooling, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, or imply Claude-shaped files can be copied directly into Codex surfaces.
