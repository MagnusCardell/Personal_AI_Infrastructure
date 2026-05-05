# V5-S0 Discovery Plan

## Purpose

Create a read-only S0 evidence baseline for adapting PAI v5.0.0 so Codex can later be evaluated as a user-selectable local PAI runtime engine candidate.

This plan is only for S0 discovery. It is not an implementation plan, not a migration plan, and not a continuation of older pre-v5 adapter work.

## Scope

- Canonical target: `Releases/v5.0.0/`.
- Primary upstream baseline: `Releases/v5.0.0/.claude/`.
- Allowed supporting docs: repository release README files and adapter docs if present.
- Explicitly out of scope: installers, Pulse startup, dependency installation, Claude Code invocation, Codex migration/import tooling, runtime adapter files, release edits, root `AGENTS.md` edits, `.codex/` reads or writes, and user-local private state.

## Approved Files

Only these repository files may be created or modified:

- `docs/adapters/V5_S0_DISCOVERY_PLAN.md`
- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`

The `docs/` and `docs/adapters/` directories were absent at baseline, so the path parent directory had to be created to hold the two required files.

## Protected Files

Protected from modification during S0:

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

## Discovery Steps

1. Run required baseline state commands from repository root.
2. Confirm `Releases/v5.0.0/.claude` exists and probe the v5 README.
3. Generate v5 release file listings and the `/tmp/pai-v5-files.txt` manifest.
4. Run the required broad `rg` evidence search across `Releases/v5.0.0`.
5. Inspect key v5 authority and runtime files without executing installers or daemons.
6. Separate Claude-specific runtime surfaces from engine-neutral PAI doctrine and state.
7. Write the S0 report with path-cited evidence and explicit Codex drop-in assessment.
8. Run final changed-file, diff, and protected-path verification.

## Evidence Log

Baseline commands run:

- `git status --short`
- `test -d Releases/v5.0.0/.claude`
- `test -f Releases/v5.0.0/README.md || true`
- `find Releases/v5.0.0 -maxdepth 4 -type f | sort | sed -n '1,300p'`
- `find Releases/v5.0.0/.claude -maxdepth 5 -type f | sort > /tmp/pai-v5-files.txt`
- `sed -n '1,300p' /tmp/pai-v5-files.txt`
- Required broad `rg` search over `Releases/v5.0.0`
- `git diff --name-only`
- `git diff --check`
- Protected-path `git status --short -- ...`

Primary files inspected:

- `Releases/v5.0.0/README.md`
- `Releases/v5.0.0/.claude/README.md`
- `Releases/v5.0.0/.claude/CLAUDE.md`
- `Releases/v5.0.0/.claude/settings.json`
- `Releases/v5.0.0/.claude/install.sh`
- `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md`
- `Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts`
- `Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/PAISystemArchitecture.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/ARCHITECTURE_SUMMARY.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Algorithm/AlgorithmSystem.md`
- `Releases/v5.0.0/.claude/PAI/ALGORITHM/v6.3.0.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Isa/IsaSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md`
- `Releases/v5.0.0/.claude/skills/ISA/SKILL.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md`
- `Releases/v5.0.0/.claude/PAI/MEMORY/README.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Observability/ObservabilitySystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Tools/CliFirstArchitecture.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Tools/Tools.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Config/ConfigSystem.md`
- `Releases/v5.0.0/.claude/hooks/README.md`
- `Releases/v5.0.0/.claude/hooks/LoadContext.hook.ts`
- `Releases/v5.0.0/.claude/hooks/PromptProcessing.hook.ts`
- `Releases/v5.0.0/.claude/hooks/lib/paths.ts`
- `Releases/v5.0.0/.claude/PAI/PAI-Install/README.md`
- `Releases/v5.0.0/.claude/PAI/PAI-Install/engine/actions.ts`
- `Releases/v5.0.0/.claude/PAI/PAI-Install/engine/config-gen.ts`
- `Releases/v5.0.0/.claude/PAI/PAI-Install/engine/detect.ts`
- `Releases/v5.0.0/.claude/agents/Engineer.md`
- `Releases/v5.0.0/.claude/commands/context-search.md`

## Completion Criteria

- Exactly the two required docs exist.
- No release, root agent, `.claude`, `PAI`, `.codex`, hook, skill, settings, prompt, or installer files are modified.
- The report cites repository evidence by path.
- The report explicitly answers the S0 questions.
- Codex drop-in status, existing-local-v5 implications, and dual-memory implications are explicit.
- Final protected-path verification lists no protected files.

## Stop Conditions

Stop immediately if discovery requires any of the following:

- Reading user-local private state such as `~/.claude/`, `~/.codex/`, or `~/.codex/memories/`.
- Starting Pulse or invoking a local dashboard endpoint.
- Running installers or installing dependencies.
- Invoking Claude Code.
- Invoking Codex import or migration tooling.
- Creating runtime adapter files.
- Modifying release files, protected root files, `.claude/`, `PAI/`, `.codex/`, hooks, skills, or settings.

## Progress

- Completed required baseline discovery commands.
- Completed v5 release tree and `.claude` manifest listing.
- Completed required broad search across `Releases/v5.0.0`.
- Completed targeted inspection of authority, runtime, Pulse, ISA, Memory, PAI_DIR, installer, launcher, hook, and tool evidence.
- Created this plan and the S0 discovery report.
- Final verification showed exactly the two requested docs in `git diff --name-only | sort`, clean `git diff --check`, both files present, and no protected paths listed.

## Surprises & Discoveries

- `docs/` and `docs/adapters/` were absent at baseline, despite the required output paths.
- The v5 release is intentionally installed into `~/.claude/`, not into a repo-local docs-only tree.
- `PAI_DIR` resolves to `~/.claude/PAI`, while hooks and skills remain under `~/.claude`.
- Pulse is not a side feature. It is the central local daemon, dashboard, voice, hook-validation, observability, schedule, and event surface on port `31337`.
- The launcher and inference stack are strongly Claude-specific: `pai.ts` launches `claude`, appends `PAI_SYSTEM_PROMPT.md`, and `Inference.ts` shells out to `claude`.
- The ISA is repeatedly defined as the system-of-record primitive, and PAI memory is the canonical PAI state surface for work, learning, knowledge, relationship, and evidence.

## Decision Log

- Treat PAI v5.0.0 as canonical and ignore older adapter framing.
- Treat Claude Code as the official/full-support v5.0.0 runtime until replacement-grade validation exists.
- Treat Codex replacement as plausible only through a designed adapter, not by copying `.claude` files into a Codex location.
- Treat `PAI_SYSTEM_PROMPT.md` as high-authority doctrine.
- Treat Pulse as central v5 infrastructure.
- Treat PAI memory and ISA artifacts as canonical PAI state.
- Require a future single-writer policy before any Codex adapter writes to PAI state.

## Outcomes & Retrospective

S0 produced a read-only evidence baseline and no runtime implementation. The only repository content added is this plan and the paired report. The evidence supports a conservative architect decision: Codex is not proven drop-in for existing local PAI v5 files at S0. Future work should first design a reversible Codex runtime adapter and validation harness, with no requirement to uninstall Claude Code and no permission for Codex to write PAI state until single-writer rules and rollback behavior are proven.
