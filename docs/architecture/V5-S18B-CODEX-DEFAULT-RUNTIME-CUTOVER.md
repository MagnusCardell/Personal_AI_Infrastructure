# V5 S18B — Codex Default Runtime Cutover

S18B converts the S18A replacement-grade candidate result into an explicit
default-runtime decision.

Baseline:

- commit: `08029fec71cbc624d52c53e7341a700f55b008f0`
- subject: `S18A Codex primary runtime trial`
- tag: `v5-s18a-codex-primary-runtime-trial`

## S18A Candidate Result

S18A completed real E1, E2, and E3 work with Codex as the PAI runtime.

S18A decision:

- replacement-grade candidate;
- no concrete blocker found;
- not final replacement-grade;
- operational caveat: nested Codex probes and git index writes required normal
  escalation in this environment.

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s18a-replacement-grade-evaluation.md`
- `docs/architecture/V5-S18A-CODEX-PRIMARY-RUNTIME-TRIAL.md`

## Cutover Purpose

S18B answers:

Should Codex now become the default PAI runtime?

The target is default PAI runtime with fallback available. S18B does not claim
sole runtime status and does not remove fallback/advisor runtime options.

## S18B0 Tag Boundary

S18B0 created and pushed the S18A boundary tag:

- `v5-s18a-codex-primary-runtime-trial`

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s18b0-tag-boundary.md`

## S18B1 Readiness

S18B1 reran lightweight cutover readiness probes:

- `codex exec --json "who am I?"`
- `codex exec --json "what are my active projects?"`
- `codex exec --json "summarize the S18A replacement-grade candidate decision from live evidence"`
- `codex exec --json "run pwd and explain the result"`

Result:

- passed;
- live identity and projects were read;
- S18A decision evidence was read;
- Bash/tool execution worked;
- no concrete blocker appeared.

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s18b1-cutover-readiness.md`

## S18B2 Live Project State

S18B2 updated the live PAI project state in:

- `~/.claude/PAI/USER/PROJECTS/PROJECTS.md`

The update removed stale S16/S17 milestone wording and recorded:

- S16E adapter chapter closed;
- S17 Codex runtime MVP complete;
- S17D native Codex skills and read-only agents complete;
- S17E privacy and containment hardening complete;
- S18A primary runtime trial complete;
- S18B cutover state;
- BYOM-C runtime-native Codex as mainline;
- adapter/provider work as archived evidence.

After S18B4 approval, the same live project section was brought forward to:

- `Codex default PAI runtime approved`;
- default runtime with fallback available.

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s18b2-live-project-state-update.md`
- `~/.claude/PAI/MEMORY/WORK/20260520-115056_s18b2-live-project-state-update/ISA.md`
- `~/.claude/PAI/MEMORY/OBSERVABILITY/s18b-default-runtime-decision.md`

## S18B3 Cutover Run

S18B3 ran a realistic default-runtime cutover task:

- read live context;
- created a live cutover decision note;
- updated repo runtime docs with the S18B decision path;
- updated the sanitized evidence index;
- maintained a canonical ISA;
- verified outputs;
- wrote learning only after explicit completion.

Evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s18b3-default-runtime-cutover-run.md`
- `~/.claude/PAI/MEMORY/WORK/20260520-115236_s18b-default-runtime-cutover/ISA.md`
- `~/.claude/PAI/MEMORY/WORK/20260520-115236_s18b-default-runtime-cutover/CUTOVER_DECISION_NOTE.md`
- `~/.claude/PAI/MEMORY/LEARNING/ALGORITHM/2026-05/2026-05-20-115356_LEARNING_s18b-default-runtime-cutover.md`

Result:

- passed;
- no concrete blocker appeared;
- no separate S18B3 repo commit was created because repo changes were carried
  into the final S18B commit.

## S18B4 Decision

Final decision:

**APPROVED: Codex is now the default PAI runtime.**

Decision evidence:

- `~/.claude/PAI/MEMORY/OBSERVABILITY/s18b-default-runtime-decision.md`

The approval is scoped:

- Codex is default PAI runtime.
- BYOM-C runtime-native Codex is the mainline.
- Fallback/advisor runtime use remains available when explicitly needed.
- This is not a sole-runtime claim.

## Residual Operational Frictions

The cutover did not expose concrete runtime blockers.

Observed frictions:

- nested `codex exec` probes require outer sandbox escalation;
- git index writes require escalation in this environment.

These are operational frictions, not blockers. They did not prevent live PAI
context reads, live PAI state updates, canonical ISA/learning writes, repo docs,
verification, or the decision.

## Non-Revival And Safety Boundary

S18B does not revive S13-S16 adapter delegation.

S18B does not create capsule, shadow, or human-gate adapter ceremony.

S18B does not add runtime backup behavior.

S18B does not add write-capable subagents.

S18B preserves the S17E runtime posture:

- workspace-write;
- on-request approval;
- narrowed writable roots;
- hook logs with prompt privacy and redaction;
- hooks as guardrails, not a complete security boundary.

## Default, Sole, And Fallback Runtime

Default runtime:

- the normal PAI session runtime path;
- now Codex.

Sole runtime:

- would mean no fallback/advisor runtime remains available;
- not claimed by S18B.

Fallback/advisor runtime:

- remains available when explicitly needed;
- does not make the adapter line mainline again.
