#!/usr/bin/env bun

import { afterEach, describe, expect, test } from "bun:test";
import {
  existsSync,
  mkdirSync,
  mkdtempSync,
  readdirSync,
  readFileSync,
  rmSync,
  statSync,
  symlinkSync,
  writeFileSync,
} from "fs";
import { tmpdir } from "os";
import { dirname, join, resolve } from "path";
import { spawnSync } from "child_process";
import {
  buildInstructions,
  renderInstructionTemplate,
} from "../Releases/v4.0.3/.claude/PAI/Tools/BuildInstructions";
import {
  build as buildClaude,
  needsRebuild as claudeNeedsRebuild,
} from "../Releases/v4.0.3/.claude/PAI/Tools/BuildCLAUDE";

const REPO_ROOT = resolve(import.meta.dir, "..");
const HOOK_HANDLER = join(REPO_ROOT, "Releases/v4.0.3/.claude/hooks/handlers/BuildCLAUDE.ts");
const BUILD_CLAUDE = join(REPO_ROOT, "Releases/v4.0.3/.claude/PAI/Tools/BuildCLAUDE.ts");
const RELEASE_TEMPLATE = join(REPO_ROOT, "Releases/v4.0.3/.claude/CLAUDE.md.template");
const RELEASE_ALGORITHM_LATEST = join(REPO_ROOT, "Releases/v4.0.3/.claude/PAI/Algorithm/LATEST");
const ROOT_AGENTS = join(REPO_ROOT, "AGENTS.md");

const tempRoots: string[] = [];

afterEach(() => {
  for (const root of tempRoots.splice(0)) {
    rmSync(root, { recursive: true, force: true });
  }
});

interface InstructionFixture {
  root: string;
  home: string;
  paiHome: string;
  adapterHome: string;
  templatePath: string;
  outputPath: string;
  settingsPath: string;
  algorithmDir: string;
  algorithmLatestPath: string;
}

function makeFixture(): InstructionFixture {
  const root = mkdtempSync(join(tmpdir(), "pai-instructions-"));
  tempRoots.push(root);

  const home = join(root, "home");
  const paiHome = join(root, "pai-home");
  const adapterHome = join(root, "codex-config");
  const algorithmDir = join(paiHome, "PAI/Algorithm");
  const templatePath = join(paiHome, "CLAUDE.md.template");
  const outputPath = join(paiHome, "CLAUDE.md");
  const settingsPath = join(paiHome, "settings.json");
  const algorithmLatestPath = join(algorithmDir, "LATEST");

  mkdirSync(algorithmDir, { recursive: true });
  mkdirSync(home, { recursive: true });
  mkdirSync(adapterHome, { recursive: true });

  writeFileSync(
    templatePath,
    [
      "# PAI {{PAI_VERSION}}",
      "DA: {DAIDENTITY.NAME}",
      "DA full: {DAIDENTITY.FULLNAME}",
      "DA display: {DAIDENTITY.DISPLAYNAME}",
      "Principal: {PRINCIPAL.NAME}",
      "Timezone: {PRINCIPAL.TIMEZONE}",
      "Algorithm: {{ALGO_PATH}}",
      "Version: {{ALGO_VERSION}}",
      "🗣️ {DAIDENTITY.NAME}: ready",
      "",
    ].join("\n"),
  );

  writeFileSync(
    settingsPath,
    JSON.stringify(
      {
        daidentity: {
          name: "Ava",
          fullName: "Ava System",
          displayName: "Ava",
        },
        principal: {
          name: "Morgan",
          timezone: "Europe/Stockholm",
        },
        pai: {
          version: "4.0.3",
        },
      },
      null,
      2,
    ),
  );

  writeFileSync(algorithmLatestPath, "v3.7.0\n");

  return {
    root,
    home,
    paiHome,
    adapterHome,
    templatePath,
    outputPath,
    settingsPath,
    algorithmDir,
    algorithmLatestPath,
  };
}

