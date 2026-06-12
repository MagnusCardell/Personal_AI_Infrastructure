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

TMP_HOME="$(mktemp -d "${TMPDIR:-/tmp}/pai-codex-voice.XXXXXX")"
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

mkdir -p "$TMP_HOME/.claude/PAI/MEMORY/WORK/voice-test" \
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
  echo "timed out waiting for voice test events: expected $expected got $(event_count)" >&2
  return 1
}

stop_payload='{"hook_event_name":"Stop","turn_id":"voice-stop","last_assistant_message":"done"}'

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
assert payload["event"] == "codex.turn.complete", payload
assert payload["voice_enabled"] is False, payload
assert "voice_id" not in payload, payload
assert "voice" not in payload, payload
PY

summary_payload="$(
  python3 - <<'PY'
from __future__ import annotations

import json

print(json.dumps({
    "hook_event_name": "Stop",
    "turn_id": "voice-summary",
    "last_assistant_message": (
        "PAI_MODE=ALGORITHM\n"
        "PAI_TIER=E3\n\n"
        "Implemented dynamic Codex voice summaries for turn completion.\n\n"
        "VERIFY\n"
        "The voice runtime test passed."
    ),
}))
PY
)"

printf '%s\n' "$summary_payload" |
  PAI_DIR="" HOME="$TMP_HOME" \
  PAI_CODEX_PULSE_ENABLED=1 \
  PAI_CODEX_PULSE_URL="$server_url" \
  PAI_CODEX_VOICE_ENABLED=1 \
  PAI_CODEX_VOICE_EVENTS=turn_complete \
  PAI_CODEX_VOICE_MESSAGE_TURN_COMPLETE="Codex turn finished." \
  "$PKG_DIR/hooks/stop.sh" |
  json_ok

wait_for_count 2

python3 - "$received_file" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import sys

entries = [json.loads(line) for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()]
payload = entries[1]
assert payload["event"] == "codex.turn.complete", payload
assert payload["voice_enabled"] is True, payload
assert payload["message"] == "Implemented dynamic Codex voice summaries for turn completion.", payload
assert payload["details"]["voice_message_source"] == "first_sentence", payload
assert payload["details"]["voice_message_length"] == len(payload["message"]), payload
PY

printf '%s\n' "$stop_payload" |
  PAI_DIR="" HOME="$TMP_HOME" \
  PAI_CODEX_PULSE_ENABLED=1 \
  PAI_CODEX_PULSE_URL="$server_url" \
  PAI_CODEX_VOICE_ENABLED=1 \
  PAI_CODEX_VOICE_EVENTS=turn_complete \
  PAI_CODEX_VOICE_MESSAGE_TURN_COMPLETE="Codex turn finished." \
  "$PKG_DIR/hooks/stop.sh" |
  json_ok

wait_for_count 3

python3 - "$received_file" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import sys

entries = [json.loads(line) for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()]
payload = entries[2]
assert payload["event"] == "codex.turn.complete", payload
assert payload["voice_enabled"] is True, payload
assert payload["message"] == "Codex turn finished.", payload
assert "voice_id" not in payload, payload
assert "voice" not in payload, payload
PY

printf '%s\n' "$stop_payload" |
  PAI_DIR="" HOME="$TMP_HOME" \
  PAI_CODEX_PULSE_ENABLED=1 \
  PAI_CODEX_PULSE_URL="$server_url" \
  PAI_CODEX_VOICE_ENABLED=1 \
  PAI_CODEX_VOICE_EVENTS=turn_complete \
  PAI_CODEX_VOICE_ID=voice_test_id_123 \
  "$PKG_DIR/hooks/stop.sh" |
  json_ok

wait_for_count 4

python3 - "$received_file" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import sys

entries = [json.loads(line) for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()]
payload = entries[3]
assert payload["voice_enabled"] is True, payload
assert payload["voice_id"] == "voice_test_id_123", payload
PY

