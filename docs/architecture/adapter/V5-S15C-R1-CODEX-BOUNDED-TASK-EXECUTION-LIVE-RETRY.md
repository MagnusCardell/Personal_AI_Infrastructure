# V5-S15C-R1-CODEX-BOUNDED-TASK-EXECUTION-LIVE-RETRY: Retry Live Bounded Synthetic Code Task with Sealed Audit Inputs

## 1. Architect decision

S15C-R1 retried bounded synthetic code task execution through the live Codex adapter.

This retry is approved as a live bounded task-execution milestone, not a documentation-only milestone and not replacement readiness.

## 2. Dependency on accepted S15B-R2 and blocked S15C evidence

S15C-R1 depends on V5-S15A-CODEX-ADAPTER-LIVE-ACTIVATION-PILOT accepted at commit ee2479a2122022ca72ddfed37be4b889902f5077 and V5-S15B-R2-CODEX-RUNTIME-EVENT-ATTRIBUTED-WORKLOOP accepted at commit 9dd03b4a4d75b628980c8612acf989bcb892779a.

S15C-R1 uses the staged retry-prep evidence from commit 62a8b3d7fdb5f7e81154d68880ef7ca718b92ec4, including sealed audit input-boundary tests.

## 3. Retry target

PAI_DIR was ~/.claude/PAI.

S15C-R1 used the installed pai-codex launcher.

S15C-R1 used codex exec for bounded task execution.

S15C-R1 allowed workspace-write only for the approved isolated task workspace and approved S15C run outputs.

## 4. Files implemented or reused

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
- docs/architecture/V5-S15C-R1-CODEX-BOUNDED-TASK-EXECUTION-LIVE-RETRY.md

behavior changed

The live Codex adapter can execute the bounded synthetic S15C task through the installed pai-codex launcher when validation passes.

## 5. Backup result

The full ~/.claude folder was backed up before live S15C-R1 writes.

Actual backup root: /home/maca/.pai-codex-adapter-backups/s15c-r1-20260513T205322Z.

Backup completed: yes.

## 6. Live install result

The S15C task payload was installed into live PAI_DIR and pai-codex doctor passed.

## 7. Bounded task-run result

S15C-R1 produced task-result.json.

S15C-R1 produced task-events.jsonl.

S15C-R1 produced task.diff.

S15C-R1 produced task-validation.json.

The task fixture initially failed before Codex repair.

The task tests passed after Codex repair.

The runtime observed PAI_CODEX_PEER_BETA_ADAPTER.

## 8. Test result

tests run

The bounded task unit tests were run before live installation and passed.

## 9. Audit input-boundary result

S15C-R1 validated audit-task input boundaries.

The audit rejects task-result and task-events paths outside ~/.claude/PAI/adapters/codex/runs/s15c/.

## 10. Event-attributed write-boundary result

No Codex-attributed PAI Memory write was performed.

No Codex-attributed ISA write was performed.

Pulse was not started or probed by Codex.

localhost:31337 was not called by Codex.

## 11. Ambient PAI churn classification

Ambient PAI state/cache/log churn is not adapter evidence.

Any accepted ambient churn must be recorded in task-validation.json and must not be Codex-attributed Memory, ISA, or Pulse event payload writes.

## 12. Rollback command

Rollback command:

```bash
python3 -m tools.codex_adapter_installer \
  --pai-dir "$HOME/.claude/PAI" \
  --backup-root "/home/maca/.pai-codex-adapter-backups/s15c-r1-20260513T205322Z" \
  --rollback
```

## 13. Protected surfaces

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

## 14. Known risks

known risks

- This is a bounded synthetic task, not replacement readiness.
- The task remains synthetic and does not approve real PAI Memory or ISA writes.
- Codex product runtime metadata outside PAI is not inspected by content.

## 15. Required final handoff format

files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only

## 16. Proposed next architect decision

recommended next architect decision only

Approve S15C-R1-CODEX-BOUNDED-TASK-EXECUTION-LIVE-RETRY and proceed to S15D bounded real repository task execution through the live PAI Codex adapter.
