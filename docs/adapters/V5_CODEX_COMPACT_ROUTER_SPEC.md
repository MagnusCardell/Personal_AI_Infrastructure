# V5 Codex Compact Router Spec

## Purpose

Specify the future compact Codex router concept without creating root `AGENTS.md` or any Codex runtime guidance file.

## Scope

S7A does not create `AGENTS.md`.

Root `AGENTS.md` remains repo-maintainer governance unless later explicitly authorized.

`.codex/` remains protected and is not created in S7A.

This document is design-only. It does not implement a Codex adapter, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create runtime files, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, or run Codex import or migration tooling.

## Evidence Base

Evidence comes from:

- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `Releases/v5.0.0/.claude/CLAUDE.md`
- `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md`

No new Codex capability claim is introduced in S7A. Codex `AGENTS.md`, Codex config, Codex memory, instruction ordering, and size-risk facts are inherited from S2/S3 official-source evidence.

## Router Problem Statement

Codex is not currently proven drop-in for existing local PAI v5 files.

The future router problem is to give Codex a small, native orientation layer that points to PAI doctrine, trial policy, protected paths, unsupported surfaces, and handoff expectations without cloning Claude Code files.

Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists. Codex replacement is plausible only through a designed adapter.

## Router Non-Goals

The future compact router is not:

- A clone of `CLAUDE.md`.
- A clone of `PAI_SYSTEM_PROMPT.md`.
- A replacement for PAI doctrine.
- A Codex config/profile file.
- PAI Memory.
- ISA.
- Pulse state.
- A Pulse bridge.
- A launcher.
- A read-only trial manifest.
- Proof that Codex is drop-in.

## Router Design Principles

Router principles:

- Compact router, not doctrine dump.
- Native Codex guidance, not Claude-shaped material.
- PAI doctrine remains in `PAI_SYSTEM_PROMPT.md` semantics.
- `CLAUDE.md` remains Claude-facing evidence only.
- No direct copying of Claude-shaped files.
- No release-file mutation.
- No product memory content.
- No ISA acceptance logic.
- No Pulse bridge claim.
- Read-only first.
- Reversible by default.
- Single-writer policy required before future writes.

## Future Router Placement Options

Future router placement options are design candidates only:

| Option | Candidate placement | S7A status | Key risk |
| --- | --- | --- | --- |
| RPO-1 | Root `AGENTS.md` as repo-level guidance, if maintainer-authorized. | Not created. | Could mix repo governance with runtime adapter material. |
| RPO-2 | Nested adapter-local guidance, if future layout authorizes it. | Not created. | Might not apply to actual PAI runtime roots. |
| RPO-3 | Future launcher-mediated instructions, if supported and tested. | Not created. | Requires launcher seam and authority envelope proof. |
| RPO-4 | No-router mode for evidence-only trial. | Design candidate. | May leave too much guidance outside Codex-native discovery. |

S7A does not choose or implement any placement.

## Router Content Model

Compact router content categories:

- PAI role statement.
- PAI doctrine reference.
- `PAI_DIR` resolution rule.
- Read-only trial posture.
- Protected path summary.
- Unsupported-surface reporting.
- Handoff/audit behavior.
- Escalation-to-architect rule.

The router must reference approved doctrine and trial policy without embedding the full doctrine body.

## Router Exclusion Model

Router exclusions:

- No full `PAI_SYSTEM_PROMPT.md`.
- No full `CLAUDE.md`.
- No Claude hook code.
- No Claude settings JSON.
- No Claude skill, agent, or command copy.
- No product memory content.
- No ISA acceptance logic.
- No Pulse bridge claim.
- No private user-local state.
- No generated Codex config.
- No runtime launch instructions.

Claude-shaped files must not be copied directly into Codex surfaces.

## Router Reference Model

Future router references must be explicit, bounded, and reviewable.

Allowed reference types for a future design may include:

- Approved PAI doctrine source identifiers.
- Approved read-only adapter docs.
- Approved release fixture paths.
- Approved trial policy or manifest identifiers.
- Unsupported-surface report instructions.

Denied reference behavior:

- Unbounded recursive imports.
- Private user-local state references.
- Product memory reads.
- Live PAI Memory or ISA reads without an approved read-only trial policy.
- Pulse endpoint calls.
- Release-file mutation.

## Router Safety Requirements

Safety requirements:

