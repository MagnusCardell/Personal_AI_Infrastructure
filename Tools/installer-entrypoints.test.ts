#!/usr/bin/env bun

import { describe, expect, test } from "bun:test";
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

const REPO_ROOT = resolve(import.meta.dir, "..");
const RELEASE_ROOT = join(REPO_ROOT, "Releases", "v4.0.3", ".claude");
const INSTALLER_ROOT = join(RELEASE_ROOT, "PAI-Install");

const OUTER_INSTALL = join(RELEASE_ROOT, "install.sh");
const INNER_INSTALL = join(INSTALLER_ROOT, "install.sh");
const MAIN_TS = join(INSTALLER_ROOT, "main.ts");
const WEB_SERVER_TS = join(INSTALLER_ROOT, "web", "server.ts");
const PUBLIC_APP_JS = join(INSTALLER_ROOT, "public", "app.js");
const ELECTRON_MAIN_JS = join(INSTALLER_ROOT, "electron", "main.js");

type IsolatedEnv = {
  root: string;
  env: Record<string, string>;
  home: string;
  paiHome: string;
  paiDir: string;
  paiConfigDir: string;
  codexHome: string;
  claudeHome: string;
  claudeDir: string;
  cleanup: () => void;
};

const SYSTEM_PATH = `${dirname(process.execPath)}:/usr/local/bin:/usr/bin:/bin`;

function createIsolatedEnv(path = SYSTEM_PATH): IsolatedEnv {
  const root = mkdtempSync(join(tmpdir(), "pai-entrypoint-env-"));
  const home = join(root, "home");
  const temp = join(root, "tmp");
  const paiHome = join(root, "pai-home");
  const paiDir = join(root, "pai-dir");
  const paiConfigDir = join(root, "pai-config");
  const codexHome = join(root, "codex-home");
  const claudeHome = join(root, "claude-home");
  const claudeDir = join(root, "claude-dir");

  mkdirSync(home);
  mkdirSync(temp);

  return {
    root,
    home,
    paiHome,
    paiDir,
    paiConfigDir,
    codexHome,
    claudeHome,
    claudeDir,
    env: {
      PATH: path,
      HOME: home,
      TMPDIR: temp,
      TMP: temp,
      TEMP: temp,
      PAI_HOME: paiHome,
      PAI_DIR: paiDir,
      PAI_CONFIG_DIR: paiConfigDir,
      CODEX_HOME: codexHome,
      CLAUDE_HOME: claudeHome,
      CLAUDE_DIR: claudeDir,
      XDG_CACHE_HOME: join(root, "xdg-cache"),
      XDG_CONFIG_HOME: join(root, "xdg-config"),
      XDG_DATA_HOME: join(root, "xdg-data"),
      BUN_INSTALL_CACHE_DIR: join(root, "bun-cache"),
      NO_COLOR: "1",
      LANG: "C.UTF-8",
      LC_ALL: "C.UTF-8",
    },
    cleanup: () => rmSync(root, { recursive: true, force: true }),
  };
}

function assertNoRuntimeWrites(env: IsolatedEnv): void {
  const disallowedPaths = [
    join(env.home, ".pai"),
    join(env.home, ".codex"),
    join(env.home, ".claude"),
    join(env.home, ".config", "pai"),
    join(env.home, ".config", "codex"),
    join(env.home, ".config", "claude"),
    join(env.home, ".local", "share", "pai"),
    env.paiHome,
    env.paiDir,
    env.paiConfigDir,
    env.codexHome,
    env.claudeHome,
    env.claudeDir,
    join(env.codexHome, "config.toml"),
    join(env.codexHome, "hooks.json"),
    join(env.codexHome, "AGENTS.md"),
    join(env.paiConfigDir, "install-state.json"),
    join(env.paiHome, "AGENTS.md"),
    join(env.paiHome, "config.toml"),
    join(env.claudeDir, "settings.json"),
  ];

  for (const path of disallowedPaths) {
    expect(existsSync(path)).toBe(false);
  }
}

function runCommand(
  command: string,
  args: string[],
  options: { env: Record<string, string>; cwd?: string },
): SpawnSyncReturns<string> {
  return spawnSync(command, args, {
    cwd: options.cwd ?? REPO_ROOT,
    env: options.env,
    encoding: "utf-8",
  });
}

function expectSuccess(result: SpawnSyncReturns<string>, label: string): void {
  if (result.status !== 0) {
    throw new Error(
      `${label} failed with status ${result.status}\nstdout:\n${result.stdout}\nstderr:\n${result.stderr}`,
    );
  }
}

