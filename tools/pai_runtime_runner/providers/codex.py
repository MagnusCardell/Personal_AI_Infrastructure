from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


RUN_ID = "s15d-codex-synthetic-bugfix"
RUN_RESULT_NAME = "run-result.json"
EVENTS_NAME = "runtime-events.jsonl"
REPO_RUN_RESULT_NAME = "repo-run-result.json"
REPO_EVENTS_NAME = "repo-events.jsonl"
REPO_RUN_ID = "s15e-provider-registry"
REPO_TASK_ID = "s15e-provider-registry-repo-task"
REPO_MILESTONE = "V5-S15E-PAI-RUNTIME-CODEX-REAL-REPO-TASK"
S15F_REPO_RUN_ID = "s15f-patch-proposal"
S15F_REPO_TASK_ID = "s15f-patch-proposal-repo-task"
S15F_REPO_MILESTONE = "V5-S15F-PAI-RUNTIME-PATCH-PROPOSAL-APPLIER"
S15I_CONTEXT_RUN_ID = "s15i-read-only-pai-context"
S15I_CONTEXT_TASK_ID = "s15i-readonly-pai-context-task"
S15I_CONTEXT_MILESTONE = "V5-S15I-PAI-RUNTIME-READONLY-PAI-CONTEXT-TASK"
PAI_CONTEXT_REPORT_NAME = "pai-context-report.json"
PAI_CONTEXT_EVENTS_NAME = "pai-context-events.jsonl"
MARKER = "PAI_CODEX_PEER_BETA_ADAPTER"


class CodexProviderError(ValueError):
    pass


def provider_driver(pai_dir: Path) -> Path:
    return pai_dir / "adapters" / "codex" / "bin" / "pai-codex"


def build_provider_command(pai_dir: Path, task_card: Path, run_dir: Path) -> list[str]:
    driver = provider_driver(pai_dir)
    return [
        str(driver),
        "provider-run",
        "--pai-dir",
        str(pai_dir),
        "--task-card",
        str(task_card),
        "--run-dir",
        str(run_dir),
        "--result",
        str(run_dir / RUN_RESULT_NAME),
        "--events-output",
        str(run_dir / EVENTS_NAME),
    ]


