from __future__ import annotations

import json
import shutil
import stat
from pathlib import Path


class RuntimeInstallError(ValueError):
    pass


REPO_ROOT = Path(__file__).resolve().parents[2]

INSTALL_TEXT_TARGETS = {
    REPO_ROOT / "runtimes" / "codex" / "README.md": Path("runtimes") / "codex" / "README.md",
    REPO_ROOT / "runtimes" / "codex" / "provider-manifest.json": Path("runtimes") / "codex" / "provider-manifest.json",
    REPO_ROOT / "pai-runtime" / "provider-manifest.schema.json": Path("runtime-schemas") / "provider-manifest.schema.json",
    REPO_ROOT / "pai-runtime" / "run-result.schema.json": Path("runtime-schemas") / "run-result.schema.json",
    REPO_ROOT / "pai-runtime" / "run-validation.schema.json": Path("runtime-schemas") / "run-validation.schema.json",
    REPO_ROOT / "pai-runtime" / "repo-task.schema.json": Path("runtime-schemas") / "repo-task.schema.json",
    REPO_ROOT / "pai-runtime" / "repo-run-result.schema.json": Path("runtime-schemas") / "repo-run-result.schema.json",
    REPO_ROOT / "pai-runtime" / "repo-run-validation.schema.json": Path("runtime-schemas") / "repo-run-validation.schema.json",
    REPO_ROOT / "pai-runtime" / "tasks" / "s15d-codex-synthetic-bugfix.json": Path("runtime-tasks") / "s15d-codex-synthetic-bugfix.json",
    REPO_ROOT / "pai-runtime" / "tasks" / "s15e-provider-registry-repo-task.json": Path("runtime-tasks") / "s15e-provider-registry-repo-task.json",
    REPO_ROOT / "pai-runtime" / "task-fixtures" / "s15d_bugfix" / "README.md": Path("runtime-task-fixtures") / "s15d_bugfix" / "README.md",
    REPO_ROOT / "pai-runtime" / "task-fixtures" / "s15d_bugfix" / "src" / "pai_priority.py": Path("runtime-task-fixtures") / "s15d_bugfix" / "src" / "pai_priority.py",
    REPO_ROOT / "pai-runtime" / "task-fixtures" / "s15d_bugfix" / "tests" / "test_pai_priority.py": Path("runtime-task-fixtures") / "s15d_bugfix" / "tests" / "test_pai_priority.py",
    REPO_ROOT / "adapters" / "codex" / "bin" / "pai-codex": Path("adapters") / "codex" / "bin" / "pai-codex",
}

APPROVED_LIVE_RELATIVES = tuple(INSTALL_TEXT_TARGETS.values()) + (
    Path("bin") / "pai-runtime",
    Path("runtime-state.json"),
    Path("adapters") / "codex" / "install-state.json",
    Path("runs") / "s15d" / "codex-synthetic-bugfix" / "run-result.json",
    Path("runs") / "s15d" / "codex-synthetic-bugfix" / "runtime-events.jsonl",
    Path("runs") / "s15d" / "codex-synthetic-bugfix" / "task.diff",
    Path("runs") / "s15d" / "codex-synthetic-bugfix" / "run-validation.json",
    Path("runs") / "s15d" / "codex-synthetic-bugfix" / "run-state.json",
    Path("runs") / "s15e" / "provider-registry" / "repo-run-result.json",
    Path("runs") / "s15e" / "provider-registry" / "repo-events.jsonl",
    Path("runs") / "s15e" / "provider-registry" / "repo-task.diff",
    Path("runs") / "s15e" / "provider-registry" / "repo-run-validation.json",
    Path("runs") / "s15e" / "provider-registry" / "repo-run-state.json",
)

RUN_DIR_RELATIVE = Path("runs") / "s15d" / "codex-synthetic-bugfix"
S15E_RUN_DIR_RELATIVE = Path("runs") / "s15e" / "provider-registry"