- The router must state that it is not PAI Memory.
- The router must state that it is not ISA.
- The router must state that it is not Pulse state.
- The router must preserve `PAI_SYSTEM_PROMPT.md` as high-authority doctrine.
- The router must preserve `CLAUDE.md` as a Claude-facing surface, not a Codex destination file.
- The router must report unsupported surfaces rather than hiding them.
- The router must not authorize writes.
- The router must not authorize trial execution by itself.
- The router must not require uninstalling Claude Code.

## Router Size and Truncation Policy

The compact router should be intentionally small.

Future validation must prove:

- The router fits the selected Codex guidance mechanism.
- It does not crowd out higher-priority trial policy.
- It does not depend on unbounded doctrine copying.
- It reports omitted or unsupported context.
- Size limits cannot silently remove read-only, protected-path, memory, ISA, Pulse, or no-copy rules.

## Router Interaction With Codex Config

Codex config/profile is policy/configuration, not Life OS doctrine.

The router must not depend on `.codex/` creation in S7A. Future interaction with Codex config requires architect approval, explicit write set, trust model, protected-path policy, and validation.

## Router Interaction With Codex Memory

Codex memory is not doctrine and not PAI Memory.

The router must not embed, import, summarize, or promote Codex memory. If future Codex memory conflicts with PAI doctrine, PAI doctrine wins and the conflict is reported.

## Router Interaction With Goal State

`/goal` state is workflow-control state.

The router must not treat `/goal` state as doctrine, ISA, PAI Memory, Pulse state, or replacement readiness. Goal completion is not ISA acceptance.

## Router Interaction With PAI Memory and ISA

PAI Memory and ISA artifacts are canonical PAI state.

The router may only describe their protected status. It must not authorize PAI Memory writes, ISA writes, live reads, curation, promotion, or acceptance behavior.

Future writes require a single-writer policy, provenance, rollback, and validation.

## Router Interaction With Pulse

Pulse remains central v5 infrastructure, but S7A does not design or implement a Pulse bridge.

The router must not claim Pulse parity, start Pulse, contact Pulse, write Pulse state, or overload Claude Pulse job identity.

## Example Non-Executable Router Skeleton

`NON-EXECUTABLE DESIGN SKETCH — DO NOT INSTALL`

```text
Purpose:
  This future Codex router orients Codex to PAI v5 adapter trial posture.
  It is not PAI doctrine, not PAI Memory, not ISA, and not Pulse state.

Doctrine:
  Preserve PAI_SYSTEM_PROMPT.md semantics as high-authority PAI doctrine.
  Do not copy PAI_SYSTEM_PROMPT.md into this router.
  Treat CLAUDE.md as Claude-facing operational evidence only.

Runtime posture:
  Codex is not currently proven drop-in for existing local PAI v5 files.
  Operate only under an architect-approved read-only trial or adapter milestone.
  Report unsupported Claude-shaped surfaces explicitly.

State boundaries:
  Do not write PAI Memory, ISA, Pulse state, release files, root AGENTS.md, or .codex/.
  Do not treat Codex memory, transcripts, SDK threads, or /goal state as PAI Memory.

Escalation:
  Stop and request architect review if authority ordering, source scope, protected paths,
  memory boundaries, ISA boundaries, or Pulse posture are unclear.
```

This skeleton is a markdown design sketch only. It must not be installed, copied into root `AGENTS.md`, copied into `.codex/`, or used as runtime material in S7A.

## Router Validation Requirements

Future router validation must prove:

- The router is compact.
- The router does not clone `CLAUDE.md`.
- The router does not clone `PAI_SYSTEM_PROMPT.md`.
- The router preserves high-authority doctrine priority.
- The router reports unsupported surfaces.
- The router blocks copying Claude-shaped files.
- The router does not authorize writes.
- The router does not authorize existing-local-v5 trial execution.
- The router does not treat Codex memory, transcripts, SDK threads, or `/goal` state as PAI Memory.
- The router does not treat `/goal` as ISA.
- The router does not claim Pulse implementation.

## Prohibited Router Designs

Prohibited router designs:

- Root `AGENTS.md` creation in S7A.
- `.codex/` creation in S7A.
- Full `PAI_SYSTEM_PROMPT.md` copy.
- Full `CLAUDE.md` copy.
- Claude settings JSON copy.
- Claude hooks, skills, agents, or commands copy.
- Product memory imports.
- ISA acceptance logic.
- Pulse bridge or parity claim.
- Generated Codex config.
- Runtime launcher instructions.
- Installation instructions for the non-executable router skeleton.

## Non-Goals

S7A does not create `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create runtime files, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, run Codex import or migration tooling, claim Codex is drop-in today, claim Codex is the official upstream engine, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, or advance beyond S7A.
