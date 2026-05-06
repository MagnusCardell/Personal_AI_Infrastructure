# V5 Codex PAI_DIR Dry-Run Detection Model

## Purpose

Define future PAI_DIR dry-run detection behavior without implementing or executing detection.

Codex is not currently proven drop-in for existing local PAI v5 files. S12C designs future PAI_DIR detection dry-run behavior only.

## Scope

This document is documentation/design only. S12C does not implement detection, does not create a detector script, does not create a consent artifact, does not create a consent validator, does not run a live read-only trial, and does not inspect live `PAI_DIR`.

S12C does not inspect live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, private user-local state, existing-local-v5 state, or the user's second personal clone. It does not create root `AGENTS.md`, `.codex/`, runtime adapter files, reports, fixtures, manifests, executable schemas, Memory payloads, ISA payloads, Pulse payloads, or runtime payloads.

## Evidence Base

Evidence base:

- S12A live read-only consent model.
- S12A PAI_DIR detection and source selection spec.
- S12B consent artifact schema proposal.
- S12B consent validation and revocation spec.
- S12B consent failure and abort cases.
- Existing S10/S11 fixture and harness validations.

No live user-local state, live `PAI_DIR`, live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, product memory, existing-local-v5 state, or personal clone was read for S12C.

## Detection Problem Statement

Future PAI_DIR detection must distinguish a declared source root from a live local PAI subsystem root without treating path existence as permission to read. The dry-run problem is to design how a future tool would reason about a candidate PAI_DIR under explicit consent and source selection, while refusing broad discovery, default home scans, writes, runtime invocation, Pulse calls, product-memory reads, and drop-in claims.

S12C does not solve the problem by implementing detection. It defines the future safety model that a later architect-approved detector would have to satisfy.

## Dry-Run Detection Principles

Future detection is dry-run, read-only, consent-bound, source-specific, path-bounded, abortable, and non-canonical.

The future dry-run must:

- Require an approved consent artifact reference before any live source could be considered.
- Require an explicit declared source kind and declared source root.
- Treat no default live local read as a hard boundary.
- Refuse arbitrary home-directory scans.
- Refuse runtime adapter execution.
- Refuse Pulse startup, Pulse endpoint calls, and `localhost:31337` probes.
- Refuse PAI Memory writes, ISA writes, product-memory reads by default, product-memory promotion, root `AGENTS.md`, and `.codex/`.

## Detection Input Model

Future detection inputs:

- Consent artifact reference.
- Declared source kind.
- Declared source root.
- Expected `PAI_DIR` candidate.
- Allowed read scope.
- Forbidden read scope.
- Forbidden write scope.
- Runtime prohibition policy.
- Product memory policy.
- Pulse policy.
- Memory policy.
- ISA policy.

All inputs must come from a future architect-approved contract and explicit user consent. S12C creates none of these inputs as artifacts.

## Detection Output Model

Future detection outputs:

- `detection_id`
- `source_kind`
- `declared_source_root`
- `pai_dir_candidate`
- `candidate_status`
- `confidence`
- `allowed_reads`
- `forbidden_reads`
- `forbidden_writes`
- `abort_required`
- `failure_reason`
- `non_canonical_statement`

Detection output is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.

## PAI_DIR Candidate Model

A future `pai_dir_candidate` is a declared candidate path or repository-relative fixture path, not a permission grant. It may be considered only inside a future consent-bound, source-specific, dry-run design.

Candidate statuses should be limited to future values such as:

- `not-evaluated`
- `candidate-matches-declared-root`
- `candidate-mismatch`
- `candidate-ambiguous`
- `candidate-forbidden`
- `candidate-confidence-insufficient`
- `abort-required`

S12C does not inspect live `PAI_DIR` and does not evaluate any live candidate.

## Consent Dependency Model

Future detection depends on explicit user consent plus architect approval. Consent must identify the source kind, source root, expected `PAI_DIR` candidate, allowed reads, forbidden reads, forbidden writes, retention, reporting output, and rollback/no-residue expectation.

Missing, expired, revoked, ambiguous, mismatched, or replayed consent must set `abort_required` to true before any live path read.

## Source Selection Dependency Model

Future detection depends on a source selection record that binds the declared source kind to a declared source root.

