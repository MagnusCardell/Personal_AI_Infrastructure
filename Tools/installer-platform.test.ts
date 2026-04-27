#!/usr/bin/env bun

import { describe, expect, test } from "bun:test";
import { join } from "path";
import { runPrerequisites, runRepository } from "../Releases/v4.0.3/.claude/PAI-Install/engine/actions";
import { detectSystem, type CommandRunner } from "../Releases/v4.0.3/.claude/PAI-Install/engine/detect";
import { parseInstallerOptions } from "../Releases/v4.0.3/.claude/PAI-Install/engine/options";
import { createFreshState, normalizeInstallState } from "../Releases/v4.0.3/.claude/PAI-Install/engine/state";
import type { EngineEvent } from "../Releases/v4.0.3/.claude/PAI-Install/engine/types";

const HOME = "/tmp/pai-pr03a-home";

function makeRunner(commands: Record<string, string | null>, seen: string[] = []): CommandRunner {
  return (cmd) => {
    seen.push(cmd);
    return Object.prototype.hasOwnProperty.call(commands, cmd) ? commands[cmd] : null;
  };
}

function detectForPlatform(
  platform: "claude" | "codex" | "both",
  commands: Record<string, string | null>,
  env: Record<string, string | undefined> = {},
  seen: string[] = [],
) {
  return detectSystem({
    platform,
    env: { HOME, SHELL: "/bin/sh", ...env },
    homeDir: HOME,
    osPlatform: "linux",
    runner: makeRunner(commands, seen),
  });
}

const baseTools = {
  "which bun": "/usr/local/bin/bun",
  "bun --version": "1.2.3",
  "which git": "/usr/bin/git",
  "git --version": "git version 2.44.0",
  "which node": "/usr/bin/node",
  "node --version": "v22.0.0",
  "which brew": null,
};

describe("installer platform option parsing", () => {
  test("defaults to Claude when no platform is specified", () => {
    const options = parseInstallerOptions([]);

    expect(options.mode).toBe("gui");
    expect(options.platform).toBe("claude");
    expect(options.targetPlatforms).toEqual(["claude"]);
  });

  test("parses space-separated platform values", () => {
    expect(parseInstallerOptions(["--platform", "claude"]).targetPlatforms).toEqual(["claude"]);
    expect(parseInstallerOptions(["--platform", "codex"]).targetPlatforms).toEqual(["codex"]);
    expect(parseInstallerOptions(["--platform", "both"]).targetPlatforms).toEqual(["claude", "codex"]);
  });

  test("parses equals-form platform values", () => {
    const options = parseInstallerOptions(["--platform=codex"]);

    expect(options.platform).toBe("codex");
    expect(options.targetPlatforms).toEqual(["codex"]);
  });

  test("rejects invalid platform values", () => {
    expect(() => parseInstallerOptions(["--platform", "vim"])).toThrow("Unsupported installer platform: vim");
    expect(() => parseInstallerOptions(["--platform=unknown"])).toThrow("Unsupported installer platform: unknown");
  });

  test("preserves existing mode parsing", () => {
    const options = parseInstallerOptions(["--mode", "cli", "--platform", "codex"]);

    expect(options.mode).toBe("cli");
    expect(options.platform).toBe("codex");
  });
});

describe("installer platform state", () => {
  test("normalizes legacy saved state without platform fields to Claude", () => {
    const legacy = createFreshState("cli") as any;
    delete legacy.platform;
    delete legacy.targetPlatforms;

    const normalized = normalizeInstallState(legacy);

    expect(normalized.platform).toBe("claude");
    expect(normalized.targetPlatforms).toEqual(["claude"]);
  });
});

