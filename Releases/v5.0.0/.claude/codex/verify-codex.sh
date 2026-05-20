#!/usr/bin/env bash
set -euo pipefail

SCRIPT_SOURCE="${BASH_SOURCE[0]}"
while [[ -L "$SCRIPT_SOURCE" ]]; do
  SCRIPT_DIR_LINK="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
  SCRIPT_SOURCE="$(readlink "$SCRIPT_SOURCE")"
  [[ "$SCRIPT_SOURCE" != /* ]] && SCRIPT_SOURCE="$SCRIPT_DIR_LINK/$SCRIPT_SOURCE"
done
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"

MODE="package"
SCAN_TMP="$(mktemp "${TMPDIR:-/tmp}/pai-codex-verify.XXXXXX")"
trap 'rm -f "$SCAN_TMP"' EXIT

usage() {
  cat <<'EOF'
usage: verify-codex.sh [--package|--installed]

  --package    verify the release package in this directory (default)
  --installed  verify files installed into the user's Codex/PAI locations
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --package) MODE="package" ;;
    --installed) MODE="installed" ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

failures=0

ok() {
  echo "ok: $*"
}

fail() {
  echo "fail: $*" >&2
  failures=$((failures + 1))
}

require_file() {
  local path="$1"
  [[ -f "$path" ]] && ok "file $path" || fail "missing file $path"
}

require_exec() {
  local path="$1"
  [[ -x "$path" ]] && ok "executable $path" || fail "not executable $path"
}

require_contains() {
  local path="$1"
  local pattern="$2"
  local label="$3"
  if rg -q "$pattern" "$path"; then
    ok "$label"
  else
    fail "$label"
  fi
}

json_check() {
  local path="$1"
  python3 -m json.tool "$path" >/dev/null && ok "json $path" || fail "invalid json $path"
}

python_check() {
  local path="$1"
  python3 - "$path" <<'PY' && ok "python $path" || fail "python syntax $path"
from pathlib import Path
import sys

path = Path(sys.argv[1])
compile(path.read_text(encoding="utf-8"), str(path), "exec")
PY
}

bash_check() {
  local path="$1"
  bash -n "$path" && ok "bash $path" || fail "bash syntax $path"
}

scan_private_refs() {
  local root="$1"
  local patterns
  patterns=(
    "/home/""maca"
    "Mag""nus"
    "Lov""able"
    "P""wC"
    "S""17"
    "S""18"
    "S""19"
    "replacement-""grade"
    "ad""apter ""chapter"
    "sha""dow"
    "cap""sule"
  )
  local pattern
  for pattern in "${patterns[@]}"; do
    if rg -n --fixed-strings "$pattern" "$root" >"$SCAN_TMP" 2>/dev/null; then
      cat "$SCAN_TMP" >&2
      fail "private or research reference found: $pattern"
    else
      ok "no reference: $pattern"
    fi
  done
}

scan_secret_refs() {
  local root="$1"
  local patterns
  patterns=(
    "OPENAI_""API_KEY"
    "ANTHROPIC_""API_KEY"
    "ghp""_"
    "sk""-"
    "BEGIN ""PRIVATE KEY"
    "AWS_SECRET_""ACCESS_KEY"
    "ELEVEN""LABS_""API_KEY"
    "ELEVEN_""API_KEY"
  )
  local pattern
  for pattern in "${patterns[@]}"; do
    if rg -n --fixed-strings "$pattern" "$root" >"$SCAN_TMP" 2>/dev/null; then
      cat "$SCAN_TMP" >&2
      fail "secret-like reference found: $pattern"
    else
      ok "no secret reference: $pattern"
    fi
  done
}

scan_provider_call_refs() {
  local root="$1"
  local cword="curl"
  local vword="voice"
  local tword="tts"
  local oword="openai"
  local aword="audio"
  local patterns
  patterns=(
    "eleven""labs"
    "api.eleven""labs"
    "text-to-""speech"
    "speech-to-""text"
    "${oword}.${aword}"
    "${cword}.*${vword}"
    "${cword}.*${tword}"
  )
  local pattern
  for pattern in "${patterns[@]}"; do
    if rg -n -i "$pattern" "$root" >"$SCAN_TMP" 2>/dev/null; then
      cat "$SCAN_TMP" >&2
      fail "direct provider invocation reference found: $pattern"
    else
      ok "no provider call reference: $pattern"
    fi
  done
}

check_pulse_env_defaults() {
  local path="$1"
  require_file "$path"
  require_contains "$path" '^export PAI_CODEX_PULSE_ENABLED=0$' "Pulse disabled by default"
  require_contains "$path" '^export PAI_CODEX_VOICE_ENABLED=0$' "voice disabled by default"
  require_contains "$path" '^export PAI_CODEX_VOICE_ID=$' "voice id empty by default"
  require_contains "$path" '^export PAI_CODEX_LEARNING_ENABLED=0$' "learning disabled by default"
  require_contains "$path" '^export PAI_CODEX_CHECKPOINT_ENABLED=0$' "checkpoint disabled by default"
  if rg -q '^export PAI_CODEX_VOICE_ID=.+$' "$path"; then
    fail "non-empty voice id in package pulse.env"
  else
    ok "no personal voice id in package pulse.env"
  fi
}

check_pulse_env_sourcing() {
  local path="$1"
  require_contains "$path" 'PAI_CODEX_ENV=.*pulse\.env' "$path sources pulse env path"
  require_contains "$path" '\. "\$PAI_CODEX_ENV"' "$path sources pulse env file"
}

verify_tree() {
  local root="$1"
  require_file "$root/README.md"
  require_file "$root/AGENTS.md.template"
  require_file "$root/hooks.json.template"
  require_file "$root/config.example.toml"
  require_file "$root/install-codex.sh"
  require_file "$root/uninstall-codex.sh"
  require_file "$root/verify-codex.sh"
  require_file "$root/tests/test-dry-run-purity.sh"
  require_file "$root/tests/acceptance-clean-home.sh"
  require_file "$root/tests/test-da-runtime-context.sh"
  require_file "$root/tests/test-algorithm-isa-runtime.sh"
  require_file "$root/tests/test-pulse-runtime.sh"
  require_file "$root/tests/test-voice-runtime.sh"
  require_file "$root/tests/run-all.sh"
  require_file "$root/RELEASE_CHECKLIST.md"
  require_file "$root/hooks/probe.sh"
  check_pulse_env_defaults "$root/hooks/pulse.env"
  check_pulse_env_sourcing "$root/hooks/post-tool-use.sh"
  check_pulse_env_sourcing "$root/hooks/stop.sh"

  json_check "$root/hooks.json.template"

  for script in "$root"/*.sh "$root"/hooks/*.sh "$root"/skills/pai-isa/scripts/*.sh "$root"/skills/pai-runtime-audit/scripts/*.sh; do
    [[ -e "$script" ]] || continue
    bash_check "$script"
  done

  for py in "$root"/hooks/lib/*.py; do
    [[ -e "$py" ]] || continue
    python_check "$py"
  done

  scan_private_refs "$root"
  scan_secret_refs "$root"
  scan_provider_call_refs "$root"
}

verify_installed() {
  require_file "$HOME/.codex/AGENTS.md"
  require_file "$HOME/.codex/hooks.json"
  require_file "$HOME/.codex/config.toml"
  require_file "$HOME/.claude/hooks/codex/session-start.sh"
  require_file "$HOME/.claude/hooks/codex/prompt-processing.sh"
  require_file "$HOME/.claude/hooks/codex/pre-tool-use.sh"
  require_file "$HOME/.claude/hooks/codex/post-tool-use.sh"
  require_file "$HOME/.claude/hooks/codex/permission-request.sh"
  require_file "$HOME/.claude/hooks/codex/stop.sh"
  require_file "$HOME/.claude/hooks/codex/probe.sh"
  require_file "$HOME/.claude/hooks/codex/pulse.env"
  require_file "$HOME/.claude/hooks/codex/lib/redact.py"
  require_file "$HOME/.claude/hooks/codex/lib/log_event.py"
  require_file "$HOME/.claude/hooks/codex/lib/pai_context.py"
  require_file "$HOME/.claude/hooks/codex/lib/pulse_notify.py"
  check_pulse_env_sourcing "$HOME/.claude/hooks/codex/post-tool-use.sh"
  check_pulse_env_sourcing "$HOME/.claude/hooks/codex/stop.sh"

  json_check "$HOME/.codex/hooks.json"
  for script in "$HOME/.claude/hooks/codex"/*.sh; do
    bash_check "$script"
    require_exec "$script"
  done
  for py in "$HOME/.claude/hooks/codex/lib"/*.py; do
    python_check "$py"
  done

  for skill in pai-algorithm pai-memory pai-isa pai-runtime-audit; do
    require_file "$HOME/.agents/skills/$skill/SKILL.md"
  done
  require_exec "$HOME/.agents/skills/pai-isa/scripts/validate-isa.sh"
  require_exec "$HOME/.agents/skills/pai-runtime-audit/scripts/runtime-audit.sh"

  for agent in pai_explorer pai_reviewer pai_security_reviewer; do
    require_file "$HOME/.codex/agents/$agent.toml"
    if rg -q 'sandbox_mode\s*=\s*"read-only"' "$HOME/.codex/agents/$agent.toml"; then
      ok "read-only agent $agent"
    else
      fail "agent not read-only: $agent"
    fi
  done
}

verify_tree "$SCRIPT_DIR"
if [[ "$MODE" == "installed" ]]; then
  verify_installed
fi

if command -v shellcheck >/dev/null 2>&1; then
  while IFS= read -r script; do
    shellcheck "$script" && ok "shellcheck $script" || fail "shellcheck $script"
  done < <(find "$SCRIPT_DIR" -name '*.sh' -type f | sort)
else
  echo "skip: shellcheck not installed"
fi

if command -v codex >/dev/null 2>&1; then
  echo "codex: $(codex --version 2>/dev/null || echo found)"
else
  echo "skip: codex CLI not found"
fi

if [[ "$failures" -gt 0 ]]; then
  echo "verify failed: $failures issue(s)" >&2
  exit 1
fi

echo "verify passed"
