from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import os
import re


DEFAULT_FILE_LIMIT = 2500
DEFAULT_SUMMARY_LIMIT = 900
ALGORITHM_LIMIT = 1600


SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----", re.I | re.S),
    re.compile(r"\b" + "sk" + r"-(?:ant-)?[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key|client[_-]?secret)\s*[:=]\s*[^\s\"'`,;]{6,}"),
    re.compile(r"\b([a-z][a-z0-9+.-]*://)([^/\s:@]{1,128}):([^@\s/]{1,128})@"),
)


@dataclass(frozen=True)
class ReadResult:
    path: Path
    text: str
    ok: bool
    missing_label: str | None = None


def pai_root() -> Path:
    raw = os.environ.get("PAI_DIR") or str(Path.home() / ".claude" / "PAI")
    return Path(raw).expanduser().resolve(strict=False)


def _redact(text: str) -> str:
    safe = text
    for pattern in SECRET_PATTERNS:
        safe = pattern.sub("[REDACTED]", safe)
    return safe


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + f"\n[truncated:{len(text) - limit}]"


def read_bounded(path: Path, *, limit: int = DEFAULT_FILE_LIMIT) -> ReadResult:
    expanded = path.expanduser()
    if not expanded.exists():
        return ReadResult(expanded, "", False, str(expanded))
    if not expanded.is_file():
        return ReadResult(expanded, "", False, f"{expanded} is not a file")
    try:
        raw = expanded.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return ReadResult(expanded, "", False, f"{expanded} unreadable: {exc.__class__.__name__}")
    return ReadResult(expanded, _truncate(_redact(raw.strip()), limit), True)


def summarize_markdown(text: str, *, limit: int = DEFAULT_SUMMARY_LIMIT) -> str:
    if not text.strip():
        return "[empty]"
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#") or line.startswith("- ") or line.startswith("* ") or line[:3].isdigit():
            lines.append(line)
        elif len(lines) < 8:
            lines.append(line)
        if len("\n".join(lines)) >= limit:
            break
    summary = "\n".join(lines) if lines else text.strip()
    return _truncate(summary, limit)


def _algorithm_candidate_paths(pointer: str, algorithm_root: Path) -> list[Path]:
    raw = pointer.strip()
    if not raw:
        return []
    raw_path = Path(raw).expanduser()
    candidates: list[Path] = []
    if raw_path.is_absolute():
        candidates.append(raw_path)
    else:
        candidates.append(algorithm_root / raw)
        if not raw.endswith(".md"):
            candidates.append(algorithm_root / f"v{raw}.md")
            candidates.append(algorithm_root / f"{raw}.md")
    return candidates


def resolve_algorithm(root: Path) -> tuple[str, Path | None, ReadResult | None, list[str]]:
    algorithm_root = root / "ALGORITHM"
    latest = read_bounded(algorithm_root / "LATEST", limit=240)
    if not latest.ok:
        return "", None, None, [latest.missing_label or str(latest.path)]

    pointer = latest.text.strip().splitlines()[0].strip() if latest.text.strip() else ""
    missing: list[str] = []
    try:
        safe_algorithm_root = algorithm_root.resolve(strict=False)
    except OSError:
        safe_algorithm_root = algorithm_root

    for candidate in _algorithm_candidate_paths(pointer, algorithm_root):
        resolved = candidate.resolve(strict=False)
        if safe_algorithm_root != resolved and safe_algorithm_root not in resolved.parents:
            missing.append(f"{candidate} outside PAI/ALGORITHM")
            continue
        result = read_bounded(resolved, limit=ALGORITHM_LIMIT)
        if result.ok:
            return pointer, resolved, result, []
        missing.append(result.missing_label or str(result.path))
    return pointer, None, None, missing or [f"unresolved Algorithm pointer: {pointer}"]


def load_pai_context() -> dict[str, Any]:
    root = pai_root()
    paths = {
        "principal": root / "USER" / "PRINCIPAL_IDENTITY.md",
        "da": root / "USER" / "DA_IDENTITY.md",
        "projects": root / "USER" / "PROJECTS" / "PROJECTS.md",
        "telos": root / "USER" / "TELOS" / "PRINCIPAL_TELOS.md",
    }
    reads = {key: read_bounded(path) for key, path in paths.items()}
    algorithm_pointer, algorithm_path, algorithm_read, algorithm_missing = resolve_algorithm(root)

    missing = [
        result.missing_label or str(result.path)
        for result in reads.values()
        if not result.ok
    ] + algorithm_missing
    available_count = sum(1 for result in reads.values() if result.ok) + (1 if algorithm_read and algorithm_read.ok else 0)
    status = "available" if not missing else ("partial" if available_count else "missing")

    return {
        "pai_dir": str(root),
        "status": status,
        "principal_path": str(paths["principal"]),
        "da_path": str(paths["da"]),
        "projects_path": str(paths["projects"]),
        "telos_path": str(paths["telos"]),
        "principal_summary": summarize_markdown(reads["principal"].text),
        "da_summary": summarize_markdown(reads["da"].text),
        "projects_summary": summarize_markdown(reads["projects"].text, limit=1200),
        "telos_summary": summarize_markdown(reads["telos"].text),
        "algorithm_pointer": algorithm_pointer or "[missing]",
        "algorithm_path": str(algorithm_path) if algorithm_path else "[unresolved]",
        "algorithm_summary": summarize_markdown(algorithm_read.text, limit=900) if algorithm_read else "[missing]",
        "missing_files": missing,
    }
