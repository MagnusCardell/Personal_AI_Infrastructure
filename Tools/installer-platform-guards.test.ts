#!/usr/bin/env bun

import { describe, expect, test } from "bun:test";
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";
import { statePlatformMatchesOptions } from "../Releases/v4.0.3/.claude/PAI-Install/cli/index";
import {
  runConfiguration,
  runPrerequisites,
  runRepository,
  runVoiceSetup,
} from "../Releases/v4.0.3/.claude/PAI-Install/engine/actions";
import { detectSystem, type CommandRunner } from "../Releases/v4.0.3/.claude/PAI-Install/engine/detect";
import {
  clearState,
  createFreshState,
  loadState,
  saveState,
} from "../Releases/v4.0.3/.claude/PAI-Install/engine/state";
import type { EngineEvent } from "../Releases/v4.0.3/.claude/PAI-Install/engine/types";

type InstallerPlatformSelection = "claude" | "codex" | "both";

function tempHome(): string {
  return mkdtempSync(join(tmpdir(), "pai-pr03a-home-"));
}

function strictRunner(commands: Record<string, string | null>, seen: string[] = []): CommandRunner {
  return (cmd) => {
    seen.push(cmd);
    if (!Object.prototype.hasOwnProperty.call(commands, cmd)) {
      throw new Error(`Unexpected command in detection fixture: ${cmd}`);
    }
    return commands[cmd];
  };
}

function detectForPlatform(
  platform: InstallerPlatformSelection,
  commands: Record<string, string | null>,
  env: Record<string, string | undefined> = {},
  seen: string[] = [],
  home = tempHome(),
) {
  return detectSystem({
    platform,
    env: { HOME: home, SHELL: "/bin/sh", ...env },
    homeDir: home,
    osPlatform: "linux",
    runner: strictRunner(commands, seen),
  });
}

const baseCommands = {
  "cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"'": "Ubuntu 24.04.1 LTS",
  "uname -r": "6.8.0-test",
  "/bin/sh --version 2>&1 | head -1": "GNU bash, version 5.2.21",
  "which bun": "/usr/local/bin/bun",
  "bun --version": "1.2.3",
  "which git": "/usr/bin/git",
  "git --version": "git version 2.44.0",
  "which node": "/usr/bin/node",
  "node --version": "v22.0.0",
  "which brew": null,
};

