# V5-S5 Execution Plan

## Purpose

Define implementation-neutral schema proposals and dry-run validation design for the future PAI v5 Codex read-only trial manifest and audit output.

S5 is a design milestone only. It does not create executable schema files, JSON, YAML, TOML, generated config, fixture material, manifest instances, audit artifacts, validators, test harnesses, launchers, installers, wrappers, root `AGENTS.md`, `.codex/`, hooks, rules, skills, subagents, agents, commands, or runtime adapter files.

## Scope

S5 is limited to non-executable markdown proposals for:

- Future read-only trial manifest schema shape.
- Future read-only trial audit output schema shape.
- Future dry-run validation design for those schemas.

S5 does not run a read-only trial, inspect or modify private user-local state, modify release files, start Pulse, run installers, run Codex import or migration tooling, implement runtime adapter surfaces, or advance beyond S5.

## Approved Write Set

Only these files may be created or modified during S5:

- `docs/adapters/V5_S5_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_TRIAL_MANIFEST_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_SCHEMA_DRY_RUN_VALIDATION_SPEC.md`

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

Protected user-local paths:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`

## Source Protocol

Use S0/S1/S2/S3/S4 adapter docs as the main evidence base.

Use read-only PAI v5 release evidence only for targeted facts already relevant to S5.

Use official OpenAI Codex documentation only if a new current Codex capability claim is needed. S5 is expected to require no new Codex capability claims beyond S2/S3/S4.

Keep all schema material in markdown tables and prose. Do not create executable schema files or literal JSON, YAML, or TOML artifacts.

## Source Material

Primary S4 contract sources:

- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_MANIFEST_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_OUTPUT_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_FIXTURE_AND_PATH_MODEL_SPEC.md`
- `docs/adapters/V5_CODEX_AUTHORITY_EQUIVALENCE_TEST_SPEC.md`
- `docs/adapters/V5_S4_EXEC_PLAN.md`

Supporting adapter sources:

- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- `docs/adapters/V5_ADAPTER_BOUNDARIES.md`
- `docs/adapters/V5_CODEX_RUNTIME_STRATEGY.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`
- `docs/adapters/V5_CODEX_AUTHORITY_MAPPING_SPEC.md`
- `docs/adapters/V5_CODEX_READ_ONLY_TRIAL_SPEC.md`

Required S5 outputs:

- `docs/adapters/V5_CODEX_TRIAL_MANIFEST_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_SCHEMA_DRY_RUN_VALIDATION_SPEC.md`

The outputs must remain markdown proposals, not executable schemas or validators.

## Milestones

1. Create this execution plan first.
2. Read S4 contracts needed for schema proposal derivation.
3. Draft the manifest schema proposal.
4. Draft the audit schema proposal.
5. Draft the dry-run validation design.
6. Self-review against S5 boundaries.
7. Run validation commands.
8. Update this plan with progress, decisions, and outcomes.

## Self-Review Rubric

S5 passes only if:

- Exactly the four approved S5 files are created or modified.
- No protected path is modified.
- No executable schema file is created.
- No JSON, YAML, TOML, generated config, fixture, manifest instance, audit artifact, validator, test harness, launcher, installer, wrapper, root `AGENTS.md`, `.codex/`, hook, rule, skill, subagent, agent, command, or runtime adapter file is created.
- No read-only trial is run.
- No private user-local state is inspected or modified.
- No release file is modified.
- Pulse is not started.
- Installers are not run.
- Codex import or migration tooling is not run.
- The docs preserve that Codex is not currently proven drop-in for existing local PAI v5 files.
- The docs preserve that Claude Code remains the current official/full-support upstream engine until replacement-grade validation exists.
- The docs preserve that `PAI_SYSTEM_PROMPT.md` is high-authority PAI doctrine.
- The docs preserve that PAI Memory and ISA artifacts are canonical PAI state.
- The docs preserve that Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.
- The docs do not authorize PAI Memory writes, ISA writes, Pulse implementation, or existing-local-v5 trial execution.

## Hard Failure Conditions

Stop and report a blocker if S5 requires:

