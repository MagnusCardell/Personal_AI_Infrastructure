# V5 Upstream Risk Register

## Purpose

This register translates the V5-S0 discovery evidence into replacement-adapter risks for PAI v5.0.0. It is an S1 design artifact only. It does not authorize runtime adapter implementation, release edits, installer edits, live `PAI_DIR` access, `.codex/` access, or writes to existing local v5 state.

## Scope

This register covers upstream, replacement, existing-user, dual-engine, dual-subscription, Pulse, ISA, and PAI Memory risks for the PAI v5.0.0 Codex replacement-adapter effort.

It does not implement an adapter, create runtime adapter files, authorize Pulse implementation, authorize PAI Memory writes, modify release files, inspect user-local state, or claim Codex is the official upstream engine.

## Canonical Target

The canonical target is PAI v5.0.0 as discovered in S0. The upstream release is Claude Code-native and the official/full-support runtime engine remains Claude Code until replacement-grade validation exists.

Codex is a replacement-capable beta local engine candidate only behind a designed adapter. Replacement means user-selectable local engine substitution, not overwriting Claude files and not turning PAI into an OpenAI project.

## Evidence Base

Primary evidence comes from:

- `docs/adapters/V5_S0_DISCOVERY_PLAN.md`
- `docs/adapters/V5_S0_DISCOVERY_REPORT.md`

Key release evidence cited by S0 includes:

