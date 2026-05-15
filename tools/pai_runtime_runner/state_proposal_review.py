from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.pai_runtime_runner.pai_context import collect_pai_context_metadata, validate_context_capsule
from tools.pai_runtime_runner.state_proposal import (
    MARKER_VALUE,
    PAI_DIR_LABEL,
    S16A_RUN_ID,
    STATE_PROPOSAL_NAME,
    _command_has_runtime_probe,
    _command_reads_isa_body,
    _command_reads_memory_body,
    _command_reads_pulse_payload,
    _command_text,
    _event_type,
    _extract_paths,
    _is_known_ambient_churn,
    _is_within,
    _looks_like_command_execution,
    _looks_like_file_change,
    _parse_events,
    _redact_pai_text,
    _redact_value,
    _relative_to_pai,
    _schema_errors,
    _state_write_class,
    validate_state_proposal,
)

try:
    from jsonschema import Draft202012Validator
except Exception:  # noqa: BLE001 - review validation reports unavailable schema validation.
    Draft202012Validator = None  # type: ignore[assignment]


S16B_MILESTONE = "V5-S16B-PAI-STATE-PROPOSAL-REVIEW-POLICY"
S16B_RUN_ID = "s16b-proposal-review"
S16B_TASK_ID = "s16b-state-proposal-review-task"
S16B_TASK_KIND = "proposal-review-without-commit"
S16B_RUN_RELATIVE = Path("runs") / "s16b" / "proposal-review"
S16B_TASK_RELATIVE = Path("runtime-tasks") / "s16b-state-proposal-review-task.json"
S16B_SOURCE_PROPOSAL_RELATIVE = Path("runs") / "s16a" / "state-proposal" / STATE_PROPOSAL_NAME
REVIEW_CONTEXT_CAPSULE_NAME = "review-context-capsule.json"
STATE_PROPOSAL_REVIEW_NAME = "state-proposal-review.json"
STATE_PROPOSAL_DECISIONS_NAME = "state-proposal-decisions.json"
STATE_PROPOSAL_REVIEW_EVENTS_NAME = "state-proposal-review-events.jsonl"
STATE_PROPOSAL_REVIEW_VALIDATION_NAME = "state-proposal-review-validation.json"
STATE_PROPOSAL_REVIEW_SCHEMA_NAME = "state-proposal-review.schema.json"
STATE_PROPOSAL_DECISIONS_SCHEMA_NAME = "state-proposal-decisions.schema.json"
STATE_PROPOSAL_REVIEW_STATE_NAME = "state-proposal-review-state.json"

DECISION_VALUES = {
    "approved_for_future_commit_candidate",
    "rejected",
    "deferred",
    "needs_revision",
}

STATE_PROPOSAL_REVIEW_INSTALL_RELATIVES = {
    Path("bin") / "pai-runtime",
    Path("runtime-state.json"),
    Path("runtime-schemas") / "state-proposal-review-task.schema.json",
    Path("runtime-schemas") / "state-proposal-review.schema.json",
    Path("runtime-schemas") / "state-proposal-decisions.schema.json",
    Path("runtime-schemas") / "state-proposal-review-validation.schema.json",
    Path("runtime-tasks") / "s16b-state-proposal-review-task.json",
    Path("runtimes") / "codex" / "provider-manifest.json",
}


class StateProposalReviewError(ValueError):
    pass


