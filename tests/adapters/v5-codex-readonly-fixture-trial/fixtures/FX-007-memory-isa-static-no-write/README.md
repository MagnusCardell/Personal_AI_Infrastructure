# FX-007 Memory ISA Static No-Write

This fixture is isolated adapter-test material for S10A fixture-only validation.

It is not runtime payload, not a manifest, and not an audit artifact. It does not authorize Codex drop-in claims and does not authorize live existing-local-v5 access.

The fixture validates metadata for PAI Memory and ISA no-write boundaries only. Codex memory, Claude Code auto memory, transcripts, SDK threads, and `/goal` state are not PAI Memory.
