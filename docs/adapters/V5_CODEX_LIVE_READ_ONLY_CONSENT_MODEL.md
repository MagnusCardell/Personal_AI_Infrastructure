# V5 Codex Live Read-Only Consent Model

## Purpose

Define the future explicit user consent model required before any live local PAI v5 read-only trial can be considered.

Codex is not currently proven drop-in for existing local PAI v5 files. S12A designs consent only; it does not collect consent, does not read live existing-local-v5 state, does not read live user-local state, and does not authorize a live read-only trial.

## Scope

This document is documentation/design only. It applies to future architect-reviewed live read-only trial planning and to the conditions that must exist before any future source root can be read.

This document does not implement a Codex runtime adapter, does not create runtime adapter files, does not create root `AGENTS.md`, does not create `.codex/`, does not create a consent artifact, and does not authorize Codex config, hooks, rules, skills, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, Memory payloads, ISA payloads, Pulse payloads, manifests, audit artifacts, executable schemas, live-trial artifacts, runtime payloads, or committed negative fixtures.

## Evidence Base

Evidence base:

- S10 fixture-only validation closeout.
- S11 release-fixture read-only evidence closeout.
- S11D proposed S12 live read-only readiness gates.
- S11D proposed S12 write set and completion contract.
- S11D decision that future live read requires explicit user consent design and architect approval.

No live user-local state, no live `~/.claude/PAI`, no live `~/.claude/projects`, no live `~/.codex`, and no existing-local-v5 state were read for S12A.

## Consent Problem Statement

A future live read-only trial would touch private local state if it were approved. That cannot be treated as an ordinary repository-local fixture read. The consent problem is to make any future access explicit, bounded, revocable, source-specific, and abortable before a tool can read a selected live source.

Consent must protect the distinction between release fixtures, sanitized user fixtures, and future `existing-local-v5-read-only` sources. Consent must also preserve no-write behavior and must not weaken PAI Memory, ISA, Pulse, product memory, root `AGENTS.md`, or `.codex` boundaries.

## Consent Principles

Future consent must be explicit user consent. It must not be inferred from having Claude Code installed. It must not be inferred from having Codex installed. It must not be inferred from having both subscriptions.

Future consent must be:

- Bounded to a named source root.
- Source-specific rather than global.
- Read-only by default.
- Revocable before the trial begins and during any abortable preflight.
- Clear about retention and reporting outputs.
- Separate from any claim that Codex is a drop-in runtime.

Consent does not authorize live writes, runtime adapter implementation, product memory access, product-memory promotion, Pulse startup, Pulse endpoint calls, PAI Memory writes, ISA writes, root `AGENTS.md`, or `.codex/`.

## Consent Boundary Model

The consent boundary has three layers:

- Human decision: the user explicitly approves a future source kind and source root after disclosure.
- Architect contract: a future card names the allowed read scope, forbidden read scope, write prohibitions, report output, validation commands, and stop conditions.
- Tool behavior: the future trial refuses to read anything outside the approved source root and refuses to continue if consent is absent, ambiguous, expired, or revoked.

S12A creates no consent artifact and does not record a consent decision. It records only the design boundary required before any future consent artifact could be proposed.

## User Disclosure Requirements

Future disclosure must state:

- Codex is not currently proven drop-in for existing local PAI v5 files.
- The trial is read-only and non-runtime unless a separate architect-approved card says otherwise.
- The selected source root and why it is needed.
- The allowed read scope.
- The forbidden read scope.
- The forbidden writes.
- The reporting output.
- The retention policy.
- The rollback/no-residue expectation.
- The fact that refusal or revocation stops the trial without penalty.

The disclosure must also state that Claude-shaped files must not be copied directly into Codex surfaces and that any future Codex `AGENTS.md`, if later authorized, must be a compact router rather than a copied Claude file.

## Consent Capture Requirements

Future consent capture must separately identify:

- Source root.
- Allowed read scope.
- Forbidden read scope.
- Forbidden writes.
- Reporting output.
- Retention policy.
- Rollback/no-residue expectation.

The capture must be designed as non-canonical evidence unless separately approved. It must not write to PAI Memory, ISA, Pulse state, Claude memory, Codex memory, root `AGENTS.md`, `.codex/`, or product memory. It must not become a manifest, runtime payload, or PAI runtime audit artifact by default.

