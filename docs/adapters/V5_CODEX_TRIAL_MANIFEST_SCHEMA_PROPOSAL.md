# V5 Codex Trial Manifest Schema Proposal

## Purpose

Define an implementation-neutral schema proposal for a future PAI v5 Codex read-only trial manifest.

This document is a markdown proposal only. It does not create an executable schema file, JSON, YAML, TOML, generated config, fixture, manifest instance, validator, test harness, root `AGENTS.md`, `.codex/`, runtime adapter file, launcher, installer, wrapper, hook, rule, skill, subagent, agent, or command.

## Scope

This proposal translates the S4 manifest contract into machine-checkable field definitions and validation intent.

It does not choose a serialization format. A future implementation milestone may choose an executable schema technology only after architect approval.

S5 does not run a read-only trial and does not authorize existing-local-v5 trial execution.

## Evidence Base

Primary inputs:

- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_MANIFEST_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_FIXTURE_AND_PATH_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_EQUIVALENCE_TEST_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_OUTPUT_SPEC.md`

Supporting inputs:

- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`
- `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`

No new Codex capability claims are introduced in this proposal.

## Schema Proposal Status

This schema proposal is not executable.

It intentionally avoids:

- JSON Schema.
- YAML schema.
- TOML schema.
- Generated config.
- Manifest instances.
- Validator code.
- Test harnesses.
- Runtime adapter files.

The proposal defines field names, expected kinds, cardinality, allowed value sets, and cross-field constraints in markdown tables so a future milestone can convert them into a reviewed executable schema.

## Schema Design Principles

The manifest schema must preserve these invariants:

- Codex is not currently proven drop-in for existing local PAI v5 files.
- Codex replacement is plausible only through a designed adapter.
- Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
- A read-only trial must not require uninstalling Claude Code.
- A read-only trial must be reversible and must not write PAI state.
- `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
- `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
- Codex `AGENTS.md`, if later authorized, must be a compact router.
- Claude-shaped files must not be copied directly into Codex surfaces.
- PAI Memory and ISA artifacts are canonical PAI state.
- Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.
- Product memories and product memories imported from engine state must not be silently promoted into PAI Memory.
- Future writes require a single-writer policy, provenance, rollback, and validation.
- Pulse remains central v5 infrastructure, but S5 does not design or implement a Pulse bridge.

## Top-Level Field Model

| Section | Kind | Required | Cardinality | Purpose |
| --- | --- | --- | --- | --- |
| `manifest_identity` | Object | Yes | One | Identifies the manifest and review status. |
| `trial_identity` | Object | Yes | One | Identifies engine, official engine baseline, mode, phase, source kind, and PAI target. |
| `source_policy` | Object | Yes | One | Describes source roots, provenance, source kind, and privacy status. |
| `authority_policy` | Object | Yes | One | Captures authority envelope and prohibited direct copies. |
| `filesystem_policy` | Object | Yes | One | Defines `allowed_read_roots`, `denied_read_roots`, and `denied_write_roots`. |
| `memory_policy` | Object | Yes | One | Defines PAI Memory, non-PAI memory, transcript, and product-memory handling. |
| `isa_policy` | Object | Yes | One | Defines ISA boundary handling. |
| `pulse_policy` | Object | Yes | One | Defines no-start, no-call, no-write, and no-parity posture for Pulse. |
| `network_policy` | Object | Yes | One | Defines default network denial and reviewed exception posture. |
| `tooling_policy` | Object | Yes | One | Defines sandbox, approvals, installer, migration, service, hook, config, and runtime-surface posture. |
| `output_policy` | Object | Yes | One | Defines advisory-only output and proposal handling. |
| `audit_policy` | Object | Yes | One | Records architect, user, privacy, authority, path, and audit approvals. |
| `rollback_policy` | Object | Yes | One | Records reversibility and future-write prerequisites. |
| `stop_conditions` | Array | Yes | One or more | Lists conditions that stop the future trial. |
| `non_authorizations` | Array | Yes | One or more | States what the manifest does not authorize. |

## Identity and Version Fields

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `manifest_id` | String | Yes | Stable identifier | Must be non-empty and unique within future manifest registry. |
| `manifest_version` | String or integer label | Yes | Implementation-defined version label | Must be present and immutable after approval. |
| `created_by_role` | String | Yes | Role label | Must not contain personal credential material. |
| `review_state` | Enum | Yes | `draft`, `architect-review`, `approved`, `rejected`, `expired` | Only `approved` may be eligible for future trial execution. |
| `expires_at` | Date label | Yes | Future date or explicit no-expiry policy | Expired manifests are invalid. |
| `supersedes` | Array of strings | No | Manifest IDs | If present, must reference prior manifest IDs. |
| `source_spec` | String | Yes | S4/S5 or later approved spec path | Must identify the governing manifest schema proposal or implementation schema. |

