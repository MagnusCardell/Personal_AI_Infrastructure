#!/usr/bin/env bash
set -euo pipefail

SCRIPT_SOURCE="${BASH_SOURCE[0]}"
while [[ -L "$SCRIPT_SOURCE" ]]; do
  SCRIPT_DIR_LINK="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
  SCRIPT_SOURCE="$(readlink "$SCRIPT_SOURCE")"
  [[ "$SCRIPT_SOURCE" != /* ]] && SCRIPT_SOURCE="$SCRIPT_DIR_LINK/$SCRIPT_SOURCE"
done
TEST_DIR="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
PKG_DIR="$(cd "$TEST_DIR/.." && pwd)"

TMP_HOME="$(mktemp -d "${TMPDIR:-/tmp}/pai-codex-pulse.XXXXXX")"
SERVER_PID=""
cleanup() {
  if [[ -n "$SERVER_PID" ]]; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
  find "$TMP_HOME" -depth -type f -delete 2>/dev/null || true
  find "$TMP_HOME" -depth -type d -empty -delete 2>/dev/null || true
}
trap cleanup EXIT

mkdir -p "$TMP_HOME/.claude/PAI/MEMORY/WORK/pulse-test" \
  "$TMP_HOME/.claude/PAI/MEMORY/OBSERVABILITY" \
  "$TMP_HOME/.claude/hooks" \
  "$TMP_HOME/bin"

server_py="$TMP_HOME/server.py"
port_file="$TMP_HOME/server-port"
received_file="$TMP_HOME/received.jsonl"

cat > "$server_py" <<'PY'
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
import sys

port_file = Path(sys.argv[1])
received_file = Path(sys.argv[2])


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8", errors="replace")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"raw": body}
        payload["_path"] = self.path
        with received_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, sort_keys=True) + "\n")
        self.send_response(204)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        return


server = HTTPServer(("127.0.0.1", 0), Handler)
port_file.write_text(str(server.server_port), encoding="utf-8")
server.serve_forever()
PY

python3 "$server_py" "$port_file" "$received_file" &
SERVER_PID="$!"

for _ in $(seq 1 50); do
  [[ -s "$port_file" ]] && break
  sleep 0.1
done
test -s "$port_file"
server_url="http://127.0.0.1:$(cat "$port_file")"

json_ok() {
  python3 -m json.tool >/dev/null
}

event_count() {
  if [[ -f "$received_file" ]]; then
    wc -l < "$received_file" | tr -d ' '
  else
    printf '0'
  fi
}

wait_for_count() {
  local expected="$1"
  for _ in $(seq 1 50); do
    [[ "$(event_count)" -ge "$expected" ]] && return 0
    sleep 0.1
  done
  echo "timed out waiting for Pulse events: expected $expected got $(event_count)" >&2
  return 1
}

stop_payload='{"hook_event_name":"Stop","turn_id":"pulse-stop","last_assistant_message":"done"}'

printf '%s\n' "$stop_payload" |
  PAI_DIR="" HOME="$TMP_HOME" PAI_CODEX_PULSE_ENABLED=0 PAI_CODEX_PULSE_URL="$server_url" "$PKG_DIR/hooks/stop.sh" |
  json_ok

[[ "$(event_count)" == "0" ]] || {
  echo "Pulse disabled still sent a network notification" >&2
  exit 1
}

printf '%s\n' "$stop_payload" |
  PAI_DIR="" HOME="$TMP_HOME" PAI_CODEX_PULSE_ENABLED=1 PAI_CODEX_PULSE_URL="http://127.0.0.1:1" "$PKG_DIR/hooks/stop.sh" |
  json_ok

printf '%s\n' "$stop_payload" |
  PAI_DIR="" HOME="$TMP_HOME" PAI_CODEX_PULSE_ENABLED=1 PAI_CODEX_PULSE_URL="$server_url" "$PKG_DIR/hooks/stop.sh" |
  json_ok

wait_for_count 1

python3 - "$received_file" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import sys

payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()[0])
assert payload["_path"] == "/notify", payload
assert payload["source"] == "pai-codex", payload
assert payload["event"] == "codex.turn.complete", payload
assert payload["message"], payload
assert payload["timestamp"], payload
assert "voice" not in payload, payload
PY

cat > "$TMP_HOME/.claude/PAI/MEMORY/WORK/pulse-test/ISA.md" <<'EOF'
---
task: Pulse test ISA
slug: pulse-test
effort: E1
phase: verify
progress: 0.5
mode: ALGORITHM
started: 2026-05-20T00:00:00Z
updated: 2026-05-20T00:00:00Z
---

## Goal

Test optional Pulse notification.

## Criteria

- [ ] ISC-1: PostToolUse detects this ISA path.
EOF

cat > "$TMP_HOME/bin/bun" <<'EOF'
#!/usr/bin/env bash
cat >/dev/null || true
exit 0
EOF
chmod +x "$TMP_HOME/bin/bun"
printf '%s\n' '// fake ISASync hook' > "$TMP_HOME/.claude/hooks/ISASync.hook.ts"

isa_path="$TMP_HOME/.claude/PAI/MEMORY/WORK/pulse-test/ISA.md"
post_payload="$TMP_HOME/posttool.json"
cat > "$post_payload" <<EOF
{
  "tool_name": "apply_patch",
  "cwd": "$TMP_HOME",
  "tool_input": {
    "command": "*** Begin Patch\\n*** Update File: $isa_path\\n@@\\n ## Criteria\\n\\n - [ ] ISC-1: PostToolUse detects this ISA path.\\n*** End Patch\\n"
  }
}
EOF

PAI_DIR="" HOME="$TMP_HOME" PATH="$TMP_HOME/bin:$PATH" PAI_CODEX_PULSE_ENABLED=1 PAI_CODEX_PULSE_URL="$server_url" \
  "$PKG_DIR/hooks/post-tool-use.sh" < "$post_payload" | json_ok

wait_for_count 2

python3 - "$received_file" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import sys

entries = [json.loads(line) for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()]
isa = entries[-1]
assert isa["_path"] == "/notify", isa
assert isa["source"] == "pai-codex", isa
assert isa["event"] == "codex.algorithm.isa_updated", isa
assert isa["message"], isa
assert isa["timestamp"], isa
assert "voice" not in isa, isa
assert isa["details"]["isa_slug"] == "pulse-test", isa
PY

echo "Pulse runtime test passed"
