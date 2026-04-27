/**
 * PAI Installer v4.0 — CLI Wizard
 * Interactive command-line installation experience.
 */

import type { EngineEvent, InstallerOptions, InstallState, StepId } from "../engine/types";
import { STEPS, getProgress } from "../engine/steps";
import {
  createFreshState,
  hasSavedState,
  loadState,
  saveState,
  clearState,
  completeStep,
  completeStepInMemory,
} from "../engine/state";
import {
  runSystemDetect,
  runPrerequisites,
  runApiKeys,
  runIdentity,
  runRepository,
  runConfiguration,
  runVoiceSetup,
} from "../engine/actions";
import { runValidation, generateSummary } from "../engine/validate";
import { includesTargetPlatform, normalizeInstallerOptions } from "../engine/options";
import {
  isPlatformBoundaryStop,
  maybeStopForUnsupportedCodexInstall,
} from "../engine/platform-boundary";
import {
  printBanner,
  printStep,
  printDetection,
  printValidation,
  printSummary,
  print,
  printSuccess,
  printError,
  printWarning,
  printInfo,
  progressBar,
  c,
} from "./display";
import { promptText, promptSecret, promptChoice, promptConfirm } from "./prompts";

/**
 * Handle engine events in CLI mode.
 */
function createEventHandler(): (event: EngineEvent) => void {
  return (event: EngineEvent) => {
    switch (event.event) {
      case "step_start":
        // Handled by the main loop with printStep
        break;
      case "step_complete":
        printSuccess("Step complete");
        break;
      case "step_skip":
        printInfo(`Skipped: ${event.reason}`);
        break;
      case "step_error":
        printError(`Error: ${event.error}`);
        break;
      case "progress":
        print(`  ${progressBar(event.percent)} ${c.gray}${event.detail}${c.reset}`);
        break;
      case "message":
        print(`\n  ${event.content}\n`);
        break;
      case "error":
        printError(event.message);
        break;
    }
  };
}

/**
 * CLI input adapter — bridges engine's input requests to readline prompts.
 */
async function getInput(
  id: string,
  prompt: string,
  type: "text" | "password" | "key",
  placeholder?: string
): Promise<string> {
  if (type === "key" || type === "password") {
    return promptSecret(prompt, placeholder);
  }
  return promptText(prompt, placeholder);
}

/**
 * CLI choice adapter.
 */
async function getChoice(
  id: string,
  prompt: string,
  choices: { label: string; value: string; description?: string }[]
): Promise<string> {
  return promptChoice(prompt, choices);
}

/**
 * Run the full CLI installation wizard.
 */
export function statePlatformMatchesOptions(state: InstallState, options: Partial<InstallerOptions>): boolean {
  const requested = normalizeInstallerOptions({
    ...options,
    mode: "cli",
  });
  return state.platform === requested.platform;
}

