# V5 Codex Runtime Strategy

## Purpose

Define the canonical S1 runtime strategy for a future Codex replacement adapter for PAI v5.0.0.

This document is design-only. It does not implement a Codex adapter, create runtime adapter files, modify release files, create Codex native surfaces, authorize Pulse implementation, authorize PAI Memory writes, or authorize live local v5 trials.

## Strategic Position

Claude Code remains the current official/full-support upstream engine for PAI v5.0.0 until replacement-grade validation exists.

Codex should be designed as a replacement-capable beta local engine. Codex is a future local runtime candidate behind a designed adapter, not the official upstream engine today.

## Replacement Thesis

Codex replacement is plausible only through a designed adapter.

The thesis is that PAI v5.0.0 has a conceptual engine layer, but the shipped implementation is wired to Claude Code. A future adapter can make Codex a user-selectable local engine only if it preserves PAI authority, Pulse centrality, ISA semantics, PAI Memory ownership, hook behavior, skill and agent activation, settings/security intent, sandbox constraints, and rollback safety.

## What Replacement Means

Replacement means user-selectable local engine substitution.

Valid replacement means a user can select Codex as the local engine after replacement-grade validation while preserving:

- PAI doctrine.
- `PAI_SYSTEM_PROMPT.md` high-authority semantics.
- Pulse as central infrastructure.
- PAI Memory and ISA as canonical PAI state.
- Claude Code as an available fallback until an architect approves otherwise.
- Reversible setup.
- Single-writer policy before writes.

## What Replacement Does Not Mean

Replacement does not mean:

- Codex is drop-in today.
- Codex is the official upstream engine today.
- PAI becomes an OpenAI project.
- Claude Code must be uninstalled.
- Claude files are overwritten.
- `.claude` is copied into `.codex`.
- Claude-shaped files are treated as native Codex files.
- `CLAUDE.md` is cloned into a future Codex `AGENTS.md`.
- Codex memory or Codex `/goal` state becomes PAI Memory.
- Goal completion becomes ISA acceptance.
- Pulse parity exists without an event bridge.
- PAI Memory writes are allowed without a single-writer policy.

## Canonical Baseline

The canonical baseline is PAI v5.0.0 as shipped under `Releases/v5.0.0/.claude/` and documented by S0.

The release baseline is read-only evidence for S1R.

## Evidence Base

Evidence comes from `docs/adapters/V5_S0_DISCOVERY_REPORT.md` and cited upstream files.

Important evidence includes:

- `Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts`
- `Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts`
- `Releases/v5.0.0/.claude/settings.json`
- `Releases/v5.0.0/.claude/hooks/README.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md`
- `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md`

## V5 Architecture Confirmation

S0 confirms that PAI v5.0.0 is a Life OS architecture with Pulse, Algorithm, ISA, Memory, hooks, skills, agents, commands, settings, and `PAI_SYSTEM_PROMPT.md` wired into Claude Code's home directory and runtime model.

Some PAI concepts may be engine-neutral if semantics are preserved. The shipped runtime implementation is not engine-neutral today.

## Current Drop-In Assessment

Is Codex a drop-in replacement today for existing local PAI v5 files?

No. Codex is not currently proven drop-in for existing local PAI v5 files.

Blocking reasons:

- The v5 launcher invokes Claude Code.
- The v5 inference path invokes Claude Code.
- The v5 settings schema is Claude Code-specific.
- Hooks are Claude Code lifecycle-specific.
- Skills, commands, and agents use Claude-shaped activation and frontmatter.
- Pulse includes Claude job semantics.
- `PAI_SYSTEM_PROMPT.md` authority semantics require explicit mapping.
- PAI Memory and ISA writes require single-writer control.

## Existing Local v5 User Model

Future user modes must be explicit and architect-approved.

| Mode | Description | Write Permission | Required Gate |
| --- | --- | --- | --- |
| Read-only trial mode | Codex reasons over a copied or explicitly read-only view of existing local v5 files. | None | Fixture or read-only guard proof. |
| Assisted patch mode | Codex proposes changes while another approved actor applies them. | Proposed changes only | Provenance and review workflow. |
| Controlled single-writer mode | Codex writes selected PAI state under a lock or lease. | Limited and explicit | Single-writer policy, rollback, tests. |
| Codex-only replacement mode | Codex is selected as the local engine after replacement-grade validation. | As approved by adapter policy | Full readiness criteria pass. |
| Dual-engine coexistence mode | Claude Code and Codex are both available with one writer per canonical state surface. | Controlled by owner map | Engine labels and writer ownership. |

