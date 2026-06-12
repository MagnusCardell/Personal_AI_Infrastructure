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
FORCE_REPLACE=0
GENERATE_AGENTS=0

usage() {
  cat <<'EOF'
usage: install-codex.sh [--global|--pai-local] [--dry-run] [--force-replace] [--generate-agents]

  --pai-local        stage PAI-local Codex files only (default)
  --global           activate Codex-facing ~/.codex and ~/.agents files
  --dry-run          print intended changes without writing
  --force-replace    explicitly replace managed global Codex files instead of merging
  --generate-agents  regenerate ~/.codex/AGENTS.md from live PAI state; requires --global
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --global) SCOPE="global" ;;
    --pai-local) SCOPE="pai-local" ;;
    --dry-run) DRY_RUN=1 ;;
    --force-replace) FORCE_REPLACE=1 ;;
    --generate-agents) GENERATE_AGENTS=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

PAI_DIR="${PAI_DIR:-$HOME/.claude/PAI}"
HOOK_DEST="$HOME/.claude/hooks/codex"
LOCAL_DEST="$HOME/.claude/codex"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
BACKUP_ROOT="$LOCAL_DEST/backups"
BACKUP_DIR="$BACKUP_ROOT/$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_CREATED=0
CHANGED=()

AGENTS_BEGIN='<!-- PAI-CODEX:BEGIN managed by Personal_AI_Infrastructure -->'
AGENTS_END='<!-- PAI-CODEX:END managed by Personal_AI_Infrastructure -->'

say() {
  printf '%s\n' "$*"
}

changed() {
  CHANGED+=("$1")
}

require_python3() {
  if ! command -v python3 >/dev/null 2>&1; then
    say "python3 is required for merge-safe Codex install."
    exit 1
  fi
}

backup_if_needed() {
  local dest="$1"
  [[ -e "$dest" ]] || return 0
  local rel
  rel="${dest#"$HOME"/}"
  local backup="$BACKUP_DIR/files/$rel"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "would back up $dest -> $backup"
    return 0
  fi
  mkdir -p "$(dirname "$backup")"
  cp -p "$dest" "$backup"
  mkdir -p "$BACKUP_DIR"
  printf '%s\n' "$rel" >> "$BACKUP_DIR/manifest.txt"
  BACKUP_CREATED=1
  say "backup: $dest -> $backup"
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
      *.sh|*.ts) mode="0755" ;;
    esac
    install_file "$src" "$dest_dir/$rel" "$mode"
  done < <(find "$src_dir" -type f ! -path '*/__pycache__/*' ! -name '*.pyc' | sort)
}

install_pulse_env() {
  local src="$SCRIPT_DIR/hooks/pulse.env"
  local dest="$HOOK_DEST/pulse.env"
  [[ -f "$src" ]] || return 0

  if [[ ! -e "$dest" ]]; then
    install_file "$src" "$dest" "0644"
    return 0
  fi

  if cmp -s "$src" "$dest"; then
    say "pulse.env: unchanged $dest"
    return 0
  fi

  if [[ "$FORCE_REPLACE" -eq 1 ]]; then
    install_file "$src" "$dest" "0644"
    say "pulse.env: force-replaced $dest"
    return 0
  fi

  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "pulse.env: would preserve existing local file at $dest"
  else
    say "pulse.env: preserved existing local file at $dest; use --force-replace to install package defaults"
  fi
}

install_hooks() {
  while IFS= read -r src; do
    local rel="${src#$SCRIPT_DIR/hooks/}"
    local mode="0644"
    case "$src" in
      *.sh) mode="0755" ;;
    esac
    install_file "$src" "$HOOK_DEST/$rel" "$mode"
  done < <(find "$SCRIPT_DIR/hooks" -type f ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name 'pulse.env' | sort)
  install_pulse_env
}

agents_action() {
  local dest="$1"
  local template="$2"
  python3 - "$dest" "$template" "$FORCE_REPLACE" "$AGENTS_BEGIN" "$AGENTS_END" action <<'PY'
from __future__ import annotations

from pathlib import Path
import re
import sys

dest = Path(sys.argv[1])
template = Path(sys.argv[2])
force = sys.argv[3] == "1"
begin = sys.argv[4]
end = sys.argv[5]

old = dest.read_text(encoding="utf-8") if dest.exists() else ""
body = template.read_text(encoding="utf-8").strip()
block = f"{begin}\n{body}\n{end}\n"
pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end) + r"\n?", re.S)

if force:
    new = block
    action = "force-replace"
elif not dest.exists():
    new = block
    action = "create managed block"
elif pattern.search(old):
    new = pattern.sub(block, old)
    action = "replace managed block"
else:
    sep = "" if old.endswith("\n\n") or not old else "\n\n"
    new = old + sep + block
    action = "append managed block"

