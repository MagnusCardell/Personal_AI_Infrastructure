#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=0

usage() {
  cat <<'EOF'
usage: uninstall-codex.sh [--dry-run]

Removes known PAI Codex runtime files. It does not remove unrelated Codex files.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

remove_file() {
  local path="$1"
  [[ -e "$path" ]] || return 0
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "would remove file: $path"
  else
    command rm "$path"
    echo "removed file: $path"
  fi
}

remove_dir_if_empty() {
  local path="$1"
  [[ -d "$path" ]] || return 0
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "would remove dir if empty: $path"
  else
    rmdir "$path" 2>/dev/null || true
  fi
}

remove_managed_file() {
  local path="$1"
  local marker="$2"
  [[ -f "$path" ]] || return 0
  if rg -q "$marker" "$path"; then
    remove_file "$path"
  else
    echo "skipped non-managed file: $path"
  fi
}

for name in session-start prompt-processing pre-tool-use post-tool-use permission-request stop; do
  remove_file "$HOME/.claude/hooks/codex/$name.sh"
done
for name in redact log_event; do
  remove_file "$HOME/.claude/hooks/codex/lib/$name.py"
done
remove_dir_if_empty "$HOME/.claude/hooks/codex/lib"
remove_dir_if_empty "$HOME/.claude/hooks/codex"

for skill in pai-algorithm pai-memory pai-isa pai-runtime-audit; do
  if [[ -d "$HOME/.agents/skills/$skill" ]]; then
    while IFS= read -r file; do
      remove_file "$file"
    done < <(find "$HOME/.agents/skills/$skill" -type f | sort -r)
    while IFS= read -r dir; do
      remove_dir_if_empty "$dir"
    done < <(find "$HOME/.agents/skills/$skill" -type d | sort -r)
  fi
done

for agent in pai_explorer pai_reviewer pai_security_reviewer; do
  remove_file "$HOME/.codex/agents/$agent.toml"
done
remove_dir_if_empty "$HOME/.codex/agents"

remove_managed_file "$HOME/.codex/AGENTS.md" "PAI Codex Runtime Instructions"
remove_managed_file "$HOME/.codex/hooks.json" "Loading PAI context"
remove_file "$HOME/.codex/pai-config.example.toml"

echo "config note: ~/.codex/config.toml is left in place. Restore installer backups manually if needed."
