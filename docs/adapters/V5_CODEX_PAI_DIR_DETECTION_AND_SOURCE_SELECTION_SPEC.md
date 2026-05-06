# V5 Codex PAI_DIR Detection and Source Selection Spec

## Purpose

Define future read-only `PAI_DIR` detection and source-selection behavior without reading live local state in S12A.

Codex is not currently proven drop-in for existing local PAI v5 files. S12A designs detection and source selection only; it does not detect live `PAI_DIR`, does not read live existing-local-v5 state, and does not authorize a live read-only trial.

## Scope

This spec defines how a future architect-approved trial should distinguish repository-local evidence sources, sanitized user fixtures, and future live local sources.

This spec does not run detection, does not scan home directories, does not inspect `~/.claude/PAI`, does not inspect `~/.claude/projects`, does not inspect `~/.codex`, does not invoke Claude Code or Codex, and does not create root `AGENTS.md`, `.codex/`, runtime adapter files, manifests, audit artifacts, executable schemas, Memory payloads, ISA payloads, Pulse payloads, live-trial artifacts, or runtime payloads.

## Evidence Base

Evidence base:

- S10 fixture-only closeout.
- S11 release-fixture evidence closeout.
- S11D S12 live read-only trial readiness gates.
- S11D proposed S12 consent and protected-path requirements.
- S11D decision that `PAI_DIR` detection must be read-only and future-only.

No live user-local state was inspected to draft this spec.

## PAI_DIR Problem Statement

`PAI_DIR` means the PAI subsystem root, usually `~/.claude/PAI`, but S12A does not inspect it. The problem for a future milestone is to define whether a selected source root is a release fixture, sanitized user fixture, or existing local PAI v5 root without default live reads, broad discovery, or writes to canonical state.

Any future `PAI_DIR` handling must avoid treating a detected path as permission to read it. Detection and source selection are separate from consent.

## Detection Principles

Future detection must be:

- Read-only.
- Path-bounded.
- Abortable.
- Consent-bound.
- Architect-approved.
- No-write by construction.
- Independent from runtime adapter execution.

There is no default live local read. The phrase no default live read is a hard boundary for future designs.

## Source Kind Model

Source kinds:

- `release-fixture`: repository-local fixture data approved by S10/S11.
- `sanitized-user-fixture`: future user-provided fixture data that is sanitized and copied into an approved repository or temporary fixture boundary by explicit process.
- `existing-local-v5-read-only`: future-only read-only access to existing local PAI v5 state after explicit user consent plus architect approval.

The `existing-local-v5-read-only` source kind is not approved by S12A. It remains future-only.

## Candidate Source Roots

Candidate roots must be explicitly selected by a future contract. They must not be discovered through broad scans.

Allowed future candidates may include:

- The approved repository-local fixture root.
- A future approved sanitized-user-fixture root.
- A future explicitly consented `existing-local-v5-read-only` root.

Candidate roots must be rejected if they are absolute paths without consent, parent traversal paths, arbitrary home directory paths, `~/.claude/projects` memory paths, `~/.codex/memories`, product memory paths by default, root `AGENTS.md`, `.codex/`, or any path outside the approved source selection model.

## Allowed Detection Inputs

Allowed future detection inputs must be named in a future architect-approved card:

- Explicit user-provided source root.
- Explicit source kind.
- Explicit consent reference.
- Approved source selection record.
- Repository-local fixture root.

S12A does not read those live inputs. It only defines the model.

## Forbidden Detection Inputs

Forbidden detection inputs:

- Default reads of `~/.claude/`.
- Default reads of `~/.claude/PAI/`.
- Reads of `~/.claude/projects/**/memory`.
- Reads of `~/.codex/memories`.
- Broad home-directory scans.
- Shell history, product memories, subscription state, or inferred local configuration.
- Any Pulse endpoint or `localhost:31337` probe.

No discovered path may be written into PAI Memory, ISA, Pulse, Claude memory, or Codex memory.

## PAI_DIR Confirmation Model

