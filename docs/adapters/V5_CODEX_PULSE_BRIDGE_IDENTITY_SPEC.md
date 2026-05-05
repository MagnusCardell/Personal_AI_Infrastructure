# V5 Codex Pulse Bridge Identity Spec

## Purpose

Define the future identity model for any Codex-to-Pulse bridge so Codex activity is never confused with Claude Code, the official Claude engine, the DA identity, or canonical PAI state.

## Scope

S7E designs Pulse bridge identity only. It does not implement a Pulse bridge, create a bridge identity instance, start Pulse, call Pulse endpoints, probe `localhost:31337`, create Pulse payloads, create runtime files, create Codex config, create hooks, create rules, create launchers, create wrappers, create root `AGENTS.md`, create `.codex/`, run a read-only trial, inspect private user-local state, or modify release files.

Codex is not currently proven drop-in for existing local PAI v5 files. Codex replacement is plausible only through a designed adapter. Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.

## Evidence Base

Evidence comes from:

- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/DaSubsystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Observability/ObservabilitySystem.md`
- `Releases/v5.0.0/.claude/PAI/PULSE/pulse.ts`
- `Releases/v5.0.0/.claude/PAI/PULSE/PULSE.toml.example`
- `Releases/v5.0.0/.claude/PAI/PULSE/modules/hooks.ts`
- `Releases/v5.0.0/.claude/PAI/PULSE/Observability/observability.ts`
- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md`
- `/tmp/v5-s7e-pulse-files.txt`
- `/tmp/v5-s7e-pulse-search.txt`

No new Codex capability claim is introduced in S7E. Codex config/profile, Codex hooks, Codex rules, Codex memory, `AGENTS.md`, sandbox, and approval facts are inherited from prior official-source adapter evidence.

## Pulse Identity Problem Statement

Pulse is central v5 infrastructure and not optional background trivia. Release evidence describes Pulse as the Life Dashboard, the visible surface of the PAI Life Operating System, and the unified local runtime for cron jobs, voice notifications, hook validation, observability APIs, dashboard serving, chat modules, work polling, and DA subsystem work.

Current Pulse release evidence is Claude Code-native in several places: it can run `type = "claude"` jobs, it includes hook guard routes shaped for Claude tool payloads, it reads state under `~/.claude/PAI`, and its observability events use Claude session and hook-derived fields. A future Codex bridge identity must make Codex-originated activity explicitly distinguishable instead of overloading Claude identity, DA identity, or canonical PAI Memory/ISA/Pulse state.

S7E does not start Pulse or call Pulse endpoints.

## PAI Pulse Role Model

Pulse is the release-local daemon and dashboard layer for visible PAI activity. Evidence identifies:

- A single Bun daemon process in `PULSE/pulse.ts`.
- A default port of `31337`.
- A Life Dashboard served by the observability module.
- Hook validation routes under `/hooks/*`.
- Voice and notification routes such as `/notify`.
- Observability APIs, JSONL event readers, static dashboard pages, Wiki/Knowledge APIs, and health/status reporting.
- Cron/job execution and state persistence.

S7E treats Pulse centrality as a safety requirement. Codex must not be considered replacement-capable until Pulse identity, event, audit, rollback, PAI Memory, and ISA boundaries have future proof.

## Engine Identity Model

Future engine identity must distinguish:

| Engine identity | Meaning | S7E posture |
| --- | --- | --- |
| `claude-code-official` | Current official/full-support upstream engine for PAI v5. | Evidence only; not invoked. |
| `codex-adapter-candidate` | Future beta local engine candidate behind a designed adapter. | Design candidate only. |
| `unknown-engine` | Any runtime whose identity cannot be proven. | Denied for Pulse bridge use. |

Codex must not impersonate Claude Code. Codex must not claim official/full-support engine identity. Codex may only appear in future Pulse-facing data as a clearly labeled Codex adapter candidate after architect approval and tests.

## Bridge Identity Model

A future bridge identity is a provenance envelope for Pulse-facing Codex activity. It is not a runtime bridge, not Pulse state, not PAI Memory, not ISA, and not product memory.

Required future identity fields:

