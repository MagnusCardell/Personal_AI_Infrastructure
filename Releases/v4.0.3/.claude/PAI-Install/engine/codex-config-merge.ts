/**
 * Codex config.toml merge primitive.
 *
 * PR-04B keeps this module unwired. It supports explicit, contained paths for
 * future installer use, but no installer runtime flow calls it yet.
 */

import {
  chmodSync,
  closeSync,
  constants,
  existsSync,
  lstatSync,
  openSync,
  readFileSync,
  realpathSync,
  renameSync,
  statSync,
  unlinkSync,
  writeFileSync,
} from "fs";
import { randomUUID } from "crypto";
import { homedir, tmpdir } from "os";
import { basename, dirname, isAbsolute, join, relative, resolve, sep } from "path";

export interface CodexConfigMergeOptions {
  configPath: string;
  fragment: string;
  sourceLabel?: string;
  dryRun?: boolean;
  backup?: boolean;
  now?: Date;
  allowedRoot?: string;
  allowNonDefaultBasenameForTests?: boolean;
  env?: Record<string, string | undefined>;
}

export interface CodexConfigMergeConflict {
  table: string;
  key: string;
  existingLine: number;
  reason: string;
}

export interface CodexConfigMergeResult {
  changed: boolean;
  configPath: string;
  content: string;
  backupPath?: string;
  conflicts: CodexConfigMergeConflict[];
  insertedTables: string[];
  insertedKeys: string[];
}

interface FragmentBlock {
  table: string;
  lines: string[];
  keys: string[];
}

interface ExistingAssignment {
  table: string;
  key: string;
  line: number;
}

interface ExistingTable {
  table: string;
  start: number;
  end: number;
}

interface ManagedBlock {
  table: string;
  start: number;
  end: number;
}

interface ExistingParse {
  assignments: ExistingAssignment[];
  tables: ExistingTable[];
  managedBlocks: ManagedBlock[];
  unsupportedByTable: Map<string, number[]>;
  duplicateTables: Set<string>;
}

const MANAGED_START = "# >>> PAI managed: codex config";
const MANAGED_END = "# <<< PAI managed: codex config";
const DEFAULT_SOURCE_LABEL = "PAI";

function productRootFromEnginePath(): string {
  return resolve(import.meta.dir, "../../../../..");
}

function isWithinPath(parentPath: string, candidatePath: string): boolean {
  const parent = resolve(parentPath);
  const candidate = resolve(candidatePath);
  const rel = relative(parent, candidate);
  return rel === "" || (!!rel && !rel.startsWith("..") && !isAbsolute(rel));
}

