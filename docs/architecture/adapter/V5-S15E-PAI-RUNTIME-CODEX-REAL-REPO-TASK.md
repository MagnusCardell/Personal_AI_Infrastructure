# V5-S15E-PAI-RUNTIME-CODEX-REAL-REPO-TASK: PAI Runtime Executes a Bounded Real Repository Task with runtime=codex

## 1. Architect decision

S15E is the architect-approved next milestone after accepted S15D. It is an implementation and live runtime repository-task milestone, not replacement readiness.

S15E executed a bounded real repository task through the live PAI runtime runner.

## 2. Dependency on accepted S15D

S15E started from accepted S15D commit `6aabb84af919cc965532e4d6ab8646660152d18c` with a clean worktree before S15E edits began. S15D established that PAI owns the run and Codex is registered as runtime provider `codex`.

## 3. Real repository task target

S15E executed a bounded real repository task through the live PAI runtime runner.

PAI_DIR was ~/.claude/PAI.

S15E used pai-runtime run-repo --runtime codex.

S15E implemented the PAI runtime provider registry.

## 4. Files implemented

S15E modified tools/pai_runtime_runner/provider_registry.py.

S15E modified tests/test_pai_runtime_provider_registry.py.

files changed: S15E added the provider registry, repo-task runner/audit support, repo-run schemas, S15E task card, S15E tests, and this activation note within the approved repository write set.

behavior changed: PAI runtime now supports `run-repo` and `audit-repo-run` for a bounded real repository task with runtime provider `codex`; the provider registry validates Codex peer-beta runtime semantics.

## 5. Backup result

Backup root path: `/home/maca/.pai-codex-adapter-backups/s15e-20260514T103228Z`.

Backup completed: yes.

Rollback command:

```bash
python3 -m tools.pai_runtime_runner --pai-dir "$HOME/.claude/PAI" --backup-root "/home/maca/.pai-codex-adapter-backups/s15e-20260514T103228Z" --rollback
```

## 6. Live install result

Live PAI runtime runner install result: passed.

`pai-runtime doctor` passed before attempt 1, before attempt 2, and before attempt 3.

The live PAI runtime runner remains installed because validation passed.

## 7. PAI-owned repo-run result

S15E produced repo-run-result.json.

S15E produced repo-events.jsonl.

S15E produced repo-task.diff.

S15E produced repo-run-validation.json.

Artifact paths:

```text
/home/maca/.claude/PAI/runs/s15e/provider-registry/repo-run-result.json
/home/maca/.claude/PAI/runs/s15e/provider-registry/repo-events.jsonl
/home/maca/.claude/PAI/runs/s15e/provider-registry/repo-task.diff
/home/maca/.claude/PAI/runs/s15e/provider-registry/repo-run-validation.json
```

## 8. Codex provider invocation result

The runtime observed PAI_CODEX_PEER_BETA_ADAPTER.

Codex remains peer beta.

Claude remains the official/full-support upstream adapter.

Codex exec ran through the PAI runtime runner.

Attempt count: 3 live repo-task attempts.

Rollback needed: no.

Attempt 1 reached `codex exec` but produced no repository diff because nested shell/apply-patch execution hit the local sandbox loopback failure.

Attempt 2 reached `codex exec` but failed because the structured-output schema needed all properties listed in `required`.

Attempt 3 passed using Codex-authored materialized replacement content through the PAI runtime runner.

## 9. Repository test result

The provider registry tests passed.

tests run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_pai_runtime_runner_repo_task tests.test_pai_runtime_provider_registry
```

Final post-live test result: 23 tests passed.

## 10. Event-attributed write-boundary result

No Codex-attributed PAI Memory write was performed.

No Codex-attributed ISA write was performed.

Pulse was not started or probed by Codex.

localhost:31337 was not called by Codex.

No repo root AGENTS.md was created.

No repo .codex/ directory was created.

No PAI adapter files were installed under ~/.codex.

The live repo task modified only approved repository paths.

Event attribution passed.

protected files changed yes/no: no.

## 11. Ambient PAI churn classification

Ambient PAI state/cache/log churn is not adapter evidence.

Ambient PAI churn was observed in existing state/cache/log paths and classified separately from adapter evidence in `repo-run-validation.json`.

## 12. Rollback command

Rollback command:

```bash
python3 -m tools.pai_runtime_runner --pai-dir "$HOME/.claude/PAI" --backup-root "/home/maca/.pai-codex-adapter-backups/s15e-20260514T103228Z" --rollback
```

Rollback was not run because S15E validation passed.

## 13. Protected surfaces

No Memory writer, ISA writer, Pulse bridge, root repository AGENTS.md, repository `.codex/`, or `~/.codex` adapter installation is approved by S15E.

No Codex hooks, Codex rules, Codex skills, Codex agents, Codex commands, Claude hooks, Claude agents, Claude commands, Codex launchers outside approved PAI runtime/provider paths, PAI Memory writer, or ISA writer was created by S15E.

## 14. Known risks

known risks: S15E is one bounded real repository task. It does not prove Codex replacement readiness, Memory write safety, ISA write safety, or Pulse bridge readiness.

The nested Codex CLI environment could not execute local shell/apply-patch tools because of the local sandbox loopback failure, so the successful attempt used Codex-authored structured replacement content materialized by the PAI runtime runner.

## 15. Required final handoff format

The final handoff must use exactly these sections:

```text
files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only
```

goal state: S15E complete.

## 16. Proposed next architect decision

recommended next architect decision only: Approve S15E-PAI-RUNTIME-CODEX-REAL-REPO-TASK and proceed to S15F larger bounded repository task through PAI runtime=codex.

A later broader repository task or Memory/ISA write policy milestone requires a separate architect-approved Goal Card.