function makeReleaseClaudeFixture(): InstructionFixture {
  const root = mkdtempSync(join(tmpdir(), "pai-release-instructions-"));
  tempRoots.push(root);

  const home = join(root, "home");
  const paiHome = join(home, ".claude");
  const adapterHome = paiHome;
  const algorithmDir = join(paiHome, "PAI/Algorithm");
  const templatePath = join(paiHome, "CLAUDE.md.template");
  const outputPath = join(paiHome, "CLAUDE.md");
  const settingsPath = join(paiHome, "settings.json");
  const algorithmLatestPath = join(algorithmDir, "LATEST");

  mkdirSync(algorithmDir, { recursive: true });
  writeFileSync(templatePath, readFileSync(RELEASE_TEMPLATE, "utf-8"));
  writeFileSync(algorithmLatestPath, readFileSync(RELEASE_ALGORITHM_LATEST, "utf-8"));
  writeFileSync(
    settingsPath,
    JSON.stringify(
      {
        daidentity: {
          name: "Ava",
          fullName: "Ava System",
          displayName: "Ava",
        },
        principal: {
          name: "Morgan",
          timezone: "Europe/Stockholm",
        },
        pai: {
          version: "4.0.3",
        },
      },
      null,
      2,
    ),
  );

  return {
    root,
    home,
    paiHome,
    adapterHome,
    templatePath,
    outputPath,
    settingsPath,
    algorithmDir,
    algorithmLatestPath,
  };
}

function legacyClaudeRender(fixture: InstructionFixture): string {
  const settings = JSON.parse(readFileSync(fixture.settingsPath, "utf-8"));
  const algoVersion = readFileSync(fixture.algorithmLatestPath, "utf-8").trim();
  const variables: Record<string, string> = {
    "{DAIDENTITY.NAME}": settings.daidentity?.name || "Assistant",
    "{DAIDENTITY.FULLNAME}": settings.daidentity?.fullName || "Assistant",
    "{DAIDENTITY.DISPLAYNAME}": settings.daidentity?.displayName || "Assistant",
    "{PRINCIPAL.NAME}": settings.principal?.name || "User",
    "{PRINCIPAL.TIMEZONE}": settings.principal?.timezone || "UTC",
    "{{PAI_VERSION}}": settings.pai?.version || "4.0.3",
    "{{ALGO_VERSION}}": algoVersion,
    "{{ALGO_PATH}}": `PAI/Algorithm/${algoVersion}.md`,
  };

  let content = readFileSync(fixture.templatePath, "utf-8");
  for (const [key, value] of Object.entries(variables)) {
    content = content.replaceAll(key, value);
  }
  return content;
}

function claudeOptions(fixture: InstructionFixture) {
  return {
    paiHome: fixture.paiHome,
    templatePath: fixture.templatePath,
    outputPath: fixture.outputPath,
    settingsPath: fixture.settingsPath,
    algorithmDir: fixture.algorithmDir,
    algorithmLatestPath: fixture.algorithmLatestPath,
  };
}

function codexOptions(fixture: InstructionFixture, outputPath?: string) {
  return {
    target: "codex" as const,
    paiHome: fixture.paiHome,
    adapterHome: fixture.adapterHome,
    outputPath,
    settingsPath: fixture.settingsPath,
    algorithmDir: fixture.algorithmDir,
    algorithmLatestPath: fixture.algorithmLatestPath,
  };
}

function gitProtectedDiff(): string {
  const result = spawnSync("git", ["diff", "--name-only", "--", "AGENTS.md", ".codex"], {
    cwd: REPO_ROOT,
    encoding: "utf-8",
  });
  expect(result.status).toBe(0);
  return result.stdout;
}

function gitProtectedStatus(): string {
  const result = spawnSync("git", ["status", "--short", "--untracked-files=all", "--", "AGENTS.md", ".codex"], {
    cwd: REPO_ROOT,
    encoding: "utf-8",
  });
  expect(result.status).toBe(0);
  return result.stdout;
}