function assertNotWithin(label: string, deniedRoot: string, candidatePath: string): void {
  if (isWithinPath(deniedRoot, candidatePath)) {
    throw new Error(`Refusing Codex config merge inside ${label}: ${candidatePath}`);
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

function isExplicitTempHomePath(options: CodexConfigMergeOptions, home: string, configPath: string): boolean {
  if (!options.env?.HOME || !options.allowedRoot) return false;

  const requestedHome = resolve(home);
  return resolve(options.env.HOME) === requestedHome
    && isWithinPath(tmpdir(), requestedHome)
    && isWithinPath(requestedHome, configPath)
    && isWithinPath(resolve(options.allowedRoot), configPath);
}

function assertNoSymlinkComponents(rootPath: string, descendantPath: string): void {
  const root = resolve(rootPath);
  const descendant = resolve(descendantPath);

  if (isSymlink(root)) {
    throw new Error(`Refusing Codex config merge through symlink allowedRoot: ${root}`);
  }

  const rel = relative(root, descendant);
  if (rel.startsWith("..") || isAbsolute(rel)) return;

  let current = root;
  for (const segment of rel.split(sep)) {
    if (!segment) continue;
    current = join(current, segment);
    if (existsSync(current) && isSymlink(current)) {
      throw new Error(`Refusing Codex config merge through symlink path component: ${current}`);
    }
  }
}

function assertProtectedHomeRoots(options: CodexConfigMergeOptions, configPath: string): void {
  const configuredHome = currentHome(options.env);
  const processHome = resolve(process.env.HOME || homedir());
  const candidatePaths = [resolve(configPath)];
  try {
    candidatePaths.push(realpathSync(configPath));
  } catch {
    try {
      candidatePaths.push(realpathSync(dirname(configPath)));
    } catch {
      // Parent existence is checked separately; lexical checks still apply here.
    }
  }

  const protectedHomeRoots = [
    ["real/home Codex CLI state/config home", join(processHome, ".codex"), processHome, false],
    ["real/home default PAI home", join(processHome, ".pai"), processHome, false],
    ["real/home Claude adapter home", join(processHome, ".claude"), processHome, false],
    ["configured HOME Codex CLI state/config home", join(configuredHome, ".codex"), configuredHome, true],
    ["configured HOME default PAI home", join(configuredHome, ".pai"), configuredHome, false],
    ["configured HOME Claude adapter home", join(configuredHome, ".claude"), configuredHome, false],
  ] as const;

  for (const [label, root, home, allowExplicitTempHome] of protectedHomeRoots) {
    const allowedTempHomePath = allowExplicitTempHome && isExplicitTempHomePath(options, home, configPath);
    const rootCandidates = [root];
    try {
      rootCandidates.push(realpathSync(root));
    } catch {
      try {
        rootCandidates.push(join(realpathSync(home), basename(root)));
      } catch {
        // Lexical root remains enough when the configured home does not exist.
      }
    }

    for (const rootCandidate of rootCandidates) {
      if (candidatePaths.some((candidatePath) => isWithinPath(rootCandidate, candidatePath)) && !allowedTempHomePath) {
        throw new Error(`Refusing Codex config merge inside ${label}: ${options.configPath}`);
      }
    }
  }
}

function assertConfigPathAllowed(options: CodexConfigMergeOptions): string {
  if (!options.configPath || !options.configPath.trim()) {
    throw new Error("Codex config merge requires an explicit configPath");
  }

  const configPath = resolve(options.configPath);
  const parent = dirname(configPath);
  const allowedRoot = options.allowedRoot ? resolve(options.allowedRoot) : "";

  if (!options.allowNonDefaultBasenameForTests && basename(configPath) !== "config.toml") {
    throw new Error(`Codex config merge only supports config.toml outputs: ${options.configPath}`);
  }

  const productRoot = productRootFromEnginePath();
  assertNotWithin("repository governance .codex directory", join(productRoot, ".codex"), configPath);

  if (!options.allowedRoot) {
    throw new Error("Codex config merge requires an explicit allowedRoot");
  }

  if (!existsSync(allowedRoot)) {
    throw new Error(`Codex config merge allowedRoot must exist: ${allowedRoot}`);
  }

  if (!isWithinPath(allowedRoot, configPath)) {
    throw new Error(`Refusing Codex config merge outside allowedRoot: ${options.configPath}`);
  }

  assertProtectedHomeRoots(options, configPath);

  if (!existsSync(parent)) {
    throw new Error(`Codex config merge parent directory must exist: ${parent}`);
  }

  if (existsSync(configPath) && isSymlink(configPath)) {
    throw new Error(`Refusing Codex config merge into symlink config path: ${options.configPath}`);
  }

  if (isSymlink(parent)) {
    throw new Error(`Refusing Codex config merge through symlink parent directory: ${parent}`);
  }

  assertNoSymlinkComponents(allowedRoot, parent);

  const realAllowedRoot = realpathSync(allowedRoot);
  const realParent = realpathSync(parent);
  if (!isWithinPath(realAllowedRoot, realParent)) {
    throw new Error(`Refusing Codex config merge outside allowedRoot after realpath resolution: ${options.configPath}`);
  }

  assertProtectedHomeRoots(options, existsSync(configPath) ? realpathSync(configPath) : realParent);

  return configPath;
}

function normalizeTomlText(text: string, label: string): string[] {
  if (text.includes("\r")) {
    throw new Error(`${label} must use LF line endings; CR bytes are unsupported`);
  }

  if (!text) return [];
  return text.endsWith("\n") ? text.slice(0, -1).split("\n") : text.split("\n");
}

function fromLines(lines: string[]): string {
  return lines.length === 0 ? "" : `${lines.join("\n")}\n`;
}

function parseTableHeader(line: string): string | null {
  const trimmed = line.trim();
  if (trimmed.startsWith("[[")) {
    return null;
  }

  const match = trimmed.match(/^\[([A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*)\](?:\s*#.*)?$/);
  return match ? match[1] : null;
}

function parseSimpleAssignment(line: string): { key: string; raw: string } | null {
  const trimmed = line.trim();
  const match = trimmed.match(/^([A-Za-z0-9_-]+)\s*=\s*(.+)$/);
  if (!match) return null;
  return { key: match[1], raw: trimmed };
}

function parseDottedAssignment(line: string): { table: string; key: string } | null {
  const trimmed = line.trim();
  const match = trimmed.match(/^([A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+)\s*=\s*(.+)$/);
  if (!match) return null;

  const parts = match[1].split(".");
  return {
    table: parts.slice(0, -1).join("."),
    key: parts[parts.length - 1],
  };
}

function isCommentOrBlank(line: string): boolean {
  const trimmed = line.trim();
  return trimmed === "" || trimmed.startsWith("#");
}

function rejectUnsupportedFragmentLine(line: string, lineNumber: number): never {
  throw new Error(`Unsupported Codex config fragment syntax on line ${lineNumber}: ${line}`);
}

function parseFragment(fragment: string): FragmentBlock[] {
  const lines = normalizeTomlText(fragment, "Codex config fragment");
  const blocks = new Map<string, FragmentBlock>();
  const order: string[] = [];
  let table = "";

  const blockFor = (tableName: string): FragmentBlock => {
    let block = blocks.get(tableName);
    if (!block) {
      block = { table: tableName, lines: [], keys: [] };
      blocks.set(tableName, block);
      order.push(tableName);
    }
    return block;
  };

  blockFor("");

  for (let index = 0; index < lines.length; index++) {
    const line = lines[index];
    const lineNumber = index + 1;
    const trimmed = line.trim();

    if (trimmed === "") {
      blockFor(table).lines.push("");
      continue;
    }

    if (trimmed.startsWith("#")) {
      blockFor(table).lines.push(line.trimEnd());
      continue;
    }

    if (trimmed.startsWith("[[")) {
      rejectUnsupportedFragmentLine(line, lineNumber);
    }

    if (trimmed.startsWith("[")) {
      const parsedTable = parseTableHeader(line);
      if (!parsedTable) rejectUnsupportedFragmentLine(line, lineNumber);
      table = parsedTable;
      blockFor(table);
      continue;
    }

    if (/^[A-Za-z0-9_-]+\.[A-Za-z0-9_.-]+\s*=/.test(trimmed)) {
      rejectUnsupportedFragmentLine(line, lineNumber);
    }

    const assignment = parseSimpleAssignment(line);
    if (!assignment) rejectUnsupportedFragmentLine(line, lineNumber);

    const rawValue = assignment.raw.slice(assignment.raw.indexOf("=") + 1).trim();
    if (
      !rawValue
      || rawValue.startsWith("[")
      || rawValue.startsWith("{")
      || rawValue.startsWith('"""')
      || rawValue.startsWith("'''")
    ) {
      rejectUnsupportedFragmentLine(line, lineNumber);
    }

    const block = blockFor(table);
    if (block.keys.includes(assignment.key)) {
      throw new Error(`Duplicate Codex config fragment key ${table ? `${table}.` : ""}${assignment.key}`);
    }
    block.keys.push(assignment.key);
    block.lines.push(assignment.raw);
  }

  return order
    .map((tableName) => blocks.get(tableName)!)
    .filter((block) => block.lines.some((line) => line.trim() !== "") || block.keys.length > 0);
}

function parseExisting(lines: string[]): ExistingParse {
  const assignments: ExistingAssignment[] = [];
  const managedBlocks: ManagedBlock[] = [];
  const unsupportedByTable = new Map<string, number[]>();
  const duplicateTables = new Set<string>();
  const tableStarts = new Map<string, number>();
  const tables: ExistingTable[] = [];
  let table = "";
  let managedStart: { table: string; index: number } | null = null;

  const addUnsupported = (tableName: string, lineNumber: number): void => {
    const existing = unsupportedByTable.get(tableName) || [];
    existing.push(lineNumber);
    unsupportedByTable.set(tableName, existing);
  };

  const closeCurrentTable = (endIndex: number): void => {
    if (!table) return;
    const start = tableStarts.get(table);
    if (start !== undefined) tables.push({ table, start, end: endIndex });
  };

  for (let index = 0; index < lines.length; index++) {
    const line = lines[index];
    const trimmed = line.trim();
    const lineNumber = index + 1;

    if (trimmed === MANAGED_START) {
      if (managedStart) throw new Error(`Nested PAI-managed Codex config block at line ${lineNumber}`);
      managedStart = { table, index };
      continue;
    }

    if (trimmed === MANAGED_END) {
      if (!managedStart) throw new Error(`Unmatched PAI-managed Codex config block end at line ${lineNumber}`);
      managedBlocks.push({ table: managedStart.table, start: managedStart.index, end: index });
      managedStart = null;
      continue;
    }

    if (managedStart) continue;
    if (isCommentOrBlank(line)) continue;

    if (trimmed.startsWith("[[")) {
      addUnsupported(table, lineNumber);
      const arrayTableMatch = trimmed.match(/^\[\[([A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*)\]\]/);
      if (arrayTableMatch) addUnsupported(arrayTableMatch[1], lineNumber);
      table = `__unsupported_array_table_${lineNumber}`;
      continue;
    }

    if (trimmed.startsWith("[")) {
      const parsedTable = parseTableHeader(line);
      if (!parsedTable) {
        addUnsupported(table, lineNumber);
        continue;
      }

      closeCurrentTable(index);
      table = parsedTable;
      if (tableStarts.has(table)) duplicateTables.add(table);
      tableStarts.set(table, index);
      continue;
    }

    const dottedAssignment = parseDottedAssignment(line);
    if (dottedAssignment) {
      addUnsupported(table, lineNumber);
      addUnsupported(table ? `${table}.${dottedAssignment.table}` : dottedAssignment.table, lineNumber);
      continue;
    }

    const assignment = parseSimpleAssignment(line);
    if (assignment) {
      assignments.push({ table, key: assignment.key, line: lineNumber });
      continue;
    }

    addUnsupported(table, lineNumber);
  }

  if (managedStart) {
    throw new Error(`Unclosed PAI-managed Codex config block at line ${managedStart.index + 1}`);
  }

  closeCurrentTable(lines.length);
  return { assignments, tables, managedBlocks, unsupportedByTable, duplicateTables };
}

function removeManagedBlocks(lines: string[], managedBlocks: ManagedBlock[], targetTables: Set<string>): string[] {
  const remove = new Set<number>();
  for (const block of managedBlocks) {
    if (!targetTables.has(block.table)) continue;
    for (let index = block.start; index <= block.end; index++) remove.add(index);
  }
  return lines.filter((_, index) => !remove.has(index));
}

function findTable(lines: string[], table: string): { start: number; end: number } | null {
  let start = -1;
  for (let index = 0; index < lines.length; index++) {
    if (parseTableHeader(lines[index]) === table) {
      start = index;
      break;
    }
  }
  if (start === -1) return null;

  let end = lines.length;
  for (let index = start + 1; index < lines.length; index++) {
    if (parseTableHeader(lines[index]) !== null || lines[index].trim().startsWith("[[")) {
      end = index;
      break;
    }
  }
  return { start, end };
}

function firstTableIndex(lines: string[]): number {
  const index = lines.findIndex((line) => parseTableHeader(line) !== null || line.trim().startsWith("[["));
  return index === -1 ? lines.length : index;
}

function managedLines(block: FragmentBlock, sourceLabel: string): string[] {
  const fragmentLines = [...block.lines];
  while (fragmentLines[0]?.trim() === "") fragmentLines.shift();
  while (fragmentLines[fragmentLines.length - 1]?.trim() === "") fragmentLines.pop();
  return [MANAGED_START, `# source: ${sourceLabel}`, ...fragmentLines, MANAGED_END];
}

function insertBlock(lines: string[], block: FragmentBlock, sourceLabel: string): { insertedTable: boolean } {
  const blockLines = managedLines(block, sourceLabel);

  if (block.table === "") {
    const index = firstTableIndex(lines);
    const insertion = [...blockLines];
    if (index < lines.length && lines[index] !== "") insertion.push("");
    if (index > 0 && lines[index - 1] !== "") insertion.unshift("");
    lines.splice(index, 0, ...insertion);
    return { insertedTable: false };
  }

  const section = findTable(lines, block.table);
  if (section) {
    const insertion = [...blockLines];
    const previousLineIsTableHeader = section.end - 1 === section.start;
    if (!previousLineIsTableHeader && section.end > 0 && lines[section.end - 1] !== "") insertion.unshift("");
    if (section.end < lines.length && lines[section.end] !== "") insertion.push("");
    lines.splice(section.end, 0, ...insertion);
    return { insertedTable: false };
  }

  if (lines.length > 0 && lines[lines.length - 1] !== "") lines.push("");
  lines.push(`[${block.table}]`, ...blockLines);
  return { insertedTable: true };
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

function validateSourceLabel(sourceLabel: string): string {
  if (sourceLabel.includes("\n") || sourceLabel.includes("\r")) {
    throw new Error("Codex config sourceLabel must be a single line");
  }
  return sourceLabel;
}

function tablesOverlap(a: string, b: string): boolean {
  return a === b || (!!a && b.startsWith(`${a}.`)) || (!!b && a.startsWith(`${b}.`));
}

function validateTomlContent(content: string): void {
  try {
    Bun.TOML.parse(content);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    throw new Error(`Merged Codex config TOML is invalid: ${message}`);
  }
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

function writeConfigAtomically(configPath: string, content: string, mode: number): void {
  const parent = dirname(configPath);
  const tempPath = join(parent, `.${basename(configPath)}.pai-tmp-${process.pid}-${randomUUID()}`);

  try {
    writeExclusiveFile(tempPath, content, mode);
    renameSync(tempPath, configPath);
  } catch (error) {
    try {
      if (existsSync(tempPath)) unlinkSync(tempPath);
    } catch {
      // Best-effort cleanup only.
    }
    throw error;
  }
}

export function mergeCodexConfig(options: CodexConfigMergeOptions): CodexConfigMergeResult {
  const configPath = assertConfigPathAllowed(options);
  const sourceLabel = validateSourceLabel(options.sourceLabel || DEFAULT_SOURCE_LABEL);
  const fragmentBlocks = parseFragment(options.fragment);
  const existingContent = existsSync(configPath) ? readFileSync(configPath, "utf-8") : "";
  const existingLines = normalizeTomlText(existingContent, "Existing Codex config");
  const initialParse = parseExisting(existingLines);
  const targetTables = new Set(fragmentBlocks.map((block) => block.table));

  for (const table of targetTables) {
    const unsupported = [...initialParse.unsupportedByTable.entries()].find(([unsupportedTable]) =>
      tablesOverlap(table, unsupportedTable),
    )?.[1];
    if (unsupported?.length) {
      throw new Error(`Unsupported TOML syntax in target table ${table || "<top-level>"} at line ${unsupported[0]}`);
    }
    if (initialParse.duplicateTables.has(table)) {
      throw new Error(`Duplicate TOML table ${table || "<top-level>"} cannot be merged safely`);
    }
  }

  const strippedLines = removeManagedBlocks(existingLines, initialParse.managedBlocks, targetTables);
  const conflicts: CodexConfigMergeConflict[] = [];

  for (const block of fragmentBlocks) {
    for (const key of block.keys) {
      const existing = initialParse.assignments.find(
        (assignment) => assignment.table === block.table && assignment.key === key,
      );
      if (existing) {
        conflicts.push({
          table: block.table,
          key,
          existingLine: existing.line,
          reason: "Existing user-owned Codex config key would be overwritten",
        });
      }
    }
  }

  if (conflicts.length > 0) {
    return {
      changed: false,
      configPath,
      content: existingContent,
      conflicts,
      insertedTables: [],
      insertedKeys: [],
    };
  }

  const mergedLines = [...strippedLines];
  const insertedTables: string[] = [];
  for (const block of fragmentBlocks) {
    if (block.keys.length === 0 && block.lines.every((line) => line.trim() === "" || line.trim().startsWith("#"))) {
      continue;
    }
    const inserted = insertBlock(mergedLines, block, sourceLabel);
    if (inserted.insertedTable) insertedTables.push(block.table);
  }

  const content = fromLines(mergedLines);
  const changed = content !== existingContent;
  const insertedKeys = changed
    ? fragmentBlocks.flatMap((block) => block.keys.map((key) => (block.table ? `${block.table}.${key}` : key)))
    : [];

  if (changed) {
    validateTomlContent(content);
  }

  if (!changed || options.dryRun) {
    return {
      changed,
      configPath,
      content,
      conflicts: [],
      insertedTables: changed ? insertedTables : [],
      insertedKeys,
    };
  }

  let backupPath: string | undefined;
  const mode = existsSync(configPath) ? statSync(configPath).mode & 0o777 : 0o600;
  if (options.backup && existsSync(configPath)) {
    backupPath = join(dirname(configPath), `${basename(configPath)}.pai-backup-${timestamp(options.now || new Date())}`);
    if (existsSync(backupPath)) {
      throw new Error(`Refusing to overwrite existing Codex config backup: ${backupPath}`);
    }
    if (isSymlink(backupPath)) {
      throw new Error(`Refusing Codex config backup through symlink path: ${backupPath}`);
    }
    writeExclusiveFile(backupPath, existingContent, mode);
  }

  writeConfigAtomically(configPath, content, mode);

  return {
    changed: true,
    configPath,
    content,
    backupPath,
    conflicts: [],
    insertedTables,
    insertedKeys,
  };
}
