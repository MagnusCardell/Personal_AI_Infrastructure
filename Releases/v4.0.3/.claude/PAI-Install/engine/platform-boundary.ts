import type { InstallState, InstallerPlatform, DetectionResult, EngineEventHandler } from "./types";
import { includesTargetPlatform } from "./options";

export class PlatformBoundaryStop extends Error {
  readonly name = "PlatformBoundaryStop";
  readonly exitCode = 2;
  readonly platform: InstallerPlatform;

  constructor(message: string, platform: InstallerPlatform) {
    super(message);
    this.platform = platform;
  }
}

export class CodexPrerequisiteMissingError extends Error {
  readonly name = "CodexPrerequisiteMissingError";
  readonly exitCode = 2;

  constructor(message: string) {
    super(message);
  }
}

export function isPlatformBoundaryStop(error: unknown): error is PlatformBoundaryStop | CodexPrerequisiteMissingError {
  return error instanceof PlatformBoundaryStop || error instanceof CodexPrerequisiteMissingError;
}

export function buildCodexPrerequisiteMissingMessage(): string {
  return [
    "Codex CLI is required for the selected platform but was not found.",
    "Install it manually with one of:",
    "  npm install -g @openai/codex",
    "  brew install codex",
  ].join("\n");
}

function codexPaths(detection: DetectionResult): { paiHome: string; adapterHome: string } {
  const paths = detection.platformPaths.codex;
  return {
    paiHome: paths?.paiHome || detection.paiDir,
    adapterHome: paths?.adapterHome || "unknown",
  };
}

export function buildCodexBoundaryMessage(state: InstallState): string {
  const detection = state.detection;
  const selected = state.platform;
  const codexStatus = detection?.tools.codex.installed
    ? `Codex CLI detected: v${detection.tools.codex.version || "unknown"}${detection.tools.codex.path ? ` at ${detection.tools.codex.path}` : ""}`
    : "Codex CLI missing.";
  const paths = detection ? codexPaths(detection) : { paiHome: "unknown", adapterHome: "unknown" };
  const modeLine = selected === "both"
    ? "Both-mode installation is not implemented yet."
    : "Codex installer support is not implemented yet.";

  return [
    codexStatus,
    `Selected platform = ${selected}.`,
    `Planned PAI home = ${paths.paiHome}.`,
    `Planned Codex adapter/config home = ${paths.adapterHome}.`,
    modeLine,
    "No files were written.",
    "Run --platform claude for the current stable installer path.",
  ].join("\n");
}

export async function maybeStopForUnsupportedCodexInstall(
  state: InstallState,
  emit?: EngineEventHandler,
): Promise<void> {
  if (!includesTargetPlatform(state, "codex")) return;

  const message = buildCodexBoundaryMessage(state);
  if (emit) {
    await emit({ event: "message", content: message });
  }
  throw new PlatformBoundaryStop(message, state.platform);
}
