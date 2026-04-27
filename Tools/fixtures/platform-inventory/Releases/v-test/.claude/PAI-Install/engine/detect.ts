#!/usr/bin/env bun

import { execSync } from "child_process";

export function detectClaude(): string {
  return execSync("claude --version 2>&1", { encoding: "utf-8" });
}

export function promptClaude(): string {
  return execSync("claude -p fixture", { encoding: "utf-8" });
}
