#!/usr/bin/env bash
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAI_DIR="${PAI_DIR:-$HOME/.claude/PAI}"
OBS_DIR="$PAI_DIR/MEMORY/OBSERVABILITY"
mkdir -p "$OBS_DIR"
export PYTHONPATH="$HOOK_DIR/lib${PYTHONPATH:+:$PYTHONPATH}"

PAI_CODEX_ENV="$HOOK_DIR/pulse.env"
if [[ -f "$PAI_CODEX_ENV" ]]; then
  PAI_CODEX_ENV_VARS=(
    PAI_CODEX_PULSE_ENABLED
    PAI_CODEX_PULSE_URL
    PAI_CODEX_VOICE_ENABLED
    PAI_CODEX_VOICE_ID
    PAI_CODEX_VOICE_EVENTS
    PAI_CODEX_VOICE_MESSAGE_TURN_COMPLETE
    PAI_CODEX_VOICE_MESSAGE_ISA_UPDATED
    PAI_CODEX_LEARNING_ENABLED
    PAI_CODEX_CHECKPOINT_ENABLED
  )
  for name in "${PAI_CODEX_ENV_VARS[@]}"; do
    had_name="__PAI_CODEX_HAD_${name}"
    saved_name="__PAI_CODEX_SAVED_${name}"
    if [[ ${!name+x} ]]; then
      printf -v "$had_name" '%s' "1"
      printf -v "$saved_name" '%s' "${!name}"
    else
      printf -v "$had_name" '%s' "0"
    fi
  done
  set -a
  # shellcheck source=/dev/null
  . "$PAI_CODEX_ENV"
  set +a
  for name in "${PAI_CODEX_ENV_VARS[@]}"; do
    had_name="__PAI_CODEX_HAD_${name}"
    saved_name="__PAI_CODEX_SAVED_${name}"
    if [[ ${!had_name} == "1" ]]; then
      printf -v "$name" '%s' "${!saved_name}"
      export "$name"
    fi
    unset "$had_name" "$saved_name"
  done
  unset PAI_CODEX_ENV_VARS name had_name saved_name
fi

if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' '{}'
  exit 0
fi

learning_enabled() {
  case "${PAI_CODEX_LEARNING_ENABLED:-0}" in
    1|true|TRUE|yes|YES|on|ON) return 0 ;;
    *) return 1 ;;
  esac
}

run_stop_learning() {
  learning_enabled || return 0
  local helper="$HOOK_DIR/lib/learning.py"
  local work_dir="$PAI_DIR/MEMORY/WORK"
  [[ -f "$helper" && -d "$work_dir" ]] || return 0

  while IFS= read -r -d '' isa_path; do
    python3 "$helper" "$isa_path" >/dev/null || true
  done < <(
    python3 - "$work_dir" <<'PY' 2>/dev/null || true
from __future__ import annotations

from pathlib import Path
import re
import sys


def parse_phase(path: Path) -> str:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    if not lines:
        return ""
    if lines[0].strip() == "---":
        scan = []
        for line in lines[1:120]:
            if line.strip() == "---":
                break
            scan.append(line)
    else:
        scan = []
        for line in lines[:80]:
            if line.lstrip().startswith("#"):
                break
            scan.append(line)
    for line in scan:
        match = re.match(r"^\s*phase\s*:\s*['\"]?([A-Za-z_-]+)['\"]?\s*$", line)
        if match:
            return match.group(1).strip().lower()
    return ""


work_dir = Path(sys.argv[1]).expanduser()
for isa in sorted(work_dir.glob("**/ISA.md")):
    if parse_phase(isa) in {"complete", "learn"}:
        sys.stdout.buffer.write(str(isa).encode("utf-8") + b"\0")
PY
  )
}

TMP_INPUT="$(mktemp "${TMPDIR:-/tmp}/pai-codex-stop.XXXXXX")"
trap 'command rm "$TMP_INPUT" 2>/dev/null || true' EXIT
cat > "$TMP_INPUT"

run_stop_learning || true

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
