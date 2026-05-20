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

TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/pai-codex-learning.XXXXXX")"
cleanup() {
  find "$TMP_ROOT" -depth -type f -delete 2>/dev/null || true
  find "$TMP_ROOT" -depth -type d -empty -delete 2>/dev/null || true
}
trap cleanup EXIT

json_ok() {
  python3 -m json.tool >/dev/null
}

make_home() {
  local name="$1"
  local home_dir="$TMP_ROOT/$name"
  mkdir -p "$home_dir/.claude/PAI/MEMORY/WORK" "$home_dir/.claude/PAI/MEMORY/OBSERVABILITY"
  printf '%s\n' "$home_dir"
}

write_isa() {
  local home_dir="$1"
  local slug="$2"
  local phase="$3"
  local body="$4"
  local dir="$home_dir/.claude/PAI/MEMORY/WORK/$slug"
  mkdir -p "$dir"
  cat > "$dir/ISA.md" <<EOF
---
task: Test learning
slug: $slug
effort: E1
phase: $phase
progress: 1
mode: ALGORITHM
started: 2026-05-20T00:00:00Z
updated: 2026-05-20T00:00:00Z
---

## Goal

Test Stop-gated learning.

## Criteria

- [x] ISC-1: The learning helper writes only explicit learning content.

## Changelog

$body

## Verification

- ISC-1: test fixture evidence.
EOF
}

stop_payload='{"hook_event_name":"Stop","turn_id":"learning-stop","last_assistant_message":"done"}'

learning_file() {
  local home_dir="$1"
  find "$home_dir/.claude/PAI/MEMORY/LEARNING/ALGORITHM" -name session.jsonl -type f -print -quit 2>/dev/null || true
}

learning_count() {
  local file="$1"
  if [[ -n "$file" && -f "$file" ]]; then
    wc -l < "$file" | tr -d ' '
  else
    printf '0'
  fi
}

disabled_home="$(make_home disabled)"
write_isa "$disabled_home" disabled-isa complete "- learned: Disabled learning should not write."
printf '%s\n' "$stop_payload" |
  HOME="$disabled_home" "$PKG_DIR/hooks/stop.sh" |
  json_ok
[[ -z "$(learning_file "$disabled_home")" ]] || { echo "learning file written while disabled" >&2; exit 1; }

incomplete_home="$(make_home incomplete)"
write_isa "$incomplete_home" incomplete-isa verify "- learned: Incomplete ISA should not write."
printf '%s\n' "$stop_payload" |
  HOME="$incomplete_home" PAI_CODEX_LEARNING_ENABLED=1 "$PKG_DIR/hooks/stop.sh" |
  json_ok
[[ -z "$(learning_file "$incomplete_home")" ]] || { echo "learning file written for non-complete ISA" >&2; exit 1; }

complete_home="$(make_home complete)"
write_isa "$complete_home" complete-isa complete "- learned: Explicit Changelog learning is captured."
printf '%s\n' "$stop_payload" |
  HOME="$complete_home" PAI_CODEX_LEARNING_ENABLED=1 "$PKG_DIR/hooks/stop.sh" |
  json_ok
complete_file="$(learning_file "$complete_home")"
test -f "$complete_file"
[[ "$(learning_count "$complete_file")" == "1" ]] || { echo "expected one learning record" >&2; exit 1; }
python3 - "$complete_file" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import sys

record = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()[0])
assert record["source"] == "codex_stop_learning", record
assert record["isa_slug"] == "complete-isa", record
assert record["phase"] == "complete", record
assert record["entries"], record
assert record["content_hash"], record
PY

printf '%s\n' "$stop_payload" |
  HOME="$complete_home" PAI_CODEX_LEARNING_ENABLED=1 "$PKG_DIR/hooks/stop.sh" |
  json_ok
[[ "$(learning_count "$complete_file")" == "1" ]] || { echo "learning record duplicated" >&2; exit 1; }

write_isa "$complete_home" secret-isa learn "- learned: secret marker password=supersecretvalue must be redacted."
printf '%s\n' "$stop_payload" |
  HOME="$complete_home" PAI_CODEX_LEARNING_ENABLED=1 "$PKG_DIR/hooks/stop.sh" |
  json_ok
[[ "$(learning_count "$complete_file")" == "2" ]] || { echo "expected second learning record" >&2; exit 1; }
! rg -q 'supersecretvalue' "$complete_file"
rg -q 'REDACTED' "$complete_file"

fallback_home="$(make_home fallback)"
mkdir -p "$fallback_home/bin"
for name in bash dirname mkdir; do
  ln -s "$(command -v "$name")" "$fallback_home/bin/$name"
done
printf '%s\n' "$stop_payload" |
  HOME="$fallback_home" PATH="$fallback_home/bin" PAI_CODEX_LEARNING_ENABLED=1 "$PKG_DIR/hooks/stop.sh" |
  json_ok
[[ -z "$(learning_file "$fallback_home")" ]] || { echo "learning file written without python3" >&2; exit 1; }

echo "learning runtime test passed"
