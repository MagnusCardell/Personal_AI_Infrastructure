from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.pai_runtime_runner.pai_context import collect_pai_context_metadata, validate_context_capsule

try:
    from jsonschema import Draft202012Validator
except Exception:  # noqa: BLE001 - proposal validation reports unavailable schema validation.
    Draft202012Validator = None  # type: ignore[assignment]


S16A_MILESTONE = "V5-S16A-PAI-STATE-PROPOSAL-RUNTIME-CODEX"
S16A_RUN_ID = "s16a-state-proposal"
S16A_TASK_ID = "s16a-state-proposal-task"
S16A_TASK_KIND = "proposal-only-memory-isa-state-update"
S16A_RUN_RELATIVE = Path("runs") / "s16a" / "state-proposal"
S16A_TASK_RELATIVE = Path("runtime-tasks") / "s16a-state-proposal-task.json"
STATE_CONTEXT_CAPSULE_NAME = "state-context-capsule.json"
STATE_PROPOSAL_NAME = "state-proposal.json"
STATE_PROPOSAL_EVENTS_NAME = "state-proposal-events.jsonl"
STATE_PROPOSAL_VALIDATION_NAME = "state-proposal-validation.json"
STATE_PROPOSAL_SCHEMA_NAME = "state-proposal.schema.json"
STATE_PROPOSAL_STATE_NAME = "state-proposal-state.json"
PAI_DIR_LABEL = "~/.claude/PAI"
MARKER_VALUE = "PAI_CODEX_PEER_BETA_ADAPTER"

STATE_PROPOSAL_INSTALL_RELATIVES = {
    Path("bin") / "pai-runtime",
    Path("runtime-state.json"),
    Path("runtime-schemas") / "state-proposal-task.schema.json",
    Path("runtime-schemas") / "state-context-capsule.schema.json",
    Path("runtime-schemas") / "state-proposal.schema.json",
    Path("runtime-schemas") / "state-proposal-validation.schema.json",
    Path("runtime-tasks") / "s16a-state-proposal-task.json",
    Path("runtimes") / "codex" / "provider-manifest.json",
}


class StateProposalError(ValueError):
    pass


