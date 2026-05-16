from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from tools.pai_runtime_runner.pai_context import collect_pai_context_metadata, validate_context_capsule
from tools.pai_runtime_runner.state_commit_dry_run import (
    ALLOWED_TARGET_PREFIXES,
    NOT_WRITTEN,
    S16C_RUN_ID,
    STATE_COMMIT_DRY_RUN_PLAN_NAME,
    STATE_COMMIT_DRY_RUN_PLAN_SCHEMA_NAME,
    STATE_COMMIT_DRY_RUN_INSTALL_RELATIVES,
    _target_path_errors,
    all_target_paths_allowed,
    all_target_paths_relative,
    load_source_state_proposal,
    validate_state_commit_dry_run_plan,
)
from tools.pai_runtime_runner.state_proposal import (
    MARKER_VALUE,
    PAI_DIR_LABEL,
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
)


S16D_MILESTONE = "V5-S16D-PAI-STATE-SINGLE-PROPOSAL-SHADOW-COMMIT"
S16D_RUN_ID = "s16d-single-proposal-shadow-commit"
S16D_TASK_ID = "s16d-state-shadow-commit-task"
S16D_TASK_KIND = "single-proposal-shadow-commit-policy"
S16D_RUN_RELATIVE = Path("runs") / "s16d" / "single-proposal-shadow-commit"
S16D_TASK_RELATIVE = Path("runtime-tasks") / "s16d-state-shadow-commit-task.json"
S16D_SOURCE_DRY_RUN_PLAN_RELATIVE = Path("runs") / "s16c" / "commit-dry-run" / STATE_COMMIT_DRY_RUN_PLAN_NAME
S16D_HUMAN_GATE = "S16D_SHADOW_APPLY_ONLY_NO_LIVE_MEMORY_ISA_WRITE"

SHADOW_COMMIT_CONTEXT_CAPSULE_NAME = "shadow-commit-context-capsule.json"
SINGLE_PROPOSAL_POLICY_REVIEW_NAME = "single-proposal-policy-review.json"
SELECTED_COMMIT_CANDIDATE_NAME = "selected-commit-candidate.json"
SHADOW_APPLY_RESULT_NAME = "shadow-apply-result.json"
SHADOW_COMMIT_EVENTS_NAME = "shadow-commit-events.jsonl"
SHADOW_COMMIT_VALIDATION_NAME = "shadow-commit-validation.json"
SINGLE_PROPOSAL_POLICY_REVIEW_SCHEMA_NAME = "single-proposal-policy-review.schema.json"
SELECTED_COMMIT_CANDIDATE_SCHEMA_NAME = "selected-commit-candidate.schema.json"
SHADOW_APPLY_RESULT_SCHEMA_NAME = "shadow-apply-result.schema.json"
SHADOW_COMMIT_STATE_NAME = "shadow-commit-state.json"
SHADOW_STATE_DIR_NAME = "shadow-state"

SELECTION_POLICY = "first-memory-lexical-else-first-isa-lexical"
SELECTION_STATUS = "selected_for_shadow_apply_only"
SHADOW_APPLY_STATUS = "shadow_written"
LIVE_COMMIT_STATUS = "not_committed"

STATE_SHADOW_COMMIT_INSTALL_RELATIVES = {
    Path("bin") / "pai-runtime",
    Path("runtime-state.json"),
    Path("runtime-schemas") / "state-shadow-commit-task.schema.json",
    Path("runtime-schemas") / "single-proposal-policy-review.schema.json",
    Path("runtime-schemas") / "selected-commit-candidate.schema.json",
    Path("runtime-schemas") / "shadow-apply-result.schema.json",
    Path("runtime-schemas") / "shadow-commit-validation.schema.json",
    Path("runtime-tasks") / "s16d-state-shadow-commit-task.json",
    Path("runtimes") / "codex" / "provider-manifest.json",
}


class StateShadowCommitError(ValueError):
    pass


