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

TMP_INPUT="$(mktemp "${TMPDIR:-/tmp}/pai-codex-pretool.XXXXXX")"
trap 'rm -f "$TMP_INPUT"' EXIT
cat > "$TMP_INPUT"

python3 - "$TMP_INPUT" "$OBS_DIR/codex-pretool.jsonl" <<'PY'
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
HOME = str(Path.home())


def command_text(payload: dict) -> tuple[str, str]:
    tool_name = str(payload.get("tool_name") or payload.get("toolName") or "")
    tool_input = payload.get("tool_input") if isinstance(payload.get("tool_input"), dict) else {}
    command = tool_input.get("command") if isinstance(tool_input.get("command"), str) else ""
    if command:
        return tool_name, command
    return tool_name, json.dumps(tool_input, sort_keys=True)


def protected_terms() -> list[str]:
    home_low = HOME.lower()
    dot = "."
    return [
        "~/" + dot + "ssh",
        home_low + "/" + dot + "ssh",
        "$home/" + dot + "ssh",
        "~/" + dot + "gnupg",
        home_low + "/" + dot + "gnupg",
        "$home/" + dot + "gnupg",
        "~/" + dot + "aws",
        home_low + "/" + dot + "aws",
        "$home/" + dot + "aws",
        "~/" + dot + "config/gcloud",
        home_low + "/" + dot + "config/gcloud",
        "$home/" + dot + "config/gcloud",
        "~/" + dot + "codex/" + "auth.json",
        home_low + "/" + dot + "codex/" + "auth.json",
        "$home/" + dot + "codex/" + "auth.json",
        "~/" + dot + "claude/" + ".env",
        home_low + "/" + dot + "claude/" + ".env",
        "$home/" + dot + "claude/" + ".env",
    ]


def danger_reason(command: str) -> str | None:
    compact = re.sub(r"\s+", " ", command.lower())
    flags = risk_flags(command)
    forced_remove = r"\br" + r"m\s+-[^\n;]*r[^\n;]*f"
    if flags["contains_url_credentials"]:
        return "credentials must not be placed in URLs"
    if re.search(forced_remove + r"[^\n;]*\s+/(?:\s|$|\*)", compact):
        return "blocks recursive force delete against filesystem root"
    if re.search(r"\bsudo\s+" + forced_remove, compact):
        return "blocks elevated recursive force delete"
    if re.search(r"\bcurl\b[^\n|;]*\|\s*(?:sudo\s+)?(?:bash|sh)\b", compact):
        return "blocks network input piped to shell"
    if re.search(r"\bwget\b[^\n|;]*\|\s*(?:sudo\s+)?(?:bash|sh)\b", compact):
        return "blocks network input piped to shell"
    if flags["mentions_shell_eval"]:
        return "blocks eval of command substitution"
    if re.search(r"\bchmod\s+-r\s+777\s+/(?:\s|$)", compact):
        return "blocks world-writable chmod against filesystem root"
    account_paths = ["/etc/" + "passwd", "/etc/" + "shad" + "ow"]
    if any(path in compact for path in account_paths):
        if re.search(r"(>|>>|\btee\b|\bsed\s+-i\b|\bperl\s+-i\b|\bmv\b|\bcp\b|\brm\b|\bchmod\b|\bchown\b)", compact):
            return "blocks writes or destructive operations against system account files"
    if any(path in compact for path in protected_terms()):
        return "blocks operations against protected credential or secret paths"
    return None


try:
    payload = load_json_file(input_path)
    tool_name, command = command_text(payload)
    reason = danger_reason(command)
    decision = "deny" if reason else "allow"
    append_jsonl(
        log_path,
        {
            "timestamp": now(),
            "hook_event_name": "PreToolUse",
            "tool_name": tool_name,
            "cwd": payload.get("cwd") or os.getcwd(),
            "turn_id": payload.get("turn_id") or payload.get("turnId"),
            "tool_use_id": payload.get("tool_use_id") or payload.get("toolUseId"),
            "decision": decision,
            "reason": reason,
            "command": text_facts(command),
        },
    )
    if reason:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}}))
    else:
        print("{}")
except Exception as exc:
    try:
        append_jsonl(log_path, {"timestamp": now(), "hook_event_name": "PreToolUse", "decision": "fallback", "error": safe_error(exc)})
    except Exception:
        pass
    print("{}")
PY
