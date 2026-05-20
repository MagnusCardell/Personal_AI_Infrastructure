#!/usr/bin/env bash
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAI_DIR="${PAI_DIR:-$HOME/.claude/PAI}"
OBS_DIR="$PAI_DIR/MEMORY/OBSERVABILITY"
mkdir -p "$OBS_DIR"
export PYTHONPATH="$HOOK_DIR/lib${PYTHONPATH:+:$PYTHONPATH}"

if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"PAI_RUNTIME_CONTEXT_ERROR=python3 unavailable; read live PAI files directly when needed.\n"}}'
  exit 0
fi

TMP_INPUT="$(mktemp "${TMPDIR:-/tmp}/pai-codex-session-start.XXXXXX")"
trap 'rm -f "$TMP_INPUT"' EXIT
cat > "$TMP_INPUT"

python3 - "$TMP_INPUT" "$PAI_DIR" "$OBS_DIR/codex-hooks.jsonl" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import os
import sys

from log_event import append_jsonl, load_json_file, now, safe_error

input_path = Path(sys.argv[1])
pai_dir = Path(sys.argv[2]).expanduser()
log_path = Path(sys.argv[3]).expanduser()


def read_text(path: Path, *, limit: int | None = None) -> tuple[str, bool]:
    if not path.exists():
        return f"[missing: {path}]", False
    try:
        text = path.read_text(encoding="utf-8", errors="replace").strip()
    except Exception as exc:
        return f"[unreadable: {path}: {exc.__class__.__name__}]", False
    if limit is not None and len(text) > limit:
        text = text[:limit].rstrip() + f"\n[truncated at {limit} chars]"
    return text, True


def extract_section(markdown: str, heading: str, *, limit: int) -> str:
    marker = f"## {heading}"
    start = markdown.find(marker)
    if start < 0:
        suffix = "\n[section not found; truncated full file]" if len(markdown) > limit else ""
        return markdown[:limit].rstrip() + suffix
    next_start = markdown.find("\n## ", start + len(marker))
    section = markdown[start:] if next_start < 0 else markdown[start:next_start]
    if len(section) > limit:
        section = section[:limit].rstrip() + f"\n[truncated at {limit} chars]"
    return section.strip()


def resolve_algorithm() -> tuple[str, str, bool]:
    latest_path = pai_dir / "ALGORITHM" / "LATEST"
    pointer, ok = read_text(latest_path, limit=200)
    if not ok:
        return pointer, "[missing algorithm pointer]", False
    raw = pointer.strip()
    raw_path = Path(raw)
    candidates: list[Path] = [raw_path] if raw_path.is_absolute() else [pai_dir / "ALGORITHM" / raw]
    if not raw.endswith(".md"):
        candidates.extend([pai_dir / "ALGORITHM" / f"v{raw}.md", pai_dir / "ALGORITHM" / f"{raw}.md"])
    for candidate in candidates:
        if candidate.exists():
            return raw, str(candidate), True
    return raw, f"[unresolved algorithm pointer: {raw}]", False


try:
    payload = load_json_file(input_path)
    principal_path = pai_dir / "USER" / "PRINCIPAL_IDENTITY.md"
    da_path = pai_dir / "USER" / "DA_IDENTITY.md"
    projects_path = pai_dir / "USER" / "PROJECTS" / "PROJECTS.md"
    telos_path = pai_dir / "USER" / "TELOS" / "PRINCIPAL_TELOS.md"

    principal, principal_ok = read_text(principal_path, limit=5000)
    da_identity, da_ok = read_text(da_path, limit=2500)
    projects_raw, projects_ok = read_text(projects_path, limit=None)
    active_projects = extract_section(projects_raw, "Active Projects", limit=9000) if projects_ok else projects_raw
    telos, telos_ok = read_text(telos_path, limit=3500)
    algorithm_pointer, algorithm_file, algorithm_ok = resolve_algorithm()

    missing = [
        label
        for label, ok in [
            (str(principal_path), principal_ok),
            (str(da_path), da_ok),
            (str(projects_path), projects_ok),
            (str(telos_path), telos_ok),
            (algorithm_file, algorithm_ok),
        ]
        if not ok
    ]

    context = "\n".join(
        [
            "PAI_RUNTIME_CONTEXT=Codex runtime support",
            f"PAI_DIR={pai_dir}",
            "PAI_MODE_DEFAULT=NATIVE for identity, project, Telos, and status questions",
            "PAI_ALGORITHM_MODE=Use ALGORITHM for execution-oriented work and live ISA updates",
            f"PAI_ALGORITHM_POINTER={algorithm_pointer}",
            f"PAI_ALGORITHM_FILE={algorithm_file}",
            f"PAI_CONTEXT_MISSING={'; '.join(missing) if missing else 'none'}",
            "",
            "## Principal Identity Source",
            str(principal_path),
            principal,
            "",
            "## Runtime Assistant Identity Source",
            str(da_path),
            da_identity,
            "",
            "## Active Projects Source",
            str(projects_path),
            active_projects,
            "",
            "## Telos Source",
            str(telos_path),
            telos,
        ]
    )

    append_jsonl(
        log_path,
        {
            "timestamp": now(),
            "hook_event_name": "SessionStart",
            "cwd": payload.get("cwd") or os.getcwd(),
            "turn_id": payload.get("turn_id") or payload.get("turnId"),
            "missing_files": missing,
            "context_chars": len(context),
        },
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))
except Exception as exc:
    try:
        append_jsonl(log_path, {"timestamp": now(), "hook_event_name": "SessionStart", "error": safe_error(exc)})
    except Exception:
        pass
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "PAI_RUNTIME_CONTEXT_ERROR=SessionStart failed; continue with live reads when needed.\n"}}))
PY
