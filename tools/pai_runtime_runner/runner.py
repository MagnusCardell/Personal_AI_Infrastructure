from __future__ import annotations

import argparse
import difflib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except Exception:  # noqa: BLE001 - runner reports unavailable schema validation.
    Draft202012Validator = None  # type: ignore[assignment]

from tools.pai_runtime_runner.audit import audit_capability_policy as run_capability_policy_audit
from tools.pai_runtime_runner.audit import audit_pai_context_run as run_pai_context_audit
from tools.pai_runtime_runner.audit import audit_repo_run as run_repo_audit
from tools.pai_runtime_runner.audit import audit_provider_lifecycle as run_provider_lifecycle_audit
from tools.pai_runtime_runner.audit import audit_run as run_audit
from tools.pai_runtime_runner.capabilities import (
    CapabilityPolicyError,
    MATERIALIZED_REPO_TASK_CAPABILITIES,
    PAI_CONTEXT_TASK_CAPABILITIES,
    PATCH_PROPOSAL_REPO_TASK_CAPABILITIES,
    STATE_PROPOSAL_REVIEW_TASK_CAPABILITIES,
    STATE_PROPOSAL_TASK_CAPABILITIES,
    enforce_capability_policy,
    task_required_capabilities,
)
from tools.pai_runtime_runner.beta_readiness import (
    BetaReadinessError,
    S15J_RUN_RELATIVE,
    run_beta_readiness_gate,
)
from tools.pai_runtime_runner.pai_context import (
    PaiContextError,
    S15I_MILESTONE,
    S15I_RUN_ID,
    S15I_TASK_ID,
    S15I_TASK_KIND,
    collect_pai_context_metadata,
    normalize_context_report,
    validate_context_capsule,
)
from tools.pai_runtime_runner.state_proposal import (
    S16A_MILESTONE,
    S16A_RUN_ID,
    S16A_RUN_RELATIVE,
    S16A_TASK_ID,
    S16A_TASK_KIND,
    S16A_TASK_RELATIVE,
    STATE_CONTEXT_CAPSULE_NAME,
    STATE_PROPOSAL_EVENTS_NAME,
    STATE_PROPOSAL_NAME,
    STATE_PROPOSAL_SCHEMA_NAME,
    STATE_PROPOSAL_STATE_NAME,
    STATE_PROPOSAL_VALIDATION_NAME,
    StateProposalError,
    audit_state_proposal_run as run_state_proposal_audit,
    collect_state_context_metadata,
    normalize_state_proposal,
    validate_state_context_capsule,
    validate_state_proposal,
)
from tools.pai_runtime_runner.state_proposal_review import (
    REVIEW_CONTEXT_CAPSULE_NAME,
    S16B_MILESTONE,
    S16B_RUN_ID,
    S16B_RUN_RELATIVE,
    S16B_SOURCE_PROPOSAL_RELATIVE,
    S16B_TASK_ID,
    S16B_TASK_KIND,
    S16B_TASK_RELATIVE,
    STATE_PROPOSAL_DECISIONS_NAME,
    STATE_PROPOSAL_DECISIONS_SCHEMA_NAME,
    STATE_PROPOSAL_REVIEW_EVENTS_NAME,
    STATE_PROPOSAL_REVIEW_NAME,
    STATE_PROPOSAL_REVIEW_SCHEMA_NAME,
    STATE_PROPOSAL_REVIEW_STATE_NAME,
    STATE_PROPOSAL_REVIEW_VALIDATION_NAME,
    StateProposalReviewError,
    audit_state_proposal_review_run as run_state_proposal_review_audit,
    collect_review_context_metadata,
    load_source_state_proposal,
    normalize_state_proposal_decisions,
    normalize_state_proposal_review,
    validate_review_context_capsule,
)
from tools.pai_runtime_runner.patch_proposal import (
    PatchProposalError,
    load_patch_proposal,
    materialize_patch_proposal,
    validate_patch_proposal,
)
from tools.pai_runtime_runner.provider_registry import (
    ProviderRegistryError,
    discover_runtime_providers,
    doctor_provider_by_name,
    get_provider_by_name,
    summarize_provider_manifest,
    validate_provider_by_name,
)
from tools.pai_runtime_runner.providers.codex import (
    build_provider_command,
    build_repo_provider_command,
    run_codex_state_proposal_review_provider,
    run_codex_state_proposal_provider,
    run_codex_provider,
    run_codex_pai_context_provider,
    run_codex_repo_provider,
)


MILESTONE = "V5-S15D-PAI-RUNTIME-RUNNER-CODEX"
RUN_ID = "s15d-codex-synthetic-bugfix"
MARKER = "PAI_CODEX_PEER_BETA_ADAPTER"
RUN_RELATIVE = Path("runs") / "s15d" / "codex-synthetic-bugfix"
TASK_RELATIVE = Path("runtime-tasks") / "s15d-codex-synthetic-bugfix.json"
S15E_MILESTONE = "V5-S15E-PAI-RUNTIME-CODEX-REAL-REPO-TASK"
S15E_RUN_ID = "s15e-provider-registry"
S15E_TASK_ID = "s15e-provider-registry-repo-task"
S15E_RUN_RELATIVE = Path("runs") / "s15e" / "provider-registry"
S15E_TASK_RELATIVE = Path("runtime-tasks") / "s15e-provider-registry-repo-task.json"
S15E_RESULT_NAME = "repo-run-result.json"
S15E_EVENTS_NAME = "repo-events.jsonl"
S15E_DIFF_NAME = "repo-task.diff"
S15E_STATE_NAME = "repo-run-state.json"
S15E_VALIDATION_NAME = "repo-run-validation.json"
S15E_TARGET_FILES = {
    "tools/pai_runtime_runner/provider_registry.py",
    "tests/test_pai_runtime_provider_registry.py",
}
S15F_MILESTONE = "V5-S15F-PAI-RUNTIME-PATCH-PROPOSAL-APPLIER"
S15F_RUN_ID = "s15f-patch-proposal"
S15F_TASK_ID = "s15f-patch-proposal-repo-task"
S15F_RUN_RELATIVE = Path("runs") / "s15f" / "patch-proposal"
S15F_TASK_RELATIVE = Path("runtime-tasks") / "s15f-patch-proposal-repo-task.json"
S15F_PATCH_NAME = "patch-proposal.json"
S15I_RUN_RELATIVE = Path("runs") / "s15i" / "read-only-pai-context"
S15I_TASK_RELATIVE = Path("runtime-tasks") / "s15i-readonly-pai-context-task.json"
S15I_CAPSULE_NAME = "pai-context-capsule.json"
S15I_REPORT_NAME = "pai-context-report.json"
S15I_EVENTS_NAME = "pai-context-events.jsonl"
S15I_STATE_NAME = "pai-context-state.json"
S15I_VALIDATION_NAME = "pai-context-validation.json"
S15I_REQUIRED_CAPABILITY = "pai.context.read.metadata"
S15J_RESULT_NAME = "beta-readiness-result.json"
S15J_EVENTS_NAME = "beta-readiness-events.jsonl"
S15J_VALIDATION_NAME = "beta-readiness-validation.json"
S15J_EVIDENCE_INDEX_NAME = "evidence-index.json"
S15F_TARGET_FILES = {
    "tools/pai_runtime_runner/patch_proposal.py",
    "tests/test_pai_runtime_patch_proposal.py",
}
APPROVED_REPOSITORY_WRITE_SET = {
    "pai-runtime/README.md",
    "pai-runtime/repo-task.schema.json",
    "pai-runtime/repo-run-result.schema.json",
    "pai-runtime/repo-run-validation.schema.json",
    "pai-runtime/patch-proposal.schema.json",
    "pai-runtime/pai-context-task.schema.json",
    "pai-runtime/pai-context-capsule.schema.json",
    "pai-runtime/pai-context-report.schema.json",
    "pai-runtime/pai-context-validation.schema.json",
    "pai-runtime/tasks/s15f-patch-proposal-repo-task.json",
    "pai-runtime/tasks/s15i-readonly-pai-context-task.json",
    "pai-runtime/tasks/s15e-provider-registry-repo-task.json",
    "tools/pai_runtime_runner/__main__.py",
    "tools/pai_runtime_runner/runner.py",
    "tools/pai_runtime_runner/audit.py",
    "tools/pai_runtime_runner/install.py",
    "tools/pai_runtime_runner/provider_registry.py",
    "tools/pai_runtime_runner/patch_proposal.py",
    "tools/pai_runtime_runner/pai_context.py",
    "tools/pai_runtime_runner/capabilities.py",
    "tools/pai_runtime_runner/providers/codex.py",
    "tests/test_pai_runtime_runner_codex.py",
    "tests/test_pai_runtime_runner_repo_task.py",
    "tests/test_pai_runtime_provider_registry.py",
    "tests/test_pai_runtime_patch_proposal.py",
    "tests/test_pai_runtime_readonly_pai_context.py",
    "docs/architecture/V5-S15E-PAI-RUNTIME-CODEX-REAL-REPO-TASK.md",
    "docs/architecture/V5-S15F-PAI-RUNTIME-PATCH-PROPOSAL-APPLIER.md",
    "docs/architecture/V5-S15I-PAI-RUNTIME-READONLY-PAI-CONTEXT-TASK.md",
}
REPO_RUN_RESULT_FIELDS = {
    "milestone_name",
    "run_id",
    "runtime",
    "runtime_status",
    "provider_type",
    "pai_dir",
    "repo_root",
    "task_id",
    "task_kind",
    "adapter_identity_marker",
    "adapter_status",
    "upstream_adapter",
    "agents_router_observed",
    "pai_owned_run_directory",
    "repository_files_modified",
    "tests_run",
    "tests_passed",
    "memory_write_performed",
    "isa_write_performed",
    "pulse_probe_performed",
    "localhost_31337_called",
    "runtime_surface_created",
    "result_summary",
    "evidence_classification",
    "known_limits",
    "provider_registry_file_content",
    "provider_registry_test_file_content",
    "patch_proposal",
    "patch_proposal_produced",
    "patch_proposal_validated",
    "patch_proposal_applied_by_pai",
}


class RunnerError(ValueError):
    pass