function listFiles(root: string): string[] {
  if (!existsSync(root)) return [];

  const files: string[] = [];
  const visit = (dir: string): void => {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const path = join(dir, entry.name);
      const rel = path.slice(root.length + 1);
      if (entry.isDirectory()) {
        visit(path);
      } else {
        files.push(rel);
      }
    }
  };

  visit(root);
  return files.sort();
}

function withEnv<T>(overrides: Record<string, string | undefined>, fn: () => T): T {
  const previous: Record<string, string | undefined> = {};
  for (const key of Object.keys(overrides)) {
    previous[key] = process.env[key];
  }

  try {
    for (const [key, value] of Object.entries(overrides)) {
      if (value === undefined) {
        delete process.env[key];
      } else {
        process.env[key] = value;
      }
    }
    return fn();
  } finally {
    for (const [key, value] of Object.entries(previous)) {
      if (value === undefined) {
        delete process.env[key];
      } else {
        process.env[key] = value;
      }
    }
  }
}

function expectCodexRouterSafe(content: string, fixture: InstructionFixture): void {
  expect(Buffer.byteLength(content, "utf-8")).toBeLessThan(16 * 1024);
  expect(content).toContain(`PAI_HOME: ${fixture.paiHome}`);
  expect(content).toContain(`PAI algorithm: ${join(fixture.algorithmDir, "v3.7.0.md")}`);
  expect(content).toContain(`Codex adapter/config home: ${fixture.adapterHome}`);
  expect(content).toContain(join(fixture.paiHome, "PAI/CONTEXT_ROUTING.md"));
  expect(content).toContain("not full runtime parity");
  expect(content).toContain("compatibility matrix");
  expect(content).not.toMatch(/\{\{[A-Z0-9_]+\}\}|\{[A-Z0-9_.]+\}/);
  expect(content).not.toContain("~/.claude");
  expect(content).not.toContain(`PAI_HOME: ${join(fixture.home, ".codex")}`);
  expect(content).not.toContain("AskUserQuestion");
  expect(content).not.toContain("MultiEdit");
  expect(content).not.toContain("Task");
  expect(content).not.toContain("Skill");
  expect(content).not.toContain("Read tool");
  expect(content).not.toContain("Write tool");
  expect(content).not.toContain("Edit tool");
}

