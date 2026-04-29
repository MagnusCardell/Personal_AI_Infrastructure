# Codex Adapter Compatibility Matrix

This matrix is intentionally conservative. PR-02 added a tested platform/path
primitive. Phase 3 adds installer platform selection state, read-only Codex CLI
detection, and a first-class Codex-selected boundary after detection and
prerequisite reporting. PR-04A adds an unwired target-aware instruction
generator for Claude `CLAUDE.md` compatibility and compact Codex `AGENTS.md`
router output. PR-04B adds an unwired, explicit-path Codex `config.toml` merge
primitive with conflict detection, backup, idempotency, and path-safety tests.
PR-04C adds an unwired Codex adapter install-plan and temp-HOME
`AGENTS.md` writer primitive, plus optional test-only integration with the
PR-04B config merge helper. It does not implement Codex installer writes,
runtime config writes, hook, skill, agent, transcript, or release runtime
behavior.

Labels follow the repository guidance:

- `full`: tested and equivalent enough for normal use.
- `partial`: implemented with known semantic gaps.
- `claude-only`: intentionally not available in Codex.
- `codex-only`: available only through the Codex adapter.
- `unsupported`: not implemented and not promised.
- `breaking-for-codex`: Claude feature cannot be mapped without changed
  semantics.

The `Label` column applies to current Codex compatibility. `partial` is used
only for rows explicitly scoped to implemented primitives that still have known
runtime gaps.