function writeExecutable(path: string, content: string): void {
  writeFileSync(path, content, { mode: 0o755 });
  chmodSync(path, 0o755);
}

function makeToolStubs(binDir: string, argsFile: string, forbiddenFile: string): void {
  writeExecutable(
    join(binDir, "bun"),
    `#!/usr/bin/env bash
set -euo pipefail
if [ "\${1:-}" = "--version" ]; then
  echo "1.2.3"
  exit 0
fi
printf '%s\\n' "$@" > "$BUN_ARGS_FILE"
exit 0
`,
  );

  const forbiddenStub = `#!/usr/bin/env bash
set -euo pipefail
printf '%s %s\\n' "$0" "$*" >> "$FORBIDDEN_COMMANDS_FILE"
exit 79
`;

  for (const name of ["curl", "git", "claude", "brew", "apt-get", "yum", "sudo", "xcode-select", "npm"]) {
    writeExecutable(join(binDir, name), forbiddenStub);
  }
}

function runBootstrap(
  scriptPath: string,
  args: string[],
  displayState: "empty" | "unset" = "empty",
): { bunArgs: string[] | null; stdout: string; stderr: string; status: number | null } {
  const tempRoot = mkdtempSync(join(tmpdir(), "pai-entrypoint-tools-"));
  const binDir = join(tempRoot, "bin");
  const argsFile = join(tempRoot, "bun-args.txt");
  const forbiddenFile = join(tempRoot, "forbidden-commands.txt");
  const env = createIsolatedEnv(`${binDir}:/usr/bin:/bin:/usr/local/bin`);

  mkdirSync(binDir);
  makeToolStubs(binDir, argsFile, forbiddenFile);

  try {
    const childEnv = {
      ...env.env,
      BUN_ARGS_FILE: argsFile,
      FORBIDDEN_COMMANDS_FILE: forbiddenFile,
    };

    if (displayState === "empty") {
      childEnv.DISPLAY = "";
      childEnv.WAYLAND_DISPLAY = "";
    }

    const result = runCommand("bash", [scriptPath, ...args], {
      env: childEnv,
    });

    const forbiddenCalls = existsSync(forbiddenFile) ? readFileSync(forbiddenFile, "utf-8").trim() : "";
    expect(forbiddenCalls).toBe("");
    assertNoRuntimeWrites(env);

    return {
      bunArgs: existsSync(argsFile) ? readFileSync(argsFile, "utf-8").trim().split("\n") : null,
      stdout: result.stdout,
      stderr: result.stderr,
      status: result.status,
    };
  } finally {
    env.cleanup();
    rmSync(tempRoot, { recursive: true, force: true });
  }
}

function buildEntryPoint(entrypoint: string, outDirName: string, extraArgs: string[] = []): void {
  const outDir = mkdtempSync(join(tmpdir(), outDirName));
  const env = createIsolatedEnv();
  try {
    const result = runCommand("bun", [
      "build",
      entrypoint,
      "--target=bun",
      "--outdir",
      outDir,
      ...extraArgs,
    ], { env: env.env });
    expectSuccess(result, `bun build ${entrypoint}`);
    assertNoRuntimeWrites(env);
  } finally {
    env.cleanup();
    rmSync(outDir, { recursive: true, force: true });
  }
}

