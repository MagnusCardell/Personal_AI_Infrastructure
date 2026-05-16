from __future__ import annotations

import json
import re
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
from tools.pai_runtime_runner.state_proposal_review import (
    S16B_RUN_ID,
    STATE_PROPOSAL_DECISIONS_NAME,
    load_source_state_proposal,
    validate_state_proposal_decisions,
)

try:
    from jsonschema import Draft202012Validator
except Exception:  # noqa: BLE001 - validation reports unavailable schema validation.
    Draft202012Validator = None  # type: ignore[assignment]


S16C_MILESTONE = "V5-S16C-PAI-STATE-COMMIT-DRY-RUN"
S16C_RUN_ID = "s16c-commit-dry-run"
S16C_TASK_ID = "s16c-state-commit-dry-run-task"
S16C_TASK_KIND = "human-gated-state-commit-dry-run"
S16C_RUN_RELATIVE = Path("runs") / "s16c" / "commit-dry-run"
S16C_TASK_RELATIVE = Path("runtime-tasks") / "s16c-state-commit-dry-run-task.json"
S16C_SOURCE_PROPOSAL_RELATIVE = Path("runs") / "s16a" / "state-proposal" / STATE_PROPOSAL_NAME
S16C_SOURCE_DECISIONS_RELATIVE = Path("runs") / "s16b" / "proposal-review" / STATE_PROPOSAL_DECISIONS_NAME
S16C_HUMAN_GATE = "S16C_DRY_RUN_ONLY_NO_MEMORY_ISA_WRITE"

COMMIT_DRY_RUN_CONTEXT_CAPSULE_NAME = "commit-dry-run-context-capsule.json"
STATE_COMMIT_DRY_RUN_REVIEW_NAME = "state-commit-dry-run-review.json"
STATE_COMMIT_DRY_RUN_PLAN_NAME = "state-commit-dry-run-plan.json"
STATE_COMMIT_DRY_RUN_EVENTS_NAME = "state-commit-dry-run-events.jsonl"
STATE_COMMIT_DRY_RUN_VALIDATION_NAME = "state-commit-dry-run-validation.json"
STATE_COMMIT_DRY_RUN_REVIEW_SCHEMA_NAME = "state-commit-dry-run-review.schema.json"
STATE_COMMIT_DRY_RUN_PLAN_SCHEMA_NAME = "state-commit-dry-run-plan.schema.json"
STATE_COMMIT_DRY_RUN_STATE_NAME = "state-commit-dry-run-state.json"

APPROVED_DECISION = "approved_for_future_commit_candidate"
NOT_COMMITTED = "not_committed"
NOT_WRITTEN = "not_written"
ALLOWED_MEMORY_CATEGORIES = {"WORK", "LEARNING", "KNOWLEDGE"}
ALLOWED_TARGET_PREFIXES = (
    "Memory/WORK/",
    "Memory/LEARNING/",
    "Memory/KNOWLEDGE/",
    "ISA/",
)

STATE_COMMIT_DRY_RUN_INSTALL_RELATIVES = {
    Path("bin") / "pai-runtime",
    Path("runtime-state.json"),
    Path("runtime-schemas") / "state-commit-dry-run-task.schema.json",
    Path("runtime-schemas") / "state-commit-dry-run-review.schema.json",
    Path("runtime-schemas") / "state-commit-dry-run-plan.schema.json",
    Path("runtime-schemas") / "state-commit-dry-run-validation.schema.json",
    Path("runtime-tasks") / "s16c-state-commit-dry-run-task.json",
    Path("runtimes") / "codex" / "provider-manifest.json",
}


class StateCommitDryRunError(ValueError):
    pass


