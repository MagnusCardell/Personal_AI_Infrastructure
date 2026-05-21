from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
import json
import os
import re
import sys


SECTION_TITLES = {
    "decisions": "Decisions",
    "changelog": "Changelog",
    "verification": "Verification",
}

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private_key_block", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----", re.I | re.S)),
    ("provider_token", re.compile(r"\b" + "sk" + r"-(?:ant-)?[A-Za-z0-9_-]{20,}\b")),
    ("github_token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b")),
    ("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("bearer_token", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}")),
    ("generic_secret_kv", re.compile(r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key|private[_-]?key|client[_-]?secret)\s*[:=]\s*[^\s\"'`,;]{6,}")),
)


class SkillError(Exception):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def pai_root() -> Path:
    raw = os.environ.get("PAI_DIR") or str(Path.home() / ".claude" / "PAI")
    return Path(raw).expanduser().resolve(strict=False)


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def redact_text(text: str) -> tuple[str, dict[str, Any]]:
    redacted = text
    counts: dict[str, int] = {}
    for name, pattern in SECRET_PATTERNS:
        def repl(match: re.Match[str]) -> str:
            counts[name] = counts.get(name, 0) + 1
            if name == "generic_secret_kv":
                key = match.group(1)
                return f"{key}=[REDACTED:{name}]"
            return f"[REDACTED:{name}]"

        redacted = pattern.sub(repl, redacted)
    return redacted, {"redacted": bool(counts), "redaction_counts": counts}


def content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8", errors="replace")).hexdigest()


def safe_log(record: dict[str, Any]) -> None:
    root = pai_root()
    log_path = root / "MEMORY" / "SKILLS" / "codex-execution.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def protected_paths() -> list[Path]:
    home = Path.home()
    return [
        home / ".ssh",
        home / ".gnupg",
        home / ".aws",
        home / ".codex" / "auth.json",
        home / ".claude" / ".env",
        Path("/") / "etc" / "passwd",
        Path("/") / "etc" / ("shad" + "ow"),
    ]


def resolve_isa_path(raw_path: str) -> Path:
    root = pai_root()
    work_root = (root / "MEMORY" / "WORK").resolve(strict=False)
    requested = Path(raw_path).expanduser()
    if not requested.exists():
        raise SkillError(f"ISA path does not exist: {requested}")
    resolved = requested.resolve(strict=True)
    if resolved.name != "ISA.md":
        raise SkillError("ISA path must be named ISA.md")
    if not is_relative_to(resolved, work_root):
        raise SkillError("ISA path must resolve under PAI MEMORY/WORK")
    for protected in protected_paths():
        protected_resolved = protected.expanduser().resolve(strict=False)
        if resolved == protected_resolved or is_relative_to(resolved, protected_resolved):
            raise SkillError("ISA path targets a protected path")
    return resolved


def append_to_section(text: str, section_key: str, content: str) -> str:
    title = SECTION_TITLES[section_key]
    heading = f"## {title}"
    lines = text.splitlines()
    heading_index: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            heading_index = index
            break

    block_lines = content.rstrip().splitlines()
    if heading_index is None:
        prefix = text.rstrip()
        section_text = "\n".join([heading, "", *block_lines]).rstrip()
        if not prefix:
            return section_text + "\n"
        return prefix + "\n\n" + section_text + "\n"

    insert_index = len(lines)
    for index in range(heading_index + 1, len(lines)):
        if re.match(r"^##\s+", lines[index]):
            insert_index = index
            break

    before = lines[:insert_index]
    after = lines[insert_index:]
    while before and before[-1] == "":
        before.pop()
    insertion = ["", *block_lines]
    if after:
        insertion.append("")
    return "\n".join(before + insertion + after).rstrip() + "\n"


def append_skill(isa_arg: str, section_arg: str, raw_content: str) -> int:
    section = section_arg.strip().lower()
    if section not in SECTION_TITLES:
        raise SkillError("unsupported section; allowed: decisions, changelog, verification")
    if not raw_content.strip():
        raise SkillError("content must not be empty")

    isa_path = resolve_isa_path(isa_arg)
    safe_content, redaction = redact_text(raw_content.strip())
    if not safe_content.strip():
        raise SkillError("content became empty after redaction")

    original = isa_path.read_text(encoding="utf-8", errors="replace")
    updated = append_to_section(original, section, safe_content)
    isa_path.write_text(updated, encoding="utf-8")

    record = {
        "ts": now(),
        "source": "codex_skill_dispatch",
        "skill": "isa_append",
        "isa_slug": isa_path.parent.name,
        "isa_path": str(isa_path),
        "section": section,
        "content_hash": content_hash(safe_content),
        "result": "appended",
        "redaction": redaction,
    }
    safe_log(record)
    print(json.dumps({"result": "appended", "section": section, "isa_path": str(isa_path), "redacted": redaction["redacted"]}, sort_keys=True))
    return 0


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("usage: isa_append.py <isa_path> <section> <content>", file=sys.stderr)
        return 2
    isa_arg, section_arg, content = argv[1], argv[2], argv[3]
    try:
        return append_skill(isa_arg, section_arg, content)
    except Exception as exc:
        section = section_arg.strip().lower() if len(argv) > 2 else ""
        record = {
            "ts": now(),
            "source": "codex_skill_dispatch",
            "skill": "isa_append",
            "isa_slug": Path(isa_arg).expanduser().parent.name if isa_arg else "",
            "isa_path": str(Path(isa_arg).expanduser()) if isa_arg else "",
            "section": section,
            "content_hash": content_hash(content) if content else None,
            "result": "rejected",
            "error_type": exc.__class__.__name__,
        }
        try:
            safe_log(record)
        except Exception:
            pass
        print(str(exc), file=sys.stderr)
        return 1 if isinstance(exc, SkillError) else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
