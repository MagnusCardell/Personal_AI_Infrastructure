#!/usr/bin/env bun
/**
 * PAI platform inventory
 *
 * Scans the repository for Claude-specific coupling that must be classified
 * before Codex adapter work changes runtime behavior.
 *
 * Usage:
 *   bun Tools/platform-inventory.ts
 *   bun Tools/platform-inventory.ts --format markdown --top 10
 *   bun Tools/platform-inventory.ts --format json
 *   bun Tools/platform-inventory.ts --root Tools/fixtures/platform-inventory
 */

import { existsSync, realpathSync, readdirSync, readFileSync, statSync } from "fs";
import { basename, extname, isAbsolute, join, relative, resolve } from "path";

type Classification =
  | "claude-only"
  | "platform-neutralizable"
  | "codex-equivalent"
  | "breaking-for-codex"
  | "docs-only"
  | "unknown-needs-fixture";

interface InventoryPattern {
  id: string;
  label: string;
  regex: RegExp;
  baseRisk: number;
  description: string;
}

interface Occurrence {
  file: string;
  line: number;
  match: string;
  excerpt: string;
  patternId: string;
  patternLabel: string;
  classification: Classification;
  risk: number;
  rationale: string;
}

interface GroupedCoupling {
  key: string;
  file: string;
  patternId: string;
  patternLabel: string;
  classification: Classification;
  count: number;
  risk: number;
  rationale: string;
  firstLine: number;
  excerpt: string;
}

interface InventoryResult {
  root: string;
  generatedAt: string;
  filesScanned: number;
  occurrences: Occurrence[];
  groupedCouplings: GroupedCoupling[];
  counts: {
    byClassification: Record<Classification, number>;
    byPattern: Record<string, number>;
  };
}

const PAI_ROOT = realpathSync(resolve(import.meta.dir, ".."));

const CLASSIFICATIONS: Classification[] = [
  "claude-only",
  "platform-neutralizable",
  "codex-equivalent",
  "breaking-for-codex",
  "docs-only",
  "unknown-needs-fixture",
];

