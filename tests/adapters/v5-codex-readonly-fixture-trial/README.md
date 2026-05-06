# V5 Codex Read-Only Fixture Trial

S10A is fixture-only adapter-test material for the PAI v5 Codex replacement-adapter effort. The read-only harness validates fixture metadata and safety posture only.

The harness does not run Codex, does not run Claude Code, does not start Pulse, does not call Pulse endpoints, and does not inspect live user-local state. It does not write PAI Memory or ISA, and it does not authorize product memories to be promoted into PAI Memory.

The fixture metadata is not a manifest. Harness stdout is not an audit artifact. The files in this directory are not runtime payload, not Codex config, not hooks, not rules, not launchers, and not adapter payloads.

Codex is not currently proven drop-in for existing local PAI v5 files. Replacement remains plausible only through a designed adapter. `PAI_SYSTEM_PROMPT.md` remains high-authority doctrine, `CLAUDE.md` remains a Claude-facing surface, and future `AGENTS.md` must be a compact router only if later authorized. Claude-shaped files must not be copied directly into Codex surfaces.

The S10A posture is no live user-local access, no Pulse startup, no PAI Memory writes, no ISA writes, rollback/no-residue oriented validation, `denied_action_report` coverage, and `unsupported_surface_report` coverage.

## S10B Negative Controls

S10B adds negative-control self-tests for the read-only harness. These tests generate malformed or unsafe fixture metadata only inside temporary directories and verify the harness rejects it.

The negative controls are not committed fixtures. The temporary self-test data is not a fixture corpus, not a manifest, not an audit artifact, not a schema, not a config, not runtime files, and not runtime payload.

The self-test does not run Codex, does not run Claude Code, does not start Pulse, does not call Pulse endpoints, and does not inspect live user-local state. It does not write PAI Memory or ISA, and it does not authorize product memories to be promoted into PAI Memory.

Codex is not currently proven drop-in for existing local PAI v5 files. S10B proves only positive and negative fixture-harness behavior, not Codex drop-in behavior, not Pulse parity, and not existing-local-v5 trial readiness.

## S10C Semantic Hardening

S10C adds semantic fixture metadata so fixture validity is tied to the accepted safety and coverage model, not only JSON shape. Each fixture metadata file now carries `covered_seams`, `coverage_ids`, `gate_ids`, `safety_assertions`, and `semantic_status`.

The semantic fields connect fixtures to seam coverage, gate coverage, safety assertions, and a stronger source-path policy. Source paths remain repository-relative or approved synthetic markers, and the harness rejects private, protected, absolute, parent-traversal, `.codex/`, root `AGENTS.md`, root `CLAUDE.md`, and live user-local paths.

S10C extends negative controls from `NC-001` through `NC-030`, covering both the S10B structural failures and semantic policy failures. The harness remains a read-only harness. It does not run Codex, does not run Claude Code, does not start Pulse, does not call Pulse endpoints, and does not inspect live user-local state.

The harness does not write PAI Memory or ISA. Fixture metadata is not a manifest. Harness stdout is not an audit artifact. Codex is not currently proven drop-in for existing local PAI v5 files.

## S10D Fixture Case Data

S10D adds `case.json` fixture case data to each approved fixture directory. `case.json` is fixture case data only. It is not a manifest, not an audit artifact, and not runtime payload.

S10D adds expected-behavior and denied-behavior validation. The harness now validates fixture case input symbols, source references, expected behaviors, `denied_behaviors`, `unsupported_surface_expectations`, `no_write_expectations`, `audit_expectations`, `rollback_expectations`, `prohibited_actions`, source policy, and the false authorization booleans that preserve non-drop-in posture.

S10D extends negative controls from `NC-001` through `NC-045`. The new controls cover missing or malformed `case.json`, fixture ID mismatch, required case fields, invalid case type or status, empty expected-behavior lists, denied behavior coverage, unsupported-surface coverage, no-write coverage, source policy failures, forbidden source references, prohibited booleans, and S10D fixture file-set rules.

The harness remains a read-only harness. It does not run Codex, does not run Claude Code, does not start Pulse, does not call Pulse endpoints, and does not inspect live user-local state.

The harness does not write PAI Memory or ISA. Codex is not currently proven drop-in for existing local PAI v5 files.
