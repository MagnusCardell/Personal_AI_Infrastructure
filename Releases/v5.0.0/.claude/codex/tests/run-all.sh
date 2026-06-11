#!/usr/bin/env bash
set -euo pipefail

SCRIPT_SOURCE="${BASH_SOURCE[0]}"
while [[ -L "$SCRIPT_SOURCE" ]]; do
  SCRIPT_DIR_LINK="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
  SCRIPT_SOURCE="$(readlink "$SCRIPT_SOURCE")"
  [[ "$SCRIPT_SOURCE" != /* ]] && SCRIPT_SOURCE="$SCRIPT_DIR_LINK/$SCRIPT_SOURCE"
done
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
PKG_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

TESTS=(
  "$PKG_DIR/verify-codex.sh --package"
  "$SCRIPT_DIR/test-dry-run-purity.sh"
  "$SCRIPT_DIR/acceptance-clean-home.sh"
  "$SCRIPT_DIR/test-da-runtime-context.sh"
  "$SCRIPT_DIR/test-algorithm-isa-runtime.sh"
  "$SCRIPT_DIR/test-pulse-runtime.sh"
  "$SCRIPT_DIR/test-voice-runtime.sh"
  "$SCRIPT_DIR/test-learning-runtime.sh"
  "$SCRIPT_DIR/test-generate-agents.sh"
  "$SCRIPT_DIR/test-security-runtime.sh"
  "$SCRIPT_DIR/test-checkpoint-runtime.sh"
  "$SCRIPT_DIR/test-skill-dispatch-runtime.sh"
  "$SCRIPT_DIR/test-lib-parity.sh"
)

PASS_COUNT=0
FAIL_COUNT=0
FAILED=()

printf 'PAI Codex package test runner\n'
printf 'package: %s\n' "$PKG_DIR"
printf 'note: Pulse and voice tests use localhost loopback; restricted sandboxes may require local-bind permission.\n'
printf '\n'

for test_cmd in "${TESTS[@]}"; do
  printf '==> %s\n' "$test_cmd"
  if bash -c "$test_cmd"; then
    printf 'PASS: %s\n\n' "$test_cmd"
    PASS_COUNT=$((PASS_COUNT + 1))
  else
    printf 'FAIL: %s\n\n' "$test_cmd"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    FAILED+=("$test_cmd")
  fi
done

printf 'Summary: %d passed, %d failed\n' "$PASS_COUNT" "$FAIL_COUNT"
if [[ "$FAIL_COUNT" -gt 0 ]]; then
  printf 'Failed tests:\n'
  printf '  %s\n' "${FAILED[@]}"
  exit 1
fi

printf 'All PAI Codex package tests passed.\n'
