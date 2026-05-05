# V5 Codex Inference Seam Spec

## Purpose

Define the future inference seam that would let PAI v5 delegate model calls to Codex-native mechanisms without assuming Claude CLI behavior.

## Scope

The inference seam is a future model-call abstraction, not an implementation.

This document defines inference seam as a future model-call abstraction, not an implementation.

S7C designs launcher and inference seams only. It does not implement inference replacement, create an inference adapter, create a runtime wrapper, create an engine profile instance, create Codex config, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create migration scripts, create runtime files, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, invoke Claude Code, invoke Codex as a runtime engine, or run Codex import or migration tooling.

## Evidence Base

Evidence comes from:

- `Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts`
- `Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts`
- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_ENVELOPE_VALIDATION_SPEC.md`
- `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`

No new Codex capability claim is introduced in S7C. Codex noninteractive, CLI, SDK, config, sandbox, and approval facts are inherited from S2/S3/S7A official-source evidence.

## Inference Problem Statement

Codex is not currently proven drop-in for existing local PAI v5 files.

`Inference.ts` is a Claude CLI subprocess wrapper, not an engine-neutral provider contract. Future Codex replacement requires a designed adapter with a request envelope, response envelope, audit envelope, unsupported surface reporting, and state boundaries.

Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Existing Claude Inference Couplings

Observed inference assumptions from `Inference.ts`, S6, and S7A evidence:

| Coupling | Evidence | Replacement hazard |
| --- | --- | --- |
| Claude executable | Uses `spawn('claude', args, ...)`. | Codex cannot be substituted without a provider boundary. |
| Claude model names | Maps `fast`, `standard`, and `smart` to `haiku`, `sonnet`, and `opus`. | Codex model/runtime reporting cannot reuse Claude tier names as proof. |
| Claude flags | Uses `--print`, `--model`, `--tools`, `--allowedTools`, `--output-format`, `--exclude-dynamic-system-prompt-sections`, `--setting-sources`, and `--system-prompt`. | Codex-native arguments and semantics require explicit future proof. |
| Stdin prompt passing | Writes user prompt to stdin to avoid argument limits. | Future stdin/stdout behavior must be modeled, not assumed. |
| Stdout parsing | Treats trimmed stdout as model output and extracts JSON with regex candidates. | Codex output framing may differ and needs a response envelope. |
| Stderr and exit handling | Nonzero close code returns `stderr` or process code as error. | Future exit-code and error classification must be deterministic. |
| Timeout behavior | Kills process on timeout with `SIGTERM`. | Runtime timeout and retry policy need future engine contract. |
| Auth and billing | Deletes `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, and `CLAUDECODE`. | Codex auth and billing boundaries cannot inherit Anthropic-specific logic. |
| Advisor mode | Uses the same inference path for advisor escalation and can read ISA from live PAI paths. | Future Codex inference must not read private user-local state or write ISA without policy. |
| Image paths | Enables Claude `Read` tool for image path references. | Tool allowlists and context sources require native Codex policy. |

## Inference Seam Principles

Principles:

- Model calls pass through explicit request envelope and response envelope contracts.
- Unsupported surface behavior is reported, not hidden.
- Claude CLI flags are evidence, not portable API.
- Tool and MCP behavior is bounded and cannot silently emulate Claude behavior.
- Authority envelope ID is explicit.
- PAI Memory and ISA writes are blocked in read-only mode.
- Codex memory must not be promoted into PAI Memory.
- Pulse actions are blocked unless later authorized.
- Audit and provenance are required for every future model-call path.
- Future write-capable modes require single-writer policy, provenance, rollback, and validation.

## Request Envelope Model

Required future request fields:

| Field | Meaning |
| --- | --- |
| `request_id` | Stable inference request identifier. |
| `engine_id` | Selected engine identifier. |
| `adapter_mode` | Requested adapter mode. S7C permits documentation-only only. |
| `authority_envelope_id` | Approved authority envelope for the request. |
| `prompt_source` | Source of the prompt or task. |
| `context_sources` | Explicitly approved context roots or documents. |
| `allowed_tools` | Tool names or classes explicitly allowed. |
| `denied_tools` | Tool names or classes explicitly denied. |
| `memory_policy` | PAI Memory and product memory boundaries. |
| `isa_policy` | ISA read/write and acceptance boundaries. |
| `pulse_policy` | Pulse no-start, no-call, or future bridge policy. |
| `audit_policy` | Required audit and provenance output. |
| `output_policy` | Output format, JSON, streaming, and classification policy. |

## Response Envelope Model

Required future response fields:

| Field | Meaning |
| --- | --- |
| `request_id` | Echo of request ID. |
| `engine_id` | Engine that produced or attempted the response. |
| `status` | `success`, `failure`, `blocked`, or `unsupported`. |
| `model_or_runtime_report` | Engine/model/runtime metadata without overclaiming parity. |
| `output` | Produced output, if allowed. |
| `unsupported_surface_report` | Unsupported Claude or Codex surfaces encountered. |
| `denied_action_report` | Denied tools, writes, Pulse actions, or path access. |
| `memory_write_status` | Must be `not-requested`, `blocked`, or future approved status. |
| `isa_write_status` | Must be `not-requested`, `blocked`, or future approved status. |
| `pulse_action_status` | Must report no-start/no-call unless later authorized. |
| `provenance` | Source and engine trace for audit review. |
| `failure_reason` | Structured failure reason when not successful. |

