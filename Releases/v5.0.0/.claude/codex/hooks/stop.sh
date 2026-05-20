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

TMP_INPUT="$(mktemp "${TMPDIR:-/tmp}/pai-codex-stop.XXXXXX")"
trap 'command rm "$TMP_INPUT" 2>/dev/null || true' EXIT
cat > "$TMP_INPUT"

python3 - "$TMP_INPUT" "$OBS_DIR/codex-stop.jsonl" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import os
import sys

from log_event import append_jsonl, load_json_file, now, safe_error
from pulse_notify import notify

input_path = Path(sys.argv[1])
log_path = Path(sys.argv[2]).expanduser()


def last_assistant_len(payload: dict) -> int:
    for key in ("last_assistant_message", "lastAssistantMessage", "assistant_message", "message"):
        value = payload.get(key)
        if isinstance(value, str):
            return len(value)
    return 0


try:
    payload = load_json_file(input_path)
    pulse_result = notify(
        "codex.turn.complete",
        "PAI Codex turn complete",
        details={
            "turn_id_present": bool(payload.get("turn_id") or payload.get("turnId")),
            "last_assistant_message_length": last_assistant_len(payload),
        },
    )
    append_jsonl(
        log_path,
        {
            "timestamp": now(),
            "hook_event_name": "Stop",
            "turn_id": payload.get("turn_id") or payload.get("turnId"),
            "cwd": payload.get("cwd") or os.getcwd(),
            "stop_hook_active": True,
            "last_assistant_message_length": last_assistant_len(payload),
            "pulse": pulse_result,
        },
    )
except Exception as exc:
    try:
        append_jsonl(log_path, {"timestamp": now(), "hook_event_name": "Stop", "stop_hook_active": True, "error": safe_error(exc)})
    except Exception:
        pass
print("{}")
PY