def _is_within(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _resolve_pai_dir(value: str | Path) -> Path:
    if str(value) == "":
        raise RunnerError("--pai-dir must not be empty")
    path = Path(value)
    if any(part == ".." for part in path.parts):
        raise RunnerError("--pai-dir must not contain path traversal")
    resolved = path.resolve(strict=True)
    if not resolved.is_dir():
        raise RunnerError("--pai-dir must be a directory")
    return resolved


def _load_json(path: Path, label: str) -> dict[str, object]:
    if not path.is_file():
        raise RunnerError(f"{label} is missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RunnerError(f"{label} is not valid JSON") from exc
    if not isinstance(data, dict):
        raise RunnerError(f"{label} must be a JSON object")
    return data


def _validate_json_schema(instance: dict[str, object], schema_path: Path, label: str) -> list[str]:
    if Draft202012Validator is None:
        return [f"{label} schema validation unavailable: jsonschema is not installed"]
    if not schema_path.is_file():
        return [f"{label} schema is missing: {schema_path}"]
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{label} schema is not valid JSON: {exc}"]
    if not isinstance(schema, dict):
        return [f"{label} schema must be a JSON object"]
    try:
        Draft202012Validator.check_schema(schema)
        errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda error: list(error.path))
    except Exception as exc:  # noqa: BLE001 - runner reports schema failures instead of raising raw exceptions.
        return [f"{label} schema validation failed: {exc}"]
    return [
        f"{label} schema mismatch at {'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in errors
    ]


def _load_task_card(path: Path) -> dict[str, object]:
    card = _load_json(path, "task card")
    if card.get("runtime") != "codex":
        raise RunnerError("task card runtime must be codex")
    if card.get("task_kind") != "bounded-synthetic-code-repair":
        raise RunnerError("task card has unexpected task_kind")
    return card


def _enforce_runtime_capabilities(
    pai_dir: Path,
    runtime: str,
    task_card: dict[str, object],
    inferred: tuple[str, ...] = (),
) -> list[str]:
    manifest = get_provider_by_name(pai_dir, runtime)
    required = task_required_capabilities(task_card, inferred)
    enforce_capability_policy(manifest, required)
    return sorted(required)


def _safe_task_card(pai_dir: Path, task_card: str | Path) -> Path:
    path = Path(task_card)
    if str(task_card) == "":
        raise RunnerError("--task-card must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--task-card must not contain path traversal")
    resolved = path.resolve(strict=True)
    expected = (pai_dir / TASK_RELATIVE).resolve(strict=True)
    if resolved != expected:
        raise RunnerError("--task-card must be the installed S15D task card")
    return resolved


def _safe_run_dir(pai_dir: Path, run_dir: str | Path) -> Path:
    path = Path(run_dir)
    if str(run_dir) == "":
        raise RunnerError("--run-dir must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--run-dir must not contain path traversal")
    resolved = path.resolve(strict=False)
    expected = (pai_dir / RUN_RELATIVE).resolve(strict=False)
    if resolved != expected:
        raise RunnerError("PAI runtime run directory must be runs/s15d/codex-synthetic-bugfix")
    if path.exists() and not path.is_dir():
        raise RunnerError("--run-dir target is not a directory")
    if path.is_symlink():
        raise RunnerError("--run-dir target is a symlink")
    return path


def _safe_marker(marker: str | Path) -> Path:
    path = Path(marker)
    if str(marker) == "":
        raise RunnerError("--marker must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--marker must not contain path traversal")
    resolved = path.resolve(strict=True)
    if path.is_symlink():
        raise RunnerError("--marker must not be a symlink")
    return resolved


def _safe_audit_output(run_dir: Path, output: str | Path) -> Path:
    path = Path(output)
    if str(output) == "":
        raise RunnerError("--output must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--output must not contain path traversal")
    resolved = path.resolve(strict=False)
    if not _is_within(run_dir.resolve(strict=False), resolved):
        raise RunnerError("--output must stay under runs/s15d/codex-synthetic-bugfix")
    if resolved.name != "run-validation.json":
        raise RunnerError("--output must be named run-validation.json")
    if path.exists() and not path.is_file():
        raise RunnerError("--output target is not a file")
    if path.is_symlink():
        raise RunnerError("--output target is a symlink")
    return path


def _safe_provider_lifecycle_audit_output(pai_dir: Path, output: str | Path) -> Path:
    path = Path(output)
    if str(output) == "":
        raise RunnerError("--output must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--output must not contain path traversal")
    resolved = path.resolve(strict=False)
    run_root = (pai_dir / "runs" / "s15g" / "provider-lifecycle").resolve(strict=False)
    if not _is_within(run_root, resolved):
        raise RunnerError("--output must stay under runs/s15g/provider-lifecycle")
    if resolved.name != "provider-lifecycle-validation.json":
        raise RunnerError("--output must be named provider-lifecycle-validation.json")
    if path.exists() and not path.is_file():
        raise RunnerError("--output target is not a file")
    if path.is_symlink():
        raise RunnerError("--output target is a symlink")
    return path


def _safe_capability_policy_audit_output(pai_dir: Path, output: str | Path) -> Path:
    path = Path(output)
    if str(output) == "":
        raise RunnerError("--output must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--output must not contain path traversal")
    resolved = path.resolve(strict=False)
    run_root = (pai_dir / "runs" / "s15h" / "capability-policy").resolve(strict=False)
    if not _is_within(run_root, resolved):
        raise RunnerError("--output must stay under runs/s15h/capability-policy")
    if resolved.name != "capability-policy-validation.json":
        raise RunnerError("--output must be named capability-policy-validation.json")
    if path.exists() and not path.is_file():
        raise RunnerError("--output target is not a file")
    if path.is_symlink():
        raise RunnerError("--output target is a symlink")
    return path


def _safe_pai_context_task_card(pai_dir: Path, task_card: str | Path) -> Path:
    path = Path(task_card)
    if str(task_card) == "":
        raise RunnerError("--task-card must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--task-card must not contain path traversal")
    resolved = path.resolve(strict=True)
    expected = (pai_dir / S15I_TASK_RELATIVE).resolve(strict=True)
    if resolved != expected:
        raise RunnerError("--task-card must be the installed S15I PAI context task card")
    return resolved


def _safe_pai_context_run_dir(pai_dir: Path, run_dir: str | Path) -> Path:
    path = Path(run_dir)
    if str(run_dir) == "":
        raise RunnerError("--run-dir must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--run-dir must not contain path traversal")
    resolved = path.resolve(strict=False)
    expected = (pai_dir / S15I_RUN_RELATIVE).resolve(strict=False)
    if resolved != expected:
        raise RunnerError("PAI runtime PAI context run directory must be runs/s15i/read-only-pai-context")
    if path.exists() and not path.is_dir():
        raise RunnerError("--run-dir target is not a directory")
    if path.is_symlink():
        raise RunnerError("--run-dir target is a symlink")
    return path


def _safe_beta_readiness_run_dir(pai_dir: Path, run_dir: str | Path) -> Path:
    path = Path(run_dir)
    if str(run_dir) == "":
        raise RunnerError("--run-dir must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--run-dir must not contain path traversal")
    resolved = path.resolve(strict=False)
    expected = (pai_dir / S15J_RUN_RELATIVE).resolve(strict=False)
    if resolved != expected:
        raise RunnerError("S15J beta-readiness run directory must be runs/s15j/codex-beta-readiness")
    if path.exists() and not path.is_dir():
        raise RunnerError("--run-dir target is not a directory")
    if path.is_symlink():
        raise RunnerError("--run-dir target is a symlink")
    return path


def _safe_state_proposal_task_card(pai_dir: Path, task_card: str | Path) -> Path:
    path = Path(task_card)
    if str(task_card) == "":
        raise RunnerError("--task-card must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--task-card must not contain path traversal")
    resolved = path.resolve(strict=True)
    expected = (pai_dir / S16A_TASK_RELATIVE).resolve(strict=True)
    if resolved != expected:
        raise RunnerError("--task-card must be the installed S16A state proposal task card")
    return resolved


def _safe_state_proposal_run_dir(pai_dir: Path, run_dir: str | Path) -> Path:
    path = Path(run_dir)
    if str(run_dir) == "":
        raise RunnerError("--run-dir must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--run-dir must not contain path traversal")
    resolved = path.resolve(strict=False)
    expected = (pai_dir / S16A_RUN_RELATIVE).resolve(strict=False)
    if resolved != expected:
        raise RunnerError("S16A state proposal run directory must be runs/s16a/state-proposal")
    if path.exists() and not path.is_dir():
        raise RunnerError("--run-dir target is not a directory")
    if path.is_symlink():
        raise RunnerError("--run-dir target is a symlink")
    return path


def _safe_state_proposal_review_task_card(pai_dir: Path, task_card: str | Path) -> Path:
    path = Path(task_card)
    if str(task_card) == "":
        raise RunnerError("--task-card must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--task-card must not contain path traversal")
    resolved = path.resolve(strict=True)
    expected = (pai_dir / S16B_TASK_RELATIVE).resolve(strict=True)
    if resolved != expected:
        raise RunnerError("--task-card must be the installed S16B state proposal review task card")
    return resolved


def _safe_state_proposal_review_source(pai_dir: Path, source_proposal: str | Path) -> Path:
    path = Path(source_proposal)
    if str(source_proposal) == "":
        raise RunnerError("--source-proposal must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--source-proposal must not contain path traversal")
    resolved = path.resolve(strict=True)
    expected = (pai_dir / S16B_SOURCE_PROPOSAL_RELATIVE).resolve(strict=True)
    if resolved != expected:
        raise RunnerError("--source-proposal must be the accepted S16A state proposal artifact")
    if resolved.is_symlink():
        raise RunnerError("--source-proposal target is a symlink")
    return resolved


def _safe_state_proposal_review_run_dir(pai_dir: Path, run_dir: str | Path) -> Path:
    path = Path(run_dir)
    if str(run_dir) == "":
        raise RunnerError("--run-dir must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--run-dir must not contain path traversal")
    resolved = path.resolve(strict=False)
    expected = (pai_dir / S16B_RUN_RELATIVE).resolve(strict=False)
    if resolved != expected:
        raise RunnerError("S16B proposal review run directory must be runs/s16b/proposal-review")
    if path.exists() and not path.is_dir():
        raise RunnerError("--run-dir target is not a directory")
    if path.is_symlink():
        raise RunnerError("--run-dir target is a symlink")
    return path


def _safe_pai_context_audit_output(run_dir: Path, output: str | Path) -> Path:
    path = Path(output)
    if str(output) == "":
        raise RunnerError("--output must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--output must not contain path traversal")
    resolved = path.resolve(strict=False)
    if not _is_within(run_dir.resolve(strict=False), resolved):
        raise RunnerError("--output must stay under runs/s15i/read-only-pai-context")
    if resolved.name != S15I_VALIDATION_NAME:
        raise RunnerError("--output must be named pai-context-validation.json")
    if path.exists() and not path.is_file():
        raise RunnerError("--output target is not a file")
    if path.is_symlink():
        raise RunnerError("--output target is a symlink")
    return path


def _safe_state_proposal_audit_output(run_dir: Path, output: str | Path) -> Path:
    path = Path(output)
    if str(output) == "":
        raise RunnerError("--output must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--output must not contain path traversal")
    resolved = path.resolve(strict=False)
    if not _is_within(run_dir.resolve(strict=False), resolved):
        raise RunnerError("--output must stay under runs/s16a/state-proposal")
    if resolved.name != STATE_PROPOSAL_VALIDATION_NAME:
        raise RunnerError("--output must be named state-proposal-validation.json")
    if path.exists() and not path.is_file():
        raise RunnerError("--output target is not a file")
    if path.is_symlink():
        raise RunnerError("--output target is a symlink")
    return path


def _safe_state_proposal_review_audit_output(run_dir: Path, output: str | Path) -> Path:
    path = Path(output)
    if str(output) == "":
        raise RunnerError("--output must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--output must not contain path traversal")
    resolved = path.resolve(strict=False)
    if not _is_within(run_dir.resolve(strict=False), resolved):
        raise RunnerError("--output must stay under runs/s16b/proposal-review")
    if resolved.name != STATE_PROPOSAL_REVIEW_VALIDATION_NAME:
        raise RunnerError("--output must be named state-proposal-review-validation.json")
    if path.exists() and not path.is_file():
        raise RunnerError("--output target is not a file")
    if path.is_symlink():
        raise RunnerError("--output target is a symlink")
    return path


def _load_pai_context_task_card(path: Path) -> dict[str, object]:
    card = _load_json(path, "PAI context task card")
    expected = {
        "milestone_name": S15I_MILESTONE,
        "run_id": S15I_RUN_ID,
        "runtime": "codex",
        "task_id": S15I_TASK_ID,
        "task_kind": S15I_TASK_KIND,
    }
    for key, value in expected.items():
        if card.get(key) != value:
            raise RunnerError(f"PAI context task card mismatch for {key}")
    return card


def _validate_pai_context_task_card_schema(pai_dir: Path, card: dict[str, object]) -> None:
    schema_errors = _validate_json_schema(
        card,
        pai_dir / "runtime-schemas" / "pai-context-task.schema.json",
        "pai-context-task.json",
    )
    if schema_errors:
        raise RunnerError("PAI context task card schema validation failed: " + "; ".join(schema_errors))


def _load_state_proposal_task_card(path: Path) -> dict[str, object]:
    card = _load_json(path, "state proposal task card")
    expected = {
        "milestone_name": S16A_MILESTONE,
        "run_id": S16A_RUN_ID,
        "runtime": "codex",
        "task_id": S16A_TASK_ID,
        "task_kind": S16A_TASK_KIND,
        "proposal_only": True,
        "memory_writes_allowed": False,
        "isa_writes_allowed": False,
        "pulse_probe_allowed": False,
        "codex_direct_live_pai_traversal_allowed": False,
    }
    for key, value in expected.items():
        if card.get(key) != value:
            raise RunnerError(f"state proposal task card mismatch for {key}")
    return card


def _validate_state_proposal_task_card_schema(pai_dir: Path, card: dict[str, object]) -> None:
    schema_errors = _validate_json_schema(
        card,
        pai_dir / "runtime-schemas" / "state-proposal-task.schema.json",
        "state-proposal-task.json",
    )
    if schema_errors:
        raise RunnerError("state proposal task card schema validation failed: " + "; ".join(schema_errors))


def _load_state_proposal_review_task_card(path: Path) -> dict[str, object]:
    card = _load_json(path, "state proposal review task card")
    expected = {
        "milestone_name": S16B_MILESTONE,
        "run_id": S16B_RUN_ID,
        "runtime": "codex",
        "task_id": S16B_TASK_ID,
        "task_kind": S16B_TASK_KIND,
        "review_only": True,
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_writes_allowed": False,
        "isa_writes_allowed": False,
        "pulse_probe_allowed": False,
        "codex_direct_live_pai_traversal_allowed": False,
    }
    for key, value in expected.items():
        if card.get(key) != value:
            raise RunnerError(f"state proposal review task card mismatch for {key}")
    return card


def _validate_state_proposal_review_task_card_schema(pai_dir: Path, card: dict[str, object]) -> None:
    schema_errors = _validate_json_schema(
        card,
        pai_dir / "runtime-schemas" / "state-proposal-review-task.schema.json",
        "state-proposal-review-task.json",
    )
    if schema_errors:
        raise RunnerError("state proposal review task card schema validation failed: " + "; ".join(schema_errors))


def doctor(pai_dir: Path) -> dict[str, object]:
    router = pai_dir / "AGENTS.md"
    if not router.is_file():
        raise RunnerError("PAI_DIR/AGENTS.md is missing")
    router_text = router.read_text(encoding="utf-8")
    if MARKER not in router_text:
        raise RunnerError("PAI_DIR/AGENTS.md is missing PAI_CODEX_PEER_BETA_ADAPTER")

    provider_doctor = provider_lifecycle_doctor(pai_dir, "codex")
    if not provider_doctor.get("doctor_passed"):
        raise RunnerError("codex provider lifecycle doctor failed")
    for path, label in (
        (pai_dir / "bin" / "pai-runtime", "pai-runtime"),
        (pai_dir / "runtime-schemas" / "provider-manifest.schema.json", "provider manifest schema"),
        (pai_dir / "runtime-schemas" / "run-result.schema.json", "run result schema"),
        (pai_dir / "runtime-schemas" / "run-validation.schema.json", "run validation schema"),
        (pai_dir / "runtime-schemas" / "repo-task.schema.json", "repo task schema"),
        (pai_dir / "runtime-schemas" / "repo-run-result.schema.json", "repo run result schema"),
        (pai_dir / "runtime-schemas" / "repo-run-validation.schema.json", "repo run validation schema"),
        (pai_dir / "runtime-schemas" / "patch-proposal.schema.json", "patch proposal schema"),
        (pai_dir / "runtime-schemas" / "pai-context-task.schema.json", "PAI context task schema"),
        (pai_dir / "runtime-schemas" / "pai-context-capsule.schema.json", "PAI context capsule schema"),
        (pai_dir / "runtime-schemas" / "pai-context-report.schema.json", "PAI context report schema"),
        (pai_dir / "runtime-schemas" / "pai-context-validation.schema.json", "PAI context validation schema"),
        (pai_dir / "runtime-schemas" / "beta-readiness-result.schema.json", "S15J beta-readiness result schema"),
        (pai_dir / "runtime-schemas" / "beta-readiness-validation.schema.json", "S15J beta-readiness validation schema"),
        (pai_dir / "runtime-schemas" / "evidence-index.schema.json", "S15J evidence index schema"),
        (pai_dir / "runtime-schemas" / "state-proposal-task.schema.json", "S16A state proposal task schema"),
        (pai_dir / "runtime-schemas" / "state-context-capsule.schema.json", "S16A state context capsule schema"),
        (pai_dir / "runtime-schemas" / "state-proposal.schema.json", "S16A state proposal schema"),
        (pai_dir / "runtime-schemas" / "state-proposal-validation.schema.json", "S16A state proposal validation schema"),
        (pai_dir / "runtime-schemas" / "state-proposal-review-task.schema.json", "S16B state proposal review task schema"),
        (pai_dir / "runtime-schemas" / "state-proposal-review.schema.json", "S16B state proposal review schema"),
        (pai_dir / "runtime-schemas" / "state-proposal-decisions.schema.json", "S16B state proposal decisions schema"),
        (pai_dir / "runtime-schemas" / "state-proposal-review-validation.schema.json", "S16B state proposal review validation schema"),
        (pai_dir / TASK_RELATIVE, "S15D task card"),
        (pai_dir / S15E_TASK_RELATIVE, "S15E repo task card"),
        (pai_dir / S15F_TASK_RELATIVE, "S15F patch proposal repo task card"),
        (pai_dir / S15I_TASK_RELATIVE, "S15I PAI context task card"),
        (pai_dir / S16A_TASK_RELATIVE, "S16A state proposal task card"),
        (pai_dir / S16B_TASK_RELATIVE, "S16B state proposal review task card"),
        (pai_dir / "runtime-task-fixtures" / "s15d_bugfix" / "src" / "pai_priority.py", "S15D task fixture"),
        (pai_dir / "adapters" / "codex" / "bin" / "pai-codex", "Codex provider driver"),
    ):
        if not path.is_file():
            raise RunnerError(f"{label} is missing: {path}")
    return {
        "ok": True,
        "pai_dir": str(pai_dir),
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "adapter_identity_marker_observed": True,
        "provider_registry_used": True,
    }


def provider_lifecycle_list(pai_dir: Path) -> dict[str, object]:
    providers = discover_runtime_providers(pai_dir)
    return {
        "ok": True,
        "pai_dir": str(pai_dir),
        "providers": [summarize_provider_manifest(provider) for provider in providers],
        "provider_count": len(providers),
        "provider_registry_used": True,
    }


def provider_lifecycle_status(pai_dir: Path, runtime_name: str) -> dict[str, object]:
    provider = get_provider_by_name(pai_dir, runtime_name)
    return {
        "ok": True,
        "pai_dir": str(pai_dir),
        "runtime": runtime_name,
        "provider": summarize_provider_manifest(provider),
        "provider_registry_used": True,
    }


def provider_lifecycle_validate(pai_dir: Path, runtime_name: str) -> dict[str, object]:
    validation = validate_provider_by_name(pai_dir, runtime_name)
    if not validation.get("valid"):
        raise RunnerError(
            f"provider manifest validation failed for {runtime_name}: "
            + "; ".join(str(error) for error in validation.get("validation_errors", []))
        )
    return {
        "ok": True,
        "pai_dir": str(pai_dir),
        "runtime": runtime_name,
        "manifest_path": validation["manifest_path"],
        "provider": validation["provider"],
        "valid": True,
        "validation_errors": [],
        "provider_registry_used": True,
    }


def provider_lifecycle_doctor(pai_dir: Path, runtime_name: str) -> dict[str, object]:
    doctor_result = doctor_provider_by_name(pai_dir, runtime_name)
    if not doctor_result.get("doctor_passed"):
        raise RunnerError(
            f"provider lifecycle doctor failed for {runtime_name}: "
            + "; ".join(str(error) for error in doctor_result.get("validation_errors", []))
        )
    return {
        "ok": True,
        "pai_dir": str(pai_dir),
        "runtime": runtime_name,
        "manifest_path": doctor_result["manifest_path"],
        "provider": doctor_result["provider"],
        "driver_path": doctor_result["driver_path"],
        "valid": True,
        "doctor_passed": True,
        "validation_errors": [],
        "provider_registry_used": True,
    }


def run_runtime(
    pai_dir: Path,
    runtime: str,
    task_card: str | Path,
    run_dir: str | Path,
    dry_run: bool = False,
) -> dict[str, object]:
    # PAI owns the run; Codex is only runtime provider codex.
    doctor(pai_dir)
    if runtime != "codex":
        raise RunnerError(f"unknown runtime provider: {runtime}")
    task_path = _safe_task_card(pai_dir, task_card)
    card = _load_task_card(task_path)
    required_capabilities = _enforce_runtime_capabilities(pai_dir, "codex", card)
    safe_run_dir = _safe_run_dir(pai_dir, run_dir)
    command = [
        str(pai_dir / "bin" / "pai-runtime"),
        "run",
        "--pai-dir",
        str(pai_dir),
        "--runtime",
        "codex",
        "--task-card",
        str(task_path),
        "--run-dir",
        str(safe_run_dir),
    ]
    provider_command = build_provider_command(pai_dir, task_path, safe_run_dir)
    if dry_run:
        return {
            "dry_run": True,
            "pai_runtime_command": command,
            "provider_command": provider_command,
            "run_dir": str(safe_run_dir),
            "required_capabilities": required_capabilities,
        }
    safe_run_dir.mkdir(parents=True, exist_ok=True)
    provider_result = run_codex_provider(pai_dir, task_path, safe_run_dir)
    state_path = safe_run_dir / "run-state.json"
    state = _load_json(state_path, "run-state.json") if state_path.exists() else {}
    state["pai_runtime_command"] = command
    state["provider_command"] = provider_result.get("provider_command", provider_command)
    state["required_capabilities"] = required_capabilities
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    provider_result["pai_runtime_command"] = command
    provider_result["provider_command"] = state["provider_command"]
    provider_result["pai_owned_run_directory"] = str(safe_run_dir)
    return provider_result


def _safe_repo_task_card(pai_dir: Path, task_card: str | Path) -> Path:
    path = Path(task_card)
    if str(task_card) == "":
        raise RunnerError("--task-card must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--task-card must not contain path traversal")
    resolved = path.resolve(strict=True)
    expected = {
        (pai_dir / S15E_TASK_RELATIVE).resolve(strict=True),
        (pai_dir / S15F_TASK_RELATIVE).resolve(strict=True),
    }
    if resolved not in expected:
        raise RunnerError("--task-card must be an installed PAI repo task card")
    return resolved


def _safe_repo_run_dir(pai_dir: Path, run_dir: str | Path) -> Path:
    path = Path(run_dir)
    if str(run_dir) == "":
        raise RunnerError("--run-dir must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--run-dir must not contain path traversal")
    resolved = path.resolve(strict=False)
    expected = {
        (pai_dir / S15E_RUN_RELATIVE).resolve(strict=False),
        (pai_dir / S15F_RUN_RELATIVE).resolve(strict=False),
    }
    if resolved not in expected:
        raise RunnerError("PAI runtime repo run directory must be an approved repo run directory")
    if path.exists() and not path.is_dir():
        raise RunnerError("--run-dir target is not a directory")
    if path.is_symlink():
        raise RunnerError("--run-dir target is a symlink")
    return path


def _safe_repo_audit_output(run_dir: Path, output: str | Path) -> Path:
    path = Path(output)
    if str(output) == "":
        raise RunnerError("--output must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--output must not contain path traversal")
    resolved = path.resolve(strict=False)
    if not _is_within(run_dir.resolve(strict=False), resolved):
        raise RunnerError("--output must stay under the PAI repo run directory")
    if resolved.name != S15E_VALIDATION_NAME:
        raise RunnerError("--output must be named repo-run-validation.json")
    if path.exists() and not path.is_file():
        raise RunnerError("--output target is not a file")
    if path.is_symlink():
        raise RunnerError("--output target is a symlink")
    return path


def _safe_repo_root(repo_root: str | Path) -> Path:
    path = Path(repo_root)
    if str(repo_root) == "":
        raise RunnerError("--repo-root must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--repo-root must not contain path traversal")
    resolved = path.resolve(strict=True)
    if not resolved.is_dir():
        raise RunnerError("--repo-root must be a directory")
    if path.is_symlink():
        raise RunnerError("--repo-root must not be a symlink")
    try:
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=resolved,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.strip()
    except subprocess.CalledProcessError as exc:
        raise RunnerError("--repo-root must be inside a git worktree") from exc
    if Path(top).resolve(strict=True) != resolved:
        raise RunnerError("--repo-root must be the git worktree root")
    return resolved


def _repo_task_profile(card: dict[str, object]) -> dict[str, object]:
    if card.get("milestone_name") == S15F_MILESTONE and card.get("task_id") == S15F_TASK_ID:
        return {
            "label": "S15F",
            "milestone_name": S15F_MILESTONE,
            "run_id": S15F_RUN_ID,
            "task_id": S15F_TASK_ID,
            "required_targets": S15F_TARGET_FILES,
            "uses_patch_proposal": True,
        }
    if card.get("milestone_name") == S15E_MILESTONE and card.get("task_id") == S15E_TASK_ID:
        return {
            "label": "S15E",
            "milestone_name": S15E_MILESTONE,
            "run_id": S15E_RUN_ID,
            "task_id": S15E_TASK_ID,
            "required_targets": S15E_TARGET_FILES,
            "uses_patch_proposal": False,
        }
    raise RunnerError("repo task card has unexpected milestone_name or task_id")


def _load_repo_task_card(path: Path) -> dict[str, object]:
    card = _load_json(path, "repo task card")
    _repo_task_profile(card)
    if card.get("task_kind") != "bounded-real-repository-code-change":
        raise RunnerError("repo task card has unexpected task_kind")
    if card.get("runtime") != "codex":
        raise RunnerError("repo task card runtime must be codex")
    return card


def _repo_task_capabilities(profile: dict[str, object]) -> tuple[str, ...]:
    return PATCH_PROPOSAL_REPO_TASK_CAPABILITIES if profile["uses_patch_proposal"] else MATERIALIZED_REPO_TASK_CAPABILITIES


def _approved_repository_write_set(card: dict[str, object]) -> set[str]:
    raw = card.get("approved_repository_write_set")
    if not isinstance(raw, list) or not raw or not all(isinstance(item, str) for item in raw):
        raise RunnerError("repo task card approved_repository_write_set is invalid")
    approved = set(raw)
    for item in approved:
        path = Path(item)
        if path.is_absolute() or any(part == ".." for part in path.parts):
            raise RunnerError(f"approved repository path is unsafe: {item}")
    unexpected = approved - APPROVED_REPOSITORY_WRITE_SET
    if unexpected:
        raise RunnerError(f"repo task card includes unapproved repository paths: {sorted(unexpected)}")
    profile = _repo_task_profile(card)
    required_targets = profile["required_targets"]
    if not isinstance(required_targets, set) or not required_targets.issubset(approved):
        raise RunnerError(f"{profile['label']} task card does not include required target files")
    return approved


def _repository_target_files(card: dict[str, object], approved: set[str]) -> set[str]:
    raw = card.get("repository_target_files")
    if not isinstance(raw, list) or not raw or not all(isinstance(item, str) for item in raw):
        raise RunnerError("repo task card repository_target_files is invalid")
    targets = set(raw)
    profile = _repo_task_profile(card)
    required_targets = profile["required_targets"]
    if not isinstance(required_targets, set) or not required_targets.issubset(targets):
        raise RunnerError(f"{profile['label']} repo task card does not target required files")
    if not targets.issubset(approved):
        raise RunnerError("repo task card targets paths outside approved write set")
    return targets


def _repo_test_command(card: dict[str, object]) -> list[str]:
    raw = card.get("test_command")
    if not isinstance(raw, list) or not raw or not all(isinstance(item, str) for item in raw):
        raise RunnerError("repo task card test_command is invalid")
    return list(raw)


def _snapshot_repository_files(repo_root: Path, paths: set[str]) -> dict[str, str | None]:
    snapshot: dict[str, str | None] = {}
    for relative in sorted(paths):
        path = repo_root / relative
        if path.is_file():
            snapshot[relative] = path.read_text(encoding="utf-8")
        else:
            snapshot[relative] = None
    return snapshot


def _write_repository_diff(before: dict[str, str | None], repo_root: Path, diff_path: Path) -> list[str]:
    modified: list[str] = []
    diff_lines: list[str] = []
    for relative, old in sorted(before.items()):
        path = repo_root / relative
        new = path.read_text(encoding="utf-8") if path.is_file() else None
        if old == new:
            continue
        modified.append(relative)
        old_lines = [] if old is None else old.splitlines(keepends=True)
        new_lines = [] if new is None else new.splitlines(keepends=True)
        diff_lines.extend(
            difflib.unified_diff(
                old_lines,
                new_lines,
                fromfile=f"a/{relative}",
                tofile=f"b/{relative}",
            )
        )
    diff_path.write_text("".join(diff_lines), encoding="utf-8")
    return modified


def _apply_materialized_repo_changes(repo_root: Path, result: dict[str, object]) -> None:
    replacements = {
        "tools/pai_runtime_runner/provider_registry.py": result.get("provider_registry_file_content"),
        "tests/test_pai_runtime_provider_registry.py": result.get("provider_registry_test_file_content"),
    }
    for relative, content in replacements.items():
        if not isinstance(content, str) or content == "":
            continue
        path = Path(relative)
        if path.is_absolute() or any(part == ".." for part in path.parts):
            raise RunnerError(f"S15E materialized replacement path is unsafe: {relative}")
        target = (repo_root / path).resolve(strict=False)
        if not _is_within(repo_root.resolve(strict=True), target):
            raise RunnerError(f"S15E materialized replacement escapes repository: {relative}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def _write_provider_patch_proposal(result: dict[str, object], proposal_path: Path) -> dict[str, object]:
    raw = result.get("patch_proposal")
    if isinstance(raw, dict):
        proposal_path.parent.mkdir(parents=True, exist_ok=True)
        proposal_path.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return raw
    if proposal_path.is_file():
        return load_patch_proposal(proposal_path)
    raise RunnerError("S15F Codex repo provider did not produce patch_proposal")


def _run_repo_tests(repo_root: Path, command: list[str]) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        command,
        cwd=repo_root,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )


def _normalize_repo_run_result(
    *,
    result: dict[str, object],
    pai_dir: Path,
    repo_root: Path,
    run_dir: Path,
    card: dict[str, object],
    modified: list[str],
    test_command: list[str],
    tests_passed: bool,
    patch_proposal_produced: bool = False,
    patch_proposal_validated: bool = False,
    patch_proposal_applied_by_pai: bool = False,
) -> dict[str, object]:
    profile = _repo_task_profile(card)
    normalized = {key: result[key] for key in REPO_RUN_RESULT_FIELDS if key in result}
    normalized.update(
        {
            "milestone_name": profile["milestone_name"],
            "run_id": profile["run_id"],
            "runtime": "codex",
            "runtime_status": "peer-beta",
            "provider_type": "codex-cli",
            "pai_dir": str(pai_dir),
            "repo_root": str(repo_root),
            "task_id": profile["task_id"],
            "task_kind": "bounded-real-repository-code-change",
            "adapter_identity_marker": MARKER,
            "adapter_status": "peer-beta",
            "upstream_adapter": "claude",
            "agents_router_observed": True,
            "pai_owned_run_directory": True,
            "repository_files_modified": sorted(modified),
            "tests_run": [" ".join(test_command)],
            "tests_passed": tests_passed,
            "memory_write_performed": False,
            "isa_write_performed": False,
            "pulse_probe_performed": False,
            "localhost_31337_called": False,
            "runtime_surface_created": False,
            "result_summary": str(
                result.get("result_summary")
                or (
                    "Implemented and validated the PAI-owned patch proposal pipeline through a bounded real repository task."
                    if profile["uses_patch_proposal"]
                    else "Implemented and validated the PAI runtime provider registry through a bounded real repository task."
                )
            ),
            "evidence_classification": result.get("evidence_classification")
            if isinstance(result.get("evidence_classification"), list)
            else [
                "PAI-owned real repository task evidence",
                "patch proposal apply pipeline evidence"
                if profile["uses_patch_proposal"]
                else "runtime provider registry evidence",
                "not replacement readiness",
            ],
            "known_limits": result.get("known_limits")
            if isinstance(result.get("known_limits"), list)
            else [
                f"{profile['label']} is a bounded real repository task, not Codex replacement readiness.",
                "Memory, ISA, and Pulse writes remain disabled for runtime=codex.",
            ],
        }
    )
    if profile["uses_patch_proposal"]:
        normalized.update(
            {
                "patch_proposal_produced": patch_proposal_produced,
                "patch_proposal_validated": patch_proposal_validated,
                "patch_proposal_applied_by_pai": patch_proposal_applied_by_pai,
            }
        )
    if card.get("task_id") != normalized["task_id"]:
        raise RunnerError(f"{profile['label']} normalized result task_id mismatch")
    return normalized


def run_repo_runtime(
    pai_dir: Path,
    runtime: str,
    task_card: str | Path,
    repo_root: str | Path,
    run_dir: str | Path,
    dry_run: bool = False,
) -> dict[str, object]:
    doctor(pai_dir)
    if runtime != "codex":
        raise RunnerError(f"unknown runtime provider: {runtime}")
    task_path = _safe_repo_task_card(pai_dir, task_card)
    card = _load_repo_task_card(task_path)
    profile = _repo_task_profile(card)
    required_capabilities = _enforce_runtime_capabilities(pai_dir, "codex", card, _repo_task_capabilities(profile))
    safe_repo_root = _safe_repo_root(repo_root)
    safe_run_dir = _safe_repo_run_dir(pai_dir, run_dir)
    approved_repository_write_set = _approved_repository_write_set(card)
    targets = _repository_target_files(card, approved_repository_write_set)
    test_command = _repo_test_command(card)
    command = [
        str(pai_dir / "bin" / "pai-runtime"),
        "run-repo",
        "--pai-dir",
        str(pai_dir),
        "--runtime",
        "codex",
        "--task-card",
        str(task_path),
        "--repo-root",
        str(safe_repo_root),
        "--run-dir",
        str(safe_run_dir),
    ]
    provider_command = build_repo_provider_command(
        pai_dir,
        card,
        safe_repo_root,
        safe_run_dir,
        safe_run_dir / S15E_RESULT_NAME,
    )
    if dry_run:
        return {
            "dry_run": True,
            "pai_runtime_command": command,
            "provider_command": provider_command,
            "repo_root": str(safe_repo_root),
            "run_dir": str(safe_run_dir),
            "approved_repository_write_set": sorted(approved_repository_write_set),
            "required_capabilities": required_capabilities,
        }

    safe_run_dir.mkdir(parents=True, exist_ok=True)
    before = _snapshot_repository_files(safe_repo_root, approved_repository_write_set)
    provider_result = run_codex_repo_provider(pai_dir, card, safe_repo_root, safe_run_dir)
    patch_proposal_produced = False
    patch_proposal_validated = False
    patch_proposal_applied_by_pai = False
    patch_proposal_validation_errors: list[str] = []
    patch_proposal_applied_paths: list[str] = []
    if profile["uses_patch_proposal"]:
        proposal_path = safe_run_dir / S15F_PATCH_NAME
        proposal = _write_provider_patch_proposal(provider_result, proposal_path)
        patch_proposal_produced = True
        patch_proposal_validation_errors = validate_patch_proposal(proposal, approved_repository_write_set)
        if patch_proposal_validation_errors:
            raise RunnerError("S15F patch proposal validation failed: " + "; ".join(patch_proposal_validation_errors))
        patch_proposal_validated = True
        try:
            patch_proposal_applied_paths = materialize_patch_proposal(
                proposal,
                safe_repo_root,
                approved_repository_write_set,
            )
        except PatchProposalError as exc:
            raise RunnerError(f"S15F patch proposal apply failed: {exc}") from exc
        patch_proposal_applied_by_pai = True
    else:
        _apply_materialized_repo_changes(safe_repo_root, provider_result)
    modified = _write_repository_diff(before, safe_repo_root, safe_run_dir / S15E_DIFF_NAME)
    tests = _run_repo_tests(safe_repo_root, test_command)
    tests_passed = tests.returncode == 0
    state = {
        "pai_runtime_command": command,
        "provider_command": provider_result.get("provider_command", provider_command),
        "approved_repository_write_set": sorted(approved_repository_write_set),
        "required_capabilities": required_capabilities,
        "repository_target_files": sorted(targets),
        "repository_files_modified": sorted(modified),
        "patch_proposal_path": str(safe_run_dir / S15F_PATCH_NAME) if profile["uses_patch_proposal"] else "",
        "patch_proposal_produced": patch_proposal_produced,
        "patch_proposal_validated": patch_proposal_validated,
        "patch_proposal_validation_errors": patch_proposal_validation_errors,
        "patch_proposal_applied_by_pai": patch_proposal_applied_by_pai,
        "patch_proposal_applied_paths": sorted(patch_proposal_applied_paths),
        "patch_proposal_tests_returncode": tests.returncode if profile["uses_patch_proposal"] else None,
        "patch_proposal_tests_stdout": tests.stdout if profile["uses_patch_proposal"] else "",
        "patch_proposal_tests_stderr": tests.stderr if profile["uses_patch_proposal"] else "",
        "provider_registry_tests_returncode": tests.returncode,
        "provider_registry_tests_stdout": tests.stdout,
        "provider_registry_tests_stderr": tests.stderr,
        "repo_root": str(safe_repo_root),
    }
    (safe_run_dir / S15E_STATE_NAME).write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result_path = safe_run_dir / S15E_RESULT_NAME
    result = _load_json(result_path, S15E_RESULT_NAME)
    normalized = _normalize_repo_run_result(
        result=result,
        pai_dir=pai_dir,
        repo_root=safe_repo_root,
        run_dir=safe_run_dir,
        card=card,
        modified=modified,
        test_command=test_command,
        tests_passed=tests_passed,
        patch_proposal_produced=patch_proposal_produced,
        patch_proposal_validated=patch_proposal_validated,
        patch_proposal_applied_by_pai=patch_proposal_applied_by_pai,
    )
    result_path.write_text(json.dumps(normalized, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not tests_passed:
        raise RunnerError(f"{profile['label']} repository tests did not pass after Codex repo task")
    if not modified:
        raise RunnerError(f"{profile['label']} repo task did not produce a repository diff")
    required_targets = profile["required_targets"]
    if not isinstance(required_targets, set) or not required_targets.issubset(set(modified)):
        raise RunnerError(f"{profile['label']} repo task did not modify required target files")
    return {
        "ok": True,
        "repo_root": str(safe_repo_root),
        "run_dir": str(safe_run_dir),
        "result": str(result_path),
        "events_output": str(safe_run_dir / S15E_EVENTS_NAME),
        "diff": str(safe_run_dir / S15E_DIFF_NAME),
        "patch_proposal": str(safe_run_dir / S15F_PATCH_NAME) if profile["uses_patch_proposal"] else "",
        "patch_proposal_produced": patch_proposal_produced,
        "patch_proposal_validated": patch_proposal_validated,
        "patch_proposal_applied_by_pai": patch_proposal_applied_by_pai,
        "repository_files_modified": sorted(modified),
        "provider_registry_tests_passed": tests_passed if not profile["uses_patch_proposal"] else False,
        "patch_proposal_tests_passed": tests_passed if profile["uses_patch_proposal"] else False,
    }


def run_pai_context_runtime(
    pai_dir: Path,
    runtime: str,
    task_card: str | Path,
    run_dir: str | Path,
    dry_run: bool = False,
) -> dict[str, object]:
    doctor(pai_dir)
    if runtime != "codex":
        raise RunnerError(f"unknown runtime provider: {runtime}")
    task_path = _safe_pai_context_task_card(pai_dir, task_card)
    card = _load_pai_context_task_card(task_path)
    _validate_pai_context_task_card_schema(pai_dir, card)
    required_capabilities = _enforce_runtime_capabilities(
        pai_dir,
        "codex",
        card,
        PAI_CONTEXT_TASK_CAPABILITIES,
    )
    safe_run_dir = _safe_pai_context_run_dir(pai_dir, run_dir)
    command = [
        str(pai_dir / "bin" / "pai-runtime"),
        "run-pai-context",
        "--pai-dir",
        str(pai_dir),
        "--runtime",
        "codex",
        "--task-card",
        str(task_path),
        "--run-dir",
        str(safe_run_dir),
    ]
    capsule = collect_pai_context_metadata(pai_dir)
    capsule_errors = validate_context_capsule(capsule)
    if capsule_errors:
        raise RunnerError("PAI context capsule validation failed: " + "; ".join(capsule_errors))
    capsule_schema_errors = _validate_json_schema(
        capsule,
        pai_dir / "runtime-schemas" / "pai-context-capsule.schema.json",
        "pai-context-capsule.json",
    )
    if capsule_schema_errors:
        raise RunnerError("PAI context capsule schema validation failed: " + "; ".join(capsule_schema_errors))
    dry_provider_result = run_codex_pai_context_provider(pai_dir, card, capsule, safe_run_dir, dry_run=True)
    if dry_run:
        return {
            "dry_run": True,
            "pai_runtime_command": command,
            "provider_command": dry_provider_result["provider_command"],
            "run_dir": str(safe_run_dir),
            "required_capabilities": required_capabilities,
            "context_capsule_metadata_only": True,
        }

    safe_run_dir.mkdir(parents=True, exist_ok=True)
    capsule_path = safe_run_dir / S15I_CAPSULE_NAME
    capsule_path.write_text(json.dumps(capsule, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    schema_source = pai_dir / "runtime-schemas" / "pai-context-report.schema.json"
    schema_target = safe_run_dir / "pai-context-report.schema.json"
    schema_target.write_text(schema_source.read_text(encoding="utf-8"), encoding="utf-8")

    provider_result = run_codex_pai_context_provider(pai_dir, card, capsule, safe_run_dir)
    report = normalize_context_report(provider_result, capsule)
    report_schema_errors = _validate_json_schema(report, schema_target, "pai-context-report.json")
    if report_schema_errors:
        raise RunnerError("PAI context report schema validation failed: " + "; ".join(report_schema_errors))
    report_path = safe_run_dir / S15I_REPORT_NAME
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    state = {
        "pai_runtime_command": command,
        "provider_command": provider_result.get("provider_command", dry_provider_result["provider_command"]),
        "required_capabilities": required_capabilities,
        "context_capsule_path": str(capsule_path),
        "context_report_path": str(report_path),
        "context_events_path": str(safe_run_dir / S15I_EVENTS_NAME),
        "context_capsule_metadata_only": True,
        "context_report_normalized_by_pai": True,
    }
    (safe_run_dir / S15I_STATE_NAME).write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "ok": True,
        "run_dir": str(safe_run_dir),
        "context_capsule": str(capsule_path),
        "context_report": str(report_path),
        "events_output": str(safe_run_dir / S15I_EVENTS_NAME),
        "required_capabilities": required_capabilities,
        "context_capsule_metadata_only": True,
    }


def propose_state_runtime(
    pai_dir: Path,
    runtime: str,
    task_card: str | Path,
    run_dir: str | Path,
    dry_run: bool = False,
) -> dict[str, object]:
    doctor(pai_dir)
    if runtime != "codex":
        raise RunnerError(f"unknown runtime provider: {runtime}")
    task_path = _safe_state_proposal_task_card(pai_dir, task_card)
    card = _load_state_proposal_task_card(task_path)
    _validate_state_proposal_task_card_schema(pai_dir, card)
    required_capabilities = _enforce_runtime_capabilities(
        pai_dir,
        "codex",
        card,
        STATE_PROPOSAL_TASK_CAPABILITIES,
    )
    safe_run_dir = _safe_state_proposal_run_dir(pai_dir, run_dir)
    command = [
        str(pai_dir / "bin" / "pai-runtime"),
        "propose-state",
        "--pai-dir",
        str(pai_dir),
        "--runtime",
        "codex",
        "--task-card",
        str(task_path),
        "--run-dir",
        str(safe_run_dir),
    ]
    capsule = collect_state_context_metadata(pai_dir)
    capsule_errors = validate_state_context_capsule(capsule)
    if capsule_errors:
        raise RunnerError("state context capsule validation failed: " + "; ".join(capsule_errors))
    capsule_schema_errors = _validate_json_schema(
        capsule,
        pai_dir / "runtime-schemas" / "state-context-capsule.schema.json",
        STATE_CONTEXT_CAPSULE_NAME,
    )
    if capsule_schema_errors:
        raise RunnerError("state context capsule schema validation failed: " + "; ".join(capsule_schema_errors))
    dry_provider_result = run_codex_state_proposal_provider(pai_dir, card, capsule, safe_run_dir, dry_run=True)
    if dry_run:
        return {
            "dry_run": True,
            "pai_runtime_command": command,
            "provider_command": dry_provider_result["provider_command"],
            "run_dir": str(safe_run_dir),
            "required_capabilities": required_capabilities,
            "state_context_capsule_metadata_only": True,
        }

    safe_run_dir.mkdir(parents=True, exist_ok=True)
    capsule_path = safe_run_dir / STATE_CONTEXT_CAPSULE_NAME
    capsule_path.write_text(json.dumps(capsule, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    schema_source = pai_dir / "runtime-schemas" / "state-proposal.schema.json"
    schema_target = safe_run_dir / STATE_PROPOSAL_SCHEMA_NAME
    schema_target.write_text(schema_source.read_text(encoding="utf-8"), encoding="utf-8")

    provider_result = run_codex_state_proposal_provider(pai_dir, card, capsule, safe_run_dir)
    proposal = normalize_state_proposal(provider_result, capsule)
    proposal_schema_errors = _validate_json_schema(proposal, schema_target, STATE_PROPOSAL_NAME)
    if proposal_schema_errors:
        raise RunnerError("state proposal schema validation failed: " + "; ".join(proposal_schema_errors))
    proposal_path = safe_run_dir / STATE_PROPOSAL_NAME
    proposal_path.write_text(json.dumps(proposal, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    state = {
        "pai_runtime_command": command,
        "provider_command": provider_result.get("provider_command", dry_provider_result["provider_command"]),
        "required_capabilities": required_capabilities,
        "state_context_capsule_path": str(capsule_path),
        "state_proposal_path": str(proposal_path),
        "state_proposal_events_path": str(safe_run_dir / STATE_PROPOSAL_EVENTS_NAME),
        "state_context_capsule_metadata_only": True,
        "state_proposal_normalized_by_pai": True,
        "proposal_only": True,
    }
    (safe_run_dir / STATE_PROPOSAL_STATE_NAME).write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "ok": True,
        "run_dir": str(safe_run_dir),
        "state_context_capsule": str(capsule_path),
        "state_proposal": str(proposal_path),
        "events_output": str(safe_run_dir / STATE_PROPOSAL_EVENTS_NAME),
        "required_capabilities": required_capabilities,
        "state_context_capsule_metadata_only": True,
        "proposal_only": True,
    }


def review_state_proposal_runtime(
    pai_dir: Path,
    runtime: str,
    task_card: str | Path,
    source_proposal: str | Path,
    run_dir: str | Path,
    dry_run: bool = False,
) -> dict[str, object]:
    doctor(pai_dir)
    if runtime != "codex":
        raise RunnerError(f"unknown runtime provider: {runtime}")
    task_path = _safe_state_proposal_review_task_card(pai_dir, task_card)
    source_path = _safe_state_proposal_review_source(pai_dir, source_proposal)
    card = _load_state_proposal_review_task_card(task_path)
    _validate_state_proposal_review_task_card_schema(pai_dir, card)
    required_capabilities = _enforce_runtime_capabilities(
        pai_dir,
        "codex",
        card,
        STATE_PROPOSAL_REVIEW_TASK_CAPABILITIES,
    )
    safe_run_dir = _safe_state_proposal_review_run_dir(pai_dir, run_dir)
    command = [
        str(pai_dir / "bin" / "pai-runtime"),
        "review-state-proposal",
        "--pai-dir",
        str(pai_dir),
        "--runtime",
        "codex",
        "--task-card",
        str(task_path),
        "--source-proposal",
        str(source_path),
        "--run-dir",
        str(safe_run_dir),
    ]
    source = load_source_state_proposal(source_path)
    source_schema_errors = _validate_json_schema(
        source,
        pai_dir / "runtime-schemas" / "state-proposal.schema.json",
        STATE_PROPOSAL_NAME,
    )
    if source_schema_errors:
        raise RunnerError("source S16A proposal schema validation failed: " + "; ".join(source_schema_errors))

    capsule = collect_review_context_metadata(pai_dir, source)
    capsule_errors = validate_review_context_capsule(capsule)
    if capsule_errors:
        raise RunnerError("review context capsule validation failed: " + "; ".join(capsule_errors))
    dry_provider_result = run_codex_state_proposal_review_provider(
        pai_dir,
        card,
        capsule,
        source,
        safe_run_dir,
        dry_run=True,
    )
    if dry_run:
        return {
            "dry_run": True,
            "pai_runtime_command": command,
            "provider_command": dry_provider_result["provider_command"],
            "run_dir": str(safe_run_dir),
            "required_capabilities": required_capabilities,
            "review_context_capsule_metadata_only": True,
            "source_proposal": str(source_path),
        }

    safe_run_dir.mkdir(parents=True, exist_ok=True)
    capsule_path = safe_run_dir / REVIEW_CONTEXT_CAPSULE_NAME
    capsule_path.write_text(json.dumps(capsule, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    review_schema_source = pai_dir / "runtime-schemas" / "state-proposal-review.schema.json"
    review_schema_target = safe_run_dir / STATE_PROPOSAL_REVIEW_SCHEMA_NAME
    review_schema_target.write_text(review_schema_source.read_text(encoding="utf-8"), encoding="utf-8")
    decisions_schema_source = pai_dir / "runtime-schemas" / "state-proposal-decisions.schema.json"
    decisions_schema_target = safe_run_dir / STATE_PROPOSAL_DECISIONS_SCHEMA_NAME
    decisions_schema_target.write_text(decisions_schema_source.read_text(encoding="utf-8"), encoding="utf-8")

    provider_result = run_codex_state_proposal_review_provider(pai_dir, card, capsule, source, safe_run_dir)
    review = normalize_state_proposal_review(provider_result, source, capsule)
    review_schema_errors = _validate_json_schema(review, review_schema_target, STATE_PROPOSAL_REVIEW_NAME)
    if review_schema_errors:
        raise RunnerError("state proposal review schema validation failed: " + "; ".join(review_schema_errors))
    review_path = safe_run_dir / STATE_PROPOSAL_REVIEW_NAME
    review_path.write_text(json.dumps(review, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    decisions = normalize_state_proposal_decisions(review)
    decisions_schema_errors = _validate_json_schema(decisions, decisions_schema_target, STATE_PROPOSAL_DECISIONS_NAME)
    if decisions_schema_errors:
        raise RunnerError("state proposal decisions schema validation failed: " + "; ".join(decisions_schema_errors))
    decisions_path = safe_run_dir / STATE_PROPOSAL_DECISIONS_NAME
    decisions_path.write_text(json.dumps(decisions, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    state = {
        "pai_runtime_command": command,
        "provider_command": provider_result.get("provider_command", dry_provider_result["provider_command"]),
        "required_capabilities": required_capabilities,
        "source_proposal_path": str(source_path),
        "review_context_capsule_path": str(capsule_path),
        "state_proposal_review_path": str(review_path),
        "state_proposal_decisions_path": str(decisions_path),
        "state_proposal_review_events_path": str(safe_run_dir / STATE_PROPOSAL_REVIEW_EVENTS_NAME),
        "review_context_capsule_metadata_only": True,
        "state_proposal_review_normalized_by_pai": True,
        "state_proposal_decisions_authority": "pai-policy",
        "commit_authority_granted": False,
        "commit_performed": False,
    }
    (safe_run_dir / STATE_PROPOSAL_REVIEW_STATE_NAME).write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "ok": True,
        "run_dir": str(safe_run_dir),
        "source_proposal": str(source_path),
        "review_context_capsule": str(capsule_path),
        "state_proposal_review": str(review_path),
        "state_proposal_decisions": str(decisions_path),
        "events_output": str(safe_run_dir / STATE_PROPOSAL_REVIEW_EVENTS_NAME),
        "required_capabilities": required_capabilities,
        "review_context_capsule_metadata_only": True,
        "commit_authority_granted": False,
        "commit_performed": False,
    }


def beta_readiness_runtime(
    pai_dir: Path,
    runtime: str,
    run_dir: str | Path,
    runtime_attempt_number: int = 1,
) -> dict[str, object]:
    doctor(pai_dir)
    if runtime != "codex":
        raise RunnerError(f"unknown runtime provider: {runtime}")
    provider_validation = provider_lifecycle_validate(pai_dir, runtime)
    if not provider_validation.get("valid"):
        raise RunnerError("codex provider validation failed")
    safe_run_dir = _safe_beta_readiness_run_dir(pai_dir, run_dir)
    return run_beta_readiness_gate(
        pai_dir=pai_dir,
        runtime=runtime,
        run_dir=safe_run_dir,
        runtime_attempt_number=runtime_attempt_number,
        repo_root=Path.cwd(),
    )


def audit_runtime_run(
    pai_dir: Path,
    marker: str | Path,
    run_dir: str | Path,
    output: str | Path,
    runtime_attempt_number: int,
) -> dict[str, object]:
    doctor(pai_dir)
    marker_path = _safe_marker(marker)
    safe_run_dir = _safe_run_dir(pai_dir, run_dir)
    output_path = _safe_audit_output(safe_run_dir, output)
    result = run_audit(
        pai_dir=pai_dir,
        marker=marker_path,
        run_dir=safe_run_dir,
        result_path=safe_run_dir / "run-result.json",
        events_path=safe_run_dir / "runtime-events.jsonl",
        runtime_attempt_number=runtime_attempt_number,
        repo_root=Path.cwd(),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result.get("validation_passed"):
        raise RunnerError(f"S15D PAI runtime audit failed; wrote {output_path}")
    return {
        "ok": True,
        "output": str(output_path),
        "event_attribution_passed": result.get("event_attribution_passed"),
        "validation_passed": result.get("validation_passed"),
    }


def audit_repo_runtime_run(
    pai_dir: Path,
    marker: str | Path,
    repo_root: str | Path,
    run_dir: str | Path,
    output: str | Path,
    runtime_attempt_number: int,
) -> dict[str, object]:
    doctor(pai_dir)
    marker_path = _safe_marker(marker)
    safe_repo_root = _safe_repo_root(repo_root)
    safe_run_dir = _safe_repo_run_dir(pai_dir, run_dir)
    output_path = _safe_repo_audit_output(safe_run_dir, output)
    result = run_repo_audit(
        pai_dir=pai_dir,
        marker=marker_path,
        repo_root=safe_repo_root,
        run_dir=safe_run_dir,
        result_path=safe_run_dir / S15E_RESULT_NAME,
        events_path=safe_run_dir / S15E_EVENTS_NAME,
        diff_path=safe_run_dir / S15E_DIFF_NAME,
        runtime_attempt_number=runtime_attempt_number,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result.get("validation_passed"):
        raise RunnerError(f"PAI runtime repo audit failed; wrote {output_path}")
    return {
        "ok": True,
        "output": str(output_path),
        "event_attribution_passed": result.get("event_attribution_passed"),
        "validation_passed": result.get("validation_passed"),
    }


def audit_pai_context_runtime_run(
    pai_dir: Path,
    marker: str | Path,
    run_dir: str | Path,
    output: str | Path,
    runtime_attempt_number: int,
) -> dict[str, object]:
    doctor(pai_dir)
    marker_path = _safe_marker(marker)
    safe_run_dir = _safe_pai_context_run_dir(pai_dir, run_dir)
    output_path = _safe_pai_context_audit_output(safe_run_dir, output)
    result = run_pai_context_audit(
        pai_dir=pai_dir,
        marker=marker_path,
        run_dir=safe_run_dir,
        capsule_path=safe_run_dir / S15I_CAPSULE_NAME,
        report_path=safe_run_dir / S15I_REPORT_NAME,
        events_path=safe_run_dir / S15I_EVENTS_NAME,
        runtime_attempt_number=runtime_attempt_number,
        repo_root=Path.cwd(),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result.get("validation_passed"):
        raise RunnerError(f"PAI context runtime audit failed; wrote {output_path}")
    validation_schema_errors = _validate_json_schema(
        result,
        pai_dir / "runtime-schemas" / "pai-context-validation.schema.json",
        "pai-context-validation.json",
    )
    if validation_schema_errors:
        raise RunnerError(
            "PAI context validation artifact schema validation failed: "
            + "; ".join(validation_schema_errors)
            + f"; wrote {output_path}"
        )
    return {
        "ok": True,
        "output": str(output_path),
        "event_attribution_passed": result.get("event_attribution_passed"),
        "validation_passed": result.get("validation_passed"),
    }


def audit_state_proposal_runtime_run(
    pai_dir: Path,
    marker: str | Path,
    run_dir: str | Path,
    output: str | Path,
    runtime_attempt_number: int,
) -> dict[str, object]:
    doctor(pai_dir)
    marker_path = _safe_marker(marker)
    safe_run_dir = _safe_state_proposal_run_dir(pai_dir, run_dir)
    output_path = _safe_state_proposal_audit_output(safe_run_dir, output)
    result = run_state_proposal_audit(
        pai_dir=pai_dir,
        marker=marker_path,
        run_dir=safe_run_dir,
        capsule_path=safe_run_dir / STATE_CONTEXT_CAPSULE_NAME,
        proposal_path=safe_run_dir / STATE_PROPOSAL_NAME,
        events_path=safe_run_dir / STATE_PROPOSAL_EVENTS_NAME,
        runtime_attempt_number=runtime_attempt_number,
        repo_root=Path.cwd(),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result.get("validation_passed"):
        raise RunnerError(f"state proposal runtime audit failed; wrote {output_path}")
    validation_schema_errors = _validate_json_schema(
        result,
        pai_dir / "runtime-schemas" / "state-proposal-validation.schema.json",
        STATE_PROPOSAL_VALIDATION_NAME,
    )
    if validation_schema_errors:
        raise RunnerError(
            "state proposal validation artifact schema validation failed: "
            + "; ".join(validation_schema_errors)
            + f"; wrote {output_path}"
        )
    return {
        "ok": True,
        "output": str(output_path),
        "event_attribution_passed": result.get("event_attribution_passed"),
        "validation_passed": result.get("validation_passed"),
    }


def audit_state_proposal_review_runtime_run(
    pai_dir: Path,
    marker: str | Path,
    run_dir: str | Path,
    output: str | Path,
    runtime_attempt_number: int,
) -> dict[str, object]:
    doctor(pai_dir)
    marker_path = _safe_marker(marker)
    safe_run_dir = _safe_state_proposal_review_run_dir(pai_dir, run_dir)
    output_path = _safe_state_proposal_review_audit_output(safe_run_dir, output)
    state = _load_json(safe_run_dir / STATE_PROPOSAL_REVIEW_STATE_NAME, "state proposal review state")
    source_value = state.get("source_proposal_path")
    source_path = _safe_state_proposal_review_source(
        pai_dir,
        source_value if isinstance(source_value, str) else pai_dir / S16B_SOURCE_PROPOSAL_RELATIVE,
    )
    result = run_state_proposal_review_audit(
        pai_dir=pai_dir,
        marker=marker_path,
        run_dir=safe_run_dir,
        source_proposal_path=source_path,
        capsule_path=safe_run_dir / REVIEW_CONTEXT_CAPSULE_NAME,
        review_path=safe_run_dir / STATE_PROPOSAL_REVIEW_NAME,
        decisions_path=safe_run_dir / STATE_PROPOSAL_DECISIONS_NAME,
        events_path=safe_run_dir / STATE_PROPOSAL_REVIEW_EVENTS_NAME,
        runtime_attempt_number=runtime_attempt_number,
        repo_root=Path.cwd(),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result.get("validation_passed"):
        raise RunnerError(f"state proposal review runtime audit failed; wrote {output_path}")
    validation_schema_errors = _validate_json_schema(
        result,
        pai_dir / "runtime-schemas" / "state-proposal-review-validation.schema.json",
        STATE_PROPOSAL_REVIEW_VALIDATION_NAME,
    )
    if validation_schema_errors:
        raise RunnerError(
            "state proposal review validation artifact schema validation failed: "
            + "; ".join(validation_schema_errors)
            + f"; wrote {output_path}"
        )
    return {
        "ok": True,
        "output": str(output_path),
        "event_attribution_passed": result.get("event_attribution_passed"),
        "validation_passed": result.get("validation_passed"),
    }


def audit_provider_lifecycle_run(
    pai_dir: Path,
    marker: str | Path,
    repo_root: str | Path,
    output: str | Path,
    runtime: str = "codex",
) -> dict[str, object]:
    marker_path = _safe_marker(marker)
    safe_repo_root = _safe_repo_root(repo_root)
    output_path = _safe_provider_lifecycle_audit_output(pai_dir, output)
    result = run_provider_lifecycle_audit(
        pai_dir=pai_dir,
        marker=marker_path,
        repo_root=safe_repo_root,
        runtime_name=runtime,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result.get("validation_passed"):
        raise RunnerError(f"PAI provider lifecycle audit failed; wrote {output_path}")
    return {
        "ok": True,
        "output": str(output_path),
        "event_attribution_passed": result.get("event_attribution_passed"),
        "validation_passed": result.get("validation_passed"),
    }


def audit_capability_policy_run(
    pai_dir: Path,
    marker: str | Path,
    repo_root: str | Path,
    output: str | Path,
    runtime: str = "codex",
) -> dict[str, object]:
    marker_path = _safe_marker(marker)
    safe_repo_root = _safe_repo_root(repo_root)
    output_path = _safe_capability_policy_audit_output(pai_dir, output)
    result = run_capability_policy_audit(
        pai_dir=pai_dir,
        marker=marker_path,
        repo_root=safe_repo_root,
        runtime_name=runtime,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result.get("validation_passed"):
        raise RunnerError(f"PAI capability policy audit failed; wrote {output_path}")
    return {
        "ok": True,
        "output": str(output_path),
        "event_attribution_passed": result.get("event_attribution_passed"),
        "validation_passed": result.get("validation_passed"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PAI-owned runtime runner.")
    subcommands = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subcommands.add_parser("doctor")
    doctor_parser.add_argument("--pai-dir", required=True)

    providers_parser = subcommands.add_parser("providers")
    providers_subcommands = providers_parser.add_subparsers(dest="providers_command", required=True)

    providers_list_parser = providers_subcommands.add_parser("list")
    providers_list_parser.add_argument("--pai-dir", required=True)

    providers_status_parser = providers_subcommands.add_parser("status")
    providers_status_parser.add_argument("runtime")
    providers_status_parser.add_argument("--pai-dir", required=True)

    providers_doctor_parser = providers_subcommands.add_parser("doctor")
    providers_doctor_parser.add_argument("runtime")
    providers_doctor_parser.add_argument("--pai-dir", required=True)

    providers_validate_parser = providers_subcommands.add_parser("validate")
    providers_validate_parser.add_argument("runtime")
    providers_validate_parser.add_argument("--pai-dir", required=True)

    run_parser = subcommands.add_parser("run")
    run_parser.add_argument("--pai-dir", required=True)
    run_parser.add_argument("--runtime", required=True)
    run_parser.add_argument("--task-card", required=True)
    run_parser.add_argument("--run-dir", required=True)
    run_parser.add_argument("--dry-run", action="store_true")

    repo_parser = subcommands.add_parser("run-repo")
    repo_parser.add_argument("--pai-dir", required=True)
    repo_parser.add_argument("--runtime", required=True)
    repo_parser.add_argument("--task-card", required=True)
    repo_parser.add_argument("--repo-root", required=True)
    repo_parser.add_argument("--run-dir", required=True)
    repo_parser.add_argument("--dry-run", action="store_true")

    context_parser = subcommands.add_parser("run-pai-context")
    context_parser.add_argument("--pai-dir", required=True)
    context_parser.add_argument("--runtime", required=True)
    context_parser.add_argument("--task-card", required=True)
    context_parser.add_argument("--run-dir", required=True)
    context_parser.add_argument("--dry-run", action="store_true")

    state_parser = subcommands.add_parser("propose-state")
    state_parser.add_argument("--pai-dir", required=True)
    state_parser.add_argument("--runtime", required=True)
    state_parser.add_argument("--task-card", required=True)
    state_parser.add_argument("--run-dir", required=True)
    state_parser.add_argument("--dry-run", action="store_true")

    review_parser = subcommands.add_parser("review-state-proposal")
    review_parser.add_argument("--pai-dir", required=True)
    review_parser.add_argument("--runtime", required=True)
    review_parser.add_argument("--task-card", required=True)
    review_parser.add_argument("--source-proposal", required=True)
    review_parser.add_argument("--run-dir", required=True)
    review_parser.add_argument("--dry-run", action="store_true")

    beta_readiness_parser = subcommands.add_parser("beta-readiness")
    beta_readiness_parser.add_argument("--pai-dir", required=True)
    beta_readiness_parser.add_argument("--runtime", required=True)
    beta_readiness_parser.add_argument("--run-dir", required=True)
    beta_readiness_parser.add_argument("--runtime-attempt-number", type=int, default=1)

    audit_parser = subcommands.add_parser("audit-run")
    audit_parser.add_argument("--pai-dir", required=True)
    audit_parser.add_argument("--marker", required=True)
    audit_parser.add_argument("--run-dir", required=True)
    audit_parser.add_argument("--output", required=True)
    audit_parser.add_argument("--runtime-attempt-number", type=int, default=1)

    repo_audit_parser = subcommands.add_parser("audit-repo-run")
    repo_audit_parser.add_argument("--pai-dir", required=True)
    repo_audit_parser.add_argument("--marker", required=True)
    repo_audit_parser.add_argument("--repo-root", required=True)
    repo_audit_parser.add_argument("--run-dir", required=True)
    repo_audit_parser.add_argument("--output", required=True)
    repo_audit_parser.add_argument("--runtime-attempt-number", type=int, default=1)

    context_audit_parser = subcommands.add_parser("audit-pai-context")
    context_audit_parser.add_argument("--pai-dir", required=True)
    context_audit_parser.add_argument("--marker", required=True)
    context_audit_parser.add_argument("--run-dir", required=True)
    context_audit_parser.add_argument("--output", required=True)
    context_audit_parser.add_argument("--runtime-attempt-number", type=int, default=1)

    state_audit_parser = subcommands.add_parser("audit-state-proposal")
    state_audit_parser.add_argument("--pai-dir", required=True)
    state_audit_parser.add_argument("--marker", required=True)
    state_audit_parser.add_argument("--run-dir", required=True)
    state_audit_parser.add_argument("--output", required=True)
    state_audit_parser.add_argument("--runtime-attempt-number", type=int, default=1)

    review_audit_parser = subcommands.add_parser("audit-state-proposal-review")
    review_audit_parser.add_argument("--pai-dir", required=True)
    review_audit_parser.add_argument("--marker", required=True)
    review_audit_parser.add_argument("--run-dir", required=True)
    review_audit_parser.add_argument("--output", required=True)
    review_audit_parser.add_argument("--runtime-attempt-number", type=int, default=1)

    provider_lifecycle_audit_parser = subcommands.add_parser("audit-provider-lifecycle")
    provider_lifecycle_audit_parser.add_argument("--pai-dir", required=True)
    provider_lifecycle_audit_parser.add_argument("--marker", required=True)
    provider_lifecycle_audit_parser.add_argument("--repo-root", required=True)
    provider_lifecycle_audit_parser.add_argument("--output", required=True)
    provider_lifecycle_audit_parser.add_argument("--runtime", default="codex")

    capability_audit_parser = subcommands.add_parser("audit-capabilities")
    capability_audit_parser.add_argument("--pai-dir", required=True)
    capability_audit_parser.add_argument("--marker", required=True)
    capability_audit_parser.add_argument("--repo-root", required=True)
    capability_audit_parser.add_argument("--output", required=True)
    capability_audit_parser.add_argument("--runtime", default="codex")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        pai_dir = _resolve_pai_dir(args.pai_dir)
        if args.command == "doctor":
            result = doctor(pai_dir)
        elif args.command == "providers":
            if args.providers_command == "list":
                result = provider_lifecycle_list(pai_dir)
            elif args.providers_command == "status":
                result = provider_lifecycle_status(pai_dir, args.runtime)
            elif args.providers_command == "doctor":
                result = provider_lifecycle_doctor(pai_dir, args.runtime)
            elif args.providers_command == "validate":
                result = provider_lifecycle_validate(pai_dir, args.runtime)
            else:
                raise RunnerError(f"unknown providers command: {args.providers_command}")
        elif args.command == "run":
            result = run_runtime(pai_dir, args.runtime, args.task_card, args.run_dir, args.dry_run)
        elif args.command == "run-repo":
            result = run_repo_runtime(
                pai_dir,
                args.runtime,
                args.task_card,
                args.repo_root,
                args.run_dir,
                args.dry_run,
            )
        elif args.command == "run-pai-context":
            result = run_pai_context_runtime(
                pai_dir,
                args.runtime,
                args.task_card,
                args.run_dir,
                args.dry_run,
            )
        elif args.command == "propose-state":
            result = propose_state_runtime(
                pai_dir,
                args.runtime,
                args.task_card,
                args.run_dir,
                args.dry_run,
            )
        elif args.command == "review-state-proposal":
            result = review_state_proposal_runtime(
                pai_dir,
                args.runtime,
                args.task_card,
                args.source_proposal,
                args.run_dir,
                args.dry_run,
            )
        elif args.command == "beta-readiness":
            result = beta_readiness_runtime(
                pai_dir,
                args.runtime,
                args.run_dir,
                args.runtime_attempt_number,
            )
        elif args.command == "audit-run":
            result = audit_runtime_run(pai_dir, args.marker, args.run_dir, args.output, args.runtime_attempt_number)
        elif args.command == "audit-repo-run":
            result = audit_repo_runtime_run(
                pai_dir,
                args.marker,
                args.repo_root,
                args.run_dir,
                args.output,
                args.runtime_attempt_number,
            )
        elif args.command == "audit-pai-context":
            result = audit_pai_context_runtime_run(
                pai_dir,
                args.marker,
                args.run_dir,
                args.output,
                args.runtime_attempt_number,
            )
        elif args.command == "audit-state-proposal":
            result = audit_state_proposal_runtime_run(
                pai_dir,
                args.marker,
                args.run_dir,
                args.output,
                args.runtime_attempt_number,
            )
        elif args.command == "audit-state-proposal-review":
            result = audit_state_proposal_review_runtime_run(
                pai_dir,
                args.marker,
                args.run_dir,
                args.output,
                args.runtime_attempt_number,
            )
        elif args.command == "audit-provider-lifecycle":
            result = audit_provider_lifecycle_run(
                pai_dir,
                args.marker,
                args.repo_root,
                args.output,
                args.runtime,
            )
        elif args.command == "audit-capabilities":
            result = audit_capability_policy_run(
                pai_dir,
                args.marker,
                args.repo_root,
                args.output,
                args.runtime,
            )
        else:
            raise RunnerError(f"unknown command: {args.command}")
    except (
        BetaReadinessError,
        CapabilityPolicyError,
        PaiContextError,
        ProviderRegistryError,
        RunnerError,
        StateProposalError,
        StateProposalReviewError,
        OSError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