def _is_within(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _resolve_pai_dir(value: str | Path | None) -> Path:
    if value is None or str(value) == "":
        raise RuntimeInstallError("--pai-dir is required")
    path = Path(value)
    if any(part == ".." for part in path.parts):
        raise RuntimeInstallError("--pai-dir must not contain path traversal")
    resolved = path.resolve(strict=True)
    if not resolved.is_dir():
        raise RuntimeInstallError("--pai-dir must be a directory")
    return resolved


def _resolve_backup_root(value: str | Path | None) -> Path:
    if value is None or str(value) == "":
        raise RuntimeInstallError("--backup-root is required")
    path = Path(value)
    if any(part == ".." for part in path.parts):
        raise RuntimeInstallError("--backup-root must not contain path traversal")
    resolved = path.resolve(strict=True)
    if not resolved.is_dir():
        raise RuntimeInstallError("--backup-root must be a directory")
    return resolved


def _safe_live_path(pai_dir: Path, relative: Path) -> Path:
    if relative.is_absolute() or any(part == ".." for part in relative.parts):
        raise RuntimeInstallError(f"unsafe live relative path: {relative}")
    resolved = (pai_dir / relative).resolve(strict=False)
    if not _is_within(pai_dir, resolved):
        raise RuntimeInstallError(f"live target escapes PAI_DIR: {relative}")
    return resolved


def _write_text_if_changed(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.is_symlink():
        raise RuntimeInstallError(f"live target is a symlink: {path}")
    if path.exists() and not path.is_file():
        raise RuntimeInstallError(f"live target is not a file: {path}")
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def _mark_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def _wrapper_text() -> str:
    return (
        "#!/usr/bin/env python3\n"
        "from pathlib import Path\n"
        "import sys\n"
        f"sys.path.insert(0, {str(REPO_ROOT)!r})\n"
        "from tools.pai_runtime_runner.runner import main\n"
        "raise SystemExit(main())\n"
    )


def _runtime_state() -> str:
    payload = {
        "installed": True,
        "milestone_name": "V5-S15E-PAI-RUNTIME-CODEX-REAL-REPO-TASK",
        "ownership_model": "PAI owns the run; Codex is runtime provider codex.",
        "runtime_provider": "codex",
        "runtime_status": "peer-beta",
        "upstream_adapter": "claude",
        "supports_repo_tasks": True,
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _load_provider_manifest() -> dict[str, object]:
    return json.loads((REPO_ROOT / "runtimes" / "codex" / "provider-manifest.json").read_text(encoding="utf-8"))


def validate_staged_payload() -> None:
    manifest = _load_provider_manifest()
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
            raise RuntimeInstallError(f"provider manifest mismatch for {key}")
    for source in INSTALL_TEXT_TARGETS:
        if not source.is_file():
            raise RuntimeInstallError(f"missing staged runtime file: {source}")
    runner = (REPO_ROOT / "tools" / "pai_runtime_runner" / "runner.py").read_text(encoding="utf-8")
    audit = (REPO_ROOT / "tools" / "pai_runtime_runner" / "audit.py").read_text(encoding="utf-8")
    provider_registry = (REPO_ROOT / "tools" / "pai_runtime_runner" / "provider_registry.py").read_text(encoding="utf-8")
    if "PAI owns the run" not in runner or "runs/s15d" not in runner or "run-repo" not in runner:
        raise RuntimeInstallError("runner is missing PAI ownership tokens")
    if "audit-repo-run" not in runner or "approved_repository_write_set" not in runner + audit:
        raise RuntimeInstallError("runner/audit is missing S15E repo-task tokens")
    for token in (
        "discover_runtime_providers",
        "load_provider_manifest",
        "validate_provider_manifest",
        "get_provider_by_name",
    ):
        if token not in provider_registry:
            raise RuntimeInstallError(f"provider registry is missing {token}")


def install_runtime(pai_dir: str | Path | None, backup_root: str | Path | None) -> dict[str, object]:
    resolved_pai_dir = _resolve_pai_dir(pai_dir)
    _resolve_backup_root(backup_root)
    validate_staged_payload()
    changed: list[Path] = []

    wrapper = _safe_live_path(resolved_pai_dir, Path("bin") / "pai-runtime")
    if _write_text_if_changed(wrapper, _wrapper_text()):
        changed.append(wrapper)
    _mark_executable(wrapper)

    for source, relative in INSTALL_TEXT_TARGETS.items():
        target = _safe_live_path(resolved_pai_dir, relative)
        if _write_text_if_changed(target, source.read_text(encoding="utf-8")):
            changed.append(target)
        if target.name == "pai-codex":
            _mark_executable(target)

    runtime_state = _safe_live_path(resolved_pai_dir, Path("runtime-state.json"))
    if _write_text_if_changed(runtime_state, _runtime_state()):
        changed.append(runtime_state)

    return {"pai_dir": str(resolved_pai_dir), "changed_targets": [str(path) for path in changed]}


def _backup_pai_dir(backup_root: Path) -> Path:
    backup_pai = backup_root / ".claude" / "PAI"
    if not backup_pai.is_dir():
        raise RuntimeInstallError("backup root does not contain .claude/PAI")
    return backup_pai


def _restore_or_remove(pai_dir: Path, backup_pai: Path, relative: Path) -> bool:
    target = _safe_live_path(pai_dir, relative)
    source = backup_pai / relative
    if source.exists():
        if source.is_symlink() or not source.is_file():
            raise RuntimeInstallError(f"backup source is not a safe file: {source}")
        changed = _write_text_if_changed(target, source.read_text(encoding="utf-8"))
        if target.name in {"pai-runtime", "pai-codex"}:
            _mark_executable(target)
        return changed
    if target.exists():
        if target.is_symlink() or not target.is_file():
            raise RuntimeInstallError(f"rollback target is not a safe file: {target}")
        target.unlink()
        return True
    return False


def _rollback_run_dir(pai_dir: Path, backup_pai: Path, run_relative: Path) -> list[Path]:
    live_run = _safe_live_path(pai_dir, run_relative)
    backup_run = backup_pai / run_relative
    changed: list[Path] = []
    if live_run.exists():
        if live_run.is_symlink() or not live_run.is_dir():
            raise RuntimeInstallError(f"S15D run rollback target is unsafe: {live_run}")
        shutil.rmtree(live_run)
        changed.append(live_run)
    if backup_run.exists():
        if backup_run.is_symlink() or not backup_run.is_dir():
            raise RuntimeInstallError(f"S15D backup run directory is unsafe: {backup_run}")
        shutil.copytree(backup_run, live_run, symlinks=True)
        changed.append(live_run)
    return changed


def _remove_empty_dirs(paths: tuple[Path, ...]) -> None:
    for path in paths:
        try:
            path.rmdir()
        except OSError:
            continue


def rollback_runtime(pai_dir: str | Path | None, backup_root: str | Path | None) -> dict[str, object]:
    resolved_pai_dir = _resolve_pai_dir(pai_dir)
    resolved_backup_root = _resolve_backup_root(backup_root)
    backup_pai = _backup_pai_dir(resolved_backup_root)
    changed: list[Path] = []
    for run_relative in (RUN_DIR_RELATIVE, S15E_RUN_DIR_RELATIVE):
        changed.extend(_rollback_run_dir(resolved_pai_dir, backup_pai, run_relative))
    for relative in APPROVED_LIVE_RELATIVES:
        if relative == RUN_DIR_RELATIVE or _is_within(RUN_DIR_RELATIVE, relative):
            continue
        if relative == S15E_RUN_DIR_RELATIVE or _is_within(S15E_RUN_DIR_RELATIVE, relative):
            continue
        if _restore_or_remove(resolved_pai_dir, backup_pai, relative):
            changed.append(resolved_pai_dir / relative)
    _remove_empty_dirs(
        (
            resolved_pai_dir / RUN_DIR_RELATIVE,
            resolved_pai_dir / S15E_RUN_DIR_RELATIVE,
            resolved_pai_dir / "runs" / "s15e",
            resolved_pai_dir / "runs" / "s15d",
            resolved_pai_dir / "runs",
            resolved_pai_dir / "runtime-task-fixtures" / "s15d_bugfix" / "src",
            resolved_pai_dir / "runtime-task-fixtures" / "s15d_bugfix" / "tests",
            resolved_pai_dir / "runtime-task-fixtures" / "s15d_bugfix",
            resolved_pai_dir / "runtime-task-fixtures",
            resolved_pai_dir / "runtime-tasks",
            resolved_pai_dir / "runtime-schemas",
            resolved_pai_dir / "runtimes" / "codex",
            resolved_pai_dir / "runtimes",
            resolved_pai_dir / "bin",
        )
    )
    return {"pai_dir": str(resolved_pai_dir), "changed_targets": [str(path) for path in changed]}
