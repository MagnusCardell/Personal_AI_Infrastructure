# V5-S15D-PAI-RUNTIME-RUNNER-CODEX: Promote Codex from Adapter-local Execution to PAI Runtime Provider

## 1. Architect decision

S15D promotes Codex from adapter-local execution to a PAI-owned runtime provider model.

This is an implementation and live runtime milestone. It is not a documentation-only milestone, not a smoke test, and not replacement readiness.

## 2. Dependency on accepted S15C-R1

S15D depends on the accepted S15C-R1 live retry state.

S15D started from committed S15C-R1 base `64e15bcf95e763d93410065e6f8e6fc887367d5e`.

## 3. Runtime-runner target

S15D installed a PAI-owned runtime runner into live PAI_DIR.

PAI_DIR was ~/.claude/PAI.

S15D registered Codex as runtime provider codex.

The target command is `pai-runtime run --runtime codex`, with PAI owning the task card, run directory, artifacts, validation, and Memory/ISA/Pulse policy.

## 4. Files implemented

The milestone implements the PAI runtime runner package, the Codex runtime provider manifest, PAI-owned run schemas, a synthetic bounded task fixture, runtime audit logic, and tests for the PAI-owned runtime model.

S15D uses the installed Codex provider driver.

## 5. Backup result

The full local `~/.claude` backup completed before live S15D writes.

Backup root: `/home/maca/.pai-codex-adapter-backups/s15d-20260513T214629Z`.

## 6. Live install result

The live S15D runtime runner was installed into `~/.claude/PAI/bin/pai-runtime`.

`pai-runtime doctor` passed on live PAI_DIR.

## 7. PAI-owned run result

S15D used pai-runtime run --runtime codex.

S15D created a PAI-owned run directory under ~/.claude/PAI/runs/s15d/.

S15D produced run-result.json.

S15D produced runtime-events.jsonl.

S15D produced task.diff.

S15D produced run-validation.json.

The task fixture initially failed before Codex repair.

The task tests passed after Codex repair.

The live run passed on attempt 2.

## 8. Codex provider invocation result

S15D used the installed Codex provider driver.

The runtime observed PAI_CODEX_PEER_BETA_ADAPTER.

Claude remains the official/full-support upstream adapter.

Codex remains peer beta.

## 9. Test result

Synthetic tests cover provider manifest policy, PAI-owned install, doctor, run delegation, unknown runtime rejection, run directory boundary rejection, audit acceptance, audit rejection for Memory/ISA/Pulse/localhost/out-of-bound writes, ambient churn classification, and repo governance surface protection.

## 10. Event-attributed write-boundary result

No Codex-attributed PAI Memory write was performed.

No Codex-attributed ISA write was performed.

Pulse was not started or probed by Codex.

localhost:31337 was not called by Codex.

No repo root AGENTS.md was created.

No repo .codex/ directory was created.

No PAI adapter files were installed under ~/.codex.

Event attribution passed with no forbidden semantic writes and no unknown unclassified writes.

## 11. Ambient PAI churn classification

Ambient PAI state/cache/log churn is not adapter evidence.

Ambient churn is accepted only when Codex event attribution remains clean and the changed paths are not Memory WORK/LEARNING/KNOWLEDGE content, ISA content, or Pulse event payloads.

The live audit observed ambient PAI churn and classified it as non-evidence.

## 12. Rollback command

Rollback command:

```bash
python3 -m tools.pai_runtime_runner --pai-dir "$HOME/.claude/PAI" --backup-root "/home/maca/.pai-codex-adapter-backups/s15d-20260513T214629Z" --rollback
```

## 13. Protected surfaces

S15D does not approve writes to PAI Memory, ISA, Pulse event payloads, Claude project memory, root repository `AGENTS.md`, repository `.codex/`, Codex native adapter install surfaces under `~/.codex`, hooks, rules, skills, agents, commands, Pulse bridge, PAI Memory writer, or ISA writer.

A later real repository task or Memory/ISA write policy milestone requires a separate architect-approved Goal Card.

## 14. Known risks

The task is synthetic and bounded. It proves that the PAI runner can invoke runtime provider codex for one contained repair, but it does not prove Claude equivalence, replacement readiness, real repository task policy, or Memory/ISA write policy.

## 15. Required final handoff format

files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only

## 16. Proposed next architect decision

Approve S15D-PAI-RUNTIME-RUNNER-CODEX and proceed to S15E bounded real repository task through PAI runtime=codex.