Allowed future source kinds are constrained by prior S12 design:

- `release-fixture`
- `sanitized-user-fixture`
- `existing-local-v5-read-only`
- `personal-clone-read-only`
- `unknown`

`existing-local-v5-read-only` and `personal-clone-read-only` remain future-only and require explicit architect approval plus explicit user consent.

## No-Default-Live-Read Model

No default live local read is allowed. A future detector must not read live `~/.claude`, live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, live `~/.codex/memories`, product memory, existing-local-v5 state, or a personal clone unless a later architect-approved card explicitly authorizes that exact source kind, source root, read scope, and validation model.

No default live read also means no source inference from Claude Code installation, Codex installation, dual subscriptions, shell history, product memory, or arbitrary home-directory scans.

## No-Write Detection Model

Future detection must be no-write by construction. It must not write discovered paths, confidence scores, source roots, or abort state into PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, `.codex/`, manifests, executable schemas, runtime payloads, reports, fixtures, or committed negative fixtures unless a future card separately approves a specific non-canonical write boundary.

Consent does not authorize writes.

## Product Memory Boundary

Product memory reads remain denied by default. Future detection must not infer `PAI_DIR` from product memory and must not promote product memories into PAI Memory.

Product-memory promotion requires a separate future policy with explicit architect approval, provenance, rollback, validation, conflict handling, and single-writer controls.

## Pulse Boundary

Future detection must not start Pulse, call Pulse endpoints, probe `localhost:31337`, create Pulse payloads, create Pulse bridge files, or claim Pulse parity.

Pulse status for S12C and the future dry-run model remains `not-started-not-called` unless a separate architect-approved card changes the boundary.

## Memory and ISA Boundary

PAI Memory and ISA artifacts are canonical PAI state. Future detection must not write either one.

Detection output, candidate status, source-root classification, confidence values, abort flags, and failure reasons are non-canonical dry-run evidence by default. They are not PAI Memory and not ISA.

## Abort and Failure Model

Future detection must abort when:

- Consent is missing, expired, revoked, ambiguous, mismatched, or replayed.
- The source kind or source root does not match consent.
- The candidate is ambiguous or outside allowed scope.
- The design would require reading live `~/.claude/PAI` by default.
- The design would require reading `~/.claude/projects`, `~/.codex`, product memory, or a personal clone without approval.
- The design would require any write, Pulse behavior, runtime invocation, Claude Code invocation, Codex runtime invocation, installer execution, or drop-in claim.

Abort is required safety behavior, not a warning to bypass.

## Required Future Proofs

Future detector approval would require proof that:

- Detection is dry-run, read-only, consent-bound, source-specific, path-bounded, abortable, and non-canonical.
- No default live local read occurs.
- No arbitrary home scan occurs.
- No product memory read occurs by default.
- No personal clone is inspected without explicit architect approval plus explicit user consent.
- No PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, root `AGENTS.md`, `.codex/`, runtime adapter execution, Claude Code invocation, or Codex runtime invocation occurs.
- Detection output is non-canonical and not proof that Codex is drop-in.

## Prohibited Detection Designs

Prohibited detection designs:

- Implementing a detector in S12C.
- Creating a detector script in S12C.
- Inspecting live `PAI_DIR`.
- Default reads of `~/.claude`, `~/.claude/PAI`, `~/.claude/projects`, `~/.codex`, or `~/.codex/memories`.
- Inspecting the user's second personal clone.
- Broad home-directory scans.
- Product memory reads by default.
- Writing discovered paths to PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, or `.codex/`.
- Runtime adapter execution, Claude Code invocation, Codex runtime invocation, Pulse startup, Pulse endpoint calls, installer execution, or drop-in claims.

## Non-Goals

S12C does not implement detection, create a detector script, create a consent artifact, create a consent validator, create a detection report, run a live read-only trial, read live existing-local-v5 state, inspect live user-local state, inspect live `~/.claude/PAI`, inspect live `~/.claude/projects`, inspect live `~/.codex`, inspect any personal clone, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, invoke Claude Code, invoke Codex runtime, implement a runtime adapter, create root `AGENTS.md`, create `.codex/`, authorize product-memory promotion, or claim Codex is drop-in today.
