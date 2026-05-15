from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
from typing import Any


class PatchProposalError(ValueError):
    pass


FORBIDDEN_EXACT_PATHS = {
    "AGENTS.md",
}

FORBIDDEN_PREFIXES = (
    ".codex/",
    ".claude/",
    "PAI/",
    "CLAUDE.md",
    "Memory/WORK/",
    "Memory/LEARNING/",
    "Memory/KNOWLEDGE/",
    "ISA/",
    "Pulse/events/",
)

SUPPORTED_PATCH_PROPOSAL_MODES = ("replace-file",)

PATCH_PROPOSAL_TEXT_ENCODING = "utf-8"


def load_patch_proposal(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise PatchProposalError(f"patch proposal is missing: {path}")
    try:
        proposal = json.loads(path.read_text(encoding=PATCH_PROPOSAL_TEXT_ENCODING))
    except json.JSONDecodeError as exc:
        raise PatchProposalError(f"patch proposal is not valid JSON: {path}") from exc
    if not isinstance(proposal, dict):
        raise PatchProposalError("patch proposal must be a JSON object")
    return proposal


def _change_path(change: dict[str, Any]) -> str | None:
    value = change.get("path")
    return value if isinstance(value, str) else None


def _normalized_repository_path(path_text: str) -> str:
    return PurePosixPath(path_text).as_posix()


def _validate_relative_path(path_text: str, approved_write_set: set[str]) -> list[str]:
    errors: list[str] = []
    if path_text == "":
        return ["path must be a non-empty string"]
    if "\x00" in path_text:
        return ["path must be text, not binary content"]
    if path_text.startswith("~/") or path_text.startswith("~/.codex"):
        errors.append("path must not target ~/.codex")
    path = PurePosixPath(path_text)
    if path.is_absolute():
        errors.append("path must not be absolute")
    if any(part == ".." for part in path.parts):
        errors.append("path traversal is not allowed")
    normalized = _normalized_repository_path(path_text)
    if normalized in FORBIDDEN_EXACT_PATHS:
        errors.append("repo root AGENTS.md is forbidden")
    if any(normalized == prefix.rstrip("/") or normalized.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
        errors.append(f"forbidden semantic or adapter path: {normalized}")
    if normalized not in approved_write_set:
        errors.append(f"path is outside approved_write_set: {normalized}")
    return errors


def _validate_change(change: Any, approved_write_set: set[str], index: int) -> list[str]:
    errors: list[str] = []
    if not isinstance(change, dict):
        return [f"changes[{index}] must be an object"]
    mode = change.get("mode")
    if mode not in SUPPORTED_PATCH_PROPOSAL_MODES:
        errors.append(f"changes[{index}].mode must be replace-file")
    path_text = _change_path(change)
    if path_text is None:
        errors.append(f"changes[{index}].path must be a string")
    else:
        errors.extend(f"changes[{index}].{error}" for error in _validate_relative_path(path_text, approved_write_set))
    content = change.get("content")
    if not isinstance(content, str):
        errors.append(f"changes[{index}].content must be a string")
    elif "\x00" in content:
        errors.append(f"changes[{index}].content must be text, not binary content")
    diff = change.get("unified_diff")
    if diff is not None and not isinstance(diff, str):
        errors.append(f"changes[{index}].unified_diff must be a string when present")
    elif isinstance(diff, str) and "\x00" in diff:
        errors.append(f"changes[{index}].unified_diff must be text, not binary content")
    return errors


def validate_patch_proposal(proposal: dict[str, Any], approved_write_set: set[str]) -> list[str]:
    errors: list[str] = []
    if not isinstance(proposal, dict):
        return ["patch proposal must be a JSON object"]
    if not approved_write_set:
        errors.append("approved_write_set must not be empty")

    proposal_id = proposal.get("proposal_id")
    if not isinstance(proposal_id, str) or proposal_id == "":
        errors.append("proposal_id must be a non-empty string")

    proposal_kind = proposal.get("proposal_kind")
    if proposal_kind != "full-file-replacement":
        errors.append("proposal_kind must be full-file-replacement")

    unified_diff = proposal.get("unified_diff")
    if unified_diff is not None and not isinstance(unified_diff, str):
        errors.append("unified_diff must be a string when present")
    elif isinstance(unified_diff, str) and "\x00" in unified_diff:
        errors.append("unified_diff must be text, not binary content")

    changes = proposal.get("changes")
    if not isinstance(changes, list) or not changes:
        errors.append("changes must be a non-empty list")
        return errors

    seen: set[str] = set()
    for index, change in enumerate(changes):
        errors.extend(_validate_change(change, approved_write_set, index))
        if isinstance(change, dict):
            path_text = _change_path(change)
            if path_text in seen:
                errors.append(f"changes[{index}].path duplicates another change")
            if path_text is not None:
                seen.add(path_text)
    return errors


def materialize_patch_proposal(proposal: dict[str, Any], repo_root: Path, approved_write_set: set[str]) -> list[str]:
    errors = validate_patch_proposal(proposal, approved_write_set)
    if errors:
        raise PatchProposalError("; ".join(errors))

    applied: list[str] = []
    root = repo_root.resolve(strict=True)
    for change in proposal["changes"]:
        relative = Path(change["path"])
        target = (root / relative).resolve(strict=False)
        try:
            target.relative_to(root)
        except ValueError as exc:
            raise PatchProposalError(f"patch target escapes repository: {change['path']}") from exc
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(change["content"], encoding=PATCH_PROPOSAL_TEXT_ENCODING)
        applied.append(relative.as_posix())
    return applied