describe("installer read-only platform detection", () => {
  test("Claude platform does not require or probe Codex", () => {
    const seen: string[] = [];
    const detection = detectForPlatform("claude", {
      ...baseTools,
      "which claude": "/usr/local/bin/claude",
      "claude --version 2>&1": "1.0.0",
    }, {}, seen);

    expect(detection.platform).toBe("claude");
    expect(detection.targetPlatforms).toEqual(["claude"]);
    expect(detection.tools.claude.installed).toBe(true);
    expect(detection.tools.codex.installed).toBe(false);
    expect(seen).not.toContain("which codex");
    expect(seen).not.toContain("codex --version 2>&1");
  });

  test("Codex platform detects installed Codex with an injected runner", () => {
    const seen: string[] = [];
    const detection = detectForPlatform("codex", {
      ...baseTools,
      "which codex": "/usr/local/bin/codex",
      "codex --version 2>&1": "codex 0.5.0",
    }, {}, seen);

    expect(detection.platform).toBe("codex");
    expect(detection.targetPlatforms).toEqual(["codex"]);
    expect(detection.tools.codex).toEqual({
      installed: true,
      version: "0.5.0",
      path: "/usr/local/bin/codex",
    });
    expect(detection.tools.claude.installed).toBe(false);
    expect(seen).not.toContain("which claude");
  });

  test("Codex platform reports missing Codex with manual install hints", async () => {
    const state = createFreshState("cli", { platform: "codex" });
    state.detection = detectForPlatform("codex", {
      ...baseTools,
      "which codex": null,
    });
    const events: EngineEvent[] = [];

    let error: unknown;
    try {
      await runPrerequisites(state, async (event) => events.push(event));
    } catch (err) {
      error = err;
    }

    expect(error).toBeInstanceOf(Error);
    expect(String(error)).toContain("Codex CLI is required for the selected platform");
    expect(String(error)).toContain("npm install -g @openai/codex");
    expect(String(error)).toContain("brew install codex");
    expect(events.some((event) => event.event === "message" && event.content.includes("npm install -g @openai/codex"))).toBe(true);
  });

  test("Both platform records Claude and Codex tool status", () => {
    const detection = detectForPlatform("both", {
      ...baseTools,
      "which claude": "/usr/local/bin/claude",
      "claude --version 2>&1": "1.1.0",
      "which codex": "/usr/local/bin/codex",
      "codex --version 2>&1": "codex 0.5.0",
    });

    expect(detection.platform).toBe("both");
    expect(detection.targetPlatforms).toEqual(["claude", "codex"]);
    expect(detection.tools.claude.installed).toBe(true);
    expect(detection.tools.claude.version).toBe("1.1.0");
    expect(detection.tools.codex.installed).toBe(true);
    expect(detection.tools.codex.version).toBe("0.5.0");
  });

  test("Codex selection plans ~/.pai as PAI home by default", () => {
    const detection = detectForPlatform("codex", {
      ...baseTools,
      "which codex": "/usr/local/bin/codex",
      "codex --version 2>&1": "codex 0.5.0",
    });

    expect(detection.paiDir).toBe(join(HOME, ".pai"));
    expect(detection.platformPaths.codex?.paiHome).toBe(join(HOME, ".pai"));
    expect(detection.platformPaths.codex?.adapterHome).toBe(join(HOME, ".codex"));
  });

  test("CODEX_HOME changes Codex adapter home without changing PAI home", () => {
    const detection = detectForPlatform("codex", {
      ...baseTools,
      "which codex": "/usr/local/bin/codex",
      "codex --version 2>&1": "codex 0.5.0",
    }, { CODEX_HOME: "~/codex-state" });

    expect(detection.platformPaths.codex?.paiHome).toBe(join(HOME, ".pai"));
    expect(detection.platformPaths.codex?.adapterHome).toBe(join(HOME, "codex-state"));
  });

  test("Claude selection with PAI_HOME keeps adapter home at ~/.claude", () => {
    const detection = detectForPlatform("claude", {
      ...baseTools,
      "which claude": "/usr/local/bin/claude",
      "claude --version 2>&1": "1.0.0",
    }, { PAI_HOME: "~/pai-core" });

    expect(detection.platformPaths.claude?.paiHome).toBe(join(HOME, "pai-core"));
    expect(detection.platformPaths.claude?.adapterHome).toBe(join(HOME, ".claude"));
  });

  test("Codex selected install fails closed before repository writes", async () => {
    const state = createFreshState("cli", { platform: "codex" });
    state.detection = detectForPlatform("codex", {
      ...baseTools,
      "which codex": "/usr/local/bin/codex",
      "codex --version 2>&1": "codex 0.5.0",
    });
    const events: EngineEvent[] = [];

    let error: unknown;
    try {
      await runRepository(state, async (event) => events.push(event));
    } catch (err) {
      error = err;
    }

    expect(error).toBeInstanceOf(Error);
    expect(String(error)).toContain("Codex installer writer support is not implemented yet");
    expect(events[0]).toEqual({ event: "step_start", step: "repository" });
  });
});
