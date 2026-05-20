#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: validate-isa.sh /absolute/path/to/ISA.md" >&2
  exit 2
fi

isa_path="$1"
case "$isa_path" in
  "$HOME/.claude/PAI/MEMORY/WORK/"*/ISA.md) ;;
  *)
    echo "invalid ISA path: expected ~/.claude/PAI/MEMORY/WORK/{slug}/ISA.md" >&2
    exit 1
    ;;
esac

test -f "$isa_path"

require() {
  local pattern="$1"
  local label="$2"
  if ! rg -q "$pattern" "$isa_path"; then
    echo "invalid ISA: missing $label" >&2
    exit 1
  fi
}

require '^---$' 'frontmatter delimiter'
for field in task slug effort phase progress mode started updated; do
  require "^${field}:" "frontmatter field ${field}"
done

require '^## Goal$' 'Goal section'
require '^## Criteria$' 'Criteria section'
require '^- \[[ x]\] ISC-[0-9]+(\.[0-9]+)?:' 'at least one ISC'

if rg -q '^- \[x\] ISC-|^phase: complete$' "$isa_path"; then
  require '^## Verification$' 'Verification section for completed criteria'
  require '^- ISC-[0-9]+(\.[0-9]+)?:' 'verification entry for completed criteria'
fi

echo "ok: $isa_path"
