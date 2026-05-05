# V5 Codex Decoupling Decision Log

## Purpose

Record S6 decisions, non-decisions, blocked decisions, and future architect questions for the Claude coupling inventory and Codex decoupling seam design.

## Scope

This log is design-only. It records S6 architecture decisions and advisory next milestone options.

It does not authorize S7, implement a Codex adapter, create runtime files, create root `AGENTS.md`, create `.codex/`, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create migration scripts, inspect user-local state, start Pulse, run installers, or run Codex import or migration tooling.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- S0-S5 adapter docs.
- Repository-local PAI v5 release files under `Releases/v5.0.0/.claude/`.

## Decisions Made in S6

S6 decisions:

- Codex is not currently proven drop-in for existing local PAI v5 files.
- Codex remains not drop-in today.
- Decoupling requires explicit seams, not direct file copying.
- Authority must be solved before a future router is created.
- Read-only posture must precede write-capable modes.
- Pulse bridge work remains out of S6 scope.
- PAI Memory and ISA writes remain blocked.
- Root `AGENTS.md` and `.codex/` remain protected.
- No user-local private state is inspected in S6.
- No runtime release files are changed in S6.

## Non-Decisions in S6

S6 does not decide:

- Which exact Codex-native authority surface will carry PAI doctrine.
- Whether a future root `AGENTS.md` will be authorized.
- Whether PAI commands become Codex skills, MCP tools, plugin material, docs, or another native surface.
- Whether Codex will ever become the official upstream PAI engine.
- Which future single-writer mechanism will own PAI Memory, ISA, Pulse, or work-state writes.
- Whether Pulse should support a `codex`, `adapter`, or different job identity.

## Blocked Decisions

Blocked decisions:

- Drop-in readiness is blocked until gates G0-G15 pass or are explicitly waived by architect review.
- Runtime implementation is blocked because S6 creates no runtime seams.
- Existing-local-v5 trial execution is blocked until manifest, fixture/path, no-write, denied-path, and audit requirements are approved and implemented in a later milestone.
- PAI Memory and ISA writes are blocked until single-writer policy, provenance, rollback, and validation exist.
- Pulse implementation is blocked because S6 does not design or implement a Pulse bridge.

## Future Architect Questions

Questions for architect review:

- Should V5-S7 begin with authority seam and compact router design, or with fixture-only coupling validation harness design?
- What is the acceptable authority-equivalence proof for `PAI_SYSTEM_PROMPT.md`?
- Should future Codex `AGENTS.md` exist, and if so where should it live?
- Which Pulse event and job identity should represent Codex-originated activity?
- Which state surfaces require locks, leases, or human-mediated writes?
- What is the minimum safe fixture evidence before an existing-local-v5 read-only trial?
- What user-facing support language is acceptable before drop-in readiness?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S6-D01 | Codex remains not drop-in today. | Current v5 release is Claude Code-native in launcher, inference, settings, hooks, skills, agents, commands, Pulse, Memory, and ISA boundaries. | S0/S1/S2 docs; S6 coupling inventory. | Decided for S6. | All G0-G15 readiness gates pass or are architect-waived. |
| S6-D02 | Decoupling requires explicit seams, not direct file copying. | Claude-shaped files must not be copied directly into Codex surfaces. | S1 boundaries; S2 matrix; S6 seam spec. | Decided for S6. | Architect approves a transformation spec with tests. |
| S6-D03 | Authority seam must be resolved before router creation. | `PAI_SYSTEM_PROMPT.md` is high-authority doctrine and `CLAUDE.md` is not a Codex destination file. | S3 authority mapping; release authority evidence. | Decided for S6. | Authority-equivalence spec is approved. |
| S6-D04 | Read-only local trial must precede write-capable modes. | Existing local v5 files may contain live canonical state and private data. | S3/S4/S5 read-only trial specs. | Decided for S6. | Manifest, fixture/path, no-write, and audit gates pass. |
| S6-D05 | Pulse bridge remains out of S6 scope. | Pulse is central infrastructure, but S6 does not design or implement a Pulse bridge. | Pulse docs; S1/S4/S5 boundaries. | Decided for S6. | Architect approves V5-S7E or equivalent Pulse design. |
| S6-D06 | PAI Memory/ISA writes remain blocked. | PAI Memory and ISA are canonical PAI state and require single-writer control. | MemorySystem, IsaFormat, S1/S5 docs. | Decided for S6. | Single-writer, provenance, rollback, and validation are approved. |
| S6-D07 | Root `AGENTS.md` and `.codex/` remain protected governance. | Future Codex surfaces must be authorized separately and native. | S1 boundaries; S3 authority mapping; S6 contract. | Decided for S6. | Architect approves a router/config milestone with explicit write set. |
| S6-D08 | Future implementation must begin with either fixture/harness work or authority/router design, pending architect approval. | Both are prerequisite paths; S6 does not choose or authorize S7. | S4/S5 fixture and schema docs; S6 gates. | Advisory. | Architect selects an S7 milestone. |
| S6-D09 | No user-local state is inspected in S6. | Private state is explicitly protected. | S6 source protocol and validation scope. | Decided for S6. | Future live-root trial gets explicit user and privacy approval. |
| S6-D10 | No runtime release files are changed in S6. | Release files are read-only evidence and protected paths. | S6 write set and protected-path contract. | Decided for S6. | Future approved release-edit milestone, if any. |

## Next Milestone Candidates

Advisory-only options:

- `V5-S7A`: Authority seam and compact router design.
- `V5-S7B`: Fixture-only coupling validation harness design.
- `V5-S7C`: Launcher and inference seam design.
- `V5-S7D`: Hook/lifecycle mapping design.
- `V5-S7E`: Pulse bridge identity and read-only event model.

Architect approval is required before any S7 work. This document does not begin S7.

## Non-Goals

S6 does not implement decoupling, create runtime adapter seams, create root `AGENTS.md`, create `.codex/`, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create migration scripts, inspect user-local private state, start Pulse, run installers, run Codex import or migration tooling, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, claim Codex is drop-in today, claim Codex is the official upstream engine, or imply Claude-shaped files can be copied directly into Codex surfaces.
