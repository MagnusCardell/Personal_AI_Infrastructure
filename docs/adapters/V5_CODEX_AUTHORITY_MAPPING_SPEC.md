# V5 Codex Authority Mapping Spec

## Purpose

Define the non-runtime authority mapping required before a future Codex adapter can safely test against existing local PAI v5 files.

This spec is design-only. It does not implement a Codex adapter, create root `AGENTS.md`, create `.codex/`, create hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixture harnesses, tests, generated config, or runtime files. It does not modify release files, inspect private user-local state, start Pulse, run installers, or run Codex import or migration tooling.

## Source Discipline

PAI facts come from S0/S1/S2 adapter docs and targeted read-only release evidence.

Codex facts come only from official OpenAI Codex documentation.

OpenAI Codex source URLs used:

- `https://developers.openai.com/codex/guides/agents-md`
- `https://developers.openai.com/codex/config-basic`
- `https://developers.openai.com/codex/config-reference`
- `https://developers.openai.com/codex/hooks`
- `https://developers.openai.com/codex/agent-approvals-security`
- `https://developers.openai.com/codex/concepts/sandboxing`
- `https://developers.openai.com/codex/memories`
- `https://developers.openai.com/codex/cli/features`

## Executive Position

Codex is not currently proven drop-in for existing local PAI v5 files.

The PAI v5 authority stack is currently Claude Code-native. A future Codex authority design must preserve the semantics of `PAI_SYSTEM_PROMPT.md` as high-authority doctrine without copying Claude-shaped runtime files into Codex surfaces.

The safest S3 position is:

- `PAI_SYSTEM_PROMPT.md` remains source doctrine.
- A future Codex authority surface must be designed natively.
- A future Codex `AGENTS.md`, if later authorized, must be a compact router, not a clone of `CLAUDE.md` or `PAI_SYSTEM_PROMPT.md`.
- Codex hooks, config, rules, skills, subagents, agents, commands, transcripts, and memories are not PAI authority merely because they exist.
- Authority equivalence must be proven before any read-only trial against existing local v5 files.

## Current PAI Authority Stack

S0 and read-only release evidence identify the current PAI v5 authority stack:

| PAI Layer | Current Source | Current Role | Evidence | S3 Mapping Status |
| --- | --- | --- | --- | --- |
| Layer 1 | `PAI/PAI_SYSTEM_PROMPT.md` | Highest authority system prompt loaded through Claude Code `--append-system-prompt-file`. Contains constitutional rules, identity, mode architecture, format mandate, verification requirements, prohibitions, permission boundaries, and security protocol. | `docs/adapters/V5_S0_DISCOVERY_REPORT.md`; `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/PAISystemArchitecture.md:125-155`; `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md:183-187` | Requires future authority-equivalence design. |
| Layer 2 | `~/.claude/CLAUDE.md` | Operational procedures, templates, routing, and references below the system prompt. | `docs/adapters/V5_S0_DISCOVERY_REPORT.md`; `Releases/v5.0.0/.claude/CLAUDE.md:70-84` | Must not be cloned into Codex. May inform a future compact router. |
| Layer 3 | `@` imported files | Rich identity context, project routing, goals, and architecture map loaded with Claude context. | `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/PAISystemArchitecture.md:140-144` | Requires explicit source allowlist and privacy review before any live trial. |
| Layer 4 | `LoadContext.hook.ts` dynamic context | Session-specific relationship context, learning readback, and active work summary. Does not survive compaction. | `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/PAISystemArchitecture.md:145-147` | Future-only; Codex hooks are adjacent but not equivalent. |
| State doctrine | Algorithm, ISA, PAI Memory, Pulse docs | Execution doctrine, canonical acceptance/state artifacts, and central infrastructure. | `docs/adapters/V5_S0_DISCOVERY_REPORT.md` | Read-only doctrine only in S3; writes remain blocked. |

## Codex Native Authority Surfaces

Official OpenAI documentation identifies these Codex-native surfaces relevant to authority:

| Codex Surface | Official Fact | S3 Implication |
| --- | --- | --- |
| Global `AGENTS.md` | Codex reads global guidance from Codex home, defaulting to `~/.codex`, using `AGENTS.override.md` before `AGENTS.md`. | User-local Codex guidance is product state, not PAI doctrine. S3 does not inspect or create it. |
| Project `AGENTS.md` | Codex walks from project root to current directory and concatenates one instruction file per directory, with later files overriding earlier guidance. | A future project router is possible but must be compact and native. S3 does not create root `AGENTS.md`. |
| Fallback instruction filenames | Codex can use configured fallback names through `project_doc_fallback_filenames`. | Future adapter cannot rely on fallback filenames without explicit config and trust design. |
| Instruction byte limit | Codex stops adding files after `project_doc_max_bytes`, 32 KiB by default. | Large PAI doctrine cannot be assumed to load whole; future mapping needs size budgeting and tests. |
| `model_instructions_file` | Codex config has a `model_instructions_file` key described as a replacement for built-in instructions instead of `AGENTS.md`. | Candidate for future authority-equivalence exploration, not proof of PAI system-prompt parity. |
| Project config trust | Project `.codex/config.toml`, hooks, and rules load only for trusted projects. | Read-only trials must define trust posture before any project-local Codex layer is used. |
| Hooks | Codex hooks can add extra developer context on supported events and can guard some tool use, but `PreToolUse` is not a complete enforcement boundary. | Hooks are dynamic context or guardrails, not constitutional authority. |
| Sandbox and approvals | Codex supports `read-only`, `workspace-write`, and `danger-full-access` sandbox modes with approval policies. | Useful for trial safety, not a source of doctrine. |
| Codex memories | Codex memories are off by default, live under Codex home when enabled, and are a generated recall layer. | Codex memory is not authority and is not PAI Memory. |
| Transcripts and resume | Codex can resume sessions with transcript, plan history, and approvals. | Transcript continuity is not PAI doctrine, ISA, Pulse state, or PAI Memory. |

## Authority Mapping Thesis

The future Codex authority design should use a native Codex authority envelope rather than a migrated Claude tree.

The authority envelope is a design concept, not an S3 runtime artifact. It is the set of future Codex-native inputs that would carry PAI doctrine, operational routing, allowed dynamic context, and trial constraints.

The authority envelope must satisfy these constraints:

- Preserve `PAI_SYSTEM_PROMPT.md` as source doctrine.
- Preserve the fact that `PAI_SYSTEM_PROMPT.md` outranks `CLAUDE.md`-style operational procedures.
- Keep operational routing separate from constitutional doctrine.
- Keep user identity and private state out of repo-level generated artifacts.
- Keep Codex product memory and session state non-canonical.
- Keep trial constraints explicit and higher priority than convenience.
- Fail closed if Codex instruction ordering cannot be proven.

## Proposed Future Authority Stack

This stack is advisory for a future milestone. S3 does not create any of these surfaces.

| Future Rank | Conceptual Surface | Source Material | Purpose | S3 Status |
| --- | --- | --- | --- | --- |
| A0 | Invocation guardrail | Architect-approved adapter policy and trial mode declaration. | States engine, mode, filesystem roots, no-write rule, privacy restrictions, and stop conditions for a trial. | Design only. |
| A1 | PAI doctrine capsule | Semantics extracted from `PAI_SYSTEM_PROMPT.md`, not blindly copied. | Carries constitutional PAI rules with proven high-authority behavior. | Future authority-equivalence work. |
| A2 | Codex router | Future compact `AGENTS.md` or equivalent native project instruction surface if later authorized. | Points Codex to approved doctrine and trial procedure without cloning Claude files. | Not created in S3. |
| A3 | Operational context allowlist | Explicitly approved read-only release docs, S0/S1/S2/S3 adapter docs, and future sanitized fixtures. | Supplies architecture and procedure context under the authority envelope. | Documentation only. |
| A4 | Dynamic context bridge | Future Codex hook, MCP, or prompt-time context mechanism. | Supplies session-specific facts if authorized and privacy-reviewed. | Future-only; no hooks created. |
| A5 | Product/session state | Codex transcript, resume, plan, memories, and `/goal` state. | Helps Codex continue work, but never becomes PAI authority. | Non-canonical. |

## Mapping Table