describe("installer entrypoint syntax guards", () => {
  test("shell bootstrap scripts pass bash syntax checks", () => {
    const env = createIsolatedEnv();
    try {
      expectSuccess(runCommand("bash", ["-n", OUTER_INSTALL], { env: env.env }), "bash -n release install.sh");
      expectSuccess(runCommand("bash", ["-n", INNER_INSTALL], { env: env.env }), "bash -n PAI-Install install.sh");
      assertNoRuntimeWrites(env);
    } finally {
      env.cleanup();
    }
  });

  test("Codex-selected bootstrap scripts reach bun and skip mutating installers", () => {
    const cases = [
      {
        args: ["--platform", "codex", "--mode", "cli"],
        expected: ["run", MAIN_TS, "--platform", "codex", "--mode", "cli"],
      },
      {
        args: ["--platform=codex", "--mode", "cli"],
        expected: ["run", MAIN_TS, "--platform=codex", "--mode", "cli"],
      },
      {
        args: ["--platform", "both", "--mode", "cli"],
        expected: ["run", MAIN_TS, "--platform", "both", "--mode", "cli"],
      },
      {
        args: ["--platform", "codex", "--mode", "gui"],
        expected: ["run", MAIN_TS, "--platform", "codex", "--mode", "gui"],
      },
      {
        args: ["--platform=codex", "--mode=gui"],
        expected: ["run", MAIN_TS, "--platform=codex", "--mode=gui"],
      },
      {
        args: ["--platform", "codex"],
        expected: ["run", MAIN_TS, "--mode", "cli", "--platform", "codex"],
      },
      {
        args: ["--platform=codex"],
        expected: ["run", MAIN_TS, "--mode", "cli", "--platform=codex"],
      },
      {
        args: ["--platform", "both"],
        expected: ["run", MAIN_TS, "--mode", "cli", "--platform", "both"],
      },
      {
        args: ["--platform=both"],
        expected: ["run", MAIN_TS, "--mode", "cli", "--platform=both"],
      },
    ];

    for (const scriptPath of [OUTER_INSTALL, INNER_INSTALL]) {
      for (const testCase of cases) {
        const result = runBootstrap(scriptPath, testCase.args);

        expect(result.status).toBe(0);
        expect(result.bunArgs).toEqual(testCase.expected);
        expect(result.stdout).toContain("Codex platform selection is read-only in PR-03A");
        expect(result.stdout).toContain("Skipping Git bootstrap for Codex-selected PR-03A run.");
        expect(result.stdout).toContain("Skipping Claude Code bootstrap for Codex-selected PR-03A run.");
        expect(result.stderr).toBe("");
      }
    }
  });

  test("Codex-selected bootstrap scripts tolerate unset display variables", () => {
    const cases = [
      {
        args: ["--platform", "codex"],
        expected: ["run", MAIN_TS, "--mode", "cli", "--platform", "codex"],
      },
      {
        args: ["--platform=codex"],
        expected: ["run", MAIN_TS, "--mode", "cli", "--platform=codex"],
      },
      {
        args: ["--platform", "both"],
        expected: ["run", MAIN_TS, "--mode", "cli", "--platform", "both"],
      },
      {
        args: ["--platform=both"],
        expected: ["run", MAIN_TS, "--mode", "cli", "--platform=both"],
      },
    ];

    for (const scriptPath of [OUTER_INSTALL, INNER_INSTALL]) {
      for (const testCase of cases) {
        const result = runBootstrap(scriptPath, testCase.args, "unset");

        expect(result.status).toBe(0);
        expect(result.bunArgs).toEqual(testCase.expected);
        expect(result.stdout).toContain("Codex platform selection is read-only in PR-03A");
        expect(result.stdout).toContain("Skipping Git bootstrap for Codex-selected PR-03A run.");
        expect(result.stdout).toContain("Skipping Claude Code bootstrap for Codex-selected PR-03A run.");
        expect(result.stderr).toBe("");
      }
    }
  });

  test("invalid platform selections fail closed before bootstrap tools run", () => {
    const cases = [
      {
        args: ["--platform"],
        message: "Unsupported installer platform: (missing). Expected one of: claude, codex, both.",
      },
      {
        args: ["--platform", "vim"],
        message: "Unsupported installer platform: vim. Expected one of: claude, codex, both.",
      },
      {
        args: ["--platform=unknown"],
        message: "Unsupported installer platform: unknown. Expected one of: claude, codex, both.",
      },
    ];

    for (const scriptPath of [OUTER_INSTALL, INNER_INSTALL]) {
      for (const testCase of cases) {
        const result = runBootstrap(scriptPath, testCase.args);

        expect(result.status).not.toBe(0);
        expect(result.bunArgs).toBeNull();
        expect(result.stdout + result.stderr).toContain(testCase.message);
      }
    }
  });

  test("JavaScript entrypoints pass syntax checks", () => {
    const env = createIsolatedEnv();
    try {
      const nodeProbe = runCommand("node", ["--version"], { env: env.env });

      if (nodeProbe.status === 0) {
        expectSuccess(runCommand("node", ["--check", PUBLIC_APP_JS], { env: env.env }), "node --check public/app.js");
        expectSuccess(runCommand("node", ["--check", ELECTRON_MAIN_JS], { env: env.env }), "node --check electron/main.js");
        assertNoRuntimeWrites(env);
        return;
      }

      buildEntryPoint(PUBLIC_APP_JS, "pai-entrypoint-public-");
      buildEntryPoint(ELECTRON_MAIN_JS, "pai-entrypoint-electron-", ["--external", "electron"]);
      assertNoRuntimeWrites(env);
    } finally {
      env.cleanup();
    }
  });

  test("TypeScript entrypoints build with Bun", () => {
    buildEntryPoint(MAIN_TS, "pai-entrypoint-main-");
    buildEntryPoint(WEB_SERVER_TS, "pai-entrypoint-web-");
  });
});
