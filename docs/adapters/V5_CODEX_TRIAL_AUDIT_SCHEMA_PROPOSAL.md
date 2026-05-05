# V5 Codex Trial Audit Schema Proposal

## Purpose

Define an implementation-neutral schema proposal for future PAI v5 Codex read-only trial audit output.

This document is a markdown proposal only. It does not create an executable schema file, JSON, YAML, TOML, generated config, audit artifact, manifest instance, validator, test harness, fixture, launcher, installer, wrapper, root `AGENTS.md`, `.codex/`, hook, rule, skill, subagent, agent, command, or runtime adapter file.

## Scope

This proposal translates the S4 audit output contract into machine-checkable field definitions and validation intent.

It does not choose a serialization format and does not create audit output.

S5 does not run a read-only trial and does not authorize existing-local-v5 trial execution.

## Evidence Base

Primary inputs:

- `docs/adapters/V5_CODEX_TRIAL_AUDIT_OUTPUT_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_MANIFEST_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_FIXTURE_AND_PATH_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_EQUIVALENCE_TEST_SPEC.md`

Supporting inputs:

- `docs/adapters/V5_CODEX_TRIAL_MANIFEST_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`

No new Codex capability claims are introduced in this proposal.

## Strategic Invariants

The audit schema must preserve these invariants:

- Audit output is advisory evidence only.
- Audit output is not PAI Memory, not ISA, not Pulse state, not Codex memory, and not replacement readiness.
- Codex is not currently proven drop-in for existing local PAI v5 files.
- Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
- A read-only trial must be reversible and must not write PAI state.
- `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine.
- `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
- Codex `AGENTS.md`, if later authorized, must be a compact router.
- Claude-shaped files must not be copied directly into Codex surfaces.
- PAI Memory and ISA artifacts are canonical PAI state.
- Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.
- Product memories must not be silently promoted into PAI Memory.
- Pulse remains central v5 infrastructure, but S5 does not design or implement a Pulse bridge.

## Schema Proposal Status

This audit schema proposal is not executable.

It defines field names, expected kinds, cardinality, allowed value sets, and cross-field constraints in markdown tables only.

It does not write audit artifacts and does not define a storage location. Future audit output, if later authorized, must be written only to an approved generated-output quarantine outside live PAI, Claude, Codex, release, and runtime roots.

## Top-Level Shape

| Section | Kind | Required | Cardinality | Purpose |
| --- | --- | --- | --- | --- |
| `audit_identity` | Object | Yes | One | Identifies the audit artifact and source manifest. |
| `trial_summary` | Object | Yes | One | Summarizes engine, mode, source kind, and non-drop-in posture. |
| `manifest_echo` | Object | Yes | One | Echoes manifest policies needed to review audit evidence. |
| `provenance` | Object | Yes | One | Records source roots, omitted sources, authority sources, and source kind. |
| `filesystem_access` | Object | Yes | One | Reports allowed reads, denied reads, denied writes, and path handling. |
| `authority_mapping` | Object | Yes | One | Reports authority-equivalence status and conflict outcomes. |
| `state_boundaries` | Object | Yes | One | Reports Memory, ISA, Pulse, product memory, transcript, and goal boundaries. |
| `runtime_posture` | Object | Yes | One | Reports sandbox, approval, network, Pulse, installer, migration, service, hook, and config posture. |
| `operations` | Array | Yes | Zero or more | Classifies requested operations. |
| `findings` | Array | Yes | Zero or more | Advisory observations only. |
| `proposals` | Array | Yes | Zero or more | Non-applied future proposals only. |
| `stop_conditions` | Array | Yes | One or more | Reports triggered and non-triggered stops. |
| `final_verdicts` | Object | Yes | One | Records required review verdicts. |
| `non_authorization` | Object | Yes | One | States what the audit does not authorize. |
| `review_requirements` | Array | Yes | One or more | Lists required next reviews. |