## Consent Scope Model

Future consent scope must bind to one source kind and one selected source root. The allowed source kinds remain:

- `release-fixture`
- `sanitized-user-fixture`
- `existing-local-v5-read-only`

The `existing-local-v5-read-only` source kind is future-only. It requires explicit user consent plus architect approval before any live local read. It cannot be enabled by default and cannot be inferred from subscriptions, installations, local config, shell history, or product memory.

## Consent Expiration and Revocation

Future consent must expire at the end of the approved trial window. It must be revocable before a preflight reads live state and must remain abortable if the future tool detects scope ambiguity, unexpected private state, any write requirement, Pulse startup requirement, Pulse endpoint call requirement, Memory/ISA write requirement, product-memory access requirement, runtime adapter requirement, or drop-in claim pressure.

Revocation must not write to PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, or `.codex/`.

## Consent and No-Write Policy

Consent is not a write authorization. Future consent can only authorize the exact read-only source scope named by a future architect-approved card.

Consent does not authorize:

- PAI Memory writes.
- ISA writes.
- Pulse state writes.
- Product-memory reads by default.
- Product-memory promotion.
- Root `AGENTS.md`.
- `.codex/`.
- Runtime adapter files.
- Manifests, executable schemas, runtime payloads, or live-trial artifacts outside an approved write set.

## Consent and Product Memory Boundary

Product memory remains outside the default read scope. Future consent must not authorize product-memory reads by implication and must not authorize product-memory promotion into PAI Memory.

Product memories must not be silently promoted into PAI Memory. Any future product memory access would require a separate architect-approved policy, explicit disclosure, explicit consent, provenance, rollback, validation, and conflict handling.

## Consent and Pulse Boundary

Consent does not authorize Pulse startup. Consent does not authorize Pulse endpoint calls. Consent does not authorize probing `localhost:31337`.

Pulse is central v5 infrastructure, but S12A does not start Pulse, call Pulse endpoints, or claim Pulse parity. A future live read-only trial must preserve `not-started-not-called` Pulse status unless a separate architect-approved card explicitly changes the boundary.

## Consent and PAI Memory ISA Boundary

PAI Memory and ISA artifacts are canonical PAI state. Future consent for a read-only trial must not authorize PAI Memory writes or ISA writes.

Future consent must also state that report output is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, and not runtime payload unless a separate approved contract explicitly changes that status.

## Consent Failure Conditions

Future consent fails closed if:

- Consent is absent.
- Consent is stale, ambiguous, or revoked.
- The source root does not match the consent record.
- The read scope is broader than the consent record.
- The future tool would need to read a forbidden path.
- Any write is required.
- Pulse startup or Pulse endpoint calls are required.
- PAI Memory or ISA writes are required.
- Product memory reads or promotion are required.
- Runtime adapter execution is required.
- A drop-in claim is pressured or implied.

## Required Future Proofs

Before any future live read-only trial, a later architect-approved card must prove:

- The consent disclosure is complete.
- The consent capture is explicit, bounded, revocable, and source-specific.
- Consent is not inferred from Claude Code installation, Codex installation, or dual subscriptions.
- The source root matches the consent record.
- The no-write policy is enforced.
- No root `AGENTS.md`, `.codex/`, PAI Memory write, ISA write, Pulse startup, Pulse endpoint call, product-memory promotion, Codex runtime invocation, or Claude Code invocation occurs.

## Prohibited Consent Designs

Prohibited designs:

- Consent inferred from having Claude Code installed.
- Consent inferred from having Codex installed.
- Consent inferred from having both subscriptions.
- Blanket consent over a home directory.
- Consent that includes product memory by default.
- Consent that writes to PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, or `.codex/`.
- Consent that authorizes a drop-in claim, runtime adapter implementation, live writes, Pulse startup, Pulse endpoint calls, product-memory promotion, or dual-engine uncoordinated writes.

## Non-Goals

S12A does not collect user consent, create a consent artifact, run a live read-only trial, read live existing-local-v5 state, inspect live user-local state, inspect `~/.claude/PAI`, inspect `~/.claude/projects`, inspect `~/.codex`, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, invoke Claude Code, invoke Codex as a runtime engine, implement a runtime adapter, create root `AGENTS.md`, create `.codex/`, or authorize product-memory promotion into PAI Memory.