cat > "$TMP_HOME/.claude/PAI/MEMORY/WORK/voice-test/ISA.md" <<'EOF'
---
task: Voice test ISA
slug: voice-test
effort: E1
phase: verify
progress: 0.5
mode: ALGORITHM
started: 2026-05-20T00:00:00Z
updated: 2026-05-20T00:00:00Z
---

## Goal

Test optional voice intent.

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

isa_path="$TMP_HOME/.claude/PAI/MEMORY/WORK/voice-test/ISA.md"
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

PAI_DIR="" HOME="$TMP_HOME" PATH="$TMP_HOME/bin:$PATH" \
  PAI_CODEX_PULSE_ENABLED=1 \
  PAI_CODEX_PULSE_URL="$server_url" \
  PAI_CODEX_VOICE_ENABLED=1 \
  PAI_CODEX_VOICE_EVENTS=algorithm_isa_updated \
  PAI_CODEX_VOICE_MESSAGE_ISA_UPDATED="Codex updated the ISA." \
  "$PKG_DIR/hooks/post-tool-use.sh" < "$post_payload" |
  json_ok

wait_for_count 5

python3 - "$received_file" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import sys

entries = [json.loads(line) for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()]
payload = entries[4]
assert payload["event"] == "codex.algorithm.isa_updated", payload
assert payload["voice_enabled"] is True, payload
assert payload["message"] == "Codex updated the ISA.", payload
assert payload["details"]["isa_slug"] == "voice-test", payload
assert "voice_id" not in payload, payload
PY

printf '%s\n' "$stop_payload" |
  PAI_DIR="" HOME="$TMP_HOME" \
  PAI_CODEX_PULSE_ENABLED=1 \
  PAI_CODEX_PULSE_URL="http://127.0.0.1:1" \
  PAI_CODEX_VOICE_ENABLED=1 \
  "$PKG_DIR/hooks/stop.sh" |
  json_ok

PAI_DIR="" HOME="$TMP_HOME" PATH="$TMP_HOME/bin:$PATH" \
  PAI_CODEX_PULSE_ENABLED=1 \
  PAI_CODEX_PULSE_URL="http://127.0.0.1:1" \
  PAI_CODEX_VOICE_ENABLED=1 \
  PAI_CODEX_VOICE_EVENTS=algorithm_isa_updated \
  "$PKG_DIR/hooks/post-tool-use.sh" < "$post_payload" |
  json_ok

secret_value="s""k-testsecretvalue000000000000000000"
printf '%s\n' '{"hook_event_name":"Stop","turn_id":"voice-secret","last_assistant_message":"password=do-not-say"}' |
  PAI_DIR="" HOME="$TMP_HOME" \
  PAI_CODEX_PULSE_ENABLED=1 \
  PAI_CODEX_PULSE_URL="$server_url" \
  PAI_CODEX_VOICE_ENABLED=1 \
  PAI_CODEX_VOICE_EVENTS=turn_complete \
  PAI_CODEX_VOICE_MESSAGE_TURN_COMPLETE="Do not speak $secret_value" \
  "$PKG_DIR/hooks/stop.sh" |
  json_ok

wait_for_count 6
! rg -q --fixed-strings "$secret_value" "$received_file"
! rg -q --fixed-strings "$secret_value" "$TMP_HOME/.claude/PAI/MEMORY/OBSERVABILITY"

cword="curl"
vword="voice"
tword="tts"
oword="openai"
aword="audio"
for pattern in "eleven""labs" "api.eleven""labs" "text-to-""speech" "speech-to-""text" "${oword}.${aword}" "${cword}.*${vword}" "${cword}.*${tword}"; do
  if rg -n -i "$pattern" "$PKG_DIR" >/dev/null 2>&1; then
    echo "direct provider invocation pattern found: $pattern" >&2
    exit 1
  fi
done

echo "Voice runtime test passed"
