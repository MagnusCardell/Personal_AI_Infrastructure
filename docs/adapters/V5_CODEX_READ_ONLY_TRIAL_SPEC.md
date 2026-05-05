# V5 Codex Read-Only Trial Spec

## Purpose

Define the non-runtime read-only trial posture required before Codex can safely be tested against existing local PAI v5 files.

This spec is design-only. It does not implement a Codex adapter, create root `AGENTS.md`, create `.codex/`, create hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixture harnesses, tests, generated config, or runtime files. It does not modify release files, inspect private user-local state, start Pulse, run installers, or run Codex import or migration tooling.

## Source Discipline

PAI facts come from S0/S1/S2 adapter docs and targeted read-only release evidence.

Codex facts come only from official OpenAI Codex documentation.

OpenAI Codex source URLs used:

- `https://developers.openai.com/codex/agent-approvals-security`
- `https://developers.openai.com/codex/concepts/sandboxing`
- `https://developers.openai.com/codex/noninteractive`
- `https://developers.openai.com/codex/config-basic`
- `https://developers.openai.com/codex/config-reference`
- `https://developers.openai.com/codex/guides/agents-md`
- `https://developers.openai.com/codex/hooks`
- `https://developers.openai.com/codex/memories`
- `https://developers.openai.com/codex/cli/features`

## Executive Position

Read-only trial means Codex may inspect explicitly approved PAI evidence and produce advisory findings, but cannot write to PAI state, Codex project config, Claude files, release files, Pulse state, Memory, ISA, hooks, skills, agents, commands, settings, installers, wrappers, or user-local state.

S3 does not run a read-only trial. S3 defines the posture a future milestone must satisfy before a read-only trial is allowed.

The first safe target remains copied or sanitized fixtures. Existing local v5 files are private, live, and potentially canonical. A future trial against them requires explicit consent, a path manifest, technical read-only enforcement, provenance labels, and a stop condition for any write attempt.

## Non-Goals

S3 does not:

- Run Codex.
- Run Claude Code.
- Start Pulse.
- Run installers.
- Run migration or import tooling.
- Read `~/.claude/`, `~/.claude/PAI/`, `~/.claude/projects/`, `~/.codex/`, or `~/.codex/memories/`.
- Create fixture harnesses.
- Create sandbox profiles.
- Create root `AGENTS.md`.
- Create `.codex/`.
- Create generated config.
- Create wrappers or launchers.
- Write PAI Memory, ISA, Pulse state, settings, hooks, skills, agents, commands, or release files.

## Read-Only Definition

For S3 and future trial design, read-only has three meanings:

| Dimension | Requirement |
| --- | --- |
| Filesystem writes | No writes to approved read roots, no generated config under those roots, no side-effect files, no transcript export into PAI roots, no chmod/chown/touch/copy/move/delete operations. |
| Runtime side effects | No Pulse startup, no installer execution, no migration/import tooling, no service launch, no network calls to local PAI endpoints, no hook execution against live PAI state. |
| Canonical state | No accepted write to PAI Memory, ISA, Pulse state, settings, hooks, skills, agents, commands, user identity files, or Claude/Codex product memory. |

Advisory text output is allowed only if it is clearly labeled as advisory and not canonical PAI state.

## Trial Phase Model

Future work must advance in phases. S3 authorizes none of these phases at runtime.

| Phase | Name | Input | Write Permission | Exit Requirement |
| --- | --- | --- | --- | --- |
| T0 | Documentation-only design | S0/S1/S2/S3 docs and read-only release evidence. | None | Specs reviewed. |
| T1 | Release fixture reasoning | Copied release baseline or repository release files treated as read-only. | None | Authority and read-only posture proven on non-private material. |
| T2 | Sanitized existing-user fixture | User-provided sanitized copy of local v5 state, not live paths. | None | Privacy review and no-write proof. |
| T3 | Existing local v5 read-only trial | Explicitly approved live local paths mounted or exposed read-only. | None | No writes, no Pulse startup, no installer calls, no private-path escapes, advisory output only. |
| T4 | Assisted patch mode | Codex proposes changes; separate approved actor applies them. | Codex none | Provenance and human acceptance workflow. |
| T5 | Controlled single-writer mode | Selected canonical PAI state under lock or lease. | Limited, future-only | Single-writer policy, rollback, and architect approval. |

