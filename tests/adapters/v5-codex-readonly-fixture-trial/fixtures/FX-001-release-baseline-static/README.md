# FX-001 Release Baseline Static

This fixture is isolated adapter-test material for S10A fixture-only validation.

It is not runtime payload, not a manifest, and not an audit artifact. It does not authorize Codex drop-in claims and does not authorize live existing-local-v5 access.

The fixture captures release-baseline metadata only, with no live user-local reads, no Pulse calls, no PAI Memory writes, no ISA writes, rollback/no-residue expectations, `denied_action_report`, and `unsupported_surface_report` coverage.
