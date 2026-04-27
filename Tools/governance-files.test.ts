#!/usr/bin/env bun

import { describe, expect, test } from "bun:test";
import { existsSync } from "fs";
import { join } from "path";
import { spawnSync } from "child_process";

const REPO_ROOT = import.meta.dir.replace(/\/Tools$/, "");

const GOVERNANCE_FILES = [
  "AGENTS.md",
  ".codex/config.toml",
  ".codex/README.md",
  ".codex/governance/ARCHITECTURE_STEWARD_PROTOCOL.md",
  ".codex/governance/PHASE_PLAN.md",
  ".codex/governance/PROTECTED_FILES.md",
  ".codex/prompts/pai-codex-adapter-architecture.md",
  ".codex/prompts/pr-01-inventory.md",
  ".codex/prompts/pr-02-platform-path-abstraction.md",
  ".codex/prompts/review-current-diff.md",
];

describe("architect governance harness", () => {
  test("required governance files are present and not git-ignored", () => {
    for (const relPath of GOVERNANCE_FILES) {
      expect(existsSync(join(REPO_ROOT, relPath))).toBe(true);

      const ignored = spawnSync("git", ["check-ignore", "-q", "--", relPath], {
        cwd: REPO_ROOT,
      });

      expect(ignored.status).not.toBe(0);
    }
  });
});