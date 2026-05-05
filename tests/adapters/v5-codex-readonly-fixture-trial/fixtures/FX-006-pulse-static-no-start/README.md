# FX-006 Pulse Static No-Start

This fixture is isolated adapter-test material for S10A fixture-only validation.

It is not runtime payload, not a manifest, and not an audit artifact. It does not authorize Codex drop-in claims and does not authorize live existing-local-v5 access.

The fixture validates metadata for Pulse no-start and no-call boundaries only. Pulse remains central v5 infrastructure, but this fixture does not start Pulse, call endpoints, probe `localhost:31337`, or claim Pulse parity.
