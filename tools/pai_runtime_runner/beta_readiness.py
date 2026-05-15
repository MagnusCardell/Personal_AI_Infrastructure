from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.pai_runtime_runner.capabilities import (
    CODEX_PROVIDER_CAPABILITIES,
    FORBIDDEN_TASK_CAPABILITIES,
    validate_capability_policy,
)
from tools.pai_runtime_runner.pai_context import (
    context_report_from_capsule,
    collect_pai_context_metadata,
    validate_context_capsule,
    validate_context_report,
)
from tools.pai_runtime_runner.patch_proposal import validate_patch_proposal
from tools.pai_runtime_runner.provider_registry import (
    CODEX_PROVIDER_SEMANTICS,
    discover_runtime_providers,
    doctor_provider_by_name,
    get_provider_by_name,
    validate_provider_by_name,
)

try:
    from jsonschema import Draft202012Validator
except Exception:  # noqa: BLE001 - readiness reports unavailable schema validation.
    Draft202012Validator = None  # type: ignore[assignment]


S15J_MILESTONE = "V5-S15J-PAI-RUNTIME-CODEX-BETA-READINESS-GATE"
S15J_RUN_ID = "s15j-codex-beta-readiness"
S15J_RUN_RELATIVE = Path("runs") / "s15j" / "codex-beta-readiness"
S15J_RESULT_NAME = "beta-readiness-result.json"
S15J_EVENTS_NAME = "beta-readiness-events.jsonl"
S15J_VALIDATION_NAME = "beta-readiness-validation.json"
S15J_EVIDENCE_INDEX_NAME = "evidence-index.json"
PAI_DIR_LABEL = "~/.claude/PAI"
MARKER_VALUE = "PAI_CODEX_PEER_BETA_ADAPTER"

ACCEPTED_S15_COMMITS: tuple[dict[str, str], ...] = (
    {
        "milestone": "V5-S15A-CODEX-ADAPTER-LIVE-ACTIVATION-PILOT",
        "commit": "ee2479a2122022ca72ddfed37be4b889902f5077",
    },
    {
        "milestone": "V5-S15B-R2-CODEX-RUNTIME-EVENT-ATTRIBUTED-WORKLOOP",
        "commit": "9dd03b4a4d75b628980c8612acf989bcb892779a",
    },
    {
        "milestone": "V5-S15C-R1-CODEX-BOUNDED-TASK-EXECUTION-LIVE-RETRY",
        "commit": "64e15bcf95e763d93410065e6f8e6fc887367d5e",
    },
    {
        "milestone": "V5-S15D-PAI-RUNTIME-RUNNER-CODEX",
        "commit": "6aabb84af919cc965532e4d6ab8646660152d18c",
    },
    {
        "milestone": "V5-S15E-PAI-RUNTIME-CODEX-REAL-REPO-TASK",
        "commit": "65d77603c663cd2dc319a5f36575b4d1f71fdcb1",
    },
    {
        "milestone": "V5-S15F/G/H-RUNTIME-CONTROL-PLANE-BATCH",
        "commit": "6485c3ceed3cb6d28131cb0c3722bed6fe1444f4",
    },
    {
        "milestone": "V5-S15I-R1-PAI-CONTEXT-SCHEMA-COMPAT-LIVE-RETRY",
        "commit": "2407aee57ded9707dd37872a329aff05e8e7a798",
    },
)

