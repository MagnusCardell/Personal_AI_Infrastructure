# V5-S7E Execution Plan

## Purpose

Create the design-only V5-S7E Pulse bridge identity, read-only event, observability, audit, and decision-log artifacts for the PAI v5 Codex replacement-adapter effort.

S7E does not implement a Pulse bridge, does not start Pulse, does not call Pulse endpoints, and does not create runtime material.

## Scope

S7E is limited to non-runtime documentation under the approved write set. It designs future Pulse bridge identity, read-only event, observability, and audit posture for later architect review.

S7E preserves the current strategy that Codex is not currently proven drop-in for existing local PAI v5 files and that Codex replacement is plausible only through a designed adapter.

## Approved Write Set

- `docs/adapters/V5_S7E_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_PULSE_BRIDGE_IDENTITY_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_READ_ONLY_EVENT_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_OBSERVABILITY_AND_AUDIT_SPEC.md`
- `docs/adapters/V5_CODEX_PULSE_DECISION_LOG.md`

No other files may be created or modified.

## Protected Paths

Protected repository paths:

- `Releases/`
- `Releases/v5.0.0/`
- `Releases/v5.0.0/.claude/`
- `.claude/`
- `PAI/`
- `CLAUDE.md`
- `AGENTS.md`
- `.codex/`
- `install.sh`
- `PAI_SYSTEM_PROMPT.md`
- `settings.json`
- `hooks/`
- `skills/`
- `subagents/`
- `agents/`
- `commands/`
- `.github/`
- `.agents/`

