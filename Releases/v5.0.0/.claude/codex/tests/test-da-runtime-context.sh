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
rg -q 'PAI_ALGORITHM_POINTER=test-algorithm.md' <<<"$additional"
rg -q 'PAI_CONTEXT_MODE=compact' <<<"$additional"
rg -q 'PAI_PRINCIPAL_FILE=.*PRINCIPAL_IDENTITY\.md \| Principal' <<<"$additional"
rg -q 'PAI_DA_FILE=.*DA_IDENTITY\.md \| Runtime Assistant' <<<"$additional"
rg -q 'PAI_PROJECTS_FILE=.*PROJECTS/PROJECTS\.md \| Active Projects' <<<"$additional"
rg -q 'PAI_TELOS_FILE=.*PRINCIPAL_TELOS\.md \| Telos' <<<"$additional"
! rg -q 'PAI_PRINCIPAL_CONTEXT=' <<<"$additional"
! rg -q '^Source:' <<<"$additional"
! rg -q 'PRINCIPAL_TEST_MARKER' <<<"$additional"
! rg -q 'DA_TEST_MARKER' <<<"$additional"
! rg -q 'PROJECTS_TEST_MARKER' <<<"$additional"
! rg -q 'TELOS_TEST_MARKER' <<<"$additional"
! rg -q 'ALGORITHM_TEST_MARKER' <<<"$additional"
! rg -q 'supersecretvalue' <<<"$additional"
printf '%s' "$additional" | python3 -c 'import sys; data=sys.stdin.read(); assert len(data) <= 1500, len(data)'
! rg -q 'supersecretvalue' "$TMP_HOME/.claude/PAI/MEMORY/OBSERVABILITY" 2>/dev/null

full_output="$(
  printf '{"hook_event_name":"SessionStart","cwd":"/tmp"}\n' |
    PAI_CODEX_CONTEXT_MODE=full PAI_DIR="" HOME="$TMP_HOME" "$PKG_DIR/hooks/session-start.sh"
)"

printf '%s\n' "$full_output" | python3 -m json.tool >/dev/null
full_additional="$(
  printf '%s\n' "$full_output" | python3 -c 'import json, sys; print(json.load(sys.stdin)["hookSpecificOutput"]["additionalContext"])'
)"

rg -q 'PAI_RUNTIME_CONTEXT=available' <<<"$full_additional"
rg -q 'PRINCIPAL_TEST_MARKER' <<<"$full_additional"
rg -q 'DA_TEST_MARKER' <<<"$full_additional"
rg -q 'PROJECTS_TEST_MARKER' <<<"$full_additional"
rg -q 'TELOS_TEST_MARKER' <<<"$full_additional"
rg -q 'PAI_ALGORITHM_POINTER=test-algorithm.md' <<<"$full_additional"
rg -q 'ALGORITHM_TEST_MARKER' <<<"$full_additional"
! rg -q 'supersecretvalue' <<<"$full_additional"

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
rg -q 'PAI_CONTEXT_MODE=compact' <<<"$partial_additional"
rg -q 'DA_IDENTITY.md' <<<"$partial_additional"
rg -q 'test-algorithm.md' <<<"$partial_additional"
rg -q 'PAI_PRINCIPAL_FILE=.*PRINCIPAL_IDENTITY\.md \| Principal' <<<"$partial_additional"
rg -q 'PAI_PROJECTS_FILE=.*PROJECTS/PROJECTS\.md \| Active Projects' <<<"$partial_additional"
rg -q 'PAI_TELOS_FILE=.*PRINCIPAL_TELOS\.md \| Telos' <<<"$partial_additional"
! rg -q 'PAI_DA_FILE=' <<<"$partial_additional"

echo "DA runtime context test passed"
