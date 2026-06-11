#!/usr/bin/env bash
# PAI Codex PreCompact hook: snapshot observability before context compaction.
# This hook must NEVER block compaction: every step is best-effort and the
# hook always exits 0 without emitting a continue/decision field.
set -uo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAI_DIR="${PAI_DIR:-$HOME/.claude/PAI}"
OBS_DIR="$PAI_DIR/MEMORY/OBSERVABILITY"
mkdir -p "$OBS_DIR" 2>/dev/null || true
export PYTHONPATH="$HOOK_DIR/lib${PYTHONPATH:+:$PYTHONPATH}"

PAYLOAD="$(cat 2>/dev/null || true)"

if command -v python3 >/dev/null 2>&1; then
  printf '%s' "$PAYLOAD" | python3 - "$OBS_DIR/codex-precompact.jsonl" "$PAI_DIR" <<'PY' 2>/dev/null || true
import json, sys
from datetime import datetime, timezone
from pathlib import Path

log_path = Path(sys.argv[1])
pai_dir = Path(sys.argv[2])
raw = sys.stdin.read()
try:
    payload = json.loads(raw) if raw.strip() else {}
except Exception:
    payload = {"parse_error": True}

work_dir = pai_dir / "MEMORY" / "WORK"
active = []
try:
    if work_dir.is_dir():
        for isa in sorted(work_dir.glob("*/ISA.md")):
            head = isa.read_text(encoding="utf-8", errors="replace")[:600]
            phase = ""
            for line in head.splitlines():
                if line.startswith("phase:"):
                    phase = line.split(":", 1)[1].strip()
                    break
            if phase and phase not in {"complete"}:
                active.append({"isa": str(isa), "phase": phase})
            if len(active) >= 10:
                break
except Exception:
    pass

record = {
    "ts": datetime.now(timezone.utc).isoformat(),
    "event": "PreCompact",
    "session_id": str(payload.get("session_id", payload.get("sessionId", "")))[:64],
    "trigger": str(payload.get("trigger", ""))[:32],
    "active_isas": active,
}
log_path.parent.mkdir(parents=True, exist_ok=True)
with log_path.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(record) + "\n")
PY
fi

# Never block compaction: no decision payload, always success.
printf '%s\n' '{}'
exit 0
