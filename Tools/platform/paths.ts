import { homedir } from "os";
import { isAbsolute, join, resolve } from "path";

export type PaiPlatform = "claude" | "codex";

export type PaiHomeSource = "PAI_DIR" | "PAI_HOME" | "platform-default";
export type AdapterHomeSource = "PAI_DIR" | "CODEX_HOME" | "platform-default";
export type HomeDirSource = "explicit" | "HOME" | "os";

export interface PlatformPathEnv {
  HOME?: string;
  PAI_DIR?: string;
  PAI_HOME?: string;
  CODEX_HOME?: string;
  [key: string]: string | undefined;
}

export interface ResolvePlatformPathsOptions {
  platform: PaiPlatform;
  env?: PlatformPathEnv;
  homeDir?: string;
  osPlatform?: string;
}

export interface PlatformPaths {
  platform: PaiPlatform;
  homeDir: string;
  paiHome: string;
  adapterHome: string;
  claudeHome?: string;
  codexHome?: string;
  sources: {
    homeDir: HomeDirSource;
    paiHome: PaiHomeSource;
    adapterHome: AdapterHomeSource;
  };
}

interface ResolvedHomeDir {
  path: string;
  source: HomeDirSource;
}

interface ResolvedPathSource<Source extends string> {
  path: string;
  source: Source;
}

function nonEmpty(value: string | undefined): string | undefined {
  const trimmed = value?.trim();
  return trimmed ? trimmed : undefined;
}

function assertSupportedRuntime(osPlatform: string): void {
  if (osPlatform !== "darwin" && osPlatform !== "linux") {
    throw new Error(`Unsupported OS platform for PAI path resolution: ${osPlatform}`);
  }
}

function assertPaiPlatform(platform: string): asserts platform is PaiPlatform {
  if (platform !== "claude" && platform !== "codex") {
    throw new Error(`Unsupported PAI platform: ${platform}`);
  }
}

function absolutePath(pathValue: string, baseDir: string): string {
  return isAbsolute(pathValue) ? pathValue : resolve(baseDir, pathValue);
}

export function expandHomePath(pathValue: string, homeDir: string): string {
  return pathValue
    .replace(/^\$HOME(?=\/|$)/, homeDir)
    .replace(/^\$\{HOME\}(?=\/|$)/, homeDir)
    .replace(/^~(?=\/|$)/, homeDir);
}

export function resolvePathValue(pathValue: string, homeDir: string): string {
  return absolutePath(expandHomePath(pathValue, homeDir), homeDir);
}

export function resolveHomeDir(options: Pick<ResolvePlatformPathsOptions, "env" | "homeDir"> = {}): ResolvedHomeDir {
  const explicitHome = nonEmpty(options.homeDir);
  if (explicitHome) {
    return {
      path: absolutePath(explicitHome, process.cwd()),
      source: "explicit",
    };
  }

  const envHome = nonEmpty(options.env?.HOME);
  if (envHome) {
    return {
      path: absolutePath(envHome, process.cwd()),
      source: "HOME",
    };
  }

  return {
    path: homedir(),
    source: "os",
  };
}

export function defaultPaiHome(platform: PaiPlatform, homeDir: string): string {
  assertPaiPlatform(platform);
  return join(homeDir, platform === "claude" ? ".claude" : ".pai");
}

export function defaultAdapterHome(platform: PaiPlatform, homeDir: string): string {
  assertPaiPlatform(platform);
  return join(homeDir, platform === "claude" ? ".claude" : ".codex");
}

export function resolvePaiHome(
  platform: PaiPlatform,
  env: PlatformPathEnv = {},
  homeDir = resolveHomeDir({ env }).path,
): ResolvedPathSource<PaiHomeSource> {
  assertPaiPlatform(platform);

  const legacyPaiDir = nonEmpty(env.PAI_DIR);
  if (legacyPaiDir) {
    return {
      path: resolvePathValue(legacyPaiDir, homeDir),
      source: "PAI_DIR",
    };
  }

  const paiHome = nonEmpty(env.PAI_HOME);
  if (paiHome) {
    return {
      path: resolvePathValue(paiHome, homeDir),
      source: "PAI_HOME",
    };
  }

  return {
    path: defaultPaiHome(platform, homeDir),
    source: "platform-default",
  };
}

export function resolveAdapterHome(
  platform: PaiPlatform,
  env: PlatformPathEnv = {},
  homeDir = resolveHomeDir({ env }).path,
  resolvedPaiHome?: ResolvedPathSource<PaiHomeSource>,
): ResolvedPathSource<AdapterHomeSource> {
  assertPaiPlatform(platform);

  if (platform === "claude") {
    const paiHome = resolvedPaiHome ?? resolvePaiHome(platform, env, homeDir);
    if (paiHome.source === "PAI_DIR") {
      return {
        path: paiHome.path,
        source: "PAI_DIR",
      };
    }

    return {
      path: defaultAdapterHome(platform, homeDir),
      source: "platform-default",
    };
  }

  const codexHome = nonEmpty(env.CODEX_HOME);
  if (codexHome) {
    return {
      path: resolvePathValue(codexHome, homeDir),
      source: "CODEX_HOME",
    };
  }

  return {
    path: defaultAdapterHome(platform, homeDir),
    source: "platform-default",
  };
}

export function resolvePlatformPaths(options: ResolvePlatformPathsOptions): PlatformPaths {
  assertPaiPlatform(options.platform);
  assertSupportedRuntime(options.osPlatform ?? process.platform);

  const env = options.env ?? process.env;
  const homeDir = resolveHomeDir({ env, homeDir: options.homeDir });
  const paiHome = resolvePaiHome(options.platform, env, homeDir.path);
  const adapterHome = resolveAdapterHome(options.platform, env, homeDir.path, paiHome);

  return {
    platform: options.platform,
    homeDir: homeDir.path,
    paiHome: paiHome.path,
    adapterHome: adapterHome.path,
    claudeHome: options.platform === "claude" ? adapterHome.path : undefined,
    codexHome: options.platform === "codex" ? adapterHome.path : undefined,
    sources: {
      homeDir: homeDir.source,
      paiHome: paiHome.source,
      adapterHome: adapterHome.source,
    },
  };
}
