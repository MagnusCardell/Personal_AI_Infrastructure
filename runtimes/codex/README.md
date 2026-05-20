# Codex Runtime Provider

Codex is registered as runtime provider `codex` for the S15D PAI runtime runner.
It remains peer beta and not replacement-grade. Memory writes, ISA writes, Pulse
probing, hooks, rules, skills, agents, and Codex native adapter installation are
not approved.

## S17 BYOM-C runtime-native line

S15D remains historical peer-beta provider evidence for the adapter-era runtime
runner. It is not the active S17 implementation path.

S17 starts a separate BYOM-C line where Codex is the PAI session runtime rather
than an adapter-backed provider. The S17 runtime surfaces are live user-level
Codex and PAI files:

- `~/.codex/AGENTS.md`
- `~/.codex/hooks.json`
- `~/.claude/hooks/codex/*`

The S17 line reads live `~/.claude/PAI` state directly, classifies
MINIMAL/NATIVE/ALGORITHM mode through Codex hooks, and adds live Memory/ISA
writes only after the S17A runtime-MVP exit criteria pass. The S15D language
above is preserved intentionally because it describes the historical provider
contract, not the S17 runtime-native effort.

S17 evidence is recorded in live PAI observability memory:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-runtime-probe-summary.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17a-runtime-mvp-evidence.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17b-live-write-evidence.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17c-full-algorithm-evidence.md`

S17C remains runtime-MVP evidence. Replacement-grade status is not claimed by
this README.

Current evidence:

- S17A0 probe: `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-runtime-probe-summary.md`
- S17A MVP session: `~/.claude/PAI/MEMORY/OBSERVABILITY/s17a-runtime-mvp-evidence.md`
- S17B live ISA write: `~/.claude/PAI/MEMORY/OBSERVABILITY/s17b-live-write-evidence.md`
- S17C full Algorithm run: `~/.claude/PAI/MEMORY/OBSERVABILITY/s17c-full-algorithm-evidence.md`

## S17D native Codex skills and read-only agents

S17D extends the BYOM-C runtime-native line with native Codex skills and
read-only custom agents. It does not revive adapter delegation, task-runner
ceremony, capsules, shadow commits, or human-gate adapter flows.

S17D0 sealed the S17C baseline at:

- commit: `45e00fbd9f351c0ad84d6991c7ac277c0e5cf26d`
- tag: `v5-s17c-codex-runtime-mvp`
- manifest: `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d0-runtime-baseline-manifest.json`
- regression evidence: `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d0-regression-evidence.md`

S17D1 installed user-level PAI skills under `~/.agents/skills`:

- `pai-algorithm`
- `pai-memory`
- `pai-isa`
- `pai-runtime-audit`

S17D2 installed read-only custom Codex agents under `~/.codex/agents`:

- `pai_explorer`
- `pai_reviewer`
- `pai_security_reviewer`

The custom agents are review/exploration surfaces only. They do not write PAI
Memory, do not mutate `~/.codex`, `~/.claude`, `~/.agents`, or the repository,
and do not become delegated write authorities. Parent runtime hooks may still
record normal observability/state activity around agent work.

S17D evidence is recorded at:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d-skills-evidence.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d-subagents-evidence.md`

Replacement-grade status is still not claimed.

## S17E privacy and containment hardening

S17E hardens the BYOM-C runtime-native line before any write-capable subagent
surface is considered. It does not add write-capable custom agents, does not
expand agent fan-out, does not revive adapter delegation, and does not introduce
runtime backup behavior.

S17E changes the live runtime posture:

- prompt classification is deterministic and local by default;
- raw prompts are not forwarded to nested classifier/model inference by default;
- hook logs use shared redaction and structured safe facts instead of raw prompt
  or command previews;
- persisted writable roots are narrowed from `/home/maca/.claude` to
  `/home/maca/.claude/PAI` plus this repo;
- S17D read-only custom agents have negative write-test evidence;
- current hook coverage is explicitly mapped without overclaiming MCP,
  WebSearch, or internal developer-tool surfaces.

S17E evidence is recorded at:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e0-runtime-baseline-manifest.json`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e0-regression-evidence.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e1-prompt-privacy-evidence.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e2-redaction-evidence.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e3-writable-root-evidence.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e4-readonly-agent-enforcement.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e5-hook-coverage-matrix.md`

Replacement-grade status is still not claimed after S17E.
