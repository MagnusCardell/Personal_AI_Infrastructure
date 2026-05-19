# V5 S17D - Codex Native Skills And Subagents

## Status

S17D extends the S17 BYOM-C runtime-native line after the S17C runtime MVP.
It does not reopen S13-S16 adapter work, does not introduce capsule/shadow/
human-gate ceremony, and does not claim replacement-grade status.

Baseline:

- S17C commit: `45e00fbd9f351c0ad84d6991c7ac277c0e5cf26d`
- S17C tag: `v5-s17c-codex-runtime-mvp`
- branch: `codex-support-v5`
- runtime line: BYOM-C, where Codex is the PAI session runtime

S17C remains runtime-MVP evidence. Replacement-grade still requires further
evidence beyond S17D.

## S17D0 Baseline Seal

S17D0 is a baseline-sealing and regression gate, not a feature milestone. It
freezes the known-good S17C state before S17D skill and custom-agent surfaces
are added.

Live PAI evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d0-runtime-baseline-manifest.json`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d0-regression-evidence.md`

The manifest records sanitized hashes and runtime metadata only. It includes:

- `~/.codex/AGENTS.md` sha256
- `~/.codex/hooks.json` sha256
- `~/.codex/config.toml` sha256 with redaction check metadata
- `~/.claude/hooks/codex/*.sh` sha256 values
- Codex version
- sandbox mode
- approval policy
- writable roots
- hook trust status from `[hooks.state]`
- S17A0/S17A/S17B/S17C evidence paths
- S17B/S17C ISA paths
- S17C learning path
- seal-time visibility that S17D skill and custom-agent directories were absent
- confirmation that no runtime backup hook exists

S17D0 regression prompts:

- `codex exec --json "who am I?"`
- `codex exec --json "what are my active projects?"`
- `codex exec --json "run pwd and explain the result"`
- `codex exec --json "start a harmless E1 Algorithm run that only writes an ISA under MEMORY/WORK"`
- `codex exec --json "summarize the last S17C learning entry"`

Result: passed, with caveats recorded in the evidence. Nested Codex regression
required the outer sandbox approval path because nested Codex needed normal
local state writes. Codex's persisted runtime config remained
`workspace-write` / `on-request`.

The harmless E1 regression created:

- `~/.claude/PAI/MEMORY/WORK/20260519-215005_harmless-e1-work-isa-only/ISA.md`

Normal hook observability/state side effects may occur during these prompts.
Those side effects are not runtime backup behavior.

## S17D1 Native PAI Skills

S17D1 adds a small user-level PAI skill set under `~/.agents/skills`. These
are Codex-native skills, not plugins and not adapter tasks.

Installed skills:

- `~/.agents/skills/pai-algorithm/SKILL.md`
  - Trigger: run, structure, verify, or complete a PAI Algorithm run.
  - Reads `~/.claude/PAI/ALGORITHM/LATEST`.
  - Preserves `OBSERVE`, `THINK`, `PLAN`, `BUILD`, `EXECUTE`, `VERIFY`, `LEARN`.
  - Writes ISA/learning only under PAI runtime rules.

- `~/.agents/skills/pai-memory/SKILL.md`
  - Trigger: reading, summarizing, or safely writing PAI Memory.
  - Maps `USER`, `MEMORY/WORK`, `MEMORY/LEARNING`, and `MEMORY/OBSERVABILITY`.
  - Prohibits secret/auth paths and requires explicit completion before learning capture.

- `~/.agents/skills/pai-isa/SKILL.md`
  - Trigger: creating or updating `ISA.md`, ISCs, status markers, verification, or ISASync.
  - Enforces canonical `~/.claude/PAI/MEMORY/WORK/{slug}/ISA.md` pathing.
  - Documents ISASync fallback to `~/.claude/hooks/ISASync.hook.ts` because
    `~/.claude/PAI/TOOLS/ISASync.ts` is absent.
  - Includes `scripts/validate-isa.sh`.

- `~/.agents/skills/pai-runtime-audit/SKILL.md`
  - Trigger: runtime health, hooks, sandbox, permissions, logs, hashes, or regression evidence.
  - Includes `scripts/runtime-audit.sh`.
  - Checks `~/.codex/AGENTS.md`, `~/.codex/hooks.json`, `~/.codex/config.toml`,
    `~/.claude/hooks/codex/*.sh`, Codex observability logs, no runtime backup hooks,
    and the `workspace-write` / `on-request` policy.