## Audit Identity Object

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `audit_id` | String | Yes | Stable identifier | Must be non-empty and unique within future audit registry. |
| `manifest_id` | String | Yes | Approved manifest ID | Must match the manifest under review. |
| `audit_spec` | String | Yes | S4/S5 or later approved audit spec path | Must identify governing audit schema. |
| `created_at` | Date or timestamp label | Yes | Implementation-defined date/time label | Must be present. |
| `created_by_role` | String | Yes | Role label | Must not contain personal credential material. |
| `trial_phase` | Enum | Yes | `release-fixture`, `sanitized-user-fixture`, `existing-local-v5-read-only` | Must match manifest. |
| `source_kind` | Enum | Yes | Same family as trial phase | Must match manifest. |
| `audit_destination` | Path label | Yes | Approved output quarantine label | Must not be live PAI, Claude, Codex, release, or runtime root. |

## Trial Summary Object

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `engine` | Enum | Yes | `codex-candidate` | Must not imply official upstream engine. |
| `official_engine_statement` | String | Yes | Must name Claude Code as current official/full-support engine | Must preserve current engine status. |
| `mode` | Enum | Yes | `read-only-trial` | Must match manifest. |
| `drop_in_claim_made` | Boolean | Yes | `false` expected | Any true value triggers review failure. |
| `write_claim_made` | Boolean | Yes | `false` expected | Any true value triggers review failure. |
| `next_phase_authorized` | Boolean | Yes | `false` only for read-only audit | Must be false. |
| `implementation_authorized` | Boolean | Yes | `false` only | Must be false. |

## Manifest Echo Object

| Field | Kind | Required | Validation Intent |
| --- | --- | --- | --- |
| `allowed_read_roots` | Array of path labels | Yes | Must echo manifest. |
| `denied_read_roots` | Array of path labels | Yes | Must echo manifest. |
| `denied_write_roots` | Array of path labels | Yes | Must echo manifest. |
| `source_kind` | Enum | Yes | Must echo manifest. |
| `authority_policy` | Summary object | Yes | Must echo authority constraints. |
| `output_policy` | Summary object | Yes | Must echo advisory-only policy. |
| `stop_conditions` | Array | Yes | Must echo manifest stop conditions. |
| `non_authorizations` | Array | Yes | Must echo manifest non-authorizations. |

## Provenance Object

| Field | Kind | Required | Validation Intent |
| --- | --- | --- | --- |
| `source_roots_used` | Array | Yes | Lists roots actually used. |
| `source_roots_omitted` | Array | Yes | Lists omitted approved roots with reasons. |
| `denied_roots_not_read` | Array | Yes | Lists denied roots without exposing contents. |
| `authority_sources_used` | Array | Yes | Lists authority sources used. |
| `authority_sources_omitted` | Array | Yes | Lists omitted authority sources with reasons. |
| `source_root_kind` | Enum | Yes | Must align with manifest source kind. |
| `private_state_handling` | Summary | Yes | Must state whether private state was excluded, sanitized, or manifest-approved. |
| `provenance_labels` | Array | Yes | Must match manifest provenance labels. |

## Filesystem Access Object

| Field | Kind | Required | Validation Intent |
| --- | --- | --- | --- |
| `allowed_reads_observed` | Array | Yes | Records reads of allowed roots only. |
| `denied_reads_requested` | Array | Yes | Records denied read attempts or `none`. |
| `denied_writes_requested` | Array | Yes | Records write attempts or `none`. |
| `path_resolution_outcome` | Enum | Yes | `pass`, `fail`, `blocked`, `not-run` | Must summarize canonicalization. |
| `symlink_outcome` | Enum | Yes | `pass`, `fail`, `blocked`, `not-run` | Must report link handling. |
| `hardlink_outcome` | Enum | Yes | `pass`, `fail`, `blocked`, `not-run` | Must report hardlink handling. |
| `fixture_live_alias_outcome` | Enum | Yes | `pass`, `fail`, `blocked`, `not-run` | Must report fixture/live alias check. |
| `generated_output_location` | Path label or enum | Yes | Approved quarantine or `not-created` | S5-derived audits default to `not-created`. |

