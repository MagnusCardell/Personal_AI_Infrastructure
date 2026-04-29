/**
 * Codex adapter install-plan primitive.
 *
 * PR-04C keeps this module unwired from CLI, web, and installer runtime flows.
 * It renders Codex AGENTS.md content through BuildInstructions and writes only
 * to explicit, contained temp adapter homes when called directly by tests.
 */

import {
  chmodSync,
  closeSync,
  constants,
  existsSync,
  lstatSync,
  mkdirSync,
  openSync,
  readFileSync,
  realpathSync,
  renameSync,
  rmdirSync,
  statSync,
  unlinkSync,
  writeFileSync,
} from "fs";
import { randomUUID } from "crypto";
import { homedir, tmpdir } from "os";
import { basename, dirname, isAbsolute, join, parse, relative, resolve, sep } from "path";
import { buildInstructions } from "../../PAI/Tools/BuildInstructions";
import { mergeCodexConfig } from "./codex-config-merge";

export interface CodexAdapterPlanOptions {
  paiHome: string;
  adapterHome: string;
  allowedRoot: string;
  env?: Record<string, string | undefined>;
  dryRun?: boolean;
  backup?: boolean;
  now?: Date;

  settingsPath?: string;
  algorithmDir?: string;
  algorithmLatestPath?: string;
  agentsTemplatePath?: string;

  configFragment?: string;
  configPath?: string;
  sourceLabel?: string;
}

export interface CodexAdapterPlanOperation {
  kind:
    | "render-agents"
    | "write-agents"
    | "merge-config"
    | "skip-config";
  path?: string;
  changed?: boolean;
  backupPath?: string;
  reason?: string;
}

export interface CodexAdapterPlanResult {
  paiHome: string;
  adapterHome: string;
  agentsPath: string;
  configPath: string;
  operations: CodexAdapterPlanOperation[];
  agentsContent: string;
}

const DEFAULT_SOURCE_LABEL = "PAI PR-04C test fragment";

function productRootFromEnginePath(): string {
  return resolve(import.meta.dir, "../../../../..");
}

function productCodexAgentsTemplatePath(): string {
  return resolve(import.meta.dir, "../../PAI/Adapters/codex/AGENTS.md.template");
}

function isWithinPath(parentPath: string, candidatePath: string): boolean {
  const parent = resolve(parentPath);
  const candidate = resolve(candidatePath);
  const rel = relative(parent, candidate);
  return rel === "" || (!!rel && !rel.startsWith("..") && !isAbsolute(rel));
}

function assertNotWithin(label: string, deniedRoot: string, candidatePath: string): void {
  if (isWithinPath(deniedRoot, candidatePath)) {
    throw new Error(`Refusing Codex adapter plan inside ${label}: ${candidatePath}`);
  }
}

function isSymlink(path: string): boolean {
  try {
    return lstatSync(path).isSymbolicLink();
  } catch {
    return false;
  }
}

function currentHome(env: Record<string, string | undefined> = process.env): string {
  return resolve(env.HOME || homedir());
}

function isExplicitTempHomeAgentsPath(options: CodexAdapterPlanOptions, home: string, agentsPath: string): boolean {
  if (!options.env?.HOME || !options.allowedRoot) return false;

  const requestedHome = resolve(home);
  const expectedAgentsPath = join(requestedHome, ".codex", "AGENTS.md");
  return resolve(options.env.HOME) === requestedHome
    && resolve(agentsPath) === expectedAgentsPath
    && isWithinPath(tmpdir(), requestedHome)
    && requestedHome !== resolve(tmpdir())
    && isWithinPath(requestedHome, agentsPath)
    && isWithinPath(resolve(options.allowedRoot), agentsPath);
}

