# V5-S15G PAI Runtime Provider Lifecycle

## Current Status

S15G implements provider lifecycle UX for the PAI-owned runtime runner:

- `pai-runtime providers list`
- `pai-runtime providers status codex`
- `pai-runtime providers doctor codex`
- `pai-runtime providers validate codex`

Provider discovery and validation use `tools/pai_runtime_runner/provider_registry.py`.
The runner no longer carries a separate hardcoded Codex manifest validator for
provider lifecycle checks.

## Acceptance Claims

S15G implemented PAI runtime provider lifecycle commands.
S15G provider lifecycle discovery uses provider_registry.py.
S15G live PAI runner listed runtime=codex from the live provider manifest.
S15G live PAI runner reported runtime=codex status from the live provider manifest.
S15G live PAI runner passed provider doctor for runtime=codex.
S15G live PAI runner validated runtime=codex.
S15G event attribution and live write-boundary validation passed.

No Codex-attributed PAI Memory write was performed.
No Codex-attributed ISA write was performed.
Pulse was not started or probed by Codex.
localhost:31337 was not called by Codex.
No repo governance writes were performed.
No repo root AGENTS.md was created.
No repo .codex/ directory was created.
No PAI adapter files were installed under ~/.codex.

Claude remains the official/full-support upstream adapter.
Codex remains peer beta.

## files changed

- `tools/pai_runtime_runner/provider_registry.py`
- `tools/pai_runtime_runner/runner.py`
- `tools/pai_runtime_runner/__main__.py`
- `tools/pai_runtime_runner/audit.py`
- `tests/test_pai_runtime_provider_lifecycle.py`
- `docs/architecture/V5-S15G-PAI-RUNTIME-PROVIDER-LIFECYCLE.md`

## behavior changed

The PAI runtime runner now exposes provider lifecycle commands backed by the
provider registry. `providers list`, `providers status`, `providers doctor`, and
`providers validate` inspect the installed provider manifest under the PAI
runtime directory and report Codex as peer beta with Claude as upstream.

S15G also adds a provider lifecycle audit path for live write-boundary checks.
The lifecycle commands are PAI runner commands and do not invoke Codex exec.

## tests run

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_pai_runtime_provider_lifecycle tests.test_pai_runtime_provider_registry tests.test_pai_runtime_runner_repo_task tests.test_pai_runtime_runner_codex`

## known risks

S15G covers provider lifecycle UX and validation only. It does not implement
runtime capability policy; that remains S15H. It does not claim replacement
readiness.

## protected files changed yes/no

No protected repository paths were changed outside the S15G implementation set.

## goal state

S15G is ready for architect review after live provider lifecycle validation.

## recommended next architect decision only

Approve S15G-PAI-RUNTIME-PROVIDER-LIFECYCLE and proceed to S15H PAI runtime
capability policy.
