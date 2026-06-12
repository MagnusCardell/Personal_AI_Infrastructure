#!/usr/bin/env bun

import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, renameSync, rmSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, relative, resolve } from "node:path";

const BEGIN = "<!-- PAI-CODEX:BEGIN managed by Personal_AI_Infrastructure -->";
const END = "<!-- PAI-CODEX:END managed by Personal_AI_Infrastructure -->";

type Options = {
  dryRun: boolean;
  output: string;
  paiDir: string;
  help: boolean;
};

type PaiContext = {
  principalSummary: string;
  assistantSummary: string;
  algorithmPointer: string;
  algorithmSummary: string;
  missing: string[];
};

function usage(): string {
  return `usage: bun GenerateAgentsMd.ts [--dry-run] [--output PATH] [--pai-dir PATH]

  --dry-run       print a diff-like summary and write nothing
  --output PATH   target AGENTS.md path (default: \${HOME}/.codex/AGENTS.md)
  --pai-dir PATH  PAI root (default: \${PAI_DIR} or \${HOME}/.claude/PAI)
`;
}

function parseArgs(argv: string[]): Options {
  const home = process.env.HOME || homedir();
  const options: Options = {
    dryRun: false,
    output: join(home, ".codex", "AGENTS.md"),
    paiDir: process.env.PAI_DIR || join(home, ".claude", "PAI"),
    help: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--dry-run") {
      options.dryRun = true;
    } else if (arg === "--output") {
      index += 1;
      if (!argv[index]) throw new Error("--output requires a path");
      options.output = argv[index];
    } else if (arg === "--pai-dir") {
      index += 1;
      if (!argv[index]) throw new Error("--pai-dir requires a path");
      options.paiDir = argv[index];
    } else if (arg === "-h" || arg === "--help") {
      options.help = true;
    } else {
      throw new Error(`unknown option: ${arg}`);
    }
  }

  return {
    ...options,
    output: resolve(options.output),
    paiDir: resolve(options.paiDir),
  };
}

function scriptPath(): string {
  return new URL(import.meta.url).pathname;
}

function packageRoot(): string {
  return dirname(dirname(scriptPath()));
}

function readText(path: string): string | null {
  if (!existsSync(path)) return null;
  return readFileSync(path, "utf8");
}

function sha256(text: string): string {
  return createHash("sha256").update(text).digest("hex");
}

