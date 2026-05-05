# V5 Adapter Boundaries

## Purpose

This document defines the S1 boundary contract for a future Codex replacement adapter for PAI v5.0.0. It separates engine-neutral PAI concepts, Claude Code-native runtime surfaces, Codex-specific future responsibilities, adapter-owned bridge responsibilities, and prohibited behavior.

This is a design document only. It does not implement a Codex adapter and does not authorize edits outside the S1 approved write set.

## Source Position

S0 found that PAI v5.0.0 is Claude Code-native, with canonical upstream content under `Releases/v5.0.0/.claude/` and installed runtime expectations under `~/.claude/` (`docs/adapters/V5_S0_DISCOVERY_REPORT.md`, "Executive Finding").

S0 also found that some PAI concepts may be engine-neutral if their semantics are preserved:

- Algorithm doctrine and architecture docs are markdown doctrine rather than engine code (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/ARCHITECTURE_SUMMARY.md:14-45`).
- ISA is a file-shape contract and system-of-record primitive (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md:1-16`).
- PAI Memory is filesystem-based canonical state with typed directories (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:1-15`).
- Pulse exposes HTTP, event, observability, and job surfaces but is central infrastructure, not optional (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md:1-13`).

Those findings define the boundary: preserve PAI semantics first, then adapt engine behavior.

## Boundary Map

| Boundary | Owns | S1 Position | Future Adapter Responsibility |
| --- | --- | --- | --- |
| PAI doctrine | Life OS philosophy, Algorithm, ISA meaning, Memory taxonomy, high-level architecture | Evidence-only; no edits. | Preserve semantics across engine choice. |
| Authority layer | `PAI_SYSTEM_PROMPT.md`, `CLAUDE.md`, imported identity/project/system files, dynamic context | Evidence-only; no edits. | Provide Codex authority equivalence before runtime claims. |
| Canonical PAI state | `PAI/MEMORY`, ISA files, `STATE/work.json`, user identity files | No writes. | Read through fixtures first; future live writes require single writer, provenance, and rollback. |
| Pulse infrastructure | Dashboard, daemon, observability, hooks, jobs, event APIs | No startup, calls, or writes. | Bridge Codex events explicitly before parity claims. |
| Claude runtime | `~/.claude`, `settings.json`, hooks, skills, agents, commands, `pai.ts`, `Inference.ts` | Current proven v5 runtime; evidence-only. | Remain installed and recoverable; do not mutate during Codex trial by default. |
| Codex runtime | Codex config, memory, goal state, tools, lifecycle behavior | Not inspected through `.codex/` in S1. | Verify current behavior in a later approved phase before mapping. |
| Adapter bridge | Authority mapping, event mapping, state access broker, settings/security mapping, inference provider, Pulse bridge | Strategy-only in S1. | Implement only in a future authorized phase after gates pass. |
| Strategy docs | `docs/adapters/` S1 files | Approved S1 write surface. | Serve as review basis for later phases. |

## Write Policy

| Surface | S1 Read | S1 Write | Future Default | Required Gate Before Future Write |
| --- | --- | --- | --- | --- |
| `docs/adapters/V5_S1_EXEC_PLAN.md` | Yes | Yes | Documentation | S1 approved write set |
| Other S1 strategy docs | Yes | Yes | Documentation | S1 approved write set |
| `docs/adapters/V5_S0_DISCOVERY_*.md` | Yes | No | Evidence | Separate approval to edit S0 docs |
| `Releases/v5.0.0/` | Evidence reads only | No | Read-only baseline | Release-maintainer approval, not adapter trial |
| `.claude/` repo root or user-local `~/.claude/` | No user-local reads | No | Protected | Explicit future approval, fixture first |
| Live `PAI_DIR` | No | No | Protected live state | Fixture validation, single writer, rollback |
| `PAI/MEMORY` | Evidence via release docs only | No | Canonical state | Single writer, curation, provenance, rollback |
| ISA files | Evidence via release docs only | No | Canonical state | Single writer, acceptance semantics, rollback |
| `settings.json` | Evidence via release docs only | No | Runtime config | Codex security mapping and reversible generation |
| hooks, skills, agents, commands | Evidence via release docs only | No | Runtime extension surfaces | Semantic transformation design and fixture validation |
| `.codex/` and Codex memories | No | No | Separate Codex state | Explicit future bridge decision and privacy review |
| Pulse state and endpoints | No live calls | No | Central runtime infrastructure | Event bridge schema and fixture mode |

## Authority Boundary

The adapter must not lower PAI doctrine from high-authority instruction to ordinary retrieved text.

Boundary rules:

- `PAI_SYSTEM_PROMPT.md` remains doctrine, not memory.
- Codex goal state cannot override doctrine.
- Product memory cannot override doctrine.
- Operational docs cannot silently supersede doctrine.
- Dynamic context cannot be treated as equivalent to the Layer 1 authority identified by S0.

Any future adapter must identify where this authority lives in Codex and how conflicts are resolved. If no equivalent exists, replacement readiness is blocked.

## State Boundary

Canonical PAI state includes at minimum:

- `PAI/MEMORY`
- Project-root `ISA.md`
- `PAI/MEMORY/WORK/{slug}/ISA.md`
- `STATE/work.json`
- User identity and profile files
- Observability JSONL and Pulse state once live runtime writes are involved

Boundary rules:

- Read release docs as evidence; do not confuse them with live state.
- Treat `PAI_DIR` as live user-local state unless explicitly fixture-bound.
- Do not write canonical state from Codex without single-writer control.
- Do not let Claude and Codex write the same PAI state concurrently.
- Do not promote Codex memory, Claude memory, or Codex goal state into PAI Memory without explicit curation and provenance.
- Do not create parallel ISA or work-record formats.

## Runtime Boundary

Claude Code remains the only proven PAI v5.0.0 runtime at S1. Codex is a future candidate runtime behind an adapter.

Boundary rules:

- Do not replace `pai.ts` in the v5.0.0 release during S1.
- Do not copy Claude `settings.json` into Codex as proof of compatibility.
- Do not copy hooks, skills, agents, or commands into Codex without semantic transformation.
- Do not overload Pulse `type = "claude"` jobs as Codex jobs without a reviewed identity decision.
- Do not claim prompt-processing parity until context injection and classification semantics are mapped.
- Do not claim inference parity until Codex provider behavior is verified.

## Installation Boundary

A Codex replacement adapter must not depend on removing Claude Code.

Boundary rules:

- Existing `~/.claude` must remain recoverable.
- Installer overlay semantics from the Claude-native v5 release must not be reused accidentally for Codex trials.
- Future generated Codex config must be separate, reversible, and fixture-tested first.
- Rollback proof is required before any live mode.
- A failed Codex trial must leave Claude Code usable.

## Pulse Boundary

Pulse remains central infrastructure.

Boundary rules:

- S1 does not start Pulse, call `localhost:31337`, or write Pulse state.
- Future Codex activity is not Pulse-visible until a bridge emits provenance-labeled events.
- Dashboard parity requires event schema parity, not just process execution.
- Scheduled work needs an explicit Codex or adapter job identity.
- Bridge failures must be observable and must not imply successful state writes.

## Goal And Memory Boundary

Codex `/goal` is useful for bounded adapter work, but it is not PAI state.

Boundary rules:

- Goal progress may live in Codex goal metadata and approved docs.
- Goal progress does not become PAI Memory automatically.
- Goal completion does not equal ISA acceptance.
- Goal state must not be used as a hidden bridge between Codex memory and PAI Memory.
- Any future display of goals inside PAI must be read-only, provenance-labeled, and separate from canonical state until a curation path is approved.

## Prohibited Substitutions

These substitutions are explicitly invalid:

- `.claude` tree copied into `.codex` equals adapter.
- `PAI_SYSTEM_PROMPT.md` stored as ordinary memory equals authority.
- Claude hook scripts invoked without event mapping equals lifecycle support.
- Claude `settings.json` copied into Codex equals security compatibility.
- Pulse `type = "claude"` reused for Codex equals job parity.
- Codex goal completion equals ISA acceptance.
- Codex memory equals PAI Memory.
- Release tree `Releases/v5.0.0/.claude/PAI` equals live `PAI_DIR`.
- Read-only fixture success equals live-write safety.

## Future Phase Gates

These gates describe what later phases must prove. They do not authorize implementation during S1.

- Authority gate: documented Codex authority equivalence for `PAI_SYSTEM_PROMPT.md`.
- Event gate: lifecycle compatibility matrix for required Claude hook events.
- Pulse gate: event and job schema for Codex-originated activity.
- State gate: fixture root guardrails, single-writer policy, provenance, and rollback.
- Settings gate: Codex-specific permission and security mapping.
- Inference gate: Codex provider contract and failure behavior.
- Transformation gate: skills, commands, and agents semantic inventory.
- Existing-user gate: reversible setup that leaves Claude Code installed and usable.

## S1 Boundary Conclusion

The S1 boundary is intentionally narrow: document the strategy, preserve upstream evidence, and prevent premature runtime writes. A future Codex adapter may be plausible, but only as a bridge that respects PAI authority, Pulse centrality, canonical state ownership, memory separation, and existing-user rollback.
