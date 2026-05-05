# V5 Codex Read-Only Trial Manifest Spec

## Purpose

Define the manifest contract a future milestone must satisfy before any read-only Codex trial can be run against PAI v5 fixture material or existing local PAI v5 files.

This document is design-only. It does not create a manifest instance, run a trial, create fixtures, implement a Codex adapter, create root `AGENTS.md`, create `.codex/`, create hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, runtime files, or test harnesses.

## Scope

This spec defines future manifest fields, lifecycle expectations, policy sections, stop conditions, validation rules, and prohibited semantics for a later read-only trial design.

It does not create a manifest, schema, fixture, harness, runtime configuration, or audit output. It does not authorize existing-local-v5 trial execution.

## Evidence Base

This spec derives from S0/S1/S2/S3 adapter docs. It does not make new Codex capability claims beyond S2/S3.

Primary sources:

- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`
- `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`

## Manifest Role

A future read-only trial manifest is a preflight contract, not a runtime file and not a permission slip for writes.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement is plausible only through a designed adapter.

The manifest must make trial scope explicit before Codex sees any PAI fixture or existing local v5 material. It must identify the engine, mode, source kind, authority envelope, allowed reads, denied reads, denied writes, state boundaries, stop conditions, audit expectations, and required approvals.

No future trial may proceed from an implicit prompt, ad hoc path list, or general trust that "read-only" is understood.

## Manifest Lifecycle

S4 defines a manifest specification only.

S4 does not create:

- A manifest file.
- A schema file.
- A fixture.
- A trial harness.
- A generated config.
- A Codex command.
- A root `AGENTS.md`.
- A `.codex/` directory.
- An audit output file.

Lifecycle states must remain reviewable: `draft`, `architect-review`, `approved`, `rejected`, `expired`, or a later approved equivalent. Expired or ambiguous manifests cannot authorize a future trial.

## Required Manifest Fields

| Section | Purpose | Required |
| --- | --- | --- |
| `manifest_identity` | Identifies the manifest and its review state. | Yes |
| `trial_identity` | Identifies engine, mode, PAI version, source kind, and trial phase. | Yes |
| `authority_envelope` | Names the approved authority sources and conflict rules. | Yes |
| `source_material` | Lists the source material category and provenance. | Yes |
| `path_policy` | Defines allowed reads, denied reads, and denied writes. | Yes |
| `runtime_posture` | Defines future sandbox, approval, network, Pulse, installer, and migration posture. | Yes |
| `state_boundary_policy` | Defines Memory, ISA, Pulse, Claude product state, Codex product state, and audit-state boundaries. | Yes |
| `output_policy` | Defines advisory-only output and proposal labeling. | Yes |
| `audit_policy` | Defines required audit fields and evidence expectations. | Yes |
| `approvals` | Records architect and user approvals needed before a future trial. | Yes |
| `stop_conditions` | Lists conditions that stop before or during a future trial. | Yes |
| `non_authorizations` | States what the manifest does not authorize. | Yes |

**Manifest identity fields:**

| Field | Requirement |
| --- | --- |
| `manifest_id` | Stable unique identifier, such as `v5-s5-release-fixture-readonly-001`. |
| `manifest_version` | Manifest spec version. Future first implementation should start at `1`. |
| `created_by_role` | Role that drafted the manifest, not a person credential. |
| `review_state` | One of `draft`, `architect-review`, `approved`, `rejected`, or `expired`. |
| `expires_at` | Date after which the manifest must be re-reviewed. |
| `supersedes` | Optional prior manifest IDs superseded by this manifest. |
| `source_spec` | Must reference this S4 spec or a later approved manifest spec. |

**Trial identity fields:**

| Field | Requirement |
| --- | --- |
| `engine` | Must be `codex-candidate`, not `official-pai-engine`. |
| `official_engine` | Must state `Claude Code remains current official/full-support engine for PAI v5.0.0 until replacement-grade validation exists`. |
| `mode` | Must be `read-only-trial`. |
| `pai_version` | Must identify the target PAI baseline, initially `v5.0.0`. |
| `trial_phase` | One of `release-fixture`, `sanitized-user-fixture`, or `existing-local-v5-read-only`. |
| `source_kind` | Same value family as `trial_phase`, used for audit consistency. |
| `drop_in_claim_allowed` | Must be `false`. |
| `write_claim_allowed` | Must be `false`. |
| `advance_beyond_read_only_allowed` | Must be `false`. |

**Authority envelope fields:**

| Field | Requirement |
| --- | --- |
| `authority_spec` | Must reference `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md` or a later approved authority spec. |
| `pai_system_prompt_status` | Must state `source doctrine; high-authority semantics required; not ordinary markdown`. |
| `codex_router_status` | Must state whether a future compact router is in scope. For S4-derived trials, default is `not-created`. |
| `claude_file_copy_allowed` | Must be `false`. |
| `agents_md_creation_allowed` | Must be `false` unless a later architect-approved implementation milestone changes it. |
| `codex_config_creation_allowed` | Must be `false` unless a later architect-approved implementation milestone changes it. |
| `dynamic_context_allowed` | Must list explicit allowed mechanisms or `none`. |
| `conflict_policy` | Must state that PAI doctrine and read-only constraints outrank convenience, Codex memory, transcripts, plans, and future router text. |

## Source Kind Model

| Field | Requirement |
| --- | --- |
| `source_roots` | Declared roots that may be considered as input. |
| `source_root_kind` | One of `repo-release`, `copied-release-fixture`, `sanitized-user-fixture`, or `existing-local-live-root`. |
| `provenance_label` | Human-readable label that will appear in audit output. |
| `private_state_present` | Must be `false` for release fixtures; explicit and reviewed for sanitized or existing-local roots. |
| `secret_scan_required` | Must be `true` for sanitized and existing-local material. |
| `symlink_policy` | Must deny symlink traversal outside approved roots. |
| `hardlink_policy` | Must deny hardlink-based aliasing to live roots. |
| `fixture_created_by_this_manifest` | Must be `false`; manifest describes use of a fixture but does not create it. |

Source kind values must distinguish release fixture material, sanitized user fixture material, and existing local v5 read-only roots. Existing local v5 roots require explicit user approval and remain private, live, and potentially canonical.

## Authority Policy Fields

Authority policy fields must preserve the S3 authority mapping:

- `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
- `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
- Codex `AGENTS.md`, if later authorized, must be a compact router.
- Claude-shaped files must not be copied directly into Codex surfaces.
- Codex memory, transcripts, SDK threads, and `/goal` state are not authority and not PAI Memory.

## Filesystem Policy Fields

| Field | Requirement |
| --- | --- |
| `allowed_read_roots` | Explicit list. Empty or wildcard-only lists are invalid. |
| `denied_read_roots` | Explicit list. Must include protected private state and credential classes. |
| `denied_write_roots` | Explicit list. Must include all allowed read roots plus protected runtime and state roots. |
| `deny_by_default` | Must be `true`. |
| `write_exception_allowed` | Must be `false`. |
| `path_glob_policy` | Globs may only narrow access, never broaden it. |
| `path_resolution_policy` | Paths must be resolved to canonical absolute paths before a future trial. |
| `escape_policy` | Access outside the manifest roots is a stop condition. |

**Runtime posture fields:**

| Field | Requirement |
| --- | --- |
| `sandbox_mode` | Must target read-only behavior. |
| `approval_policy` | Must not allow write approvals during the trial. |
| `network_policy` | Default `disabled`; any exception must be separate, explicit, and not for Pulse. |
| `pulse_policy` | Must state no Pulse startup, no Pulse endpoint calls, no Pulse writes, and no Pulse parity claims. |
| `installer_policy` | Must state no installer execution. |
| `migration_policy` | Must state no Codex import or migration tooling. |
| `service_policy` | Must state no service or daemon startup. |
| `hook_policy` | Must state no live PAI hook execution. |
| `generated_config_policy` | Must state no generated config creation. |

## Memory and ISA Policy Fields

| Surface | Manifest Requirement |
| --- | --- |
| PAI Memory | Identify as canonical PAI state; default live policy is deny-read and deny-write unless explicitly read-approved. |
| ISA artifacts | Identify as canonical PAI state; Codex plans, goals, transcripts, and final answers are not ISA acceptance. |
| Pulse state | Identify as PAI runtime state; no startup, calls, writes, or parity claims. |
| Claude Code memory | Identify as Claude product state, not PAI Memory. |
| Codex memory | Identify as Codex product state, not PAI Memory. |
| Codex `/goal` state | Identify as orchestration metadata, not PAI Memory, ISA, or Pulse state. |
| Codex transcripts | Identify as product/session audit material, not canonical PAI state. |
| Audit output | Identify as advisory evidence, not runtime state. |

PAI Memory and ISA artifacts are canonical PAI state. A read-only trial must be reversible and must not write PAI state. Future writes require a single-writer policy, provenance, rollback, and validation.

Product memories must not be silently promoted into PAI Memory, and product memories remain outside canonical PAI state unless a later architect-approved bridge says otherwise.

## Pulse Policy Fields

Pulse remains central v5 infrastructure, but S4 does not design or implement a Pulse bridge.

Manifest Pulse policy must state:

- No Pulse startup.
- No Pulse endpoint calls.
- No Pulse writes.
- No Pulse parity claims.
- No bridge implementation.

## Network and Tooling Policy Fields

Network and tooling policy must deny or explicitly scope:

- Network access.
- Installer execution.
- Codex import or migration tooling.
- Service or daemon startup.
- Live PAI hook execution.
- Generated config creation.
- Runtime wrapper, launcher, or harness creation.

## Output Policy Fields

| Field | Requirement |
| --- | --- |
| `output_mode` | Must be `advisory-only`. |
| `patch_policy` | Must be `proposals-only`; no patch application. |
| `state_update_policy` | Must be `none`. |
| `claims_policy` | Must forbid drop-in, official-engine, write-readiness, Pulse-parity, and memory-merge claims. |
| `required_sections` | Must reference the audit output spec. |
| `destination_policy` | Must forbid output writes into live PAI roots. |

**Approval fields:**

| Field | Requirement |
| --- | --- |
| `architect_approval` | Required before any future trial execution. |
| `user_live_root_approval` | Required for each existing local live root. |
| `privacy_review` | Required for sanitized and existing-local material. |
| `authority_review` | Required before the trial can evaluate PAI behavior. |
| `path_model_review` | Required before any filesystem exposure. |
| `audit_review` | Required before results are accepted as trial evidence. |

## Stop Condition Fields

The manifest must stop the trial if:

- Codex is treated as drop-in.
- Codex is treated as the official upstream PAI engine.
- A write is attempted or requested.
- A denied path is read or requested.
- Pulse would be started or contacted.
- An installer would run.
- Codex import or migration tooling would run.
- Root `AGENTS.md`, `.codex/`, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, runtime files, or test harnesses would be created.
- Claude-shaped files would be copied into Codex-native surfaces.
- Codex memory, transcripts, plans, or `/goal` state would be treated as PAI Memory, ISA, or Pulse state.
- A fixture path resolves into a live user-local root.
- The manifest is incomplete, expired, unapproved, or ambiguous.

## Example Non-Executable Manifest

Non-executable sketch:

```yaml
manifest_id: example-only-not-valid-for-execution
engine: codex-candidate
mode: read-only-trial
source_kind: release-fixture
allowed_read_roots: []
denied_read_roots:
  - private-user-local-state
