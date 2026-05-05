# V5 Codex Trial Failure Rollback and Audit Model

## Purpose

Define future failure handling, rollback/no-residue requirements, and audit reporting for an integrated read-only fixture trial.

## Scope

This document is design-only. S9A creates no audit artifact, fixture, harness, manifest, executable schema, generated config, runtime file, adapter payload, Memory payload, ISA payload, Pulse payload, trial output, root `AGENTS.md`, or `.codex/`.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement is plausible only through a designed adapter. Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CODEX_TRIAL_AUDIT_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_SCHEMA_DRY_RUN_VALIDATION_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_OBSERVABILITY_AND_AUDIT_SPEC.md`
- `docs/adapters/V5_CODEX_MEMORY_ISA_AUDIT_AND_CONFLICT_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_SEQUENCE_AND_GATE_MODEL.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_COVERAGE_MATRIX.md`

No new Codex capability claim is introduced in S9A.

## Failure Model Problem Statement

A future read-only fixture trial needs fail-closed behavior. Any protected-path modification, private-state access, Pulse startup, Pulse endpoint call, Memory write, ISA write, product-memory promotion, unsupported-surface silence, drop-in overclaim, missing rollback, or residue must stop the trial and block readiness claims.

S9A proves none of this; it designs the future model only.

## Failure Classification

Failure classes:

| Failure class | Meaning | S9A posture |
| --- | --- | --- |
| `scope-violation` | Future run touches outside approved scope. | Designed only. |
| `protected-path-modification` | Future run modifies protected paths. | Designed only. |
| `fixture-isolation-failure` | Future fixture reads or writes live state. | Designed only. |
| `private-state-access` | Future run inspects private user-local state. | Designed only. |
| `root-agents-write` | Future run creates or modifies root `AGENTS.md`. | Designed only. |
| `codex-surface-write` | Future run creates or modifies `.codex/` or Codex runtime surfaces. | Designed only. |
| `release-file-write` | Future run mutates release files. | Designed only. |
| `pulse-startup` | Future run starts Pulse. | Designed only. |
| `pulse-endpoint-call` | Future run calls Pulse endpoints or probes `localhost:31337`. | Designed only. |
| `memory-write` | Future run writes PAI Memory. | Designed only. |
| `isa-write` | Future run writes ISA. | Designed only. |
| `product-memory-promotion` | Future run promotes product memories into PAI Memory. | Designed only. |
| `unsupported-surface-silence` | Future run ignores unsupported behavior. | Designed only. |
| `drop-in-overclaim` | Future run claims Codex is drop-in before gates pass. | Designed only. |
| `rollback-missing` | Future run lacks rollback proof. | Designed only. |
| `residue-detected` | Future run leaves files, processes, state, or config residue. | Designed only. |

## Stop Condition Model

Future stop conditions:

- Any failure class is detected.
- Any denied action is requested and not denied.
- Any unsupported surface is omitted from report.
- Any fixture isolation condition is violated.
- Any live user-local state is read without approval.
- Any Pulse startup or endpoint call occurs.
- Any PAI Memory or ISA write occurs.
- Any product memory is promoted into PAI Memory.
- Any trial output is promoted into canonical state.
- Any drop-in claim is produced before gates pass.

## Rollback and No-Residue Model

Rollback/no-residue requirements:

- No repository writes outside approved future output path.
- No live user-local writes.
- No Pulse state.
- No PAI Memory writes.
- No ISA writes.
- No `.codex/` or root `AGENTS.md`.
- No generated runtime config.
- No hidden temp artifacts committed to repository.
- Explicit residue report.

Future rollback must prove that Claude Code remains usable and release files remain untouched.

## Audit Report Model

Audit output is future advisory reporting only. It is not PAI Memory, not ISA, not Pulse state, not Claude memory, and not Codex memory.

Required future audit fields:

| Field | Purpose |
| --- | --- |
| `audit_id` | Future advisory audit identifier. |
| `trial_id` | Future trial identifier. |
| `fixture_id` | Future fixture identifier. |
| `source_kind` | Future source class such as release fixture or sanitized fixture. |
| `engine_id` | Engine identity. |
| `adapter_mode` | Adapter mode. |
| `authority_envelope_id` | Authority envelope reference. |
| `manifest_id` | Future manifest identifier. |
| `coverage_matrix_id` | Future coverage matrix identifier. |
| `files_inspected` | Files inspected in approved scope. |
| `files_not_inspected` | Files denied or not inspected. |
| `denied_action_report` | Denied action report. |
| `unsupported_surface_report` | Unsupported surface report. |
| `pulse_action_status` | Pulse startup/call/write status. |
| `memory_write_status` | PAI Memory write status. |
| `isa_write_status` | ISA write status. |
| `product_memory_status` | Product memory non-promotion status. |
| `rollback_status` | Rollback status. |
| `residue_status` | Residue status. |
| `drop_in_claim_status` | Drop-in claim status. |
| `failure_reason` | Failure reason, if any. |
| `provenance` | Source and decision lineage. |
| `non_promotion_statement` | Statement that audit output is not canonical state. |

## Denied Action Reporting

Future `denied_action_report` must include denied writes, protected-path attempts, root `AGENTS.md` attempts, `.codex/` attempts, Pulse startup/call attempts, PAI Memory write attempts, ISA write attempts, product-memory promotion attempts, installer attempts, migration/import attempts, Claude Code invocation, Codex runtime invocation, and hook/rule/execpolicy command attempts.

## Unsupported Surface Reporting

Future `unsupported_surface_report` must list unmapped Claude surfaces, Codex surfaces, hook lifecycle gaps, Pulse gaps, Memory/ISA gaps, manifest/audit/schema gaps, rollback gaps, and coverage gaps.

Unsupported surfaces must be reported, not silently ignored.

## No-Write Reporting

Future no-write reporting must include:

- `memory_write_status`
- `isa_write_status`
- `pulse_action_status`
- Release-file write status.
- Root `AGENTS.md` write status.
- `.codex/` write status.
- Generated runtime config status.
- Trial output status.

## Pulse Reporting

Pulse is central v5 infrastructure, but S9A does not start Pulse, call Pulse endpoints, probe `localhost:31337`, create a Pulse bridge, or claim Pulse parity.

Future Pulse reporting must include no-start status, endpoint call status, write status, job status, notification status, unsupported Pulse surfaces, and rollback status.

## Memory and ISA Reporting

PAI Memory and ISA artifacts are canonical PAI state. Future reporting must include Memory read mode, Memory write status, ISA read mode, ISA write status, writer role, single-writer status, conflict status, rollback status, and non-promotion statement.

## Product Memory Reporting

Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory. Product memories must not be silently promoted into PAI Memory.

Future product memory reporting must identify product memory use, denial status, non-promotion status, and conflict risk.

## Existing Local v5 Reporting

Existing-local-v5 trial execution is not authorized in S9A.

Future reporting must state whether live local PAI state was not inspected, whether separate approval exists, which roots were allowed or denied, and whether rollback/no-residue proof exists.

## Drop-In Claim Reporting

Future audit must report that Codex is not drop-in unless all required gates pass or are explicitly waived by architect review.

S9A does not claim Codex is drop-in today and does not claim Codex is the official upstream engine.

## Required Future Proofs

Required future proofs:

- Failure classes are detected.
- Stop conditions fail closed.
- Rollback/no-residue proof exists.
- Audit fields are complete.
- Denied actions are reported.
- Unsupported surfaces are reported.
- No-write status is recorded.
- Pulse no-start/no-call status is recorded.
- PAI Memory and ISA no-write status is recorded.
- Product memory non-promotion status is recorded.
- Drop-in claim status blocks overclaim.

## Prohibited Failure and Audit Designs

Prohibited designs:

- Creating an audit artifact in S9A.
- Treating audit output as PAI Memory, ISA, Pulse state, Claude memory, or Codex memory.
- Hiding unsupported surfaces.
- Continuing after a hard failure.
- Leaving repository or user-local residue.
- Writing PAI Memory or ISA.
- Starting Pulse or calling Pulse endpoints.
- Claiming rollback is proven in S9A.
- Claiming Codex is drop-in today.

## Non-Goals

S9A does not implement the adapter, create fixtures, create a test harness, create manifests, create audit artifacts, create executable schemas, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create generated configs, create migration scripts, create runtime files, create adapter payloads, create Memory payloads, create ISA payloads, create Pulse payloads, create trial outputs, run a read-only trial, inspect private user-local state, read live existing-local-v5 state, modify release files, start Pulse, call Pulse endpoints, probe `localhost:31337`, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, run Codex hook/rule/execpolicy commands, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, authorize product-memory promotion into PAI Memory, authorize dual-engine uncoordinated writes, or advance beyond S9A.
