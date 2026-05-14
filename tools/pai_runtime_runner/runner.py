from __future__ import annotations

import argparse
import difflib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from tools.pai_runtime_runner.audit import audit_repo_run as run_repo_audit
from tools.pai_runtime_runner.audit import audit_run as run_audit
from tools.pai_runtime_runner.providers.codex import (
    build_provider_command,
    build_repo_provider_command,
    run_codex_provider,
    run_codex_repo_provider,
)


MILESTONE = "V5-S15D-PAI-RUNTIME-RUNNER-CODEX"
RUN_ID = "s15d-codex-synthetic-bugfix"
MARKER = "PAI_CODEX_PEER_BETA_ADAPTER"
RUN_RELATIVE = Path("runs") / "s15d" / "codex-synthetic-bugfix"
TASK_RELATIVE = Path("runtime-tasks") / "s15d-codex-synthetic-bugfix.json"
S15E_MILESTONE = "V5-S15E-PAI-RUNTIME-CODEX-REAL-REPO-TASK"
S15E_RUN_ID = "s15e-provider-registry"
S15E_TASK_ID = "s15e-provider-registry-repo-task"
S15E_RUN_RELATIVE = Path("runs") / "s15e" / "provider-registry"
S15E_TASK_RELATIVE = Path("runtime-tasks") / "s15e-provider-registry-repo-task.json"
S15E_RESULT_NAME = "repo-run-result.json"
S15E_EVENTS_NAME = "repo-events.jsonl"
S15E_DIFF_NAME = "repo-task.diff"
S15E_STATE_NAME = "repo-run-state.json"
S15E_VALIDATION_NAME = "repo-run-validation.json"
S15E_TARGET_FILES = {
    "tools/pai_runtime_runner/provider_registry.py",
    "tests/test_pai_runtime_provider_registry.py",
}
APPROVED_REPOSITORY_WRITE_SET = {
    "pai-runtime/README.md",
    "pai-runtime/repo-task.schema.json",
    "pai-runtime/repo-run-result.schema.json",
    "pai-runtime/repo-run-validation.schema.json",
    "pai-runtime/tasks/s15e-provider-registry-repo-task.json",
    "tools/pai_runtime_runner/__main__.py",
    "tools/pai_runtime_runner/runner.py",
    "tools/pai_runtime_runner/audit.py",
    "tools/pai_runtime_runner/install.py",
    "tools/pai_runtime_runner/provider_registry.py",
    "tools/pai_runtime_runner/providers/codex.py",
    "tests/test_pai_runtime_runner_codex.py",
    "tests/test_pai_runtime_runner_repo_task.py",
    "tests/test_pai_runtime_provider_registry.py",
    "docs/architecture/V5-S15E-PAI-RUNTIME-CODEX-REAL-REPO-TASK.md",
}
REPO_RUN_RESULT_FIELDS = {
    "milestone_name",
    "run_id",
    "runtime",
    "runtime_status",
    "provider_type",
    "pai_dir",
    "repo_root",
    "task_id",
    "task_kind",
    "adapter_identity_marker",
    "adapter_status",
    "upstream_adapter",
    "agents_router_observed",
    "pai_owned_run_directory",
    "repository_files_modified",
    "tests_run",
    "tests_passed",
    "memory_write_performed",
    "isa_write_performed",
    "pulse_probe_performed",
    "localhost_31337_called",
    "runtime_surface_created",
    "result_summary",
    "evidence_classification",
    "known_limits",
    "provider_registry_file_content",
    "provider_registry_test_file_content",
}


class RunnerError(ValueError):
    pass


