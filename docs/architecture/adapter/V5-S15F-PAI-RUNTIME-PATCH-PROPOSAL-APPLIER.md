# V5-S15F PAI Runtime Patch Proposal Applier

## Current Status

S15F local implementation, install, doctor, tests, schemas, dry-run, path gates,
live `pai-runtime run-repo --runtime codex`, and live audit are complete.

The S15F provider command is hardened to `--sandbox read-only`. Codex produced a
structured full-file replacement proposal, and PAI validated and applied the
approved repository writes.

The full live proof exists under `~/.claude/PAI/runs/s15f/patch-proposal/`:

- `repo-run-result.json`
- `repo-events.jsonl`
- `repo-task.diff`
- `patch-proposal.json`
- `repo-run-validation.json`

## Acceptance Claims

S15F implemented PAI-owned patch proposal validation and application.
S15F used pai-runtime run-repo --runtime codex.
S15F produced patch-proposal.json.
S15F produced repo-run-result.json.
S15F produced repo-events.jsonl.
S15F produced repo-task.diff.
S15F produced repo-run-validation.json.

The patch proposal was validated before PAI applied repository writes.
The patch proposal was limited to the approved repository write set.
The patch proposal tests passed.
The runtime observed PAI_CODEX_PEER_BETA_ADAPTER.
Claude remains the official/full-support upstream adapter.
Codex remains peer beta.

No Codex-attributed PAI Memory write was performed.
No Codex-attributed ISA write was performed.
Pulse was not started or probed by Codex.
localhost:31337 was not called by Codex.
No repo root AGENTS.md was created.
No repo .codex/ directory was created.
No PAI adapter files were installed under ~/.codex.

## files changed

- `tools/pai_runtime_runner/patch_proposal.py`
- `tests/test_pai_runtime_patch_proposal.py`
- `tools/pai_runtime_runner/runner.py`
- `tools/pai_runtime_runner/audit.py`
- `tools/pai_runtime_runner/providers/codex.py`
- `tools/pai_runtime_runner/install.py`
- `pai-runtime/README.md`
- `pai-runtime/repo-task.schema.json`
- `pai-runtime/repo-run-result.schema.json`
- `pai-runtime/repo-run-validation.schema.json`
- `pai-runtime/patch-proposal.schema.json`
- `pai-runtime/tasks/s15f-patch-proposal-repo-task.json`
- `tests/test_pai_runtime_runner_repo_task.py`

## behavior changed

Codex can now return a structured full-file replacement proposal for a bounded
repository task. PAI owns the proposal artifact, validates every path and text
payload, applies only approved repository writes, records applied paths, writes a
diff, runs tests, and audits the result.

## tests run

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_pai_runtime_patch_proposal tests.test_pai_runtime_runner_repo_task tests.test_pai_runtime_provider_registry`

## known risks

S15F covers full-file replacement proposals only. Unified-diff metadata is
validated and preserved as proposal metadata, but initial materialization applies
full replacement content. The first live attempt exposed that current Codex
structured output rejects `allOf` in the output schema; S15F flattened the
repo-run result schema and the second live attempt passed.

## protected files changed yes/no

No protected repository paths were changed outside the approved S15F write set.

## goal state

S15F is ready for architect review with live artifact validation complete.

## recommended next architect decision only

Approve S15F-PAI-RUNTIME-PATCH-PROPOSAL-APPLIER and proceed to S15G PAI runtime
provider lifecycle commands.
