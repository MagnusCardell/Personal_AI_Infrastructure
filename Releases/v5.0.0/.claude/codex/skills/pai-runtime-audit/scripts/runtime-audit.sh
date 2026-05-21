#!/usr/bin/env bash
set -euo pipefail

failures=0
warnings=0
PAI_ROOT="${PAI_DIR:-$HOME/.claude/PAI}"

report() {
  local level="$1"
  local check="$2"
  local detail="$3"
  printf '%s|%s|%s\n' "$level" "$check" "$detail"
  case "$level" in
    FAIL) failures=$((failures + 1)) ;;
    WARN) warnings=$((warnings + 1)) ;;
  esac
}

check_file() {
  local label="$1"
  local path="$2"
  if [[ -f "$path" ]]; then
    report OK "$label" "$path"
  else
    report WARN "$label" "missing: $path"
  fi
}

check_required_file() {
  local label="$1"
  local path="$2"
  if [[ -f "$path" ]]; then
    report OK "$label" "$path"
  else
    report FAIL "$label" "missing: $path"
  fi
}

check_dir() {
  local label="$1"
  local path="$2"
  if [[ -d "$path" ]]; then
    report OK "$label" "$path"
  else
    report WARN "$label" "missing: $path"
  fi
}

check_exec() {
  local label="$1"
  local path="$2"
  if [[ -x "$path" ]]; then
    report OK "$label" "$path"
  elif [[ -e "$path" ]]; then
    report FAIL "$label" "not executable: $path"
  else
    report FAIL "$label" "missing: $path"
  fi
}

