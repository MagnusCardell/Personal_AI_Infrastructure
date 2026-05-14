from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


MILESTONE = "V5-S15D-PAI-RUNTIME-RUNNER-CODEX"
RUN_ID = "s15d-codex-synthetic-bugfix"
MARKER_VALUE = "PAI_CODEX_PEER_BETA_ADAPTER"
RUN_RELATIVE = Path("runs") / "s15d" / "codex-synthetic-bugfix"
WORKSPACE_RELATIVE = RUN_RELATIVE / "workspace"
RUN_STATE_NAME = "run-state.json"
TASK_DIFF_NAME = "task.diff"
S15E_MILESTONE = "V5-S15E-PAI-RUNTIME-CODEX-REAL-REPO-TASK"
S15E_RUN_ID = "s15e-provider-registry"
S15E_TASK_ID = "s15e-provider-registry-repo-task"
S15E_RUN_RELATIVE = Path("runs") / "s15e" / "provider-registry"
S15E_STATE_NAME = "repo-run-state.json"

APPROVED_INSTALL_RELATIVES = {
    Path("bin") / "pai-runtime",
    Path("runtimes") / "codex" / "README.md",
    Path("runtimes") / "codex" / "provider-manifest.json",
    Path("runtime-state.json"),
    Path("runtime-schemas") / "provider-manifest.schema.json",
    Path("runtime-schemas") / "run-result.schema.json",
    Path("runtime-schemas") / "run-validation.schema.json",
    Path("runtime-tasks") / "s15d-codex-synthetic-bugfix.json",
    Path("runtime-task-fixtures") / "s15d_bugfix" / "README.md",
    Path("runtime-task-fixtures") / "s15d_bugfix" / "src" / "pai_priority.py",
    Path("runtime-task-fixtures") / "s15d_bugfix" / "tests" / "test_pai_priority.py",
    Path("adapters") / "codex" / "bin" / "pai-codex",
    Path("adapters") / "codex" / "install-state.json",
}

