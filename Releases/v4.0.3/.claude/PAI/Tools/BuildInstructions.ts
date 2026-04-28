#!/usr/bin/env bun

/**
 * BuildInstructions.ts - target-aware PAI instruction generation.
 *
 * Claude remains the default/stable target. Codex generation is an unwired
 * substrate for later installer phases and only writes when an explicit output
 * path is provided.
 */

import { existsSync, lstatSync, readFileSync, realpathSync, writeFileSync } from "fs";
import { homedir } from "os";
import { basename, dirname, isAbsolute, join, relative, resolve } from "path";
import { resolvePlatformPaths } from "./platform/paths";

export type InstructionTarget = "claude" | "codex";

export interface BuildInstructionOptions {
  target: InstructionTarget;
  paiHome?: string;
  adapterHome?: string;
  templatePath?: string;
  outputPath?: string;
  settingsPath?: string;
  algorithmDir?: string;
  algorithmLatestPath?: string;
  dryRun?: boolean;
}

export interface BuildInstructionResult {
  target: InstructionTarget;
  rebuilt: boolean;
  outputPath: string;
  content?: string;
  reason?: string;
}

export interface InstructionVariableContext {
  target: InstructionTarget;
  paiHome: string;
  adapterHome: string;
  templatePath: string;
  outputPath: string;
  settingsPath: string;
  algorithmDir: string;
  algorithmLatestPath: string;
}

const DEFAULT_PAI_VERSION = "4.0.3";
const DEFAULT_ALGORITHM_VERSION = "v3.7.0";

function currentHome(): string {
  return process.env.HOME || homedir();
}

function legacyClaudePaiHome(): string {
  return join(currentHome(), ".claude");
}

function productCodexTemplatePath(): string {
  return join(import.meta.dir, "../Adapters/codex/AGENTS.md.template");
}

function productRootFromToolPath(): string {
  return resolve(import.meta.dir, "../../../../..");
}

function defaultCodexPaths(): { paiHome: string; adapterHome: string } {
  const paths = resolvePlatformPaths({
    platform: "codex",
    env: process.env,
  });

  return {
    paiHome: paths.paiHome,
    adapterHome: paths.adapterHome,
  };
}

function resolveOutputPath(target: InstructionTarget, paiHome: string, outputPath?: string, dryRun = false): string {
  if (outputPath) return outputPath;
  if (target === "claude") return join(paiHome, "CLAUDE.md");
  if (dryRun) return join(paiHome, "AGENTS.md");

  throw new Error("Codex instruction generation requires dryRun or an explicit outputPath in PR-04A");
}

function isWithinPath(parentPath: string, candidatePath: string): boolean {
  const parent = resolve(parentPath);
  const candidate = resolve(candidatePath);
  const rel = relative(parent, candidate);
  return rel === "" || (!!rel && !rel.startsWith("..") && !isAbsolute(rel));
}

function assertNotWithin(label: string, deniedRoot: string, candidatePath: string): void {
  if (isWithinPath(deniedRoot, candidatePath)) {
    throw new Error(`Refusing Codex instruction write inside ${label}: ${candidatePath}`);
  }
}

function isSymlink(path: string): boolean {
  try {
    return lstatSync(path).isSymbolicLink();
  } catch {
    return false;
  }
}

function assertExistingDirectory(label: string, path: string): void {
  if (!existsSync(path) || !lstatSync(path).isDirectory()) {
    throw new Error(`Codex instruction write ${label} must be an existing directory: ${path}`);
  }
}

function assertNoSymlinkComponents(rootPath: string, parentPath: string, originalOutputPath: string): void {
  const relativeParent = relative(rootPath, parentPath);
  if (!relativeParent) return;

  let current = rootPath;
  for (const segment of relativeParent.split(/[\\/]+/).filter(Boolean)) {
    current = join(current, segment);
    if (isSymlink(current)) {
      throw new Error(`Refusing Codex instruction write through symlink path component: ${originalOutputPath}`);
    }
  }
}