print("unchanged" if old == new else action)
PY
}

write_agents() {
  local dest="$1"
  local template="$2"
  python3 - "$dest" "$template" "$FORCE_REPLACE" "$AGENTS_BEGIN" "$AGENTS_END" write <<'PY'
from __future__ import annotations

from pathlib import Path
import re
import sys

dest = Path(sys.argv[1])
template = Path(sys.argv[2])
force = sys.argv[3] == "1"
begin = sys.argv[4]
end = sys.argv[5]

old = dest.read_text(encoding="utf-8") if dest.exists() else ""
body = template.read_text(encoding="utf-8").strip()
block = f"{begin}\n{body}\n{end}\n"
pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end) + r"\n?", re.S)

if force or not dest.exists():
    new = block
elif pattern.search(old):
    new = pattern.sub(block, old)
else:
    sep = "" if old.endswith("\n\n") or not old else "\n\n"
    new = old + sep + block

dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(new.rstrip() + "\n", encoding="utf-8")
PY
}

merge_agents() {
  local dest="$1"
  local template="$2"
  local action
  action="$(agents_action "$dest" "$template")"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "AGENTS.md: would $action at $dest"
    [[ "$action" == "unchanged" ]] || changed "$dest"
    return 0
  fi
  if [[ "$action" == "unchanged" ]]; then
    say "AGENTS.md: unchanged $dest"
    return 0
  fi
  backup_if_needed "$dest"
  write_agents "$dest" "$template"
  say "AGENTS.md: $action at $dest"
  changed "$dest"
}

agents_has_generated_block() {
  local dest="$1"
  [[ -f "$dest" ]] || return 1
  python3 - "$dest" "$AGENTS_BEGIN" "$AGENTS_END" <<'PY'
from __future__ import annotations

from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
begin = sys.argv[2]
end = sys.argv[3]
text = path.read_text(encoding="utf-8", errors="replace")
match = re.search(re.escape(begin) + r"(?P<body>.*?)" + re.escape(end), text, re.S)
if match and "## Managed Runtime Summary" in match.group("body"):
    raise SystemExit(0)
raise SystemExit(1)
PY
}

hooks_action() {
  local dest="$1"
  local template="$2"
  python3 - "$dest" "$template" "$FORCE_REPLACE" action <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import sys

dest = Path(sys.argv[1])
template = Path(sys.argv[2])
force = sys.argv[3] == "1"


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


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


def merged(existing: dict, pai: dict) -> dict:
    if force or not existing:
        return pai
    if "hooks" in existing and not isinstance(existing["hooks"], dict):
        raise SystemExit("existing hooks.json has non-object hooks field")
    result = dict(existing)
    result_hooks = dict(result.get("hooks") or {})
    pai_hooks = pai.get("hooks") or {}
    for event, groups in pai_hooks.items():
        old_groups = result_hooks.get(event, [])
        if not isinstance(old_groups, list):
            raise SystemExit(f"existing hooks.{event} is not a list")
        kept = [group for group in old_groups if not is_pai_group(group)]
        result_hooks[event] = kept + groups
    result["hooks"] = result_hooks
    return result


existing = load(dest)
pai = load(template)
new = merged(existing, pai)
old_text = json.dumps(existing, indent=2, sort_keys=False) + "\n" if existing else ""
new_text = json.dumps(new, indent=2, sort_keys=False) + "\n"
events = sorted((pai.get("hooks") or {}).keys())
if dest.exists() and old_text == new_text:
    print("unchanged")
elif force:
    print("force-replace hooks.json")
else:
    print("merge PAI hook groups for events: " + ", ".join(events))
PY
}

write_hooks_json() {
  local dest="$1"
  local template="$2"
  python3 - "$dest" "$template" "$FORCE_REPLACE" write <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import sys

dest = Path(sys.argv[1])
template = Path(sys.argv[2])
force = sys.argv[3] == "1"


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


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


existing = load(dest)
pai = load(template)
if force or not existing:
    new = pai
else:
    if "hooks" in existing and not isinstance(existing["hooks"], dict):
        raise SystemExit("existing hooks.json has non-object hooks field")
    new = dict(existing)
    result_hooks = dict(new.get("hooks") or {})
    for event, groups in (pai.get("hooks") or {}).items():
        old_groups = result_hooks.get(event, [])
        if not isinstance(old_groups, list):
            raise SystemExit(f"existing hooks.{event} is not a list")
        result_hooks[event] = [group for group in old_groups if not is_pai_group(group)] + groups
    new["hooks"] = result_hooks

dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(new, indent=2, sort_keys=False) + "\n", encoding="utf-8")
PY
}

