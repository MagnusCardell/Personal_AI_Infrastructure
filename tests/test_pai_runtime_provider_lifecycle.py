from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.pai_runtime_runner.audit import audit_provider_lifecycle
from tools.pai_runtime_runner.install import install_runtime
from tools.pai_runtime_runner.runner import (
    audit_provider_lifecycle_run,
    doctor,
    provider_lifecycle_doctor,
    provider_lifecycle_list,
    provider_lifecycle_status,
    provider_lifecycle_validate,
)


MARKER = "PAI_CODEX_PEER_BETA_ADAPTER"


class PaiRuntimeProviderLifecycleTests(unittest.TestCase):
    def _synthetic_layout(self, tmp: str) -> tuple[Path, Path]:
        base = Path(tmp)
        pai_dir = base / "home" / ".claude" / "PAI"
        pai_dir.mkdir(parents=True)
        (pai_dir / "AGENTS.md").write_text(
            "PAI_CODEX_PEER_BETA_ADAPTER\n"
            "Codex is a peer beta adapter for PAI v5.\n"
            "Claude remains the official/full-support upstream adapter.\n",
            encoding="utf-8",
        )
        backup_root = base / "backup"
        (backup_root / ".claude" / "PAI").mkdir(parents=True)
        return pai_dir, backup_root

    def _install_synthetic(self, tmp: str) -> tuple[Path, Path]:
        pai_dir, backup_root = self._synthetic_layout(tmp)
        install_runtime(pai_dir, backup_root)
        return pai_dir, pai_dir / "bin" / "pai-runtime"

    def _git_repo(self, tmp: str) -> Path:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return repo

    def _run_launcher(self, launcher: Path, *args: str) -> dict[str, object]:
        completed = subprocess.run(
            [str(launcher), *args],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        return json.loads(completed.stdout)

    def test_provider_lifecycle_list_uses_registry_discovery(self):
        with tempfile.TemporaryDirectory(prefix="s15g.providers.") as tmp:
            pai_dir, _ = self._install_synthetic(tmp)
            result = provider_lifecycle_list(pai_dir)
            self.assertTrue(result["provider_registry_used"])
            self.assertEqual(result["provider_count"], 1)
            self.assertEqual(result["providers"][0]["runtime_name"], "codex")
            self.assertEqual(result["providers"][0]["runtime_status"], "peer-beta")

    def test_provider_lifecycle_status_reports_codex_manifest(self):
        with tempfile.TemporaryDirectory(prefix="s15g.providers.") as tmp:
            pai_dir, _ = self._install_synthetic(tmp)
            result = provider_lifecycle_status(pai_dir, "codex")
            self.assertTrue(result["provider_registry_used"])
            self.assertEqual(result["provider"]["provider_type"], "codex-cli")
            self.assertEqual(result["provider"]["upstream_adapter"], "claude")

    def test_provider_lifecycle_validate_accepts_codex_manifest(self):
        with tempfile.TemporaryDirectory(prefix="s15g.providers.") as tmp:
            pai_dir, _ = self._install_synthetic(tmp)
            result = provider_lifecycle_validate(pai_dir, "codex")
            self.assertTrue(result["valid"])
            self.assertEqual(result["validation_errors"], [])
            self.assertTrue(result["manifest_path"].endswith("runtimes/codex/provider-manifest.json"))

    def test_provider_lifecycle_doctor_checks_manifest_driver(self):
        with tempfile.TemporaryDirectory(prefix="s15g.providers.") as tmp:
            pai_dir, _ = self._install_synthetic(tmp)
            result = provider_lifecycle_doctor(pai_dir, "codex")
            self.assertTrue(result["doctor_passed"])
            self.assertTrue(Path(result["driver_path"]).is_file())

    def test_pai_runtime_doctor_uses_provider_registry(self):
        with tempfile.TemporaryDirectory(prefix="s15g.providers.") as tmp:
            pai_dir, _ = self._install_synthetic(tmp)
            result = doctor(pai_dir)
            self.assertTrue(result["provider_registry_used"])
            self.assertTrue(result["adapter_identity_marker_observed"])

    def test_installed_cli_provider_lifecycle_commands(self):
        with tempfile.TemporaryDirectory(prefix="s15g.providers.") as tmp:
            pai_dir, launcher = self._install_synthetic(tmp)
            listed = self._run_launcher(launcher, "providers", "list", "--pai-dir", str(pai_dir))
            status = self._run_launcher(launcher, "providers", "status", "codex", "--pai-dir", str(pai_dir))
            checked = self._run_launcher(launcher, "providers", "doctor", "codex", "--pai-dir", str(pai_dir))
            validated = self._run_launcher(launcher, "providers", "validate", "codex", "--pai-dir", str(pai_dir))
            self.assertEqual(listed["providers"][0]["runtime_name"], "codex")
            self.assertEqual(status["provider"]["runtime_status"], "peer-beta")
            self.assertTrue(checked["doctor_passed"])
            self.assertTrue(validated["valid"])

    def test_provider_lifecycle_validate_rejects_invalid_manifest(self):
        with tempfile.TemporaryDirectory(prefix="s15g.providers.") as tmp:
            pai_dir, _ = self._install_synthetic(tmp)
            manifest_path = pai_dir / "runtimes" / "codex" / "provider-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["pulse_policy"] = "probe"
            manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                provider_lifecycle_validate(pai_dir, "codex")

    def test_provider_lifecycle_audit_passes_without_writes(self):
        with tempfile.TemporaryDirectory(prefix="s15g.providers.") as tmp:
            pai_dir, _ = self._install_synthetic(tmp)
            repo = self._git_repo(tmp)
            marker = Path(tmp) / "marker"
            marker.write_text("marker\n", encoding="utf-8")
            provider_lifecycle_list(pai_dir)
            provider_lifecycle_status(pai_dir, "codex")
            provider_lifecycle_doctor(pai_dir, "codex")
            provider_lifecycle_validate(pai_dir, "codex")
            result = audit_provider_lifecycle(pai_dir=pai_dir, marker=marker, repo_root=repo, runtime_name="codex")
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["event_attribution_passed"])
            self.assertEqual(result["forbidden_repository_writes"], [])
            self.assertEqual(result["forbidden_semantic_writes"], [])

    def test_provider_lifecycle_audit_run_writes_validation_artifact(self):
        with tempfile.TemporaryDirectory(prefix="s15g.providers.") as tmp:
            pai_dir, _ = self._install_synthetic(tmp)
            repo = self._git_repo(tmp)
            marker = Path(tmp) / "marker"
            marker.write_text("marker\n", encoding="utf-8")
            output = pai_dir / "runs" / "s15g" / "provider-lifecycle" / "provider-lifecycle-validation.json"
            result = audit_provider_lifecycle_run(pai_dir, marker, repo, output, "codex")
            self.assertTrue(result["validation_passed"])
            self.assertTrue(output.is_file())
            validation = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(validation["milestone_name"], "V5-S15G-PAI-RUNTIME-PROVIDER-LIFECYCLE")


if __name__ == "__main__":
    unittest.main()
