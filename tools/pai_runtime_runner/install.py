from __future__ import annotations

import json
import shutil
import stat
from pathlib import Path

from tools.pai_runtime_runner.capabilities import CODEX_S16B_PROVIDER_CAPABILITIES, CapabilityPolicyError, provider_capabilities

try:
    from jsonschema import Draft202012Validator
except Exception:  # noqa: BLE001 - install reports unavailable schema validation.
    Draft202012Validator = None  # type: ignore[assignment]


class RuntimeInstallError(ValueError):
    pass


REPO_ROOT = Path(__file__).resolve().parents[2]

INSTALL_TEXT_TARGETS = {
    REPO_ROOT / "runtimes" / "codex" / "README.md": Path("runtimes") / "codex" / "README.md",
    REPO_ROOT / "runtimes" / "codex" / "provider-manifest.json": Path("runtimes") / "codex" / "provider-manifest.json",
    REPO_ROOT / "pai-runtime" / "provider-manifest.schema.json": Path("runtime-schemas") / "provider-manifest.schema.json",
    REPO_ROOT / "pai-runtime" / "run-result.schema.json": Path("runtime-schemas") / "run-result.schema.json",
    REPO_ROOT / "pai-runtime" / "run-validation.schema.json": Path("runtime-schemas") / "run-validation.schema.json",
    REPO_ROOT / "pai-runtime" / "repo-task.schema.json": Path("runtime-schemas") / "repo-task.schema.json",
    REPO_ROOT / "pai-runtime" / "repo-run-result.schema.json": Path("runtime-schemas") / "repo-run-result.schema.json",
    REPO_ROOT / "pai-runtime" / "repo-run-validation.schema.json": Path("runtime-schemas") / "repo-run-validation.schema.json",
    REPO_ROOT / "pai-runtime" / "patch-proposal.schema.json": Path("runtime-schemas") / "patch-proposal.schema.json",
    REPO_ROOT / "pai-runtime" / "pai-context-task.schema.json": Path("runtime-schemas") / "pai-context-task.schema.json",
    REPO_ROOT / "pai-runtime" / "pai-context-capsule.schema.json": Path("runtime-schemas") / "pai-context-capsule.schema.json",
    REPO_ROOT / "pai-runtime" / "pai-context-report.schema.json": Path("runtime-schemas") / "pai-context-report.schema.json",
    REPO_ROOT / "pai-runtime" / "pai-context-validation.schema.json": Path("runtime-schemas") / "pai-context-validation.schema.json",
    REPO_ROOT / "pai-runtime" / "beta-readiness-result.schema.json": Path("runtime-schemas") / "beta-readiness-result.schema.json",
    REPO_ROOT / "pai-runtime" / "beta-readiness-validation.schema.json": Path("runtime-schemas") / "beta-readiness-validation.schema.json",
    REPO_ROOT / "pai-runtime" / "evidence-index.schema.json": Path("runtime-schemas") / "evidence-index.schema.json",
    REPO_ROOT / "pai-runtime" / "state-proposal-task.schema.json": Path("runtime-schemas") / "state-proposal-task.schema.json",
    REPO_ROOT / "pai-runtime" / "state-context-capsule.schema.json": Path("runtime-schemas") / "state-context-capsule.schema.json",
    REPO_ROOT / "pai-runtime" / "state-proposal.schema.json": Path("runtime-schemas") / "state-proposal.schema.json",
    REPO_ROOT / "pai-runtime" / "state-proposal-validation.schema.json": Path("runtime-schemas") / "state-proposal-validation.schema.json",
    REPO_ROOT / "pai-runtime" / "state-proposal-review-task.schema.json": Path("runtime-schemas") / "state-proposal-review-task.schema.json",
    REPO_ROOT / "pai-runtime" / "state-proposal-review.schema.json": Path("runtime-schemas") / "state-proposal-review.schema.json",
    REPO_ROOT / "pai-runtime" / "state-proposal-decisions.schema.json": Path("runtime-schemas") / "state-proposal-decisions.schema.json",
    REPO_ROOT / "pai-runtime" / "state-proposal-review-validation.schema.json": Path("runtime-schemas") / "state-proposal-review-validation.schema.json",
    REPO_ROOT / "pai-runtime" / "tasks" / "s15d-codex-synthetic-bugfix.json": Path("runtime-tasks") / "s15d-codex-synthetic-bugfix.json",
    REPO_ROOT / "pai-runtime" / "tasks" / "s15e-provider-registry-repo-task.json": Path("runtime-tasks") / "s15e-provider-registry-repo-task.json",
    REPO_ROOT / "pai-runtime" / "tasks" / "s15f-patch-proposal-repo-task.json": Path("runtime-tasks") / "s15f-patch-proposal-repo-task.json",
    REPO_ROOT / "pai-runtime" / "tasks" / "s15i-readonly-pai-context-task.json": Path("runtime-tasks") / "s15i-readonly-pai-context-task.json",
    REPO_ROOT / "pai-runtime" / "tasks" / "s16a-state-proposal-task.json": Path("runtime-tasks") / "s16a-state-proposal-task.json",
    REPO_ROOT / "pai-runtime" / "tasks" / "s16b-state-proposal-review-task.json": Path("runtime-tasks") / "s16b-state-proposal-review-task.json",
    REPO_ROOT / "pai-runtime" / "task-fixtures" / "s15d_bugfix" / "README.md": Path("runtime-task-fixtures") / "s15d_bugfix" / "README.md",
    REPO_ROOT / "pai-runtime" / "task-fixtures" / "s15d_bugfix" / "src" / "pai_priority.py": Path("runtime-task-fixtures") / "s15d_bugfix" / "src" / "pai_priority.py",
    REPO_ROOT / "pai-runtime" / "task-fixtures" / "s15d_bugfix" / "tests" / "test_pai_priority.py": Path("runtime-task-fixtures") / "s15d_bugfix" / "tests" / "test_pai_priority.py",
    REPO_ROOT / "adapters" / "codex" / "bin" / "pai-codex": Path("adapters") / "codex" / "bin" / "pai-codex",
}