Future confirmation must require both:

- A path-bounded read-only source selection.
- Explicit user consent for that exact source root.

Confirmation must fail closed if the source root is ambiguous, if the path does not match the consent record, if the path would require reading forbidden private state, or if any write mode is needed.

S12A does not confirm or detect live `PAI_DIR`.

## Source Selection Workflow

Future source selection workflow:

1. Identify source kind without reading live local state by default.
2. Present the selected source root and source kind in disclosure.
3. Capture explicit user consent in a future approved non-canonical record.
4. Run read-only preflight against the selected root only if future scope allows it.
5. Abort if consent, path, no-write, Pulse, PAI Memory, ISA, product memory, or runtime boundaries fail.
6. Report only non-canonical evidence unless separately approved.

Source selection must not create root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, skills, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, manifests, schemas, audit artifacts, live-trial artifacts, or runtime payloads.

## Source Selection Failure Conditions

Source selection fails if:

- The source kind is missing or invalid.
- The source root is ambiguous.
- Consent is absent, ambiguous, expired, or revoked.
- The source root does not match consent.
- The path requires parent traversal, broad home scanning, or default live user-local reads.
- Detection would read product memory by default.
- Detection would write to PAI Memory, ISA, Pulse, Claude memory, or Codex memory.
- Detection requires Pulse startup, Pulse endpoint calls, Claude Code invocation, Codex runtime invocation, or installer execution.

## No-Default-Live-Read Rule

No default live local read is allowed. A future tool must not inspect live `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, product memory, or existing-local-v5 state unless a later architect-approved card explicitly authorizes the source kind, source root, consent model, allowed reads, forbidden reads, and validation commands.

S12A performs no default live read and no live read of any kind.

## Existing Local v5 Boundary

The `existing-local-v5-read-only` boundary is future-only. It requires explicit user consent plus architect approval.

Existing local PAI v5 state must not be treated as public because it exists on disk. Future read-only access must be path-bounded, abortable, and reported as non-canonical evidence. It must not write to PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, or `.codex/`.

## Product Memory Boundary

Product memory reads remain denied by default. Product memories must not be silently promoted into PAI Memory.

Future detection must not read product memories, infer source roots from product memories, or promote product memory into canonical PAI state without a separate architect-approved policy.

## Pulse Boundary

PAI_DIR detection does not require Pulse. Future source selection must not start Pulse, call Pulse endpoints, probe `localhost:31337`, or write Pulse state.

Pulse status must remain `not-started-not-called` unless a future card explicitly changes the boundary.

## Required Future Proofs

Required future proofs before any live detection:

- Explicit architect approval.
- Explicit user consent for the exact source root.
- Path-bounded read-only detection design.
- No arbitrary home-directory scanning.
- No reads of `~/.claude/projects/**/memory`.
- No reads of `~/.codex/memories`.
- No product memory reads by default.
- No writes to PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, or `.codex/`.
- Abort behavior for ambiguous roots and forbidden paths.

## Prohibited Detection Designs

Prohibited designs:

- Default live `PAI_DIR` detection.
- Broad home-directory scans.
- Source selection inferred from Claude Code installation, Codex installation, dual subscriptions, shell history, or product memory.
- Reading `~/.claude/projects/**/memory`.
- Reading `~/.codex/memories`.
- Writing discovered paths to PAI Memory, ISA, Pulse, Claude memory, or Codex memory.
- Runtime adapter execution, Claude Code invocation, Codex runtime invocation, Pulse startup, Pulse endpoint calls, root `AGENTS.md`, or `.codex/`.

## Non-Goals

S12A does not detect live `PAI_DIR`, read `~/.claude/PAI`, read `~/.claude/projects`, read `~/.codex`, read product memory, read existing-local-v5 state, run a live read-only trial, implement a runtime adapter, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, invoke Claude Code, invoke Codex runtime, create root `AGENTS.md`, create `.codex/`, authorize product-memory promotion, or claim Codex is drop-in today.
