# V5 Codex Authority Seam Spec

## Purpose

Define the future authority seam that preserves PAI v5 authority semantics inside a Codex-native runtime without copying Claude-shaped files into Codex surfaces.

## Scope

S7A designs authority and router seams only.

This document is design-only. It does not implement authority injection, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create runtime files, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, or run Codex import or migration tooling.

## Evidence Base

S7A uses these evidence sources:

- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_EQUIVALENCE_TEST_SPEC.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md`
- `Releases/v5.0.0/.claude/CLAUDE.md`

No new Codex capability claim is introduced in S7A. Codex authority, guidance, config, profile, sandbox, memory, transcript, and `AGENTS.md` facts are inherited from S2/S3 adapter docs, which cite official OpenAI Codex documentation.

## Authority Problem Statement

Codex is not currently proven drop-in for existing local PAI v5 files.

Codex replacement is plausible only through a designed adapter. The first authority problem is not file placement; it is preserving PAI authority semantics without treating Claude Code files as portable Codex runtime material.

The current PAI v5 release relies on `PAI_SYSTEM_PROMPT.md` as high-authority upstream PAI doctrine and `CLAUDE.md` as the official Claude-facing operational guidance surface. Codex has native guidance and configuration surfaces, but those surfaces are not Claude surfaces and do not by themselves prove PAI authority equivalence.

## PAI Authority Model

`PAI_SYSTEM_PROMPT.md` is high-authority upstream PAI doctrine, not ordinary markdown.

It contains constitutional rules, identity rules, output format requirements, mode architecture, verification requirements, security protocol, and context hierarchy. In the current Claude Code engine, release evidence and S3 describe it as the highest authority system prompt loaded above `CLAUDE.md`.

`CLAUDE.md` is an official Claude-facing operational guidance surface. It contains mode templates, routing tables, operational rules, `@` imports, and Claude Code-specific tool and workflow references. It is not a Codex destination file.

PAI Memory and ISA artifacts are canonical PAI state. Pulse remains central v5 infrastructure. Product memories, transcripts, SDK threads, and `/goal` state are not PAI Memory, not ISA, and not Pulse state.

## Codex Authority and Guidance Model

S7A uses the Codex authority and guidance model already captured in S2/S3:

| Codex surface | S7A treatment |
| --- | --- |
| `AGENTS.md` | Future compact router candidate only. S7A does not create it. |
| Codex config/profile | Policy/configuration for native Codex behavior, not Life OS doctrine. S7A does not create Codex config. |
| Codex memory | Local recall/product memory, not doctrine and not PAI Memory. |
| Codex transcripts and resume state | Product/session continuity, not doctrine, not ISA, and not PAI Memory. |
| Codex SDK threads | Programmatic session continuity, not canonical PAI state. |
| `/goal` state | Workflow-control state for Codex task persistence, not ISA and not PAI Memory. |
| Sandbox and approvals | Safety controls, not doctrine. |

Future Codex `AGENTS.md`, if later authorized, must be a compact router. The compact router must not clone `CLAUDE.md` and must not clone `PAI_SYSTEM_PROMPT.md`.

## Non-Equivalent Surfaces

The following surfaces are not equivalent and must not be treated as interchangeable:

| PAI or Claude surface | Codex-adapter posture |
| --- | --- |
| `PAI_SYSTEM_PROMPT.md` | Source doctrine requiring authority preservation; not copied whole into a router by S7A. |
| `CLAUDE.md` | Claude-facing operational guidance; not a Codex destination file. |
| Claude `settings.json` | Claude Code configuration; not portable Codex config. |
| Claude hooks | Claude lifecycle material; not Codex hooks without explicit future mapping. |
| Claude skills, agents, commands | Claude-shaped runtime material; not copied directly into Codex surfaces. |
| PAI Memory | Canonical PAI state; not Codex memory. |
| ISA | Canonical PAI system-of-record artifact; not Codex plan or `/goal` state. |
| Pulse | Central PAI infrastructure; not implemented or bridged in S7A. |

## Authority Seam Principles

Authority seam principles:

- Preserve PAI doctrine priority.
- Use native Codex surfaces only.
- Treat Codex config/profile as policy/config, not Life OS doctrine.
- Keep operational routing separate from doctrine.
- Keep product memories out of PAI Memory.
- Keep `/goal` state out of ISA and PAI Memory.
- Keep Pulse centrality visible without claiming Pulse parity.
- Report unsupported surfaces explicitly.
- Do not copy Claude-shaped files directly into Codex surfaces.
- Do not mutate release files.
- Remain read-only until a future approved milestone.
- Require single-writer policy, provenance, rollback, and validation before any PAI state writes.
- Keep the future authority seam reversible.

## Authority Envelope Model

An authority envelope is a future Codex-native source set and ordering contract for a trial or runtime session.

The authority envelope must preserve:

- PAI doctrine priority.
- Operational routing below doctrine.
- Explicit unsupported-surface reporting.
- No silent promotion of memory.
- No direct clone of Claude-shaped files.
- No release-file mutation.
- Read-only trial posture until later approval.
- Reversible adapter posture.

S7A does not create an authority envelope artifact. It defines the model future milestones must prove.

## Authority Source Classes

| Class | Source type | Authority role | S7A status |
| --- | --- | --- | --- |
| A0 | Architect-approved trial policy | Declares engine, mode, roots, no-write posture, and stop conditions. | Future only. |
| A1 | `PAI_SYSTEM_PROMPT.md` semantics | High-authority PAI doctrine. | Source evidence only. |
| A2 | Future compact router | Native Codex routing to doctrine and trial constraints. | Design candidate only. |
| A3 | Approved PAI release docs and adapter docs | Operational context and evidence. | Read-only evidence. |
| A4 | Future dynamic context bridge | Session-specific context lower than doctrine. | Out of S7A scope. |
| A5 | Codex memory, transcript, SDK thread, `/goal` state | Product/session continuity only. | Non-authority. |

## Authority Ordering Rules

Future authority ordering rules:

- Trial policy and stop conditions outrank convenience.
- `PAI_SYSTEM_PROMPT.md` semantics outrank operational routing.
- Future compact router text points to doctrine and cannot override doctrine.
- Dynamic context, if later authorized, is lower authority than doctrine.
- Codex memory, transcripts, SDK threads, and `/goal` state are non-authority.
- PAI Memory and ISA ownership rules outrank product memory or goal convenience.
- Unsupported mappings must be reported as unsupported, not silently approximated.

## Conflict Resolution Rules

Future conflict rules:

- If PAI doctrine conflicts with a future compact router, PAI doctrine wins.
- If PAI doctrine conflicts with Codex memory, PAI doctrine wins and Codex memory remains product memory.
- If PAI doctrine conflicts with `/goal` state, PAI doctrine wins and `/goal` remains workflow-control state.
- If ISA state conflicts with Codex plan completion, ISA remains the system of record.
- If read-only trial policy conflicts with a requested write, read-only policy wins.
- If Pulse centrality conflicts with no-bridge posture, Pulse is reported as unsupported, not treated as optional.
- If required doctrine is omitted or truncated, authority readiness fails.

## Truncation and Size Risk Model

S2/S3 identify Codex instruction discovery and size limits as an authority risk. PAI doctrine is larger and more layered than a compact project note, so S7A treats truncation as a blocker unless future validation proves the authority envelope preserves required doctrine.

Required future handling:

- Keep any router compact.
- Never rely on unbounded doctrine dumps.
- List omitted sources explicitly.
- Fail closed when required doctrine cannot be loaded or referenced reliably.
- Test that truncation cannot turn a prohibited behavior into an allowed behavior.

## Memory and Goal Non-Authority Rules

Codex memory is local recall and not doctrine.

Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.

`/goal` state is workflow-control state. It is not ISA, not PAI Memory, and not Pulse state.

Product memories must not be silently promoted into PAI Memory. Any future promotion requires explicit curation, provenance, consent, single-writer ownership, rollback, and validation.

## Pulse and ISA Boundary Rules

Pulse remains central v5 infrastructure, but S7A does not design or implement a Pulse bridge.

ISA artifacts are canonical PAI state. Codex plan completion, transcript continuity, final answers, and `/goal` completion do not create ISA acceptance.

Future writes to PAI Memory, ISA, Pulse state, or related canonical state require a single-writer policy, provenance, rollback, and validation.

## Existing Local v5 Authority Safety

Future read-only trials must not require uninstalling Claude Code.

An existing local v5 authority trial must be reversible, read-only, explicit about allowed and denied roots, and unable to mutate PAI state, release files, Claude files, Codex config, root `AGENTS.md`, `.codex/`, PAI Memory, ISA, or Pulse.

S7A does not authorize existing-local-v5 trial execution.

## Candidate Authority Seam Designs

| Candidate | Summary | Inputs | Outputs | Safety | Reversibility | Drop-in readiness | Authority loss risk | Required future proofs | S7A decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AS-1 | Compact router plus read-only doctrine references. | S3 authority mapping, `PAI_SYSTEM_PROMPT.md` evidence, compact router spec. | Future small router that references approved doctrine and trial rules. | Low write risk if no router is created until authorized; high ordering risk until tested. | Reversible if no generated files are installed and references are read-only. | Candidate prerequisite for G1/G2 only. | Medium: references can be missed, stale, or truncated. | Source ordering, size, omission, conflict, and no-copy tests. | Design candidate only; no runtime implementation chosen. |
| AS-2 | Generated authority envelope for explicit trial sessions. | Manifest/trial policy, doctrine source list, adapter docs, validation cases. | Future per-session authority envelope text or structured source set. | Stronger source control, but generation itself needs approval and quarantine. | Reversible if generated output is outside live roots and never promoted silently. | Candidate for controlled read-only validation. | Medium: generation can drift or flatten doctrine unless tested. | Proven generation rules, provenance, no-release-mutation, no-memory-promotion, and truncation tests. | Design candidate only; no runtime implementation chosen. |
| AS-3 | Future launcher/profile-mediated authority envelope. | Future launcher seam, Codex config/profile evidence, approved authority spec. | Runtime-selected authority envelope mediated by future engine selection. | Highest integration risk because it touches launch/profile policy in a later milestone. | Reversible only after launcher rollback is proven. | Candidate for later replacement-capable mode, not S7A. | High: launcher/profile mistakes can misbind live authority or state. | Launcher/profile tests, trust model, rollback, no-write proof, and G0-G15 gate progress. | Deferred; no runtime implementation chosen. |

## Required Future Proofs

Future authority work must prove:

- `PAI_SYSTEM_PROMPT.md` semantics retain high-authority priority.
- `CLAUDE.md` is not copied into Codex.
- `AGENTS.md`, if authorized, is a compact router.
- Codex config/profile is policy/configuration, not Life OS doctrine.
- Codex memory and `/goal` state are not doctrine.
- PAI Memory and ISA remain canonical PAI state.
- Pulse is not started or treated as implemented by authority design.
- Unsupported surfaces are reported explicitly.
- Read-only trial constraints block writes.
- The design is reversible and does not require uninstalling Claude Code.

## Prohibited Designs

Prohibited designs:

- Copying `PAI_SYSTEM_PROMPT.md` into root `AGENTS.md`.
- Copying `CLAUDE.md` into root `AGENTS.md`.
- Copying Claude-shaped files directly into Codex surfaces.
- Treating Codex config/profile as Life OS doctrine.
- Treating Codex memory as PAI Memory.
- Treating `/goal` completion as ISA acceptance.
- Treating transcripts or SDK threads as canonical PAI state.
- Creating root `AGENTS.md` or `.codex/` in S7A.
- Mutating release files.
- Authorizing PAI Memory writes, ISA writes, Pulse implementation, or existing-local-v5 trial execution.

## Non-Goals

S7A does not implement authority injection, implement a Codex adapter, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create runtime files, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, run Codex import or migration tooling, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, or advance beyond S7A.