APPROVED_LIVE_RELATIVES = tuple(INSTALL_TEXT_TARGETS.values()) + (
    Path("bin") / "pai-runtime",
    Path("runtime-state.json"),
    Path("adapters") / "codex" / "install-state.json",
    Path("runs") / "s15d" / "codex-synthetic-bugfix" / "run-result.json",
    Path("runs") / "s15d" / "codex-synthetic-bugfix" / "runtime-events.jsonl",
    Path("runs") / "s15d" / "codex-synthetic-bugfix" / "task.diff",
    Path("runs") / "s15d" / "codex-synthetic-bugfix" / "run-validation.json",
    Path("runs") / "s15d" / "codex-synthetic-bugfix" / "run-state.json",
    Path("runs") / "s15e" / "provider-registry" / "repo-run-result.json",
    Path("runs") / "s15e" / "provider-registry" / "repo-events.jsonl",
    Path("runs") / "s15e" / "provider-registry" / "repo-task.diff",
    Path("runs") / "s15e" / "provider-registry" / "repo-run-validation.json",
    Path("runs") / "s15e" / "provider-registry" / "repo-run-state.json",
    Path("runs") / "s15f" / "patch-proposal" / "repo-run-result.json",
    Path("runs") / "s15f" / "patch-proposal" / "repo-events.jsonl",
    Path("runs") / "s15f" / "patch-proposal" / "repo-task.diff",
    Path("runs") / "s15f" / "patch-proposal" / "patch-proposal.json",
    Path("runs") / "s15f" / "patch-proposal" / "repo-run-validation.json",
    Path("runs") / "s15f" / "patch-proposal" / "repo-run-state.json",
    Path("runs") / "s15i" / "read-only-pai-context" / "pai-context-capsule.json",
    Path("runs") / "s15i" / "read-only-pai-context" / "pai-context-report.schema.json",
    Path("runs") / "s15i" / "read-only-pai-context" / "pai-context-report.json",
    Path("runs") / "s15i" / "read-only-pai-context" / "pai-context-events.jsonl",
    Path("runs") / "s15i" / "read-only-pai-context" / "pai-context-state.json",
    Path("runs") / "s15i" / "read-only-pai-context" / "pai-context-validation.json",
    Path("runs") / "s15j" / "codex-beta-readiness" / "beta-readiness-result.json",
    Path("runs") / "s15j" / "codex-beta-readiness" / "beta-readiness-events.jsonl",
    Path("runs") / "s15j" / "codex-beta-readiness" / "beta-readiness-validation.json",
    Path("runs") / "s15j" / "codex-beta-readiness" / "evidence-index.json",
    Path("runs") / "s16a" / "state-proposal" / "state-context-capsule.json",
    Path("runs") / "s16a" / "state-proposal" / "state-proposal.schema.json",
    Path("runs") / "s16a" / "state-proposal" / "state-proposal.json",
    Path("runs") / "s16a" / "state-proposal" / "state-proposal-events.jsonl",
    Path("runs") / "s16a" / "state-proposal" / "state-proposal-state.json",
    Path("runs") / "s16a" / "state-proposal" / "state-proposal-validation.json",
    Path("runs") / "s16b" / "proposal-review" / "review-context-capsule.json",
    Path("runs") / "s16b" / "proposal-review" / "state-proposal-review.schema.json",
    Path("runs") / "s16b" / "proposal-review" / "state-proposal-decisions.schema.json",
    Path("runs") / "s16b" / "proposal-review" / "state-proposal-review.json",
    Path("runs") / "s16b" / "proposal-review" / "state-proposal-decisions.json",
    Path("runs") / "s16b" / "proposal-review" / "state-proposal-review-events.jsonl",
    Path("runs") / "s16b" / "proposal-review" / "state-proposal-review-state.json",
    Path("runs") / "s16b" / "proposal-review" / "state-proposal-review-validation.json",
)

