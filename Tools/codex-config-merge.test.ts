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
import { basename, dirname, join, resolve } from "path";
import {
  mergeCodexConfig,
  type CodexConfigMergeOptions,
} from "../Releases/v4.0.3/.claude/PAI-Install/engine/codex-config-merge";

const REPO_ROOT = resolve(import.meta.dir, "..");
const tempRoots: string[] = [];

afterEach(() => {
  for (const root of tempRoots.splice(0)) {
    rmSync(root, { recursive: true, force: true });
  }
});

function makeRoot(): string {
  const root = mkdtempSync(join(tmpdir(), "pai-codex-config-merge-"));
  tempRoots.push(root);
  return root;
}

function makeConfig(root: string, relativePath = "codex/config.toml"): string {
  const configPath = join(root, relativePath);
  mkdirSync(dirname(configPath), { recursive: true });
  return configPath;
}

function testEnv(root: string): Record<string, string> {
  return { HOME: join(root, "home") };
}

function options(
  root: string,
  configPath: string,
  fragment: string,
  overrides: Partial<CodexConfigMergeOptions> = {},
): CodexConfigMergeOptions {
  return {
    configPath,
    fragment,
    sourceLabel: "PR-04B test",
    dryRun: true,
    allowedRoot: root,
    env: testEnv(root),
    ...overrides,
  };
}

function countOccurrences(content: string, needle: string): number {
  return content.split(needle).length - 1;
}

