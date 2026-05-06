# V5-S10F Execution Plan

## Purpose

Execute V5-S10F No-Residue and Determinism Guard for the fixture-only Codex adapter validation track. S10F validates that the existing read-only fixture harness can be executed in-process repeatedly without changing fixture content, creating repository residue, or destabilizing its stdout report shape.

Codex is not currently proven drop-in for existing local PAI v5 files. S10F validates determinism and no-residue behavior only; it does not implement or authorize a runtime adapter, live trial, Pulse bridge, Memory writer, ISA writer, Codex surface, or migration path.

## Scope

In scope:

- Create this S10F execution plan.
- Create a standard-library no-residue determinism self-test for the approved fixture root.
- Add an S10F section to the fixture-trial README.
- Optionally adjust the existing read-only harness only if required to support deterministic, no-write validation without weakening S10A through S10E guarantees.
- Run the required validation commands and record results.

Out of scope:

- Runtime adapter implementation.
- Live read-only trials.
- Existing-local-v5 access.
- Private user-local reads.
- Pulse startup or endpoint calls.
- PAI Memory or ISA writes.
- Root `AGENTS.md`, `.codex/`, runtime payloads, manifests, audit artifacts, executable schemas, live-trial artifacts, Memory payloads, ISA payloads, or Pulse payloads.

## Approved Write Set

Required new files:

- `docs/adapters/V5_S10F_EXEC_PLAN.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py`

Required modified file:

- `tests/adapters/v5-codex-readonly-fixture-trial/README.md`

Optional modified file only if required:

- `tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py`

No fixture metadata, fixture case data, fixture README, or existing S10B/S10E self-test file may be modified in S10F.

## Protected Paths

Protected paths remain unchanged:

- `Releases/`
- `Releases/v5.0.0/`
- `Releases/v5.0.0/.claude/`
- `.claude/`
- `PAI/`
- `CLAUDE.md`
- `AGENTS.md`
- `.codex/`
- `install.sh`
- `PAI_SYSTEM_PROMPT.md`
- `settings.json`
- `hooks/`
- `skills/`
- `subagents/`
- `agents/`
- `commands/`
- `.github/`
- `.agents/`

Private user-local state remains forbidden:

- `~/.claude/`
- `~/.claude/PAI/`
- `~/.claude/projects/`
- `~/.codex/`
- `~/.codex/memories/`

## Source Protocol

Allowed sources:

- S10F handoff prompt and Completion Contract.
- Existing repository-local S10A through S10E adapter docs and fixture-trial harness files as needed.
- Existing fixture corpus metadata and case data only as read-only fixture-test material.

Forbidden sources and operations:

- Live `~/.claude`, `~/.codex`, or other private user-local state.
- Pulse startup, Pulse endpoint calls, or `localhost:31337` probes.
- Claude Code invocation.
- Codex runtime invocation.
- Codex import or migration tooling.
- Installers.
- Network sources.

## Source Material

Baseline evidence reviewed or validated:

- `tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py`
- `tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`
- `tests/adapters/v5-codex-readonly-fixture-trial/README.md`
- `tests/adapters/v5-codex-readonly-fixture-trial/fixtures/`

Baseline commands already run before S10F edits:

