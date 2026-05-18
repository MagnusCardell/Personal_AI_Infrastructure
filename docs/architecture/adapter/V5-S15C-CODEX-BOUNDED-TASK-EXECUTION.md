# V5-S15C-CODEX-BOUNDED-TASK-EXECUTION: Live Codex Adapter Executes a Bounded Synthetic Code Task

## 1. Architect decision

Approved as an implementation and live runtime task-execution milestone.

S15C was attempted as a bounded synthetic code task through the live Codex adapter.

The live milestone did not complete. Three live task attempts were used, task-run did not produce an accepted passing validation result, and rollback to the S15C backup was required.

## 2. Dependency on accepted S15B-R2

S15C depends on V5-S15A-CODEX-ADAPTER-LIVE-ACTIVATION-PILOT accepted at commit ee2479a2122022ca72ddfed37be4b889902f5077 and V5-S15B-R2-CODEX-RUNTIME-EVENT-ATTRIBUTED-WORKLOOP accepted at commit 9dd03b4a4d75b628980c8612acf989bcb892779a.

## 3. Task execution target

PAI_DIR was ~/.claude/PAI.

S15C used the installed pai-codex launcher.

S15C used codex exec for bounded task execution.

S15C initially attempted workspace-write only inside the approved isolated task workspace. The nested Codex runtime could not write the task workspace in this host environment, and the final fallback attempt failed before producing a valid structured task result.

PAI_CODEX_PEER_BETA_ADAPTER was observed by the live adapter install and doctor path, but no accepted S15C task-result artifact was produced.

## 4. Files implemented

files changed

- adapters/codex/AGENTS.md
- adapters/codex/README.md
- adapters/codex/adapter-manifest.json
- adapters/codex/bin/pai-codex
- adapters/codex/runtime-proof.schema.json
- adapters/codex/workloop-once.schema.json
- adapters/codex/runtime-validation.schema.json
- adapters/codex/task-card.schema.json
- adapters/codex/task-result.schema.json
- adapters/codex/task-validation.schema.json
- adapters/codex/tasks/s15c-synthetic-bugfix.json
- adapters/codex/task-fixtures/s15c_bugfix/README.md
- adapters/codex/task-fixtures/s15c_bugfix/src/pai_priority.py
- adapters/codex/task-fixtures/s15c_bugfix/tests/test_pai_priority.py
- tools/codex_adapter_installer/__main__.py
- tools/codex_adapter_installer/install.py
- tools/codex_adapter_installer/runtime_audit.py
- tools/codex_adapter_installer/task_audit.py
- tests/test_codex_adapter_bounded_task_execution.py
- docs/architecture/V5-S15C-CODEX-BOUNDED-TASK-EXECUTION.md

behavior changed

The installed adapter launcher supports task-run and audit-task for the S15C bounded synthetic bugfix task.

## 5. Backup result

The full ~/.claude folder was backed up before live S15C writes.

Actual backup root: /home/maca/.pai-codex-adapter-backups/s15c-20260513T194748Z.

Backup completed: yes.

## 6. Live install result

The live task payload installed during each attempt, then was rolled back after the third failed task attempt.

Rollback completed, restoring the live PAI adapter state from the S15C backup.

## 7. Bounded task-run result

S15C did not produce an accepted final task-result.json.

S15C produced task-events.jsonl during failed attempts before rollback.

S15C did not produce an accepted non-empty task.diff.

S15C did not produce an accepted task-validation.json because task-run failed before a passing audit.

Task result path: ~/.claude/PAI/adapters/codex/runs/s15c/task-result.json.

Task events path: ~/.claude/PAI/adapters/codex/runs/s15c/task-events.jsonl.

Task diff path: ~/.claude/PAI/adapters/codex/runs/s15c/task.diff.

Task validation path: ~/.claude/PAI/adapters/codex/runs/s15c/task-validation.json.

## 8. Test result

The task fixture initially failed before Codex repair.

The task tests did not pass after Codex repair within the three allowed live attempts.

## 9. Event-attributed write-boundary result

No Codex-attributed PAI Memory write was performed.

No Codex-attributed ISA write was performed.

Pulse was not started or probed by Codex.

localhost:31337 was not called by Codex.

Event attribution did not pass for S15C because no accepted audited task run was produced before the stop condition.

## 10. Ambient PAI churn classification

Ambient PAI state/cache/log churn is not adapter evidence.

Any accepted ambient churn must be reported in task-validation.json and must not be Codex-attributed Memory, ISA, or Pulse event payload writes.

## 11. Rollback command

Rollback command used after the third failed live task attempt:

```bash
python3 -m tools.codex_adapter_installer \
  --pai-dir "$HOME/.claude/PAI" \
  --backup-root "/home/maca/.pai-codex-adapter-backups/s15c-20260513T194748Z" \
  --rollback
```

## 12. Protected surfaces

Claude remains the official/full-support upstream adapter.

Codex remains peer beta.

No repo root AGENTS.md was created.

No repo .codex/ directory was created.

No PAI adapter files were installed under ~/.codex.

No Memory writer was implemented.

No ISA writer was implemented.

No Pulse bridge was implemented.

A later real PAI task or Memory/ISA write policy milestone requires a separate architect-approved Goal Card.

protected files changed yes/no

Protected files changed: no.

## 13. Known risks

known risks

- This is a synthetic bounded code task, not replacement readiness.
- Codex JSONL event attribution is the primary task write-boundary signal, with filesystem mtime scanning as a secondary detector.
- Codex product runtime metadata outside PAI is not inspected by content.
- The S15C implementation is not accepted. Attempt 1 and attempt 2 were blocked by nested Codex workspace write failures. Attempt 3 was blocked by a structured-output schema mismatch after adding repair materialization fields.

## 14. Required final handoff format

files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only

## 15. Proposed next architect decision

recommended next architect decision only

Request rollback/revision of S15C-CODEX-BOUNDED-TASK-EXECUTION before further runtime task work.
