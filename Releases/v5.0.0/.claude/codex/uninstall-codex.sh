#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=0
ACTION="uninstall"
RESTORE_TARGET=""
BACKUP_ROOT="$HOME/.claude/codex/backups"
AGENTS_BEGIN='<!-- PAI-CODEX:BEGIN managed by Personal_AI_Infrastructure -->'
AGENTS_END='<!-- PAI-CODEX:END managed by Personal_AI_Infrastructure -->'

usage() {
  cat <<'EOF'
usage: uninstall-codex.sh [--dry-run] [--list-backups|--restore-latest|--restore ID_OR_PATH]

  --dry-run         print intended changes without writing
  --list-backups    list installer-created backup directories
  --restore-latest  restore the newest installer backup
  --restore VALUE   restore a backup by directory path or backup id

Uninstall removes only managed PAI Codex files, managed AGENTS blocks, and PAI
hook groups. It does not remove unrelated Codex configuration.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --list-backups) ACTION="list-backups" ;;
    --restore-latest) ACTION="restore-latest" ;;
    --restore)
      ACTION="restore"
      shift
      [[ $# -gt 0 ]] || { echo "--restore requires a backup id or path" >&2; exit 2; }
      RESTORE_TARGET="$1"
      ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

say() {
  printf '%s\n' "$*"
}

require_python3() {
  if ! command -v python3 >/dev/null 2>&1; then
    say "python3 is required for safe Codex uninstall."
    exit 1
  fi
}

remove_file() {
  local path="$1"
  [[ -e "$path" ]] || return 0
  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "would remove file: $path"
  else
    command rm "$path"
    say "removed file: $path"
  fi
}

remove_dir_if_empty() {
  local path="$1"
  [[ -d "$path" ]] || return 0
  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "would remove dir if empty: $path"
  else
    rmdir "$path" 2>/dev/null || true
  fi
}

remove_tree_files() {
  local path="$1"
  [[ -d "$path" ]] || return 0
  while IFS= read -r file; do
    remove_file "$file"
  done < <(find "$path" -type f ! -path '*/backups/*' | sort -r)
  while IFS= read -r dir; do
    remove_dir_if_empty "$dir"
  done < <(find "$path" -depth -type d ! -path '*/backups*' | sort -r)
}

remove_pulse_env() {
  local path="$HOME/.claude/hooks/codex/pulse.env"
  [[ -f "$path" ]] || return 0
  python3 - "$path" "$DRY_RUN" <<'PY'
from __future__ import annotations

from pathlib import Path
import sys

path = Path(sys.argv[1])
dry = sys.argv[2] == "1"
expected = {
    "export PAI_CODEX_PULSE_ENABLED=0",
    "export PAI_CODEX_VOICE_ENABLED=0",
    "export PAI_CODEX_VOICE_ID=",
    "export PAI_CODEX_VOICE_EVENTS=turn_complete,algorithm_isa_updated",
    "export PAI_CODEX_LEARNING_ENABLED=0",
    "export PAI_CODEX_CHECKPOINT_ENABLED=0",
}
lines = [
    line.strip()
    for line in path.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.lstrip().startswith("#")
]
if set(lines) == expected and len(lines) == len(expected):
    if dry:
        print(f"would remove managed pulse.env: {path}")
    else:
        path.unlink()
        print(f"removed managed pulse.env: {path}")
else:
    print(f"preserved local pulse.env: {path}")
PY
}

remove_agents_block() {
  local path="$1"
  [[ -f "$path" ]] || return 0
  python3 - "$path" "$AGENTS_BEGIN" "$AGENTS_END" "$DRY_RUN" <<'PY'
from __future__ import annotations

from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
begin = sys.argv[2]
end = sys.argv[3]
dry = sys.argv[4] == "1"
old = path.read_text(encoding="utf-8")
pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end) + r"\n?", re.S)
new, count = pattern.subn("", old)
new = re.sub(r"\n{3,}", "\n\n", new).strip() + ("\n" if new.strip() else "")
if count == 0:
    print(f"AGENTS.md: no managed block in {path}")
elif dry:
    print(f"AGENTS.md: would remove managed block from {path}")
elif new == old:
    print(f"AGENTS.md: unchanged {path}")
else:
    path.write_text(new, encoding="utf-8")
    print(f"AGENTS.md: removed managed block from {path}")
PY
}

