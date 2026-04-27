#!/usr/bin/env bun

interface HookInput {
  session_id: string;
  tool_name: "Read" | "Write" | "Edit" | "Task";
  tool_input: Record<string, unknown>;
}

function handle(input: HookInput): void {
  if (input.tool_name === "Task") {
    console.log(JSON.stringify({ decision: "ask", message: "Confirm Task use" }));
    return;
  }

  if (input.tool_name === "Write") {
    process.exit(2);
  }

  console.log(JSON.stringify({ continue: true }));
}

handle(JSON.parse("{}"));