function redactSecrets(text: string): string {
  const providerToken = new RegExp("\\b" + "sk" + "-(?:ant-)?[A-Za-z0-9_-]{20,}\\b", "g");
  return text
    .replace(/-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z0-9 ]*PRIVATE KEY-----/gi, "[REDACTED]")
    .replace(/\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b/g, "[REDACTED]")
    .replace(providerToken, "[REDACTED]")
    .replace(/\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/gi, "[REDACTED]")
    .replace(/\bhttps?:\/\/\S+/gi, "[REDACTED]")
    .replace(/\b(password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key|client[_-]?secret)\s*[:=]\s*[^\s"',;`]{6,}/gi, "$1=[REDACTED]");
}

function safeSummary(markdown: string | null, fallback: string): string {
  if (!markdown || !markdown.trim()) return fallback;
  const result: string[] = [];
  const blocked = /\b(email|github|linkedin|voice|color|url|token|secret|password|api[_-]?key|access[_-]?key)\b/i;
  for (const rawLine of markdown.split(/\r?\n/)) {
    const line = redactSecrets(rawLine.trim());
    if (!line) continue;
    if (line.startsWith(">")) continue;
    if (blocked.test(line)) continue;
    if (line.startsWith("#")) {
      result.push(line.replace(/^#+\s*/, ""));
    } else if (/^[-*]\s+/.test(line)) {
      result.push(line);
    } else if (result.length < 3) {
      result.push(line);
    }
    if (result.length >= 6) break;
  }
  return result.length ? result.join("\n") : fallback;
}

function algorithmCandidates(pointer: string, algorithmDir: string): string[] {
  const raw = pointer.trim();
  if (!raw) return [];
  if (raw.startsWith("/")) return [raw];
  const candidates = [join(algorithmDir, raw)];
  if (!raw.endsWith(".md")) {
    candidates.push(join(algorithmDir, `v${raw}.md`));
    candidates.push(join(algorithmDir, `${raw}.md`));
  }
  return candidates;
}

function isInside(path: string, parent: string): boolean {
  const rel = relative(resolve(parent), resolve(path));
  return rel === "" || (!rel.startsWith("..") && !rel.startsWith("/"));
}

function resolveAlgorithm(paiDir: string): { pointer: string; summary: string; missing: string[] } {
  const algorithmDir = join(paiDir, "ALGORITHM");
  const latestPath = join(algorithmDir, "LATEST");
  const latest = readText(latestPath);
  if (!latest) return { pointer: "[missing]", summary: "[missing]", missing: ["PAI/ALGORITHM/LATEST"] };
  const pointer = latest.split(/\r?\n/)[0]?.trim() || "[missing]";
  for (const candidate of algorithmCandidates(pointer, algorithmDir)) {
    const resolved = resolve(candidate);
    if (!isInside(resolved, algorithmDir)) continue;
    const text = readText(resolved);
    if (text) return { pointer, summary: safeSummary(text, "[empty Algorithm file]"), missing: [] };
  }
  return { pointer, summary: "[unresolved]", missing: [`PAI/ALGORITHM/${pointer}`] };
}

function loadContext(paiDir: string): PaiContext {
  const principal = readText(join(paiDir, "USER", "PRINCIPAL_IDENTITY.md"));
  const assistant = readText(join(paiDir, "USER", "DA_IDENTITY.md"));
  const algorithm = resolveAlgorithm(paiDir);
  const missing = [...algorithm.missing];
  if (!principal) missing.push("PAI/USER/PRINCIPAL_IDENTITY.md");
  if (!assistant) missing.push("PAI/USER/DA_IDENTITY.md");
  return {
    principalSummary: safeSummary(principal, "[missing principal identity]"),
    assistantSummary: safeSummary(assistant, "[missing assistant identity]"),
    algorithmPointer: algorithm.pointer,
    algorithmSummary: algorithm.summary,
    missing,
  };
}

function stripTitle(template: string): string {
  return template.replace(/^# PAI Codex Runtime Instructions\s*\n+/u, "").trim();
}

function managedBody(context: PaiContext, template: string): string {
  const lines = [
    "# PAI Codex Runtime Instructions",
    "",
    "## Managed Runtime Summary",
    "",
    "Principal Summary:",
    context.principalSummary,
    "",
    "Runtime Assistant Summary:",
    context.assistantSummary,
    "",
    `Algorithm Pointer: ${redactSecrets(context.algorithmPointer)}`,
    "",
    "Algorithm Summary:",
    context.algorithmSummary,
  ];
  if (context.missing.length) {
    lines.push("", "Missing Source Files:", ...context.missing.map((item) => `- ${item}`));
  }
  lines.push("", stripTitle(template));
  return lines.join("\n").trim() + "\n";
}

function managedBlock(body: string): string {
  return `${BEGIN}\n${body}${END}\n`;
}

function replaceManagedBlock(existing: string, block: string): { next: string; action: string } {
  const pattern = new RegExp(`${escapeRegExp(BEGIN)}[\\s\\S]*?${escapeRegExp(END)}\\n?`, "m");
  if (!existing) return { next: block, action: "create managed block" };
  if (pattern.test(existing)) return { next: existing.replace(pattern, block), action: "replace managed block" };
  const separator = existing.endsWith("\n\n") ? "" : existing.endsWith("\n") ? "\n" : "\n\n";
  return { next: `${existing}${separator}${block}`, action: "append managed block" };
}

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function atomicWrite(path: string, content: string): void {
  const dir = dirname(path);
  mkdirSync(dir, { recursive: true });
  const tempDir = mkdtempSync(join(dir, ".pai-codex-agents."));
  const tempPath = join(tempDir, "AGENTS.md");
  try {
    writeFileSync(tempPath, content, { encoding: "utf8", mode: 0o644 });
    renameSync(tempPath, path);
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
}

function main(): number {
  let options: Options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    console.error(usage());
    return 2;
  }

  if (options.help) {
    process.stdout.write(usage());
    return 0;
  }

  const templatePath = join(packageRoot(), "AGENTS.md.template");
  const template = readText(templatePath);
  if (!template) {
    console.error(`missing template: ${templatePath}`);
    return 1;
  }

  const context = loadContext(options.paiDir);
  const block = managedBlock(managedBody(context, template));
  const existing = readText(options.output) || "";
  const { next, action } = replaceManagedBlock(existing, block);
  const changed = existing !== next;

  if (options.dryRun) {
    process.stdout.write([
      "AGENTS.md dry-run",
      `output: ${options.output}`,
      `template: ${templatePath}`,
      `action: ${changed ? action : "unchanged"}`,
      `old_sha256: ${existing ? sha256(existing) : "[missing]"}`,
      `new_sha256: ${sha256(next)}`,
      `missing_sources: ${context.missing.length ? context.missing.join(", ") : "none"}`,
      "",
    ].join("\n"));
    return 0;
  }

  if (!changed) {
    process.stdout.write(`AGENTS.md: unchanged ${options.output}\n`);
    return 0;
  }
  atomicWrite(options.output, next.trimEnd() + "\n");
  process.stdout.write(`AGENTS.md: ${action} at ${options.output}\n`);
  return 0;
}

process.exitCode = main();
