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
from pai_context import load_pai_context

input_path = Path(sys.argv[1])
log_path = Path(sys.argv[3]).expanduser()


try:
    payload = load_json_file(input_path)
    ctx = load_pai_context()

    context = "\n".join(
        [
            f"PAI_RUNTIME_CONTEXT={ctx['status']}",
            f"PAI_DIR={ctx['pai_dir']}",
            "PAI_MODE_DEFAULT=NATIVE for identity, project, Telos, and status questions",
            "PAI_ALGORITHM_MODE=Use ALGORITHM for execution-oriented work and live ISA updates",
            f"PAI_ALGORITHM_POINTER={ctx['algorithm_pointer']}",
            f"PAI_ALGORITHM_FILE={ctx['algorithm_path']}",
            f"PAI_CONTEXT_MISSING={'; '.join(ctx['missing_files']) if ctx['missing_files'] else 'none'}",
            "",
            "PAI_PRINCIPAL_CONTEXT=",
            f"Source: {ctx['principal_path']}",
            ctx["principal_summary"],
            "",
            "PAI_DA_CONTEXT=",
            f"Source: {ctx['da_path']}",
            ctx["da_summary"],
            "",
            "PAI_ACTIVE_PROJECTS_CONTEXT=",
            f"Source: {ctx['projects_path']}",
            ctx["projects_summary"],
            "",
            "PAI_TELOS_CONTEXT=",
            f"Source: {ctx['telos_path']}",
            ctx["telos_summary"],
            "",
            "PAI_ALGORITHM_CONTEXT=",
            ctx["algorithm_summary"],
        ]
    )

    append_jsonl(
        log_path,
        {
            "timestamp": now(),
            "hook_event_name": "SessionStart",
            "cwd": payload.get("cwd") or os.getcwd(),
            "turn_id": payload.get("turn_id") or payload.get("turnId"),
            "runtime_context": ctx["status"],
            "missing_files": ctx["missing_files"],
            "algorithm_pointer": ctx["algorithm_pointer"],
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
