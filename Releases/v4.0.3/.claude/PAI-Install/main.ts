#!/usr/bin/env bun
/**
 * PAI Installer v4.0 — Main Entry Point
 * Routes to CLI, Web server (for Electron), or GUI (Electron app).
 *
 * Modes:
 *   --mode cli   → Interactive terminal wizard
 *   --mode web   → Start HTTP/WebSocket server (used internally by Electron)
 *   --mode gui   → Launch Electron app (which spawns web mode internally)
 */

import { spawn, spawnSync, execSync } from "child_process";
import { join } from "path";
import { existsSync } from "fs";
import { includesTargetPlatform, parseInstallerOptions } from "./engine/options";

const args = process.argv.slice(2);

const ROOT = import.meta.dir;

async function main() {
  const options = parseInstallerOptions(args);
  const mode = options.mode;

  if (mode === "cli") {
    // Run CLI wizard
    const { runCLI } = await import("./cli/index");
    await runCLI(options);
  } else if (mode === "web") {
    // Start the HTTP + WebSocket server (Electron loads this)
    process.env.PAI_INSTALL_PLATFORM = options.platform;
    await import("./web/server");
  } else {
    // Launch Electron GUI app
    const electronDir = join(ROOT, "electron");
    const electronPkg = join(electronDir, "node_modules", ".package-lock.json");

    // Install electron dependencies if needed
    if (!existsSync(electronPkg)) {
      if (includesTargetPlatform(options, "codex")) {
        throw new Error(
          "GUI dependencies are not installed. Codex-selected GUI runs do not auto-install GUI dependencies yet. " +
          "Run with --mode cli for read-only detection, or preinstall GUI dependencies before launching GUI mode.",
        );
      }

      console.log("Installing GUI dependencies (first run only)...\n");
      const install = spawnSync("npm", ["install"], {
        cwd: electronDir,
        stdio: "inherit",
      });
      if (install.status !== 0) {
        console.error("Failed to install GUI dependencies. Falling back to CLI...\n");
        const { runCLI } = await import("./cli/index");
        await runCLI(options);
        return;
      }
    }

    // Clear macOS quarantine flags (prevents "app is damaged" error on copied installs)
    if (process.platform === "darwin") {
      try {
        execSync(`xattr -cr "${electronDir}"`, { stdio: "pipe", timeout: 30000 });
        console.log("Cleared macOS quarantine flags.\n");
      } catch {
        // Non-fatal
      }
    }

    console.log("Starting PAI Installer GUI...\n");
    const child = spawn("npm", ["start"], {
      cwd: electronDir,
      env: {
        ...process.env,
        PAI_INSTALL_PLATFORM: options.platform,
      },
      stdio: "inherit",
    });

    child.on("exit", (code) => {
      process.exit(code || 0);
    });
  }
}

main().catch((err) => {
  console.error("Fatal error:", err.message);
  process.exit(1);
});