S1R authorizes none of these modes at runtime.

## Dual-Subscription and Memory Coexistence Model

Dual subscription does not merge memory.

Memory model:

- PAI Memory is canonical PAI state.
- ISA artifacts are canonical PAI state.
- Claude Code auto memory is not PAI Memory.
- Codex memory is not PAI Memory.
- Codex `/goal` state is not PAI Memory, not ISA, and not Pulse state.
- Product memories must not be silently promoted into PAI Memory.

Future coexistence requires labels for engine source, memory source, canonical status, writer mode, and provenance.

## Runtime Architecture

The future architecture should use adapter lanes rather than a migrated tree.

| Lane | Purpose | S1R Position |
| --- | --- | --- |
| Authority | Preserve `PAI_SYSTEM_PROMPT.md` semantics. | Future spec required. |
| Launcher and inference | Invoke Codex natively without editing the v5 release baseline. | Future-only. |
| Hooks and events | Map lifecycle behavior. | Compatibility matrix required. |
| Pulse | Emit provenance-labeled events and job identity. | Bridge required before parity. |
| Memory | Read and write PAI Memory only under policy. | Read-only first. |
| ISA | Preserve system-of-record semantics. | No shadow ISA. |
| Skills | Transform activation rules into native Codex material. | No direct copy. |
| Agents | Transform model, permission, isolation, and routing semantics. | No direct copy. |
| Commands | Transform slash command semantics natively. | No direct copy. |
| Settings and security | Map security intent, not file syntax. | Native Codex mapping required. |
| Sandbox and permissions | Preserve least privilege and fail-closed behavior. | Future spec required. |
| Installer and launcher | Keep setup reversible and non-destructive. | No installer edits in S1R. |
| Rollback | Restore previous state and keep Claude usable. | Required before live mode. |

## Instruction-Layer Strategy

`PAI_SYSTEM_PROMPT.md` is high-authority doctrine, not ordinary markdown.

Future Codex design must identify a native authority surface, preserve instruction ordering, keep doctrine out of product memory and goal state, test conflicts, and fail readiness if equivalent authority cannot be proven.

## Native Surface Mapping Strategy

Codex native surfaces are not Claude surfaces.

Claude-shaped files must not be copied directly into Codex. A future Codex `AGENTS.md`, if later authorized, must be a compact router, not a clone of `CLAUDE.md`.

Codex hooks, rules, config, skills, subagents, agents, and commands must be designed as native Codex material. Behavior-preserving transformation requires an explicit adapter spec and tests.

## Pulse Strategy

Pulse is central v5 infrastructure, not optional background trivia.

Future Codex support requires a Pulse event bridge, engine identity, mode labels, explicit Codex or adapter job identity, error events, rollback events, and dashboard parity tests.

S1R does not start Pulse, write Pulse state, implement Pulse endpoints, or claim Pulse parity.

## Memory Strategy

PAI Memory remains canonical PAI state.

Future Codex memory behavior must keep Codex memory non-canonical unless explicitly bridged, prevent silent promotion into PAI Memory, use provenance for proposed writes, require single-writer control before accepted writes, and support read-only trial behavior against existing local v5 files.

## ISA Strategy

ISA artifacts remain canonical PAI state.

Future Codex behavior must avoid shadow ISA formats, keep Codex `/goal` completion separate from ISA acceptance, preserve done and verification semantics, and require single-writer control before ISA writes.

## Skills Strategy

Skills must be transformed by semantics, not copied by file shape.

Future work must map activation descriptions, frontmatter, tool assumptions, memory assumptions, permission requirements, and failure behavior.

## Hooks and Rules Strategy

Hooks and rules must be designed natively for Codex.

Future work must map Claude Code lifecycle events, stdin payloads, `additionalContext`, fail-open and fail-closed behavior, security hook behavior, and Pulse hook validation behavior.

Unsupported lifecycle behavior must be explicit.

## Agents and Commands Strategy

Agents and commands are high-risk transformation surfaces.

Future work must map agent role semantics, model selection, isolation, permissions, max-turn behavior, voice and Pulse startup calls, slash command routing, and `Skill(...)` or `Agent(...)` references.

## Sandbox and Permission Strategy

A future Codex adapter must preserve security intent.

Unknown mappings must fail closed. Write-capable operations require explicit permission. Filesystem access must distinguish fixture roots from live roots. Tool permissions must map to native Codex controls.