def _load_json(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise StateShadowCommitError(f"{label} is missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise StateShadowCommitError(f"{label} is not valid JSON") from exc
    if not isinstance(data, dict):
        raise StateShadowCommitError(f"{label} must be a JSON object")
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
    if value != S16D_HUMAN_GATE:
        raise StateShadowCommitError(f"--human-gate must be exactly {S16D_HUMAN_GATE}")


def load_source_dry_run_plan(path: Path) -> dict[str, Any]:
    plan = _load_json(path, STATE_COMMIT_DRY_RUN_PLAN_NAME)
    errors = validate_state_commit_dry_run_plan(plan)
    if errors:
        raise StateShadowCommitError("; ".join(errors))
    return plan


def _planned_items(plan: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = plan.get(key)
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _target_family(relative_target_path: str) -> str:
    if relative_target_path.startswith("Memory/WORK/"):
        return "Memory/WORK"
    if relative_target_path.startswith("Memory/LEARNING/"):
        return "Memory/LEARNING"
    if relative_target_path.startswith("Memory/KNOWLEDGE/"):
        return "Memory/KNOWLEDGE"
    if relative_target_path.startswith("ISA/"):
        return "ISA"
    return "unknown"


def _candidate_errors(candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if candidate.get("dry_run_status") != NOT_WRITTEN:
        errors.append("selected candidate dry_run_status must be not_written")
    errors.extend(_target_path_errors(candidate.get("relative_target_path")))
    content = candidate.get("rendered_content_preview")
    if not isinstance(content, str) or content == "":
        errors.append("selected candidate rendered_content_preview must be present text")
    if not isinstance(candidate.get("proposal_id"), str) or candidate.get("proposal_id") == "":
        errors.append("selected candidate proposal_id must be present")
    return errors


def _sorted_candidates(plan: dict[str, Any], collection_name: str) -> list[dict[str, Any]]:
    candidates = []
    for item in _planned_items(plan, collection_name):
        target = item.get("relative_target_path")
        if isinstance(target, str):
            candidates.append(item)
    return sorted(candidates, key=lambda item: str(item.get("relative_target_path", "")))


def select_single_commit_candidate(plan: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    errors = validate_state_commit_dry_run_plan(plan)
    if errors:
        raise StateShadowCommitError("; ".join(errors))

    kind = "memory"
    candidates = _sorted_candidates(plan, "planned_memory_writes")
    if not candidates:
        kind = "isa"
        candidates = _sorted_candidates(plan, "planned_isa_writes")
    if not candidates:
        raise StateShadowCommitError("no planned Memory or ISA writes exist")

    candidate = candidates[0]
    candidate_errors = _candidate_errors(candidate)
    if candidate_errors:
        raise StateShadowCommitError("; ".join(candidate_errors))

    target = str(candidate["relative_target_path"])
    selected = {
        "milestone_name": S16D_MILESTONE,
        "run_id": S16D_RUN_ID,
        "source_dry_run_plan_run_id": S16C_RUN_ID,
        "selection_authority": "pai-policy",
        "selection_policy": SELECTION_POLICY,
        "selected_candidate_count": 1,
        "human_gate": S16D_HUMAN_GATE,
        "selected_candidate_kind": kind,
        "selected_proposal_id": str(candidate["proposal_id"]),
        "relative_target_path": target,
        "target_path_family": _target_family(target),
        "dry_run_status_from_source": NOT_WRITTEN,
        "rendered_content_present": True,
        "selection_status": SELECTION_STATUS,
        "commit_authority_granted": False,
        "commit_performed": False,
        "known_limits": [
            "S16D selects exactly one dry-run candidate for shadow apply only.",
            "S16D does not grant live Memory or ISA write authority.",
        ],
    }
    selected_errors = validate_selected_commit_candidate(selected)
    if selected_errors:
        raise StateShadowCommitError("; ".join(selected_errors))
    return selected, candidate


def collect_shadow_commit_context_metadata(
    pai_dir: Path,
    source_dry_run_plan: dict[str, Any],
    selected_candidate: dict[str, Any],
) -> dict[str, Any]:
    capsule = collect_pai_context_metadata(pai_dir)
    capsule.update(
        {
            "milestone_name": S16D_MILESTONE,
            "run_id": S16D_RUN_ID,
            "task_id": S16D_TASK_ID,
            "task_kind": S16D_TASK_KIND,
            "source_dry_run_plan_run_id": S16C_RUN_ID,
            "human_gate_required": S16D_HUMAN_GATE,
            "source_dry_run_plan_metadata": {
                "candidate_decision_count": len(source_dry_run_plan.get("candidate_decisions_used", []))
                if isinstance(source_dry_run_plan.get("candidate_decisions_used"), list)
                else 0,
                "planned_memory_write_count": len(_planned_items(source_dry_run_plan, "planned_memory_writes")),
                "planned_isa_write_count": len(_planned_items(source_dry_run_plan, "planned_isa_writes")),
                "all_planned_writes_not_written": all(
                    item.get("dry_run_status") == NOT_WRITTEN
                    for item in _planned_items(source_dry_run_plan, "planned_memory_writes")
                    + _planned_items(source_dry_run_plan, "planned_isa_writes")
                ),
                "commit_authority_granted": source_dry_run_plan.get("commit_authority_granted") is True,
                "commit_performed": source_dry_run_plan.get("commit_performed") is True,
            },
            "selected_candidate_metadata": {
                "selected_candidate_count": selected_candidate.get("selected_candidate_count"),
                "selected_candidate_kind": selected_candidate.get("selected_candidate_kind"),
                "relative_target_path": selected_candidate.get("relative_target_path"),
                "target_path_family": selected_candidate.get("target_path_family"),
                "selection_policy": selected_candidate.get("selection_policy"),
            },
            "shadow_commit_policy": [
                "S16D admits memory.commit.shadow_apply and isa.commit.shadow_apply only.",
                "PAI selects exactly one candidate from the S16C dry-run plan.",
                "PAI materializes selected content only under the S16D run directory shadow-state tree.",
                "S16D does not write live Memory or ISA and does not probe Pulse.",
            ],
        }
    )
    errors = validate_shadow_commit_context_capsule(capsule)
    if errors:
        raise StateShadowCommitError("; ".join(errors))
    return capsule


def validate_shadow_commit_context_capsule(capsule: dict[str, Any]) -> list[str]:
    errors = validate_context_capsule(capsule)
    expected = {
        "milestone_name": S16D_MILESTONE,
        "run_id": S16D_RUN_ID,
        "task_id": S16D_TASK_ID,
        "task_kind": S16D_TASK_KIND,
        "source_dry_run_plan_run_id": S16C_RUN_ID,
        "human_gate_required": S16D_HUMAN_GATE,
        "metadata_only": True,
        "redacted_paths": True,
    }
    for key, expected_value in expected.items():
        if capsule.get(key) != expected_value:
            errors.append(f"shadow commit context capsule mismatch for {key}")
    if not isinstance(capsule.get("shadow_commit_policy"), list) or not capsule.get("shadow_commit_policy"):
        errors.append("shadow commit context capsule must include shadow_commit_policy")
    if not isinstance(capsule.get("source_dry_run_plan_metadata"), dict):
        errors.append("shadow commit context capsule must include source_dry_run_plan_metadata")
    if not isinstance(capsule.get("selected_candidate_metadata"), dict):
        errors.append("shadow commit context capsule must include selected_candidate_metadata")
    return errors


def normalize_single_proposal_policy_review(
    provider_result: dict[str, Any],
    capsule: dict[str, Any],
    human_gate: str,
) -> dict[str, Any]:
    validate_human_gate(human_gate)
    evidence = provider_result.get("evidence_classification")
    limits = provider_result.get("known_limits")
    review = {
        "milestone_name": S16D_MILESTONE,
        "run_id": S16D_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "task_id": S16D_TASK_ID,
        "task_kind": S16D_TASK_KIND,
        "adapter_identity_marker": MARKER_VALUE,
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "source_dry_run_plan_run_id": S16C_RUN_ID,
        "source_dry_run_plan_used": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": capsule.get("metadata_only") is True,
        "human_gate_observed": True,
        "shadow_apply_only": True,
        "single_candidate_policy_observed": True,
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
            "PAI-owned single-proposal shadow commit evidence",
            "shadow-apply-only Memory/ISA commit policy",
            "not Memory/ISA commit authority",
        ],
        "known_limits": limits
        if isinstance(limits, list)
        else [
            "S16D materializes content only under the PAI-owned run directory shadow-state tree.",
            "Commit authority remains false and requires a later architect-approved milestone.",
            "Pulse probing and Pulse event emission remain blocked.",
        ],
    }
    errors = validate_single_proposal_policy_review(review)
    if errors:
        raise StateShadowCommitError("; ".join(errors))
    return review


def validate_single_proposal_policy_review(review: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "milestone_name": S16D_MILESTONE,
        "run_id": S16D_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "task_id": S16D_TASK_ID,
        "task_kind": S16D_TASK_KIND,
        "adapter_identity_marker": MARKER_VALUE,
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "source_dry_run_plan_run_id": S16C_RUN_ID,
        "source_dry_run_plan_used": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": True,
        "human_gate_observed": True,
        "shadow_apply_only": True,
        "single_candidate_policy_observed": True,
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
            errors.append(f"single-proposal policy review mismatch for {key}")
    if not isinstance(review.get("evidence_classification"), list):
        errors.append("single-proposal policy review evidence_classification must be a list")
    if not isinstance(review.get("known_limits"), list):
        errors.append("single-proposal policy review known_limits must be a list")
    return errors


def validate_selected_commit_candidate(selected: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "milestone_name": S16D_MILESTONE,
        "run_id": S16D_RUN_ID,
        "source_dry_run_plan_run_id": S16C_RUN_ID,
        "selection_authority": "pai-policy",
        "selection_policy": SELECTION_POLICY,
        "selected_candidate_count": 1,
        "human_gate": S16D_HUMAN_GATE,
        "dry_run_status_from_source": NOT_WRITTEN,
        "rendered_content_present": True,
        "selection_status": SELECTION_STATUS,
        "commit_authority_granted": False,
        "commit_performed": False,
    }
    for key, value in expected.items():
        if selected.get(key) != value:
            errors.append(f"selected commit candidate mismatch for {key}")
    for key in ("selected_candidate_kind", "selected_proposal_id", "relative_target_path", "target_path_family"):
        if not isinstance(selected.get(key), str) or selected.get(key) == "":
            errors.append(f"selected commit candidate missing {key}")
    for error in _target_path_errors(selected.get("relative_target_path")):
        errors.append(f"selected commit candidate {error}")
    if selected.get("target_path_family") != _target_family(str(selected.get("relative_target_path", ""))):
        errors.append("selected commit candidate target_path_family mismatch")
    if not isinstance(selected.get("known_limits"), list):
        errors.append("selected commit candidate known_limits must be a list")
    return errors


def _shadow_relative_target(relative_target_path: str) -> Path:
    parts = relative_target_path.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise StateShadowCommitError(f"unsafe relative target path for shadow apply: {relative_target_path}")
    return Path(SHADOW_STATE_DIR_NAME, *parts)


def shadow_apply_candidate(
    run_dir: Path,
    selected_candidate: dict[str, Any],
    source_candidate: dict[str, Any],
) -> dict[str, Any]:
    selected_errors = validate_selected_commit_candidate(selected_candidate)
    if selected_errors:
        raise StateShadowCommitError("; ".join(selected_errors))
    candidate_errors = _candidate_errors(source_candidate)
    if candidate_errors:
        raise StateShadowCommitError("; ".join(candidate_errors))
    if source_candidate.get("proposal_id") != selected_candidate.get("selected_proposal_id"):
        raise StateShadowCommitError("source candidate does not match selected proposal id")
    if source_candidate.get("relative_target_path") != selected_candidate.get("relative_target_path"):
        raise StateShadowCommitError("source candidate does not match selected relative target path")

    run_root = run_dir.resolve(strict=False)
    shadow_relative = _shadow_relative_target(str(selected_candidate["relative_target_path"]))
    shadow_target = (run_root / shadow_relative).resolve(strict=False)
    shadow_root = (run_root / SHADOW_STATE_DIR_NAME).resolve(strict=False)
    if not _is_within(shadow_root, shadow_target) or not _is_within(run_root, shadow_target):
        raise StateShadowCommitError("shadow target would escape the S16D run directory")
    content = str(source_candidate["rendered_content_preview"])
    encoded = content.encode("utf-8")
    shadow_target.parent.mkdir(parents=True, exist_ok=True)
    if shadow_target.exists() and shadow_target.is_symlink():
        raise StateShadowCommitError(f"shadow target is a symlink: {shadow_target}")
    if shadow_target.exists() and not shadow_target.is_file():
        raise StateShadowCommitError(f"shadow target is not a file: {shadow_target}")
    shadow_target.write_text(content, encoding="utf-8")

    result = {
        "milestone_name": S16D_MILESTONE,
        "run_id": S16D_RUN_ID,
        "source_dry_run_plan_run_id": S16C_RUN_ID,
        "selected_proposal_id": selected_candidate["selected_proposal_id"],
        "relative_target_path": selected_candidate["relative_target_path"],
        "shadow_target_path": str(shadow_target),
        "shadow_target_path_relative_to_run": shadow_relative.as_posix(),
        "content_sha256": hashlib.sha256(encoded).hexdigest(),
        "content_byte_count": len(encoded),
        "shadow_apply_status": SHADOW_APPLY_STATUS,
        "live_commit_status": LIVE_COMMIT_STATUS,
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_files_modified": False,
        "isa_files_modified": False,
        "pulse_files_modified": False,
        "known_limits": [
            "S16D writes only the selected content under shadow-state in the run directory.",
            "The corresponding live Memory/ISA target remains untouched.",
        ],
    }
    result_errors = validate_shadow_apply_result(result, run_dir)
    if result_errors:
        raise StateShadowCommitError("; ".join(result_errors))
    return result


def validate_shadow_apply_result(result: dict[str, Any], run_dir: Path | None = None) -> list[str]:
    errors: list[str] = []
    expected = {
        "milestone_name": S16D_MILESTONE,
        "run_id": S16D_RUN_ID,
        "source_dry_run_plan_run_id": S16C_RUN_ID,
        "shadow_apply_status": SHADOW_APPLY_STATUS,
        "live_commit_status": LIVE_COMMIT_STATUS,
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_files_modified": False,
        "isa_files_modified": False,
        "pulse_files_modified": False,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            errors.append(f"shadow apply result mismatch for {key}")
    for key in ("selected_proposal_id", "relative_target_path", "shadow_target_path", "shadow_target_path_relative_to_run"):
        if not isinstance(result.get(key), str) or result.get(key) == "":
            errors.append(f"shadow apply result missing {key}")
    for error in _target_path_errors(result.get("relative_target_path")):
        errors.append(f"shadow apply result {error}")
    if not isinstance(result.get("content_sha256"), str) or len(str(result.get("content_sha256", ""))) != 64:
        errors.append("shadow apply result content_sha256 must be a sha256 hex digest")
    if not isinstance(result.get("content_byte_count"), int) or int(result.get("content_byte_count", 0)) < 0:
        errors.append("shadow apply result content_byte_count must be a non-negative integer")
    relative_to_run = result.get("shadow_target_path_relative_to_run")
    if isinstance(relative_to_run, str):
        if Path(relative_to_run).is_absolute() or any(part in {"", ".", ".."} for part in relative_to_run.split("/")):
            errors.append("shadow_target_path_relative_to_run must be a safe relative path")
        if not relative_to_run.startswith(f"{SHADOW_STATE_DIR_NAME}/"):
            errors.append("shadow_target_path_relative_to_run must be under shadow-state")
    if run_dir is not None and isinstance(result.get("shadow_target_path"), str):
        target = Path(str(result["shadow_target_path"])).resolve(strict=False)
        if not _is_within(run_dir.resolve(strict=False), target):
            errors.append("shadow_target_path must be under the S16D run directory")
        if isinstance(relative_to_run, str):
            expected = (run_dir.resolve(strict=False) / relative_to_run).resolve(strict=False)
            if target != expected:
                errors.append("shadow_target_path must match shadow_target_path_relative_to_run")
    if not isinstance(result.get("known_limits"), list):
        errors.append("shadow apply result known_limits must be a list")
    return errors


def validate_shadow_commit(
    *,
    source_dry_run_plan: dict[str, Any],
    selected_candidate: dict[str, Any],
    shadow_apply_result: dict[str, Any],
    run_dir: Path | None = None,
) -> list[str]:
    errors = validate_state_commit_dry_run_plan(source_dry_run_plan)
    errors.extend(validate_selected_commit_candidate(selected_candidate))
    errors.extend(validate_shadow_apply_result(shadow_apply_result, run_dir))
    if selected_candidate.get("selected_candidate_count") != 1:
        errors.append("selected_candidate_count must be 1")
    if shadow_apply_result.get("selected_proposal_id") != selected_candidate.get("selected_proposal_id"):
        errors.append("shadow apply result selected_proposal_id mismatch")
    if shadow_apply_result.get("relative_target_path") != selected_candidate.get("relative_target_path"):
        errors.append("shadow apply result relative_target_path mismatch")
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
        if relative in STATE_SHADOW_COMMIT_INSTALL_RELATIVES or relative in STATE_COMMIT_DRY_RUN_INSTALL_RELATIVES:
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
        if relative_path in STATE_SHADOW_COMMIT_INSTALL_RELATIVES:
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


def audit_state_shadow_commit(
    *,
    pai_dir: Path,
    marker: Path,
    run_dir: Path,
    source_dry_run_plan_path: Path,
    capsule_path: Path,
    review_path: Path,
    selected_path: Path,
    shadow_apply_path: Path,
    events_path: Path,
    runtime_attempt_number: int = 1,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    pai_dir = pai_dir.resolve(strict=True)
    marker = marker.resolve(strict=True)
    run_dir = run_dir.resolve(strict=True)
    repo_root = (repo_root or Path.cwd()).resolve(strict=False)

    source_dry_run_plan_present = source_dry_run_plan_path.is_file()
    shadow_context_capsule_present = capsule_path.is_file()
    policy_review_present = review_path.is_file()
    selected_candidate_present = selected_path.is_file()
    shadow_apply_result_present = shadow_apply_path.is_file()
    event_logs_present = events_path.is_file() and events_path.stat().st_size > 0

    source_plan = _load_json(source_dry_run_plan_path, STATE_COMMIT_DRY_RUN_PLAN_NAME) if source_dry_run_plan_present else {}
    capsule = _load_json(capsule_path, SHADOW_COMMIT_CONTEXT_CAPSULE_NAME) if shadow_context_capsule_present else {}
    review = _load_json(review_path, SINGLE_PROPOSAL_POLICY_REVIEW_NAME) if policy_review_present else {}
    selected = _load_json(selected_path, SELECTED_COMMIT_CANDIDATE_NAME) if selected_candidate_present else {}
    shadow = _load_json(shadow_apply_path, SHADOW_APPLY_RESULT_NAME) if shadow_apply_result_present else {}
    state = _try_load_json(run_dir / SHADOW_COMMIT_STATE_NAME)

    source_errors = (
        validate_state_commit_dry_run_plan(source_plan)
        if source_dry_run_plan_present
        else [f"{STATE_COMMIT_DRY_RUN_PLAN_NAME} is missing"]
    )
    source_schema_errors = (
        _schema_errors(
            source_plan,
            pai_dir / "runtime-schemas" / STATE_COMMIT_DRY_RUN_PLAN_SCHEMA_NAME,
            STATE_COMMIT_DRY_RUN_PLAN_NAME,
        )
        if source_dry_run_plan_present
        else [f"{STATE_COMMIT_DRY_RUN_PLAN_NAME} is missing"]
    )
    capsule_errors = (
        validate_shadow_commit_context_capsule(capsule)
        if shadow_context_capsule_present
        else [f"{SHADOW_COMMIT_CONTEXT_CAPSULE_NAME} is missing"]
    )
    review_errors = (
        validate_single_proposal_policy_review(review)
        if policy_review_present
        else [f"{SINGLE_PROPOSAL_POLICY_REVIEW_NAME} is missing"]
    )
    review_schema_errors = (
        _schema_errors(
            review,
            pai_dir / "runtime-schemas" / "single-proposal-policy-review.schema.json",
            SINGLE_PROPOSAL_POLICY_REVIEW_NAME,
        )
        if policy_review_present
        else [f"{SINGLE_PROPOSAL_POLICY_REVIEW_NAME} is missing"]
    )
    selected_errors = (
        validate_selected_commit_candidate(selected)
        if selected_candidate_present
        else [f"{SELECTED_COMMIT_CANDIDATE_NAME} is missing"]
    )
    selected_schema_errors = (
        _schema_errors(
            selected,
            pai_dir / "runtime-schemas" / "selected-commit-candidate.schema.json",
            SELECTED_COMMIT_CANDIDATE_NAME,
        )
        if selected_candidate_present
        else [f"{SELECTED_COMMIT_CANDIDATE_NAME} is missing"]
    )
    shadow_errors = (
        validate_shadow_apply_result(shadow, run_dir)
        if shadow_apply_result_present
        else [f"{SHADOW_APPLY_RESULT_NAME} is missing"]
    )
    shadow_schema_errors = (
        _schema_errors(
            shadow,
            pai_dir / "runtime-schemas" / "shadow-apply-result.schema.json",
            SHADOW_APPLY_RESULT_NAME,
        )
        if shadow_apply_result_present
        else [f"{SHADOW_APPLY_RESULT_NAME} is missing"]
    )

    source_dry_run_plan_schema_valid = source_dry_run_plan_present and not source_errors and not source_schema_errors
    shadow_context_capsule_metadata_only = (
        capsule.get("metadata_only") is True and review.get("context_capsule_metadata_only") is True
    )
    policy_review_schema_valid = policy_review_present and not review_errors and not review_schema_errors
    selected_candidate_schema_valid = selected_candidate_present and not selected_errors and not selected_schema_errors
    selected_candidate_count = selected.get("selected_candidate_count") if isinstance(selected.get("selected_candidate_count"), int) else 0
    single_candidate_selected = selected_candidate_count == 1 and selected.get("selection_status") == SELECTION_STATUS
    selected_target_path_relative = (
        isinstance(selected.get("relative_target_path"), str)
        and not str(selected["relative_target_path"]).startswith("/")
        and ".." not in str(selected["relative_target_path"]).split("/")
    )
    selected_target_path_allowed = not _target_path_errors(selected.get("relative_target_path"))
    shadow_apply_result_schema_valid = shadow_apply_result_present and not shadow_errors and not shadow_schema_errors
    shadow_target_relative = shadow.get("shadow_target_path_relative_to_run")
    shadow_target = (
        (run_dir / shadow_target_relative).resolve(strict=False)
        if isinstance(shadow_target_relative, str)
        else Path("__missing__")
    )
    shadow_target_written = shadow_target.is_file()
    shadow_target_under_run_dir = _is_within(run_dir, shadow_target.resolve(strict=False))
    shadow_content_hash_recorded = isinstance(shadow.get("content_sha256"), str) and len(str(shadow.get("content_sha256"))) == 64

    human_gate_present = state.get("human_gate") is not None or selected.get("human_gate") is not None
    human_gate_valid = state.get("human_gate") == S16D_HUMAN_GATE and selected.get("human_gate") == S16D_HUMAN_GATE
    commit_authority_granted = (
        review.get("commit_authority_granted") is True
        or selected.get("commit_authority_granted") is True
        or shadow.get("commit_authority_granted") is True
        or state.get("commit_authority_granted") is True
    )
    commit_performed = (
        review.get("commit_performed") is True
        or selected.get("commit_performed") is True
        or shadow.get("commit_performed") is True
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
    memory_files_modified = bool(memory_modified) or shadow.get("memory_files_modified") is True
    isa_files_modified = bool(isa_modified) or shadow.get("isa_files_modified") is True
    pulse_files_modified = bool(pulse_modified) or shadow.get("pulse_files_modified") is True

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
        + selected_errors
        + selected_schema_errors
        + shadow_errors
        + shadow_schema_errors
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
        source_dry_run_plan_present
        and source_dry_run_plan_schema_valid
        and human_gate_present
        and human_gate_valid
        and shadow_context_capsule_present
        and shadow_context_capsule_metadata_only
        and policy_review_present
        and policy_review_schema_valid
        and selected_candidate_present
        and selected_candidate_schema_valid
        and selected_candidate_count == 1
        and single_candidate_selected
        and selected_target_path_relative
        and selected_target_path_allowed
        and shadow_apply_result_present
        and shadow_apply_result_schema_valid
        and shadow_target_written
        and shadow_target_under_run_dir
        and shadow_content_hash_recorded
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
        "milestone_name": S16D_MILESTONE,
        "run_id": S16D_RUN_ID,
        "runtime": "codex",
        "runtime_attempt_number": runtime_attempt_number,
        "pai_runtime_command": _redact_value(pai_dir, state.get("pai_runtime_command", [])),
        "provider_command": _redact_value(pai_dir, state.get("provider_command", [])),
        "source_dry_run_plan_present": source_dry_run_plan_present,
        "source_dry_run_plan_schema_valid": source_dry_run_plan_schema_valid,
        "human_gate_present": human_gate_present,
        "human_gate_valid": human_gate_valid,
        "shadow_context_capsule_present": shadow_context_capsule_present,
        "shadow_context_capsule_metadata_only": shadow_context_capsule_metadata_only,
        "policy_review_present": policy_review_present,
        "policy_review_schema_valid": policy_review_schema_valid,
        "selected_candidate_present": selected_candidate_present,
        "selected_candidate_schema_valid": selected_candidate_schema_valid,
        "selected_candidate_count": selected_candidate_count,
        "single_candidate_selected": single_candidate_selected,
        "selected_target_path_relative": selected_target_path_relative,
        "selected_target_path_allowed": selected_target_path_allowed,
        "shadow_apply_result_present": shadow_apply_result_present,
        "shadow_apply_result_schema_valid": shadow_apply_result_schema_valid,
        "shadow_target_written": shadow_target_written,
        "shadow_target_under_run_dir": shadow_target_under_run_dir,
        "shadow_content_hash_recorded": shadow_content_hash_recorded,
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
            "S16D stores the exact selected content only under shadow-state in the PAI-owned run directory.",
            "S16D does not grant commit authority and does not write live Memory or ISA.",
            "Filesystem mtime scanning is a secondary detector for forbidden state writes.",
        ],
    }