## Authority Mapping Object

| Field | Kind | Required | Validation Intent |
| --- | --- | --- | --- |
| `authority_equivalence_status` | Enum | Yes | `pass`, `fail`, `blocked`, `not-run` | Summarizes authority-equivalence test status. |
| `pai_system_prompt_status` | Enum | Yes | `high-authority-preserved`, `failed`, `blocked`, `not-run` | Must preserve high-authority doctrine. |
| `claude_md_router_status` | Enum | Yes | `not-copied`, `failed`, `blocked`, `not-run` | Must not clone `CLAUDE.md`. |
| `agents_md_router_status` | Enum | Yes | `not-created`, `compact-router-approved`, `failed`, `blocked` | S5 default is `not-created`. |
| `conflict_case_results` | Array | Yes | Results per conflict case | Must include pass/fail/blocked. |
| `truncation_or_omission_findings` | Array | Yes | Findings or `none` | Must report omitted required doctrine. |
| `unsupported_authority_mappings` | Array | Yes | Unsupported mappings or `none` | Must stay visible. |

## State Boundaries Object

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `pai_memory_status` | Enum | Yes | `canonical-unchanged`, `changed`, `unknown` | Must not be changed in read-only audit. |
| `isa_status` | Enum | Yes | `canonical-unchanged`, `changed`, `unknown` | Must not be changed in read-only audit. |
| `pulse_status` | Enum | Yes | `unchanged-no-start-no-call`, `changed`, `unknown` | Must report no Pulse activity. |
| `claude_memory_status` | Enum | Yes | `not-pai-memory` | Must remain non-canonical. |
| `codex_memory_status` | Enum | Yes | `not-pai-memory` | Must remain non-canonical. |
| `codex_goal_status` | Enum | Yes | `not-pai-memory-not-isa-not-pulse` | Must remain non-canonical. |
| `transcript_status` | Enum | Yes | `audit-material-not-canonical-state` | Must remain non-canonical. |
| `product_memory_promotion` | Enum | Yes | `none`, `attempted`, `unknown` | `attempted` is failure. |

## Runtime Posture Object

| Field | Kind | Required | Expected Value |
| --- | --- | --- | --- |
| `sandbox_posture` | Enum | Yes | `read-only` or `not-run` |
| `approval_posture` | Enum | Yes | `no-write-approvals` or `not-run` |
| `network_posture` | Enum | Yes | `disabled`, `approved-exception`, or `not-run` |
| `pulse_posture` | Enum | Yes | `no-start-no-call-no-write` |
| `installer_posture` | Enum | Yes | `not-run` |
| `migration_posture` | Enum | Yes | `not-run` |
| `service_posture` | Enum | Yes | `not-started` |
| `hook_posture` | Enum | Yes | `no-live-pai-hook-execution` |
| `generated_config_posture` | Enum | Yes | `not-created` |

## Operations Array

Each operation entry must include:

| Field | Kind | Required | Validation Intent |
| --- | --- | --- | --- |
| `operation_id` | String | Yes | Stable operation label. |
| `operation_class` | Enum | Yes | Read, denied read, denied write, skipped, stopped, not requested. |
| `requested_target` | String | Yes | Target label, not secret contents. |
| `outcome` | Enum | Yes | `allowed-read`, `denied-read`, `denied-write`, `skipped`, `stopped`, `not-requested`. |
| `evidence_summary` | String | Yes | Summary without private denied contents. |
| `stop_condition_triggered` | Boolean | Yes | True if operation stopped the trial. |

## Findings Array

Each advisory finding must include:

- `finding_id`.
- `source_root_or_class`.
- `evidence_summary`.
- `compatibility_implication`.
- `state_implication`.
- `authority_implication`.
- `risk_level`.
- `architect_review_required`.

Findings must not claim drop-in compatibility, official-engine status, Pulse parity, write safety, or direct Claude-to-Codex copying.

## Proposals Array

Each non-applied proposal must include:

- `proposal_id`.
- `target_future_milestone`.
- `required_approval`.
- `expected_files_or_surfaces_if_later_authorized`.
- `state_risk`.
- `rollback_concern`.
- `not_applied_statement`.

Proposals are advisory only and must not be framed as applied changes.

## Stop Conditions Array

Each stop condition entry must include:

- `stop_condition_id`.
- `triggered`.
- `evidence_summary`.
- `required_follow_up`.

Required stop conditions include drop-in claim, official-engine claim, write request, denied read request, Pulse startup or call, installer request, migration tooling request, root `AGENTS.md` or `.codex/` creation request, runtime surface creation request, state promotion attempt, and manifest ambiguity.

## Final Verdicts Object

| Field | Required | Allowed Values |
| --- | --- | --- |
| `read_only_preserved` | Yes | `yes`, `no`, `unknown` |
| `denied_paths_preserved` | Yes | `yes`, `no`, `unknown` |
| `authority_equivalence_status` | Yes | `pass`, `fail`, `blocked`, `not-run` |
| `pai_memory_unchanged` | Yes | `yes`, `no`, `unknown` |
| `isa_unchanged` | Yes | `yes`, `no`, `unknown` |
| `pulse_unchanged` | Yes | `yes`, `no`, `unknown` |
| `protected_paths_unchanged` | Yes | `yes`, `no`, `unknown` |
| `drop_in_claim_made` | Yes | `yes`, `no` |
| `write_readiness_claim_made` | Yes | `yes`, `no` |
| `next_phase_authorized` | Yes | `no` only |

Any `unknown` value must include an evidence-gap note.

## Non-Authorization Object

The non-authorization object must state that audit output does not authorize:

- Implementation.
- Live writes.
- Assisted patch mode.
- Controlled single-writer mode.
- Codex-only replacement mode.
- Pulse bridge work.
- Installer work.
- Migration tooling.
- Root `AGENTS.md` creation.
- `.codex/` creation.
- Copying Claude-shaped files into Codex surfaces.
- Trial execution beyond the manifest scope.

## Cross-Field Rules

| Rule ID | Rule |
| --- | --- |
| AU-R001 | `manifest_id` must match the manifest under review. |
| AU-R002 | `trial_phase` and `source_kind` must match the manifest echo. |
| AU-R003 | If any stop condition is triggered, final verdict cannot present the trial as completed evidence. |
| AU-R004 | `next_phase_authorized` must be `no`. |
| AU-R005 | If `product_memory_promotion` is `attempted`, the audit fails state-boundary review. |
| AU-R006 | If `drop_in_claim_made` is `yes`, the audit fails compatibility review. |
| AU-R007 | If `write_readiness_claim_made` is `yes`, the audit fails safety review. |
| AU-R008 | Audit output must not contain private denied path contents. |
| AU-R009 | Audit output destination must not be inside live PAI, Claude, Codex, release, or runtime roots. |
| AU-R010 | Any unknown future field must fail review unless a later schema explicitly permits extensions. |

## Prohibited Schema Semantics

Future executable schema work must not encode:

- Audit output as canonical PAI state.
- Audit output as replacement readiness.
- PAI Memory writes as safe.
- ISA writes as safe.
- Pulse parity as proven.
- Read-only success as authorization for writes.
- Product memory promotion into PAI Memory.
- Codex as official upstream PAI engine.
- Codex as drop-in replacement.

## Future Implementation Gates

A future executable audit schema milestone requires:

- Architect approval.
- Serialization format decision.
- Manifest schema alignment.
- Output quarantine design.
- Privacy review.
- Denied-content redaction design.
- Final-verdict review policy.
- Dry-run validation results.

## Non-Goals

This proposal does not create executable schema files, JSON, YAML, TOML, generated config, fixture material, manifest instances, audit artifacts, validators, test harnesses, runtime adapter files, root `AGENTS.md`, `.codex/`, hooks, rules, skills, subagents, agents, commands, launchers, installers, or wrappers.