export async function runCLI(options: Partial<InstallerOptions> = {}): Promise<void> {
  printBanner();

  const emit = createEventHandler();
  const normalizedOptions = normalizeInstallerOptions({ ...options, mode: "cli" });
  const codexRequested = includesTargetPlatform(normalizedOptions, "codex");

  // Check for resume
  let state: InstallState;

  if (codexRequested) {
    state = createFreshState("cli", normalizedOptions);
  } else if (hasSavedState()) {
    const saved = loadState();
    if (saved) {
      if (!statePlatformMatchesOptions(saved, options)) {
        printWarning(
          `Saved install platform (${saved.platform}) does not match requested platform; starting a fresh ${normalizedOptions.platform} install.`,
        );
        clearState();
        state = createFreshState("cli", options);
      } else {
        print(`  ${c.yellow}Found previous installation in progress.${c.reset}`);
        print(`  ${c.gray}Started: ${saved.startedAt}${c.reset}`);
        print(`  ${c.gray}Progress: ${getProgress(saved)}% (${saved.completedSteps.length} steps completed)${c.reset}`);
        print("");

        const resume = await promptConfirm("Resume previous installation?");
        if (resume) {
          state = saved;
          state.mode = "cli";
          print(`\n  ${c.green}Resuming from step: ${state.currentStep}${c.reset}\n`);
        } else {
          state = createFreshState("cli", options);
        }
      }
    } else {
      state = createFreshState("cli", options);
    }
  } else {
    state = createFreshState("cli", options);
  }

  try {
    const codexSelected = includesTargetPlatform(state, "codex");

    // ── Step 1: System Detection ──
    if (!state.completedSteps.includes("system-detect")) {
      const step = STEPS[0];
      printStep(step.number, 8, step.name);
      const detection = await runSystemDetect(state, emit);
      printDetection(detection);
      if (codexSelected) {
        completeStepInMemory(state, "system-detect");
      } else {
        completeStep(state, "system-detect");
      }
      state.currentStep = "prerequisites";
    }

    // ── Step 2: Prerequisites ──
    if (!state.completedSteps.includes("prerequisites")) {
      const step = STEPS[1];
      printStep(step.number, 8, step.name);
      await runPrerequisites(state, emit);
      if (codexSelected) {
        completeStepInMemory(state, "prerequisites");
      } else {
        completeStep(state, "prerequisites");
        state.currentStep = "api-keys";
      }
    }

    await maybeStopForUnsupportedCodexInstall(state, emit);

    // ── Step 3: API Keys ──
    if (!state.completedSteps.includes("api-keys")) {
      const step = STEPS[2];
      printStep(step.number, 8, step.name);
      await runApiKeys(state, emit, getInput, getChoice);
      completeStep(state, "api-keys");
      state.currentStep = "identity";
    }

    // ── Step 4: Identity ──
    if (!state.completedSteps.includes("identity")) {
      const step = STEPS[3];
      printStep(step.number, 8, step.name);
      await runIdentity(state, emit, getInput);
      completeStep(state, "identity");
      state.currentStep = "repository";
    }

    // ── Step 5: Repository ──
    if (!state.completedSteps.includes("repository")) {
      const step = STEPS[4];
      printStep(step.number, 8, step.name);
      await runRepository(state, emit);
      completeStep(state, "repository");
      state.currentStep = "configuration";
    }

    // ── Step 6: Configuration ──
    if (!state.completedSteps.includes("configuration")) {
      const step = STEPS[5];
      printStep(step.number, 8, step.name);
      await runConfiguration(state, emit);
      completeStep(state, "configuration");
      state.currentStep = "voice";
    }

    // ── Step 7: Voice ──
    if (!state.completedSteps.includes("voice") && !state.skippedSteps.includes("voice")) {
      const step = STEPS[6];
      printStep(step.number, 8, step.name);
      await runVoiceSetup(state, emit, getChoice, getInput);
      completeStep(state, "voice");
      state.currentStep = "validation";
    }

    // ── Step 8: Validation ──
    if (!state.completedSteps.includes("validation")) {
      const step = STEPS[7];
      printStep(step.number, 8, step.name);

      const checks = await runValidation(state);
      printValidation(checks);

      const allCritical = checks.filter((c) => c.critical).every((c) => c.passed);
      if (allCritical) {
        completeStep(state, "validation");
      } else {
        printError("\nSome critical checks failed. Please review and fix the issues above.");
      }
    }

    // ── Summary ──
    const summary = generateSummary(state);
    printSummary(summary);

    // Clean up state file on success
    clearState();

    print(`  ${c.green}${c.bold}Installation complete!${c.reset}`);
    print(`  ${c.gray}Run ${c.bold}source ~/.zshrc && pai${c.reset}${c.gray} to launch PAI.${c.reset}`);
    print("");

    process.exit(0);
  } catch (error: any) {
    if (isPlatformBoundaryStop(error)) {
      process.exit(error.exitCode);
    }

    printError(`\nInstallation failed: ${error.message}`);
    if (includesTargetPlatform(state, "codex")) {
      process.exit(1);
    }

    printInfo("Your progress has been saved. Run the installer again to resume.");
    saveState(state);
    process.exit(1);
  }
}
