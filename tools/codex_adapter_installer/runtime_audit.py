"""Event-attributed write-boundary audit for the Codex PAI runtime launcher."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any


MILESTONE = "V5-S15B-R2-CODEX-RUNTIME-EVENT-ATTRIBUTED-WORKLOOP"
MARKER_VALUE = "PAI_CODEX_PEER_BETA_ADAPTER"

CLASSIFICATIONS = (
    "approved_adapter_write",
    "codex_event_file_change",
    "codex_event_command_execution",
    "codex_event_runtime_warning",
    "ambient_pai_state_churn",
    "forbidden_semantic_write",
    "forbidden_runtime_probe",
    "unknown_unclassified_write",
)

RUN_RELATIVE = Path("adapters") / "codex" / "runs" / "s15b-r2"
APPROVED_RUN_RELATIVES = {
    RUN_RELATIVE / "runtime-proof.json",
    RUN_RELATIVE / "workloop-once.json",
    RUN_RELATIVE / "runtime-events.jsonl",
    RUN_RELATIVE / "workloop-events.jsonl",
    RUN_RELATIVE / "runtime-validation.json",
}

APPROVED_INSTALL_RELATIVES = {
    Path("AGENTS.md"),
    Path("adapters") / "codex" / "AGENTS.md",
    Path("adapters") / "codex" / "README.md",
    Path("adapters") / "codex" / "adapter-manifest.json",
    Path("adapters") / "codex" / "install-state.json",
    Path("adapters") / "codex" / "bin" / "pai-codex",
    Path("adapters") / "codex" / "runtime-proof.schema.json",
    Path("adapters") / "codex" / "workloop-once.schema.json",
    Path("adapters") / "codex" / "runtime-validation.schema.json",
    Path("adapters") / "codex" / "runtime-state.json",
}

APPROVED_LIVE_RELATIVES = APPROVED_INSTALL_RELATIVES | APPROVED_RUN_RELATIVES


class AuditError(ValueError):
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
    parts = []
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
            warnings.append(
                {
                    "classification": "codex_event_runtime_warning",
                    "path": str(path),
                    "line": lineno,
                    "reason": "non-json event line",
                }
            )
            continue
        if isinstance(parsed, dict):
            events.append(parsed)
        else:
            warnings.append(
                {
                    "classification": "codex_event_runtime_warning",
                    "path": str(path),
                    "line": lineno,
                    "reason": "json event is not an object",
                }
            )
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
    if event.get("classification") == "codex_event_command_execution":
        return True
    return False


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


def _normalize_event_path(pai_dir: Path, raw: str) -> Path | None:
    text = raw.strip()
    if text.startswith("file://"):
        text = text[7:]
    if text.startswith("~/"):
        path = Path.home() / text[2:]
    else:
        path = Path(text)
    if not path.is_absolute():
        path = pai_dir / path
    rel = _relative_to_pai(pai_dir, path)
    return rel


def _approved_run_relative(relative_path: Path | None) -> bool:
    return relative_path in APPROVED_RUN_RELATIVES


def _command_text(event: dict[str, Any]) -> str:
    keyed = _extract_keyed_strings(event, {"cmd", "command", "arguments", "input"})
    if keyed:
        return " ".join(keyed)
    return _stringify(event)


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


def _relative_parts_lower(path: Path) -> list[str]:
    return [part.lower() for part in path.parts]


def _is_known_ambient_churn(relative_path: Path) -> bool:
    parts = _relative_parts_lower(relative_path)
    if parts == [".quote-cache"]:
        return True
    if len(parts) >= 2 and parts[0] == "pulse":
        return parts[1] in {"state", "logs", "performance"} and "events" not in parts
    if len(parts) >= 2 and parts[0] == "memory":
        return parts[1] == "state"
    return False


def _is_forbidden_semantic_path(relative_path: Path) -> bool:
    parts = _relative_parts_lower(relative_path)
    if len(parts) >= 2 and parts[0] == "memory" and parts[1] in {"work", "learning", "knowledge"}:
        return True
    if parts and parts[0] == "isa":
        return True
    if len(parts) >= 2 and parts[0] == "pulse" and parts[1] == "events":
        return True
    return False


def _load_json(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise AuditError(f"{label} is missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AuditError(f"{label} is not valid JSON") from exc
    if not isinstance(data, dict):
        raise AuditError(f"{label} must be a JSON object")
    return data


def _validate_runtime_artifacts(proof: dict[str, Any], workloop: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    proof_expected = {
        "milestone_name": MILESTONE,
        "adapter_identity_marker": MARKER_VALUE,
        "adapter_status": "peer-beta",
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "memory_write_performed": False,
        "isa_write_performed": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
        "runtime_surface_created": False,
    }
    workloop_expected = {
        "milestone_name": MILESTONE,
        "workloop_kind": "bounded-read-only-adapter-workloop",
        "adapter_identity_marker": MARKER_VALUE,
        "adapter_status": "peer-beta",
        "upstream_adapter": "claude",
        "memory_write_performed": False,
        "isa_write_performed": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
        "runtime_surface_created": False,
        "requires_architect_goal_card": True,
    }
    for key, expected in proof_expected.items():
        if proof.get(key) != expected:
            errors.append(f"runtime-proof mismatch for {key}")
    for key, expected in workloop_expected.items():
        if workloop.get(key) != expected:
            errors.append(f"workloop-once mismatch for {key}")
    if not workloop.get("proposed_next_action"):
        errors.append("workloop-once missing proposed_next_action")
    return errors


def _scan_filesystem(pai_dir: Path, marker: Path) -> tuple[list[str], list[str], list[str]]:
    approved: list[str] = []
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
        relative_path = path.resolve().relative_to(pai_dir)
        display = str(path)
        if relative_path in APPROVED_LIVE_RELATIVES:
            approved.append(display)
        elif _is_forbidden_semantic_path(relative_path):
            forbidden.append(display)
        elif _is_known_ambient_churn(relative_path):
            ambient.append(display)
        else:
            unknown.append(display)
    return approved, ambient, forbidden, unknown


def audit_runtime(
    *,
    pai_dir: Path,
    marker: Path,
    runtime_proof: Path,
    workloop: Path,
    runtime_events: Path,
    workloop_events: Path,
    runtime_attempt_number: int = 1,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    pai_dir = pai_dir.resolve(strict=True)
    marker = marker.resolve(strict=True)
    repo_root = (repo_root or Path.cwd()).resolve()

    proof = _load_json(runtime_proof, "runtime-proof.json")
    workloop_data = _load_json(workloop, "workloop-once.json")
    artifact_errors = _validate_runtime_artifacts(proof, workloop_data)

    runtime_event_items, runtime_warnings = _parse_events(runtime_events)
    workloop_event_items, workloop_warnings = _parse_events(workloop_events)
    all_events = runtime_event_items + workloop_event_items

    codex_file_change_events: list[dict[str, Any]] = []
    codex_command_execution_events: list[dict[str, Any]] = []
    codex_runtime_probe_events: list[dict[str, Any]] = []
    forbidden_event_writes: list[str] = []
    event_file_change_outside_approved = False

    for event in all_events:
        if _looks_like_file_change(event):
            paths = _extract_paths(event)
            normalized = [_normalize_event_path(pai_dir, raw) for raw in paths]
            approved = bool(normalized) and all(_approved_run_relative(item) for item in normalized)
            codex_file_change_events.append(
                {
                    "classification": "codex_event_file_change",
                    "approved": approved,
                    "paths": [str(item) for item in normalized if item is not None],
                    "event_type": _event_type(event),
                }
            )
            if not approved:
                event_file_change_outside_approved = True

        if _looks_like_command_execution(event):
            command = _command_text(event)
            entry = {
                "classification": "codex_event_command_execution",
                "command": command,
                "event_type": _event_type(event),
            }
            codex_command_execution_events.append(entry)
            if _command_has_runtime_probe(command):
                codex_runtime_probe_events.append(
                    {
                        "classification": "forbidden_runtime_probe",
                        "command": command,
                    }
                )
            if _command_has_forbidden_semantic_write(command):
                forbidden_event_writes.append(command)

    approved_writes, ambient_churn, forbidden_fs_writes, unknown_fs_writes = _scan_filesystem(pai_dir, marker)

    repo_root_agents_created = (repo_root / "AGENTS.md").exists()
    repo_dotcodex_created = (repo_root / ".codex").exists()
    home_codex = Path.home() / ".codex"
    home_codex_adapter_files = [
        home_codex / "AGENTS.md",
        home_codex / "AGENTS.override.md",
        home_codex / "adapters" / "codex",
    ]
    codex_adapter_files_installed_under_home_codex = any(path.exists() for path in home_codex_adapter_files)

    event_logs_present = runtime_events.is_file() and workloop_events.is_file()
    memory_write_by_codex = any("memory" in item.lower() for item in forbidden_event_writes)
    isa_write_by_codex = any("/isa" in item.lower() or "isa/" in item.lower() for item in forbidden_event_writes)
    pulse_probe_by_codex = bool(codex_runtime_probe_events)
    localhost_called_by_codex = any(
        "localhost:31337" in _stringify(event).lower() or "127.0.0.1:31337" in _stringify(event).lower()
        for event in all_events
        if _looks_like_command_execution(event)
    )

    forbidden_semantic_writes = forbidden_fs_writes + forbidden_event_writes + artifact_errors
    unknown_unclassified_writes = unknown_fs_writes

    event_attribution_passed = not (
        event_file_change_outside_approved
        or forbidden_event_writes
        or pulse_probe_by_codex
        or localhost_called_by_codex
    )

    validation_passed = bool(
        event_logs_present
        and event_attribution_passed
        and not forbidden_semantic_writes
        and not unknown_unclassified_writes
        and not repo_root_agents_created
        and not repo_dotcodex_created
        and not codex_adapter_files_installed_under_home_codex
    )

    return {
        "milestone_name": MILESTONE,
        "pai_dir": str(pai_dir),
        "runtime_attempt_number": runtime_attempt_number,
        "codex_exec_commands": [
            "codex exec --json --sandbox read-only --ephemeral --cd PAI_DIR --output-schema runtime-proof.schema.json",
            "codex exec --json --sandbox read-only --ephemeral --cd PAI_DIR --output-schema workloop-once.schema.json",
        ],
        "event_logs_present": event_logs_present,
        "event_attribution_passed": event_attribution_passed,
        "codex_file_change_events": codex_file_change_events,
        "codex_command_execution_events": codex_command_execution_events,
        "codex_runtime_probe_events": codex_runtime_probe_events,
        "approved_adapter_writes": sorted(approved_writes),
        "ambient_pai_state_churn": sorted(ambient_churn),
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
            "Codex JSONL event attribution is the primary write-boundary signal.",
            "Filesystem mtime scanning is a secondary detector.",
            "Ambient PAI state/cache/log churn is not adapter evidence.",
            "Codex product runtime metadata outside PAI is not inspected by content.",
        ],
        "runtime_warnings": runtime_warnings + workloop_warnings,
        "classifications": list(CLASSIFICATIONS),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit S15B-R2 Codex runtime event attribution.")
    parser.add_argument("--pai-dir", required=True)
    parser.add_argument("--marker", required=True)
    parser.add_argument("--runtime-proof", required=True)
    parser.add_argument("--workloop", required=True)
    parser.add_argument("--runtime-events", required=True)
    parser.add_argument("--workloop-events", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--runtime-attempt-number", type=int, default=1)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = audit_runtime(
        pai_dir=Path(args.pai_dir),
        marker=Path(args.marker),
        runtime_proof=Path(args.runtime_proof),
        workloop=Path(args.workloop),
        runtime_events=Path(args.runtime_events),
        workloop_events=Path(args.workloop_events),
        runtime_attempt_number=args.runtime_attempt_number,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"ok": result["validation_passed"], "output": str(output)}, sort_keys=True))
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
