#!/usr/bin/env bash
set -euo pipefail

SCRIPT_SOURCE="${BASH_SOURCE[0]}"
while [[ -L "$SCRIPT_SOURCE" ]]; do
  SCRIPT_DIR_LINK="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
  SCRIPT_SOURCE="$(readlink "$SCRIPT_SOURCE")"
  [[ "$SCRIPT_SOURCE" != /* ]] && SCRIPT_SOURCE="$SCRIPT_DIR_LINK/$SCRIPT_SOURCE"
done
TEST_DIR="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
PKG_DIR="$(cd "$TEST_DIR/.." && pwd)"

TMP_HOME="$(mktemp -d "${TMPDIR:-/tmp}/pai-codex-clean-home.XXXXXX")"
cleanup() {
  find "$TMP_HOME" -depth -type f -delete 2>/dev/null || true
  find "$TMP_HOME" -depth -type d -empty -delete 2>/dev/null || true
}
trap cleanup EXIT

mkdir -p "$TMP_HOME/.claude/PAI/USER/PROJECTS" \
  "$TMP_HOME/.claude/PAI/USER/TELOS" \
  "$TMP_HOME/.claude/PAI/ALGORITHM" \
  "$TMP_HOME/.claude/PAI/MEMORY/OBSERVABILITY" \
  "$TMP_HOME/.codex"

printf '# Principal\nTest User\n' > "$TMP_HOME/.claude/PAI/USER/PRINCIPAL_IDENTITY.md"
printf '# Runtime Assistant\nTest Assistant\n' > "$TMP_HOME/.claude/PAI/USER/DA_IDENTITY.md"
printf '## Active Projects\n- Existing project\n' > "$TMP_HOME/.claude/PAI/USER/PROJECTS/PROJECTS.md"
printf '# Telos\nBuild useful systems.\n' > "$TMP_HOME/.claude/PAI/USER/TELOS/PRINCIPAL_TELOS.md"
printf '6.3.0\n' > "$TMP_HOME/.claude/PAI/ALGORITHM/LATEST"
printf '# Algorithm\n' > "$TMP_HOME/.claude/PAI/ALGORITHM/v6.3.0.md"

cat > "$TMP_HOME/.codex/AGENTS.md" <<'EOF'
# Existing Codex Instructions

Keep this user content.
EOF

cat > "$TMP_HOME/.codex/hooks.json" <<'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo user-hook",
            "timeout": 1,
            "statusMessage": "User hook"
          }
        ]
      }
    ]
  }
}
EOF

cat > "$TMP_HOME/.codex/config.toml" <<'EOF'
approval_policy = "on-failure"
sandbox_mode = "read-only"

[features]
hooks = false

[sandbox_workspace_write]
writable_roots = [
  "/tmp/user-root",
]
EOF

HOME="$TMP_HOME" "$PKG_DIR/install-codex.sh" >/dev/null
test -f "$TMP_HOME/.claude/codex/AGENTS.md.template"
test -f "$TMP_HOME/.claude/codex/tools/GenerateAgentsMd.ts"
test -f "$TMP_HOME/.claude/hooks/codex/session-start.sh"
test -f "$TMP_HOME/.claude/hooks/codex/lib/learning.py"

HOME="$TMP_HOME" "$PKG_DIR/install-codex.sh" --global >/dev/null

rg -q 'Keep this user content' "$TMP_HOME/.codex/AGENTS.md"
rg -q 'PAI-CODEX:BEGIN' "$TMP_HOME/.codex/AGENTS.md"
rg -q 'echo user-hook' "$TMP_HOME/.codex/hooks.json"
rg -q '.claude/hooks/codex/session-start.sh' "$TMP_HOME/.codex/hooks.json"
rg -q '"/tmp/user-root"' "$TMP_HOME/.codex/config.toml"
rg -q "\"$TMP_HOME/.claude/PAI\"" "$TMP_HOME/.codex/config.toml"
rg -q "\"$TMP_HOME/.claude/hooks/codex\"" "$TMP_HOME/.codex/config.toml"
rg -q 'approval_policy = "on-failure"' "$TMP_HOME/.codex/config.toml"
rg -q 'sandbox_mode = "read-only"' "$TMP_HOME/.codex/config.toml"
rg -q 'hooks = true' "$TMP_HOME/.codex/config.toml"

for skill in pai-algorithm pai-memory pai-isa pai-runtime-audit; do
  test -f "$TMP_HOME/.agents/skills/$skill/SKILL.md"
done
for agent in pai_explorer pai_reviewer pai_security_reviewer; do
  test -f "$TMP_HOME/.codex/agents/$agent.toml"
  rg -q 'sandbox_mode = "read-only"' "$TMP_HOME/.codex/agents/$agent.toml"
done
for hook in session-start prompt-processing pre-tool-use post-tool-use permission-request stop probe; do
  test -x "$TMP_HOME/.claude/hooks/codex/$hook.sh"
done
test -f "$TMP_HOME/.claude/hooks/codex/pulse.env"
rg -q '^export PAI_CODEX_PULSE_ENABLED=0$' "$TMP_HOME/.claude/hooks/codex/pulse.env"
rg -q '^export PAI_CODEX_VOICE_ENABLED=0$' "$TMP_HOME/.claude/hooks/codex/pulse.env"
rg -q '^export PAI_CODEX_VOICE_ID=$' "$TMP_HOME/.claude/hooks/codex/pulse.env"
rg -q '^export PAI_CODEX_LEARNING_ENABLED=0$' "$TMP_HOME/.claude/hooks/codex/pulse.env"
HOME="$TMP_HOME" "$TMP_HOME/.agents/skills/pai-runtime-audit/scripts/runtime-audit.sh" >/dev/null

sha_before="$(sha256sum "$TMP_HOME/.codex/AGENTS.md" "$TMP_HOME/.codex/hooks.json" "$TMP_HOME/.codex/config.toml")"
backup_count_before="$(find "$TMP_HOME/.claude/codex/backups" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
HOME="$TMP_HOME" "$PKG_DIR/install-codex.sh" --global >/dev/null
sha_after="$(sha256sum "$TMP_HOME/.codex/AGENTS.md" "$TMP_HOME/.codex/hooks.json" "$TMP_HOME/.codex/config.toml")"
backup_count_after="$(find "$TMP_HOME/.claude/codex/backups" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
[[ "$sha_before" == "$sha_after" ]] || { echo "global reinstall changed merged files" >&2; exit 1; }
[[ "$backup_count_before" == "$backup_count_after" ]] || { echo "idempotent reinstall created backups" >&2; exit 1; }

printf '\nexport PAI_CODEX_PULSE_URL=http://localhost:31337\n' >> "$TMP_HOME/.claude/hooks/codex/pulse.env"
HOME="$TMP_HOME" "$PKG_DIR/install-codex.sh" --global >/dev/null
rg -q '^export PAI_CODEX_PULSE_URL=http://localhost:31337$' "$TMP_HOME/.claude/hooks/codex/pulse.env"

HOME="$TMP_HOME" "$PKG_DIR/uninstall-codex.sh" --dry-run >/dev/null
HOME="$TMP_HOME" "$PKG_DIR/uninstall-codex.sh" >/dev/null

rg -q 'Keep this user content' "$TMP_HOME/.codex/AGENTS.md"
! rg -q 'PAI-CODEX:BEGIN' "$TMP_HOME/.codex/AGENTS.md"
rg -q 'echo user-hook' "$TMP_HOME/.codex/hooks.json"
! rg -q '.claude/hooks/codex/session-start.sh' "$TMP_HOME/.codex/hooks.json"
rg -q '"/tmp/user-root"' "$TMP_HOME/.codex/config.toml"

test ! -e "$TMP_HOME/.agents/skills/pai-algorithm/SKILL.md"
test ! -e "$TMP_HOME/.codex/agents/pai_explorer.toml"
test ! -e "$TMP_HOME/.claude/codex/tools/GenerateAgentsMd.ts"
test ! -e "$TMP_HOME/.claude/hooks/codex/session-start.sh"
test -f "$TMP_HOME/.claude/hooks/codex/pulse.env"

HOME="$TMP_HOME" "$PKG_DIR/uninstall-codex.sh" --list-backups >/dev/null
HOME="$TMP_HOME" "$PKG_DIR/uninstall-codex.sh" --restore-latest --dry-run >/dev/null

echo "clean-home acceptance passed"