## Source and Fixture Fields

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `engine` | Enum | Yes | `codex-candidate` | Must not identify Codex as official upstream PAI engine. |
| `official_engine` | String | Yes | Must name Claude Code as current official/full-support engine | Must preserve current engine status. |
| `mode` | Enum | Yes | `read-only-trial` | No other mode is allowed by this schema proposal. |
| `pai_version` | String | Yes | `v5.0.0` or later approved baseline | Must identify target PAI baseline. |
| `trial_phase` | Enum | Yes | `release-fixture`, `sanitized-user-fixture`, `existing-local-v5-read-only` | Determines required approvals and privacy handling. |
| `source_kind` | Enum | Yes | Same family as `trial_phase` | Must align with source policy. |
| `drop_in_claim_allowed` | Boolean | Yes | `false` only | Must be false. |
| `write_claim_allowed` | Boolean | Yes | `false` only | Must be false. |
| `advance_beyond_read_only_allowed` | Boolean | Yes | `false` only | Must be false. |

Additional source and fixture fields:

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `source_roots` | Array of path labels | Yes | Non-empty for executable future manifests | Must be explicit; no broad home-root defaults. |
| `source_root_kind` | Enum | Yes | `repo-release`, `copied-release-fixture`, `sanitized-user-fixture`, `existing-local-live-root` | Must align with `trial_phase`. |
| `provenance_label` | String | Yes | Human-readable label | Must appear in audit output. |
| `private_state_present` | Boolean | Yes | `false` for release fixtures; reviewed value for other kinds | If true, requires privacy review and user approval. |
| `secret_scan_required` | Boolean | Yes | `true` for sanitized and existing-local material | Must be true where private state may exist. |
| `symlink_policy` | Enum | Yes | `deny-escape` | Symlink escape must be denied. |
| `hardlink_policy` | Enum | Yes | `deny-live-root-alias` | Hardlink aliasing to live roots must be denied. |
| `fixture_created_by_manifest` | Boolean | Yes | `false` only | Manifest describes future fixture use; it does not create fixtures. |

## Authority Policy Schema

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `authority_spec` | String | Yes | Approved authority spec path | Must reference S3/S4 authority design or later approved successor. |
| `pai_system_prompt_status` | Enum | Yes | `source-doctrine-high-authority` | Must preserve high-authority status. |
| `claude_md_status` | Enum | Yes | `claude-facing-not-codex-destination` | Must prevent direct Codex destination use. |
| `codex_router_status` | Enum | Yes | `not-created`, `future-compact-router-approved` | S5 default is `not-created`. |
| `claude_file_copy_allowed` | Boolean | Yes | `false` only | Must be false. |
| `agents_md_creation_allowed` | Boolean | Yes | `false` by default | Must remain false unless later approved outside S5. |
| `codex_config_creation_allowed` | Boolean | Yes | `false` by default | Must remain false unless later approved outside S5. |
| `dynamic_context_allowed` | Array or enum | Yes | `none` or explicit future-approved mechanisms | Unlisted dynamic context is denied. |
| `conflict_policy` | String | Yes | PAI doctrine and read-only safety win | Must define conflict resolution. |

## Filesystem Policy Schema

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `allowed_read_roots` | Array of path labels | Yes | Explicit approved roots | Must not be wildcard-only. |
| `denied_read_roots` | Array of path labels | Yes | Explicit denied roots and classes | Must include private state and credential classes. |
| `denied_write_roots` | Array of path labels | Yes | Explicit denied roots and classes | Must include every allowed read root. |
| `deny_by_default` | Boolean | Yes | `true` only | Must be true. |
| `write_exception_allowed` | Boolean | Yes | `false` only | Must be false. |
| `path_glob_policy` | Enum | Yes | `narrow-only` | Globs may narrow access only. |
| `path_resolution_policy` | Enum | Yes | `canonical-before-trial` | Paths must resolve before future execution. |
| `escape_policy` | Enum | Yes | `escape-stops-trial` | Access outside manifest roots stops the trial. |

