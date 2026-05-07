# V5 Codex S14 Risk Register

## Purpose

Define the future S14 risk register for architect review.

S14 is proposed only. S13C does not approve S14 and does not begin S14.

## Scope

This risk register covers a possible future source-selected live-read-only S14 milestone. It does not authorize existing-local-v5 access, personal-clone access, sanitized-user-fixture access, runtime adapter work, Pulse behavior, PAI Memory writes, ISA writes, root AGENTS.md, `.codex`, or drop-in claims.

## Evidence Base

Evidence base:

- S13A clean-clone positive-control trial artifacts.
- S13B clean-clone negative controls and path-safety hardening.
- S13C clean-clone closeout conclusions.
- S12/S13 consent, source-selection, PAI_DIR, preflight, abort, non-canonical evidence, and no-residue policies.

Codex is not currently proven drop-in for existing local PAI v5 files.

## Risk Scoring Model

Scoring model:

```text
Impact: Low | Medium | High | Critical
Likelihood: Low | Medium | High
Status: Open | Monitoring | Blocked | Mitigated | Accepted
```

Risk table columns:

| Risk ID | Risk | Impact | Likelihood | Detection Signal | Mitigation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| S14-R01 | Consent ambiguity. | Critical | Medium | Consent is absent, inferred, stale, broad, expired, or not source-class-bound. | Require explicit user consent with source class, source root, allowed reads, forbidden reads, retention, and no-write terms. | Open |
| S14-R02 | Source class ambiguity. | Critical | Medium | Source class is inferred, mixed, or changed mid-run. | Require architect-approved source class decision before S14 begins. | Open |
| S14-R03 | Source root mismatch. | High | Medium | Source root differs from consent or source-selection record. | Bind source root to consent and preflight; abort on mismatch. | Open |
| S14-R04 | Clean clone mistaken for live PAI install. | High | Medium | Clean-clone fixture paths are classified as live existing-local-v5 state. | Require source class classification and PAI_DIR confidence limits. | Monitoring |
| S14-R05 | Personal clone access without approval. | Critical | Medium | Personal-clone-like path appears without selected source class and consent. | Block personal-clone access unless explicitly selected and consented. | Open |
| S14-R06 | Existing-local-v5 access without approval. | Critical | Medium | Live PAI paths are accessed without explicit source class and consent. | Block existing-local-v5 access unless explicitly selected and consented. | Open |
| S14-R07 | Default home-directory scan. | Critical | Medium | `/home`, `/Users`, `~`, shell history, or broad recursive home scanning appears. | Forbid default home scans; require exact source root. | Open |
| S14-R08 | `PAI_DIR` confidence overclaim. | High | Medium | PAI_DIR detection asserts canonical identity without sufficient evidence. | Require confidence-qualified read-only PAI_DIR detection and abort cases. | Open |
| S14-R09 | Root `AGENTS.md` write pressure. | High | Medium | Root AGENTS.md appears in changed files or proposed outputs. | Protected-path validation and no root AGENTS.md acceptance criterion. | Open |
| S14-R10 | `.codex/` write pressure. | High | Medium | `.codex` config, hooks, skills, rules, memory, or commands appear. | Protected-path validation and no `.codex` acceptance criterion. | Open |
| S14-R11 | Pulse startup pressure. | Critical | Medium | Pulse service, launcher, bridge, or process starts. | Explicit no Pulse startup gate and validation. | Open |
| S14-R12 | Pulse endpoint call pressure. | Critical | Medium | `localhost:31337`, HTTP, socket, curl, health check, or bridge call appears. | Explicit no Pulse endpoint call gate and validation. | Open |
| S14-R13 | PAI Memory write pressure. | Critical | Medium | PAI Memory file mutation, generated Memory payload, or promotion appears. | Forbid PAI Memory writes; changed-file and protected-path checks. | Open |
| S14-R14 | ISA write pressure. | Critical | Medium | ISA file mutation, generated ISA payload, or update appears. | Forbid ISA writes; changed-file and protected-path checks. | Open |
| S14-R15 | Product memory read leakage. | High | Medium | Product memory is read, scanned, summarized, or used for source selection. | Product memory excluded by default; require separate approval. | Open |
| S14-R16 | Product memory promotion leakage. | Critical | Medium | Product memory is promoted into PAI Memory or canonical state. | Deny product-memory promotion and audit outputs. | Open |
| S14-R17 | Claude file direct-copy. | High | Medium | `PAI_SYSTEM_PROMPT.md`, `CLAUDE.md`, hooks, commands, or skills are copied into Codex surfaces. | Require unsupported-surface reporting instead of direct-copy. | Open |
| S14-R18 | Claude Code invocation. | High | Low | `claude` or Claude Code tooling executes. | Forbid Claude Code invocation; validate command logs and scripts. | Open |
| S14-R19 | Codex runtime adapter execution. | Critical | Medium | Codex runtime, adapter wrapper, import, migration, hook, rule, or execpolicy executes. | Keep S14 read-only evidence only; forbid runtime adapter execution. | Open |
| S14-R20 | Unsupported surface silently ignored. | Medium | Medium | Unsupported surfaces are omitted or represented as supported. | Require unsupported-surface report. | Open |
| S14-R21 | Report becomes canonical state. | High | Medium | Evidence output is copied into PAI Memory, ISA, Pulse, product memory, or runtime payload. | Non-canonical statement and forbidden-write validation. | Open |
| S14-R22 | Drop-in overclaim. | Critical | Medium | Documentation or handoff claims Codex is drop-in today. | Mandatory no drop-in claim language and content checks. | Open |
| S14-R23 | Official upstream overclaim. | Critical | Medium | Documentation claims Codex is the official upstream engine. | Mandatory no official-upstream claim language and content checks. | Open |
| S14-R24 | No-residue failure. | High | Medium | Temporary files, report sprawl, modified source roots, or generated Python artifacts remain. | Rollback/no-residue reporting and changed-file checks. | Open |
| S14-R25 | Dual-engine uncoordinated write pressure. | Critical | Medium | Claude/Codex writes occur without coordination or canonical ownership. | S14 remains read-only; no dual-engine writes. | Open |
| S14-R26 | User misunderstands read-only scope. | High | Medium | User expects migration, install, runtime adapter, or state write behavior. | Clear consent and final handoff boundaries. | Open |
| S14-R27 | Runtime adapter work begins prematurely. | Critical | Medium | Runtime files, launchers, wrappers, `.codex`, root AGENTS.md, or adapter payloads appear. | Stop condition and architect approval requirement. | Open |
| S14-R28 | Sanitized fixture mistaken for live state. | High | Medium | Sanitized fixture is treated as existing-local-v5 or personal-clone evidence. | Require explicit source class and evidence labeling. | Open |
| S14-R29 | Consent artifact persisted as product memory. | High | Low | Consent record appears in product memory or PAI Memory. | Non-canonical retention policy and forbidden writes. | Open |
| S14-R30 | Evidence report promoted into PAI state. | Critical | Low | Evidence report appears in PAI Memory, ISA, Pulse, or runtime state. | Non-canonical output policy and protected-path validation. | Open |