merge_hooks_json() {
  local dest="$1"
  local template="$2"
  local action
  action="$(hooks_action "$dest" "$template")"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "hooks.json: would $action at $dest"
    [[ "$action" == "unchanged" ]] || changed "$dest"
    return 0
  fi
  if [[ "$action" == "unchanged" ]]; then
    say "hooks.json: unchanged $dest"
    return 0
  fi
  backup_if_needed "$dest"
  write_hooks_json "$dest" "$template"
  say "hooks.json: $action at $dest"
  changed "$dest"
}

run_agents_generator() {
  local generator="$SCRIPT_DIR/tools/GenerateAgentsMd.ts"
  local dest="$CODEX_HOME/AGENTS.md"
  [[ -f "$generator" ]] || { echo "missing AGENTS generator: $generator" >&2; exit 1; }
  if ! command -v bun >/dev/null 2>&1; then
    echo "bun is required for --generate-agents" >&2
    exit 1
  fi
  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "AGENTS.md: dry-run generator for $dest"
    bun "$generator" --dry-run --output "$dest" --pai-dir "$PAI_DIR"
    changed "$dest"
    return 0
  fi
  backup_if_needed "$dest"
  bun "$generator" --output "$dest" --pai-dir "$PAI_DIR"
  changed "$dest"
}

config_plan() {
  local config_path="$1"
  python3 - "$config_path" "$HOME/.claude/PAI" "$HOME/.claude/hooks/codex" "$FORCE_REPLACE" plan <<'PY'
from __future__ import annotations

from pathlib import Path
import re
import sys

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - depends on Python version
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:
        raise SystemExit("cannot parse TOML safely: install Python 3.11+ or the tomli package")

config_path = Path(sys.argv[1])
required_roots = [sys.argv[2], sys.argv[3]]
force = sys.argv[4] == "1"
text = config_path.read_text(encoding="utf-8") if config_path.exists() else ""

try:
    data = tomllib.loads(text) if text.strip() else {}
except tomllib.TOMLDecodeError as exc:
    raise SystemExit(f"cannot parse existing TOML safely: {exc}")

roots = data.get("sandbox_workspace_write", {}).get("writable_roots", [])
if roots is None:
    roots = []
if not isinstance(roots, list) or not all(isinstance(root, str) for root in roots):
    raise SystemExit("sandbox_workspace_write.writable_roots must be a string array")

result_roots = list(dict.fromkeys(roots + required_roots))
features = data.get("features", {})
hooks_enabled = isinstance(features, dict) and features.get("hooks") is True
needs_top = force or "approval_policy" not in data or "sandbox_mode" not in data
changed = (
    result_roots != roots
    or not hooks_enabled
    or "features" not in data
    or needs_top
    or not config_path.exists()
)
print("current_roots=" + repr(roots))
print("result_roots=" + repr(result_roots))
print("action=" + ("update config.toml" if changed else "unchanged"))
PY
}

write_config() {
  local config_path="$1"
  python3 - "$config_path" "$HOME/.claude/PAI" "$HOME/.claude/hooks/codex" "$FORCE_REPLACE" write <<'PY'
from __future__ import annotations

from pathlib import Path
import re
import sys

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - depends on Python version
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:
        raise SystemExit("cannot parse TOML safely: install Python 3.11+ or the tomli package")

config_path = Path(sys.argv[1])
required_roots = [sys.argv[2], sys.argv[3]]
force = sys.argv[4] == "1"
text = config_path.read_text(encoding="utf-8") if config_path.exists() else ""

try:
    data = tomllib.loads(text) if text.strip() else {}
except tomllib.TOMLDecodeError as exc:
    raise SystemExit(f"cannot parse existing TOML safely: {exc}")

roots = data.get("sandbox_workspace_write", {}).get("writable_roots", [])
if roots is None:
    roots = []
if not isinstance(roots, list) or not all(isinstance(root, str) for root in roots):
    raise SystemExit("sandbox_workspace_write.writable_roots must be a string array")
result_roots = list(dict.fromkeys(roots + required_roots))


def split_prefix(source: str) -> tuple[str, str]:
    match = re.search(r"(?m)^\[", source)
    if not match:
        return source, ""
    return source[:match.start()], source[match.start():]


def set_top_level(source: str, key: str, value: str, *, only_if_absent: bool) -> str:
    prefix, rest = split_prefix(source)
    pattern = re.compile(rf"(?m)^{re.escape(key)}\s*=.*$")
    line = f'{key} = "{value}"'
    if pattern.search(prefix):
        if only_if_absent:
            return source
        prefix = pattern.sub(line, prefix)
    else:
        prefix = prefix.rstrip() + ("\n" if prefix.strip() else "") + line + "\n"
    return prefix + rest


def ensure_section_bool(source: str, section: str, key: str, value: bool) -> str:
    header = f"[{section}]"
    rendered = "true" if value else "false"
    section_re = re.compile(rf"(?ms)^{re.escape(header)}\s*\n(?P<body>.*?)(?=^\[|\Z)")
    match = section_re.search(source)
    line = f"{key} = {rendered}"
    if not match:
        return source.rstrip() + f"\n\n{header}\n{line}\n"
    body = match.group("body")
    key_re = re.compile(rf"(?m)^{re.escape(key)}\s*=.*$")
    if key_re.search(body):
        body = key_re.sub(line, body)
    else:
        body = line + "\n" + body
    return source[:match.start("body")] + body + source[match.end("body"):]


def ensure_writable_roots(source: str, roots: list[str]) -> str:
    header = "[sandbox_workspace_write]"
    formatted = "writable_roots = [\n" + "".join(f'  "{root}",\n' for root in roots) + "]"
    section_re = re.compile(r"(?ms)^\[sandbox_workspace_write\]\s*\n(?P<body>.*?)(?=^\[|\Z)")
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


new = text
new = set_top_level(new, "approval_policy", "on-request", only_if_absent=not force)
new = set_top_level(new, "sandbox_mode", "workspace-write", only_if_absent=not force)
new = ensure_section_bool(new, "features", "hooks", True)
new = ensure_writable_roots(new, result_roots)

config_path.parent.mkdir(parents=True, exist_ok=True)
config_path.write_text(new.rstrip() + "\n", encoding="utf-8")
PY
}

