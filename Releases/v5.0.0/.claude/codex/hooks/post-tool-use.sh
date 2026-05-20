#!/usr/bin/env bash
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAI_DIR="${PAI_DIR:-$HOME/.claude/PAI}"
OBS_DIR="$PAI_DIR/MEMORY/OBSERVABILITY"
mkdir -p "$OBS_DIR"
export PYTHONPATH="$HOOK_DIR/lib${PYTHONPATH:+:$PYTHONPATH}"

TMP_INPUT="$(mktemp "${TMPDIR:-/tmp}/pai-codex-posttool.XXXXXX")"
trap 'command rm "$TMP_INPUT" 2>/dev/null || true' EXIT
cat > "$TMP_INPUT"

python3 - "$TMP_INPUT" "$PAI_DIR" "$OBS_DIR/codex-posttool.jsonl" "$OBS_DIR/codex-isasync.jsonl" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import sys

from log_event import append_jsonl, load_json_file, now, safe_error
from redact import risk_flags, text_facts

input_path = Path(sys.argv[1])
pai_dir = Path(sys.argv[2]).expanduser()
tool_log_path = Path(sys.argv[3]).expanduser()
sync_log_path = Path(sys.argv[4]).expanduser()
home = str(Path.home())


def get_tool(payload: dict) -> tuple[str, dict, str]:
    tool_name = str(payload.get("tool_name") or payload.get("toolName") or "")
    tool_input = payload.get("tool_input") if isinstance(payload.get("tool_input"), dict) else {}
    command = tool_input.get("command") if isinstance(tool_input.get("command"), str) else json.dumps(tool_input, sort_keys=True)
    return tool_name, tool_input, command


def expand_path(raw_path: str, cwd: str) -> Path:
    cleaned = raw_path.strip().strip("'\"`.,")
    cleaned = cleaned.replace("${HOME}", home).replace("$HOME", home)
    if cleaned.startswith("~/"):
        cleaned = home + cleaned[1:]
    path = Path(cleaned)
    if not path.is_absolute():
        path = Path(cwd) / path
    return path


def extract_isa_paths(payload: dict, tool_name: str, tool_input: dict, command: str) -> list[Path]:
    cwd = str(payload.get("cwd") or os.getcwd())
    candidates: set[Path] = set()
    search_text = command or ""

    for key in ("file_path", "path"):
        value = tool_input.get(key)
        if isinstance(value, str):
            search_text += "\n" + value

    for line in command.splitlines():
        match = re.match(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", line.strip())
        if match:
            candidates.add(expand_path(match.group(1), cwd))

    token_pattern = r"(?P<path>(?:/|~|\$HOME|\$\{HOME\}|[A-Za-z0-9_.-]+/)[^\s\"'`;|<>]*MEMORY/WORK/[^\s\"'`;|<>]*ISA\.md)"
    for match in re.finditer(token_pattern, search_text):
        candidates.add(expand_path(match.group("path"), cwd))

    if tool_name == "Bash":
        expanded = search_text.replace("${HOME}", home).replace("$HOME", home).replace("~/", home + "/")
        for match in re.finditer(r"(?:>|>>)\s*(?P<path>[^\s;|]+ISA\.md)", expanded):
            candidates.add(expand_path(match.group("path"), cwd))
        for match in re.finditer(r"\btee\s+(?:-a\s+)?(?P<path>[^\s;|]+ISA\.md)", expanded):
            candidates.add(expand_path(match.group("path"), cwd))

    work_root = pai_dir / "MEMORY" / "WORK"
    resolved: list[Path] = []
    for candidate in candidates:
        try:
            real_candidate = candidate.expanduser().resolve(strict=False)
            real_work = work_root.expanduser().resolve(strict=False)
            if real_candidate.name == "ISA.md" and real_work in real_candidate.parents:
                resolved.append(real_candidate)
        except Exception:
            continue
    return sorted(set(resolved), key=str)


def run_isasync(isa_path: Path, payload: dict) -> dict:
    bun = shutil.which("bun")
    if not bun:
        return {"status": "absent", "reason": "bun unavailable", "isa_path": str(isa_path)}

    tool_sync = pai_dir / "TOOLS" / "ISASync.ts"
    hook_sync = Path(home) / ".claude" / "hooks" / "ISASync.hook.ts"
    if tool_sync.exists():
        cmd = [bun, str(tool_sync), str(isa_path)]
        input_text = None
        kind = "PAI/TOOLS/ISASync.ts"
    elif hook_sync.exists():
        cmd = [bun, str(hook_sync)]
        synthetic = {
            "hook_event_name": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": str(isa_path)},
            "session_id": payload.get("session_id") or payload.get("sessionId"),
            "turn_id": payload.get("turn_id") or payload.get("turnId"),
            "cwd": payload.get("cwd") or os.getcwd(),
        }
        input_text = json.dumps(synthetic)
        kind = "~/.claude/hooks/ISASync.hook.ts"
    else:
        return {"status": "absent", "reason": "no ISASync implementation found", "isa_path": str(isa_path)}

    try:
        proc = subprocess.run(
            cmd,
            input=input_text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=8,
            check=False,
        )
    except Exception as exc:
        return {"status": "failed", "kind": kind, "isa_path": str(isa_path), "error": safe_error(exc)}

    return {
        "status": "ran" if proc.returncode == 0 else "failed",
        "kind": kind,
        "isa_path": str(isa_path),
        "exit_code": proc.returncode,
        "stdout": text_facts(proc.stdout),
        "stderr": text_facts(proc.stderr),
    }


try:
    payload = load_json_file(input_path)
    tool_name, tool_input, command = get_tool(payload)
    flags = risk_flags(command)
    isa_paths = extract_isa_paths(payload, tool_name, tool_input, command)

    append_jsonl(
        tool_log_path,
        {
            "timestamp": now(),
            "hook_event_name": "PostToolUse",
            "tool_name": tool_name,
            "cwd": payload.get("cwd") or os.getcwd(),
            "turn_id": payload.get("turn_id") or payload.get("turnId"),
            "tool_use_id": payload.get("tool_use_id") or payload.get("toolUseId"),
            "mentions_pai_dir": flags["mentions_pai"],
            "mentions_memory_work": flags["mentions_memory_work"],
            "mentions_isa": flags["mentions_isa"],
            "detected_isa_paths": [str(path) for path in isa_paths],
            "command": text_facts(command),
        },
    )

    for isa_path in isa_paths:
        result = run_isasync(isa_path, payload)
        result["timestamp"] = now()
        append_jsonl(sync_log_path, result)
except Exception as exc:
    try:
        append_jsonl(tool_log_path, {"timestamp": now(), "hook_event_name": "PostToolUse", "error": safe_error(exc)})
    except Exception:
        pass
print("{}")
PY
