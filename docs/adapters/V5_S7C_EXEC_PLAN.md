# V5-S7C Execution Plan

## Purpose

Execute V5-S7C Launcher and Inference Seam Design as a documentation-only architecture milestone for future PAI v5 Codex replacement-adapter work.

## Scope

S7C designs the launcher and inference seams needed to decouple PAI v5 runtime invocation from Claude Code.

S7C does not implement the adapter, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create migration scripts, create runtime files, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, run Codex import or migration tooling, invoke Claude Code, or invoke Codex as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available.

## Approved Write Set

Create exactly these files:

- `docs/adapters/V5_S7C_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_ENGINE_PROFILE_AND_CAPABILITY_CONTRACT.md`
- `docs/adapters/V5_CODEX_LAUNCHER_INFERENCE_DECISION_LOG.md`

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

1. S0-S7A adapter docs for prior adapter conclusions.
2. Repository-local PAI v5 release files for PAI facts.
3. Official OpenAI Codex docs for Codex CLI, noninteractive, config, and sandbox facts if S7C adds or refreshes any Codex capability claim.
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
- `Releases/v5.0.0/`
- `Releases/v5.0.0/.claude/`

## Completion Contract

> This Completion Contract is the authoritative contract for V5-S7C.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S7C_EXEC_PLAN.md`.
>
> Do not mark S7C complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S7C docs must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S7C designs launcher and inference seams only.
> * S7C does not implement launcher or inference replacement.
> * S7C does not create root `AGENTS.md`.
> * S7C does not create `.codex/`.
> * S7C does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, migration scripts, or runtime files.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Future Codex `AGENTS.md`, if later authorized, must be a compact router.
> * The compact router must not clone `CLAUDE.md`.
> * The compact router must not clone `PAI_SYSTEM_PROMPT.md`.
> * Codex config/profile is policy/configuration, not Life OS doctrine.
> * Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Product memories must not be silently promoted into PAI Memory.
> * Pulse remains central v5 infrastructure, but S7C does not design or implement a Pulse bridge.
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
> test -f Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts
> test -f Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts
> test -f docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md
> test -f docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md
> test -f docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md
>
> rg -n --hidden --glob '!**/.git/**' \
>   'pai\.ts|Inference\.ts|claude|Claude|CLAUDE|codex|Codex|spawn|exec|command|process|argv|stdin|stdout|stderr|exit code|model|inference|prompt|system prompt|append-system-prompt|PAI_SYSTEM_PROMPT|PAI_DIR|Pulse|PULSE|31337|ISA|Memory|WORK|LEARNING|KNOWLEDGE|Bun|node|settings|permission|sandbox|profile|MCP|mcp' \
>   Releases/v5.0.0 docs/adapters \
>   > /tmp/v5-s7c-launcher-inference-search.txt || true
>
> sed -n '1,260p' /tmp/v5-s7c-launcher-inference-search.txt
> ```
>
> Do not write `/tmp/v5-s7c-launcher-inference-search.txt` into the repository.
>
> Do not run installers.
>
> Do not start Pulse.
>
> Do not invoke Claude Code.
>
> Do not run Codex import/migration tooling.
>
> Do not read user-local private state.
>
> ### Required file: `docs/adapters/V5_S7C_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S7C Execution Plan
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
> 2. S0-S7A reread.
> 3. Launcher/inference release evidence reread.
> 4. Official Codex CLI/noninteractive/config/sandbox evidence refresh if new Codex claims are needed.
> 5. Launcher seam spec drafting.
> 6. Inference seam spec drafting.
> 7. Engine profile and capability contract drafting.
> 8. Launcher/inference decision log drafting.
> 9. Self-review and repair.
> 10. Final handoff and goal-state report.
>
> The self-review rubric must total 100 points:
>
> | Area                                                       | Points |
> | ---------------------------------------------------------- | -----: |
> | Scope and protected-path discipline                        |     15 |
> | Evidence discipline                                        |     15 |
> | Launcher coupling and seam quality                         |     20 |
> | Inference coupling and seam quality                        |     20 |
> | Engine profile/capability contract quality                 |     15 |
> | Existing-local-v5, memory, ISA, Pulse, and rollback safety |     10 |
> | Verification quality                                       |      5 |
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
> ### Required file: `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
>
> Purpose: define the future launcher seam that would allow PAI v5 to select Codex as a local runtime engine without mutating upstream release files or invoking Claude-shaped behavior.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Launcher Seam Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Launcher Problem Statement
> ## Existing Claude Launcher Couplings
> ## Launcher Seam Principles
> ## Engine Selection Model
> ## Invocation Boundary Model
> ## Environment and Path Model
> ## Argument and Flag Model
> ## Authority Envelope Handoff
> ## Sandbox and Permission Handoff
> ## Pulse Startup Boundary
> ## Memory and ISA Boundary
> ## Error and Exit-Code Model
> ## Rollback and Fallback Model
> ## Candidate Launcher Seam Designs
> ## Required Future Proofs
> ## Prohibited Launcher Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * Define launcher seam as a future engine-selection boundary, not an implementation.
> * Inventory observed Claude launcher assumptions from `pai.ts`, S6, and S7A evidence where supported.
> * Define that future launcher must preserve PAI semantics without mutating release files.
> * Define engine selection as future policy, not S7C action.
> * Define required future inputs:
>
>   * `engine_id`
>   * `pai_dir`
>   * `authority_envelope_id`
>   * `adapter_mode`
>   * `source_kind`
>   * `sandbox_policy`
>   * `permission_policy`
>   * `memory_policy`
>   * `isa_policy`
>   * `pulse_policy`
>   * `audit_policy`
>   * `rollback_policy`
> * Define required future outputs:
>
>   * selected engine;
>   * resolved paths;
>   * invocation plan;
>   * denied behaviors;
>   * unsupported-surface report;
>   * audit envelope;
>   * rollback path.
> * Define that future launcher must not start Pulse unless explicitly authorized by later Pulse milestone.
> * Define that future launcher must not write PAI Memory or ISA during read-only trial mode.
> * Define at least three candidate launcher seam designs:
>
>   * `LS-1`: documentation-only engine selection contract;
>   * `LS-2`: future manifest-mediated launcher plan;
>   * `LS-3`: future profile-mediated launcher wrapper.
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
>   * `S7C decision`
> * State that S7C chooses no runtime implementation.
>
> ### Required file: `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`
>
> Purpose: define the future inference seam that would let PAI v5 delegate model calls to Codex-native mechanisms without assuming Claude CLI behavior.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Inference Seam Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Inference Problem Statement
> ## Existing Claude Inference Couplings
> ## Inference Seam Principles
> ## Request Envelope Model
> ## Response Envelope Model
> ## Streaming and Non-Streaming Model
> ## Error and Retry Model
> ## Tool and MCP Boundary
> ## Authority and Context Boundary
> ## Memory and ISA Boundary
> ## Pulse Boundary
> ## Audit and Provenance Boundary
> ## Candidate Inference Seam Designs
> ## Required Future Proofs
> ## Prohibited Inference Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * Define inference seam as a future model-call abstraction, not an implementation.
> * Inventory observed Claude inference assumptions from `Inference.ts`, S6, and S7A evidence where supported.
> * Define required future request fields:
>
>   * `request_id`
>   * `engine_id`
>   * `adapter_mode`
>   * `authority_envelope_id`
>   * `prompt_source`
>   * `context_sources`
>   * `allowed_tools`
>   * `denied_tools`
>   * `memory_policy`
>   * `isa_policy`
>   * `pulse_policy`
>   * `audit_policy`
>   * `output_policy`
> * Define required future response fields:
>
>   * `request_id`
>   * `engine_id`
>   * `status`
>   * `model_or_runtime_report`
>   * `output`
>   * `unsupported_surface_report`
>   * `denied_action_report`
>   * `memory_write_status`
>   * `isa_write_status`
>   * `pulse_action_status`
>   * `provenance`
>   * `failure_reason`
> * Define streaming and non-streaming as future compatibility dimensions.
> * Define that tool/MCP behavior must be bounded and cannot silently emulate Claude behavior.
> * Define that inference must not promote Codex memory into PAI Memory.
> * Define that inference must not write ISA or PAI Memory in read-only mode.
> * Define at least three candidate inference seam designs:
>
>   * `IS-1`: documentation-only inference envelope contract;
>   * `IS-2`: future manifest-mediated noninteractive inference plan;
>   * `IS-3`: future engine adapter interface with audit envelope.
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
>   * `S7C decision`
> * State that S7C chooses no runtime implementation.
>
> ### Required file: `docs/adapters/V5_CODEX_ENGINE_PROFILE_AND_CAPABILITY_CONTRACT.md`
>
> Purpose: define the future engine profile and capability contract needed before PAI can decide whether Codex is eligible for read-only, assisted, or write-capable modes.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Engine Profile and Capability Contract
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Engine Profile Problem Statement
> ## Engine Identity Model
> ## Capability Declaration Model
> ## Unsupported Surface Reporting
> ## Authority Capability Fields
> ## Launcher Capability Fields
> ## Inference Capability Fields
> ## Tool and MCP Capability Fields
> ## Sandbox and Permission Capability Fields
> ## Memory Capability Fields
> ## ISA Capability Fields
> ## Pulse Capability Fields
> ## Audit and Provenance Capability Fields
> ## Mode Eligibility Rules
> ## Compatibility Scoring Model
> ## Required Future Proofs
> ## Prohibited Capability Claims
> ## Non-Goals
> ```
>
> Required content:
>
> * Define engine profile as future declarative metadata, not a runtime config file.
> * State that S7C creates no engine profile instance.
> * Define required future fields:
>
>   * `engine_id`
>   * `engine_name`
>   * `engine_kind`
>   * `adapter_status`
>   * `supported_modes`
>   * `authority_capabilities`
>   * `launcher_capabilities`
>   * `inference_capabilities`
>   * `tool_capabilities`
>   * `sandbox_capabilities`
>   * `memory_capabilities`
>   * `isa_capabilities`
>   * `pulse_capabilities`
>   * `audit_capabilities`
>   * `unsupported_surfaces`
>   * `proof_artifacts`
>   * `rollback_support`
> * Define allowed future `supported_modes` values:
>
>   * `documentation-only`
>   * `fixture-read-only`
>   * `existing-local-v5-read-only`
>   * `assisted-patch`
>   * `controlled-single-writer`
>   * `codex-only-replacement`
>   * `dual-engine-coexistence`
> * State that S7C permits only documentation-only status.
> * Define that unsupported surfaces must be reported explicitly.
> * Define that missing Pulse, Memory, ISA, launcher, or inference proofs block drop-in claims.
> * Define that any write-capable mode requires single-writer policy.
> * Define compatibility scoring as future evaluation only.
> * State that S7C cannot mark Codex as drop-in-capable.
>
> ### Required file: `docs/adapters/V5_CODEX_LAUNCHER_INFERENCE_DECISION_LOG.md`
>
> Purpose: record S7C decisions, non-decisions, blocked decisions, and future architect questions for launcher and inference seams.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Launcher and Inference Decision Log
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Decisions Made in S7C
> ## Non-Decisions in S7C
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
> * `S7C-D01`: Codex remains not drop-in today.
> * `S7C-D02`: Launcher replacement requires an explicit engine seam.
> * `S7C-D03`: Inference replacement requires an explicit request/response envelope.
> * `S7C-D04`: Future launcher must preserve authority envelope boundaries.
> * `S7C-D05`: Future inference must report unsupported surfaces instead of silently emulating Claude.
> * `S7C-D06`: Pulse startup remains blocked in S7C.
> * `S7C-D07`: PAI Memory and ISA writes remain blocked.
> * `S7C-D08`: No engine profile instance is created in S7C.
> * `S7C-D09`: Runtime wrappers and generated configs remain prohibited.
> * `S7C-D10`: Root `AGENTS.md` and `.codex/` remain protected.
> * `S7C-D11`: Future drop-in claims require launcher, inference, authority, Pulse, Memory, ISA, and rollback proofs.
> * `S7C-D12`: No user-local state is inspected in S7C.
>
> The `## Next Milestone Candidates` section must list advisory-only options, not approvals:
>
> * `V5-S7B`: Fixture-only coupling validation harness design.
> * `V5-S7D`: Hook/lifecycle mapping design.
> * `V5-S7E`: Pulse bridge identity and read-only event model.
> * `V5-S8B`: Engine profile schema proposal, if S7C is accepted.
> * `V5-S8C`: Launcher/inference fixture validation design, if S7C is accepted.
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
> S7C fails immediately if:
>
> * Any file outside the approved write set is created or modified.
> * Any protected file is modified.
> * Runtime adapter files are created.
> * Root `AGENTS.md` is created or modified.
> * `.codex/` is created or modified.
> * Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, or migration scripts are created.
> * An engine profile instance is created.
> * User-local private state is inspected or modified.
> * Pulse is started.
> * Installers are run.
> * Claude Code is invoked.
> * Codex is invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available.
> * Codex import or migration tooling is run.
> * The docs claim Codex is drop-in today.
> * The docs claim Codex is the official upstream engine.
> * The docs authorize PAI Memory writes.
> * The docs authorize ISA writes.
> * The docs authorize Pulse implementation.
> * The docs authorize existing-local-v5 trial execution.
> * The docs imply Claude-shaped files can be copied directly into Codex surfaces.
> * The docs propose installing any launcher, wrapper, engine profile, or inference adapter.
> * The goal advances beyond S7C.
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
>     "docs/adapters/V5_CODEX_ENGINE_PROFILE_AND_CAPABILITY_CONTRACT.md",
>     "docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md",
>     "docs/adapters/V5_CODEX_LAUNCHER_INFERENCE_DECISION_LOG.md",
>     "docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md",
>     "docs/adapters/V5_S7C_EXEC_PLAN.md",
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
>     "docs/adapters/V5_S7C_EXEC_PLAN.md": [
>         "# V5-S7C Execution Plan",
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
>     "docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md": [
>         "# V5 Codex Launcher Seam Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Launcher Problem Statement",
>         "## Existing Claude Launcher Couplings",
>         "## Launcher Seam Principles",
>         "## Engine Selection Model",
>         "## Invocation Boundary Model",
>         "## Environment and Path Model",
>         "## Argument and Flag Model",
>         "## Authority Envelope Handoff",
>         "## Sandbox and Permission Handoff",
>         "## Pulse Startup Boundary",
>         "## Memory and ISA Boundary",
>         "## Error and Exit-Code Model",
>         "## Rollback and Fallback Model",
>         "## Candidate Launcher Seam Designs",
>         "## Required Future Proofs",
>         "## Prohibited Launcher Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md": [
>         "# V5 Codex Inference Seam Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Inference Problem Statement",
>         "## Existing Claude Inference Couplings",
>         "## Inference Seam Principles",
>         "## Request Envelope Model",
>         "## Response Envelope Model",
>         "## Streaming and Non-Streaming Model",
>         "## Error and Retry Model",
>         "## Tool and MCP Boundary",
>         "## Authority and Context Boundary",
>         "## Memory and ISA Boundary",
>         "## Pulse Boundary",
>         "## Audit and Provenance Boundary",
>         "## Candidate Inference Seam Designs",
>         "## Required Future Proofs",
>         "## Prohibited Inference Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_ENGINE_PROFILE_AND_CAPABILITY_CONTRACT.md": [
>         "# V5 Codex Engine Profile and Capability Contract",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Engine Profile Problem Statement",
>         "## Engine Identity Model",
>         "## Capability Declaration Model",
>         "## Unsupported Surface Reporting",
>         "## Authority Capability Fields",
>         "## Launcher Capability Fields",
>         "## Inference Capability Fields",
>         "## Tool and MCP Capability Fields",
>         "## Sandbox and Permission Capability Fields",
>         "## Memory Capability Fields",
>         "## ISA Capability Fields",
>         "## Pulse Capability Fields",
>         "## Audit and Provenance Capability Fields",
>         "## Mode Eligibility Rules",
>         "## Compatibility Scoring Model",
>         "## Required Future Proofs",
>         "## Prohibited Capability Claims",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_LAUNCHER_INFERENCE_DECISION_LOG.md": [
>         "# V5 Codex Launcher and Inference Decision Log",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Decisions Made in S7C",
>         "## Non-Decisions in S7C",
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
>         "docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md",
>         "docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md",
>         "docs/adapters/V5_CODEX_ENGINE_PROFILE_AND_CAPABILITY_CONTRACT.md",
>         "docs/adapters/V5_CODEX_LAUNCHER_INFERENCE_DECISION_LOG.md",
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
>     "authority envelope",
>     "launcher seam",
>     "inference seam",
>     "engine profile",
>     "capability contract",
>     "unsupported surface",
>     "PAI Memory",
>     "ISA",
>     "Pulse",
>     "single-writer",
>     "not PAI Memory",
>     "product memories",
>     "read-only",
>     "reversible",
>     "rollback",
>     "exit-code",
>     "request envelope",
>     "response envelope",
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
> Run launcher candidate check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md").read_text(encoding="utf-8")
>
> required_ids = ["LS-1", "LS-2", "LS-3"]
>
> missing = [rid for rid in required_ids if rid not in text]
>
> if missing:
>     print("missing launcher seam candidates:")
>     for rid in missing:
>         print(f"- {rid}")
>     raise SystemExit(1)
>
> print("launcher seam candidates ok")
> PY
> ```
>
> Run inference candidate check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md").read_text(encoding="utf-8")
>
> required_ids = ["IS-1", "IS-2", "IS-3"]
>
> missing = [rid for rid in required_ids if rid not in text]
>
> if missing:
>     print("missing inference seam candidates:")
>     for rid in missing:
>         print(f"- {rid}")
>     raise SystemExit(1)
>
> print("inference seam candidates ok")
> PY
> ```
>
> Run decision ID check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_LAUNCHER_INFERENCE_DECISION_LOG.md").read_text(encoding="utf-8")
>
> required_ids = [
>     "S7C-D01",
>     "S7C-D02",
>     "S7C-D03",
>     "S7C-D04",
>     "S7C-D05",
>     "S7C-D06",
>     "S7C-D07",
>     "S7C-D08",
>     "S7C-D09",
>     "S7C-D10",
>     "S7C-D11",
>     "S7C-D12",
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
> S7C is complete only if:
>
> * Exactly the five approved S7C files are created or modified.
> * No protected files are changed.
> * No runtime adapter files are created.
> * No root `AGENTS.md` is created or modified.
> * No `.codex/` files are created or modified.
> * No Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, or migration scripts are created.
> * No engine profile instance is created.
> * No user-local state is inspected or modified.
> * Pulse is not started.
> * Installers are not run.
> * Claude Code is not invoked.
> * Codex is not invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available.
> * Codex import/migration tooling is not run.
> * `V5_S7C_EXEC_PLAN.md` contains the Completion Contract copied into its `## Completion Contract` section.
> * The launcher seam spec includes candidate designs `LS-1`, `LS-2`, and `LS-3`.
> * The inference seam spec includes candidate designs `IS-1`, `IS-2`, and `IS-3`.
> * The engine profile contract defines documentation-only as the only S7C-permitted status.
> * The decision log includes all required `S7C-D01` through `S7C-D12` decisions.
> * The docs do not claim Codex is drop-in today.
> * The docs do not claim Codex is the official upstream engine.
> * The docs do not authorize PAI Memory writes.
> * The docs do not authorize ISA writes.
> * The docs do not authorize Pulse implementation.
> * The docs do not authorize existing-local-v5 trial execution.
> * The docs do not imply Claude-shaped files can be copied directly into Codex surfaces.
> * The docs do not propose installing any launcher, wrapper, engine profile, or inference adapter.
> * The execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures.
> * Changed-file check passes.
> * Heading sequence check passes.
> * Content invariant check passes.
> * Launcher candidate check passes.
> * Inference candidate check passes.
> * Decision ID check passes.
> * Protected-path check has no output.
> * Final handoff reports every required validation command.
>
> ### Final handoff format
>
> End with exactly these headings:
>
> ```markdown
> ## Files changed
>
> ## Behavior changed
>
> ## Tests run
>
> ## Known risks
>
> ## Protected files changed
>
> ## Goal state
>
> ## Recommended next architect decision
> ```
>
> `Protected files changed` must be exactly `Yes` or `No`, followed by a brief explanation.
>
> Expected value:
>
> ```text
> No - only the five approved S7C docs were created or modified.
> ```
>
> `Recommended next architect decision` must be advisory only. Do not begin S7B, S7D, S7E, S8B, or S8C.
>
> ### Stop conditions
>
> Stop and report immediately if:
>
> * Any protected file must be edited.
> * Any file outside the approved write set is modified.
> * Runtime implementation seems necessary.
> * Root `AGENTS.md` or `.codex/` would need to be modified.
> * A Codex config, hook, rule, skill, subagent, agent, command, launcher, installer, wrapper, fixture, harness, executable schema, manifest, audit artifact, generated config, or migration script would need to be created.
> * An engine profile instance would need to be created.
> * Upstream v5 would need to be patched.
> * Private user-local memory would need to be read.
> * Codex import/migration tooling seems necessary.
> * Pulse would need to be started.
> * Claude Code would need to be invoked.
> * Codex would need to be invoked as a runtime engine.
> * The goal tries to continue beyond S7C.
> * The Completion Contract cannot be copied into the execution plan.
> * The self-review cannot reach 94/100 without leaving scope.

## Milestones

1. Baseline status check.
2. S0-S7A reread.
3. Launcher/inference release evidence reread.
4. Official Codex CLI/noninteractive/config/sandbox evidence refresh if new Codex claims are needed.
5. Launcher seam spec drafting.
6. Inference seam spec drafting.
7. Engine profile and capability contract drafting.
8. Launcher/inference decision log drafting.
9. Self-review and repair.
10. Final handoff and goal-state report.

## Self-Review Rubric

| Area | Points |
| --- | ---: |
| Scope and protected-path discipline | 15 |
| Evidence discipline | 15 |
| Launcher coupling and seam quality | 20 |
| Inference coupling and seam quality | 20 |
| Engine profile/capability contract quality | 15 |
| Existing-local-v5, memory, ISA, Pulse, and rollback safety | 10 |
| Verification quality | 5 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

S7C fails immediately if:

- Any file outside the approved write set is created or modified.
- Any protected file is modified.
- Runtime adapter files are created.
- Root `AGENTS.md` is created or modified.
- `.codex/` is created or modified.
- Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, or migration scripts are created.
- An engine profile instance is created.
- User-local private state is inspected or modified.
- Pulse is started.
- Installers are run.
- Claude Code is invoked.
- Codex is invoked as a runtime engine beyond non-invasive `codex --version` or `codex --help` if already available.
- Codex import or migration tooling is run.
- The docs claim Codex is drop-in today.
- The docs claim Codex is the official upstream engine.
- The docs authorize PAI Memory writes.
- The docs authorize ISA writes.
- The docs authorize Pulse implementation.
- The docs authorize existing-local-v5 trial execution.
- The docs imply Claude-shaped files can be copied directly into Codex surfaces.
- The docs propose installing any launcher, wrapper, engine profile, or inference adapter.
- The goal advances beyond S7C.

## Validation Commands

Required validation commands:

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Changed-file Python check.
- Exact H1/H2 heading sequence check.
- Content invariant check.
- Launcher candidate check.
- Inference candidate check.
- Decision ID check.
- Protected-path check.

## Progress

- Started the bounded V5-S7C goal.
- Confirmed the baseline worktree was clean before S7C edits.
- Created this execution plan first.
- Copied the Completion Contract into this execution plan before drafting other S7C deliverables.
- Confirmed required source files exist:
  - `Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts`
  - `Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts`
  - `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
  - `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
  - `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- Ran the required launcher/inference search and wrote results only to `/tmp/v5-s7c-launcher-inference-search.txt`.
- Reviewed allowed S0-S7A adapter docs and repository-local v5 release evidence.
- Created `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`.
- Created `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`.
- Created `docs/adapters/V5_CODEX_ENGINE_PROFILE_AND_CAPABILITY_CONTRACT.md`.
- Created `docs/adapters/V5_CODEX_LAUNCHER_INFERENCE_DECISION_LOG.md`.
- Did not refresh official Codex docs because S7C did not add new Codex capability claims beyond prior official-source adapter evidence.
- Did not invoke Claude Code.
- Did not invoke Codex as a runtime engine.
- Did not inspect private user-local state.
- Did not run installers, start Pulse, run Codex import or migration tooling, run a read-only trial, create runtime files, or modify release files.
- Completed preliminary validation before this final execution-plan update:
  - `git status --short`: showed only the five approved S7C docs as intent-to-add.
  - `git diff --name-only | sort`: listed exactly the five approved S7C docs.
  - `git diff --check`: passed.
  - Changed-file Python check: passed.
  - Exact H1/H2 heading sequence check: passed.
  - Content invariant check: passed.
  - Launcher candidate check: passed.
  - Inference candidate check: passed.
  - Decision ID check: passed.
  - Protected-path check: passed with no output.

## Iteration Log

| Iteration | Scope discipline | Evidence discipline | Launcher seam | Inference seam | Engine contract | Safety | Verification | Total | Hard failures | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| S7C-I0 initial plan | 15 | 10 | 0 | 0 | 0 | 8 | 1 | 34/100 | 0 | Execution plan created; deliverables not yet drafted. |
| S7C-I1 final self-review | 15 | 15 | 19 | 19 | 15 | 10 | 5 | 98/100 | 0 | Pass. Launcher and inference seams are design-only, evidence-backed, and validated against the S7C contract. |

## Surprises & Discoveries

- `pai.ts` is not only a launcher wrapper; it also contains update and MCP helper behavior. S7C records the launcher-relevant couplings without authorizing any installer, updater, MCP mutation, wrapper, or generated config work.
- `pai.ts` launch behavior includes Claude version checks, `.claude` path defaults, `--append-system-prompt-file`, environment cleanup, Pulse notification attempts, and process exit handling. These are future launcher-seam concerns, not S7C implementation work.
- `Inference.ts` is tightly shaped around Claude CLI flags, stdin/stdout/stderr behavior, model aliases, text output parsing, timeout handling, and restricted tool options. These are future inference-envelope concerns, not S7C implementation work.
- Release evidence includes live user-local path references under `~/.claude/PAI/`, but S7C read only repository-local release files and did not inspect user-local private state.

## Decision Log

- S7C will use S0-S7A adapter docs and repository-local v5 release evidence.
- S7C will use official OpenAI Codex docs only if a new or refreshed Codex capability claim is needed.
- S7C will not invoke Claude Code.
- S7C will not invoke Codex as a runtime engine.
- S7C will not inspect private user-local state.
- S7C will not create launcher, wrapper, engine profile instance, inference adapter, or generated config.
- S7C keeps Codex as not currently proven drop-in for existing local PAI v5 files.
- S7C defines launcher and inference seams as future contracts, not files to install or run.
- S7C keeps `PAI_SYSTEM_PROMPT.md` as high-authority doctrine and `CLAUDE.md` as an official Claude-facing surface, not a Codex destination file.
- S7C keeps PAI Memory and ISA writes blocked and treats Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state as not PAI Memory.
- S7C keeps Pulse central to v5 infrastructure while blocking Pulse startup or bridge implementation in this milestone.

## Outcomes & Retrospective

S7C created exactly the five approved design documents and stayed inside the approved write set.

Deliverables:

- `docs/adapters/V5_S7C_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_LAUNCHER_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_INFERENCE_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_ENGINE_PROFILE_AND_CAPABILITY_CONTRACT.md`
- `docs/adapters/V5_CODEX_LAUNCHER_INFERENCE_DECISION_LOG.md`

Final validation results:

- `git status --short`: passed; output lists only the five approved S7C docs.
- `git diff --name-only | sort`: passed; output lists exactly the five approved S7C docs.
- `git diff --check`: passed with no output.
- Changed-file Python check: passed.
- Exact H1/H2 heading sequence check: passed.
- Content invariant check: passed.
- Launcher candidate check: passed.
- Inference candidate check: passed.
- Decision ID check: passed.
- Protected-path check: passed with no output.

Completion audit result:

- Prompt-to-artifact audit passed after confirming the five approved docs, required headings, required candidate IDs, required decision IDs, required launcher/inference/engine contract fields, non-implementation posture, protected-path cleanliness, and no authorization of runtime behavior.

Goal-state note:

- `/goal clear` is unavailable in this tool surface unless a later tool appears.
