# V5 Codex Source Root Classification and Guardrail Spec

## Purpose

Define future source-root classes, allowed and denied root behavior, and guardrails for PAI_DIR detection dry-run design.

Codex is not currently proven drop-in for existing local PAI v5 files. S12C designs classification and guardrails only.

## Scope

This document is documentation/design only. It does not implement classification, does not inspect live roots, does not inspect any personal clone, and does not authorize live existing-local-v5 access.

S12C does not create a detector script, consent artifact, consent validator, runtime adapter file, report, fixture, manifest, executable schema, live-trial artifact, runtime payload, root `AGENTS.md`, or `.codex/`.

## Evidence Base

Evidence base:

- S12A PAI_DIR detection and source selection spec.
- S12A consent model.
- S12B consent artifact schema proposal.
- S12B consent validation and revocation spec.
- S12B consent failure and abort cases.
- Existing S10/S11 fixture evidence.

No live `~/.claude/PAI`, live `~/.claude/projects`, live `~/.codex`, private user-local state, existing-local-v5 state, product memory, or personal clone was read.

## Classification Problem Statement

Future dry-run detection needs a conservative source-root classification model so a tool does not mistake a clean clone, release fixture, sanitized fixture, existing local PAI install, or unknown path for a read authorization.

Classification is not consent. Classification is not write permission. Classification is not proof that Codex is drop-in.

## Source Root Classification Model

Source root classes:

- `release-fixture`: repository-local release or fixture material approved by S10/S11/S12 contracts.
- `sanitized-user-fixture`: future sanitized user-provided fixture data approved by a later card.
- `existing-local-v5-read-only`: future-only read-only access to live existing local PAI v5 state.
- `personal-clone-read-only`: future-only read-only access to a user-provided personal clone.
- `unknown`: any source root that cannot be classified safely.

`existing-local-v5-read-only` and `personal-clone-read-only` are future-only and require explicit architect approval plus explicit user consent.

## Release Fixture Source Rules

`release-fixture` sources are repository-local, approved by prior fixture/evidence contracts, and bounded to the current repository. S12C may refer to repository-local release fixture evidence but does not modify release files.

Release fixture classification must not imply permission to write `Releases/`, update manifests, create runtime payloads, or treat fixture metadata as live local state.

## Sanitized User Fixture Source Rules

`sanitized-user-fixture` remains future-only unless a later architect-approved card supplies a sanitized fixture inside an approved boundary.

Sanitized fixture classification requires explicit provenance, no private-state leakage, no product-memory promotion, no Pulse startup/calls, and no PAI Memory or ISA writes.

S12C creates no sanitized fixture.

## Existing Local v5 Source Rules

`existing-local-v5-read-only` is future-only. It requires explicit architect approval plus explicit user consent.

Future classification must not read live `~/.claude/PAI` by default. It must not infer an existing-local-v5 source from home-directory layout, Claude Code installation, Codex installation, dual subscriptions, shell history, or product memory.

Existing local v5 classification never implies permission to write.

## Personal Clone Boundary Rules

`personal-clone-read-only` is future-only. It requires explicit architect approval plus explicit user consent.

S12C does not inspect any personal clone. S12C does not inspect the user's second personal clone.

A clean cloned repo without installer-run PAI state can be classified only from repository-local evidence in S12C. Clean clone status does not imply live PAI install, existing-local-v5 state, user consent, or permission to read private local state.

## Allowed Root Patterns

Allowed future root patterns are design-only and require future approval:

- Repository-local approved fixture roots.
- Repository-local approved release fixture paths used as evidence.
- Future approved sanitized-user-fixture roots.
- Future explicitly consented `existing-local-v5-read-only` roots.
- Future explicitly consented `personal-clone-read-only` roots.

No root is read by default.

## Forbidden Root Patterns

Forbidden root patterns:

- `~/.claude`
- `~/.claude/PAI`
- `~/.claude/projects`
- `~/.codex`
- `~/.codex/memories`
- Arbitrary home-directory scans.
- Root `AGENTS.md`.
- `.codex/`.
- `Releases/` writes.

Any future root pattern that would require product memory reads, Pulse startup/calls, PAI Memory writes, ISA writes, runtime adapter execution, Claude Code invocation, Codex runtime invocation, installer execution, or unapproved personal-clone access must be rejected.

## Guardrail Model

Guardrails:

- No root is read by default.
- No source-root classification may imply permission to write.
- Classification must fail closed on ambiguity.
- Classification must preserve forbidden read and forbidden write scopes.
- Classification output is non-canonical.
- Classification cannot authorize root `AGENTS.md`, `.codex/`, runtime adapter files, reports, fixtures, manifests, schemas, live-trial artifacts, runtime payloads, Memory payloads, ISA payloads, or Pulse payloads.

## Product Memory Guardrails

Product memory reads remain denied by default. Source-root classification must not inspect product memory and must not infer source roots from product memory.

Product memories must not be silently promoted into PAI Memory.

## Pulse Guardrails

Source-root classification must not start Pulse, call Pulse endpoints, probe `localhost:31337`, create Pulse payloads, create Pulse bridge files, or claim Pulse parity.

Pulse status remains not-started-not-called.

## Memory and ISA Guardrails

Source-root classification must not write PAI Memory or ISA. It must not store discovered roots, candidate paths, confidence, abort state, or reports in canonical PAI state.

Classification output is not PAI Memory and not ISA.

## Runtime Guardrails

Source-root classification must not invoke Claude Code, invoke Codex as a runtime engine, run Codex import/migration tooling, run Codex hook/rule/execpolicy commands, run installers, create launchers, create wrappers, or implement runtime adapter behavior.

Claude-shaped files must not be copied directly into Codex surfaces.

## Required Future Proofs

Future classification approval would require proof that:

- Source root classes are explicit and source-specific.
- `existing-local-v5-read-only` and `personal-clone-read-only` require explicit architect approval plus explicit user consent.
- No default root read occurs.
- No arbitrary home-directory scan occurs.
- No personal clone is inspected without approval.
- Clean clone status is not treated as live PAI install.
- No classification implies permission to write.

## Prohibited Classification Designs

Prohibited designs:

- Reading live `~/.claude/PAI` by default.
- Reading live `~/.claude/projects` or live `~/.codex`.
- Inspecting the user's second personal clone.
- Treating a clean clone as a live PAI install.
- Inferring consent from source-root classification.
- Authorizing personal-clone access in S12C.
- Writing classification output to PAI Memory, ISA, Pulse, Claude memory, Codex memory, root `AGENTS.md`, or `.codex/`.
- Running Claude Code, Codex runtime, installers, Pulse, or runtime adapter code.

## Non-Goals

S12C does not inspect any personal clone, inspect live `~/.claude/PAI`, inspect live `~/.claude/projects`, inspect live `~/.codex`, read live existing-local-v5 state, classify an actual live source root, implement a classifier, create a detector script, create a consent artifact, create a consent validator, create reports, create fixtures, modify releases, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, invoke Claude Code, invoke Codex runtime, create root `AGENTS.md`, create `.codex/`, or claim Codex is drop-in today.
