# V5 Codex Engine Profile and Capability Contract

## Purpose

Define the future engine profile and capability contract needed before PAI can decide whether Codex is eligible for read-only, assisted, or write-capable modes.

## Scope

An engine profile is future declarative metadata, not a runtime config file.

S7C creates no engine profile instance. S7C permits only documentation-only status.

This document is design-only. It does not create Codex config, root `AGENTS.md`, `.codex/`, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, migration scripts, runtime files, or adapter implementation.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`
- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`

No new Codex capability claim is introduced in S7C.

## Engine Profile Problem Statement

Codex is not currently proven drop-in for existing local PAI v5 files.

PAI needs a future way to declare what an engine can and cannot do before selecting it for read-only, assisted, controlled-write, replacement, or coexistence modes. Without an explicit engine profile and capability contract, launcher and inference seams can overclaim capability, hide unsupported surface gaps, or imply write safety before proof exists.

## Engine Identity Model

Future engine identity fields:

| Field | Meaning |
| --- | --- |
| `engine_id` | Stable identifier for the engine or adapter candidate. |
| `engine_name` | Human-readable engine name. |
| `engine_kind` | Engine family such as official Claude Code, Codex candidate, or future adapter. |
| `adapter_status` | Maturity label for the adapter. S7C permits only documentation-only. |
| `supported_modes` | Explicit list of modes that have proof. |
| `proof_artifacts` | References to approved evidence, tests, audits, or gates. |
| `rollback_support` | Declared fallback and restore capability. |

Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Capability Declaration Model

Required future fields:

- `engine_id`
- `engine_name`
- `engine_kind`
- `adapter_status`
- `supported_modes`
- `authority_capabilities`
- `launcher_capabilities`
- `inference_capabilities`
- `tool_capabilities`
- `sandbox_capabilities`
- `memory_capabilities`
- `isa_capabilities`
- `pulse_capabilities`
- `audit_capabilities`
- `unsupported_surfaces`
- `proof_artifacts`
- `rollback_support`

The capability contract must report unsupported surface gaps explicitly.

Unsupported surfaces must be reported explicitly by any future engine profile evidence.

## Unsupported Surface Reporting

Unsupported surfaces must be reported explicitly.

The rule is direct: unsupported surfaces must be reported explicitly.

Required unsupported surface categories:

- Authority ordering gaps.
- Launcher invocation gaps.
- Inference request/response gaps.
- Claude flag or CLI behavior gaps.
- Tool and MCP gaps.
- Sandbox and permission gaps.
- PAI Memory gaps.
- ISA gaps.
- Pulse gaps.
- Rollback gaps.
- Existing-local-v5 read-only gaps.

Missing Pulse, Memory, ISA, launcher, or inference proofs block drop-in claims.

## Authority Capability Fields

Future authority capability fields:

| Field | Meaning |
| --- | --- |
| `authority_envelope_supported` | Whether an approved authority envelope is supported. |
| `pai_system_prompt_priority_proven` | Whether `PAI_SYSTEM_PROMPT.md` high-authority semantics are proven. |
| `compact_router_supported` | Whether future `AGENTS.md` compact router behavior is supported. |
| `claude_md_not_copied_proven` | Whether `CLAUDE.md` non-copy behavior is proven. |
| `codex_config_is_policy_only` | Whether Codex config/profile is kept out of Life OS doctrine. |

`PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown. `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file. Future Codex `AGENTS.md`, if later authorized, must be a compact router and must not clone `CLAUDE.md` or `PAI_SYSTEM_PROMPT.md`.

## Launcher Capability Fields

Future launcher capability fields:

| Field | Meaning |
| --- | --- |
| `engine_selection_supported` | Whether the engine can be selected by policy. |
| `path_resolution_supported` | Whether `pai_dir` and source roots are resolved safely. |
| `invocation_plan_supported` | Whether an invocation plan can be produced. |
| `exit_code_model_supported` | Whether exit-code behavior is defined. |
| `rollback_supported` | Whether fallback and restore are proven. |
| `no_release_mutation_proven` | Whether release files remain unchanged. |

## Inference Capability Fields

Future inference capability fields:

| Field | Meaning |
| --- | --- |
| `request_envelope_supported` | Whether request envelope validation exists. |
| `response_envelope_supported` | Whether response envelope validation exists. |
| `streaming_supported` | Whether streaming behavior is defined and tested. |
| `non_streaming_supported` | Whether buffered output behavior is defined and tested. |
| `error_model_supported` | Whether errors, timeouts, and retries are classified. |
| `unsupported_surface_reporting_supported` | Whether unsupported surfaces are reported. |

## Tool and MCP Capability Fields

Future tool and MCP fields:

| Field | Meaning |
| --- | --- |
| `allowed_tools_supported` | Whether allowed tools are explicit. |
| `denied_tools_supported` | Whether denied tools are explicit. |
| `mcp_policy_supported` | Whether MCP access is explicit and bounded. |
| `claude_tool_emulation_blocked` | Whether silent Claude tool emulation is blocked. |

Tool and MCP behavior must be bounded and cannot silently emulate Claude behavior.

## Sandbox and Permission Capability Fields

Future sandbox and permission fields:

