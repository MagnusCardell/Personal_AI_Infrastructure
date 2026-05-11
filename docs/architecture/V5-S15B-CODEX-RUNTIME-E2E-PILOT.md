# V5-S15B-CODEX-RUNTIME-E2E-PILOT: Live Codex Runtime Launcher and End-to-End PAI_DIR Execution Proof

## 1. Architect decision

S15B is approved as an implementation and runtime execution milestone.

Claude remains the official/full-support upstream adapter.
Codex remains peer beta.

## 2. Dependency on accepted S15A

S15B depends on accepted S15A at commit `ee2479a2122022ca72ddfed37be4b889902f5077`.

## 3. Runtime target

PAI_DIR was ~/.claude/PAI.
S15B installed a Codex runtime launcher into live PAI_DIR.
S15B ran Codex runtime from live PAI_DIR.
S15B used codex exec for non-interactive runtime proof.
The runtime proof observed PAI_CODEX_PEER_BETA_ADAPTER.

## 4. Files implemented

files changed

- `adapters/codex/AGENTS.md`
- `adapters/codex/README.md`
- `adapters/codex/adapter-manifest.json`
- `adapters/codex/bin/pai-codex`
- `adapters/codex/runtime-proof.schema.json`
- `tools/codex_adapter_installer/__main__.py`
- `tools/codex_adapter_installer/install.py`
- `tests/test_codex_adapter_runtime_e2e_pilot.py`
- `docs/architecture/V5-S15B-CODEX-RUNTIME-E2E-PILOT.md`

behavior changed

- A live Codex runtime launcher was installed at `~/.claude/PAI/adapters/codex/bin/pai-codex` during the S15B attempts.
- Codex was run non-interactively from live PAI_DIR.
- A runtime proof artifact was produced at `~/.claude/PAI/adapters/codex/runs/s15b/runtime-proof.json` during attempt 3.
- S15B was rolled back after post-marker live-write validation failed on the third runtime attempt.

## 5. Backup result

Backup root: `/home/maca/.pai-codex-adapter-backups/s15b-20260511T170118Z`.
Backup completed: yes.

## 6. Live runtime install result

Live runtime install validation passed: yes.
Number of live runtime attempts: 3.
Rollback needed: yes.
Rollback completed: yes, for approved S15B adapter targets.

## 7. Codex exec runtime proof result

Runtime proof passed: yes, during attempt 3 before rollback.
Runtime proof path: `~/.claude/PAI/adapters/codex/runs/s15b/runtime-proof.json`.
Codex exec ran from PAI_DIR: yes.
Adapter identity marker observed: yes.

## 8. Validation result

tests run

- Repository changed-path validation: pass.
- Protected repository path validation: pass.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_codex_adapter_runtime_e2e_pilot`: pass.
- Staged runtime payload validation: pass.
- S15B backup creation: pass.
- Runtime attempt 1 install and doctor: pass.
- Runtime attempt 1 proof validation: fail, proof had non-canonical field values and forbidden endpoint text.
- Runtime attempt 2 install and doctor: pass.
- Runtime attempt 2 exec-proof: fail, runtime rejected schema shape.
- Runtime attempt 3 install and doctor: pass.
- Runtime attempt 3 exec-proof: pass.
- Runtime attempt 3 runtime-proof artifact validation: pass.
- Post-marker live PAI write validation: fail, unapproved live PAI file mtimes were detected after the S15B marker.
- S15B rollback of approved adapter targets: pass.

## 9. Rollback command

Rollback command:

```bash
python3 -m tools.codex_adapter_installer \
  --pai-dir "$HOME/.claude/PAI" \
  --backup-root "/home/maca/.pai-codex-adapter-backups/s15b-20260511T170118Z" \
  --rollback
```

## 10. Protected surfaces

protected files changed yes/no

- No PAI Memory write was performed.
- No ISA write was performed.
- Pulse was not started or probed.
- localhost:31337 was not called.
- The runtime proof reported these protected-surface booleans as false.
- No repo root AGENTS.md was created.
- No repo .codex/ directory was created.
- No PAI adapter files were installed under ~/.codex.

Protected files changed: yes, by validation result. The post-marker scan observed unapproved live PAI file mtimes after the S15B marker in existing PULSE and MEMORY state/cache paths. The approved S15B adapter targets were rolled back.

## 11. Known risks

known risks

- This is a runtime proof milestone, not replacement readiness.
- A later Memory/ISA write policy milestone requires a separate architect-approved Goal Card.
- Runtime proof succeeded, but S15B acceptance did not pass because post-marker live-write validation failed on the third runtime attempt.
- A metadata-only check observed `/home/maca/.codex/config.toml` with an mtime after the S15B marker. Contents were not read. Treat this as a Codex product runtime side-effect risk for architect review, not as intentional PAI adapter installation under `~/.codex`.

## 12. Required final handoff format

goal state

The final handoff must use exactly these section labels:

```text
files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only
```

It must include actual backup root, rollback command, number of live runtime attempts, whether rollback was needed, whether runtime proof passed, runtime-proof.json path, whether PAI_CODEX_PEER_BETA_ADAPTER was observed, and whether Codex exec ran from PAI_DIR.

## 13. Proposed next architect decision

recommended next architect decision only

Request rollback/revision of S15B-CODEX-RUNTIME-E2E-PILOT before further runtime work.
