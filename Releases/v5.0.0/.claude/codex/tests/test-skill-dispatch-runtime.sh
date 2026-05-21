#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="${BASH_SOURCE[0]%/*}"
case "$SCRIPT_DIR" in
  /*) ;;
  *) SCRIPT_DIR="$PWD/$SCRIPT_DIR" ;;
esac
PKG_DIR="${SCRIPT_DIR%/tests}"
DISPATCH="$PKG_DIR/hooks/skills/dispatch.sh"

TMP_HOME="${TMPDIR:-/tmp}/pai-codex-skill-dispatch-${BASHPID:-$$}"
cleanup() {
  find "$TMP_HOME" -depth -type f -delete 2>/dev/null || true
  find "$TMP_HOME" -depth -type l -delete 2>/dev/null || true
  find "$TMP_HOME" -depth -type d -empty -delete 2>/dev/null || true
}
trap cleanup EXIT

mkdir -p "$TMP_HOME"

PAI_DIR="$TMP_HOME/.claude/PAI"
WORK_DIR="$PAI_DIR/MEMORY/WORK"
SKILL_LOG="$PAI_DIR/MEMORY/SKILLS/codex-execution.jsonl"
OUT="$TMP_HOME/out.txt"

mkdir -p "$WORK_DIR/skill-test" "$WORK_DIR/missing-section" "$WORK_DIR/not-isa" "$WORK_DIR/link-test" "$TMP_HOME/outside"

ISA="$WORK_DIR/skill-test/ISA.md"
MISSING_ISA="$WORK_DIR/missing-section/ISA.md"
OUTSIDE_ISA="$TMP_HOME/outside/ISA.md"
NOTE_PATH="$WORK_DIR/not-isa/NOTE.md"
LINK_ISA="$WORK_DIR/link-test/ISA.md"

cat > "$ISA" <<'EOF'
---
phase: build
---

## Goal

Test skill dispatch.

## Decisions

- Existing decision.

## Changelog

- Existing change.

## Verification

- Existing verification.
EOF

cat > "$MISSING_ISA" <<'EOF'
---
phase: build
---

## Goal

Test missing section creation.
EOF

printf '# Outside ISA\n' > "$OUTSIDE_ISA"
printf '# Note\n' > "$NOTE_PATH"
ln -s "$OUTSIDE_ISA" "$LINK_ISA"

json_ok() {
  python3 -m json.tool >/dev/null
}

assert_json_empty_file() {
  python3 - "$1" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert payload == {}, payload
PY
}

assert_section_contains() {
  local file="$1"
  local heading="$2"
  local expected="$3"
  python3 - "$file" "$heading" "$expected" <<'PY'
from __future__ import annotations

from pathlib import Path
import sys

path = Path(sys.argv[1])
heading = sys.argv[2]
expected = sys.argv[3]
lines = path.read_text(encoding="utf-8").splitlines()
try:
    start = lines.index(heading)
except ValueError as exc:
    raise SystemExit(f"missing heading: {heading}") from exc
end = len(lines)
for index in range(start + 1, len(lines)):
    if lines[index].startswith("## "):
        end = index
        break
section = "\n".join(lines[start:end])
if expected not in section:
    raise SystemExit(f"missing expected content under {heading}: {expected}")
PY
}

run_append() {
  HOME="$TMP_HOME" PAI_DIR="$PAI_DIR" "$DISPATCH" isa_append "$@"
}

if "$DISPATCH" > "$OUT" 2>&1; then
  echo "dispatch without args unexpectedly succeeded" >&2
  exit 1
fi
rg -q 'usage: dispatch\.sh' "$OUT"

if "$DISPATCH" unknown_skill > "$OUT" 2>&1; then
  echo "unknown skill unexpectedly succeeded" >&2
  exit 1
fi
rg -q 'Available skills:' "$OUT"
rg -q 'isa_append' "$OUT"

run_append "$ISA" decisions "- D1: selected explicit dispatch." > "$OUT"
json_ok < "$OUT"
assert_section_contains "$ISA" "## Decisions" "- D1: selected explicit dispatch."

run_append "$ISA" changelog "- Added ISA append dispatch test." > "$OUT"
json_ok < "$OUT"
assert_section_contains "$ISA" "## Changelog" "- Added ISA append dispatch test."

run_append "$ISA" verification "- Verified ISA append output." > "$OUT"
json_ok < "$OUT"
assert_section_contains "$ISA" "## Verification" "- Verified ISA append output."

run_append "$MISSING_ISA" verification "- Created missing verification section." > "$OUT"
json_ok < "$OUT"
assert_section_contains "$MISSING_ISA" "## Verification" "- Created missing verification section."

if run_append "$OUTSIDE_ISA" decisions "- should fail" > "$OUT" 2>&1; then
  echo "outside path unexpectedly succeeded" >&2
  exit 1
fi
rg -q 'MEMORY/WORK' "$OUT"

if run_append "$NOTE_PATH" decisions "- should fail" > "$OUT" 2>&1; then
  echo "non-ISA path unexpectedly succeeded" >&2
  exit 1
fi
rg -q 'ISA\.md' "$OUT"

if run_append "$LINK_ISA" decisions "- should fail" > "$OUT" 2>&1; then
  echo "symlink escape unexpectedly succeeded" >&2
  exit 1
fi
rg -q 'MEMORY/WORK' "$OUT"

if run_append "$ISA" decisions "   " > "$OUT" 2>&1; then
  echo "empty content unexpectedly succeeded" >&2
  exit 1
fi
rg -q 'content must not be empty' "$OUT"

run_append "$ISA" changelog "- password=supersecretvalue" > "$OUT"
json_ok < "$OUT"
rg -q '\[REDACTED:generic_secret_kv\]' "$ISA"
! rg -q 'supersecretvalue' "$ISA"

test -s "$SKILL_LOG"
rg -q '"content_hash"' "$SKILL_LOG"
rg -q '"source": "codex_skill_dispatch"' "$SKILL_LOG"
! rg -q 'supersecretvalue' "$SKILL_LOG"

test ! -e "$PAI_DIR/MEMORY/OBSERVABILITY/codex-isa-state.json"
test ! -e "$PAI_DIR/MEMORY/OBSERVABILITY/codex-checkpoint.jsonl"

security_payload='{"tool_name":"Bash","cwd":"'"$TMP_HOME"'","tool_input":{"command":"printf safe"}}'
printf '%s\n' "$security_payload" | HOME="$TMP_HOME" "$PKG_DIR/hooks/pre-tool-use.sh" > "$OUT"
json_ok < "$OUT"
assert_json_empty_file "$OUT"

checkpoint_payload='{"tool_name":"apply_patch","cwd":"'"$TMP_HOME"'","tool_input":{"command":"*** Begin Patch\n*** End Patch\n"}}'
printf '%s\n' "$checkpoint_payload" | HOME="$TMP_HOME" PAI_CODEX_CHECKPOINT_ENABLED=0 "$PKG_DIR/hooks/post-tool-use.sh" > "$OUT"
json_ok < "$OUT"
assert_json_empty_file "$OUT"

echo "skill dispatch runtime test passed"
