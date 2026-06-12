#!/usr/bin/env bash
# Codex skill: fabric — thin wrapper over the locally installed fabric CLI.
# usage: fabric.sh PATTERN [extra fabric args...]   (input on stdin)
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAI_DIR="${PAI_DIR:-$HOME/.claude/PAI}"

log_event() {
  local status="$1"
  local pattern="${2:-}"
  python3 - "$PAI_DIR" "$status" "$pattern" <<'PY' 2>/dev/null || true
import json, sys
from datetime import datetime, timezone
from pathlib import Path

root, status, pattern = sys.argv[1], sys.argv[2], sys.argv[3]
log_path = Path(root) / "MEMORY" / "SKILLS" / "codex-execution.jsonl"
log_path.parent.mkdir(parents=True, exist_ok=True)
record = {
    "ts": datetime.now(timezone.utc).isoformat(),
    "skill": "fabric",
    "pattern": pattern[:64],
    "status": status,
}
with log_path.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(record) + "\n")
PY
}

if [[ $# -lt 1 ]]; then
  echo "usage: fabric.sh PATTERN [extra fabric args...] (input on stdin)" >&2
  exit 2
fi

PATTERN="$1"
shift

if ! command -v fabric >/dev/null 2>&1; then
  log_event "unavailable" "$PATTERN"
  echo "PAI_CODEX_FABRIC_UNAVAILABLE: fabric binary not found on PATH." >&2
  echo "Install fabric (github.com/danielmiessler/fabric) to enable this skill." >&2
  exit 3
fi

TIMEOUT_SECS="${PAI_CODEX_FABRIC_TIMEOUT:-120}"
if timeout "$TIMEOUT_SECS" fabric --pattern "$PATTERN" "$@"; then
  log_event "ok" "$PATTERN"
else
  status=$?
  log_event "error" "$PATTERN"
  echo "PAI_CODEX_FABRIC_FAILED: fabric exited $status for pattern $PATTERN" >&2
  exit "$status"
fi
