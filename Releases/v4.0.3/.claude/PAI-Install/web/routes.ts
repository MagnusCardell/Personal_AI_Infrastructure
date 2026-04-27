/**
 * PAI Installer v4.0 — API Routes
 * HTTP + WebSocket API for the web installer.
 */

import type { InstallState, EngineEvent, ServerMessage, ClientMessage, InstallerOptions } from "../engine/types";
import {
  runSystemDetect,
  runPrerequisites,
  runApiKeys,
  runIdentity,
  runRepository,
  runConfiguration,
  runVoiceSetup,
} from "../engine/actions";
import type { DetectSystemOptions } from "../engine/detect";
import { runValidation, generateSummary } from "../engine/validate";
import { includesTargetPlatform, normalizeInstallerOptions } from "../engine/options";
import {
  createFreshState,
  hasSavedState,
  loadState,
  saveState,
  clearState,
  completeStep,
  completeStepInMemory,
  skipStep,
} from "../engine/state";
import { STEPS, getProgress, getStepStatuses } from "../engine/steps";
import {
  isPlatformBoundaryStop,
  maybeStopForUnsupportedCodexInstall,
} from "../engine/platform-boundary";

// ─── State ───────────────────────────────────────────────────────

let installState: InstallState | null = null;
let wsClients = new Set<any>();
let messageHistory: ServerMessage[] = [];
let pendingRequests = new Map<string, { resolve: (value: string) => void }>();
const installerOptions = normalizeInstallerOptions({
  mode: "web",
  platform: process.env.PAI_INSTALL_PLATFORM as any,
});

// ─── Broadcasting ────────────────────────────────────────────────

function broadcast(msg: ServerMessage): void {
  const raw = JSON.stringify(msg);
  messageHistory.push(msg);
  for (const ws of wsClients) {
    try {
      ws.send(raw);
    } catch {
      wsClients.delete(ws);
    }
  }
}

// ─── Engine Event → WebSocket ────────────────────────────────────

function createWsEmitter(): (event: EngineEvent) => Promise<void> {
  return async (event: EngineEvent) => {
    switch (event.event) {
      case "step_start":
        broadcast({ type: "step_update", step: event.step, status: "active" });
        break;
      case "step_complete":
        broadcast({ type: "step_update", step: event.step, status: "completed" });
        break;
      case "step_skip":
        broadcast({ type: "step_update", step: event.step, status: "skipped", detail: event.reason });
        break;
      case "step_error":
        broadcast({ type: "error", message: event.error, step: event.step });
        break;
      case "progress":
        broadcast({ type: "progress", step: event.step, percent: event.percent, detail: event.detail });
        break;
      case "message":
        broadcast({ type: "message", role: "assistant", content: event.content, speak: event.speak });
        break;
      case "error":
        broadcast({ type: "error", message: event.message });
        break;
    }
  };
}

// ─── Input Request Bridge ────────────────────────────────────────

async function requestInput(
  id: string,
  prompt: string,
  type: "text" | "password" | "key",
  placeholder?: string
): Promise<string> {
  return new Promise<string>((resolve) => {
    pendingRequests.set(id, { resolve });
    broadcast({ type: "input_request", id, prompt, inputType: type, placeholder });
  });
}

async function requestChoice(
  id: string,
  prompt: string,
  choices: { label: string; value: string; description?: string }[]
): Promise<string> {
  return new Promise<string>((resolve) => {
    pendingRequests.set(id, { resolve });
    broadcast({ type: "choice_request", id, prompt, choices });
  });
}

// ─── WebSocket Message Handler ───────────────────────────────────

export function handleWsMessage(ws: any, raw: string): void {
  let msg: ClientMessage;
  try {
    msg = JSON.parse(raw);
  } catch {
    return;
  }

  switch (msg.type) {
    case "client_ready":
      // Replay message history
      for (const m of messageHistory) {
        ws.send(JSON.stringify({ ...m, replayed: true }));
      }
      // Send current state
      if (installState) {
        const steps = getStepStatuses(installState);
        for (const s of steps) {
          ws.send(JSON.stringify({ type: "step_update", step: s.id, status: s.status }));
        }
      }
      break;

    case "user_input": {
      const pending = pendingRequests.get(msg.requestId);
      if (pending) {
        pending.resolve(msg.value);
        pendingRequests.delete(msg.requestId);
        // Echo user message (masked for keys)
        const display = msg.value.startsWith("sk-") || msg.value.startsWith("xi-")
          ? msg.value.substring(0, 8) + "..."
          : msg.value;
        if (display) {
          broadcast({ type: "message", role: "system" as any, content: display });
        }
      }
      break;
    }

    case "user_choice": {
      const pending = pendingRequests.get(msg.requestId);
      if (pending) {
        pending.resolve(msg.value);
        pendingRequests.delete(msg.requestId);
      }
      break;
    }

    case "start_install": {
      if (!installState) {
        startInstallation();
      }
      break;
    }
  }
}

