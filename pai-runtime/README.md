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

The S15I repository payload is not accepted live evidence by itself. The first
live S15I validation batch exhausted the three-attempt policy and rolled back;
a later live revision attempt requires separate architect approval.
