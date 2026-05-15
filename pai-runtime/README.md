# PAI Runtime Runner

S15D introduces a PAI-owned runtime runner. PAI owns run directories, task cards,
schemas, validation, and Memory/ISA/Pulse policy. Runtime providers execute
bounded work under PAI control.

The first provider is `codex`, registered as peer beta. Claude remains the
official/full-support upstream adapter.

S15E adds bounded real-repository execution through:

```bash
pai-runtime run-repo --runtime codex
```

The first real repository task is the PAI runtime provider registry. It remains
bounded to an approved repository write set and emits `repo-run-result.json`,
`repo-events.jsonl`, `repo-task.diff`, and `repo-run-validation.json` under a
PAI-owned run directory.

S15F adds a PAI-owned patch proposal path for real repository tasks. Codex
returns a structured full-file replacement proposal, PAI writes
`patch-proposal.json`, validates every proposed path against the approved
repository write set, and only then materializes the replacement files. The
runtime remains `codex` peer beta; Claude remains the official/full-support
upstream adapter.

S15I adds repository support for a read-only PAI metadata context task through:

```bash
pai-runtime run-pai-context --runtime codex
```

PAI collects bounded live metadata, writes a sanitized context capsule, and
invokes `runtime=codex` only over that capsule inside a PAI-owned run
directory. Codex does not receive authority to traverse live PAI Memory, ISA,
Pulse, Claude project memory, Codex memory, or arbitrary home files. The
intended run emits `pai-context-capsule.json`, `pai-context-report.json`, and
`pai-context-events.jsonl`. The paired `audit-pai-context` command validates
the run and writes `pai-context-validation.json`.

S15I-R1 completed the read-only PAI metadata context task with a
Codex-compatible provider-facing schema and PAI-owned semantic validation.

S15J adds an executable closeout gate through:

```bash
pai-runtime beta-readiness --runtime codex
```

The gate verifies provider lifecycle, capability policy, patch proposal policy,
read-only PAI context policy, event attribution, and protected surfaces. It
emits `beta-readiness-result.json`, `beta-readiness-events.jsonl`,
`beta-readiness-validation.json`, and `evidence-index.json` under a PAI-owned
S15J run directory. The gate preserves the S15 boundary: Codex remains
peer beta, Claude remains the official/full-support upstream adapter, and no
replacement-readiness or Claude-equivalence claim is made.

S16A adds proposal-only PAI state semantics through:

```bash
pai-runtime propose-state --runtime codex
```

PAI collects a sanitized metadata-only state context capsule, invokes
`runtime=codex` only over that capsule, and stores structured Memory/ISA
proposals under the S16A run directory. The proposals are not applied to Memory
or ISA. The paired `audit-state-proposal` command validates that all proposal
entries have `apply_status=proposed_only`, that no Memory, ISA, or Pulse files
were modified, and that Codex remains a peer-beta runtime provider rather than a
replacement-grade adapter.
