# Platform Inventory Fixture

This fixture gives `Tools/platform-inventory.ts` representative Claude-specific
couplings without depending on release artifacts.

```json
{
  "env": {
    "PAI_DIR": "${HOME}/.claude",
    "CLAUDE_DIR": "$HOME/.claude"
  },
  "hooks": {
    "PreToolUse": [
      { "matcher": "Task", "hooks": [{ "type": "command", "command": "${PAI_DIR}/hooks/SecurityValidator.hook.ts" }] }
    ],
    "Stop": [
      { "hooks": [{ "type": "command", "command": "${PAI_DIR}/hooks/VoiceCompletion.hook.ts" }] }
    ]
  },
  "statusLine": {
    "type": "command",
    "command": "$PAI_DIR/statusline-command.sh"
  }
}
```

Hook output examples:

```ts
console.log(JSON.stringify({ continue: true }));
console.log(JSON.stringify({ decision: "ask", message: "Confirm?" }));
process.exit(2);
```

Transcript examples:

```ts
const input = { transcript_path: "~/.claude/projects/example/session.jsonl" };
if (entry.type === "assistant" && entry.message?.content) {
  // Claude transcript content.
}
```

Instruction and CLI examples:

```bash
claude --version
claude -p "hello"
```

`CLAUDE.md`, `BuildCLAUDE`, `Claude Code`, `@anthropic-ai/claude-code`,
`AskUserQuestion`, `Skill`, `Read`, `Write`, `Edit`, `MultiEdit`.
