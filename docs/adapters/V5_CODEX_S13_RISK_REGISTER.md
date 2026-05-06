# V5 Codex S13 Risk Register

## Purpose

Define the future S13 risk register for architect review.

S13 is proposed only and not approved by S12E.

## Scope

This register identifies risks for a possible future read-only S13 live local PAI v5 trial. It does not approve S13, begin S13, run a live trial, read live local state, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, create root `AGENTS.md`, create `.codex/`, or implement runtime adapter work.

## Evidence Base

Evidence base:

- S11 release-fixture evidence and readiness gates.
- S12A consent, source selection, PAI_DIR, preflight, abort, and reporting designs.
- S12B consent artifact schema and validation design.
- S12C PAI_DIR dry-run detection and source classification design.
- S12D preflight report schema, validation sequence, abort/evidence, and non-canonical output policies.
- S12E proposed S13 gates and contract.

Codex is not currently proven drop-in for existing local PAI v5 files.

## Risk Scoring Model

Impact: Low | Medium | High | Critical

Likelihood: Low | Medium | High

Status: Open | Monitoring | Blocked | Mitigated | Accepted

Risk table columns:

| Risk ID | Risk | Impact | Likelihood | Detection Signal | Mitigation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| S13-R01 | Consent ambiguity. | Critical | Medium | Consent missing, stale, revoked, inferred, or source-mismatched. | Require explicit user consent, expiration, revocation, and fail-closed validation. | Open |
| S13-R02 | Source root mismatch. | High | Medium | Selected root does not match consent or approved source record. | Bind source selection to consent and abort on mismatch. | Open |
| S13-R03 | Clean clone mistaken for live PAI install. | High | Medium | Repository clone classified as existing-local-v5 state. | Require source-root classification and evidence labels. | Open |
| S13-R04 | Personal clone access without approval. | Critical | Medium | Reads from an unapproved personal clone or second clone. | Require explicit architect approval plus explicit user consent. | Blocked |
| S13-R05 | Default home-directory scan. | Critical | Medium | Reads from `~`, `~/.claude`, `~/.codex`, or broad globbing. | Prohibit default live local reads and broad home scans. | Open |
| S13-R06 | `PAI_DIR` confidence overclaim. | High | Medium | Candidate treated as confirmed without confidence proof. | Require confidence-qualified dry-run evidence and abort on ambiguity. | Open |
| S13-R07 | Root `AGENTS.md` write pressure. | High | Medium | Root `AGENTS.md` appears in write set or changed files. | Protected-path validation and fail-closed hard failure. | Open |
| S13-R08 | `.codex/` write pressure. | High | Medium | `.codex/` appears in write set or changed files. | Protected-path validation and runtime-surface prohibition. | Open |
| S13-R09 | Pulse startup pressure. | Critical | Medium | Command starts Pulse or service bridge. | No Pulse startup gate and process/command evidence. | Open |
| S13-R10 | Pulse endpoint call pressure. | Critical | Medium | HTTP, socket, curl, or `localhost:31337` access. | No Pulse endpoint call gate and command audit. | Open |
| S13-R11 | PAI Memory write pressure. | Critical | Medium | PAI Memory file mutation, migration, or generated payload. | Memory write denial and changed-file validation. | Open |
| S13-R12 | ISA write pressure. | Critical | Medium | ISA mutation, migration, or generated payload. | ISA write denial and changed-file validation. | Open |
| S13-R13 | Product memory read leakage. | High | Medium | Product memory appears in read scope or evidence. | Deny product memory reads by default. | Open |
| S13-R14 | Product memory promotion leakage. | Critical | Low | Product memory imported or promoted into PAI Memory. | Prohibit promotion and require denied-action reporting. | Open |
| S13-R15 | Claude file direct-copy. | High | Medium | `CLAUDE.md`, hooks, commands, or skills copied into Codex surfaces. | Require unsupported-surface reporting and no direct-copy validation. | Open |
| S13-R16 | Claude Code invocation. | High | Low | Claude Code command appears in validation or logs. | Runtime invocation denial and command audit. | Open |
| S13-R17 | Codex runtime adapter execution. | Critical | Medium | Codex runtime, adapter, hook, rule, execpolicy, import, or migration command runs. | S13 remains read-only evidence; runtime execution is hard failure. | Open |
| S13-R18 | Unsupported surface silently ignored. | High | Medium | Missing unsupported-surface report or unsupported surface marked supported. | Mandatory unsupported-surface reporting. | Open |
| S13-R19 | Report becomes canonical state. | High | Medium | Report stored as PAI Memory, ISA, Pulse state, manifest, or runtime payload. | Non-canonical statement and output-path validation. | Open |
| S13-R20 | Drop-in overclaim. | Critical | Medium | Any claim Codex is drop-in today or replacement-grade. | Required no drop-in claim and content validation. | Open |
| S13-R21 | Official upstream overclaim. | High | Medium | Claim Codex is official upstream engine. | Required no official-upstream claim and content validation. | Open |
| S13-R22 | No-residue failure. | High | Medium | Residual files outside approved write set or live-source modifications. | Rollback/no-residue validation and changed-file check. | Open |
| S13-R23 | Dual-engine uncoordinated write pressure. | Critical | Low | Claude and Codex both proposed as writers to canonical state. | Preserve single-writer controls; deny all read-only S13 writes. | Open |
| S13-R24 | User misunderstands read-only scope. | High | Medium | Consent disclosure lacks clear no-write and no-drop-in boundaries. | Explicit disclosure, confirmation, and abort on ambiguity. | Open |
| S13-R25 | Runtime adapter work begins prematurely. | Critical | Medium | Runtime files, adapter plans, generated configs, launchers, or wrappers appear. | Block runtime adapter work until live-read-only evidence is accepted. | Open |