remove_pai_hook_groups() {
  local path="$1"
  [[ -f "$path" ]] || return 0
  python3 - "$path" "$DRY_RUN" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import sys

path = Path(sys.argv[1])
dry = sys.argv[2] == "1"

with path.open(encoding="utf-8") as handle:
    data = json.load(handle)
if not isinstance(data, dict):
    raise SystemExit(f"{path} must contain a JSON object")


def is_pai_group(group: object) -> bool:
    if not isinstance(group, dict):
        return False
    hooks = group.get("hooks")
    if not isinstance(hooks, list):
        return False
    for hook in hooks:
        if not isinstance(hook, dict):
            continue
        command = str(hook.get("command") or "")
        status = str(hook.get("statusMessage") or "")
        if ".claude/hooks/codex/" in command or status.startswith("PAI ") or " PAI " in f" {status} ":
            return True
    return False


hooks = data.get("hooks")
if hooks is None:
    print(f"hooks.json: no hooks field in {path}")
    raise SystemExit(0)
if not isinstance(hooks, dict):
    raise SystemExit("hooks field is not an object")

removed: dict[str, int] = {}
for event, groups in list(hooks.items()):
    if not isinstance(groups, list):
        continue
    kept = [group for group in groups if not is_pai_group(group)]
    count = len(groups) - len(kept)
    if count:
        removed[event] = count
        hooks[event] = kept

if not removed:
    print(f"hooks.json: no PAI hook groups in {path}")
elif dry:
    print("hooks.json: would remove PAI hook groups: " + ", ".join(f"{event}:{count}" for event, count in sorted(removed.items())))
else:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print("hooks.json: removed PAI hook groups: " + ", ".join(f"{event}:{count}" for event, count in sorted(removed.items())))
PY
}

list_backups() {
  if [[ ! -d "$BACKUP_ROOT" ]]; then
    say "no backups found at $BACKUP_ROOT"
    return 0
  fi
  find "$BACKUP_ROOT" -mindepth 1 -maxdepth 1 -type d -printf '%f\t%p\n' | sort
}

latest_backup() {
  [[ -d "$BACKUP_ROOT" ]] || return 1
  find "$BACKUP_ROOT" -mindepth 1 -maxdepth 1 -type d | sort | tail -n 1
}

resolve_backup() {
  local target="$1"
  if [[ -z "$target" ]]; then
    latest_backup
  elif [[ -d "$target" ]]; then
    printf '%s\n' "$target"
  elif [[ -d "$BACKUP_ROOT/$target" ]]; then
    printf '%s\n' "$BACKUP_ROOT/$target"
  else
    return 1
  fi
}

restore_backup() {
  local target="$1"
  local backup
  backup="$(resolve_backup "$target")" || { echo "backup not found: ${target:-latest}" >&2; exit 1; }
  [[ -f "$backup/manifest.txt" && -d "$backup/files" ]] || {
    echo "not an installer backup: $backup" >&2
    exit 1
  }
  say "backup path: $backup"
  while IFS= read -r rel; do
    [[ -n "$rel" ]] || continue
    local src="$backup/files/$rel"
    local dest="$HOME/$rel"
    [[ -f "$src" ]] || { say "skip missing backup file: $src"; continue; }
    if [[ "$DRY_RUN" -eq 1 ]]; then
      say "would restore $src -> $dest"
    else
      mkdir -p "$(dirname "$dest")"
      cp -p "$src" "$dest"
      say "restored $src -> $dest"
    fi
  done < "$backup/manifest.txt"
}

case "$ACTION" in
  list-backups)
    list_backups
    exit 0
    ;;
  restore-latest)
    restore_backup ""
    exit 0
    ;;
  restore)
    restore_backup "$RESTORE_TARGET"
    exit 0
    ;;
esac

require_python3

for name in session-start prompt-processing pre-tool-use post-tool-use permission-request stop probe; do
  remove_file "$HOME/.claude/hooks/codex/$name.sh"
done
remove_pulse_env
for name in redact log_event pai_context pulse_notify learning; do
  remove_file "$HOME/.claude/hooks/codex/lib/$name.py"
done
remove_dir_if_empty "$HOME/.claude/hooks/codex/lib"
remove_dir_if_empty "$HOME/.claude/hooks/codex"

for skill in pai-algorithm pai-memory pai-isa pai-runtime-audit; do
  remove_tree_files "$HOME/.agents/skills/$skill"
done

for agent in pai_explorer pai_reviewer pai_security_reviewer; do
  remove_file "$HOME/.codex/agents/$agent.toml"
done
remove_dir_if_empty "$HOME/.codex/agents"

remove_agents_block "$HOME/.codex/AGENTS.md"
remove_pai_hook_groups "$HOME/.codex/hooks.json"
remove_file "$HOME/.codex/pai-config.example.toml"

remove_tree_files "$HOME/.claude/codex/skills"
remove_tree_files "$HOME/.claude/codex/agents"
remove_tree_files "$HOME/.claude/codex/tools"
for file in README.md AGENTS.md.template hooks.json.template config.example.toml install-codex.sh uninstall-codex.sh verify-codex.sh install-state/last-install.txt; do
  remove_file "$HOME/.claude/codex/$file"
done
remove_dir_if_empty "$HOME/.claude/codex/install-state"
remove_dir_if_empty "$HOME/.claude/codex"

say "config note: ~/.codex/config.toml is left in place. Use --list-backups and --restore-latest if you need to restore installer backups."
