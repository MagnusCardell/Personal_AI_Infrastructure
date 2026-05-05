# V5 Adapter Boundaries

## Purpose

This document defines the S1 boundary contract for a future Codex replacement adapter for PAI v5.0.0. It separates engine-neutral PAI concepts, Claude Code-native runtime surfaces, Codex-specific future responsibilities, adapter-owned bridge responsibilities, and prohibited behavior.

This is a design document only. It does not implement a Codex adapter and does not authorize edits outside the S1 approved write set.

## Boundary Model

The boundary model separates six areas:

| Area | Description | S1R Status |
| --- | --- | --- |
| Upstream PAI runtime payload | The v5.0.0 release payload under `Releases/v5.0.0/.claude/`. | Read-only evidence. |
| Official Claude Code engine surface | The current full-support runtime engine and Claude-shaped files. | Proven upstream engine. |
| Codex replacement-candidate engine surface | Future native Codex material needed for replacement-capable beta use. | Not created in S1R. |
| Repo-maintainer governance | Repository decisions, docs, review gates, and architecture policy. | Documentation only. |
| Documentation-only adapter area | `docs/adapters/` strategy files. | Approved S1R write area. |
| User-local state | `~/.claude/`, `~/.claude/PAI/`, `~/.codex/`, memories, credentials, runtime files. | Not inspected or modified. |

## Upstream PAI Runtime Payload

The upstream PAI runtime payload is the v5.0.0 release content discovered in S0.

It includes:

- `Releases/v5.0.0/.claude/CLAUDE.md`
- `Releases/v5.0.0/.claude/settings.json`
- `Releases/v5.0.0/.claude/hooks/`
- `Releases/v5.0.0/.claude/skills/`
- `Releases/v5.0.0/.claude/agents/`
- `Releases/v5.0.0/.claude/commands/`
- `Releases/v5.0.0/.claude/PAI/`
- `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md`
- `Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts`
- `Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts`
- `Releases/v5.0.0/.claude/PAI/PULSE/`
- `Releases/v5.0.0/.claude/PAI/MEMORY/`

S1R treats this payload as read-only evidence.

## Official Claude Code Engine Surface

The official Claude Code engine surface is the current upstream-supported runtime for PAI v5.0.0.

It includes Claude Code launcher behavior, Claude Code settings schema, Claude Code hook events, Claude Code skills, Claude Code agents, Claude Code commands, Claude Code auto memory, project transcripts, and Claude-specific inference assumptions.

Claude Code remains the current official/full-support upstream engine for v5.0.0 until replacement-grade validation exists.

## Codex Replacement-Candidate Engine Surface

The Codex replacement-candidate engine surface is future native Codex material required for a replacement-capable beta local engine.

It may eventually include Codex-native instruction routing, config, hooks, rules, skills, subagents, agents, commands, sandbox controls, permission controls, launch behavior, provenance, and Pulse bridge configuration.

S1R creates none of these surfaces.

Codex native surfaces are not Claude surfaces.

## Repo-Maintainer Governance

Repo-maintainer governance owns architecture decisions, adapter phase approval, review gates, documentation policy, release policy, protected path policy, safety requirements, and rollback requirements.

Governance docs define future adapter expectations. They do not create runtime behavior.

Replacement does not turn PAI into an OpenAI project.

## Documentation-Only Adapter Area

The documentation-only adapter area is `docs/adapters/`.

S1R may modify only:

- `docs/adapters/V5_S1_EXEC_PLAN.md`
- `docs/adapters/V5_UPSTREAM_RISK_REGISTER.md`
- `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
- `docs/adapters/V5_CODEX_GOAL_RUNBOOK.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`

This area can describe strategy, risks, boundaries, runbooks, and review gates. It cannot implement the adapter.

## User-Local State

User-local state includes:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`

S1R must not inspect or modify user-local state.

Future adapter work must treat user-local state as private, live, and potentially canonical. Read-only trial mode must be designed before existing local v5 files are inspected by Codex.

## Memory Boundary Model

Memory and state boundaries:

| Surface | Canonical PAI State | Owner | Boundary Rule |
| --- | --- | --- | --- |
| PAI Memory | Yes | PAI | Writes require single-writer policy, provenance, and rollback. |
| ISA artifacts | Yes | PAI | Goal completion does not equal ISA acceptance. |
| Pulse state | Runtime-canonical when live | PAI runtime | Codex requires a bridge before parity. |
| Claude Code memory | No | Claude Code | Not PAI Memory. |
| Codex memory | No | Codex | Not PAI Memory. |
| Codex `/goal` state | No | Codex | Not PAI Memory, not ISA, not Pulse state. |
| Future Codex adapter config | No by default | Adapter | Must be native, reversible, and separate. |
| Repo governance files | No runtime state | Maintainers | Policy only. |