def _load_json(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise StateCommitDryRunError(f"{label} is missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise StateCommitDryRunError(f"{label} is not valid JSON") from exc
    if not isinstance(data, dict):
        raise StateCommitDryRunError(f"{label} must be a JSON object")
    return data


def _try_load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def validate_human_gate(value: str | None) -> None:
    if value != S16C_HUMAN_GATE:
        raise StateCommitDryRunError(f"--human-gate must be exactly {S16C_HUMAN_GATE}")


def load_source_state_decisions(path: Path) -> dict[str, Any]:
    decisions = _load_json(path, STATE_PROPOSAL_DECISIONS_NAME)
    errors = validate_state_proposal_decisions(decisions)
    if errors:
        raise StateCommitDryRunError("; ".join(errors))
    return decisions


def _proposal_items(source_proposal: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = source_proposal.get(key)
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _decision_items(source_decisions: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = source_decisions.get(key)
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _proposal_id(prefix: str, index: int) -> str:
    return f"{prefix}-{index}"


def _proposal_map(source_proposal: dict[str, Any], key: str, prefix: str) -> dict[str, dict[str, Any]]:
    return {
        _proposal_id(prefix, index): item
        for index, item in enumerate(_proposal_items(source_proposal, key))
    }


def _string_value(value: Any, fallback: str) -> str:
    return value if isinstance(value, str) and value else fallback


def _slug(value: str, fallback: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not cleaned:
        cleaned = fallback
    return cleaned[:60].strip("-") or fallback


def _preview(value: str, limit: int = 2000) -> str:
    text = value.strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _memory_target_path(proposal_id: str, proposal: dict[str, Any]) -> str:
    category = proposal.get("category")
    if category not in ALLOWED_MEMORY_CATEGORIES:
        raise StateCommitDryRunError(f"{proposal_id} has invalid Memory category for dry-run target")
    title = _string_value(proposal.get("title"), proposal_id)
    return f"Memory/{category}/s16c-dry-run/{proposal_id}-{_slug(title, proposal_id)}.md"


def _isa_target_path(proposal_id: str, proposal: dict[str, Any]) -> str:
    title = _string_value(proposal.get("title"), proposal_id)
    return f"ISA/s16c-dry-run/{proposal_id}-{_slug(title, proposal_id)}.md"


def _memory_rendered_content(proposal: dict[str, Any]) -> str:
    title = _string_value(proposal.get("title"), "Untitled Memory proposal")
    body = _string_value(proposal.get("proposed_body"), "")
    rationale = _string_value(proposal.get("rationale"), "")
    source_context = _string_value(proposal.get("source_context"), "")
    return _preview(f"# {title}\n\n{body}\n\nRationale: {rationale}\n\nSource context: {source_context}\n")


def _isa_rendered_content(proposal: dict[str, Any]) -> str:
    title = _string_value(proposal.get("title"), "Untitled ISA proposal")
    record = _string_value(proposal.get("proposed_record"), "")
    rationale = _string_value(proposal.get("rationale"), "")
    source_context = _string_value(proposal.get("source_context"), "")
    return _preview(f"# {title}\n\n{record}\n\nRationale: {rationale}\n\nSource context: {source_context}\n")


def _target_path_errors(value: Any) -> list[str]:
    if not isinstance(value, str) or value == "" or "\x00" in value:
        return ["relative_target_path must be a non-empty string"]
    if value.startswith("/") or value.startswith("~"):
        return [f"relative_target_path must be relative: {value}"]
    if "\\" in value:
        return [f"relative_target_path must use forward slashes: {value}"]
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return [f"relative_target_path must not contain empty, current, or traversal segments: {value}"]
    if not any(value.startswith(prefix) for prefix in ALLOWED_TARGET_PREFIXES):
        return [f"relative_target_path is outside allowed Memory/ISA dry-run families: {value}"]
    if value.startswith("Pulse/"):
        return [f"relative_target_path must not target Pulse: {value}"]
    return []


def _planned_write_items(plan: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for collection_name in ("planned_memory_writes", "planned_isa_writes"):
        collection = plan.get(collection_name)
        if isinstance(collection, list):
            items.extend(item for item in collection if isinstance(item, dict))
    return items


def all_planned_writes_not_written(plan: dict[str, Any]) -> bool:
    return all(item.get("dry_run_status") == NOT_WRITTEN for item in _planned_write_items(plan))


def all_target_paths_relative(plan: dict[str, Any]) -> bool:
    for item in _planned_write_items(plan):
        target = item.get("relative_target_path")
        if not isinstance(target, str) or target.startswith("/") or ".." in target.split("/"):
            return False
    return True


def all_target_paths_allowed(plan: dict[str, Any]) -> bool:
    return all(not _target_path_errors(item.get("relative_target_path")) for item in _planned_write_items(plan))


def _candidate_decision(decision: dict[str, Any]) -> bool:
    return decision.get("decision") == APPROVED_DECISION and decision.get("commit_status") == NOT_COMMITTED


def _decision_record(item: dict[str, Any], family: str) -> dict[str, Any]:
    return {
        "proposal_id": _string_value(item.get("proposal_id"), "unknown"),
        "decision_family": family,
        "decision": _string_value(item.get("decision"), "needs_revision"),
        "rationale": _string_value(item.get("rationale"), "PAI preserved the S16B decision."),
        "commit_status": _string_value(item.get("commit_status"), "unknown"),
    }


def collect_commit_dry_run_context_metadata(
    pai_dir: Path,
    source_proposal: dict[str, Any],
    source_decisions: dict[str, Any],
) -> dict[str, Any]:
    capsule = collect_pai_context_metadata(pai_dir)
    memory_decisions = _decision_items(source_decisions, "memory_decisions")
    isa_decisions = _decision_items(source_decisions, "isa_decisions")
    memory_candidates = [item for item in memory_decisions if _candidate_decision(item)]
    isa_candidates = [item for item in isa_decisions if _candidate_decision(item)]
    capsule.update(
        {
            "milestone_name": S16C_MILESTONE,
            "run_id": S16C_RUN_ID,
            "task_id": S16C_TASK_ID,
            "task_kind": S16C_TASK_KIND,
            "source_proposal_run_id": S16A_RUN_ID,
            "source_decisions_run_id": S16B_RUN_ID,
            "human_gate_required": S16C_HUMAN_GATE,
            "source_proposal_metadata": {
                "memory_proposal_count": len(_proposal_items(source_proposal, "memory_proposals")),
                "isa_proposal_count": len(_proposal_items(source_proposal, "isa_proposals")),
                "proposal_only": source_proposal.get("proposal_only") is True,
            },
            "source_decisions_metadata": {
                "memory_decision_count": len(memory_decisions),
                "isa_decision_count": len(isa_decisions),
                "candidate_decision_count": len(memory_candidates) + len(isa_candidates),
                "all_decisions_not_committed": all(
                    item.get("commit_status") == NOT_COMMITTED for item in memory_decisions + isa_decisions
                ),
                "commit_authority_granted": source_decisions.get("commit_authority_granted") is True,
                "commit_performed": source_decisions.get("commit_performed") is True,
            },
            "dry_run_policy": [
                "S16C admits memory.commit.dry_run and isa.commit.dry_run only.",
                "PAI may produce a human-gated dry-run commit plan from approved S16B candidates.",
                "S16C does not grant Memory write authority.",
                "S16C does not grant ISA write authority.",
                "Pulse probing and Pulse event emission remain forbidden.",
            ],
        }
    )
    errors = validate_commit_dry_run_context_capsule(capsule)
    if errors:
        raise StateCommitDryRunError("; ".join(errors))
    return capsule


def validate_commit_dry_run_context_capsule(capsule: dict[str, Any]) -> list[str]:
    errors = validate_context_capsule(capsule)
    expected = {
        "milestone_name": S16C_MILESTONE,
        "run_id": S16C_RUN_ID,
        "task_id": S16C_TASK_ID,
        "task_kind": S16C_TASK_KIND,
        "source_proposal_run_id": S16A_RUN_ID,
        "source_decisions_run_id": S16B_RUN_ID,
        "human_gate_required": S16C_HUMAN_GATE,
        "metadata_only": True,
        "redacted_paths": True,
    }
    for key, expected_value in expected.items():
        if capsule.get(key) != expected_value:
            errors.append(f"commit dry-run context capsule mismatch for {key}")
    if not isinstance(capsule.get("dry_run_policy"), list) or not capsule.get("dry_run_policy"):
        errors.append("commit dry-run context capsule must include dry_run_policy")
    if not isinstance(capsule.get("source_proposal_metadata"), dict):
        errors.append("commit dry-run context capsule must include source_proposal_metadata")
    if not isinstance(capsule.get("source_decisions_metadata"), dict):
        errors.append("commit dry-run context capsule must include source_decisions_metadata")
    return errors


def normalize_state_commit_dry_run_review(
    provider_result: dict[str, Any],
    capsule: dict[str, Any],
    human_gate: str,
) -> dict[str, Any]:
    validate_human_gate(human_gate)
    evidence = provider_result.get("evidence_classification")
    limits = provider_result.get("known_limits")
    review = {
        "milestone_name": S16C_MILESTONE,
        "run_id": S16C_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "task_id": S16C_TASK_ID,
        "task_kind": S16C_TASK_KIND,
        "adapter_identity_marker": MARKER_VALUE,
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "source_proposal_run_id": S16A_RUN_ID,
        "source_decisions_run_id": S16B_RUN_ID,
        "source_proposal_used": True,
        "source_decisions_used": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": capsule.get("metadata_only") is True,
        "human_gate_observed": True,
        "dry_run_only": True,
        "commit_authority_requested": False,
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_write_performed": False,
        "isa_write_performed": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
        "evidence_classification": evidence
        if isinstance(evidence, list)
        else [
            "PAI-owned state commit dry-run evidence",
            "dry-run-only Memory/ISA commit planning",
            "not Memory/ISA commit authority",
        ],
        "known_limits": limits
        if isinstance(limits, list)
        else [
            "S16C produces a dry-run plan only and does not apply Memory or ISA writes.",
            "Commit authority remains false and requires a later architect-approved milestone.",
            "Pulse probing and Pulse event emission remain blocked.",
        ],
    }
    errors = validate_state_commit_dry_run_review(review)
    if errors:
        raise StateCommitDryRunError("; ".join(errors))
    return review


def validate_state_commit_dry_run_review(review: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "milestone_name": S16C_MILESTONE,
        "run_id": S16C_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "task_id": S16C_TASK_ID,
        "task_kind": S16C_TASK_KIND,
        "adapter_identity_marker": MARKER_VALUE,
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "source_proposal_run_id": S16A_RUN_ID,
        "source_decisions_run_id": S16B_RUN_ID,
        "source_proposal_used": True,
        "source_decisions_used": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": True,
        "human_gate_observed": True,
        "dry_run_only": True,
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
            errors.append(f"state commit dry-run review mismatch for {key}")
    if not isinstance(review.get("evidence_classification"), list):
        errors.append("state commit dry-run review evidence_classification must be a list")
    if not isinstance(review.get("known_limits"), list):
        errors.append("state commit dry-run review known_limits must be a list")
    return errors


def build_commit_dry_run_plan(
    source_proposal: dict[str, Any],
    source_decisions: dict[str, Any],
    human_gate: str,
) -> dict[str, Any]:
    validate_human_gate(human_gate)
    proposal_errors = validate_state_proposal(source_proposal)
    decision_errors = validate_state_proposal_decisions(source_decisions)
    if proposal_errors or decision_errors:
        raise StateCommitDryRunError("; ".join(proposal_errors + decision_errors))

    memory_proposals = _proposal_map(source_proposal, "memory_proposals", "memory")
    isa_proposals = _proposal_map(source_proposal, "isa_proposals", "isa")
    candidate_decisions: list[dict[str, Any]] = []
    non_planned_decisions: list[dict[str, Any]] = []
    planned_memory_writes: list[dict[str, Any]] = []
    planned_isa_writes: list[dict[str, Any]] = []

    for item in _decision_items(source_decisions, "memory_decisions"):
        record = _decision_record(item, "memory")
        proposal_id = record["proposal_id"]
        if _candidate_decision(item):
            proposal = memory_proposals.get(proposal_id)
            if proposal is None:
                raise StateCommitDryRunError(f"approved Memory decision has no source proposal: {proposal_id}")
            candidate_decisions.append(record)
            planned_memory_writes.append(
                {
                    "proposal_id": proposal_id,
                    "relative_target_path": _memory_target_path(proposal_id, proposal),
                    "rendered_content_preview": _memory_rendered_content(proposal),
                    "dry_run_status": NOT_WRITTEN,
                }
            )
        else:
            non_planned = dict(record)
            non_planned["non_planned_reason"] = record["decision"]
            non_planned_decisions.append(non_planned)

    for item in _decision_items(source_decisions, "isa_decisions"):
        record = _decision_record(item, "isa")
        proposal_id = record["proposal_id"]
        if _candidate_decision(item):
            proposal = isa_proposals.get(proposal_id)
            if proposal is None:
                raise StateCommitDryRunError(f"approved ISA decision has no source proposal: {proposal_id}")
            candidate_decisions.append(record)
            planned_isa_writes.append(
                {
                    "proposal_id": proposal_id,
                    "relative_target_path": _isa_target_path(proposal_id, proposal),
                    "rendered_content_preview": _isa_rendered_content(proposal),
                    "dry_run_status": NOT_WRITTEN,
                }
            )
        else:
            non_planned = dict(record)
            non_planned["non_planned_reason"] = record["decision"]
            non_planned_decisions.append(non_planned)

    if not candidate_decisions:
        raise StateCommitDryRunError("no approved_for_future_commit_candidate decisions are present")

    plan = {
        "milestone_name": S16C_MILESTONE,
        "run_id": S16C_RUN_ID,
        "source_proposal_run_id": S16A_RUN_ID,
        "source_decisions_run_id": S16B_RUN_ID,
        "plan_authority": "pai-policy",
        "plan_mode": "dry-run-only",
        "human_gate": human_gate,
        "candidate_decisions_used": candidate_decisions,
        "planned_memory_writes": planned_memory_writes,
        "planned_isa_writes": planned_isa_writes,
        "non_planned_decisions": non_planned_decisions,
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_files_modified": False,
        "isa_files_modified": False,
        "pulse_files_modified": False,
        "known_limits": [
            "S16C renders proposed Memory/ISA content only inside the dry-run plan artifact.",
            "No planned write is materialized under live Memory or ISA.",
            "A later actual commit policy milestone requires separate architect approval.",
        ],
    }
    errors = validate_state_commit_dry_run_plan(plan)
    if errors:
        raise StateCommitDryRunError("; ".join(errors))
    return plan


def validate_state_commit_dry_run_plan(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "milestone_name": S16C_MILESTONE,
        "run_id": S16C_RUN_ID,
        "source_proposal_run_id": S16A_RUN_ID,
        "source_decisions_run_id": S16B_RUN_ID,
        "plan_authority": "pai-policy",
        "plan_mode": "dry-run-only",
        "human_gate": S16C_HUMAN_GATE,
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_files_modified": False,
        "isa_files_modified": False,
        "pulse_files_modified": False,
    }
    for key, value in expected.items():
        if plan.get(key) != value:
            errors.append(f"state commit dry-run plan mismatch for {key}")
    candidate_decisions = plan.get("candidate_decisions_used")
    if not isinstance(candidate_decisions, list) or not candidate_decisions:
        errors.append("state commit dry-run plan requires candidate_decisions_used")
    else:
        for index, item in enumerate(candidate_decisions):
            if not isinstance(item, dict):
                errors.append(f"candidate_decisions_used[{index}] must be an object")
                continue
            for key in ("proposal_id", "decision_family", "decision", "rationale", "commit_status"):
                if key not in item:
                    errors.append(f"candidate_decisions_used[{index}] missing {key}")
            if item.get("decision") != APPROVED_DECISION:
                errors.append(f"candidate_decisions_used[{index}].decision must be {APPROVED_DECISION}")
            if item.get("commit_status") != NOT_COMMITTED:
                errors.append(f"candidate_decisions_used[{index}].commit_status must be {NOT_COMMITTED}")

    for collection_name in ("planned_memory_writes", "planned_isa_writes"):
        items = plan.get(collection_name)
        if not isinstance(items, list):
            errors.append(f"{collection_name} must be a list")
            continue
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"{collection_name}[{index}] must be an object")
                continue
            for key in ("proposal_id", "relative_target_path", "rendered_content_preview", "dry_run_status"):
                if key not in item:
                    errors.append(f"{collection_name}[{index}] missing {key}")
            if item.get("dry_run_status") != NOT_WRITTEN:
                errors.append(f"{collection_name}[{index}].dry_run_status must be {NOT_WRITTEN}")
            for error in _target_path_errors(item.get("relative_target_path")):
                errors.append(f"{collection_name}[{index}].{error}")
    if not isinstance(plan.get("non_planned_decisions"), list):
        errors.append("non_planned_decisions must be a list")
    if not isinstance(plan.get("known_limits"), list):
        errors.append("state commit dry-run plan known_limits must be a list")
    return errors


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
        if relative in STATE_COMMIT_DRY_RUN_INSTALL_RELATIVES:
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
        if relative_path in STATE_COMMIT_DRY_RUN_INSTALL_RELATIVES:
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


def audit_state_commit_dry_run(
    *,
    pai_dir: Path,
    marker: Path,
    run_dir: Path,
    source_proposal_path: Path,
    source_decisions_path: Path,
    capsule_path: Path,
    review_path: Path,
    plan_path: Path,
    events_path: Path,
    runtime_attempt_number: int = 1,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    pai_dir = pai_dir.resolve(strict=True)
    marker = marker.resolve(strict=True)
    run_dir = run_dir.resolve(strict=True)
    repo_root = (repo_root or Path.cwd()).resolve(strict=False)

    source_proposal_present = source_proposal_path.is_file()
    source_decisions_present = source_decisions_path.is_file()
    dry_run_context_capsule_present = capsule_path.is_file()
    dry_run_review_present = review_path.is_file()
    dry_run_plan_present = plan_path.is_file()
    event_logs_present = events_path.is_file() and events_path.stat().st_size > 0

    source_proposal = _load_json(source_proposal_path, STATE_PROPOSAL_NAME) if source_proposal_present else {}
    source_decisions = _load_json(source_decisions_path, STATE_PROPOSAL_DECISIONS_NAME) if source_decisions_present else {}
    capsule = _load_json(capsule_path, COMMIT_DRY_RUN_CONTEXT_CAPSULE_NAME) if dry_run_context_capsule_present else {}
    review = _load_json(review_path, STATE_COMMIT_DRY_RUN_REVIEW_NAME) if dry_run_review_present else {}
    plan = _load_json(plan_path, STATE_COMMIT_DRY_RUN_PLAN_NAME) if dry_run_plan_present else {}
    state = _try_load_json(run_dir / STATE_COMMIT_DRY_RUN_STATE_NAME)

    source_errors = validate_state_proposal(source_proposal) if source_proposal_present else [f"{STATE_PROPOSAL_NAME} is missing"]
    source_schema_errors = (
        _schema_errors(source_proposal, pai_dir / "runtime-schemas" / "state-proposal.schema.json", STATE_PROPOSAL_NAME)
        if source_proposal_present
        else [f"{STATE_PROPOSAL_NAME} is missing"]
    )
    decisions_errors = (
        validate_state_proposal_decisions(source_decisions)
        if source_decisions_present
        else [f"{STATE_PROPOSAL_DECISIONS_NAME} is missing"]
    )
    decisions_schema_errors = (
        _schema_errors(
            source_decisions,
            pai_dir / "runtime-schemas" / "state-proposal-decisions.schema.json",
            STATE_PROPOSAL_DECISIONS_NAME,
        )
        if source_decisions_present
        else [f"{STATE_PROPOSAL_DECISIONS_NAME} is missing"]
    )
    capsule_errors = (
        validate_commit_dry_run_context_capsule(capsule)
        if dry_run_context_capsule_present
        else [f"{COMMIT_DRY_RUN_CONTEXT_CAPSULE_NAME} is missing"]
    )
    review_errors = (
        validate_state_commit_dry_run_review(review)
        if dry_run_review_present
        else [f"{STATE_COMMIT_DRY_RUN_REVIEW_NAME} is missing"]
    )
    review_schema_errors = (
        _schema_errors(
            review,
            pai_dir / "runtime-schemas" / "state-commit-dry-run-review.schema.json",
            STATE_COMMIT_DRY_RUN_REVIEW_NAME,
        )
        if dry_run_review_present
        else [f"{STATE_COMMIT_DRY_RUN_REVIEW_NAME} is missing"]
    )
    plan_errors = (
        validate_state_commit_dry_run_plan(plan)
        if dry_run_plan_present
        else [f"{STATE_COMMIT_DRY_RUN_PLAN_NAME} is missing"]
    )
    plan_schema_errors = (
        _schema_errors(
            plan,
            pai_dir / "runtime-schemas" / "state-commit-dry-run-plan.schema.json",
            STATE_COMMIT_DRY_RUN_PLAN_NAME,
        )
        if dry_run_plan_present
        else [f"{STATE_COMMIT_DRY_RUN_PLAN_NAME} is missing"]
    )

    source_proposal_schema_valid = source_proposal_present and not source_errors and not source_schema_errors
    source_decisions_schema_valid = source_decisions_present and not decisions_errors and not decisions_schema_errors
    dry_run_context_capsule_metadata_only = (
        capsule.get("metadata_only") is True and review.get("context_capsule_metadata_only") is True
    )
    dry_run_review_schema_valid = dry_run_review_present and not review_errors and not review_schema_errors
    dry_run_plan_schema_valid = dry_run_plan_present and not plan_errors and not plan_schema_errors
    human_gate_present = state.get("human_gate") is not None or plan.get("human_gate") is not None
    human_gate_valid = state.get("human_gate") == S16C_HUMAN_GATE and plan.get("human_gate") == S16C_HUMAN_GATE
    candidate_decisions_present = bool(plan.get("candidate_decisions_used"))
    planned_writes_not_written = dry_run_plan_present and all_planned_writes_not_written(plan)
    target_paths_relative = dry_run_plan_present and all_target_paths_relative(plan)
    target_paths_allowed = dry_run_plan_present and all_target_paths_allowed(plan)
    commit_authority_granted = (
        review.get("commit_authority_granted") is True
        or plan.get("commit_authority_granted") is True
        or state.get("commit_authority_granted") is True
    )
    commit_performed = (
        review.get("commit_performed") is True
        or plan.get("commit_performed") is True
        or state.get("commit_performed") is True
    )

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
    memory_files_modified = bool(memory_modified) or plan.get("memory_files_modified") is True
    isa_files_modified = bool(isa_modified) or plan.get("isa_files_modified") is True
    pulse_files_modified = bool(pulse_modified) or plan.get("pulse_files_modified") is True

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
        + decisions_errors
        + decisions_schema_errors
        + capsule_errors
        + review_errors
        + review_schema_errors
        + plan_errors
        + plan_schema_errors
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
        and source_decisions_present
        and source_decisions_schema_valid
        and human_gate_present
        and human_gate_valid
        and dry_run_context_capsule_present
        and dry_run_context_capsule_metadata_only
        and dry_run_review_present
        and dry_run_review_schema_valid
        and dry_run_plan_present
        and dry_run_plan_schema_valid
        and candidate_decisions_present
        and planned_writes_not_written
        and target_paths_relative
        and target_paths_allowed
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
        "milestone_name": S16C_MILESTONE,
        "run_id": S16C_RUN_ID,
        "runtime": "codex",
        "runtime_attempt_number": runtime_attempt_number,
        "pai_runtime_command": _redact_value(pai_dir, state.get("pai_runtime_command", [])),
        "provider_command": _redact_value(pai_dir, state.get("provider_command", [])),
        "source_proposal_present": source_proposal_present,
        "source_proposal_schema_valid": source_proposal_schema_valid,
        "source_decisions_present": source_decisions_present,
        "source_decisions_schema_valid": source_decisions_schema_valid,
        "human_gate_present": human_gate_present,
        "human_gate_valid": human_gate_valid,
        "dry_run_context_capsule_present": dry_run_context_capsule_present,
        "dry_run_context_capsule_metadata_only": dry_run_context_capsule_metadata_only,
        "dry_run_review_present": dry_run_review_present,
        "dry_run_review_schema_valid": dry_run_review_schema_valid,
        "dry_run_plan_present": dry_run_plan_present,
        "dry_run_plan_schema_valid": dry_run_plan_schema_valid,
        "candidate_decisions_present": candidate_decisions_present,
        "all_planned_writes_not_written": planned_writes_not_written,
        "all_target_paths_relative": target_paths_relative,
        "all_target_paths_allowed": target_paths_allowed,
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
            "S16C stores the dry-run plan only as a PAI-owned run artifact.",
            "S16C does not grant commit authority and does not write Memory or ISA.",
            "Filesystem mtime scanning is a secondary detector for forbidden state writes.",
        ],
    }