## Streaming and Non-Streaming Model

Streaming and non-streaming are future compatibility dimensions.

Future inference design must define:

- Whether output is streamed, buffered, or both.
- Whether partial output is auditable.
- How cancellation and timeout are represented.
- How stdout, stderr, and exit-code behavior map into a response envelope.
- Whether JSON output is validated structurally rather than extracted opportunistically.

S7C does not run or implement either mode.

## Error and Retry Model

Future errors must be classified explicitly:

- Invocation blocked.
- Unsupported surface.
- Invalid request envelope.
- Authority envelope missing.
- Sandbox or permission denied.
- Timeout.
- Nonzero exit-code.
- Output parse failure.
- Tool denied.
- Memory write denied.
- ISA write denied.
- Pulse action denied.

Retry must not bypass denied actions, read-only posture, authority envelope constraints, or protected paths.

## Tool and MCP Boundary

Tool and MCP behavior must be bounded and cannot silently emulate Claude behavior.

Future request envelopes must list allowed and denied tools. A missing or ambiguous tool policy must fail closed. Claude tool names, MCP profile files, and `settings.json` permissions must not be copied directly into Codex surfaces.

## Authority and Context Boundary

Future inference must receive `authority_envelope_id` and approved context sources.

`PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown. `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file. Future Codex `AGENTS.md`, if later authorized, must be a compact router and must not clone `CLAUDE.md` or `PAI_SYSTEM_PROMPT.md`.

Codex config/profile is policy/configuration, not Life OS doctrine.

## Memory and ISA Boundary

Inference must not promote Codex memory into PAI Memory.

Inference must not write ISA or PAI Memory in read-only mode.

Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory. PAI Memory and ISA artifacts are canonical PAI state. Product memories must not be silently promoted into PAI Memory.

## Pulse Boundary

Pulse remains central v5 infrastructure, but S7C does not design or implement a Pulse bridge.

Future inference must not start Pulse, call Pulse endpoints, write Pulse state, claim Pulse parity, or overload Claude Pulse job identity unless later authorized.

## Audit and Provenance Boundary

Every future inference response must be auditable.

Audit and provenance must record:

- `request_id`
- `engine_id`
- `adapter_mode`
- `authority_envelope_id`
- Context sources used and omitted.
- Tool and MCP decisions.
- Unsupported surface report.
- Denied action report.
- Memory, ISA, and Pulse statuses.
- Exit-code and failure classification.
- Rollback or fallback implications.

## Candidate Inference Seam Designs

| Candidate | Summary | Inputs | Outputs | Safety | Reversibility | Drop-in readiness | Main risk | Required future proofs | S7C decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IS-1 | Documentation-only inference envelope contract. | S7C request and response fields, S6/S7A authority and seam docs. | Future provider contract without executable behavior. | Safe because it creates no runtime artifact. | Fully reversible; docs only. | Prerequisite design only. | Too abstract without future validation. | Field completeness, unsupported surface review, no-write proof. | Design candidate only; no runtime implementation chosen. |
| IS-2 | Future manifest-mediated noninteractive inference plan. | Approved manifest, authority envelope, context roots, sandbox and output policies. | Non-executable plan for future fixture/read-only inference. | Safer because policy is explicit before model call. | Reversible if generated plan remains quarantined and non-runtime. | Candidate for read-only validation. | Manifest or context source drift. | Manifest validation, source inventory, timeout/error tests, no-write proof. | Deferred; no runtime implementation chosen. |
| IS-3 | Future engine adapter interface with audit envelope. | Engine profile, request envelope, response envelope, audit policy. | Runtime abstraction between PAI and engine-specific providers. | Highest risk because it approaches implementation. | Requires rollback and fallback proof before use. | Candidate for later replacement-capable mode. | Adapter could silently emulate Claude or hide unsupported surfaces. | Provider tests, output tests, tool denial, Memory/ISA/Pulse proof, rollback. | Deferred; no runtime implementation chosen. |

S7C chooses no runtime implementation for `IS-1`, `IS-2`, or `IS-3`.

## Required Future Proofs

Future inference work must prove:

- Request envelope validation.
- Response envelope validation.
- Unsupported surface reporting.
- Deterministic exit-code and error mapping.
- Tool and MCP allow/deny behavior.
- Authority envelope preservation.
- No PAI Memory writes in read-only mode.
- No ISA writes in read-only mode.
- No Pulse startup or call.
- No silent product memory promotion.
- Reversible behavior and audit provenance.

## Prohibited Inference Designs

Prohibited designs:

- Editing `Inference.ts` in S7C.
- Creating an inference adapter in S7C.
- Treating Claude model names as Codex compatibility proof.
- Translating Claude flags mechanically into Codex flags.
- Copying Claude-shaped settings, tool, MCP, or command behavior into Codex surfaces.
- Promoting Codex memory into PAI Memory.
- Writing PAI Memory or ISA in read-only mode.
- Starting or contacting Pulse.
- Invoking Claude Code.
- Invoking Codex as a runtime engine.
- Proposing installation of any launcher, wrapper, engine profile, or inference adapter.

## Non-Goals

S7C does not implement inference replacement, implement a Codex adapter, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create migration scripts, create runtime files, create an engine profile instance, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, or advance beyond S7C.
