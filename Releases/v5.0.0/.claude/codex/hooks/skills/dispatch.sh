#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
usage: dispatch.sh SKILL_NAME [args...]

Available skills:
  isa_append      append decisions/changelog/verification to an ISA
  context_search  Phase-1 scan of prior PAI work (registry, WORK dirs, ISA titles)
  fabric          run a fabric pattern via the local fabric CLI (input on stdin)
  advisor         second-opinion review via PAI_CODEX_ADVISOR_PROVIDER (opt-in)
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
  context_search|CONTEXT_SEARCH)
    exec python3 "$SKILL_DIR/context_search.py" "$@"
    ;;
  fabric|FABRIC)
    exec bash "$SKILL_DIR/fabric.sh" "$@"
    ;;
  advisor|ADVISOR)
    exec bash "$SKILL_DIR/advisor.sh" "$@"
    ;;
  *)
    echo "unknown skill: $skill" >&2
    usage >&2
    exit 2
    ;;
esac
