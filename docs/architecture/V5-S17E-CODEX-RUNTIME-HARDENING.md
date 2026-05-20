# V5 S17E — Codex Runtime Privacy And Containment Hardening

S17E hardens the S17 BYOM-C Codex-as-PAI runtime before any write-capable
subagent surface is considered.

S17E baseline commit:

- `e3f5f76b71b7e17b82d66c1a15e957b6dcc69e6d`
- subject: `S17D Codex native PAI skills bridge`

S17E does not start S18, does not claim replacement-grade, does not add
write-capable custom agents, does not expand agent fan-out, and does not add
runtime backup behavior.

## Baseline Seal

S17E0 sealed the S17D runtime baseline before behavior changes.

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e0-runtime-baseline-manifest.json`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e0-regression-evidence.md`

The baseline captured Codex version, persisted sandbox and approval policy,
writable roots, hook enablement/trust state where available, skill and custom
agent paths, sanitized SHA-256 hashes, and S17C/S17D evidence paths.

Baseline regressions covered:

- `codex exec --json "who am I?"`
- `codex exec --json "what are my active projects?"`
- `codex exec --json "run pwd and explain the result"`
- `codex exec --json "Use $pai-runtime-audit ..."`
- `codex exec --json "Spawn pai_security_reviewer ..."`

## Prompt Privacy

S17E1 removes the default raw-prompt forwarding path from
`~/.claude/hooks/codex/prompt-processing.sh`.

Before S17E, prompt classification could route the full prompt into
`Inference.ts` / nested model inference. After S17E:

- deterministic local classification is the default;
- raw prompts are not logged;
- raw prompts are not forwarded to nested model inference by default;
- hook context includes `PAI_CLASSIFIER` and `PAI_PRIVACY`;
- the hook still returns `hookSpecificOutput.hookEventName =
  "UserPromptSubmit"` with `additionalContext`.

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e1-prompt-privacy-evidence.md`

Residual precision: the main Codex model still receives the user's prompt as
normal session input. S17E1 hardens classifier/privacy behavior, not the primary
model conversation channel.

## Redaction And Logging

S17E2 adds shared hook helpers:

- `~/.claude/hooks/codex/lib/redact.py`
- `~/.claude/hooks/codex/lib/log_event.py`

The primary Codex PAI hooks now use shared safe logging:

- `session-start.sh`
- `prompt-processing.sh`
- `pre-tool-use.sh`
- `post-tool-use.sh`
- `permission-request.sh`
- `stop.sh`

The logging contract is:

- no raw prompts by default;
- no raw commands by default;
- log hashes, lengths, risk flags, tool names, decisions, and redaction
  metadata;
- redact token-like values, authorization headers, private-key material,
  credential-bearing URLs, session/cookie-looking values, high-entropy strings,
  protected credential paths, email addresses, and generic secret key/value
  patterns;
- raw debug preview requires an explicit local debug flag and is still redacted.

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e2-redaction-evidence.md`

Historical caveat: S17E does not rewrite old observability logs, so pre-S17E
`command_preview` / `stdout_preview` fields remain as historical evidence.

## Writable Roots

S17E3 tested three writable-root profiles:

- Profile A: current broad persisted configuration.
- Profile B: narrow `.claude` into PAI and explicitly include hook/Codex/skills
  maintenance roots.
- Profile C: PAI state and the repo only; hook/config mutation requires
  approval.

Profile C passed the core runtime checks:

- live identity read;
- live project read;
- `pwd` Bash hook regression;
- harmless E1 ISA-only Algorithm write under `MEMORY/WORK`;
- ISA validation;
- post-persist `who am I?`, active-projects, and `pwd` regressions.

S17E persisted Profile C in `~/.codex/config.toml`:

```diff
 [sandbox_workspace_write]
 writable_roots = [
-  "/home/maca/.claude",
+  "/home/maca/.claude/PAI",
   "/home/maca/code/Personal_AI_Infrastructure_fork",
 ]
```

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e3-writable-root-evidence.md`
- Profile C ISA:
  `~/.claude/PAI/MEMORY/WORK/s17e3-profile-c-privacy-containment/ISA.md`

Residual risk: `~/.claude/PAI` remains writable by design. PAI Memory writes are
still governed by runtime policy, hook guardrails, and Codex approval semantics,
not by path-scope denial alone.

## Read-Only Agents

S17E4 tested the S17D read-only custom agents:

- `pai_explorer`
- `pai_reviewer`
- `pai_security_reviewer`

Negative tests asked the agents to write under `/tmp`, mutate a live ISA, mutate
`~/.codex/config.toml`, append to PAI Memory, and attempt approval-requiring
commands. The agents refused by read-only instruction before sending write
commands to the tool layer.

Parent-side checks found:

- no `/tmp` canary file;
- no expected negative-test PAI Memory files;
- unchanged target ISA hash;
- unchanged `config.toml` hash during the agent test window;
- no write-capable custom agents created.

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e4-readonly-agent-enforcement.md`

Important limitation: this proves instruction-level/custom-agent refusal, not
universal sandbox write denial for PAI Memory. Parent hooks may still write
normal observability/state records around read-only agent work.

## Hook Coverage

S17E5 maps the current hook guardrail coverage.

Covered by configured matcher:

- `Bash`
- `apply_patch`
- `Edit`
- `Write`

Direct probes confirmed:

- simple Bash allowed and logged;
- dangerous Bash denied;
- safe `apply_patch` allowed and logged;
- dangerous `apply_patch` denied for protected path;
- nested Codex invocation is visible as a Bash wrapper command;
- network request falls back to Codex approval unless it matches known-bad
  patterns;
- unknown `PermissionRequest` returns `{}`;
- `Stop` returns `{}` and remains turn-scoped.

Not claimed covered:

- MCP tools unless Codex maps them to a matched tool;
- WebSearch or equivalent unless mapped to a matched tool;
- developer/internal unified exec surfaces outside Codex hook semantics.

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e5-hook-coverage-matrix.md`

## Residual Risks

- Hooks are guardrails, not a complete security boundary.
- PAI Memory remains writable for the parent runtime.
- Read-only custom agents refuse writes by policy, but parent runtime hooks may
  still record observability/state.
- PostToolUse can run ISASync when a command mentions a canonical ISA path, so
  some read-oriented ISA checks can update `MEMORY/STATE/work.json`.
- Effective noninteractive approval behavior can differ from persisted
  `approval_policy = "on-request"` in nested Codex execution.
- Historical pre-S17E logs may contain old preview fields.

## Non-Claims

S17E does not claim replacement-grade.

S17E does not add write-capable subagents.

S17E does not add runtime backup behavior.

S17E does not revive S13-S16 adapter delegation, capsules, shadow commits, or
human-gate adapter ceremony.