APPROVED_S15E_INSTALL_RELATIVES = {
    Path("bin") / "pai-runtime",
    Path("runtime-state.json"),
    Path("runtime-schemas") / "repo-task.schema.json",
    Path("runtime-schemas") / "repo-run-result.schema.json",
    Path("runtime-schemas") / "repo-run-validation.schema.json",
    Path("runtime-tasks") / "s15e-provider-registry-repo-task.json",
    Path("runtimes") / "codex" / "README.md",
    Path("runtimes") / "codex" / "provider-manifest.json",
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

S15E_REQUIRED_REPOSITORY_MODIFICATIONS = {
    "tools/pai_runtime_runner/provider_registry.py",
    "tests/test_pai_runtime_provider_registry.py",
}

CLASSIFICATIONS = (
    "approved_task_workspace_write",
    "approved_pai_run_writes",
    "codex_event_file_change",
    "codex_event_command_execution",
    "codex_event_runtime_warning",
    "ambient_pai_state_churn",
    "forbidden_semantic_write",
    "forbidden_runtime_probe",
    "unknown_unclassified_write",
)


class RuntimeAuditError(ValueError):
    pass


def _is_within(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _relative_to_pai(pai_dir: Path, path: Path) -> Path | None:
    try:
        return path.resolve(strict=False).relative_to(pai_dir)
    except ValueError:
        return None


def _stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)) or value is None:
        return str(value)
    if isinstance(value, list):
        return " ".join(_stringify(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{key} {_stringify(item)}" for key, item in value.items())
    return str(value)


def _flatten_strings(value: Any) -> list[str]:
    strings: list[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, list):
        for item in value:
            strings.extend(_flatten_strings(item))
    elif isinstance(value, dict):
        for item in value.values():
            strings.extend(_flatten_strings(item))
    return strings


def _extract_keyed_strings(value: Any, keys: set[str]) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in keys and isinstance(item, str):
                found.append(item)
            found.extend(_extract_keyed_strings(item, keys))
    elif isinstance(value, list):
        for item in value:
            found.extend(_extract_keyed_strings(item, keys))
    return found


def _event_type(event: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ("type", "event", "name", "category", "kind"):
        value = event.get(key)
        if isinstance(value, str):
            parts.append(value)
    item = event.get("item")
    if isinstance(item, dict):
        for key in ("type", "name", "tool_name"):
            value = item.get(key)
            if isinstance(value, str):
                parts.append(value)
    return " ".join(parts).lower()


def _parse_events(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    events: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    if not path.is_file():
        return events, [{"classification": "codex_event_runtime_warning", "path": str(path), "reason": "missing event log"}]
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            warnings.append({"classification": "codex_event_runtime_warning", "path": str(path), "line": lineno})
            continue
        if isinstance(parsed, dict):
            events.append(parsed)
        else:
            warnings.append({"classification": "codex_event_runtime_warning", "path": str(path), "line": lineno})
    return events, warnings


def _looks_like_file_change(event: dict[str, Any]) -> bool:
    text = _event_type(event)
    return any(token in text for token in ("file_change", "file changed", "write_file", "apply_patch", "patch"))


def _looks_like_command_execution(event: dict[str, Any]) -> bool:
    text = _event_type(event)
    if any(token in text for token in ("exec_command", "command_execution", "shell_command")):
        return True
    if "tool_call" in text or "function_call" in text:
        keyed = _extract_keyed_strings(event, {"cmd", "command", "tool_name", "name"})
        return any("exec" in item.lower() or "shell" in item.lower() or "command" in item.lower() for item in keyed)
    return event.get("classification") == "codex_event_command_execution"


def _extract_paths(event: dict[str, Any]) -> list[str]:
    keyed = _extract_keyed_strings(event, {"path", "file", "file_path", "filename", "target", "output"})
    candidates = list(keyed)
    for text in _flatten_strings(event):
        candidates.extend(re.findall(r"(?:~?/|\./|[A-Za-z0-9_.-]+/)[A-Za-z0-9_./~:-]+", text))
    cleaned: list[str] = []
    for candidate in candidates:
        if candidate and candidate not in cleaned:
            cleaned.append(candidate)
    return cleaned


def _command_text(event: dict[str, Any]) -> str:
    keyed = _extract_keyed_strings(event, {"cmd", "command", "arguments", "input"})
    return " ".join(keyed) if keyed else _stringify(event)


def _command_has_runtime_probe(command: str) -> bool:
    lower = command.lower()
    if "localhost:31337" in lower or "127.0.0.1:31337" in lower:
        return True
    if "pulse" in lower and any(tool in lower for tool in ("curl", "wget", "nc ", "http", "socket", "probe")):
        return True
    return "31337" in lower and any(tool in lower for tool in ("curl", "wget", "nc ", "http", "socket"))


def _command_has_forbidden_semantic_write(command: str) -> bool:
    lower = command.lower()
    forbidden_tokens = (
        "memory/work",
        "memory/learning",
        "memory/knowledge",
        "/memory/work",
        "/memory/learning",
        "/memory/knowledge",
        "/isa",
        "isa/",
        "pulse/events",
        ".codex/",
        "~/.codex",
        "agents.md",
    )
    mutating_tokens = ("touch ", "mkdir ", "rm ", "mv ", "cp ", "tee ", ">", ">>", "write", "unlink", "rename")
    if any(token in lower for token in forbidden_tokens):
        return any(token in lower for token in mutating_tokens) or any(
            token in lower for token in ("memory/work", "memory/learning", "memory/knowledge", "/isa", "pulse/events")
        )
    return False


def _parts_lower(path: Path) -> list[str]:
    return [part.lower() for part in path.parts]


def _is_known_ambient_churn(relative_path: Path) -> bool:
    parts = _parts_lower(relative_path)
    if parts == [".quote-cache"]:
        return True
    if len(parts) >= 2 and parts[0] == "pulse":
        if parts[1] == "observability":
            return "events" not in parts
        return parts[1] in {"state", "logs", "performance"} and "events" not in parts
    if len(parts) >= 2 and parts[0] == "memory":
        return parts[1] in {"state", "observability"}
    return False


def _is_forbidden_semantic_path(relative_path: Path) -> bool:
    parts = _parts_lower(relative_path)
    if len(parts) >= 2 and parts[0] == "memory" and parts[1] in {"work", "learning", "knowledge"}:
        return True
    if parts and parts[0] == "isa":
        return True
    if len(parts) >= 2 and parts[0] == "pulse" and parts[1] == "events":
        return True
    return False


def _load_json(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise RuntimeAuditError(f"{label} is missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeAuditError(f"{label} is not valid JSON") from exc
    if not isinstance(data, dict):
        raise RuntimeAuditError(f"{label} must be a JSON object")
    return data


def _classify_path(pai_dir: Path, workspace: Path, raw: str) -> tuple[str, str]:
    text = raw.strip()
    if text.startswith("file://"):
        text = text[7:]
    if text.startswith("~/"):
        candidates = [Path.home() / text[2:]]
    else:
        raw_path = Path(text)
        candidates = [raw_path] if raw_path.is_absolute() else [workspace / raw_path, pai_dir / raw_path]

    run_root = pai_dir / RUN_RELATIVE
    for candidate in candidates:
        resolved = candidate.resolve(strict=False)
        if _is_within(workspace, resolved):
            return "approved_task_workspace_write", str(resolved)
        if _is_within(run_root, resolved):
            return "approved_pai_run_writes", str(resolved)
        relative = _relative_to_pai(pai_dir, resolved)
        if relative is None:
            continue
        if _is_forbidden_semantic_path(relative):
            return "forbidden_semantic_write", str(resolved)
        if _is_known_ambient_churn(relative):
            return "ambient_pai_state_churn", str(resolved)
    return "unknown_unclassified_write", raw


def _validate_result(result: dict[str, Any], workspace: Path) -> list[str]:
    errors: list[str] = []
    expected = {
        "milestone_name": MILESTONE,
        "run_id": RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "task_id": RUN_ID,
        "task_kind": "bounded-synthetic-code-repair",
        "adapter_identity_marker": MARKER_VALUE,
        "adapter_status": "peer-beta",
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "pai_owned_run_directory": True,
        "tests_passed": True,
        "memory_write_performed": False,
        "isa_write_performed": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
        "runtime_surface_created": False,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            errors.append(f"run-result mismatch for {key}")
    files_modified = result.get("files_modified")
    if not isinstance(files_modified, list) or not files_modified:
        errors.append("run-result files_modified must be a non-empty list")
        return errors
    for item in files_modified:
        if not isinstance(item, str) or item == "" or "\x00" in item:
            errors.append("run-result files_modified contains invalid path")
            continue
        path = Path(item)
        if path.is_absolute() or any(part == ".." for part in path.parts):
            errors.append(f"run-result files_modified escapes workspace: {item}")
            continue
        if not _is_within(workspace, (workspace / path).resolve(strict=False)):
            errors.append(f"run-result files_modified outside workspace: {item}")
    return errors


def _diff_limited_to_workspace(diff_text: str) -> bool:
    for line in diff_text.splitlines():
        if not (line.startswith("--- ") or line.startswith("+++ ")):
            continue
        path_text = line[4:].strip()
        if path_text == "/dev/null":
            continue
        if path_text.startswith(("a/", "b/")):
            path_text = path_text[2:]
        path = Path(path_text)
        if path.is_absolute() or any(part == ".." for part in path.parts):
            return False
    return True


def _load_run_state(run_dir: Path) -> dict[str, Any]:
    path = run_dir / RUN_STATE_NAME
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _load_repo_run_state(run_dir: Path) -> dict[str, Any]:
    path = run_dir / S15E_STATE_NAME
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _scan_filesystem(pai_dir: Path, marker: Path) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
    approved_task: list[str] = []
    approved_run: list[str] = []
    ambient: list[str] = []
    forbidden: list[str] = []
    unknown: list[str] = []
    marker_mtime = marker.stat().st_mtime
    run_root = pai_dir / RUN_RELATIVE
    workspace_root = pai_dir / WORKSPACE_RELATIVE

    for path in pai_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime <= marker_mtime:
                continue
        except OSError:
            continue
        resolved = path.resolve(strict=False)
        relative_path = resolved.relative_to(pai_dir)
        display = str(path)
        if _is_within(workspace_root, resolved):
            approved_task.append(display)
        elif _is_within(run_root, resolved):
            approved_run.append(display)
        elif relative_path in APPROVED_INSTALL_RELATIVES:
            approved_run.append(display)
        elif _is_forbidden_semantic_path(relative_path):
            forbidden.append(display)
        elif _is_known_ambient_churn(relative_path):
            ambient.append(display)
        else:
            unknown.append(display)
    return approved_task, approved_run, ambient, forbidden, unknown


def audit_run(
    *,
    pai_dir: Path,
    marker: Path,
    run_dir: Path,
    result_path: Path,
    events_path: Path,
    runtime_attempt_number: int = 1,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    pai_dir = pai_dir.resolve(strict=True)
    marker = marker.resolve(strict=True)
    run_dir = run_dir.resolve(strict=True)
    repo_root = (repo_root or Path.cwd()).resolve()
    workspace = run_dir / "workspace"
    diff_path = run_dir / TASK_DIFF_NAME

    result = _load_json(result_path, "run-result.json")
    run_state = _load_run_state(run_dir)
    result_errors = _validate_result(result, workspace)

    event_items, event_warnings = _parse_events(events_path)
    codex_file_change_events: list[dict[str, Any]] = []
    codex_command_execution_events: list[dict[str, Any]] = []
    forbidden_event_writes: list[str] = []
    runtime_probe_events: list[dict[str, Any]] = []
    event_file_change_outside_approved = False

    for event in event_items:
        if _looks_like_file_change(event):
            paths = _extract_paths(event)
            classifications = [_classify_path(pai_dir, workspace, raw) for raw in paths]
            approved = bool(classifications) and all(
                classification in {"approved_task_workspace_write", "approved_pai_run_writes"}
                for classification, _ in classifications
            )
            codex_file_change_events.append(
                {
                    "classification": "codex_event_file_change",
                    "approved": approved,
                    "paths": [path for _, path in classifications],
                    "event_type": _event_type(event),
                }
            )
            if not approved:
                event_file_change_outside_approved = True
                forbidden_event_writes.extend(
                    path for classification, path in classifications if classification == "forbidden_semantic_write"
                )

        if _looks_like_command_execution(event):
            command = _command_text(event)
            codex_command_execution_events.append(
                {
                    "classification": "codex_event_command_execution",
                    "command": command,
                    "event_type": _event_type(event),
                }
            )
            if _command_has_runtime_probe(command):
                runtime_probe_events.append({"classification": "forbidden_runtime_probe", "command": command})
            if _command_has_forbidden_semantic_write(command):
                forbidden_event_writes.append(command)

    approved_task, approved_run, ambient, forbidden_fs, unknown_fs = _scan_filesystem(pai_dir, marker)
    repo_root_agents_created = (repo_root / "AGENTS.md").exists()
    repo_dotcodex_created = (repo_root / ".codex").exists()
    home_codex = Path.home() / ".codex"
    codex_adapter_files_installed_under_home_codex = any(
        path.exists()
        for path in (
            home_codex / "AGENTS.md",
            home_codex / "AGENTS.override.md",
            home_codex / "adapters" / "codex",
        )
    )

    diff_text = diff_path.read_text(encoding="utf-8", errors="replace") if diff_path.is_file() else ""
    diff_present = bool(diff_text.strip())
    diff_limited = diff_present and _diff_limited_to_workspace(diff_text)
    task_initially_failed = run_state.get("initial_test_returncode") not in (None, 0)
    task_tests_passed_after_repair = run_state.get("post_test_returncode") == 0
    event_logs_present = events_path.is_file()
    memory_write_by_codex = any("memory" in item.lower() for item in forbidden_event_writes)
    isa_write_by_codex = any("/isa" in item.lower() or "isa/" in item.lower() for item in forbidden_event_writes)
    pulse_probe_by_codex = bool(runtime_probe_events)
    localhost_called_by_codex = any(
        "localhost:31337" in _stringify(event).lower() or "127.0.0.1:31337" in _stringify(event).lower()
        for event in event_items
        if _looks_like_command_execution(event)
    )

    forbidden_semantic_writes = forbidden_fs + forbidden_event_writes + result_errors
    unknown_unclassified_writes = unknown_fs
    event_attribution_passed = not (
        event_file_change_outside_approved
        or forbidden_event_writes
        or pulse_probe_by_codex
        or localhost_called_by_codex
    )
    validation_passed = bool(
        task_initially_failed
        and task_tests_passed_after_repair
        and diff_present
        and diff_limited
        and event_logs_present
        and event_attribution_passed
        and not forbidden_semantic_writes
        and not unknown_unclassified_writes
        and not repo_root_agents_created
        and not repo_dotcodex_created
        and not codex_adapter_files_installed_under_home_codex
    )

    return {
        "milestone_name": MILESTONE,
        "run_id": RUN_ID,
        "runtime": "codex",
        "runtime_attempt_number": runtime_attempt_number,
        "pai_runtime_command": run_state.get("pai_runtime_command", []),
        "provider_command": run_state.get("provider_command", []),
        "task_workspace": str(workspace),
        "task_initially_failed": task_initially_failed,
        "task_tests_passed_after_repair": task_tests_passed_after_repair,
        "diff_present": diff_present,
        "diff_limited_to_task_workspace": diff_limited,
        "event_logs_present": event_logs_present,
        "event_attribution_passed": event_attribution_passed,
        "codex_file_change_events": codex_file_change_events,
        "codex_command_execution_events": codex_command_execution_events,
        "approved_task_workspace_writes": sorted(approved_task),
        "approved_pai_run_writes": sorted(approved_run),
        "ambient_pai_state_churn": sorted(ambient),
        "forbidden_semantic_writes": sorted(forbidden_semantic_writes),
        "unknown_unclassified_writes": sorted(unknown_unclassified_writes),
        "memory_write_performed_by_codex": memory_write_by_codex,
        "isa_write_performed_by_codex": isa_write_by_codex,
        "pulse_probe_performed_by_codex": pulse_probe_by_codex,
        "localhost_31337_called_by_codex": localhost_called_by_codex,
        "repo_root_agents_created": repo_root_agents_created,
        "repo_dotcodex_created": repo_dotcodex_created,
        "codex_adapter_files_installed_under_home_codex": codex_adapter_files_installed_under_home_codex,
        "validation_passed": validation_passed,
        "known_limits": [
            "Codex JSONL event attribution is the primary runtime-provider write-boundary signal.",
            "Filesystem mtime scanning is a secondary detector.",
            "Ambient PAI state/cache/log churn is not adapter evidence.",
            "The bounded task is synthetic and is not replacement readiness.",
        ],
        "runtime_warnings": event_warnings,
        "classifications": list(CLASSIFICATIONS),
    }


def _validate_repo_result(result: dict[str, Any], repo_root: Path) -> list[str]:
    errors: list[str] = []
    expected = {
        "milestone_name": S15E_MILESTONE,
        "run_id": S15E_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "task_id": S15E_TASK_ID,
        "task_kind": "bounded-real-repository-code-change",
        "adapter_identity_marker": MARKER_VALUE,
        "adapter_status": "peer-beta",
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "pai_owned_run_directory": True,
        "tests_passed": True,
        "memory_write_performed": False,
        "isa_write_performed": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
        "runtime_surface_created": False,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            errors.append(f"repo-run-result mismatch for {key}")
    if Path(str(result.get("repo_root", ""))).resolve(strict=False) != repo_root:
        errors.append("repo-run-result repo_root mismatch")
    modified = result.get("repository_files_modified")
    if not isinstance(modified, list) or not modified:
        errors.append("repo-run-result repository_files_modified must be a non-empty list")
        return errors
    modified_set: set[str] = set()
    for item in modified:
        if not isinstance(item, str) or item == "" or "\x00" in item:
            errors.append("repo-run-result repository_files_modified contains invalid path")
            continue
        path = Path(item)
        if path.is_absolute() or any(part == ".." for part in path.parts):
            errors.append(f"repo-run-result repository_files_modified escapes repo: {item}")
            continue
        if item not in APPROVED_REPOSITORY_WRITE_SET:
            errors.append(f"repo-run-result repository_files_modified includes unapproved path: {item}")
        modified_set.add(item)
    if not S15E_REQUIRED_REPOSITORY_MODIFICATIONS.issubset(modified_set):
        errors.append("repo-run-result missing required provider registry modified files")
    return errors


def _diff_repository_paths(diff_text: str) -> set[str]:
    paths: set[str] = set()
    for line in diff_text.splitlines():
        if not (line.startswith("--- ") or line.startswith("+++ ")):
            continue
        path_text = line[4:].strip()
        if path_text == "/dev/null":
            continue
        if path_text.startswith(("a/", "b/")):
            path_text = path_text[2:]
        paths.add(path_text)
    return paths


def _diff_limited_to_approved_repository_write_set(diff_text: str) -> bool:
    paths = _diff_repository_paths(diff_text)
    if not paths:
        return False
    for item in paths:
        path = Path(item)
        if path.is_absolute() or any(part == ".." for part in path.parts):
            return False
        if item not in APPROVED_REPOSITORY_WRITE_SET:
            return False
    return True


def _classify_repo_event_path(pai_dir: Path, repo_root: Path, run_dir: Path, raw: str) -> tuple[str, str]:
    text = raw.strip()
    if text.startswith("file://"):
        text = text[7:]
    candidates: list[Path] = []
    if text.startswith("~/"):
        candidates.append(Path.home() / text[2:])
    else:
        raw_path = Path(text)
        if raw_path.is_absolute():
            candidates.append(raw_path)
        else:
            candidates.extend([repo_root / raw_path, run_dir / raw_path, pai_dir / raw_path])

    for candidate in candidates:
        resolved = candidate.resolve(strict=False)
        if _is_within(run_dir, resolved):
            return "approved_pai_run_writes", str(resolved)
        try:
            relative_repo = resolved.relative_to(repo_root)
        except ValueError:
            relative_repo = None
        if relative_repo is not None:
            relative_text = str(relative_repo)
            if relative_text in APPROVED_REPOSITORY_WRITE_SET:
                return "approved_repository_write", relative_text
            return "forbidden_repository_write", relative_text
        relative_pai = _relative_to_pai(pai_dir, resolved)
        if relative_pai is not None:
            if _is_forbidden_semantic_path(relative_pai):
                return "forbidden_semantic_write", str(resolved)
            if _is_known_ambient_churn(relative_pai):
                return "ambient_pai_state_churn", str(resolved)
    return "unknown_unclassified_write", raw


def _scan_repo_filesystem(repo_root: Path, marker: Path) -> tuple[list[str], list[str]]:
    approved: list[str] = []
    forbidden: list[str] = []
    marker_mtime = marker.stat().st_mtime
    for path in repo_root.rglob("*"):
        if ".git" in path.parts:
            continue
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime <= marker_mtime:
                continue
        except OSError:
            continue
        relative = str(path.resolve(strict=False).relative_to(repo_root))
        if relative in APPROVED_REPOSITORY_WRITE_SET:
            approved.append(relative)
        else:
            forbidden.append(relative)
    return approved, forbidden


def _scan_pai_filesystem_s15e(
    pai_dir: Path,
    marker: Path,
    run_dir: Path,
) -> tuple[list[str], list[str], list[str], list[str]]:
    approved_run: list[str] = []
    ambient: list[str] = []
    forbidden: list[str] = []
    unknown: list[str] = []
    marker_mtime = marker.stat().st_mtime

    for path in pai_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime <= marker_mtime:
                continue
        except OSError:
            continue
        resolved = path.resolve(strict=False)
        relative_path = resolved.relative_to(pai_dir)
        display = str(path)
        if _is_within(run_dir, resolved):
            approved_run.append(display)
        elif relative_path in APPROVED_S15E_INSTALL_RELATIVES:
            approved_run.append(display)
        elif _is_forbidden_semantic_path(relative_path):
            forbidden.append(display)
        elif _is_known_ambient_churn(relative_path):
            ambient.append(display)
        else:
            unknown.append(display)
    return approved_run, ambient, forbidden, unknown


def audit_repo_run(
    *,
    pai_dir: Path,
    marker: Path,
    repo_root: Path,
    run_dir: Path,
    result_path: Path,
    events_path: Path,
    diff_path: Path,
    runtime_attempt_number: int = 1,
) -> dict[str, Any]:
    pai_dir = pai_dir.resolve(strict=True)
    marker = marker.resolve(strict=True)
    repo_root = repo_root.resolve(strict=True)
    run_dir = run_dir.resolve(strict=True)

    result = _load_json(result_path, "repo-run-result.json")
    run_state = _load_repo_run_state(run_dir)
    result_errors = _validate_repo_result(result, repo_root)

    event_items, event_warnings = _parse_events(events_path)
    codex_file_change_events: list[dict[str, Any]] = []
    codex_command_execution_events: list[dict[str, Any]] = []
    forbidden_event_writes: list[str] = []
    forbidden_repo_event_writes: list[str] = []
    unknown_event_writes: list[str] = []
    runtime_probe_events: list[dict[str, Any]] = []
    event_file_change_outside_approved = False

    for event in event_items:
        if _looks_like_file_change(event):
            paths = _extract_paths(event)
            classifications = [_classify_repo_event_path(pai_dir, repo_root, run_dir, raw) for raw in paths]
            approved = bool(classifications) and all(
                classification in {"approved_repository_write", "approved_pai_run_writes"}
                for classification, _ in classifications
            )
            codex_file_change_events.append(
                {
                    "classification": "codex_event_file_change",
                    "approved": approved,
                    "paths": [path for _, path in classifications],
                    "event_type": _event_type(event),
                }
            )
            if not approved:
                event_file_change_outside_approved = True
                for classification, path in classifications:
                    if classification == "forbidden_semantic_write":
                        forbidden_event_writes.append(path)
                    elif classification == "forbidden_repository_write":
                        forbidden_repo_event_writes.append(path)
                    elif classification == "unknown_unclassified_write":
                        unknown_event_writes.append(path)

        if _looks_like_command_execution(event):
            command = _command_text(event)
            codex_command_execution_events.append(
                {
                    "classification": "codex_event_command_execution",
                    "command": command,
                    "event_type": _event_type(event),
                }
            )
            if _command_has_runtime_probe(command):
                runtime_probe_events.append({"classification": "forbidden_runtime_probe", "command": command})
            if _command_has_forbidden_semantic_write(command):
                forbidden_event_writes.append(command)

    approved_repository_writes, forbidden_repository_writes = _scan_repo_filesystem(repo_root, marker)
    approved_pai_run_writes, ambient, forbidden_fs, unknown_fs = _scan_pai_filesystem_s15e(pai_dir, marker, run_dir)

    repo_root_agents_created = (repo_root / "AGENTS.md").exists()
    repo_dotcodex_created = (repo_root / ".codex").exists()
    home_codex = Path.home() / ".codex"
    codex_adapter_files_installed_under_home_codex = any(
        path.exists()
        for path in (
            home_codex / "AGENTS.md",
            home_codex / "AGENTS.override.md",
            home_codex / "adapters" / "codex",
        )
    )

    diff_text = diff_path.read_text(encoding="utf-8", errors="replace") if diff_path.is_file() else ""
    diff_present = bool(diff_text.strip())
    diff_limited = diff_present and _diff_limited_to_approved_repository_write_set(diff_text)
    event_logs_present = events_path.is_file()
    provider_registry_tests_passed = run_state.get("provider_registry_tests_returncode") == 0
    repository_files_modified = result.get("repository_files_modified") if isinstance(result.get("repository_files_modified"), list) else []

    memory_write_by_codex = any("memory" in item.lower() for item in forbidden_event_writes + forbidden_fs)
    isa_write_by_codex = any("/isa" in item.lower() or "isa/" in item.lower() for item in forbidden_event_writes + forbidden_fs)
    pulse_probe_by_codex = bool(runtime_probe_events)
    localhost_called_by_codex = any(
        "localhost:31337" in _stringify(event).lower() or "127.0.0.1:31337" in _stringify(event).lower()
        for event in event_items
        if _looks_like_command_execution(event)
    )

    forbidden_semantic_writes = forbidden_fs + forbidden_event_writes + result_errors
    forbidden_repository = sorted(set(forbidden_repository_writes + forbidden_repo_event_writes))
    unknown_unclassified = sorted(set(unknown_fs + unknown_event_writes))
    event_attribution_passed = not (
        event_file_change_outside_approved
        or forbidden_event_writes
        or forbidden_repo_event_writes
        or unknown_event_writes
        or pulse_probe_by_codex
        or localhost_called_by_codex
    )
    validation_passed = bool(
        diff_present
        and diff_limited
        and event_logs_present
        and event_attribution_passed
        and provider_registry_tests_passed
        and not forbidden_repository
        and not forbidden_semantic_writes
        and not unknown_unclassified
        and not repo_root_agents_created
        and not repo_dotcodex_created
        and not codex_adapter_files_installed_under_home_codex
    )

    return {
        "milestone_name": S15E_MILESTONE,
        "run_id": S15E_RUN_ID,
        "runtime": "codex",
        "runtime_attempt_number": runtime_attempt_number,
        "pai_runtime_command": run_state.get("pai_runtime_command", []),
        "provider_command": run_state.get("provider_command", []),
        "repo_root": str(repo_root),
        "approved_repository_write_set": sorted(APPROVED_REPOSITORY_WRITE_SET),
        "repository_files_modified": repository_files_modified,
        "diff_present": diff_present,
        "diff_limited_to_approved_repository_write_set": diff_limited,
        "event_logs_present": event_logs_present,
        "event_attribution_passed": event_attribution_passed,
        "codex_file_change_events": codex_file_change_events,
        "codex_command_execution_events": codex_command_execution_events,
        "approved_repository_writes": sorted(approved_repository_writes),
        "approved_pai_run_writes": sorted(approved_pai_run_writes),
        "ambient_pai_state_churn": sorted(ambient),
        "forbidden_repository_writes": forbidden_repository,
        "forbidden_semantic_writes": sorted(forbidden_semantic_writes),
        "unknown_unclassified_writes": unknown_unclassified,
        "provider_registry_tests_passed": provider_registry_tests_passed,
        "memory_write_performed_by_codex": memory_write_by_codex,
        "isa_write_performed_by_codex": isa_write_by_codex,
        "pulse_probe_performed_by_codex": pulse_probe_by_codex,
        "localhost_31337_called_by_codex": localhost_called_by_codex,
        "repo_root_agents_created": repo_root_agents_created,
        "repo_dotcodex_created": repo_dotcodex_created,
        "codex_adapter_files_installed_under_home_codex": codex_adapter_files_installed_under_home_codex,
        "validation_passed": validation_passed,
        "known_limits": [
            "Codex JSONL event attribution is a runtime-provider signal, not replacement readiness.",
            "Filesystem mtime scanning is a secondary detector for repository and PAI write boundaries.",
            "Ambient PAI state/cache/log churn is not adapter evidence.",
            "S15E covers one bounded real repository task only.",
        ],
        "runtime_warnings": event_warnings,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit S15D PAI-owned Codex runtime run.")
    parser.add_argument("--pai-dir", required=True)
    parser.add_argument("--marker", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--runtime-attempt-number", type=int, default=1)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    run_dir = Path(args.run_dir)
    result = audit_run(
        pai_dir=Path(args.pai_dir),
        marker=Path(args.marker),
        run_dir=run_dir,
        result_path=run_dir / "run-result.json",
        events_path=run_dir / "runtime-events.jsonl",
        runtime_attempt_number=args.runtime_attempt_number,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"ok": result["validation_passed"], "output": str(output)}, sort_keys=True))
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