def _load_json(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise StateProposalReviewError(f"{label} is missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise StateProposalReviewError(f"{label} is not valid JSON") from exc
    if not isinstance(data, dict):
        raise StateProposalReviewError(f"{label} must be a JSON object")
    return data


def _try_load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _proposal_items(source_proposal: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = source_proposal.get(key)
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _proposal_id(prefix: str, index: int) -> str:
    return f"{prefix}-{index}"


def load_source_state_proposal(path: Path) -> dict[str, Any]:
    proposal = _load_json(path, STATE_PROPOSAL_NAME)
    errors = validate_state_proposal(proposal)
    if errors:
        raise StateProposalReviewError("; ".join(errors))
    return proposal


def collect_review_context_metadata(pai_dir: Path, source_proposal: dict[str, Any]) -> dict[str, Any]:
    capsule = collect_pai_context_metadata(pai_dir)
    memory_items = _proposal_items(source_proposal, "memory_proposals")
    isa_items = _proposal_items(source_proposal, "isa_proposals")
    capsule.update(
        {
            "milestone_name": S16B_MILESTONE,
            "run_id": S16B_RUN_ID,
            "task_id": S16B_TASK_ID,
            "task_kind": S16B_TASK_KIND,
            "source_proposal_run_id": source_proposal.get("run_id"),
            "source_proposal_metadata": {
                "memory_proposal_count": len(memory_items),
                "isa_proposal_count": len(isa_items),
                "all_memory_apply_status_proposed_only": all(
                    item.get("apply_status") == "proposed_only" for item in memory_items
                ),
                "all_isa_apply_status_proposed_only": all(
                    item.get("apply_status") == "proposed_only" for item in isa_items
                ),
            },
            "review_policy": [
                "S16B admits memory.proposal.review and isa.proposal.review only.",
                "Codex may review proposal-only Memory/ISA updates but must not commit them.",
                "PAI owns final review decisions and stores them as non-committing run artifacts.",
                "Every decision must use commit_status=not_committed.",
                "Pulse probing and Pulse event emission remain forbidden.",
            ],
        }
    )
    errors = validate_review_context_capsule(capsule)
    if errors:
        raise StateProposalReviewError("; ".join(errors))
    return capsule


def validate_review_context_capsule(capsule: dict[str, Any]) -> list[str]:
    errors = validate_context_capsule(capsule)
    expected = {
        "milestone_name": S16B_MILESTONE,
        "run_id": S16B_RUN_ID,
        "task_id": S16B_TASK_ID,
        "task_kind": S16B_TASK_KIND,
        "source_proposal_run_id": S16A_RUN_ID,
        "metadata_only": True,
        "redacted_paths": True,
    }
    for key, expected_value in expected.items():
        if capsule.get(key) != expected_value:
            errors.append(f"review context capsule mismatch for {key}")
    if not isinstance(capsule.get("review_policy"), list) or not capsule.get("review_policy"):
        errors.append("review context capsule must include review_policy")
    metadata = capsule.get("source_proposal_metadata")
    if not isinstance(metadata, dict):
        errors.append("review context capsule must include source_proposal_metadata")
    return errors


def _coerce_review_items(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _string_value(value: Any, fallback: str) -> str:
    return value if isinstance(value, str) and value else fallback


def _decision_value(value: Any, fallback: str = "needs_revision") -> str:
    return value if isinstance(value, str) and value in DECISION_VALUES else fallback


def _default_decision(source_item: dict[str, Any]) -> str:
    confidence = source_item.get("confidence")
    if source_item.get("apply_status") != "proposed_only":
        return "rejected"
    if isinstance(confidence, (int, float)) and confidence >= 0.7:
        return "approved_for_future_commit_candidate"
    return "needs_revision"


def _normalize_review_list(
    provider_items: Any,
    source_items: list[dict[str, Any]],
    prefix: str,
) -> list[dict[str, Any]]:
    provider_by_id: dict[str, dict[str, Any]] = {}
    for item in _coerce_review_items(provider_items):
        proposal_id = item.get("proposal_id")
        if isinstance(proposal_id, str) and proposal_id:
            provider_by_id[proposal_id] = item

    reviews: list[dict[str, Any]] = []
    for index, source_item in enumerate(source_items):
        proposal_id = _proposal_id(prefix, index)
        provider_item = provider_by_id.get(proposal_id, {})
        title = _string_value(provider_item.get("title"), _string_value(source_item.get("title"), proposal_id))
        default_decision = _default_decision(source_item)
        recommended = _decision_value(provider_item.get("recommended_decision"), default_decision)
        reviews.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "review_summary": _string_value(
                    provider_item.get("review_summary"),
                    "PAI normalized this review from the accepted S16A proposal artifact.",
                ),
                "rationale": _string_value(
                    provider_item.get("rationale"),
                    "S16B review remains non-committing and requires later human-gated policy before any commit.",
                ),
                "recommended_decision": recommended,
                "commit_status": "not_committed",
            }
        )
    return reviews


def normalize_state_proposal_review(
    provider_result: dict[str, Any],
    source_proposal: dict[str, Any],
    capsule: dict[str, Any],
) -> dict[str, Any]:
    review = {
        "milestone_name": S16B_MILESTONE,
        "run_id": S16B_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "task_id": S16B_TASK_ID,
        "task_kind": S16B_TASK_KIND,
        "adapter_identity_marker": MARKER_VALUE,
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "source_proposal_run_id": S16A_RUN_ID,
        "source_proposal_used": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": capsule.get("metadata_only") is True,
        "memory_proposal_reviews": _normalize_review_list(
            provider_result.get("memory_proposal_reviews"),
            _proposal_items(source_proposal, "memory_proposals"),
            "memory",
        ),
        "isa_proposal_reviews": _normalize_review_list(
            provider_result.get("isa_proposal_reviews"),
            _proposal_items(source_proposal, "isa_proposals"),
            "isa",
        ),
        "commit_authority_requested": False,
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_write_performed": False,
        "isa_write_performed": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
        "evidence_classification": [
            "PAI-owned state proposal review evidence",
            "review-only Memory/ISA proposal policy",
            "not Memory/ISA commit authority",
        ],
        "known_limits": [
            "S16B reviews proposals only and does not apply them to Memory or ISA.",
            "PAI owns final decisions and stores them only as run artifacts.",
            "A later commit policy milestone requires separate architect approval.",
        ],
    }
    errors = validate_state_proposal_review(review)
    if errors:
        raise StateProposalReviewError("; ".join(errors))
    return review


def validate_state_proposal_review(review: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "milestone_name": S16B_MILESTONE,
        "run_id": S16B_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "task_id": S16B_TASK_ID,
        "task_kind": S16B_TASK_KIND,
        "adapter_identity_marker": MARKER_VALUE,
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "source_proposal_run_id": S16A_RUN_ID,
        "source_proposal_used": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": True,
        "commit_authority_requested": False,
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_write_performed": False,
        "isa_write_performed": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
    }
    for key, value in expected.items():
        if review.get(key) != value:
            errors.append(f"state proposal review mismatch for {key}")

    for collection_name in ("memory_proposal_reviews", "isa_proposal_reviews"):
        items = review.get(collection_name)
        if not isinstance(items, list):
            errors.append(f"{collection_name} must be a list")
            continue
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"{collection_name}[{index}] must be an object")
                continue
            for key in ("proposal_id", "title", "review_summary", "rationale", "recommended_decision", "commit_status"):
                if key not in item:
                    errors.append(f"{collection_name}[{index}] missing {key}")
            if item.get("recommended_decision") not in DECISION_VALUES:
                errors.append(f"{collection_name}[{index}].recommended_decision is invalid")
            if item.get("commit_status") != "not_committed":
                errors.append(f"{collection_name}[{index}].commit_status must be not_committed")

    raw = json.dumps(review, sort_keys=True)
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
            errors.append(f"state proposal review contains forbidden token: {token}")
    return errors


def normalize_state_proposal_decisions(review: dict[str, Any]) -> dict[str, Any]:
    def decisions_from_reviews(collection_name: str) -> list[dict[str, Any]]:
        decisions: list[dict[str, Any]] = []
        for item in review.get(collection_name, []):
            if not isinstance(item, dict):
                continue
            decisions.append(
                {
                    "proposal_id": _string_value(item.get("proposal_id"), "unknown"),
                    "decision": _decision_value(item.get("recommended_decision")),
                    "rationale": _string_value(
                        item.get("rationale"),
                        "PAI preserved a non-committing review-only decision.",
                    ),
                    "commit_status": "not_committed",
                }
            )
        return decisions

    decisions = {
        "milestone_name": S16B_MILESTONE,
        "run_id": S16B_RUN_ID,
        "source_proposal_run_id": S16A_RUN_ID,
        "decision_authority": "pai-policy",
        "decision_mode": "review-only",
        "memory_decisions": decisions_from_reviews("memory_proposal_reviews"),
        "isa_decisions": decisions_from_reviews("isa_proposal_reviews"),
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_files_modified": False,
        "isa_files_modified": False,
        "pulse_files_modified": False,
        "known_limits": [
            "S16B decisions are candidates only and do not commit Memory or ISA.",
            "commit_status remains not_committed for every decision.",
            "A later commit policy milestone requires separate architect approval.",
        ],
    }
    errors = validate_state_proposal_decisions(decisions)
    if errors:
        raise StateProposalReviewError("; ".join(errors))
    return decisions


def validate_state_proposal_decisions(decisions: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "milestone_name": S16B_MILESTONE,
        "run_id": S16B_RUN_ID,
        "source_proposal_run_id": S16A_RUN_ID,
        "decision_authority": "pai-policy",
        "decision_mode": "review-only",
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_files_modified": False,
        "isa_files_modified": False,
        "pulse_files_modified": False,
    }
    for key, value in expected.items():
        if decisions.get(key) != value:
            errors.append(f"state proposal decisions mismatch for {key}")

    for collection_name in ("memory_decisions", "isa_decisions"):
        items = decisions.get(collection_name)
        if not isinstance(items, list):
            errors.append(f"{collection_name} must be a list")
            continue
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"{collection_name}[{index}] must be an object")
                continue
            for key in ("proposal_id", "decision", "rationale", "commit_status"):
                if key not in item:
                    errors.append(f"{collection_name}[{index}] missing {key}")
            if item.get("decision") not in DECISION_VALUES:
                errors.append(f"{collection_name}[{index}].decision is invalid")
            if item.get("commit_status") != "not_committed":
                errors.append(f"{collection_name}[{index}].commit_status must be not_committed")
    return errors