function assertExplicitTempHomeCodexAgentsPath(options: CodexAdapterPlanOptions, agentsPath: string): void {
  if (!options.env?.HOME) {
    throw new Error("Codex adapter plan writes require explicit env.HOME for temp HOME/.codex targeting");
  }

  const requestedHome = resolve(options.env.HOME);
  const expectedAgentsPath = join(requestedHome, ".codex", "AGENTS.md");

  if (!isWithinPath(tmpdir(), requestedHome) || requestedHome === resolve(tmpdir())) {
    throw new Error(`Codex adapter plan writes require a temp HOME under ${tmpdir()}: ${requestedHome}`);
  }
  assertNoSymlinkComponents(parse(requestedHome).root, requestedHome);
  if (isSymlink(requestedHome)) {
    throw new Error(`Refusing Codex adapter plan through symlink temp HOME: ${requestedHome}`);
  }
  if (!existsSync(requestedHome) || !lstatSync(requestedHome).isDirectory()) {
    throw new Error(`Codex adapter plan writes require an existing temp HOME directory: ${requestedHome}`);
  }
  if (resolve(agentsPath) !== expectedAgentsPath) {
    throw new Error(`Codex adapter plan writes are limited to explicit temp HOME/.codex/AGENTS.md: ${agentsPath}`);
  }
  if (!isWithinPath(resolve(options.allowedRoot), agentsPath)) {
    throw new Error(`Refusing Codex adapter plan outside allowedRoot: ${agentsPath}`);
  }
}

function candidateRealPaths(path: string): string[] {
  const candidates = [resolve(path)];
  try {
    candidates.push(realpathSync(path));
  } catch {
    try {
      candidates.push(join(realpathSync(dirname(path)), basename(path)));
    } catch {
      // Lexical checks still apply when neither the file nor parent exists.
    }
  }
  return [...new Set(candidates)];
}

function assertProtectedHomeRoots(options: CodexAdapterPlanOptions, agentsPath: string): void {
  const configuredHome = currentHome(options.env);
  const processHome = resolve(process.env.HOME || homedir());
  const candidatePaths = candidateRealPaths(agentsPath);

  const protectedHomeRoots = [
    ["real/home Codex CLI state/config home", join(processHome, ".codex"), processHome, false],
    ["real/home default PAI home", join(processHome, ".pai"), processHome, false],
    ["real/home Claude adapter home", join(processHome, ".claude"), processHome, false],
    ["configured HOME Codex CLI state/config home", join(configuredHome, ".codex"), configuredHome, true],
    ["configured HOME default PAI home", join(configuredHome, ".pai"), configuredHome, false],
    ["configured HOME Claude adapter home", join(configuredHome, ".claude"), configuredHome, false],
  ] as const;

  for (const [label, root, home, allowExplicitTempHome] of protectedHomeRoots) {
    const allowedTempHomePath = allowExplicitTempHome && isExplicitTempHomeAgentsPath(options, home, agentsPath);
    const rootCandidates = candidateRealPaths(root);

    for (const rootCandidate of rootCandidates) {
      if (candidatePaths.some((candidatePath) => isWithinPath(rootCandidate, candidatePath)) && !allowedTempHomePath) {
        throw new Error(`Refusing Codex adapter plan inside ${label}: ${agentsPath}`);
      }
    }
  }
}

function assertAllowedRoot(options: CodexAdapterPlanOptions): string {
  if (!options.allowedRoot || !options.allowedRoot.trim()) {
    throw new Error("Codex adapter plan requires an explicit allowedRoot");
  }

  const allowedRoot = resolve(options.allowedRoot);
  const productRoot = productRootFromEnginePath();
  if (allowedRoot === parse(allowedRoot).root || allowedRoot === resolve(tmpdir()) || allowedRoot === resolve(productRoot)) {
    throw new Error(`Refusing broad Codex adapter plan allowedRoot: ${options.allowedRoot}`);
  }

  if (!existsSync(allowedRoot)) {
    throw new Error(`Codex adapter plan allowedRoot must exist: ${allowedRoot}`);
  }
  assertNoSymlinkComponents(parse(allowedRoot).root, allowedRoot);
  if (isSymlink(allowedRoot)) {
    throw new Error(`Refusing Codex adapter plan through symlink allowedRoot: ${allowedRoot}`);
  }
  if (!lstatSync(allowedRoot).isDirectory()) {
    throw new Error(`Codex adapter plan allowedRoot must be a directory: ${allowedRoot}`);
  }

  return allowedRoot;
}

