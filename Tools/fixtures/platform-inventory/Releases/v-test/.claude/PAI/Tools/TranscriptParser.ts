#!/usr/bin/env bun

interface StopPayload {
  transcript_path: string;
  hook_event_name: "Stop";
}

function readLastAssistant(payload: StopPayload, lines: string[]): string {
  let last = "";

  for (const line of lines) {
    const entry = JSON.parse(line);
    if (entry.type === "assistant" && entry.message?.content) {
      last = String(entry.message.content);
    }
  }

  return `${payload.transcript_path}: ${last}`;
}

readLastAssistant({ transcript_path: "~/.claude/projects/example/session.jsonl", hook_event_name: "Stop" }, []);
