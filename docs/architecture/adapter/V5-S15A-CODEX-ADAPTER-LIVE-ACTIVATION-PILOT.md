# V5-S15A-CODEX-ADAPTER-LIVE-ACTIVATION-PILOT: Backup, Install, Validate, and Iterate Codex Adapter Activation

## 1. Architect decision

S15A is approved as an implementation and live activation milestone for the Codex peer beta adapter router.

Claude remains the official/full-support upstream adapter.
Codex remains peer beta.

## 2. Activation target

PAI_DIR was ~/.claude/PAI.
S15A installed the Codex peer beta adapter router into live PAI_DIR.

## 3. Files implemented

files changed

- `adapters/codex/AGENTS.md`
- `adapters/codex/README.md`
- `adapters/codex/adapter-manifest.json`
- `tools/codex_adapter_installer/__init__.py`
- `tools/codex_adapter_installer/__main__.py`
- `tools/codex_adapter_installer/install.py`
- `tests/test_codex_adapter_activation_installer.py`
- `docs/architecture/V5-S15A-CODEX-ADAPTER-LIVE-ACTIVATION-PILOT.md`

behavior changed

- A live Codex peer beta adapter router is installed at `~/.claude/PAI/AGENTS.md`.
- Codex adapter metadata is installed at `~/.claude/PAI/adapters/codex/`.

## 4. Backup result

The full ~/.claude folder was backed up before live writes.

Backup root: `/home/maca/.pai-codex-adapter-backups/s15a-20260511T154401Z`.
Backup completed: yes.

## 5. Live install result

Live install validation passed: yes.
Number of live install attempts: 1.
Rollback needed: no.

## 6. Validation result

tests run

- `python3` repository changed-path validation: pass.
- `python3` protected repository path validation: pass.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_codex_adapter_activation_installer`: pass.
- `python3` staged Codex adapter payload validation: pass.
- `python3 -m tools.codex_adapter_installer --apply`: pass.
- `python3 -m tools.codex_adapter_installer --validate`: pass.
- live post-marker approved-write validation: pass.
- live installer idempotence validation: pass.

The staged payload validator confirmed the compact router and peer beta manifest criteria.
The live installer validator confirmed installed files match staged payload criteria.
The idempotence validator confirmed repeated installer apply and validate passes.

## 7. Rollback command

Rollback command:

```bash
python3 -m tools.codex_adapter_installer \
  --pai-dir "$HOME/.claude/PAI" \
  --backup-root "/home/maca/.pai-codex-adapter-backups/s15a-20260511T154401Z" \
  --rollback
```

## 8. Protected surfaces

protected files changed yes/no

- No repo root AGENTS.md was created.
- No repo .codex/ directory was created.
- No ~/.codex write was performed.
- No PAI Memory write was performed.
- No ISA write was performed.
- Pulse was not started or probed.
- localhost:31337 was not called.
- Claude Code was not invoked.
- Codex runtime was not invoked.

Protected files changed: no.

## 9. Known risks

known risks

- This is a router activation milestone, not a runtime smoke milestone.
- A later runtime smoke milestone requires a separate architect-approved Goal Card.
- Codex remains peer beta and is not replacement-grade.

## 10. Required final handoff format

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

It must include actual backup root, rollback command, number of live install attempts, whether rollback was needed, and whether live install validation passed.

## 11. Proposed next architect decision

recommended next architect decision only

Approve S15A-CODEX-ADAPTER-LIVE-ACTIVATION-PILOT and proceed to S15B live Codex runtime smoke from PAI_DIR.
