#!/usr/bin/env bun

import { describe, expect, test } from "bun:test";
import { execFileSync, spawnSync } from "child_process";
import { join } from "path";

const REPO_ROOT = import.meta.dir.replace(/\/Tools$/, "");
const TOOL_PATH = join(REPO_ROOT, "Tools", "platform-inventory.ts");
const FIXTURE_ROOT = join(REPO_ROOT, "Tools", "fixtures", "platform-inventory");

interface InventoryResult {
  filesScanned: number;
  occurrences: Array<{
    file: string;
    patternId: string;
    classification: string;
    risk: number;
  }>;
  groupedCouplings: Array<{
    file: string;
    patternId: string;
    classification: string;
    risk: number;
  }>;
  counts: {
    byClassification: Record<string, number>;
    byPattern: Record<string, number>;
  };
}

function runInventory(args: string[] = []): InventoryResult {
  const output = execFileSync("bun", [TOOL_PATH, "--root", FIXTURE_ROOT, "--format", "json", ...args], {
    cwd: REPO_ROOT,
    encoding: "utf-8",
  });
  return JSON.parse(output) as InventoryResult;
}

function hasOccurrence(result: InventoryResult, file: string, patternId: string, classification: string): boolean {
  return result.occurrences.some(
    (occurrence) =>
      occurrence.file === file &&
      occurrence.patternId === patternId &&
      occurrence.classification === classification,
  );
}