## Memory Policy Schema

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `pai_memory_status` | Enum | Yes | `canonical-pai-state` | Must preserve PAI Memory ownership. |
| `isa_status` | Enum | Yes | `canonical-pai-state` | Must preserve ISA ownership. |
| `pulse_status` | Enum | Yes | `central-v5-infrastructure-no-bridge-in-s5` | Must not claim Pulse bridge implementation. |
| `claude_memory_status` | Enum | Yes | `not-pai-memory` | Must remain non-canonical. |
| `codex_memory_status` | Enum | Yes | `not-pai-memory` | Must remain non-canonical. |
| `codex_goal_status` | Enum | Yes | `not-pai-memory-not-isa-not-pulse` | Must remain non-canonical. |
| `codex_transcript_status` | Enum | Yes | `audit-material-not-canonical-state` | Must not become PAI state. |
| `product_memory_promotion_allowed` | Boolean | Yes | `false` only | Must be false. |
| `single_writer_required_for_future_writes` | Boolean | Yes | `true` only | Must be true. |

## ISA Policy Schema

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `isa_status` | Enum | Yes | `canonical-pai-state` | Must preserve ISA ownership. |
| `isa_write_allowed` | Boolean | Yes | `false` only | Must be false for read-only posture. |
| `goal_state_promotes_to_isa` | Boolean | Yes | `false` only | `/goal` state must not become ISA evidence by itself. |
| `isa_acceptance_source` | String | Yes | Architect-approved future evidence only | Must not treat transcripts or dry-run notes as ISA artifacts. |

## Pulse Policy Schema

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `pulse_status` | Enum | Yes | `central-v5-infrastructure-no-bridge-in-s5` | Must not claim Pulse bridge implementation. |
| `pulse_start_allowed` | Boolean | Yes | `false` only | Must be false. |
| `pulse_call_allowed` | Boolean | Yes | `false` only | Must be false. |
| `pulse_write_allowed` | Boolean | Yes | `false` only | Must be false. |
| `pulse_parity_claim_allowed` | Boolean | Yes | `false` only | Must be false. |

## Network Policy Schema

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `network_policy` | Enum | Yes | `disabled`, `explicit-exception-reviewed` | Default must be disabled. |
| `network_exception_approved` | Boolean | Yes | `false` by default | Any exception requires later review outside S5. |
| `provider_network_required` | Boolean | Yes | `false` for S5 proposal | S5 does not run Codex or provider calls. |

## Tooling Policy Schema

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `sandbox_mode_intent` | Enum | Yes | `read-only` | Describes future intent only. |
| `approval_policy_intent` | Enum | Yes | `no-write-approvals` | Must not permit writes. |
| `network_policy` | Enum | Yes | `disabled`, `explicit-exception-reviewed` | Default must be disabled. |
| `pulse_policy` | Enum | Yes | `no-start-no-call-no-write-no-parity` | Must block Pulse activity. |
| `installer_policy` | Enum | Yes | `no-execution` | Must block installers. |
| `migration_policy` | Enum | Yes | `no-import-no-migration` | Must block migration tooling. |
| `service_policy` | Enum | Yes | `no-service-start` | Must block services and daemons. |
| `hook_policy` | Enum | Yes | `no-live-pai-hook-execution` | Must block live hook execution. |
| `generated_config_policy` | Enum | Yes | `no-generated-config` | Must block generated config. |

## Output Policy Schema

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `output_mode` | Enum | Yes | `advisory-only` | Output is evidence only. |
| `patch_policy` | Enum | Yes | `proposals-only` | No patch application. |
| `state_update_policy` | Enum | Yes | `none` | No PAI state updates. |
| `claims_policy` | Array of forbidden claims | Yes | Drop-in, official-engine, write-readiness, Pulse parity, memory merge | Must forbid unsafe claims. |
| `required_audit_sections` | Array of section labels | Yes | Audit schema section labels | Must align with audit schema proposal. |
| `destination_policy` | Enum | Yes | `outside-live-pai-roots` | Must forbid output into live PAI roots. |

## Audit Policy Schema

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `architect_approval` | Approval record | Yes | Approved or not approved | Required before future execution. |
| `user_live_root_approval` | Array of approval records | Conditional | Required for existing local live roots | Must cover each live root. |
| `privacy_review` | Approval record | Conditional | Required for sanitized and existing-local material | Must exist when private state may be present. |
| `authority_review` | Approval record | Yes | Approved or not approved | Required before behavior evaluation. |
| `path_model_review` | Approval record | Yes | Approved or not approved | Required before filesystem exposure. |
| `audit_review` | Approval record | Yes | Approved or not approved | Required before accepting results. |