def _is_within(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _parts_lower(path: Path) -> list[str]:
    return [part.lower() for part in path.parts]


def _relative_to_pai(pai_dir: Path, path: Path) -> Path | None:
    try:
        return path.resolve(strict=False).relative_to(pai_dir.resolve(strict=False))
    except ValueError:
        return None


def _redact_pai_text(pai_dir: Path, text: str) -> str:
    redacted = text.replace(str(pai_dir.resolve(strict=False)), PAI_DIR_LABEL)
    home = str(Path.home())
    if home != "/" and home in redacted:
        redacted = redacted.replace(home, "~")
    return redacted


def _redact_value(pai_dir: Path, value: Any) -> Any:
    if isinstance(value, str):
        return _redact_pai_text(pai_dir, value)
    if isinstance(value, list):
        return [_redact_value(pai_dir, item) for item in value]
    if isinstance(value, dict):
        return {key: _redact_value(pai_dir, item) for key, item in value.items()}
    return value


def _is_known_ambient_churn(relative_path: Path) -> bool:
    parts = _parts_lower(relative_path)
    if parts == [".quote-cache"]:
        return True
    if len(parts) >= 2 and parts[0] == "pulse":
        if parts[1] == "observability":
            return "events" not in parts
        return parts[1] in {"logs", "performance"} and "events" not in parts
    if len(parts) >= 2 and parts[0] == "memory":
        return parts[1] in {"state", "observability"}
    return False


def _state_write_class(relative_path: Path) -> str | None:
    parts = _parts_lower(relative_path)
    if len(parts) >= 2 and parts[0] == "memory" and parts[1] in {"work", "learning", "knowledge"}:
        return "memory"
    if parts and parts[0] == "isa":
        return "isa"
    if parts and parts[0] == "pulse" and not _is_known_ambient_churn(relative_path):
        return "pulse"
    return None


def _load_json(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise StateProposalError(f"{label} is missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise StateProposalError(f"{label} is not valid JSON") from exc
    if not isinstance(data, dict):
        raise StateProposalError(f"{label} must be a JSON object")
    return data


def _try_load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _schema_errors(instance: dict[str, Any], schema_path: Path, label: str) -> list[str]:
    if Draft202012Validator is None:
        return [f"{label} schema validation unavailable: jsonschema is not installed"]
    if not schema_path.is_file():
        return [f"{label} schema is missing: {schema_path}"]
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{label} schema is not valid JSON: {exc}"]
    if not isinstance(schema, dict):
        return [f"{label} schema must be a JSON object"]
    try:
        Draft202012Validator.check_schema(schema)
        errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda error: list(error.path))
    except Exception as exc:  # noqa: BLE001 - normalize schema errors for validation artifacts.
        return [f"{label} schema validation failed: {exc}"]
    return [
        f"{label} schema mismatch at {'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in errors
    ]


def collect_state_context_metadata(pai_dir: Path) -> dict[str, Any]:
    capsule = collect_pai_context_metadata(pai_dir)
    capsule.update(
        {
            "milestone_name": S16A_MILESTONE,
            "run_id": S16A_RUN_ID,
            "task_id": S16A_TASK_ID,
            "task_kind": S16A_TASK_KIND,
            "proposal_policy": [
                "S16A admits memory.write.proposal and isa.write.proposal only.",
                "Codex may propose Memory updates but S16A does not write Memory.",
                "Codex may propose ISA updates but S16A does not write ISA.",
                "All Memory and ISA proposal entries must use apply_status=proposed_only.",
                "Pulse probing and Pulse event emission remain forbidden.",
            ],
        }
    )
    errors = validate_state_context_capsule(capsule)
    if errors:
        raise StateProposalError("; ".join(errors))
    return capsule


def validate_state_context_capsule(capsule: dict[str, Any]) -> list[str]:
    errors = validate_context_capsule(capsule)
    expected = {
        "milestone_name": S16A_MILESTONE,
        "run_id": S16A_RUN_ID,
        "task_id": S16A_TASK_ID,
        "task_kind": S16A_TASK_KIND,
        "metadata_only": True,
        "redacted_paths": True,
    }
    for key, expected_value in expected.items():
        if capsule.get(key) != expected_value:
            errors.append(f"state context capsule mismatch for {key}")
    if not isinstance(capsule.get("proposal_policy"), list) or not capsule.get("proposal_policy"):
        errors.append("state context capsule must include proposal_policy")
    return errors


def _coerce_proposal_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def normalize_state_proposal(provider_result: dict[str, Any], capsule: dict[str, Any]) -> dict[str, Any]:
    proposal = {
        "milestone_name": S16A_MILESTONE,
        "run_id": S16A_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "pai_dir_label": PAI_DIR_LABEL,
        "task_id": S16A_TASK_ID,
        "task_kind": S16A_TASK_KIND,
        "adapter_identity_marker": MARKER_VALUE,
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": capsule.get("metadata_only") is True,
        "memory_proposals": _coerce_proposal_list(provider_result.get("memory_proposals")),
        "isa_proposals": _coerce_proposal_list(provider_result.get("isa_proposals")),
        "proposal_only": True,
        "memory_write_performed": False,
        "isa_write_performed": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
        "evidence_classification": [
            "PAI-owned state proposal evidence",
            "proposal-only Memory/ISA semantics",
            "not Memory/ISA commit authority",
        ],
        "known_limits": [
            "S16A stores proposals only under the PAI-owned run directory.",
            "S16A does not apply proposals to Memory or ISA.",
            "Pulse probing and Pulse event emission remain blocked.",
        ],
    }
    errors = validate_state_proposal(proposal)
    if errors:
        raise StateProposalError("; ".join(errors))
    return proposal


def validate_state_proposal(proposal: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "milestone_name": S16A_MILESTONE,
        "run_id": S16A_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "pai_dir_label": PAI_DIR_LABEL,
        "task_id": S16A_TASK_ID,
        "task_kind": S16A_TASK_KIND,
        "adapter_identity_marker": MARKER_VALUE,
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": True,
        "proposal_only": True,
        "memory_write_performed": False,
        "isa_write_performed": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
    }
    for key, value in expected.items():
        if proposal.get(key) != value:
            errors.append(f"state proposal mismatch for {key}")

    memory_proposals = proposal.get("memory_proposals")
    if not isinstance(memory_proposals, list):
        errors.append("state proposal memory_proposals must be a list")
    else:
        for index, item in enumerate(memory_proposals):
            if not isinstance(item, dict):
                errors.append(f"memory_proposals[{index}] must be an object")
                continue
            required = ("category", "title", "rationale", "source_context", "proposed_body", "confidence", "apply_status")
            for key in required:
                if key not in item:
                    errors.append(f"memory_proposals[{index}] missing {key}")
            if item.get("category") not in {"WORK", "LEARNING", "KNOWLEDGE"}:
                errors.append(f"memory_proposals[{index}].category is invalid")
            if item.get("apply_status") != "proposed_only":
                errors.append(f"memory_proposals[{index}].apply_status must be proposed_only")

    isa_proposals = proposal.get("isa_proposals")
    if not isinstance(isa_proposals, list):
        errors.append("state proposal isa_proposals must be a list")
    else:
        for index, item in enumerate(isa_proposals):
            if not isinstance(item, dict):
                errors.append(f"isa_proposals[{index}] must be an object")
                continue
            required = ("proposal_type", "title", "rationale", "proposed_record", "source_context", "confidence", "apply_status")
            for key in required:
                if key not in item:
                    errors.append(f"isa_proposals[{index}] missing {key}")
            if item.get("apply_status") != "proposed_only":
                errors.append(f"isa_proposals[{index}].apply_status must be proposed_only")

    raw = json.dumps(proposal, sort_keys=True)
    raw_lower = raw.lower()
    for token in (
        "/home/",
        "/users/",
        "\\users\\",
        "claude.md contents",
        "auth.json",
        "~/.codex",
        "~/.claude/projects",
        "~/.claude/claude.md",
        "~/.claude/settings",
        "localhost:31337",
        "127.0.0.1:31337",
    ):
        if token in raw_lower:
            errors.append(f"state proposal contains forbidden token: {token}")
    return errors


def all_memory_proposals_proposed_only(proposal: dict[str, Any]) -> bool:
    items = proposal.get("memory_proposals")
    return isinstance(items, list) and all(isinstance(item, dict) and item.get("apply_status") == "proposed_only" for item in items)


def all_isa_proposals_proposed_only(proposal: dict[str, Any]) -> bool:
    items = proposal.get("isa_proposals")
    return isinstance(items, list) and all(isinstance(item, dict) and item.get("apply_status") == "proposed_only" for item in items)


def _parse_events(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    events: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    if not path.is_file():
        return events, [{"classification": "codex_event_runtime_warning", "path": str(path), "reason": "missing event log"}]
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            warnings.append({"classification": "codex_event_runtime_warning", "path": str(path), "line": line_number})
            continue
        if isinstance(parsed, dict):
            events.append(parsed)
        else:
            warnings.append({"classification": "codex_event_runtime_warning", "path": str(path), "line": line_number})
    return events, warnings


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
    candidates = _extract_keyed_strings(event, {"path", "file", "file_path", "filename", "target", "output"})
    cleaned: list[str] = []
    for candidate in candidates:
        if candidate and candidate not in cleaned:
            cleaned.append(candidate)
    return cleaned


def _command_text(event: dict[str, Any]) -> str:
    keyed = _extract_keyed_strings(event, {"cmd", "command", "arguments", "input"})
    if keyed:
        return " ".join(keyed)
    return " ".join(_flatten_strings(event))


def _command_has_runtime_probe(command: str) -> bool:
    lower = command.lower()
    if "localhost:31337" in lower or "127.0.0.1:31337" in lower:
        return True
    if "pulse" in lower and any(tool in lower for tool in ("curl", "wget", "nc ", "http", "socket", "probe")):
        return True
    return "31337" in lower and any(tool in lower for tool in ("curl", "wget", "nc ", "http", "socket"))


def _command_reads_memory_body(command: str) -> bool:
    lower = command.lower()
    return any(token in lower for token in ("memory/work", "memory/learning", "memory/knowledge"))


def _command_reads_isa_body(command: str) -> bool:
    lower = command.lower()
    return "/isa" in lower or " isa/" in lower or "isa/" in lower


def _command_reads_pulse_payload(command: str) -> bool:
    return "pulse/events" in command.lower()


def _classify_event_path(pai_dir: Path, run_dir: Path, raw: str) -> tuple[str, str]:
    text = raw.strip()
    if text.startswith("file://"):
        text = text[7:]
    if text.startswith("~/"):
        candidates = [Path.home() / text[2:]]
    else:
        raw_path = Path(text)
        candidates = [raw_path] if raw_path.is_absolute() else [run_dir / raw_path, pai_dir / raw_path]

    for candidate in candidates:
        resolved = candidate.resolve(strict=False)
        if _is_within(run_dir, resolved):
            return "approved_pai_run_writes", str(resolved)
        relative = _relative_to_pai(pai_dir, resolved)
        if relative is None:
            continue
        if relative in STATE_PROPOSAL_INSTALL_RELATIVES:
            return "approved_pai_run_writes", str(resolved)
        state_class = _state_write_class(relative)
        if state_class is not None:
            return "forbidden_semantic_write", str(resolved)
        if _is_known_ambient_churn(relative):
            return "ambient_pai_state_churn", str(resolved)
    return "unknown_unclassified_write", raw


def _scan_pai_filesystem(
    pai_dir: Path,
    marker: Path,
    run_dir: Path,
) -> tuple[list[str], list[str], list[str], list[str], list[str], list[str]]:
    approved_run: list[str] = []
    ambient: list[str] = []
    forbidden: list[str] = []
    unknown: list[str] = []
    memory_modified: list[str] = []
    isa_modified: list[str] = []
    pulse_modified: list[str] = []
    marker_mtime = marker.stat().st_mtime

    for path in pai_dir.rglob("*"):
        try:
            if path.lstat().st_mtime < marker_mtime:
                continue
        except OSError:
            continue
        display = str(path)
        if path.is_symlink():
            unknown.append(display)
            continue
        if not path.is_file():
            continue
        resolved = path.resolve(strict=False)
        relative_path = _relative_to_pai(pai_dir, resolved)
        if relative_path is None:
            unknown.append(display)
            continue
        if _is_within(run_dir, resolved):
            approved_run.append(display)
            continue
        if relative_path in STATE_PROPOSAL_INSTALL_RELATIVES:
            approved_run.append(display)
            continue
        state_class = _state_write_class(relative_path)
        if state_class == "memory":
            memory_modified.append(display)
            forbidden.append(display)
        elif state_class == "isa":
            isa_modified.append(display)
            forbidden.append(display)
        elif state_class == "pulse":
            pulse_modified.append(display)
            forbidden.append(display)
        elif _is_known_ambient_churn(relative_path):
            ambient.append(display)
        else:
            unknown.append(display)
    return approved_run, ambient, forbidden, unknown, memory_modified + isa_modified, pulse_modified


def audit_state_proposal_run(
    *,
    pai_dir: Path,
    marker: Path,
    run_dir: Path,
    capsule_path: Path,
    proposal_path: Path,
    events_path: Path,
    runtime_attempt_number: int = 1,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    pai_dir = pai_dir.resolve(strict=True)
    marker = marker.resolve(strict=True)
    run_dir = run_dir.resolve(strict=True)
    repo_root = (repo_root or Path.cwd()).resolve(strict=False)

    state_context_capsule_present = capsule_path.is_file()
    state_proposal_present = proposal_path.is_file()
    event_logs_present = events_path.is_file() and events_path.stat().st_size > 0
    capsule = _load_json(capsule_path, STATE_CONTEXT_CAPSULE_NAME) if state_context_capsule_present else {}
    proposal = _load_json(proposal_path, STATE_PROPOSAL_NAME) if state_proposal_present else {}
    state = _try_load_json(run_dir / STATE_PROPOSAL_STATE_NAME)

    capsule_errors = validate_state_context_capsule(capsule) if state_context_capsule_present else [f"{STATE_CONTEXT_CAPSULE_NAME} is missing"]
    proposal_errors = validate_state_proposal(proposal) if state_proposal_present else [f"{STATE_PROPOSAL_NAME} is missing"]
    schema_errors = (
        _schema_errors(proposal, pai_dir / "runtime-schemas" / "state-proposal.schema.json", STATE_PROPOSAL_NAME)
        if state_proposal_present
        else [f"{STATE_PROPOSAL_NAME} is missing"]
    )
    state_proposal_schema_valid = state_proposal_present and not schema_errors
    state_proposal_semantically_valid = state_proposal_present and not proposal_errors
    state_context_capsule_metadata_only = capsule.get("metadata_only") is True and proposal.get("context_capsule_metadata_only") is True
    memory_proposals_proposed_only = all_memory_proposals_proposed_only(proposal)
    isa_proposals_proposed_only = all_isa_proposals_proposed_only(proposal)

    event_items, event_warnings = _parse_events(events_path)
    codex_file_change_events: list[dict[str, Any]] = []
    codex_command_execution_events: list[dict[str, Any]] = []
    forbidden_event_writes: list[str] = []
    unknown_event_writes: list[str] = []
    runtime_probe_events: list[dict[str, Any]] = []
    memory_body_read_events: list[str] = []
    isa_body_read_events: list[str] = []
    pulse_payload_read_events: list[str] = []
    event_file_change_outside_approved = False

    for event in event_items:
        if _looks_like_file_change(event):
            classifications = [_classify_event_path(pai_dir, run_dir, raw) for raw in _extract_paths(event)]
            approved = bool(classifications) and all(
                classification == "approved_pai_run_writes" for classification, _ in classifications
            )
            codex_file_change_events.append(
                {
                    "classification": "codex_event_file_change",
                    "approved": approved,
                    "paths": [_redact_pai_text(pai_dir, path) for _, path in classifications],
                    "event_type": _event_type(event),
                }
            )
            if not approved:
                event_file_change_outside_approved = True
                for classification, path in classifications:
                    if classification == "forbidden_semantic_write":
                        forbidden_event_writes.append(path)
                    elif classification == "unknown_unclassified_write":
                        unknown_event_writes.append(path)

        if _looks_like_command_execution(event):
            command = _command_text(event)
            codex_command_execution_events.append(
                {
                    "classification": "codex_event_command_execution",
                    "command": _redact_pai_text(pai_dir, command),
                    "event_type": _event_type(event),
                }
            )
            if _command_has_runtime_probe(command):
                runtime_probe_events.append({"classification": "forbidden_runtime_probe", "command": command})
            if _command_reads_memory_body(command):
                memory_body_read_events.append(command)
            if _command_reads_isa_body(command):
                isa_body_read_events.append(command)
            if _command_reads_pulse_payload(command):
                pulse_payload_read_events.append(command)

    approved_run, ambient, forbidden_fs, unknown_fs, memory_isa_modified, pulse_modified = _scan_pai_filesystem(
        pai_dir,
        marker,
        run_dir,
    )
    memory_files_modified = any("/Memory/" in item or "\\Memory\\" in item for item in memory_isa_modified)
    isa_files_modified = any("/ISA/" in item or item.endswith("/ISA") or "\\ISA\\" in item for item in memory_isa_modified)
    pulse_files_modified = bool(pulse_modified)

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

    memory_body_read_by_codex = bool(memory_body_read_events)
    isa_body_read_by_codex = bool(isa_body_read_events)
    pulse_event_payload_read_by_codex = bool(pulse_payload_read_events)
    memory_write_performed_by_codex = memory_files_modified or proposal.get("memory_write_performed") is True
    isa_write_performed_by_codex = isa_files_modified or proposal.get("isa_write_performed") is True
    pulse_probe_performed_by_codex = bool(runtime_probe_events) or proposal.get("pulse_probe_performed") is True
    localhost_31337_called_by_codex = any(
        "localhost:31337" in json.dumps(event).lower() or "127.0.0.1:31337" in json.dumps(event).lower()
        for event in event_items
        if _looks_like_command_execution(event)
    ) or proposal.get("localhost_31337_called") is True

    forbidden_semantic_writes = sorted(
        set(forbidden_fs + forbidden_event_writes + capsule_errors + proposal_errors + schema_errors)
    )
    unknown_unclassified_writes = sorted(set(unknown_fs + unknown_event_writes))
    event_attribution_passed = not (
        event_warnings
        or event_file_change_outside_approved
        or forbidden_event_writes
        or unknown_event_writes
        or memory_body_read_by_codex
        or isa_body_read_by_codex
        or pulse_event_payload_read_by_codex
        or memory_write_performed_by_codex
        or isa_write_performed_by_codex
        or pulse_probe_performed_by_codex
        or localhost_31337_called_by_codex
    )
    validation_passed = bool(
        state_context_capsule_present
        and state_context_capsule_metadata_only
        and state_proposal_present
        and state_proposal_schema_valid
        and state_proposal_semantically_valid
        and memory_proposals_proposed_only
        and isa_proposals_proposed_only
        and not memory_files_modified
        and not isa_files_modified
        and not pulse_files_modified
        and event_logs_present
        and event_attribution_passed
        and not forbidden_semantic_writes
        and not unknown_unclassified_writes
        and not repo_root_agents_created
        and not repo_dotcodex_created
        and not codex_adapter_files_installed_under_home_codex
    )

    return {
        "milestone_name": S16A_MILESTONE,
        "run_id": S16A_RUN_ID,
        "runtime": "codex",
        "runtime_attempt_number": runtime_attempt_number,
        "pai_runtime_command": _redact_value(pai_dir, state.get("pai_runtime_command", [])),
        "provider_command": _redact_value(pai_dir, state.get("provider_command", [])),
        "state_context_capsule_present": state_context_capsule_present,
        "state_context_capsule_metadata_only": state_context_capsule_metadata_only,
        "state_proposal_present": state_proposal_present,
        "state_proposal_schema_valid": state_proposal_schema_valid,
        "state_proposal_semantically_valid": state_proposal_semantically_valid,
        "all_memory_proposals_proposed_only": memory_proposals_proposed_only,
        "all_isa_proposals_proposed_only": isa_proposals_proposed_only,
        "memory_files_modified": memory_files_modified,
        "isa_files_modified": isa_files_modified,
        "pulse_files_modified": pulse_files_modified,
        "event_logs_present": event_logs_present,
        "event_attribution_passed": event_attribution_passed,
        "codex_file_change_events": codex_file_change_events,
        "codex_command_execution_events": codex_command_execution_events,
        "approved_pai_run_writes": sorted(_redact_pai_text(pai_dir, item) for item in approved_run),
        "ambient_pai_state_churn": sorted(_redact_pai_text(pai_dir, item) for item in ambient),
        "forbidden_semantic_writes": sorted(_redact_pai_text(pai_dir, item) for item in forbidden_semantic_writes),
        "unknown_unclassified_writes": sorted(_redact_pai_text(pai_dir, item) for item in unknown_unclassified_writes),
        "memory_body_read_by_codex": memory_body_read_by_codex,
        "isa_body_read_by_codex": isa_body_read_by_codex,
        "pulse_event_payload_read_by_codex": pulse_event_payload_read_by_codex,
        "memory_write_performed_by_codex": memory_write_performed_by_codex,
        "isa_write_performed_by_codex": isa_write_performed_by_codex,
        "pulse_probe_performed_by_codex": pulse_probe_performed_by_codex,
        "localhost_31337_called_by_codex": localhost_31337_called_by_codex,
        "repo_root_agents_created": repo_root_agents_created,
        "repo_dotcodex_created": repo_dotcodex_created,
        "codex_adapter_files_installed_under_home_codex": codex_adapter_files_installed_under_home_codex,
        "validation_passed": validation_passed,
        "known_limits": [
            "S16A stores Memory/ISA proposals only as PAI-owned run artifacts.",
            "S16A does not apply proposals to Memory or ISA.",
            "Filesystem mtime scanning is a secondary detector for forbidden state writes.",
        ],
    }
