#!/usr/bin/env bun

import { afterEach, describe, expect, test } from "bun:test";
import {
  chmodSync,
  existsSync,
  lstatSync,
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
import { dirname, join, relative, resolve } from "path";
import { runCodexAdapterPlan } from "../Releases/v4.0.3/.claude/PAI-Install/engine/codex-adapter-plan";

const REPO_ROOT = resolve(import.meta.dir, "..");
const tempRoots: string[] = [];

afterEach(() => {
  for (const root of tempRoots.splice(0)) {
    rmSync(root, { recursive: true, force: true });
  }
});

interface PlanFixture {
  root: string;
  home: string;
  paiHome: string;
  adapterHome: string;
  settingsPath: string;
  algorithmDir: string;
  algorithmLatestPath: string;
  configPath: string;
}

function makeRoot(prefix = "pai-codex-adapter-plan-"): string {
  const root = mkdtempSync(join(tmpdir(), prefix));
  tempRoots.push(root);
  return root;
}

function makeFixture(): PlanFixture {
  const root = makeRoot();
  const home = join(root, "home");
  const paiHome = join(root, "pai-home");
  const adapterHome = join(home, ".codex");
  const algorithmDir = join(paiHome, "PAI/Algorithm");
  const settingsPath = join(paiHome, "settings.json");
  const algorithmLatestPath = join(algorithmDir, "LATEST");
  const configPath = join(adapterHome, "config.toml");

  mkdirSync(home, { recursive: true });
  mkdirSync(algorithmDir, { recursive: true });
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
    settingsPath,
    algorithmDir,
    algorithmLatestPath,
    configPath,
  };
}

function planOptions(fixture: PlanFixture, overrides: Partial<Parameters<typeof runCodexAdapterPlan>[0]> = {}) {
  return {
    paiHome: fixture.paiHome,
    adapterHome: fixture.adapterHome,
    allowedRoot: fixture.home,
    env: { HOME: fixture.home },
    settingsPath: fixture.settingsPath,
    algorithmDir: fixture.algorithmDir,
    algorithmLatestPath: fixture.algorithmLatestPath,
    ...overrides,
  };
}

function operation(result: ReturnType<typeof runCodexAdapterPlan>, kind: string) {
  const found = result.operations.find((op) => op.kind === kind);
  expect(found).toBeDefined();
  return found!;
}

function listFiles(root: string): string[] {
  if (!existsSync(root)) return [];

  const files: string[] = [];
  const visit = (dir: string): void => {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const path = join(dir, entry.name);
      if (entry.isDirectory()) {
        visit(path);
      } else {
        files.push(relative(root, path));
      }
    }
  };

  visit(root);
  return files.sort();
}

function withProcessHome<T>(home: string, callback: () => T): T {
  const originalHome = process.env.HOME;
  process.env.HOME = home;

  try {
    return callback();
  } finally {
    if (originalHome === undefined) {
      delete process.env.HOME;
    } else {
      process.env.HOME = originalHome;
    }
  }
}

function expectCodexRouterSafe(content: string, fixture: PlanFixture): void {
  expect(Buffer.byteLength(content, "utf-8")).toBeLessThan(16 * 1024);
  expect(content).toContain(`PAI_HOME: ${fixture.paiHome}`);
  expect(content).toContain(`PAI algorithm: ${join(fixture.algorithmDir, "v3.7.0.md")}`);
  expect(content).toContain(join(fixture.paiHome, "PAI/CONTEXT_ROUTING.md"));
  expect(content).toContain(`Codex adapter/config home: ${fixture.adapterHome}`);
  expect(content).not.toMatch(/\{\{[A-Z0-9_]+\}\}|\{[A-Z0-9_.]+\}/);
  expect(content).not.toContain("AskUserQuestion");
  expect(content).not.toContain("MultiEdit");
  expect(content).not.toContain("Task");
  expect(content).not.toContain("Skill");
  expect(content).not.toContain("Read tool");
  expect(content).not.toContain("Write tool");
  expect(content).not.toContain("Edit tool");
  expect(content).not.toContain("Codex support is implemented");
  expect(content).not.toContain("full Codex support");
  expect(content).not.toContain("Codex runtime parity is implemented");
}

function expectNoTempFiles(dir: string): void {
  const tempFiles = existsSync(dir) ? readdirSync(dir).filter((name) => name.includes(".pai-tmp-")) : [];
  expect(tempFiles).toEqual([]);
}

