#!/usr/bin/env bash
set -euo pipefail

SCRIPT_SOURCE="${BASH_SOURCE[0]}"
while [[ -L "$SCRIPT_SOURCE" ]]; do
  SCRIPT_DIR_LINK="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
  SCRIPT_SOURCE="$(readlink "$SCRIPT_SOURCE")"
  [[ "$SCRIPT_SOURCE" != /* ]] && SCRIPT_SOURCE="$SCRIPT_DIR_LINK/$SCRIPT_SOURCE"
done
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"

SCOPE="pai-local"
DRY_RUN=0

usage() {
  cat <<'EOF'
usage: install-codex.sh [--global|--pai-local] [--dry-run]

  --pai-local   stage PAI-local Codex files only (default)
  --global      activate Codex by writing ~/.codex and ~/.agents files
  --dry-run     print intended changes without writing
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --global) SCOPE="global" ;;
    --pai-local) SCOPE="pai-local" ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

PAI_DIR="${PAI_DIR:-$HOME/.claude/PAI}"
HOOK_DEST="$HOME/.claude/hooks/codex"
LOCAL_DEST="$HOME/.claude/codex"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
BACKUP_DIR="$LOCAL_DEST/backups/$(date -u +%Y%m%dT%H%M%SZ)"
CHANGED=()

say() {
  printf '%s\n' "$*"
}

changed() {
  CHANGED+=("$1")
}

backup_if_needed() {
  local dest="$1"
  [[ -e "$dest" ]] || return 0
  local rel="${dest#$HOME/}"
  local backup="$BACKUP_DIR/${rel//\//__}"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "would back up $dest -> $backup"
    return 0
  fi
  mkdir -p "$BACKUP_DIR"
  cp -p "$dest" "$backup"
}

install_file() {
  local src="$1"
  local dest="$2"
  local mode="${3:-0644}"

  if [[ -f "$dest" ]] && cmp -s "$src" "$dest"; then
    say "unchanged: $dest"
    return 0
  fi

  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "would install $src -> $dest"
    changed "$dest"
    return 0
  fi

  mkdir -p "$(dirname "$dest")"
  backup_if_needed "$dest"
  cp -p "$src" "$dest"
  chmod "$mode" "$dest"
  changed "$dest"
}

install_tree() {
  local src_dir="$1"
  local dest_dir="$2"
  local default_mode="${3:-0644}"
  while IFS= read -r src; do
    local rel="${src#$src_dir/}"
    local mode="$default_mode"
    case "$src" in
      *.sh) mode="0755" ;;
    esac
    install_file "$src" "$dest_dir/$rel" "$mode"
  done < <(find "$src_dir" -type f ! -path '*/__pycache__/*' ! -name '*.pyc' | sort)
}

configure_codex_config() {
  local config_path="$CODEX_HOME/config.toml"
  local example_path="$CODEX_HOME/pai-config.example.toml"

  install_file "$SCRIPT_DIR/config.example.toml" "$example_path" "0644"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "would ensure hooks, workspace-write, on-request, and PAI writable roots in $config_path"
    changed "$config_path"
    return 0
  fi

  mkdir -p "$CODEX_HOME"
  backup_if_needed "$config_path"
  python3 - "$config_path" "$HOME/.claude/PAI" "$HOME/.claude/hooks/codex" <<'PY'
from __future__ import annotations

from pathlib import Path
import re
import sys

config_path = Path(sys.argv[1])
roots = [sys.argv[2], sys.argv[3]]
text = config_path.read_text(encoding="utf-8") if config_path.exists() else ""


def set_top_level(source: str, key: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^{re.escape(key)}\s*=.*$")
    line = f'{key} = "{value}"'
    if pattern.search(source):
        return pattern.sub(line, source)
    return line + "\n" + source


def ensure_section_key(source: str, section: str, key: str, value: str) -> str:
    header = f"[{section}]"
    section_re = re.compile(rf"(?ms)^{re.escape(header)}\s*\n(?P<body>.*?)(?=^\[|\Z)")
    match = section_re.search(source)
    line = f"{key} = {value}"
    if not match:
        return source.rstrip() + f"\n\n{header}\n{line}\n"
    body = match.group("body")
    key_re = re.compile(rf"(?m)^{re.escape(key)}\s*=.*$")
    if key_re.search(body):
        body = key_re.sub(line, body)
    else:
        body = line + "\n" + body
    return source[:match.start("body")] + body + source[match.end("body"):]


def ensure_writable_roots(source: str) -> str:
    header = "[sandbox_workspace_write]"
    section_re = re.compile(r"(?ms)^\[sandbox_workspace_write\]\s*\n(?P<body>.*?)(?=^\[|\Z)")
    formatted = "writable_roots = [\n" + "".join(f'  "{root}",\n' for root in roots) + "]"
    match = section_re.search(source)
    if not match:
        return source.rstrip() + f"\n\n{header}\n{formatted}\n"
    body = match.group("body")
    list_re = re.compile(r"(?ms)^writable_roots\s*=\s*\[.*?\]")
    if list_re.search(body):
        body = list_re.sub(formatted, body)
    else:
        body = formatted + "\n" + body
    return source[:match.start("body")] + body + source[match.end("body"):]


text = set_top_level(text, "approval_policy", "on-request")
text = set_top_level(text, "sandbox_mode", "workspace-write")
text = ensure_section_key(text, "features", "hooks", "true")
text = ensure_writable_roots(text)
config_path.write_text(text.rstrip() + "\n", encoding="utf-8")
PY
  changed "$config_path"
}

if [[ ! -d "$PAI_DIR" ]]; then
  say "PAI engine not found at $PAI_DIR"
  say "Install PAI before enabling Codex support."
  exit 1
fi

if command -v codex >/dev/null 2>&1; then
  say "Codex CLI found: $(codex --version 2>/dev/null || echo unknown)"
else
  say "Codex CLI not found. Install Codex before running Codex as a PAI runtime."
fi

say "install scope: $SCOPE"
say "source: $SCRIPT_DIR"

install_tree "$SCRIPT_DIR/hooks" "$HOOK_DEST" "0644"
install_file "$SCRIPT_DIR/README.md" "$LOCAL_DEST/README.md" "0644"
install_file "$SCRIPT_DIR/AGENTS.md.template" "$LOCAL_DEST/AGENTS.md.template" "0644"
install_file "$SCRIPT_DIR/hooks.json.template" "$LOCAL_DEST/hooks.json.template" "0644"
install_file "$SCRIPT_DIR/config.example.toml" "$LOCAL_DEST/config.example.toml" "0644"
install_file "$SCRIPT_DIR/install-codex.sh" "$LOCAL_DEST/install-codex.sh" "0755"
install_file "$SCRIPT_DIR/uninstall-codex.sh" "$LOCAL_DEST/uninstall-codex.sh" "0755"
install_file "$SCRIPT_DIR/verify-codex.sh" "$LOCAL_DEST/verify-codex.sh" "0755"

if [[ "$SCOPE" == "global" ]]; then
  mkdir -p "$CODEX_HOME" "$HOME/.agents/skills" "$CODEX_HOME/agents"
  install_file "$SCRIPT_DIR/AGENTS.md.template" "$CODEX_HOME/AGENTS.md" "0644"
  install_file "$SCRIPT_DIR/hooks.json.template" "$CODEX_HOME/hooks.json" "0644"
  configure_codex_config
  install_tree "$SCRIPT_DIR/skills" "$HOME/.agents/skills" "0644"
  install_tree "$SCRIPT_DIR/agents" "$CODEX_HOME/agents" "0644"
else
  install_tree "$SCRIPT_DIR/skills" "$LOCAL_DEST/skills" "0644"
  install_tree "$SCRIPT_DIR/agents" "$LOCAL_DEST/agents" "0644"
  say "PAI-local staging complete. Re-run with --global to activate Codex-facing files."
fi

if [[ "$DRY_RUN" -eq 0 ]]; then
  mkdir -p "$LOCAL_DEST/install-state"
  {
    printf 'timestamp=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'scope=%s\n' "$SCOPE"
    printf 'files_changed=\n'
    printf '%s\n' "${CHANGED[@]}"
  } > "$LOCAL_DEST/install-state/last-install.txt"
fi

say "files changed:"
if [[ "${#CHANGED[@]}" -eq 0 ]]; then
  say "  none"
else
  printf '  %s\n' "${CHANGED[@]}"
fi

say "verify with: $LOCAL_DEST/verify-codex.sh --installed"
