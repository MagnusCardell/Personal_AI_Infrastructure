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

TMP_HOME="$(mktemp -d "${TMPDIR:-/tmp}/pai-codex-checkpoint.XXXXXX")"
cleanup() {
  find "$TMP_HOME" -depth -type f -delete 2>/dev/null || true
  find "$TMP_HOME" -depth -type d -empty -delete 2>/dev/null || true
}
trap cleanup EXIT

PAI_DIR="$TMP_HOME/.claude/PAI"
WORK_DIR="$PAI_DIR/MEMORY/WORK"
OBS_DIR="$PAI_DIR/MEMORY/OBSERVABILITY"
mkdir -p "$WORK_DIR/checkpoint-test" "$WORK_DIR/dirty-test" "$WORK_DIR/malformed-test" "$OBS_DIR"

write_isa() {
  local path="$1"
  local slug="$2"
  local checked="$3"
  local mark=" "
  [[ "$checked" == "yes" ]] && mark="x"
  cat > "$path" <<EOF
---
task: Checkpoint test
slug: $slug
effort: E1
phase: verify
progress: 0.5
mode: ALGORITHM
started: 2026-05-20T00:00:00Z
updated: 2026-05-20T00:00:00Z
---

## Goal

Test opt-in checkpointing.

## Criteria

- [$mark] ISC-1: Checkpoint this criterion.

## Verification

- ISC-1: test fixture evidence.
EOF
}

json_ok() {
  python3 -m json.tool >/dev/null
}

post_payload() {
  local isa_path="$1"
  cat <<EOF
{
  "tool_name": "apply_patch",
  "cwd": "$TMP_HOME",
  "tool_input": {
    "command": "*** Begin Patch\\n*** Update File: $isa_path\\n@@\\n ## Criteria\\n\\n - [ ] ISC-1: Checkpoint this criterion.\\n*** End Patch\\n"
  }
}
EOF
}

run_post() {
  local isa_path="$1"
  post_payload "$isa_path" | HOME="$TMP_HOME" PAI_CODEX_CHECKPOINT_ENABLED="${2:-1}" "$PKG_DIR/hooks/post-tool-use.sh"
}

commit_count() {
  git -C "$TMP_HOME/.claude" rev-list --count HEAD
}

isa="$WORK_DIR/checkpoint-test/ISA.md"
dirty_isa="$WORK_DIR/dirty-test/ISA.md"
malformed_isa="$WORK_DIR/malformed-test/ISA.md"
write_isa "$isa" checkpoint-test no
write_isa "$dirty_isa" dirty-test no
printf '# malformed\n' > "$malformed_isa"

git -C "$TMP_HOME/.claude" init >/dev/null
git -C "$TMP_HOME/.claude" config user.email "test@example.invalid"
git -C "$TMP_HOME/.claude" config user.name "Test Runner"
git -C "$TMP_HOME/.claude" add PAI/MEMORY/WORK
git -C "$TMP_HOME/.claude" commit -m "initial test state" >/dev/null

before="$(commit_count)"
run_post "$isa" 0 | json_ok
[[ "$(commit_count)" == "$before" ]] || { echo "disabled checkpoint created commit" >&2; exit 1; }
test ! -e "$OBS_DIR/codex-isa-state.json"

run_post "$isa" 1 | json_ok
[[ "$(commit_count)" == "$before" ]] || { echo "no-transition checkpoint created commit" >&2; exit 1; }
test -f "$OBS_DIR/codex-isa-state.json"

write_isa "$isa" checkpoint-test yes
run_post "$isa" 1 | json_ok
after_transition="$(commit_count)"
[[ "$after_transition" == "$((before + 1))" ]] || { echo "transition checkpoint did not create exactly one commit" >&2; exit 1; }
git -C "$TMP_HOME/.claude" log -1 --format=%s | rg -q 'ISC checkpoint: checkpoint-test'
rg -q '"status": "committed"' "$OBS_DIR/codex-checkpoint.jsonl"
rg -q '"ISC-1"' "$OBS_DIR/codex-checkpoint.jsonl"

run_post "$isa" 1 | json_ok
[[ "$(commit_count)" == "$after_transition" ]] || { echo "idempotent checkpoint duplicated commit" >&2; exit 1; }

run_post "$dirty_isa" 1 | json_ok
write_isa "$dirty_isa" dirty-test yes
printf 'local dirt\n' > "$TMP_HOME/.claude/unrelated.txt"
dirty_before="$(commit_count)"
run_post "$dirty_isa" 1 | json_ok
[[ "$(commit_count)" == "$dirty_before" ]] || { echo "dirty repo checkpoint created commit" >&2; exit 1; }
rg -q 'unrelated dirty paths' "$OBS_DIR/codex-checkpoint.jsonl"

run_post "$malformed_isa" 1 | json_ok
rg -q 'no ISC checkbox state found' "$OBS_DIR/codex-checkpoint.jsonl"

echo "checkpoint runtime test passed"
