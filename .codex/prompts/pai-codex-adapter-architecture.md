# Canonical Architecture Prompt: PAI Codex CLI Adapter

Use this as the root prompt for a new Codex implementation thread in the PAI fork.

You are implementing the PAI Codex CLI adapter under architect-led project-steward constraints.

## Authority model

The migration is not autonomous. Codex implements the assigned phase or PR-sized task. Codex does not decide phase completion, rewrite the architecture, or advance to the next phase without architect review.

For every phase:

1. Implement only the current assigned scope.
2. Produce a reviewable diff and test evidence.
3. Run required review agents.
4. Stop after summarizing results and recommended next actions.
5. Wait for the architect-issued next prompt.

Codex recommendations are advisory. Architect-issued prompts are authoritative.

## Protected governance files

Do not edit these files unless the current prompt starts with `GOVERNANCE-UPDATE:` and names the files:

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/README.md`
- `.codex/.gitignore`
- `.codex/agents/**`
- `.codex/prompts/**`
- `.codex/governance/**`

If any protected file changes accidentally, stop and report.

## Goal

Adapt PAI so it supports Codex CLI as a first-class adapter while preserving existing Claude Code support by default.

This is not a replacement of Claude Code. This is a platform-adapter extension:

- PAI core: platform-neutral memory, context routing, algorithms, skills corpus, tools, voice, policy abstractions, backup/restore, installer engine.
- Claude adapter: existing Claude Code behavior, `~/.claude`, `CLAUDE.md`, Claude settings, Claude hooks, Claude tools, Claude transcripts.
- Codex adapter: Codex CLI config, `AGENTS.md`, hooks, rules, skills, custom agents, transcript/session parsing, and install integration.

## Primary invariants

1. Existing Claude users must keep working without migration.
2. Claude is the stable adapter; Codex starts as beta/partial until tests prove parity.
3. `~/.claude` remains the default Claude adapter home.
4. `~/.codex` is Codex CLI state/config space, not the PAI application home.
5. Default Codex PAI home is `~/.pai`.
6. `PAI_DIR` remains a legacy compatibility alias and takes priority where current behavior expects it.
7. Introduce `PAI_HOME` as the neutral preferred home.
8. Do not touch real user auth, history, sessions, logs, tokens, keys, or credentials.
9. Installer behavior must be idempotent and must backup before modifying existing user config.
10. Unsupported parity must be documented, not hidden.

## Codex-native mapping

Design Codex support around Codex primitives:

- `AGENTS.md` is a compact context router, not a full copy of `CLAUDE.md`.
- `~/.codex/config.toml` is merged, never overwritten.
- Codex hooks are registered through Codex-native config/hook files and normalized through a PAI hook adapter.
- Codex rules carry static command allow/prompt/forbidden policy.
- Contextual validation and PAI lifecycle work live in hooks where Codex supports it.
- Codex skills are exposed through `.agents/skills`, `~/.agents/skills`, or admin skill paths with proper `SKILL.md` metadata.
- Codex custom agents are TOML files, not Claude agent markdown.
- Codex transcript/session parsing must be based on Codex fixtures and hook-provided paths, not Claude transcript assumptions.

## Known breaking or partial mappings

Flag these explicitly:

- Claude dynamic statusline: breaking/Claude-only unless a Codex-native replacement exists.
- Claude `ask`/permission decision shapes: breaking if copied directly to Codex.
- Claude `SessionEnd`: remap to Codex `Stop` or explicit `pai finalize` fallback.
- Claude `Task`, `Skill`, and `AskUserQuestion` semantics: partial until deliberate Codex mapping exists.
- Claude transcript JSONL parsing: requires Codex parser and fixtures.
- Claude skill activation text: requires Codex skill frontmatter and descriptions.

## Canonical ten implementation phases

1. Inventory and compatibility baseline.
2. Platform core and path abstraction.
3. Installer platform selection and detection.
4. Instruction generation and Codex config merge.
5. Hook adapter and lifecycle mapping.
6. Security policy split: Codex rules plus contextual hooks.
7. Skills and pack conversion.
8. Agents and subagents conversion.
9. Transcript, memory, voice, notify, and status integration.
10. E2E install tests, release packaging, documentation, and beta readiness.

Phases may be decomposed into smaller PRs, but phase progression requires architect review.

## Required review agents

For every implementation PR:

1. `pai_reviewer`
2. `pai_security_reviewer`
3. `pai_test_engineer`

For architecture-sensitive PRs, also run:

1. `pai_architect`
2. `pai_codex_researcher`

For docs/release PRs, also run:

1. `pai_docs_reviewer`
2. `pai_release_manager`

## Implementation rules

- Do not broaden the assigned task.
- Do not run installer tests against the real home directory.
- Do not add hooks/rules to the repository `.codex` development harness as product behavior.
- Product Codex files must live in product adapter/release paths.
- Preserve comments and user settings when merging config where feasible.
- Add fixture tests for every schema touched.
- Keep Claude compatibility shims until explicitly removed by a major release decision.
- End every final response with whether protected governance files changed.

## Final response required from Codex

Return:

1. Task completed.
2. Files changed.
3. Behavior changed.
4. Tests added/updated.
5. Commands run and results.
6. Known risks.
7. Compatibility matrix updates needed.
8. Protected governance files changed: yes/no.
9. Recommended next PR, marked advisory only.