- Creating executable schema files.
- Creating JSON, YAML, TOML, generated config, fixture material, manifest instances, audit artifacts, validators, or test harnesses.
- Running a read-only trial.
- Implementing a Codex adapter.
- Creating runtime adapter surfaces.
- Creating root `AGENTS.md`.
- Creating `.codex/`.
- Modifying protected paths.
- Inspecting private user-local state.
- Starting Pulse.
- Running installers.
- Running Codex import or migration tooling.
- Claiming Codex drop-in compatibility.
- Claiming Codex is the official upstream PAI engine.
- Authorizing PAI Memory writes, ISA writes, Pulse implementation, or existing-local-v5 trial execution.

## Validation Commands

Run from repository root:

```bash
git status --short
git diff --name-only | sort
git diff --check
```

Run a changed-file check expecting exactly:

- `docs/adapters/V5_CODEX_SCHEMA_DRY_RUN_VALIDATION_SPEC.md`
- `docs/adapters/V5_CODEX_TRIAL_AUDIT_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_CODEX_TRIAL_MANIFEST_SCHEMA_PROPOSAL.md`
- `docs/adapters/V5_S5_EXEC_PLAN.md`

Run protected-path check:

```bash
git status --short -- Releases/ .claude/ PAI/ CLAUDE.md AGENTS.md .codex/ install.sh settings.json hooks/ skills/ subagents/ agents/ commands/ .github/ .agents/
```

Expected protected-path result: no output.

## Progress

- Started the bounded S5 goal.
- Confirmed the repository was clean before S5 edits.
- Created this execution plan as the first S5 file and living self-evaluation contract.
- Read S4 manifest, audit, fixture/path, and authority-equivalence contracts.
- Determined no new Codex capability claims were needed beyond S2/S3/S4, so no new OpenAI documentation lookup was required.
- Created `docs/adapters/V5_CODEX_TRIAL_MANIFEST_SCHEMA_PROPOSAL.md`.
- Created `docs/adapters/V5_CODEX_TRIAL_AUDIT_SCHEMA_PROPOSAL.md`.
- Created `docs/adapters/V5_CODEX_SCHEMA_DRY_RUN_VALIDATION_SPEC.md`.
- Marked the four approved S5 docs as intent-to-add so `git diff --name-only` validates the approved write set.
- Ran S5 validation commands and confirmed only the four approved S5 files are changed.

## Iteration Log

- Original S5 created the schema proposal set as design-only markdown.
- S5R normalized the existing S5 markdown artifacts without starting a new `/goal`.
- S5R converted extra H2 headings into required sections, tables, lists, labels, or prose.

## Surprises & Discoveries

- No new source evidence was needed for S5R.
- No new Codex capability claims were needed for S5R.
- The existing S5 content was scope-safe and required structural normalization rather than architecture expansion.

## Decision Log

- Keep S5 schema work as markdown-only proposals.
- Do not create executable schema files or literal data artifacts.
- Treat S4 manifest, fixture/path, authority-equivalence, and audit-output specs as the canonical S5 input contracts.
- Avoid new OpenAI documentation lookup unless a new Codex capability claim becomes necessary.
- Represent schema shape as field tables, value domains, and cross-field rules rather than JSON, YAML, TOML, or executable schema syntax.
- Treat dry-run validation as design review only; no validator, parser, fixture, manifest instance, audit artifact, or test harness is created.

## Outcomes & Retrospective

Created the S5 manifest schema proposal, audit schema proposal, and dry-run validation spec as implementation-neutral markdown documentation.

Validation results:

- `git status --short` listed only the four approved S5 docs as intent-to-add files.
- `git diff --name-only | sort` listed exactly the four approved S5 docs.
- `git diff --check` passed.
- The explicit changed-file Python check printed `changed files ok`.
- The content/scope invariant check printed `content/scope invariants ok`.
- Protected-path status produced no output.

S5 did not create executable schema files, JSON, YAML, TOML, generated config, fixtures, manifest instances, audit artifacts, validators, test harnesses, launchers, installers, wrappers, root `AGENTS.md`, `.codex/`, hooks, rules, skills, subagents, agents, commands, or runtime adapter files. S5 did not run a read-only trial, inspect or modify private user-local state, modify release files, start Pulse, run installers, run Codex import or migration tooling, authorize PAI Memory writes, authorize ISA writes, authorize Pulse implementation, authorize existing-local-v5 trial execution, or advance beyond S5.