Product memories must not be silently promoted into PAI Memory.

## Native Surface Rule

Codex native surfaces are not Claude surfaces.

Claude-shaped files must not be copied directly into Codex.

If a future Codex `AGENTS.md` is authorized, it must be a compact router, not a clone of `CLAUDE.md`.

Codex hooks, rules, config, skills, subagents, agents, and commands must be designed as native Codex material.

## Transformation Rule

Behavior-preserving transformation requires an explicit adapter spec and tests.

Transformation must define:

- Source Claude surface.
- Target Codex native surface.
- Preserved behavior.
- Changed behavior.
- Unsupported behavior.
- Security implications.
- State implications.
- Test evidence.
- Rollback behavior.

No direct file copy is a valid transformation proof.

## Read/Write Policy

Read/write policy:

| Surface | S1R Read | S1R Write | Future Default |
| --- | --- | --- | --- |
| S1R docs | Yes | Yes | Documentation only. |
| S0 docs | Yes | No | Evidence only. |
| Release files | Evidence only | No | Read-only baseline. |
| `.claude/` | No user-local reads | No | Protected. |
| `.codex/` | No | No | Protected. |
| `PAI/` | No live reads | No | Protected. |
| PAI Memory | Evidence only | No | Read-only trial before writes. |
| ISA | Evidence only | No | Read-only trial before writes. |
| Pulse | No live calls | No | Bridge required. |
| Settings, hooks, skills, agents, commands | Evidence only | No | Native transformation required. |

Future writes require architect approval, explicit writer ownership, lock or lease behavior, provenance, dry run, rollback, and tests.

## Existing Local v5 Trial Policy

Existing local v5 files must be protected.

Future trials must progress in this order:

1. Copied fixture inspection.
2. Sanitized fixture tests.
3. Read-only trial mode against existing local v5 files.
4. Assisted patch mode with external writer.
5. Controlled single-writer mode.
6. Codex-only replacement mode only after replacement readiness.

No trial may require uninstalling Claude Code.

## Dual-Engine Policy

Dual-engine use means Claude Code and Codex may both be installed or available.

Policy:

- Exactly one writer owns each canonical PAI state surface at a time.
- Engine identity must be visible in provenance.
- Claude Code memory remains separate from PAI Memory.
- Codex memory remains separate from PAI Memory.
- Codex `/goal` state remains separate from PAI Memory, ISA, and Pulse state.
- Pulse events must identify engine and mode.
- User-selectable local engine substitution must not overwrite Claude files.

## Installer and Rollback Boundary

Installer and rollback rules:

- S1R does not edit installers.
- Future Codex replacement must be reversible.
- Future Codex replacement must not require uninstalling Claude Code.
- Future setup must not overlay or clear `~/.claude/`.
- Future generated Codex files must be separate from Claude files.
- A failed Codex trial must leave Claude Code usable.
- Rollback proof is required before live write mode.

## Protected Paths

Protected repository paths:

- `Releases/`
- `Releases/v5.0.0/`
- `Releases/v5.0.0/.claude/`
- `.claude/`
- `PAI/`
- `CLAUDE.md`
- `AGENTS.md`
- `.codex/`
- `install.sh`
- `PAI_SYSTEM_PROMPT.md`
- `settings.json`
- `hooks/`
- `skills/`
- `subagents/`
- `agents/`
- `commands/`
- `.github/`
- `.agents/`

Protected user-local paths:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`

## Boundary Violations

Boundary violations include:

- Claiming Codex is drop-in today.
- Claiming Codex is the official upstream engine today.
- Copying `.claude` into `.codex`.
- Copying Claude `settings.json` into Codex.
- Cloning `CLAUDE.md` into a future Codex `AGENTS.md`.
- Treating `PAI_SYSTEM_PROMPT.md` as ordinary markdown.
- Treating Codex memory as PAI Memory.
- Treating Codex `/goal` state as PAI Memory, ISA, or Pulse state.
- Writing PAI Memory without single-writer control.
- Writing ISA without single-writer control.
- Claiming Pulse parity without a bridge.
- Running existing local v5 trials that require uninstalling Claude Code.
- Treating read-only trial success as live-write safety.

## Review Gates

Required review gates before implementation:

- Authority gate for `PAI_SYSTEM_PROMPT.md`.
- Native surface gate for Codex hooks, rules, config, skills, subagents, agents, and commands.
- Transformation spec gate with tests.
- Pulse bridge gate.
- Memory and ISA boundary gate.
- Single-writer gate.
- Existing local v5 read-only trial gate.
- Sandbox and permission gate.
- Installer and launcher reversibility gate.
- Rollback proof gate.
- Governance separation gate.

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
