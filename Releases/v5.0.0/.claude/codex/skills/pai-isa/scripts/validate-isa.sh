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

effort_line="$(rg -m1 '^effort:' "$isa_path" || true)"
resolved_effort='E1'
if [[ -n "$effort_line" ]]; then
  raw_effort="$(printf '%s\n' "$effort_line" | sed -E 's/^effort:[[:space:]]*//; s/[[:space:]]*(#.*)?$//')"
  raw_effort="${raw_effort#\"}"
  raw_effort="${raw_effort%\"}"
  raw_effort="${raw_effort#\'}"
  raw_effort="${raw_effort%\'}"
  raw_effort="${raw_effort#"${raw_effort%%[![:space:]]*}"}"
  raw_effort="${raw_effort%"${raw_effort##*[![:space:]]}"}"
  raw_effort="${raw_effort^^}"
  case "$raw_effort" in
    E1|E2|E3|E4|E5) resolved_effort="$raw_effort" ;;
  esac
fi

required_sections=()
case "$resolved_effort" in
  E1)
    required_sections=('## Goal' '## Criteria')
    ;;
  E2)
    required_sections=('## Goal' '## Criteria' '## Problem' '## Test Strategy')
    ;;
  E3)
    required_sections=('## Goal' '## Criteria' '## Problem' '## Test Strategy' '## Vision' '## Out of Scope' '## Constraints' '## Features')
    ;;
  E4|E5)
    required_sections=('## Problem' '## Vision' '## Out of Scope' '## Principles' '## Constraints' '## Goal' '## Criteria' '## Test Strategy' '## Features' '## Decisions' '## Changelog' '## Verification')
    ;;
esac

missing_required_sections=0
for heading in "${required_sections[@]}"; do
  if ! rg -q "^${heading}$" "$isa_path"; then
    echo "missing required section for ${resolved_effort}: ${heading}" >&2
    missing_required_sections=1
  fi
done

if [[ $missing_required_sections -ne 0 ]]; then
  exit 1
fi

require '^- \[[ x]\] ISC-[0-9]+(\.[0-9]+)?:' 'at least one ISC'

if rg -q '^- \[x\] ISC-|^phase: complete$' "$isa_path"; then
  require '^## Verification$' 'Verification section for completed criteria'
  require '^- ISC-[0-9]+(\.[0-9]+)?:' 'verification entry for completed criteria'
fi

echo "ok: $isa_path"
