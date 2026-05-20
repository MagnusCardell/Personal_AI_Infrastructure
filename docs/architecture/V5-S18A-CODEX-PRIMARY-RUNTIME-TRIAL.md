# V5 S18A — Codex Primary Runtime Trial

S18A evaluates whether Codex can operate as the primary PAI session runtime
across real E1, E2, and E3 work.

Baseline commit:

- `42fdae57238c16664e94f531d61b019660b309dd`
- subject: `S17E Codex runtime privacy and containment hardening`

S18A does not add write-capable subagents, does not add runtime backup behavior,
and does not revive S13-S16 adapter delegation, capsules, shadow commits, or
human-gate adapter ceremony.

## Purpose

The primary question for S18A is:

Can Codex run PAI as the session runtime across real E1, E2, and E3 work with
correct PAI context, Algorithm behavior, Memory/ISA writes, verification, and
learning capture?

S18A is a runtime trial, not another hardening milestone. S17E remains the
privacy and containment baseline.

## Baseline Check

S18A0 confirmed the S17E runtime still works:

- `codex exec --json "who am I?"`
- `codex exec --json "what are my active projects?"`
- `codex exec --json "run pwd and explain the result"`
- `codex exec --json "summarize the current Codex PAI runtime status from the latest S17E evidence"`

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s18a0-baseline-check.md`

Result:

- NATIVE identity and project answers read live PAI state.
- E1 shell execution worked and used tool hooks.
- S17E status was read from live evidence.
- No blocking regression was found.

## E1 Trial

Task:

- Add a runtime README pointer to the S18A0 baseline evidence.

Mode/tier:

- `ALGORITHM` / `E1`

Files changed:

- `runtimes/codex/README.md`

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s18a1-e1-trial.md`

Commit:

- `301ac581d1d7b344bd51e534b33162bfa15717e0`
- subject: `S18A start primary runtime trial`

Result:

- Passed. The task was useful, low-risk, verified by grep/diff, and committed as
  a focused repo-only documentation change.

## E2 Trial

Task:

- Add a sanitized runtime evidence index script.

Mode/tier:

- `ALGORITHM` / `E2`

ISA:

- `~/.claude/PAI/MEMORY/WORK/20260520-082915_s18a2-codex-evidence-index/ISA.md`

Files changed:

- `tools/codex_runtime_evidence_index.py`
- `runtimes/codex/README.md`

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s18a2-e2-trial.md`

Commit:

- `5abc98620d80f6033571505ccb797b4919428d30`
- subject: `S18A add Codex runtime evidence index`

Result:

- Passed. The script reports known S17/S18 evidence paths and file metadata
  without reading evidence bodies. Verification covered syntax, Markdown output,
  JSON output, executable invocation, and ISA validation.

## E3 Trial

Task:

- Consolidate S17A-S17E and S18A evidence into a sanitized operational
  readiness report, then update the evidence index with the S18A3 report, ISA,
  evidence, and learning path.

Mode/tier:

- `ALGORITHM` / `E3`

ISA:

- `~/.claude/PAI/MEMORY/WORK/20260520-083325_s18a3-runtime-readiness-report/ISA.md`

Learning:

- `~/.claude/PAI/MEMORY/LEARNING/ALGORITHM/2026-05/2026-05-20-083505_LEARNING_s18a-primary-runtime-trial.md`

Files changed:

- `docs/architecture/V5-S18A-CODEX-RUNTIME-READINESS-REPORT.md`
- `tools/codex_runtime_evidence_index.py`

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s18a3-e3-trial.md`

Commit:

- `015245967d11fa7ec3346798fb109f3c1ffa1d93`
- subject: `S18A add Codex runtime readiness report`

Result:

- Passed. The full Algorithm run included OBSERVE, THINK, PLAN, BUILD, EXECUTE,
  VERIFY, and LEARN. The ISA validator initially exposed a heading mismatch; the
  ISA was corrected and then validated successfully.

## Scorecard

Replacement-grade evaluation:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s18a-replacement-grade-evaluation.md`

| category | result | summary |
| --- | --- | --- |
| Mode/tier correctness | pass | NATIVE for live-state reads; Algorithm for execution; E1/E2/E3 matched task scope. |
| Live PAI context retrieval | pass | Identity, projects, S17E evidence, ISA paths, and learning paths were read from live state. |
| Algorithm adherence | pass | E3 included all seven phases and a canonical ISA. |
| ISA quality | pass | S18A2/S18A3 ISAs used canonical paths, criteria, verification, and complete status. |
| Memory/learning quality | pass | Evidence stayed in OBSERVABILITY; learning was written only after explicit E3 completion. |
| Tool/hook behavior | pass | Hooks remained active; repo edits, validation, and commits worked. |
| Verification quality | pass | Checks included grep, diff, syntax parse, script output, JSON output, ISA validation, and git state. |
| Unnecessary ceremony / over-refusal | pass | No extra safety loop, adapter ceremony, runtime backup, or write-capable subagents. |
| Human intervention needed | partial | Nested Codex and git index writes needed normal escalation in this environment. |
| Commit quality | pass | Commits were focused and sanitized. |

## Decision

S18A decision: **replacement-grade candidate**.

This is not a final replacement-grade declaration. It means the E1/E2/E3 trial
evidence supports advancing Codex as a candidate primary PAI runtime. The only
trial-affecting issue was operational friction around environment approvals for
nested Codex and git index writes.

Concrete blockers:

- none found in S18A.

Operational frictions:

- nested `codex exec` required outer sandbox escalation;
- git index writes required escalation;
- one ISA validation shape issue was found and fixed.

Residual risks that actually affected trial work:

- escalation was required for nested Codex and git index writes;
- the live project file contained stale PAI milestone wording, and Codex
  correctly reported it as live state instead of silently editing USER memory.

## Non-Claims

S18A does not declare final replacement-grade status.

S18A does not add write-capable subagents.

S18A does not add runtime backup behavior.

S18A does not revive adapter delegation.

S18A does not create capsule, shadow, or human-gate adapter ceremony.