describe("installer platform guard coverage", () => {
  test("state persistence preserves platform fields under temp PAI_CONFIG_DIR", () => {
    const oldConfigDir = process.env.PAI_CONFIG_DIR;
    const configDir = mkdtempSync(join(tmpdir(), "pai-pr03a-config-"));

    try {
      process.env.PAI_CONFIG_DIR = configDir;
      clearState();

      const state = createFreshState("cli", { platform: "both" });
      saveState(state);

      const loaded = loadState();
      expect(loaded?.platform).toBe("both");
      expect(loaded?.targetPlatforms).toEqual(["claude", "codex"]);

      clearState();
      expect(loadState()).toBeNull();
      expect(existsSync(join(configDir, "install-state.json"))).toBe(false);
    } finally {
      if (oldConfigDir === undefined) {
        delete process.env.PAI_CONFIG_DIR;
      } else {
        process.env.PAI_CONFIG_DIR = oldConfigDir;
      }
      rmSync(configDir, { recursive: true, force: true });
    }
  });

  test("legacy on-disk state without platform fields loads as Claude", () => {
    const oldConfigDir = process.env.PAI_CONFIG_DIR;
    const configDir = mkdtempSync(join(tmpdir(), "pai-pr03a-config-"));

    try {
      process.env.PAI_CONFIG_DIR = configDir;
      const legacy = createFreshState("cli") as any;
      delete legacy.platform;
      delete legacy.targetPlatforms;
      writeFileSync(join(configDir, "install-state.json"), JSON.stringify(legacy), { mode: 0o600 });

      const loaded = loadState();
      expect(loaded?.platform).toBe("claude");
      expect(loaded?.targetPlatforms).toEqual(["claude"]);
    } finally {
      if (oldConfigDir === undefined) {
        delete process.env.PAI_CONFIG_DIR;
      } else {
        process.env.PAI_CONFIG_DIR = oldConfigDir;
      }
      rmSync(configDir, { recursive: true, force: true });
    }
  });

  test("CLI resume state must match requested platform", () => {
    const saved = createFreshState("cli", { platform: "claude" });

    expect(statePlatformMatchesOptions(saved, { platform: "claude" })).toBe(true);
    expect(statePlatformMatchesOptions(saved, { platform: "codex" })).toBe(false);
  });

  test("strict Codex detection does not probe Claude", () => {
    const seen: string[] = [];
    const detection = detectForPlatform("codex", {
      ...baseCommands,
      "which codex": "/usr/local/bin/codex",
      "codex --version 2>&1": "codex 0.5.0",
    }, {}, seen);

    expect(detection.tools.codex.installed).toBe(true);
    expect(seen).not.toContain("which claude");
    expect(seen).not.toContain("claude --version 2>&1");
  });

  test("unsafe SHELL values are not executed during detection", () => {
    const seen: string[] = [];
    const detection = detectForPlatform("claude", {
      ...baseCommands,
      "which claude": "/usr/local/bin/claude",
      "claude --version 2>&1": "1.0.0",
    }, { SHELL: "/bin/sh\";touch /tmp/pai-pr03a-bad" }, seen);

    expect(detection.shell.version).toBe("");
    expect(seen.some((cmd) => cmd.includes("touch /tmp/pai-pr03a-bad"))).toBe(false);
  });

  test("Claude PAI_HOME is planning metadata and does not move writer paiDir", () => {
    const home = tempHome();
    const detection = detectForPlatform("claude", {
      ...baseCommands,
      "which claude": "/usr/local/bin/claude",
      "claude --version 2>&1": "1.0.0",
    }, { PAI_HOME: "~/pai-core" }, [], home);

    expect(detection.paiDir).toBe(join(home, ".claude"));
    expect(detection.platformPaths.claude?.paiHome).toBe(join(home, "pai-core"));
    expect(detection.platformPaths.claude?.adapterHome).toBe(join(home, ".claude"));
  });

  test("Claude PAI_DIR preserves legacy writer and adapter home", () => {
    const home = tempHome();
    const detection = detectForPlatform("claude", {
      ...baseCommands,
      "which claude": "/usr/local/bin/claude",
      "claude --version 2>&1": "1.0.0",
    }, { PAI_DIR: "~/legacy-claude" }, [], home);

    expect(detection.paiDir).toBe(join(home, "legacy-claude"));
    expect(detection.platformPaths.claude?.paiHome).toBe(join(home, "legacy-claude"));
    expect(detection.platformPaths.claude?.adapterHome).toBe(join(home, "legacy-claude"));
  });

  test("Codex prerequisites skip mutating installs even when generic tools are missing", async () => {
    const state = createFreshState("cli", { platform: "codex" });
    state.detection = detectForPlatform("codex", {
      ...baseCommands,
      "which bun": null,
      "which git": null,
      "which codex": "/usr/local/bin/codex",
      "codex --version 2>&1": "codex 0.5.0",
    });
    const events: EngineEvent[] = [];

    await runPrerequisites(state, async (event) => events.push(event));

    expect(events).toContainEqual({ event: "step_complete", step: "prerequisites" });
    expect(events.some(
      (event) => event.event === "progress" && event.detail.includes("skipping mutating prerequisite installs"),
    )).toBe(true);
  });

  test("Codex and both selections fail closed before repository/configuration/voice writes", async () => {
    const home = tempHome();
    const state = createFreshState("cli", { platform: "both" });
    state.detection = detectForPlatform("both", {
      ...baseCommands,
      "which claude": "/usr/local/bin/claude",
      "claude --version 2>&1": "1.1.0",
      "which codex": "/usr/local/bin/codex",
      "codex --version 2>&1": "codex 0.5.0",
    }, {}, [], home);

    await expect(runRepository(state, async () => {})).rejects.toThrow("Codex installer writer support is not implemented yet");
    await expect(runConfiguration(state, async () => {})).rejects.toThrow("Codex installer writer support is not implemented yet");
    await expect(runVoiceSetup(
      state,
      async () => {},
      async () => "disabled",
      async () => "",
    )).rejects.toThrow("Codex installer writer support is not implemented yet");

    expect(existsSync(join(home, ".claude", "settings.json"))).toBe(false);
    expect(existsSync(join(home, ".pai"))).toBe(false);
    expect(existsSync(join(home, ".codex"))).toBe(false);
  });

  test("Claude writer stages reject shell-unsafe PAI directory values", async () => {
    const state = createFreshState("cli", { platform: "claude" });
    state.detection = detectForPlatform("claude", {
      ...baseCommands,
      "which claude": "/usr/local/bin/claude",
      "claude --version 2>&1": "1.0.0",
    });
    state.detection.paiDir = "/tmp/pai-pr03a-unsafe\";touch /tmp/pai-pr03a-bad";

    await expect(runRepository(state, async () => {})).rejects.toThrow("unsafe for installer shell commands");
  });

  test("shell bootstrap preserves headless mode forwarding with platform args", () => {
    const innerScript = readFileSync(
      join(import.meta.dir, "..", "Releases", "v4.0.3", ".claude", "PAI-Install", "install.sh"),
      "utf-8",
    );
    const outerScript = readFileSync(
      join(import.meta.dir, "..", "Releases", "v4.0.3", ".claude", "install.sh"),
      "utf-8",
    );

    expect(innerScript).toContain('exec bun run "$INSTALLER_DIR/main.ts" --mode "$INSTALL_MODE" "$@"');
    expect(innerScript).toContain("Codex platform selection is read-only");
    expect(innerScript).toContain("Skipping Git bootstrap for Codex-selected installer boundary.");
    expect(innerScript).toContain("Skipping Claude Code bootstrap for Codex-selected installer boundary.");
    expect(innerScript).toContain("Unsupported installer platform: (missing)");
    expect(innerScript).not.toContain("PR-03A");

    expect(outerScript).toContain("Codex platform selection is read-only");
    expect(outerScript).toContain("Skipping Git bootstrap for Codex-selected installer boundary.");
    expect(outerScript).toContain("Skipping Claude Code bootstrap for Codex-selected installer boundary.");
    expect(outerScript).toContain("Unsupported installer platform: (missing)");
    expect(outerScript).not.toContain("PR-03A");
  });

  test("Codex GUI mode cannot trigger Electron dependency npm install", () => {
    const main = readFileSync(
      join(import.meta.dir, "..", "Releases", "v4.0.3", ".claude", "PAI-Install", "main.ts"),
      "utf-8",
    );
    const guardIndex = main.indexOf('includesTargetPlatform(options, "codex")');
    const npmInstallIndex = main.indexOf('spawnSync("npm", ["install"]');

    expect(guardIndex).toBeGreaterThan(-1);
    expect(npmInstallIndex).toBeGreaterThan(-1);
    expect(guardIndex).toBeLessThan(npmInstallIndex);
    expect(main).toContain("Codex-selected GUI runs do not auto-install GUI dependencies yet");
  });
});
