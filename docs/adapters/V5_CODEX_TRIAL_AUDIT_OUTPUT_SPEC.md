# V5 Codex Trial Audit Output Spec

## Purpose

Define the audit output contract a future read-only Codex trial must satisfy before its results can be reviewed.

This document is design-only. It does not create audit output, run a trial, create fixtures, create test harnesses, implement a Codex adapter, create root `AGENTS.md`, create `.codex/`, or create runtime files.

## Scope

This spec defines future audit output sections, provenance requirements, access reporting, authority reporting, memory and ISA reporting, Pulse reporting, advisory finding format, failure report format, and non-promotion rules.

It does not create audit output, run a trial, create fixtures, create a harness, or create runtime files.

## Evidence Base

This spec derives from S0/S1/S2/S3 adapter docs and the S4 manifest, path model, and authority-equivalence specs. It does not make new Codex capability claims beyond S2/S3.

Primary sources:

- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_MANIFEST_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_FIXTURE_AND_PATH_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_EQUIVALENCE_TEST_SPEC.md`

## Audit Output Role

Audit output is advisory evidence. It is not PAI Memory, not ISA, not Pulse state, not Codex memory, and not replacement readiness.

A future read-only trial is reviewable only if its audit output proves scope, provenance, authority posture, path handling, read/write boundaries, stop conditions, and non-authorization claims.

S4 does not create audit output. It defines what future audit output must contain.

**Audit output status:**

S4 does not create:

- Audit logs.
- Audit JSON.
- Audit markdown.
- Output directories.
- Transcript exports.
- Test reports.
- Fixture inventories.
- Hash manifests.
- Runtime logs.

Future audit output, if later authorized, must be written only to an approved generated-output quarantine outside live PAI, Claude, Codex, release, and runtime roots.

## Required Audit Sections

| Section | Purpose |
| --- | --- |
| `audit_identity` | Identifies the audit artifact and the manifest it evaluates. |
| `trial_summary` | States engine, mode, phase, source kind, and non-drop-in posture. |
| `source_summary` | Lists allowed sources and denied sources without exposing denied contents. |
| `authority_summary` | Records authority sources, conflict policy, and equivalence case outcomes. |
| `path_summary` | Records allowed reads, denied reads, denied writes, and path-resolution outcomes. |
| `runtime_posture_summary` | Records sandbox, approval, network, Pulse, installer, migration, and service posture. |
| `state_boundary_summary` | Records PAI Memory, ISA, Pulse, Claude memory, Codex memory, goal, and transcript boundaries. |
| `operations_summary` | Lists requested operations and whether each was allowed, denied, skipped, or stopped. |
| `findings` | Advisory observations only. |
| `proposals` | Proposed next steps only, with no applied changes. |
| `stop_conditions` | Lists triggered and non-triggered stop conditions. |
| `non_authorizations` | States what the audit does not authorize. |
| `review_requirements` | States the next architect decisions required before further work. |

## Provenance Requirements

| Field | Requirement |
| --- | --- |
| `audit_id` | Stable unique identifier. |
| `manifest_id` | Must reference the approved future manifest. |
| `audit_spec` | Must reference this spec or a later approved audit spec. |
| `created_at` | Timestamp or date. |
| `created_by_role` | Role, not personal credential. |
| `trial_phase` | Must match manifest. |
| `source_kind` | Must match manifest. |
| `audit_destination` | Must identify approved output quarantine, never live PAI roots. |

Provenance must also identify source roots, denied roots, omitted sources, manifest ID, authority source set, and whether the material was release evidence, fixture material, sanitized user fixture material, or existing local v5 read-only material.

## Manifest Echo Requirements

The audit must state:

- Codex is a candidate engine only.
- Claude Code remains the current official/full-support PAI v5.0.0 engine until replacement-grade validation exists.
- Trial mode was read-only.
- Drop-in claims were not allowed.
- Writes were not allowed.
- Trial success does not authorize assisted patch mode, single-writer mode, or Codex-only replacement.
- Trial success does not authorize implementation.

The audit must echo `allowed_read_roots`, `denied_read_roots`, `denied_write_roots`, source kind, authority policy, output policy, stop conditions, and non-authorizations from the manifest.

## Filesystem Access Reporting

The audit must list:

- Allowed read roots.
- Denied read roots.
- Denied write roots.
- Source root kinds.
- Provenance labels.
- Any source intentionally omitted.
- Any source unavailable.
- Any source excluded for privacy.
- Any source excluded because it would require Pulse, installers, migration tooling, generated config, root `AGENTS.md`, `.codex/`, or runtime surfaces.

Denied source contents must not be copied into audit output.

## Denied Path Reporting

Denied path reporting must list denied roots, denied classes, attempted denied reads, and proof that denied contents were not copied into audit output.

## Write Attempt Reporting

Write attempt reporting must classify each requested or attempted write as `denied-write`, `stopped`, `not-requested`, or `unknown`.

It must report attempts to create root `AGENTS.md`, `.codex/`, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, runtime files, test harnesses, fixtures, or migration scripts.

## Authority Mapping Reporting

The audit must record:

- Whether the authority-equivalence preconditions were satisfied.
- Which authority sources were used.
- Which authority sources were not used and why.
- Whether `PAI_SYSTEM_PROMPT.md` semantics were treated as high-authority doctrine.
- Whether any future router text was used.
- Whether any future router text was confirmed not to be a clone of `CLAUDE.md` or `PAI_SYSTEM_PROMPT.md`.
- Whether Codex product/session state was kept non-canonical.
- Conflict case outcomes.
- Truncation or omission findings.
- Unsupported authority mappings.

**Path summary requirements:**

The audit must record:

- Canonical resolved paths for allowed roots.
- Canonical resolved paths for denied roots.
- Confirmation that denied roots dominate allowed roots.
- Confirmation that write-deny covers all read roots.
- Symlink handling outcome.
- Hardlink handling outcome.
- Fixture/live-root alias checks.
- Generated-output quarantine location.
- Any path resolution ambiguity.
- Any path stop condition.

The audit must not disclose private denied path contents.

**Runtime posture summary:**

The audit must state:

- Sandbox posture used or planned.
- Approval posture used or planned.
- Network posture.
- Pulse posture.
- Installer posture.
- Migration/import tooling posture.
- Service/daemon posture.
- Hook execution posture.
- Generated config posture.

For a valid read-only trial, the expected values are:

- No write approvals.
- No network unless separately approved.
- No Pulse startup.
- No Pulse endpoint calls.
- No installer execution.
- No migration or import tooling.
- No service startup.
- No live PAI hook execution.
- No generated config.

## Memory and ISA Reporting

The audit must explicitly state:

- PAI Memory is canonical PAI state.
- ISA artifacts are canonical PAI state.
- Claude Code memory is not PAI Memory.
- Codex memory is not PAI Memory.
- Codex `/goal` state is not PAI Memory, ISA, or Pulse state.
- Codex transcripts are not PAI Memory, ISA, or Pulse state.
- Audit output is not PAI Memory, ISA, or Pulse state.
- No product memory was silently promoted into PAI Memory.
- No Codex plan, transcript, final answer, or goal completion was treated as ISA acceptance.

## Pulse Reporting

Pulse remains central v5 infrastructure, but S4 does not design or implement a Pulse bridge.

Audit output must report:

- No Pulse startup.
- No Pulse endpoint calls.
- No Pulse writes.
- No Pulse bridge implementation.
- No Pulse parity claim.

## Output Classification

Future audit output must classify every requested operation:

| Operation Outcome | Meaning |
| --- | --- |
| `allowed-read` | Operation read an explicitly allowed root. |
| `denied-read` | Operation attempted or requested a denied read and was blocked. |
| `denied-write` | Operation attempted or requested a write and was blocked. |
| `skipped` | Operation was not attempted because it was outside scope. |
| `stopped` | Operation triggered a stop condition. |
| `not-requested` | Operation did not occur. |

Operations that must be reported if requested:

- Reading PAI Memory.
- Reading ISA.
- Reading user identity.
- Reading credentials or secrets.
- Reading Claude product memory.
- Reading Codex product memory.
- Creating root `AGENTS.md`.
- Creating `.codex/`.
- Creating hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, runtime files, or test harnesses.
- Starting or contacting Pulse.
- Running installers.
- Running Codex import or migration tooling.
- Applying patches or edits.

Output classification must mark trial findings as advisory and must not classify audit output as PAI Memory, ISA, Pulse state, Codex memory, or replacement readiness.

## Advisory Finding Format

Findings must be advisory and evidence-labeled.

Each finding must include:

- Finding ID.
- Source root or source class.
- Evidence summary.
- Compatibility implication.
- State implication.
- Authority implication.
- Risk level.
- Whether the finding requires architect review.

Findings must not claim:

- Codex is drop-in.
- Codex is official upstream engine.
- Pulse parity exists.
- PAI Memory writes are safe.
- ISA writes are safe.
- Claude-shaped files can be copied directly into Codex surfaces.
- Read-only success authorizes writes.

**Proposal requirements:**

Proposals must be clearly non-applied.

Each proposal must include:

- Proposal ID.
- Target future milestone.
- Required approval.
- Expected files or surfaces if later authorized.
- State risk.
- Rollback concern.
- Explicit statement that the proposal was not applied during the read-only trial.

## Failure Report Format

The audit must include a stop-condition table:

| Stop Condition | Triggered | Evidence |
| --- | --- | --- |
| Drop-in claim attempted | yes/no | Summary only. |
| Official-engine claim attempted | yes/no | Summary only. |
| Write requested | yes/no | Summary only. |
| Denied read requested | yes/no | Summary only. |
| Pulse startup or call requested | yes/no | Summary only. |
| Installer requested | yes/no | Summary only. |
| Migration/import tooling requested | yes/no | Summary only. |
| Root `AGENTS.md` or `.codex/` creation requested | yes/no | Summary only. |
| Runtime surface creation requested | yes/no | Summary only. |
| State promotion attempted | yes/no | Summary only. |
| Manifest ambiguity found | yes/no | Summary only. |

If any triggered stop condition is `yes`, the audit must mark the trial as stopped and must not present findings as completed trial evidence.

**Required final audit verdicts:**

Future audit output must include all verdicts below:

| Verdict | Allowed Values |
| --- | --- |
| `read_only_preserved` | `yes`, `no`, `unknown` |
| `denied_paths_preserved` | `yes`, `no`, `unknown` |
| `authority_equivalence_status` | `pass`, `fail`, `blocked`, `not-run` |
| `pai_memory_unchanged` | `yes`, `no`, `unknown` |
| `isa_unchanged` | `yes`, `no`, `unknown` |
| `pulse_unchanged` | `yes`, `no`, `unknown` |
| `protected_paths_unchanged` | `yes`, `no`, `unknown` |
| `drop_in_claim_made` | `yes`, `no` |
| `write_readiness_claim_made` | `yes`, `no` |
| `next_phase_authorized` | Must be `no` for read-only audit output. |

Any `unknown` value must explain the evidence gap and require review.

## Non-Promotion Rule

Every future audit output must include:

```text
This audit is advisory evidence only. It is not PAI Memory, not ISA, not Pulse state, not Codex memory, and not replacement readiness. It does not authorize implementation, live writes, assisted patch mode, controlled single-writer mode, Codex-only replacement mode, Pulse bridge work, installer work, migration tooling, root AGENTS.md creation, .codex creation, or copying Claude-shaped files into Codex surfaces.
```

Product memories must not be silently promoted into PAI Memory. Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.

## Retention and Privacy Notes

Future audit output must not include secrets, credential contents, private denied path contents, or user-local product memory excerpts.

Audit output must be retained only in an approved generated-output quarantine outside live PAI, Claude, Codex, release, and runtime roots.

**Audit review requirements:**

Before a future audit can be accepted as evidence, reviewers must confirm:

- Manifest ID matches the trial.
- Path model was applied.
- Authority test outcomes are included.
- Denied path contents are not leaked.
- No audit output was written into live PAI roots.
- No advisory proposal is framed as an applied change.
- Final verdicts are present.
- Stop conditions are fully reported.

## Future Implementation Gates

Future implementation gates include manifest approval, path model approval, authority-equivalence test approval, audit output format approval, privacy review, generated-output quarantine approval, and architect approval.

## Non-Goals

This spec does not authorize audit output creation, output directory creation, trial execution, fixture creation, harness creation, runtime execution, adapter implementation, root `AGENTS.md`, `.codex/`, generated configs, private-state inspection, Pulse startup, installer execution, migration tooling, writes, or movement beyond S4.
