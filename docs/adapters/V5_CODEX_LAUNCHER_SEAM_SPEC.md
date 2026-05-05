# V5 Codex Launcher Seam Spec

## Purpose

Define the future launcher seam that would allow PAI v5 to select Codex as a local runtime engine without mutating upstream release files or invoking Claude-shaped behavior.

## Scope

The launcher seam is a future engine-selection boundary, not an implementation.

This document defines launcher seam as a future engine-selection boundary, not an implementation.

S7C designs launcher and inference seams only. It does not implement launcher replacement, create a launcher, create a wrapper, create an engine profile instance, create Codex config, create root `AGENTS.md`, create `.codex/`, create runtime files, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, invoke Claude Code, invoke Codex as a runtime engine, or run Codex import or migration tooling.

## Evidence Base

Evidence comes from:

- `Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts`
- `Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts`
- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_COMPACT_ROUTER_SPEC.md`
- `docs/adapters/V5_CODEX_ENGINE_PROFILE_AND_CAPABILITY_CONTRACT.md`

No new Codex capability claim is introduced in S7C. Codex CLI, noninteractive, config, sandbox, and approval facts are inherited from S2/S3/S7A official-source evidence.

## Launcher Problem Statement

Codex is not currently proven drop-in for existing local PAI v5 files.

The current launcher is Claude Code-native. It is not a generic PAI engine selector. Codex replacement is plausible only through a designed adapter that can preserve PAI semantics while selecting a future Codex-native local runtime path.

Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Existing Claude Launcher Couplings

Observed launcher assumptions from `pai.ts`, S6, and S7A evidence:

| Coupling | Evidence | Replacement hazard |
| --- | --- | --- |
| Claude identity | File header describes a CLI for managing Claude Code. | Future Codex path cannot be a simple flag swap. |
| Claude executable | `getCurrentVersion()` calls `claude --version`; launch uses `const args = ["claude"]`; one-shot prompt uses `["claude", "-p", prompt]`. | Runtime invocation is hard-coupled to Claude CLI behavior. |
| `.claude` root | `CLAUDE_DIR = join(homedir(), ".claude")`; launcher changes directory to that root unless `--local` is set. | Codex must not be bound to live Claude roots without explicit policy. |
| MCP profile layout | MCP profiles and `.mcp.json` are managed under `.claude`. | Codex MCP/config behavior cannot copy Claude layout or mutate live state. |
| System prompt append | Launcher appends `PAI_SYSTEM_PROMPT.md` using Claude `--append-system-prompt-file`. | Codex authority envelope needs a native proof, not Claude flag reuse. |
| Subscription billing guard | Launcher deletes `ANTHROPIC_API_KEY` before spawning Claude. | Future engine profile must expose auth/billing boundaries without assuming Anthropic env behavior. |
| Pulse voice notification | Launcher calls local Pulse notification endpoints before launch. | Future launcher must not start or contact Pulse unless later Pulse milestone authorizes it. |
| Update path | `update` runs Bun/Brew and Claude install shell path. | Future Codex replacement must not run installers or mutate release files in S7C. |
| Exit behavior | One-shot prompt exits with the Claude process exit code. | Future exit-code model must be specified instead of inherited. |

## Launcher Seam Principles

Principles:

- Preserve PAI semantics without mutating release files.
- Treat engine selection as future policy, not S7C action.
- Keep Claude Code installed and recoverable.
- Keep `PAI_SYSTEM_PROMPT.md` as high-authority doctrine through an authority envelope.
- Use future native Codex surfaces only after architect approval.
- Do not copy Claude-shaped files directly into Codex surfaces.
- Do not create root `AGENTS.md` or `.codex/`.
- Do not create Codex config/profile in S7C.
- Keep launcher decisions auditable and reversible.
- Preserve read-only first posture.
- Require single-writer policy, provenance, rollback, and validation before any PAI state writes.

## Engine Selection Model

Engine selection is future policy, not S7C action.

Required future inputs:

| Input | Meaning |
| --- | --- |
| `engine_id` | Stable engine identifier, such as `claude-code-official` or a future `codex-candidate` value. |
| `pai_dir` | Explicit PAI root to use, never inferred from live user-local state without approval. |
| `authority_envelope_id` | Reference to the approved authority envelope for the run. |
| `adapter_mode` | Mode such as `documentation-only`, `fixture-read-only`, or future controlled mode. |
| `source_kind` | Release evidence, fixture, sanitized fixture, or future approved existing-local-v5 scope. |
| `sandbox_policy` | Allowed command and filesystem posture. |
| `permission_policy` | Tool, network, approval, and write-denial posture. |
| `memory_policy` | PAI Memory, product memory, and no-promotion rules. |
| `isa_policy` | ISA read/write and acceptance boundary. |
| `pulse_policy` | Pulse no-start, no-call, or future bridge policy. |
| `audit_policy` | Required audit envelope and provenance fields. |
| `rollback_policy` | Fallback, restore, and recovery behavior. |

Required future outputs:

- Selected engine.
- Resolved paths.
- Invocation plan.
- Denied behaviors.
- Unsupported surface report.
- Audit envelope.
- Rollback path.

The future output contract must preserve these labels exactly for downstream validation: selected engine, resolved paths, invocation plan, denied behaviors, unsupported-surface report, audit envelope, and rollback path.

## Invocation Boundary Model

The future launcher seam must separate policy resolution from process invocation.

Future invocation planning must identify:

- Runtime command or API surface, if any.
- Working directory.
- Environment variables.
- Stdin/stdout/stderr handling.
- Exit-code handling.
- Authority envelope source.
- Sandbox and permission policy.
- Unsupported Claude behavior.
- Fallback to official Claude Code engine.

S7C does not execute this plan and does not invoke Codex as a runtime engine.

## Environment and Path Model

Future path handling must:

- Resolve `pai_dir` explicitly.
- Never infer live `~/.claude/PAI` access without later approval.
- Keep repository-local release evidence read-only.
- Keep `.claude/`, `.codex/`, root `AGENTS.md`, release files, and private user-local state protected.
- Keep generated output outside live PAI, Claude, Codex, release, and runtime roots unless later authorized.
- Report unsupported surface and path gaps.

Future environment handling must not assume Anthropic env behavior maps to Codex. It must separately model auth, billing, API keys, network, sandbox, and approval posture.

## Argument and Flag Model

The future launcher must not translate Claude flags mechanically.

Claude launcher flags and behavior such as `--append-system-prompt-file`, `--resume`, `-p`, MCP profile mutation, `.mcp.json`, and Claude update commands must be treated as Claude-specific evidence.

Any future Codex invocation plan must define native arguments, stdin behavior, stdout/stderr expectations, exit-code semantics, and unsupported behavior explicitly, with tests before use.

## Authority Envelope Handoff

The launcher seam must hand off an approved `authority_envelope_id`.

Future launcher behavior must preserve:

- `PAI_SYSTEM_PROMPT.md` as high-authority PAI doctrine.
- `CLAUDE.md` as a Claude-facing surface, not a Codex destination file.
- Future `AGENTS.md`, if authorized, as a compact router that must not clone `CLAUDE.md` or `PAI_SYSTEM_PROMPT.md`.
- Codex config/profile as policy/configuration, not Life OS doctrine.
- Codex memory, transcripts, SDK threads, and `/goal` state as non-authority and not PAI Memory.

## Sandbox and Permission Handoff

The future launcher must hand off sandbox and permission policy before runtime invocation.

Required policy dimensions:

- Filesystem read roots.
- Denied read roots.
- Denied write roots.
- Network posture.
- Tool and MCP allow/deny lists.
- Approval posture.
- Protected path list.
- Failure behavior when policy is incomplete.

Claude `settings.json` must not be copied into Codex config. Security intent must be mapped by behavior and validated.

## Pulse Startup Boundary

Pulse remains central v5 infrastructure, but S7C does not design or implement a Pulse bridge.

The future launcher must not start Pulse, call Pulse endpoints, emit Pulse events, or claim Pulse parity unless explicitly authorized by a later Pulse milestone.

The future launcher must not start Pulse unless explicitly authorized by later architect-approved Pulse work.

## Memory and ISA Boundary

The future launcher must not write PAI Memory or ISA during read-only trial mode.

PAI Memory and ISA artifacts are canonical PAI state. Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory. Product memories must not be silently promoted into PAI Memory.

Future writes require a single-writer policy, provenance, rollback, and validation.

## Error and Exit-Code Model

The future launcher must define exit-code behavior explicitly.

Required future error fields:

- `engine_id`
- `adapter_mode`
- `exit_code`
- `status`
- `failure_reason`
- `stderr_summary`
- `unsupported_surface_report`
- `denied_action_report`
- `rollback_action`
- `audit_reference`

No future launcher may hide unsupported Codex or Claude behavior behind a generic success code.

## Rollback and Fallback Model

The future launcher must preserve rollback and fallback to Claude Code.

Rollback requirements:

- No release-file mutation.
- No root `AGENTS.md` or `.codex/` creation unless later authorized.
- No installer execution.
- No live PAI state write during read-only mode.
- Clear fallback path to the official Claude Code engine.
- Audit record of selected engine, denied actions, unsupported surfaces, and rollback state.

## Candidate Launcher Seam Designs

| Candidate | Summary | Inputs | Outputs | Safety | Reversibility | Drop-in readiness | Main risk | Required future proofs | S7C decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LS-1 | Documentation-only engine selection contract. | S7C specs, S6 seams, S7A authority envelope design. | Future contract fields and gate list. | Safe because it creates no runtime artifact. | Fully reversible; docs only. | Prerequisite design only. | Too abstract without later fixture validation. | Contract completeness, review approval, no-write proof. | Design candidate only; no runtime implementation chosen. |
| LS-2 | Future manifest-mediated launcher plan. | Approved manifest, source kind, authority envelope, sandbox policy, rollback policy. | Non-executable invocation plan and denied behavior report. | Safer for read-only trials because mode and roots are explicit. | Reversible if generated plan stays quarantined and non-runtime. | Candidate for fixture and read-only validation. | Manifest drift or path misbinding. | Manifest validation, path proof, no-Pulse-start proof, no-write proof. | Deferred; no runtime implementation chosen. |
| LS-3 | Future profile-mediated launcher wrapper. | Future engine profile, Codex config/profile policy, launcher seam tests. | Engine-selectable wrapper behavior. | Highest risk because it approaches runtime invocation. | Requires rollback and fallback proof before use. | Candidate for later replacement-capable mode only. | Wrapper could become an unreviewed runtime adapter. | Authority, launcher, inference, sandbox, Pulse, Memory, ISA, and rollback proofs. | Deferred; no runtime implementation chosen. |

S7C chooses no runtime implementation for `LS-1`, `LS-2`, or `LS-3`.

## Required Future Proofs

Future launcher work must prove:

- Engine selection is explicit.
- Release files are not mutated.
- Claude Code remains installed and recoverable.
- Authority envelope boundaries are preserved.
- Paths are resolved without private user-local state inspection unless approved.
- Read-only mode cannot write PAI Memory, ISA, Pulse state, `.claude`, `.codex`, root `AGENTS.md`, or release files.
- Pulse is not started unless later authorized.
- Unsupported surfaces are reported.
- Exit-code behavior is deterministic.
- Rollback path is tested.

## Prohibited Launcher Designs

Prohibited launcher designs:

- Editing `pai.ts` in S7C.
- Creating a runtime launcher or wrapper in S7C.
- Copying Claude flags directly into a Codex invocation.
- Creating root `AGENTS.md`.
- Creating `.codex/`.
- Creating Codex config/profile.
- Mutating `.claude` or release files.
- Running installers.
- Invoking Claude Code.
- Invoking Codex as a runtime engine.
- Starting or contacting Pulse.
- Writing PAI Memory or ISA.
- Proposing installation of any launcher, wrapper, engine profile, or inference adapter.

## Non-Goals

S7C does not implement launcher replacement, implement a Codex adapter, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create migration scripts, create runtime files, create an engine profile instance, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, or advance beyond S7C.