- `git status --short`: no output.
- `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures`: pass.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`: pass with `negative_control_count: 60`.

## Completion Contract

The S10F Completion Contract is copied below in quoted form to preserve the required execution-plan H1/H2 sequence while retaining the contract text.

> ## Completion Contract
>
> Copy this entire Completion Contract into `docs/adapters/V5_S10F_EXEC_PLAN.md`.
>
> ### Required conclusions
>
> S10F must preserve:
>
> * Codex is not currently proven drop-in for existing local PAI v5 files.
> * S10F validates determinism and no-residue behavior only.
> * S10F does not implement a runtime adapter.
> * S10F does not create root `AGENTS.md`, `.codex/`, runtime payload, manifest, audit artifact, executable schema, live-trial artifact, Memory payload, ISA payload, or Pulse payload.
> * Harness stdout is not an audit artifact.
> * Fixture metadata and case data are not manifests.
> * Pulse is not started or called.
> * Live user-local state is not read.
> * PAI Memory and ISA are not written.
>
> ### Required execution-plan headings
>
> `docs/adapters/V5_S10F_EXEC_PLAN.md` must contain exactly:
>
> ```markdown
> # V5-S10F Execution Plan
> ## Purpose
> ## Scope
> ## Approved Write Set
> ## Protected Paths
> ## Source Protocol
> ## Source Material
> ## Completion Contract
> ## Milestones
> ## Self-Review Rubric
> ## Hard Failure Conditions
> ## Validation Commands
> ## Progress
> ## Iteration Log
> ## Surprises & Discoveries
> ## Decision Log
> ## Outcomes & Retrospective
> ```
>
> ### Required no-residue self-test
>
> Create:
>
> ```text
> tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py
> ```
>
> The script must use only the Python standard library.
>
> The script must:
>
> * set `sys.dont_write_bytecode = True`;
> * import the harness without creating `__pycache__`;
> * compute deterministic content digests for the fixture root before and after harness execution;
> * execute the harness in-process at least twice against the approved fixture root;
> * capture stdout in memory;
> * prove both executions return success;
> * prove fixture tree content digests are unchanged;
> * prove no `__pycache__`, `.pyc`, or temporary artifacts are left in the repository;
> * prove harness output has stable required fields;
> * emit stdout only;
> * exit `0` when all checks pass;
> * exit non-zero on failure.
>
> The script must not:
>
> * use subprocesses;
> * use network access;
> * read release files;
> * read user-local state;
> * invoke Claude Code;
> * invoke Codex;
> * start Pulse;
> * call Pulse endpoints;
> * probe `localhost:31337`;
> * write files inside the repository.
>
> The report must include:
>
> ```text
> S10F no-residue determinism report
> first_run_status
> second_run_status
> fixture_digest_stable
> stdout_shape_stable
> repository_residue_status
> status
> ```
>
> ### Required README update
>
> Add an S10F section explaining:
>
> * S10F validates deterministic, no-residue harness behavior.
> * S10F does not create audit artifacts.
> * S10F does not run Codex, Claude Code, Pulse, or live trials.
> * S10F does not read live user-local state.
> * S10F does not write PAI Memory or ISA.
> * Codex is not currently proven drop-in for existing local PAI v5 files.
>
> ### Hard failures
>
> S10F fails if:
>
> * Any file outside the approved write set changes.
> * Fixture files change.
> * Any protected path changes.
> * The no-residue script, harness, or self-test uses non-stdlib dependencies, subprocesses, or network access.
> * Any script writes files in the repository.
> * `__pycache__`, `.pyc`, or temporary artifacts remain.
> * Pulse is started or called.
> * Claude Code or Codex runtime is invoked.
> * Live user-local state is read.
> * PAI Memory or ISA is written.
> * Any deliverable claims Codex is drop-in today or official upstream engine.
> * Any deliverable authorizes live trials, runtime adapter work, Memory writes, ISA writes, Pulse implementation, product-memory promotion, or dual-engine uncoordinated writes.
>
> ### Required validation commands
>
> Run:
>
> ```bash
> git status --short
> git diff --name-only | sort
> git diff --check
> python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py
> PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py
> ```
>
> Run changed-file check:
>
> ```bash
> python3 - <<'PY'
> import subprocess
> allowed = {
>     "docs/adapters/V5_S10F_EXEC_PLAN.md",
>     "tests/adapters/v5-codex-readonly-fixture-trial/README.md",
>     "tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py",
>     "tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py",
> }
> required = {
>     "docs/adapters/V5_S10F_EXEC_PLAN.md",
>     "tests/adapters/v5-codex-readonly-fixture-trial/README.md",
>     "tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py",
> }
> actual = set(subprocess.check_output(["git", "diff", "--name-only"], text=True).splitlines())
> actual |= set(subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], text=True).splitlines())
> unexpected = sorted(actual - allowed)
> missing = sorted(required - actual)
> if unexpected or missing:
>     if unexpected:
>         print("unexpected changed files:")
>         print("\n".join(unexpected))
>     if missing:
>         print("missing required files:")
>         print("\n".join(missing))
>     raise SystemExit(1)
> print("changed files ok")
> PY
> ```
>
> Run execution-plan heading check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
> import re
> file = Path("docs/adapters/V5_S10F_EXEC_PLAN.md")
> expected = [
>     "# V5-S10F Execution Plan",
>     "## Purpose",
>     "## Scope",
>     "## Approved Write Set",
>     "## Protected Paths",
>     "## Source Protocol",
>     "## Source Material",
>     "## Completion Contract",
>     "## Milestones",
>     "## Self-Review Rubric",
>     "## Hard Failure Conditions",
>     "## Validation Commands",
>     "## Progress",
>     "## Iteration Log",
>     "## Surprises & Discoveries",
>     "## Decision Log",
>     "## Outcomes & Retrospective",
> ]
> lines = [line.rstrip() for line in file.read_text(encoding="utf-8").splitlines()]
> actual = [line for line in lines if re.match(r"^(#|##) [^#]", line)]
> if actual != expected:
>     print("heading mismatch")
>     print(actual)
>     raise SystemExit(1)
> print("heading structure ok")
> PY
> ```
>
> Run no-residue source/static check:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
> import ast
>
> script = Path("tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py")
> text = script.read_text(encoding="utf-8")
> tree = ast.parse(text)
>
> required_terms = [
>     "S10F no-residue determinism report",
>     "first_run_status",
>     "second_run_status",
>     "fixture_digest_stable",
>     "stdout_shape_stable",
>     "repository_residue_status",
>     "status",
>     "dont_write_bytecode",
> ]
> for term in required_terms:
>     if term not in text:
>         print(f"missing term: {term}")
>         raise SystemExit(1)
>
> forbidden = {"subprocess", "requests", "http", "urllib", "socket", "webbrowser", "shutil"}
> for node in ast.walk(tree):
>     if isinstance(node, ast.Import):
>         for alias in node.names:
>             if alias.name.split(".")[0] in forbidden:
>                 print(f"forbidden import: {alias.name}")
>                 raise SystemExit(1)
>     if isinstance(node, ast.ImportFrom):
>         if (node.module or "").split(".")[0] in forbidden:
>             print(f"forbidden import: {node.module}")
>             raise SystemExit(1)
>     if isinstance(node, ast.Call):
>         if isinstance(node.func, ast.Attribute) and node.func.attr in {"system", "popen"}:
>             print("runtime command call detected")
>             raise SystemExit(1)
> print("no-residue source ok")
> PY
> ```
>
> Run generated-artifact and protected-path checks:
>
> ```bash
> python3 - <<'PY'
> from pathlib import Path
> failures = []
> for p in Path(".").rglob("*"):
>     s = str(p)
>     if "__pycache__" in s or p.suffix == ".pyc":
>         failures.append(s)
> if failures:
>     print("\n".join(failures))
>     raise SystemExit(1)
> print("no generated artifacts ok")
> PY
>
> git status --short -- Releases/ .claude/ PAI/ CLAUDE.md AGENTS.md .codex/ install.sh settings.json hooks/ skills/ subagents/ agents/ commands/ .github/ .agents/
> ```
>
> Expected protected-path result: no output.
>
> ### Final handoff format
>
> End with exactly:
>
> ```markdown
> ## Files changed
>
> ## Behavior changed
>
> ## Tests run
>
> ## Known risks
>
> ## Protected files changed
>
> ## Goal state
>
> ## Recommended next architect decision
> ```

## Milestones

1. Baseline status check.
2. Existing S10E harness validation.
3. S10F execution plan creation.
4. No-residue self-test implementation.
5. README S10F update.
6. Harness determinism and no-residue validation.
7. Protected-path and no-extra-file validation.
8. Self-review and repair.
9. Final handoff and goal-state report.

## Self-Review Rubric

| Area | Points |
| --- | ---: |
| Scope and approved write-set discipline | 20 |
| Evidence discipline and baseline preservation | 10 |
| No-residue digest validation quality | 25 |
| Deterministic in-process harness execution quality | 20 |
| No-write, no-private-state, Pulse, Memory, ISA, and runtime-invocation safety | 15 |
| Verification quality and recorded results | 10 |
| Total | 100 |

Pass threshold:

```text
Minimum score: 94/100
Hard failures: 0
```

## Hard Failure Conditions

S10F stops or fails if any file outside the approved S10F write set changes; any fixture file changes; any protected path changes; the no-residue script, harness, or self-test uses non-stdlib dependencies, subprocesses, or network access; any script writes files in the repository; `__pycache__`, `.pyc`, or temporary artifacts remain; Pulse is started or called; Claude Code or Codex runtime is invoked; live user-local state is read; PAI Memory or ISA is written; or any deliverable claims Codex is drop-in today or the official upstream engine.

S10F also fails if any deliverable authorizes live trials, runtime adapter work, Memory writes, ISA writes, Pulse implementation, product-memory promotion, or dual-engine uncoordinated writes.

## Validation Commands

Required commands:

```bash
git status --short
git diff --name-only | sort
git diff --check
python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures
PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py
```

Additional required checks:

- Changed-file check.
- Execution-plan heading check.
- No-residue source/static check.
- Generated-artifact check.
- Protected-path check.

## Progress

- Baseline status check: complete; `git status --short` produced no output before edits.
- Existing S10E harness validation: complete; harness passed.
- Existing negative-control validation: complete; self-test passed with `negative_control_count: 60`.
- S10F execution plan creation: complete.
- No-residue self-test implementation: complete.
- README S10F update: complete.
- Validation execution: complete; all required checks passed.
- Final handoff and goal-state report: pending.

## Iteration Log

Iteration 1 target score before implementation: 94/100 minimum, hard failures 0. Baseline scope is feasible without modifying fixtures, protected paths, runtime files, Codex surfaces, Pulse surfaces, PAI Memory, or ISA.

Iteration 2 scored self-review after validation:

| Area | Score |
| --- | ---: |
| Scope and approved write-set discipline | 20/20 |
| Evidence discipline and baseline preservation | 10/10 |
| No-residue digest validation quality | 25/25 |
| Deterministic in-process harness execution quality | 20/20 |
| No-write, no-private-state, Pulse, Memory, ISA, and runtime-invocation safety | 15/15 |
| Verification quality and recorded results | 10/10 |
| Total | 100/100 |

Hard failures: 0.

## Surprises & Discoveries

The sandbox returned a loopback setup error for several read-only commands. Those commands were rerun with explicit escalation as read-only repository operations. No private user-local state, Pulse endpoint, installer, Claude Code command, or Codex runtime command was invoked.

No harness defect was found, so `run_readonly_fixture_trial.py` did not need modification in S10F.

## Decision Log

- S10F-D01: Keep the existing S10E harness unchanged unless no-residue validation proves a deterministic-support defect.
- S10F-D02: Implement the no-residue proof as an in-process Python script using only the standard library.
- S10F-D03: Compute fixture-root content digests before and after repeated harness runs, and separately scan for repository `__pycache__` and `.pyc` residue.
- S10F-D04: Treat harness stdout as validation output only, not an audit artifact.
- S10F-D05: Preserve the non-drop-in posture and keep S10F limited to fixture-test validation.

## Outcomes & Retrospective

S10F created the no-residue determinism guard without modifying the harness or any fixture files. The no-residue script imports the harness with `sys.dont_write_bytecode = True`, runs it in-process twice, captures stdout in memory, compares fixture-root digests before and after execution, verifies stable stdout shape, and confirms no repository `__pycache__`, `.pyc`, or S10F temporary residue is present.

Required validation results:

- `git status --short`: showed only the approved S10F execution plan, README update, and no-residue self-test.
- `git diff --name-only | sort`: showed only the approved S10F files.
- `git diff --check`: passed with no output.
- `python3 tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py --fixture-root tests/adapters/v5-codex-readonly-fixture-trial/fixtures`: passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py`: passed with `negative_control_count: 60`.
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py`: passed with stable fixture digest and stdout shape.
- Changed-file check: passed.
- Execution-plan heading check: passed.
- No-residue source/static check: passed.
- Generated-artifact check: passed.
- Protected-path check: passed with no output.

S10F remains fixture-test validation only. It does not prove Codex drop-in behavior, implement a runtime adapter, authorize live trials, read existing-local-v5 state, write PAI Memory or ISA, start or call Pulse, create root `AGENTS.md`, create `.codex/`, or create runtime, manifest, audit, executable schema, live-trial, Memory, ISA, or Pulse payloads.
