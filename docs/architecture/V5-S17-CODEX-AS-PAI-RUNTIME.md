# V5 S17 - Codex As PAI Runtime

## Baseline

S16E is closed. The BYOM-A adapter chapter is complete and remains preserved as
historical evidence under the existing `adapters/codex` and `runtimes/codex`
materials.

S17 does not continue the S13-S16 adapter pattern. It does not add another
capsule, shadow-state, or human-gate adapter pipeline. The S17 decision is
BYOM-C: Codex becomes the native PAI session runtime.

## Decision

S17 makes Codex responsible for the live PAI session path:

- Read live PAI state directly from `~/.claude/PAI`.
- Speak PAI-native MINIMAL, NATIVE, and ALGORITHM formats.
- Classify prompts at `UserPromptSubmit`.
- Load identity, projects, Telos, and Algorithm pointers at `SessionStart`.
- Guard dangerous tool use before execution.
- Record turn and tool observability into live PAI memory.
- Preserve Codex sandbox and approval semantics.

The adapter chapter remains BYOM-A evidence. The S17 runtime is a new
runtime-native line and should not mutate the historical adapter contract.

## Runtime Surfaces

Runtime files live outside the repository:

- `~/.codex/AGENTS.md`
- `~/.codex/hooks.json`
- `~/.codex/config.toml`
- `~/.claude/hooks/codex/session-start.sh`
- `~/.claude/hooks/codex/prompt-processing.sh`
- `~/.claude/hooks/codex/pre-tool-use.sh`
- `~/.claude/hooks/codex/post-tool-use.sh`
- `~/.claude/hooks/codex/permission-request.sh`
- `~/.claude/hooks/codex/stop.sh`

Live PAI evidence and runtime logs live under:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-runtime-probe-summary.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17a-runtime-mvp-evidence.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17b-live-write-evidence.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17c-full-algorithm-evidence.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-hooks.jsonl`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-prompt-classification.jsonl`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-pretool.jsonl`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-posttool.jsonl`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-permissions.jsonl`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-stop.jsonl`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-isasync.jsonl`

## Build Checkpoint

S17A0 created a build-time checkpoint before editing live Codex and PAI hook
surfaces:

- `~/.pai-codex-build-checkpoints/s17-20260518T223129Z/`

This checkpoint is build safety only. Backup is not a runtime behavior. No
runtime hook may create a pre-session backup, git checkpoint, tar archive, or
backup-retention workflow.

## Hook Semantics

Codex 0.130.0 accepts the current hook config shape:

- top-level `hooks`
- event name
- array of matcher groups
- group-level `matcher` when needed
- group-level `hooks` array
- command handlers with `type = command`

Model-visible context is returned through:

- `hookSpecificOutput.hookEventName`
- `hookSpecificOutput.additionalContext`

Tool hooks read:

- `tool_name`
- `tool_input.command`

The S17A `PreToolUse` hook returns `{}` for allowed operations and returns a
hook-specific `permissionDecision = deny` only for blocked dangerous patterns.
It does not return `{"decision":"allow"}`.

The S17A `PermissionRequest` hook denies known-bad requests and returns `{}` for
all unknown cases so Codex falls back to its normal approval flow. The initial
proposal to auto-allow narrowly safe PAI-local requests was rejected by the
approval reviewer, so S17A uses the safer fallback-only policy.

`Stop` is turn-scoped. It is not true SessionEnd. It logs the turn stop event and
returns `{}`. It does not run backup retention or full WorkCompletionLearning.

## Milestones

### S17A0 - Native Probe

S17A0 proved:

- Codex version: `codex-cli 0.130.0`
- `~/.codex/hooks.json` loads.
- `/hooks` trust review is required after hook command changes.
- `SessionStart` fires.
- `UserPromptSubmit` fires.
- `PreToolUse` sees Bash.
- `PostToolUse` sees Bash.
- `Stop` returns valid JSON and does not break Codex.

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-runtime-probe-summary.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-runtime-probe.jsonl`

### S17A - MVP Session

S17A installs:

- lean global Codex PAI instructions in `~/.codex/AGENTS.md`
- current-shape hooks in `~/.codex/hooks.json`
- runtime hook scripts under `~/.claude/hooks/codex/`

Exit target:

- `codex "who am I?"` answers in NATIVE mode from live identity files.
- `codex "what are my active projects?"` answers in NATIVE mode from live
  `PROJECTS.md`.
- `codex "run pwd and explain the result"` records Bash in PreToolUse and
  PostToolUse logs.

S17A is runtime-MVP only. It is not replacement-grade.

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17a-runtime-mvp-evidence.md`

### S17B - Live Memory / ISA Writes

S17B began only after S17A exit criteria passed.

S17B proved:

- a real live ISA exists under `~/.claude/PAI/MEMORY/WORK/{slug}/ISA.md`
- `PostToolUse` detects canonical ISA paths for Bash and apply_patch events
- ISASync-lite runs when an ISA path is detected
- unknown permission requests fall back to normal Codex approval
- no runtime backup hook exists

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17b-live-write-evidence.md`
- `~/.claude/PAI/MEMORY/WORK/20260519-083122_add-test-project-projects-md-s17b/ISA.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-isasync.jsonl`

S17B used the existing `~/.claude/hooks/ISASync.hook.ts` fallback because
`~/.claude/PAI/TOOLS/ISASync.ts` was not present. ISASync returned exit code 0
for the S17B ISA path. The verification work intentionally did not mutate live
`PROJECTS.md`; it created a harmless work item under `MEMORY/WORK`.

### S17C - Full Algorithm Runtime

S17C begins only after S17B exit criteria pass. The first S17C run is a bounded
E3 run that closes the runtime MVP evidence trail, writes explicit completion
learning, and commits repository documentation.

Target:

- full E3 Algorithm run through OBSERVE, THINK, PLAN, BUILD, EXECUTE, VERIFY,
  and LEARN
- phase notifications when Pulse is reachable
- learning capture only on explicit completion
- coherent live `MEMORY/WORK` state

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17c-full-algorithm-evidence.md`
- `~/.claude/PAI/MEMORY/WORK/20260519-085317_s17c-full-algorithm-runtime/ISA.md`

S17C is still runtime-MVP evidence, not replacement-grade status. It preserves
Codex approval and sandbox semantics, keeps Stop turn-scoped, and writes
`MEMORY/LEARNING` only because Phase 17 explicitly asked for completion
evidence.

### S17D+ - Native Codex Skills / Subagents Bridge

Codex has native skills and subagents. S17A through S17C do not port them into
PAI. They remain future S17D+ surfaces.

## Safety Rules

- Do not use `danger-full-access`.
- Use workspace-write with on-request approvals.
- Do not commit secrets, tokens, auth files, API keys, `auth.json`, or env files.
- Never place tokens in URLs.
- Never read or write `~/.ssh`, `~/.gnupg`, cloud credential files, `auth.json`,
  or secrets unless explicitly instructed and approved.
- Hooks are guardrails, not a complete security boundary.
- Unknown PermissionRequest cases must fall back to Codex approval.
- No runtime backup hook exists.
