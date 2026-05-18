# V5-S16D-PAI-STATE-SINGLE-PROPOSAL-SHADOW-COMMIT: Single-Proposal Memory/ISA Commit Policy with Shadow Apply Only

## 1. Architect decision

S16D was approved as an implementation and live runtime milestone.

S16D selected exactly one Memory/ISA dry-run candidate through the live PAI runtime runner.

## 2. Dependency on accepted S16C

S16D depends on accepted S16A at e4af71415394d0bdc7c90dad925f3d3c9bcbccba, accepted S16B at c84305f5781a87b8e9a3b75f636d73270f4a2cd5, and accepted S16C at 9a8cd629def32a282c49930b34bbdf55430fe812.

S16D consumed the accepted S16C dry-run plan artifact.

## 3. Shadow commit target

PAI_DIR was ~/.claude/PAI.

S16D used pai-runtime shadow-apply-state-commit --runtime codex.

S16D required the exact human gate S16D_SHADOW_APPLY_ONLY_NO_LIVE_MEMORY_ISA_WRITE.

Exactly one candidate was selected.

The selected target path was relative.

The selected target path was allowed.

The shadow target was written under the S16D run directory.

No commit authority was granted.

No commit was performed.

## 4. Files implemented

The repository implementation adds the S16D task schema, policy review schema, selected candidate schema, shadow apply result schema, validation schema, task card, shadow commit module, runner command, provider invocation, install policy, focused tests, and this activation note.

files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only

## 5. Backup result

A full local backup is required before live install.

Actual backup root: /home/maca/.pai-codex-adapter-backups/s16d-20260516T210208Z.

## 6. Live install result

The live install updates only the S16D-approved PAI runtime launcher, runtime state, S16D runtime schemas, S16D task card, and Codex provider manifest.

No PAI adapter files were installed under ~/.codex.

## 7. Source dry-run plan result

S16D consumed the accepted S16C dry-run plan artifact.

The source plan remains the authority for candidate writes and is not altered by S16D.

## 8. Human gate result

S16D required the exact human gate S16D_SHADOW_APPLY_ONLY_NO_LIVE_MEMORY_ISA_WRITE.

The gate authorizes shadow apply only and does not authorize Memory writes, ISA writes, Pulse probing, or Pulse events.

## 9. Single-candidate selection result

S16D produced selected-commit-candidate.json.

Exactly one candidate was selected.

The selected target path was relative.

The selected target path was allowed.

## 10. Shadow apply result

S16D produced shadow-apply-result.json.

The shadow target was written under the S16D run directory.

No commit authority was granted.

No commit was performed.

## 11. Non-commit validation result

S16D produced shadow-commit-validation.json.

No PAI Memory file was modified.

No ISA file was modified.

No Pulse file was modified.

No PAI Memory body was read.

No ISA body was read.

No Pulse event payload was read.

## 12. Event-attributed validation result

S16D produced shadow-commit-events.jsonl.

PAI created a sanitized metadata-only shadow commit context capsule before invoking Codex.

Codex consumed the shadow commit context capsule rather than directly traversing live PAI state.

S16D produced shadow-commit-context-capsule.json.

S16D produced single-proposal-policy-review.json.

Pulse was not started or probed by Codex.

localhost:31337 was not called by Codex.

The runtime observed PAI_CODEX_PEER_BETA_ADAPTER.

Claude remains the official/full-support upstream adapter.

Codex remains peer beta.

## 13. Protected state surfaces

No repo root AGENTS.md was created.

No repo .codex/ directory was created.

No PAI adapter files were installed under ~/.codex.

Memory, ISA, Pulse, Claude product state, Codex product state, repository root AGENTS.md, and repository .codex/ remain protected from S16D writes.

## 14. Rollback command

Rollback command shape:

```bash
python3 -m tools.pai_runtime_runner \
  --pai-dir "$HOME/.claude/PAI" \
  --backup-root "/home/maca/.pai-codex-adapter-backups/s16d-20260516T210208Z" \
  --rollback
```

## 15. Known risks

Filesystem mtime scanning remains a secondary detector for forbidden state writes.

Codex JSONL event attribution remains the primary provider-side event signal.

A later actual single-proposal commit milestone requires a separate architect-approved Goal Card.

## 16. Required final handoff format

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

## 17. Proposed next architect decision

Approve S16D-PAI-STATE-SINGLE-PROPOSAL-SHADOW-COMMIT and proceed to S16E actual single-proposal commit with explicit human gate.