function assertNoReservedCodexOutputSubdirs(rootPath: string, outputPath: string): void {
  const reserved = new Set([".agents", ".codex", "agents", "hooks", "rules", "skills"]);
  const relativeOutput = relative(rootPath, outputPath);
  const segments = relativeOutput.split(/[\\/]+/).filter(Boolean).slice(0, -1);
  const reservedSegment = segments.find((segment) => reserved.has(segment.toLowerCase()));
  if (reservedSegment) {
    throw new Error(`Refusing Codex instruction write inside reserved ${reservedSegment} path: ${outputPath}`);
  }
}

function assertCodexOutputPathAllowed(options: BuildInstructionOptions, context: InstructionVariableContext): void {
  if (!options.outputPath) {
    throw new Error("Codex instruction generation requires an explicit outputPath when dryRun is false");
  }

  if (!options.paiHome) {
    throw new Error("Codex instruction writes require an explicit paiHome containment root in PR-04A");
  }

  const outputPath = resolve(context.outputPath);
  const paiHome = resolve(context.paiHome);
  const outputParent = dirname(outputPath);

  if (basename(outputPath) !== "AGENTS.md") {
    throw new Error(`Codex instruction writes are limited to AGENTS.md outputs in PR-04A: ${context.outputPath}`);
  }

  if (!isWithinPath(paiHome, outputPath)) {
    throw new Error(`Refusing Codex instruction write outside explicit paiHome: ${context.outputPath}`);
  }

  const home = resolve(currentHome());
  assertNotWithin("Codex CLI state/config home", join(home, ".codex"), outputPath);
  assertNotWithin("default PAI home", join(home, ".pai"), outputPath);
  assertNotWithin("Claude adapter home", join(home, ".claude"), outputPath);
  assertNotWithin("Codex adapter/config home", context.adapterHome, outputPath);

  const productRoot = productRootFromToolPath();
  assertNotWithin("repository governance directory", join(productRoot, ".codex"), outputPath);
  assertNotWithin("working directory governance directory", join(process.cwd(), ".codex"), outputPath);

  if (outputPath === resolve(productRoot, "AGENTS.md") || outputPath === resolve(process.cwd(), "AGENTS.md")) {
    throw new Error(`Refusing Codex instruction write to repository AGENTS.md: ${context.outputPath}`);
  }

  assertExistingDirectory("paiHome", paiHome);
  assertNoSymlinkComponents(paiHome, outputParent, context.outputPath);
  assertExistingDirectory("output parent", outputParent);
  const realPaiHome = realpathSync(paiHome);
  const realOutputParent = realpathSync(outputParent);
  if (!isWithinPath(realPaiHome, realOutputParent)) {
    throw new Error(`Refusing Codex instruction write outside real explicit paiHome: ${context.outputPath}`);
  }
  assertNoReservedCodexOutputSubdirs(paiHome, outputPath);

  if (isSymlink(outputPath)) {
    throw new Error(`Refusing Codex instruction write to symlink output path: ${context.outputPath}`);
  }
}

export function resolveInstructionContext(options: BuildInstructionOptions): InstructionVariableContext {
  if (options.target !== "claude" && options.target !== "codex") {
    throw new Error(`Unsupported instruction target: ${String(options.target)}`);
  }

  const codexDefaults = options.target === "codex" ? defaultCodexPaths() : undefined;
  const paiHome = options.paiHome ?? (options.target === "claude" ? legacyClaudePaiHome() : codexDefaults!.paiHome);
  const adapterHome = options.adapterHome ?? (options.target === "claude" ? paiHome : codexDefaults!.adapterHome);
  const algorithmDir = options.algorithmDir ?? join(paiHome, "PAI/Algorithm");
  const outputPath = resolveOutputPath(options.target, paiHome, options.outputPath, options.dryRun);

  return {
    target: options.target,
    paiHome,
    adapterHome,
    templatePath:
      options.templatePath ?? (options.target === "claude" ? join(paiHome, "CLAUDE.md.template") : productCodexTemplatePath()),
    outputPath,
    settingsPath: options.settingsPath ?? join(paiHome, "settings.json"),
    algorithmDir,
    algorithmLatestPath: options.algorithmLatestPath ?? join(algorithmDir, "LATEST"),
  };
}

function readJsonFile(path: string): Record<string, any> {
  return existsSync(path) ? JSON.parse(readFileSync(path, "utf-8")) : {};
}