function assertNoSymlinkComponents(rootPath: string, descendantPath: string): void {
  const root = resolve(rootPath);
  const descendant = resolve(descendantPath);
  const rel = relative(root, descendant);
  if (rel.startsWith("..") || isAbsolute(rel)) return;

  let current = root;
  for (const segment of rel.split(sep)) {
    if (!segment) continue;
    current = join(current, segment);
    if (existsSync(current) && isSymlink(current)) {
      throw new Error(`Refusing Codex adapter plan through symlink path component: ${current}`);
    }
  }
}

function assertNoProtectedRepositoryPaths(agentsPath: string): void {
  const productRoot = productRootFromEnginePath();
  const rootAgents = resolve(productRoot, "AGENTS.md");
  if (resolve(agentsPath) === rootAgents) {
    throw new Error(`Refusing Codex adapter plan write to repository AGENTS.md: ${agentsPath}`);
  }

  assertNotWithin("repository governance .codex directory", join(productRoot, ".codex"), agentsPath);
  assertNotWithin("working directory governance .codex directory", join(process.cwd(), ".codex"), agentsPath);
}

function assertTemplateSourceAllowed(options: CodexAdapterPlanOptions): void {
  if (!options.agentsTemplatePath) return;

  const productRoot = productRootFromEnginePath();
  const resolvedTemplate = resolve(options.agentsTemplatePath);
  const allowedRoot = resolve(options.allowedRoot);
  const productTemplateCandidates = candidateRealPaths(productCodexAgentsTemplatePath());
  const templateCandidates = candidateRealPaths(resolvedTemplate);
  for (const templateCandidate of templateCandidates) {
    assertNotWithin("repository governance .codex template source", join(productRoot, ".codex"), templateCandidate);
    assertNotWithin("working directory governance .codex template source", join(process.cwd(), ".codex"), templateCandidate);
  }
  for (const templateCandidate of templateCandidates) {
    if (productTemplateCandidates.some((productTemplate) => resolve(templateCandidate) === resolve(productTemplate))) {
      continue;
    }
    if (!isWithinPath(tmpdir(), allowedRoot) || !isWithinPath(allowedRoot, templateCandidate)) {
      throw new Error(`Codex adapter plan explicit agentsTemplatePath must be the product template or inside temp allowedRoot: ${options.agentsTemplatePath}`);
    }
    assertNoSymlinkComponents(allowedRoot, templateCandidate);
  }
}

function assertPaiHomeAllowed(options: CodexAdapterPlanOptions): string {
  const paiHome = resolve(options.paiHome);
  const adapterHome = resolve(options.adapterHome);

  if (isWithinPath(adapterHome, paiHome) || isWithinPath(paiHome, adapterHome)) {
    throw new Error(`Codex adapter plan requires PAI_HOME separate from Codex adapter/config home: ${paiHome}`);
  }

  const productRoot = productRootFromEnginePath();
  const configuredHome = currentHome(options.env);
  const processHome = resolve(process.env.HOME || homedir());
  const deniedRoots = [
    ["repository governance .codex directory", join(productRoot, ".codex")],
    ["working directory governance .codex directory", join(process.cwd(), ".codex")],
    ["real/home Codex CLI state/config home", join(processHome, ".codex")],
    ["configured HOME Codex CLI state/config home", join(configuredHome, ".codex")],
  ] as const;

  for (const paiHomeCandidate of candidateRealPaths(paiHome)) {
    for (const [label, deniedRoot] of deniedRoots) {
      for (const deniedCandidate of candidateRealPaths(deniedRoot)) {
        if (isWithinPath(deniedCandidate, paiHomeCandidate)) {
          throw new Error(`Refusing Codex adapter plan with PAI_HOME inside ${label}: ${paiHome}`);
        }
      }
    }
  }

  return paiHome;
}

