from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CODEX_PROVIDER_SEMANTICS: dict[str, object] = {
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

EXPECTED_CODEX_SEMANTIC_FIELDS: tuple[str, ...] = tuple(CODEX_PROVIDER_SEMANTICS)

REQUIRED_PROVIDER_FIELDS = (
    "runtime_name",
    "runtime_status",
    "provider_type",
    "upstream_adapter",
)


class ProviderRegistryError(ValueError):
    pass


def load_provider_manifest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ProviderRegistryError(f"provider manifest is missing: {path}")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ProviderRegistryError(f"provider manifest is not valid JSON: {path}") from exc
    if not isinstance(manifest, dict):
        raise ProviderRegistryError(f"provider manifest must be a JSON object: {path}")
    return manifest


def validate_provider_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["provider manifest must be a JSON object"]

    for field in REQUIRED_PROVIDER_FIELDS:
        value = manifest.get(field)
        if not isinstance(value, str) or value == "":
            errors.append(f"{field} must be a non-empty string")

    if manifest.get("runtime_name") != "codex":
        return errors

    for field in EXPECTED_CODEX_SEMANTIC_FIELDS:
        expected = CODEX_PROVIDER_SEMANTICS[field]
        actual = manifest.get(field)
        if actual != expected:
            errors.append(f"{field} must be {expected!r}, got {actual!r}")
    return errors


def discover_runtime_providers(pai_root: Path) -> list[dict[str, Any]]:
    runtimes_dir = Path(pai_root) / "runtimes"
    if not runtimes_dir.is_dir():
        return []

    providers: list[dict[str, Any]] = []
    for manifest_path in sorted(runtimes_dir.glob("*/provider-manifest.json")):
        manifest = load_provider_manifest(manifest_path)
        errors = validate_provider_manifest(manifest)
        if errors:
            joined = "; ".join(errors)
            raise ProviderRegistryError(f"invalid provider manifest {manifest_path}: {joined}")
        providers.append(manifest)

    return sorted(providers, key=lambda item: str(item.get("runtime_name", "")))


def get_provider_by_name(pai_root: Path, runtime_name: str) -> dict[str, Any]:
    if runtime_name == "":
        raise ProviderRegistryError("runtime_name must not be empty")
    for provider in discover_runtime_providers(pai_root):
        if provider.get("runtime_name") == runtime_name:
            return provider
    raise ProviderRegistryError(f"runtime provider not found: {runtime_name}")
