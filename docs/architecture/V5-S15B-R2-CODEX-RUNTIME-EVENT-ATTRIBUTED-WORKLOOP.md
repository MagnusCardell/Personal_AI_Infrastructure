# V5-S15B-R2-CODEX-RUNTIME-EVENT-ATTRIBUTED-WORKLOOP: Contained Live Codex Runtime with Event-Attributed Write Boundary

## 1. Architect decision

Approved as an implementation and live runtime milestone.

S15B-R2 installed a contained Codex runtime launcher into live PAI_DIR.

## 2. Dependency on accepted S15A and blocked S15B/S15B-R1 evidence

S15B-R2 depends on V5-S15A-CODEX-ADAPTER-LIVE-ACTIVATION-PILOT accepted at commit ee2479a2122022ca72ddfed37be4b889902f5077.

S15B-R2 incorporates blocked evidence from S15B commit 1e55f957c729841d58cfb658f1c1ca78ffe63d1f and S15B-R1 commit 356b521bc1cb72722fed2cc6921fc37085006615.

## 3. Runtime target

PAI_DIR was ~/.claude/PAI.

S15B-R2 ran Codex runtime from live PAI_DIR.

S15B-R2 used codex exec for non-interactive runtime proof.

S15B-R2 captured Codex JSONL event streams.

S15B-R2 produced a bounded workloop-once artifact.

## 4. Files implemented

files changed

- adapters/codex/AGENTS.md
- adapters/codex/README.md
- adapters/codex/adapter-manifest.json
- adapters/codex/bin/pai-codex
- adapters/codex/runtime-proof.schema.json
- adapters/codex/workloop-once.schema.json
- adapters/codex/runtime-validation.schema.json
- tools/codex_adapter_installer/__main__.py
- tools/codex_adapter_installer/install.py
- tools/codex_adapter_installer/runtime_audit.py
- tests/test_codex_adapter_runtime_event_attribution.py
- docs/architecture/V5-S15B-R2-CODEX-RUNTIME-EVENT-ATTRIBUTED-WORKLOOP.md

behavior changed

The live adapter launcher supports doctor, exec-proof, workloop-once, and audit-run. Runtime proof and work-loop commands capture Codex JSONL event streams for event-attributed write-boundary validation.

## 5. Backup result

The full ~/.claude folder was backed up before live S15B-R2 writes.

Actual backup root: /home/maca/.pai-codex-adapter-backups/s15b-r2-20260513T191649Z.

Backup completed: yes.

## 6. Live runtime install result

The live runtime launcher target is ~/.claude/PAI/adapters/codex/bin/pai-codex.

The live run directory is ~/.claude/PAI/adapters/codex/runs/s15b-r2/.

Live runtime install validation passed.

Number of live runtime attempts: 1.

Rollback needed: no.

Live runtime remains installed: yes.

## 7. Codex exec runtime proof result

The runtime proof observed PAI_CODEX_PEER_BETA_ADAPTER.

Runtime proof artifact: ~/.claude/PAI/adapters/codex/runs/s15b-r2/runtime-proof.json.

Runtime event stream: ~/.claude/PAI/adapters/codex/runs/s15b-r2/runtime-events.jsonl.

Runtime proof passed: yes.

Codex exec ran from PAI_DIR: yes.

## 8. Work-loop artifact result

Work-loop artifact: ~/.claude/PAI/adapters/codex/runs/s15b-r2/workloop-once.json.

Work-loop event stream: ~/.claude/PAI/adapters/codex/runs/s15b-r2/workloop-events.jsonl.

workloop-once passed: yes.

## 9. Event-attributed write-boundary result

Runtime validation artifact: ~/.claude/PAI/adapters/codex/runs/s15b-r2/runtime-validation.json.

Event attribution passed: yes.

No Codex-attributed PAI Memory write was performed.

No Codex-attributed ISA write was performed.

Pulse was not started or probed by Codex.

localhost:31337 was not called by Codex.

## 10. Ambient PAI churn classification

Ambient PAI state/cache/log churn is not adapter evidence.

Any accepted ambient churn must be reported in runtime-validation.json and must not be Codex-attributed Memory, ISA, or Pulse event payload writes.

Ambient PAI churn observed: yes.

## 11. Rollback command

Rollback command:

```bash
python3 -m tools.codex_adapter_installer \
  --pai-dir "$HOME/.claude/PAI" \
  --backup-root "/home/maca/.pai-codex-adapter-backups/s15b-r2-20260513T191649Z" \
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

A later Memory/ISA write policy milestone requires a separate architect-approved Goal Card.

protected files changed yes/no

Protected files changed: no.

## 13. Known risks

known risks

- Codex JSONL event attribution is the primary write-boundary signal, but Codex product runtime metadata outside PAI is not inspected by content.
- Filesystem mtime scanning remains a secondary detector and can identify ambient PAI state/cache/log churn that is not adapter evidence.
- This milestone is non-canonical runtime evidence and is not replacement readiness.

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

Approve S15B-R2-CODEX-RUNTIME-EVENT-ATTRIBUTED-WORKLOOP and proceed to S15C bounded Codex adapter task execution.