export function getAlgorithmVersion(context: Pick<InstructionVariableContext, "algorithmLatestPath">): string {
  if (!existsSync(context.algorithmLatestPath)) {
    console.error("⚠ PAI/Algorithm/LATEST not found, defaulting to v3.7.0");
    return DEFAULT_ALGORITHM_VERSION;
  }

  return readFileSync(context.algorithmLatestPath, "utf-8").trim();
}

function instructionPath(context: InstructionVariableContext, algoVersion: string): string {
  if (context.target === "claude") {
    return `PAI/Algorithm/${algoVersion}.md`;
  }

  return join(context.algorithmDir, `${algoVersion}.md`);
}

export function loadInstructionVariables(options: BuildInstructionOptions): Record<string, string> {
  const context = resolveInstructionContext(options);
  const settings = readJsonFile(context.settingsPath);
  const algoVersion = getAlgorithmVersion(context);

  return {
    "{DAIDENTITY.NAME}": settings.daidentity?.name || "Assistant",
    "{DAIDENTITY.FULLNAME}": settings.daidentity?.fullName || "Assistant",
    "{DAIDENTITY.DISPLAYNAME}": settings.daidentity?.displayName || "Assistant",
    "{PRINCIPAL.NAME}": settings.principal?.name || "User",
    "{PRINCIPAL.TIMEZONE}": settings.principal?.timezone || "UTC",
    "{{PAI_VERSION}}": settings.pai?.version || DEFAULT_PAI_VERSION,
    "{{ALGO_VERSION}}": algoVersion,
    "{{ALGO_PATH}}": instructionPath(context, algoVersion),
    "{{PAI_HOME}}": context.paiHome,
    "{{ADAPTER_HOME}}": context.adapterHome,
    "{{CONTEXT_ROUTING_PATH}}": join(context.paiHome, "PAI/CONTEXT_ROUTING.md"),
  };
}

export function renderInstructionTemplate(template: string, options: BuildInstructionOptions): string {
  let content = template;
  const variables = loadInstructionVariables(options);

  for (const [key, value] of Object.entries(variables)) {
    content = content.replaceAll(key, value);
  }

  return content;
}

export function needsRebuild(options: BuildInstructionOptions): boolean {
  const context = resolveInstructionContext(options);
  if (!existsSync(context.outputPath)) return true;
  if (!existsSync(context.templatePath)) return false;

  const outputContent = readFileSync(context.outputPath, "utf-8");
  const variables = loadInstructionVariables(options);

  for (const key of Object.keys(variables)) {
    if (outputContent.includes(key)) return true;
  }

  if (context.target === "claude") {
    const algoVersion = getAlgorithmVersion(context);
    const algoPathPattern = /PAI\/Algorithm\/(.+?)\.md/;
    const match = outputContent.match(algoPathPattern);
    if (match && match[1] !== algoVersion) return true;

    const settings = readJsonFile(context.settingsPath);
    const daName = settings.daidentity?.name || "Assistant";
    if (!outputContent.includes(`🗣️ ${daName}:`)) return true;
  }

  return false;
}

export function buildInstructions(options: BuildInstructionOptions): BuildInstructionResult {
  const context = resolveInstructionContext(options);
  const templateName = options.target === "claude" ? "CLAUDE.md.template" : "AGENTS.md.template";

  if (!existsSync(context.templatePath)) {
    return {
      target: options.target,
      rebuilt: false,
      outputPath: context.outputPath,
      reason: `No ${templateName} found`,
    };
  }

  const content = renderInstructionTemplate(readFileSync(context.templatePath, "utf-8"), options);

  if (!options.dryRun && options.target === "codex") {
    assertCodexOutputPathAllowed(options, context);
  }

  if (existsSync(context.outputPath)) {
    const existing = readFileSync(context.outputPath, "utf-8");
    if (existing === content) {
      return {
        target: options.target,
        rebuilt: false,
        outputPath: context.outputPath,
        content: options.dryRun ? content : undefined,
        reason: `${options.target === "claude" ? "CLAUDE.md" : "AGENTS.md"} already current`,
      };
    }
  }

  if (!options.dryRun) {
    writeFileSync(context.outputPath, content);
  }

  return {
    target: options.target,
    rebuilt: true,
    outputPath: context.outputPath,
    content: options.dryRun ? content : undefined,
    reason: options.dryRun ? "dryRun" : undefined,
  };
}