describe("target-aware instruction generation", () => {
  test("Claude target renders exactly like legacy BuildCLAUDE behavior", () => {
    const fixture = makeFixture();
    const content = renderInstructionTemplate(readFileSync(fixture.templatePath, "utf-8"), {
      target: "claude",
      ...claudeOptions(fixture),
      dryRun: true,
    });

    expect(content).toBe(legacyClaudeRender(fixture));
  });

  test("BuildCLAUDE.build writes CLAUDE.md in a directed temp fixture", () => {
    const fixture = makeFixture();

    const result = buildClaude(claudeOptions(fixture));

    expect(result).toEqual({ rebuilt: true });
    expect(readFileSync(fixture.outputPath, "utf-8")).toBe(legacyClaudeRender(fixture));
  });

  test("manual BuildCLAUDE entrypoint builds real release template under temp HOME", () => {
    const fixture = makeReleaseClaudeFixture();

    const result = spawnSync("bun", [BUILD_CLAUDE], {
      cwd: REPO_ROOT,
      env: {
        ...process.env,
        HOME: fixture.home,
      },
      encoding: "utf-8",
    });

    expect(result.status).toBe(0);
    expect(readFileSync(fixture.outputPath, "utf-8")).toBe(legacyClaudeRender(fixture));
    expect(result.stdout).toContain("Built CLAUDE.md from template");
  });

  test("BuildCLAUDE.needsRebuild is true when output is missing", () => {
    const fixture = makeFixture();

    expect(claudeNeedsRebuild(claudeOptions(fixture))).toBe(true);
  });

  test("BuildCLAUDE.needsRebuild is false when output is current", () => {
    const fixture = makeFixture();
    buildClaude(claudeOptions(fixture));

    expect(claudeNeedsRebuild(claudeOptions(fixture))).toBe(false);
  });

  test("BuildCLAUDE.needsRebuild preserves legacy rebuild edge cases", () => {
    const fixture = makeFixture();

    buildClaude(claudeOptions(fixture));
    rmSync(fixture.templatePath);
    expect(claudeNeedsRebuild(claudeOptions(fixture))).toBe(false);
    expect(buildClaude(claudeOptions(fixture))).toEqual({
      rebuilt: false,
      reason: "No CLAUDE.md.template found",
    });

    writeFileSync(fixture.templatePath, "Version {{PAI_VERSION}}\n🗣️ {DAIDENTITY.NAME}: ready\n");
    writeFileSync(fixture.outputPath, "Unresolved {{PAI_VERSION}}\n🗣️ Ava: ready\n");
    expect(claudeNeedsRebuild(claudeOptions(fixture))).toBe(true);

    writeFileSync(fixture.outputPath, "Algorithm: PAI/Algorithm/v0.0.0.md\n🗣️ Ava: ready\n");
    expect(claudeNeedsRebuild(claudeOptions(fixture))).toBe(true);

    writeFileSync(fixture.outputPath, "Algorithm: PAI/Algorithm/v3.7.0.md\n🗣️ OldName: ready\n");
    expect(claudeNeedsRebuild(claudeOptions(fixture))).toBe(true);
  });

  test("existing hook handler BuildCLAUDE import path still builds", () => {
    const fixture = makeFixture();
    const outdir = join(fixture.root, "bundle");
    mkdirSync(outdir, { recursive: true });

    const result = spawnSync("bun", ["build", HOOK_HANDLER, "--target=bun", "--outdir", outdir], {
      cwd: REPO_ROOT,
      env: {
        ...process.env,
        HOME: fixture.home,
        PAI_HOME: fixture.paiHome,
        CODEX_HOME: fixture.adapterHome,
      },
      encoding: "utf-8",
    });

    expect(result.status).toBe(0);
  });

  test("existing hook handler runs against temp .claude and rebuilds CLAUDE.md", () => {
    const fixture = makeReleaseClaudeFixture();

    const result = spawnSync("bun", [HOOK_HANDLER], {
      cwd: REPO_ROOT,
      env: {
        ...process.env,
        HOME: fixture.home,
      },
      encoding: "utf-8",
    });

    expect(result.status).toBe(0);
    expect(readFileSync(fixture.outputPath, "utf-8")).toBe(legacyClaudeRender(fixture));
    expect(result.stderr).toContain("CLAUDE.md rebuilt from template");
  });

  test("Codex target generates compact AGENTS.md content in dry-run mode", () => {
    const fixture = makeFixture();
    const filesBefore = listFiles(fixture.root);

    const result = buildInstructions({
      ...codexOptions(fixture),
      dryRun: true,
    });

    expect(result.target).toBe("codex");
    expect(result.rebuilt).toBe(true);
    expect(typeof result.content).toBe("string");
    expect(result.outputPath).toBe(join(fixture.paiHome, "AGENTS.md"));
    expectCodexRouterSafe(result.content!, fixture);
    expect(existsSync(join(fixture.home, ".codex", "AGENTS.md"))).toBe(false);
    expect(existsSync(join(fixture.home, ".pai", "AGENTS.md"))).toBe(false);
    expect(existsSync(join(fixture.paiHome, "AGENTS.md"))).toBe(false);
    expect(existsSync(join(fixture.adapterHome, "AGENTS.md"))).toBe(false);
    expect(listFiles(fixture.root)).toEqual(filesBefore);
  });

  test("Codex target writes only to an explicit temp output path", () => {
    const fixture = makeFixture();
    const outputPath = join(fixture.paiHome, "generated", "AGENTS.md");
    mkdirSync(dirname(outputPath), { recursive: true });

    const result = buildInstructions({
      ...codexOptions(fixture, outputPath),
      dryRun: false,
    });

    expect(result).toMatchObject({
      target: "codex",
      rebuilt: true,
      outputPath,
    });
    expect(result.content).toBeUndefined();
    expectCodexRouterSafe(readFileSync(outputPath, "utf-8"), fixture);
    expect(existsSync(join(fixture.home, ".codex", "AGENTS.md"))).toBe(false);
    expect(existsSync(join(fixture.home, ".pai", "AGENTS.md"))).toBe(false);
    expect(existsSync(join(fixture.adapterHome, "AGENTS.md"))).toBe(false);

    const secondResult = buildInstructions({
      ...codexOptions(fixture, outputPath),
      dryRun: false,
    });

    expect(secondResult).toEqual({
      target: "codex",
      rebuilt: false,
      outputPath,
      reason: "AGENTS.md already current",
    });
  });

  test("Codex dry-run defaults keep PAI home and adapter home split under temp HOME", () => {
    const fixture = makeFixture();
    withEnv(
      {
        HOME: fixture.home,
        PAI_DIR: undefined,
        PAI_HOME: undefined,
        CODEX_HOME: undefined,
      },
      () => {
        const result = buildInstructions({
          target: "codex",
          settingsPath: fixture.settingsPath,
          algorithmDir: fixture.algorithmDir,
          algorithmLatestPath: fixture.algorithmLatestPath,
          dryRun: true,
        });

        expect(result.outputPath).toBe(join(fixture.home, ".pai", "AGENTS.md"));
        expect(result.content).toContain(`PAI_HOME: ${join(fixture.home, ".pai")}`);
        expect(result.content).toContain(`Codex adapter/config home: ${join(fixture.home, ".codex")}`);
        expect(existsSync(join(fixture.home, ".pai"))).toBe(false);
        expect(existsSync(join(fixture.home, ".codex"))).toBe(false);
      },
    );
  });

  test("Codex dry-run honors PAI_HOME, PAI_DIR, and CODEX_HOME without writes", () => {
    const fixture = makeFixture();

    withEnv(
      {
        HOME: fixture.home,
        PAI_DIR: undefined,
        PAI_HOME: join(fixture.home, "custom-pai"),
        CODEX_HOME: join(fixture.home, "custom-codex"),
      },
      () => {
        const result = buildInstructions({
          target: "codex",
          settingsPath: fixture.settingsPath,
          algorithmDir: fixture.algorithmDir,
          algorithmLatestPath: fixture.algorithmLatestPath,
          dryRun: true,
        });

        expect(result.outputPath).toBe(join(fixture.home, "custom-pai", "AGENTS.md"));
        expect(result.content).toContain(`PAI_HOME: ${join(fixture.home, "custom-pai")}`);
        expect(result.content).toContain(`Codex adapter/config home: ${join(fixture.home, "custom-codex")}`);
      },
    );

    withEnv(
      {
        HOME: fixture.home,
        PAI_DIR: join(fixture.home, "legacy-pai"),
        PAI_HOME: join(fixture.home, "custom-pai"),
        CODEX_HOME: join(fixture.home, "custom-codex"),
      },
      () => {
        const result = buildInstructions({
          target: "codex",
          settingsPath: fixture.settingsPath,
          algorithmDir: fixture.algorithmDir,
          algorithmLatestPath: fixture.algorithmLatestPath,
          dryRun: true,
        });

        expect(result.outputPath).toBe(join(fixture.home, "legacy-pai", "AGENTS.md"));
        expect(result.content).toContain(`PAI_HOME: ${join(fixture.home, "legacy-pai")}`);
        expect(result.content).toContain(`Codex adapter/config home: ${join(fixture.home, "custom-codex")}`);
      },
    );

    expect(existsSync(join(fixture.home, "custom-pai"))).toBe(false);
    expect(existsSync(join(fixture.home, "custom-codex"))).toBe(false);
    expect(existsSync(join(fixture.home, "legacy-pai"))).toBe(false);
  });

  test("Codex target does not default to runtime writes", () => {
    const fixture = makeFixture();

    expect(() =>
      buildInstructions({
        ...codexOptions(fixture),
        dryRun: false,
      }),
    ).toThrow("explicit outputPath");
    expect(existsSync(join(fixture.home, ".codex", "AGENTS.md"))).toBe(false);
    expect(existsSync(join(fixture.home, ".pai", "AGENTS.md"))).toBe(false);
  });

  test("Codex explicit writes reject runtime, protected, traversal, and symlink paths", () => {
    const fixture = makeFixture();
    const runtimePaiHome = join(fixture.home, ".pai");
    mkdirSync(runtimePaiHome, { recursive: true });
    const adapterInsidePai = join(fixture.paiHome, "codex-adapter");
    mkdirSync(adapterInsidePai, { recursive: true });
    const symlinkOutput = join(fixture.paiHome, "AGENTS.md");
    symlinkSync(join(fixture.root, "outside-AGENTS.md"), symlinkOutput);
    const outsideDirectory = join(fixture.root, "outside-real");
    mkdirSync(outsideDirectory, { recursive: true });
    const parentSymlink = join(fixture.paiHome, "link");
    symlinkSync(outsideDirectory, parentSymlink, "dir");
    for (const dirname of ["rules", "skills", "agents", ".agents/skills", ".codex", "hooks"]) {
      mkdirSync(join(fixture.paiHome, dirname), { recursive: true });
    }

    const base = {
      target: "codex" as const,
      paiHome: fixture.paiHome,
      adapterHome: fixture.adapterHome,
      settingsPath: fixture.settingsPath,
      algorithmDir: fixture.algorithmDir,
      algorithmLatestPath: fixture.algorithmLatestPath,
      dryRun: false,
    };

    withEnv(
      {
        HOME: fixture.home,
        PAI_DIR: undefined,
        PAI_HOME: undefined,
        CODEX_HOME: undefined,
      },
      () => {
        expect(() =>
          buildInstructions({
            target: "codex",
            outputPath: join(fixture.paiHome, "AGENTS.md"),
            settingsPath: fixture.settingsPath,
            algorithmDir: fixture.algorithmDir,
            algorithmLatestPath: fixture.algorithmLatestPath,
            dryRun: false,
          }),
        ).toThrow("explicit paiHome");
        expect(() => buildInstructions({ ...base, outputPath: join(fixture.root, "outside", "AGENTS.md") })).toThrow(
          "outside explicit paiHome",
        );
        expect(() =>
          buildInstructions({
            ...base,
            paiHome: runtimePaiHome,
            outputPath: join(runtimePaiHome, "AGENTS.md"),
          }),
        ).toThrow("default PAI home");
        expect(() =>
          buildInstructions({
            ...base,
            paiHome: fixture.home,
            outputPath: join(fixture.home, ".codex", "AGENTS.md"),
          }),
        ).toThrow("Codex CLI state/config home");
        expect(() =>
          buildInstructions({
            ...base,
            outputPath: join(fixture.paiHome, "..", "escape", "AGENTS.md"),
          }),
        ).toThrow("outside explicit paiHome");
        expect(() => buildInstructions({ ...base, outputPath: join(fixture.paiHome, "settings.json") })).toThrow(
          "AGENTS.md outputs",
        );
        expect(() => buildInstructions({ ...base, outputPath: join(fixture.paiHome, "config.toml") })).toThrow(
          "AGENTS.md outputs",
        );
        expect(() => buildInstructions({ ...base, outputPath: join(fixture.paiHome, "hooks.json") })).toThrow(
          "AGENTS.md outputs",
        );
        expect(() => buildInstructions({ ...base, outputPath: join(fixture.paiHome, "rules", "AGENTS.md") })).toThrow(
          "reserved rules path",
        );
        expect(() => buildInstructions({ ...base, outputPath: join(fixture.paiHome, "skills", "AGENTS.md") })).toThrow(
          "reserved skills path",
        );
        expect(() => buildInstructions({ ...base, outputPath: join(fixture.paiHome, "agents", "AGENTS.md") })).toThrow(
          "reserved agents path",
        );
        expect(() => buildInstructions({ ...base, outputPath: join(fixture.paiHome, "hooks", "AGENTS.md") })).toThrow(
          "reserved hooks path",
        );
        expect(() =>
          buildInstructions({ ...base, outputPath: join(fixture.paiHome, ".agents", "skills", "AGENTS.md") }),
        ).toThrow("reserved .agents path");
        expect(() =>
          buildInstructions({ ...base, outputPath: join(fixture.paiHome, ".codex", "AGENTS.md") }),
        ).toThrow("reserved .codex path");
        expect(() =>
          buildInstructions({
            ...base,
            adapterHome: adapterInsidePai,
            outputPath: join(adapterInsidePai, "AGENTS.md"),
          }),
        ).toThrow("Codex adapter/config home");
        expect(() => buildInstructions({ ...base, outputPath: symlinkOutput })).toThrow("symlink output path");
        expect(() => buildInstructions({ ...base, outputPath: join(parentSymlink, "AGENTS.md") })).toThrow(
          "symlink path component",
        );
        expect(existsSync(join(outsideDirectory, "AGENTS.md"))).toBe(false);
        expect(() =>
          buildInstructions({
            ...base,
            paiHome: REPO_ROOT,
            outputPath: ROOT_AGENTS,
          }),
        ).toThrow("repository AGENTS.md");
        expect(() =>
          buildInstructions({
            ...base,
            paiHome: REPO_ROOT,
            outputPath: join(REPO_ROOT, ".codex", "AGENTS.md"),
          }),
        ).toThrow("repository governance directory");
      },
    );
  });

  test("Codex explicit writes reject source-tree protected paths from a different cwd", () => {
    const fixture = makeFixture();
    const previousCwd = process.cwd();

    try {
      process.chdir(fixture.root);
      expect(() =>
        buildInstructions({
          ...codexOptions(fixture),
          paiHome: REPO_ROOT,
          outputPath: ROOT_AGENTS,
          dryRun: false,
        }),
      ).toThrow("repository AGENTS.md");
      expect(() =>
        buildInstructions({
          ...codexOptions(fixture),
          paiHome: REPO_ROOT,
          outputPath: join(REPO_ROOT, ".codex", "AGENTS.md"),
          dryRun: false,
        }),
      ).toThrow("repository governance directory");
    } finally {
      process.chdir(previousCwd);
    }
  });

  test("Codex target reports a missing AGENTS template without writing", () => {
    const fixture = makeFixture();
    const outputPath = join(fixture.paiHome, "generated", "AGENTS.md");

    const result = buildInstructions({
      ...codexOptions(fixture, outputPath),
      templatePath: join(fixture.root, "missing-AGENTS.md.template"),
      dryRun: true,
    });

    expect(result).toEqual({
      target: "codex",
      rebuilt: false,
      outputPath,
      reason: "No AGENTS.md.template found",
    });
    expect(existsSync(outputPath)).toBe(false);
  });

  test("instruction generation does not modify root AGENTS.md or protected .codex governance", () => {
    const fixture = makeFixture();
    const rootAgentsBefore = readFileSync(ROOT_AGENTS, "utf-8");
    const rootAgentsStatBefore = statSync(ROOT_AGENTS).mtimeMs;
    const protectedDiffBefore = gitProtectedDiff();
    const protectedStatusBefore = gitProtectedStatus();

    buildInstructions({
      ...codexOptions(fixture),
      dryRun: true,
    });

    expect(readFileSync(ROOT_AGENTS, "utf-8")).toBe(rootAgentsBefore);
    expect(statSync(ROOT_AGENTS).mtimeMs).toBe(rootAgentsStatBefore);
    expect(gitProtectedDiff()).toBe(protectedDiffBefore);
    expect(gitProtectedStatus()).toBe(protectedStatusBefore);
  });
});