// ─── Installation Flow ───────────────────────────────────────────

export async function startInstallation(
  options: Partial<InstallerOptions> = installerOptions,
  detectOptions: DetectSystemOptions = {},
): Promise<void> {
  const normalizedOptions = normalizeInstallerOptions({ ...options, mode: "web" });
  const codexRequested = includesTargetPlatform(normalizedOptions, "codex");

  // Always start fresh — GUI should not silently resume stale state.
  // Unsupported Codex-selected boundary runs must leave saved Claude state untouched.
  if (!codexRequested && hasSavedState()) clearState();
  installState = createFreshState("web", normalizedOptions);

  const emit = createWsEmitter();

  try {
    const codexSelected = includesTargetPlatform(installState, "codex");

    // Step 1: System Detection
    if (!installState.completedSteps.includes("system-detect")) {
      await runSystemDetect(installState, emit, detectOptions);
      broadcast({ type: "detection_result", data: installState.detection! });
      if (codexSelected) {
        completeStepInMemory(installState, "system-detect");
      } else {
        completeStep(installState, "system-detect");
      }
      installState.currentStep = "prerequisites";
    }

    // Step 2: Prerequisites
    if (!installState.completedSteps.includes("prerequisites")) {
      await runPrerequisites(installState, emit);
      if (codexSelected) {
        completeStepInMemory(installState, "prerequisites");
      } else {
        completeStep(installState, "prerequisites");
        installState.currentStep = "api-keys";
      }
    }

    await maybeStopForUnsupportedCodexInstall(installState, emit);

    // Step 3: API Keys
    if (!installState.completedSteps.includes("api-keys")) {
      await runApiKeys(installState, emit, requestInput, requestChoice);
      completeStep(installState, "api-keys");
      installState.currentStep = "identity";
    }

    // Step 4: Identity
    if (!installState.completedSteps.includes("identity")) {
      await runIdentity(installState, emit, requestInput);
      completeStep(installState, "identity");
      installState.currentStep = "repository";
    }

    // Step 5: Repository
    if (!installState.completedSteps.includes("repository")) {
      await runRepository(installState, emit);
      completeStep(installState, "repository");
      installState.currentStep = "configuration";
    }

    // Step 6: Configuration
    if (!installState.completedSteps.includes("configuration")) {
      await runConfiguration(installState, emit);
      completeStep(installState, "configuration");
      installState.currentStep = "voice";
    }

    // Step 7: Voice (handles key collection + voice selection + server test)
    if (!installState.completedSteps.includes("voice") && !installState.skippedSteps.includes("voice")) {
      try {
        await runVoiceSetup(installState, emit, requestChoice, requestInput);
        if (!installState.skippedSteps.includes("voice")) {
          completeStep(installState, "voice");
        }
      } catch (voiceErr: any) {
        broadcast({ type: "error", message: `Voice setup error: ${voiceErr?.message || "Unknown error"}` });
        broadcast({ type: "message", role: "assistant", content: "Voice setup encountered an error. Continuing with installation..." });
        skipStep(installState, "voice", voiceErr?.message || "error");
      }
      installState.currentStep = "validation";
    }

    // Step 8: Validation
    broadcast({ type: "step_update", step: "validation", status: "active" });
    const checks = await runValidation(installState);
    broadcast({ type: "validation_result", checks });
    completeStep(installState, "validation");
    broadcast({ type: "step_update", step: "validation", status: "completed" });

    const summary = generateSummary(installState);
    broadcast({ type: "install_complete", success: true, summary });

    clearState();
  } catch (error: any) {
    if (isPlatformBoundaryStop(error)) {
      broadcast({ type: "error", message: error.message });
      return;
    }

    broadcast({ type: "error", message: error.message });
    if (installState && includesTargetPlatform(installState, "codex")) {
      return;
    }

    saveState(installState);
  }
}

// ─── Connection Management ───────────────────────────────────────

export function addClient(ws: any): void {
  wsClients.add(ws);
}

export function removeClient(ws: any): void {
  wsClients.delete(ws);
}

export function getState(): InstallState | null {
  return installState;
}

export function getMessageHistory(): ServerMessage[] {
  return [...messageHistory];
}

export function resetForTests(): void {
  installState = null;
  wsClients = new Set<any>();
  messageHistory = [];
  pendingRequests = new Map<string, { resolve: (value: string) => void }>();
}
