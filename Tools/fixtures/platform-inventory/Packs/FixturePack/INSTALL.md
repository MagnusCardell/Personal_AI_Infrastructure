# Fixture Pack Install

This pack installer writes to Claude-specific locations today.

```bash
CLAUDE_DIR="$HOME/.claude"
mkdir -p "$CLAUDE_DIR/skills/FixturePack"
cp src/SKILL.md "$CLAUDE_DIR/skills/FixturePack/SKILL.md"
```

Use AskUserQuestion before installing.