resolve_algorithm() {
  local latest="$PAI_ROOT/ALGORITHM/LATEST"
  if [[ ! -f "$latest" ]]; then
    report WARN "algorithm_pointer" "missing: $latest"
    return 0
  fi

  local pointer
  pointer="$(sed -n '1p' "$latest" | tr -d '\r')"
  if [[ -z "$pointer" ]]; then
    report WARN "algorithm_pointer" "empty: $latest"
    return 0
  fi

  local candidate=""
  if [[ "$pointer" = /* ]]; then
    case "$pointer" in
      "$PAI_ROOT/ALGORITHM/"*) candidate="$pointer" ;;
      *) report WARN "algorithm_pointer" "outside PAI algorithm root: $pointer"; return 0 ;;
    esac
  elif [[ -f "$PAI_ROOT/ALGORITHM/$pointer" ]]; then
    candidate="$PAI_ROOT/ALGORITHM/$pointer"
  elif [[ -f "$PAI_ROOT/ALGORITHM/v$pointer.md" ]]; then
    candidate="$PAI_ROOT/ALGORITHM/v$pointer.md"
  elif [[ -f "$PAI_ROOT/ALGORITHM/$pointer.md" ]]; then
    candidate="$PAI_ROOT/ALGORITHM/$pointer.md"
  fi

  if [[ -n "$candidate" && -f "$candidate" ]]; then
    report OK "algorithm_pointer" "$pointer -> $candidate"
  else
    report WARN "algorithm_pointer" "unresolved: $pointer"
  fi
}

report OK "pai_root" "$PAI_ROOT"
check_dir "pai_root_exists" "$PAI_ROOT"
check_file "principal_identity" "$PAI_ROOT/USER/PRINCIPAL_IDENTITY.md"
check_file "da_identity" "$PAI_ROOT/USER/DA_IDENTITY.md"
check_file "projects" "$PAI_ROOT/USER/PROJECTS/PROJECTS.md"
check_file "telos" "$PAI_ROOT/USER/TELOS/PRINCIPAL_TELOS.md"
resolve_algorithm
check_dir "memory_work" "$PAI_ROOT/MEMORY/WORK"
check_dir "memory_observability" "$PAI_ROOT/MEMORY/OBSERVABILITY"
check_dir "memory_learning" "$PAI_ROOT/MEMORY/LEARNING"

check_dir "codex_hooks_dir" "$HOME/.claude/hooks/codex"
for hook in session-start prompt-processing pre-tool-use post-tool-use permission-request stop; do
  check_exec "hook_$hook" "$HOME/.claude/hooks/codex/$hook.sh"
done
check_required_file "hook_lib_redact" "$HOME/.claude/hooks/codex/lib/redact.py"
check_required_file "hook_lib_log_event" "$HOME/.claude/hooks/codex/lib/log_event.py"
check_required_file "hook_lib_pai_context" "$HOME/.claude/hooks/codex/lib/pai_context.py"

if [[ -f "$HOME/.codex/AGENTS.md" ]]; then
  report OK "codex_agents_instructions" "$HOME/.codex/AGENTS.md"
elif [[ -f "$HOME/.claude/codex/AGENTS.md.template" ]]; then
  report OK "codex_agents_instructions" "staged: $HOME/.claude/codex/AGENTS.md.template"
else
  report WARN "codex_agents_instructions" "missing installed or staged instructions"
fi

if [[ -f "$HOME/.codex/hooks.json" ]]; then
  if python3 -m json.tool "$HOME/.codex/hooks.json" >/dev/null 2>&1; then
    report OK "codex_hooks_json" "$HOME/.codex/hooks.json"
  else
    report FAIL "codex_hooks_json" "invalid JSON: $HOME/.codex/hooks.json"
  fi
elif [[ -f "$HOME/.claude/codex/hooks.json.template" ]]; then
  report OK "codex_hooks_json" "staged: $HOME/.claude/codex/hooks.json.template"
else
  report WARN "codex_hooks_json" "missing installed or staged hook config"
fi

if [[ -f "$HOME/.codex/config.toml" ]]; then
  report OK "codex_config" "$HOME/.codex/config.toml"
  if rg -q 'hooks\s*=\s*true' "$HOME/.codex/config.toml"; then
    report OK "codex_hooks_enabled" "$HOME/.codex/config.toml"
  else
    report WARN "codex_hooks_enabled" "hooks flag not found in $HOME/.codex/config.toml"
  fi
elif [[ -f "$HOME/.claude/codex/config.example.toml" ]]; then
  report OK "codex_config" "staged: $HOME/.claude/codex/config.example.toml"
else
  report WARN "codex_config" "missing installed or staged config"
fi

for skill in pai-algorithm pai-memory pai-isa pai-runtime-audit; do
  if [[ -f "$HOME/.agents/skills/$skill/SKILL.md" ]]; then
    report OK "skill_$skill" "$HOME/.agents/skills/$skill/SKILL.md"
  elif [[ -f "$HOME/.claude/codex/skills/$skill/SKILL.md" ]]; then
    report OK "skill_$skill" "staged: $HOME/.claude/codex/skills/$skill/SKILL.md"
  else
    report WARN "skill_$skill" "missing installed or staged skill"
  fi
done

for agent in pai_explorer pai_reviewer pai_security_reviewer; do
  agent_path=""
  if [[ -f "$HOME/.codex/agents/$agent.toml" ]]; then
    agent_path="$HOME/.codex/agents/$agent.toml"
  elif [[ -f "$HOME/.claude/codex/agents/$agent.toml" ]]; then
    agent_path="$HOME/.claude/codex/agents/$agent.toml"
  fi

  if [[ -z "$agent_path" ]]; then
    report WARN "agent_$agent" "missing installed or staged agent"
  elif rg -q 'sandbox_mode\s*=\s*"read-only"' "$agent_path"; then
    report OK "agent_$agent" "$agent_path"
  else
    report FAIL "agent_$agent" "not read-only: $agent_path"
  fi
done

if [[ -d "$HOME/.claude/hooks/codex" ]]; then
  if rg -n 'tar\s|retention|backup' "$HOME/.claude/hooks/codex" >/dev/null 2>&1; then
    report FAIL "runtime_backup_behavior" "review hidden maintenance keywords in hooks"
  elif rg -n 'git commit' "$HOME/.claude/hooks/codex" >/dev/null 2>&1; then
    if [[ -f "$HOME/.claude/hooks/codex/post-tool-use.sh" ]] \
      && [[ -f "$HOME/.claude/hooks/codex/pulse.env" ]] \
      && rg -q 'PAI_CODEX_CHECKPOINT_ENABLED' "$HOME/.claude/hooks/codex/post-tool-use.sh" \
      && rg -q '^export PAI_CODEX_CHECKPOINT_ENABLED=0$' "$HOME/.claude/hooks/codex/pulse.env"; then
      report OK "runtime_backup_behavior" "git checkpoint path is opt-in and disabled by default"
    else
      report FAIL "runtime_backup_behavior" "review ungated git commit keyword in hooks"
    fi
  else
    report OK "runtime_backup_behavior" "no hidden maintenance keywords in hooks"
  fi
else
  report WARN "runtime_backup_behavior" "hooks directory missing"
fi

report OK "summary" "failures=$failures warnings=$warnings"
exit "$failures"
