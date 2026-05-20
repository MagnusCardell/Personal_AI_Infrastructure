#!/usr/bin/env bash
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAI_DIR="${PAI_DIR:-$HOME/.claude/PAI}"
OBS_DIR="$PAI_DIR/MEMORY/OBSERVABILITY"
mkdir -p "$OBS_DIR"
export PYTHONPATH="$HOOK_DIR/lib${PYTHONPATH:+:$PYTHONPATH}"

TMP_INPUT="$(mktemp "${TMPDIR:-/tmp}/pai-codex-permission.XXXXXX")"
trap 'rm -f "$TMP_INPUT"' EXIT
cat > "$TMP_INPUT"

python3 - "$TMP_INPUT" "$OBS_DIR/codex-permissions.jsonl" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import os
import re
import sys

from log_event import append_jsonl, load_json_file, now, safe_error
from redact import risk_flags, text_facts

input_path = Path(sys.argv[1])
log_path = Path(sys.argv[2]).expanduser()


def flattened(payload: dict) -> str:
    tool_input = payload.get("tool_input") if isinstance(payload.get("tool_input"), dict) else {}
    command = tool_input.get("command") if isinstance(tool_input.get("command"), str) else ""
    return command or json.dumps(payload, sort_keys=True)


def known_bad(text: str) -> str | None:
    low = text.lower()
    protected = ["/." + "ssh", "/." + "gnupg", "/." + "aws", "/." + "config/gcloud", "/." + "codex/" + "auth.json", "/." + "claude/" + ".env"]
    forced_remove = r"\br" + r"m\s+-[^\n;]*r[^\n;]*f"
    if any(path in low for path in protected):
        return "permission request touches protected credential or secret paths"
    if re.search(r"\b(sudo\s+)?" + forced_remove, low):
        return "permission request contains recursive force delete"
    if re.search(r"\b(curl|wget)\b[^\n|;]*\|\s*(bash|sh)", low):
        return "permission request pipes network input to a shell"
    account_paths = ["/etc/" + "passwd", "/etc/" + "shad" + "ow"]
    if any(path in low for path in account_paths):
        return "permission request touches system account files"
    if risk_flags(text)["contains_url_credentials"]:
        return "permission request contains credentials in a URL"
    return None


try:
    payload = load_json_file(input_path)
    text = flattened(payload)
    bad = known_bad(text)
    if bad:
        behavior = "deny"
        output = {"hookSpecificOutput": {"hookEventName": "PermissionRequest", "decision": {"behavior": "deny", "message": bad}}}
    else:
        behavior = "fallback"
        output = {}
    append_jsonl(
        log_path,
        {
            "timestamp": now(),
            "hook_event_name": "PermissionRequest",
            "tool_name": payload.get("tool_name") or payload.get("toolName"),
            "cwd": payload.get("cwd") or os.getcwd(),
            "turn_id": payload.get("turn_id") or payload.get("turnId"),
            "behavior": behavior,
            "message": bad,
            "request": text_facts(text),
        },
    )
    print(json.dumps(output))
except Exception as exc:
    try:
        append_jsonl(log_path, {"timestamp": now(), "hook_event_name": "PermissionRequest", "behavior": "fallback", "error": safe_error(exc)})
    except Exception:
        pass
    print("{}")
PY