- `Releases/v5.0.0/.claude/PAI/TOOLS/pai.ts`
- `Releases/v5.0.0/.claude/PAI/TOOLS/Inference.ts`
- `Releases/v5.0.0/.claude/settings.json`
- `Releases/v5.0.0/.claude/hooks/README.md`
- `Releases/v5.0.0/.claude/hooks/PromptProcessing.hook.ts`
- `Releases/v5.0.0/.claude/hooks/lib/paths.ts`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Pulse/PulseSystem.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md`
- `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md`
- `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md`
- `Releases/v5.0.0/.claude/agents/Engineer.md`
- `Releases/v5.0.0/.claude/commands/context-search.md`

## Risk Scoring Model

Risk scoring combines severity, likelihood, and priority.

| Severity | Meaning |
| --- | --- |
| Critical | Can corrupt canonical PAI state, expose private user-local state, destroy rollback, remove the proven runtime, or falsely claim replacement readiness. |
| High | Can break major runtime semantics, create misleading Pulse or memory behavior, weaken security, or block replacement-grade validation. |
| Medium | Can create review ambiguity, maintenance drift, fixture gaps, or operator confusion. |
| Low | Can create documentation, naming, or ergonomics issues that do not directly affect state safety. |

| Likelihood | Meaning |
| --- | --- |
| Likely | Expected unless actively controlled. |
| Possible | Plausible during design or prototype work. |
| Unlikely | Requires unusual conditions but must still be tracked. |

| Priority | Rule |
| --- | --- |
| P0 | Critical severity with likely or possible likelihood. Must block implementation until mitigated. |
| P1 | High severity with likely or possible likelihood. Must have an explicit architect gate. |
| P2 | Medium severity or low-likelihood high severity. Track and review before phase exit. |
| P3 | Low severity. Track if it affects docs or operator clarity. |

## Evidence Baseline

Primary evidence comes from `docs/adapters/V5_S0_DISCOVERY_REPORT.md` and its cited upstream paths under `Releases/v5.0.0/`.

S0 established that:

- PAI v5.0.0 is Claude Code-native and installed under `~/.claude/` (`docs/adapters/V5_S0_DISCOVERY_REPORT.md`, "Executive Finding").
- Codex is not proven drop-in for existing local PAI v5 files at S0 (`docs/adapters/V5_S0_DISCOVERY_REPORT.md`, "Drop-In Replacement Assessment").
- Pulse is central v5 infrastructure, not optional trivia (`docs/adapters/V5_S0_DISCOVERY_REPORT.md`, "Pulse Evidence").
- `PAI_SYSTEM_PROMPT.md` is high-authority doctrine, loaded above `CLAUDE.md` in the current Claude Code runtime (`Releases/v5.0.0/README.md:86`, `Releases/v5.0.0/README.md:257-268`, `Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md:183-187`).
- ISA artifacts and PAI Memory are canonical PAI state (`Releases/v5.0.0/.claude/PAI/DOCUMENTATION/IsaFormat.md:1-10`, `Releases/v5.0.0/.claude/PAI/DOCUMENTATION/Memory/MemorySystem.md:1-15`).
- PAI Memory, Claude Code memory, Codex memory, and Codex goal state are separate state surfaces unless a future adapter explicitly bridges them with provenance (`docs/adapters/V5_S0_DISCOVERY_REPORT.md`, "Dual Claude/Codex Subscription Memory Implications").

## Severity Scale

- Critical: can corrupt canonical PAI state, expose private user-local state, remove an existing working runtime, or falsely claim replacement readiness.
- High: can break major runtime semantics, produce misleading dashboard or memory behavior, or create unrecoverable adapter drift.
- Medium: can block validation, confuse operators, or create maintenance risk without immediate state corruption.
- Low: can create documentation or ergonomics issues that are unlikely to affect safety gates.

## Initial Risk Register

| ID | Risk | Affected Surfaces | Severity | Likelihood | Priority | Evidence | Mitigation | Verification Gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-001 | Upstream drift changes assumptions before implementation. | Release baseline, Codex behavior, adapter docs | Medium | Likely | P2 | S0 is a snapshot of `Releases/v5.0.0/`. | Refresh evidence before later milestones. | Evidence refresh logged. |
| R-002 | False drop-in confidence treats Codex as ready today. | Launcher, inference, settings, hooks, skills, agents, commands, Pulse jobs | Critical | Likely | P0 | S0 says Codex is not currently proven drop-in. | Define Codex as adapter-only until validation. | Runtime strategy answers drop-in as no. |
| R-003 | Authority loss demotes `PAI_SYSTEM_PROMPT.md`. | Instruction hierarchy, doctrine, conflicts | Critical | Possible | P0 | S0 identifies high-authority doctrine. | Require Codex authority-equivalence spec. | Authority gate with tests. |
| R-004 | `PAI_DIR` misbinding points Codex at live state. | `~/.claude/PAI`, Memory, USER, PULSE | Critical | Possible | P0 | S0 shows `PAI_DIR` defaults to user-local PAI. | Require explicit fixture root and live-root guards. | Fixture-root guard test. |
| R-005 | Pulse parity overclaim hides missing event support. | Dashboard, observability, jobs, hook validation | High | Likely | P1 | S0 establishes Pulse as central infrastructure. | Require Pulse bridge schema. | Pulse bridge reviewed. |
| R-006 | Pulse job identity confusion overloads Claude job type. | Scheduled reasoning, job history | High | Possible | P1 | S0 notes Claude job semantics. | Define Codex or adapter job identity. | Architect job identity decision. |
| R-007 | Hook lifecycle mismatch drops required behavior. | SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop, PreCompact, SessionEnd | High | Likely | P1 | Hooks are Claude lifecycle-specific. | Build event compatibility matrix. | Unsupported events explicit. |
| R-008 | Inference drift changes model, auth, output, or routing. | `Inference.ts`, model tiers, classification | High | Likely | P1 | S0 shows Claude subprocess inference. | Define Codex-native provider contract. | Provider contract approved. |
| R-009 | Settings and security mismatch weakens permissions. | `settings.json`, permissions, HTTP hooks, tools | Critical | Possible | P0 | S0 shows Claude Code settings schema. | Design native Codex policy. | Security mapping reviewed. |
| R-010 | Skills, commands, and agents lose semantics. | `skills/`, `commands/`, `agents/`, frontmatter | High | Likely | P1 | S0 shows Claude-shaped activation. | Transform by spec, not copy. | Transformation tests. |
| R-011 | Product-memory confusion treats non-canonical memory as PAI Memory. | Claude memory, Codex memory, Codex `/goal`, PAI Memory | High | Likely | P1 | S0 separates memory surfaces. | Require labels, curation, provenance. | Memory boundary check. |
| R-012 | Single-writer failure corrupts canonical state. | `PAI/MEMORY`, ISA, `STATE/work.json`, JSONL | Critical | Possible | P0 | S0 requires single-writer before writes. | No writes until lock or lease policy. | Single-writer policy approved. |
| R-013 | Existing-local-v5 overwrite damages user install. | `~/.claude`, settings, hooks, skills, agents, user files | Critical | Possible | P0 | S0 shows installer overlay risk. | Begin with read-only trial mode. | Existing-user trial plan approved. |
| R-014 | Rollback is unproven before live use. | Runtime config, Memory, ISA, Pulse state | Critical | Possible | P0 | S0 requires reversible replacement. | Treat rollback proof as gate. | Restore test passes. |
| R-015 | Governance confusion treats Codex as PAI owner. | Repo docs, architecture, vendor surfaces | Medium | Possible | P2 | Replacement is engine substitution only. | Separate PAI governance from engine vendor. | Governance reviewed. |

## Replacement-Specific Risks

Replacement-specific risks arise when "replacement" is interpreted too broadly.

Invalid interpretations:

- Replacement means copying `.claude` into `.codex`.
- Replacement means Codex is official upstream today.
- Replacement means Claude Code must be uninstalled.
- Replacement means PAI becomes an OpenAI project.
- Replacement means Claude-shaped files can be reused as Codex native surfaces.

Required control: Codex native surfaces must not be copied directly from Claude-shaped files. Behavior-preserving transformation requires an explicit adapter spec and tests.

## Existing Local v5 User Risks

Existing users may already have live and private state under `~/.claude/` and `~/.claude/PAI/`.

| Scenario | Future Mode | Primary Risk | Required Control |
| --- | --- | --- | --- |
| User wants to inspect whether Codex could work. | Read-only trial mode | Accidental live writes. | Read-only filesystem guard and no state mutation. |
| User wants Codex to suggest changes. | Assisted patch mode | Proposed patches mistaken for accepted PAI state. | Human review and external writer. |
| User wants Codex to write selected state. | Controlled single-writer mode | Concurrent Claude and Codex writes. | Single-writer lock or lease. |
| User wants only Codex locally. | Codex-only replacement mode | Missing Claude fallback. | Replacement readiness and rollback. |
| User wants both engines. | Dual-engine coexistence mode | Memory and state confusion. | Engine labels and writer ownership. |

S1R authorizes none of these modes at runtime.

## Dual-Engine and Dual-Subscription Memory Risks

Dual-engine and dual-subscription use does not merge state.

| Surface | Owner | Canonical PAI State | S1R Handling | Future Risk |
| --- | --- | --- | --- | --- |
| PAI Memory | PAI | Yes | Evidence only | Product memory could be silently promoted. |
| ISA | PAI | Yes | Evidence only | Codex could create shadow acceptance artifacts. |
| Pulse state | PAI runtime | Runtime-canonical when live | No live calls or writes | Events could be missing or mislabeled. |
| Claude Code memory | Claude Code | No | Separate product memory | Could be mistaken for PAI Memory. |
| Codex memory | Codex | No | Not inspected or modified | Could be mistaken for PAI Memory. |
| Codex `/goal` state | Codex | No | Orchestration metadata only | Could be mistaken for ISA or Pulse state. |
| Codex future adapter config | Future adapter | No by default | Not created in S1R | Could overwrite or imitate Claude config. |
| Repo governance files | Maintainers | Governance, not runtime state | Documentation only | Could blur policy with runtime behavior. |

Codex goal state is not PAI Memory, not ISA, and not Pulse state.

## Pulse, ISA, and Memory Risks

Pulse risks:

- Pulse is central v5 infrastructure, not optional background trivia.
- Pulse parity cannot be claimed without an event bridge.
- Codex job activity needs explicit Codex or adapter identity.

ISA risks:

- ISA is canonical PAI state.
- Codex must not create shadow ISA formats.
- Codex `/goal` completion is not ISA acceptance.

Memory risks:

- PAI Memory is canonical PAI state.
- Claude Code memory, Codex memory, and Codex `/goal` state are not PAI Memory.
- Product memories must not be silently promoted into PAI Memory.
- Writes require single-writer control.

## Known Upstream Observations

S0 records these upstream observations:

- PAI v5.0.0 is Claude Code-native.
- `pai.ts` launches `claude`.
- `Inference.ts` shells out to `claude`.
- `settings.json` is Claude Code settings.
- Hooks depend on Claude Code lifecycle payloads.
- Skills, commands, and agents are Claude-shaped.
- Pulse has Claude job semantics.
- `PAI_DIR` points to user-local live state.
- `PAI_SYSTEM_PROMPT.md` is high-authority doctrine.

## Risk Update Protocol

Update this register when:

- Current Codex runtime behavior is approved for inspection.
- A future phase proposes generated Codex config.
- A future phase proposes reading existing local v5 files.
- A future phase proposes writing PAI Memory, ISA, Pulse state, or user identity files.
- Upstream v5 evidence changes.
- Replacement scope changes.

Each risk update must include the risk ID, evidence, severity, likelihood, mitigation, verification gate, and architect decision required.

## Stop Conditions

Stop and request architect review if:

- Codex is claimed as drop-in today.
- Codex is claimed as the official upstream engine today.
- Claude files are proposed for direct copy into Codex.
- Live `PAI_DIR` writes are proposed without single-writer control.
- Pulse parity is claimed without a bridge.
- `PAI_SYSTEM_PROMPT.md` is demoted to ordinary markdown or memory.
- Codex goal state is treated as PAI Memory, ISA, or Pulse state.
- Existing local v5 trials require uninstalling Claude Code.
- Rollback is not demonstrated before live write mode.

## Architect Review Requirements

Before any implementation phase, an architect must approve:

- Authority-equivalence design for `PAI_SYSTEM_PROMPT.md`.
- Native Codex surface strategy.
- Hook and rule event compatibility matrix.
- Pulse event and job identity model.
- Memory and ISA read/write policy.
- Existing local v5 read-only trial plan.
- Single-writer policy.
- Rollback and reversibility proof.
- Governance separation between PAI and engine vendor.

## Cross-Risk Controls

The following controls apply to all critical and high risks:

- Read-only first: all future runtime validation must start against copied fixtures, not live `~/.claude` or live `PAI_DIR`.
- No drop-in claim: Codex is only a candidate replacement engine behind a designed adapter.
- No uninstall requirement: Claude Code remains installed and recoverable during any future Codex trial.
- Single-writer before writes: no Codex write path touches canonical PAI state until ownership, locking, provenance, and rollback are proven.
- Explicit provenance: future adapter-originated reads, events, generated config, and writes must identify engine, mode, source fixture or live root, and adapter version.
- Unknowns stay visible: unsupported Codex runtime mappings are recorded as gaps, not hidden behind compatibility language.

## S1 Risk Posture

At S1 completion, all risks remain design risks. None are resolved by implementation. The intended S1 outcome is a coherent strategy and set of gates that prevent premature adapter work from corrupting canonical PAI state or overstating Codex readiness.
