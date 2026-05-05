# V5 Codex Authority Router Decision Log

## Purpose

Record S7A decisions, non-decisions, blocked decisions, and future architect questions for the authority seam and compact router.

## Scope

This log is design-only. It records S7A decisions and advisory next milestone options.

It does not authorize S7B, S7C, S7D, S7E, S8, runtime implementation, root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, runtime files, read-only trial execution, private user-local state inspection, release modification, Pulse startup, installer execution, or Codex import or migration tooling.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_COMPACT_ROUTER_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_ENVELOPE_VALIDATION_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md`
- `Releases/v5.0.0/.claude/CLAUDE.md`

## Decisions Made in S7A

S7A decisions:

- Codex is not currently proven drop-in for existing local PAI v5 files.
- Codex replacement is plausible only through a designed adapter.
- Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
- Authority seam must precede any router file creation.
- Future router must be compact and must not clone `CLAUDE.md`.
- Future router must not clone `PAI_SYSTEM_PROMPT.md`.
- `PAI_SYSTEM_PROMPT.md` must remain high-authority doctrine.
- `CLAUDE.md` remains an official Claude-facing surface, not a Codex destination file.
- Codex config/profile is policy/configuration, not Life OS doctrine.
- Codex memory is not doctrine and not PAI Memory.
- `/goal` state is not ISA and not PAI Memory.
- PAI Memory and ISA writes remain blocked.
- Pulse bridge remains out of S7A scope.
- Root `AGENTS.md` remains protected in S7A.
- `.codex/` remains protected in S7A.
- S7A creates no runtime authority material.

## Non-Decisions in S7A

S7A does not decide:

- Whether root `AGENTS.md` will ever be authorized.
- Whether nested adapter-local guidance will be authorized.
- Whether launcher-mediated instructions will be used.
- Which final authority seam candidate, `AS-1`, `AS-2`, or `AS-3`, will be implemented.
- Which Codex config/profile layout, if any, will exist in a future milestone.
- How Pulse bridge identity will work.
- When PAI Memory or ISA writes may be enabled.
- Whether Codex can become the official upstream PAI engine.

## Blocked Decisions

Blocked decisions:

- Router file creation is blocked until authority seam validation and architect approval.
- Existing-local-v5 trial execution is blocked until future validation, manifest, path, audit, and no-write gates are approved.
- PAI Memory and ISA writes are blocked until single-writer policy, provenance, rollback, and validation exist.
- Pulse implementation is blocked because S7A does not design or implement a Pulse bridge.
- Drop-in claims are blocked until the S6 G0-G15 readiness gates pass or are explicitly waived by architect review.

## Future Architect Questions

Questions for architect review:

- Should a future router live at root `AGENTS.md`, nested adapter-local guidance, launcher-mediated instructions, or no-router mode?
- Which authority seam candidate should proceed first: `AS-1`, `AS-2`, or `AS-3`?
- What minimum evidence proves `PAI_SYSTEM_PROMPT.md` high-authority semantics in Codex?
- What size budget should govern a future compact router?
- What should count as unacceptable router drift from compact reference into doctrine clone?
- Should authority validation occur before fixture-only harness design or alongside it?
- Which S7B/S7C/S7D/S7E path should follow S7A?

## Decision Table

| Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger |
| --- | --- | --- | --- | --- | --- |
| S7A-D01 | Codex remains not drop-in today. | Authority equivalence, router safety, launcher, inference, settings, hooks, Pulse, Memory, ISA, read-only trial, single-writer, and rollback gates remain unresolved. | S6 readiness gates; S7A authority spec. | Decided for S7A. | G0-G15 pass or receive explicit architect waiver. |
| S7A-D02 | Authority seam must precede any router file creation. | Router safety depends on preserving `PAI_SYSTEM_PROMPT.md` priority before any Codex guidance file exists. | S3 authority mapping; S6 seam dependency graph. | Decided for S7A. | Authority envelope validation is approved. |
| S7A-D03 | Future router must be compact and must not clone `CLAUDE.md`. | `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file. | S3 authority mapping; S7A compact router spec. | Decided for S7A. | Architect approves a router fixture or runtime guidance milestone. |
| S7A-D04 | `PAI_SYSTEM_PROMPT.md` must remain high-authority doctrine. | It carries constitutional PAI rules and current release authority semantics. | Release system prompt; S3 authority mapping. | Decided for S7A. | Authority validation proves an equivalent native envelope. |
| S7A-D05 | Codex memory is not doctrine and not PAI Memory. | Product memory is local recall and cannot silently become canonical PAI state. | S2 native evidence; S3/S4 memory boundary specs. | Decided for S7A. | Future curation and single-writer policy is approved. |
| S7A-D06 | `/goal` state is not ISA and not PAI Memory. | Goal state is workflow-control metadata, not canonical PAI state or acceptance. | S1 goal runbook; S4 authority-equivalence tests. | Decided for S7A. | Future bridge spec explicitly maps goal state with provenance. |
| S7A-D07 | Root `AGENTS.md` remains protected in S7A. | S7A designs a compact router but creates no router file. | S7A contract; compact router spec. | Decided for S7A. | Architect authorizes a future router write set. |
| S7A-D08 | `.codex/` remains protected in S7A. | S7A creates no Codex config, rules, hooks, or project-local Codex material. | S7A contract; protected-path validation. | Decided for S7A. | Architect authorizes future Codex config or project guidance work. |
| S7A-D09 | S7A creates no runtime authority material. | The milestone is design-only and must not install a router skeleton or authority envelope. | S7A scope and non-goals. | Decided for S7A. | Future implementation milestone is approved. |
| S7A-D10 | Future authority validation must pass before read-only trial execution. | Copying files does not prove authority equivalence, and live local v5 exposure requires no-write proof. | S4 authority test spec; S7A validation spec. | Decided for S7A. | Validation cases pass with audit evidence. |
| S7A-D11 | Pulse bridge remains out of S7A scope. | Pulse is central v5 infrastructure, but S7A handles authority/router only. | S6 Pulse seam; S7A authority spec. | Decided for S7A. | Architect approves V5-S7E or equivalent Pulse bridge design. |
| S7A-D12 | PAI Memory/ISA writes remain blocked. | PAI Memory and ISA are canonical PAI state and require single-writer policy before writes. | S1/S4/S5/S6 memory and ISA specs. | Decided for S7A. | Single-writer, provenance, rollback, and validation are approved. |

## Next Milestone Candidates

Advisory-only options:

- `V5-S7B`: Fixture-only coupling validation harness design.
- `V5-S7C`: Launcher and inference seam design.
- `V5-S7D`: Hook/lifecycle mapping design.
- `V5-S7E`: Pulse bridge identity and read-only event model.
- `V5-S8A`: First non-runtime router fixture proposal, if authority validation design is accepted.

Architect approval is required before any future milestone. This decision log does not begin S7B, S7C, S7D, S7E, or S8.

## Non-Goals

S7A does not implement the adapter, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create runtime files, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, run Codex import or migration tooling, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, imply Claude-shaped files can be copied directly into Codex surfaces, propose installing the non-executable router skeleton, or advance beyond S7A.