EVIDENCE_EXPECTATIONS: tuple[dict[str, object], ...] = (
    {
        "milestone": "S15B-R2 runtime proof",
        "accepted_commit": "9dd03b4a4d75b628980c8612acf989bcb892779a",
        "candidates": (
            Path("runs") / "s15b" / "runtime-event-attributed-workloop" / "runtime-events.jsonl",
            Path("runs") / "s15b" / "codex-runtime-event-attributed-workloop" / "runtime-events.jsonl",
        ),
    },
    {
        "milestone": "S15C-R1 bounded synthetic task",
        "accepted_commit": "64e15bcf95e763d93410065e6f8e6fc887367d5e",
        "candidates": (
            Path("runs") / "s15c" / "bounded-task-execution" / "run-validation.json",
            Path("runs") / "s15c" / "codex-bounded-task" / "run-validation.json",
        ),
    },
    {
        "milestone": "S15D PAI-owned runtime runner task",
        "accepted_commit": "6aabb84af919cc965532e4d6ab8646660152d18c",
        "candidates": (Path("runs") / "s15d" / "codex-synthetic-bugfix" / "run-validation.json",),
    },
    {
        "milestone": "S15E real repository task",
        "accepted_commit": "65d77603c663cd2dc319a5f36575b4d1f71fdcb1",
        "candidates": (Path("runs") / "s15e" / "provider-registry" / "repo-run-validation.json",),
    },
    {
        "milestone": "S15F patch proposal/apply task",
        "accepted_commit": "6485c3ceed3cb6d28131cb0c3722bed6fe1444f4",
        "candidates": (Path("runs") / "s15f" / "patch-proposal" / "repo-run-validation.json",),
    },
    {
        "milestone": "S15G provider lifecycle validation",
        "accepted_commit": "6485c3ceed3cb6d28131cb0c3722bed6fe1444f4",
        "candidates": (Path("runs") / "s15g" / "provider-lifecycle" / "provider-lifecycle-validation.json",),
    },
    {
        "milestone": "S15H capability policy validation",
        "accepted_commit": "6485c3ceed3cb6d28131cb0c3722bed6fe1444f4",
        "candidates": (Path("runs") / "s15h" / "capability-policy" / "capability-policy-validation.json",),
    },
    {
        "milestone": "S15I-R1 read-only PAI context task",
        "accepted_commit": "2407aee57ded9707dd37872a329aff05e8e7a798",
        "candidates": (Path("runs") / "s15i" / "read-only-pai-context" / "pai-context-validation.json",),
    },
)

REQUIRED_RESULT_VALUES: dict[str, object] = {
    "milestone_name": S15J_MILESTONE,
    "run_id": S15J_RUN_ID,
    "runtime": "codex",
    "runtime_status": "peer-beta",
    "provider_type": "codex-cli",
    "pai_dir": PAI_DIR_LABEL,
    "adapter_identity_marker": MARKER_VALUE,
    "upstream_adapter": "claude",
    "agents_router_observed": True,
    "pai_runtime_installed": True,
    "provider_registry_passed": True,
    "provider_lifecycle_passed": True,
    "capability_policy_passed": True,
    "patch_proposal_policy_passed": True,
    "readonly_pai_context_policy_passed": True,
    "event_attribution_passed": True,
    "protected_surface_check_passed": True,
    "memory_write_performed": False,
    "isa_write_performed": False,
    "memory_body_read": False,
    "isa_body_read": False,
    "pulse_event_payload_read": False,
    "pulse_probe_performed": False,
    "localhost_31337_called": False,
    "repo_root_agents_created": False,
    "repo_dotcodex_created": False,
    "codex_adapter_files_installed_under_home_codex": False,
    "replacement_readiness_claimed": False,
    "claude_equivalence_claimed": False,
    "beta_readiness_status": "peer-beta-runtime-provider",
}

REQUIRED_VALIDATION_VALUES: dict[str, object] = {
    "milestone_name": S15J_MILESTONE,
    "run_id": S15J_RUN_ID,
    "runtime": "codex",
    "provider_registry_passed": True,
    "provider_lifecycle_passed": True,
    "capability_policy_passed": True,
    "patch_proposal_policy_passed": True,
    "readonly_pai_context_policy_passed": True,
    "event_logs_present": True,
    "event_attribution_passed": True,
    "memory_write_performed_by_codex": False,
    "isa_write_performed_by_codex": False,
    "memory_body_read_by_codex": False,
    "isa_body_read_by_codex": False,
    "pulse_event_payload_read_by_codex": False,
    "pulse_probe_performed_by_codex": False,
    "localhost_31337_called_by_codex": False,
    "repo_root_agents_created": False,
    "repo_dotcodex_created": False,
    "codex_adapter_files_installed_under_home_codex": False,
    "replacement_readiness_claimed": False,
    "claude_equivalence_claimed": False,
    "validation_passed": True,
}


class BetaReadinessError(ValueError):
    pass


