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
GENERATOR="$PKG_DIR/tools/GenerateAgentsMd.ts"

if ! command -v bun >/dev/null 2>&1; then
  echo "skip: bun not available; AGENTS generator test skipped"
  exit 0
fi

TMP_HOME="$(mktemp -d "${TMPDIR:-/tmp}/pai-codex-generate-agents.XXXXXX")"
cleanup() {
  find "$TMP_HOME" -depth -type f -delete 2>/dev/null || true
  find "$TMP_HOME" -depth -type d -empty -delete 2>/dev/null || true
}
trap cleanup EXIT

PAI_DIR="$TMP_HOME/.claude/PAI"
OUTPUT="$TMP_HOME/.codex/AGENTS.md"

mkdir -p "$PAI_DIR/USER" \
  "$PAI_DIR/ALGORITHM" \
  "$PAI_DIR/CONTACTS" \
  "$PAI_DIR/OPINIONS" \
  "$PAI_DIR/FINANCES" \
  "$PAI_DIR/BUSINESS" \
  "$PAI_DIR/RESUME" \
  "$TMP_HOME/.codex"

cat > "$PAI_DIR/USER/PRINCIPAL_IDENTITY.md" <<'EOF'
# Principal Identity
- Name: Test Principal
- Role: Test Builder
- Email: principal@example.invalid
EOF

cat > "$PAI_DIR/USER/DA_IDENTITY.md" <<'EOF'
# Runtime Assistant Identity
- Name: Test Assistant
- Role: Runtime peer
- Voice: private-voice-id
EOF

printf 'test-algorithm.md\n' > "$PAI_DIR/ALGORITHM/LATEST"
cat > "$PAI_DIR/ALGORITHM/test-algorithm.md" <<'EOF'
# Test Algorithm
Seven phases and ISA guidance for tests.
EOF

for dir in CONTACTS OPINIONS FINANCES BUSINESS RESUME; do
  printf 'PRIVATE_%s_MARKER\n' "$dir" > "$PAI_DIR/$dir/private.md"
done

cat > "$OUTPUT" <<'EOF'
# Existing Local Instructions

Keep this user content.
EOF

HOME="$TMP_HOME" bun "$GENERATOR" --output "$OUTPUT" --pai-dir "$PAI_DIR" >/dev/null

rg -q 'Keep this user content' "$OUTPUT"
rg -q 'PAI-CODEX:BEGIN' "$OUTPUT"
rg -q 'Principal Summary:' "$OUTPUT"
rg -q 'Test Principal' "$OUTPUT"
rg -q 'Runtime Assistant Summary:' "$OUTPUT"
rg -q 'Test Assistant' "$OUTPUT"
rg -q 'Algorithm Pointer: test-algorithm.md' "$OUTPUT"
rg -q '## Operational Rules' "$OUTPUT"
rg -q '## Context Override Escalation' "$OUTPUT"
rg -q '## Advisor Unavailable' "$OUTPUT"
rg -q '## Output Formats' "$OUTPUT"
rg -q '## Algorithm And ISA Rules' "$OUTPUT"
! rg -q 'principal@example.invalid' "$OUTPUT"
! rg -q 'private-voice-id' "$OUTPUT"
for dir in CONTACTS OPINIONS FINANCES BUSINESS RESUME; do
  ! rg -q "PRIVATE_${dir}_MARKER" "$OUTPUT"
done

before="$(sha256sum "$OUTPUT")"
HOME="$TMP_HOME" bun "$GENERATOR" --output "$OUTPUT" --pai-dir "$PAI_DIR" >/dev/null
after="$(sha256sum "$OUTPUT")"
[[ "$before" == "$after" ]] || { echo "generator is not idempotent" >&2; exit 1; }

dry_output="$TMP_HOME/.codex/DRY_AGENTS.md"
dry_summary="$(
  HOME="$TMP_HOME" bun "$GENERATOR" --dry-run --output "$dry_output" --pai-dir "$PAI_DIR"
)"
rg -q 'AGENTS.md dry-run' <<<"$dry_summary"
test ! -e "$dry_output"

cat > "$OUTPUT" <<'EOF'
# User Top

before block

<!-- PAI-CODEX:BEGIN managed by Personal_AI_Infrastructure -->
old managed content
<!-- PAI-CODEX:END managed by Personal_AI_Infrastructure -->

after block
EOF

HOME="$TMP_HOME" bun "$GENERATOR" --output "$OUTPUT" --pai-dir "$PAI_DIR" >/dev/null
rg -q 'before block' "$OUTPUT"
rg -q 'after block' "$OUTPUT"
! rg -q 'old managed content' "$OUTPUT"
[[ "$(rg -c 'PAI-CODEX:BEGIN' "$OUTPUT")" == "1" ]] || { echo "expected one managed block" >&2; exit 1; }

echo "AGENTS generator test passed"
