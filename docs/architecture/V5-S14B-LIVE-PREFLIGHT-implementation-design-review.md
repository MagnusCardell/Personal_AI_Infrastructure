# V5-S14B-LIVE-PREFLIGHT-IMPLEMENTATION-DESIGN: Explicit Consent-Gated ~/.claude/PAI Preflight Implementation Contract

## 1. Architect decision

V5-S14B-LIVE-PREFLIGHT-IMPLEMENTATION-DESIGN is approved as a documentation/design-review milestone only.

This document converts the accepted S14A live-state contract into an implementation-ready contract for a future consent-gated live installed PAI preflight tool. It does not authorize a live read, does not implement the tool, and does not run any live preflight.

## 2. Dependency on accepted S14A live-state contract

V5-S14A-LIVE-DESIGN is accepted at commit 3278f77c234a3a63e29086e45f9852d614809b27.

S14A corrected the live-state model: the actual live installed PAI state is in ~/.claude/ and especially ~/.claude/PAI.

The clean repository clone is only the adapter-development workspace.

The personal-clone S14A framing is superseded and must not be reused as the live-state model.

This S14B design assumes S14A is the upstream contract for live installed PAI read-only trial boundaries. The future implementation must preserve the S14A distinction between repository design artifacts and installed user-local PAI state.

## 3. Design-only boundary

This S14B milestone:

- does not read ~/.claude
- does not read ~/.claude/PAI
- does not read ~/.codex
- does not implement a live preflight runner
- does not run a live preflight trial
- does not create runtime adapter files
- does not create root AGENTS.md
- does not create .codex/
- does not start Pulse
- does not probe Pulse
- does not call localhost:31337
- does not invoke Claude Code
- does not invoke Codex runtime
- does not read product memory
- does not write PAI Memory
- does not write ISA
- does not modify installed PAI state

This milestone does not change runtime behavior, tests, hooks, configs, launchers, commands, installers, Memory behavior, ISA behavior, Pulse behavior, Claude behavior, Codex behavior, or adapter behavior.

## 4. Future implementation objective

The future implementation objective is a read-only, consent-gated preflight tool that can examine installed PAI structure under ~/.claude/PAI without reading personal content bodies and without creating runtime adapter surfaces.

The future tool should answer only structural preflight questions: whether the explicitly approved root exists, whether it is a directory, whether it is the likely PAI_DIR, whether expected high-level structure is present, whether protected targets are excluded, whether evidence can be emitted in a redacted non-canonical form, and whether no residue was created.

The future tool must not perform migration, import, adapter runtime setup, Pulse bridge creation, Memory integration, ISA integration, root AGENTS.md creation, .codex/ creation, or live Codex replacement work.

## 5. Future consent artifact model

The future implementation contract requires an explicit consent artifact before any live installed PAI path is read.

The exact required future consent phrase is:

I approve a read-only preflight of my installed PAI state at ~/.claude/PAI for V5-S14A-LIVE-PREFLIGHT.

Consent must not be inferred from:

- Claude Code installation
- Codex installation
- having both subscriptions
- presence of ~/.claude
- presence of ~/.claude/PAI
- presence of ~/.codex
- S14A acceptance
- S14B acceptance
- prior clean-clone trial approval
- prior release-fixture approval
- prior fixture-trial approval

The future consent artifact must include at least:

- milestone name
- exact consent phrase
- explicit source root
- timestamp
- operator identity or local user identity if available without external lookup
- statement that the trial is read-only
- statement that the trial is preflight-only
- statement that Memory, ISA, Pulse, Claude memory, and Codex memory are excluded

The future implementation must reject consent artifacts when:

- the consent phrase differs by even one character
- the source root is not exactly approved
- the consent artifact names a broader source root than approved
- the consent artifact is missing
- the consent artifact is stale under the future contract's chosen freshness rule
- the consent artifact would require reading product memory to validate

The consent artifact may authorize only the future preflight defined by its architect card. It must not authorize runtime adapter work, migration, imports, Pulse startup, Claude Code invocation, Codex runtime invocation, Memory writes, ISA writes, or product-memory reads.

## 6. Future source-root resolution model

The only approved future live source-root candidates are:

- ~/.claude/PAI
- ~/.claude

The future implementation should default to treating ~/.claude/PAI as the likely PAI_DIR.

The future implementation must not scan arbitrary home directories to discover PAI.

The future implementation must not resolve from ~/.claude to broader product memory reads.

The future implementation must treat ~/.claude as an outer installed-state container and ~/.claude/PAI as the likely PAI subsystem root.

