#!/usr/bin/env bash
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAI_DIR="${PAI_DIR:-$HOME/.claude/PAI}"
OBS_DIR="$PAI_DIR/MEMORY/OBSERVABILITY"
mkdir -p "$OBS_DIR"
export PYTHONPATH="$HOOK_DIR/lib${PYTHONPATH:+:$PYTHONPATH}"

if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' '{}'
  exit 0
fi

TMP_INPUT="$(mktemp "${TMPDIR:-/tmp}/pai-codex-probe.XXXXXX")"
trap 'command rm "$TMP_INPUT" 2>/dev/null || true' EXIT
cat > "$TMP_INPUT"

python3 - "$TMP_INPUT" "$OBS_DIR/codex-runtime-probe.jsonl" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import os
import sys

from log_event import append_jsonl, load_json_file, now, safe_error
from redact import text_facts

input_path = Path(sys.argv[1])
log_path = Path(sys.argv[2]).expanduser()

try:
    payload = load_json_file(input_path)
    event = str(payload.get("hook_event_name") or payload.get("hookEventName") or payload.get("event") or payload.get("name") or "unknown")
    tool_input = payload.get("tool_input") if isinstance(payload.get("tool_input"), dict) else {}
    command = tool_input.get("command") if isinstance(tool_input.get("command"), str) else ""
    prompt = payload.get("prompt") if isinstance(payload.get("prompt"), str) else ""

    append_jsonl(
        log_path,
        {
            "timestamp": now(),
            "hook_event_name": event,
            "probe": True,
            "tool_name": payload.get("tool_name") or payload.get("toolName") or "",
            "cwd": payload.get("cwd") or os.getcwd(),
            "has_prompt": bool(prompt),
            "prompt": text_facts(prompt),
            "has_tool_input_command": bool(command),
            "command": text_facts(command),
        },
    )

    if event == "SessionStart":
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "PAI_CODEX_PROBE=SessionStart observed.\n",
            }
        }
    elif event == "UserPromptSubmit":
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "PAI_CODEX_PROBE=UserPromptSubmit observed.\n",
            }
        }
    else:
        output = {}
except Exception as exc:
    try:
        append_jsonl(log_path, {"timestamp": now(), "probe": True, "error": safe_error(exc)})
    except Exception:
        pass
    output = {}

print(json.dumps(output, sort_keys=True))
PY