| PAI Source | Future Codex Candidate | Required Transformation | Hard Constraint |
| --- | --- | --- | --- |
| `PAI_SYSTEM_PROMPT.md` | Authority-equivalent doctrine capsule, possibly delivered through a future native instruction mechanism such as `model_instructions_file` or an invocation envelope. | Extract behavioral obligations, conflict rules, privacy boundaries, mode constraints, verification expectations, and prohibited behavior. | Must not be demoted to ordinary project markdown. Must not be silently loaded through untested ordering. |
| `CLAUDE.md` | Compact Codex router if later authorized. | Convert operational routing into short native Codex guidance that points to approved docs and trial rules. | Must not clone `CLAUDE.md`. Must not carry Claude-specific tool names as if native. |
| `@` imported identity/project files | Explicit trial allowlist or sanitized fixture context. | Separate public release doctrine from private user-local identity and project context. | Must not inspect private user-local state in S3 or any future trial without explicit consent and guards. |
| `LoadContext.hook.ts` dynamic context | Future Codex hook, MCP, or prompt-time context bridge. | Map event timing, payload, privacy, provenance, and compaction behavior. | Codex hooks are not complete enforcement boundaries; unsupported lifecycle behavior must remain explicit. |
| Algorithm docs | Read-only operational doctrine. | Surface current-state-to-ideal-state semantics under A3. | Must not create shadow Algorithm doctrine. |
| ISA docs and artifacts | Read-only canonical state references. | Make ISA acceptance separate from Codex plan or goal completion. | Must not write ISA without single-writer policy. |
| PAI Memory docs and artifacts | Read-only canonical state references. | Label PAI Memory as PAI-owned canonical state. | Codex memory must not be promoted silently into PAI Memory. |
| Pulse docs and state | Read-only central infrastructure references. | Treat Pulse as central and blocked pending bridge design. | Must not start Pulse or claim Pulse parity. |

## Conflict Handling Model

Future authority-equivalence tests must include conflict cases.

Required conflict rules:

- If `PAI_SYSTEM_PROMPT.md` conflicts with a future Codex router, `PAI_SYSTEM_PROMPT.md` semantics win.
- If S3 read-only trial constraints conflict with convenience, read-only constraints win.
- If Codex memory or transcript context conflicts with PAI doctrine, PAI doctrine wins.
- If Codex product behavior conflicts with PAI Memory or ISA ownership, canonical PAI state rules win.
- If a future Codex hook allows a behavior that the authority envelope denies, the authority envelope wins and the behavior remains blocked.
- If Codex instruction discovery truncates or omits required PAI doctrine, the trial fails authority readiness.
- If any source is private user-local state and not explicitly authorized for the trial, it is excluded.

## Native Surface Rule

Codex native surfaces are not Claude surfaces.

Claude-shaped files must not be copied directly into Codex. This includes:

- `.claude/`
- `CLAUDE.md`
- Claude Code `settings.json`
- Claude hooks
- Claude skills
- Claude agents
- Claude commands
- Claude Pulse job semantics

If a future Codex `AGENTS.md` is authorized, it must be a compact router. It may point to approved PAI doctrine and trial instructions, but it must not clone `CLAUDE.md`, clone `PAI_SYSTEM_PROMPT.md`, or pretend Claude Code tools are native Codex tools.

## Authority Readiness Criteria

Authority mapping is ready for a future read-only trial only when an architect approves evidence for all items below:

- The future Codex authority envelope is documented.
- `PAI_SYSTEM_PROMPT.md` semantics are mapped and prioritized.
- Codex instruction ordering is proven with a deterministic source list.
- Required doctrine fits within documented Codex instruction limits or is otherwise explicitly loaded by an approved native mechanism.
- Future `AGENTS.md` content, if any, is a compact router and not a clone.
- Dynamic context sources are allowlisted and privacy-reviewed.
- Codex memory, transcripts, plans, and `/goal` state are labeled non-canonical.
- Conflicts are tested and fail closed.
- The read-only trial mode can state exactly which roots are readable and which roots are unreadable or write-denied.
- No PAI Memory, ISA, Pulse, settings, hook, installer, or release write path is authorized.

## Stop Conditions

Stop before any future trial if:

- Codex is claimed as drop-in.
- Codex is claimed as the official upstream PAI engine.
- `PAI_SYSTEM_PROMPT.md` is treated as ordinary markdown.
- `CLAUDE.md` is cloned into Codex `AGENTS.md`.
- Claude-shaped runtime files are copied into Codex surfaces.
- Codex memory, transcripts, plans, or `/goal` state are treated as PAI Memory, ISA, or Pulse state.
- Private user-local state would be inspected without explicit approval and technical guards.
- Pulse would need to be started.
- A write to PAI Memory, ISA, Pulse state, settings, hooks, release files, or installer files would be required.

## S3 Non-Authorization

This spec does not authorize implementation.

This spec does not authorize root `AGENTS.md`, `.codex/`, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixture harnesses, tests, generated config, live local v5 inspection, PAI Memory writes, ISA writes, Pulse writes, or Pulse startup.