RUN_DIR_RELATIVE = Path("runs") / "s15d" / "codex-synthetic-bugfix"
S15E_RUN_DIR_RELATIVE = Path("runs") / "s15e" / "provider-registry"
S15F_RUN_DIR_RELATIVE = Path("runs") / "s15f" / "patch-proposal"
S15I_RUN_DIR_RELATIVE = Path("runs") / "s15i" / "read-only-pai-context"
S15J_RUN_DIR_RELATIVE = Path("runs") / "s15j" / "codex-beta-readiness"
S16A_RUN_DIR_RELATIVE = Path("runs") / "s16a" / "state-proposal"
S16B_RUN_DIR_RELATIVE = Path("runs") / "s16b" / "proposal-review"
S15I_MUTABLE_INSTALL_RELATIVES = {
    Path("bin") / "pai-runtime",
    Path("runtime-state.json"),
    Path("runtime-schemas") / "pai-context-task.schema.json",
    Path("runtime-schemas") / "pai-context-capsule.schema.json",
    Path("runtime-schemas") / "pai-context-report.schema.json",
    Path("runtime-schemas") / "pai-context-validation.schema.json",
    Path("runtime-schemas") / "beta-readiness-result.schema.json",
    Path("runtime-schemas") / "beta-readiness-validation.schema.json",
    Path("runtime-schemas") / "evidence-index.schema.json",
    Path("runtime-schemas") / "state-proposal-task.schema.json",
    Path("runtime-schemas") / "state-context-capsule.schema.json",
    Path("runtime-schemas") / "state-proposal.schema.json",
    Path("runtime-schemas") / "state-proposal-validation.schema.json",
    Path("runtime-schemas") / "state-proposal-review-task.schema.json",
    Path("runtime-schemas") / "state-proposal-review.schema.json",
    Path("runtime-schemas") / "state-proposal-decisions.schema.json",
    Path("runtime-schemas") / "state-proposal-review-validation.schema.json",
    Path("runtime-tasks") / "s15i-readonly-pai-context-task.json",
    Path("runtime-tasks") / "s16a-state-proposal-task.json",
    Path("runtime-tasks") / "s16b-state-proposal-review-task.json",
    Path("runtimes") / "codex" / "provider-manifest.json",
}


