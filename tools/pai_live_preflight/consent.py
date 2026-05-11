"""Consent parsing for fixture-only S14C preflight tests."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXACT_CONSENT_PHRASE = "I approve a read-only preflight of my installed PAI state at ~/.claude/PAI for V5-S14A-LIVE-PREFLIGHT."
APPROVED_DECLARED_SOURCE_ROOT = "~/.claude/PAI"


class ConsentValidationError(ValueError):
    """Raised when the fixture-only consent artifact is invalid."""


@dataclass(frozen=True)
class ValidatedConsent:
    milestone_name: str
    declared_source_root: str
    consent_phrase: str
    consent_status: str = "valid"


def _load_json_artifact(consent_path: Path) -> dict[str, Any]:
    if not consent_path.exists():
        raise ConsentValidationError("missing consent artifact")
    if not consent_path.is_file():
        raise ConsentValidationError("consent artifact is not a file")
    try:
        payload = json.loads(consent_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConsentValidationError(f"invalid consent JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ConsentValidationError("consent artifact must be a JSON object")
    return payload


def _reject_ambiguous_declared_root(source_root: str, field_name: str) -> None:
    if not source_root:
        raise ConsentValidationError(f"{field_name} is empty")
    if "\x00" in source_root:
        raise ConsentValidationError(f"{field_name} contains a NUL byte")
    if "$HOME" in source_root or "${HOME}" in source_root:
        raise ConsentValidationError(f"{field_name} requires environment expansion")
    if any(part == ".." for part in source_root.replace("\\", "/").split("/")):
        raise ConsentValidationError(f"{field_name} contains path traversal")


def validate_declared_source_root(source_root: str, field_name: str = "declared source root") -> None:
    _reject_ambiguous_declared_root(source_root, field_name)
    if source_root != APPROVED_DECLARED_SOURCE_ROOT:
        raise ConsentValidationError(f"{field_name} is not exactly approved")


def validate_consent_artifact(consent_path: str | Path, declared_source_root: str) -> ValidatedConsent:
    validate_declared_source_root(declared_source_root, "CLI declared source root")
    payload = _load_json_artifact(Path(consent_path))

    consent_phrase = payload.get("consent_phrase")
    if consent_phrase != EXACT_CONSENT_PHRASE:
        raise ConsentValidationError("the consent phrase differs by even one character")

    artifact_root = payload.get("declared_source_root")
    if not isinstance(artifact_root, str):
        raise ConsentValidationError("explicit source root is missing")
    validate_declared_source_root(artifact_root, "artifact declared source root")
    if artifact_root != declared_source_root:
        raise ConsentValidationError("artifact source root does not match CLI declared source root")

    milestone_name = payload.get("milestone_name")
    if not isinstance(milestone_name, str) or not milestone_name:
        raise ConsentValidationError("milestone name is missing")

    if payload.get("trial_mode") != "read-only-preflight-only":
        raise ConsentValidationError("statement that the trial is read-only and preflight-only is missing")

    exclusions = payload.get("excluded_surfaces")
    required_exclusions = {"Memory", "ISA", "Pulse", "Claude memory", "Codex memory"}
    if not isinstance(exclusions, list) or not required_exclusions.issubset(set(exclusions)):
        raise ConsentValidationError(
            "statement that Memory, ISA, Pulse, Claude memory, and Codex memory are excluded is missing"
        )

    return ValidatedConsent(
        milestone_name=milestone_name,
        declared_source_root=artifact_root,
        consent_phrase=consent_phrase,
    )