| Field | Meaning |
| --- | --- |
| `sandbox_policy_supported` | Whether sandbox posture is explicit. |
| `permission_policy_supported` | Whether approval and permission posture is explicit. |
| `protected_paths_supported` | Whether protected paths are enforced or reported. |
| `network_policy_supported` | Whether network posture is explicit. |
| `codex_config_status` | Whether Codex config is absent, generated, or approved. S7C creates none. |

Claude `settings.json` must not be copied directly into Codex config.

## Memory Capability Fields

Future memory fields:

| Field | Meaning |
| --- | --- |
| `pai_memory_read_status` | Whether PAI Memory reads are denied, fixture-only, or approved. |
| `pai_memory_write_status` | Must remain blocked until single-writer policy exists. |
| `product_memory_boundary_supported` | Whether Codex and Claude product memories stay non-canonical. |
| `non_promotion_supported` | Whether product memories cannot be silently promoted. |

Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.

## ISA Capability Fields

Future ISA fields:

| Field | Meaning |
| --- | --- |
| `isa_read_status` | Whether ISA reads are denied, fixture-only, or approved. |
| `isa_write_status` | Must remain blocked until single-writer policy exists. |
| `isa_acceptance_supported` | Whether acceptance semantics are proven. |
| `goal_state_separation_supported` | Whether `/goal` state is kept separate from ISA. |

PAI Memory and ISA artifacts are canonical PAI state.

## Pulse Capability Fields

Future Pulse fields:

| Field | Meaning |
| --- | --- |
| `pulse_startup_status` | Must remain blocked unless later Pulse milestone approves. |
| `pulse_event_status` | Whether event identity is designed and tested. |
| `pulse_job_identity_status` | Whether Codex job identity is distinct from Claude job identity. |
| `pulse_parity_claim_status` | Must remain blocked until bridge proof exists. |

Pulse remains central v5 infrastructure, but S7C does not design or implement a Pulse bridge.

## Audit and Provenance Capability Fields

Future audit fields:

| Field | Meaning |
| --- | --- |
| `audit_envelope_supported` | Whether every launch/inference action is auditable. |
| `provenance_supported` | Whether source, engine, mode, and policy are recorded. |
| `denied_action_reporting_supported` | Whether denied action reports are emitted. |
| `unsupported_surface_reporting_supported` | Whether unsupported surface gaps are emitted. |
| `rollback_audit_supported` | Whether fallback and rollback are recorded. |

## Mode Eligibility Rules

Allowed future `supported_modes` values:

- `documentation-only`
- `fixture-read-only`
- `existing-local-v5-read-only`
- `assisted-patch`
- `controlled-single-writer`
- `codex-only-replacement`
- `dual-engine-coexistence`

S7C permits only documentation-only status.

Mode eligibility:

| Mode | S7C eligibility | Required future proof |
| --- | --- | --- |
| `documentation-only` | Permitted in S7C. | Approved docs and validation checks. |
| `fixture-read-only` | Not permitted in S7C. | Fixture, manifest, sandbox, no-write, audit proof. |
| `existing-local-v5-read-only` | Not permitted in S7C. | Existing-local-v5 manifest, path, privacy, rollback, and no-write proof. |
| `assisted-patch` | Not permitted in S7C. | Human-mediated patch policy and protected-path tests. |
| `controlled-single-writer` | Not permitted in S7C. | Single-writer policy, provenance, rollback, and validation. |
| `codex-only-replacement` | Not permitted in S7C. | All drop-in gates and rollback proof. |
| `dual-engine-coexistence` | Not permitted in S7C. | Product memory separation, engine labels, single-writer ownership. |

## Compatibility Scoring Model

Compatibility scoring is future evaluation only.

A future score must be gate-based, not a subjective percentage. Missing authority, launcher, inference, Pulse, Memory, ISA, existing-local-v5 read-only, single-writer, or rollback proof blocks drop-in claims.

S7C cannot mark Codex as drop-in-capable.

## Required Future Proofs

Future engine profile work must prove:

- Engine identity is explicit.
- Supported modes are evidence-backed.
- Unsupported surfaces are reported.
- Launcher seam proof exists.
- Inference seam proof exists.
- Authority envelope proof exists.
- Pulse no-start or bridge proof exists.
- PAI Memory and ISA safety proof exists.
- Rollback proof exists.
- Any write-capable mode has single-writer policy.
- Any write-capable mode requires single-writer policy, provenance, rollback, and validation.

## Prohibited Capability Claims

Prohibited capability claims:

- Codex is drop-in today.
- Codex is the official upstream engine.
- Codex can copy Claude-shaped files directly into Codex surfaces.
- Claude Code can be uninstalled as a prerequisite.
- PAI Memory writes are safe without single-writer policy.
- ISA writes are safe without single-writer policy.
- Pulse implementation or parity exists in S7C.
- Existing-local-v5 trial execution is authorized in S7C.
- An engine profile instance exists in S7C.
- Launcher, wrapper, engine profile, or inference adapter installation is proposed by S7C.

## Non-Goals

S7C does not create an engine profile instance, create Codex config, create root `AGENTS.md`, create `.codex/`, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create migration scripts, create runtime files, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, or advance beyond S7C.
