# S14C Live Preflight Fixtures

These fixtures are synthetic repository fixtures for V5-S14C-LIVE-PREFLIGHT-FIXTURE-IMPLEMENTATION.

They are not live installed PAI state, not personal live-state evidence, not PAI Memory, not ISA, and not Pulse state. The fixture root represents only enough high-level structure to test consent parsing, path safety, forbidden-target rejection, redaction, non-canonical report generation, and no-runtime/no-Pulse behavior.

The `DO_NOT_READ` files contain sentinel body strings. The fixture-only preflight must not read those bodies and generated reports must not contain those sentinel strings.