function resolveAgentsPath(options: CodexAdapterPlanOptions): string {
  if (!options.adapterHome || !options.adapterHome.trim()) {
    throw new Error("Codex adapter plan requires an explicit adapterHome");
  }

  const adapterHome = resolve(options.adapterHome);
  return join(adapterHome, "AGENTS.md");
}

function assertAgentsPathAllowed(options: CodexAdapterPlanOptions): { allowedRoot: string; adapterHome: string; agentsPath: string } {
  const agentsPath = resolveAgentsPath(options);
  const adapterHome = dirname(agentsPath);

  if (basename(agentsPath) !== "AGENTS.md") {
    throw new Error(`Codex adapter plan writes are limited to AGENTS.md outputs: ${agentsPath}`);
  }

  assertNoProtectedRepositoryPaths(agentsPath);

  const allowedRoot = assertAllowedRoot(options);
  if (!isWithinPath(allowedRoot, agentsPath)) {
    throw new Error(`Refusing Codex adapter plan outside allowedRoot: ${agentsPath}`);
  }
  if (!options.dryRun) {
    assertExplicitTempHomeCodexAgentsPath(options, agentsPath);
  }

  assertProtectedHomeRoots(options, agentsPath);

  if (existsSync(adapterHome) && isSymlink(adapterHome)) {
    throw new Error(`Refusing Codex adapter plan through symlink adapterHome: ${adapterHome}`);
  }
  if (isSymlink(dirname(adapterHome))) {
    throw new Error(`Refusing Codex adapter plan through symlink parent directory: ${dirname(adapterHome)}`);
  }
  if (isSymlink(agentsPath)) {
    throw new Error(`Refusing Codex adapter plan into symlink AGENTS.md path: ${agentsPath}`);
  }

  assertNoSymlinkComponents(allowedRoot, adapterHome);

  if (existsSync(adapterHome)) {
    const realAllowedRoot = realpathSync(allowedRoot);
    const realAdapterHome = realpathSync(adapterHome);
    if (!isWithinPath(realAllowedRoot, realAdapterHome)) {
      throw new Error(`Refusing Codex adapter plan outside allowedRoot after realpath resolution: ${agentsPath}`);
    }
    assertProtectedHomeRoots(options, join(realAdapterHome, "AGENTS.md"));
  }

  return { allowedRoot, adapterHome, agentsPath };
}

function timestamp(now: Date): string {
  const pad = (value: number): string => String(value).padStart(2, "0");
  return [
    now.getUTCFullYear(),
    pad(now.getUTCMonth() + 1),
    pad(now.getUTCDate()),
    "-",
    pad(now.getUTCHours()),
    pad(now.getUTCMinutes()),
    pad(now.getUTCSeconds()),
  ].join("");
}

function writeExclusiveFile(path: string, content: string, mode: number): void {
  const fd = openSync(path, constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL, mode);
  let closed = false;

  try {
    writeFileSync(fd, content, "utf-8");
    closeSync(fd);
    closed = true;
    chmodSync(path, mode);
  } catch (error) {
    if (!closed) {
      try {
        closeSync(fd);
      } catch {
        // Best-effort cleanup only.
      }
    }
    try {
      unlinkSync(path);
    } catch {
      // Best-effort cleanup only.
    }
    throw error;
  }
}

function writeAgentsAtomically(agentsPath: string, content: string, mode: number): void {
  const parent = dirname(agentsPath);
  const tempPath = join(parent, `.${basename(agentsPath)}.pai-tmp-${process.pid}-${randomUUID()}`);

  try {
    writeExclusiveFile(tempPath, content, mode);
    renameSync(tempPath, agentsPath);
  } catch (error) {
    try {
      if (existsSync(tempPath) || isSymlink(tempPath)) unlinkSync(tempPath);
    } catch {
      // Best-effort cleanup only.
    }
    throw error;
  }
}

