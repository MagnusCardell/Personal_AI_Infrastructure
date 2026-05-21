#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
usage: dispatch.sh SKILL_NAME [args...]

Available skills:
  isa_append
EOF
}

if [[ $# -lt 1 ]]; then
  usage >&2
  exit 2
fi

skill="$1"
shift

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required for Codex skill dispatch." >&2
  exit 1
fi

case "$skill" in
  isa_append|ISA_APPEND)
    exec python3 "$SKILL_DIR/isa_append.py" "$@"
    ;;
  *)
    echo "unknown skill: $skill" >&2
    usage >&2
    exit 2
    ;;
esac
