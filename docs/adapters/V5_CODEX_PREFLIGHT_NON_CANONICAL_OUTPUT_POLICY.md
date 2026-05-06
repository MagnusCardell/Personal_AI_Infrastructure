# V5 Codex Preflight Non-Canonical Output Policy

## Purpose

Define future non-canonical output policy for preflight reports.

Codex is not currently proven drop-in for existing local PAI v5 files. S12D creates no preflight report.

## Scope

This document is documentation/design only. It defines future preflight output policy without creating output.

S12D does not create a preflight report, implement a preflight runner, create a detector script, create a consent artifact, create a consent validator, run a live read-only trial, read live existing-local-v5 state, inspect private user-local state, inspect a personal clone, or implement runtime adapter behavior.

## Evidence Base

Evidence base:

- S12A live read-only reporting boundary spec.
- S12A preflight and abort model.
- S12B consent non-canonical reporting design.
- S12C PAI_DIR dry-run reporting spec.
- S12D preflight report schema and abort evidence models.

No live local state was read and no report was created for S12D.

## Output Policy Problem Statement

Future preflight output may be useful for architect review, but it must not become canonical PAI state, runtime payload, manifest, memory, Pulse state, or drop-in proof.

The output policy must prevent report data from becoming a back door into writes, product-memory promotion, runtime adapter work, Pulse calls, or live existing-local-v5 trial authorization.

## Output Principles

Future preflight output must be:

- Advisory.
- Non-canonical by default.
- Read-only in source behavior.
- Consent-bound.
- Retention-bounded.
- Rollback/no-residue-bounded.
- Clear about denied actions and unsupported surfaces.
- Explicit that Codex is not currently proven drop-in.

## Non-Canonical Output Model

Future preflight output must be advisory and non-canonical by default.

Future output is not PAI Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a manifest, not runtime payload, and not proof that Codex is drop-in.

Non-canonical output cannot authorize live reads, writes, runtime adapter implementation, Pulse startup/calls, product-memory promotion, root `AGENTS.md`, `.codex/`, or dual-engine uncoordinated writes.

## Retention Policy Model

Future preflight output must include a retention policy. Retention must be bounded by consent, revocation, expiration, rollback/no-residue expectations, and a future approved write set.

Missing retention policy must abort or fail preflight validation.

## Privacy Policy Model

Future output must minimize private path disclosure and must not include forbidden read content.

Output must not include live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, product memory, personal clone content, or existing-local-v5 content unless a future architect-approved card explicitly permits the exact read and report scope.

## No-Promotion Policy

Future output must not be promoted into PAI Memory by default.

Future output must not be used to update ISA by default. Future output must not be submitted to Pulse by default. Future output must not be stored in Claude memory or Codex memory by default.

Product memories must not be silently promoted into PAI Memory.

## PAI Memory Boundary

PAI Memory is canonical PAI state. Future preflight output is not PAI Memory and must not write PAI Memory.

Any future promotion into PAI Memory would require a separate architect-approved write policy, single-writer controls, provenance, rollback, validation, and conflict handling.

## ISA Boundary

ISA is canonical PAI state. Future preflight output is not ISA and must not update ISA by default.

Any future ISA write would require separate architect approval and is outside S12D.

## Pulse Boundary

Future output is not Pulse state and must not be submitted to Pulse by default.

Preflight output must not start Pulse, call Pulse endpoints, probe `localhost:31337`, create Pulse payloads, create Pulse bridge files, or claim Pulse parity.

## Claude Memory Boundary

Future output is not Claude memory and must not be stored in Claude memory by default.

Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists, but S12D does not invoke Claude Code and does not write Claude-facing memory.

## Codex Memory Boundary

Future output is not Codex memory and must not be stored in Codex memory by default.

S12D does not create `.codex/`, Codex config, Codex memory, Codex hooks, Codex rules, Codex commands, or runtime adapter files.

## Manifest Boundary

Future output is not a manifest. It must not be treated as an executable schema, manifest instance, install manifest, audit artifact, or runtime adapter payload.

Manifest pressure must abort or fail validation.

## Runtime Payload Boundary

Future output is not runtime payload. It must not create generated runtime configs, launchers, wrappers, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, live-trial artifacts, or runtime files.

Runtime payload pressure must abort.

## Drop-In Claim Boundary

Future output must keep drop-in claim status as `not-claimed`.

Future preflight output can only say whether a future source is eligible for an architect-approved read-only trial. It cannot prove Codex drop-in behavior, official upstream engine status, runtime parity, or replacement-grade behavior.

## Required Future Proofs

Future implementation would need proof that:

- Output is non-canonical.
- Output writes only to an approved future path.
- Output has retention and rollback/no-residue boundaries.
- Output is not PAI Memory, ISA, Pulse state, Claude memory, Codex memory, manifest, runtime payload, or drop-in proof.
- Output does not create root `AGENTS.md` or `.codex/`.
- Output does not authorize PAI Memory writes, ISA writes, Pulse startup/calls, product-memory promotion, personal-clone access, runtime adapter work, or live trial execution.

## Prohibited Output Policies

Prohibited output policies:

- Treating preflight output as canonical state by default.
- Promoting preflight output into PAI Memory.
- Updating ISA from preflight output by default.
- Submitting preflight output to Pulse by default.
- Storing preflight output in Claude memory or Codex memory by default.
- Creating root `AGENTS.md` or `.codex/`.
- Treating output as a manifest, runtime payload, executable schema, or drop-in proof.
- Using output to authorize live existing-local-v5 trial execution or runtime adapter work.

## Non-Goals

S12D creates no preflight report, creates no preflight runner, creates no detector script, creates no consent artifact, creates no consent validator, creates no runtime payload, creates no manifest, runs no live read-only trial, reads no live existing-local-v5 state, inspects no private user-local state, inspects no personal clone, writes no PAI Memory, writes no ISA, starts no Pulse, calls no Pulse endpoints, invokes no Claude Code, invokes no Codex runtime, implements no runtime adapter, creates no root `AGENTS.md`, creates no `.codex/`, and authorizes no product-memory promotion.
