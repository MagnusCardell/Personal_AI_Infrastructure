from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
import json
import os
import re
import sys

try:
    from redact import redact_obj, redact_text
except Exception:  # pragma: no cover - direct fallback for damaged installs
    def redact_text(text: str | None, *, max_length: int | None = None) -> tuple[str, dict[str, Any]]:
        value = "" if text is None else str(text)
        safe = re.sub(r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key)\s*[:=]\s*[^\s\"'`,;]{6,}", r"\1=[REDACTED]", value)
        safe = re.sub(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b", "[REDACTED]", safe)
        safe = re.sub(r"\b" + "sk" + r"-(?:ant-)?[A-Za-z0-9_-]{20,}\b", "[REDACTED]", safe)
        if max_length is not None and len(safe) > max_length:
            safe = safe[:max_length].rstrip() + f"...[truncated:{len(safe) - max_length}]"
        return safe, {"redacted": safe != value}

    def redact_obj(value: Any) -> tuple[Any, dict[str, Any]]:
        if isinstance(value, str):
            return redact_text(value)[0], {}
        if isinstance(value, list):
            return [redact_obj(item)[0] for item in value], {}
        if isinstance(value, dict):
            return {str(key): redact_obj(item)[0] for key, item in value.items()}, {}
        return value, {}


TRIGGER_PHASES = {"complete", "learn"}
LEARNING_SECTIONS = {"changelog", "learning"}
FILTERED_SECTIONS = {"decisions", "verification"}
FILTERED_MARKERS = ("learned:", "learning:", "lesson:", "refined:")


def pai_root() -> Path:
    raw = os.environ.get("PAI_DIR") or str(Path.home() / ".claude" / "PAI")
    return Path(raw).expanduser().resolve(strict=False)


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def safe_error(message: str) -> None:
    safe, _ = redact_text(message, max_length=360)
    print(f"codex_stop_learning: {safe}", file=sys.stderr)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_metadata(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines:
        return {}

    meta_lines: list[str] = []
    if lines[0].strip() == "---":
        for line in lines[1:120]:
            if line.strip() == "---":
                break
            meta_lines.append(line)
    else:
        for line in lines[:80]:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                break
            meta_lines.append(line)

    metadata: dict[str, str] = {}
    for line in meta_lines:
        match = re.match(r"^\s*([A-Za-z0-9_-]+)\s*:\s*(.*?)\s*$", line)
        if not match:
            continue
        value = match.group(2).strip().strip("\"'")
        metadata[match.group(1).lower()] = value
    return metadata


def markdown_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            current = match.group(1).strip().lower()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def entry_chunks(body: str) -> list[str]:
    chunks: list[str] = []
    current: list[str] = []

    def flush() -> None:
        nonlocal current
        text = "\n".join(line.rstrip() for line in current).strip()
        if text:
            chunks.append(text)
        current = []

    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        starts_entry = bool(re.match(r"^(-|\*|\d+\.)\s+", stripped))
        if starts_entry and current:
            flush()
        current.append(stripped)
    flush()
    return chunks


def extract_entries(text: str) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    sections = markdown_sections(text)
    for name, body in sections.items():
        normalized = name.lower()
        include_all = normalized in LEARNING_SECTIONS
        include_filtered = normalized in FILTERED_SECTIONS
        if not include_all and not include_filtered:
            continue
        for chunk in entry_chunks(body):
            lower = chunk.lower()
            if include_all or any(marker in lower for marker in FILTERED_MARKERS):
                safe_chunk, _ = redact_text(chunk)
                if safe_chunk.strip():
                    result.append({"section": name, "text": safe_chunk.strip()})
    return result


def content_hash(isa_path: Path, phase: str, entries: list[dict[str, str]]) -> str:
    payload = {
        "isa_path": str(isa_path),
        "phase": phase,
        "entries": entries,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def existing_hashes(learning_root: Path) -> set[str]:
    hashes: set[str] = set()
    if not learning_root.exists():
        return hashes
    for path in learning_root.glob("*/session.jsonl"):
        try:
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                if not line.strip():
                    continue
                value = json.loads(line)
                if isinstance(value, dict) and isinstance(value.get("content_hash"), str):
                    hashes.add(value["content_hash"])
        except Exception as exc:
            safe_error(f"could not inspect existing learning file {path}: {exc}")
    return hashes


def write_record(root: Path, record: dict[str, Any]) -> Path:
    now = datetime.now(timezone.utc)
    output = root / "MEMORY" / "LEARNING" / "ALGORITHM" / now.strftime("%Y-%m") / "session.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    safe_record, _ = redact_obj(record)
    with output.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(safe_record, sort_keys=True) + "\n")
    return output


def process_isa(arg: str) -> bool:
    root = pai_root()
    work_root = (root / "MEMORY" / "WORK").resolve(strict=False)
    isa_path = Path(arg).expanduser().resolve(strict=False)
    if not is_relative_to(isa_path, work_root):
        return False
    if isa_path.name != "ISA.md" or not isa_path.is_file():
        return False

    text = read_text(isa_path)
    metadata = parse_metadata(text)
    phase = metadata.get("phase", "").strip().lower()
    if phase not in TRIGGER_PHASES:
        return False

    entries = extract_entries(text)
    if not entries:
        return False

    isa_slug = metadata.get("slug", "").strip() or isa_path.parent.name
    digest = content_hash(isa_path, phase, entries)
    learning_root = root / "MEMORY" / "LEARNING" / "ALGORITHM"
    if digest in existing_hashes(learning_root):
        return False

    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "source": "codex_stop_learning",
        "isa_slug": isa_slug,
        "isa_path": str(isa_path),
        "phase": phase,
        "entries": entries,
        "content_hash": digest,
    }
    write_record(root, record)
    return True


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        safe_error("usage: learning.py /path/to/MEMORY/WORK/slug/ISA.md")
        return 0
    try:
        process_isa(argv[1])
    except Exception as exc:
        safe_error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