describe("platform-inventory fixture", () => {
  test("classifies every planning category from release-shaped fixtures", () => {
    const result = runInventory();

    expect(result.filesScanned).toBe(8);
    expect(result.counts.byClassification["claude-only"]).toBeGreaterThan(0);
    expect(result.counts.byClassification["platform-neutralizable"]).toBeGreaterThan(0);
    expect(result.counts.byClassification["codex-equivalent"]).toBeGreaterThan(0);
    expect(result.counts.byClassification["breaking-for-codex"]).toBeGreaterThan(0);
    expect(result.counts.byClassification["docs-only"]).toBeGreaterThan(0);
    expect(result.counts.byClassification["unknown-needs-fixture"]).toBeGreaterThan(0);

    expect(hasOccurrence(result, "Releases/v-test/.claude/settings.json", "claude-hook-event", "breaking-for-codex")).toBe(true);
    expect(hasOccurrence(result, "Releases/v-test/.claude/hooks/SecurityValidator.hook.ts", "claude-hook-decision", "breaking-for-codex")).toBe(true);
    expect(hasOccurrence(result, "Releases/v-test/.claude/PAI/Tools/TranscriptParser.ts", "claude-hook-event", "breaking-for-codex")).toBe(true);
    expect(hasOccurrence(result, "Releases/v-test/.claude/PAI/Tools/TranscriptParser.ts", "claude-transcript", "unknown-needs-fixture")).toBe(true);
    expect(hasOccurrence(result, "Releases/v-test/.claude/PAI-Install/engine/detect.ts", "claude-cli-detection", "codex-equivalent")).toBe(true);
    expect(hasOccurrence(result, "Releases/v-test/.claude/PAI-Install/engine/detect.ts", "claude-cli-prompt-exec", "breaking-for-codex")).toBe(true);
    expect(hasOccurrence(result, "Releases/v-test/.claude/hooks/README.md", "claude-hook-event", "docs-only")).toBe(true);
    expect(hasOccurrence(result, "Packs/FixturePack/INSTALL.md", "claude-home-path", "platform-neutralizable")).toBe(true);
    expect(hasOccurrence(result, "Tools/example-runtime.ts", "pai-dir-env", "platform-neutralizable")).toBe(true);
  });

  test("excludes planning and self-test fixtures by default, then includes them on request", () => {
    const defaultResult = runInventory();
    const includedResult = runInventory(["--include-planning"]);

    const defaultFiles = new Set(defaultResult.occurrences.map((occurrence) => occurrence.file));
    const includedFiles = new Set(includedResult.occurrences.map((occurrence) => occurrence.file));

    expect(defaultFiles.has(".codex/prompts/pr-99.md")).toBe(false);
    expect(defaultFiles.has("docs/adapters/IGNORED.md")).toBe(false);
    expect(defaultFiles.has("Tools/platform-inventory.ts")).toBe(false);
    expect(defaultFiles.has("Tools/fixtures/platform-inventory/ignored.md")).toBe(false);

    expect(includedFiles.has(".codex/prompts/pr-99.md")).toBe(true);
    expect(includedFiles.has("docs/adapters/IGNORED.md")).toBe(true);
    expect(includedFiles.has("Tools/platform-inventory.ts")).toBe(true);
    expect(includedFiles.has("Tools/fixtures/platform-inventory/ignored.md")).toBe(true);
    expect(includedResult.filesScanned).toBeGreaterThan(defaultResult.filesScanned);
  });

  test("reports CLI argument failures", () => {
    const invalidFormat = spawnSync("bun", [TOOL_PATH, "--format", "xml"], {
      cwd: REPO_ROOT,
      encoding: "utf-8",
    });
    expect(invalidFormat.status).toBe(1);
    expect(invalidFormat.stderr).toContain("Unsupported format");

    const invalidRoot = spawnSync("bun", [TOOL_PATH, "--root", join(FIXTURE_ROOT, "missing"), "--format", "json"], {
      cwd: REPO_ROOT,
      encoding: "utf-8",
    });
    expect(invalidRoot.status).toBe(1);
    expect(invalidRoot.stderr).toContain("Root does not exist");

    const invalidTop = spawnSync("bun", [TOOL_PATH, "--top", "0"], {
      cwd: REPO_ROOT,
      encoding: "utf-8",
    });
    expect(invalidTop.status).toBe(1);
    expect(invalidTop.stderr).toContain("--top must be a positive number");
  });

  test("rejects existing roots outside the repository", () => {
    const outsideRoot = spawnSync("bun", [TOOL_PATH, "--root", "/tmp", "--format", "json"], {
      cwd: REPO_ROOT,
      encoding: "utf-8",
    });
    expect(outsideRoot.status).toBe(1);
    expect(outsideRoot.stderr).toContain("Refusing to scan outside repository root");
  });

  test("rejects protected planning roots without include-planning", () => {
    const protectedRoot = spawnSync("bun", [TOOL_PATH, "--root", join(REPO_ROOT, ".codex"), "--format", "json"], {
      cwd: REPO_ROOT,
      encoding: "utf-8",
    });
    expect(protectedRoot.status).toBe(1);
    expect(protectedRoot.stderr).toContain("without --include-planning");

    const includedProtectedRoot = spawnSync(
      "bun",
      [TOOL_PATH, "--root", join(REPO_ROOT, ".codex"), "--include-planning", "--format", "json"],
      {
        cwd: REPO_ROOT,
        encoding: "utf-8",
      },
    );
    expect(includedProtectedRoot.status).toBe(0);

    const agentsRoot = spawnSync("bun", [TOOL_PATH, "--root", join(REPO_ROOT, "AGENTS.md"), "--format", "json"], {
      cwd: REPO_ROOT,
      encoding: "utf-8",
    });
    expect(agentsRoot.status).toBe(1);
    expect(agentsRoot.stderr).toContain("without --include-planning");
  });

  test("rejects private repository state roots", () => {
    const gitRoot = spawnSync("bun", [TOOL_PATH, "--root", join(REPO_ROOT, ".git"), "--format", "json"], {
      cwd: REPO_ROOT,
      encoding: "utf-8",
    });
    expect(gitRoot.status).toBe(1);
    expect(gitRoot.stderr).toContain("private repository state");

    const gitLogsRoot = spawnSync("bun", [TOOL_PATH, "--root", join(REPO_ROOT, ".git", "logs"), "--format", "json"], {
      cwd: REPO_ROOT,
      encoding: "utf-8",
    });
    expect(gitLogsRoot.status).toBe(1);
    expect(gitLogsRoot.stderr).toContain("private repository state");
  });
});