function assertAdapterHomeDirectorySafe(options: CodexAdapterPlanOptions, adapterHome: string, agentsPath: string): void {
  if (!existsSync(adapterHome) || !lstatSync(adapterHome).isDirectory()) {
    throw new Error(`Codex adapter plan adapterHome must be a directory: ${adapterHome}`);
  }
  if (isSymlink(adapterHome)) {
    throw new Error(`Refusing Codex adapter plan through symlink adapterHome: ${adapterHome}`);
  }

  assertNoSymlinkComponents(resolve(options.allowedRoot), adapterHome);
  const realAllowedRoot = realpathSync(resolve(options.allowedRoot));
  const realAdapterHome = realpathSync(adapterHome);
  if (!isWithinPath(realAllowedRoot, realAdapterHome)) {
    throw new Error(`Refusing Codex adapter plan outside allowedRoot after realpath resolution: ${agentsPath}`);
  }
  assertProtectedHomeRoots(options, join(realAdapterHome, "AGENTS.md"));
}

function ensureAdapterHomeDirectoryForWrite(
  options: CodexAdapterPlanOptions,
  adapterHome: string,
  agentsPath: string,
): boolean {
  let created = false;
  if (!existsSync(adapterHome)) {
    mkdirSync(adapterHome, { recursive: true, mode: 0o700 });
    created = true;
  }

  assertAdapterHomeDirectorySafe(options, adapterHome, agentsPath);
  return created;
}

function writeAgentsFile(
  options: CodexAdapterPlanOptions,
  agentsPath: string,
  adapterHome: string,
  content: string,
): CodexAdapterPlanOperation {
  if (options.dryRun) {
    return {
      kind: "write-agents",
      path: agentsPath,
      changed: false,
      reason: "dryRun",
    };
  }

  ensureAdapterHomeDirectoryForWrite(options, adapterHome, agentsPath);
  if (isSymlink(agentsPath)) {
    throw new Error(`Refusing Codex adapter plan into symlink AGENTS.md path: ${agentsPath}`);
  }

  const existingContent = existsSync(agentsPath) ? readFileSync(agentsPath, "utf-8") : "";
  if (existsSync(agentsPath) && existingContent === content) {
    return {
      kind: "write-agents",
      path: agentsPath,
      changed: false,
      reason: "AGENTS.md already current",
    };
  }

  let backupPath: string | undefined;
  const mode = existsSync(agentsPath) ? statSync(agentsPath).mode & 0o777 : 0o600;

  if (options.backup && existsSync(agentsPath)) {
    backupPath = join(dirname(agentsPath), `${basename(agentsPath)}.pai-backup-${timestamp(options.now || new Date())}`);
    if (isSymlink(backupPath)) {
      throw new Error(`Refusing Codex adapter plan backup through symlink path: ${backupPath}`);
    }
    if (existsSync(backupPath)) {
      throw new Error(`Refusing to overwrite existing Codex AGENTS.md backup: ${backupPath}`);
    }
    writeExclusiveFile(backupPath, existingContent, mode);
  }

  writeAgentsAtomically(agentsPath, content, mode);

  return {
    kind: "write-agents",
    path: agentsPath,
    changed: true,
    backupPath,
  };
}

function renderCodexAgents(options: CodexAdapterPlanOptions): string {
  assertTemplateSourceAllowed(options);

  const result = buildInstructions({
    target: "codex",
    paiHome: options.paiHome,
    adapterHome: options.adapterHome,
    templatePath: options.agentsTemplatePath,
    settingsPath: options.settingsPath,
    algorithmDir: options.algorithmDir,
    algorithmLatestPath: options.algorithmLatestPath,
    dryRun: true,
  });

  if (!result.content) {
    throw new Error(result.reason || "Codex AGENTS.md content was not rendered");
  }

  return result.content;
}

