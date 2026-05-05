# V5-S2 Execution Plan

## Purpose

Create a current, evidence-backed compatibility matrix between PAI v5.0.0 runtime surfaces and Codex-native surfaces.

S2 is a design and evidence milestone only. It does not implement a Codex adapter, create runtime adapter files, modify release files, modify protected runtime surfaces, or authorize runtime behavior.

## Scope

S2 is limited to:

- Collecting current Codex-native surface facts from official OpenAI Codex documentation.
- Reusing existing S0/S1 adapter evidence for PAI v5.0.0 facts.
- Producing an evidence document and compatibility matrix under `docs/adapters/`.
- Identifying compatibility status, gaps, risks, and future architect decisions.

S2 may not advance into adapter implementation, fixture harness creation, runtime configuration generation, installer design, Pulse bridge implementation, live PAI trials, or Codex migration/import work.

## Approved Write Set

Only these files may be created or modified during S2:

- `docs/adapters/V5_S2_EXEC_PLAN.md`
- `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`

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

## Source Material

Codex-native facts must come only from official OpenAI Codex documentation.

PAI v5 facts must come only from:

- `docs/adapters/V5_S0_DISCOVERY_PLAN.md`
- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`
- Existing S1 strategy docs under `docs/adapters/`
- Upstream release paths cited by S0

The OpenAI developer-docs MCP tooling was not available in this session, and installing it would modify Codex configuration. Because `.codex/` and user-local Codex state are protected for S2, official OpenAI web documentation is the approved fallback source for current Codex-native facts.

## Required Outputs

S2 must create:

- `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`
- `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`

The evidence document must cite official OpenAI Codex documentation for current Codex-native surface facts. The matrix must cite both Codex evidence and PAI S0/S1 evidence for each major compatibility judgment.

## Evidence Questions

S2 must answer:

- What current official OpenAI documentation says about Codex cloud tasks, CLI, IDE extension, local code access, environments, internet access, AGENTS.md, config, MCP, tools, approvals, sandboxing, exec behavior, patch edits, prompts, images, web search, multimodal input, task delegation, GitHub integration, reviews, and memory or goal-like persistence.
- Which PAI v5 surfaces have plausible native Codex counterparts.
- Which PAI v5 surfaces have partial counterparts requiring transformation.
- Which PAI v5 surfaces have no documented native Codex counterpart.
- Which gaps block replacement readiness.

## Compatibility Labels

Use these labels in the compatibility matrix:

- `native`: Codex has an official native surface that can plausibly carry the PAI responsibility, subject to later adapter tests.
- `partial`: Codex has an adjacent native surface, but behavior-preserving transformation or missing semantics remain.
- `gap`: official Codex docs do not document a native counterpart for the PAI surface.
- `blocked`: surface cannot be treated as compatible until an architect-approved gate is satisfied.
- `out-of-scope`: not evaluated in S2 because it would require implementation, private state, or non-official evidence.

No label authorizes implementation.

## Milestones

1. Create this execution plan first.
2. Collect official OpenAI Codex documentation evidence.
3. Draft `V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`.
4. Draft `V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`.
5. Self-review the evidence and matrix for source discipline, scope hygiene, and S2 boundaries.
6. Run validation commands.
7. Update this plan with final progress, validation, decisions, and retrospective.

## Self-Review Rubric

S2 passes only if:

- Exactly the three approved S2 files are created or modified.
- No protected path is modified.
- No runtime adapter files are created.
- No release files are modified.
- No `.codex/`, `.claude/`, `PAI/`, hooks, skills, agents, commands, settings, installer, prompt, or user-local state is read or modified.
- Codex-native facts cite official OpenAI Codex documentation.
- PAI facts cite S0/S1 evidence or S0-cited release paths.
- The matrix preserves the S1 conclusion that Codex is not currently proven drop-in for existing local PAI v5 files.
- The matrix does not claim Codex is the official upstream PAI engine.
- The matrix does not imply Claude-shaped files can be copied directly into Codex surfaces.
- The matrix does not authorize PAI Memory, ISA, Pulse, or settings writes.
- Open unknowns and unsupported surfaces are explicit.

## Hard Failure Conditions

Stop and report a blocker if S2 requires:

- Implementing a Codex adapter.
- Creating runtime adapter files.
- Modifying protected paths.
- Installing MCP tooling into `.codex/` or user-local Codex state.
- Running Codex import or migration tooling.
- Reading private user-local memory.
- Starting Pulse or invoking local Pulse endpoints.
- Using non-official OpenAI sources for Codex-native facts.
- Claiming undocumented Codex behavior as fact.

## Validation Commands

Run from repository root:

```bash
git status --short
git diff --name-only | sort
git diff --check
git status --short -- Releases/ .claude/ PAI/ CLAUDE.md AGENTS.md .codex/ install.sh settings.json hooks/ skills/ subagents/ agents/ commands/ .github/ .agents/
```

Run this changed-file check:

```bash
python3 - <<'PY'
import subprocess

expected = [
    "docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md",
    "docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md",
    "docs/adapters/V5_S2_EXEC_PLAN.md",
]

actual = sorted(subprocess.check_output(
    ["git", "diff", "--name-only"],
    text=True,
).splitlines())

if actual != expected:
    print("unexpected changed files")
    print("expected:")
    print("\n".join(expected))
    print("actual:")
    print("\n".join(actual))
    raise SystemExit(1)

print("changed files ok")
PY
```

## Progress

- Started the bounded S2 goal.
- Read current repository status.
- Read S0 and S1 evidence needed to define the S2 contract.
- Created this execution plan as the living self-evaluation contract.
- Collected official OpenAI Codex documentation evidence for native Codex surfaces.
- Created `docs/adapters/V5_CODEX_NATIVE_SURFACE_EVIDENCE.md`.
- Created `docs/adapters/V5_CODEX_PAI_COMPATIBILITY_MATRIX.md`.
- Marked the three approved S2 docs as intent-to-add so `git diff --name-only` validates the approved write set.
- Ran S2 validation commands and confirmed only the three approved S2 files are changed.

## Decision Log

- Use official OpenAI web documentation for Codex-native facts because installing the OpenAI docs MCP would modify protected Codex configuration.
- Treat S0/S1 docs as the PAI evidence baseline.
- Treat S2 as evidence and compatibility analysis only.
- Preserve S1 boundaries: Codex is not currently proven drop-in, Claude Code remains current official/full-support upstream engine, and future Codex replacement requires designed native surfaces.
- Treat Codex memories, local transcripts, SDK threads, and goal-like state as Codex product/session state, not PAI Memory, ISA, or Pulse state.
- Label Pulse, PAI Memory, ISA, single-writer behavior, existing local v5 writes, installer behavior, and rollback as blocked until architect-approved future gates exist.

## Outcomes & Retrospective

Created the S2 evidence and compatibility matrix as design-only documentation.

Validation results:

- `git status --short` listed only the three approved S2 docs as intent-to-add files.
- `git diff --name-only | sort` listed exactly the three approved S2 docs.
- `git diff --check` passed.
- The explicit changed-file Python check printed `changed files ok`.
- Protected-path status produced no output.

S2 did not implement a Codex adapter, create runtime adapter files, modify release files, modify protected runtime paths, inspect private user-local state, run Codex migration/import tooling, authorize PAI Memory writes, authorize Pulse implementation, or claim Codex is drop-in today.
