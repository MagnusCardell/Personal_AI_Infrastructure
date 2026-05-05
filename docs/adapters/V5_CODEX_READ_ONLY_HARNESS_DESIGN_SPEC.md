# V5 Codex Read-Only Harness Design Spec

## Purpose

Define the future read-only harness design without implementing a harness.

## Scope

S9B creates no harness.

This document is design-only. It does not create harness files, fixture files, manifests, audit artifacts, executable schemas, generated configs, runtime files, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, trial outputs, root `AGENTS.md`, or `.codex/`.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement is plausible only through a designed adapter. Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_SEQUENCE_AND_GATE_MODEL.md`
- `docs/adapters/V5_CODEX_FIXTURE_TRIAL_COVERAGE_MATRIX.md`
- `docs/adapters/V5_CODEX_TRIAL_FAILURE_ROLLBACK_AND_AUDIT_MODEL.md`
- `docs/adapters/V5_CODEX_FIXTURE_CORPUS_DESIGN_SPEC.md`
- S7A, S7C, S7D, S7E, and S8H seam docs.

No new Codex capability claim is introduced in S9B.

## Harness Design Status

The read-only harness is proposed only. S9B does not create a harness, harness script, harness README, harness test file, manifest, schema, audit artifact, or trial output.

Future S10A may create a harness only after architect approval. S10A is not approved by S9B.

## Harness Design Principles

Principles:

- Read-only.
- Fixture-only.
- No live user-local state.
- No runtime invocation.
- No Claude Code invocation.
- No Codex runtime invocation unless separately approved.
- No Pulse startup or endpoint call.
- No PAI Memory writes.
- No ISA writes.
- No root `AGENTS.md`.
- No `.codex/`.
- No release mutation.
- No direct Claude-file copy into Codex surfaces.
- Fail closed on missing denial or unsupported-surface reports.

## Harness Responsibility Model

Future harness responsibilities:

- Validate fixture root is approved.
- Validate fixture metadata exists.
- Validate protected paths are absent or untouched.
- Validate root `AGENTS.md` and `.codex/` are not created.
- Validate no release file writes.
- Validate no live user-local paths.
- Validate no direct Claude-file copy into Codex surfaces.
- Validate no-start/no-call Pulse posture.
- Validate PAI Memory and ISA no-write posture.
- Validate product-memory non-promotion.
- Validate `denied_action_report`.
- Validate `unsupported_surface_report`.
- Validate audit provenance reporting.
- Validate rollback/no-residue reporting.

## Harness Non-Responsibility Model

The future harness must not:

- Implement a runtime adapter.
- Invoke Claude Code.
- Invoke Codex as a runtime engine unless separately approved.
- Start Pulse.
- Call Pulse endpoints.
- Probe `localhost:31337`.
- Write PAI Memory.
- Write ISA.
- Read live `~/.claude/PAI`.
- Read live `~/.codex`.
- Create root `AGENTS.md`.
- Create `.codex/`.
- Create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, or migration scripts.
- Promote product memories into PAI Memory.
- Claim drop-in readiness.

## Harness Input Model

Future harness inputs:

- Fixture root.
- Fixture metadata.
- Proposed manifest.
- Coverage matrix.
- Expected-denial catalog.
- Protected-path catalog.
- Audit field requirements.

S9B creates none of these input files.

## Harness Output Model

Future harness outputs:

- Validation report.
- Denied-action report.
- Unsupported-surface report.
- No-write proof report.
- No-private-state proof report.
- Pulse no-start/no-call report.
- Memory/ISA no-write report.
- Rollback/no-residue report.

Future output must be advisory only and not PAI Memory, ISA, Pulse state, Claude memory, or Codex memory.

## Harness Check Catalog

| Check ID | Check area | Purpose | Input evidence | Expected result | Failure signal | Future implementation status |
| --- | --- | --- | --- | --- | --- | --- |
| HC-001 | Fixture root | Approved fixture root only. | Fixture metadata and approved path catalog. | Fixture root is under approved future path. | Live or unapproved root used. | Proposed / requires architect approval. |
| HC-002 | Private state | No live user-local paths. | Fixture metadata and path scan. | No `~/.claude`, `~/.codex`, or private roots. | Live user-local path detected. | Proposed / requires architect approval. |
| HC-003 | Router surface | No root `AGENTS.md`. | Path catalog. | Root `AGENTS.md` absent or untouched. | Root `AGENTS.md` created or modified. | Proposed / requires architect approval. |
| HC-004 | Codex surface | No `.codex/`. | Path catalog. | `.codex/` absent or untouched. | `.codex/` created or modified. | Proposed / requires architect approval. |
| HC-005 | Release safety | No release file writes. | Git status and path catalog. | `Releases/` unchanged. | Release file write or mutation. | Proposed / requires architect approval. |
| HC-006 | Direct-copy safety | No Claude file direct-copy into Codex surfaces. | Fixture metadata and content classification. | Claude-shaped files are source evidence only. | `CLAUDE.md`, hooks, settings, skills, agents, or commands copied into Codex surfaces. | Proposed / requires architect approval. |
| HC-007 | Authority | Authority doctrine reference preserved. | Authority fixture metadata. | `PAI_SYSTEM_PROMPT.md` stays high-authority doctrine. | Doctrine omitted, demoted, or treated as ordinary markdown. | Proposed / requires architect approval. |
| HC-008 | Router | Compact router remains non-installed. | Router fixture metadata. | Router is absent or explicitly non-installable design material. | Root router file installed. | Proposed / requires architect approval. |
| HC-009 | Launcher | Launcher plan remains non-executable. | Launcher fixture metadata. | No launcher, wrapper, or process invocation exists. | Runtime command path created or executed. | Proposed / requires architect approval. |
| HC-010 | Inference | Inference plan remains non-executable. | Inference fixture metadata. | No Codex or Claude model call occurs. | Runtime inference call or Claude CLI use. | Proposed / requires architect approval. |
| HC-011 | Hook lifecycle | Hook lifecycle mapping remains non-executable. | Hook fixture metadata. | No hook, rule, or config is installed or run. | Hook/rule file created or hook command run. | Proposed / requires architect approval. |
| HC-012 | Pulse | Pulse no-start. | Pulse fixture metadata and process policy. | Pulse startup status is none or denied. | Pulse startup attempt. | Proposed / requires architect approval. |
| HC-013 | Pulse | Pulse no-call. | Pulse fixture metadata and endpoint policy. | Pulse endpoint call status is none or denied. | Endpoint call or `localhost:31337` probe. | Proposed / requires architect approval. |
| HC-014 | Memory | PAI Memory no-write. | Memory fixture metadata. | `memory_write_status` is none or denied. | PAI Memory write or unreported write attempt. | Proposed / requires architect approval. |
| HC-015 | ISA | ISA no-write. | ISA fixture metadata. | `isa_write_status` is none or denied. | ISA write or unreported write attempt. | Proposed / requires architect approval. |
| HC-016 | Product memory | Product-memory non-promotion. | Product memory negative fixture. | Product memories remain not PAI Memory. | Promotion into PAI Memory. | Proposed / requires architect approval. |
| HC-017 | Unsupported surfaces | Unsupported-surface reporting. | Unsupported-surface fixture. | `unsupported_surface_report` is present and complete. | Unsupported gap silently ignored. | Proposed / requires architect approval. |
| HC-018 | Denied actions | Denied-action reporting. | Expected-denial catalog. | `denied_action_report` is present and complete. | Denied action missing or allowed. | Proposed / requires architect approval. |
| HC-019 | Audit | Audit provenance reporting. | Audit field requirements. | Provenance fields are present in advisory output. | Missing provenance. | Proposed / requires architect approval. |
| HC-020 | Rollback | Rollback/no-residue reporting. | Rollback fixture metadata. | No-residue report is present. | Residue detected or rollback status missing. | Proposed / requires architect approval. |

## Authority Checks

Authority checks must prove `PAI_SYSTEM_PROMPT.md` remains high-authority doctrine and `CLAUDE.md` remains a Claude-facing source, not a Codex destination file. Future Codex `AGENTS.md`, if later authorized, must be a compact router.

## Launcher and Inference Checks

Launcher and inference checks must remain non-executable. The harness must not create launchers, wrappers, request executors, runtime files, or model-call adapters.

## Hook and Lifecycle Checks

Hook and lifecycle checks must inspect fixture metadata only. They must not execute Claude hooks, create Codex hooks, create Codex rules, create Codex config, run Codex hook commands, run Codex rule commands, or run execpolicy commands.

## Pulse Checks

Pulse is central v5 infrastructure. Future harness checks must prove Pulse no-start and Pulse no-call. The harness must not call Pulse endpoints, probe `localhost:31337`, create Pulse payloads, or claim Pulse parity.

## Memory and ISA Checks

PAI Memory and ISA artifacts are canonical PAI state. Future harness checks must prove PAI Memory no-write, ISA no-write, product memories not PAI Memory, and single-writer mode not entered.

## Protected Path Checks

Protected path checks must include `Releases/`, `.claude/`, `PAI/`, `CLAUDE.md`, `AGENTS.md`, `.codex/`, `install.sh`, `PAI_SYSTEM_PROMPT.md`, `settings.json`, `hooks/`, `skills/`, `subagents/`, `agents/`, `commands/`, `.github/`, and `.agents/`.

## Unsupported Surface Checks

Unsupported surface checks must require `unsupported_surface_report` for unmapped authority, router, launcher, inference, hook lifecycle, Pulse, Memory, ISA, manifest, audit, schema, rollback, product memory, and dual-engine surfaces.

## Rollback and No-Residue Checks

Rollback/no-residue checks must report repository residue, protected-path residue, live user-local residue, Pulse state, Memory writes, ISA writes, root `AGENTS.md`, `.codex/`, generated runtime config, hidden temp artifacts, and drop-in claim status.

## Required Future Proofs

Required future proofs:

- Harness is read-only.
- Harness uses approved fixture root only.
- Harness reads no live user-local state.
- Harness invokes no Claude Code and no Codex runtime unless separately approved.
- Harness starts no Pulse and calls no Pulse endpoints.
- Harness writes no PAI Memory and no ISA.
- Harness produces advisory validation reports only.
- Harness does not become runtime adapter implementation.

## Prohibited Harness Designs

Prohibited designs:

- Creating a harness in S9B.
- Creating runtime adapter implementation.
- Creating Codex config, hooks, rules, launchers, wrappers, or generated configs.
- Reading live user-local state.
- Invoking Claude Code.
- Invoking Codex runtime without separate approval.
- Starting Pulse or calling Pulse endpoints.
- Writing PAI Memory or ISA.
- Promoting product memories into PAI Memory.
- Claiming Codex is drop-in today.

## Non-Goals

S9B does not implement the adapter, approve S10A, create fixtures, create a test harness, create manifests, create audit artifacts, create executable schemas, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create generated configs, create migration scripts, create runtime files, create adapter payloads, create Memory payloads, create ISA payloads, create Pulse payloads, create trial outputs, create fixture files, create harness files, run a read-only trial, inspect private user-local state, read live existing-local-v5 state, modify release files, start Pulse, call Pulse endpoints, probe `localhost:31337`, run installers, invoke Claude Code, invoke Codex as a runtime engine, run Codex import or migration tooling, run Codex hook/rule/execpolicy commands, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, imply Claude-shaped files can be copied directly into Codex surfaces, authorize product-memory promotion into PAI Memory, authorize dual-engine uncoordinated writes, or advance beyond S9B.
