#!/usr/bin/env bash
# Codex skill: advisor — second-opinion review through an explicitly configured provider.
#
# usage: advisor.sh "TASK: ..." "QUESTION: ..."
#
# Providers are OPT-IN via PAI_CODEX_ADVISOR_PROVIDER. No provider is ever
# called implicitly; an unset provider is a loud, structured failure so the
# caller can distinguish "advisor unavailable" from "advisor had no concerns".
#
#   claude-inference  route through the live PAI inference tool
#                     (bun $PAI_DIR/TOOLS/Inference.ts --mode advisor).
#                     Cross-vendor second opinion; requires bun and the
#                     live PAI tree. Refused inside a nested vendor session.
#   codex-exec        spawn a read-only `codex exec` subprocess. Nested
#                     Codex sessions are attempted, not assumed — a failure
#                     here is reported, never silently swallowed.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAI_DIR="${PAI_DIR:-$HOME/.claude/PAI}"
PROVIDER="${PAI_CODEX_ADVISOR_PROVIDER:-}"
TIMEOUT_SECS="${PAI_CODEX_ADVISOR_TIMEOUT:-120}"

log_event() {
  local status="$1"
  local provider="${2:-none}"
  python3 - "$PAI_DIR" "$status" "$provider" <<'PY' 2>/dev/null || true
import json, sys
from datetime import datetime, timezone
from pathlib import Path

root, status, provider = sys.argv[1], sys.argv[2], sys.argv[3]
log_path = Path(root) / "MEMORY" / "SKILLS" / "codex-execution.jsonl"
log_path.parent.mkdir(parents=True, exist_ok=True)
record = {
    "ts": datetime.now(timezone.utc).isoformat(),
    "skill": "advisor",
    "provider": provider,
    "status": status,
}
with log_path.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(record) + "\n")
PY
}

if [[ $# -lt 2 ]]; then
  echo "usage: advisor.sh \"TASK: ...\" \"QUESTION: ...\"" >&2
  exit 2
fi

if [[ -z "$PROVIDER" ]]; then
  log_event "unavailable" "none"
  echo "PAI_CODEX_ADVISOR_UNAVAILABLE: no advisor provider configured." >&2
  echo "Set PAI_CODEX_ADVISOR_PROVIDER=claude-inference or codex-exec to enable." >&2
  echo "Until then, name the missing advisor coverage as a gap instead of skipping review." >&2
  exit 4
fi

run_claude_inference() {
  if [[ -n "${CLAUDECODE:-}" ]]; then
    echo "PAI_CODEX_ADVISOR_REFUSED: nested vendor session detected (CLAUDECODE set)." >&2
    return 4
  fi
  if ! command -v bun >/dev/null 2>&1; then
    echo "PAI_CODEX_ADVISOR_UNAVAILABLE: bun not found; claude-inference provider needs bun." >&2
    return 4
  fi
  local tool="$PAI_DIR/TOOLS/Inference.ts"
  if [[ ! -f "$tool" ]]; then
    echo "PAI_CODEX_ADVISOR_UNAVAILABLE: $tool not found; live PAI tree required." >&2
    return 4
  fi
  timeout "$TIMEOUT_SECS" bun "$tool" --mode advisor "$@"
}

run_codex_exec() {
  if ! command -v codex >/dev/null 2>&1; then
    echo "PAI_CODEX_ADVISOR_UNAVAILABLE: codex binary not found on PATH." >&2
    return 4
  fi
  timeout "$TIMEOUT_SECS" codex exec --sandbox read-only \
    "You are a skeptical advisor. Review the following and answer the question with concrete gaps, ordered by severity. $*"
}

OUTPUT=""
STATUS=0
case "$PROVIDER" in
  claude-inference)
    OUTPUT="$(run_claude_inference "$@" 2>&1)" || STATUS=$?
    ;;
  codex-exec)
    OUTPUT="$(run_codex_exec "$@" 2>&1)" || STATUS=$?
    ;;
  *)
    log_event "bad-provider" "$PROVIDER"
    echo "PAI_CODEX_ADVISOR_UNAVAILABLE: unknown provider '$PROVIDER'." >&2
    echo "Supported: claude-inference, codex-exec." >&2
    exit 4
    ;;
esac

if [[ $STATUS -ne 0 ]]; then
  log_event "error" "$PROVIDER"
  printf '%s\n' "$OUTPUT" >&2
  echo "PAI_CODEX_ADVISOR_FAILED: provider $PROVIDER exited $STATUS." >&2
  exit "$STATUS"
fi

if [[ -z "${OUTPUT//[[:space:]]/}" ]]; then
  log_event "empty" "$PROVIDER"
  echo "PAI_CODEX_ADVISOR_EMPTY: provider $PROVIDER returned no advice; treat as inconclusive, not as approval." >&2
  exit 5
fi

log_event "ok" "$PROVIDER"
printf '%s\n' "$OUTPUT"
