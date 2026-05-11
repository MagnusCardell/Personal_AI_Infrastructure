# V5-S14A-LIVE-DESIGN: Installed PAI ~/.claude/PAI Read-Only Trial Contract

## 1. Architect decision

Approved as a design/contract-only milestone for a future explicitly consented read-only preflight trial against installed live PAI state.

This milestone produces only the corrected S14-level contract. It does not perform the future live read, does not implement the future live preflight runner, does not run a live preflight trial, and does not use the superseded source-selected repository framing as the operational model.

Expected behavior change: none. This document changes design guidance only. It does not change runtime behavior, tests, hooks, configs, launchers, commands, Memory behavior, ISA behavior, Pulse behavior, Claude behavior, or Codex behavior.

## 2. Corrected live-state model

The actual live installed PAI state is in ~/.claude/ and especially ~/.claude/PAI.

The clean repository clone is only the adapter-development workspace.

The previous personal-clone S14A framing is superseded and must not be reused unmodified.

The future live installed PAI preflight must model the repository and the installed PAI state as separate surfaces:

- The repository is the adapter-development workspace where contracts, tests, and later implementation artifacts may be developed under an approved write set.
- The installed live PAI state is a user-local product state surface under ~/.claude/ and especially ~/.claude/PAI.
- A clean repository clone is not proof that installed PAI state is readable, structured as expected, or safe to use as an adapter input.
- Installed PAI state must be read only after explicit future consent and only inside a narrowly approved preflight boundary.

## 3. Non-goals

This milestone:

- does not read ~/.claude
- does not read ~/.claude/PAI
- does not implement a live preflight runner
- does not run a live preflight trial
- does not create a runtime adapter
- does not create root AGENTS.md
- does not create .codex/
- does not start or probe Pulse
- does not call localhost:31337
- does not read product memory
- does not write PAI Memory
- does not write ISA

This design does not authorize migration, import, runtime adapter behavior, dual-engine writes, Claude-to-Codex surface copying, Codex runtime setup, Pulse startup, Pulse endpoint calls, product-memory promotion, PAI Memory writes, or ISA writes.

## 4. Future trial consent model

A future implementation milestone must require explicit consent that names the live source root before reading installed PAI state.

The exact consent phrase required before any future installed PAI state read is:

I approve a read-only preflight of my installed PAI state at ~/.claude/PAI for V5-S14A-LIVE-PREFLIGHT.

Consent must be recorded in a future approved consent artifact before the future preflight reads ~/.claude/PAI or ~/.claude. The future preflight must compare the consent phrase exactly and abort if it does not match.

Consent must not be inferred from:

- Claude Code installation
- Codex installation
- having both subscriptions
- presence of ~/.claude
- presence of ~/.claude/PAI
- presence of ~/.codex
- prior clean-clone trial approval
- prior release-fixture approval
- prior fixture-trial approval

Consent to inspect installed PAI structure is not consent to read product memories, personal file contents, PAI Memory content bodies, ISA content bodies, or Pulse event payload bodies. Consent to run a read-only preflight is not consent to write runtime adapter files or create Codex governance surfaces.

## 5. Approved future source roots

The future candidate source roots are:

- ~/.claude/PAI
- ~/.claude

A future implementation should default to treating ~/.claude/PAI as the likely PAI_DIR.

The future implementation must not scan arbitrary home directories to discover PAI. It must not enumerate $HOME, /home, /Users, ~/.claude/projects, ~/.codex, or any unrelated user-local directory to locate candidate state. The future source root must be exactly approved and exactly consented.

If the future user consents to ~/.claude/PAI, the future preflight must stay within that root and must not broaden to ~/.claude. If the future user consents to ~/.claude, the preflight must still apply explicit protected target exclusions and must not treat the broader directory as consent to read memories or project state.

## 6. Forbidden future read targets

The future trial must forbid reading by default:

- ~/.claude/projects/**
- ~/.claude/projects/**/memory
- ~/.codex/**
- ~/.codex/memories/**
- product memories
- Claude memory
- Codex memory
- PAI Memory content bodies
- ISA content bodies
- Pulse event payload bodies
- arbitrary home-directory files

The future trial may only inspect bounded metadata needed for preflight, such as existence, type, relative structure, and permission/readability signals, and only after explicit consent.

Forbidden means no recursive scan, no grep, no content read, no hashing of file bodies, no sampling, no parsing, no summarization, and no persistence of content. If a forbidden target is encountered through structure metadata, the future evidence may report only redacted existence/count/status metadata when that metadata is explicitly in scope.

## 7. Future read-only preflight scope

The future live preflight is read-only and limited to structural checks such as:

- source root exists
- source root is a directory
- PAI_DIR candidate detection
- presence/absence of expected high-level PAI directories
- presence/absence of expected high-level PAI files
- basic readability checks
- protected target exclusion checks
- dry-run evidence output
- no-residue confirmation

The future preflight must explicitly forbid:

- running installers
- running migrations
- running imports
- starting Pulse
- probing Pulse
- calling Pulse endpoints
- invoking Claude Code
- invoking Codex runtime
- creating Codex adapter files
- creating hooks
- creating rules
- creating skills
- creating subagents
- creating commands
- creating launchers
- writing Memory
- writing ISA
- rewriting reports outside the approved write set

The preflight is a structural readiness check only. It must not transform installed PAI state, generate runtime configuration, create adapter payloads, or make replacement-readiness claims.

## 8. Sensitive-data handling rules

The future trial:

- must not print personal file contents
- must not persist personal file contents
- must not persist raw sensitive absolute paths unless explicitly approved
- must prefer redacted or relative paths
- must report only non-canonical evidence
- must not produce canonical PAI Memory, ISA, or Pulse facts

Evidence should use stable labels, redacted path classes, relative paths beneath the approved source root, booleans, counts, type signals, readability status, and explicit omission notes. It must not include full personal paths, file bodies, memory bodies, product-memory bodies, Pulse payload bodies, authentication material, environment secrets, command history, project content, or user-local Codex memory.

If a future preflight cannot answer a question without reading sensitive content, it must report the limitation and abort or mark the evidence unavailable instead of expanding scope.

## 9. Evidence model

The future evidence model must distinguish:

- canonical evidence
- non-canonical evidence
- personal live-state evidence
- release-fixture evidence
- clean-clone evidence
- fixture evidence

Future live installed PAI preflight evidence is personal live-state evidence, non-canonical, not proof of runtime adapter correctness, not proof of Claude equivalence, and not proof of replacement readiness.

Canonical evidence means approved PAI state or doctrine that the PAI system itself recognizes as authoritative, such as approved PAI Memory or ISA state when produced by their own authorized writers. The future live preflight must not create canonical evidence.

Non-canonical evidence means adapter-test or design evidence used only for architecture review and future implementation planning. Future preflight reports may support decisions about whether to design or implement adapter behavior, but they do not become PAI Memory, ISA, Pulse state, Claude memory, Codex memory, manifests, runtime payloads, or proof that Codex can replace Claude.

Release-fixture evidence, clean-clone evidence, and fixture evidence remain separate from personal live-state evidence. A pass in one evidence class must not be treated as a pass in another evidence class.

## 10. No-residue and rollback model

The future implementation must prove no residue by checking that it did not modify:

- ~/.claude/**
- ~/.claude/PAI/**
- ~/.codex/**
- repo root AGENTS.md
- repo .codex/**
- runtime adapter files
- PAI Memory
- ISA
- Pulse state

For this design milestone itself, no live no-residue check against ~/.claude is allowed, because ~/.claude must not be touched.

The future preflight should use before/after repository status checks for approved repository outputs and a carefully scoped live-state no-residue method that does not require reading forbidden content bodies. If no safe no-residue method exists for a target, the future implementation must state that limitation and avoid touching that target.

Rollback for the future implementation must be trivial because the live trial is read-only. Any need to rollback ~/.claude, ~/.codex, PAI Memory, ISA, Pulse state, Codex config, hooks, rules, skills, agents, commands, launchers, or adapter runtime files means the future implementation has exceeded the allowed preflight scope.

## 11. Protected-path and write-boundary model

For this design milestone, the only approved write is this design contract file. No runtime, test, release, protected, product-state, memory, ISA, Pulse, Claude, or Codex surfaces are approved for modification.

For the future implementation milestone, the write set must be explicit and minimal. The future preflight may write only approved non-canonical evidence outputs and any approved consent/preflight artifacts. It must not write installed live PAI state or user-local Codex state.

Protected future write targets include:

- ~/.claude/**
- ~/.claude/PAI/**
- ~/.codex/**
- repo root AGENTS.md
- repo .codex/**
- runtime adapter files
- Codex config
- Codex hooks
- Codex rules
- Codex skills
- Codex agents
- Codex commands
- Codex launchers
- Codex installers
- Claude hooks
- Claude agents
- Claude commands
- Pulse bridge
- PAI Memory writer
- ISA writer

The future implementation must not create root AGENTS.md, .codex/, Codex hooks, rules, skills, subagents, agents, commands, launchers, installers, wrappers, generated runtime configs, migration scripts, adapter payloads, Memory payloads, ISA payloads, Pulse payloads, Pulse bridge files, or runtime payloads.

## 12. Abort conditions

The future trial must abort before reading live state if:

- explicit consent artifact is missing
- consent phrase does not exactly match the approved phrase
- source root is not exactly approved
- source root resolves outside approved roots
- path traversal is detected
- symlink escape is detected
- the trial would read forbidden targets
- the trial would write outside its approved write set
- Pulse probing would occur
- Memory or ISA content-body reading would occur
- any command would modify ~/.claude
- any command would modify ~/.codex
- any command would modify root AGENTS.md
- any command would modify .codex/
- any validation command would rewrite reports outside the approved write set

The future trial must also abort if it would invoke Claude Code, invoke Codex runtime, run installers, run migrations, run imports, start Pulse, call Pulse endpoints, read product memories by default, print personal file contents, persist personal file contents, persist raw sensitive absolute paths without explicit approval, or require implementation of a runtime adapter.

## 13. Validation model for the future implementation milestone

The proposed later implementation milestone name is V5-S14B-LIVE-PREFLIGHT-IMPLEMENTATION. If the architect chooses a smaller step, the name may be V5-S14A-LIVE-PREFLIGHT.

No implementation occurs in this milestone.

The future implementation validation model must separate:

- read-only validation commands
- commands that may write only approved outputs
- commands forbidden because their outputs are outside the write set

Read-only validation commands may inspect repository status, validate consent artifact syntax, validate report schemas, stat the explicitly consented live source root, and check bounded structural metadata only after consent. Commands that may write only approved outputs may generate future non-canonical preflight and evidence reports inside the approved write set. Commands forbidden because their outputs are outside the write set include installers, migrations, imports, runtime invocations, formatters over unrelated files, generators for runtime adapter files, and any command that rewrites existing reports not listed in the approved write set.

The future implementation must include validation for exact consent phrase matching, approved source-root matching, path traversal rejection, symlink escape rejection, forbidden target exclusion, no content-body persistence, no raw sensitive absolute path persistence unless approved, no protected writes, no live-state residue, no Pulse activity, no Claude Code invocation, no Codex runtime invocation, and no files changed outside the approved write set.

## 14. Required final handoff format

Future Codex milestones must end with exactly:

files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only

The recommended next architect decision must remain advisory only. A future handoff must not start the live trial, implementation, migration, runtime adapter work, or broader live-state access unless a separate architect-issued goal card explicitly approves that scope.

## 15. Proposed next architect decision

Approve S14A-LIVE-DESIGN and proceed to a separate explicitly consented preflight implementation design review.

Alternatively, request revision to S14A-LIVE-DESIGN before any live installed PAI work.

Do not run a live trial from this milestone. Do not implement the live preflight runner from this milestone. Do not treat this document as consent to read ~/.claude or ~/.claude/PAI.
