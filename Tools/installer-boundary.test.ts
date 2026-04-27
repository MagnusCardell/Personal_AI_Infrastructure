#!/usr/bin/env bun

import { afterEach, describe, expect, test } from "bun:test";
import { spawnSync, type SpawnSyncReturns } from "child_process";
import {
  chmodSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from "fs";
import { tmpdir } from "os";
import { dirname, join, resolve } from "path";
import {
  runPrerequisites,
  runSystemDetect,
} from "../Releases/v4.0.3/.claude/PAI-Install/engine/actions";
import { detectSystem, type CommandRunner } from "../Releases/v4.0.3/.claude/PAI-Install/engine/detect";
import {
  buildCodexBoundaryMessage,
  CodexPrerequisiteMissingError,
  isPlatformBoundaryStop,
  maybeStopForUnsupportedCodexInstall,
  PlatformBoundaryStop,
} from "../Releases/v4.0.3/.claude/PAI-Install/engine/platform-boundary";
import {
  completeStepInMemory,
  createFreshState,
  loadState,
} from "../Releases/v4.0.3/.claude/PAI-Install/engine/state";
import type { EngineEvent, InstallerPlatform, ServerMessage } from "../Releases/v4.0.3/.claude/PAI-Install/engine/types";
import {
  getState,
  getMessageHistory,
  resetForTests,
  startInstallation,
} from "../Releases/v4.0.3/.claude/PAI-Install/web/routes";

const REPO_ROOT = resolve(import.meta.dir, "..");
const MAIN_TS = join(REPO_ROOT, "Releases", "v4.0.3", ".claude", "PAI-Install", "main.ts");
const TEST_TMPDIR = tmpdir();

type Scenario = {
  root: string;
  home: string;
  env: Record<string, string>;
  cleanup: () => void;
};

const savedEnv = {
  HOME: process.env.HOME,
  PATH: process.env.PATH,
  PAI_HOME: process.env.PAI_HOME,
  PAI_DIR: process.env.PAI_DIR,
  PAI_CONFIG_DIR: process.env.PAI_CONFIG_DIR,
  CODEX_HOME: process.env.CODEX_HOME,
  CLAUDE_HOME: process.env.CLAUDE_HOME,
  CLAUDE_DIR: process.env.CLAUDE_DIR,
  XDG_CACHE_HOME: process.env.XDG_CACHE_HOME,
  XDG_CONFIG_HOME: process.env.XDG_CONFIG_HOME,
  XDG_DATA_HOME: process.env.XDG_DATA_HOME,
  TMPDIR: process.env.TMPDIR,
  TMP: process.env.TMP,
  TEMP: process.env.TEMP,
  BUN_INSTALL_CACHE_DIR: process.env.BUN_INSTALL_CACHE_DIR,
  NO_COLOR: process.env.NO_COLOR,
  LANG: process.env.LANG,
  LC_ALL: process.env.LC_ALL,
  SHELL: process.env.SHELL,
};

afterEach(() => {
  for (const [key, value] of Object.entries(savedEnv)) {
    if (value === undefined) {
      delete process.env[key];
    } else {
      process.env[key] = value;
    }
  }
  resetForTests();
});

function makeScenario(): Scenario {
  const root = mkdtempSync(join(TEST_TMPDIR, "pai-pr03b-boundary-"));
  const home = join(root, "home");
  const temp = join(root, "tmp");
  mkdirSync(home);
  mkdirSync(temp);

  return {
    root,
    home,
    env: {
      HOME: home,
      SHELL: "/bin/sh",
      PAI_HOME: join(root, "pai-home"),
      PAI_DIR: join(root, "pai-dir"),
      PAI_CONFIG_DIR: join(root, "pai-config"),
      CODEX_HOME: join(root, "codex-home"),
      CLAUDE_HOME: join(root, "claude-home"),
      CLAUDE_DIR: join(root, "claude-dir"),
      XDG_CACHE_HOME: join(root, "xdg-cache"),
      XDG_CONFIG_HOME: join(root, "xdg-config"),
      XDG_DATA_HOME: join(root, "xdg-data"),
      TMPDIR: temp,
      TMP: temp,
      TEMP: temp,
      BUN_INSTALL_CACHE_DIR: join(root, "bun-cache"),
      NO_COLOR: "1",
      LANG: "C.UTF-8",
      LC_ALL: "C.UTF-8",
    },
    cleanup: () => rmSync(root, { recursive: true, force: true }),
  };
}

function assertNoRuntimeWrites(scenario: Scenario): void {
  const paths = [
    join(scenario.home, ".pai"),
    join(scenario.home, ".codex"),
    join(scenario.home, ".claude"),
    scenario.env.PAI_HOME,
    scenario.env.PAI_DIR,
    scenario.env.PAI_CONFIG_DIR,
    scenario.env.CODEX_HOME,
    scenario.env.CLAUDE_HOME,
    scenario.env.CLAUDE_DIR,
    join(scenario.env.PAI_CONFIG_DIR, "install-state.json"),
    join(scenario.env.CODEX_HOME, "config.toml"),
    join(scenario.env.CODEX_HOME, "hooks.json"),
    join(scenario.env.CODEX_HOME, "AGENTS.md"),
    join(scenario.env.CLAUDE_DIR, "settings.json"),
  ];

  for (const path of paths) {
    expect(existsSync(path)).toBe(false);
  }
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

function codexInstalledCommands() {
  return {
    ...baseCommands,
    "which codex": "/usr/local/bin/codex",
    "codex --version 2>&1": "codex 0.5.0",
  };
}

function stateFilePath(scenario: Scenario): string {
  return join(scenario.env.PAI_CONFIG_DIR, "install-state.json");
}

function seedSavedState(scenario: Scenario, platform: InstallerPlatform = "claude"): string {
  mkdirSync(scenario.env.PAI_CONFIG_DIR, { recursive: true });
  const content = JSON.stringify({
    version: "4.0",
    startedAt: "2026-04-27T00:00:00.000Z",
    updatedAt: "2026-04-27T00:00:00.000Z",
    currentStep: "identity",
    completedSteps: ["system-detect", "prerequisites", "api-keys"],
    skippedSteps: [],
    mode: "cli",
    platform,
    targetPlatforms: platform === "both" ? ["claude", "codex"] : [platform],
    detection: null,
    collected: { principalName: "Existing Claude User" },
    installType: null,
    errors: [],
  }, null, 2);
  writeFileSync(stateFilePath(scenario), content, { mode: 0o600 });
  return content;
}

function writeSeed(path: string, content: string): void {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, content);
}

function seedRuntimeFiles(scenario: Scenario): Map<string, string> {
  const seeds = new Map<string, string>([
    [join(scenario.home, ".pai", "marker.txt"), "home pai marker\n"],
    [join(scenario.home, ".codex", "config.toml"), "home codex config\n"],
    [join(scenario.home, ".codex", "hooks.json"), "{\"home\":true}\n"],
    [join(scenario.home, ".codex", "AGENTS.md"), "home codex agents\n"],
    [join(scenario.home, ".codex", "rules", "pai.md"), "home codex rule\n"],
    [join(scenario.home, ".claude", "settings.json"), "{\"homeClaude\":true}\n"],
    [join(scenario.home, ".agents", "skills", "Existing", "SKILL.md"), "existing global skill\n"],
    [join(scenario.env.PAI_HOME, "marker.txt"), "explicit pai home\n"],
    [join(scenario.env.PAI_DIR, "settings.json"), "{\"pai\":{\"version\":\"seed\"}}\n"],
    [join(scenario.env.CODEX_HOME, "config.toml"), "explicit codex config\n"],
    [join(scenario.env.CODEX_HOME, "hooks.json"), "{\"explicit\":true}\n"],
    [join(scenario.env.CODEX_HOME, "rules", "pai.md"), "explicit codex rule\n"],
    [join(scenario.env.CODEX_HOME, "agents", "pai.toml"), "name = \"pai\"\n"],
    [join(scenario.env.CLAUDE_HOME, "marker.txt"), "explicit claude home\n"],
    [join(scenario.env.CLAUDE_DIR, "settings.json"), "{\"explicitClaude\":true}\n"],
  ]);

  for (const [path, content] of seeds) {
    writeSeed(path, content);
  }
  return seeds;
}

function expectSeededFilesUnchanged(seeds: Map<string, string>): void {
  for (const [path, content] of seeds) {
    expect(readFileSync(path, "utf-8")).toBe(content);
  }
}

function writeExecutable(path: string, content: string): void {
  writeFileSync(path, content, { mode: 0o755 });
  chmodSync(path, 0o755);
}

function makeCliToolPath(scenario: Scenario): string {
  const binDir = join(scenario.root, "bin");
  mkdirSync(binDir);

  writeExecutable(join(binDir, "bun"), `#!/usr/bin/env bash
if [ "\${1:-}" = "--version" ]; then
  echo "1.2.3"
  exit 0
fi
echo "unexpected bun invocation" >&2
exit 79
`);
  writeExecutable(join(binDir, "git"), `#!/usr/bin/env bash
echo "git version 2.44.0"
`);
  writeExecutable(join(binDir, "node"), `#!/usr/bin/env bash
echo "v22.0.0"
`);
  writeExecutable(join(binDir, "codex"), `#!/usr/bin/env bash
echo "codex 0.5.0"
`);
  writeExecutable(join(binDir, "claude"), `#!/usr/bin/env bash
echo "1.0.0"
`);

  return `${binDir}:${process.env.PATH || "/usr/bin:/bin"}`;
}

function runCliMain(platform: InstallerPlatform, scenario: Scenario): SpawnSyncReturns<string> {
  return spawnSync(process.execPath, ["run", MAIN_TS, "--mode", "cli", "--platform", platform], {
    cwd: REPO_ROOT,
    env: {
      ...scenario.env,
      PATH: makeCliToolPath(scenario),
    },
    encoding: "utf-8",
    input: "",
  });
}

function runWebSocketStartInstall(platform: InstallerPlatform, scenario: Scenario): SpawnSyncReturns<string> {
  const routesPath = join(
    REPO_ROOT,
    "Releases",
    "v4.0.3",
    ".claude",
    "PAI-Install",
    "web",
    "routes.ts",
  );
  const script = `
const routes = await import(${JSON.stringify(routesPath)});
const messages = [];
const ws = { send(raw) { messages.push(JSON.parse(raw)); } };
routes.resetForTests();
routes.addClient(ws);
routes.handleWsMessage(ws, JSON.stringify({ type: "start_install" }));
await new Promise((resolve) => {
  const deadline = Date.now() + 2000;
  const tick = () => {
    if (messages.some((message) => message.type === "error" || message.type === "install_complete")) {
      resolve(undefined);
      return;
    }
    if (Date.now() >= deadline) {
      resolve(undefined);
      return;
    }
    setTimeout(tick, 10);
  };
  tick();
});
console.log(JSON.stringify(messages));
`;

  return spawnSync(process.execPath, ["-e", script], {
    cwd: REPO_ROOT,
    env: {
      ...scenario.env,
      PATH: makeCliToolPath(scenario),
      PAI_INSTALL_PLATFORM: platform,
    },
    encoding: "utf-8",
  });
}

async function runCliBoundaryFlow(
  platform: InstallerPlatform,
  scenario: Scenario,
  commands: Record<string, string | null>,
): Promise<{ state: ReturnType<typeof createFreshState>; events: EngineEvent[]; error: unknown }> {
  const oldConfigDir = process.env.PAI_CONFIG_DIR;
  process.env.PAI_CONFIG_DIR = scenario.env.PAI_CONFIG_DIR;

  const state = createFreshState("cli", { platform });
  const events: EngineEvent[] = [];
  const emit = async (event: EngineEvent) => {
    events.push(event);
  };

  let error: unknown;
  try {
    await runSystemDetect(state, emit, {
      env: scenario.env,
      homeDir: scenario.home,
      osPlatform: "linux",
      runner: strictRunner(commands),
    });
    completeStepInMemory(state, "system-detect");
    state.currentStep = "prerequisites";

    await runPrerequisites(state, emit);
    completeStepInMemory(state, "prerequisites");

    await maybeStopForUnsupportedCodexInstall(state, emit);
  } catch (err) {
    error = err;
  } finally {
    if (oldConfigDir === undefined) {
      delete process.env.PAI_CONFIG_DIR;
    } else {
      process.env.PAI_CONFIG_DIR = oldConfigDir;
    }
  }

  return { state, events, error };
}

function eventText(events: EngineEvent[]): string {
  return events
    .map((event) => {
      if (event.event === "message") return event.content;
      if (event.event === "progress") return event.detail;
      if (event.event === "error") return event.message;
      return event.event;
    })
    .join("\n");
}

function expectNoCollectionSteps(events: EngineEvent[]): void {
  const stepStarts = events
    .filter((event): event is Extract<EngineEvent, { event: "step_start" }> => event.event === "step_start")
    .map((event) => event.step);

  expect(stepStarts).toContain("system-detect");
  expect(stepStarts).toContain("prerequisites");
  expect(stepStarts).not.toContain("api-keys");
  expect(stepStarts).not.toContain("identity");
  expect(stepStarts).not.toContain("repository");
  expect(stepStarts).not.toContain("configuration");
  expect(stepStarts).not.toContain("voice");
  expect(stepStarts).not.toContain("validation");
}

function withProcessEnv(scenario: Scenario, path: string): void {
  process.env.HOME = scenario.home;
  process.env.PATH = path;
  for (const [key, value] of Object.entries(scenario.env)) {
    process.env[key] = value;
  }
}

function messageText(messages: ServerMessage[]): string {
  return messages
    .map((message) => {
      if (message.type === "message") return message.content;
      if (message.type === "error") return message.message;
      if (message.type === "progress") return message.detail;
      return message.type;
    })
    .join("\n");
}

function expectNoPr03aText(text: string): void {
  expect(text).not.toContain("PR-03A");
}

describe("Codex-selected installer boundary", () => {
  test("CLI flow stops after read-only prerequisites when Codex is installed", async () => {
    const scenario = makeScenario();
    try {
      const result = await runCliBoundaryFlow("codex", scenario, codexInstalledCommands());

      expect(result.error).toBeInstanceOf(PlatformBoundaryStop);
      expectNoCollectionSteps(result.events);
      expect(result.state.completedSteps).toEqual(["system-detect", "prerequisites"]);
      expect(result.state.currentStep).toBe("prerequisites");
      expect(result.state.collected).toEqual({});
      expect(existsSync(join(scenario.env.PAI_CONFIG_DIR, "install-state.json"))).toBe(false);

      const text = eventText(result.events);
      expectNoPr03aText(text);
      expect(text).toContain("Codex CLI detected");
      expect(text).toContain("Selected platform = codex");
      expect(text).toContain(`Planned PAI home = ${scenario.env.PAI_DIR}`);
      expect(text).toContain(`Planned Codex adapter/config home = ${scenario.env.CODEX_HOME}`);
      expect(text).toContain("Codex installer support is not implemented yet");
      expect(text).toContain("No files were written");
      expect(text).toContain("Run --platform claude");
      assertNoRuntimeWrites(scenario);
    } finally {
      scenario.cleanup();
    }
  });

  test("both-mode flow does not perform a partial Claude install", async () => {
    const scenario = makeScenario();
    try {
      const result = await runCliBoundaryFlow("both", scenario, {
        ...codexInstalledCommands(),
        "which claude": "/usr/local/bin/claude",
        "claude --version 2>&1": "1.0.0",
      });

      expect(result.error).toBeInstanceOf(PlatformBoundaryStop);
      expectNoCollectionSteps(result.events);
      expect(result.state.completedSteps).toEqual(["system-detect", "prerequisites"]);
      expect(result.state.currentStep).toBe("prerequisites");
      expect(result.state.collected).toEqual({});
      expect(existsSync(join(scenario.env.PAI_CONFIG_DIR, "install-state.json"))).toBe(false);

      const text = eventText(result.events);
      expectNoPr03aText(text);
      expect(text).toContain("Selected platform = both");
      expect(text).toContain("Both-mode installation is not implemented yet");
      expect(text).toContain("Run --platform claude");
      expect(result.events.some((event) => event.event === "step_start" && event.step === "repository")).toBe(false);
      assertNoRuntimeWrites(scenario);
    } finally {
      scenario.cleanup();
    }
  });

  test("CLI flow reports missing Codex with manual install hints before prompts", async () => {
    for (const platform of ["codex", "both"] as const) {
      const scenario = makeScenario();
      try {
        const result = await runCliBoundaryFlow(platform, scenario, {
          ...baseCommands,
          "which codex": null,
          "which claude": "/usr/local/bin/claude",
          "claude --version 2>&1": "1.0.0",
        });

        expect(result.error).toBeInstanceOf(CodexPrerequisiteMissingError);
        expect(isPlatformBoundaryStop(result.error)).toBe(true);
        expectNoCollectionSteps(result.events);
        expect(result.state.completedSteps).toEqual(["system-detect"]);
        expect(result.state.currentStep).toBe("prerequisites");
        expect(result.state.collected).toEqual({});
        expect(existsSync(join(scenario.env.PAI_CONFIG_DIR, "install-state.json"))).toBe(false);

        const text = eventText(result.events);
        expectNoPr03aText(text);
        expect(text).toContain("Codex CLI is required for the selected platform");
        expect(text).toContain("npm install -g @openai/codex");
        expect(text).toContain("brew install codex");
        assertNoRuntimeWrites(scenario);
      } finally {
        scenario.cleanup();
      }
    }
  });

  test("real CLI boundary leaves pre-existing saved state and runtime files untouched", () => {
    for (const platform of ["codex", "both"] as const) {
      const scenario = makeScenario();
      try {
        const savedState = seedSavedState(scenario, "claude");
        const seeds = seedRuntimeFiles(scenario);
        const result = runCliMain(platform, scenario);
        const output = `${result.stdout}\n${result.stderr}`;

        expect(result.status).toBe(2);
        expectNoPr03aText(output);
        expect(output).toContain(`Selected platform = ${platform}`);
        expect(output).toContain("No files were written");
        expect(output).not.toContain("Resume previous installation?");
        expect(output).not.toContain("API Keys");
        expect(output).not.toContain("Identity");
        expect(output).not.toContain("Installation complete");
        expect(readFileSync(stateFilePath(scenario), "utf-8")).toBe(savedState);
        expectSeededFilesUnchanged(seeds);
      } finally {
        scenario.cleanup();
      }
    }
  });

  test("web route flow emits terminal boundary without input or choice requests", async () => {
    for (const platform of ["codex", "both"] as const) {
      const scenario = makeScenario();
      try {
        withProcessEnv(scenario, "/usr/bin:/bin");
        resetForTests();

        await startInstallation({ platform, mode: "web" }, {
          env: scenario.env,
          homeDir: scenario.home,
          osPlatform: "linux",
          runner: strictRunner(platform === "both"
            ? {
              ...codexInstalledCommands(),
              "which claude": null,
            }
            : codexInstalledCommands()),
        });
        const messages = getMessageHistory();
        const types = messages.map((message) => message.type);
        const text = messageText(messages);
        expectNoPr03aText(text);

        expect(types).toContain("detection_result");
        expect(types).toContain("error");
        expect(types).not.toContain("input_request");
        expect(types).not.toContain("choice_request");
        expect(types).not.toContain("install_complete");
        expect(types).not.toContain("validation_result");
        expect(text).toContain(`Selected platform = ${platform}`);
        expect(text).toContain(platform === "both"
          ? "Both-mode installation is not implemented yet"
          : "Codex installer support is not implemented yet");
        expect(text).toContain("No files were written");
        expect(getState()?.currentStep).toBe("prerequisites");
        expect(loadState()).toBeNull();
        assertNoRuntimeWrites(scenario);
      } finally {
        scenario.cleanup();
      }
    }
  });

  test("web start_install message honors PAI_INSTALL_PLATFORM Codex boundary", () => {
    for (const platform of ["codex", "both"] as const) {
      const scenario = makeScenario();
      try {
        const savedState = seedSavedState(scenario, "claude");
        const seeds = seedRuntimeFiles(scenario);
        const result = runWebSocketStartInstall(platform, scenario);

        expect(result.status).toBe(0);
        expect(result.stderr).toBe("");

        const messages = JSON.parse(result.stdout.trim()) as ServerMessage[];
        const types = messages.map((message) => message.type);
        const text = messageText(messages);

        expectNoPr03aText(text);
        expect(types).toContain("detection_result");
        expect(types).toContain("error");
        expect(types).not.toContain("input_request");
        expect(types).not.toContain("choice_request");
        expect(types).not.toContain("install_complete");
        expect(types).not.toContain("validation_result");
        expect(text).toContain(`Selected platform = ${platform}`);
        expect(text).toContain(platform === "both"
          ? "Both-mode installation is not implemented yet"
          : "Codex installer support is not implemented yet");
        expect(text).toContain("No files were written");
        expect(readFileSync(stateFilePath(scenario), "utf-8")).toBe(savedState);
        expectSeededFilesUnchanged(seeds);
      } finally {
        scenario.cleanup();
      }
    }
  });

  test("web route boundary leaves pre-existing saved state and runtime files untouched", async () => {
    for (const platform of ["codex", "both"] as const) {
      const scenario = makeScenario();
      try {
        withProcessEnv(scenario, "/usr/bin:/bin");
        const savedState = seedSavedState(scenario, "claude");
        const seeds = seedRuntimeFiles(scenario);
        resetForTests();

        await startInstallation({ platform, mode: "web" }, {
          env: scenario.env,
          homeDir: scenario.home,
          osPlatform: "linux",
          runner: strictRunner(platform === "both"
            ? {
              ...codexInstalledCommands(),
              "which claude": null,
            }
            : codexInstalledCommands()),
        });

        const messages = getMessageHistory();
        const types = messages.map((message) => message.type);
        const text = messageText(messages);
        expectNoPr03aText(text);

        expect(types).toContain("error");
        expect(types).not.toContain("input_request");
        expect(types).not.toContain("choice_request");
        expect(text).toContain(`Selected platform = ${platform}`);
        expect(text).toContain("No files were written");
        expect(getState()?.currentStep).toBe("prerequisites");
        expect(readFileSync(stateFilePath(scenario), "utf-8")).toBe(savedState);
        expectSeededFilesUnchanged(seeds);
      } finally {
        scenario.cleanup();
      }
    }
  });

  test("web route flow reports missing Codex without saving state", async () => {
    for (const platform of ["codex", "both"] as const) {
      const scenario = makeScenario();
      try {
        withProcessEnv(scenario, "/usr/bin:/bin");
        resetForTests();

        await startInstallation({ platform, mode: "web" }, {
          env: scenario.env,
          homeDir: scenario.home,
          osPlatform: "linux",
          runner: strictRunner({
            ...baseCommands,
            "which codex": null,
            "which claude": "/usr/local/bin/claude",
            "claude --version 2>&1": "1.0.0",
          }),
        });
        const messages = getMessageHistory();
        const types = messages.map((message) => message.type);
        const text = messageText(messages);
        expectNoPr03aText(text);

        expect(types).toContain("error");
        expect(types).not.toContain("input_request");
        expect(types).not.toContain("choice_request");
        expect(types).not.toContain("install_complete");
        expect(text).toContain("Codex CLI is required for the selected platform");
        expect(text).toContain("npm install -g @openai/codex");
        expect(text).toContain("brew install codex");
        expect(getState()?.currentStep).toBe("prerequisites");
        expect(loadState()).toBeNull();
        assertNoRuntimeWrites(scenario);
      } finally {
        scenario.cleanup();
      }
    }
  });

  test("web route Codex-selected generic detection errors do not save state", async () => {
    const scenario = makeScenario();
    try {
      withProcessEnv(scenario, "/usr/bin:/bin");
      resetForTests();

      await startInstallation({ platform: "codex", mode: "web" }, {
        env: scenario.env,
        homeDir: scenario.home,
        osPlatform: "linux",
        runner: () => {
          throw new Error("fixture detection failure");
        },
      });

      const messages = getMessageHistory();
      const types = messages.map((message) => message.type);
      const text = messageText(messages);
      expectNoPr03aText(text);

      expect(types).toContain("error");
      expect(text).toContain("fixture detection failure");
      expect(loadState()).toBeNull();
      assertNoRuntimeWrites(scenario);
    } finally {
      scenario.cleanup();
    }
  });

  test("boundary message builder reports planned Codex paths", () => {
    const scenario = makeScenario();
    try {
      const state = createFreshState("cli", { platform: "codex" });
      state.detection = detectSystem({
        platform: "codex",
        env: scenario.env,
        homeDir: scenario.home,
        osPlatform: "linux",
        runner: strictRunner(codexInstalledCommands()),
      });

      const message = buildCodexBoundaryMessage(state);
      expectNoPr03aText(message);
      expect(message).toContain(`Planned PAI home = ${scenario.env.PAI_DIR}`);
      expect(message).toContain(`Planned Codex adapter/config home = ${scenario.env.CODEX_HOME}`);
    } finally {
      scenario.cleanup();
    }
  });
});
