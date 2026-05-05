# V5 Codex Schema Dry-Run Validation Spec

## Purpose

Define implementation-neutral dry-run validation design for future PAI v5 Codex read-only trial manifest and audit output schemas.

This document is a markdown proposal only. It does not create validators, executable schema files, JSON, YAML, TOML, generated config, fixtures, manifest instances, audit artifacts, test harnesses, launchers, installers, wrappers, root `AGENTS.md`, `.codex/`, hooks, rules, skills, subagents, agents, commands, or runtime adapter files.

## Scope

S5 dry-run validation means validating schema proposals as design artifacts, not executing a validator or trial.

This spec defines future dry-run phases, review checks, example review scenarios, expected failure classes, and evidence requirements.

It does not run a read-only trial and does not authorize existing-local-v5 trial execution.

## Evidence Base

Primary inputs:

- `docs/adapters/V5_CODEX_TRIAL_MANIFEST_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_MANIFEST_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_OUTPUT_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_FIXTURE_AND_PATH_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_EQUIVALENCE_TEST_SPEC.md`

Supporting inputs:

- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`
- `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`

No new Codex capability claims are introduced in this spec.

## Dry-Run Status

S5 dry-run validation is a design review process.

It does not execute:

- A validator.
- A schema compiler.
- A manifest parser.
- An audit parser.
- Codex.
- Claude Code.
- Pulse.
- Installers.
- Migration tooling.
- Test harnesses.

It does not create:

- Executable schemas.
- JSON, YAML, or TOML files.
- Manifest instances.
- Audit artifacts.
- Fixtures.
- Generated configs.
- Runtime surfaces.

## Validation Philosophy

Dry-run validation must preserve these invariants:

- Codex is not currently proven drop-in for existing local PAI v5 files.
- Codex replacement is plausible only through a designed adapter.
- Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
- S5 does not run a trial.
- S5 does not create fixtures.
- S5 does not implement a harness.
- S5 does not create executable schema files.
- S5 does not create manifest or audit instances.
- S5 does not implement validators.
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

| Phase | Name | Purpose | S5 Status |
| --- | --- | --- | --- |
| DR-0 | Proposal completeness review | Check whether schema proposals cover all S4 contract sections. | Design only. |
| DR-1 | Required-field review | Check whether required manifest and audit fields are listed. | Design only. |
| DR-2 | Value-domain review | Check whether allowed values prevent unsafe claims and writes. | Design only. |
| DR-3 | Cross-field invariant review | Check relationships such as read roots also being write-denied. | Design only. |
| DR-4 | Negative-case review | Check that invalid future manifests or audits would be rejected. | Design only. |
| DR-5 | Evidence-preservation review | Check that S0-S4 strategic conclusions remain represented. | Design only. |
| DR-6 | Implementation-gate review | Check that future executable schema work is properly blocked. | Design only. |

## Manifest Dry-Run Checks

Future design reviewers should confirm:

- Top-level manifest sections are present.
- `engine` cannot identify Codex as official upstream PAI engine.
- `mode` is constrained to read-only trial.
- Drop-in and write claims are disallowed.
- `PAI_SYSTEM_PROMPT.md` is high-authority.
- `CLAUDE.md` is not a Codex destination file.
- Codex `AGENTS.md`, if later authorized, is a compact router.
- Claude-shaped files must not be copied directly into Codex surfaces.
- `allowed_read_roots` are explicit.
- `denied_read_roots` are explicit.
- `denied_write_roots` include every allowed read root.
- Deny-by-default is required.
- Write exceptions are forbidden.
- PAI Memory and ISA are canonical PAI state.
- Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.
- Product memory promotion is forbidden.
- Pulse startup, calls, writes, parity claims, and bridge implementation are forbidden by S5-derived manifests.
- Installer execution and migration tooling are forbidden.
- Root `AGENTS.md`, `.codex/`, generated config, fixtures, runtime files, and harnesses are not created.

## Audit Dry-Run Checks

Future design reviewers should confirm:

- Audit output is advisory.
- Audit output is not PAI Memory, ISA, Pulse state, Codex memory, or replacement readiness.
- Audit identity fields are present.
- Manifest echo fields are present.
- Provenance fields are present.
- Filesystem access reporting covers allowed reads, denied reads, and denied writes.
- Write attempt reporting covers runtime surface creation attempts.
- Authority mapping reporting includes `PAI_SYSTEM_PROMPT.md`, `CLAUDE.md`, and `AGENTS.md` status.
- Memory and ISA reporting preserves canonical PAI state boundaries.
- Pulse reporting states no startup, no calls, no writes, no bridge, and no parity claim.
- Advisory findings cannot claim drop-in compatibility.
- Failure report format includes stop conditions.
- Final verdicts include `next_phase_authorized` as `no`.
- Non-promotion rule is present.
- Retention and privacy notes forbid secret and denied-content disclosure.

## Cross-Document Consistency Checks

| Check ID | Alignment Rule |
| --- | --- |
| XS-001 | Manifest `manifest_id` must be echoed by audit `manifest_id`. |
| XS-002 | Manifest `trial_phase` must match audit `trial_phase`. |
| XS-003 | Manifest `source_kind` must match audit `source_kind`. |
| XS-004 | Manifest `allowed_read_roots` must be echoed in audit filesystem reporting. |
| XS-005 | Manifest `denied_read_roots` must be echoed in audit denied path reporting. |
| XS-006 | Manifest `denied_write_roots` must be echoed in audit write attempt reporting. |
| XS-007 | Manifest authority policy must align with audit authority mapping reporting. |
| XS-008 | Manifest state policy must align with audit Memory, ISA, Pulse, and product-state reporting. |
| XS-009 | Manifest stop conditions must align with audit failure report format. |
| XS-010 | Manifest non-authorizations must align with audit non-authorization object. |

## Denied-Path Reasoning Checks

Dry-run validation design must include denied-path and other negative scenarios.

| Scenario ID | Invalid Condition | Expected Dry-Run Result |
| --- | --- | --- |
| NEG-001 | Manifest allows Codex as official upstream PAI engine. | Reject. |
| NEG-002 | Manifest allows drop-in claim. | Reject. |
| NEG-003 | Manifest omits `denied_write_roots`. | Reject. |
| NEG-004 | Manifest allows write exceptions during read-only trial. | Reject. |
| NEG-005 | Manifest allows root `AGENTS.md` creation. | Reject. |
| NEG-006 | Manifest allows `.codex/` creation. | Reject. |
| NEG-007 | Manifest allows Pulse startup or endpoint calls. | Reject. |
| NEG-008 | Manifest treats Codex memory as PAI Memory. | Reject. |
| NEG-009 | Audit output marks `next_phase_authorized` as true. | Reject. |
| NEG-010 | Audit output omits denied path reporting. | Reject. |
| NEG-011 | Audit output includes private denied path contents. | Reject. |
| NEG-012 | Audit output treats goal completion as ISA acceptance. | Reject. |
| NEG-013 | Manifest points a fixture root at a live user-local root without explicit approval. | Reject. |
| NEG-014 | Manifest allows installers or migration tooling. | Reject. |
| NEG-015 | Audit claims Pulse parity. | Reject. |

## No-Write Reasoning Checks

Future dry-run review must confirm:

- Every `allowed_read_roots` entry is also represented in `denied_write_roots`.
- `write_exception_allowed` is false.
- `write_attempt_report` exists in the audit schema proposal.
- PAI Memory writes are not authorized.
- ISA writes are not authorized.
- Pulse writes are not authorized.
- Runtime adapter file creation is not authorized.
- Root `AGENTS.md`, `.codex/`, generated config, fixtures, validators, and harnesses are not authorized.

## Authority Reasoning Checks

Future dry-run review must confirm:

- `PAI_SYSTEM_PROMPT.md` remains high-authority PAI doctrine.
- `CLAUDE.md` remains an official Claude-facing surface, not a Codex destination file.
- Codex `AGENTS.md`, if later authorized, is treated only as a compact router.
- Claude-shaped files must not be copied directly into Codex surfaces.
- Authority equivalence findings remain advisory until architect review.
- Unsupported authority mappings are reported as blocked rather than converted into replacement claims.

## Memory and ISA Reasoning Checks

Future dry-run review must confirm:

- PAI Memory and ISA artifacts are canonical PAI state.
- Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.
- Product memories are not silently promoted into PAI Memory.
- Goal completion is not treated as ISA acceptance.
- Future writes require a single-writer policy, provenance, rollback, and validation.

## Pulse Reasoning Checks

Future dry-run review must confirm:

- Pulse remains central v5 infrastructure.
- S5 does not design or implement a Pulse bridge.
- Pulse startup, calls, writes, parity claims, and bridge implementation are not authorized.
- Pulse reporting in audit output remains advisory.

## Existing-Local-v5 Reasoning Checks

Future dry-run review must confirm:

- Existing-local-v5 trial execution is not authorized by S5.
- A future read-only trial must not require uninstalling Claude Code.
- A future read-only trial must be reversible and must not write PAI state.
- Live roots require explicit user approval and privacy review in any later milestone.
- Private user-local state is not inspected by S5.

## Failure Classification

| Outcome | Meaning |
| --- | --- |
| `proposal-complete` | Required proposal sections are present and aligned. |
| `proposal-incomplete` | Required proposal sections are missing. |
| `unsafe-semantics-found` | Proposal would allow an unsafe future manifest or audit. |
| `blocked-by-open-question` | Architect decision is needed before schema implementation. |
| `not-reviewed` | Dry-run review did not occur. |

S5 can only design these outcomes. It does not execute a dry-run review.

## Review Workflow

Dry-run validation design should include limited positive scenarios.

| Scenario ID | Valid Condition | Expected Dry-Run Result |
| --- | --- | --- |
| POS-001 | Manifest is draft and complete but not approved. | Structurally valid, not executable. |
| POS-002 | Manifest targets release fixture, has explicit allowed reads, denied reads, denied writes, and no write exceptions. | Structurally valid pending approval. |
| POS-003 | Audit echoes manifest, reports no writes, no denied reads, no Pulse activity, and no next phase authorization. | Structurally valid advisory output. |
| POS-004 | Audit reports an unsupported authority mapping as blocked. | Structurally valid if trial verdict reflects the block. |
| POS-005 | Manifest includes a network exception marked for future review but does not approve it. | Structurally valid only if exception remains non-executable. |

Positive scenarios do not authorize trial execution.

## Required Evidence Before Implementation

A future dry-run validation report should include:

- Schema proposal versions reviewed.
- Manifest proposal sections checked.
- Audit proposal sections checked.
- Cross-schema alignment results.
- Negative scenario results.
- Positive scenario results.
- Unknown or unresolved fields.
- Required architect decisions.
- Confirmation that no executable schema files were created.
- Confirmation that no manifest instances or audit artifacts were created.
- Confirmation that no fixtures, validators, or harnesses were created.
- Confirmation that no read-only trial was run.
- Confirmation that protected paths and private user-local state were not touched.

S5 does not create such a report.

Review outcome values are defined in failure classification and remain design-only.

## Prohibited Dry-Run Semantics

Dry-run validation must not:

- Instantiate a real manifest.
- Instantiate a real audit output.
- Create a fixture.
- Run Codex.
- Run Claude Code.
- Start Pulse.
- Run installers.
- Run migration tooling.
- Read private user-local state.
- Write PAI Memory.
- Write ISA.
- Create root `AGENTS.md`.
- Create `.codex/`.
- Create validators or test harnesses.
- Claim Codex is drop-in.
- Claim Codex is the official upstream PAI engine.

## Future Implementation Gates

A future executable schema or validation milestone requires:

- Architect approval.
- Serialization format decision.
- Executable schema write set approval.
- Validator write set approval.
- Fixture and path model approval.
- Privacy review.
- No-write proof design.
- Denied-path proof design.
- Audit output retention decision.
- Explicit statement that schema validation still does not authorize trial execution.

## Non-Goals

This spec does not create executable schema files, JSON, YAML, TOML, generated config, fixture material, manifest instances, audit artifacts, validators, test harnesses, runtime adapter files, root `AGENTS.md`, `.codex/`, hooks, rules, skills, subagents, agents, commands, launchers, installers, or wrappers.