## Live Read Risk Register

The highest live-read risks are default home-directory scans, source root mismatch, personal clone access without approval, clean clone misclassification, and PAI_DIR confidence overclaim.

All live-read risks remain blocked until architect approval, explicit user consent, explicit source selection, and future preflight pass exist.

## Consent Risks

Consent risks include ambiguity, stale consent, revoked consent, inferred consent, overbroad consent, and user misunderstanding of read-only scope.

Mitigation is explicit user consent with source-specific scope, expiration, revocation, disclosure, and fail-closed validation.

## Source Selection Risks

Source selection risks include source root mismatch, clean clone confusion, personal clone access, broad home scans, and inferred source selection.

Mitigation is explicit source selection and a future source-root classification step.

## PAI_DIR Detection Risks

PAI_DIR detection risks include confidence overclaim, default live `~/.claude/PAI` reads, ambiguity, and treating path existence as permission.

Mitigation is dry-run, read-only, consent-bound, path-bounded, confidence-qualified detection with abort on ambiguity.

## Preflight Risks

Preflight risks include missing approval, invalid consent, invalid source, invalid PAI_DIR candidate, insufficient forbidden-read coverage, and treating warnings as pass.

Mitigation is a future preflight sequence that fails closed and requires pass before live reads.

## Pulse Risks

Pulse risks include startup pressure, endpoint call pressure, `localhost:31337` probes, Pulse payload creation, and Pulse parity claims.

Mitigation is no Pulse startup, no Pulse endpoint calls, no Pulse payloads, and no Pulse parity claim unless separately approved.

## Memory and ISA Risks

Memory and ISA risks include write pressure, report promotion, consent artifact promotion, and dual-engine uncoordinated writes.

Mitigation is read-only S13, no PAI Memory writes, no ISA writes, non-canonical output, and single-writer governance before any future write-mode milestone.

## Product Memory Risks

Product memory risks include read leakage and promotion into PAI Memory.

Mitigation is no product-memory reads by default, no product-memory promotion, explicit denied-action reporting, and separate architect approval for any future product-memory policy.

## Runtime Boundary Risks

Runtime boundary risks include Claude Code invocation, Codex runtime adapter execution, Codex import or migration tooling, installer execution, root `AGENTS.md`, `.codex/`, launchers, wrappers, and generated runtime config creation.

Mitigation is a hard read-only boundary and no runtime adapter work until live-read-only evidence is accepted by an architect.

## Reporting and Non-Canonical Output Risks

Reporting risks include output becoming canonical state, manifest, runtime payload, PAI runtime audit artifact, Pulse state, Memory, ISA, Claude memory, or Codex memory.

Mitigation is non-canonical output statements, approved write set only, retention policy, rollback/no-residue reporting, and content validation.

## Stop Conditions

Future S13 must stop if consent is invalid, source selection is invalid, PAI_DIR candidate confidence is insufficient, preflight does not pass, any forbidden read or write is required, Pulse behavior is required, PAI Memory or ISA writes are required, product memory access is required by default, runtime invocation is required, unsupported surfaces cannot be reported, output would become canonical, or a drop-in claim or official-upstream claim is pressured.

## Architect Review Requirements

Architect review must decide whether the S12 readiness design is accepted, whether S13A can be approved, what exact future write set is allowed, what live read scope is allowed, what consent artifact or record is acceptable, what preflight pass evidence is required, and what no-residue validation is sufficient.

S13 cannot begin without architect approval.

## Non-Goals

This risk register does not approve S13, begin S13, run a live read-only trial, read live state, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, create root `AGENTS.md`, create `.codex/`, invoke Claude Code, invoke Codex runtime, run installers, implement runtime adapter work, promote product memory, authorize dual-engine uncoordinated writes, claim Codex is drop-in today, or claim Codex is the official upstream engine.