The future implementation must expand and resolve only the explicitly approved and consented source root. It must not enumerate $HOME, /home, /Users, ~/.claude/projects, ~/.codex, or unrelated user-local directories to discover possible state.

## 7. Future path-safety algorithm

The future path-safety algorithm must include at least:

- expand only the explicitly approved source root
- resolve the approved source root
- verify the resolved root is one of the approved roots
- reject path traversal
- reject symlink escape
- reject reads outside the resolved approved root
- reject reads into forbidden subtrees
- use an allowlist for high-level metadata probes
- use relative or redacted paths in reports by default
- fail closed on ambiguity

The future implementation must distinguish:

- source-root existence checks
- source-root directory checks
- high-level structural metadata checks
- content-body reads

The future live preflight may perform only the first three categories unless a later architect card explicitly approves more.

The implementation should model every candidate probe as a relative path under the resolved approved root, normalize it without following unsafe escapes, reject parent traversal segments before access, reject symlinks whose resolved target leaves the approved root, and apply forbidden-subtree checks before any metadata read.

## 8. Future approved read model

The future implementation design limits future live reads to bounded metadata such as:

- source root exists
- source root is a directory
- PAI_DIR candidate detection
- presence/absence of expected high-level PAI directories
- presence/absence of expected high-level PAI files
- basic readability checks
- protected target exclusion checks
- dry-run evidence output
- no-residue confirmation

The future implementation must not read personal file contents.

The future implementation must not read PAI Memory content bodies.

The future implementation must not read ISA content bodies.

The future implementation must not read Pulse event payload bodies.

Approved metadata reads should be shallow, bounded, and allowlisted. They may report existence, type, relative path label, read permission signal, omission reason, and redacted count/status where the later architect card permits it.

## 9. Future forbidden read model

The future implementation must forbid reading by default:

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

The future implementation must not call, probe, or infer from:

- Pulse
- localhost:31337
- 127.0.0.1:31337
- Claude Code runtime
- Codex runtime
- Codex /goal state
- Codex import commands
- Codex migration commands
- Codex hook commands
- Codex rule commands
- Codex execpolicy commands

Forbidden reads include recursive scans, greps, body hashing, file sampling, parsing, summarization, or any operation that turns personal content into evidence.

## 10. Future evidence and report schema

The future report schema must contain only non-canonical evidence fields.

The evidence model must include these classifications:

- canonical evidence
- non-canonical evidence
- personal live-state evidence
- release-fixture evidence
- clean-clone evidence
- fixture evidence

Future live installed PAI preflight evidence is personal live-state evidence, non-canonical, not proof of runtime adapter correctness, not proof of Claude equivalence, not proof of replacement readiness, not proof that Codex can replace Claude, and not proof that installed PAI state is safe to migrate.

The future report schema must avoid raw personal content and must include at least:

- milestone name
- consent status
- source root label
- source root redacted display path
- PAI_DIR candidate result
- structural check results
- forbidden target exclusion results
- Pulse not probed confirmation
- Memory not read confirmation
- ISA not read confirmation
- no-residue result
- abort status
- known risks

The future report should also record report type, report status, source-root persistence policy, raw sensitive path persistence policy, runtime invocation status, protected write status, missing evidence classification, and limitations. These fields remain non-canonical and must not be promoted into PAI Memory, ISA, Pulse state, Claude memory, Codex memory, manifests, runtime payloads, or replacement-readiness claims.

## 11. Sensitive-data and redaction model

The future implementation must follow these rules:

- must not print personal file contents
- must not persist personal file contents
- must not persist raw sensitive absolute paths unless explicitly approved
- must prefer redacted or relative paths
- must report only non-canonical evidence
- must not produce canonical PAI Memory, ISA, or Pulse facts
- must not include Memory bodies
- must not include ISA bodies
- must not include Pulse payload bodies
- must not include Claude memory
- must not include Codex memory

Redaction should prefer source-root labels, relative allowlisted paths, booleans, counts, existence/status metadata, permission/readability signals, and explicit skipped-target reasons. If a future preflight cannot answer a question without exposing sensitive content, it must report the limitation instead of widening scope.

## 12. Future no-residue and rollback validation

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

For this S14B design milestone itself, no live no-residue check against ~/.claude is allowed because ~/.claude must not be touched.

The future no-residue model must separate:

- repository write-boundary checks
- approved report-output checks
- installed-state no-write checks
- runtime-surface absence checks

Rollback should be unnecessary for the future live preflight because the live preflight is read-only. If rollback is needed for ~/.claude, ~/.codex, PAI Memory, ISA, Pulse state, root AGENTS.md, repo .codex, or runtime adapter files, the future implementation has exceeded its contract.

