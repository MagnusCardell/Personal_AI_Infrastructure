# V5 Codex Trial Fixture and Path Model Spec

## Purpose

Define the fixture and path model required before any future read-only Codex trial can be run against PAI v5 fixture material or existing local PAI v5 files.

This document is design-only. It does not create fixtures, copy files, inspect private user-local state, run a trial, implement a Codex adapter, create root `AGENTS.md`, create `.codex/`, or create runtime surfaces.

## Scope

This spec defines future fixture families, path classifications, allowed read classes, denied read classes, denied write classes, proof requirements, and failure conditions.

It does not create fixture material, copy release files, inspect existing local v5 files, or implement a test harness.

## Evidence Base

This spec derives from S0/S1/S2/S3 adapter docs. It does not make new Codex capability claims beyond S2/S3.

Primary sources:

- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_MANIFEST_SPEC.md`

## Fixture Model

Future trial safety depends on path modeling before execution.

The path model must distinguish public release evidence, copied release fixtures, sanitized user fixtures, existing local live roots, private product state, canonical PAI state, generated output quarantine, and protected repository paths.

S4 does not create any of these roots. It defines the classification and invariants a future milestone must satisfy before it creates fixture material or exposes live paths.

**Root classes:**

| Root Class | Description | S4 Status | Future Default |
| --- | --- | --- | --- |
| `repo-release-evidence` | Read-only upstream release content under `Releases/v5.0.0/`. | Existing evidence only. | Read-only, no modification. |
| `copied-release-fixture` | Future copy of release evidence for fixture trials. | Not created in S4. | Read-only after creation and verification. |
| `sanitized-user-fixture` | Future user-provided or generated copy of local v5 state with private material removed. | Not created in S4. | Read-only after privacy review. |
| `existing-local-live-root` | Future explicitly approved live local PAI or Claude root. | Not inspected in S4. | Deny by default; read-only only by manifest. |
| `repo-governance-docs` | `docs/adapters/` design docs. | S4 write set only. | Evidence, not runtime state. |
| `codex-product-state` | `~/.codex/`, memories, transcripts, config. | Not inspected in S4. | Not PAI state; deny read/write for PAI trial. |
| `claude-product-state` | `~/.claude/projects/`, Claude Code memory, transcripts, caches. | Not inspected in S4. | Not PAI Memory; deny read/write unless explicitly authorized. |
| `generated-output-quarantine` | Future directory for advisory audit output outside live PAI roots. | Not created in S4. | Required before any future run writes audit artifacts. |

## Path Classification Model

| Path Class | Examples | Canonical State | Future Read Policy | Future Write Policy |
| --- | --- | --- | --- | --- |
| Public release docs | `Releases/v5.0.0/README.md`, release `PAI/DOCUMENTATION/`. | No | Allow for design and release-fixture trials. | Deny. |
| PAI doctrine | `PAI_SYSTEM_PROMPT.md`, Algorithm docs, Memory docs, ISA docs, Pulse docs. | Doctrine | Allow read when manifest-approved. | Deny. |
| Claude runtime files | `CLAUDE.md`, `settings.json`, hooks, skills, agents, commands. | Runtime surface | Allow evidence reads for release/fixture only. | Deny. |
| PAI Memory | `PAI/MEMORY/`. | Yes | Deny live reads by default; allow sanitized or explicitly manifest-approved reads only. | Deny until single-writer milestone. |
| ISA artifacts | `ISA.md`, `MEMORY/WORK/*/ISA.md`. | Yes | Deny live reads by default; allow explicit read-only manifest scope. | Deny until single-writer milestone. |
| Pulse state | Pulse logs, event streams, jobs, local endpoints. | Runtime-canonical when live | Deny live interaction. | Deny. |
| User identity | `PAI/USER/`, identity, projects, telos, relationships. | Private state | Deny live reads by default. | Deny. |
| Credentials and secrets | Credential files, env files, keys, tokens. | Private/security state | Deny. | Deny. |
| Product memory | Claude Code memory, Codex memory. | No PAI canonical status | Deny by default. | Deny for PAI trial. |
| Adapter docs | `docs/adapters/`. | Governance only | Allow for design evidence. | Only approved milestone write set. |

## Release Fixture Policy

| Fixture Family | Purpose | Required Preconditions | S4 Status |
| --- | --- | --- | --- |
| Release baseline fixture | Test read-only reasoning against public PAI v5 release material. | Release source inventory, copy strategy, hash plan, no write plan. | Design only. |
| Sanitized local fixture | Test against user-like local state without secrets or live roots. | User consent, copy procedure, secret stripping, private-state review, provenance labels. | Design only. |
| Existing local read-only exposure | Inspect explicitly approved live local v5 roots without writes. | Architect approval, user approval for each root, read-only mount or equivalent, denied-path proof. | Future-only. |

No fixture family may include root `AGENTS.md`, `.codex/`, generated Codex config, hooks, rules, wrappers, launchers, test harnesses, or runtime files created by S4.

Release fixture policy is the first future fixture family because it avoids private user-local state. S4 does not create a release fixture.

## Sanitized User Fixture Policy

Sanitized user fixtures are future-only. They require user consent, copy procedure review, secret stripping, private-state review, provenance labels, link handling, and read-only enforcement.

S4 does not create sanitized fixtures and does not inspect private user-local state.

## Existing Local v5 Read-Only Policy

Existing local v5 roots are private, live, and potentially canonical.

Future existing-local exposure requires:

- User approval for each root.
- Architect approval for the trial phase.
- Technical read-only mount or equivalent.
- Denied child paths for credentials and private product state.
- No Pulse startup.
- No installer execution.
- No migration tooling.
- No generated config.
- No root `AGENTS.md`.
- No `.codex/`.
- No move to writes after the trial.

## Allowed Read Classes

Allowed read classes may include public release docs, PAI doctrine, adapter docs, copied release fixtures, sanitized fixtures, and existing local roots only when manifest-approved.

**Logical root names:**

Future manifests should avoid ambiguous natural-language roots by using logical root names.

| Logical Root | Meaning |
| --- | --- |
| `REPO_ROOT` | Repository root for governance docs and release evidence. |
| `RELEASE_ROOT` | `Releases/v5.0.0/` or later approved release baseline. |
| `RELEASE_CLAUDE_PAYLOAD_ROOT` | Release payload under `Releases/v5.0.0/.claude/`. |
| `FIXTURE_ROOT` | Future copied fixture root, never a live user root. |
| `SANITIZED_FIXTURE_ROOT` | Future sanitized local fixture root. |
| `LIVE_CLAUDE_HOME` | Future explicitly approved `~/.claude/` root, denied by default. |
| `LIVE_PAI_ROOT` | Future explicitly approved `~/.claude/PAI/` root, denied by default. |
| `LIVE_CLAUDE_PROJECTS_ROOT` | Future explicitly approved `~/.claude/projects/` root, denied by default. |
| `CODEX_HOME` | Future Codex product root, denied by default for PAI trial. |
| `AUDIT_OUTPUT_ROOT` | Future output quarantine outside live PAI roots. |

S4 does not resolve these names to actual paths.

## Denied Read Classes

Denied read classes include credentials, secrets, user-local product memory, unapproved user identity, unapproved PAI Memory, unapproved ISA artifacts, Pulse runtime state, and any root outside the manifest.

Denied read classes dominate allowed read classes.

## Denied Write Classes

Denied write classes include all allowed read roots and all live PAI, Claude, Codex, release, runtime, installer, hook, skill, agent, command, wrapper, generated config, and fixture roots.

**Path resolution rules:**

Future implementation must resolve paths before trial execution:

- Expand `~`, `$HOME`, and environment variables only through an approved resolver.
- Convert all roots to canonical absolute paths.
- Reject roots that do not exist unless they are future generated-output roots approved by a later milestone.
- Reject duplicate roots that resolve to the same path under different spelling.
- Reject child roots that bypass a denied parent unless specifically allowed and technically isolated.
- Reject symlinks that escape approved roots.
- Reject hardlinks to live roots from fixture roots.
- Reject bind mounts or aliases that point a fixture root into live user-local state.
- Reject path globs that broaden access beyond the reviewed manifest.

**Symlink and link policy:**

Symlinks and hardlinks are high risk because a fixture can appear isolated while pointing at live state.

Future fixture policy:

- Symlink traversal outside an approved read root is forbidden.
- Symlinks inside a fixture must either be removed, rewritten to safe fixture-local paths, or recorded and denied.
- Hardlinks to live roots are forbidden.
- Device files, sockets, FIFOs, and service endpoints are forbidden in fixture material.
- Any unresolved or ambiguous link is a stop condition.

**Fixture integrity requirements:**

A future fixture design must record:

- Source root.
- Copy method.
- Excluded path classes.
- Secret stripping method.
- Sanitization reviewer.
- Hash or inventory strategy.
- Link handling result.
- Read-only enforcement mechanism.
- Provenance label.
- Expiration date.
- Scope of allowed PAI state simulation.

This S4 spec does not implement hashing, inventory, copying, or sanitization.

## Secret and Credential Handling

Future trial manifests must deny these classes at minimum:

- `~/.claude/` unless a specific future live-root trial approves a narrower path.
- `~/.claude/PAI/USER/` unless sanitized or explicitly approved.
- `~/.claude/PAI/USER/CREDENTIALS/`.
- `~/.claude/projects/`.
- `~/.codex/`.
- `~/.codex/memories/`.
- Any credential, key, token, secret, or local env file.
- Pulse runtime logs, sockets, service handles, and local HTTP endpoints.
- Installer files as executable entry points.
- Migration and import tools as executable entry points.
- Root `AGENTS.md` and `.codex/` creation destinations.

Denied path classes dominate allowed read classes.

Secrets and credentials must never be read, copied into fixtures, emitted in audit output, or placed in generated output quarantine.

## Product Memory Handling

Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.

Product memories must not be silently promoted into PAI Memory.

## PAI Memory and ISA Handling

PAI Memory and ISA artifacts are canonical PAI state.

A read-only trial must not write PAI state. Future writes require a single-writer policy, provenance, rollback, and validation.

## Pulse State Handling

Pulse remains central v5 infrastructure, but S4 does not design or implement a Pulse bridge.

Future path models must deny Pulse startup, Pulse endpoint calls, Pulse writes, and Pulse parity claims unless a later bridge milestone approves otherwise.

## No-Write Proof Requirements

No-write proof must show that all read roots are write-denied and that generated output, if later authorized, is isolated from live PAI, Claude, Codex, release, and runtime roots.

**Generated output quarantine:**

Future trials that need persistent audit artifacts must write them only to an explicitly approved `AUDIT_OUTPUT_ROOT`.

Rules:

- `AUDIT_OUTPUT_ROOT` must not be inside `LIVE_PAI_ROOT`, `LIVE_CLAUDE_HOME`, `RELEASE_ROOT`, `.codex/`, or `.claude/`.
- `AUDIT_OUTPUT_ROOT` must not be treated as PAI Memory, ISA, or Pulse state.
- Audit artifacts must be advisory evidence only.
- Audit artifacts must record denied roots without reading their contents.
- Audit artifacts must not include secrets or private state excerpts.

S4 does not create `AUDIT_OUTPUT_ROOT`.

**Existing local v5 exposure policy:**

Existing local v5 roots require stricter handling than fixtures.

Future existing-local exposure requires:

- User approval for each root.
- Architect approval for the trial phase.
- Explicit statement that the root is live, private, and potentially canonical.
- Technical read-only mount or equivalent.
- Denied child paths for credentials and private product state.
- No Pulse startup.
- No installer execution.
- No migration tooling.
- No generated config.
- No root `AGENTS.md`.
- No `.codex/`.
- No move to writes after the trial.

If any of these are absent, the future trial must not start.

## Denied-Path Proof Requirements

Denied-path proof must show that denied roots were neither read nor traversed through symlink, hardlink, bind mount, alias, glob, or generated-output path.

## Failure Conditions

Stop before any future trial if:

- A path resolves outside the approved roots.
- A read root also appears as a write root.
- A denied root is inside an allowed root without an explicit deny override.
- A fixture contains symlinks or hardlinks to live roots.
- A fixture contains credentials or secrets.
- A fixture root is actually a live user-local root.
- A live root lacks explicit user approval.
- Generated output would land inside a PAI, Claude, Codex, release, or runtime root.
- Pulse endpoints, installers, or migration tools are reachable as executable actions.

## Future Implementation Gates

Future implementation gates include architect approval, manifest approval, path model review, no-write proof design, denied-path proof design, privacy review, rollback statement, and audit output review.

## Non-Goals

This spec does not authorize fixture creation, path scanning, live-root inspection, trial execution, audit artifact writing, generated output directories, runtime files, adapter implementation, Pulse startup, installer execution, migration tooling, or movement beyond S4.
