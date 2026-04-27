import type { InstallerMode, InstallerOptions, InstallerPlatform } from "./types";
import type { PaiPlatform } from "../../PAI/Tools/platform/paths";

const INSTALLER_PLATFORMS = new Set<InstallerPlatform>(["claude", "codex", "both"]);

export function targetPlatformsFor(platform: InstallerPlatform): PaiPlatform[] {
  return platform === "both" ? ["claude", "codex"] : [platform];
}

export function isInstallerPlatform(value: string): value is InstallerPlatform {
  return INSTALLER_PLATFORMS.has(value as InstallerPlatform);
}

function normalizeMode(value: string | undefined): InstallerMode {
  return value === "cli" || value === "web" || value === "gui" ? value : "gui";
}

export function normalizeInstallerOptions(options: Partial<InstallerOptions> = {}): InstallerOptions {
  const platform = options.platform ?? "claude";
  if (!isInstallerPlatform(platform)) {
    throw new Error(`Unsupported installer platform: ${platform}. Expected one of: claude, codex, both.`);
  }

  return {
    mode: normalizeMode(options.mode),
    platform,
    targetPlatforms: targetPlatformsFor(platform),
  };
}

export function includesTargetPlatform(
  target: Pick<InstallerOptions, "targetPlatforms">,
  platform: PaiPlatform,
): boolean {
  return target.targetPlatforms.includes(platform);
}

export function parseInstallerOptions(argv: string[]): InstallerOptions {
  let mode: InstallerMode = "gui";
  let platform: InstallerPlatform = "claude";

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];

    if (arg === "--mode") {
      mode = normalizeMode(argv[++i]);
      continue;
    }

    if (arg.startsWith("--mode=")) {
      mode = normalizeMode(arg.slice("--mode=".length));
      continue;
    }

    if (arg === "--platform") {
      const value = argv[++i];
      if (!value || !isInstallerPlatform(value)) {
        throw new Error(`Unsupported installer platform: ${value || "(missing)"}. Expected one of: claude, codex, both.`);
      }
      platform = value;
      continue;
    }

    if (arg.startsWith("--platform=")) {
      const value = arg.slice("--platform=".length);
      if (!isInstallerPlatform(value)) {
        throw new Error(`Unsupported installer platform: ${value || "(missing)"}. Expected one of: claude, codex, both.`);
      }
      platform = value;
    }
  }

  return normalizeInstallerOptions({ mode, platform });
}