configure_codex_config() {
  local config_path="$CODEX_HOME/config.toml"
  local example_path="$CODEX_HOME/pai-config.example.toml"
  install_file "$SCRIPT_DIR/config.example.toml" "$example_path" "0644"

  local plan
  plan="$(config_plan "$config_path")"
  say "$plan"
  if grep -q '^action=unchanged$' <<<"$plan"; then
    say "config.toml: unchanged $config_path"
    return 0
  fi
  if [[ "$DRY_RUN" -eq 1 ]]; then
    say "config.toml: would merge required PAI settings into $config_path"
    changed "$config_path"
    return 0
  fi
  backup_if_needed "$config_path"
  write_config "$config_path"
  say "config.toml: merged required PAI settings into $config_path"
  changed "$config_path"
}

require_python3

if [[ "$GENERATE_AGENTS" -eq 1 && "$SCOPE" != "global" ]]; then
  echo "--generate-agents requires --global" >&2
  exit 2
fi

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
say "force replace: $FORCE_REPLACE"

install_hooks
install_file "$SCRIPT_DIR/README.md" "$LOCAL_DEST/README.md" "0644"
install_file "$SCRIPT_DIR/AGENTS.md.template" "$LOCAL_DEST/AGENTS.md.template" "0644"
install_file "$SCRIPT_DIR/hooks.json.template" "$LOCAL_DEST/hooks.json.template" "0644"
install_file "$SCRIPT_DIR/config.example.toml" "$LOCAL_DEST/config.example.toml" "0644"
install_file "$SCRIPT_DIR/install-codex.sh" "$LOCAL_DEST/install-codex.sh" "0755"
install_file "$SCRIPT_DIR/uninstall-codex.sh" "$LOCAL_DEST/uninstall-codex.sh" "0755"
install_file "$SCRIPT_DIR/verify-codex.sh" "$LOCAL_DEST/verify-codex.sh" "0755"
install_tree "$SCRIPT_DIR/tools" "$LOCAL_DEST/tools" "0644"

if [[ "$SCOPE" == "global" ]]; then
  if [[ "$GENERATE_AGENTS" -eq 1 ]]; then
    run_agents_generator
  elif [[ "$FORCE_REPLACE" -eq 0 ]] && agents_has_generated_block "$CODEX_HOME/AGENTS.md"; then
    say "AGENTS.md: preserved generated managed block at $CODEX_HOME/AGENTS.md; use --generate-agents to refresh or --force-replace to install the static template"
  else
    merge_agents "$CODEX_HOME/AGENTS.md" "$SCRIPT_DIR/AGENTS.md.template"
  fi
  merge_hooks_json "$CODEX_HOME/hooks.json" "$SCRIPT_DIR/hooks.json.template"
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
    printf 'force_replace=%s\n' "$FORCE_REPLACE"
    printf 'backup_dir=%s\n' "$BACKUP_DIR"
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

if [[ "$DRY_RUN" -eq 1 ]]; then
  say "backup directory if needed: $BACKUP_DIR"
elif [[ "$BACKUP_CREATED" -eq 1 ]]; then
  say "backup directory: $BACKUP_DIR"
else
  say "backup directory: none created"
fi

say "verify with: $LOCAL_DEST/verify-codex.sh --installed"
say "AGENTS regeneration preview: bun $LOCAL_DEST/tools/GenerateAgentsMd.ts --dry-run"
say "skill dispatch: $HOOK_DEST/skills/dispatch.sh isa_append <ISA.md> <decisions|changelog|verification> <content>"
