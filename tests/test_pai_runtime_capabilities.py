from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.pai_runtime_runner.audit import audit_capability_policy
from tools.pai_runtime_runner.capabilities import (
    CODEX_PROVIDER_CAPABILITIES,
    CapabilityPolicyError,
    provider_capabilities,
    validate_capability_policy,
)
from tools.pai_runtime_runner.install import install_runtime
from tools.pai_runtime_runner.runner import (
    S15F_RUN_RELATIVE,
    S15F_TASK_RELATIVE,
    TASK_RELATIVE,
    audit_capability_policy_run,
    run_repo_runtime,
    run_runtime,
)


class PaiRuntimeCapabilityPolicyTests(unittest.TestCase):
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

    def _install_synthetic(self, tmp: str) -> Path:
        pai_dir, backup_root = self._synthetic_layout(tmp)
        install_runtime(pai_dir, backup_root)
        return pai_dir

    def _git_repo(self, tmp: str) -> Path:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return repo

    def _write_required_capabilities(self, task_path: Path, capabilities: list[str]) -> None:
        task = json.loads(task_path.read_text(encoding="utf-8"))
        task["required_capabilities"] = capabilities
        task_path.write_text(json.dumps(task, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def test_codex_manifest_declares_required_capabilities(self):
        manifest = json.loads(Path("runtimes/codex/provider-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(provider_capabilities(manifest), set(CODEX_PROVIDER_CAPABILITIES))

    def test_capability_policy_accepts_codex_repo_proposal_apply(self):
        manifest = json.loads(Path("runtimes/codex/provider-manifest.json").read_text(encoding="utf-8"))
        errors = validate_capability_policy(manifest, ["repo.read", "repo.write.proposal", "repo.write.apply"])
        self.assertEqual(errors, [])

    def test_capability_policy_rejects_memory_write(self):
        manifest = json.loads(Path("runtimes/codex/provider-manifest.json").read_text(encoding="utf-8"))
        errors = validate_capability_policy(manifest, ["memory.write"])
        self.assertTrue(errors)
        self.assertTrue(any("memory.write" in error for error in errors))

    def test_capability_policy_rejects_isa_write(self):
        manifest = json.loads(Path("runtimes/codex/provider-manifest.json").read_text(encoding="utf-8"))
        errors = validate_capability_policy(manifest, ["isa.write"])
        self.assertTrue(errors)
        self.assertTrue(any("isa.write" in error for error in errors))

    def test_capability_policy_rejects_pulse_probe(self):
        manifest = json.loads(Path("runtimes/codex/provider-manifest.json").read_text(encoding="utf-8"))
        errors = validate_capability_policy(manifest, ["pulse.probe"])
        self.assertTrue(errors)
        self.assertTrue(any("pulse.probe" in error for error in errors))

    def test_run_repo_accepts_patch_proposal_apply_capabilities(self):
        with tempfile.TemporaryDirectory(prefix="s15h.capabilities.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            repo = self._git_repo(tmp)
            task_path = pai_dir / S15F_TASK_RELATIVE
            self._write_required_capabilities(task_path, ["repo.read", "repo.write.proposal", "repo.write.apply"])
            result = run_repo_runtime(
                pai_dir,
                "codex",
                task_path,
                repo,
                pai_dir / S15F_RUN_RELATIVE,
                dry_run=True,
            )
            self.assertEqual(
                result["required_capabilities"],
                ["repo.read", "repo.write.apply", "repo.write.proposal"],
            )

    def test_run_repo_refuses_memory_write_capability(self):
        with tempfile.TemporaryDirectory(prefix="s15h.capabilities.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            repo = self._git_repo(tmp)
            task_path = pai_dir / S15F_TASK_RELATIVE
            self._write_required_capabilities(task_path, ["memory.write"])
            with self.assertRaises(CapabilityPolicyError):
                run_repo_runtime(pai_dir, "codex", task_path, repo, pai_dir / S15F_RUN_RELATIVE, dry_run=True)

    def test_run_repo_refuses_isa_write_capability(self):
        with tempfile.TemporaryDirectory(prefix="s15h.capabilities.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            repo = self._git_repo(tmp)
            task_path = pai_dir / S15F_TASK_RELATIVE
            self._write_required_capabilities(task_path, ["isa.write"])
            with self.assertRaises(CapabilityPolicyError):
                run_repo_runtime(pai_dir, "codex", task_path, repo, pai_dir / S15F_RUN_RELATIVE, dry_run=True)

    def test_run_repo_refuses_pulse_probe_capability(self):
        with tempfile.TemporaryDirectory(prefix="s15h.capabilities.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            repo = self._git_repo(tmp)
            task_path = pai_dir / S15F_TASK_RELATIVE
            self._write_required_capabilities(task_path, ["pulse.probe"])
            with self.assertRaises(CapabilityPolicyError):
                run_repo_runtime(pai_dir, "codex", task_path, repo, pai_dir / S15F_RUN_RELATIVE, dry_run=True)

    def test_synthetic_runtime_refuses_forbidden_capability(self):
        with tempfile.TemporaryDirectory(prefix="s15h.capabilities.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            task_path = pai_dir / TASK_RELATIVE
            self._write_required_capabilities(task_path, ["memory.write"])
            with self.assertRaises(CapabilityPolicyError):
                run_runtime(
                    pai_dir,
                    "codex",
                    task_path,
                    pai_dir / "runs" / "s15d" / "codex-synthetic-bugfix",
                    dry_run=True,
                )

    def test_capability_policy_audit_passes_without_writes(self):
        with tempfile.TemporaryDirectory(prefix="s15h.capabilities.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            repo = self._git_repo(tmp)
            marker = Path(tmp) / "marker"
            marker.write_text("marker\n", encoding="utf-8")
            result = audit_capability_policy(pai_dir=pai_dir, marker=marker, repo_root=repo, runtime_name="codex")
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["positive_capabilities_passed"])
            self.assertTrue(result["forbidden_capabilities_rejected"])

    def test_capability_policy_audit_run_writes_validation_artifact(self):
        with tempfile.TemporaryDirectory(prefix="s15h.capabilities.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            repo = self._git_repo(tmp)
            marker = Path(tmp) / "marker"
            marker.write_text("marker\n", encoding="utf-8")
            output = pai_dir / "runs" / "s15h" / "capability-policy" / "capability-policy-validation.json"
            result = audit_capability_policy_run(pai_dir, marker, repo, output, "codex")
            self.assertTrue(result["validation_passed"])
            validation = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(validation["milestone_name"], "V5-S15H-PAI-RUNTIME-CAPABILITY-POLICY")


if __name__ == "__main__":
    unittest.main()
