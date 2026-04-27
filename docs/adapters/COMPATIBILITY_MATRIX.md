# Codex Adapter Compatibility Matrix

This matrix is intentionally conservative. PR-01 does not implement Codex
runtime behavior; it records what is known from inventory and where fixtures or
adapter work are required.

Labels follow the repository guidance:

- `full`: tested and equivalent enough for normal use.
- `partial`: implemented with known semantic gaps.
- `claude-only`: intentionally not available in Codex.
- `codex-only`: available only through the Codex adapter.
- `unsupported`: not implemented and not promised.
- `breaking-for-codex`: Claude feature cannot be mapped without changed
  semantics.

The `Label` column applies to current Codex compatibility. Because PR-01 does
not implement Codex runtime behavior, rows must not use `partial` unless a
future PR has implemented that Codex path with known semantic gaps.

| Area | Claude Status | Codex Status | Label | Evidence | Required Before Raising Claim |
|---|---|---|---|---|---|
| Existing Claude release artifacts | Current release shape under `Releases/*/.claude/` | Not applicable as Codex runtime | `claude-only` | Release settings, hooks, skills, and tools are stored under `.claude` | Keep untouched unless a Claude adapter task explicitly requires changes |
| Default PAI application home | `~/.claude` through settings and path helpers | Must default to `~/.pai`, not `~/.codex` | `breaking-for-codex` | `settings.json`, `hooks/lib/paths.ts`, `SessionHarvester.ts`, pack installers | Platform path abstraction with temp-HOME tests |
| `PAI_DIR` compatibility alias | Used widely and points at Claude home by default | Not implemented for Codex; must remain the legacy alias and keep priority over `PAI_HOME` where legacy behavior requires it. Codex's default PAI app home is `~/.pai`; `~/.codex` remains Codex CLI state/config space | `breaking-for-codex` | Settings env, hooks, installer config generation | Path precedence tests for `PAI_DIR`, `PAI_HOME`, Claude home, and Codex home |
| Claude CLI detection | Installer detects `claude --version`; older hooks check Claude package updates | Codex detection not implemented | `unsupported` | `PAI-Install/engine/detect.ts`, older `CheckVersion.hook.ts` | Platform-selecting detection that preserves Claude default |
| Claude CLI prompt execution | Any `claude -p` use is Claude non-interactive prompt execution, not detection | Codex execution mapping not implemented | `breaking-for-codex` | Inventory pattern for `claude -p` | Explicit Codex execution contract and fixtures before mapping |
| Settings/config generation | Claude `settings.json` template and generated fallback | Codex `config.toml` merge not implemented | `breaking-for-codex` | Release `settings.json`, `config-gen.ts` | Idempotent Codex config merge with backup tests |
| Instruction file | `CLAUDE.md` generated and loaded by Claude Code | Codex `AGENTS.md` router not implemented | `breaking-for-codex` | `BuildCLAUDE.ts`, settings `contextFiles`, hooks/handlers/BuildCLAUDE.ts | Split instruction builder and fixture-test generated outputs |
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
| Backup/restore tooling | Backs up/restores `~/.claude` | Codex/neutral PAI backup not implemented | `claude-only` | `Tools/BackupRestore.ts` | Decide whether to keep Claude-only or introduce platform backup mode |
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

Codex support is not implemented by PR-01. The only `codex-equivalent` findings
are planning signals, such as CLI detection having an eventual Codex analogue.
The high-risk areas remain path resolution, config merge, hook lifecycle,
security policy split, skills, agents, and transcript/session parsing.
