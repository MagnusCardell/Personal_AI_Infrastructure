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

TMP_HOME="$(mktemp -d "${TMPDIR:-/tmp}/pai-codex-dry-run.XXXXXX")"
cleanup() {
  find "$TMP_HOME" -depth -type f -delete 2>/dev/null || true
  find "$TMP_HOME" -depth -type d -empty -delete 2>/dev/null || true
}
trap cleanup EXIT

mkdir -p "$TMP_HOME/.claude/PAI/MEMORY/OBSERVABILITY"

snapshot() {
  find "$TMP_HOME" -print | sed "s#^$TMP_HOME#.#" | sort
}

before="$(snapshot)"

HOME="$TMP_HOME" "$PKG_DIR/install-codex.sh" --dry-run >/dev/null
after_local="$(snapshot)"
[[ "$before" == "$after_local" ]] || {
  echo "dry-run local install changed HOME" >&2
  diff <(printf '%s\n' "$before") <(printf '%s\n' "$after_local") >&2 || true
  exit 1
}

HOME="$TMP_HOME" "$PKG_DIR/install-codex.sh" --global --dry-run >/dev/null
after_global="$(snapshot)"
[[ "$before" == "$after_global" ]] || {
  echo "dry-run global install changed HOME" >&2
  diff <(printf '%s\n' "$before") <(printf '%s\n' "$after_global") >&2 || true
  exit 1
}

HOME="$TMP_HOME" "$PKG_DIR/uninstall-codex.sh" --dry-run >/dev/null
after_uninstall="$(snapshot)"
[[ "$before" == "$after_uninstall" ]] || {
  echo "dry-run uninstall changed HOME" >&2
  diff <(printf '%s\n' "$before") <(printf '%s\n' "$after_uninstall") >&2 || true
  exit 1
}

if [[ -d "$TMP_HOME/.claude/codex/backups" ]]; then
  echo "dry-run created backup directory" >&2
  exit 1
fi

if [[ -e "$TMP_HOME/.claude/codex/install-state/last-install.txt" ]]; then
  echo "dry-run wrote install-state" >&2
  exit 1
fi

echo "dry-run purity passed"
