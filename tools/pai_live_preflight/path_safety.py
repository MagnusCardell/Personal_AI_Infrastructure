"""Path-safety helpers for fixture-only S14C preflight tests."""

from __future__ import annotations

from pathlib import Path


class PathSafetyError(ValueError):
    """Raised when a fixture path would escape the approved boundary."""


SOURCE_ROOT_EXISTENCE_CHECK = "source-root existence checks"
SOURCE_ROOT_DIRECTORY_CHECK = "source-root directory checks"
HIGH_LEVEL_STRUCTURAL_METADATA_CHECK = "high-level structural metadata checks"
CONTENT_BODY_READ = "content-body reads"

FORBIDDEN_SUBTREE_MARKERS = (
    (".claude", "projects"),
    ("projects",),
    (".codex",),
    ("codex",),
    ("Memory", "WORK", "DO_NOT_READ.md"),
    ("ISA", "DO_NOT_READ.md"),
    ("Pulse", "events", "DO_NOT_READ.json"),
)


def reject_path_traversal(path_value: str | Path, *, allow_absolute: bool = False) -> Path:
    candidate = Path(path_value)
    if not allow_absolute and candidate.is_absolute():
        raise PathSafetyError("absolute paths are not allowed for relative probes")
    if any(part == ".." for part in candidate.parts):
        raise PathSafetyError("path traversal is detected")
    if "\x00" in str(path_value):
        raise PathSafetyError("NUL byte is not allowed in paths")
    if str(path_value).startswith("~") or "$HOME" in str(path_value) or "${HOME}" in str(path_value):
        raise PathSafetyError("home-directory expansion is not allowed")
    return candidate


def is_within_root(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def resolve_fixture_root(fixture_root: str | Path) -> Path:
    root = reject_path_traversal(fixture_root, allow_absolute=True)
    try:
        resolved = root.resolve(strict=False)
    except RuntimeError as exc:
        raise PathSafetyError("ambiguous path resolution") from exc
    if not resolved.exists():
        raise PathSafetyError("source root exists check failed")
    if not resolved.is_dir():
        raise PathSafetyError("source root is a directory check failed")
    return resolved


def reject_symlink_escape(root: Path, candidate: Path) -> Path:
    try:
        resolved_candidate = candidate.resolve(strict=False)
    except RuntimeError as exc:
        raise PathSafetyError("ambiguous path resolution") from exc
    if not is_within_root(root, resolved_candidate):
        raise PathSafetyError("symlink escape is detected")
    return resolved_candidate


def _parts_match(parts: tuple[str, ...], marker: tuple[str, ...]) -> bool:
    marker_len = len(marker)
    if marker_len == 0:
        return False
    for index in range(0, len(parts) - marker_len + 1):
        if parts[index : index + marker_len] == marker:
            return True
    return False


def reject_forbidden_subtree(relative_path: str | Path) -> None:
    parts = tuple(Path(relative_path).parts)
    for marker in FORBIDDEN_SUBTREE_MARKERS:
        if _parts_match(parts, marker):
            raise PathSafetyError("the trial would read forbidden targets")


def ensure_allowed_probe(root: Path, relative_path: str | Path, category: str) -> Path:
    if category == CONTENT_BODY_READ:
        raise PathSafetyError("content-body reads are not allowed")
    if category not in {
        SOURCE_ROOT_EXISTENCE_CHECK,
        SOURCE_ROOT_DIRECTORY_CHECK,
        HIGH_LEVEL_STRUCTURAL_METADATA_CHECK,
    }:
        raise PathSafetyError("unknown probe category")

    rel = reject_path_traversal(relative_path)
    reject_forbidden_subtree(rel)
    candidate = root / rel
    reject_symlink_escape(root, candidate)
    return candidate


def redact_path(path: str | Path) -> str:
    candidate = Path(path)
    if candidate.name:
        return f"<redacted>/{candidate.name}"
    return "<redacted>"