const INVENTORY_PATTERNS: InventoryPattern[] = [
  {
    id: "claude-home-path",
    label: "~/.claude / .claude path",
    regex: /~\/\.claude|\$HOME\/\.claude|\$\{HOME\}\/\.claude|\.claude/g,
    baseRisk: 5,
    description: "Claude home and release artifact paths.",
  },
  {
    id: "claude-dir-env",
    label: "CLAUDE_DIR",
    regex: /\bCLAUDE_DIR\b/g,
    baseRisk: 4,
    description: "Claude-specific environment variable used as an install root.",
  },
  {
    id: "pai-dir-env",
    label: "PAI_DIR",
    regex: /\bPAI_DIR\b/g,
    baseRisk: 4,
    description: "Legacy PAI application-home variable that currently often points at Claude home.",
  },
  {
    id: "claude-md",
    label: "CLAUDE.md",
    regex: /\bCLAUDE\.md\b/g,
    baseRisk: 5,
    description: "Claude-native instruction file generation and references.",
  },
  {
    id: "build-claude",
    label: "BuildCLAUDE",
    regex: /\bBuildCLAUDE\b/g,
    baseRisk: 5,
    description: "Instruction build path currently named and shaped around Claude.",
  },
  {
    id: "claude-cli-detection",
    label: "claude CLI detection",
    regex: /\bclaude\s+--version\b/g,
    baseRisk: 4,
    description: "Claude CLI detection.",
  },
  {
    id: "claude-cli-prompt-exec",
    label: "claude -p prompt execution",
    regex: /\bclaude\s+-p\b/g,
    baseRisk: 5,
    description: "Claude CLI non-interactive prompt execution.",
  },
  {
    id: "anthropic-package",
    label: "@anthropic-ai/claude-code",
    regex: /@anthropic-ai\/claude-code/g,
    baseRisk: 3,
    description: "Claude Code npm package reference.",
  },
  {
    id: "claude-code-name",
    label: "Claude Code",
    regex: /Claude Code/g,
    baseRisk: 2,
    description: "Product-specific documentation or runtime wording.",
  },
  {
    id: "claude-hook-event",
    label: "Claude settings hook event",
    regex: /\b(?:PreToolUse|PostToolUse|UserPromptSubmit|SessionStart|SessionEnd|Stop|SubagentStop|PreCompact|Notification)\b/g,
    baseRisk: 5,
    description: "Claude settings hook lifecycle event names.",
  },
  {
    id: "claude-hook-decision",
    label: "Claude hook decision output",
    regex: /decision\s*[:=]\s*["'](?:ask|block)["']|continue\s*:\s*true|exit\s*\(\s*2\s*\)/g,
    baseRisk: 5,
    description: "Claude hook stdout or exit-code decision contract.",
  },
  {
    id: "claude-transcript",
    label: "Claude transcript assumption",
    regex: /transcript_path|\.jsonl|message\??\.content|tool_use|tool_result|entry\.type\s*===\s*["'](?:assistant|user|human)["']|type:\s*["'](?:assistant|user|human)["']/g,
    baseRisk: 5,
    description: "Claude Code transcript shape, transcript path, or JSONL session parsing.",
  },
  {
    id: "claude-tool-name",
    label: "Claude tool name",
    regex: /(["'`])(?:Read|Write|Edit|MultiEdit|Task|Skill|AskUserQuestion|Stop)\1|\b(?:AskUserQuestion|MultiEdit|Task tool|Skill tool|Task Tool)\b/g,
    baseRisk: 4,
    description: "Claude tool names used in permissions, hook matchers, or agent workflows.",
  },
  {
    id: "claude-statusline",
    label: "Claude statusline assumption",
    regex: /statusLine|statusline-command|statusline/gi,
    baseRisk: 4,
    description: "Claude status line configuration or command assumptions.",
  },
  {
    id: "claude-skills-agents-path",
    label: "Claude skills/agents path",
    regex: /\.claude\/(?:skills|Agents|commands|projects)|CLAUDE_PROJECT_DIR|CLAUDE_AGENT_TYPE|subagent_type|skills\/[A-Za-z0-9_-]+\/SKILL\.md/g,
    baseRisk: 4,
    description: "Claude skills, commands, project transcripts, or agent runtime paths.",
  },
];

const BINARY_EXTENSIONS = new Set([
  ".png",
  ".jpg",
  ".jpeg",
  ".gif",
  ".webp",
  ".ico",
  ".pdf",
  ".woff",
  ".woff2",
  ".ttf",
  ".otf",
  ".lockb",
]);

const DEFAULT_IGNORED_DIRS = new Set([
  ".git",
  "node_modules",
  ".next",
  "dist",
  "build",
  "coverage",
]);

function parseArgs(argv: string[]): {
  root: string;
  format: "text" | "markdown" | "json";
  top: number;
  includePlanning: boolean;
  help: boolean;
} {
  let root = PAI_ROOT;
  let format: "text" | "markdown" | "json" = "text";
  let top = 10;
  let includePlanning = false;
  let help = false;

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--root") {
      root = resolve(argv[++i] || root);
    } else if (arg === "--format") {
      const value = argv[++i];
      if (value !== "text" && value !== "markdown" && value !== "json") {
        throw new Error(`Unsupported format: ${value}`);
      }
      format = value;
    } else if (arg === "--top") {
      const value = Number(argv[++i]);
      if (!Number.isFinite(value) || value < 1) {
        throw new Error("--top must be a positive number");
      }
      top = Math.floor(value);
    } else if (arg === "--include-planning") {
      includePlanning = true;
    } else if (arg === "--help" || arg === "-h") {
      help = true;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  return { root, format, top, includePlanning, help };
}

function assertSafeRoot(root: string, includePlanning: boolean): void {
  const realRoot = realpathSync(root);
  const relativeToRepo = relative(PAI_ROOT, realRoot);
  const insideRepo = relativeToRepo === "" || (!relativeToRepo.startsWith("..") && !isAbsolute(relativeToRepo));

  if (!insideRepo) {
    throw new Error(`Refusing to scan outside repository root: ${realRoot}`);
  }

  const rel = relativeToRepo.replace(/\\/g, "/");
  const fixtureRoot = "Tools/fixtures/platform-inventory";
  const isExplicitFixtureRoot = rel === fixtureRoot;
  const isPrivateStateRoot = rel === ".git" || rel.startsWith(".git/");

  if (isPrivateStateRoot) {
    throw new Error(`Refusing to scan private repository state: ${realRoot}`);
  }

  const isPlanningRoot =
    rel === "AGENTS.md" ||
    rel === ".codex" ||
    rel.startsWith(".codex/") ||
    rel === "docs/adapters" ||
    rel.startsWith("docs/adapters/") ||
    rel === "Tools/platform-inventory.ts" ||
    rel === "Tools/platform-inventory.test.ts" ||
    (rel.startsWith(`${fixtureRoot}/`) && !isExplicitFixtureRoot);

  if (!includePlanning && isPlanningRoot) {
    throw new Error(`Refusing to scan planning/protected path without --include-planning: ${realRoot}`);
  }
}

function printHelp(): void {
  console.log(`PAI platform inventory

Usage:
  bun Tools/platform-inventory.ts [options]

Options:
  --root <path>            Repository or fixture root to scan.
  --format text|markdown|json
                           Output format. Default: text.
  --top <n>                Number of high-risk grouped couplings to show. Default: 10.
  --include-planning       Include .codex governance and docs/adapters planning files.
  -h, --help               Show this help.
`);
}

function shouldIgnorePath(root: string, fullPath: string, includePlanning: boolean): boolean {
  const rel = relative(root, fullPath).replace(/\\/g, "/");
  const parts = rel.split("/");
  const name = basename(fullPath);

  if (!includePlanning) {
    if (rel === "AGENTS.md") return true;
    if (rel.startsWith("docs/adapters/")) return true;
    if (rel === "Tools/platform-inventory.ts") return true;
    if (rel === "Tools/platform-inventory.test.ts") return true;
    if (rel.startsWith("Tools/fixtures/platform-inventory/")) return true;
  }

  if (DEFAULT_IGNORED_DIRS.has(name)) return true;
  if (!includePlanning && parts.includes(".codex")) return true;

  return false;
}

function listFiles(root: string, includePlanning: boolean): string[] {
  const files: string[] = [];

  function walk(dir: string): void {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const fullPath = join(dir, entry.name);
      if (shouldIgnorePath(root, fullPath, includePlanning)) continue;

      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (entry.isFile()) {
        if (!BINARY_EXTENSIONS.has(extname(entry.name).toLowerCase())) {
          files.push(fullPath);
        }
      }
    }
  }

  walk(root);
  return files.sort();
}

function isDocsPath(file: string): boolean {
  return file.endsWith(".md") || file.endsWith(".txt");
}

function isPackInstall(file: string): boolean {
  return /^Packs\/[^/]+\/INSTALL\.md$/.test(file);
}

function isReleaseArtifact(file: string): boolean {
  return /^Releases\/[^/]+\/\.claude\//.test(file);
}

function isReleaseSettings(file: string): boolean {
  return /^Releases\/[^/]+\/\.claude\/settings\.json$/.test(file);
}

function isReleaseHook(file: string): boolean {
  return /^Releases\/[^/]+\/\.claude\/hooks\//.test(file);
}

function isReleaseTranscriptOrSessionTool(file: string): boolean {
  return /^Releases\/[^/]+\/\.claude\/PAI\/Tools\/.*(?:Transcript|Session).*\.ts$/.test(file);
}

function isInstallerEngine(file: string): boolean {
  return /^Releases\/[^/]+\/\.claude\/PAI-Install\/engine\//.test(file);
}

function pathRisk(file: string): number {
  if (isReleaseSettings(file)) return 3;
  if (isReleaseHook(file)) return 3;
  if (isReleaseTranscriptOrSessionTool(file)) return 3;
  if (isInstallerEngine(file)) return 2;
  if (isPackInstall(file)) return 1;
  if (file.startsWith("Tools/")) return 1;
  return 0;
}

function classificationRisk(classification: Classification): number {
  switch (classification) {
    case "breaking-for-codex":
      return 3;
    case "unknown-needs-fixture":
      return 2;
    case "platform-neutralizable":
      return 1;
    case "claude-only":
      return 1;
    case "codex-equivalent":
      return 0;
    case "docs-only":
      return -1;
  }
}

function classify(pattern: InventoryPattern, file: string): { classification: Classification; rationale: string } {
  const docs = isDocsPath(file);
  const packInstall = isPackInstall(file);
  const release = isReleaseArtifact(file);
  const releaseSettings = isReleaseSettings(file);
  const releaseHook = isReleaseHook(file);
  const releaseTranscript = isReleaseTranscriptOrSessionTool(file);
  const installerEngine = isInstallerEngine(file);

  if (docs && !packInstall) {
    return {
      classification: "docs-only",
      rationale: "Documentation reference; update only when adapter docs or user-facing docs are in scope.",
    };
  }

  switch (pattern.id) {
    case "claude-home-path":
      if (releaseTranscript) {
        return {
          classification: "breaking-for-codex",
          rationale: "Session and transcript tooling assumes Claude's ~/.claude/projects and PAI home layout.",
        };
      }
      if (installerEngine || packInstall) {
        return {
          classification: "platform-neutralizable",
          rationale: "Installer or pack path can be routed through future platform path selection.",
        };
      }
      if (release) {
        return {
          classification: "claude-only",
          rationale: "Current release artifact is intentionally Claude-shaped and should remain unchanged in PR-01.",
        };
      }
      return {
        classification: "platform-neutralizable",
        rationale: "Hardcoded Claude home needs a platform path abstraction before Codex support.",
      };

    case "claude-dir-env":
      return {
        classification: "platform-neutralizable",
        rationale: "Claude-specific env var should be isolated under a Claude adapter or replaced by platform paths.",
      };

    case "pai-dir-env":
      return {
        classification: "platform-neutralizable",
        rationale: "PAI_DIR is a legacy compatibility alias and must be preserved while adding PAI_HOME semantics.",
      };

    case "claude-md":
    case "build-claude":
      if (releaseHook || releaseSettings) {
        return {
          classification: "breaking-for-codex",
          rationale: "Instruction generation and SessionStart loading are Claude-specific and need a Codex AGENTS.md/config path.",
        };
      }
      return {
        classification: "platform-neutralizable",
        rationale: "Instruction generation can become platform-specific while preserving Claude output.",
      };

    case "claude-cli-detection":
      return {
        classification: "codex-equivalent",
        rationale: "Codex support needs analogous CLI detection without changing Claude detection.",
      };

    case "claude-cli-prompt-exec":
      return {
        classification: "breaking-for-codex",
        rationale: "Claude prompt execution is not CLI detection and needs an explicit Codex execution contract before mapping.",
      };

    case "anthropic-package":
      return {
        classification: "claude-only",
        rationale: "Claude Code package checks are Claude-adapter concerns.",
      };

    case "claude-code-name":
      return {
        classification: docs ? "docs-only" : "claude-only",
        rationale: docs
          ? "Narrative documentation reference."
          : "Runtime wording or comments are tied to Claude Code behavior.",
      };

    case "claude-hook-event":
      if (releaseSettings || releaseHook || releaseTranscript) {
        return {
          classification: "breaking-for-codex",
          rationale: "Claude lifecycle event names and matcher semantics require adapter mapping and fixtures.",
        };
      }
      return {
        classification: packInstall ? "platform-neutralizable" : "docs-only",
        rationale: packInstall
          ? "Pack installer instructions can be split by platform in a later pack conversion phase."
          : "Hook lifecycle mention in documentation.",
      };

    case "claude-hook-decision":
      if (releaseHook) {
        return {
          classification: "breaking-for-codex",
          rationale: "Hook stdout decisions and exit-code blocking are platform-specific contracts.",
        };
      }
      return {
        classification: "docs-only",
        rationale: "Decision output mention outside runtime hook code.",
      };

    case "claude-transcript":
      if (releaseHook || releaseTranscript) {
        return {
          classification: "unknown-needs-fixture",
          rationale: "Codex transcript/session shape must be fixture-tested before compatibility can be claimed.",
        };
      }
      return {
        classification: docs ? "docs-only" : "platform-neutralizable",
        rationale: docs
          ? "Transcript mention in documentation."
          : "Transcript-dependent logic needs a platform parser interface.",
      };

    case "claude-tool-name":
      if (releaseSettings || releaseHook) {
        return {
          classification: "breaking-for-codex",
          rationale: "Claude tool names in permissions and hook matchers do not map directly to Codex surfaces.",
        };
      }
      if (packInstall) {
        return {
          classification: "platform-neutralizable",
          rationale: "Pack installer instructions can use platform-specific interaction surfaces later.",
        };
      }
      return {
        classification: docs ? "docs-only" : "platform-neutralizable",
        rationale: docs ? "Tool-name documentation reference." : "Tool-name dependency needs adapter mapping.",
      };

    case "claude-statusline":
      if (releaseSettings || releaseHook) {
        return {
          classification: "breaking-for-codex",
          rationale: "Claude status line and terminal UI behavior do not have proven Codex parity.",
        };
      }
      return {
        classification: docs ? "docs-only" : "claude-only",
        rationale: docs ? "Statusline documentation reference." : "Statusline behavior is Claude-specific until mapped.",
      };

    case "claude-skills-agents-path":
      if (releaseHook) {
        return {
          classification: "breaking-for-codex",
          rationale: "Claude subagent and project environment assumptions need Codex custom-agent mapping.",
        };
      }
      if (packInstall) {
        return {
          classification: "platform-neutralizable",
          rationale: "Pack install destinations can be routed to Codex skill or command locations later.",
        };
      }
      return {
        classification: release ? "claude-only" : "platform-neutralizable",
        rationale: release
          ? "Current release artifact is a Claude package."
          : "Skills and agent paths need platform-specific install destinations.",
      };

    default:
      return {
        classification: "unknown-needs-fixture",
        rationale: "No classifier rule matched; requires manual review.",
      };
  }
}

function scanFile(root: string, filePath: string): Occurrence[] {
  const rel = relative(root, filePath).replace(/\\/g, "/");
  const stat = statSync(filePath);
  if (stat.size > 2_000_000) return [];

  let content: string;
  try {
    content = readFileSync(filePath, "utf-8");
  } catch {
    return [];
  }

  if (content.includes("\u0000")) return [];

  const occurrences: Occurrence[] = [];
  const lines = content.split(/\r?\n/);

  lines.forEach((lineText, index) => {
    for (const pattern of INVENTORY_PATTERNS) {
      pattern.regex.lastIndex = 0;
      let match: RegExpExecArray | null;
      while ((match = pattern.regex.exec(lineText)) !== null) {
        const { classification, rationale } = classify(pattern, rel);
        const risk = Math.max(1, pattern.baseRisk + pathRisk(rel) + classificationRisk(classification));
        occurrences.push({
          file: rel,
          line: index + 1,
          match: match[0],
          excerpt: lineText.trim().slice(0, 180),
          patternId: pattern.id,
          patternLabel: pattern.label,
          classification,
          risk,
          rationale,
        });

        if (match[0].length === 0) pattern.regex.lastIndex += 1;
      }
    }
  });

  return occurrences;
}

function groupOccurrences(occurrences: Occurrence[]): GroupedCoupling[] {
  const groups = new Map<string, GroupedCoupling>();

  for (const occurrence of occurrences) {
    const key = `${occurrence.file}\0${occurrence.patternId}\0${occurrence.classification}`;
    const existing = groups.get(key);
    if (existing) {
      existing.count += 1;
      existing.risk = Math.max(existing.risk, occurrence.risk);
      continue;
    }

    groups.set(key, {
      key,
      file: occurrence.file,
      patternId: occurrence.patternId,
      patternLabel: occurrence.patternLabel,
      classification: occurrence.classification,
      count: 1,
      risk: occurrence.risk,
      rationale: occurrence.rationale,
      firstLine: occurrence.line,
      excerpt: occurrence.excerpt,
    });
  }

  return [...groups.values()].sort((a, b) => {
    if (b.risk !== a.risk) return b.risk - a.risk;
    if (b.count !== a.count) return b.count - a.count;
    return a.file.localeCompare(b.file);
  });
}

function buildResult(root: string, includePlanning: boolean): InventoryResult {
  if (!existsSync(root)) {
    throw new Error(`Root does not exist: ${root}`);
  }
  assertSafeRoot(root, includePlanning);
  if (!statSync(root).isDirectory()) {
    throw new Error(`Root must be a directory: ${root}`);
  }

  const files = listFiles(root, includePlanning);
  const occurrences = files.flatMap((file) => scanFile(root, file));
  const byClassification = Object.fromEntries(CLASSIFICATIONS.map((label) => [label, 0])) as Record<Classification, number>;
  const byPattern: Record<string, number> = {};

  for (const occurrence of occurrences) {
    byClassification[occurrence.classification] += 1;
    byPattern[occurrence.patternLabel] = (byPattern[occurrence.patternLabel] || 0) + 1;
  }

  return {
    root,
    generatedAt: new Date().toISOString(),
    filesScanned: files.length,
    occurrences,
    groupedCouplings: groupOccurrences(occurrences),
    counts: {
      byClassification,
      byPattern: Object.fromEntries(Object.entries(byPattern).sort((a, b) => b[1] - a[1])),
    },
  };
}

function renderText(result: InventoryResult, top: number): string {
  const lines: string[] = [];
  lines.push("PAI Platform Inventory");
  lines.push(`Root: ${result.root}`);
  lines.push(`Files scanned: ${result.filesScanned}`);
  lines.push(`Occurrences: ${result.occurrences.length}`);
  lines.push("");
  lines.push("By classification:");
  for (const label of CLASSIFICATIONS) {
    lines.push(`  ${label}: ${result.counts.byClassification[label]}`);
  }
  lines.push("");
  lines.push(`Top ${top} highest-risk grouped couplings:`);
  for (const group of result.groupedCouplings.slice(0, top)) {
    lines.push(
      `  [risk ${group.risk}] ${group.file}:${group.firstLine} ${group.patternLabel} ` +
        `(${group.classification}, ${group.count} occurrence${group.count === 1 ? "" : "s"})`
    );
    lines.push(`    ${group.rationale}`);
  }
  return lines.join("\n");
}

function escapeMarkdown(value: string): string {
  return value.replace(/\|/g, "\\|").replace(/\n/g, " ");
}

function renderMarkdown(result: InventoryResult, top: number): string {
  const lines: string[] = [];
  lines.push("# PAI Platform Inventory");
  lines.push("");
  lines.push(`- Root: \`${result.root}\``);
  lines.push(`- Generated: \`${result.generatedAt}\``);
  lines.push(`- Files scanned: \`${result.filesScanned}\``);
  lines.push(`- Occurrences: \`${result.occurrences.length}\``);
  lines.push("");
  lines.push("## Counts By Classification");
  lines.push("");
  lines.push("| Classification | Occurrences |");
  lines.push("|---|---:|");
  for (const label of CLASSIFICATIONS) {
    lines.push(`| \`${label}\` | ${result.counts.byClassification[label]} |`);
  }
  lines.push("");
  lines.push("## Counts By Pattern");
  lines.push("");
  lines.push("| Pattern | Occurrences |");
  lines.push("|---|---:|");
  for (const [label, count] of Object.entries(result.counts.byPattern)) {
    lines.push(`| ${escapeMarkdown(label)} | ${count} |`);
  }
  lines.push("");
  lines.push(`## Top ${top} Highest-Risk Grouped Couplings`);
  lines.push("");
  lines.push("| Risk | File | Pattern | Class | Count | Rationale |");
  lines.push("|---:|---|---|---|---:|---|");
  for (const group of result.groupedCouplings.slice(0, top)) {
    lines.push(
      `| ${group.risk} | \`${escapeMarkdown(group.file)}:${group.firstLine}\` | ` +
        `${escapeMarkdown(group.patternLabel)} | \`${group.classification}\` | ${group.count} | ` +
        `${escapeMarkdown(group.rationale)} |`
    );
  }
  return lines.join("\n");
}

function main(): void {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) {
      printHelp();
      return;
    }

    const result = buildResult(options.root, options.includePlanning);

    if (options.format === "json") {
      console.log(JSON.stringify(result, null, 2));
    } else if (options.format === "markdown") {
      console.log(renderMarkdown(result, options.top));
    } else {
      console.log(renderText(result, options.top));
    }
  } catch (error) {
    console.error(`platform-inventory error: ${error instanceof Error ? error.message : String(error)}`);
    process.exit(1);
  }
}

main();
