# V5 S18A — Codex Runtime Operational Readiness Report

S18A tests whether Codex can operate as the primary PAI session runtime across
real E1, E2, and E3 work. This report consolidates S17A-S17E evidence and the
S18A trial artifacts available at the time of the E3 trial.

This document is an operational readiness report, not a replacement-grade claim.
The replacement-grade decision belongs to the S18A scorecard.

## Baseline

- Baseline repo commit:
  `42fdae57238c16664e94f531d61b019660b309dd`
- Baseline subject:
  `S17E Codex runtime privacy and containment hardening`
- Current line: S17/S18 BYOM-C runtime-native Codex
- Historical line: S13-S16 BYOM-A adapter/provider evidence

S18A does not reopen adapter delegation, does not add capsule/shadow/human-gate
ceremony, does not add write-capable subagents, and does not add runtime backup
behavior.

## Evidence Map

Live PAI evidence:

- S17A0 probe:
  `~/.claude/PAI/MEMORY/OBSERVABILITY/codex-runtime-probe-summary.md`
- S17A MVP:
  `~/.claude/PAI/MEMORY/OBSERVABILITY/s17a-runtime-mvp-evidence.md`
- S17B live write:
  `~/.claude/PAI/MEMORY/OBSERVABILITY/s17b-live-write-evidence.md`
- S17C full Algorithm:
  `~/.claude/PAI/MEMORY/OBSERVABILITY/s17c-full-algorithm-evidence.md`
- S17D skills:
  `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d-skills-evidence.md`
- S17D read-only agents:
  `~/.claude/PAI/MEMORY/OBSERVABILITY/s17d-subagents-evidence.md`
- S17E hardening:
  `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e0-runtime-baseline-manifest.json`
  through
  `~/.claude/PAI/MEMORY/OBSERVABILITY/s17e5-hook-coverage-matrix.md`
- S18A0 baseline:
  `~/.claude/PAI/MEMORY/OBSERVABILITY/s18a0-baseline-check.md`
- S18A1 E1 trial:
  `~/.claude/PAI/MEMORY/OBSERVABILITY/s18a1-e1-trial.md`
- S18A2 E2 trial:
  `~/.claude/PAI/MEMORY/OBSERVABILITY/s18a2-e2-trial.md`
- S18A3 E3 trial:
  `~/.claude/PAI/MEMORY/OBSERVABILITY/s18a3-e3-trial.md`

Repo evidence:

- `docs/architecture/V5-S17-CODEX-AS-PAI-RUNTIME.md`
- `docs/architecture/V5-S17D-CODEX-NATIVE-SKILLS-AND-SUBAGENTS.md`
- `docs/architecture/V5-S17E-CODEX-RUNTIME-HARDENING.md`
- `tools/codex_runtime_evidence_index.py`

## Runtime Capability Summary

S17A established a minimal native Codex PAI session:

- live identity/project context reads;
- NATIVE answers for identity and project state;
- hook-loaded PAI context;
- prompt classification;
- dangerous-command guardrails.

S17B added live Memory/ISA writes:

- canonical `MEMORY/WORK/{slug}/ISA.md` writes;
- PostToolUse ISASync-lite detection;
- honest fallback behavior where canonical ISASync tooling was absent.

S17C proved full Algorithm execution:

- OBSERVE, THINK, PLAN, BUILD, EXECUTE, VERIFY, LEARN;
- live ISA status markers;
- explicit learning capture on completion;
- repo documentation and commit.

S17D added native Codex surfaces:

- PAI skills for Algorithm, Memory, ISA, and runtime audit;
- read-only custom agents for exploration, review, and security review;
- no write-capable subagents.

S17E hardened privacy and containment:

- raw prompts are not forwarded to nested classifier/model inference by default;
- hook logs use shared redaction and structured facts;
- writable roots were narrowed to live PAI state plus the repo;
- read-only custom agents passed negative write tests by refusal;
- hook coverage was mapped without overclaiming.

## S18A Trial Progress

S18A0 baseline check passed:

- identity answer used NATIVE mode and live PAI identity state;
- active-projects answer used NATIVE mode and live PAI projects state;
- `pwd` execution used E1 Algorithm behavior and tool hooks;
- S17E status summary read live S17E evidence and did not claim replacement-grade.

S18A1 E1 trial passed:

- task: add a README pointer to the S18A0 baseline evidence;
- mode/tier: E1 maintenance;
- commit: `301ac581d1d7b344bd51e534b33162bfa15717e0`;
- verification: targeted grep and diff before commit.

S18A2 E2 trial passed:

- task: add a sanitized runtime evidence index script;
- mode/tier: E2 bounded implementation;
- ISA:
  `~/.claude/PAI/MEMORY/WORK/20260520-082915_s18a2-codex-evidence-index/ISA.md`;
- commit: `5abc98620d80f6033571505ccb797b4919428d30`;
- verification: Python syntax, Markdown output, JSON output, executable
  invocation, and ISA validation.

S18A3 E3 trial purpose:

- consolidate the evidence above into this operational readiness report;
- update the evidence index so future sessions can locate the report, ISA,
  evidence, and learning path;
- write a concise learning after explicit completion.

## What Worked

- Codex retrieved live PAI context for identity, projects, and S17E runtime
  status without inventing state.
- Codex used NATIVE mode for direct live-state answers and Algorithm mode for
  execution work.
- Codex created canonical live ISAs under `MEMORY/WORK`.
- Codex produced useful repo commits with focused diffs.
- The S17D skills were available and useful for Algorithm, ISA, Memory, and
  runtime-audit behavior.
- S17E redaction and prompt privacy remained active during S18A.
- The evidence-index script gives future sessions a safer discovery path than
  broad grep across private memory.

## Trial Friction

- Nested `codex exec` probes required outer sandbox escalation so nested Codex
  could use its app-server/runtime files.
- Git index writes required escalation in this environment.
- The live project file still contains stale S16/S17 wording for the PAI
  project. Codex correctly reported it as live state instead of rewriting USER
  memory without instruction.
- Generated Python bytecode needed cleanup after syntax checking; this was a
  local verification artifact, not runtime behavior.

## Defects Versus Residual Risks

Concrete trial-affecting defects:

- None blocking so far.

Operational frictions:

- Outer sandbox escalation is needed for nested Codex and git index writes.
  This affects ergonomics, not correctness of runtime answers or artifacts.

Residual risks retained from S17E:

- Hooks are guardrails, not a complete security boundary.
- `~/.claude/PAI` remains writable by design.
- Read-only custom agents are tested by instruction/refusal and read-only
  policy, not by a universal proof that every PAI write path is impossible.
- MCP/WebSearch/internal developer-tool surfaces must not be assumed covered by
  Codex hook matchers unless mapped explicitly.
- Historical pre-S17E logs were not rewritten.

## Readiness Assessment

Current evidence supports this status:

- Codex is operational as the PAI runtime for bounded real E1/E2/E3 work.
- Codex is not yet declared replacement-grade in this report.
- Replacement-grade candidacy depends on the S18A4 scorecard after S18A3 is
  complete.

The strongest positive signal is that Codex performed real maintenance and
implementation tasks with live PAI context, canonical ISA writes, verification,
and focused commits without returning to adapter machinery or adding new safety
ceremony.

The strongest caution is that some operational paths still depend on environment
approval/escalation behavior, especially nested Codex probes and git writes.

## Non-Claims

S18A does not add write-capable custom agents.

S18A does not add runtime backup behavior.

S18A does not revive adapter delegation, capsules, shadow commits, or human-gate
adapter ceremony.

This report does not claim replacement-grade status.