## Installer and Launcher Strategy

Future design must avoid uninstalling Claude Code, avoid overlaying or clearing `~/.claude`, avoid modifying release files, keep generated Codex config separate and reversible, and provide read-only trial mode before live mode.

## Rollback and Reversibility Strategy

Future replacement must be reversible.

Rollback requires fixture restore proof, backups for generated config, no destructive installer behavior, a clear writer owner map, ability to return to Claude Code, and audit trail for proposed and accepted writes.

## Governance Separation

PAI remains governed by its repository and architecture. Codex is a candidate local engine, not the owner of PAI.

Do not turn PAI into an OpenAI project. Do not treat Codex product state as PAI state. Do not let engine vendor conventions override PAI doctrine.

## Compatibility Posture

Compatibility is not assumed. It must be proven.

Claude Code remains the proven v5 engine. Codex is replacement-capable only as a future beta local engine. Read-only trial is the first safe future mode. Writes require single-writer control.

## Replacement Readiness Criteria

Codex replacement readiness requires tests and review for authority, hooks, Pulse, Memory, ISA, skills, agents, commands, settings/security, sandbox/permissions, installer/launcher reversibility, existing-local-v5 read-only trial, controlled single-writer behavior, and rollback.

## Candidate Milestones Requiring Architect Approval

Future advisory milestones requiring architect approval:

- Codex runtime evidence refresh.
- Authority and instruction-layer design.
- Native surface mapping inventory.
- Read-only fixture trial harness.
- Pulse event bridge design.
- Memory and ISA single-writer design.
- Reversible installer and launcher design.
- Controlled beta trial plan.

S1R does not advance into these milestones.

## Non-Goals

S1R does not implement a Codex adapter, create Codex config, modify `.codex/`, modify `.claude/`, modify `PAI/`, modify release files, modify root `AGENTS.md`, run Pulse, invoke Claude Code, invoke Codex import tooling, read user-local private state, authorize PAI Memory writes, claim Codex is drop-in today, or claim Codex is the official upstream engine today.

## Executive Strategy

The V5 Codex replacement strategy is adapter-first, read-only-first, and reversible. Codex is not treated as a drop-in replacement for Claude Code in PAI v5.0.0. The target is a future compatibility adapter that lets Codex act as a selectable runtime engine only after authority, event, Pulse, state, settings, and rollback gates are satisfied.

This document is an S1 strategy artifact only. It does not implement a runtime adapter, create adapter files, modify release files, or authorize live local PAI writes.

## Evidence Baseline

S0 established these constraints:

- PAI v5.0.0 is currently Claude Code-native and installed under `~/.claude/` (`docs/adapters/V5_S0_DISCOVERY_REPORT.md`, "Executive Finding").
- `pai.ts` launches `claude` and appends `PAI_SYSTEM_PROMPT.md` with Claude Code's `--append-system-prompt-file` flag (`Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts:391-404`).
- `Inference.ts` shells out to `claude`, uses Claude model names, and assumes Claude Code subscription behavior (`Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts:85-140`).
- `settings.json` is a Claude Code settings file with Claude tools, permissions, hook events, status line, HTTP hook allowlists, and plugin fields (`Releases/v5.0.0/.claude/settings.json:1-84`, `Releases/v5.0.0/.claude/settings.json:277-372`).
- Hooks depend on Claude Code lifecycle events and payload semantics (`Releases/v5.0.0/.claude/hooks/README.md:39-90`, `Releases/v5.0.0/.claude/hooks/README.md:95-130`).
- Pulse is the central daemon, dashboard, observability, voice, hooks, jobs, and event API surface (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md:1-13`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Observability/ObservabilitySystem.md:187-220`).
- ISA and PAI Memory are canonical PAI state (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md:1-10`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:1-15`).

## North Star

The future adapter should make Codex a selectable PAI runtime engine without changing the meaning of PAI.

That means:

- PAI doctrine remains authoritative.
- Pulse remains central.
- ISA remains the system-of-record primitive.
- PAI Memory remains canonical PAI state.
- Claude Code can remain installed and usable.
- Codex runtime state, Codex memory, and Codex goal metadata remain separate unless explicitly bridged.
- Replacement readiness is proven by fixtures, compatibility matrices, and rollback, not by copying files.

## Runtime Shape

The safest target shape is a boundary adapter, not a migrated tree.

Conceptually, the future adapter has these lanes:

