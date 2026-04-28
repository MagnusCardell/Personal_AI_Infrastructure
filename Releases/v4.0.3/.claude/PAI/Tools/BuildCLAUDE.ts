#!/usr/bin/env bun

/**
 * BuildCLAUDE.ts - compatibility entrypoint for Claude instruction generation.
 *
 * Existing hooks and manual usage import/call this file. The target-aware
 * implementation lives in BuildInstructions.ts.
 */

import {
  type BuildInstructionOptions,
  buildInstructions,
  loadInstructionVariables,
  needsRebuild as instructionNeedsRebuild,
} from "./BuildInstructions";

export type BuildClaudeOptions = Omit<BuildInstructionOptions, "target">;

function claudeOptions(options: BuildClaudeOptions = {}): BuildInstructionOptions {
  return {
    ...options,
    target: "claude",
  };
}

export function needsRebuild(options: BuildClaudeOptions = {}): boolean {
  return instructionNeedsRebuild(claudeOptions(options));
}

export function build(options: BuildClaudeOptions = {}): { rebuilt: boolean; reason?: string } {
  const result = buildInstructions(claudeOptions(options));
  return result.reason ? { rebuilt: result.rebuilt, reason: result.reason } : { rebuilt: result.rebuilt };
}

function loadVariables(options: BuildClaudeOptions = {}): Record<string, string> {
  return loadInstructionVariables(claudeOptions(options));
}

if (import.meta.main) {
  const result = build();
  if (result.rebuilt) {
    const vars = loadVariables();
    console.log("✅ Built CLAUDE.md from template");
    console.log(`   Algorithm: ${vars["{{ALGO_VERSION}}"]}`);
    console.log(`   DA: ${vars["{DAIDENTITY.NAME}"]}`);
    console.log(`   Principal: ${vars["{PRINCIPAL.NAME}"]}`);
  } else {
    console.log(`ℹ ${result.reason}`);
  }
}