S17D1 evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d-skills-evidence.md`

Verification performed:

- Static frontmatter and shell syntax checks.
- `codex debug prompt-input` visibility check for all four skills.
- Explicit invocation tests for `$pai-algorithm`, `$pai-memory`, `$pai-isa`, and
  `$pai-runtime-audit`.
- Implicit invocation test for `pai-runtime-audit`.
- `validate-isa.sh` was tightened after reviewer feedback to require canonical
  path, frontmatter fields, `Goal`, `Criteria`, at least one ISC, and
  verification for completed criteria.

## S17D2 Read-only Custom Agents

S17D2 adds bounded custom agents under `~/.codex/agents`. These are read-only
specialist review/exploration agents. They are not write-capable PAI subagents.
The parent runtime remains responsible for all writes.

Installed agents:

- `~/.codex/agents/pai_explorer.toml`
  - Maps PAI runtime files, docs, hook logs, and evidence.
  - Returns cited paths and concise findings.
  - No changes.

- `~/.codex/agents/pai_reviewer.toml`
  - Reviews PAI runtime changes for correctness, coherence, test gaps, and
    replacement-grade risk.
  - No changes.

- `~/.codex/agents/pai_security_reviewer.toml`
  - Reviews hooks, permissions, sandbox, secrets exposure, command-injection
    risk, unsafe writable roots, and custom-agent policy.
  - No changes.

Read-only policy:

- Each TOML sets `sandbox_mode = "read-only"`.
- Each TOML forbids file edits.
- Each TOML forbids PAI Memory writes.
- Each TOML forbids mutation of `~/.codex`, `~/.claude`, `~/.agents`, and the repository.
- Each TOML keeps the parent runtime responsible for writes.

Important precision: read-only applies to the custom agent tool sandbox and
instructions. The parent Codex runtime remains `workspace-write` / `on-request`,
and parent hooks may still write normal observability/state logs around agent
activity.

S17D2 evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d-subagents-evidence.md`

Verification performed:

- Static TOML inspection for required fields and read-only policy.
- `pai_explorer` custom-agent spawn test.
- `pai_reviewer` and `pai_security_reviewer` custom-agent spawn and wait test.
- Confirmation that subagent activity was explicit, not automatic.
- Confirmation that no write-capable custom PAI subagents were created.

Codex behavior notes:

- `codex debug prompt-input` did not expose custom-agent registry visibility the
  way it exposes skills.
- The outer session's static `spawn_agent` schema did not dynamically load the
  new custom agent names.
- Nested Codex multi-agent execution did recognize the custom agents.
- Full-history forking with custom agent type is blocked; custom agents must be
  spawned without full-history fork and given explicit scope/context.

## Safety Boundary

S17D preserves the S17C safety model:

- no `danger-full-access`
- no `approval_policy = "never"` in persisted Codex config
- no `network_access = true`
- hooks remain guardrails and observability, not a complete security boundary
- unknown PermissionRequest cases fall back to Codex approval
- no SessionStart backup
- no Stop backup retention
- no adapter, capsule, shadow-state, or human-gate pipeline is reintroduced
- no runtime backup behavior is installed
- no secrets, auth files, tokens, API keys, or private runtime contents are committed

## Verification Prompts

S17D1 explicit skill prompts:

- `Use $pai-algorithm to summarize the active Algorithm pointer and list the seven required phases. Do not write files.`
- `Use $pai-memory to summarize the PAI Memory map and state the rule for MEMORY/LEARNING writes. Do not write files.`
- `Use $pai-isa to inspect /home/maca/.claude/PAI/MEMORY/WORK/20260519-215005_harmless-e1-work-isa-only/ISA.md and report whether it is a valid E1 task ISA. Do not write files.`
- `Use $pai-runtime-audit to run a read-only runtime audit summary using the installed audit script. Do not modify files.`

S17D1 implicit skill prompt:

- `Audit the PAI runtime hooks, sandbox, approval policy, and absence of runtime backup behavior. Do not modify files.`

S17D2 custom-agent prompts:

- `Spawn the pai_explorer custom agent for a read-only S17D runtime audit...`
- `Spawn the pai_reviewer and pai_security_reviewer custom agents for read-only review of S17D files, then wait for both agents to complete...`

## Evidence Paths

- S17D0 manifest: `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d0-runtime-baseline-manifest.json`
- S17D0 regression: `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d0-regression-evidence.md`
- S17D skills: `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d-skills-evidence.md`
- S17D subagents: `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d-subagents-evidence.md`
- S17C full Algorithm evidence: `~/.claude/PAI/MEMORY/OBSERVABILITY/s17c-full-algorithm-evidence.md`
- S17C learning: `~/.claude/PAI/MEMORY/LEARNING/ALGORITHM/2026-05/2026-05-19-085500_LEARNING_s17c-codex-native-runtime.md`

## Gaps

- `prompt-processing.sh` may route full prompts through `Inference.ts` and a
  nested Claude CLI before normal Codex handling. This is inherited S17 runtime
  behavior and should be reviewed in a later safety-hardening milestone.
- Read-only custom-agent policy does not mean zero runtime writes; parent hooks
  may still append observability/state.
- Persisted writable root `/home/maca/.claude` is broad. It is currently used
  for live PAI runtime work but remains a containment risk.
- Hook log redaction is blocklist-based and too narrow for strong future
  secret-safety guarantees.
- Dangerous-command and protected-path denial is useful but incomplete; hooks
  remain guardrails.
- `pai-runtime-audit/scripts/runtime-audit.sh` is a small deterministic snapshot,
  not a full semantic runtime audit.
- Custom-agent registry visibility is proven by nested spawn tests rather than
  by `codex debug prompt-input`.
- S17D still does not claim replacement-grade status.