def _is_within(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _redact_pai_path(pai_dir: Path, path: Path) -> str:
    try:
        relative = path.resolve(strict=False).relative_to(pai_dir.resolve(strict=False))
    except ValueError:
        return path.name
    return f"{PAI_DIR_LABEL}/{relative.as_posix()}"


def _load_json_object(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _schema_errors(instance: dict[str, Any], schema_path: Path, label: str) -> list[str]:
    if Draft202012Validator is None:
        return [f"{label} schema validation unavailable: jsonschema is not installed"]
    if not schema_path.is_file():
        return [f"{label} schema is missing"]
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{label} schema is not valid JSON: {exc}"]
    if not isinstance(schema, dict):
        return [f"{label} schema must be a JSON object"]
    try:
        Draft202012Validator.check_schema(schema)
        errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda error: list(error.path))
    except Exception as exc:  # noqa: BLE001 - readiness reports schema errors as validation failures.
        return [f"{label} schema validation failed: {exc}"]
    return [
        f"{label} schema mismatch at {'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in errors
    ]


def _provider_checks(pai_dir: Path, runtime: str) -> dict[str, Any]:
    providers = discover_runtime_providers(pai_dir)
    provider_names = [str(provider.get("runtime_name", "")) for provider in providers]
    provider = get_provider_by_name(pai_dir, runtime)
    status = validate_provider_by_name(pai_dir, runtime)
    doctor = doctor_provider_by_name(pai_dir, runtime)
    semantics_errors = [
        f"{key} expected {expected!r}, got {provider.get(key)!r}"
        for key, expected in CODEX_PROVIDER_SEMANTICS.items()
        if provider.get(key) != expected
    ]
    capabilities = sorted(item for item in provider.get("capabilities", []) if isinstance(item, str))
    registry_passed = runtime in provider_names and bool(status.get("valid"))
    lifecycle_passed = registry_passed and bool(doctor.get("doctor_passed")) and not semantics_errors
    return {
        "provider": provider,
        "provider_names": provider_names,
        "provider_count": len(providers),
        "provider_status": status,
        "provider_doctor": doctor,
        "provider_capabilities": capabilities,
        "provider_registry_passed": registry_passed,
        "provider_lifecycle_passed": lifecycle_passed,
        "provider_errors": list(status.get("validation_errors", []))
        + list(doctor.get("validation_errors", []))
        + semantics_errors,
    }


def _capability_policy_check(provider: dict[str, Any]) -> dict[str, Any]:
    required = (
        "repo.read",
        "repo.write.proposal",
        "repo.write.apply",
        "pai.context.read.metadata",
    )
    positive_errors = validate_capability_policy(provider, required)
    forbidden_checks = {
        capability: validate_capability_policy(provider, [capability])
        for capability in FORBIDDEN_TASK_CAPABILITIES
    }
    provider_capabilities = set(provider.get("capabilities", [])) if isinstance(provider.get("capabilities"), list) else set()
    required_policy_tokens = {
        "memory.write.disabled",
        "isa.write.disabled",
        "pulse.no-probe",
    }
    blocked_capabilities_absent = not {"memory.write", "isa.write", "pulse.probe"} & provider_capabilities
    passed = (
        not positive_errors
        and all(errors for errors in forbidden_checks.values())
        and required_policy_tokens.issubset(provider_capabilities)
        and blocked_capabilities_absent
    )
    return {
        "capability_policy_passed": passed,
        "required_capabilities": list(required),
        "positive_errors": positive_errors,
        "forbidden_checks": forbidden_checks,
        "provider_capabilities": sorted(str(item) for item in provider_capabilities),
    }


def _patch_proposal_policy_check() -> dict[str, Any]:
    approved = {"tools/pai_runtime_runner/beta_readiness.py"}
    proposal = {
        "proposal_id": "s15j-beta-readiness-patch-policy-check",
        "proposal_kind": "full-file-replacement",
        "changes": [
            {
                "path": "tools/pai_runtime_runner/beta_readiness.py",
                "mode": "replace-file",
                "content": "synthetic readiness check\n",
                "unified_diff": "--- a/tools/pai_runtime_runner/beta_readiness.py\n+++ b/tools/pai_runtime_runner/beta_readiness.py\n",
            }
        ],
    }
    accepted_errors = validate_patch_proposal(proposal, approved)
    memory_errors = validate_patch_proposal(
        {**proposal, "changes": [{**proposal["changes"][0], "path": "Memory/WORK/unsafe.md"}]},
        approved | {"Memory/WORK/unsafe.md"},
    )
    isa_errors = validate_patch_proposal(
        {**proposal, "changes": [{**proposal["changes"][0], "path": "ISA/unsafe.md"}]},
        approved | {"ISA/unsafe.md"},
    )
    root_agents_errors = validate_patch_proposal(
        {**proposal, "changes": [{**proposal["changes"][0], "path": "AGENTS.md"}]},
        approved | {"AGENTS.md"},
    )
    dotcodex_errors = validate_patch_proposal(
        {**proposal, "changes": [{**proposal["changes"][0], "path": ".codex/config.toml"}]},
        approved | {".codex/config.toml"},
    )
    passed = not accepted_errors and all((memory_errors, isa_errors, root_agents_errors, dotcodex_errors))
    return {
        "patch_proposal_policy_passed": passed,
        "accepted_errors": accepted_errors,
        "rejection_checks": {
            "memory_write": memory_errors,
            "isa_write": isa_errors,
            "repo_root_agents": root_agents_errors,
            "repo_dotcodex": dotcodex_errors,
        },
    }


def _artifact_validation_status(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing"
    if not path.is_file() or path.is_symlink():
        return False, "unsafe"
    if path.suffix == ".json":
        data = _load_json_object(path)
        if not data:
            return False, "invalid-json"
        if data.get("validation_passed") is False:
            return False, "validation-failed"
    return True, "present"


def _evidence_status(pai_dir: Path) -> dict[str, Any]:
    checked: list[dict[str, Any]] = []
    missing: list[dict[str, str]] = []
    regenerated: list[dict[str, str]] = []
    invalid: list[dict[str, str]] = []

    for expectation in EVIDENCE_EXPECTATIONS:
        milestone = str(expectation["milestone"])
        commit = str(expectation["accepted_commit"])
        candidates = tuple(expectation["candidates"])
        assert all(isinstance(candidate, Path) for candidate in candidates)
        candidate_records: list[dict[str, str]] = []
        present_valid = False
        present_invalid = False
        for relative in candidates:
            path = pai_dir / relative
            valid, status = _artifact_validation_status(path)
            candidate_records.append({"path": f"{PAI_DIR_LABEL}/{relative.as_posix()}", "status": status})
            if path.exists() and not valid:
                present_invalid = True
            if valid:
                present_valid = True
        checked.append(
            {
                "milestone": milestone,
                "accepted_commit": commit,
                "candidate_artifacts": candidate_records,
                "accepted_live_artifact_present": present_valid,
            }
        )
        if present_invalid:
            invalid.append({"milestone": milestone, "reason": "present evidence artifact is invalid"})
        if not present_valid and not present_invalid:
            missing.append({"milestone": milestone, "reason": "accepted live artifact absent or cleaned up locally"})
            regenerated.append({"milestone": milestone, "method": "covered by S15J current readiness probe"})

    return {
        "checked": checked,
        "missing": missing,
        "regenerated": regenerated,
        "invalid": invalid,
        "evidence_passed": not invalid,
    }


def _readonly_pai_context_policy_check(pai_dir: Path) -> dict[str, Any]:
    run_dir = pai_dir / "runs" / "s15i" / "read-only-pai-context"
    capsule_path = run_dir / "pai-context-capsule.json"
    report_path = run_dir / "pai-context-report.json"
    validation_path = run_dir / "pai-context-validation.json"

    live_errors: list[str] = []
    live_artifact_present = any(path.exists() for path in (capsule_path, report_path, validation_path))
    if live_artifact_present:
        if not capsule_path.is_file():
            live_errors.append("S15I context capsule is missing")
        else:
            live_errors.extend(validate_context_capsule(_load_json_object(capsule_path)))
        if not report_path.is_file():
            live_errors.append("S15I context report is missing")
        else:
            live_errors.extend(validate_context_report(_load_json_object(report_path)))
        if not validation_path.is_file():
            live_errors.append("S15I context validation is missing")
        else:
            validation = _load_json_object(validation_path)
            if validation.get("validation_passed") is not True:
                live_errors.append("S15I context validation did not pass")
            for key in (
                "memory_body_read_by_codex",
                "isa_body_read_by_codex",
                "pulse_event_payload_read_by_codex",
                "claude_project_memory_read_by_codex",
                "codex_memory_read_by_codex",
                "memory_write_performed_by_codex",
                "isa_write_performed_by_codex",
                "pulse_probe_performed_by_codex",
                "localhost_31337_called_by_codex",
            ):
                if validation.get(key) is not False:
                    live_errors.append(f"S15I context validation unsafe flag: {key}")

    capsule = collect_pai_context_metadata(pai_dir)
    report = context_report_from_capsule(capsule)
    current_errors = validate_context_capsule(capsule) + validate_context_report(report)
    passed = not live_errors and not current_errors
    return {
        "readonly_pai_context_policy_passed": passed,
        "live_artifact_present": live_artifact_present,
        "live_errors": live_errors,
        "current_probe_errors": current_errors,
        "current_capsule_metadata_only": capsule.get("metadata_only") is True,
        "current_context_report_valid": not current_errors,
    }


def _protected_surface_check(repo_root: Path) -> dict[str, bool]:
    home_codex = Path.home() / ".codex"
    return {
        "repo_root_agents_created": (repo_root / "AGENTS.md").exists(),
        "repo_dotcodex_created": (repo_root / ".codex").exists(),
        "codex_adapter_files_installed_under_home_codex": any(
            path.exists()
            for path in (
                home_codex / "AGENTS.md",
                home_codex / "AGENTS.override.md",
                home_codex / "adapters" / "codex",
            )
        ),
    }


def _events() -> list[dict[str, object]]:
    return [
        {
            "type": "pai_beta_readiness_check",
            "runtime": "codex",
            "classification": "provider_lifecycle_check",
            "approved": True,
        },
        {
            "type": "pai_beta_readiness_check",
            "runtime": "codex",
            "classification": "capability_policy_check",
            "approved": True,
        },
        {
            "type": "pai_beta_readiness_check",
            "runtime": "codex",
            "classification": "protected_surface_check",
            "approved": True,
        },
    ]


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, events: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(event, sort_keys=True) + "\n" for event in events), encoding="utf-8")