def run_codex_provider(pai_dir: Path, task_card: Path, run_dir: Path, dry_run: bool = False) -> dict[str, object]:
    """Run Codex as a PAI runtime provider.

    PAI owns the run. The provider driver only performs the bounded Codex
    execution step for the PAI-owned run directory.
    """

    driver = provider_driver(pai_dir)
    if not driver.is_file():
        raise CodexProviderError(f"Codex provider driver is missing: {driver}")
    command = build_provider_command(pai_dir, task_card, run_dir)
    if dry_run:
        return {
            "dry_run": True,
            "provider_command": command,
            "driver_path": str(driver),
            "run_dir": str(run_dir),
        }

    completed = subprocess.run(
        command,
        cwd=Path.cwd(),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise CodexProviderError(f"Codex provider failed: {completed.stderr.strip()}")
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise CodexProviderError("Codex provider did not return JSON") from exc
    if not isinstance(payload, dict):
        raise CodexProviderError("Codex provider response must be a JSON object")
    payload["provider_command"] = command
    return payload


def _repo_task_context(task_card: dict[str, object]) -> tuple[str, str, str]:
    milestone = str(task_card.get("milestone_name", ""))
    run_id = str(task_card.get("run_id", ""))
    task_id = str(task_card.get("task_id", ""))
    return milestone, run_id, task_id


def _repo_task_prompt_s15e(pai_dir: Path, task_card: dict[str, object], repo_root: Path, run_dir: Path) -> str:
    approved = task_card.get("approved_repository_write_set")
    targets = task_card.get("repository_target_files")
    test_command = task_card.get("test_command")
    approved_lines = "\n".join(f"- {item}" for item in approved if isinstance(item, str)) if isinstance(approved, list) else ""
    target_lines = "\n".join(f"- {item}" for item in targets if isinstance(item, str)) if isinstance(targets, list) else ""
    test_text = " ".join(test_command) if isinstance(test_command, list) and all(isinstance(item, str) for item in test_command) else ""
    registry_path = repo_root / "tools" / "pai_runtime_runner" / "provider_registry.py"
    registry_test_path = repo_root / "tests" / "test_pai_runtime_provider_registry.py"
    registry_text = registry_path.read_text(encoding="utf-8") if registry_path.is_file() else ""
    registry_test_text = registry_test_path.read_text(encoding="utf-8") if registry_test_path.is_file() else ""
    return (
        "You are Codex running as runtime provider codex under the PAI-owned runtime runner. "
        "PAI owns the run directory, task card, validation, and Memory/ISA/Pulse policy. "
        f"PAI_DIR is {str(pai_dir)!r}. "
        f"The actual adapter-development repository root is {str(repo_root)!r}. "
        f"The PAI-owned S15E run directory is {str(run_dir)!r}. "
        f"The installed router identity marker observed by the runtime runner is {MARKER!r}. "
        "Implement the bounded real repository task: improve the PAI runtime provider registry module and tests. "
        "Modify only the repository target files listed below. Do not create repo root AGENTS.md, repo .codex, "
        "Codex native install surfaces, Memory writers, ISA writers, Pulse bridges, hooks, skills, agents, commands, "
        "or files outside the approved repository write set. Do not call localhost:31337 or probe Pulse. "
        "The provider registry must support discover_runtime_providers, load_provider_manifest, "
        "validate_provider_manifest, and get_provider_by_name, and must enforce Codex peer-beta semantics: "
        "runtime_name=codex, runtime_status=peer-beta, provider_type=codex-cli, upstream_adapter=claude, "
        "supports_codex_exec=true, supports_jsonl_events=true, supports_structured_output=true, "
        "memory_write_policy=disabled, isa_write_policy=disabled, pulse_policy=no-probe, "
        "replacement_status=not-replacement-grade. "
        "If the implementation already exists, make a small real improvement by adding an explicit exported "
        "EXPECTED_CODEX_SEMANTIC_FIELDS tuple derived from the Codex semantics and add a provider-registry test "
        "that asserts it covers the Memory, ISA, Pulse, and replacement-grade guard fields. "
        "Always return complete final replacement contents in provider_registry_file_content and "
        "provider_registry_test_file_content. If your direct repository editing tools work, still include the final "
        "contents in those fields. If shell or direct edit tools fail, use these structured fields as the canonical "
        "Codex-authored patch for the PAI runtime runner to materialize, and still report the target files in "
        "repository_files_modified. "
        f"Run the provider registry tests with {test_text!r}. "
        "Return only JSON matching the provided schema. "
        f"Use milestone_name {REPO_MILESTONE!r}, run_id {REPO_RUN_ID!r}, runtime 'codex', runtime_status 'peer-beta', "
        "provider_type 'codex-cli', task_id 's15e-provider-registry-repo-task', "
        "task_kind 'bounded-real-repository-code-change', adapter_identity_marker exactly as observed, "
        "adapter_status 'peer-beta', upstream_adapter 'claude', agents_router_observed true, "
        "pai_owned_run_directory true, tests_passed true, memory_write_performed false, isa_write_performed false, "
        "pulse_probe_performed false, localhost_31337_called false, and runtime_surface_created false. "
        "Set patch_proposal to null, patch_proposal_produced false, patch_proposal_validated false, "
        "and patch_proposal_applied_by_pai false. "
        "Set repository_files_modified to the repository-relative files you changed. "
        "Use evidence_classification values including 'PAI-owned real repository task evidence', "
        "'runtime provider registry evidence', and 'not replacement readiness'. "
        "Do not include raw Memory, ISA, Pulse, backup, credential, or personal file contents. "
        f"Approved repository write set:\n{approved_lines}\n"
        f"Repository target files:\n{target_lines}\n"
        f"Current tools/pai_runtime_runner/provider_registry.py:\n{registry_text}\n"
        f"Current tests/test_pai_runtime_provider_registry.py:\n{registry_test_text}\n"
    )


def _repo_task_prompt_s15f(pai_dir: Path, task_card: dict[str, object], repo_root: Path, run_dir: Path) -> str:
    approved = task_card.get("approved_repository_write_set")
    targets = task_card.get("repository_target_files")
    test_command = task_card.get("test_command")
    approved_lines = "\n".join(f"- {item}" for item in approved if isinstance(item, str)) if isinstance(approved, list) else ""
    target_lines = "\n".join(f"- {item}" for item in targets if isinstance(item, str)) if isinstance(targets, list) else ""
    test_text = " ".join(test_command) if isinstance(test_command, list) and all(isinstance(item, str) for item in test_command) else ""
    module_path = repo_root / "tools" / "pai_runtime_runner" / "patch_proposal.py"
    test_path = repo_root / "tests" / "test_pai_runtime_patch_proposal.py"
    module_text = module_path.read_text(encoding="utf-8") if module_path.is_file() else ""
    test_file_text = test_path.read_text(encoding="utf-8") if test_path.is_file() else ""
    return (
        "You are Codex running as runtime provider codex under the PAI-owned runtime runner. "
        "PAI owns the run directory, patch proposal validation, repository mutation, and Memory/ISA/Pulse policy. "
        f"PAI_DIR is {str(pai_dir)!r}. "
        f"The actual adapter-development repository root is {str(repo_root)!r}. "
        f"The PAI-owned S15F run directory is {str(run_dir)!r}. "
        f"The installed router identity marker observed by the runtime runner is {MARKER!r}. "
        "Implement the bounded real repository task by proposing full-file replacements for the patch proposal "
        "module and tests. Do not directly edit repository files. Return a patch_proposal JSON object only; "
        "PAI will write patch-proposal.json, validate it against the approved write set, and apply it. "
        "Do not create repo root AGENTS.md, repo .codex, Codex native install surfaces, Memory writers, ISA writers, "
        "Pulse bridges, hooks, skills, agents, commands, or files outside the approved repository write set. "
        "Do not call localhost:31337 or probe Pulse. "
        "The proposal must use proposal_kind 'full-file-replacement' and changes with mode 'replace-file'. "
        "Each change must include path, content, and unified_diff metadata. "
        "Make a small real improvement in the target files: add an explicit PATCH_PROPOSAL_TEXT_ENCODING = 'utf-8' "
        "constant to tools/pai_runtime_runner/patch_proposal.py and add a unit test asserting that text encoding "
        "constant. Preserve the existing public functions load_patch_proposal, validate_patch_proposal, and "
        "materialize_patch_proposal, including the approved_write_set validation and path traversal protections. "
        f"The tests must pass with {test_text!r}. "
        "Return only JSON matching the provided schema. "
        f"Use milestone_name {S15F_REPO_MILESTONE!r}, run_id {S15F_REPO_RUN_ID!r}, runtime 'codex', "
        "runtime_status 'peer-beta', provider_type 'codex-cli', task_id 's15f-patch-proposal-repo-task', "
        "task_kind 'bounded-real-repository-code-change', adapter_identity_marker exactly as observed, "
        "adapter_status 'peer-beta', upstream_adapter 'claude', agents_router_observed true, "
        "pai_owned_run_directory true, patch_proposal_produced true, patch_proposal_validated false, "
        "patch_proposal_applied_by_pai false, tests_passed true, memory_write_performed false, "
        "isa_write_performed false, pulse_probe_performed false, localhost_31337_called false, "
        "and runtime_surface_created false. Set provider_registry_file_content and "
        "provider_registry_test_file_content to empty strings. Set repository_files_modified to the two "
        "repository target files. "
        "Use evidence_classification values including 'PAI-owned real repository task evidence', "
        "'patch proposal apply pipeline evidence', and 'not replacement readiness'. "
        "Do not include raw Memory, ISA, Pulse, backup, credential, or personal file contents. "
        f"Approved repository write set:\n{approved_lines}\n"
        f"Repository target files:\n{target_lines}\n"
        f"Current tools/pai_runtime_runner/patch_proposal.py:\n{module_text}\n"
        f"Current tests/test_pai_runtime_patch_proposal.py:\n{test_file_text}\n"
    )


def _repo_task_prompt(pai_dir: Path, task_card: dict[str, object], repo_root: Path, run_dir: Path) -> str:
    _, _, task_id = _repo_task_context(task_card)
    if task_id == S15F_REPO_TASK_ID:
        return _repo_task_prompt_s15f(pai_dir, task_card, repo_root, run_dir)
    return _repo_task_prompt_s15e(pai_dir, task_card, repo_root, run_dir)


def build_repo_provider_command(
    pai_dir: Path,
    task_card: dict[str, object],
    repo_root: Path,
    run_dir: Path,
    result_path: Path,
) -> list[str]:
    schema_path = pai_dir / "runtime-schemas" / "repo-run-result.schema.json"
    prompt = _repo_task_prompt(pai_dir, task_card, repo_root, run_dir)
    _, _, task_id = _repo_task_context(task_card)
    sandbox = "read-only" if task_id == S15F_REPO_TASK_ID else "workspace-write"
    return [
        "codex",
        "--ask-for-approval",
        "never",
        "exec",
        "--ephemeral",
        "--json",
        "--sandbox",
        sandbox,
        "--cd",
        str(repo_root),
        "--add-dir",
        str(run_dir),
        "--output-schema",
        str(schema_path),
        "-o",
        str(result_path),
        prompt,
    ]


def run_codex_repo_provider(
    pai_dir: Path,
    task_card: dict[str, object],
    repo_root: Path,
    run_dir: Path,
    dry_run: bool = False,
) -> dict[str, object]:
    result_path = run_dir / REPO_RUN_RESULT_NAME
    events_path = run_dir / REPO_EVENTS_NAME
    command = build_repo_provider_command(pai_dir, task_card, repo_root, run_dir, result_path)
    if dry_run:
        return {
            "dry_run": True,
            "provider_command": command,
            "repo_root": str(repo_root),
            "run_dir": str(run_dir),
            "result": str(result_path),
            "events_output": str(events_path),
        }

    result_path.parent.mkdir(parents=True, exist_ok=True)
    events_path.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    with events_path.open("w", encoding="utf-8") as events_file:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            stdin=subprocess.DEVNULL,
            stdout=events_file,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
    if completed.returncode != 0:
        raise CodexProviderError(f"Codex repo provider failed: {completed.stderr.strip()}")
    try:
        payload = json.loads(result_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CodexProviderError("Codex repo provider did not write valid JSON") from exc
    if not isinstance(payload, dict):
        raise CodexProviderError("Codex repo provider response must be a JSON object")
    payload["provider_command"] = command
    return payload


def _pai_context_prompt(task_card: dict[str, object], capsule: dict[str, object]) -> str:
    capsule_json = json.dumps(capsule, indent=2, sort_keys=True)
    return (
        "You are Codex running as runtime provider codex under the PAI-owned runtime runner. "
        "PAI owns live PAI state access, policy, validation, and run artifacts. "
        "You must reason only over the sanitized PAI context capsule included below. "
        "Do not browse, list, cat, grep, inspect, or otherwise traverse live PAI state, Claude product "
        "directories, Codex product directories, PAI Memory, ISA, Pulse, Claude project memory, Codex memory, "
        "product memory, or arbitrary home files. "
        "Do not call the Pulse local control endpoint and do not probe Pulse. "
        "Return only JSON matching the provided schema. "
        f"Use milestone_name {S15I_CONTEXT_MILESTONE!r}, run_id {S15I_CONTEXT_RUN_ID!r}, runtime 'codex', "
        "runtime_status 'peer-beta', provider_type 'codex-cli', task_id "
        f"{S15I_CONTEXT_TASK_ID!r}, task_kind 'readonly-pai-metadata-context', "
        f"adapter_identity_marker {MARKER!r}, upstream_adapter 'claude', agents_router_observed true, "
        "context_capsule_used true, context_capsule_metadata_only true, memory_body_read false, "
        "isa_body_read false, pulse_event_payload_read false, claude_project_memory_read false, "
        "codex_memory_read false, pulse_probe_performed false, localhost_31337_called false. "
        "Set pai_dir_label to '~/.claude/PAI'. Summarize only the provider/runtime metadata present in the capsule. "
        "Do not include raw Memory, ISA, Pulse, backup, credential, absolute personal path, or product memory contents. "
        f"Task card: {json.dumps(task_card, sort_keys=True)}\n"
        f"Sanitized PAI context capsule JSON:\n{capsule_json}\n"
    )


def build_pai_context_provider_command(
    pai_dir: Path,
    task_card: dict[str, object],
    capsule: dict[str, object],
    run_dir: Path,
    report_path: Path,
) -> list[str]:
    schema_path = run_dir / "pai-context-report.schema.json"
    prompt = _pai_context_prompt(task_card, capsule)
    return [
        "codex",
        "--ask-for-approval",
        "never",
        "exec",
        "--skip-git-repo-check",
        "--ephemeral",
        "--json",
        "--sandbox",
        "read-only",
        "--cd",
        str(run_dir),
        "--add-dir",
        str(run_dir),
        "--output-schema",
        str(schema_path),
        "-o",
        str(report_path),
        prompt,
    ]


def redact_pai_context_provider_command(command: list[str]) -> list[str]:
    redacted = list(command)
    if redacted:
        redacted[-1] = "[sanitized-pai-context-prompt]"
    return redacted


def run_codex_pai_context_provider(
    pai_dir: Path,
    task_card: dict[str, object],
    capsule: dict[str, object],
    run_dir: Path,
    dry_run: bool = False,
) -> dict[str, object]:
    report_path = run_dir / PAI_CONTEXT_REPORT_NAME
    events_path = run_dir / PAI_CONTEXT_EVENTS_NAME
    command = build_pai_context_provider_command(pai_dir, task_card, capsule, run_dir, report_path)
    if dry_run:
        return {
            "dry_run": True,
            "provider_command": redact_pai_context_provider_command(command),
            "run_dir": str(run_dir),
            "report": str(report_path),
            "events_output": str(events_path),
        }

    run_dir.mkdir(parents=True, exist_ok=True)
    with events_path.open("w", encoding="utf-8") as events_file:
        completed = subprocess.run(
            command,
            cwd=run_dir,
            stdin=subprocess.DEVNULL,
            stdout=events_file,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    if completed.returncode != 0:
        raise CodexProviderError(f"Codex PAI context provider failed: {completed.stderr.strip()}")
    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CodexProviderError("Codex PAI context provider did not write valid JSON") from exc
    if not isinstance(payload, dict):
        raise CodexProviderError("Codex PAI context provider response must be a JSON object")
    payload["provider_command"] = redact_pai_context_provider_command(command)
    return payload