def _is_within(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _resolve_pai_dir(value: str | Path) -> Path:
    if str(value) == "":
        raise RunnerError("--pai-dir must not be empty")
    path = Path(value)
    if any(part == ".." for part in path.parts):
        raise RunnerError("--pai-dir must not contain path traversal")
    resolved = path.resolve(strict=True)
    if not resolved.is_dir():
        raise RunnerError("--pai-dir must be a directory")
    return resolved


def _load_json(path: Path, label: str) -> dict[str, object]:
    if not path.is_file():
        raise RunnerError(f"{label} is missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RunnerError(f"{label} is not valid JSON") from exc
    if not isinstance(data, dict):
        raise RunnerError(f"{label} must be a JSON object")
    return data


def _provider_manifest_path(pai_dir: Path, runtime: str) -> Path:
    return pai_dir / "runtimes" / runtime / "provider-manifest.json"


def _validate_codex_manifest(manifest: dict[str, object]) -> None:
    expected = {
        "runtime_name": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "upstream_adapter": "claude",
        "supports_codex_exec": True,
        "supports_jsonl_events": True,
        "supports_structured_output": True,
        "memory_write_policy": "disabled",
        "isa_write_policy": "disabled",
        "pulse_policy": "no-probe",
        "replacement_status": "not-replacement-grade",
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            raise RunnerError(f"codex provider manifest mismatch for {key}")


def _safe_task_card(pai_dir: Path, task_card: str | Path) -> Path:
    path = Path(task_card)
    if str(task_card) == "":
        raise RunnerError("--task-card must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--task-card must not contain path traversal")
    resolved = path.resolve(strict=True)
    expected = (pai_dir / TASK_RELATIVE).resolve(strict=True)
    if resolved != expected:
        raise RunnerError("--task-card must be the installed S15D task card")
    return resolved


def _safe_run_dir(pai_dir: Path, run_dir: str | Path) -> Path:
    path = Path(run_dir)
    if str(run_dir) == "":
        raise RunnerError("--run-dir must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--run-dir must not contain path traversal")
    resolved = path.resolve(strict=False)
    expected = (pai_dir / RUN_RELATIVE).resolve(strict=False)
    if resolved != expected:
        raise RunnerError("PAI runtime run directory must be runs/s15d/codex-synthetic-bugfix")
    if path.exists() and not path.is_dir():
        raise RunnerError("--run-dir target is not a directory")
    if path.is_symlink():
        raise RunnerError("--run-dir target is a symlink")
    return path


def _safe_marker(marker: str | Path) -> Path:
    path = Path(marker)
    if str(marker) == "":
        raise RunnerError("--marker must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--marker must not contain path traversal")
    resolved = path.resolve(strict=True)
    if path.is_symlink():
        raise RunnerError("--marker must not be a symlink")
    return resolved


def _safe_audit_output(run_dir: Path, output: str | Path) -> Path:
    path = Path(output)
    if str(output) == "":
        raise RunnerError("--output must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--output must not contain path traversal")
    resolved = path.resolve(strict=False)
    if not _is_within(run_dir.resolve(strict=False), resolved):
        raise RunnerError("--output must stay under runs/s15d/codex-synthetic-bugfix")
    if resolved.name != "run-validation.json":
        raise RunnerError("--output must be named run-validation.json")
    if path.exists() and not path.is_file():
        raise RunnerError("--output target is not a file")
    if path.is_symlink():
        raise RunnerError("--output target is a symlink")
    return path


def doctor(pai_dir: Path) -> dict[str, object]:
    router = pai_dir / "AGENTS.md"
    if not router.is_file():
        raise RunnerError("PAI_DIR/AGENTS.md is missing")
    router_text = router.read_text(encoding="utf-8")
    if MARKER not in router_text:
        raise RunnerError("PAI_DIR/AGENTS.md is missing PAI_CODEX_PEER_BETA_ADAPTER")

    manifest = _load_json(_provider_manifest_path(pai_dir, "codex"), "codex provider manifest")
    _validate_codex_manifest(manifest)
    for path, label in (
        (pai_dir / "bin" / "pai-runtime", "pai-runtime"),
        (pai_dir / "runtime-schemas" / "provider-manifest.schema.json", "provider manifest schema"),
        (pai_dir / "runtime-schemas" / "run-result.schema.json", "run result schema"),
        (pai_dir / "runtime-schemas" / "run-validation.schema.json", "run validation schema"),
        (pai_dir / "runtime-schemas" / "repo-task.schema.json", "repo task schema"),
        (pai_dir / "runtime-schemas" / "repo-run-result.schema.json", "repo run result schema"),
        (pai_dir / "runtime-schemas" / "repo-run-validation.schema.json", "repo run validation schema"),
        (pai_dir / TASK_RELATIVE, "S15D task card"),
        (pai_dir / S15E_TASK_RELATIVE, "S15E repo task card"),
        (pai_dir / "runtime-task-fixtures" / "s15d_bugfix" / "src" / "pai_priority.py", "S15D task fixture"),
        (pai_dir / "adapters" / "codex" / "bin" / "pai-codex", "Codex provider driver"),
    ):
        if not path.is_file():
            raise RunnerError(f"{label} is missing: {path}")
    return {
        "ok": True,
        "pai_dir": str(pai_dir),
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "adapter_identity_marker_observed": True,
    }


def run_runtime(
    pai_dir: Path,
    runtime: str,
    task_card: str | Path,
    run_dir: str | Path,
    dry_run: bool = False,
) -> dict[str, object]:
    # PAI owns the run; Codex is only runtime provider codex.
    doctor(pai_dir)
    if runtime != "codex":
        raise RunnerError(f"unknown runtime provider: {runtime}")
    task_path = _safe_task_card(pai_dir, task_card)
    safe_run_dir = _safe_run_dir(pai_dir, run_dir)
    command = [
        str(pai_dir / "bin" / "pai-runtime"),
        "run",
        "--pai-dir",
        str(pai_dir),
        "--runtime",
        "codex",
        "--task-card",
        str(task_path),
        "--run-dir",
        str(safe_run_dir),
    ]
    provider_command = build_provider_command(pai_dir, task_path, safe_run_dir)
    if dry_run:
        return {
            "dry_run": True,
            "pai_runtime_command": command,
            "provider_command": provider_command,
            "run_dir": str(safe_run_dir),
        }
    safe_run_dir.mkdir(parents=True, exist_ok=True)
    provider_result = run_codex_provider(pai_dir, task_path, safe_run_dir)
    state_path = safe_run_dir / "run-state.json"
    state = _load_json(state_path, "run-state.json") if state_path.exists() else {}
    state["pai_runtime_command"] = command
    state["provider_command"] = provider_result.get("provider_command", provider_command)
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    provider_result["pai_runtime_command"] = command
    provider_result["provider_command"] = state["provider_command"]
    provider_result["pai_owned_run_directory"] = str(safe_run_dir)
    return provider_result


def _safe_repo_task_card(pai_dir: Path, task_card: str | Path) -> Path:
    path = Path(task_card)
    if str(task_card) == "":
        raise RunnerError("--task-card must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--task-card must not contain path traversal")
    resolved = path.resolve(strict=True)
    expected = (pai_dir / S15E_TASK_RELATIVE).resolve(strict=True)
    if resolved != expected:
        raise RunnerError("--task-card must be the installed S15E repo task card")
    return resolved


def _safe_repo_run_dir(pai_dir: Path, run_dir: str | Path) -> Path:
    path = Path(run_dir)
    if str(run_dir) == "":
        raise RunnerError("--run-dir must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--run-dir must not contain path traversal")
    resolved = path.resolve(strict=False)
    expected = (pai_dir / S15E_RUN_RELATIVE).resolve(strict=False)
    if resolved != expected:
        raise RunnerError("PAI runtime repo run directory must be runs/s15e/provider-registry")
    if path.exists() and not path.is_dir():
        raise RunnerError("--run-dir target is not a directory")
    if path.is_symlink():
        raise RunnerError("--run-dir target is a symlink")
    return path


def _safe_repo_audit_output(run_dir: Path, output: str | Path) -> Path:
    path = Path(output)
    if str(output) == "":
        raise RunnerError("--output must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--output must not contain path traversal")
    resolved = path.resolve(strict=False)
    if not _is_within(run_dir.resolve(strict=False), resolved):
        raise RunnerError("--output must stay under runs/s15e/provider-registry")
    if resolved.name != S15E_VALIDATION_NAME:
        raise RunnerError("--output must be named repo-run-validation.json")
    if path.exists() and not path.is_file():
        raise RunnerError("--output target is not a file")
    if path.is_symlink():
        raise RunnerError("--output target is a symlink")
    return path


def _safe_repo_root(repo_root: str | Path) -> Path:
    path = Path(repo_root)
    if str(repo_root) == "":
        raise RunnerError("--repo-root must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--repo-root must not contain path traversal")
    resolved = path.resolve(strict=True)
    if not resolved.is_dir():
        raise RunnerError("--repo-root must be a directory")
    if path.is_symlink():
        raise RunnerError("--repo-root must not be a symlink")
    try:
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=resolved,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.strip()
    except subprocess.CalledProcessError as exc:
        raise RunnerError("--repo-root must be inside a git worktree") from exc
    if Path(top).resolve(strict=True) != resolved:
        raise RunnerError("--repo-root must be the git worktree root")
    return resolved


def _load_repo_task_card(path: Path) -> dict[str, object]:
    card = _load_json(path, "S15E repo task card")
    if card.get("milestone_name") != S15E_MILESTONE:
        raise RunnerError("S15E repo task card has unexpected milestone_name")
    if card.get("task_id") != S15E_TASK_ID:
        raise RunnerError("S15E repo task card has unexpected task_id")
    if card.get("task_kind") != "bounded-real-repository-code-change":
        raise RunnerError("S15E repo task card has unexpected task_kind")
    if card.get("runtime") != "codex":
        raise RunnerError("S15E repo task card runtime must be codex")
    return card


def _approved_repository_write_set(card: dict[str, object]) -> set[str]:
    raw = card.get("approved_repository_write_set")
    if not isinstance(raw, list) or not raw or not all(isinstance(item, str) for item in raw):
        raise RunnerError("S15E repo task card approved_repository_write_set is invalid")
    approved = set(raw)
    for item in approved:
        path = Path(item)
        if path.is_absolute() or any(part == ".." for part in path.parts):
            raise RunnerError(f"S15E approved repository path is unsafe: {item}")
    unexpected = approved - APPROVED_REPOSITORY_WRITE_SET
    if unexpected:
        raise RunnerError(f"S15E task card includes unapproved repository paths: {sorted(unexpected)}")
    if not S15E_TARGET_FILES.issubset(approved):
        raise RunnerError("S15E task card does not include required provider registry target files")
    return approved


def _repository_target_files(card: dict[str, object], approved: set[str]) -> set[str]:
    raw = card.get("repository_target_files")
    if not isinstance(raw, list) or not raw or not all(isinstance(item, str) for item in raw):
        raise RunnerError("S15E repo task card repository_target_files is invalid")
    targets = set(raw)
    if not S15E_TARGET_FILES.issubset(targets):
        raise RunnerError("S15E repo task card does not target provider registry implementation and tests")
    if not targets.issubset(approved):
        raise RunnerError("S15E repo task card targets paths outside approved write set")
    return targets


def _repo_test_command(card: dict[str, object]) -> list[str]:
    raw = card.get("test_command")
    if not isinstance(raw, list) or not raw or not all(isinstance(item, str) for item in raw):
        raise RunnerError("S15E repo task card test_command is invalid")
    return list(raw)


def _snapshot_repository_files(repo_root: Path, paths: set[str]) -> dict[str, str | None]:
    snapshot: dict[str, str | None] = {}
    for relative in sorted(paths):
        path = repo_root / relative
        if path.is_file():
            snapshot[relative] = path.read_text(encoding="utf-8")
        else:
            snapshot[relative] = None
    return snapshot


def _write_repository_diff(before: dict[str, str | None], repo_root: Path, diff_path: Path) -> list[str]:
    modified: list[str] = []
    diff_lines: list[str] = []
    for relative, old in sorted(before.items()):
        path = repo_root / relative
        new = path.read_text(encoding="utf-8") if path.is_file() else None
        if old == new:
            continue
        modified.append(relative)
        old_lines = [] if old is None else old.splitlines(keepends=True)
        new_lines = [] if new is None else new.splitlines(keepends=True)
        diff_lines.extend(
            difflib.unified_diff(
                old_lines,
                new_lines,
                fromfile=f"a/{relative}",
                tofile=f"b/{relative}",
            )
        )
    diff_path.write_text("".join(diff_lines), encoding="utf-8")
    return modified


def _apply_materialized_repo_changes(repo_root: Path, result: dict[str, object]) -> None:
    replacements = {
        "tools/pai_runtime_runner/provider_registry.py": result.get("provider_registry_file_content"),
        "tests/test_pai_runtime_provider_registry.py": result.get("provider_registry_test_file_content"),
    }
    for relative, content in replacements.items():
        if not isinstance(content, str) or content == "":
            continue
        path = Path(relative)
        if path.is_absolute() or any(part == ".." for part in path.parts):
            raise RunnerError(f"S15E materialized replacement path is unsafe: {relative}")
        target = (repo_root / path).resolve(strict=False)
        if not _is_within(repo_root.resolve(strict=True), target):
            raise RunnerError(f"S15E materialized replacement escapes repository: {relative}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def _run_repo_tests(repo_root: Path, command: list[str]) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        command,
        cwd=repo_root,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )


def _normalize_repo_run_result(
    *,
    result: dict[str, object],
    pai_dir: Path,
    repo_root: Path,
    run_dir: Path,
    card: dict[str, object],
    modified: list[str],
    test_command: list[str],
    tests_passed: bool,
) -> dict[str, object]:
    normalized = {key: result[key] for key in REPO_RUN_RESULT_FIELDS if key in result}
    normalized.update(
        {
            "milestone_name": S15E_MILESTONE,
            "run_id": S15E_RUN_ID,
            "runtime": "codex",
            "runtime_status": "peer-beta",
            "provider_type": "codex-cli",
            "pai_dir": str(pai_dir),
            "repo_root": str(repo_root),
            "task_id": S15E_TASK_ID,
            "task_kind": "bounded-real-repository-code-change",
            "adapter_identity_marker": MARKER,
            "adapter_status": "peer-beta",
            "upstream_adapter": "claude",
            "agents_router_observed": True,
            "pai_owned_run_directory": True,
            "repository_files_modified": sorted(modified),
            "tests_run": [" ".join(test_command)],
            "tests_passed": tests_passed,
            "memory_write_performed": False,
            "isa_write_performed": False,
            "pulse_probe_performed": False,
            "localhost_31337_called": False,
            "runtime_surface_created": False,
            "result_summary": str(
                result.get("result_summary")
                or "Implemented and validated the PAI runtime provider registry through a bounded real repository task."
            ),
            "evidence_classification": result.get("evidence_classification")
            if isinstance(result.get("evidence_classification"), list)
            else [
                "PAI-owned real repository task evidence",
                "runtime provider registry evidence",
                "not replacement readiness",
            ],
            "known_limits": result.get("known_limits")
            if isinstance(result.get("known_limits"), list)
            else [
                "S15E is a bounded real repository task, not Codex replacement readiness.",
                "Memory, ISA, and Pulse writes remain disabled for runtime=codex.",
            ],
        }
    )
    if card.get("task_id") != normalized["task_id"]:
        raise RunnerError("S15E normalized result task_id mismatch")
    return normalized


def run_repo_runtime(
    pai_dir: Path,
    runtime: str,
    task_card: str | Path,
    repo_root: str | Path,
    run_dir: str | Path,
    dry_run: bool = False,
) -> dict[str, object]:
    doctor(pai_dir)
    if runtime != "codex":
        raise RunnerError(f"unknown runtime provider: {runtime}")
    task_path = _safe_repo_task_card(pai_dir, task_card)
    card = _load_repo_task_card(task_path)
    safe_repo_root = _safe_repo_root(repo_root)
    safe_run_dir = _safe_repo_run_dir(pai_dir, run_dir)
    approved_repository_write_set = _approved_repository_write_set(card)
    targets = _repository_target_files(card, approved_repository_write_set)
    test_command = _repo_test_command(card)
    command = [
        str(pai_dir / "bin" / "pai-runtime"),
        "run-repo",
        "--pai-dir",
        str(pai_dir),
        "--runtime",
        "codex",
        "--task-card",
        str(task_path),
        "--repo-root",
        str(safe_repo_root),
        "--run-dir",
        str(safe_run_dir),
    ]
    provider_command = build_repo_provider_command(
        pai_dir,
        card,
        safe_repo_root,
        safe_run_dir,
        safe_run_dir / S15E_RESULT_NAME,
    )
    if dry_run:
        return {
            "dry_run": True,
            "pai_runtime_command": command,
            "provider_command": provider_command,
            "repo_root": str(safe_repo_root),
            "run_dir": str(safe_run_dir),
            "approved_repository_write_set": sorted(approved_repository_write_set),
        }

    safe_run_dir.mkdir(parents=True, exist_ok=True)
    before = _snapshot_repository_files(safe_repo_root, approved_repository_write_set)
    provider_result = run_codex_repo_provider(pai_dir, card, safe_repo_root, safe_run_dir)
    _apply_materialized_repo_changes(safe_repo_root, provider_result)
    modified = _write_repository_diff(before, safe_repo_root, safe_run_dir / S15E_DIFF_NAME)
    tests = _run_repo_tests(safe_repo_root, test_command)
    tests_passed = tests.returncode == 0
    state = {
        "pai_runtime_command": command,
        "provider_command": provider_result.get("provider_command", provider_command),
        "approved_repository_write_set": sorted(approved_repository_write_set),
        "repository_target_files": sorted(targets),
        "repository_files_modified": sorted(modified),
        "provider_registry_tests_returncode": tests.returncode,
        "provider_registry_tests_stdout": tests.stdout,
        "provider_registry_tests_stderr": tests.stderr,
        "repo_root": str(safe_repo_root),
    }
    (safe_run_dir / S15E_STATE_NAME).write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result_path = safe_run_dir / S15E_RESULT_NAME
    result = _load_json(result_path, S15E_RESULT_NAME)
    normalized = _normalize_repo_run_result(
        result=result,
        pai_dir=pai_dir,
        repo_root=safe_repo_root,
        run_dir=safe_run_dir,
        card=card,
        modified=modified,
        test_command=test_command,
        tests_passed=tests_passed,
    )
    result_path.write_text(json.dumps(normalized, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not tests_passed:
        raise RunnerError("S15E provider registry tests did not pass after Codex repo task")
    if not modified:
        raise RunnerError("S15E repo task did not produce a repository diff")
    if not S15E_TARGET_FILES.issubset(set(modified)):
        raise RunnerError("S15E repo task did not modify both provider registry target files")
    return {
        "ok": True,
        "repo_root": str(safe_repo_root),
        "run_dir": str(safe_run_dir),
        "result": str(result_path),
        "events_output": str(safe_run_dir / S15E_EVENTS_NAME),
        "diff": str(safe_run_dir / S15E_DIFF_NAME),
        "repository_files_modified": sorted(modified),
        "provider_registry_tests_passed": tests_passed,
    }


def audit_runtime_run(
    pai_dir: Path,
    marker: str | Path,
    run_dir: str | Path,
    output: str | Path,
    runtime_attempt_number: int,
) -> dict[str, object]:
    doctor(pai_dir)
    marker_path = _safe_marker(marker)
    safe_run_dir = _safe_run_dir(pai_dir, run_dir)
    output_path = _safe_audit_output(safe_run_dir, output)
    result = run_audit(
        pai_dir=pai_dir,
        marker=marker_path,
        run_dir=safe_run_dir,
        result_path=safe_run_dir / "run-result.json",
        events_path=safe_run_dir / "runtime-events.jsonl",
        runtime_attempt_number=runtime_attempt_number,
        repo_root=Path.cwd(),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result.get("validation_passed"):
        raise RunnerError(f"S15D PAI runtime audit failed; wrote {output_path}")
    return {
        "ok": True,
        "output": str(output_path),
        "event_attribution_passed": result.get("event_attribution_passed"),
        "validation_passed": result.get("validation_passed"),
    }


def audit_repo_runtime_run(
    pai_dir: Path,
    marker: str | Path,
    repo_root: str | Path,
    run_dir: str | Path,
    output: str | Path,
    runtime_attempt_number: int,
) -> dict[str, object]:
    doctor(pai_dir)
    marker_path = _safe_marker(marker)
    safe_repo_root = _safe_repo_root(repo_root)
    safe_run_dir = _safe_repo_run_dir(pai_dir, run_dir)
    output_path = _safe_repo_audit_output(safe_run_dir, output)
    result = run_repo_audit(
        pai_dir=pai_dir,
        marker=marker_path,
        repo_root=safe_repo_root,
        run_dir=safe_run_dir,
        result_path=safe_run_dir / S15E_RESULT_NAME,
        events_path=safe_run_dir / S15E_EVENTS_NAME,
        diff_path=safe_run_dir / S15E_DIFF_NAME,
        runtime_attempt_number=runtime_attempt_number,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result.get("validation_passed"):
        raise RunnerError(f"S15E PAI runtime repo audit failed; wrote {output_path}")
    return {
        "ok": True,
        "output": str(output_path),
        "event_attribution_passed": result.get("event_attribution_passed"),
        "validation_passed": result.get("validation_passed"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PAI-owned runtime runner.")
    subcommands = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subcommands.add_parser("doctor")
    doctor_parser.add_argument("--pai-dir", required=True)

    run_parser = subcommands.add_parser("run")
    run_parser.add_argument("--pai-dir", required=True)
    run_parser.add_argument("--runtime", required=True)
    run_parser.add_argument("--task-card", required=True)
    run_parser.add_argument("--run-dir", required=True)
    run_parser.add_argument("--dry-run", action="store_true")

    repo_parser = subcommands.add_parser("run-repo")
    repo_parser.add_argument("--pai-dir", required=True)
    repo_parser.add_argument("--runtime", required=True)
    repo_parser.add_argument("--task-card", required=True)
    repo_parser.add_argument("--repo-root", required=True)
    repo_parser.add_argument("--run-dir", required=True)
    repo_parser.add_argument("--dry-run", action="store_true")

    audit_parser = subcommands.add_parser("audit-run")
    audit_parser.add_argument("--pai-dir", required=True)
    audit_parser.add_argument("--marker", required=True)
    audit_parser.add_argument("--run-dir", required=True)
    audit_parser.add_argument("--output", required=True)
    audit_parser.add_argument("--runtime-attempt-number", type=int, default=1)

    repo_audit_parser = subcommands.add_parser("audit-repo-run")
    repo_audit_parser.add_argument("--pai-dir", required=True)
    repo_audit_parser.add_argument("--marker", required=True)
    repo_audit_parser.add_argument("--repo-root", required=True)
    repo_audit_parser.add_argument("--run-dir", required=True)
    repo_audit_parser.add_argument("--output", required=True)
    repo_audit_parser.add_argument("--runtime-attempt-number", type=int, default=1)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        pai_dir = _resolve_pai_dir(args.pai_dir)
        if args.command == "doctor":
            result = doctor(pai_dir)
        elif args.command == "run":
            result = run_runtime(pai_dir, args.runtime, args.task_card, args.run_dir, args.dry_run)
        elif args.command == "run-repo":
            result = run_repo_runtime(
                pai_dir,
                args.runtime,
                args.task_card,
                args.repo_root,
                args.run_dir,
                args.dry_run,
            )
        elif args.command == "audit-run":
            result = audit_runtime_run(pai_dir, args.marker, args.run_dir, args.output, args.runtime_attempt_number)
        elif args.command == "audit-repo-run":
            result = audit_repo_runtime_run(
                pai_dir,
                args.marker,
                args.repo_root,
                args.run_dir,
                args.output,
                args.runtime_attempt_number,
            )
        else:
            raise RunnerError(f"unknown command: {args.command}")
    except (RunnerError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