| Area | Claude Status | Codex Status | Label | Evidence | Required Before Raising Claim |
|---|---|---|---|---|---|
| Existing Claude runtime artifacts | Current runtime shape under `Releases/*/.claude/` | Not applicable as Codex runtime | `claude-only` | Release settings, hooks, skills, agents, transcript tools, and generated instruction templates are stored under `.claude` | Keep non-installer runtime artifacts untouched unless a Claude adapter task explicitly requires changes |
| Platform path resolver primitive | Tested resolver preserves Claude default paths and Claude `PAI_DIR` compatibility | Tested primitive resolves Codex PAI home to `~/.pai` and Codex adapter/config home to `CODEX_HOME` or `~/.codex`; no Codex files are written | `partial` | `Releases/v4.0.3/.claude/PAI/Tools/platform/paths.ts`, `Tools/platform/paths.ts`, `Tools/platform/paths.test.ts` | Wire runtime writers in later phases without changing Claude defaults |
| Installer platform selection and boundary | Default installer platform is Claude; legacy saved state normalizes to Claude; Claude saved-state resume remains Claude-only | `--platform codex` and `--platform both` parse and are stored; Codex-containing selections run read-only detection/prerequisites, then stop before API keys, identity, repository, configuration, voice, validation, or writer phases; deliberate boundary stops do not save or delete installer state | `partial` | `PAI-Install/engine/options.ts`, `PAI-Install/engine/state.ts`, `PAI-Install/engine/platform-boundary.ts`, `Tools/installer-platform.test.ts`, `Tools/installer-platform-guards.test.ts`, `Tools/installer-boundary.test.ts`, `Tools/installer-entrypoints.test.ts` | Implement platform-specific Codex installer writers with temp-HOME tests |
| Default PAI application home runtime | `~/.claude` through settings and path helpers | Codex installer/runtime is not wired; only the resolver primitive returns `~/.pai` for future Codex use | `breaking-for-codex` | `settings.json`, `hooks/lib/paths.ts`, `SessionHarvester.ts`, pack installers, `Tools/platform/paths.test.ts` | Platform-selecting installer path usage with temp-HOME tests |
| `PAI_DIR` compatibility alias runtime | Used widely and points at Claude home by default | Codex runtime usage is not wired; only resolver precedence is tested | `breaking-for-codex` | Settings env, hooks, installer config generation, `Tools/platform/paths.test.ts` | Runtime path migration tests proving `PAI_DIR` compatibility remains intact |
| CLI detection primitives | Installer detects `claude --version` by default; older hooks check Claude package updates | Read-only Codex detection runs only for `codex` or `both`; missing Codex reports manual install hints; no Codex auto-install | `partial` | `PAI-Install/engine/detect.ts`, `PAI-Install/engine/actions.ts`, older `CheckVersion.hook.ts`, `Tools/installer-platform.test.ts`, `Tools/installer-platform-guards.test.ts`, `Tools/installer-boundary.test.ts` | Platform-specific install flow that never treats `~/.codex` as PAI home |
| Claude CLI prompt execution | Any `claude -p` use is Claude non-interactive prompt execution, not detection | Codex execution mapping not implemented | `breaking-for-codex` | Inventory pattern for `claude -p` | Explicit Codex execution contract and fixtures before mapping |
| Settings/config generation | Claude `settings.json` template and generated fallback remain full/current Claude behavior | Codex `config.toml` merge primitive exists as partial/unwired explicit-path helper; PR-04C can exercise it only with caller-supplied test fragments and explicit temp config paths; runtime writes to `~/.codex/config.toml` remain unsupported | `partial` | Release `settings.json`, `config-gen.ts`, `PAI-Install/engine/codex-config-merge.ts`, `PAI-Install/engine/codex-adapter-plan.ts`, `Tools/codex-config-merge.test.ts`, `Tools/codex-adapter-plan.test.ts` | Later installer phase with architect-approved product config fragments, temp-HOME runtime write tests, backup/idempotency validation, and no Codex defaults until authorized |
| Instruction file generation | `CLAUDE.md` generation remains full/current Claude behavior through the `BuildCLAUDE.ts` compatibility entrypoint and SessionStart hook import path | Codex `AGENTS.md` router generator/template exists but is unwired; dry-run rendering, explicit contained temp-output generation, and PR-04C temp-HOME adapter writer primitives are tested; installer/runtime writes remain unsupported | `partial` | `PAI/Tools/BuildInstructions.ts`, `PAI/Tools/BuildCLAUDE.ts`, `PAI/Adapters/codex/AGENTS.md.template`, `PAI-Install/engine/codex-adapter-plan.ts`, `Tools/instruction-generation.test.ts`, `Tools/codex-adapter-plan.test.ts`, hooks/handlers/BuildCLAUDE.ts | Wire Codex instruction output in a later installer phase without writing `~/.codex` as PAI home and without changing Claude defaults |
| Codex AGENTS.md writer primitive | Not applicable to current Claude runtime | Partial/unwired/temp-HOME only. The dedicated PR-04C writer can write `adapterHome/AGENTS.md` only at explicit temp `HOME/.codex/AGENTS.md` with `env.HOME` and `allowedRoot` supplied; it validates `PAI_HOME`/adapter-home separation, refuses `.codex` as the PAI application home, backs up and preserves modes, but no installer flow calls it | `partial` | `PAI-Install/engine/codex-adapter-plan.ts`, `Tools/codex-adapter-plan.test.ts` | Architect-approved installer wiring with temp-HOME end-to-end tests, no real-home writes, and unchanged Claude defaults |
| Codex config merge integration | Not applicable to current Claude runtime | Partial/unwired/test-only fragment. PR-04C can call the PR-04B merge helper only when a caller supplies `configFragment` and explicit `adapterHome/config.toml`; no product fragment, runtime defaults, model/provider/profile settings, approval policy, sandbox defaults, hooks, rules, skills, agents, or MCP config are introduced | `partial` | `PAI-Install/engine/codex-config-merge.ts`, `PAI-Install/engine/codex-adapter-plan.ts`, `Tools/codex-config-merge.test.ts`, `Tools/codex-adapter-plan.test.ts` | Architect-approved product config design and runtime wiring in a later phase |
| Codex instruction runtime install | Not applicable to current Claude runtime | Installer does not write real `~/.codex/AGENTS.md`, `~/.pai/AGENTS.md`, or any Codex runtime instruction file; PR-04C direct tests write only temp-home adapter paths | `unsupported` | `Tools/instruction-generation.test.ts`, `Tools/codex-adapter-plan.test.ts`, `Tools/installer-boundary.test.ts`, `Tools/installer-entrypoints.test.ts` | Later installer PR with temp-HOME tests, backup/idempotency rules, and architect approval |
| Codex runtime installer writes | Current Claude installer writes remain Claude-only by default | Unsupported. Codex-selected installer flows still stop at the Phase 3 boundary and do not call PR-04C install-plan or writer primitives | `unsupported` | `PAI-Install/engine/platform-boundary.ts`, `PAI-Install/engine/actions.ts`, `PAI-Install/cli/index.ts`, `PAI-Install/web/routes.ts`, `Tools/codex-adapter-plan.test.ts`, `Tools/installer-boundary.test.ts`, `Tools/installer-entrypoints.test.ts` | Architect-approved runtime write plan, temp-HOME end-to-end tests, rollback/backup behavior, and no writes to auth/session/history/log/credential files |
| Hook lifecycle events | Claude events and matchers are configured | Codex lifecycle mapping not implemented | `breaking-for-codex` | `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SessionEnd` | Normalized hook adapter with Claude and Codex fixtures |
| Hook decision outputs | Claude hooks emit `continue`, `decision: ask/block`, and `exit(2)` | Codex hook decision contract not proven | `breaking-for-codex` | SecurityValidator and guard hooks | Codex hook output fixtures plus hard-block behavior tests |
| Static command policy | Claude permissions `allow`/`ask` in settings plus SecurityValidator | Codex rules generation not implemented | `breaking-for-codex` | `settings.json` permissions and security hook | Split static rules from contextual hook validation |
| Claude tool permissions | Claude tool names allowed in settings | Codex tool names/surfaces differ | `breaking-for-codex` | `Read`, `Write`, `Edit`, `MultiEdit`, `Task`, `Skill`, `AskUserQuestion` | Tool mapping table with unsupported labels |
| Transcript parsing | Claude JSONL parser exists | Codex parser not implemented | `unsupported` | `TranscriptParser.ts`, `ExtractTranscript.ts`, hook `transcript_path` payloads | Codex transcript fixtures and parser interface |
| Session harvesting | Reads Claude project transcript paths | Codex session harvesting not implemented | `unsupported` | `SessionHarvester.ts` uses `~/.claude/projects` slugging | Platform transcript provider and temp fixture tests |
| Memory writes | Claude hooks write under PAI home memory paths | Codex memory writes not adapted | `unsupported` | Hooks write `MEMORY/*` through `PAI_DIR` or `paiPath` | Neutral PAI home resolution and hook adapter validation |
| Voice completion | Claude Stop hooks parse last response and trigger voice/notifications | Codex equivalent unproven | `unsupported` | `VoiceCompletion.hook.ts`, `TranscriptParser.ts`, notification helpers | Codex response-end fixture and native notification decision |
| Statusline | Claude `statusLine` command configured | Codex parity unproven | `unsupported` | Release `settings.json` statusLine and statusline docs/assets | Codex-native status mechanism or documented unsupported status |
| Terminal/tab state | Hooks manipulate terminal title/tab state | Codex parity unproven | `unsupported` | `UpdateTabTitle`, `SetQuestionTab`, `ResponseTabReset`, `KittyEnvPersist` | Codex lifecycle mapping and terminal behavior decision |
| Pack skill installs | Packs install into `~/.claude/skills` | Codex skill install paths not implemented | `breaking-for-codex` | `Packs/*/INSTALL.md` | Pack converter or platform-specific install docs |
| Pack command installs | Commands install into `~/.claude/commands` | Codex command equivalent unproven | `unsupported` | ContextSearch install docs | Codex command/rule surface decision |
| Pack READMEs | Describe current Claude/PAI usage | Codex pack docs not added outside adapter docs | `unsupported` | `Packs/*/README.md` | Update in later documentation phase after behavior exists |
| Agents/subagents | Claude `Task` tool and `.claude/Agents` assumptions | Codex custom-agent TOML not implemented | `breaking-for-codex` | Agent hooks, agent pack docs, `CLAUDE_PROJECT_DIR`, `CLAUDE_AGENT_TYPE` | Codex agent TOML generator or curated TOML files |
| Skills runtime format | Claude skill locations and `SKILL.md` frontmatter | Codex skill packaging not implemented | `breaking-for-codex` | Release skills and pack installers | Codex skill metadata validation and install destination tests |
| Backup/restore tooling | Backs up/restores `~/.claude` | Codex/neutral PAI backup not implemented | `unsupported` | `Tools/BackupRestore.ts` | Decide whether to keep Claude-only or introduce platform backup mode |
| Release packaging | Current release packages include `.claude` artifacts | Codex packaging not implemented | `unsupported` | Release tree inventory | Packaging tests excluding development `.codex` governance files |
| Windows platform support | Not supported in existing platform docs | Not in Codex adapter scope yet | `unsupported` | `PLATFORM.md` | Separate platform support plan |