function configOperation(options: CodexAdapterPlanOptions): CodexAdapterPlanOperation {
  if (options.configFragment === undefined) {
    return {
      kind: "skip-config",
      path: options.configPath || join(resolve(options.adapterHome), "config.toml"),
      changed: false,
      reason: "No configFragment supplied; PR-04C does not define product Codex config defaults",
    };
  }

  if (!options.configPath) {
    throw new Error("Codex adapter plan config merge requires an explicit configPath when configFragment is supplied");
  }
  if (resolve(options.configPath) !== join(resolve(options.adapterHome), "config.toml")) {
    throw new Error(`Codex adapter plan configPath is limited to adapterHome/config.toml: ${options.configPath}`);
  }

  const result = mergeCodexConfig({
    configPath: options.configPath,
    fragment: options.configFragment,
    sourceLabel: options.sourceLabel || DEFAULT_SOURCE_LABEL,
    dryRun: options.dryRun,
    backup: options.backup,
    now: options.now,
    allowedRoot: options.allowedRoot,
    env: options.env,
  });

  const conflictReason = result.conflicts.length
    ? `Codex config merge conflicts: ${result.conflicts
      .map((conflict) => `${conflict.table || "<top-level>"}.${conflict.key} at line ${conflict.existingLine}`)
      .join(", ")}`
    : undefined;

  return {
    kind: "merge-config",
    path: result.configPath,
    changed: result.changed,
    backupPath: result.backupPath,
    reason: conflictReason,
  };
}

function preflightConfigOperation(options: CodexAdapterPlanOptions): void {
  if (options.dryRun || options.configFragment === undefined) return;

  if (!options.configPath) {
    throw new Error("Codex adapter plan config merge requires an explicit configPath when configFragment is supplied");
  }
  if (resolve(options.configPath) !== join(resolve(options.adapterHome), "config.toml")) {
    throw new Error(`Codex adapter plan configPath is limited to adapterHome/config.toml: ${options.configPath}`);
  }

  const result = mergeCodexConfig({
    configPath: options.configPath,
    fragment: options.configFragment,
    sourceLabel: options.sourceLabel || DEFAULT_SOURCE_LABEL,
    dryRun: true,
    backup: options.backup,
    now: options.now,
    allowedRoot: options.allowedRoot,
    env: options.env,
  });

  const configPath = resolve(options.configPath);
  if (result.changed && options.backup && existsSync(configPath)) {
    const backupPath = join(dirname(configPath), `${basename(configPath)}.pai-backup-${timestamp(options.now || new Date())}`);
    if (isSymlink(backupPath)) {
      throw new Error(`Refusing Codex config backup through symlink path: ${backupPath}`);
    }
    if (existsSync(backupPath)) {
      throw new Error(`Refusing to overwrite existing Codex config backup: ${backupPath}`);
    }
  }
}

export function runCodexAdapterPlan(options: CodexAdapterPlanOptions): CodexAdapterPlanResult {
  if (!options.paiHome || !options.paiHome.trim()) {
    throw new Error("Codex adapter plan requires an explicit paiHome");
  }

  const paiHome = assertPaiHomeAllowed(options);
  const { adapterHome, agentsPath } = assertAgentsPathAllowed(options);
  const agentsContent = renderCodexAgents(options);
  let adapterHomeCreatedForPreflight = false;
  try {
    if (!options.dryRun && options.configFragment !== undefined) {
      adapterHomeCreatedForPreflight = ensureAdapterHomeDirectoryForWrite(options, adapterHome, agentsPath);
    }
    preflightConfigOperation(options);
  } catch (error) {
    if (adapterHomeCreatedForPreflight) {
      try {
        rmdirSync(adapterHome);
      } catch {
        // Best-effort cleanup only.
      }
    }
    throw error;
  }
  const operations: CodexAdapterPlanOperation[] = [
    {
      kind: "render-agents",
      path: agentsPath,
      changed: true,
    },
  ];

  operations.push(writeAgentsFile(options, agentsPath, adapterHome, agentsContent));
  operations.push(configOperation(options));

  return {
    paiHome,
    adapterHome,
    agentsPath,
    configPath: options.configPath || join(adapterHome, "config.toml"),
    operations,
    agentsContent,
  };
}
