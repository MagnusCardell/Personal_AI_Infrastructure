"""Codex skill: isa_scaffold - create a canonical starter task ISA.

This is intentionally deterministic. It does not call a model, does not
network, and writes only under PAI_DIR/MEMORY/WORK.

usage:
  isa_scaffold.py [--tier E1|E2|E3|E4|E5] [--slug SLUG] TASK...
  echo "task" | isa_scaffold.py --tier E2
"""
from __future__ import annotations

from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
import json
import os
import re
import sys


TIERS = {"E1", "E2", "E3", "E4", "E5"}

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


def timestamp_slug_prefix() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


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


def safe_log(root: Path, record: dict[str, Any]) -> None:
    try:
        log_path = root / "MEMORY" / "SKILLS" / "codex-execution.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    except Exception:
        pass


def slugify(text: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized[:56].strip("-") or "task"


def validate_slug(raw: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,120}", raw):
        raise SkillError("slug must contain only letters, numbers, dot, dash, or underscore")
    return raw


def unique_slug(work_root: Path, task: str) -> str:
    base = f"{timestamp_slug_prefix()}_{slugify(task)}"
    candidate = base
    suffix = 2
    while (work_root / candidate).exists():
        candidate = f"{base}-{suffix}"
        suffix += 1
    return candidate


def collect_task(positional: list[str]) -> str:
    task = " ".join(part.strip() for part in positional if part.strip()).strip()
    if not task and not sys.stdin.isatty():
        task = sys.stdin.read().strip()
    if not task:
        raise SkillError("task must not be empty")
    return task


def split_trailing_tier(positional: list[str], tier: str | None) -> tuple[list[str], str]:
    if tier:
        return positional, tier.upper()
    if positional and positional[-1].upper() in TIERS:
        return positional[:-1], positional[-1].upper()
    return positional, "E3"


def default_criteria() -> list[tuple[str, str]]:
    return [
        ("ISC-1", "Canonical ISA file exists at the reported work path."),
        ("ISC-2", "Frontmatter records task, slug, effort, phase, and progress."),
        ("ISC-3", "Criteria and verification sections use stable ISC identifiers."),
        ("ISC-A1", "Anti: Scaffold does not overwrite an existing ISA file."),
    ]


def yaml_value(value: str) -> str:
    return json.dumps(value)


def render_isa(task: str, slug: str, tier: str, mode: str, started: str) -> str:
    criteria = default_criteria()
    criteria_count = len(criteria)
    criterion_lines = [f"- [ ] {criterion_id}: {text}" for criterion_id, text in criteria]
    verification_lines = [f"- {criterion_id}: Pending verification." for criterion_id, _ in criteria]
    task_hash = content_hash(task)[:16]

    return "\n".join(
        [
            "---",
            f"task: {yaml_value(task)}",
            f"slug: {slug}",
            f"effort: {tier}",
            "phase: observe",
            f"progress: 0/{criteria_count}",
            f"mode: {mode}",
            f"started: {started}",
            f"updated: {started}",
            "---",
            "",
            "## Problem",
            "",
            f"The task needs a durable Ideal State Artifact before execution: {task}",
            "",
            "## Vision",
            "",
            "The work has an explicit, human-readable definition of done before edits or runtime changes proceed.",
            "",
            "## Out of Scope",
            "",
            "- Full ISA interview expansion.",
            "- Project-level ISA replacement.",
            "- Any write outside the canonical PAI work memory path.",
            "",
            "## Principles",
            "",
            "- Keep the scaffold deterministic and auditable.",
            "- Prefer stable ISC identifiers over prose-only status.",
            "- Leave high-stakes decomposition to a deeper ISA pass.",
            "",
            "## Constraints",
            "",
            "- The scaffold is generated without network access or model calls.",
            "- The output path must resolve under PAI MEMORY/WORK.",
            "- Existing ISA files are never overwritten by default.",
            "",
            "## Goal",
            "",
            f"Create a starter ISA for: {task}",
            "",
            "## Criteria",
            "",
            *criterion_lines,
            "",
            "## Test Strategy",
            "",
            "- ISC-1: Check the reported path exists and is named ISA.md.",
            "- ISC-2: Inspect frontmatter for required metadata fields.",
            "- ISC-3: Inspect Criteria and Verification for matching identifiers.",
            "- ISC-A1: Attempting to reuse an existing slug must be rejected.",
            "",
            "## Features",
            "",
            "- Deterministic task ISA creation.",
            "- Canonical PAI MEMORY/WORK pathing.",
            "- JSON result for dispatcher consumption.",
            "",
            "## Decisions",
            "",
            f"- Deterministic starter scaffold used compact criteria for task hash `{task_hash}`.",
            "- Deep tier decomposition remains the caller's responsibility when needed.",
            "",
            "## Changelog",
            "",
            f"- {started}: ISA scaffold created by Codex skill dispatch.",
            "",
            "## Verification",
            "",
            *verification_lines,
            "",
        ]
    )


def scaffold(task: str, tier: str, slug_arg: str | None, mode: str) -> dict[str, Any]:
    if tier not in TIERS:
        raise SkillError("tier must be one of E1, E2, E3, E4, or E5")

    root = pai_root()
    work_root = (root / "MEMORY" / "WORK").resolve(strict=False)
    work_root.mkdir(parents=True, exist_ok=True)
    slug = validate_slug(slug_arg) if slug_arg else unique_slug(work_root, task)
    target_dir = (work_root / slug).resolve(strict=False)
    target = target_dir / "ISA.md"
    if not is_relative_to(target.resolve(strict=False), work_root):
        raise SkillError("target path escapes PAI MEMORY/WORK")
    if target.exists():
        raise SkillError(f"ISA already exists: {target}")

    safe_task, redaction = redact_text(task)
    if not safe_task.strip():
        raise SkillError("task became empty after redaction")

    started = now()
    target_dir.mkdir(parents=True, exist_ok=False)
    target.write_text(render_isa(safe_task, slug, tier, mode, started), encoding="utf-8")

    result = {
        "result": "created",
        "skill": "isa_scaffold",
        "isa_path": str(target),
        "slug": slug,
        "effort": tier,
        "criteria_count": len(default_criteria()),
        "redacted": redaction["redacted"],
    }
    safe_log(
        root,
        {
            "ts": started,
            "source": "codex_skill_dispatch",
            "skill": "isa_scaffold",
            "isa_slug": slug,
            "isa_path": str(target),
            "effort": tier,
            "task_hash": content_hash(safe_task),
            "result": "created",
            "redaction": redaction,
        },
    )
    return result


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Create a deterministic starter task ISA.")
    parser.add_argument("--tier", "--effort", choices=sorted(TIERS), help="Effort tier. Defaults to E3.")
    parser.add_argument("--slug", help="Optional explicit work slug. Refuses overwrite.")
    parser.add_argument("--mode", default="algorithm", help="ISA mode frontmatter value.")
    parser.add_argument("task", nargs="*", help="Task prompt. Read from stdin when omitted.")
    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        task_args, tier = split_trailing_tier(args.task, args.tier)
        task = collect_task(task_args)
        result = scaffold(task, tier, args.slug, args.mode)
        print(json.dumps(result, sort_keys=True))
        return 0
    except Exception as exc:
        root = pai_root()
        safe_log(
            root,
            {
                "ts": now(),
                "source": "codex_skill_dispatch",
                "skill": "isa_scaffold",
                "result": "rejected",
                "error_type": exc.__class__.__name__,
            },
        )
        print(str(exc), file=sys.stderr)
        return 1 if isinstance(exc, SkillError) else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