def all_decisions_non_committing(decisions: dict[str, Any]) -> bool:
    if decisions.get("commit_authority_granted") is not False or decisions.get("commit_performed") is not False:
        return False
    for collection_name in ("memory_decisions", "isa_decisions"):
        items = decisions.get(collection_name)
        if not isinstance(items, list):
            return False
        for item in items:
            if not isinstance(item, dict) or item.get("commit_status") != "not_committed":
                return False
    return True


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
        if relative in STATE_PROPOSAL_REVIEW_INSTALL_RELATIVES:
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
) -> tuple[list[str], list[str], list[str], list[str], list[str], list[str], list[str]]:
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
        if relative_path in STATE_PROPOSAL_REVIEW_INSTALL_RELATIVES:
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
    return approved_run, ambient, forbidden, unknown, memory_modified, isa_modified, pulse_modified


def audit_state_proposal_review_run(
    *,
    pai_dir: Path,
    marker: Path,
    run_dir: Path,
    source_proposal_path: Path,
    capsule_path: Path,
    review_path: Path,
    decisions_path: Path,
    events_path: Path,
    runtime_attempt_number: int = 1,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    pai_dir = pai_dir.resolve(strict=True)
    marker = marker.resolve(strict=True)
    run_dir = run_dir.resolve(strict=True)
    repo_root = (repo_root or Path.cwd()).resolve(strict=False)

    source_proposal_present = source_proposal_path.is_file()
    review_context_capsule_present = capsule_path.is_file()
    state_proposal_review_present = review_path.is_file()
    state_proposal_decisions_present = decisions_path.is_file()
    event_logs_present = events_path.is_file() and events_path.stat().st_size > 0

    source_proposal = _load_json(source_proposal_path, STATE_PROPOSAL_NAME) if source_proposal_present else {}
    capsule = _load_json(capsule_path, REVIEW_CONTEXT_CAPSULE_NAME) if review_context_capsule_present else {}
    review = _load_json(review_path, STATE_PROPOSAL_REVIEW_NAME) if state_proposal_review_present else {}
    decisions = _load_json(decisions_path, STATE_PROPOSAL_DECISIONS_NAME) if state_proposal_decisions_present else {}
    state = _try_load_json(run_dir / STATE_PROPOSAL_REVIEW_STATE_NAME)

    source_errors = validate_state_proposal(source_proposal) if source_proposal_present else [f"{STATE_PROPOSAL_NAME} is missing"]
    source_schema_errors = (
        _schema_errors(source_proposal, pai_dir / "runtime-schemas" / "state-proposal.schema.json", STATE_PROPOSAL_NAME)
        if source_proposal_present
        else [f"{STATE_PROPOSAL_NAME} is missing"]
    )
    capsule_errors = (
        validate_review_context_capsule(capsule)
        if review_context_capsule_present
        else [f"{REVIEW_CONTEXT_CAPSULE_NAME} is missing"]
    )
    review_errors = (
        validate_state_proposal_review(review)
        if state_proposal_review_present
        else [f"{STATE_PROPOSAL_REVIEW_NAME} is missing"]
    )
    review_schema_errors = (
        _schema_errors(review, pai_dir / "runtime-schemas" / "state-proposal-review.schema.json", STATE_PROPOSAL_REVIEW_NAME)
        if state_proposal_review_present
        else [f"{STATE_PROPOSAL_REVIEW_NAME} is missing"]
    )
    decisions_errors = (
        validate_state_proposal_decisions(decisions)
        if state_proposal_decisions_present
        else [f"{STATE_PROPOSAL_DECISIONS_NAME} is missing"]
    )
    decisions_schema_errors = (
        _schema_errors(
            decisions,
            pai_dir / "runtime-schemas" / "state-proposal-decisions.schema.json",
            STATE_PROPOSAL_DECISIONS_NAME,
        )
        if state_proposal_decisions_present
        else [f"{STATE_PROPOSAL_DECISIONS_NAME} is missing"]
    )

    source_proposal_schema_valid = source_proposal_present and not source_errors and not source_schema_errors
    review_context_capsule_metadata_only = capsule.get("metadata_only") is True and review.get("context_capsule_metadata_only") is True
    state_proposal_review_schema_valid = state_proposal_review_present and not review_errors and not review_schema_errors
    state_proposal_decisions_schema_valid = state_proposal_decisions_present and not decisions_errors and not decisions_schema_errors
    decisions_non_committing = all_decisions_non_committing(decisions)
    commit_authority_granted = (
        review.get("commit_authority_granted") is True or decisions.get("commit_authority_granted") is True
    )
    commit_performed = review.get("commit_performed") is True or decisions.get("commit_performed") is True

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

    approved_run, ambient, forbidden_fs, unknown_fs, memory_modified, isa_modified, pulse_modified = _scan_pai_filesystem(
        pai_dir,
        marker,
        run_dir,
    )
    memory_files_modified = bool(memory_modified) or decisions.get("memory_files_modified") is True
    isa_files_modified = bool(isa_modified) or decisions.get("isa_files_modified") is True
    pulse_files_modified = bool(pulse_modified) or decisions.get("pulse_files_modified") is True

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
    memory_write_performed_by_codex = memory_files_modified or review.get("memory_write_performed") is True
    isa_write_performed_by_codex = isa_files_modified or review.get("isa_write_performed") is True
    pulse_probe_performed_by_codex = bool(runtime_probe_events) or review.get("pulse_probe_performed") is True
    localhost_31337_called_by_codex = any(
        "localhost:31337" in json.dumps(event).lower() or "127.0.0.1:31337" in json.dumps(event).lower()
        for event in event_items
        if _looks_like_command_execution(event)
    ) or review.get("localhost_31337_called") is True

    semantic_errors = (
        source_errors
        + source_schema_errors
        + capsule_errors
        + review_errors
        + review_schema_errors
        + decisions_errors
        + decisions_schema_errors
    )
    forbidden_semantic_writes = sorted(set(forbidden_fs + forbidden_event_writes + semantic_errors))
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
        source_proposal_present
        and source_proposal_schema_valid
        and review_context_capsule_present
        and review_context_capsule_metadata_only
        and state_proposal_review_present
        and state_proposal_review_schema_valid
        and state_proposal_decisions_present
        and state_proposal_decisions_schema_valid
        and decisions_non_committing
        and not commit_authority_granted
        and not commit_performed
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
        "milestone_name": S16B_MILESTONE,
        "run_id": S16B_RUN_ID,
        "runtime": "codex",
        "runtime_attempt_number": runtime_attempt_number,
        "pai_runtime_command": _redact_value(pai_dir, state.get("pai_runtime_command", [])),
        "provider_command": _redact_value(pai_dir, state.get("provider_command", [])),
        "source_proposal_present": source_proposal_present,
        "source_proposal_schema_valid": source_proposal_schema_valid,
        "review_context_capsule_present": review_context_capsule_present,
        "review_context_capsule_metadata_only": review_context_capsule_metadata_only,
        "state_proposal_review_present": state_proposal_review_present,
        "state_proposal_review_schema_valid": state_proposal_review_schema_valid,
        "state_proposal_decisions_present": state_proposal_decisions_present,
        "state_proposal_decisions_schema_valid": state_proposal_decisions_schema_valid,
        "all_decisions_non_committing": decisions_non_committing,
        "commit_authority_granted": commit_authority_granted,
        "commit_performed": commit_performed,
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
            "S16B stores proposal review decisions only as PAI-owned run artifacts.",
            "S16B does not grant commit authority and does not apply Memory or ISA writes.",
            "Filesystem mtime scanning is a secondary detector for forbidden state writes.",
        ],
    }
