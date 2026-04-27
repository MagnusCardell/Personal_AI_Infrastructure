#!/usr/bin/env bun

import { describe, expect, test } from "bun:test";
import { join } from "path";
import {
  defaultAdapterHome,
  defaultPaiHome,
  expandHomePath,
  resolveHomeDir,
  resolvePaiHome,
  resolvePathValue,
  resolvePlatformPaths,
} from "./paths";

const HOME = "/tmp/pai-pr02-home";
const OTHER_HOME = "/tmp/pai-pr02-other-home";

describe("platform path resolution", () => {
  test("resolves Claude defaults with empty env to ~/.claude", () => {
    const paths = resolvePlatformPaths({
      platform: "claude",
      env: {},
      homeDir: HOME,
      osPlatform: "linux",
    });

    expect(paths.homeDir).toBe(HOME);
    expect(paths.paiHome).toBe(join(HOME, ".claude"));
    expect(paths.adapterHome).toBe(join(HOME, ".claude"));
    expect(paths.claudeHome).toBe(join(HOME, ".claude"));
    expect(paths.codexHome).toBeUndefined();
    expect(paths.sources).toEqual({
      homeDir: "explicit",
      paiHome: "platform-default",
      adapterHome: "platform-default",
    });
  });

  test("resolves Codex defaults with empty env to ~/.pai and ~/.codex", () => {
    const paths = resolvePlatformPaths({
      platform: "codex",
      env: {},
      homeDir: HOME,
      osPlatform: "linux",
    });

    expect(paths.paiHome).toBe(join(HOME, ".pai"));
    expect(paths.adapterHome).toBe(join(HOME, ".codex"));
    expect(paths.codexHome).toBe(join(HOME, ".codex"));
    expect(paths.claudeHome).toBeUndefined();
    expect(paths.sources.paiHome).toBe("platform-default");
    expect(paths.sources.adapterHome).toBe("platform-default");
  });

  test("resolves platform defaults from helpers", () => {
    expect(defaultPaiHome("claude", HOME)).toBe(join(HOME, ".claude"));
    expect(defaultAdapterHome("claude", HOME)).toBe(join(HOME, ".claude"));
    expect(defaultPaiHome("codex", HOME)).toBe(join(HOME, ".pai"));
    expect(defaultAdapterHome("codex", HOME)).toBe(join(HOME, ".codex"));
  });

  test("uses PAI_HOME before platform defaults", () => {
    const paths = resolvePlatformPaths({
      platform: "codex",
      env: { PAI_HOME: "~/pai-home" },
      homeDir: HOME,
      osPlatform: "linux",
    });

    expect(paths.paiHome).toBe(join(HOME, "pai-home"));
    expect(paths.adapterHome).toBe(join(HOME, ".codex"));
    expect(paths.sources.paiHome).toBe("PAI_HOME");
    expect(paths.sources.adapterHome).toBe("platform-default");
  });

  test("keeps Claude adapter home at ~/.claude when PAI_HOME moves the neutral PAI home", () => {
    const paths = resolvePlatformPaths({
      platform: "claude",
      env: { PAI_HOME: "~/custom-claude-pai" },
      homeDir: HOME,
      osPlatform: "linux",
    });

    expect(paths.paiHome).toBe(join(HOME, "custom-claude-pai"));
    expect(paths.adapterHome).toBe(join(HOME, ".claude"));
    expect(paths.claudeHome).toBe(join(HOME, ".claude"));
    expect(paths.sources.paiHome).toBe("PAI_HOME");
    expect(paths.sources.adapterHome).toBe("platform-default");
  });

  test("uses PAI_DIR before PAI_HOME for legacy compatibility", () => {
    const paths = resolvePlatformPaths({
      platform: "codex",
      env: {
        PAI_DIR: "~/legacy-pai",
        PAI_HOME: "~/pai-home",
      },
      homeDir: HOME,
      osPlatform: "linux",
    });

    expect(paths.paiHome).toBe(join(HOME, "legacy-pai"));
    expect(paths.adapterHome).toBe(join(HOME, ".codex"));
    expect(paths.sources.paiHome).toBe("PAI_DIR");
    expect(paths.sources.adapterHome).toBe("platform-default");
  });

  test("uses PAI_DIR before PAI_HOME for Claude legacy compatibility", () => {
    const paths = resolvePlatformPaths({
      platform: "claude",
      env: {
        PAI_DIR: "~/legacy-claude",
        PAI_HOME: "~/pai-home",
      },
      homeDir: HOME,
      osPlatform: "linux",
    });

    expect(paths.paiHome).toBe(join(HOME, "legacy-claude"));
    expect(paths.adapterHome).toBe(join(HOME, "legacy-claude"));
    expect(paths.claudeHome).toBe(join(HOME, "legacy-claude"));
    expect(paths.sources.paiHome).toBe("PAI_DIR");
    expect(paths.sources.adapterHome).toBe("PAI_DIR");
  });

  test("uses CODEX_HOME for the Codex adapter home without changing PAI home", () => {
    const paths = resolvePlatformPaths({
      platform: "codex",
      env: {
        CODEX_HOME: "~/codex-config",
      },
      homeDir: HOME,
      osPlatform: "linux",
    });

    expect(paths.paiHome).toBe(join(HOME, ".pai"));
    expect(paths.adapterHome).toBe(join(HOME, "codex-config"));
    expect(paths.codexHome).toBe(join(HOME, "codex-config"));
    expect(paths.sources.paiHome).toBe("platform-default");
    expect(paths.sources.adapterHome).toBe("CODEX_HOME");
  });

  test("keeps PAI_HOME and CODEX_HOME separate for Codex", () => {
    const paths = resolvePlatformPaths({
      platform: "codex",
      env: {
        PAI_HOME: "~/pai-app",
        CODEX_HOME: "~/codex-state",
      },
      homeDir: HOME,
      osPlatform: "linux",
    });

    expect(paths.paiHome).toBe(join(HOME, "pai-app"));
    expect(paths.adapterHome).toBe(join(HOME, "codex-state"));
    expect(paths.sources.paiHome).toBe("PAI_HOME");
    expect(paths.sources.adapterHome).toBe("CODEX_HOME");
  });

  test("keeps PAI_DIR and CODEX_HOME separate for Codex", () => {
    const paths = resolvePlatformPaths({
      platform: "codex",
      env: {
        PAI_DIR: "~/legacy-pai",
        CODEX_HOME: "~/codex-state",
      },
      homeDir: HOME,
      osPlatform: "linux",
    });

    expect(paths.paiHome).toBe(join(HOME, "legacy-pai"));
    expect(paths.adapterHome).toBe(join(HOME, "codex-state"));
    expect(paths.sources.paiHome).toBe("PAI_DIR");
    expect(paths.sources.adapterHome).toBe("CODEX_HOME");
  });

  test("ignores CODEX_HOME for Claude path resolution", () => {
    const paths = resolvePlatformPaths({
      platform: "claude",
      env: {
        CODEX_HOME: "~/codex-state",
      },
      homeDir: HOME,
      osPlatform: "linux",
    });

    expect(paths.paiHome).toBe(join(HOME, ".claude"));
    expect(paths.adapterHome).toBe(join(HOME, ".claude"));
    expect(paths.sources.paiHome).toBe("platform-default");
    expect(paths.sources.adapterHome).toBe("platform-default");
  });

  test("ignores CODEX_HOME for Claude when PAI_DIR preserves legacy combined home", () => {
    const paths = resolvePlatformPaths({
      platform: "claude",
      env: {
        PAI_DIR: "~/legacy-claude",
        CODEX_HOME: "~/codex-state",
      },
      homeDir: HOME,
      osPlatform: "linux",
    });

    expect(paths.paiHome).toBe(join(HOME, "legacy-claude"));
    expect(paths.adapterHome).toBe(join(HOME, "legacy-claude"));
    expect(paths.claudeHome).toBe(join(HOME, "legacy-claude"));
    expect(paths.sources.paiHome).toBe("PAI_DIR");
    expect(paths.sources.adapterHome).toBe("PAI_DIR");
  });

  test("expands supported home forms in path values", () => {
    expect(expandHomePath("~", HOME)).toBe(HOME);
    expect(expandHomePath("~/PAI", HOME)).toBe(join(HOME, "PAI"));
    expect(expandHomePath("$HOME/PAI", HOME)).toBe(join(HOME, "PAI"));
    expect(expandHomePath("${HOME}/PAI", HOME)).toBe(join(HOME, "PAI"));
    expect(resolvePathValue("relative-pai", HOME)).toBe(join(HOME, "relative-pai"));
  });

  test("uses env HOME as the temp home when no explicit homeDir is supplied", () => {
    const paths = resolvePlatformPaths({
      platform: "codex",
      env: { HOME },
      osPlatform: "linux",
    });

    expect(paths.homeDir).toBe(HOME);
    expect(paths.paiHome).toBe(join(HOME, ".pai"));
    expect(paths.adapterHome).toBe(join(HOME, ".codex"));
    expect(paths.sources.homeDir).toBe("HOME");
  });

  test("accepts darwin as a supported platform gate", () => {
    const paths = resolvePlatformPaths({
      platform: "claude",
      env: {},
      homeDir: HOME,
      osPlatform: "darwin",
    });

    expect(paths.paiHome).toBe(join(HOME, ".claude"));
  });

  test("uses explicit homeDir before env HOME", () => {
    const homeDir = resolveHomeDir({
      env: { HOME: OTHER_HOME },
      homeDir: HOME,
    });

    expect(homeDir.path).toBe(HOME);
    expect(homeDir.source).toBe("explicit");

    const paths = resolvePlatformPaths({
      platform: "claude",
      env: { HOME: OTHER_HOME },
      homeDir: HOME,
      osPlatform: "linux",
    });

    expect(paths.homeDir).toBe(HOME);
    expect(paths.paiHome).toBe(join(HOME, ".claude"));
  });

  test("rejects Windows path resolution as out of scope", () => {
    expect(() =>
      resolvePlatformPaths({
        platform: "codex",
        env: {},
        homeDir: "C:\\Users\\pai",
        osPlatform: "win32",
      }),
    ).toThrow("Unsupported OS platform for PAI path resolution: win32");
  });

  test("rejects unknown PAI platforms at runtime", () => {
    expect(() =>
      resolvePlatformPaths({
        platform: "vscode" as any,
        env: {},
        homeDir: HOME,
        osPlatform: "linux",
      }),
    ).toThrow("Unsupported PAI platform: vscode");

    expect(() => resolvePaiHome("vscode" as any, {}, HOME)).toThrow("Unsupported PAI platform: vscode");
  });
});