Private user-local paths that must not be inspected or modified:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`

## Source Protocol

Use only:

1. S0-S7D adapter docs for prior adapter conclusions.
2. Repository-local PAI v5 release files for PAI and Pulse facts.
3. Official OpenAI Codex docs only if S7E adds or refreshes a Codex capability claim.
4. Local `codex --version` or `codex --help` only if already available and non-invasive.

Do not use unofficial Codex capability sources. Do not infer current Codex behavior from memory.

## Source Material

Approved read-only sources:

- S0-S7D adapter docs under `docs/adapters/`.
- Repository-local release material under `Releases/v5.0.0/`.
- Repository-local Claude release material under `Releases/v5.0.0/.claude/`.

Discovery outputs are written only to `/tmp` and are not committed into the repository.

## Completion Contract

> This Completion Contract is the authoritative contract for V5-S7E.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S7E_EXEC_PLAN.md`.
>
> Do not mark S7E complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S7E docs must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S7E designs Pulse bridge identity, read-only event, observability, and audit models only.
> * S7E does not implement a Pulse bridge.
> * S7E does not start Pulse.
> * S7E does not call Pulse endpoints.
> * S7E does not create root `AGENTS.md`.
> * S7E does not create `.codex/`.
> * S7E does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, migration scripts, runtime files, adapter payloads, or Pulse payloads.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
> * Codex config/profile is policy/configuration, not Life OS doctrine.
> * Codex hooks and rules are future native control surfaces, not Claude hook destinations.
> * Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Product memories must not be silently promoted into PAI Memory.
> * Pulse is central v5 infrastructure, but S7E does not prove Pulse parity.
> * Future Pulse interaction requires explicit identity, event, permission, audit, and rollback policy.
> * Future read-only trials must not require uninstalling Claude Code.
> * Future writes require a single-writer policy, provenance, rollback, and validation.
>
> ### Required local discovery commands
>
> Run these commands from repository root:
>
> ```bash
> git status --short
>
> test -d Releases/v5.0.0/.claude/PAI || true
> test -d Releases/v5.0.0/.claude/PAI/PULSE || test -d Releases/v5.0.0/.claude/PAI/Pulse || true
> test -f docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md
> test -f docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md
> test -f docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md
> test -f docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md
> test -f docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md
> test -f docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md
> test -f docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md
>
> find Releases/v5.0.0/.claude/PAI -maxdepth 5 -type f \( -ipath '*pulse*' -o -ipath '*observability*' -o -ipath '*dashboard*' \) | sort > /tmp/v5-s7e-pulse-files.txt
> sed -n '1,240p' /tmp/v5-s7e-pulse-files.txt
>
> rg -n --hidden --glob '!**/.git/**' \
>   'Pulse|PULSE|pulse|31337|localhost:31337|daemon|dashboard|Life Dashboard|event|events|notify|notification|observability|cron|schedule|job|jobs|hook execution|SessionStart|PreToolUse|PostToolUse|Stop|PreCompact|Voice|ElevenLabs|Wiki API|KNOWLEDGE|Memory|ISA|PAI_DIR|launchd|Bun|port|HTTP|endpoint|identity|bridge|adapter|Codex|Claude|AGENTS\.md|CLAUDE\.md|PAI_SYSTEM_PROMPT' \
>   Releases/v5.0.0 docs/adapters \
>   > /tmp/v5-s7e-pulse-search.txt || true
>
> sed -n '1,320p' /tmp/v5-s7e-pulse-search.txt
> ```
>
> Do not write `/tmp/v5-s7e-pulse-files.txt` or `/tmp/v5-s7e-pulse-search.txt` into the repository.
>
> Do not start Pulse.
>
> Do not call `localhost:31337`.
>
> Do not run `curl`, `wget`, browser automation, or HTTP probes against Pulse.
>
> Do not run installers.
>
> Do not invoke Claude Code.
>
> Do not run Codex import/migration tooling.
>
> Do not run Codex hook, rule, execpolicy, or runtime commands.
>
> Do not read user-local private state.
>
> ### Required file: `docs/adapters/V5_S7E_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S7E Execution Plan
> ## Purpose
> ## Scope
> ## Approved Write Set
> ## Protected Paths
> ## Source Protocol
> ## Source Material
> ## Completion Contract
> ## Milestones
> ## Self-Review Rubric
> ## Hard Failure Conditions
> ## Validation Commands
> ## Progress
> ## Iteration Log
> ## Surprises & Discoveries
> ## Decision Log
> ## Outcomes & Retrospective
> ```
>
> The `## Completion Contract` section must contain a verbatim copy of this Completion Contract.
>
> The execution plan must include these milestones:
>
> 1. Baseline status check.
> 2. S0-S7D reread.
> 3. Pulse release evidence reread.
> 4. Hook/lifecycle and event/context seam reread.
> 5. Pulse bridge identity spec drafting.
> 6. Pulse read-only event model drafting.
> 7. Pulse observability and audit spec drafting.
> 8. Pulse decision log drafting.
> 9. Self-review and repair.
> 10. Final handoff and goal-state report.
>
> The self-review rubric must total 100 points:
>
> | Area                                                    | Points |
> | ------------------------------------------------------- | -----: |
> | Scope and protected-path discipline                     |     15 |
> | Evidence discipline                                     |     15 |
> | Pulse centrality and subsystem accuracy                 |     20 |
> | Bridge identity model quality                           |     15 |
> | Read-only event model quality                           |     15 |
> | Observability, audit, Memory, ISA, and safety treatment |     15 |
> | Verification quality                                    |      5 |
>
> Pass threshold:
>
> ```text
> Minimum score: 94/100
> Hard failures: 0
> ```
>
> Record at least one scored iteration in `## Iteration Log`.
>
> ### Required file: `docs/adapters/V5_CODEX_PULSE_BRIDGE_IDENTITY_SPEC.md`
>
> Purpose: define the future identity model for any Codex-to-Pulse bridge so Codex activity is never confused with Claude Code, the official Claude engine, the DA identity, or canonical PAI state.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Pulse Bridge Identity Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Pulse Identity Problem Statement
> ## PAI Pulse Role Model
> ## Engine Identity Model
> ## Bridge Identity Model
> ## DA Identity Boundary
> ## Claude Code Identity Boundary
> ## Codex Identity Boundary
> ## Event Source Identity Rules
> ## Job and Automation Identity Rules
> ## Memory and ISA Identity Boundary
> ## Audit Identity Fields
> ## Candidate Bridge Identity Designs
> ## Required Future Proofs
> ## Prohibited Identity Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * Define Pulse as central v5 infrastructure and not optional background trivia.
> * State that S7E does not create a bridge identity instance.
> * State that S7E does not start Pulse or call Pulse endpoints.
> * Define future identity fields:
>
>   * `bridge_id`
>   * `bridge_kind`
>   * `engine_id`
>   * `adapter_mode`
>   * `source_kind`
>   * `pai_version`
>   * `pai_dir`
>   * `authority_envelope_id`
>   * `event_source`
>   * `event_actor`
>   * `event_origin`
>   * `da_identity_reference`
>   * `session_id`
>   * `trial_id`
>   * `audit_id`
>   * `provenance`
> * Define that Codex must not impersonate Claude Code.
> * Define that Codex must not claim official/full-support engine identity.
> * Define that Codex must not write as the DA unless a future identity policy authorizes it.
> * Define that Pulse events from Codex must be explicitly labeled as Codex-adapter events in future designs.
> * Define that product memory, `/goal`, transcripts, and SDK threads are not Pulse identity sources and are not PAI Memory.
> * Define at least three candidate bridge identity designs:
>
>   * `PI-1`: documentation-only bridge identity contract;
>   * `PI-2`: future manifest-mediated Codex adapter identity;
>   * `PI-3`: future Pulse-registered beta engine identity.
> * For each candidate, include:
>
>   * `Candidate`
>   * `Summary`
>   * `Inputs`
>   * `Outputs`
>   * `Safety`
>   * `Reversibility`
>   * `Drop-in readiness`
>   * `Main risk`
>   * `Required future proofs`
>   * `S7E decision`
> * State that S7E chooses no runtime implementation.
>
> ### Required file: `docs/adapters/V5_CODEX_PULSE_READ_ONLY_EVENT_MODEL_SPEC.md`
>
> Purpose: define future read-only Pulse event interaction classes, boundaries, and denial rules for Codex replacement work without implementing a Pulse bridge.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Pulse Read-Only Event Model Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Pulse Event Problem Statement
> ## Pulse Surface Inventory
> ## Read-Only Event Principles
> ## Event Classification Model
> ## Allowed Read-Only Event Classes
> ## Denied Event Classes
> ## Event Envelope Fields
> ## Hook and Lifecycle Event Boundary
> ## Launcher and Inference Event Boundary
> ## Memory and ISA Event Boundary
> ## Dashboard and Observability Boundary
> ## Scheduling and Job Boundary
> ## Voice and Notification Boundary
> ## Wiki and Knowledge API Boundary
> ## Candidate Read-Only Event Designs
> ## Required Future Proofs
> ## Prohibited Event Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * Define read-only Pulse event model as future design only.
> * State that S7E does not call Pulse endpoints and does not read live Pulse state.
> * Define Pulse surface inventory from release evidence where supported:
>
>   * daemon;
>   * dashboard;
>   * hook execution;
>   * observability;
>   * voice/notification;
>   * scheduling/cron/jobs;
>   * Wiki/Knowledge API;
>   * logs/status;
>   * optional integrations if present in release evidence.
> * Define event classification model:
>
> | Class                                       | Meaning                                                                    |
> | ------------------------------------------- | -------------------------------------------------------------------------- |
> | `PE-0: No interaction`                      | Pulse is acknowledged but not touched.                                     |
> | `PE-1: Static release evidence`             | Pulse files/docs are inspected from repository release only.               |
> | `PE-2: Future read-only status observation` | A future approved adapter may read status without mutation.                |
> | `PE-3: Future advisory event proposal`      | Adapter may propose an event report but not submit it.                     |
> | `PE-4: Future bridge event`                 | Adapter may submit clearly labeled bridge events after approval and tests. |
> | `PE-5: Prohibited in read-only mode`        | Startup, writes, jobs, notifications, scheduling, or state mutation.       |
> | `PE-6: Unknown / evidence gap`              | Evidence is insufficient.                                                  |
> | `PE-7: Drop-in blocker`                     | Pulse behavior blocks drop-in claims until mapped and tested.              |
>
> Include a table with columns:
>
> ```text
> Event ID | Pulse surface | Proposed interaction class | Allowed in S7E? | Allowed in future read-only trial? | Main hazard | Required future proof | S7E decision
> ```
>
> Minimum event IDs:
>
> * `PEV-001`: Pulse daemon status.
> * `PEV-002`: Life Dashboard availability.
> * `PEV-003`: Hook execution event.
> * `PEV-004`: Tool activity/observability event.
> * `PEV-005`: Voice notification event.
> * `PEV-006`: Scheduling/cron/job event.
> * `PEV-007`: Wiki/Knowledge API read.
> * `PEV-008`: Pulse log/status observation.
> * `PEV-009`: Pulse write/event submission.
> * `PEV-010`: Pulse startup/shutdown.
> * `PEV-011`: Pulse bridge identity event.
> * `PEV-012`: Pulse failure/crash report.
> * `PEV-013`: Memory/ISA-related Pulse event.
> * `PEV-014`: Pulse optional integration event.
> * `PEV-015`: Unsupported Pulse surface.
>
> If an event ID is not supported by repository evidence, mark it as `unknown / not confirmed` and explain rather than inventing details.
>
> ### Required file: `docs/adapters/V5_CODEX_PULSE_OBSERVABILITY_AND_AUDIT_SPEC.md`
>
> Purpose: define future observability, audit, provenance, denied-action reporting, and failure handling for any Codex/Pulse interaction.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Pulse Observability and Audit Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Observability Problem Statement
> ## Audit Philosophy
> ## Provenance Requirements
> ## Read-Only Observation Reporting
> ## Denied Action Reporting
> ## Unsupported Surface Reporting
> ## Pulse Startup and Call Reporting
> ## Memory and ISA Reporting
> ## Dashboard and Status Reporting
> ## Failure Classification
> ## Advisory Output Model
> ## Non-Promotion Rule
> ## Required Future Proofs
> ## Prohibited Audit Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * Define audit output as future advisory reporting only, not Pulse state and not PAI Memory.
> * State that S7E creates no audit artifact.
> * State that S7E does not call Pulse endpoints.
> * Require future audit fields:
>
>   * `audit_id`
>   * `trial_id`
>   * `engine_id`
>   * `bridge_id`
>   * `adapter_mode`
>   * `source_kind`
>   * `pulse_interaction_mode`
>   * `pulse_startup_status`
>   * `pulse_endpoint_call_status`
>   * `pulse_write_status`
>   * `pulse_job_status`
>   * `pulse_notification_status`
>   * `pulse_memory_isa_event_status`
>   * `denied_action_report`
>   * `unsupported_surface_report`
>   * `files_inspected`
>   * `files_not_inspected`
>   * `provenance`
>   * `failure_reason`
>   * `rollback_statement`
>   * `non_promotion_statement`
> * Define failure classes:
>
>   * `pulse-startup-attempt`
>   * `pulse-endpoint-call`
>   * `pulse-write-attempt`
>   * `pulse-job-mutation`
>   * `pulse-notification-attempt`
>   * `pulse-identity-confusion`
>   * `memory-isa-mutation`
>   * `private-state-access`
>   * `drop-in-overclaim`
>   * `unsupported-surface-silence`
> * State that any future Pulse observation must report unsupported surfaces rather than silently ignoring them.
> * State that advisory output must not be promoted into PAI Memory, ISA, Pulse, Claude memory, or Codex memory by default.
> * State that S7E cannot mark Pulse parity as proven.
>
> ### Required file: `docs/adapters/V5_CODEX_PULSE_DECISION_LOG.md`
>
> Purpose: record S7E decisions, non-decisions, blocked decisions, and future architect questions for Pulse bridge identity and read-only event modeling.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Pulse Decision Log
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Decisions Made in S7E
> ## Non-Decisions in S7E
> ## Blocked Decisions
> ## Future Architect Questions
> ## Decision Table
> ## Next Milestone Candidates
> ## Non-Goals
> ```
>
> Required content:
>
> Include a decision table with columns:
>
> ```text
> Decision ID | Decision | Rationale | Evidence | Status | Future revisit trigger
> ```
>
> Minimum decisions:
>
> * `S7E-D01`: Codex remains not drop-in today.
> * `S7E-D02`: Pulse is central v5 infrastructure and must not be treated as optional trivia.
> * `S7E-D03`: S7E does not start Pulse or call Pulse endpoints.
> * `S7E-D04`: Future Codex/Pulse interaction requires explicit bridge identity.
> * `S7E-D05`: Codex must not impersonate Claude Code in Pulse events.
> * `S7E-D06`: Codex must not claim official/full-support Pulse identity.
> * `S7E-D07`: Read-only Pulse posture must deny startup, writes, jobs, notifications, and state mutation.
> * `S7E-D08`: Pulse bridge work must preserve authority, launcher, inference, and hook seam decisions.
> * `S7E-D09`: PAI Memory and ISA writes remain blocked.
> * `S7E-D10`: Product memories, `/goal`, transcripts, and SDK threads are not Pulse state and not PAI Memory.
> * `S7E-D11`: Root `AGENTS.md` and `.codex/` remain protected.
> * `S7E-D12`: Future Pulse parity claims require bridge identity, event, audit, failure, rollback, Memory, and ISA proofs.
> * `S7E-D13`: No user-local state is inspected in S7E.
> * `S7E-D14`: S7E creates no bridge, event payload, audit artifact, config, hook, or runtime material.
>
> The `## Next Milestone Candidates` section must list advisory-only options, not approvals:
>
> * `V5-S7B`: Fixture-only coupling validation harness design.
> * `V5-S8E`: Codex rules and approval policy design.
> * `V5-S8F`: Tool/MCP boundary design.
> * `V5-S8G`: Pulse fixture validation design, if S7E is accepted.
> * `V5-S8H`: Memory and ISA single-writer policy design.
> * `V5-S9A`: Integrated read-only fixture-trial architecture, after S7A/S7C/S7D/S7E acceptance.
>
> State that architect approval is required before any future milestone.
>
> ### Protected paths
>
> Do not modify:
>
> * `Releases/`
> * `Releases/v5.0.0/`
> * `Releases/v5.0.0/.claude/`
> * `.claude/`
> * `PAI/`
> * `CLAUDE.md`
> * `AGENTS.md`
> * `.codex/`
> * `install.sh`
> * `PAI_SYSTEM_PROMPT.md`
> * `settings.json`
> * `hooks/`
> * `skills/`
> * `subagents/`
> * `agents/`
> * `commands/`
> * `.github/`
> * `.agents/`
>
> Do not inspect or modify private user-local state:
>
> * `~/.claude/`
> * `~/.claude/PAI/`
> * `~/.claude/projects/`
> * `~/.codex/`
> * `~/.codex/memories/`
>
> ### Hard failure conditions
>
> S7E fails immediately if:
>
> * Any file outside the approved write set is created or modified.
> * Any protected file is modified.
> * Runtime adapter files are created.
> * Root `AGENTS.md` is created or modified.
> * `.codex/` is created or modified.
> * Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, migration scripts, adapter payloads, or Pulse payloads are created.
> * A Pulse bridge is created.
> * Pulse is started.
> * Pulse endpoints are called.
> * `localhost:31337` is probed.
> * `curl`, `wget`, browser automation, or HTTP probes are run against Pulse.
> * User-local private state is inspected or modified.
> * Installers are run.
> * Claude Code is invoked.
> * Codex is invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available.
> * Codex import or migration tooling is run.
> * Codex hook, rule, or execpolicy commands are run.
> * The docs claim Codex is drop-in today.
> * The docs claim Codex is the official upstream engine.
> * The docs authorize PAI Memory writes.
> * The docs authorize ISA writes.
> * The docs authorize Pulse startup.
> * The docs authorize Pulse endpoint calls.
> * The docs authorize Pulse implementation.
> * The docs authorize existing-local-v5 trial execution.
> * The docs imply Claude-shaped files can be copied directly into Codex surfaces.
> * The docs propose installing any Pulse bridge, event model, audit reporter, hook, rule, config, or runtime adapter.
> * The goal advances beyond S7E.
>
> ### Required validation commands
>
> Run:
>
> ```bash
> git status --short
> git diff --name-only | sort
> git diff --check
> ```
>
> Run changed-file check:
>
> ```bash
> python3 - <<'PY'
> import subprocess
>
> expected = [
>     "docs/adapters/V5_CODEX_PULSE_BRIDGE_IDENTITY_SPEC.md",
>     "docs/adapters/V5_CODEX_PULSE_DECISION_LOG.md",
>     "docs/adapters/V5_CODEX_PULSE_OBSERVABILITY_AND_AUDIT_SPEC.md",
>     "docs/adapters/V5_CODEX_PULSE_READ_ONLY_EVENT_MODEL_SPEC.md",
>     "docs/adapters/V5_S7E_EXEC_PLAN.md",
> ]
>
> tracked = subprocess.check_output(
>     ["git", "diff", "--name-only"],
>     text=True,
> ).splitlines()
>
> untracked = subprocess.check_output(
>     ["git", "ls-files", "--others", "--exclude-standard"],
>     text=True,
> ).splitlines()
>
> actual = sorted(set(path for path in tracked + untracked if path.startswith("docs/adapters/")))
>
> if actual != expected:
>     print("unexpected changed docs/adapters files")
>     print("expected:")
>     print("\n".join(expected))
>     print("actual:")
>     print("\n".join(actual))
>     raise SystemExit(1)
>
> print("changed files ok")
> PY
> ```
>
> Run exact H1/H2 heading sequence check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
> import re
>
> required = {
>     "docs/adapters/V5_S7E_EXEC_PLAN.md": [
>         "# V5-S7E Execution Plan",
>         "## Purpose",
>         "## Scope",
>         "## Approved Write Set",
>         "## Protected Paths",
>         "## Source Protocol",
>         "## Source Material",
>         "## Completion Contract",
>         "## Milestones",
>         "## Self-Review Rubric",
>         "## Hard Failure Conditions",
>         "## Validation Commands",
>         "## Progress",
>         "## Iteration Log",
>         "## Surprises & Discoveries",
>         "## Decision Log",
>         "## Outcomes & Retrospective",
>     ],
>     "docs/adapters/V5_CODEX_PULSE_BRIDGE_IDENTITY_SPEC.md": [
>         "# V5 Codex Pulse Bridge Identity Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Pulse Identity Problem Statement",
>         "## PAI Pulse Role Model",
>         "## Engine Identity Model",
>         "## Bridge Identity Model",
>         "## DA Identity Boundary",
>         "## Claude Code Identity Boundary",
>         "## Codex Identity Boundary",
>         "## Event Source Identity Rules",
>         "## Job and Automation Identity Rules",
>         "## Memory and ISA Identity Boundary",
>         "## Audit Identity Fields",
>         "## Candidate Bridge Identity Designs",
>         "## Required Future Proofs",
>         "## Prohibited Identity Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_PULSE_READ_ONLY_EVENT_MODEL_SPEC.md": [
>         "# V5 Codex Pulse Read-Only Event Model Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Pulse Event Problem Statement",
>         "## Pulse Surface Inventory",
>         "## Read-Only Event Principles",
>         "## Event Classification Model",
>         "## Allowed Read-Only Event Classes",
>         "## Denied Event Classes",
>         "## Event Envelope Fields",
>         "## Hook and Lifecycle Event Boundary",
>         "## Launcher and Inference Event Boundary",
>         "## Memory and ISA Event Boundary",
>         "## Dashboard and Observability Boundary",
>         "## Scheduling and Job Boundary",
>         "## Voice and Notification Boundary",
>         "## Wiki and Knowledge API Boundary",
>         "## Candidate Read-Only Event Designs",
>         "## Required Future Proofs",
>         "## Prohibited Event Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_PULSE_OBSERVABILITY_AND_AUDIT_SPEC.md": [
>         "# V5 Codex Pulse Observability and Audit Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Observability Problem Statement",
>         "## Audit Philosophy",
>         "## Provenance Requirements",
>         "## Read-Only Observation Reporting",
>         "## Denied Action Reporting",
>         "## Unsupported Surface Reporting",
>         "## Pulse Startup and Call Reporting",
>         "## Memory and ISA Reporting",
>         "## Dashboard and Status Reporting",
>         "## Failure Classification",
>         "## Advisory Output Model",
>         "## Non-Promotion Rule",
>         "## Required Future Proofs",
>         "## Prohibited Audit Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_PULSE_DECISION_LOG.md": [
>         "# V5 Codex Pulse Decision Log",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Decisions Made in S7E",
>         "## Non-Decisions in S7E",
>         "## Blocked Decisions",
>         "## Future Architect Questions",
>         "## Decision Table",
>         "## Next Milestone Candidates",
>         "## Non-Goals",
>     ],
> }
>
> failures = []
>
> for file, expected in required.items():
>     lines = [line.rstrip() for line in Path(file).read_text(encoding="utf-8").splitlines()]
>     actual = [line for line in lines if re.match(r"^(#|##) [^#]", line)]
>
>     if actual != expected:
>         failures.append(f"{file}: H1/H2 sequence mismatch")
>         failures.append("expected:")
>         failures.extend(expected)
>         failures.append("actual:")
>         failures.extend(actual)
>
>     for i, line in enumerate(lines):
>         if line.startswith("#"):
>             if re.search(r"\s#{1,6}\s+\S", line):
>                 failures.append(f"{file}:{i+1}: multiple headings on one line: {line[:160]}")
>             if i > 0 and lines[i - 1].strip() != "":
>                 failures.append(f"{file}:{i+1}: heading lacks blank line before: {line}")
>             if i + 1 < len(lines) and lines[i + 1].strip() != "":
>                 failures.append(f"{file}:{i+1}: heading lacks blank line after: {line}")
>
> if failures:
>     print("\n".join(failures))
>     raise SystemExit(1)
>
> print("heading structure ok")
> PY
> ```
>
> Run content invariant check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> combined = "\n".join(
>     Path(path).read_text(encoding="utf-8")
>     for path in [
>         "docs/adapters/V5_CODEX_PULSE_BRIDGE_IDENTITY_SPEC.md",
>         "docs/adapters/V5_CODEX_PULSE_READ_ONLY_EVENT_MODEL_SPEC.md",
>         "docs/adapters/V5_CODEX_PULSE_OBSERVABILITY_AND_AUDIT_SPEC.md",
>         "docs/adapters/V5_CODEX_PULSE_DECISION_LOG.md",
>     ]
> )
>
> required_phrases = [
>     "Codex is not currently proven drop-in",
>     "designed adapter",
>     "Claude Code remains",
>     "PAI_SYSTEM_PROMPT.md",
>     "high-authority",
>     "CLAUDE.md",
>     "AGENTS.md",
>     "compact router",
>     "must not be copied directly",
>     "Pulse is central",
>     "Pulse bridge",
>     "bridge identity",
>     "read-only event",
>     "daemon",
>     "dashboard",
>     "31337",
>     "observability",
>     "audit",
>     "denied_action_report",
>     "unsupported_surface_report",
>     "PAI Memory",
>     "ISA",
>     "single-writer",
>     "not PAI Memory",
>     "product memories",
>     "read-only",
>     "reversible",
> ]
>
> missing = [phrase for phrase in required_phrases if phrase not in combined]
>
> if missing:
>     print("missing required phrases:")
>     for phrase in missing:
>         print(f"- {phrase}")
>     raise SystemExit(1)
>
> print("content invariants ok")
> PY
> ```
>
> Run Pulse identity candidate check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_PULSE_BRIDGE_IDENTITY_SPEC.md").read_text(encoding="utf-8")
>
> required_ids = ["PI-1", "PI-2", "PI-3"]
>
> missing = [rid for rid in required_ids if rid not in text]
>
> if missing:
>     print("missing Pulse bridge identity candidates:")
>     for rid in missing:
>         print(f"- {rid}")
>     raise SystemExit(1)
>
> print("Pulse bridge identity candidates ok")
> PY
> ```
>
> Run Pulse event ID check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_PULSE_READ_ONLY_EVENT_MODEL_SPEC.md").read_text(encoding="utf-8")
>
> required_ids = [
>     "PEV-001",
>     "PEV-002",
>     "PEV-003",
>     "PEV-004",
>     "PEV-005",
>     "PEV-006",
>     "PEV-007",
>     "PEV-008",
>     "PEV-009",
>     "PEV-010",
>     "PEV-011",
>     "PEV-012",
>     "PEV-013",
>     "PEV-014",
>     "PEV-015",
> ]
>
> missing = [rid for rid in required_ids if rid not in text]
>
> if missing:
>     print("missing Pulse event IDs:")
>     for rid in missing:
>         print(f"- {rid}")
>     raise SystemExit(1)
>
> print("Pulse event IDs ok")
> PY
> ```
>
> Run audit field check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_PULSE_OBSERVABILITY_AND_AUDIT_SPEC.md").read_text(encoding="utf-8")
>
> required_fields = [
>     "audit_id",
>     "trial_id",
>     "engine_id",
>     "bridge_id",
>     "adapter_mode",
>     "source_kind",
>     "pulse_interaction_mode",
>     "pulse_startup_status",
>     "pulse_endpoint_call_status",
>     "pulse_write_status",
>     "pulse_job_status",
>     "pulse_notification_status",
>     "pulse_memory_isa_event_status",
>     "denied_action_report",
>     "unsupported_surface_report",
>     "files_inspected",
>     "files_not_inspected",
>     "provenance",
>     "failure_reason",
>     "rollback_statement",
>     "non_promotion_statement",
> ]
>
> missing = [field for field in required_fields if field not in text]
>
> if missing:
>     print("missing Pulse audit fields:")
>     for field in missing:
>         print(f"- {field}")
>     raise SystemExit(1)
>
> print("Pulse audit fields ok")
> PY
> ```
>
> Run decision ID check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_PULSE_DECISION_LOG.md").read_text(encoding="utf-8")
>
> required_ids = [
>     "S7E-D01",
>     "S7E-D02",
>     "S7E-D03",
>     "S7E-D04",
>     "S7E-D05",
>     "S7E-D06",
>     "S7E-D07",
>     "S7E-D08",
>     "S7E-D09",
>     "S7E-D10",
>     "S7E-D11",
>     "S7E-D12",
>     "S7E-D13",
>     "S7E-D14",
> ]
>
> missing = [rid for rid in required_ids if rid not in text]
>
> if missing:
>     print("missing decision IDs:")
>     for rid in missing:
>         print(f"- {rid}")
>     raise SystemExit(1)
>
> print("decision IDs ok")
> PY
> ```
>
> Run protected-path check:
>
> ```bash
> git status --short -- Releases/ .claude/ PAI/ CLAUDE.md AGENTS.md .codex/ install.sh settings.json hooks/ skills/ subagents/ agents/ commands/ .github/ .agents/
> ```
>
> Expected protected-path result: no output.
>
> ### Acceptance criteria
>
> S7E is complete only if:
>
> * Exactly the five approved S7E files are created or modified.
> * No protected files are changed.
> * No runtime adapter files are created.
> * No root `AGENTS.md` is created or modified.
> * No `.codex/` files are created or modified.
> * No Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, migration scripts, adapter payloads, or Pulse payloads are created.
> * No Pulse bridge is created.
> * Pulse is not started.
> * Pulse endpoints are not called.
> * `localhost:31337` is not probed.
> * `curl`, `wget`, browser automation, or HTTP probes are not run against Pulse.
> * No user-local state is inspected or modified.
> * Installers are not run.
> * Claude Code is not invoked.
> * Codex is not invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available.
> * Codex import/migration tooling is not run.
> * Codex hook, rule, or execpolicy commands are not run.
> * `V5_S7E_EXEC_PLAN.md` contains the Completion Contract copied into its `## Completion Contract` section.
> * The Pulse bridge identity spec includes candidate designs `PI-1`, `PI-2`, and `PI-3`.
> * The Pulse read-only event model includes all required `PEV-001` through `PEV-015` event IDs.
> * The Pulse observability/audit spec includes all required audit fields.
> * The decision log includes all required `S7E-D01` through `S7E-D14` decisions.
> * The docs do not claim Codex is drop-in today.
> * The docs do not claim Codex is the official upstream engine.
> * The docs do not authorize PAI Memory writes.
> * The docs do not authorize ISA writes.
> * The docs do not authorize Pulse startup.
> * The docs do not authorize Pulse endpoint calls.
> * The docs do not authorize Pulse implementation.
> * The docs do not authorize existing-local-v5 trial execution.
> * The docs do not imply Claude-shaped files can be copied directly into Codex surfaces.
> * The docs do not propose installing any Pulse bridge, event model, audit reporter, hook, rule, config, or runtime adapter.
> * The execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures.
> * Changed-file check passes.
> * Heading sequence check passes.
> * Content invariant check passes.
> * Pulse identity candidate check passes.
> * Pulse event ID check passes.
> * Audit field check passes.
> * Decision ID check passes.
> * Protected-path check has no output.
> * Final handoff reports every required validation command.

## Milestones

1. Baseline status check.
2. S0-S7D reread.
3. Pulse release evidence reread.
4. Hook/lifecycle and event/context seam reread.
5. Pulse bridge identity spec drafting.
6. Pulse read-only event model drafting.
7. Pulse observability and audit spec drafting.
8. Pulse decision log drafting.
9. Self-review and repair.
10. Final handoff and goal-state report.

## Self-Review Rubric

| Area                                                    | Points |
| ------------------------------------------------------- | -----: |
| Scope and protected-path discipline                     |     15 |
| Evidence discipline                                     |     15 |
| Pulse centrality and subsystem accuracy                 |     20 |
| Bridge identity model quality                           |     15 |
| Read-only event model quality                           |     15 |
| Observability, audit, Memory, ISA, and safety treatment |     15 |
| Verification quality                                    |      5 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

- Any file outside the approved write set is created or modified.
- Any protected file is modified.
- Runtime adapter files, Pulse bridge files, Pulse payloads, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, migration scripts, hooks, rules, commands, launchers, installers, wrappers, or adapter payloads are created.
- Pulse is started, Pulse endpoints are called, or `localhost:31337` is probed.
- Private user-local state is inspected or modified.
- The docs claim Codex is drop-in today or the official upstream engine.
- The docs authorize PAI Memory writes, ISA writes, Pulse startup, Pulse endpoint calls, Pulse implementation, or existing-local-v5 trial execution.
- The docs imply Claude-shaped files can be copied directly into Codex surfaces.
- The goal advances beyond S7E.

## Validation Commands

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Changed-file check for the five approved S7E files.
- Exact H1/H2 heading sequence check.
- Content invariant check.
- Pulse identity candidate check.
- Pulse event ID check.
- Audit field check.
- Decision ID check.
- Protected-path check.

## Progress

- Baseline status check: complete. Initial worktree was clean before S7E writes; post-plan discovery showed only the intended new S7E execution plan.
- S0-S7D reread: complete. Prior S6/S7A/S7C/S7D docs were used for authority, launcher, inference, hook, Memory, ISA, Pulse, rollback, and no-copy boundaries.
- Pulse release evidence reread: complete. Release evidence confirms Pulse daemon, dashboard, observability, hook guard, voice/notification, scheduling/job, Wiki/Knowledge, status/log, and optional integration surfaces.
- Hook/lifecycle and event/context seam reread: complete. S7D boundaries were carried forward into Pulse event and audit rules.
- Pulse bridge identity spec drafting: complete.
- Pulse read-only event model drafting: complete.
- Pulse observability and audit spec drafting: complete.
- Pulse decision log drafting: complete.
- Self-review and repair: complete. First validation pass identified missing `PEV-001` through `PEV-015`; the required Pulse event table was added and the event ID check then passed.
- Final handoff and goal-state report: pending final response after validation.

## Iteration Log

| Iteration | Scope and protected-path discipline | Evidence discipline | Pulse centrality and subsystem accuracy | Bridge identity model quality | Read-only event model quality | Observability, audit, Memory, ISA, and safety treatment | Verification quality | Score | Hard failures | Notes |
| --------- | ----------------------------------: | ------------------: | --------------------------------------: | ----------------------------: | ----------------------------: | ------------------------------------------------------: | -------------------: | ----: | ------------: | ----- |
| 1 | 15 | 15 | 19 | 15 | 14 | 15 | 5 | 98 | 0 | First full draft preserved scope and evidence. Initial validation found the required Pulse event IDs missing from the event model; after adding the `PEV-001` through `PEV-015` table, the targeted event ID check passed. |

## Surprises & Discoveries

- The release Pulse tree is larger than the minimal Pulse docs imply. Static evidence includes observability static pages, dashboard code, hook guard modules, voice notification code, Wiki/Knowledge APIs, checks, menu bar files, launchd plist material, and optional integrations.
- `PulseSystem.md` explicitly describes Pulse as the Life Dashboard and the unified daemon on port `31337`.
- `ObservabilitySystem.md` documents both read-like APIs and mutation-capable APIs, so future read-only work needs route-level method classification rather than a broad "observability is safe" assumption.
- `pulse.ts` routes voice, hook, Wiki, assistant, performance, syslog, observability, and static dashboard requests through a single server. This reinforces that Pulse interaction must be identity-labeled and denied by default in S7E.

## Decision Log

- S7E goal started after the previous S7D goal was observed as complete.
- Execution plan created before the four S7E deliverables.
- No official OpenAI Codex documentation refresh was needed because S7E did not add new Codex capability claims; it reused prior official-source Codex facts from S2/S7D.
- S7E uses repository-local release files as static evidence only. It did not start Pulse, call Pulse endpoints, probe `localhost:31337`, inspect private user-local state, or create runtime material.
- Pulse bridge identity is treated as a future prerequisite before any Codex/Pulse event can be considered.
- Read-only event design denies startup, writes, jobs, notifications, scheduling, state mutation, live endpoint calls, PAI Memory writes, ISA writes, and product memory promotion.

## Outcomes & Retrospective

Validation commands run during S7E:

- `git status --short`: passed; only the five intended S7E docs are changed after intent-to-add.
- `git diff --name-only | sort`: passed; listed only the five approved S7E docs.
- `git diff --check`: passed.
- Changed-file check: passed.
- Exact H1/H2 heading sequence check: passed.
- Content invariant check: passed.
- Pulse identity candidate check: passed.
- Pulse event ID check: passed after repair.
- Audit field check: passed.
- Decision ID check: passed.
- Protected-path check: passed with no output.

S7E remains design-only. It does not authorize Pulse implementation, Pulse startup, Pulse endpoint calls, existing-local-v5 trial execution, PAI Memory writes, ISA writes, Codex drop-in claims, official upstream status claims, or direct copying of Claude-shaped files into Codex surfaces.