| Field | Purpose |
| --- | --- |
| `bridge_id` | Stable future bridge identity for a specific approved bridge design. |
| `bridge_kind` | Bridge class such as documentation-only, manifest-mediated, or future Pulse-registered beta engine. |
| `engine_id` | Explicit engine identity, never inferred from product memory or transcripts. |
| `adapter_mode` | Mode such as documentation-only, fixture-read-only, or future controlled mode. |
| `source_kind` | Evidence, fixture, sanitized fixture, or future approved existing-local-v5 source class. |
| `pai_version` | PAI release version under evaluation. |
| `pai_dir` | Explicit PAI root for future approved runs; not inferred from private user-local state in S7E. |
| `authority_envelope_id` | Reference to an approved authority envelope. |
| `event_source` | Future event origin class, such as Codex adapter or PAI runtime. |
| `event_actor` | Actor label for the future event, distinct from Claude Code and DA identity. |
| `event_origin` | Origin evidence for the event, such as release fixture or future trial session. |
| `da_identity_reference` | Reference to DA identity policy, never authority to write as the DA by default. |
| `session_id` | Future session identifier, distinct from Claude Code session identity unless explicitly mapped. |
| `trial_id` | Future trial identifier, if a trial is approved. |
| `audit_id` | Future audit output identifier. |
| `provenance` | Source, timestamp, version, and decision lineage. |

S7E does not create a bridge identity instance.

## DA Identity Boundary

Release DA subsystem design puts DA identity under Pulse and PAI user identity structures. Codex must not write as the DA unless a future identity policy authorizes it.

Future Codex/Pulse bridge events must not claim DA authorship merely because Codex produced text, advisory output, or a task handoff. DA identity, DA heartbeat, DA scheduling, and DA growth remain PAI/Pulse concerns requiring future policy.

Product memories, `/goal`, transcripts, and SDK threads are not Pulse identity sources and are not PAI Memory.

## Claude Code Identity Boundary

`CLAUDE.md` is an official Claude-facing surface, not a Codex destination file. Claude-shaped files must not be copied directly into Codex surfaces.

Future Codex events must not reuse Claude Code identity labels, Claude `type = "claude"` job identity, Claude session identity, or Claude hook payload assumptions as proof of compatibility. Claude Code remains the official/full-support upstream engine until replacement-grade validation exists.

## Codex Identity Boundary

Future Codex `AGENTS.md`, if later authorized, must be a compact router and must not clone `CLAUDE.md` or `PAI_SYSTEM_PROMPT.md`.

Codex config/profile is policy/configuration, not Life OS doctrine. Codex hooks and rules are future native control surfaces, not Claude hook destinations. Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.

Codex identity for Pulse-facing work must be explicit, beta/candidate-labeled until proven, and reversible.

## Event Source Identity Rules

Future Pulse events from Codex must be explicitly labeled as Codex-adapter events.

Identity rules:

- `PAI_SYSTEM_PROMPT.md` remains high-authority PAI doctrine.
- `CLAUDE.md` remains Claude-facing guidance and is not a Codex destination.
- `AGENTS.md`, if later authorized, is a compact router, not a Pulse identity source.
- Product memories are not PAI Memory and not Pulse identity.
- `/goal` state is workflow-control state, not ISA and not Pulse identity.
- Event source labels must preserve `engine_id`, `bridge_id`, `adapter_mode`, and provenance.
- Unsupported identity mappings must produce an `unsupported_surface_report`.

## Job and Automation Identity Rules

Pulse job evidence includes script jobs and Claude jobs. Future Codex work must not overload `type = "claude"` for Codex.

Future job or automation identity rules:

- Codex jobs, if ever authorized, require a distinct job kind or bridge label.
- Pulse startup, job mutation, scheduling, notifications, and state mutation are denied in read-only posture.
- Existing Claude jobs remain Claude jobs unless a future migration policy explicitly changes them.
- Job output must not write PAI Memory, ISA, or Pulse state in read-only mode.
- Automation identity must include rollback and audit fields.

## Memory and ISA Identity Boundary

PAI Memory and ISA artifacts are canonical PAI state. Future writes require a single-writer policy, provenance, rollback, and validation.

Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory. Product memories must not be silently promoted into PAI Memory.

Pulse-related Codex identity must not treat advisory output, event proposals, local recall, or `/goal` completion as PAI Memory, ISA acceptance, DA authorship, or Pulse state.

## Audit Identity Fields

Future audit identity reporting must include:

| Field | Required treatment |
| --- | --- |
| `audit_id` | Stable future audit identifier. |
| `bridge_id` | Bridge identity or explicit `none` for no bridge. |
| `engine_id` | Explicit engine identity. |
| `adapter_mode` | Mode that controls read/write posture. |
| `source_kind` | Source class used for evidence or future trial. |
| `event_source` | Event source label, never inferred silently. |
| `event_actor` | Actor label, distinct from DA and Claude Code unless proven. |
| `event_origin` | Origin evidence or approved trial source. |
| `authority_envelope_id` | Authority envelope reference. |
| `trial_id` | Future trial identifier or explicit `none`. |
| `provenance` | Evidence chain and version lineage. |

## Candidate Bridge Identity Designs

| Candidate | Summary | Inputs | Outputs | Safety | Reversibility | Drop-in readiness | Main risk | Required future proofs | S7E decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PI-1 | Documentation-only bridge identity contract. | S7E docs, S6 Pulse couplings, S7A/S7C/S7D seam docs, release Pulse evidence. | Future identity field model and prohibited identity rules. | Safe because it creates no bridge identity instance, Pulse payload, or runtime file. | Fully reversible; docs only. | Prerequisite design only. | Too abstract without fixture validation. | Architect review, field completeness, no-start/no-call proof, no-write proof. | Design candidate only; no runtime implementation chosen. |
| PI-2 | Future manifest-mediated Codex adapter identity. | Approved manifest, authority envelope, source kind, adapter mode, audit policy. | Non-runtime or future quarantined identity envelope for approved trials. | Safer for read-only trials because source roots and denied actions are explicit. | Reversible if generated outputs stay outside live PAI, Claude, Codex, and Pulse roots. | Candidate for fixture and later read-only validation. | Manifest drift or identity misbinding. | Manifest validation, bridge identity tests, Pulse no-start proof, Memory/ISA no-write proof. | Deferred; no runtime implementation chosen. |
| PI-3 | Future Pulse-registered beta engine identity. | Future Pulse bridge milestone, native engine profile, approved identity policy, rollback plan. | Runtime-visible beta engine identity in future Pulse bridge events. | Highest risk because it approaches live Pulse integration. | Requires rollback, single-writer, and fallback proof before use. | Candidate only after Pulse bridge tests and G8 progress. | Codex could be mistaken for official Claude Code or DA identity. | Pulse event tests, identity collision tests, audit proof, rollback proof, Memory/ISA proof. | Deferred; no runtime implementation chosen. |

S7E chooses no runtime implementation for `PI-1`, `PI-2`, or `PI-3`.

## Required Future Proofs

Future Pulse identity work must prove:

- Codex is explicitly labeled as a Codex adapter candidate.
- Codex does not impersonate Claude Code.
- Codex does not claim official/full-support engine identity.
- Codex does not write as the DA by default.
- Pulse events from Codex include bridge identity, engine identity, adapter mode, and provenance.
- Product memories, `/goal`, transcripts, and SDK threads remain outside PAI Memory, ISA, and Pulse identity.
- Pulse startup and Pulse endpoint calls are denied until a later milestone authorizes them.
- Read-only posture is reversible.
- Unsupported identity mappings are reported.

## Prohibited Identity Designs

Prohibited designs:

- Creating a Pulse bridge in S7E.
- Creating a bridge identity instance in S7E.
- Starting Pulse or calling Pulse endpoints.
- Probing `localhost:31337`.
- Reusing Claude Code identity for Codex events.
- Reusing `type = "claude"` to mean Codex.
- Claiming Codex is the official upstream engine.
- Writing as the DA without future identity policy.
- Treating product memories as PAI Memory.
- Treating `/goal` state as ISA or Pulse state.
- Copying Claude-shaped files directly into Codex surfaces.
- Creating root `AGENTS.md`, `.codex/`, Codex config, hooks, rules, runtime files, adapter payloads, or Pulse payloads.

## Non-Goals

S7E does not implement a Pulse bridge, create Pulse payloads, create bridge identity instances, start Pulse, call Pulse endpoints, probe `localhost:31337`, create Codex config, create hooks, create rules, create root `AGENTS.md`, create `.codex/`, create runtime files, run a read-only trial, inspect private user-local state, authorize PAI Memory writes, authorize ISA writes, authorize Pulse startup, authorize Pulse endpoint calls, authorize Pulse implementation, authorize existing-local-v5 trial execution, claim Codex is drop-in today, or claim Codex is the official upstream engine.
