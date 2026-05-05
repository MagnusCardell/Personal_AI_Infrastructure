# V5 Codex Decoupling Seam Spec

## Purpose

Define future engine-seam design requirements that would allow Codex to replace Claude Code for PAI v5 without copying Claude-shaped files or mutating upstream release files.

S6 is design-only and creates no runtime seam files.

## Scope

This spec defines seam responsibilities, inputs, outputs, forbidden behavior, future specs, future tests, and drop-in relevance.

It does not implement a Codex adapter, create root `AGENTS.md`, create `.codex/`, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, or create migration scripts.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_MANIFEST_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_SCHEMA_PROPOSAL.md`
- Repository-local PAI v5 release files under `Releases/v5.0.0/.claude/`.

No new Codex capability claim is introduced in S6.

## Seam Design Principles

Principles:

- Thin adapter over upstream PAI semantics.
- Native Codex surfaces only.
- No direct copying of Claude-shaped files into Codex surfaces.
- Claude-shaped files must not be copied directly into Codex surfaces.
- No mutation of release files.
- No private user-local state access without explicit future approval.
- Read-only first.
- Single-writer before any PAI state writes.
- Reversible by default.
- Provenance-tagged outputs.
- Pulse centrality preserved without claiming Pulse parity.
- PAI Memory and ISA canonicality preserved.
- Product memories remain product memories and are not PAI Memory.
- Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
- Codex is not currently proven drop-in for existing local PAI v5 files.
- Codex replacement is plausible only through a designed adapter.

## Engine Boundary Model

The future adapter boundary has five sides:

| Boundary | Owned By | S6 Status |
| --- | --- | --- |
| PAI doctrine and canonical state | PAI | Evidence only. |
| Claude Code engine surface | Claude Code release payload | Current official/full-support engine. |
| Codex candidate engine surface | Future Codex-native adapter material | Not created in S6. |
| Adapter seams | Future architecture milestones | Designed only in S6. |
| Repo governance | Maintainers and architect review | Documentation only. |

Replacement means user-selectable local runtime substitution after gates pass, not overwriting Claude files and not turning PAI into an OpenAI project.

## Authority Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Authority seam | Preserve `PAI_SYSTEM_PROMPT.md` as high-authority PAI doctrine in a Codex-native authority envelope. | `PAI_SYSTEM_PROMPT.md`, S3 authority mapping, S4 authority-equivalence test design. | Proven authority mapping and conflict rules. | Demote doctrine into ordinary markdown, memory, transcript, or goal state. | Authority-equivalence spec. | Ordering, truncation, conflict, omission, and refusal tests. | Required before any drop-in claim. |

## Router Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Router seam | Route Codex-native instructions to PAI doctrine without cloning `CLAUDE.md`. | `CLAUDE.md`, S3 router design, S2 Codex surface evidence. | Compact router proposal if later authorized. | Create root `AGENTS.md` in S6; clone `CLAUDE.md`; copy `PAI_SYSTEM_PROMPT.md`. | Compact router spec. | Router size, precedence, unsupported import, and doctrine-reference tests. | Required before Codex instruction startup. |

## Launcher Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Launcher seam | Replace `pai.ts` Claude launch behavior with a future native Codex launch path. | `PAI/TOOLS/pai.ts`, launcher flags, `PAI_DIR`, MCP profile evidence. | Engine-selectable launch contract. | Edit release launcher; call installers; overwrite Claude launcher. | Launcher seam spec. | Engine selection, no-release-mutation, fallback, and rollback tests. | Required for local engine substitution. |

## Inference Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Inference seam | Replace Claude CLI subprocess inference with a Codex-native provider contract. | `Inference.ts`, model levels, timeout, auth, output parsing. | Provider abstraction and result contract. | Assume Claude model names, Anthropic auth, or output semantics map directly. | Inference provider spec. | Model mapping, timeout, error, JSON extraction, auth, and billing-boundary tests. | Required for mode/tier and Pulse job reasoning. |

## Settings and Permission Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Settings and permission seam | Preserve security intent from Claude settings in native Codex controls. | `settings.json`, permissions, hooks, trusted services, protected paths. | Least-privilege policy map. | Copy Claude settings to Codex config or overgrant writes. | Settings/security mapping spec. | Denied path, allowed read, write denial, approval, and fail-closed tests. | Required before any runtime trial. |

## Hook and Lifecycle Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Hook and lifecycle seam | Map Claude lifecycle events, payloads, and enforcement semantics to Codex-native lifecycle behavior. | `hooks/README.md`, `PromptProcessing.hook.ts`, settings hook config, Pulse HTTP hooks. | Event compatibility matrix and unsupported-event list. | Run Claude hooks directly without payload mapping. | Hook lifecycle mapping spec. | Event order, payload shape, context injection, fail-open, fail-closed, and no-Pulse-start tests. | Required for guard, context, and mode parity. |

## Skill Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Skill seam | Transform Claude-facing skill semantics into native Codex skill material. | `.claude/skills/`, S2 skill evidence, S4 fixture policy. | Semantic skill transformation plan. | Copy skill directories directly. | Skill transformation spec. | Activation, progressive disclosure, tool permission, state write, and unsupported workflow tests. | Required for workflow parity. |

## Agent and Command Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Agent and command seam | Map Claude agents, subagent assumptions, and command files into future Codex-native behavior. | `.claude/agents/`, `.claude/commands/`, `settings.json` Agent permissions. | Role, permission, command, and delegation mapping. | Copy agent frontmatter or command files directly. | Agent/command transformation spec. | Role, model, permission, isolation, max-turn, command routing, and unsupported-command tests. | Required for delegation and slash-command parity. |

## Pulse Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pulse seam | Preserve Pulse centrality and add future Codex or adapter event identity without claiming parity. | Pulse docs, `type = "claude"` jobs, hook routes, port `31337` evidence. | Event/job identity model and read-only event bridge proposal. | Start Pulse in S6; overload Claude job type; claim Pulse parity. | Pulse bridge identity spec. | No-start proof, event schema, job identity, dashboard, rollback, and failure-mode tests. | Required for central infrastructure safety. |

## Memory Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Memory seam | Protect PAI Memory as canonical PAI state and keep product memories separate. | `MemorySystem.md`, S4/S5 memory policy, Codex memory boundary docs. | Read-only memory policy and future writer ownership map. | Treat Codex memory, Claude Code auto memory, transcripts, SDK threads, or `/goal` state as PAI Memory. | Memory boundary and single-writer spec. | Read-only, no-promotion, provenance, lock/lease, rollback, and curation tests. | Required before any memory write. |

## ISA Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ISA seam | Preserve ISA as canonical system-of-record artifact and done condition. | `IsaFormat.md`, S4 authority-equivalence tests, S5 audit proposal. | ISA read/write policy and no-shadow-artifact rule. | Treat Codex plan, transcript, final answer, or goal completion as ISA acceptance. | ISA writer policy spec. | No-write, no-shadow-ISA, frontmatter, acceptance, sync, and rollback tests. | Required before acceptance parity. |

## Installer and Local Layout Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Installer and local layout seam | Keep Claude Code installed and recoverable while introducing future Codex selection. | README install flow, PAI-Install docs, `PAI_DIR`, `.claude` layout. | Reversible local layout plan. | Overlay `~/.claude`, uninstall Claude Code, create `.codex/` in S6, or edit release files. | Installer/local layout spec. | Backup, restore, no-overwrite, live-root denial, and fallback tests. | Required for existing users. |

## Product Memory Boundary Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Product-memory boundary seam | Keep Claude Code memory, Codex memory, transcripts, SDK threads, and `/goal` state out of PAI Memory unless explicitly curated later. | S0-S5 memory boundaries, Claude auto-memory evidence, Codex memory boundary docs. | Provenance and non-promotion policy. | Silent promotion of product memories into PAI Memory. | Product-memory boundary spec. | Non-promotion, explicit curation, provenance, consent, and audit tests. | Required for dual-engine coexistence. |

## Rollback Seam

| Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rollback seam | Ensure future Codex trials are reversible and Claude Code remains usable. | S1 rollback strategy, S4/S5 manifest and audit design, installer evidence. | Restore plan and rollback proof requirements. | Proceed to writes without rollback, provenance, and validation. | Rollback and reversibility spec. | Restore, no-state-corruption, fallback, audit, and failed-trial cleanup tests. | Required before any live mode. |

## Seam Dependency Graph

| Order | Dependency | Rationale |
| --- | --- | --- |
| 1 | Authority seam before router seam | Router cannot be created safely until high-authority doctrine mapping is known. |
| 2 | Router seam before launcher seam | Launcher must know which Codex-native authority material is valid. |
| 3 | Launcher seam before inference seam integration | Engine selection and invocation boundaries must precede provider behavior. |
| 4 | Settings and permission seam before read-only trial | Trial safety depends on read/write and tool controls. |
| 5 | Hook and lifecycle seam before behavioral parity claims | Hooks drive context, guards, and state updates. |
| 6 | Memory seam and ISA seam before write-capable modes | Canonical PAI state cannot be written without ownership and rollback. |
| 7 | Pulse seam before Pulse parity or job claims | Central infrastructure requires event identity and no-start proof. |
| 8 | Skill seam and agent/command seam after authority and permissions | Transformations need authority, routing, and security constraints. |
| 9 | Installer/local layout seam and rollback seam before existing-user modes | Existing local v5 users require non-destructive setup and recovery. |

## Prohibited Seam Designs

Prohibited designs:

- Copy `.claude/` into `.codex/`.
- Clone `CLAUDE.md` into `AGENTS.md`.
- Treat `PAI_SYSTEM_PROMPT.md` as ordinary markdown or product memory.
- Copy Claude `settings.json` into Codex config.
- Run Claude hooks directly under Codex without event and payload mapping.
- Copy Claude skills, agents, or commands directly into Codex surfaces.
- Overload Pulse `type = "claude"` for Codex jobs.
- Treat Codex memory as PAI Memory.
- Treat Codex `/goal` completion as ISA acceptance.
- Require uninstalling Claude Code.
- Modify release files.
- Authorize PAI Memory writes, ISA writes, or Pulse implementation from S6.

## Future Implementation Gates

Future implementation requires:

- Architect approval.
- Approved write set for the specific milestone.
- Authority-equivalence proof.
- Native router design.
- Read-only fixture validation before existing-local-v5 exposure.
- Settings/security mapping and denied-path tests.
- Hook lifecycle compatibility tests.
- Skill, agent, and command transformation tests.
- Pulse event and job identity model.
- Memory and ISA single-writer policy.
- Rollback and reversibility proof.

## Non-Goals

S6 does not implement a Codex adapter, create runtime seams, create root `AGENTS.md`, create `.codex/`, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create migration scripts, inspect user-local private state, start Pulse, run installers, run Codex import or migration tooling, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, claim Codex is drop-in today, or claim Codex is the official upstream engine.
