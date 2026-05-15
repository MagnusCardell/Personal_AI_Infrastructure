# V5-S15H PAI Runtime Capability Policy

## Current Status

S15H implements runtime capability policy for PAI runtime providers.

The Codex provider manifest declares:

- `repo.read`
- `repo.write.proposal`
- `repo.write.apply`
- `pai.context.read.metadata`
- `memory.write.disabled`
- `isa.write.disabled`
- `pulse.no-probe`

The PAI runtime runner enforces required task capabilities before handing a task
to the runtime provider. S15F patch-proposal repo tasks are inferred to require
`repo.read`, `repo.write.proposal`, and `repo.write.apply`.

## Acceptance Claims

S15H implemented runtime capability policy.
S15H runtime=codex can run bounded repo tasks requiring repo.write.proposal/apply.
S15H runtime=codex refuses tasks requiring Memory write.
S15H runtime=codex refuses tasks requiring ISA write.
S15H runtime=codex refuses tasks requiring Pulse probe.
S15H live validation passed.

No Codex-attributed PAI Memory write was performed.
No Codex-attributed ISA write was performed.
Pulse was not started or probed by Codex.
localhost:31337 was not called by Codex.
No repo root AGENTS.md was created.
No repo .codex/ directory was created.
No PAI adapter files were installed under ~/.codex.

Claude remains the official/full-support upstream adapter.
Codex remains peer beta.
S15H does not claim replacement readiness.

## files changed

- `tools/pai_runtime_runner/capabilities.py`
- `tools/pai_runtime_runner/runner.py`
- `tools/pai_runtime_runner/audit.py`
- `runtimes/codex/provider-manifest.json`
- `tests/test_pai_runtime_capabilities.py`
- `docs/architecture/V5-S15H-PAI-RUNTIME-CAPABILITY-POLICY.md`

## behavior changed

Tasks may declare `required_capabilities`; the runner unions those requirements
with profile-inferred requirements and refuses runtime execution when the
provider manifest does not satisfy the required capabilities.

Codex supports the proposal/apply repository path and read-only PAI metadata
context capability, while Memory writes, ISA writes, and Pulse probes remain
unavailable by policy.

## tests run

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_pai_runtime_capabilities tests.test_pai_runtime_provider_lifecycle tests.test_pai_runtime_provider_registry tests.test_pai_runtime_runner_repo_task tests.test_pai_runtime_runner_codex`

## known risks

S15H introduces policy enforcement for task admission. It does not implement the
read-only PAI context runtime task; that remains S15I.

## protected files changed yes/no

No protected repository paths were changed outside the S15H implementation set.

## goal state

S15H is ready for architect review after live capability validation.

## recommended next architect decision only

Approve S15H-PAI-RUNTIME-CAPABILITY-POLICY and proceed to S15I PAI runtime
read-only PAI context task.