def _is_within(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _resolve_pai_dir(value: str | Path | None) -> Path:
    if value is None or str(value) == "":
        raise RuntimeInstallError("--pai-dir is required")
    path = Path(value)
    if any(part == ".." for part in path.parts):
        raise RuntimeInstallError("--pai-dir must not contain path traversal")
    resolved = path.resolve(strict=True)
    if not resolved.is_dir():
        raise RuntimeInstallError("--pai-dir must be a directory")
    return resolved


def _resolve_backup_root(value: str | Path | None) -> Path:
    if value is None or str(value) == "":
        raise RuntimeInstallError("--backup-root is required")
    path = Path(value)
    if any(part == ".." for part in path.parts):
        raise RuntimeInstallError("--backup-root must not contain path traversal")
    resolved = path.resolve(strict=True)
    if not resolved.is_dir():
        raise RuntimeInstallError("--backup-root must be a directory")
    return resolved


def _safe_live_path(pai_dir: Path, relative: Path) -> Path:
    if relative.is_absolute() or any(part == ".." for part in relative.parts):
        raise RuntimeInstallError(f"unsafe live relative path: {relative}")
    resolved = (pai_dir / relative).resolve(strict=False)
    if not _is_within(pai_dir, resolved):
        raise RuntimeInstallError(f"live target escapes PAI_DIR: {relative}")
    return resolved


def _write_text_if_changed(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.is_symlink():
        raise RuntimeInstallError(f"live target is a symlink: {path}")
    if path.exists() and not path.is_file():
        raise RuntimeInstallError(f"live target is not a file: {path}")
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def _mark_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def _is_live_pai_dir(path: Path) -> bool:
    return path.resolve(strict=False) == (Path.home() / ".claude" / "PAI").resolve(strict=False)


def _wrapper_text() -> str:
    return (
        "#!/usr/bin/env python3\n"
        "from pathlib import Path\n"
        "import sys\n"
        f"sys.path.insert(0, {str(REPO_ROOT)!r})\n"
        "from tools.pai_runtime_runner.runner import main\n"
        "raise SystemExit(main())\n"
    )


def _runtime_state() -> str:
    payload = {
        "installed": True,
        "milestone_name": "V5-S16B-PAI-STATE-PROPOSAL-REVIEW-POLICY",
        "ownership_model": "PAI owns the run; Codex is runtime provider codex.",
        "runtime_provider": "codex",
        "runtime_status": "peer-beta",
        "upstream_adapter": "claude",
        "supports_repo_tasks": True,
        "supports_patch_proposals": True,
        "supports_pai_context_metadata": True,
        "supports_beta_readiness_gate": True,
        "supports_state_proposals": True,
        "supports_state_proposal_reviews": True,
        "state_proposal_apply_policy": "proposed_only",
        "state_proposal_review_policy": "review_only_non_committing",
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _load_provider_manifest() -> dict[str, object]:
    return json.loads((REPO_ROOT / "runtimes" / "codex" / "provider-manifest.json").read_text(encoding="utf-8"))


def _provider_manifest_for_install() -> dict[str, object]:
    manifest = dict(_load_provider_manifest())
    capabilities = list(provider_capabilities(manifest))
    ordered = [capability for capability in CODEX_S16B_PROVIDER_CAPABILITIES if capability in set(capabilities)]
    missing = [capability for capability in CODEX_S16B_PROVIDER_CAPABILITIES if capability not in set(capabilities)]
    manifest["capabilities"] = ordered + missing
    return manifest


def _provider_manifest_install_text() -> str:
    return json.dumps(_provider_manifest_for_install(), indent=2, sort_keys=True) + "\n"


def _validate_schema_file(path: Path, label: str) -> None:
    if Draft202012Validator is None:
        raise RuntimeInstallError(f"{label} schema validation unavailable: jsonschema is not installed")
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeInstallError(f"{label} schema is not valid JSON") from exc
    if not isinstance(schema, dict):
        raise RuntimeInstallError(f"{label} schema must be a JSON object")
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # noqa: BLE001 - normalize schema failures as install errors.
        raise RuntimeInstallError(f"{label} schema failed Draft 2020-12 validation: {exc}") from exc


def _load_json_object_file(path: Path, label: str) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeInstallError(f"{label} is not valid JSON") from exc
    if not isinstance(data, dict):
        raise RuntimeInstallError(f"{label} must be a JSON object")
    return data


def _validate_json_instance(instance_path: Path, schema_path: Path, label: str) -> None:
    if Draft202012Validator is None:
        raise RuntimeInstallError(f"{label} validation unavailable: jsonschema is not installed")
    instance = _load_json_object_file(instance_path, label)
    schema = _load_json_object_file(schema_path, f"{schema_path.name} schema")
    try:
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(instance)
    except Exception as exc:  # noqa: BLE001 - normalize schema failures as install errors.
        raise RuntimeInstallError(f"{label} failed schema validation: {exc}") from exc


def validate_staged_payload() -> None:
    manifest = _provider_manifest_for_install()
    expected = {
        "runtime_name": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "upstream_adapter": "claude",
        "supports_codex_exec": True,
        "supports_jsonl_events": True,
        "supports_structured_output": True,
        "memory_write_policy": "disabled",
        "isa_write_policy": "disabled",
        "pulse_policy": "no-probe",
        "replacement_status": "not-replacement-grade",
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            raise RuntimeInstallError(f"provider manifest mismatch for {key}")
    try:
        capabilities = provider_capabilities(manifest)
    except CapabilityPolicyError as exc:
        raise RuntimeInstallError(f"provider manifest capabilities are invalid: {exc}") from exc
    expected_capabilities = set(CODEX_S16B_PROVIDER_CAPABILITIES)
    if capabilities != expected_capabilities:
        raise RuntimeInstallError("provider manifest capabilities do not match the approved Codex provider set")
    if "pai.context.read.metadata" not in capabilities:
        raise RuntimeInstallError("provider manifest is missing pai.context.read.metadata")
    for source in INSTALL_TEXT_TARGETS:
        if not source.is_file():
            raise RuntimeInstallError(f"missing staged runtime file: {source}")
    for source in (
        REPO_ROOT / "pai-runtime" / "pai-context-task.schema.json",
        REPO_ROOT / "pai-runtime" / "pai-context-capsule.schema.json",
        REPO_ROOT / "pai-runtime" / "pai-context-report.schema.json",
        REPO_ROOT / "pai-runtime" / "pai-context-validation.schema.json",
        REPO_ROOT / "pai-runtime" / "beta-readiness-result.schema.json",
        REPO_ROOT / "pai-runtime" / "beta-readiness-validation.schema.json",
        REPO_ROOT / "pai-runtime" / "evidence-index.schema.json",
        REPO_ROOT / "pai-runtime" / "state-proposal-task.schema.json",
        REPO_ROOT / "pai-runtime" / "state-context-capsule.schema.json",
        REPO_ROOT / "pai-runtime" / "state-proposal.schema.json",
        REPO_ROOT / "pai-runtime" / "state-proposal-validation.schema.json",
        REPO_ROOT / "pai-runtime" / "state-proposal-review-task.schema.json",
        REPO_ROOT / "pai-runtime" / "state-proposal-review.schema.json",
        REPO_ROOT / "pai-runtime" / "state-proposal-decisions.schema.json",
        REPO_ROOT / "pai-runtime" / "state-proposal-review-validation.schema.json",
    ):
        _validate_schema_file(source, source.name)
    _validate_json_instance(
        REPO_ROOT / "pai-runtime" / "tasks" / "s15i-readonly-pai-context-task.json",
        REPO_ROOT / "pai-runtime" / "pai-context-task.schema.json",
        "s15i-readonly-pai-context-task.json",
    )
    _validate_json_instance(
        REPO_ROOT / "pai-runtime" / "tasks" / "s16a-state-proposal-task.json",
        REPO_ROOT / "pai-runtime" / "state-proposal-task.schema.json",
        "s16a-state-proposal-task.json",
    )
    _validate_json_instance(
        REPO_ROOT / "pai-runtime" / "tasks" / "s16b-state-proposal-review-task.json",
        REPO_ROOT / "pai-runtime" / "state-proposal-review-task.schema.json",
        "s16b-state-proposal-review-task.json",
    )
    runner = (REPO_ROOT / "tools" / "pai_runtime_runner" / "runner.py").read_text(encoding="utf-8")
    audit = (REPO_ROOT / "tools" / "pai_runtime_runner" / "audit.py").read_text(encoding="utf-8")
    provider_registry = (REPO_ROOT / "tools" / "pai_runtime_runner" / "provider_registry.py").read_text(encoding="utf-8")
    if "PAI owns the run" not in runner or "runs/s15d" not in runner or "run-repo" not in runner:
        raise RuntimeInstallError("runner is missing PAI ownership tokens")
    if "audit-repo-run" not in runner or "approved_repository_write_set" not in runner + audit:
        raise RuntimeInstallError("runner/audit is missing S15E repo-task tokens")
    patch_proposal = (REPO_ROOT / "tools" / "pai_runtime_runner" / "patch_proposal.py").read_text(encoding="utf-8")
    if "materialize_patch_proposal" not in patch_proposal or "path traversal" not in patch_proposal:
        raise RuntimeInstallError("patch proposal module is missing S15F validation tokens")
    if "patch_proposal_applied_by_pai" not in runner + audit:
        raise RuntimeInstallError("runner/audit is missing S15F patch proposal apply tokens")
    pai_context = (REPO_ROOT / "tools" / "pai_runtime_runner" / "pai_context.py").read_text(encoding="utf-8")
    if "collect_pai_context_metadata" not in pai_context or "metadata_only" not in pai_context:
        raise RuntimeInstallError("PAI context collector is missing metadata-only collection tokens")
    if "run-pai-context" not in runner or "audit-pai-context" not in runner + audit:
        raise RuntimeInstallError("runner/audit is missing S15I PAI context command tokens")
    if "pai.context.read.metadata" not in runner + audit + pai_context:
        raise RuntimeInstallError("S15I context pipeline is missing pai.context.read.metadata tokens")
    state_proposal = (REPO_ROOT / "tools" / "pai_runtime_runner" / "state_proposal.py").read_text(encoding="utf-8")
    provider = (REPO_ROOT / "tools" / "pai_runtime_runner" / "providers" / "codex.py").read_text(encoding="utf-8")
    if "propose-state" not in runner or "audit-state-proposal" not in runner:
        raise RuntimeInstallError("runner is missing S16A state proposal command tokens")
    for token in (
        "validate_state_proposal",
        "all_memory_proposals_proposed_only",
        "all_isa_proposals_proposed_only",
        "memory_files_modified",
        "isa_files_modified",
        "state-context-capsule",
    ):
        if token not in state_proposal:
            raise RuntimeInstallError(f"state proposal module is missing token: {token}")
    for token in ("memory.write.proposal", "isa.write.proposal"):
        if token not in runner + state_proposal + provider:
            raise RuntimeInstallError(f"S16A state proposal pipeline is missing capability token: {token}")
    state_proposal_review = (
        REPO_ROOT / "tools" / "pai_runtime_runner" / "state_proposal_review.py"
    ).read_text(encoding="utf-8")
    if "review-state-proposal" not in runner or "audit-state-proposal-review" not in runner:
        raise RuntimeInstallError("runner is missing S16B state proposal review command tokens")
    for token in (
        "validate_state_proposal_review",
        "validate_state_proposal_decisions",
        "all_decisions_non_committing",
        "commit_authority_granted",
        "commit_performed",
        "state-proposal-review",
    ):
        if token not in state_proposal_review:
            raise RuntimeInstallError(f"state proposal review module is missing token: {token}")
    for token in ("memory.proposal.review", "isa.proposal.review"):
        if token not in runner + state_proposal_review + provider:
            raise RuntimeInstallError(f"S16B state proposal review pipeline is missing capability token: {token}")
    beta_readiness = (REPO_ROOT / "tools" / "pai_runtime_runner" / "beta_readiness.py").read_text(encoding="utf-8")
    if "beta-readiness" not in runner or "run_beta_readiness_gate" not in beta_readiness:
        raise RuntimeInstallError("runner is missing S15J beta-readiness command tokens")
    for token in (
        "provider_registry_passed",
        "provider_lifecycle_passed",
        "capability_policy_passed",
        "patch_proposal_policy_passed",
        "readonly_pai_context_policy_passed",
        "replacement_readiness_claimed",
        "claude_equivalence_claimed",
        "ee2479a2122022ca72ddfed37be4b889902f5077",
        "9dd03b4a4d75b628980c8612acf989bcb892779a",
        "64e15bcf95e763d93410065e6f8e6fc887367d5e",
        "6aabb84af919cc965532e4d6ab8646660152d18c",
        "65d77603c663cd2dc319a5f36575b4d1f71fdcb1",
        "6485c3ceed3cb6d28131cb0c3722bed6fe1444f4",
        "2407aee57ded9707dd37872a329aff05e8e7a798",
    ):
        if token not in beta_readiness:
            raise RuntimeInstallError(f"S15J beta-readiness gate is missing token: {token}")
    for token in (
        "discover_runtime_providers",
        "load_provider_manifest",
        "validate_provider_manifest",
        "get_provider_by_name",
    ):
        if token not in provider_registry:
            raise RuntimeInstallError(f"provider registry is missing {token}")


def install_runtime(pai_dir: str | Path | None, backup_root: str | Path | None) -> dict[str, object]:
    resolved_pai_dir = _resolve_pai_dir(pai_dir)
    _resolve_backup_root(backup_root)
    validate_staged_payload()
    changed: list[Path] = []
    live_pai_dir = _is_live_pai_dir(resolved_pai_dir)

    wrapper = _safe_live_path(resolved_pai_dir, Path("bin") / "pai-runtime")
    if _write_text_if_changed(wrapper, _wrapper_text()):
        changed.append(wrapper)
    _mark_executable(wrapper)

    for source, relative in INSTALL_TEXT_TARGETS.items():
        target = _safe_live_path(resolved_pai_dir, relative)
        if live_pai_dir and relative not in S15I_MUTABLE_INSTALL_RELATIVES:
            if not target.is_file():
                raise RuntimeInstallError(f"required pre-S15I live runtime file is missing: {target}")
            continue
        text = (
            _provider_manifest_install_text()
            if relative == Path("runtimes") / "codex" / "provider-manifest.json"
            else source.read_text(encoding="utf-8")
        )
        if _write_text_if_changed(target, text):
            changed.append(target)
        if target.name == "pai-codex":
            _mark_executable(target)

    runtime_state = _safe_live_path(resolved_pai_dir, Path("runtime-state.json"))
    if _write_text_if_changed(runtime_state, _runtime_state()):
        changed.append(runtime_state)

    return {"pai_dir": str(resolved_pai_dir), "changed_targets": [str(path) for path in changed]}


def _backup_pai_dir(backup_root: Path) -> Path:
    backup_pai = backup_root / ".claude" / "PAI"
    if not backup_pai.is_dir():
        raise RuntimeInstallError("backup root does not contain .claude/PAI")
    return backup_pai


def _restore_or_remove(pai_dir: Path, backup_pai: Path, relative: Path) -> bool:
    target = _safe_live_path(pai_dir, relative)
    source = backup_pai / relative
    if source.exists():
        if source.is_symlink() or not source.is_file():
            raise RuntimeInstallError(f"backup source is not a safe file: {source}")
        changed = _write_text_if_changed(target, source.read_text(encoding="utf-8"))
        if target.name in {"pai-runtime", "pai-codex"}:
            _mark_executable(target)
        return changed
    if target.exists():
        if target.is_symlink() or not target.is_file():
            raise RuntimeInstallError(f"rollback target is not a safe file: {target}")
        target.unlink()
        return True
    return False


def _rollback_run_dir(pai_dir: Path, backup_pai: Path, run_relative: Path) -> list[Path]:
    live_run = _safe_live_path(pai_dir, run_relative)
    backup_run = backup_pai / run_relative
    changed: list[Path] = []
    if live_run.exists():
        if live_run.is_symlink() or not live_run.is_dir():
            raise RuntimeInstallError(f"S15D run rollback target is unsafe: {live_run}")
        shutil.rmtree(live_run)
        changed.append(live_run)
    if backup_run.exists():
        if backup_run.is_symlink() or not backup_run.is_dir():
            raise RuntimeInstallError(f"S15D backup run directory is unsafe: {backup_run}")
        shutil.copytree(backup_run, live_run, symlinks=True)
        changed.append(live_run)
    return changed


def _remove_empty_dirs(paths: tuple[Path, ...]) -> None:
    for path in paths:
        try:
            path.rmdir()
        except OSError:
            continue


def rollback_runtime(pai_dir: str | Path | None, backup_root: str | Path | None) -> dict[str, object]:
    resolved_pai_dir = _resolve_pai_dir(pai_dir)
    resolved_backup_root = _resolve_backup_root(backup_root)
    backup_pai = _backup_pai_dir(resolved_backup_root)
    changed: list[Path] = []
    for run_relative in (
        RUN_DIR_RELATIVE,
        S15E_RUN_DIR_RELATIVE,
        S15F_RUN_DIR_RELATIVE,
        S15I_RUN_DIR_RELATIVE,
        S15J_RUN_DIR_RELATIVE,
        S16A_RUN_DIR_RELATIVE,
        S16B_RUN_DIR_RELATIVE,
    ):
        changed.extend(_rollback_run_dir(resolved_pai_dir, backup_pai, run_relative))
    for relative in APPROVED_LIVE_RELATIVES:
        if relative == RUN_DIR_RELATIVE or _is_within(RUN_DIR_RELATIVE, relative):
            continue
        if relative == S15E_RUN_DIR_RELATIVE or _is_within(S15E_RUN_DIR_RELATIVE, relative):
            continue
        if relative == S15F_RUN_DIR_RELATIVE or _is_within(S15F_RUN_DIR_RELATIVE, relative):
            continue
        if relative == S15I_RUN_DIR_RELATIVE or _is_within(S15I_RUN_DIR_RELATIVE, relative):
            continue
        if relative == S15J_RUN_DIR_RELATIVE or _is_within(S15J_RUN_DIR_RELATIVE, relative):
            continue
        if relative == S16A_RUN_DIR_RELATIVE or _is_within(S16A_RUN_DIR_RELATIVE, relative):
            continue
        if relative == S16B_RUN_DIR_RELATIVE or _is_within(S16B_RUN_DIR_RELATIVE, relative):
            continue
        if _restore_or_remove(resolved_pai_dir, backup_pai, relative):
            changed.append(resolved_pai_dir / relative)
    _remove_empty_dirs(
        (
            resolved_pai_dir / RUN_DIR_RELATIVE,
            resolved_pai_dir / S15E_RUN_DIR_RELATIVE,
            resolved_pai_dir / S15F_RUN_DIR_RELATIVE,
            resolved_pai_dir / S15I_RUN_DIR_RELATIVE,
            resolved_pai_dir / S15J_RUN_DIR_RELATIVE,
            resolved_pai_dir / S16A_RUN_DIR_RELATIVE,
            resolved_pai_dir / S16B_RUN_DIR_RELATIVE,
            resolved_pai_dir / "runs" / "s16b",
            resolved_pai_dir / "runs" / "s16a",
            resolved_pai_dir / "runs" / "s15j",
            resolved_pai_dir / "runs" / "s15i",
            resolved_pai_dir / "runs" / "s15f",
            resolved_pai_dir / "runs" / "s15e",
            resolved_pai_dir / "runs" / "s15d",
            resolved_pai_dir / "runs",
            resolved_pai_dir / "runtime-task-fixtures" / "s15d_bugfix" / "src",
            resolved_pai_dir / "runtime-task-fixtures" / "s15d_bugfix" / "tests",
            resolved_pai_dir / "runtime-task-fixtures" / "s15d_bugfix",
            resolved_pai_dir / "runtime-task-fixtures",
            resolved_pai_dir / "runtime-tasks",
            resolved_pai_dir / "runtime-schemas",
            resolved_pai_dir / "runtimes" / "codex",
            resolved_pai_dir / "runtimes",
            resolved_pai_dir / "bin",
        )
    )
    return {"pai_dir": str(resolved_pai_dir), "changed_targets": [str(path) for path in changed]}
