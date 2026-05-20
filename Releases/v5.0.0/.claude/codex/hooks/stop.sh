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
import socket
import sys
import urllib.request

from log_event import append_jsonl, load_json_file, now, safe_error

input_path = Path(sys.argv[1])
log_path = Path(sys.argv[2]).expanduser()


def last_assistant_len(payload: dict) -> int:
    for key in ("last_assistant_message", "lastAssistantMessage", "assistant_message", "message"):
        value = payload.get(key)
        if isinstance(value, str):
            return len(value)
    return 0


def pulse_reachable() -> bool:
    try:
        with socket.create_connection(("127.0.0.1", 31337), timeout=0.35):
            return True
    except OSError:
        return False


def maybe_notify(enabled: bool) -> bool:
    if not enabled:
        return False
    payload = json.dumps({"message": "PAI Codex turn complete"}).encode("utf-8")
    request = urllib.request.Request(
        "http://127.0.0.1:31337/notify",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=0.5):
            return True
    except Exception:
        return False


try:
    payload = load_json_file(input_path)
    reachable = pulse_reachable()
    notified = maybe_notify(reachable and os.environ.get("PAI_CODEX_PULSE_NOTIFY", "").lower() in {"1", "true", "yes", "on"})
    append_jsonl(
        log_path,
        {
            "timestamp": now(),
            "hook_event_name": "Stop",
            "turn_id": payload.get("turn_id") or payload.get("turnId"),
            "cwd": payload.get("cwd") or os.getcwd(),
            "stop_hook_active": True,
            "last_assistant_message_length": last_assistant_len(payload),
            "pulse_reachable": reachable,
            "pulse_notified": notified,
        },
    )
except Exception as exc:
    try:
        append_jsonl(log_path, {"timestamp": now(), "hook_event_name": "Stop", "stop_hook_active": True, "error": safe_error(exc)})
    except Exception:
        pass
print("{}")
PY
