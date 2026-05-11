# V5-S14D-LIVE-PREFLIGHT-LIVE-MODE-ENABLEMENT: Minimal Live-Mode Enablement

## 1. Architect decision

V5-S14D-LIVE-PREFLIGHT-LIVE-MODE-ENABLEMENT is approved as a minimal implementation milestone for live-mode enablement.

S14D implements live-mode enablement but does not run a live preflight.

## 2. Dependency on accepted S14A, S14B, and S14C contracts

V5-S14A-LIVE-DESIGN is accepted at commit 3278f77c234a3a63e29086e45f9852d614809b27.

V5-S14B-LIVE-PREFLIGHT-IMPLEMENTATION-DESIGN is accepted at commit d2263954218f9024fde100e89472e3b6f7d92476.

V5-S14C-LIVE-PREFLIGHT-FIXTURE-IMPLEMENTATION is accepted at commit bfc21d555cedae420e1d3768d2745c63b4866912.

The actual live installed PAI state remains ~/.claude/ and especially ~/.claude/PAI.

The clean repository clone remains only the adapter-development workspace.

## 3. Implementation boundary

S14D does not read ~/.claude.

S14D does not read ~/.claude/PAI.

S14D does not read ~/.codex.

The installed-pai mode is for a future explicitly consented live preflight run.

The implementation does not probe Pulse.

The implementation does not call localhost:31337.

The implementation does not invoke Claude Code.

The implementation does not invoke Codex runtime.

The implementation does not create root AGENTS.md.

The implementation does not create .codex/.

The implementation does not create runtime adapter files.

The implementation does not write PAI Memory.

The implementation does not write ISA.

## 4. Implemented files

S14D modifies only the approved preflight CLI, consent, path-safety, preflight, and report modules, and adds the approved S14D implementation note and live-mode enablement tests.

The approved tools remain development/preflight tooling only. They are not Codex runtime config, hooks, rules, skills, agents, commands, launchers, installers, Memory writers, ISA writers, Pulse bridges, or runtime adapter files.

## 5. Preserved S14C fixture behavior

The S14C fixture mode remains fixture evidence and non-canonical evidence.

Fixture mode remains the default CLI run context. Existing S14C tests continue to pass.

## 6. Added run-context behavior

The tool now accepts an explicit run context: fixture or installed-pai.

The implementation does not infer live mode from path shape, consent artifact existence, environment state, Claude state, Codex state, or product installation state.

## 7. Installed-PAI mode semantics

Installed-pai mode requires an explicit installed source-root argument and exact consent validation. In S14D it is validated only against temporary synthetic roots.

Installed-PAI mode evidence is personal live-state evidence only when run in a separately approved live milestone.

Installed-PAI mode evidence remains non-canonical evidence.

## 8. Consent validation behavior

The exact consent phrase remains required:

I approve a read-only preflight of my installed PAI state at ~/.claude/PAI for V5-S14A-LIVE-PREFLIGHT.

Consent is not inferred from Claude Code installation, Codex installation, having both subscriptions, presence of installed-state directories, S14A acceptance, S14B acceptance, S14C acceptance, S14D approval, or prior fixture approvals.

## 9. Source-root and path-safety behavior

The implementation does not expand ~.

The implementation does not call Path.home().

The implementation does not call expanduser().

Path safety continues to reject traversal, symlink escape, reads outside the resolved approved root, forbidden subtrees, writes outside the approved output root, and ambiguous path resolution.

## 10. Evidence classification behavior

Fixture mode reports fixture evidence, non-canonical evidence, and not personal live-state evidence.

Installed-pai mode reports future live-mode semantics as personal live-state evidence and non-canonical evidence, while S14D synthetic validation records that it is not an actual live installed PAI run.

The implementation is not proof of runtime adapter correctness.

The implementation is not proof of Claude equivalence.

The implementation is not proof of replacement readiness.

The implementation is not proof that Codex can replace Claude.

## 11. Sensitive-data and redaction behavior

The implementation does not read PAI Memory content bodies.

The implementation does not read ISA content bodies.

The implementation does not read Pulse event payload bodies.

Reports remain redacted and non-canonical. They do not persist raw synthetic source-root absolute paths and do not include Memory, ISA, or Pulse sentinel body content.

## 12. Negative controls implemented

The S14D tests cover fixture classification preservation, exact-consent enforcement, declared PAI root enforcement, explicit installed source-root requirement, tilde source-root rejection, home-variable source-root rejection, traversal rejection, symlink escape rejection, redacted non-canonical installed-mode reporting, sentinel non-leakage, and static no-runtime/no-network probe surfaces.

## 13. No-residue and write-boundary behavior

The preflight logic does not write reports directly. The report writer writes only to an explicitly approved output root and rejects output path escapes.

Validation may write only to approved repository files and temporary ${TMPDIR:-/tmp}/s14d-preflight.* directories.

## 14. Validation commands

The required validation commands cover approved changed files, protected paths, implementation-note headings, implementation-note invariants, implementation anchors, required tests, forbidden runtime/network/live-path mechanisms, content-body read restrictions, S14C and S14D unit tests, fixture-mode CLI regression smoke testing, installed-pai synthetic CLI smoke testing, and final status validation.

## 15. Known risks

S14D does not prove live installed PAI readability, live permissions, live symlink topology, live no-residue behavior, runtime adapter correctness, Claude equivalence, replacement readiness, Codex replacement readiness, or migration safety.

A future live run requires a separate architect-approved Goal Card and explicit user consent.

## 16. Required final handoff format

Future Codex milestones must end with exactly:

files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only

## 17. Proposed next architect decision

Approve S14D-LIVE-PREFLIGHT-LIVE-MODE-ENABLEMENT and proceed to an explicitly consented live ~/.claude/PAI preflight run.

Alternatively, request revision to S14D-LIVE-PREFLIGHT-LIVE-MODE-ENABLEMENT before any live installed PAI access.