denied_write_roots:
  - all-pai-state
drop_in_claim_allowed: false
write_claim_allowed: false
```

This example is illustrative only. It is incomplete and cannot authorize a trial.

## Validation Rules

Future manifest implementation must validate:

- Required fields are present.
- Unknown fields fail review unless explicitly allowed by a newer spec.
- Paths resolve inside approved roots.
- Deny lists dominate allow lists.
- Write denial covers every read root.
- Live root use has explicit user approval.
- Existing local roots cannot be reached through symlinks or hardlinks.
- Manifest output is auditable without reading private denied paths.

## Prohibited Manifest Semantics

The following are invalid:

- A manifest with `allowed_read_roots: ["~/.claude"]`.
- A manifest with `denied_write_roots` omitted.
- A manifest that allows project `.codex/` generation.
- A manifest that creates a root `AGENTS.md`.
- A manifest that treats read-only trial success as replacement readiness.
- A manifest that allows Pulse calls for convenience.
- A manifest that marks Codex memory as PAI Memory.
- A manifest that has architect approval but lacks user approval for live local roots.

## Future Implementation Gates

Future implementation gates:

- Architect approval.
- User approval for every live root.
- Authority-equivalence review.
- Path-model review.
- Audit-output review.
- No-write proof strategy.
- Denied-path proof strategy.
- Rollback statement.

## Non-Goals

This spec does not authorize a trial, manifest creation, fixture creation, runtime configuration, adapter implementation, write access, private-state inspection, Pulse startup, installer execution, migration tooling, or movement beyond S4.
