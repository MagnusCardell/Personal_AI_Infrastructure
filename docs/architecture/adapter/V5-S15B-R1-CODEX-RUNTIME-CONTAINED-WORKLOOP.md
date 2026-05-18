# V5-S15B-R1-CODEX-RUNTIME-CONTAINED-WORKLOOP: Contained Live Codex Runtime Proof and First Adapter Work-Loop Artifact

## 1. Architect decision

Approved as an implementation and live runtime milestone replacing the blocked S15B Goal Card. This milestone is not replacement readiness.

## 2. Dependency on accepted S15A and blocked S15B evidence

S15B-R1 depends on V5-S15A-CODEX-ADAPTER-LIVE-ACTIVATION-PILOT accepted at commit `ee2479a2122022ca72ddfed37be4b889902f5077`.

It incorporates the blocked S15B evidence that Codex exec ran from live PAI_DIR, PAI_CODEX_PEER_BETA_ADAPTER was observed, the runtime proof passed before rollback, and the prior validation failed because the write-boundary model was too broad for the runtime path.

## 3. Runtime target

S15B-R1 installed a contained Codex runtime launcher into live PAI_DIR.

PAI_DIR was ~/.claude/PAI.

The launcher target is `~/.claude/PAI/adapters/codex/bin/pai-codex`.

## 4. Files implemented

files changed

- `adapters/codex/AGENTS.md`
- `adapters/codex/README.md`
- `adapters/codex/adapter-manifest.json`
- `adapters/codex/bin/pai-codex`
- `adapters/codex/runtime-proof.schema.json`
- `adapters/codex/workloop-once.schema.json`
- `tools/codex_adapter_installer/__main__.py`
- `tools/codex_adapter_installer/install.py`
- `tests/test_codex_adapter_runtime_contained_workloop.py`
- `docs/architecture/V5-S15B-R1-CODEX-RUNTIME-CONTAINED-WORKLOOP.md`

## 5. Backup result

The full `~/.claude` folder is backed up before live S15B-R1 writes.

Actual backup root:

`/home/maca/.pai-codex-adapter-backups/s15b-r1-20260511T181058Z`

Backup completed: yes.

## 6. Live runtime install result

S15B-R1 installed a contained Codex runtime launcher into live PAI_DIR during live runtime attempts.

The installed launcher supports `doctor`, `exec-proof`, and `workloop-once`.

Final live state after failed validation: rolled back. The S15B-R1 live runtime launcher was not left installed.

## 7. Codex exec runtime proof result

S15B-R1 ran Codex runtime from live PAI_DIR.

S15B-R1 used codex exec for non-interactive runtime proof.

The runtime proof observed PAI_CODEX_PEER_BETA_ADAPTER.

Claude remains the official/full-support upstream adapter.

Codex remains peer beta.

Runtime proof result before rollback: passed.

## 8. Work-loop artifact result

S15B-R1 produced a bounded workloop-once artifact.

The work-loop artifact is a bounded read-only adapter decision artifact and not a Memory, ISA, or Pulse writer.

Work-loop artifact result before rollback: passed.

## 9. Live write-boundary validation result

No PAI Memory write was performed.

No ISA write was performed.

Pulse was not started or probed.

localhost:31337 was not called.

No repo root AGENTS.md was created.

No repo .codex/ directory was created.

No PAI adapter files were installed under ~/.codex.

Live write-boundary validation result: failed after three live runtime attempts. The validation detected post-marker changes under live PAI `PULSE` and `MEMORY` state/cache/log paths outside the approved S15B-R1 live targets.

Rollback was required and completed.

## 10. Rollback command

Rollback command shape:

```bash
python3 -m tools.codex_adapter_installer \
  --pai-dir "$HOME/.claude/PAI" \
  --backup-root "/home/maca/.pai-codex-adapter-backups/s15b-r1-20260511T181058Z" \
  --rollback
```

The actual rollback command was run.

## 11. Protected surfaces

The S15B-R1 runtime does not approve Memory writes, ISA writes, Pulse integration, root repository AGENTS.md, repo .codex/, PAI adapter files under ~/.codex, hooks, rules, skills, agents, commands, or launchers outside the approved adapter launcher.

A later Memory/ISA write policy milestone requires a separate architect-approved Goal Card.

protected files changed yes/no

## 12. Known risks

known risks

The runtime proof and work-loop artifacts passed before rollback, but S15B-R1 is blocked because live write-boundary validation failed after the third allowed runtime attempt.

The validation reported post-marker PAI state/cache/log changes outside the approved S15B-R1 live targets. The live runtime was rolled back as required.

The runtime proof and work-loop artifacts are bounded runtime evidence. They are not Claude equivalence, replacement readiness, or approval for Memory, ISA, or Pulse writes.

Codex runtime may read its own product authentication or configuration state. S15B-R1 does not install PAI adapter files under ~/.codex.

## 13. Required final handoff format

files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only

## 14. Proposed next architect decision

recommended next architect decision only

Request rollback/revision of S15B-R1-CODEX-RUNTIME-CONTAINED-WORKLOOP before further runtime work.