## PR-01 Inventory Classifications

The inventory tool classifies each matched occurrence using these planning
categories:

- `claude-only`: belongs under the Claude adapter or current Claude releases.
- `platform-neutralizable`: can move behind neutral path/config/tooling
  abstractions in later phases.
- `codex-equivalent`: has an analogous Codex concept, but is not implemented
  here.
- `breaking-for-codex`: cannot be copied directly without changed semantics.
- `docs-only`: narrative or planning documentation reference.
- `unknown-needs-fixture`: cannot be claimed without a fixture, most often for
  transcript, hook, or session schemas.

## Current Codex Compatibility Summary

Current implementation covers the platform/path resolver primitive, installer
platform selection, read-only Codex detection, prerequisite reporting, the
first-class Codex-selected not-implemented boundary, PR-04A's unwired
target-aware instruction generator, and PR-04B's unwired explicit-path Codex
config merge primitive. PR-04C adds an unwired temp-HOME adapter plan and
`AGENTS.md` writer primitive plus test-only config merge integration. Codex
installer writes, runtime config writes, hook, skill, agent, transcript,
memory, release, and runtime behavior remain unimplemented unless separately
labeled in this matrix. The high-risk areas remain runtime path wiring,
installer config writes, hook lifecycle, security policy split, skills, agents,
and transcript/session parsing.
