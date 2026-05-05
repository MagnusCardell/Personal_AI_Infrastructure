# V5-S7D Execution Plan

## Purpose

Execute V5-S7D Hook and Lifecycle Mapping Design as a documentation-only architecture milestone for future PAI v5 Codex replacement-adapter work.

## Scope

S7D designs future hook, lifecycle, event-context, permission, and safety mappings needed to decouple PAI v5 hook behavior from Claude Code.

S7D does not implement the adapter, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create migration scripts, create runtime files, create adapter payloads, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, run Codex import or migration tooling, invoke Claude Code, invoke Codex as a runtime engine, or run Codex hook, rule, execpolicy, or runtime commands.

## Approved Write Set

Create exactly these files:

- `docs/adapters/V5_S7D_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md`
- `docs/adapters/V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md`
- `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_DECISION_LOG.md`

No other files may be created or modified.

## Protected Paths

Do not modify:

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

Do not inspect or modify private user-local state:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`

## Source Protocol

Use only:

1. S0-S7C adapter docs for prior adapter conclusions.
2. Repository-local PAI v5 release files for PAI facts.
3. Official OpenAI Codex docs for Codex hooks, rules, config, sandbox, and approval facts if S7D adds or refreshes any Codex capability claim.
4. Local `codex --version` or `codex --help` only if already available and non-invasive.

Do not use unofficial Codex capability sources.

Do not infer current Codex behavior from memory.

## Source Material

Approved read material:

- `docs/adapters/V5_S0_DISCOVERY_PLAN.md`
- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- `docs/adapters/V5_S1_EXEC_PLAN.md`
- `docs/adapters/V5_UPSTREAM_RISK_REGISTER.md`
- `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
- `docs/adapters/V5_CODEX_GOAL_RUNBOOK.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`
- `docs/adapters/V5_S2_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_S3_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`
- `docs/adapters/V5_S4_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_MANIFEST_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_FIXTURE_AND_PATH_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_EQUIVALENCE_TEST_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_OUTPUT_SPEC.md`
- `docs/adapters/V5_S5_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_TRIAL_MANIFEST_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_SCHEMA_DRY_RUN_VALIDATION_SPEC.md`
- `docs/adapters/V5_S6_EXEC_PLAN.md`
- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_DECOUPLING_DECISION_LOG.md`
- `docs/adapters/V5_S7A_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_COMPACT_ROUTER_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_ENVELOPE_VALIDATION_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_ROUTER_DECISION_LOG.md`
- `docs/adapters/V5_S7C_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_ENGINE_PROFILE_AND_CAPABILITY_CONTRACT.md`
- `docs/adapters/V5_CODEX_LAUNCHER_INFERENCE_DECISION_LOG.md`
- `Releases/v5.0.0/`
- `Releases/v5.0.0/.claude/`

## Completion Contract

> This Completion Contract is the authoritative contract for V5-S7D.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S7D_EXEC_PLAN.md`.
>
> Do not mark S7D complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S7D docs must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S7D designs hook, lifecycle, event-context, permission, and safety mappings only.
> * S7D does not implement hook or lifecycle mapping.
> * S7D does not create root `AGENTS.md`.
> * S7D does not create `.codex/`.
> * S7D does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, migration scripts, runtime files, or adapter payloads.
> * Claude-shaped hook files must not be copied directly into Codex hook surfaces.
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
> * Pulse remains central v5 infrastructure, but S7D does not design or implement a Pulse bridge.
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
> test -d Releases/v5.0.0/.claude/hooks
> test -f Releases/v5.0.0/.claude/settings.json
> test -f docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md
> test -f docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md
> test -f docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md
> test -f docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md
> test -f docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md
>
> find Releases/v5.0.0/.claude/hooks -maxdepth 3 -type f | sort > /tmp/v5-s7d-hook-files.txt
> sed -n '1,200p' /tmp/v5-s7d-hook-files.txt
>
> rg -n --hidden --glob '!**/.git/**' \
>   'hook|hooks|Hook|Hooks|LoadContext|PromptProcessing|PreToolUse|PostToolUse|PermissionRequest|UserPromptSubmit|SessionStart|Stop|Notification|Subagent|tool|Tool|payload|stdin|stdout|stderr|context|lifecycle|permission|approval|deny|allow|settings\.json|matcher|command|event|PAI_DIR|PAI_SYSTEM_PROMPT|CLAUDE\.md|AGENTS\.md|Memory|WORK|LEARNING|KNOWLEDGE|ISA|Pulse|PULSE|31337|MCP|mcp|sandbox|rules|config' \
>   Releases/v5.0.0 docs/adapters \
>   > /tmp/v5-s7d-hook-lifecycle-search.txt || true
>
> sed -n '1,280p' /tmp/v5-s7d-hook-lifecycle-search.txt
> ```
>
> Do not write `/tmp/v5-s7d-hook-files.txt` or `/tmp/v5-s7d-hook-lifecycle-search.txt` into the repository.
>
> Do not run installers.
>
> Do not start Pulse.
>
> Do not invoke Claude Code.
>
> Do not run Codex import/migration tooling.
>
> Do not run Codex hook, rule, execpolicy, or runtime commands.
>
> Do not read user-local private state.
>
> ### Required file: `docs/adapters/V5_S7D_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S7D Execution Plan
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
> 2. S0-S7C reread.
> 3. Hook/lifecycle release evidence reread.
> 4. Official Codex hooks/rules/config/sandbox evidence refresh if new Codex claims are needed.
> 5. Hook lifecycle mapping spec drafting.
> 6. Event/context envelope spec drafting.
> 7. Hook permission and safety spec drafting.
> 8. Hook lifecycle decision log drafting.
> 9. Self-review and repair.
> 10. Final handoff and goal-state report.
>
> The self-review rubric must total 100 points:
>
> | Area                                                         | Points |
> | ------------------------------------------------------------ | -----: |
> | Scope and protected-path discipline                          |     15 |
> | Evidence discipline                                          |     15 |
> | Claude hook/lifecycle inventory quality                      |     15 |
> | Codex-native hook/rule mapping quality                       |     20 |
> | Event/context envelope quality                               |     15 |
> | Permission, sandbox, Memory, ISA, Pulse, and rollback safety |     15 |
> | Verification quality                                         |      5 |
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
> ### Required file: `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md`
>
> Purpose: define the future mapping between PAI v5 Claude-shaped hooks/lifecycle behavior and Codex-native hook/rule/control surfaces without copying Claude hook files or implementing Codex hooks.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Hook Lifecycle Mapping Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Hook Problem Statement
> ## Existing Claude Hook Inventory
> ## Claude Lifecycle Assumptions
> ## Codex Native Hook and Rule Surfaces
> ## Non-Equivalent Lifecycle Semantics
> ## Mapping Classification Model
> ## Hook Mapping Table
> ## Load Context Mapping
> ## Prompt Processing Mapping
> ## Tool Permission and Observation Mapping
> ## Session and Completion Mapping
> ## Subagent and Agent Boundary Mapping
> ## Memory and ISA Boundary Mapping
> ## Pulse Boundary Mapping
> ## Required Future Proofs
> ## Prohibited Hook Mappings
> ## Non-Goals
> ```
>
> Required content:
>
> * Define hook lifecycle mapping as a future adapter design problem, not an implementation.
> * Inventory observed release hook files and settings registrations where supported by evidence.
> * State that Claude hook files must not be copied into Codex hook files.
> * State that Codex hooks/rules/config are native Codex surfaces, not Claude hook destinations.
> * State that any future Codex hook/rule mapping requires its own spec and tests.
> * Define the mapping classification model:
>
> | Class                              | Meaning                                                                                               |
> | ---------------------------------- | ----------------------------------------------------------------------------------------------------- |
> | `M0: Not applicable`               | No hook/lifecycle mapping is needed.                                                                  |
> | `M1: Documentation-only reference` | Source informs future design but does not map to a live Codex surface.                                |
> | `M2: Authority/context candidate`  | Behavior may be represented through authority envelope or compact router design.                      |
> | `M3: Codex hook candidate`         | Behavior may map to future Codex-native hook configuration after spec and tests.                      |
> | `M4: Codex rule/policy candidate`  | Behavior may map to future Codex rules, sandbox, approval, or permission policy after spec and tests. |
> | `M5: Bridge required`              | Behavior requires an adapter bridge or dispatcher, not only native hooks/rules.                       |
> | `M6: Prohibited in read-only mode` | Behavior would write state, invoke runtime side effects, or access private state.                     |
> | `M7: Unknown / evidence gap`       | Evidence is insufficient and must be reviewed later.                                                  |
> | `M8: Drop-in blocker`              | Behavior blocks drop-in claims until mapped, tested, and validated.                                   |
>
> Include a mapping table with columns:
>
> ```text
> Mapping ID | Evidence source | Claude hook/lifecycle behavior | Current Codex-native candidate | Mapping class | Main hazard | Required future proof | S7D decision
> ```
>
> Minimum mapping IDs:
>
> * `HM-001`: `.claude/settings.json` hook registration and permission semantics.
> * `HM-002`: `LoadContext.hook.ts` or equivalent context-loading behavior.
> * `HM-003`: `PromptProcessing.hook.ts` or equivalent prompt-processing behavior.
> * `HM-004`: pre-tool or permission lifecycle behavior.
> * `HM-005`: post-tool observation or review behavior.
> * `HM-006`: user-prompt submission behavior.
> * `HM-007`: session-start or resume behavior.
> * `HM-008`: stop/completion behavior.
> * `HM-009`: hook stdin/stdout/payload assumptions.
> * `HM-010`: hook command execution and timeout assumptions.
> * `HM-011`: PAI Memory and ISA boundary behavior.
> * `HM-012`: Pulse event/job boundary behavior.
> * `HM-013`: agent/subagent lifecycle boundary behavior.
> * `HM-014`: Codex rules as possible policy/control surface.
> * `HM-015`: Codex hooks as possible event/control surface.
>
> If a mapping ID is not supported by repository evidence, mark it as `unknown / not confirmed` and explain rather than inventing details.
>
> ### Required file: `docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md`
>
> Purpose: define the future event/context envelope needed to translate hook-relevant lifecycle signals into safe, auditable Codex-native behavior.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Event Context Envelope Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Envelope Problem Statement
> ## Event Source Model
> ## Event Type Model
> ## Context Input Model
> ## Authority Context Boundary
> ## Tool Event Boundary
> ## Filesystem Event Boundary
> ## Memory and ISA Event Boundary
> ## Pulse Event Boundary
> ## Output and Audit Model
> ## Unsupported Event Reporting
> ## Candidate Envelope Designs
> ## Required Future Proofs
> ## Prohibited Envelope Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * Define event/context envelope as a future design artifact, not an implementation.
> * State that S7D creates no event envelope instance.
> * Define future event source classes:
>
>   * `codex-session`
>   * `codex-user-prompt`
>   * `codex-tool-request`
>   * `codex-tool-result`
>   * `codex-permission-request`
>   * `codex-stop`
>   * `pai-runtime`
>   * `pulse-event`
>   * `unknown`
> * Define future event type classes:
>
>   * `context-load`
>   * `prompt-process`
>   * `permission-check`
>   * `pre-tool-observe`
>   * `post-tool-observe`
>   * `audit-only`
>   * `unsupported`
>   * `prohibited`
> * Define required future envelope fields:
>
>   * `event_id`
>   * `engine_id`
>   * `adapter_mode`
>   * `event_source`
>   * `event_type`
>   * `lifecycle_phase`
>   * `pai_dir`
>   * `authority_envelope_id`
>   * `context_sources`
>   * `tool_context`
>   * `filesystem_policy`
>   * `sandbox_policy`
>   * `permission_policy`
>   * `memory_policy`
>   * `isa_policy`
>   * `pulse_policy`
>   * `output_policy`
>   * `audit_policy`
>   * `unsupported_surfaces`
>   * `denied_actions`
>   * `provenance`
> * Define that PAI Memory and ISA writes are prohibited in read-only mode.
> * Define that Pulse startup, Pulse writes, and Pulse parity claims are prohibited in S7D.
> * Define that product memory must not be injected as authority or promoted into PAI Memory.
> * Define at least three candidate envelope designs:
>
>   * `EC-1`: documentation-only event/context envelope contract.
>   * `EC-2`: future manifest-mediated event/context envelope.
>   * `EC-3`: future Codex hook dispatcher envelope.
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
>   * `S7D decision`
> * State that S7D chooses no runtime implementation.
>
> ### Required file: `docs/adapters/V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md`
>
> Purpose: define future safety, sandbox, permission, denial, and audit requirements for any hook/lifecycle mapping.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Hook Permission and Safety Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Safety Problem Statement
> ## Permission Boundary Model
> ## Sandbox Boundary Model
> ## Read-Only Enforcement Model
> ## Denied Action Model
> ## Tool and MCP Safety Model
> ## Filesystem Safety Model
> ## Memory and ISA Safety Model
> ## Pulse Safety Model
> ## Product Memory Safety Model
> ## Audit and Provenance Requirements
> ## Failure and Stop Conditions
> ## Required Future Proofs
> ## Prohibited Safety Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * Define hook safety as future policy and validation design, not implementation.
> * State that S7D creates no hook files, rules files, config files, or permission policy files.
> * State that Codex hooks/rules must not be treated as complete replacements for Claude hooks until tested.
> * State that Codex hooks/rules must not bypass Codex sandbox, approvals, or PAI protected-path policy.
> * Define denied actions:
>
>   * modifying release files;
>   * modifying root `AGENTS.md`;
>   * creating or modifying `.codex/`;
>   * reading private user-local memory;
>   * writing PAI Memory;
>   * writing ISA;
>   * starting Pulse;
>   * writing Pulse state;
>   * running installers;
>   * running migration/import tooling;
>   * invoking Claude Code;
>   * invoking Codex as runtime engine during design milestones;
>   * silently allowing unsupported Claude hook behavior.
> * Define future safety outputs:
>
>   * `allowed_action_report`
>   * `denied_action_report`
>   * `unsupported_surface_report`
>   * `sandbox_report`
>   * `permission_report`
>   * `memory_write_status`
>   * `isa_write_status`
>   * `pulse_action_status`
>   * `provenance`
>   * `failure_reason`
> * Define that any future write-capable hook behavior requires single-writer policy.
> * Define that any future hook-generated advisory output must not be promoted into PAI Memory, ISA, Pulse, Claude memory, or Codex memory by default.
> * State that S7D cannot mark hook/lifecycle parity as proven.
>
> ### Required file: `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_DECISION_LOG.md`
>
> Purpose: record S7D decisions, non-decisions, blocked decisions, and future architect questions for hook/lifecycle mapping.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Hook Lifecycle Decision Log
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Decisions Made in S7D
> ## Non-Decisions in S7D
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
> * `S7D-D01`: Codex remains not drop-in today.
> * `S7D-D02`: Claude hook files must not be copied into Codex hook surfaces.
> * `S7D-D03`: Hook/lifecycle replacement requires explicit mapping and validation.
> * `S7D-D04`: Codex hooks and rules are native surfaces, not Claude hook destinations.
> * `S7D-D05`: Context-loading behavior must respect authority seam decisions.
> * `S7D-D06`: Prompt-processing behavior must not silently mutate PAI doctrine.
> * `S7D-D07`: Tool/permission behavior requires explicit sandbox and approval policy.
> * `S7D-D08`: PAI Memory and ISA writes remain blocked.
> * `S7D-D09`: Pulse bridge remains out of S7D scope.
> * `S7D-D10`: Root `AGENTS.md` and `.codex/` remain protected.
> * `S7D-D11`: S7D creates no hook, rule, config, or runtime material.
> * `S7D-D12`: Future hook validation must precede any hook/lifecycle parity claim.
> * `S7D-D13`: No user-local state is inspected in S7D.
> * `S7D-D14`: No Claude Code or Codex runtime invocation occurs in S7D.
>
> The `## Next Milestone Candidates` section must list advisory-only options, not approvals:
>
> * `V5-S7B`: Fixture-only coupling validation harness design.
> * `V5-S7E`: Pulse bridge identity and read-only event model.
> * `V5-S8D`: Hook/lifecycle fixture validation design, if S7D is accepted.
> * `V5-S8E`: Codex rules and approval policy design, if S7D is accepted.
> * `V5-S8F`: Tool/MCP boundary design, if S7D is accepted.
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
> S7D fails immediately if:
>
> * Any file outside the approved write set is created or modified.
> * Any protected file is modified.
> * Runtime adapter files are created.
> * Root `AGENTS.md` is created or modified.
> * `.codex/` is created or modified.
> * Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, migration scripts, or adapter payloads are created.
> * User-local private state is inspected or modified.
> * Pulse is started.
> * Installers are run.
> * Claude Code is invoked.
> * Codex is invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available.
> * Codex import or migration tooling is run.
> * Codex hook, rule, or execpolicy commands are run.
> * The docs claim Codex is drop-in today.
> * The docs claim Codex is the official upstream engine.
> * The docs authorize PAI Memory writes.
> * The docs authorize ISA writes.
> * The docs authorize Pulse implementation.
> * The docs authorize existing-local-v5 trial execution.
> * The docs imply Claude-shaped files can be copied directly into Codex surfaces.
> * The docs propose installing any hook, rule, config, event envelope, or lifecycle adapter.
> * The goal advances beyond S7D.
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
>     "docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md",
>     "docs/adapters/V5_CODEX_HOOK_LIFECYCLE_DECISION_LOG.md",
>     "docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md",
>     "docs/adapters/V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md",
>     "docs/adapters/V5_S7D_EXEC_PLAN.md",
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
>     "docs/adapters/V5_S7D_EXEC_PLAN.md": [
>         "# V5-S7D Execution Plan",
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
>     "docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md": [
>         "# V5 Codex Hook Lifecycle Mapping Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Hook Problem Statement",
>         "## Existing Claude Hook Inventory",
>         "## Claude Lifecycle Assumptions",
>         "## Codex Native Hook and Rule Surfaces",
>         "## Non-Equivalent Lifecycle Semantics",
>         "## Mapping Classification Model",
>         "## Hook Mapping Table",
>         "## Load Context Mapping",
>         "## Prompt Processing Mapping",
>         "## Tool Permission and Observation Mapping",
>         "## Session and Completion Mapping",
>         "## Subagent and Agent Boundary Mapping",
>         "## Memory and ISA Boundary Mapping",
>         "## Pulse Boundary Mapping",
>         "## Required Future Proofs",
>         "## Prohibited Hook Mappings",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md": [
>         "# V5 Codex Event Context Envelope Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Envelope Problem Statement",
>         "## Event Source Model",
>         "## Event Type Model",
>         "## Context Input Model",
>         "## Authority Context Boundary",
>         "## Tool Event Boundary",
>         "## Filesystem Event Boundary",
>         "## Memory and ISA Event Boundary",
>         "## Pulse Event Boundary",
>         "## Output and Audit Model",
>         "## Unsupported Event Reporting",
>         "## Candidate Envelope Designs",
>         "## Required Future Proofs",
>         "## Prohibited Envelope Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md": [
>         "# V5 Codex Hook Permission and Safety Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Safety Problem Statement",
>         "## Permission Boundary Model",
>         "## Sandbox Boundary Model",
>         "## Read-Only Enforcement Model",
>         "## Denied Action Model",
>         "## Tool and MCP Safety Model",
>         "## Filesystem Safety Model",
>         "## Memory and ISA Safety Model",
>         "## Pulse Safety Model",
>         "## Product Memory Safety Model",
>         "## Audit and Provenance Requirements",
>         "## Failure and Stop Conditions",
>         "## Required Future Proofs",
>         "## Prohibited Safety Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_HOOK_LIFECYCLE_DECISION_LOG.md": [
>         "# V5 Codex Hook Lifecycle Decision Log",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Decisions Made in S7D",
>         "## Non-Decisions in S7D",
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
>         "docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md",
>         "docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md",
>         "docs/adapters/V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md",
>         "docs/adapters/V5_CODEX_HOOK_LIFECYCLE_DECISION_LOG.md",
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
>     "Claude hook files must not be copied",
>     "hook lifecycle",
>     "Codex hooks",
>     "Codex rules",
>     "event/context envelope",
>     "permission",
>     "sandbox",
>     "PAI Memory",
>     "ISA",
>     "Pulse",
>     "single-writer",
>     "not PAI Memory",
>     "product memories",
>     "read-only",
>     "reversible",
>     "denied_action_report",
>     "unsupported_surface_report",
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
> Run hook mapping ID check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md").read_text(encoding="utf-8")
>
> required_ids = [
>     "HM-001",
>     "HM-002",
>     "HM-003",
>     "HM-004",
>     "HM-005",
>     "HM-006",
>     "HM-007",
>     "HM-008",
>     "HM-009",
>     "HM-010",
>     "HM-011",
>     "HM-012",
>     "HM-013",
>     "HM-014",
>     "HM-015",
> ]
>
> missing = [rid for rid in required_ids if rid not in text]
>
> if missing:
>     print("missing hook mapping IDs:")
>     for rid in missing:
>         print(f"- {rid}")
>     raise SystemExit(1)
>
> print("hook mapping IDs ok")
> PY
> ```
>
> Run event envelope candidate check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md").read_text(encoding="utf-8")
>
> required_ids = ["EC-1", "EC-2", "EC-3"]
>
> missing = [rid for rid in required_ids if rid not in text]
>
> if missing:
>     print("missing event envelope candidates:")
>     for rid in missing:
>         print(f"- {rid}")
>     raise SystemExit(1)
>
> print("event envelope candidates ok")
> PY
> ```
>
> Run safety output field check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md").read_text(encoding="utf-8")
>
> required_fields = [
>     "allowed_action_report",
>     "denied_action_report",
>     "unsupported_surface_report",
>     "sandbox_report",
>     "permission_report",
>     "memory_write_status",
>     "isa_write_status",
>     "pulse_action_status",
>     "provenance",
>     "failure_reason",
> ]
>
> missing = [field for field in required_fields if field not in text]
>
> if missing:
>     print("missing safety output fields:")
>     for field in missing:
>         print(f"- {field}")
>     raise SystemExit(1)
>
> print("safety output fields ok")
> PY
> ```
>
> Run decision ID check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_HOOK_LIFECYCLE_DECISION_LOG.md").read_text(encoding="utf-8")
>
> required_ids = [
>     "S7D-D01",
>     "S7D-D02",
>     "S7D-D03",
>     "S7D-D04",
>     "S7D-D05",
>     "S7D-D06",
>     "S7D-D07",
>     "S7D-D08",
>     "S7D-D09",
>     "S7D-D10",
>     "S7D-D11",
>     "S7D-D12",
>     "S7D-D13",
>     "S7D-D14",
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
> S7D is complete only if:
>
> * Exactly the five approved S7D files are created or modified.
> * No protected files are changed.
> * No runtime adapter files are created.
> * No root `AGENTS.md` is created or modified.
> * No `.codex/` files are created or modified.
> * No Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, migration scripts, or adapter payloads are created.
> * No user-local state is inspected or modified.
> * Pulse is not started.
> * Installers are not run.
> * Claude Code is not invoked.
> * Codex is not invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available.
> * Codex import/migration tooling is not run.
> * Codex hook, rule, or execpolicy commands are not run.
> * `V5_S7D_EXEC_PLAN.md` contains the Completion Contract copied into its `## Completion Contract` section.
> * The hook lifecycle mapping spec includes all required `HM-001` through `HM-015` mapping IDs.
> * The event/context envelope spec includes candidate designs `EC-1`, `EC-2`, and `EC-3`.
> * The hook permission and safety spec includes all required safety output fields.
> * The decision log includes all required `S7D-D01` through `S7D-D14` decisions.
> * The docs do not claim Codex is drop-in today.
> * The docs do not claim Codex is the official upstream engine.
> * The docs do not authorize PAI Memory writes.
> * The docs do not authorize ISA writes.
> * The docs do not authorize Pulse implementation.
> * The docs do not authorize existing-local-v5 trial execution.
> * The docs do not imply Claude-shaped files can be copied directly into Codex surfaces.
> * The docs do not propose installing any hook, rule, config, event envelope, or lifecycle adapter.
> * The execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures.
> * Changed-file check passes.
> * Heading sequence check passes.
> * Content invariant check passes.
> * Hook mapping ID check passes.
> * Event envelope candidate check passes.
> * Safety output field check passes.
> * Decision ID check passes.
> * Protected-path check has no output.
> * Final handoff reports every required validation command.

## Milestones

1. Baseline status check.
2. S0-S7C reread.
3. Hook/lifecycle release evidence reread.
4. Official Codex hooks/rules/config/sandbox evidence refresh if new Codex claims are needed.
5. Hook lifecycle mapping spec drafting.
6. Event/context envelope spec drafting.
7. Hook permission and safety spec drafting.
8. Hook lifecycle decision log drafting.
9. Self-review and repair.
10. Final handoff and goal-state report.

## Self-Review Rubric

| Area | Points |
| --- | ---: |
| Scope and protected-path discipline | 15 |
| Evidence discipline | 15 |
| Claude hook/lifecycle inventory quality | 15 |
| Codex-native hook/rule mapping quality | 20 |
| Event/context envelope quality | 15 |
| Permission, sandbox, Memory, ISA, Pulse, and rollback safety | 15 |
| Verification quality | 5 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

S7D fails immediately if:

- Any file outside the approved write set is created or modified.
- Any protected file is modified.
- Runtime adapter files are created.
- Root `AGENTS.md` is created or modified.
- `.codex/` is created or modified.
- Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, migration scripts, or adapter payloads are created.
- User-local private state is inspected or modified.
- Pulse is started.
- Installers are run.
- Claude Code is invoked.
- Codex is invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available.
- Codex import or migration tooling is run.
- Codex hook, rule, or execpolicy commands are run.
- The docs claim Codex is drop-in today.
- The docs claim Codex is the official upstream engine.
- The docs authorize PAI Memory writes.
- The docs authorize ISA writes.
- The docs authorize Pulse implementation.
- The docs authorize existing-local-v5 trial execution.
- The docs imply Claude-shaped files can be copied directly into Codex surfaces.
- The docs propose installing any hook, rule, config, event envelope, or lifecycle adapter.
- The goal advances beyond S7D.

## Validation Commands

Required validation commands:

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Changed-file Python check.
- Exact H1/H2 heading sequence check.
- Content invariant check.
- Hook mapping ID check.
- Event envelope candidate check.
- Safety output field check.
- Decision ID check.
- Protected-path check.

## Progress

- Started the bounded V5-S7D goal.
- Confirmed the baseline worktree was clean before S7D edits.
- Created this execution plan first.
- Copied the Completion Contract into this execution plan before drafting other S7D deliverables.
- Confirmed required source paths exist:
  - `Releases/v5.0.0/.claude/hooks`
  - `Releases/v5.0.0/.claude/settings.json`
  - `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
  - `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
  - `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`
  - `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
  - `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- Ran the required hook file inventory and wrote results only to `/tmp/v5-s7d-hook-files.txt`.
- Ran the required hook/lifecycle search and wrote results only to `/tmp/v5-s7d-hook-lifecycle-search.txt`.
- Reviewed approved S0-S7C adapter docs and repository-local v5 release evidence.
- Reviewed release hook registration, hook README, hook IO, and representative hooks for context loading, prompt processing, security, permission, ISA sync, agent tracking, tool activity, learning, and voice completion.
- Created `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md`.
- Created `docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md`.
- Created `docs/adapters/V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md`.
- Created `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_DECISION_LOG.md`.
- Did not refresh official Codex docs because S7D did not add new Codex capability claims beyond prior S2 official-source evidence.
- Did not invoke Claude Code.
- Did not invoke Codex as a runtime engine.
- Did not run Codex hook, rule, execpolicy, or runtime commands.
- Did not inspect private user-local state.
- Did not run installers, start Pulse, run Codex import or migration tooling, run a read-only trial, create runtime files, create adapter payloads, or modify release files.
- Completed preliminary validation before this final execution-plan update:
  - `git status --short`: showed only the five approved S7D docs as intent-to-add.
  - `git diff --name-only | sort`: listed exactly the five approved S7D docs.
  - `git diff --check`: passed.
  - Changed-file Python check: passed.
  - Exact H1/H2 heading sequence check: passed.
  - Content invariant check: passed.
  - Hook mapping ID check: passed.
  - Event envelope candidate check: passed.
  - Safety output field check: passed.
  - Decision ID check: passed.
  - Protected-path check: passed with no output.

## Iteration Log

| Iteration | Scope discipline | Evidence discipline | Hook inventory | Native mapping | Event envelope | Safety | Verification | Total | Hard failures | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| S7D-I0 initial plan | 15 | 10 | 0 | 0 | 0 | 8 | 1 | 34/100 | 0 | Execution plan created; deliverables not yet drafted. |
| S7D-I1 final self-review | 15 | 15 | 14 | 19 | 15 | 15 | 5 | 98/100 | 0 | Pass. S7D remains design-only, maps observed Claude hook/lifecycle evidence to future native Codex candidates, and blocks runtime claims. |

## Surprises & Discoveries

- The release hook system is broader than a simple set of event scripts. `settings.json` combines permissions, command hooks, HTTP hook routes, allowed HTTP hook URLs, status line configuration, plugin configuration, timeouts, and async behavior.
- The hook README records lifecycle events that are not all visibly registered in the inspected `settings.json` excerpt. S7D treats those as evidence-backed design inputs where the README documents them, and as unknown/not confirmed where direct registration was not confirmed.
- Agent/subagent tracking is explicitly handled through `PreToolUse:Agent` and `PostToolUse:Agent` because the README says Claude built-in subagent payloads lacked enough metadata. This is a future Codex subagent mapping risk, not hook parity.
- Several release hooks write or push canonical or operational state, including ISA/work sync, observability events, learning files, relationship memory, KV sync, and voice/Pulse-related behavior. S7D keeps all such behavior blocked in read-only posture.
- Pulse appears in hook behavior through local HTTP hook routes and voice/observability relationships. S7D records the boundary but does not design or implement a Pulse bridge.

## Decision Log

- S7D will use S0-S7C adapter docs and repository-local v5 release evidence.
- S7D will use official OpenAI Codex docs only if a new or refreshed Codex capability claim is needed.
- S7D will not invoke Claude Code.
- S7D will not invoke Codex as a runtime engine.
- S7D will not run Codex hook, rule, execpolicy, or runtime commands.
- S7D will not inspect private user-local state.
- S7D will not create hook, rule, config, event envelope, lifecycle adapter, adapter payload, or runtime material.
- S7D keeps Codex as not currently proven drop-in for existing local PAI v5 files.
- S7D defines hook lifecycle mapping, event/context envelope, and hook permission/safety as future contracts, not files to install or execute.
- S7D keeps `PAI_SYSTEM_PROMPT.md` as high-authority doctrine and `CLAUDE.md` as an official Claude-facing surface, not a Codex destination file.
- S7D keeps future Codex `AGENTS.md`, if later authorized, as a compact router.
- S7D treats Codex hooks and Codex rules as native Codex surfaces, not Claude hook destinations.
- S7D keeps PAI Memory and ISA writes blocked and treats Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state as not PAI Memory.
- S7D keeps Pulse central to v5 infrastructure while blocking Pulse startup, Pulse writes, Pulse endpoint calls, and Pulse bridge implementation in this milestone.

## Outcomes & Retrospective

S7D created exactly the five approved design documents and stayed inside the approved write set.

Deliverables:

- `docs/adapters/V5_S7D_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_EVENT_CONTEXT_ENVELOPE_SPEC.md`
- `docs/adapters/V5_CODEX_HOOK_PERMISSION_AND_SAFETY_SPEC.md`
- `docs/adapters/V5_CODEX_HOOK_LIFECYCLE_DECISION_LOG.md`

Final validation results:

- `git status --short`: passed; output lists only the five approved S7D docs.
- `git diff --name-only | sort`: passed; output lists exactly the five approved S7D docs.
- `git diff --check`: passed with no output.
- Changed-file Python check: passed.
- Exact H1/H2 heading sequence check: passed.
- Content invariant check: passed.
- Hook mapping ID check: passed.
- Event envelope candidate check: passed.
- Safety output field check: passed.
- Decision ID check: passed.
- Protected-path check: passed with no output.

Completion audit result:

- Prompt-to-artifact audit passed after confirming the five approved docs, required headings, required `HM-001` through `HM-015` mapping IDs, required `EC-1` through `EC-3` event envelope candidates, required safety output fields, required `S7D-D01` through `S7D-D14` decisions, non-implementation posture, protected-path cleanliness, and no authorization of runtime behavior.

Goal-state note:

- `/goal clear` is unavailable in this tool surface unless a later tool appears.
