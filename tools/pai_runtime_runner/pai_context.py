from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.pai_runtime_runner.provider_registry import discover_runtime_providers, summarize_provider_manifest


PAI_DIR_LABEL = "~/.claude/PAI"
S15I_MILESTONE = "V5-S15I-PAI-RUNTIME-READONLY-PAI-CONTEXT-TASK"
S15I_RUN_ID = "s15i-read-only-pai-context"
S15I_TASK_ID = "s15i-readonly-pai-context-task"
S15I_TASK_KIND = "readonly-pai-metadata-context"


class PaiContextError(ValueError):
    pass


def _relative_label(pai_dir: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(pai_dir).as_posix()
    except ValueError:
        raise PaiContextError("context collector attempted to expose an unredacted path")


def _redacted_pai_label(relative: str = "") -> str:
    return PAI_DIR_LABEL if relative == "" else f"{PAI_DIR_LABEL}/{relative}"


def _parts_lower(path: Path) -> list[str]:
    return [part.lower() for part in path.parts]


def _is_forbidden_body_path(pai_dir: Path, path: Path) -> bool:
    try:
        relative = path.resolve(strict=False).relative_to(pai_dir)
    except ValueError:
        return True
    parts = _parts_lower(relative)
    if len(parts) >= 2 and parts[0] == "memory" and parts[1] in {"work", "learning", "knowledge"}:
        return True
    if len(parts) >= 1 and parts[0] == "isa":
        return True
    if len(parts) >= 2 and parts[0] == "pulse" and parts[1] == "events":
        return True
    return False


def _safe_read_json(pai_dir: Path, relative: Path, label: str) -> dict[str, Any]:
    path = pai_dir / relative
    if _is_forbidden_body_path(pai_dir, path):
        raise PaiContextError(f"refusing to read body from forbidden context path: {label}")
    if path.is_symlink():
        raise PaiContextError(f"refusing to read symlinked context metadata path: {label}")
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PaiContextError(f"{label} is not valid JSON") from exc
    return data if isinstance(data, dict) else {}


def _is_safe_dir(path: Path) -> bool:
    return not path.is_symlink() and path.is_dir()


def _safe_direct_file_count(directory: Path) -> int:
    if not _is_safe_dir(directory):
        return 0
    return sum(1 for path in directory.iterdir() if not path.is_symlink() and path.is_file())


def _first_existing_dir(pai_dir: Path, *names: str) -> Path | None:
    for name in names:
        path = pai_dir / name
        if _is_safe_dir(path):
            return path
    return None


def _top_level_structure(pai_dir: Path) -> dict[str, list[str]]:
    directories: list[str] = []
    files: list[str] = []
    for item in sorted(pai_dir.iterdir(), key=lambda candidate: candidate.name.lower()):
        if item.is_symlink():
            continue
        if item.is_dir():
            directories.append(item.name)
        elif item.is_file():
            files.append(item.name)
    return {"directories": directories, "files": files}


def _run_artifact_index(pai_dir: Path) -> list[dict[str, Any]]:
    runs_dir = pai_dir / "runs"
    if not _is_safe_dir(runs_dir):
        return []
    entries: list[dict[str, Any]] = []
    milestone_dirs = (item for item in runs_dir.iterdir() if not item.is_symlink() and item.is_dir())
    for milestone_dir in sorted(milestone_dirs, key=lambda item: item.name):
        run_dirs = (item for item in milestone_dir.iterdir() if not item.is_symlink() and item.is_dir())
        for run_dir in sorted(run_dirs, key=lambda item: item.name):
            artifact_names = sorted(item.name for item in run_dir.iterdir() if not item.is_symlink() and item.is_file())
            entries.append(
                {
                    "run_id": f"{milestone_dir.name}/{run_dir.name}",
                    "artifact_names": artifact_names,
                    "artifact_count": len(artifact_names),
                }
            )
    return entries


def _schema_names(pai_dir: Path) -> list[str]:
    schema_dir = pai_dir / "runtime-schemas"
    if not _is_safe_dir(schema_dir):
        return []
    return sorted(path.name for path in schema_dir.iterdir() if not path.is_symlink() and path.is_file())


def _task_names(pai_dir: Path) -> list[str]:
    task_dir = pai_dir / "runtime-tasks"
    if not _is_safe_dir(task_dir):
        return []
    return sorted(path.name for path in task_dir.iterdir() if not path.is_symlink() and path.is_file())


def _memory_category_metadata(pai_dir: Path) -> list[dict[str, Any]]:
    memory_dir = _first_existing_dir(pai_dir, "Memory", "MEMORY")
    categories: list[dict[str, Any]] = []
    for category in ("WORK", "LEARNING", "KNOWLEDGE"):
        path = memory_dir / category if memory_dir is not None else pai_dir / "Memory" / category
        categories.append(
            {
                "category": category,
                "present": _is_safe_dir(path),
                "file_count": _safe_direct_file_count(path),
                "file_count_scope": "direct-files-only",
                "body_read": False,
            }
        )
    return categories


def _directory_metadata(pai_dir: Path, *names: str) -> dict[str, Any]:
    path = _first_existing_dir(pai_dir, *names)
    return {
        "present": path is not None,
        "file_count": None,
        "file_count_scope": "not-collected",
        "body_read": False,
    }


def _runtime_state_metadata(pai_dir: Path) -> dict[str, Any]:
    state = _safe_read_json(pai_dir, Path("runtime-state.json"), "runtime-state.json")
    summary_keys = sorted(state)
    scalar_value_types = {
        key: type(value).__name__
        for key, value in state.items()
        if isinstance(value, (str, int, float, bool)) or value is None
    }
    return {"summary_keys": summary_keys, "scalar_value_types": scalar_value_types}


def collect_pai_context_metadata(pai_dir: Path) -> dict[str, Any]:
    pai_dir = Path(pai_dir).resolve(strict=True)
    providers = discover_runtime_providers(pai_dir)
    provider_summaries = []
    for provider in providers:
        summary = summarize_provider_manifest(provider)
        summary["capabilities"] = sorted(provider.get("capabilities", [])) if isinstance(provider.get("capabilities"), list) else []
        provider_summaries.append(summary)

    capsule = {
        "milestone_name": S15I_MILESTONE,
        "run_id": S15I_RUN_ID,
        "task_id": S15I_TASK_ID,
        "task_kind": S15I_TASK_KIND,
        "pai_dir_label": PAI_DIR_LABEL,
        "metadata_only": True,
        "redacted_paths": True,
        "runtime_providers": provider_summaries,
        "runtime_provider_names": [str(provider.get("runtime_name", "")) for provider in providers],
        "runtime_provider_count": len(providers),
        "runtime_state": _runtime_state_metadata(pai_dir),
        "top_level_pai_structure": _top_level_structure(pai_dir),
        "run_artifact_index": _run_artifact_index(pai_dir),
        "runtime_schema_names": _schema_names(pai_dir),
        "runtime_task_names": _task_names(pai_dir),
        "memory_categories": _memory_category_metadata(pai_dir),
        "isa": _directory_metadata(pai_dir, "ISA"),
        "pulse": _directory_metadata(pai_dir, "Pulse", "PULSE"),
        "forbidden_body_reads": {
            "memory_body_read": False,
            "isa_body_read": False,
            "pulse_event_payload_read": False,
            "claude_project_memory_read": False,
            "codex_memory_read": False,
        },
        "collection_policy": [
            "PAI collected bounded live metadata before invoking runtime=codex.",
            "Codex receives this sanitized capsule instead of direct live PAI traversal authority.",
            "Memory, ISA, and Pulse event payload bodies are not included.",
        ],
    }
    errors = validate_context_capsule(capsule)
    if errors:
        raise PaiContextError("; ".join(errors))
    return capsule


def validate_context_capsule(capsule: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if capsule.get("metadata_only") is not True:
        errors.append("context capsule must be metadata_only")
    if capsule.get("redacted_paths") is not True:
        errors.append("context capsule must use redacted paths")
    if capsule.get("pai_dir_label") != PAI_DIR_LABEL:
        errors.append("context capsule must use the redacted PAI_DIR label")
    raw = json.dumps(capsule, sort_keys=True)
    raw_lower = raw.lower()
    forbidden_tokens = (
        "/home/",
        "/Users/",
        "\\Users\\",
        "CLAUDE.md contents",
        "auth.json",
        "~/.codex",
        "~/.claude/projects",
        "~/.claude/CLAUDE.md",
        "~/.claude/settings",
        "localhost:31337",
        "127.0.0.1:31337",
    )
    for token in forbidden_tokens:
        if token in raw or token.lower() in raw_lower:
            errors.append(f"context capsule contains forbidden token: {token}")
    for key, value in capsule.get("forbidden_body_reads", {}).items():
        if value is not False:
            errors.append(f"context capsule body-read flag must be false: {key}")
    return errors


def context_report_from_capsule(capsule: dict[str, Any]) -> dict[str, Any]:
    providers = capsule.get("runtime_providers", [])
    provider_names = capsule.get("runtime_provider_names", [])
    codex_provider = next(
        (provider for provider in providers if isinstance(provider, dict) and provider.get("runtime_name") == "codex"),
        {},
    )
    memory_categories = [
        str(item.get("category"))
        for item in capsule.get("memory_categories", [])
        if isinstance(item, dict) and item.get("present")
    ]
    return {
        "milestone_name": S15I_MILESTONE,
        "run_id": S15I_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "pai_dir_label": PAI_DIR_LABEL,
        "task_id": S15I_TASK_ID,
        "task_kind": S15I_TASK_KIND,
        "adapter_identity_marker": "PAI_CODEX_PEER_BETA_ADAPTER",
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": True,
        "runtime_provider_count": int(capsule.get("runtime_provider_count", 0)),
        "runtime_provider_names": [str(item) for item in provider_names],
        "codex_provider_status": str(codex_provider.get("runtime_status", "")),
        "codex_capabilities_observed": [
            str(item) for item in codex_provider.get("capabilities", []) if isinstance(item, str)
        ],
        "memory_categories_observed": memory_categories,
        "memory_body_read": False,
        "isa_body_read": False,
        "pulse_event_payload_read": False,
        "claude_project_memory_read": False,
        "codex_memory_read": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
        "context_summary": "Codex reviewed a PAI-created sanitized metadata capsule for runtime-provider context.",
        "evidence_classification": [
            "PAI-owned runtime task evidence",
            "read-only PAI metadata context evidence",
            "not replacement readiness",
        ],
        "known_limits": [
            "The capsule excludes Memory bodies, ISA bodies, Pulse event payloads, and product memory.",
            "This is metadata-only context, not Memory/ISA proposal authority.",
        ],
    }


def normalize_context_report(provider_report: dict[str, Any], capsule: dict[str, Any]) -> dict[str, Any]:
    report = context_report_from_capsule(capsule)
    errors = validate_context_report(report)
    if errors:
        raise PaiContextError("; ".join(errors))
    return report


def validate_context_report(report: dict[str, Any]) -> list[str]:
    expected = {
        "milestone_name": S15I_MILESTONE,
        "run_id": S15I_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "task_id": S15I_TASK_ID,
        "task_kind": S15I_TASK_KIND,
        "adapter_identity_marker": "PAI_CODEX_PEER_BETA_ADAPTER",
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": True,
        "memory_body_read": False,
        "isa_body_read": False,
        "pulse_event_payload_read": False,
        "claude_project_memory_read": False,
        "codex_memory_read": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
    }
    errors: list[str] = []
    for key, value in expected.items():
        if report.get(key) != value:
            errors.append(f"context report mismatch for {key}")
    if "codex" not in report.get("runtime_provider_names", []):
        errors.append("context report must include codex runtime provider")
    provider_count = report.get("runtime_provider_count", 0)
    if not isinstance(provider_count, int) or provider_count < 1:
        errors.append("context report must include at least one runtime provider")
    if "pai.context.read.metadata" not in report.get("codex_capabilities_observed", []):
        errors.append("context report must include pai.context.read.metadata capability")
    raw = json.dumps(report, sort_keys=True)
    raw_lower = raw.lower()
    for token in (
        "/home/",
        "/Users/",
        "\\Users\\",
        "CLAUDE.md contents",
        "auth.json",
        "~/.codex",
        "~/.claude/projects",
        "~/.claude/CLAUDE.md",
        "~/.claude/settings",
        "localhost:31337",
        "127.0.0.1:31337",
    ):
        if token in raw or token.lower() in raw_lower:
            errors.append(f"context report contains forbidden token: {token}")
    return errors