function assertThrowsPlan(options: Parameters<typeof runCodexAdapterPlan>[0], message: string): void {
  expect(() => runCodexAdapterPlan(options)).toThrow(message);
}

describe("Codex adapter install-plan primitive", () => {
  test("dry-run plan renders AGENTS.md and skips config without writes or backups", () => {
    const fixture = makeFixture();
    const filesBefore = listFiles(fixture.root);

    const result = runCodexAdapterPlan(planOptions(fixture, { dryRun: true, backup: true }));

    expect(result.paiHome).toBe(fixture.paiHome);
    expect(result.adapterHome).toBe(fixture.adapterHome);
    expect(result.agentsPath).toBe(join(fixture.adapterHome, "AGENTS.md"));
    expect(result.configPath).toBe(fixture.configPath);
    expectCodexRouterSafe(result.agentsContent, fixture);
    expect(operation(result, "render-agents")).toMatchObject({ path: result.agentsPath, changed: true });
    expect(operation(result, "write-agents")).toMatchObject({ path: result.agentsPath, changed: false, reason: "dryRun" });
    expect(operation(result, "skip-config")).toMatchObject({
      path: fixture.configPath,
      changed: false,
      reason: "No configFragment supplied; PR-04C does not define product Codex config defaults",
    });
    expect(existsSync(fixture.adapterHome)).toBe(false);
    expect(existsSync(join(fixture.adapterHome, "AGENTS.md"))).toBe(false);
    expect(existsSync(fixture.configPath)).toBe(false);
    expect(listFiles(fixture.root)).toEqual(filesBefore);
  });

  test("dry-run plan can exercise config merge without writing AGENTS, config, or backups", () => {
    const fixture = makeFixture();
    mkdirSync(fixture.adapterHome, { recursive: true });
    const existingConfig = 'model = "gpt-5.5"\n';
    writeFileSync(fixture.configPath, existingConfig);

    const result = runCodexAdapterPlan(planOptions(fixture, {
      dryRun: true,
      backup: true,
      now: new Date("2026-04-29T04:05:06Z"),
      configFragment: "[pai_pr04c_test]\nplan_probe = true\n",
      configPath: fixture.configPath,
      sourceLabel: "PR-04C dry-run test-only fragment",
    }));

    expect(operation(result, "write-agents")).toMatchObject({
      path: join(fixture.adapterHome, "AGENTS.md"),
      changed: false,
      reason: "dryRun",
    });
    expect(operation(result, "merge-config")).toMatchObject({
      path: fixture.configPath,
      changed: true,
    });
    expect(operation(result, "merge-config").backupPath).toBeUndefined();
    expect(readFileSync(fixture.configPath, "utf-8")).toBe(existingConfig);
    expect(existsSync(join(fixture.adapterHome, "AGENTS.md"))).toBe(false);
    expect(existsSync(join(fixture.adapterHome, "config.toml.pai-backup-20260429-040506"))).toBe(false);
  });

  test("dry-run plan allows explicit templates only from temp allowedRoot fixtures", () => {
    const fixture = makeFixture();
    const templatePath = join(fixture.home, "AGENTS.md.template");
    writeFileSync(templatePath, "# Test {{PAI_VERSION}}\n- PAI_HOME: {{PAI_HOME}}\n- Adapter: {{ADAPTER_HOME}}\n");

    const result = runCodexAdapterPlan(planOptions(fixture, {
      dryRun: true,
      agentsTemplatePath: templatePath,
    }));

    expect(result.agentsContent).toContain("# Test 4.0.3");
    expect(result.agentsContent).toContain(`PAI_HOME: ${fixture.paiHome}`);
    expect(result.agentsContent).toContain(`Adapter: ${fixture.adapterHome}`);

    const outsideRoot = makeRoot("pai-codex-adapter-plan-template-outside-");
    const outsideTemplate = join(outsideRoot, "AGENTS.md.template");
    writeFileSync(outsideTemplate, "# Outside template\n");
    assertThrowsPlan(planOptions(fixture, {
      dryRun: true,
      agentsTemplatePath: outsideTemplate,
    }), "explicit agentsTemplatePath must be the product template or inside temp allowedRoot");
  });

  test("writes AGENTS.md only under explicit temp HOME .codex and exposes rendered content", () => {
    const fixture = makeFixture();

    const result = runCodexAdapterPlan(planOptions(fixture, { dryRun: false, backup: true }));

    expect(operation(result, "write-agents")).toMatchObject({
      path: join(fixture.adapterHome, "AGENTS.md"),
      changed: true,
    });
    expect(readFileSync(result.agentsPath, "utf-8")).toBe(result.agentsContent);
    expectCodexRouterSafe(readFileSync(result.agentsPath, "utf-8"), fixture);
    expect(existsSync(fixture.configPath)).toBe(false);
    expect(existsSync(join(fixture.home, ".pai", "AGENTS.md"))).toBe(false);
    expect(existsSync(join(fixture.home, ".claude", "AGENTS.md"))).toBe(false);
    expect(statSync(result.agentsPath).mode & 0o777).toBe(0o600);
    expectNoTempFiles(fixture.adapterHome);
  });

  test("idempotent AGENTS.md writes preserve existing mode and do not create no-op backups", () => {
    const fixture = makeFixture();
    mkdirSync(fixture.adapterHome, { recursive: true });
    const agentsPath = join(fixture.adapterHome, "AGENTS.md");
    writeFileSync(agentsPath, "old agents\n");
    chmodSync(agentsPath, 0o640);

    const first = runCodexAdapterPlan(planOptions(fixture, { dryRun: false, backup: false }));
    expect(operation(first, "write-agents").changed).toBe(true);
    expect(operation(first, "write-agents").backupPath).toBeUndefined();
    expect(statSync(agentsPath).mode & 0o777).toBe(0o640);

    const second = runCodexAdapterPlan(planOptions(fixture, {
      dryRun: false,
      backup: true,
      now: new Date("2026-04-29T01:02:03Z"),
    }));

    expect(operation(second, "write-agents")).toMatchObject({
      path: agentsPath,
      changed: false,
      reason: "AGENTS.md already current",
    });
    expect(readFileSync(agentsPath, "utf-8")).toBe(first.agentsContent);
    expect(statSync(agentsPath).mode & 0o777).toBe(0o640);
    expect(existsSync(join(fixture.adapterHome, "AGENTS.md.pai-backup-20260429-010203"))).toBe(false);
    expectNoTempFiles(fixture.adapterHome);
  });

  test("backs up changed AGENTS.md deterministically and fails closed on backup collisions", () => {
    const fixture = makeFixture();
    mkdirSync(fixture.adapterHome, { recursive: true });
    const agentsPath = join(fixture.adapterHome, "AGENTS.md");
    const existing = "existing agents\n";
    writeFileSync(agentsPath, existing);
    chmodSync(agentsPath, 0o600);

    const changed = runCodexAdapterPlan(planOptions(fixture, {
      dryRun: false,
      backup: true,
      now: new Date("2026-04-28T12:34:56Z"),
    }));

    const backupPath = join(fixture.adapterHome, "AGENTS.md.pai-backup-20260428-123456");
    expect(operation(changed, "write-agents")).toMatchObject({ changed: true, backupPath });
    expect(readFileSync(backupPath, "utf-8")).toBe(existing);
    expect(statSync(backupPath).mode & 0o777).toBe(0o600);
    expect(readFileSync(agentsPath, "utf-8")).toBe(changed.agentsContent);

    const collision = makeFixture();
    mkdirSync(collision.adapterHome, { recursive: true });
    const collisionAgentsPath = join(collision.adapterHome, "AGENTS.md");
    const collisionBackupPath = join(collision.adapterHome, "AGENTS.md.pai-backup-20260428-123456");
    writeFileSync(collisionAgentsPath, "old collision agents\n");
    writeFileSync(collisionBackupPath, "existing backup\n");

    assertThrowsPlan(planOptions(collision, {
      dryRun: false,
      backup: true,
      now: new Date("2026-04-28T12:34:56Z"),
    }), "overwrite existing Codex AGENTS.md backup");
    expect(readFileSync(collisionAgentsPath, "utf-8")).toBe("old collision agents\n");
    expect(readFileSync(collisionBackupPath, "utf-8")).toBe("existing backup\n");
  });

  test("optionally exercises config merge with a test-only fragment and remains idempotent", () => {
    const fixture = makeFixture();
    mkdirSync(fixture.adapterHome, { recursive: true });
    const existingConfig = [
      "# user Codex config",
      'model = "gpt-5.5"',
      "",
      "[features]",
      "multi_agent = true",
      "",
    ].join("\n");
    writeFileSync(fixture.configPath, existingConfig);

    const fragment = "[pai_pr04c_test]\nplan_probe = true\n";
    const first = runCodexAdapterPlan(planOptions(fixture, {
      dryRun: false,
      backup: true,
      now: new Date("2026-04-29T03:04:05Z"),
      configFragment: fragment,
      configPath: fixture.configPath,
      sourceLabel: "PR-04C test-only fragment",
    }));

    expect(operation(first, "merge-config")).toMatchObject({
      path: fixture.configPath,
      changed: true,
      backupPath: join(fixture.adapterHome, "config.toml.pai-backup-20260429-030405"),
    });
    expect(readFileSync(fixture.configPath, "utf-8")).toContain("# user Codex config");
    expect(readFileSync(fixture.configPath, "utf-8")).toContain('model = "gpt-5.5"');
    expect(readFileSync(fixture.configPath, "utf-8")).toContain("multi_agent = true");
    expect(readFileSync(fixture.configPath, "utf-8")).toContain("[pai_pr04c_test]");
    expect(readFileSync(fixture.configPath, "utf-8")).toContain("plan_probe = true");
    expect(readFileSync(join(fixture.adapterHome, "config.toml.pai-backup-20260429-030405"), "utf-8")).toBe(existingConfig);

    const second = runCodexAdapterPlan(planOptions(fixture, {
      dryRun: false,
      backup: true,
      now: new Date("2026-04-29T03:04:06Z"),
      configFragment: fragment,
      configPath: fixture.configPath,
      sourceLabel: "PR-04C test-only fragment",
    }));
    expect(operation(second, "merge-config")).toMatchObject({ path: fixture.configPath, changed: false });
    expect(existsSync(join(fixture.adapterHome, "config.toml.pai-backup-20260429-030406"))).toBe(false);

    const conflict = makeFixture();
    mkdirSync(conflict.adapterHome, { recursive: true });
    writeFileSync(conflict.configPath, "[pai_pr04c_test]\nplan_probe = false\n");
    const conflictResult = runCodexAdapterPlan(planOptions(conflict, {
      dryRun: false,
      backup: true,
      configFragment: fragment,
      configPath: conflict.configPath,
      sourceLabel: "PR-04C test-only fragment",
    }));
    expect(operation(conflictResult, "merge-config")).toMatchObject({
      path: conflict.configPath,
      changed: false,
    });
    expect(operation(conflictResult, "merge-config").reason).toContain("pai_pr04c_test.plan_probe");
    expect(readFileSync(conflict.configPath, "utf-8")).toBe("[pai_pr04c_test]\nplan_probe = false\n");

    expect(existsSync(join(REPO_ROOT, "Releases/v4.0.3/.claude/PAI-Install/engine/codex-config-fragment.toml"))).toBe(false);
    expect(existsSync(join(REPO_ROOT, "Releases/v4.0.3/.claude/PAI-Install/engine/codex-runtime-config.toml"))).toBe(false);
  });

  test("fresh temp HOME config merge creates adapter AGENTS and config together", () => {
    const fixture = makeFixture();

    const result = runCodexAdapterPlan(planOptions(fixture, {
      dryRun: false,
      backup: true,
      configFragment: "[pai_pr04c_test]\nplan_probe = true\n",
      configPath: fixture.configPath,
      sourceLabel: "PR-04C fresh temp-home fragment",
    }));

    expect(operation(result, "write-agents")).toMatchObject({
      path: join(fixture.adapterHome, "AGENTS.md"),
      changed: true,
    });
    expect(operation(result, "merge-config")).toMatchObject({
      path: fixture.configPath,
      changed: true,
    });
    expect(readFileSync(result.agentsPath, "utf-8")).toBe(result.agentsContent);
    expect(readFileSync(fixture.configPath, "utf-8")).toContain("[pai_pr04c_test]");
    expect(readFileSync(fixture.configPath, "utf-8")).toContain("plan_probe = true");
    expect(existsSync(join(fixture.adapterHome, "config.toml.pai-backup-20260429-030405"))).toBe(false);
    expectNoTempFiles(fixture.adapterHome);
  });

  test("path safety rejects protected homes, governance paths, traversal, broad roots, and symlinks", () => {
    const fixture = makeFixture();

    assertThrowsPlan(planOptions(fixture, {
      adapterHome: REPO_ROOT,
      allowedRoot: REPO_ROOT,
      dryRun: true,
    }), "repository AGENTS.md");

    assertThrowsPlan(planOptions(fixture, {
      adapterHome: join(REPO_ROOT, ".codex"),
      allowedRoot: REPO_ROOT,
      dryRun: true,
    }), "repository governance .codex");

    assertThrowsPlan(planOptions(fixture, {
      dryRun: true,
      configFragment: "[pai_pr04c_test]\nplan_probe = true\n",
      configPath: join(REPO_ROOT, ".codex", "config.toml"),
    }), "configPath is limited to adapterHome/config.toml");

    assertThrowsPlan(planOptions(fixture, {
      dryRun: true,
      agentsTemplatePath: join(REPO_ROOT, ".codex", "AGENTS.md.template"),
    }), "repository governance .codex template source");

    const protectedTemplateSymlink = join(fixture.root, "protected-template-link.md");
    symlinkSync(join(REPO_ROOT, ".codex", "README.md"), protectedTemplateSymlink);
    assertThrowsPlan(planOptions(fixture, {
      dryRun: true,
      agentsTemplatePath: protectedTemplateSymlink,
    }), "repository governance .codex template source");

    assertThrowsPlan(planOptions(fixture, {
      adapterHome: join(fixture.home, "not-dot-codex"),
      dryRun: false,
    }), "limited to explicit temp HOME/.codex/AGENTS.md");
    expect(existsSync(join(fixture.home, "not-dot-codex", "AGENTS.md"))).toBe(false);

    assertThrowsPlan(planOptions(fixture, {
      env: {},
      dryRun: false,
    }), "writes require explicit env.HOME");
    expect(existsSync(join(fixture.adapterHome, "AGENTS.md"))).toBe(false);

    for (const homeDirName of [".pai", ".claude"]) {
      const configuredProtectedHome = join(fixture.home, homeDirName);
      assertThrowsPlan(planOptions(fixture, {
        adapterHome: configuredProtectedHome,
        dryRun: false,
      }), "limited to explicit temp HOME/.codex/AGENTS.md");
      expect(existsSync(join(configuredProtectedHome, "AGENTS.md"))).toBe(false);
    }

    const processHome = join(fixture.root, "process-home");
    mkdirSync(processHome, { recursive: true });
    withProcessHome(processHome, () => {
      for (const homeDirName of [".codex", ".pai", ".claude"]) {
        const adapterHome = join(processHome, homeDirName);
        assertThrowsPlan(planOptions(fixture, {
          adapterHome,
          allowedRoot: processHome,
          env: { HOME: fixture.home },
          dryRun: false,
        }), "limited to explicit temp HOME/.codex/AGENTS.md");
        expect(existsSync(join(adapterHome, "AGENTS.md"))).toBe(false);
      }
    });

    const outsideRoot = makeRoot("pai-codex-adapter-plan-outside-");
    assertThrowsPlan(planOptions(fixture, {
      adapterHome: join(outsideRoot, ".codex"),
      dryRun: false,
    }), "outside allowedRoot");

    assertThrowsPlan(planOptions(fixture, {
      allowedRoot: "/",
      dryRun: true,
    }), "broad Codex adapter plan allowedRoot");

    assertThrowsPlan(planOptions(fixture, {
      allowedRoot: tmpdir(),
      dryRun: true,
    }), "broad Codex adapter plan allowedRoot");

    assertThrowsPlan(planOptions(fixture, {
      adapterHome: join(REPO_ROOT, "tmp-pr04c-codex-home"),
      allowedRoot: REPO_ROOT,
      dryRun: true,
    }), "broad Codex adapter plan allowedRoot");

    const symlinkTarget = join(fixture.root, "symlink-target");
    const symlinkAdapterHome = fixture.adapterHome;
    mkdirSync(symlinkTarget, { recursive: true });
    symlinkSync(symlinkTarget, symlinkAdapterHome, "dir");
    expect(lstatSync(symlinkAdapterHome).isSymbolicLink()).toBe(true);
    assertThrowsPlan(planOptions(fixture, {
      adapterHome: symlinkAdapterHome,
      dryRun: false,
    }), "symlink adapterHome");

    const agentsSymlinkFixture = makeFixture();
    mkdirSync(agentsSymlinkFixture.adapterHome, { recursive: true });
    const agentsSymlink = join(agentsSymlinkFixture.adapterHome, "AGENTS.md");
    symlinkSync(join(agentsSymlinkFixture.root, "real-agents.md"), agentsSymlink);
    assertThrowsPlan(planOptions(agentsSymlinkFixture, {
      dryRun: false,
    }), "symlink AGENTS.md path");

    const parentSymlinkFixture = makeFixture();
    const parentSymlinkTarget = join(parentSymlinkFixture.root, "parent-target");
    const parentSymlink = join(parentSymlinkFixture.root, "home-link");
    mkdirSync(parentSymlinkTarget, { recursive: true });
    symlinkSync(parentSymlinkTarget, parentSymlink, "dir");
    assertThrowsPlan(planOptions(parentSymlinkFixture, {
      adapterHome: join(parentSymlink, ".codex"),
      allowedRoot: parentSymlinkFixture.root,
      env: { HOME: parentSymlink },
      dryRun: false,
    }), "symlink path component");
    expect(existsSync(join(parentSymlinkTarget, ".codex", "AGENTS.md"))).toBe(false);

    const ancestorSymlinkFixture = makeFixture();
    const ancestorSymlinkTarget = join(ancestorSymlinkFixture.root, "ancestor-target");
    const ancestorSymlink = join(ancestorSymlinkFixture.root, "ancestor-link");
    const ancestorHome = join(ancestorSymlink, "home");
    mkdirSync(ancestorSymlinkTarget, { recursive: true });
    mkdirSync(join(ancestorSymlinkTarget, "home"), { recursive: true });
    symlinkSync(ancestorSymlinkTarget, ancestorSymlink, "dir");
    assertThrowsPlan(planOptions(ancestorSymlinkFixture, {
      adapterHome: join(ancestorHome, ".codex"),
      allowedRoot: ancestorSymlinkFixture.root,
      env: { HOME: ancestorHome },
      dryRun: false,
    }), "symlink path component");
    expect(existsSync(join(ancestorSymlinkTarget, "home", ".codex", "AGENTS.md"))).toBe(false);

    const allowedRootSymlinkFixture = makeFixture();
    const realRoot = join(allowedRootSymlinkFixture.root, "real-root");
    const rootLink = join(allowedRootSymlinkFixture.root, "root-link");
    const linkedHome = join(rootLink, "home");
    mkdirSync(join(realRoot, "home"), { recursive: true });
    symlinkSync(realRoot, rootLink, "dir");
    assertThrowsPlan(planOptions(allowedRootSymlinkFixture, {
      adapterHome: join(linkedHome, ".codex"),
      allowedRoot: linkedHome,
      env: { HOME: linkedHome },
      dryRun: false,
    }), "symlink path component");
    expect(existsSync(join(realRoot, "home", ".codex"))).toBe(false);
  });

  test("path safety rejects PAI_HOME and Codex adapter/config home overlap", () => {
    const fixture = makeFixture();

    assertThrowsPlan(planOptions(fixture, {
      paiHome: fixture.adapterHome,
      dryRun: true,
    }), "PAI_HOME separate from Codex adapter/config home");

    assertThrowsPlan(planOptions(fixture, {
      paiHome: join(fixture.adapterHome, "pai"),
      dryRun: true,
    }), "PAI_HOME separate from Codex adapter/config home");

    assertThrowsPlan(planOptions(fixture, {
      paiHome: fixture.home,
      dryRun: true,
    }), "PAI_HOME separate from Codex adapter/config home");

    assertThrowsPlan(planOptions(fixture, {
      paiHome: join(fixture.home, ".codex", "pai"),
      adapterHome: join(fixture.home, "codex-state"),
      dryRun: true,
    }), "configured HOME Codex CLI state/config home");

    const processHome = join(fixture.root, "process-pai-home");
    mkdirSync(processHome, { recursive: true });
    withProcessHome(processHome, () => {
      assertThrowsPlan(planOptions(fixture, {
        paiHome: join(processHome, ".codex", "pai"),
        dryRun: true,
      }), "real/home Codex CLI state/config home");
    });
  });

  test("config preflight rejects invalid config targets before AGENTS.md is written", () => {
    const fixture = makeFixture();
    const invalidConfigPath = join(fixture.home, "other-config", "config.toml");

    assertThrowsPlan(planOptions(fixture, {
      dryRun: false,
      configFragment: "[pai_pr04c_test]\nplan_probe = true\n",
      configPath: invalidConfigPath,
    }), "configPath is limited to adapterHome/config.toml");

    expect(existsSync(join(fixture.adapterHome, "AGENTS.md"))).toBe(false);
    expect(existsSync(invalidConfigPath)).toBe(false);
  });

  test("config preflight rejects merge failures before AGENTS.md is written", () => {
    const badLabel = makeFixture();

    assertThrowsPlan(planOptions(badLabel, {
      dryRun: false,
      configFragment: "[pai_pr04c_test]\nplan_probe = true\n",
      configPath: badLabel.configPath,
      sourceLabel: "bad\nlabel",
    }), "sourceLabel must be a single line");
    expect(existsSync(join(badLabel.adapterHome, "AGENTS.md"))).toBe(false);
    expect(existsSync(badLabel.adapterHome)).toBe(false);
    expect(existsSync(badLabel.configPath)).toBe(false);

    const backupCollision = makeFixture();
    mkdirSync(backupCollision.adapterHome, { recursive: true });
    writeFileSync(backupCollision.configPath, 'model = "gpt-5.5"\n');
    writeFileSync(join(backupCollision.adapterHome, "config.toml.pai-backup-20260429-030405"), "existing config backup\n");

    assertThrowsPlan(planOptions(backupCollision, {
      dryRun: false,
      backup: true,
      now: new Date("2026-04-29T03:04:05Z"),
      configFragment: "[pai_pr04c_test]\nplan_probe = true\n",
      configPath: backupCollision.configPath,
      sourceLabel: "PR-04C backup collision fragment",
    }), "overwrite existing Codex config backup");

    expect(existsSync(join(backupCollision.adapterHome, "AGENTS.md"))).toBe(false);
    expect(readFileSync(backupCollision.configPath, "utf-8")).toBe('model = "gpt-5.5"\n');
    expect(readFileSync(join(backupCollision.adapterHome, "config.toml.pai-backup-20260429-030405"), "utf-8")).toBe(
      "existing config backup\n",
    );

    const backupSymlink = makeFixture();
    mkdirSync(backupSymlink.adapterHome, { recursive: true });
    writeFileSync(backupSymlink.configPath, 'model = "gpt-5.5"\n');
    symlinkSync(join(backupSymlink.root, "backup-target"), join(backupSymlink.adapterHome, "config.toml.pai-backup-20260429-030405"));

    assertThrowsPlan(planOptions(backupSymlink, {
      dryRun: false,
      backup: true,
      now: new Date("2026-04-29T03:04:05Z"),
      configFragment: "[pai_pr04c_test]\nplan_probe = true\n",
      configPath: backupSymlink.configPath,
      sourceLabel: "PR-04C backup symlink fragment",
    }), "Codex config backup through symlink path");

    expect(existsSync(join(backupSymlink.adapterHome, "AGENTS.md"))).toBe(false);
    expect(readFileSync(backupSymlink.configPath, "utf-8")).toBe('model = "gpt-5.5"\n');
  });

  test("CLI, web, and installer actions do not import or call the new primitive", () => {
    const releaseRoot = join(REPO_ROOT, "Releases/v4.0.3/.claude/PAI-Install");
    const planModule = join(releaseRoot, "engine/codex-adapter-plan.ts");
    const searchedFiles: string[] = [];

    const visit = (dir: string): void => {
      for (const entry of readdirSync(dir, { withFileTypes: true })) {
        const path = join(dir, entry.name);
        if (entry.isDirectory()) {
          visit(path);
          continue;
        }
        if (!path.endsWith(".ts") && !path.endsWith(".js") && !path.endsWith(".sh")) continue;
        if (path === planModule) continue;
        searchedFiles.push(path);
      }
    };

    visit(releaseRoot);

    for (const path of searchedFiles) {
      const content = readFileSync(path, "utf-8");
      expect(content).not.toContain("codex-adapter-plan");
      expect(content).not.toContain("installCodex");
      expect(content).not.toContain("runCodexAdapterPlan");
    }
  });
});