## Live Read Risk Register

The live read risk register is blocked until architect approval selects a future source class, source root, consent model, allowed reads, forbidden reads, approved write set, and preflight validation.

No live-read gate is passed by S13C.

## Consent Risks

Primary consent risks are consent ambiguity, stale consent, missing source class binding, missing source root binding, overbroad retention, and confusion between adapter-test evidence and canonical state.

Future S14 must require explicit user consent and must not infer consent from local installation state, product memory, shell history, or prior interaction.

## Source Class Risks

Source class risks include clean clone mistaken for live state, personal clone access without approval, existing-local-v5 access without approval, and sanitized fixture mistaken for live state.

None of `existing-local-v5-read-only`, `personal-clone-read-only`, or `sanitized-user-fixture-read-only` is approved by S13C.

## Source Selection Risks

Source selection risks include source root mismatch, default home-directory scans, inferred source roots, product-memory-assisted selection, and unbounded path traversal.

Future S14 must require explicit source selection.

## PAI_DIR Detection Risks

PAI_DIR risks include confidence overclaim, broad discovery, default live `~/.claude/PAI` reads, and classifying clean-clone or sanitized fixtures as live installs.

PAI_DIR detection must remain read-only, source-bound, consent-bound, and abortable.

## Preflight Risks

Preflight risks include stale consent, missing source class, missing source root, failed path boundary checks, unsupported surfaces, write pressure, Pulse pressure, Memory/ISA pressure, product memory pressure, and runtime pressure.

Any failed preflight check must abort.

## Pulse Risks

Pulse is central v5 infrastructure, but S14 must not start Pulse or call Pulse endpoints unless separately approved.

Pulse risks include startup pressure, endpoint-call pressure, `localhost:31337` probes, report promotion into Pulse, and false Pulse parity claims.

## Memory and ISA Risks

PAI Memory and ISA artifacts are canonical PAI state.

Future S14 must not write PAI Memory or ISA, must not promote consent or reports into Memory or ISA, and must not authorize dual-engine uncoordinated writes.

## Product Memory Risks

Product memory risks include default reads, source selection leakage, summary leakage, and silent promotion into PAI Memory.

Future S14 must not read product memories by default and must not promote product memory.

## Runtime Boundary Risks

Runtime boundary risks include Claude Code invocation, Codex runtime adapter execution, Codex import/migration tooling, hook/rule/execpolicy commands, installer execution, root AGENTS.md creation, `.codex` creation, and runtime payload creation.

Future S14 must remain read-only unless separately approved.

## Reporting and Non-Canonical Output Risks

Reporting risks include evidence becoming canonical state, unsupported surfaces being silently ignored, denied actions being omitted, no-residue not being proven, and drop-in or official-upstream overclaims.

S14 reports must remain non-canonical adapter-test evidence only.

## Stop Conditions

Stop immediately if S14 would require unapproved source access, personal-clone access, existing-local-v5 access, broad home scans, PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, root AGENTS.md, `.codex`, Claude Code invocation, Codex runtime execution, product memory promotion, report promotion into canonical state, or runtime adapter work.

## Architect Review Requirements

Architect approval is required before any S14 work.

The architect must decide whether to approve a source class, source root boundary, consent model, PAI_DIR detection method, preflight report shape, validation commands, approved write set, no-residue expectations, and final handoff format.

## Non-Goals

This risk register does not approve S14, begin S14, select a source class, collect consent, read existing-local-v5 state, read a personal clone, read sanitized fixtures as live state, inspect live user-local state, write PAI Memory, write ISA, start Pulse, call Pulse endpoints, probe `localhost:31337`, invoke Claude Code, invoke Codex runtime, create root AGENTS.md, create `.codex`, create runtime payloads, implement a runtime adapter, claim Codex is drop-in today, or claim Codex is official upstream.