## Rollback Policy Schema

| Field | Kind | Required | Allowed Values | Validation Intent |
| --- | --- | --- | --- | --- |
| `reversibility_required` | Boolean | Yes | `true` only | Future trials must be reversible. |
| `rollback_plan_required_before_writes` | Boolean | Yes | `true` only | Future writes require rollback design. |
| `single_writer_required_before_writes` | Boolean | Yes | `true` only | Future writes require single-writer policy. |
| `provenance_required_before_writes` | Boolean | Yes | `true` only | Future writes require provenance. |
| `validation_required_before_writes` | Boolean | Yes | `true` only | Future writes require validation. |

## Stop Conditions Schema

The stop conditions array must include at least:

- Drop-in claim attempted.
- Official-engine claim attempted.
- Write attempted or requested.
- Denied read attempted or requested.
- Pulse startup or call attempted.
- Installer execution attempted.
- Codex import or migration tooling attempted.
- Root `AGENTS.md` or `.codex/` creation attempted.
- Runtime surface creation attempted.
- State promotion attempted.
- Fixture path resolves into live user-local root.
- Manifest incomplete, expired, unapproved, or ambiguous.

Each stop condition entry must define an identifier, description, trigger state, and audit reporting requirement in a future executable schema.

Non-authorization requirements:

The non-authorization array must state that the manifest does not authorize:

- Trial execution.
- Fixture creation.
- Runtime adapter implementation.
- PAI Memory writes.
- ISA writes.
- Pulse implementation.
- Existing-local-v5 trial execution.
- Root `AGENTS.md`.
- `.codex/`.
- Generated config.
- Installer execution.
- Migration tooling.
- Moving beyond read-only posture.

## Cross-Field Validation Rules

| Rule ID | Rule |
| --- | --- |
| MF-R001 | If `trial_phase` is `existing-local-v5-read-only`, every live root must have user approval and privacy review. |
| MF-R002 | Every `allowed_read_roots` entry must be covered by `denied_write_roots`. |
| MF-R003 | `deny_by_default` must be true and `write_exception_allowed` must be false. |
| MF-R004 | `drop_in_claim_allowed`, `write_claim_allowed`, and `advance_beyond_read_only_allowed` must be false. |
| MF-R005 | If `private_state_present` is true, `secret_scan_required` must be true. |
| MF-R006 | `agents_md_creation_allowed` and `codex_config_creation_allowed` default to false in S5-derived manifests. |
| MF-R007 | Product memory promotion must be false. |
| MF-R008 | Pulse policy must deny startup, calls, writes, and parity claims. |
| MF-R009 | A manifest with `review_state` other than `approved` cannot authorize a future trial. |
| MF-R010 | Any unknown future field must fail review unless a later schema explicitly permits extensions. |

## Example Non-Executable Manifest Document

This section describes a non-executable example shape in prose only.

An acceptable future manifest document would identify one manifest, one read-only trial posture, one explicit source kind, explicit `allowed_read_roots`, explicit `denied_read_roots`, explicit `denied_write_roots`, an authority policy that treats `PAI_SYSTEM_PROMPT.md` as high-authority doctrine, and output policy that permits only advisory audit output.

The example must not be serialized as JSON, YAML, TOML, generated config, or a manifest instance during S5.

## Prohibited Schema Semantics

Future executable schema work must not encode:

- Codex as official upstream PAI engine.
- Codex as drop-in replacement.
- Write access during read-only trial.
- Silent product memory promotion.
- Pulse bridge or parity implementation.
- Direct copying of Claude-shaped files into Codex-native surfaces.
- Root `AGENTS.md` or `.codex/` creation by S5-derived manifest.
- Unscoped access to `~/.claude/`, `~/.claude/PAI/`, `~/.claude/projects/`, `~/.codex/`, or `~/.codex/memories/`.

## Future Implementation Gates

A future executable schema milestone requires:

- Architect approval.
- Serialization format decision.
- Schema versioning policy.
- Privacy review for live-root fields.
- Path canonicalization design.
- Denied-path validation design.
- Audit schema alignment.
- Dry-run validation results.

## Non-Goals

This proposal does not create executable schema files, JSON, YAML, TOML, generated config, fixture material, manifest instances, audit artifacts, validators, test harnesses, runtime adapter files, root `AGENTS.md`, `.codex/`, hooks, rules, skills, subagents, agents, commands, launchers, installers, or wrappers.
