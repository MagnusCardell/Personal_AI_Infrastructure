# V5-S6 Execution Plan

## Purpose

Execute the V5-S6 Claude Coupling Inventory and Codex Decoupling Seam Design milestone as a design-only documentation milestone.

S6 identifies material Claude Code couplings in the PAI v5.0.0 release and prior adapter docs, then defines future decoupling seams and drop-in readiness gates. S6 does not implement a Codex adapter or create runtime surfaces.

## Scope

S6 creates only the approved S6 documentation artifacts:

- `docs/adapters/V5_S6_EXEC_PLAN.md`
- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_DECOUPLING_DECISION_LOG.md`

S6 does not create runtime files, root `AGENTS.md`, `.codex/`, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, or migration scripts.

## Approved Write Set

Approved write set:

- `docs/adapters/V5_S6_EXEC_PLAN.md`
- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_DECOUPLING_DECISION_LOG.md`

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

Protected private user-local paths:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`

## Source Protocol

Use only:

1. S0-S5 adapter docs for prior adapter conclusions.
2. Repository-local PAI v5 release files for PAI facts.
3. Official OpenAI Codex docs only if S6 adds a new Codex capability claim not already captured in S2/S3.
4. Local `codex --version` or `codex --help` only if already available and non-invasive.

Do not use unofficial Codex capability sources.

Do not infer current Codex behavior from memory.

## Source Material

Approved adapter docs for read-only use:

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

Approved release paths for read-only use:

- `Releases/v5.0.0/`
- `Releases/v5.0.0/.claude/`

## Completion Contract

The Completion Contract from the prompt is copied below. Markdown blockquote markers are document formatting only and are not intended to change the contract text.

> This Completion Contract is the authoritative contract for V5-S6.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S6_EXEC_PLAN.md`.
>
> Do not mark S6 complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S6 docs must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S6 does not implement decoupling.
> * S6 does not create runtime adapter seams.
> * S6 does not create root `AGENTS.md`.
> * S6 does not create `.codex/`.
> * S6 does not create fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, or migration scripts.
> * Claude-shaped files must not be copied directly into Codex surfaces.
> * Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
> * `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine, not ordinary markdown.
> * `CLAUDE.md` is an official Claude-facing surface, not a Codex destination file.
> * Codex `AGENTS.md`, if later authorized, must be a compact router.
> * PAI Memory and ISA artifacts are canonical PAI state.
> * Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.
> * Product memories must not be silently promoted into PAI Memory.
> * Future read-only trials must not require uninstalling Claude Code.
> * Future read-only trials must be reversible and must not write PAI state.
> * Future writes require a single-writer policy, provenance, rollback, and validation.
> * Pulse remains central v5 infrastructure, but S6 does not design or implement a Pulse bridge.
>
> ### Required local discovery commands
>
> Run these commands from repository root:
>
> ```bash
> git status --short
>
> test -d Releases/v5.0.0/.claude
> test -f Releases/v5.0.0/.claude/CLAUDE.md
> test -f Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md
>
> rg -n --hidden --glob '!**/.git/**' \
>   'claude|Claude|CLAUDE|anthropic|Anthropic|PAI_SYSTEM_PROMPT|append-system-prompt|AGENTS\.md|codex|Codex|PAI_DIR|Pulse|PULSE|31337|ISA|Memory|WORK|LEARNING|KNOWLEDGE|hook|hooks|skill|skills|agent|agents|command|commands|settings|Inference|pai\.ts|spawn|exec|Bun|mcp|MCP' \
>   Releases/v5.0.0 docs/adapters \
>   > /tmp/v5-s6-coupling-search.txt || true
>
> sed -n '1,240p' /tmp/v5-s6-coupling-search.txt
> ```
>
> Do not write `/tmp/v5-s6-coupling-search.txt` into the repository.
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
> ### Required file: `docs/adapters/V5_S6_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S6 Execution Plan
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
> 2. S0-S5 reread.
> 3. v5 release coupling search.
> 4. Claude coupling inventory drafting.
> 5. Codex decoupling seam design.
> 6. Drop-in readiness gate design.
> 7. Decoupling decision log drafting.
> 8. Self-review and repair.
> 9. Final handoff and goal-state report.
>
> The self-review rubric must total 100 points:
>
> | Area                                             | Points |
> | ------------------------------------------------ | -----: |
> | Scope and protected-path discipline              |     15 |
> | Evidence discipline                              |     15 |
> | Claude coupling inventory completeness           |     20 |
> | Decoupling seam quality                          |     20 |
> | Drop-in readiness gate quality                   |     15 |
> | Existing-local-v5, memory, ISA, and Pulse safety |     10 |
> | Verification quality                             |      5 |
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
> ### Required file: `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
>
> Purpose: inventory every material Claude Code coupling found in the PAI v5.0.0 release and prior adapter docs.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Claude Coupling Inventory
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Coupling Classification Model
> ## Executive Summary
> ## Instruction and Authority Couplings
> ## Launcher and Inference Couplings
> ## Settings and Permission Couplings
> ## Hook and Lifecycle Couplings
> ## Skill Couplings
> ## Agent and Command Couplings
> ## Pulse Couplings
> ## Memory and ISA Couplings
> ## Installer and Local Layout Couplings
> ## Product Memory Couplings
> ## User-Local State Couplings
> ## Coupling Inventory Table
> ## Highest-Risk Couplings
> ## Non-Couplings and False Positives
> ## Unknowns for Architect Review
> ## Non-Goals
> ```
>
> Required content:
>
> Define the coupling classification model:
>
> | Class                              | Meaning                                                                                    |
> | ---------------------------------- | ------------------------------------------------------------------------------------------ |
> | `C0: Not a coupling`               | Mention/reference only; no adapter impact.                                                 |
> | `C1: Documentation coupling`       | PAI docs assume Claude Code but runtime path is not directly coupled.                      |
> | `C2: Instruction-surface coupling` | Claude-facing instructions or authority path must be mapped to Codex-native authority.     |
> | `C3: Runtime invocation coupling`  | Code or script invokes Claude Code or assumes Claude CLI behavior.                         |
> | `C4: Lifecycle/event coupling`     | Hooks, events, or lifecycle semantics assume Claude Code.                                  |
> | `C5: State/layout coupling`        | PAI state or install layout assumes `.claude`, `PAI_DIR`, or Claude product paths.         |
> | `C6: Safety/security coupling`     | Settings, permissions, sandbox, or trust behavior assumes Claude Code.                     |
> | `C7: Central-system coupling`      | Pulse, Memory, ISA, or daemon behavior is coupled to Claude-specific identity or behavior. |
> | `C8: Blocker`                      | Coupling blocks drop-in replacement until a future seam/spec/test exists.                  |
>
> Include a table with columns:
>
> ```text
> Coupling ID | Release path or evidence source | Coupling class | Coupled surface | Observed Claude assumption | Codex replacement hazard | Required seam | Drop-in impact | S6 decision
> ```
>
> Minimum rows to include, if supported by repository evidence:
>
> * `CC-001`: `PAI_SYSTEM_PROMPT.md` authority handling.
> * `CC-002`: `CLAUDE.md` as official Claude-facing instruction surface.
> * `CC-003`: `PAI_DIR` rooted in or around `.claude` / user-local PAI layout.
> * `CC-004`: `pai.ts` launcher or command path invoking or assuming Claude Code.
> * `CC-005`: `Inference.ts` invoking or assuming Claude CLI behavior.
> * `CC-006`: `.claude/settings.json` permission/config semantics.
> * `CC-007`: Claude lifecycle hooks.
> * `CC-008`: hook payload/context assumptions.
> * `CC-009`: PAI skills authored for Claude-facing skill semantics.
> * `CC-010`: PAI agents/subagents authored for Claude-facing agent semantics.
> * `CC-011`: PAI commands/slash commands authored for Claude-facing command semantics.
> * `CC-012`: Pulse dashboard/daemon behavior tied to Claude identity or jobs.
> * `CC-013`: Pulse jobs or automation invoking Claude behavior.
> * `CC-014`: PAI Memory read/write expectations.
> * `CC-015`: ISA creation/update workflow expectations.
> * `CC-016`: installer/local install layout under `.claude`.
> * `CC-017`: Claude Code product memory boundary.
> * `CC-018`: Codex memory boundary as non-PAI state.
> * `CC-019`: repository root governance vs product payload boundary.
> * `CC-020`: future Codex native surfaces being absent by design in S6.
>
> Do not invent evidence. If a row is not supported by repository evidence, mark it as `unknown / not confirmed` and explain.
>
> ### Required file: `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
>
> Purpose: define future engine-seam design requirements that would allow Codex to replace Claude Code without copying Claude-shaped files or mutating upstream release files.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Decoupling Seam Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Seam Design Principles
> ## Engine Boundary Model
> ## Authority Seam
> ## Router Seam
> ## Launcher Seam
> ## Inference Seam
> ## Settings and Permission Seam
> ## Hook and Lifecycle Seam
> ## Skill Seam
> ## Agent and Command Seam
> ## Pulse Seam
> ## Memory Seam
> ## ISA Seam
> ## Installer and Local Layout Seam
> ## Product Memory Boundary Seam
> ## Rollback Seam
> ## Seam Dependency Graph
> ## Prohibited Seam Designs
> ## Future Implementation Gates
> ## Non-Goals
> ```
>
> Required content:
>
> Define seam design principles:
>
> * Thin adapter over upstream PAI semantics.
> * Native Codex surfaces only.
> * No direct copying of Claude-shaped files into Codex surfaces.
> * No mutation of release files.
> * No private user-local state access without explicit future approval.
> * Read-only first.
> * Single-writer before any PAI state writes.
> * Reversible by default.
> * Provenance-tagged outputs.
> * Pulse centrality preserved without claiming Pulse parity.
> * PAI Memory and ISA canonicality preserved.
>
> For each seam, include:
>
> ```text
> Seam | Purpose | Inputs | Outputs | Forbidden behavior | Required future spec | Required future tests | Drop-in relevance
> ```
>
> Minimum seams:
>
> * Authority seam.
> * Router seam.
> * Launcher seam.
> * Inference seam.
> * Settings/permission seam.
> * Hook/lifecycle seam.
> * Skill seam.
> * Agent/command seam.
> * Pulse seam.
> * Memory seam.
> * ISA seam.
> * Installer/local layout seam.
> * Product-memory boundary seam.
> * Rollback seam.
>
> Include a seam dependency graph as prose or markdown table. Do not create a diagram file.
>
> ### Required file: `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
>
> Purpose: define the gates that must pass before Codex can be described as drop-in-capable for PAI v5.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Drop-In Readiness Gates
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Drop-In Definition
> ## Non-Drop-In Conditions
> ## Gate Model
> ## Gate G0: Scope and Boundary Integrity
> ## Gate G1: Authority Equivalence
> ## Gate G2: Router Safety
> ## Gate G3: Launcher and Inference Replacement
> ## Gate G4: Settings and Permission Parity
> ## Gate G5: Hook and Lifecycle Mapping
> ## Gate G6: Skill Mapping
> ## Gate G7: Agent and Command Mapping
> ## Gate G8: Pulse Safety
> ## Gate G9: Memory Safety
> ## Gate G10: ISA Safety
> ## Gate G11: Existing Local v5 Read-Only Trial
> ## Gate G12: Single-Writer Controlled Write Mode
> ## Gate G13: Dual-Engine Coexistence
> ## Gate G14: Rollback and Reversibility
> ## Gate G15: User-Facing Support Posture
> ## Readiness Scoring Model
> ## Minimum Drop-In Claim Threshold
> ## Blockers Remaining After S6
> ## Non-Goals
> ```
>
> Required content:
>
> Define drop-in as:
>
> ```text
> A future state where a user with an existing local PAI v5 installation can choose Codex as the local runtime engine for PAI workflows without uninstalling Claude Code, overwriting Claude-facing files, corrupting PAI Memory/ISA/Pulse state, or losing rollback to the official Claude Code engine.
> ```
>
> State that S6 does not claim this threshold is met.
>
> Each gate must include:
>
> ```text
> Gate | Required proof | Failure signal | Current S6 status | Future milestone needed
> ```
>
> Gate status values:
>
> ```text
> Not started | Designed only | Evidence partial | Blocked | Candidate for future implementation | Passed
> ```
>
> S6 should not mark any runtime gate as `Passed`.
>
> The readiness scoring model must state that drop-in claims are prohibited unless:
>
> * all G0-G15 gates are either `Passed` or explicitly waived by architect review;
> * no write-safety gate is unresolved;
> * no Pulse/Memory/ISA safety gate is unresolved;
> * rollback has passed;
> * existing-local-v5 read-only trial has passed;
> * controlled-write validation has passed if write capability is claimed.
>
> ### Required file: `docs/adapters/V5_CODEX_DECOUPLING_DECISION_LOG.md`
>
> Purpose: record S6 decisions, non-decisions, and future architect questions.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Decoupling Decision Log
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Decisions Made in S6
> ## Non-Decisions in S6
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
> * `S6-D01`: Codex remains not drop-in today.
> * `S6-D02`: Decoupling requires explicit seams, not direct file copying.
> * `S6-D03`: Authority seam must be resolved before router creation.
> * `S6-D04`: Read-only local trial must precede write-capable modes.
> * `S6-D05`: Pulse bridge remains out of S6 scope.
> * `S6-D06`: PAI Memory/ISA writes remain blocked.
> * `S6-D07`: Root `AGENTS.md` and `.codex/` remain protected governance.
> * `S6-D08`: Future implementation must begin with either fixture/harness work or authority/router design, pending architect approval.
> * `S6-D09`: No user-local state is inspected in S6.
> * `S6-D10`: No runtime release files are changed in S6.
>
> The `## Next Milestone Candidates` section must list advisory-only options, not approvals:
>
> * `V5-S7A`: Authority seam and compact router design.
> * `V5-S7B`: Fixture-only coupling validation harness design.
> * `V5-S7C`: Launcher and inference seam design.
> * `V5-S7D`: Hook/lifecycle mapping design.
> * `V5-S7E`: Pulse bridge identity and read-only event model.
>
> State that architect approval is required before any S7 work.
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
> S6 fails immediately if:
>
> * Any file outside the approved write set is created or modified.
> * Any protected file is modified.
> * Runtime adapter files are created.
> * Root `AGENTS.md` is created or modified.
> * `.codex/` is created or modified.
> * Fixtures are created.
> * Harnesses are created.
> * Executable schemas are created.
> * Manifest or audit instances are created.
> * Installers, launchers, wrappers, hooks, rules, skills, subagents, agents, commands, or generated configs are created.
> * User-local private state is inspected or modified.
> * Pulse is started.
> * Installers are run.
> * Codex import or migration tooling is run.
> * The docs claim Codex is drop-in today.
> * The docs claim Codex is the official upstream engine.
> * The docs authorize PAI Memory writes.
> * The docs authorize ISA writes.
> * The docs authorize Pulse implementation.
> * The docs authorize existing-local-v5 trial execution.
> * The docs imply Claude-shaped files can be copied directly into Codex surfaces.
> * The goal advances beyond S6.
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
>     "docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md",
>     "docs/adapters/V5_CODEX_DECOUPLING_DECISION_LOG.md",
>     "docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md",
>     "docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md",
>     "docs/adapters/V5_S6_EXEC_PLAN.md",
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
>     "docs/adapters/V5_S6_EXEC_PLAN.md": [
>         "# V5-S6 Execution Plan",
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
>     "docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md": [
>         "# V5 Claude Coupling Inventory",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Coupling Classification Model",
>         "## Executive Summary",
>         "## Instruction and Authority Couplings",
>         "## Launcher and Inference Couplings",
>         "## Settings and Permission Couplings",
>         "## Hook and Lifecycle Couplings",
>         "## Skill Couplings",
>         "## Agent and Command Couplings",
>         "## Pulse Couplings",
>         "## Memory and ISA Couplings",
>         "## Installer and Local Layout Couplings",
>         "## Product Memory Couplings",
>         "## User-Local State Couplings",
>         "## Coupling Inventory Table",
>         "## Highest-Risk Couplings",
>         "## Non-Couplings and False Positives",
>         "## Unknowns for Architect Review",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md": [
>         "# V5 Codex Decoupling Seam Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Seam Design Principles",
>         "## Engine Boundary Model",
>         "## Authority Seam",
>         "## Router Seam",
>         "## Launcher Seam",
>         "## Inference Seam",
>         "## Settings and Permission Seam",
>         "## Hook and Lifecycle Seam",
>         "## Skill Seam",
>         "## Agent and Command Seam",
>         "## Pulse Seam",
>         "## Memory Seam",
>         "## ISA Seam",
>         "## Installer and Local Layout Seam",
>         "## Product Memory Boundary Seam",
>         "## Rollback Seam",
>         "## Seam Dependency Graph",
>         "## Prohibited Seam Designs",
>         "## Future Implementation Gates",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md": [
>         "# V5 Codex Drop-In Readiness Gates",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Drop-In Definition",
>         "## Non-Drop-In Conditions",
>         "## Gate Model",
>         "## Gate G0: Scope and Boundary Integrity",
>         "## Gate G1: Authority Equivalence",
>         "## Gate G2: Router Safety",
>         "## Gate G3: Launcher and Inference Replacement",
>         "## Gate G4: Settings and Permission Parity",
>         "## Gate G5: Hook and Lifecycle Mapping",
>         "## Gate G6: Skill Mapping",
>         "## Gate G7: Agent and Command Mapping",
>         "## Gate G8: Pulse Safety",
>         "## Gate G9: Memory Safety",
>         "## Gate G10: ISA Safety",
>         "## Gate G11: Existing Local v5 Read-Only Trial",
>         "## Gate G12: Single-Writer Controlled Write Mode",
>         "## Gate G13: Dual-Engine Coexistence",
>         "## Gate G14: Rollback and Reversibility",
>         "## Gate G15: User-Facing Support Posture",
>         "## Readiness Scoring Model",
>         "## Minimum Drop-In Claim Threshold",
>         "## Blockers Remaining After S6",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_DECOUPLING_DECISION_LOG.md": [
>         "# V5 Codex Decoupling Decision Log",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Decisions Made in S6",
>         "## Non-Decisions in S6",
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
>         "docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md",
>         "docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md",
>         "docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md",
>         "docs/adapters/V5_CODEX_DECOUPLING_DECISION_LOG.md",
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
>     "PAI Memory",
>     "ISA",
>     "Pulse",
>     "single-writer",
>     "not PAI Memory",
>     "product memories",
>     "read-only",
>     "reversible",
>     "drop-in",
>     "seam",
>     "launcher",
>     "inference",
>     "hook",
>     "skill",
>     "agent",
>     "command",
>     "rollback",
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
> Run coupling table minimum-row check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md").read_text(encoding="utf-8")
>
> required_ids = [
>     "CC-001",
>     "CC-002",
>     "CC-003",
>     "CC-004",
>     "CC-005",
>     "CC-006",
>     "CC-007",
>     "CC-008",
>     "CC-009",
>     "CC-010",
>     "CC-011",
>     "CC-012",
>     "CC-013",
>     "CC-014",
>     "CC-015",
>     "CC-016",
>     "CC-017",
>     "CC-018",
>     "CC-019",
>     "CC-020",
> ]
>
> missing = [rid for rid in required_ids if rid not in text]
>
> if missing:
>     print("missing coupling IDs:")
>     for rid in missing:
>         print(f"- {rid}")
>     raise SystemExit(1)
>
> print("coupling IDs ok")
> PY
> ```
>
> Run readiness gate check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md").read_text(encoding="utf-8")
>
> required_gates = [f"G{i}" for i in range(0, 16)]
> missing = [gate for gate in required_gates if gate not in text]
>
> if missing:
>     print("missing gates:")
>     for gate in missing:
>         print(f"- {gate}")
>     raise SystemExit(1)
>
> for forbidden in ["Gate G1: Authority Equivalence\n\nPassed", "Gate G8: Pulse Safety\n\nPassed", "Gate G9: Memory Safety\n\nPassed", "Gate G10: ISA Safety\n\nPassed"]:
>     if forbidden in text:
>         print(f"runtime safety gate appears incorrectly passed: {forbidden}")
>         raise SystemExit(1)
>
> print("readiness gates ok")
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
> S6 is complete only if:
>
> * Exactly the five approved S6 files are created or modified.
> * No protected files are changed.
> * No runtime adapter files are created.
> * No root `AGENTS.md` is created or modified.
> * No `.codex/` files are created or modified.
> * No fixtures are created.
> * No harnesses are created.
> * No executable schemas are created.
> * No manifest or audit instances are created.
> * No hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated configs, or migration scripts are created.
> * No user-local state is inspected or modified.
> * Pulse is not started.
> * Installers are not run.
> * Codex import/migration tooling is not run.
> * `V5_S6_EXEC_PLAN.md` contains the Completion Contract copied into its `## Completion Contract` section.
> * The Claude coupling inventory includes all required coupling IDs or explicitly marks unsupported rows as unknown/not confirmed.
> * The decoupling seam spec includes all required seams.
> * The drop-in readiness gates include G0-G15.
> * No runtime gate is marked as passed.
> * The decision log includes all required decisions.
> * The docs do not claim Codex is drop-in today.
> * The docs do not claim Codex is the official upstream engine.
> * The docs do not authorize PAI Memory writes.
> * The docs do not authorize ISA writes.
> * The docs do not authorize Pulse implementation.
> * The docs do not authorize existing-local-v5 trial execution.
> * The docs do not imply Claude-shaped files can be copied directly into Codex surfaces.
> * The execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures.
> * Changed-file check passes.
> * Heading sequence check passes.
> * Content invariant check passes.
> * Coupling table minimum-row check passes.
> * Readiness gate check passes.
> * Protected-path check has no output.
> * Final handoff reports every required validation command.

## Milestones

1. Baseline status check.
2. S0-S5 reread.
3. v5 release coupling search.
4. Claude coupling inventory drafting.
5. Codex decoupling seam design.
6. Drop-in readiness gate design.
7. Decoupling decision log drafting.
8. Self-review and repair.
9. Final handoff and goal-state report.

## Self-Review Rubric

| Area | Points |
| --- | ---: |
| Scope and protected-path discipline | 15 |
| Evidence discipline | 15 |
| Claude coupling inventory completeness | 20 |
| Decoupling seam quality | 20 |
| Drop-in readiness gate quality | 15 |
| Existing-local-v5, memory, ISA, and Pulse safety | 10 |
| Verification quality | 5 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

Scoring iterations are recorded in `## Iteration Log`.

## Hard Failure Conditions

Stop and report immediately if S6 requires:

- Any file outside the approved write set to be created or modified.
- Any protected file to be modified.
- Runtime adapter files.
- Root `AGENTS.md` creation or modification.
- `.codex/` creation or modification.
- Fixtures.
- Harnesses.
- Executable schemas.
- Manifest or audit instances.
- Installers, launchers, wrappers, hooks, rules, skills, subagents, agents, commands, or generated configs.
- User-local private state inspection or modification.
- Pulse startup.
- Installer execution.
- Codex import or migration tooling.
- Claiming Codex is drop-in today.
- Claiming Codex is the official upstream engine.
- Authorizing PAI Memory writes.
- Authorizing ISA writes.
- Authorizing Pulse implementation.
- Authorizing existing-local-v5 trial execution.
- Implying Claude-shaped files can be copied directly into Codex surfaces.
- Advancing beyond S6.

## Validation Commands

Required local discovery commands:

```bash
git status --short
test -d Releases/v5.0.0/.claude
test -f Releases/v5.0.0/.claude/CLAUDE.md
test -f Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md
rg -n --hidden --glob '!**/.git/**' \
  'claude|Claude|CLAUDE|anthropic|Anthropic|PAI_SYSTEM_PROMPT|append-system-prompt|AGENTS\.md|codex|Codex|PAI_DIR|Pulse|PULSE|31337|ISA|Memory|WORK|LEARNING|KNOWLEDGE|hook|hooks|skill|skills|agent|agents|command|commands|settings|Inference|pai\.ts|spawn|exec|Bun|mcp|MCP' \
  Releases/v5.0.0 docs/adapters \
  > /tmp/v5-s6-coupling-search.txt || true
sed -n '1,240p' /tmp/v5-s6-coupling-search.txt
```

Required final validation commands:

```bash
git status --short
git diff --name-only | sort
git diff --check
```

Additional required checks:

- Changed-file Python check.
- Exact H1/H2 heading sequence Python check.
- Content invariant Python check.
- Coupling table minimum-row Python check.
- Readiness gate Python check.
- Protected-path `git status --short -- ...` check.

## Progress

- Started the bounded V5-S6 goal.
- Confirmed the baseline worktree was clean before S6 edits.
- Created this execution plan first.
- Copied the Completion Contract into this execution plan before drafting other S6 deliverables.
- Ran required local discovery commands:
  - `git status --short` returned no output before S6 edits.
  - `test -d Releases/v5.0.0/.claude` passed.
  - `test -f Releases/v5.0.0/.claude/CLAUDE.md` passed.
  - `test -f Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md` passed.
  - Required `rg` coupling search wrote to `/tmp/v5-s6-coupling-search.txt` only.
  - `sed -n '1,240p' /tmp/v5-s6-coupling-search.txt` printed the required search excerpt.
- Reread S0-S5 adapter evidence and targeted repository-local v5 release files.
- Created `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`.
- Created `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`.
- Created `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`.
- Created `docs/adapters/V5_CODEX_DECOUPLING_DECISION_LOG.md`.
- Marked the five S6 docs as intent-to-add so `git diff --name-only`, `git diff --check`, and changed-file validation inspect the new docs.
- Ran validation checks and performed no repair outside the approved S6 write set.
- Ran final current-state validation after self-review repair; all required validation commands and the completion audit passed.

## Iteration Log

| Iteration | Scope discipline | Evidence discipline | Coupling inventory | Seam quality | Gate quality | Safety | Verification | Total | Hard failures | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| S6-I0 initial plan | 15 | 12 | 0 | 0 | 0 | 8 | 1 | 36/100 | 0 | Execution plan created; deliverables not yet drafted. |
| S6-I1 validation pass | 15 | 15 | 20 | 20 | 15 | 10 | 5 | 100/100 | 0 | All required S6 docs drafted, required IDs and gates present, validation commands passed before final execution-plan update. |

S6-I1 pass threshold record: 100/100 with 0 hard failures.

## Surprises & Discoveries

- `pai.ts` and `Inference.ts` both carry direct Claude CLI invocation assumptions, making launcher and inference seams separate blockers rather than one generic runtime lane.
- Pulse coupling is broader than scheduled Claude jobs: settings route SkillGuard and AgentGuard through Pulse HTTP hooks, and Pulse centrality affects lifecycle, observability, voice, and rollback.
- The release includes a `CodexResearcher` agent name, but S6 treats that as a false positive rather than proof of Codex runtime support.

## Decision Log

- S6 will use S0-S5 adapter docs and repository-local v5 release evidence only unless a new Codex capability claim becomes necessary.
- S6 will not use unofficial Codex capability sources.
- S6 will not inspect private user-local state.
- S6 will not create runtime adapter surfaces.
- Codex remains not drop-in today.
- Decoupling requires explicit seams, not direct file copying.
- Authority seam must be resolved before any future Codex router creation.
- Read-only local trial must precede write-capable modes.
- Pulse bridge work remains out of S6 scope.
- PAI Memory and ISA writes remain blocked.
- Root `AGENTS.md` and `.codex/` remain protected governance.
- Future S7 options are advisory only and require architect approval.

## Outcomes & Retrospective

S6 produced the five approved documentation artifacts only:

- `docs/adapters/V5_S6_EXEC_PLAN.md`
- `docs/adapters/V5_CLAUDE_COUPLING_INVENTORY.md`
- `docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_DROP_IN_READINESS_GATES.md`
- `docs/adapters/V5_CODEX_DECOUPLING_DECISION_LOG.md`

Validation results recorded before final audit:

- `git status --short` listed only the five approved S6 docs as intent-to-add files.
- `git diff --name-only | sort` listed exactly the five approved S6 docs.
- `git diff --check` passed with no output.
- Changed-file Python check printed `changed files ok`.
- Exact H1/H2 heading sequence check printed `heading structure ok`.
- Content invariant check printed `content invariants ok`.
- Coupling table minimum-row check printed `coupling IDs ok`.
- Readiness gate check printed `readiness gates ok`.
- Protected-path check produced no output.

Final current-state validation after self-review repair:

- `git status --short` listed only the five approved S6 docs as intent-to-add files.
- `git diff --name-only | sort` listed exactly the five approved S6 docs.
- `git diff --check` passed with no output.
- Changed-file Python check printed `changed files ok`.
- Exact H1/H2 heading sequence check printed `heading structure ok`.
- Content invariant check printed `content invariants ok`.
- Coupling table minimum-row check printed `coupling IDs ok`.
- Readiness gate check printed `readiness gates ok`.
- Protected-path check produced no output.
- Completion audit printed `artifact audit ok`.

S6 did not implement decoupling, create runtime adapter seams, create root `AGENTS.md`, create `.codex/`, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create migration scripts, inspect private user-local state, start Pulse, run installers, run Codex import or migration tooling, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, claim Codex is drop-in today, claim Codex is the official upstream engine, or advance beyond S6.