## 13. Future fixture and negative-control strategy

A future implementation milestone must use fixture or synthetic roots before any live read.

Negative controls must cover at least:

- missing consent artifact
- wrong consent phrase
- wrong source root
- path traversal
- symlink escape
- attempted read of ~/.claude/projects
- attempted read of ~/.codex/memories
- attempted Pulse probe
- attempted Memory content-body read
- attempted ISA content-body read
- attempted write outside approved output path
- report rewrite outside approved write set

A future implementation milestone may implement and test the preflight logic against fixtures without live ~/.claude/PAI access.

A future live run requires a separate architect-approved Goal Card and explicit user consent.

The fixture strategy should include positive synthetic roots that mimic only high-level installed PAI structure and negative synthetic roots that attempt traversal, symlink escape, forbidden subtree reads, stale consent, malformed consent, report path escape, and runtime-probe paths. Fixture content must avoid real personal memories and product-memory bodies.

## 14. Future validation command classes

The future contract must distinguish these command classes:

- read-only validation commands
- commands that may write only approved outputs
- commands forbidden because their outputs are outside the write set
- commands forbidden because they would read live state without consent
- commands forbidden because they would probe runtime services

Future validation commands must not repeat the recurring contract error where report-generation commands rewrite outputs outside the approved write set.

If a validation command would write outside the approved write set, the contract is internally inconsistent and must be revised before execution.

Read-only validation commands may validate source code, static safety properties, fixture expectations, report schemas, and repository status. Commands that may write only approved outputs may generate future non-canonical consent, preflight, and evidence reports only when the future architect card explicitly names those paths. Commands forbidden because they would read live state without consent or probe runtime services must remain excluded from implementation and validation.

## 15. Future implementation write-set proposal

The following proposal is not approved for this milestone.

Candidate paths for a future architect card could include:

- a preflight implementation module
- a consent schema or validator
- fixture roots or synthetic cases
- negative-control tests
- a generated non-canonical preflight report path

Example future paths, subject to later architect approval, could be:

- tests/adapters/v5-codex-live-pai-preflight/run_live_pai_preflight.py
- tests/adapters/v5-codex-live-pai-preflight/consent/S14C_LIVE_PAI_PREFLIGHT_CONSENT_TEMPLATE.json
- tests/adapters/v5-codex-live-pai-preflight/fixtures/
- tests/adapters/v5-codex-live-pai-preflight/reports/S14C_LIVE_PAI_PREFLIGHT_REPORT.json
- tests/adapters/v5-codex-live-pai-preflight/test_live_pai_preflight_negative_controls.py

These paths are proposed for a future architect card only and are not approved for S14B-LIVE-PREFLIGHT-IMPLEMENTATION-DESIGN.

The future write set must not include root AGENTS.md, .codex/, ~/.claude, ~/.claude/PAI, ~/.codex, release files, runtime adapter files, Codex config, hooks, rules, skills, agents, commands, launchers, installers, Memory writers, ISA writers, Pulse bridge files, or product-memory destinations.

## 16. Future abort and stop conditions

The future implementation or live trial must abort before reading live state if:

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

The future implementation or live trial must also abort if:

- the implementation needs to infer consent
- the implementation needs to scan arbitrary home directories
- the implementation needs to inspect Claude product memory
- the implementation needs to inspect Codex product memory
- the implementation needs to start or query Pulse
- the implementation cannot redact sensitive absolute paths
- the implementation cannot prove no-residue within the approved checks

Abort must be fail-closed. A future implementation must not improvise by broadening source roots, reading memory bodies, probing services, invoking runtimes, writing alternate reports, creating runtime surfaces, or treating S14A acceptance or S14B acceptance as consent.

## 17. Required final handoff format

Future Codex milestones must end with exactly:

files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only

The recommendation must be advisory only. It must not begin implementation, run a live preflight, request broader installed-state access, or recommend a live ~/.claude/PAI trial before a separate architect-approved Goal Card and explicit user consent.

## 18. Proposed next architect decision

Approve S14B-LIVE-PREFLIGHT-IMPLEMENTATION-DESIGN and proceed to a separate fixture-only implementation milestone for the consent-gated preflight tool.

Alternatively, request revision to S14B-LIVE-PREFLIGHT-IMPLEMENTATION-DESIGN before any preflight implementation work.

Do not recommend running a live ~/.claude/PAI trial yet. The next safe implementation step is fixture-only unless a later architect card explicitly authorizes implementation scope and a still later card explicitly authorizes a live run with the exact consent phrase.
