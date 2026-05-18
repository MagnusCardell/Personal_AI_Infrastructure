# V5-S15I-R1-PAI-CONTEXT-SCHEMA-COMPAT-LIVE-RETRY: Retry Read-Only PAI Context Task with Codex-Compatible Provider Schema

## 1. Architect decision

S15I-R1 is approved as a narrow live retry of the blocked S15I read-only PAI metadata context task. It does not authorize S15J beta-readiness, Memory/ISA proposal policy, Pulse integration, or broader adapter replacement work.

## 2. Dependency on blocked S15I evidence

S15I-R1 depends on blocked S15I repair evidence at `247d55e5cc0c445b7cc22fd57e4485c05ffe492c`.

## 3. Schema compatibility repair

S15I-R1 retried the read-only PAI metadata context task with a Codex-compatible provider-facing schema. S15I-R1 removed unsupported provider-facing schema composition from the Codex output path. PAI performs semantic validation after Codex output.

## 4. Read-only PAI context target

PAI_DIR was ~/.claude/PAI. S15I-R1 used pai-runtime run-pai-context --runtime codex. PAI created a sanitized context capsule before invoking Codex. Codex consumed the context capsule rather than directly traversing live PAI state.

## 5. Files implemented or reused

S15I-R1 reused the S15I implementation and adds the R1 run note plus schema-compatibility tests in the approved repository write set.

files changed

Implemented or reused files:

| Path | Role |
| --- | --- |
| `pai-runtime/pai-context-report.schema.json` | provider-facing Codex-compatible report shape |
| `tools/pai_runtime_runner/pai_context.py` | PAI-owned report semantic validation |
| `tests/test_pai_runtime_readonly_pai_context.py` | S15I and S15I-R1 repository tests |
| `docs/architecture/V5-S15I-R1-PAI-CONTEXT-SCHEMA-COMPAT-LIVE-RETRY.md` | S15I-R1 live retry note |

## 6. Backup result

Backup root: `/home/maca/.pai-codex-adapter-backups/s15i-r1-20260515T181553Z`.

Backup completed: yes.

## 7. Live install result

The updated PAI runtime runner was installed into `~/.claude/PAI/bin/pai-runtime`. `pai-runtime doctor` passed. `pai-runtime providers validate codex` passed. `pai-runtime run-pai-context --runtime codex` passed. The live PAI runtime runner remains installed because validation passed.

## 8. Context capsule result

S15I-R1 produced pai-context-capsule.json.

Artifact path: `~/.claude/PAI/runs/s15i/read-only-pai-context/pai-context-capsule.json`.

The context capsule contained metadata only.

## 9. Codex context report result

S15I-R1 produced pai-context-report.json.

Artifact path: `~/.claude/PAI/runs/s15i/read-only-pai-context/pai-context-report.json`.

The context report passed schema validation and PAI-owned semantic validation.

The runtime observed PAI_CODEX_PEER_BETA_ADAPTER. Claude remains the official/full-support upstream adapter. Codex remains peer beta.

## 10. Event-attributed validation result

S15I-R1 produced pai-context-events.jsonl.

Artifact path: `~/.claude/PAI/runs/s15i/read-only-pai-context/pai-context-events.jsonl`.

S15I-R1 produced pai-context-validation.json.

Artifact path: `~/.claude/PAI/runs/s15i/read-only-pai-context/pai-context-validation.json`.

Event attribution passed. `pai-context-validation.json` reported `validation_passed: true`.

## 11. Sensitive-data boundary result

No PAI Memory body was read. No ISA body was read. No Pulse event payload was read. No Claude project memory was read. No Codex memory was read. No Codex-attributed PAI Memory write was performed. No Codex-attributed ISA write was performed. Pulse was not started or probed by Codex. localhost:31337 was not called by Codex.

No forbidden semantic writes were reported. No unknown unclassified writes were reported.

## 12. Ambient PAI churn classification

Ambient PAI state/cache/log churn is not adapter evidence.

Observed ambient churn was limited to redacted PAI state/cache paths and was not adapter evidence.

## 13. Rollback command

Rollback was not needed because validation passed. Manual rollback command:

```bash
python3 -m tools.pai_runtime_runner \
  --pai-dir "$HOME/.claude/PAI" \
  --backup-root "/home/maca/.pai-codex-adapter-backups/s15i-r1-20260515T181553Z" \
  --rollback
```

## 14. Protected surfaces

No repo root AGENTS.md was created. No repo .codex/ directory was created. No PAI adapter files were installed under ~/.codex.

## 15. Known risks

S15I-R1 is a narrow live retry of a provider-facing schema compatibility repair. It does not establish S15J beta-readiness and does not grant Memory/ISA proposal authority. A later Memory/ISA proposal policy milestone requires a separate architect-approved Goal Card.

known risks

## 16. Required final handoff format

files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only

## 17. Proposed next architect decision

Approve S15I-R1-PAI-CONTEXT-SCHEMA-COMPAT-LIVE-RETRY and proceed to S15J Codex beta-readiness gate.