No phase may skip ahead. T3 success does not authorize T4 or T5.

## Future Trial Preconditions

A future read-only trial against existing local v5 files requires:

- Architect approval for the trial scope.
- User approval for every live root to be inspected.
- A path manifest listing allowed read paths and denied paths.
- A statement that Claude Code remains installed and usable.
- A statement that Codex is not drop-in and not the official upstream engine.
- A no-write enforcement design using Codex-native read-only sandboxing or an equivalent external read-only mount.
- No network access unless separately justified and approved.
- No Pulse startup and no local Pulse endpoint calls.
- No installer execution.
- No Codex import or migration tooling.
- No `.codex/` project config generation.
- No root `AGENTS.md` creation.
- No product-memory promotion into PAI Memory.
- No goal, transcript, or plan promotion into ISA.
- A rollback statement, even though read-only mode should produce no mutations.

## Path Classification

Future trial design must classify every path before Codex sees it.

| Class | Examples | Default Future Trial Policy |
| --- | --- | --- |
| Public release evidence | `Releases/v5.0.0/README.md`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/`, release templates. | Read-only allowed after scope approval. |
| Claude runtime surface | `CLAUDE.md`, `settings.json`, `.claude/hooks/`, `.claude/skills/`, `.claude/agents/`, `.claude/commands/`. | Read-only evidence only; no direct copy or native reuse. |
| PAI doctrine | `PAI_SYSTEM_PROMPT.md`, Algorithm docs, ISA docs, Memory docs, Pulse docs. | Read-only, authority-labeled. |
| Canonical PAI state | `PAI/MEMORY/`, ISA artifacts, `PAI/USER/`, Pulse state, work state. | Deny by default for live paths; allow only by explicit manifest and read-only guard. |
| Credentials and secrets | `PAI/USER/CREDENTIALS/`, local env files, tokens, private keys, vendor credentials. | Deny read and deny write. |
| Claude product state | `~/.claude/projects/`, Claude Code auto memory, transcripts, caches. | Deny read and deny write unless explicitly authorized outside this spec. |
| Codex product state | `~/.codex/`, `~/.codex/memories/`, Codex transcripts. | Deny read and deny write during PAI trial, except Codex may maintain its own unavoidable product state outside PAI roots if the environment requires it. |
| Adapter docs | `docs/adapters/`. | Read-only during future trial unless a separate documentation milestone authorizes edits. |

## Required Manifest Fields

A future read-only trial manifest must include:

| Field | Meaning |
| --- | --- |
| `trial_id` | Unique trial identifier. |
| `engine` | Must identify Codex as candidate engine, not official upstream PAI engine. |
| `mode` | Must be `read-only-trial`. |
| `pai_version` | Must identify the target as PAI v5.0.0 or a later approved baseline. |
| `source_kind` | `release-fixture`, `sanitized-fixture`, or `existing-local-v5-read-only`. |
| `allowed_read_roots` | Explicit paths Codex may read. |
| `denied_read_roots` | Explicit paths Codex must not read. |
| `denied_write_roots` | Explicit paths Codex must not write. |
| `network_policy` | Expected default is no network. |
| `pulse_policy` | Must state no Pulse startup and no Pulse calls unless a later bridge milestone approves otherwise. |
| `memory_policy` | Must state PAI Memory is canonical PAI state and Codex memory is not PAI Memory. |
| `isa_policy` | Must state Codex plan, transcript, goal, or final answer is not ISA acceptance. |
| `output_policy` | Must require advisory output and no generated state writes. |
| `stop_conditions` | Must list write attempts, private-state access, Pulse startup, installer calls, migration calls, or drop-in claims as stops. |

## Codex Runtime Posture For Future Trials

Official OpenAI docs establish that:

- Codex supports `read-only`, `workspace-write`, and `danger-full-access` sandbox modes.
- In read-only mode, Codex can inspect files but cannot edit files or run commands without approval.
- `codex exec` runs in a read-only sandbox by default.
- A strict non-interactive automation posture can use read-only sandboxing with no approval prompts.
- Local network access is off by default in workspace-write mode unless configured.
- Filesystem permission profiles can deny reads for exact paths or globs.
- Project `.codex/` layers load only when trusted.

Future PAI read-only trials should therefore target the strictest posture available:

- Read-only sandbox.
- No approvals that would permit writes.
- No network unless explicitly approved for a non-PAI reason.
- Denied read paths for secrets, user-local product memory, and unapproved private state.
- No project `.codex/` creation or trust dependency.
- No root `AGENTS.md` creation during the trial.

This is a posture, not an S3 command. S3 does not run Codex.

## Output Rules

Future read-only trial output must be advisory and provenance-labeled.

Required output properties:

- State that Codex is a candidate engine only.
- State that the run was read-only.
- List allowed read roots.
- List denied roots that were not inspected.
- State that no writes were authorized.
- State that no PAI Memory write occurred.
- State that no ISA write or acceptance occurred.
- State that no Pulse startup or Pulse write occurred.
- Separate observations from recommendations.
- Mark any proposed patches as proposals only.
- Avoid producing files in live PAI roots.

## State Boundary Model

| Surface | Canonical PAI State | Read-Only Trial Handling |
| --- | --- | --- |
| PAI Memory | Yes | Read-deny by default for live state; if explicitly included, read-only with provenance and no promotion from Codex memory. |
| ISA artifacts | Yes | Read-only if explicitly included; Codex output does not update done, verification, or acceptance state. |
| Pulse state | Runtime-canonical when live | No live calls, startup, writes, or parity claims. |
| Claude Code memory | No | Not inspected by default; not PAI Memory. |
| Codex memory | No | Not PAI Memory; should not be used as canonical PAI recall for the trial. |
| Codex `/goal` state | No | Not PAI Memory, not ISA, not Pulse state. |
| Codex transcript or thread | No | Useful for audit, but not canonical PAI state. |
| Adapter docs | Governance/design only | Not runtime state. |

## Threat Model

The read-only trial must guard against:

- Accidental writes through shell commands, edit tools, generated config, transcript export, or patch files.
- Accidental reads of credentials, identity files, private memories, project transcripts, or Codex memories.
- Treating advisory output as accepted PAI state.
- Treating Codex memory as PAI Memory.
- Treating Codex goal completion as ISA acceptance.
- Starting Pulse or causing Pulse to observe false events.
- Running installers or migration tooling.
- Using project trust to load unreviewed `.codex/` config, hooks, or rules.
- Network exfiltration or prompt injection through web search, live browsing, or package/network access.
- False confidence from fixture success.

## Stop Conditions

A future read-only trial must stop if:

- A write is attempted against any live PAI root.
- Codex requests approval to write, run an installer, start a service, or access a denied root.
- Codex attempts to create `.codex/`, root `AGENTS.md`, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, or generated config.
- Codex attempts to read denied private user-local state.
- Pulse would need to start or be contacted.
- Codex import or migration tooling would need to run.
- A trial result is framed as drop-in proof.
- Codex memory, transcript, plan, or `/goal` state is treated as PAI Memory, ISA, or Pulse state.
- The allowed read manifest is incomplete or ambiguous.

## Validation Requirements For Future Implementation Milestone

Before any future milestone may run a read-only trial, it must provide:

- A reviewed manifest template.
- A no-write proof strategy.
- A denied-path proof strategy.
- A no-network proof strategy or explicit network exception.
- A no-Pulse-start proof strategy.
- A no-installer proof strategy.
- A no-migration-tooling proof strategy.
- An audit output format.
- A rollback statement.
- Architect approval to move from design into test execution.

## S3 Non-Authorization

This spec does not authorize a read-only trial.

This spec only defines the posture that a future read-only trial must satisfy. It does not authorize implementation, runtime adapter surfaces, existing local v5 inspection, PAI Memory writes, ISA writes, Pulse writes, settings writes, hook writes, release writes, `.codex/` creation, root `AGENTS.md` creation, or installer changes.
