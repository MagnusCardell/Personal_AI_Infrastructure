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
