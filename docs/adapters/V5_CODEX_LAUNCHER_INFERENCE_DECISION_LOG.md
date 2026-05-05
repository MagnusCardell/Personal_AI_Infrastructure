# V5 Codex Launcher and Inference Decision Log

## Purpose

Record S7C decisions, non-decisions, blocked decisions, and future architect questions for launcher and inference seams.

## Scope

This log is design-only. It records S7C architecture decisions and advisory next milestone options.

It does not authorize S7B, S7D, S7E, S8B, S8C, runtime implementation, launcher creation, inference adapter creation, wrapper creation, engine profile instance creation, Codex config, root `AGENTS.md`, `.codex/`, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, migration scripts, release edits, Pulse startup, installer execution, Claude Code invocation, Codex runtime invocation, or Codex import or migration tooling.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_ENGINE_PROFILE_AND_CAPABILITY_CONTRACT.md`
- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts`
- `Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts`

## Decisions Made in S7C

S7C decisions:

- Codex is not currently proven drop-in for existing local PAI v5 files.
- Codex replacement is plausible only through a designed adapter.
- Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
- Launcher replacement requires an explicit engine seam.
- Inference replacement requires an explicit request envelope and response envelope.
- Future launcher must preserve authority envelope boundaries.
- Future inference must report unsupported surface gaps instead of silently emulating Claude.
- Pulse startup remains blocked in S7C.
- PAI Memory and ISA writes remain blocked.
- No engine profile instance is created in S7C.
- Runtime wrappers and generated configs remain prohibited.
- Root `AGENTS.md` and `.codex/` remain protected.
- Claude-shaped files must not be copied directly into Codex surfaces.

## Non-Decisions in S7C

S7C does not decide:

- Which launcher candidate, `LS-1`, `LS-2`, or `LS-3`, will be implemented.
- Which inference candidate, `IS-1`, `IS-2`, or `IS-3`, will be implemented.
- Which future Codex command, API, SDK, or noninteractive surface will be used for runtime invocation.
- Which engine profile schema format will be used.
- How Pulse bridge identity will work.
- Whether Codex can become the official upstream PAI engine.
- Whether any write-capable mode will ever be enabled.

## Blocked Decisions

Blocked decisions:

- Drop-in claims are blocked until launcher, inference, authority, Pulse, Memory, ISA, existing-local-v5 read-only, single-writer, and rollback proofs exist.
- Runtime launcher or wrapper creation is blocked because S7C is design-only.
- Runtime inference adapter creation is blocked because S7C is design-only.
- Engine profile instance creation is blocked because S7C defines only a capability contract.
- Pulse implementation is blocked because S7C does not design or implement a Pulse bridge.
- PAI Memory and ISA writes are blocked until single-writer policy, provenance, rollback, and validation exist.

## Future Architect Questions

Questions for architect review:

- Should the next launcher step be a manifest-mediated launcher plan or an engine profile schema proposal?
- Should the next inference step design noninteractive fixture validation or a generic engine adapter interface?
- What is the minimum acceptable exit-code and error taxonomy before fixture validation?
- What model/runtime reporting is allowed without implying model parity with Claude levels?
- What Codex sandbox or approval posture must be proven before read-only launcher validation?
- Should S7B fixture harness design precede any S8B/S8C schema work?
- Which Pulse constraints must be reflected in launcher and inference audits before S7E?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S7C-D01 | Codex remains not drop-in today. | Launcher, inference, authority, Pulse, Memory, ISA, read-only trial, single-writer, and rollback proofs remain unresolved. | S6 readiness gates; S7C specs. | Decided for S7C. | G0-G15 pass or receive explicit architect waiver. |
| S7C-D02 | Launcher replacement requires an explicit engine seam. | `pai.ts` invokes Claude Code, manages `.claude` layout, and appends PAI doctrine using Claude flags. | Release `pai.ts`; S6 coupling inventory. | Decided for S7C. | Launcher seam proof and architect approval. |
| S7C-D03 | Inference replacement requires an explicit request/response envelope. | `Inference.ts` shells out to Claude and assumes Claude models, flags, stdout/stderr, JSON parsing, auth, and timeout behavior. | Release `Inference.ts`; S6 coupling inventory. | Decided for S7C. | Inference envelope validation and fixture proof. |
| S7C-D04 | Future launcher must preserve authority envelope boundaries. | Launcher selection must not demote `PAI_SYSTEM_PROMPT.md` or clone `CLAUDE.md`. | S7A authority seam; S7C launcher seam. | Decided for S7C. | Authority envelope validation passes. |
| S7C-D05 | Future inference must report unsupported surfaces instead of silently emulating Claude. | Silent emulation would hide CLI, tool, model, and output gaps. | S7C inference seam; S6 seam spec. | Decided for S7C. | Unsupported surface reporting tests pass. |
| S7C-D06 | Pulse startup remains blocked in S7C. | Pulse is central infrastructure, but S7C does not design or implement a Pulse bridge. | S6 Pulse seam; S7C launcher/inference specs. | Decided for S7C. | Architect approves S7E or equivalent Pulse milestone. |
| S7C-D07 | PAI Memory and ISA writes remain blocked. | PAI Memory and ISA artifacts are canonical PAI state and require single-writer control before writes. | S1-S7A memory and ISA boundaries. | Decided for S7C. | Single-writer, provenance, rollback, and validation are approved. |
| S7C-D08 | No engine profile instance is created in S7C. | The engine profile contract is future declarative metadata only. | S7C engine profile contract. | Decided for S7C. | Architect approves S8B or another schema/instance milestone. |
| S7C-D09 | Runtime wrappers and generated configs remain prohibited. | S7C must not create runtime adapter material or `.codex/` config. | S7C contract and protected paths. | Decided for S7C. | Future approved implementation milestone. |
| S7C-D10 | Root `AGENTS.md` and `.codex/` remain protected. | Authority/router work remains design-only and future Codex config is not authorized. | S7A router spec; S7C contract. | Decided for S7C. | Architect approves explicit router/config write set. |
| S7C-D11 | Future drop-in claims require launcher, inference, authority, Pulse, Memory, ISA, and rollback proofs. | Drop-in must preserve runtime invocation and canonical PAI state safety. | S6 readiness gates; S7A authority; S7C seams. | Decided for S7C. | Required gates pass or are explicitly waived. |
| S7C-D12 | No user-local state is inspected in S7C. | Private user-local roots are protected; S7C uses repository-local release evidence only. | S7C source protocol and validation scope. | Decided for S7C. | Future live-root trial receives explicit approval and guards. |

## Next Milestone Candidates

Advisory-only options:

- `V5-S7B`: Fixture-only coupling validation harness design.
- `V5-S7D`: Hook/lifecycle mapping design.
- `V5-S7E`: Pulse bridge identity and read-only event model.
- `V5-S8B`: Engine profile schema proposal, if S7C is accepted.
- `V5-S8C`: Launcher/inference fixture validation design, if S7C is accepted.

Architect approval is required before any future milestone.

The architect approval is required before S7B, S7D, S7E, S8B, or S8C begins. This document does not begin S7B, S7D, S7E, S8B, or S8C.

## Non-Goals

S7C does not implement the adapter, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create migration scripts, create runtime files, create an engine profile instance, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, imply Claude-shaped files can be copied directly into Codex surfaces, propose installing any launcher, wrapper, engine profile, or inference adapter, or advance beyond S7C.