| Lane | Responsibility | S1 Position |
| --- | --- | --- |
| Authority lane | Preserve `PAI_SYSTEM_PROMPT.md` as high-authority doctrine or provide a formally equivalent Codex authority binding. | Required design problem; no equivalent is assumed. |
| Launcher lane | Provide a Codex-specific entry path without modifying or replacing `pai.ts` during S1. | Future-only; Claude launcher remains canonical upstream evidence. |
| Inference lane | Replace Claude subprocess inference with a Codex-native provider contract. | Future-only; provider details must be verified later against current Codex behavior. |
| Hook/event lane | Map Claude lifecycle events, payloads, and failure semantics to Codex runtime events or adapter events. | Blocking design lane; unsupported events must remain explicit gaps. |
| Pulse lane | Emit Pulse-compatible events and job identities through an explicit bridge. | Required before dashboard, observability, or scheduled-job parity is claimed. |
| State lane | Read PAI state through fixture-bound roots first; write only after single-writer, provenance, and rollback gates. | Read-only-first; no live writes. |
| Settings/security lane | Translate security intent from Claude settings into Codex-specific policy. | Future-only; copying `settings.json` is not compatibility. |
| Skills/commands/agents lane | Transform activation, permissions, isolation, model selection, and tool semantics. | Future-only; direct file reuse is not assumed. |
| Goal/memory lane | Use Codex goals as orchestration metadata only; do not promote them to PAI Memory automatically. | Covered by `V5_CODEX_GOAL_RUNBOOK.md`. |

## Authority Strategy

