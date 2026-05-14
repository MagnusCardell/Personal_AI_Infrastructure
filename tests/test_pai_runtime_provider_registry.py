from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.pai_runtime_runner.provider_registry import (
    CODEX_PROVIDER_SEMANTICS,
    EXPECTED_CODEX_SEMANTIC_FIELDS,
    ProviderRegistryError,
    discover_runtime_providers,
    get_provider_by_name,
    load_provider_manifest,
    validate_provider_manifest,
)


class PaiRuntimeProviderRegistryTests(unittest.TestCase):
    def _pai_root_with_codex_manifest(self, tmp: str, manifest: dict[str, object] | None = None) -> Path:
        pai_root = Path(tmp) / "PAI"
        manifest_path = pai_root / "runtimes" / "codex" / "provider-manifest.json"
        manifest_path.parent.mkdir(parents=True)
        manifest_path.write_text(
            json.dumps(manifest or CODEX_PROVIDER_SEMANTICS, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return pai_root

    def test_discover_runtime_providers_finds_codex_manifest(self):
        with tempfile.TemporaryDirectory(prefix="s15e.registry.") as tmp:
            pai_root = self._pai_root_with_codex_manifest(tmp)
            providers = discover_runtime_providers(pai_root)
            self.assertEqual(len(providers), 1)
            self.assertEqual(providers[0]["runtime_name"], "codex")

    def test_get_provider_by_name_returns_codex(self):
        with tempfile.TemporaryDirectory(prefix="s15e.registry.") as tmp:
            pai_root = self._pai_root_with_codex_manifest(tmp)
            provider = get_provider_by_name(pai_root, "codex")
            self.assertEqual(provider["provider_type"], "codex-cli")
            self.assertEqual(provider["runtime_status"], "peer-beta")

    def test_get_provider_by_name_rejects_missing_provider(self):
        with tempfile.TemporaryDirectory(prefix="s15e.registry.") as tmp:
            pai_root = self._pai_root_with_codex_manifest(tmp)
            with self.assertRaises(ProviderRegistryError):
                get_provider_by_name(pai_root, "missing")

    def test_validate_provider_manifest_accepts_peer_beta_codex(self):
        self.assertEqual(validate_provider_manifest(dict(CODEX_PROVIDER_SEMANTICS)), [])

    def test_expected_codex_semantic_fields_cover_guard_fields(self):
        self.assertEqual(EXPECTED_CODEX_SEMANTIC_FIELDS, tuple(CODEX_PROVIDER_SEMANTICS))
        for field in (
            "memory_write_policy",
            "isa_write_policy",
            "pulse_policy",
            "replacement_status",
        ):
            self.assertIn(field, EXPECTED_CODEX_SEMANTIC_FIELDS)

    def test_validate_provider_manifest_rejects_replacement_status(self):
        manifest = dict(CODEX_PROVIDER_SEMANTICS)
        manifest["replacement_status"] = "replacement-grade"
        errors = validate_provider_manifest(manifest)
        self.assertTrue(any("replacement_status" in error for error in errors))

    def test_validate_provider_manifest_rejects_memory_write_enabled(self):
        manifest = dict(CODEX_PROVIDER_SEMANTICS)
        manifest["memory_write_policy"] = "enabled"
        errors = validate_provider_manifest(manifest)
        self.assertTrue(any("memory_write_policy" in error for error in errors))

    def test_validate_provider_manifest_rejects_isa_write_enabled(self):
        manifest = dict(CODEX_PROVIDER_SEMANTICS)
        manifest["isa_write_policy"] = "enabled"
        errors = validate_provider_manifest(manifest)
        self.assertTrue(any("isa_write_policy" in error for error in errors))

    def test_validate_provider_manifest_rejects_pulse_probe_policy(self):
        manifest = dict(CODEX_PROVIDER_SEMANTICS)
        manifest["pulse_policy"] = "probe"
        errors = validate_provider_manifest(manifest)
        self.assertTrue(any("pulse_policy" in error for error in errors))

    def test_load_provider_manifest_rejects_non_object(self):
        with tempfile.TemporaryDirectory(prefix="s15e.registry.") as tmp:
            path = Path(tmp) / "provider-manifest.json"
            path.write_text("[]\n", encoding="utf-8")
            with self.assertRaises(ProviderRegistryError):
                load_provider_manifest(path)


if __name__ == "__main__":
    unittest.main()
