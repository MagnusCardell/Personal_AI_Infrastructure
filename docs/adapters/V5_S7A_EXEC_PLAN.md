# V5-S7A Execution Plan

## Purpose

Execute V5-S7A Authority Seam and Compact Router Design as a documentation-only architecture milestone for future PAI v5 Codex replacement-adapter work.

## Scope

S7A designs the authority seam, compact Codex router concept, authority envelope validation approach, and authority/router decision log.

S7A does not implement the adapter, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create runtime files, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, or run Codex import or migration tooling.

## Approved Write Set

Create exactly these files:

- `docs/adapters/V5_S7A_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_COMPACT_ROUTER_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_ENVELOPE_VALIDATION_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_ROUTER_DECISION_LOG.md`

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

1. S0-S6 adapter docs for prior adapter conclusions.
2. Repository-local PAI v5 release files for PAI facts.
3. Official OpenAI Codex docs for Codex authority, guidance, config, and sandbox facts if S7A adds or refreshes any Codex capability claim.
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
- `Releases/v5.0.0/`
- `Releases/v5.0.0/.claude/`

## Completion Contract

> This Completion Contract is the authoritative contract for V5-S7A.
>
> Before drafting the deliverables, copy this entire `## Completion Contract` section into `docs/adapters/V5_S7A_EXEC_PLAN.md`.
>
> Do not mark S7A complete unless every requirement below is satisfied.
>
> ### Strategic conclusions to preserve
>
> The S7A docs must preserve these conclusions:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * Codex replacement is plausible only through a designed adapter.
> * S7A designs authority and router seams only.
> * S7A does not implement authority injection.
> * S7A does not create root `AGENTS.md`.
> * S7A does not create `.codex/`.
> * S7A does not create Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, or runtime files.
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
> * Pulse remains central v5 infrastructure, but S7A does not design or implement a Pulse bridge.
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
> test -f Releases/v5.0.0/.claude/CLAUDE.md
> test -f Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md
> test -f docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md
> test -f docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md
>
> rg -n --hidden --glob '!**/.git/**' \
>   'PAI_SYSTEM_PROMPT|highest authority|high-authority|CLAUDE\.md|AGENTS\.md|PAI_DIR|append-system-prompt|system prompt|authority|instruction|router|compact router|Codex memory|PAI Memory|ISA|Pulse|goal|transcript|settings|config|sandbox|profile' \
>   Releases/v5.0.0 docs/adapters \
>   > /tmp/v5-s7a-authority-search.txt || true
>
> sed -n '1,240p' /tmp/v5-s7a-authority-search.txt
> ```
>
> Do not write `/tmp/v5-s7a-authority-search.txt` into the repository.
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
> ### Required file: `docs/adapters/V5_S7A_EXEC_PLAN.md`
>
> This file must be created first.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5-S7A Execution Plan
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
> 2. S0-S6 reread.
> 3. PAI authority evidence reread.
> 4. Official Codex authority/guidance evidence refresh if new Codex claims are needed.
> 5. Authority seam spec drafting.
> 6. Compact router spec drafting.
> 7. Authority envelope validation spec drafting.
> 8. Authority/router decision log drafting.
> 9. Self-review and repair.
> 10. Final handoff and goal-state report.
>
> The self-review rubric must total 100 points:
>
> | Area                                             | Points |
> | ------------------------------------------------ | -----: |
> | Scope and protected-path discipline              |     15 |
> | Evidence discipline                              |     15 |
> | PAI authority model accuracy                     |     20 |
> | Codex authority/guidance model accuracy          |     15 |
> | Compact router safety and minimality             |     15 |
> | Authority validation quality                     |     10 |
> | Existing-local-v5, memory, ISA, and Pulse safety |      5 |
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
> ### Required file: `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
>
> Purpose: define the future authority seam that preserves PAI v5 authority semantics inside a Codex-native runtime without copying Claude-shaped files into Codex surfaces.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Authority Seam Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Authority Problem Statement
> ## PAI Authority Model
> ## Codex Authority and Guidance Model
> ## Non-Equivalent Surfaces
> ## Authority Seam Principles
> ## Authority Envelope Model
> ## Authority Source Classes
> ## Authority Ordering Rules
> ## Conflict Resolution Rules
> ## Truncation and Size Risk Model
> ## Memory and Goal Non-Authority Rules
> ## Pulse and ISA Boundary Rules
> ## Existing Local v5 Authority Safety
> ## Candidate Authority Seam Designs
> ## Required Future Proofs
> ## Prohibited Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * Define `PAI_SYSTEM_PROMPT.md` as high-authority upstream PAI doctrine.
> * Define `CLAUDE.md` as Claude-facing operational guidance, not a Codex destination file.
> * Define Codex `AGENTS.md` as a future compact router candidate only.
> * Define Codex config/profile as policy/config, not Life OS doctrine.
> * Define Codex memory as local recall, not doctrine.
> * Define `/goal` state as workflow-control state, not ISA and not PAI Memory.
> * Define transcripts and SDK threads as non-authority and non-PAI state.
> * Define a future authority envelope model that preserves:
>
>   * PAI doctrine priority;
>   * operational routing;
>   * explicit unsupported-surface reporting;
>   * no silent promotion of memory;
>   * no direct clone of Claude-shaped files;
>   * no release-file mutation.
> * Include at least three candidate authority seam designs:
>
>   * `AS-1`: Compact router plus read-only doctrine references.
>   * `AS-2`: Generated authority envelope for explicit trial sessions.
>   * `AS-3`: Future launcher/profile-mediated authority envelope.
> * For each candidate, include:
>
>   * `Candidate`
>   * `Summary`
>   * `Inputs`
>   * `Outputs`
>   * `Safety`
>   * `Reversibility`
>   * `Drop-in readiness`
>   * `Authority loss risk`
>   * `Required future proofs`
>   * `S7A decision`
> * State that S7A chooses no runtime implementation.
>
> ### Required file: `docs/adapters/V5_CODEX_COMPACT_ROUTER_SPEC.md`
>
> Purpose: specify the future compact Codex router concept without creating root `AGENTS.md` or any Codex runtime guidance file.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Compact Router Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Router Problem Statement
> ## Router Non-Goals
> ## Router Design Principles
> ## Future Router Placement Options
> ## Router Content Model
> ## Router Exclusion Model
> ## Router Reference Model
> ## Router Safety Requirements
> ## Router Size and Truncation Policy
> ## Router Interaction With Codex Config
> ## Router Interaction With Codex Memory
> ## Router Interaction With Goal State
> ## Router Interaction With PAI Memory and ISA
> ## Router Interaction With Pulse
> ## Example Non-Executable Router Skeleton
> ## Router Validation Requirements
> ## Prohibited Router Designs
> ## Non-Goals
> ```
>
> Required content:
>
> * State that S7A does not create `AGENTS.md`.
> * State that root `AGENTS.md` remains repo-maintainer governance unless later explicitly authorized.
> * State that `.codex/` remains protected and is not created in S7A.
> * Define future router placement options as design candidates only:
>
>   * root `AGENTS.md` as repo-level guidance, if maintainer-authorized;
>   * nested adapter-local guidance, if future layout authorizes it;
>   * future launcher-mediated instructions, if supported and tested;
>   * no-router mode for evidence-only trial.
> * Define compact router content categories:
>
>   * PAI role statement;
>   * PAI doctrine reference;
>   * `PAI_DIR` resolution rule;
>   * read-only trial posture;
>   * protected path summary;
>   * unsupported-surface reporting;
>   * handoff/audit behavior;
>   * escalation-to-architect rule.
> * Define router exclusions:
>
>   * no full `PAI_SYSTEM_PROMPT.md`;
>   * no full `CLAUDE.md`;
>   * no Claude hook code;
>   * no Claude settings JSON;
>   * no Claude skill, agent, or command copy;
>   * no product memory content;
>   * no ISA acceptance logic;
>   * no Pulse bridge claim.
> * Include one non-executable router skeleton in markdown prose or fenced text.
> * The skeleton must be explicitly labeled:
>
>   * `NON-EXECUTABLE DESIGN SKETCH — DO NOT INSTALL`
> * Do not create any actual router file.
>
> ### Required file: `docs/adapters/V5_CODEX_AUTHORITY_ENVELOPE_VALIDATION_SPEC.md`
>
> Purpose: define future validation cases for proving that a Codex authority envelope and compact router preserve PAI authority semantics before any runtime trial.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Authority Envelope Validation Spec
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Validation Philosophy
> ## Test Case Model
> ## Authority Priority Tests
> ## Router Minimality Tests
> ## Direct-Copy Prohibition Tests
> ## Instruction Ordering Tests
> ## Instruction Size and Truncation Tests
> ## Conflict Resolution Tests
> ## Memory Non-Authority Tests
> ## Goal and ISA Separation Tests
> ## PAI Memory Write Prohibition Tests
> ## Pulse Non-Implementation Tests
> ## Existing Local v5 Safety Tests
> ## Pass and Fail Criteria
> ## Evidence Required Before Implementation
> ## Future Implementation Gates
> ## Non-Goals
> ```
>
> Required content:
>
> * Define authority validation as future behavioral proof, not S7A execution.
> * State that copying `PAI_SYSTEM_PROMPT.md` or `CLAUDE.md` does not prove authority equivalence.
> * Define test cases for:
>
>   * `PAI_SYSTEM_PROMPT.md` priority;
>   * `CLAUDE.md` not being copied;
>   * compact router minimality;
>   * router references not becoming unbounded doctrine dumps;
>   * instruction ordering;
>   * instruction size/truncation;
>   * conflict between PAI doctrine and Codex memory;
>   * conflict between PAI doctrine and `/goal` state;
>   * `/goal` not being ISA;
>   * Codex memory not being PAI Memory;
>   * no PAI Memory writes;
>   * no ISA writes;
>   * no Pulse implementation or parity claim;
>   * no existing-local-v5 trial execution.
> * Include a table with columns:
>
>   * `Test ID`
>   * `Test area`
>   * `Input condition`
>   * `Expected behavior`
>   * `Failure signal`
>   * `Required future evidence`
>   * `S7A status`
> * Include at least these test IDs:
>
>   * `AV-001`
>   * `AV-002`
>   * `AV-003`
>   * `AV-004`
>   * `AV-005`
>   * `AV-006`
>   * `AV-007`
>   * `AV-008`
>   * `AV-009`
>   * `AV-010`
>   * `AV-011`
>   * `AV-012`
>
> ### Required file: `docs/adapters/V5_CODEX_AUTHORITY_ROUTER_DECISION_LOG.md`
>
> Purpose: record S7A decisions, non-decisions, blocked decisions, and future architect questions for the authority seam and compact router.
>
> It must contain exactly these H1/H2 headings:
>
> ```markdown
> # V5 Codex Authority Router Decision Log
> ## Purpose
> ## Scope
> ## Evidence Base
> ## Decisions Made in S7A
> ## Non-Decisions in S7A
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
> * `S7A-D01`: Codex remains not drop-in today.
> * `S7A-D02`: Authority seam must precede any router file creation.
> * `S7A-D03`: Future router must be compact and must not clone `CLAUDE.md`.
> * `S7A-D04`: `PAI_SYSTEM_PROMPT.md` must remain high-authority doctrine.
> * `S7A-D05`: Codex memory is not doctrine and not PAI Memory.
> * `S7A-D06`: `/goal` state is not ISA and not PAI Memory.
> * `S7A-D07`: Root `AGENTS.md` remains protected in S7A.
> * `S7A-D08`: `.codex/` remains protected in S7A.
> * `S7A-D09`: S7A creates no runtime authority material.
> * `S7A-D10`: Future authority validation must pass before read-only trial execution.
> * `S7A-D11`: Pulse bridge remains out of S7A scope.
> * `S7A-D12`: PAI Memory/ISA writes remain blocked.
>
> The `## Next Milestone Candidates` section must list advisory-only options, not approvals:
>
> * `V5-S7B`: Fixture-only coupling validation harness design.
> * `V5-S7C`: Launcher and inference seam design.
> * `V5-S7D`: Hook/lifecycle mapping design.
> * `V5-S7E`: Pulse bridge identity and read-only event model.
> * `V5-S8A`: First non-runtime router fixture proposal, if authority validation design is accepted.
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
> S7A fails immediately if:
>
> * Any file outside the approved write set is created or modified.
> * Any protected file is modified.
> * Runtime adapter files are created.
> * Root `AGENTS.md` is created or modified.
> * `.codex/` is created or modified.
> * Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, or migration scripts are created.
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
> * The docs propose installing the non-executable router skeleton.
> * The goal advances beyond S7A.
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
>     "docs/adapters/V5_CODEX_AUTHORITY_ENVELOPE_VALIDATION_SPEC.md",
>     "docs/adapters/V5_CODEX_AUTHORITY_ROUTER_DECISION_LOG.md",
>     "docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md",
>     "docs/adapters/V5_CODEX_COMPACT_ROUTER_SPEC.md",
>     "docs/adapters/V5_S7A_EXEC_PLAN.md",
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
>     "docs/adapters/V5_S7A_EXEC_PLAN.md": [
>         "# V5-S7A Execution Plan",
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
>     "docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md": [
>         "# V5 Codex Authority Seam Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Authority Problem Statement",
>         "## PAI Authority Model",
>         "## Codex Authority and Guidance Model",
>         "## Non-Equivalent Surfaces",
>         "## Authority Seam Principles",
>         "## Authority Envelope Model",
>         "## Authority Source Classes",
>         "## Authority Ordering Rules",
>         "## Conflict Resolution Rules",
>         "## Truncation and Size Risk Model",
>         "## Memory and Goal Non-Authority Rules",
>         "## Pulse and ISA Boundary Rules",
>         "## Existing Local v5 Authority Safety",
>         "## Candidate Authority Seam Designs",
>         "## Required Future Proofs",
>         "## Prohibited Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_COMPACT_ROUTER_SPEC.md": [
>         "# V5 Codex Compact Router Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Router Problem Statement",
>         "## Router Non-Goals",
>         "## Router Design Principles",
>         "## Future Router Placement Options",
>         "## Router Content Model",
>         "## Router Exclusion Model",
>         "## Router Reference Model",
>         "## Router Safety Requirements",
>         "## Router Size and Truncation Policy",
>         "## Router Interaction With Codex Config",
>         "## Router Interaction With Codex Memory",
>         "## Router Interaction With Goal State",
>         "## Router Interaction With PAI Memory and ISA",
>         "## Router Interaction With Pulse",
>         "## Example Non-Executable Router Skeleton",
>         "## Router Validation Requirements",
>         "## Prohibited Router Designs",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_AUTHORITY_ENVELOPE_VALIDATION_SPEC.md": [
>         "# V5 Codex Authority Envelope Validation Spec",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Validation Philosophy",
>         "## Test Case Model",
>         "## Authority Priority Tests",
>         "## Router Minimality Tests",
>         "## Direct-Copy Prohibition Tests",
>         "## Instruction Ordering Tests",
>         "## Instruction Size and Truncation Tests",
>         "## Conflict Resolution Tests",
>         "## Memory Non-Authority Tests",
>         "## Goal and ISA Separation Tests",
>         "## PAI Memory Write Prohibition Tests",
>         "## Pulse Non-Implementation Tests",
>         "## Existing Local v5 Safety Tests",
>         "## Pass and Fail Criteria",
>         "## Evidence Required Before Implementation",
>         "## Future Implementation Gates",
>         "## Non-Goals",
>     ],
>     "docs/adapters/V5_CODEX_AUTHORITY_ROUTER_DECISION_LOG.md": [
>         "# V5 Codex Authority Router Decision Log",
>         "## Purpose",
>         "## Scope",
>         "## Evidence Base",
>         "## Decisions Made in S7A",
>         "## Non-Decisions in S7A",
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
>         "docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md",
>         "docs/adapters/V5_CODEX_COMPACT_ROUTER_SPEC.md",
>         "docs/adapters/V5_CODEX_AUTHORITY_ENVELOPE_VALIDATION_SPEC.md",
>         "docs/adapters/V5_CODEX_AUTHORITY_ROUTER_DECISION_LOG.md",
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
>     "authority seam",
>     "Codex config",
>     "Codex memory",
>     "/goal",
>     "not PAI Memory",
>     "PAI Memory",
>     "ISA",
>     "Pulse",
>     "single-writer",
>     "read-only",
>     "reversible",
>     "NON-EXECUTABLE DESIGN SKETCH — DO NOT INSTALL",
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
> Run authority candidate check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md").read_text(encoding="utf-8")
>
> required_ids = ["AS-1", "AS-2", "AS-3"]
>
> missing = [rid for rid in required_ids if rid not in text]
>
> if missing:
>     print("missing authority seam candidates:")
>     for rid in missing:
>         print(f"- {rid}")
>     raise SystemExit(1)
>
> print("authority seam candidates ok")
> PY
> ```
>
> Run validation test ID check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_AUTHORITY_ENVELOPE_VALIDATION_SPEC.md").read_text(encoding="utf-8")
>
> required_ids = [
>     "AV-001",
>     "AV-002",
>     "AV-003",
>     "AV-004",
>     "AV-005",
>     "AV-006",
>     "AV-007",
>     "AV-008",
>     "AV-009",
>     "AV-010",
>     "AV-011",
>     "AV-012",
> ]
>
> missing = [rid for rid in required_ids if rid not in text]
>
> if missing:
>     print("missing validation test IDs:")
>     for rid in missing:
>         print(f"- {rid}")
>     raise SystemExit(1)
>
> print("authority validation test IDs ok")
> PY
> ```
>
> Run decision ID check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
>
> text = Path("docs/adapters/V5_CODEX_AUTHORITY_ROUTER_DECISION_LOG.md").read_text(encoding="utf-8")
>
> required_ids = [
>     "S7A-D01",
>     "S7A-D02",
>     "S7A-D03",
>     "S7A-D04",
>     "S7A-D05",
>     "S7A-D06",
>     "S7A-D07",
>     "S7A-D08",
>     "S7A-D09",
>     "S7A-D10",
>     "S7A-D11",
>     "S7A-D12",
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
> S7A is complete only if:
>
> * Exactly the five approved S7A files are created or modified.
> * No protected files are changed.
> * No runtime adapter files are created.
> * No root `AGENTS.md` is created or modified.
> * No `.codex/` files are created or modified.
> * No Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, or migration scripts are created.
> * No user-local state is inspected or modified.
> * Pulse is not started.
> * Installers are not run.
> * Codex import/migration tooling is not run.
> * `V5_S7A_EXEC_PLAN.md` contains the Completion Contract copied into its `## Completion Contract` section.
> * The authority seam spec includes candidate designs `AS-1`, `AS-2`, and `AS-3`.
> * The compact router spec includes the non-executable router skeleton and clearly says not to install it.
> * The authority validation spec includes all required `AV-001` through `AV-012` test IDs.
> * The decision log includes all required `S7A-D01` through `S7A-D12` decisions.
> * The docs do not claim Codex is drop-in today.
> * The docs do not claim Codex is the official upstream engine.
> * The docs do not authorize PAI Memory writes.
> * The docs do not authorize ISA writes.
> * The docs do not authorize Pulse implementation.
> * The docs do not authorize existing-local-v5 trial execution.
> * The docs do not imply Claude-shaped files can be copied directly into Codex surfaces.
> * The docs do not propose installing the non-executable router skeleton.
> * The execution plan records at least one scored self-review iteration with score at least 94/100 and zero hard failures.
> * Changed-file check passes.
> * Heading sequence check passes.
> * Content invariant check passes.
> * Authority candidate check passes.
> * Validation test ID check passes.
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
> No — only the five approved S7A docs were created or modified.
> ```
>
> `Recommended next architect decision` must be advisory only. Do not begin S7B, S7C, S7D, S7E, or S8.
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
> * Upstream v5 would need to be patched.
> * Private user-local memory would need to be read.
> * Codex import/migration tooling seems necessary.
> * Pulse would need to be started.
> * The goal tries to continue beyond S7A.
> * The Completion Contract cannot be copied into the execution plan.
> * The self-review cannot reach 94/100 without leaving scope.

## Milestones

1. Baseline status check.
2. S0-S6 reread.
3. PAI authority evidence reread.
4. Official Codex authority/guidance evidence refresh if new Codex claims are needed.
5. Authority seam spec drafting.
6. Compact router spec drafting.
7. Authority envelope validation spec drafting.
8. Authority/router decision log drafting.
9. Self-review and repair.
10. Final handoff and goal-state report.

## Self-Review Rubric

| Area | Points |
| --- | ---: |
| Scope and protected-path discipline | 15 |
| Evidence discipline | 15 |
| PAI authority model accuracy | 20 |
| Codex authority/guidance model accuracy | 15 |
| Compact router safety and minimality | 15 |
| Authority validation quality | 10 |
| Existing-local-v5, memory, ISA, and Pulse safety | 5 |
| Verification quality | 5 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

S7A fails immediately if:

- Any file outside the approved write set is created or modified.
- Any protected file is modified.
- Runtime adapter files are created.
- Root `AGENTS.md` is created or modified.
- `.codex/` is created or modified.
- Codex config, hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, fixtures, harnesses, executable schemas, manifests, audit artifacts, generated configs, or migration scripts are created.
- User-local private state is inspected or modified.
- Pulse is started.
- Installers are run.
- Codex import or migration tooling is run.
- The docs claim Codex is drop-in today.
- The docs claim Codex is the official upstream engine.
- The docs authorize PAI Memory writes.
- The docs authorize ISA writes.
- The docs authorize Pulse implementation.
- The docs authorize existing-local-v5 trial execution.
- The docs imply Claude-shaped files can be copied directly into Codex surfaces.
- The docs propose installing the non-executable router skeleton.
- The goal advances beyond S7A.

## Validation Commands

Required validation commands:

- `git status --short`
- `git diff --name-only | sort`
- `git diff --check`
- Changed-file Python check.
- Exact H1/H2 heading sequence check.
- Content invariant check.
- Authority candidate check.
- Validation test ID check.
- Decision ID check.
- Protected-path check.

## Progress

- Started the bounded V5-S7A goal.
- Confirmed the baseline worktree was clean before S7A edits.
- Created this execution plan first.
- Copied the Completion Contract into this execution plan before drafting other S7A deliverables.
- Ran required local discovery commands:
  - `git status --short` returned no output before S7A edits.
  - `test -f Releases/v5.0.0/.claude/CLAUDE.md` passed.
  - `test -f Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md` passed.
  - `test -f docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md` passed.
  - `test -f docs/adapters/V5_CODEX_DECOUPLING_SEAM_SPEC.md` passed.
  - Required `rg` authority search wrote to `/tmp/v5-s7a-authority-search.txt` only.
  - `sed -n '1,240p' /tmp/v5-s7a-authority-search.txt` printed the required search excerpt.
- Reread S0-S6 adapter authority evidence and targeted repository-local v5 release authority files.
- Did not refresh official Codex docs because S7A introduced no new Codex capability claim beyond S2/S3 official-source evidence.
- Created `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`.
- Created `docs/adapters/V5_CODEX_COMPACT_ROUTER_SPEC.md`.
- Created `docs/adapters/V5_CODEX_AUTHORITY_ENVELOPE_VALIDATION_SPEC.md`.
- Created `docs/adapters/V5_CODEX_AUTHORITY_ROUTER_DECISION_LOG.md`.
- Marked the five S7A docs as intent-to-add so `git diff --name-only`, `git diff --check`, and changed-file validation inspect the new docs.
- Ran validation checks and performed no repair outside the approved S7A write set.

## Iteration Log

| Iteration | Scope discipline | Evidence discipline | PAI authority accuracy | Codex authority accuracy | Router safety | Validation quality | Safety | Verification | Total | Hard failures | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| S7A-I0 initial plan | 15 | 10 | 0 | 0 | 0 | 0 | 5 | 1 | 31/100 | 0 | Execution plan created; deliverables not yet drafted. |
| S7A-I1 validation pass | 15 | 15 | 20 | 15 | 15 | 10 | 5 | 5 | 100/100 | 0 | All required S7A docs drafted, required candidates and IDs present, validation commands passed before final execution-plan update. |

S7A-I1 pass threshold record: 100/100 with 0 hard failures and zero hard failures.

## Surprises & Discoveries

- S3 already captured the needed official Codex authority and guidance facts, so S7A could avoid refreshing official Codex documentation and avoid adding new Codex capability claims.
- `PAI_SYSTEM_PROMPT.md` explicitly frames itself as the highest authority layer, while `CLAUDE.md` routes operational context and templates; this reinforces that the future compact router cannot be a file copy.
- S6's dependency graph correctly places authority before router, which became the main S7A design constraint.

## Decision Log

- S7A will use S0-S6 adapter docs and repository-local v5 release evidence.
- S7A will use official OpenAI Codex docs only if a new or refreshed Codex capability claim is needed.
- S7A will not inspect private user-local state.
- S7A will not create runtime authority material.
- S7A will not create root `AGENTS.md` or `.codex/`.
- Codex remains not drop-in today.
- Authority seam must precede any router file creation.
- Future router must be compact and must not clone `CLAUDE.md` or `PAI_SYSTEM_PROMPT.md`.
- Codex config/profile is policy/configuration, not Life OS doctrine.
- Codex memory and `/goal` state are not PAI Memory or ISA.
- Pulse bridge remains out of S7A scope.
- PAI Memory and ISA writes remain blocked.
- Future authority validation must pass before read-only trial execution.

## Outcomes & Retrospective

S7A produced the five approved documentation artifacts only:

- `docs/adapters/V5_S7A_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_AUTHORITY_SEAM_SPEC.md`
- `docs/adapters/V5_CODEX_COMPACT_ROUTER_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_ENVELOPE_VALIDATION_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_ROUTER_DECISION_LOG.md`

Validation results recorded before final audit:

- `git status --short` listed only the five approved S7A docs as intent-to-add files.
- `git diff --name-only | sort` listed exactly the five approved S7A docs.
- `git diff --check` passed with no output.
- Changed-file Python check printed `changed files ok`.
- Exact H1/H2 heading sequence check printed `heading structure ok`.
- Content invariant check printed `content invariants ok`.
- Authority candidate check printed `authority seam candidates ok`.
- Validation test ID check printed `authority validation test IDs ok`.
- Decision ID check printed `decision IDs ok`.
- Protected-path check produced no output.

Final current-state validation after execution-plan result recording:

- `git status --short` listed only the five approved S7A docs as intent-to-add files.
- `git diff --name-only | sort` listed exactly the five approved S7A docs.
- `git diff --check` passed with no output.
- Changed-file Python check printed `changed files ok`.
- Exact H1/H2 heading sequence check printed `heading structure ok`.
- Content invariant check printed `content invariants ok`.
- Authority candidate check printed `authority seam candidates ok`.
- Validation test ID check printed `authority validation test IDs ok`.
- Decision ID check printed `decision IDs ok`.
- Protected-path check produced no output.

S7A did not implement the adapter, create root `AGENTS.md`, create `.codex/`, create Codex config, create hooks, create rules, create skills, create subagents, create agents, create commands, create launchers, create installers, create wrappers, create fixtures, create harnesses, create executable schemas, create manifests, create audit artifacts, create generated configs, create runtime files, run a read-only trial, inspect private user-local state, modify release files, start Pulse, run installers, run Codex import or migration tooling, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, claim Codex is drop-in today, claim Codex is the official upstream engine, propose installing the non-executable router skeleton, or advance beyond S7A.
