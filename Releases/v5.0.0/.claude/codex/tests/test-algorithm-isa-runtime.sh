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
VALIDATOR="$PKG_DIR/skills/pai-isa/scripts/validate-isa.sh"

TMP_HOME="$(mktemp -d "${TMPDIR:-/tmp}/pai-codex-algorithm-isa.XXXXXX")"
cleanup() {
  find "$TMP_HOME" -depth -type f -delete 2>/dev/null || true
  find "$TMP_HOME" -depth -type d -empty -delete 2>/dev/null || true
}
trap cleanup EXIT

mkdir -p "$TMP_HOME/.claude/PAI/MEMORY/WORK/test-isa" \
  "$TMP_HOME/.claude/PAI/MEMORY/OBSERVABILITY" \
  "$TMP_HOME/.claude/PAI/MEMORY/LEARNING"

valid_isa="$TMP_HOME/.claude/PAI/MEMORY/WORK/test-isa/ISA.md"
cat > "$valid_isa" <<'EOF'
---
task: Test ISA
slug: test-isa
effort: E1
phase: verify
progress: 0.5
mode: ALGORITHM
started: 2026-05-20T00:00:00Z
updated: 2026-05-20T00:00:00Z
---

## Goal

Create a minimal valid ISA.

## Criteria

- [ ] ISC-1: Validates with the bundled validator.
EOF

PAI_DIR="" HOME="$TMP_HOME" "$VALIDATOR" "$valid_isa" >/dev/null

bad_isa="$TMP_HOME/.claude/PAI/MEMORY/WORK/test-isa/BAD.md"
cat > "$bad_isa" <<'EOF'
# Missing canonical ISA shape
EOF

if PAI_DIR="" HOME="$TMP_HOME" "$VALIDATOR" "$bad_isa" >/dev/null 2>&1; then
  echo "malformed ISA unexpectedly passed validation" >&2
  exit 1
fi

rg -q 'validate-isa.sh' "$PKG_DIR/AGENTS.md.template"
rg -q 'frontmatter delimiter' "$PKG_DIR/AGENTS.md.template"
rg -q '## Goal' "$PKG_DIR/AGENTS.md.template"
rg -q '## Criteria' "$PKG_DIR/AGENTS.md.template"
rg -q '## Verification' "$PKG_DIR/AGENTS.md.template"

patch_payload="$TMP_HOME/apply-patch-payload.json"
cat > "$patch_payload" <<EOF
{
  "tool_name": "apply_patch",
  "cwd": "$TMP_HOME",
  "tool_input": {
    "command": "*** Begin Patch\\n*** Update File: $valid_isa\\n@@\\n ## Criteria\\n\\n - [ ] ISC-1: Validates with the bundled validator.\\n*** End Patch\\n"
  }
}
EOF

PAI_DIR="" HOME="$TMP_HOME" "$PKG_DIR/hooks/post-tool-use.sh" < "$patch_payload" | python3 -m json.tool >/dev/null
rg -q 'detected_isa_paths' "$TMP_HOME/.claude/PAI/MEMORY/OBSERVABILITY/codex-posttool.jsonl"
rg -q "$valid_isa" "$TMP_HOME/.claude/PAI/MEMORY/OBSERVABILITY/codex-posttool.jsonl"

unrelated_payload="$TMP_HOME/unrelated-payload.json"
cat > "$unrelated_payload" <<EOF
{
  "tool_name": "apply_patch",
  "cwd": "$TMP_HOME",
  "tool_input": {
    "command": "*** Begin Patch\\n*** Update File: notes.md\\n@@\\n+hello\\n*** End Patch\\n"
  }
}
EOF

PAI_DIR="" HOME="$TMP_HOME" "$PKG_DIR/hooks/post-tool-use.sh" < "$unrelated_payload" | python3 -m json.tool >/dev/null
python3 - "$TMP_HOME/.claude/PAI/MEMORY/OBSERVABILITY/codex-posttool.jsonl" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import sys

entries = [json.loads(line) for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()]
assert entries[-1]["detected_isa_paths"] == [], entries[-1]
PY

native_output="$(
  printf '{"prompt":"who am I?"}\n' |
    PAI_DIR="" HOME="$TMP_HOME" "$PKG_DIR/hooks/prompt-processing.sh"
)"
printf '%s\n' "$native_output" | python3 -m json.tool >/dev/null
rg -q 'PAI_MODE=NATIVE' <<<"$native_output"

algorithm_output="$(
  printf '{"prompt":"start an Algorithm run"}\n' |
    PAI_DIR="" HOME="$TMP_HOME" "$PKG_DIR/hooks/prompt-processing.sh"
)"
printf '%s\n' "$algorithm_output" | python3 -m json.tool >/dev/null
rg -q 'PAI_MODE=ALGORITHM' <<<"$algorithm_output"

echo "Algorithm and ISA runtime test passed"
