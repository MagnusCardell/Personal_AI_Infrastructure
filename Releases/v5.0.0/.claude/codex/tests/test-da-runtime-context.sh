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

TMP_HOME="$(mktemp -d "${TMPDIR:-/tmp}/pai-codex-da-context.XXXXXX")"
cleanup() {
  find "$TMP_HOME" -depth -type f -delete 2>/dev/null || true
  find "$TMP_HOME" -depth -type d -empty -delete 2>/dev/null || true
}
trap cleanup EXIT

mkdir -p "$TMP_HOME/.claude/PAI/USER/PROJECTS" \
  "$TMP_HOME/.claude/PAI/USER/TELOS" \
  "$TMP_HOME/.claude/PAI/ALGORITHM" \
  "$TMP_HOME/.claude/PAI/MEMORY/WORK" \
  "$TMP_HOME/.claude/PAI/MEMORY/OBSERVABILITY" \
  "$TMP_HOME/.claude/PAI/MEMORY/LEARNING"

cat > "$TMP_HOME/.claude/PAI/USER/PRINCIPAL_IDENTITY.md" <<'EOF'
# Principal
PRINCIPAL_TEST_MARKER
EOF

cat > "$TMP_HOME/.claude/PAI/USER/DA_IDENTITY.md" <<'EOF'
# Runtime Assistant
DA_TEST_MARKER
password=supersecretvalue
EOF

cat > "$TMP_HOME/.claude/PAI/USER/PROJECTS/PROJECTS.md" <<'EOF'
## Active Projects
- PROJECTS_TEST_MARKER
EOF

cat > "$TMP_HOME/.claude/PAI/USER/TELOS/PRINCIPAL_TELOS.md" <<'EOF'
# Telos
TELOS_TEST_MARKER
EOF

printf '%s\n' 'test-algorithm.md' > "$TMP_HOME/.claude/PAI/ALGORITHM/LATEST"
cat > "$TMP_HOME/.claude/PAI/ALGORITHM/test-algorithm.md" <<'EOF'
# Algorithm
ALGORITHM_TEST_MARKER
EOF

output="$(
  printf '{"hook_event_name":"SessionStart","cwd":"/tmp"}\n' |
    PAI_DIR="" HOME="$TMP_HOME" "$PKG_DIR/hooks/session-start.sh"
)"

printf '%s\n' "$output" | python3 -m json.tool >/dev/null
additional="$(
  printf '%s\n' "$output" | python3 -c 'import json, sys; print(json.load(sys.stdin)["hookSpecificOutput"]["additionalContext"])'
)"

rg -q 'PAI_RUNTIME_CONTEXT=available' <<<"$additional"
rg -q 'PRINCIPAL_TEST_MARKER' <<<"$additional"
rg -q 'DA_TEST_MARKER' <<<"$additional"
rg -q 'PROJECTS_TEST_MARKER' <<<"$additional"
rg -q 'TELOS_TEST_MARKER' <<<"$additional"
rg -q 'PAI_ALGORITHM_POINTER=test-algorithm.md' <<<"$additional"
rg -q 'ALGORITHM_TEST_MARKER' <<<"$additional"
! rg -q 'supersecretvalue' <<<"$additional"
! rg -q 'supersecretvalue' "$TMP_HOME/.claude/PAI/MEMORY/OBSERVABILITY" 2>/dev/null

rm -f "$TMP_HOME/.claude/PAI/USER/DA_IDENTITY.md"
rm -f "$TMP_HOME/.claude/PAI/ALGORITHM/test-algorithm.md"
partial_output="$(
  printf '{"hook_event_name":"SessionStart","cwd":"/tmp"}\n' |
    PAI_DIR="" HOME="$TMP_HOME" "$PKG_DIR/hooks/session-start.sh"
)"

printf '%s\n' "$partial_output" | python3 -m json.tool >/dev/null
partial_additional="$(
  printf '%s\n' "$partial_output" | python3 -c 'import json, sys; print(json.load(sys.stdin)["hookSpecificOutput"]["additionalContext"])'
)"
rg -q 'PAI_RUNTIME_CONTEXT=partial' <<<"$partial_additional"
rg -q 'PAI_CONTEXT_MISSING=' <<<"$partial_additional"
rg -q 'DA_IDENTITY.md' <<<"$partial_additional"
rg -q 'test-algorithm.md' <<<"$partial_additional"

echo "DA runtime context test passed"