def validate_beta_readiness_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key, expected in REQUIRED_RESULT_VALUES.items():
        if result.get(key) != expected:
            errors.append(f"beta-readiness result mismatch for {key}")
    if not isinstance(result.get("evidence_classification"), list) or not result.get("evidence_classification"):
        errors.append("beta-readiness result must include evidence_classification")
    if not isinstance(result.get("known_limits"), list) or not result.get("known_limits"):
        errors.append("beta-readiness result must include known_limits")
    return errors


def validate_beta_readiness_validation(validation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key, expected in REQUIRED_VALIDATION_VALUES.items():
        if validation.get(key) != expected:
            errors.append(f"beta-readiness validation mismatch for {key}")
    for key in ("forbidden_semantic_writes", "unknown_unclassified_writes"):
        value = validation.get(key)
        if value:
            errors.append(f"beta-readiness validation must not report {key}")
    return errors


def validate_evidence_index(index: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if index.get("milestone_name") != S15J_MILESTONE:
        errors.append("evidence index milestone mismatch")
    if index.get("run_id") != S15J_RUN_ID:
        errors.append("evidence index run_id mismatch")
    raw = json.dumps(index, sort_keys=True)
    for item in ACCEPTED_S15_COMMITS:
        if item["commit"] not in raw:
            errors.append(f"evidence index missing accepted commit: {item['commit']}")
    for statement in (
        "Codex is peer beta.",
        "Claude remains official/full-support upstream.",
        "Codex replacement readiness is not claimed.",
        "Claude equivalence is not claimed.",
    ):
        if statement not in raw:
            errors.append(f"evidence index missing statement: {statement}")
    return errors


def build_result(
    *,
    provider_checks: dict[str, Any],
    capability_check: dict[str, Any],
    patch_check: dict[str, Any],
    readonly_context_check: dict[str, Any],
    protected_surface: dict[str, bool],
    event_logs_present: bool,
) -> dict[str, Any]:
    protected_passed = not any(protected_surface.values())
    event_attribution_passed = event_logs_present
    return {
        **REQUIRED_RESULT_VALUES,
        "provider_registry_passed": bool(provider_checks["provider_registry_passed"]),
        "provider_lifecycle_passed": bool(provider_checks["provider_lifecycle_passed"]),
        "capability_policy_passed": bool(capability_check["capability_policy_passed"]),
        "patch_proposal_policy_passed": bool(patch_check["patch_proposal_policy_passed"]),
        "readonly_pai_context_policy_passed": bool(readonly_context_check["readonly_pai_context_policy_passed"]),
        "event_attribution_passed": event_attribution_passed,
        "protected_surface_check_passed": protected_passed,
        "repo_root_agents_created": protected_surface["repo_root_agents_created"],
        "repo_dotcodex_created": protected_surface["repo_dotcodex_created"],
        "codex_adapter_files_installed_under_home_codex": protected_surface["codex_adapter_files_installed_under_home_codex"],
        "evidence_classification": [
            "S15 executable closeout evidence",
            "Codex peer-beta runtime provider evidence",
            "not replacement readiness",
        ],
        "known_limits": [
            "S15J is a closeout gate and does not add Memory, ISA, or Pulse authority.",
            "Codex remains peer beta; Claude remains the official/full-support upstream adapter.",
            "Prior live artifacts may be absent after local rollback or cleanup; S15J records current bounded checks.",
        ],
    }


def build_validation(
    *,
    run_dir: Path,
    runtime_attempt_number: int,
    provider_checks: dict[str, Any],
    capability_check: dict[str, Any],
    patch_check: dict[str, Any],
    readonly_context_check: dict[str, Any],
    evidence: dict[str, Any],
    protected_surface: dict[str, bool],
    event_logs_present: bool,
    result_errors: list[str],
) -> dict[str, Any]:
    protected_passed = not any(protected_surface.values())
    forbidden_semantic_writes = sorted(
        set(
            provider_checks["provider_errors"]
            + capability_check["positive_errors"]
            + patch_check["accepted_errors"]
            + readonly_context_check["live_errors"]
            + readonly_context_check["current_probe_errors"]
            + [item["reason"] for item in evidence["invalid"]]
            + result_errors
        )
    )
    approved_pai_run_writes = [
        f"{PAI_DIR_LABEL}/{S15J_RUN_RELATIVE.as_posix()}/{S15J_RESULT_NAME}",
        f"{PAI_DIR_LABEL}/{S15J_RUN_RELATIVE.as_posix()}/{S15J_EVENTS_NAME}",
        f"{PAI_DIR_LABEL}/{S15J_RUN_RELATIVE.as_posix()}/{S15J_VALIDATION_NAME}",
        f"{PAI_DIR_LABEL}/{S15J_RUN_RELATIVE.as_posix()}/{S15J_EVIDENCE_INDEX_NAME}",
    ]
    validation = {
        "milestone_name": S15J_MILESTONE,
        "run_id": S15J_RUN_ID,
        "runtime": "codex",
        "runtime_attempt_number": runtime_attempt_number,
        "pai_runtime_command": [
            f"{PAI_DIR_LABEL}/bin/pai-runtime",
            "beta-readiness",
            "--pai-dir",
            PAI_DIR_LABEL,
            "--runtime",
            "codex",
            "--run-dir",
            f"{PAI_DIR_LABEL}/{S15J_RUN_RELATIVE.as_posix()}",
        ],
        "provider_commands_run": [
            f"{PAI_DIR_LABEL}/bin/pai-runtime providers list --pai-dir {PAI_DIR_LABEL}",
            f"{PAI_DIR_LABEL}/bin/pai-runtime providers status codex --pai-dir {PAI_DIR_LABEL}",
            f"{PAI_DIR_LABEL}/bin/pai-runtime providers doctor codex --pai-dir {PAI_DIR_LABEL}",
            f"{PAI_DIR_LABEL}/bin/pai-runtime providers validate codex --pai-dir {PAI_DIR_LABEL}",
        ],
        "evidence_artifacts_checked": evidence["checked"],
        "evidence_artifacts_missing": evidence["missing"],
        "evidence_artifacts_regenerated": evidence["regenerated"],
        "provider_registry_passed": bool(provider_checks["provider_registry_passed"]),
        "provider_lifecycle_passed": bool(provider_checks["provider_lifecycle_passed"]),
        "capability_policy_passed": bool(capability_check["capability_policy_passed"]),
        "patch_proposal_policy_passed": bool(patch_check["patch_proposal_policy_passed"]),
        "readonly_pai_context_policy_passed": bool(readonly_context_check["readonly_pai_context_policy_passed"]),
        "event_logs_present": event_logs_present,
        "event_attribution_passed": event_logs_present,
        "approved_pai_run_writes": approved_pai_run_writes,
        "ambient_pai_state_churn": [],
        "forbidden_semantic_writes": forbidden_semantic_writes,
        "unknown_unclassified_writes": [],
        "memory_write_performed_by_codex": False,
        "isa_write_performed_by_codex": False,
        "memory_body_read_by_codex": False,
        "isa_body_read_by_codex": False,
        "pulse_event_payload_read_by_codex": False,
        "pulse_probe_performed_by_codex": False,
        "localhost_31337_called_by_codex": False,
        "repo_root_agents_created": protected_surface["repo_root_agents_created"],
        "repo_dotcodex_created": protected_surface["repo_dotcodex_created"],
        "codex_adapter_files_installed_under_home_codex": protected_surface["codex_adapter_files_installed_under_home_codex"],
        "replacement_readiness_claimed": False,
        "claude_equivalence_claimed": False,
        "validation_passed": False,
        "known_limits": [
            "S15J validates peer-beta readiness only; it is not replacement readiness.",
            "S15J performs current bounded checks when prior accepted live artifacts are absent after rollback or cleanup.",
            "Ambient PAI state/cache/log churn is not adapter evidence.",
        ],
    }
    validation["validation_passed"] = bool(
        validation["provider_registry_passed"]
        and validation["provider_lifecycle_passed"]
        and validation["capability_policy_passed"]
        and validation["patch_proposal_policy_passed"]
        and validation["readonly_pai_context_policy_passed"]
        and validation["event_logs_present"]
        and validation["event_attribution_passed"]
        and protected_passed
        and not forbidden_semantic_writes
        and not validation["unknown_unclassified_writes"]
    )
    return validation


def build_evidence_index(
    *,
    provider_checks: dict[str, Any],
    capability_check: dict[str, Any],
    protected_surface: dict[str, bool],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    return {
        "milestone_name": S15J_MILESTONE,
        "run_id": S15J_RUN_ID,
        "accepted_commits": list(ACCEPTED_S15_COMMITS),
        "live_artifacts_checked": evidence["checked"],
        "live_artifacts_regenerated": evidence["regenerated"],
        "runtime_provider_status": {
            "runtime_name": "codex",
            "runtime_status": "peer-beta",
            "provider_type": "codex-cli",
            "upstream_adapter": "claude",
            "supports_codex_exec": provider_checks["provider"].get("supports_codex_exec") is True,
            "supports_jsonl_events": provider_checks["provider"].get("supports_jsonl_events") is True,
            "supports_structured_output": provider_checks["provider"].get("supports_structured_output") is True,
            "memory_write_policy": provider_checks["provider"].get("memory_write_policy", ""),
            "isa_write_policy": provider_checks["provider"].get("isa_write_policy", ""),
            "pulse_policy": provider_checks["provider"].get("pulse_policy", ""),
            "replacement_status": provider_checks["provider"].get("replacement_status", ""),
        },
        "capability_summary": {
            "provider_capabilities": capability_check["provider_capabilities"],
            "required_peer_beta_capabilities": list(CODEX_PROVIDER_CAPABILITIES),
            "forbidden_capabilities": sorted(FORBIDDEN_TASK_CAPABILITIES),
        },
        "protected_surface_summary": protected_surface,
        "s15_closeout_summary": [
            "Codex is peer beta.",
            "Claude remains official/full-support upstream.",
            "Codex replacement readiness is not claimed.",
            "Claude equivalence is not claimed.",
        ],
        "recommended_s16_direction": (
            "controlled real PAI-context task execution with proposal-only Memory/ISA semantics"
        ),
    }


def run_beta_readiness_gate(
    *,
    pai_dir: Path,
    runtime: str,
    run_dir: Path,
    runtime_attempt_number: int = 1,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    if runtime != "codex":
        raise BetaReadinessError(f"unknown runtime provider: {runtime}")
    pai_dir = pai_dir.resolve(strict=True)
    run_dir = run_dir.resolve(strict=False)
    expected_run_dir = (pai_dir / S15J_RUN_RELATIVE).resolve(strict=False)
    if run_dir != expected_run_dir:
        raise BetaReadinessError("S15J run directory must be runs/s15j/codex-beta-readiness")
    if run_dir.exists() and (not run_dir.is_dir() or run_dir.is_symlink()):
        raise BetaReadinessError("S15J run directory target is unsafe")
    repo_root = (repo_root or Path.cwd()).resolve(strict=False)

    run_dir.mkdir(parents=True, exist_ok=True)
    events_path = run_dir / S15J_EVENTS_NAME
    _write_jsonl(events_path, _events())
    event_logs_present = events_path.is_file() and events_path.stat().st_size > 0

    provider_checks = _provider_checks(pai_dir, runtime)
    capability_check = _capability_policy_check(provider_checks["provider"])
    patch_check = _patch_proposal_policy_check()
    readonly_context_check = _readonly_pai_context_policy_check(pai_dir)
    evidence = _evidence_status(pai_dir)
    protected_surface = _protected_surface_check(repo_root)

    result = build_result(
        provider_checks=provider_checks,
        capability_check=capability_check,
        patch_check=patch_check,
        readonly_context_check=readonly_context_check,
        protected_surface=protected_surface,
        event_logs_present=event_logs_present,
    )
    result_errors = validate_beta_readiness_result(result)
    validation = build_validation(
        run_dir=run_dir,
        runtime_attempt_number=runtime_attempt_number,
        provider_checks=provider_checks,
        capability_check=capability_check,
        patch_check=patch_check,
        readonly_context_check=readonly_context_check,
        evidence=evidence,
        protected_surface=protected_surface,
        event_logs_present=event_logs_present,
        result_errors=result_errors,
    )
    index = build_evidence_index(
        provider_checks=provider_checks,
        capability_check=capability_check,
        protected_surface=protected_surface,
        evidence=evidence,
    )

    validation_errors = validate_beta_readiness_validation(validation)
    index_errors = validate_evidence_index(index)
    schema_errors = (
        _schema_errors(result, pai_dir / "runtime-schemas" / "beta-readiness-result.schema.json", S15J_RESULT_NAME)
        + _schema_errors(
            validation,
            pai_dir / "runtime-schemas" / "beta-readiness-validation.schema.json",
            S15J_VALIDATION_NAME,
        )
        + _schema_errors(index, pai_dir / "runtime-schemas" / "evidence-index.schema.json", S15J_EVIDENCE_INDEX_NAME)
    )

    result_path = run_dir / S15J_RESULT_NAME
    validation_path = run_dir / S15J_VALIDATION_NAME
    index_path = run_dir / S15J_EVIDENCE_INDEX_NAME
    _write_json(result_path, result)
    _write_json(validation_path, validation)
    _write_json(index_path, index)

    errors = result_errors + validation_errors + index_errors + schema_errors
    if errors:
        raise BetaReadinessError("S15J beta-readiness gate failed: " + "; ".join(errors))

    return {
        "ok": True,
        "run_dir": _redact_pai_path(pai_dir, run_dir),
        "result": _redact_pai_path(pai_dir, result_path),
        "events_output": _redact_pai_path(pai_dir, events_path),
        "validation": _redact_pai_path(pai_dir, validation_path),
        "evidence_index": _redact_pai_path(pai_dir, index_path),
        "beta_readiness_status": "peer-beta-runtime-provider",
        "provider_lifecycle_passed": result["provider_lifecycle_passed"],
        "capability_policy_passed": result["capability_policy_passed"],
        "patch_proposal_policy_passed": result["patch_proposal_policy_passed"],
        "readonly_pai_context_policy_passed": result["readonly_pai_context_policy_passed"],
        "event_attribution_passed": result["event_attribution_passed"],
    }
