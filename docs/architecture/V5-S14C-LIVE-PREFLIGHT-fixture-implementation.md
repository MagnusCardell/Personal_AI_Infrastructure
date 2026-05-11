# V5-S14C-LIVE-PREFLIGHT-FIXTURE-IMPLEMENTATION: Fixture-Only Consent-Gated Preflight Tool

## 1. Architect decision

V5-S14C-LIVE-PREFLIGHT-FIXTURE-IMPLEMENTATION is approved as a fixture-only implementation milestone.

This milestone implements development tooling and tests only against repository fixtures and temporary synthetic roots. It is not a live preflight run and is not authorization to read installed PAI state.

## 2. Dependency on accepted S14A and S14B contracts

V5-S14A-LIVE-DESIGN is accepted at commit 3278f77c234a3a63e29086e45f9852d614809b27.

V5-S14B-LIVE-PREFLIGHT-IMPLEMENTATION-DESIGN is accepted at commit d2263954218f9024fde100e89472e3b6f7d92476.

The actual live installed PAI state remains ~/.claude/ and especially ~/.claude/PAI.

The clean repository clone remains only the adapter-development workspace.

The personal-clone framing is superseded and must not be reused as the live-state model.

## 3. Fixture-only boundary

S14C is fixture-only and does not read ~/.claude.

S14C is fixture-only and does not read ~/.claude/PAI.

S14C is fixture-only and does not read ~/.codex.

The fixture root is not live installed PAI state.

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

The implementation is limited to the approved S14C documentation, fixture, test, and development-tooling files.

The tool modules are under tools/pai_live_preflight/. They are fixture-only development/preflight tooling, not Codex runtime config, not hooks, not rules, not skills, not agents, not commands, not launchers, not installers, not Memory writers, not ISA writers, and not Pulse bridges.

## 5. Consent validation behavior

The exact future consent phrase is:

I approve a read-only preflight of my installed PAI state at ~/.claude/PAI for V5-S14A-LIVE-PREFLIGHT.

The declared future live source root is ~/.claude/PAI.

The implementation validates the exact consent phrase, the declared source root, the read-only/preflight-only trial mode, and explicit exclusion of Memory, ISA, Pulse, Claude memory, and Codex memory.

The implementation rejects missing consent, wrong consent phrase, wrong declared source root, broader declared roots, empty roots, traversal roots, and roots that would require home-directory or environment expansion.

## 6. Source-root and path-safety behavior

The implementation does not expand ~.

The implementation does not call Path.home().

The implementation does not call expanduser().

The implementation distinguishes the declared future live source root from the actual fixture root used for this milestone.

Path safety rejects traversal, symlink escape, reads outside the resolved fixture root, reads into forbidden subtrees, writes outside an approved output root, and ambiguous path resolution. It fails closed.

## 7. Approved fixture read behavior

The implementation performs only metadata checks for source-root existence, source-root directory status, PAI_DIR candidate detection, high-level PAI directories, high-level PAI files, readability signals, protected target exclusion, dry-run evidence output, and no-residue confirmation.

The implementation does not read PAI Memory content bodies.

The implementation does not read ISA content bodies.

The implementation does not read Pulse event payload bodies.

The implementation does not read personal file contents, Claude memory, Codex memory, or product memory.

## 8. Forbidden live-state and runtime behavior

The implementation does not inspect live installed state. It does not probe runtime services, start services, run installers, run migrations, run imports, create hooks, create rules, create skills, create agents, create commands, create launchers, write Memory, write ISA, or rewrite prior reports.

The implementation avoids subprocess, socket, requests, urllib, http.client, ftplib, telnetlib, and webbrowser imports.

## 9. Report schema and evidence classification

The report includes milestone_name, consent_status, source_root_label, source_root_redacted_display_path, declared_source_root, pai_dir_candidate_result, structural_check_results, forbidden_target_exclusion_results, pulse_not_probed_confirmation, memory_not_read_confirmation, isa_not_read_confirmation, no_residue_result, abort_status, known_risks, and evidence_classification.

The implementation reports fixture evidence.

The implementation reports non-canonical evidence.

The implementation does not report personal live-state evidence.

The implementation is not proof of runtime adapter correctness.

The implementation is not proof of Claude equivalence.

The implementation is not proof of replacement readiness.

The implementation is not proof that Codex can replace Claude.

The report is not proof that installed PAI state is safe to migrate.

## 10. Sensitive-data and redaction behavior

Reports use redacted labels and relative fixture metadata. Reports do not include raw personal file contents, raw installed absolute paths, Memory bodies, ISA bodies, Pulse payload bodies, Claude memory, Codex memory, or Pulse event payloads.

The fixture sentinel files prove that body content remains absent from generated reports.

## 11. Negative controls implemented

The fixture-only tests cover missing consent, wrong consent phrase, wrong declared source root, path traversal, symlink escape, attempted read of ~/.claude/projects, attempted read of ~/.codex/memories, attempted Memory content-body read, attempted ISA content-body read, attempted Pulse event payload-body read, output path escape, and static no-Pulse/no-runtime probe surfaces.

## 12. No-residue and write-boundary behavior

The preflight logic does not write. The report writer writes only to an explicitly approved output root and rejects paths outside that root.

Validation may write only inside the approved repository write set and the temporary ${TMPDIR:-/tmp}/s14c-preflight.* smoke-test directory.

## 13. Validation commands

The required validation commands are documentation heading validation, documentation content-invariant validation, implementation anchor validation, required test-name validation, fixture sentinel validation, static forbidden-runtime validation, static content-body read validation, fixture-only unit tests, fixture-only CLI smoke testing, write-boundary validation, and protected-path validation.

No live installed-state test is approved.

## 14. Known risks

Fixture-only evidence cannot prove live installed PAI structure, live permissions, live symlink state, live no-residue behavior, or replacement readiness.

A future live run requires a separate architect-approved Goal Card and explicit user consent.

## 15. Required final handoff format

Future Codex milestones must end with exactly:

files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only

## 16. Proposed next architect decision

Approve S14C-LIVE-PREFLIGHT-FIXTURE-IMPLEMENTATION and proceed to a separate fixture hardening/readiness-gate milestone before any live installed PAI access.

Alternatively, request revision to S14C-LIVE-PREFLIGHT-FIXTURE-IMPLEMENTATION before any further preflight work.

Do not recommend running a live ~/.claude/PAI trial yet.
