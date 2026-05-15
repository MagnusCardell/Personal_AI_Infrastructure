from __future__ import annotations

from typing import Any, Iterable


PROVIDER_CAPABILITIES_FIELD = "capabilities"
TASK_REQUIRED_CAPABILITIES_FIELD = "required_capabilities"

CODEX_PROVIDER_CAPABILITIES: tuple[str, ...] = (
    "repo.read",
    "repo.write.proposal",
    "repo.write.apply",
    "pai.context.read.metadata",
    "memory.write.disabled",
    "isa.write.disabled",
    "pulse.no-probe",
)

CODEX_S16A_PROVIDER_CAPABILITIES: tuple[str, ...] = (
    *CODEX_PROVIDER_CAPABILITIES,
    "memory.write.proposal",
    "isa.write.proposal",
)

PATCH_PROPOSAL_REPO_TASK_CAPABILITIES: tuple[str, ...] = (
    "repo.read",
    "repo.write.proposal",
    "repo.write.apply",
)

MATERIALIZED_REPO_TASK_CAPABILITIES: tuple[str, ...] = (
    "repo.read",
    "repo.write.apply",
)

PAI_CONTEXT_TASK_CAPABILITIES: tuple[str, ...] = (
    "pai.context.read.metadata",
)

STATE_PROPOSAL_TASK_CAPABILITIES: tuple[str, ...] = (
    "pai.context.read.metadata",
    "memory.write.proposal",
    "isa.write.proposal",
)

FORBIDDEN_TASK_CAPABILITIES: dict[str, str] = {
    "memory.write": "runtime provider declares memory.write.disabled",
    "isa.write": "runtime provider declares isa.write.disabled",
    "memory.write.commit": "S16A permits proposal-only Memory semantics, not Memory commits",
    "isa.write.commit": "S16A permits proposal-only ISA semantics, not ISA commits",
    "pulse.probe": "runtime provider declares pulse.no-probe",
    "pulse.emit": "S16A does not authorize Pulse event emission",
}


class CapabilityPolicyError(ValueError):
    pass


def _string_set(value: Iterable[str], label: str) -> set[str]:
    capabilities: set[str] = set()
    for item in value:
        if not isinstance(item, str) or item == "" or "\x00" in item:
            raise CapabilityPolicyError(f"{label} must contain only non-empty strings")
        capabilities.add(item)
    return capabilities


def provider_capabilities(manifest: dict[str, Any]) -> set[str]:
    raw = manifest.get(PROVIDER_CAPABILITIES_FIELD)
    if not isinstance(raw, list):
        raise CapabilityPolicyError("provider manifest capabilities must be a list")
    if not all(isinstance(item, str) for item in raw):
        raise CapabilityPolicyError("provider manifest capabilities must contain only strings")
    return _string_set(raw, "provider manifest capabilities")


def task_required_capabilities(task: dict[str, Any], inferred: Iterable[str] = ()) -> set[str]:
    required = _string_set(inferred, "inferred required capabilities")
    raw = task.get(TASK_REQUIRED_CAPABILITIES_FIELD)
    if raw is None:
        return required
    if not isinstance(raw, list):
        raise CapabilityPolicyError("task required_capabilities must be a list")
    required.update(_string_set(raw, "task required_capabilities"))
    return required


def validate_capability_policy(manifest: dict[str, Any], required: Iterable[str]) -> list[str]:
    errors: list[str] = []
    try:
        provider = provider_capabilities(manifest)
        required_set = _string_set(required, "required capabilities")
    except CapabilityPolicyError as exc:
        return [str(exc)]

    for capability in sorted(required_set):
        if capability in FORBIDDEN_TASK_CAPABILITIES:
            errors.append(f"required capability {capability!r} is forbidden: {FORBIDDEN_TASK_CAPABILITIES[capability]}")
    missing = sorted(required_set - provider)
    for capability in missing:
        errors.append(f"runtime provider missing required capability: {capability}")
    return errors


def enforce_capability_policy(manifest: dict[str, Any], required: Iterable[str]) -> None:
    errors = validate_capability_policy(manifest, required)
    if errors:
        raise CapabilityPolicyError("; ".join(errors))
