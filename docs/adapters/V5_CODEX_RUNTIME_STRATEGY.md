# V5 Codex Runtime Strategy

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
