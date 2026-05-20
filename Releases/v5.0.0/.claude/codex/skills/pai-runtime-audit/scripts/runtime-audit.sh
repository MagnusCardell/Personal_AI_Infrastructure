#!/usr/bin/env bash
set -euo pipefail

failures=0

check_file() {
  local path="$1"
  if [[ -f "$path" ]]; then
    echo "ok file: $path"
  else
    echo "missing file: $path"
    failures=$((failures + 1))
  fi
}

check_dir() {
  local path="$1"
  if [[ -d "$path" ]]; then
    echo "ok dir: $path"
  else
    echo "missing dir: $path"
    failures=$((failures + 1))
  fi
}

check_file "$HOME/.codex/AGENTS.md"
check_file "$HOME/.codex/hooks.json"
check_file "$HOME/.codex/config.toml"
check_dir "$HOME/.claude/hooks/codex"

if [[ -f "$HOME/.codex/hooks.json" ]]; then
  python3 -m json.tool "$HOME/.codex/hooks.json" >/dev/null
  echo "ok json: $HOME/.codex/hooks.json"
fi

if [[ -f "$HOME/.codex/config.toml" ]]; then
  rg -n 'sandbox_mode\s*=\s*"workspace-write"|approval_policy\s*=\s*"on-request"|hooks\s*=\s*true' "$HOME/.codex/config.toml" || true
fi

if [[ -d "$HOME/.codex/agents" ]]; then
  rg -n 'sandbox_mode\s*=\s*"read-only"' "$HOME/.codex/agents"/pai_*.toml 2>/dev/null || true
fi

if [[ -d "$HOME/.claude/hooks/codex" ]]; then
  if rg -n 'git commit|tar\s|retention' "$HOME/.claude/hooks/codex" >/dev/null 2>&1; then
    echo "warning: review possible hidden maintenance behavior in hooks"
  else
    echo "ok hooks: no hidden maintenance keywords found"
  fi
fi

exit "$failures"
