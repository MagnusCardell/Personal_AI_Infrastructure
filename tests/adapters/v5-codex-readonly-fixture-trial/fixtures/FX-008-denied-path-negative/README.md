# FX-008 Denied Path Negative

This fixture is isolated adapter-test material for S10A fixture-only validation.

It is not runtime payload, not a manifest, and not an audit artifact. It does not authorize Codex drop-in claims and does not authorize live existing-local-v5 access.

The fixture is a negative safety fixture for denied path coverage: live private state, root `AGENTS.md`, `.codex/`, release writes, PAI Memory writes, ISA writes, Pulse startup, and Pulse endpoint calls.
