# V5-S16A-PAI-STATE-PROPOSAL-RUNTIME-CODEX: Controlled Memory/ISA Proposal Generation through PAI runtime=codex

## 1. Architect decision

S16A is approved as an implementation and live runtime milestone for proposal-only PAI state semantics.
S16A generated proposal-only Memory/ISA state updates through the live PAI runtime runner.
S16A does not authorize Memory writes, ISA writes, Pulse probing, Pulse event emission, Claude replacement, or Claude equivalence.

## 2. Dependency on accepted S15J

S16A depends on accepted S15J commit f821ec667b76cb83d13b91fe155bebe72b9f2979.
S15J proved that runtime=codex is installed, validated, peer beta, and controlled by the PAI runtime runner.

## 3. State proposal target

PAI_DIR was ~/.claude/PAI.
S16A used pai-runtime propose-state --runtime codex.
The PAI-owned run directory was ~/.claude/PAI/runs/s16a/state-proposal.

## 4. Files implemented

S16A implemented state proposal task, state context capsule, state proposal, and state proposal validation schemas.
S16A implemented proposal-only capability policy for memory.write.proposal and isa.write.proposal.
S16A implemented tools/pai_runtime_runner/state_proposal.py and wired propose-state plus audit-state-proposal into the PAI runtime runner.

## 5. Backup result

S16A created a fresh full local ~/.claude backup before live writes.
The actual backup root is reported in the final handoff.

## 6. Live install result

S16A installed the updated PAI runtime runner into live PAI_DIR only after backup.
pai-runtime doctor passed.
providers validate codex passed.

## 7. Context capsule result

PAI created a sanitized metadata-only state context capsule before invoking Codex.
Codex consumed the state context capsule rather than directly traversing live PAI state.
S16A produced state-context-capsule.json.

## 8. State proposal result

S16A produced state-proposal.json.
All Memory proposals are proposed_only.
All ISA proposals are proposed_only.
The runtime observed PAI_CODEX_PEER_BETA_ADAPTER.
Claude remains the official/full-support upstream adapter.
Codex remains peer beta.

## 9. Proposal-only validation result

S16A produced state-proposal-validation.json.
No PAI Memory file was modified.
No ISA file was modified.
No Pulse file was modified.
No PAI Memory body was read.
No ISA body was read.
No Pulse event payload was read.

## 10. Event-attributed validation result

S16A produced state-proposal-events.jsonl.
Pulse was not started or probed by Codex.
localhost:31337 was not called by Codex.
Event attribution passed for the proposal-only run.

## 11. Protected state surfaces

No repo root AGENTS.md was created.
No repo .codex/ directory was created.
No PAI adapter files were installed under ~/.codex.
Memory, ISA, Pulse, Claude project memory, and Codex memory remain protected surfaces.

## 12. Rollback command

The rollback command is reported in the final handoff.
Rollback is required only if live validation fails.

## 13. Known risks

S16A stores Memory/ISA proposals only as run artifacts and does not apply them.
A later proposal-approval or commit policy milestone requires a separate architect-approved Goal Card.
S16A does not prove replacement readiness or Claude equivalence.

## 14. Required final handoff format

files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only

## 15. Proposed next architect decision

Approve S16A-PAI-STATE-PROPOSAL-RUNTIME-CODEX and proceed to S16B proposal review/approval policy without Memory/ISA commit.
