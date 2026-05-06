#!/usr/bin/env python3
"""S10F no-residue determinism report for the read-only fixture harness.

Codex is not currently proven drop-in for existing local PAI v5 files. This
fixture-only script imports the read-only harness in-process, captures stdout in
memory, and verifies deterministic no-residue behavior. It does not run Codex,
Claude Code, Pulse, live trials, subprocesses, network access, PAI Memory writes,
or ISA writes.
"""

import contextlib
import hashlib
import importlib.util
import io
import sys
from pathlib import Path


sys.dont_write_bytecode = True


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
FIXTURE_ROOT = SCRIPT_DIR / "fixtures"
HARNESS_PATH = SCRIPT_DIR / "run_readonly_fixture_trial.py"

REQUIRED_STDOUT_TERMS = (
    "S10A read-only fixture validation report",
    "S10C semantic validation",
    "S10D fixture case validation",
    "S10E global coverage validation",
    "fixture_count: 12",
    "case_count: 12",
    "seam_count: 23",
    "coverage_id_count: 25",
    "gate_id_count: 20",
    "denied_category_count: 13",
    "status: pass",
)

REPOSITORY_RESIDUE_PREFIXES = (
    "s10f-no-residue-",
    ".s10f-no-residue-",
)


def load_harness():
    spec = importlib.util.spec_from_file_location("s10f_readonly_fixture_trial", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load read-only fixture harness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture_tree_digest(root):
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        if path.is_dir():
            digest.update(b"dir")
        elif path.is_file():
            digest.update(b"file")
            digest.update(path.read_bytes())
        else:
            digest.update(b"other")
        digest.update(b"\0")
    return digest.hexdigest()


def run_harness_once(harness):
    stdout = io.StringIO()
    argv = ["--fixture-root", str(FIXTURE_ROOT)]
    with contextlib.redirect_stdout(stdout):
        status = harness.main(argv)
    return status, stdout.getvalue()


def residue_failures():
    failures = []
    for path in REPO_ROOT.rglob("*"):
        path_text = str(path)
        if "__pycache__" in path_text or path.suffix == ".pyc":
            failures.append(path.relative_to(REPO_ROOT).as_posix())
            continue
        if any(path.name.startswith(prefix) for prefix in REPOSITORY_RESIDUE_PREFIXES):
            failures.append(path.relative_to(REPO_ROOT).as_posix())
    return sorted(failures)


def stdout_shape_is_stable(first_output, second_output):
    if first_output != second_output:
        return False
    return all(term in first_output for term in REQUIRED_STDOUT_TERMS)


def status_text(condition):
    return "pass" if condition else "fail"


def main():
    harness = load_harness()

    residue_before = residue_failures()
    digest_before = fixture_tree_digest(FIXTURE_ROOT)
    first_status, first_output = run_harness_once(harness)
    second_status, second_output = run_harness_once(harness)
    digest_after = fixture_tree_digest(FIXTURE_ROOT)
    residue_after = residue_failures()

    first_ok = first_status == 0
    second_ok = second_status == 0
    fixture_digest_stable = digest_before == digest_after
    stdout_shape_stable = stdout_shape_is_stable(first_output, second_output)
    repository_residue_clean = not residue_before and not residue_after

    print("S10F no-residue determinism report")
    print(f"first_run_status: {status_text(first_ok)}")
    print(f"second_run_status: {status_text(second_ok)}")
    print(f"fixture_digest_stable: {status_text(fixture_digest_stable)}")
    print(f"stdout_shape_stable: {status_text(stdout_shape_stable)}")
    print(f"repository_residue_status: {status_text(repository_residue_clean)}")
    print(f"fixture_digest_before: {digest_before}")
    print(f"fixture_digest_after: {digest_after}")
    if residue_before:
        print("repository_residue_before:")
        for failure in residue_before:
            print(f"- {failure}")
    if residue_after:
        print("repository_residue_after:")
        for failure in residue_after:
            print(f"- {failure}")

    success = first_ok and second_ok and fixture_digest_stable and stdout_shape_stable and repository_residue_clean
    print(f"status: {status_text(success)}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