The current v5 runtime has a documented instruction hierarchy with `PAI/PAI_SYSTEM_PROMPT.md` at the highest layer, then `CLAUDE.md`, imported identity/project/system files, and dynamic hook context (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/PAISystemArchitecture.md:125-148`).

For Codex replacement, the adapter must preserve the authority intent, not merely the file content.

Minimum future requirements:

- Identify the Codex mechanism that can carry doctrine with authority comparable to the Claude Code `--append-system-prompt-file` path.
- Preserve ordering above operational procedures and dynamic context.
- Keep `PAI_SYSTEM_PROMPT.md` out of product memory, goal state, and ordinary retrieval-only context unless a reviewed design proves equivalent authority.
- Test conflict cases where doctrine, operational instructions, and user prompts disagree.
- Record unsupported authority behavior as a blocker rather than treating it as acceptable drift.

S1 does not choose the Codex binding mechanism because S0 did not inspect Codex runtime internals or `.codex/` state.

## Launcher And Inference Strategy

The current launcher and inference stack are Claude-specific. `pai.ts` invokes `claude`, and `Inference.ts` shells out to Claude models and subscription behavior.

The future adapter should separate PAI orchestration from engine invocation:

- Launcher compatibility should be a new adapter responsibility, not an edit to the upstream v5.0.0 release baseline during S1.
- Inference should become a provider contract with explicit input, output, model policy, timeout, failure, and provenance behavior.
- The provider must not assume Claude model tiers, Claude environment variables, Claude output format, or Claude subscription routing.
- Prompt-processing behavior that currently depends on Claude inference must be validated independently for Codex.

No S1 document should claim Codex model or CLI parity without a later approved evidence refresh.

## Hook And Event Strategy

S0 identified Claude Code hook events as central runtime surfaces. The future Codex adapter must create an event compatibility matrix before any runtime claim.

Minimum event questions:

- What Codex lifecycle point, if any, corresponds to Claude `SessionStart`?
- What Codex lifecycle point, if any, corresponds to `UserPromptSubmit` and `additionalContext`?
- What Codex lifecycle points, if any, correspond to `PreToolUse` and `PostToolUse`?
- What Codex lifecycle points, if any, correspond to `Stop`, `PreCompact`, and `SessionEnd`?
- Which current hook behaviors are fail-open, fail-closed, advisory, or blocking?
- Which hook payload fields are required by PAI and Pulse?

Unsupported events must be represented as gaps. The adapter must not silently skip lifecycle behavior that affects memory, ISA, security, or observability.

## Pulse Strategy

Pulse is not optional. A Codex replacement adapter must preserve Pulse as central infrastructure or explicitly state which Pulse functions remain unsupported.

Minimum future bridge requirements:

- Engine identity: events must identify whether they came from Claude, Codex, or an adapter fixture.
- Mode identity: events must identify fixture/read-only/shadow/live mode.
- Source identity: events must not confuse a copied fixture with live `PAI_DIR`.
- Job identity: scheduled Codex reasoning should not be hidden inside a Claude job type without an explicit reviewed decision.
- Event schema: prompt, tool, result, error, memory-read, proposed-write, accepted-write, and rollback events need stable fields before dashboard parity is claimed.
- Failure handling: Pulse bridge failures must not cause hidden state writes or false success.

S1 does not start Pulse or call local Pulse endpoints.

## State Strategy

The state strategy has one default: read-only until proven otherwise.

State classes:

| State Class | Examples | S1 Strategy |
| --- | --- | --- |
| Canonical PAI state | `PAI/MEMORY`, ISA files, `STATE/work.json`, user identity files | No writes. Future reads only from copied fixtures until live-read safety is approved. |
| PAI runtime telemetry | Observability JSONL, Pulse event streams, hook logs | No writes. Future bridge must include provenance and rollback references. |
| Claude Code state | `~/.claude`, Claude project memory, Claude settings | No mutation. Claude remains installed and recoverable. |
| Codex state | `.codex/`, Codex memory, Codex goal state | Not read or written in S1. Future bridge must be explicit and provenance-labeled. |
| Strategy docs | `docs/adapters/*.md` approved by S1 | Allowed S1 write surface. |

Before any future Codex write path, the adapter must prove:

- Single-writer ownership.
- Lock or lease behavior.
- Dry-run output.
- Proposed-write review.
- Provenance fields.
- Rollback from backup or fixture snapshot.
- No silent promotion from product memory or goal state into PAI Memory.

## Settings And Security Strategy

The adapter must preserve security intent, not copy settings syntax.

Claude Code settings contain permission rules, hook configuration, HTTP hook allowlists, status line behavior, and plugin fields. A Codex adapter must discover the current Codex equivalents in a later approved phase and classify each mapping as equivalent, transformed, unsupported, or unnecessary.

Default posture:

- Unknown permission mappings fail closed for write-capable behavior.
- Unsupported tool permissions do not become broad shell or filesystem access.
- HTTP hook behavior must remain restricted to explicit local surfaces.
- Generated Codex config, if ever created, must be reversible and separate from upstream release files.

## Skills, Commands, And Agents Strategy

Skills, commands, and agents cannot be assumed portable.

Future transformation must inspect:

- Activation rules and descriptions.
- Frontmatter fields such as model, permissions, isolation, and max turns.
- Tool names like `Skill(...)` and `Agent(...)`.
- Voice and Pulse startup calls.
- Slash command routing.
- Context and memory assumptions.

The first safe target is a semantic inventory, then read-only translation fixtures. Direct copy into Codex runtime locations is not a valid proof of support.

## Existing-User Strategy

The adapter must be safe for users who already have local v5 files.

Required posture:

- Do not uninstall Claude Code.
- Do not overlay or clear `~/.claude`.
- Do not point Codex at live `PAI_DIR` with writes enabled.
- Do not mutate existing Memory, ISA, USER, settings, hooks, skills, agents, commands, or Pulse state.
- Start with disposable fixtures copied from the release or sanitized user-approved snapshots.
- Require rollback proof before any future live write mode.

## S2 Gate List

This list names minimum future gates only. It is not S1 implementation authorization.

- Current Codex runtime evidence has been refreshed from approved sources.
- Authority-equivalence design is documented.
- Event compatibility matrix is documented.
- Pulse bridge schema and job identity decision are documented.
- State access broker and single-writer policy are documented.
- Fixture root guardrails are documented.
- Settings/security mapping is documented.
- Skills/commands/agents transformation inventory is documented.
- Rollback proof criteria are documented.

## Open Unknowns

- Which Codex mechanism can carry PAI doctrine with equivalent authority to Claude Code's appended system prompt?
- Which Codex lifecycle events can support PAI hook behavior without semantic loss?
- Whether Pulse should receive a first-class `codex` job type or a generic adapter job identity.
- Which current PAI tools are engine-neutral enough to reuse unchanged in a future phase.
- How Codex goal state should be displayed, if at all, without becoming canonical PAI state.
- What exact permission model should replace Claude Code `settings.json` behavior.

## S1 Conclusion

The coherent S1 strategy is to preserve PAI v5.0.0 semantics and treat Codex as a future runtime engine behind a deliberately designed adapter. The first proof target is not "Codex runs PAI"; it is "Codex can be mapped to PAI authority, events, Pulse, state, and security semantics without touching live state." Until those gates pass, Claude Code remains the only proven v5.0.0 runtime.