function paiBlock(content: string): string {
  const start = content.indexOf("# >>> PAI managed: codex config");
  const end = content.indexOf("# <<< PAI managed: codex config");
  expect(start).toBeGreaterThanOrEqual(0);
  expect(end).toBeGreaterThan(start);
  return content.slice(start, end);
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

describe("Codex config merge primitive", () => {
  test("dry-run empty config returns expected content without writes or backup", () => {
    const root = makeRoot();
    const configPath = makeConfig(root);

    const result = mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n"));

    expect(result.changed).toBe(true);
    expect(result.configPath).toBe(configPath);
    expect(result.conflicts).toEqual([]);
    expect(result.backupPath).toBeUndefined();
    expect(result.insertedTables).toEqual(["features"]);
    expect(result.insertedKeys).toEqual(["features.codex_hooks"]);
    expect(result.content).toBe(
      [
        "[features]",
        "# >>> PAI managed: codex config",
        "# source: PR-04B test",
        "codex_hooks = true",
        "# <<< PAI managed: codex config",
        "",
      ].join("\n"),
    );
    expect(existsSync(configPath)).toBe(false);
  });

  test("preserves existing user config and inserts only PAI-managed keys into existing table", () => {
    const root = makeRoot();
    const configPath = makeConfig(root);
    const existing = [
      "# user Codex config",
      'model = "gpt-5.5"',
      'profile = "work"',
      'model_provider = "openai"',
      "",
      "[features]",
      "# keep this user feature",
      "multi_agent = true",
      "",
      "[mcp_servers.github]",
      'command = "github-mcp"',
      "",
    ].join("\n");
    writeFileSync(configPath, existing);

    const result = mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n"));

    expect(result.changed).toBe(true);
    expect(result.content).toContain("# user Codex config");
    expect(result.content).toContain('model = "gpt-5.5"');
    expect(result.content).toContain('profile = "work"');
    expect(result.content).toContain('model_provider = "openai"');
    expect(result.content).toContain("multi_agent = true");
    expect(result.content).toContain("[mcp_servers.github]");
    expect(result.content).toContain('command = "github-mcp"');
    expect(result.content).toContain("codex_hooks = true");
    expect(countOccurrences(result.content, "[features]")).toBe(1);
    expect(result.insertedTables).toEqual([]);
    expect(paiBlock(result.content)).toContain("codex_hooks = true");
    expect(existsSync(configPath)).toBe(true);
    expect(readFileSync(configPath, "utf-8")).toBe(existing);
  });

  test("appends a new table when the fragment targets a missing table", () => {
    const root = makeRoot();
    const configPath = makeConfig(root);
    writeFileSync(configPath, 'model = "gpt-5.5"\n');

    const result = mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n"));

    expect(result.content).toContain('model = "gpt-5.5"');
    expect(result.content).toContain("[features]");
    expect(result.content.indexOf("[features]")).toBeGreaterThan(result.content.indexOf('model = "gpt-5.5"'));
    expect(result.insertedTables).toEqual(["features"]);
  });

  test("detects user-owned conflicts and does not write", () => {
    const root = makeRoot();
    const configPath = makeConfig(root);
    const existing = [
      "[features]",
      "# >>> PAI managed: codex config",
      "# source: old",
      "other_pai_key = true",
      "# <<< PAI managed: codex config",
      "codex_hooks = false",
      "",
    ].join("\n");
    writeFileSync(configPath, existing);

    const result = mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n", {
      dryRun: false,
      backup: true,
    }));

    expect(result.changed).toBe(false);
    expect(result.content).toBe(existing);
    expect(result.conflicts).toEqual([
      {
        table: "features",
        key: "codex_hooks",
        existingLine: 6,
        reason: "Existing user-owned Codex config key would be overwritten",
      },
    ]);
    expect(result.backupPath).toBeUndefined();
    expect(readFileSync(configPath, "utf-8")).toBe(existing);
  });

  test("replaces existing managed blocks and is idempotent on a second merge", () => {
    const root = makeRoot();
    const configPath = makeConfig(root);
    writeFileSync(
      configPath,
      [
        "[features]",
        "multi_agent = true",
        "",
        "# >>> PAI managed: codex config",
        "# source: old",
        "codex_hooks = false",
        "# <<< PAI managed: codex config",
        "",
      ].join("\n"),
    );

    const first = mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n", {
      dryRun: false,
      backup: false,
    }));
    const second = mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n", {
      dryRun: false,
      backup: true,
    }));

    expect(first.changed).toBe(true);
    expect(first.content).toContain("codex_hooks = true");
    expect(first.content).not.toContain("codex_hooks = false");
    expect(countOccurrences(first.content, "# >>> PAI managed: codex config")).toBe(1);
    expect(second.changed).toBe(false);
    expect(second.backupPath).toBeUndefined();
    expect(second.content).toBe(first.content);
  });

  test("writes with deterministic backups only when changing existing content", () => {
    const root = makeRoot();
    const configPath = makeConfig(root);
    const existing = 'model = "gpt-5.5"\n';
    writeFileSync(configPath, existing);

    const changed = mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n", {
      dryRun: false,
      backup: true,
      now: new Date("2026-04-28T12:34:56Z"),
    }));

    expect(changed.changed).toBe(true);
    expect(changed.backupPath).toBe(join(dirname(configPath), "config.toml.pai-backup-20260428-123456"));
    expect(readFileSync(changed.backupPath!, "utf-8")).toBe(existing);
    expect(readFileSync(configPath, "utf-8")).toBe(changed.content);

    const unchanged = mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n", {
      dryRun: false,
      backup: true,
      now: new Date("2026-04-29T01:02:03Z"),
    }));

    expect(unchanged.changed).toBe(false);
    expect(unchanged.backupPath).toBeUndefined();
    expect(existsSync(join(dirname(configPath), "config.toml.pai-backup-20260429-010203"))).toBe(false);

    const dryRun = mergeCodexConfig(options(root, configPath, "[features]\nother_pai_key = true\n", {
      dryRun: true,
      backup: true,
      now: new Date("2026-04-30T01:02:03Z"),
    }));

    expect(dryRun.changed).toBe(true);
    expect(dryRun.backupPath).toBeUndefined();
    expect(existsSync(join(dirname(configPath), "config.toml.pai-backup-20260430-010203"))).toBe(false);
  });

  test("backup writes fail closed on collisions and preserve file modes", () => {
    const root = makeRoot();
    const configPath = makeConfig(root);
    const existing = 'model = "gpt-5.5"\n';
    writeFileSync(configPath, existing);
    chmodSync(configPath, 0o600);

    const collidingBackup = join(dirname(configPath), "config.toml.pai-backup-20260428-123456");
    writeFileSync(collidingBackup, "existing backup\n");
    expect(() =>
      mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n", {
        dryRun: false,
        backup: true,
        now: new Date("2026-04-28T12:34:56Z"),
      })),
    ).toThrow("overwrite existing Codex config backup");
    expect(readFileSync(configPath, "utf-8")).toBe(existing);
    expect(readFileSync(collidingBackup, "utf-8")).toBe("existing backup\n");

    rmSync(collidingBackup);
    const changed = mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n", {
      dryRun: false,
      backup: true,
      now: new Date("2026-04-28T12:34:56Z"),
    }));
    expect(changed.changed).toBe(true);
    expect(statSync(configPath).mode & 0o777).toBe(0o600);
    expect(statSync(changed.backupPath!).mode & 0o777).toBe(0o600);

    const newConfigPath = makeConfig(root, "new/config.toml");
    const created = mergeCodexConfig(options(root, newConfigPath, "[features]\ncodex_hooks = true\n", {
      dryRun: false,
      backup: false,
    }));
    expect(created.changed).toBe(true);
    expect(statSync(newConfigPath).mode & 0o777).toBe(0o600);
  });

  test("atomic write leaves no temporary files in the config parent after success", () => {
    const root = makeRoot();
    const configPath = makeConfig(root);
    writeFileSync(configPath, "");

    mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n", {
      dryRun: false,
      backup: false,
    }));

    const tempFiles = readdirSync(dirname(configPath)).filter((name) => name.includes(".pai-tmp-"));
    expect(tempFiles).toEqual([]);
  });

  test("path safety rejects governance, real-home, traversal, basename, and symlink paths", () => {
    const root = makeRoot();
    const fragment = "[features]\ncodex_hooks = true\n";

    expect(() =>
      mergeCodexConfig(options(root, join(REPO_ROOT, ".codex", "config.toml"), fragment)),
    ).toThrow("repository governance .codex");

    expect(() =>
      mergeCodexConfig({
        configPath: makeConfig(root),
        fragment,
        dryRun: true,
        env: testEnv(root),
      }),
    ).toThrow("requires an explicit allowedRoot");

    const processHome = join(root, "process-home");
    mkdirSync(processHome, { recursive: true });
    withProcessHome(processHome, () => {
      for (const homeDirName of [".codex", ".pai", ".claude"]) {
        const configPath = join(processHome, homeDirName, "config.toml");
        expect(() =>
          mergeCodexConfig({
            configPath,
            fragment,
            dryRun: true,
            allowedRoot: processHome,
            env: { HOME: processHome },
          }),
        ).toThrow("real/home");

        expect(() =>
          mergeCodexConfig({
            configPath,
            fragment,
            dryRun: false,
            backup: false,
            allowedRoot: processHome,
            env: testEnv(root),
          }),
        ).toThrow("real/home");
        expect(existsSync(configPath)).toBe(false);
      }
    });

    const outsideRoot = makeRoot();
    const outside = makeConfig(outsideRoot);
    expect(() => mergeCodexConfig(options(root, outside, fragment))).toThrow("outside allowedRoot");

    const wrongBasename = makeConfig(root, "codex/not-config.toml");
    expect(() => mergeCodexConfig(options(root, wrongBasename, fragment))).toThrow("config.toml outputs");

    const allowedRootTarget = makeRoot();
    mkdirSync(join(allowedRootTarget, "codex"), { recursive: true });
    const symlinkAllowedRoot = join(root, "allowed-root-link");
    symlinkSync(allowedRootTarget, symlinkAllowedRoot, "dir");
    expect(() =>
      mergeCodexConfig({
        configPath: join(symlinkAllowedRoot, "codex", "config.toml"),
        fragment,
        dryRun: true,
        allowedRoot: symlinkAllowedRoot,
        env: testEnv(root),
      }),
    ).toThrow("symlink allowedRoot");

    const realConfig = makeConfig(root, "real/config.toml");
    writeFileSync(realConfig, "");
    const symlinkConfig = makeConfig(root, "link/config.toml");
    rmSync(symlinkConfig, { force: true });
    symlinkSync(realConfig, symlinkConfig);
    expect(lstatSync(symlinkConfig).isSymbolicLink()).toBe(true);
    expect(() => mergeCodexConfig(options(root, symlinkConfig, fragment))).toThrow("symlink config path");

    const symlinkTarget = join(root, "target-parent");
    const symlinkParent = join(root, "parent-link");
    mkdirSync(symlinkTarget, { recursive: true });
    symlinkSync(symlinkTarget, symlinkParent, "dir");
    expect(() => mergeCodexConfig(options(root, join(symlinkParent, "config.toml"), fragment))).toThrow(
      "symlink parent directory",
    );

    const symlinkOutsideRoot = makeRoot();
    const symlinkOutsideParent = join(symlinkOutsideRoot, "sub");
    mkdirSync(symlinkOutsideParent, { recursive: true });
    const symlinkAncestor = join(root, "ancestor-link");
    symlinkSync(symlinkOutsideRoot, symlinkAncestor, "dir");
    expect(() =>
      mergeCodexConfig(options(root, join(symlinkAncestor, "sub", "config.toml"), fragment, {
        dryRun: false,
        backup: false,
      })),
    ).toThrow("symlink path component");
    expect(existsSync(join(symlinkOutsideParent, "config.toml"))).toBe(false);
  });

  test("path safety rejects canonical aliases under symlinked process HOME", () => {
    const root = makeRoot();
    const homeReal = join(root, "home-real");
    const homeLink = join(root, "home-link");
    const spoofedHome = join(root, "spoofed-home");
    const fragment = "[features]\ncodex_hooks = true\n";
    mkdirSync(homeReal, { recursive: true });
    mkdirSync(spoofedHome, { recursive: true });
    symlinkSync(homeReal, homeLink, "dir");

    withProcessHome(homeLink, () => {
      for (const homeDirName of [".codex", ".pai", ".claude"]) {
        const parent = join(homeReal, homeDirName);
        const configPath = join(parent, "config.toml");
        mkdirSync(parent, { recursive: true });

        expect(() =>
          mergeCodexConfig({
            configPath,
            fragment,
            dryRun: true,
            allowedRoot: homeReal,
            env: { HOME: spoofedHome },
          }),
        ).toThrow("real/home");

        expect(() =>
          mergeCodexConfig({
            configPath,
            fragment,
            dryRun: false,
            backup: false,
            allowedRoot: homeReal,
            env: { HOME: spoofedHome },
          }),
        ).toThrow("real/home");
        expect(existsSync(configPath)).toBe(false);
      }
    });
  });

  test("allows temp HOME .codex config only with explicit temp env and allowedRoot", () => {
    const root = makeRoot();
    const tempHome = join(root, "home");
    const configPath = join(tempHome, ".codex", "config.toml");
    mkdirSync(dirname(configPath), { recursive: true });

    const result = mergeCodexConfig({
      configPath,
      fragment: "[features]\ncodex_hooks = true\n",
      dryRun: false,
      backup: false,
      allowedRoot: tempHome,
      env: { HOME: tempHome },
    });

    expect(result.changed).toBe(true);
    expect(readFileSync(configPath, "utf-8")).toBe(result.content);

    for (const homeDirName of [".pai", ".claude"]) {
      const disallowedPath = join(tempHome, homeDirName, "config.toml");
      mkdirSync(dirname(disallowedPath), { recursive: true });
      expect(() =>
        mergeCodexConfig({
          configPath: disallowedPath,
          fragment: "[features]\ncodex_hooks = true\n",
          dryRun: false,
          backup: false,
          allowedRoot: tempHome,
          env: { HOME: tempHome },
        }),
      ).toThrow("configured HOME");
    }
  });

  test("unsupported TOML forms fail closed only when the merge would modify that area", () => {
    const root = makeRoot();
    const configPath = makeConfig(root);
    writeFileSync(
      configPath,
      [
        "[[agents]]",
        'name = "preserved"',
        "",
        "[features]",
        "multi_agent = true",
        "",
      ].join("\n"),
    );

    const preserved = mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n"));
    expect(preserved.content).toContain("[[agents]]");
    expect(preserved.content).toContain('name = "preserved"');

    writeFileSync(configPath, "[features]\ncodex.hooks = true\n");
    expect(() => mergeCodexConfig(options(root, configPath, "[features]\nother_key = true\n"))).toThrow(
      "Unsupported TOML syntax in target table features",
    );

    writeFileSync(configPath, "features.codex_hooks = false\n");
    expect(() => mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n"))).toThrow(
      "Unsupported TOML syntax in target table features",
    );

    writeFileSync(configPath, 'mcp_servers.github.command = "github-mcp"\n');
    expect(() =>
      mergeCodexConfig(options(root, configPath, '[mcp_servers.github]\ncommand = "pai-github-mcp"\n')),
    ).toThrow("Unsupported TOML syntax in target table mcp_servers.github");

    writeFileSync(configPath, "[features]\na = true\n\n[features]\nb = true\n");
    expect(() => mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n"))).toThrow(
      "Duplicate TOML table features",
    );

    writeFileSync(configPath, "");
    expect(() => mergeCodexConfig(options(root, configPath, "[[features]]\ncodex_hooks = true\n"))).toThrow(
      "Unsupported Codex config fragment syntax",
    );
    expect(() => mergeCodexConfig(options(root, configPath, "[features]\ncodex.hooks = true\n"))).toThrow(
      "Unsupported Codex config fragment syntax",
    );
    expect(() => mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = [true]\n"))).toThrow(
      "Unsupported Codex config fragment syntax",
    );
    expect(() => mergeCodexConfig(options(root, configPath, '[features]\ncodex_hooks = """multi"""\n'))).toThrow(
      "Unsupported Codex config fragment syntax",
    );
    expect(() => mergeCodexConfig(options(root, configPath, '[features]\ncodex_hooks = "unterminated\n'))).toThrow(
      "Merged Codex config TOML is invalid",
    );
    expect(() =>
      mergeCodexConfig(options(root, configPath, "[features]\ncodex_hooks = true\n", {
        sourceLabel: "bad\nlabel",
      })),
    ).toThrow("sourceLabel must be a single line");
  });
});
