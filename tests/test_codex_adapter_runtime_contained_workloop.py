from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.codex_adapter_installer.install import (
    apply_install,
    read_staged_agents,
    validate_install,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SCHEMA = REPO_ROOT / "adapters" / "codex" / "runtime-proof.schema.json"
WORKLOOP_SCHEMA = REPO_ROOT / "adapters" / "codex" / "workloop-once.schema.json"


class CodexAdapterRuntimeContainedWorkloopTests(unittest.TestCase):
    def _synthetic_layout(self, tmp: str) -> tuple[Path, Path]:
        base = Path(tmp)
        pai_dir = base / "home" / ".claude" / "PAI"
        pai_dir.mkdir(parents=True)
        backup_root = base / "backup"
        (backup_root / ".claude" / "PAI").mkdir(parents=True)
        return pai_dir, backup_root

    def _install_synthetic(self, tmp: str) -> tuple[Path, Path, Path]:
        pai_dir, backup_root = self._synthetic_layout(tmp)
        apply_install(pai_dir, backup_root)
        launcher = pai_dir / "adapters" / "codex" / "bin" / "pai-codex"
        return pai_dir, backup_root, launcher

    def _run_launcher(self, launcher: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(launcher), *args],
            check=check,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def _dry_run(self, launcher: Path, command: str, pai_dir: Path, output_name: str) -> dict[str, object]:
        output = pai_dir / "adapters" / "codex" / "runs" / "s15b-r1" / output_name
        result = self._run_launcher(
            launcher,
            command,
            "--pai-dir",
            str(pai_dir),
            "--output",
            str(output),
            "--dry-run",
        )
        return json.loads(result.stdout)

    def _assert_schema_accepts(self, schema_path: Path, artifact: dict[str, object]) -> None:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        for field in schema["required"]:
            self.assertIn(field, artifact)
        for field, spec in schema["properties"].items():
            if "const" in spec and field in artifact:
                self.assertEqual(artifact[field], spec["const"])
            if spec.get("type") == "boolean" and field in artifact:
                self.assertIs(type(artifact[field]), bool)
            if spec.get("type") == "array" and field in artifact:
                self.assertIsInstance(artifact[field], list)
            if spec.get("type") == "string" and field in artifact:
                self.assertIsInstance(artifact[field], str)

    def test_router_contains_runtime_identity_marker(self):
        router = read_staged_agents()
        for text in [
            "PAI_CODEX_PEER_BETA_ADAPTER",
            "Codex is a peer beta adapter for PAI v5.",
            "Claude remains the official/full-support upstream adapter.",
            "PAI v5 is a Life OS, not just Claude config.",
            "PAI_DIR is the v5 PAI subsystem root, usually ~/.claude/PAI.",
            "PAI_SYSTEM_PROMPT.md is a high-authority instruction layer.",
            "AGENTS.md is a router into PAI v5, not a clone of CLAUDE.md.",
        ]:
            self.assertIn(text, router)
        for forbidden in [
            "Codex is replacement-grade",
            "Codex replaces Claude",
            "Codex may write Memory",
            "Codex may write ISA",
            "Codex may probe Pulse",
        ]:
            self.assertNotIn(forbidden, router)

    def test_runtime_schema_accepts_required_proof_shape(self):
        artifact = {
            "milestone_name": "V5-S15B-R1-CODEX-RUNTIME-CONTAINED-WORKLOOP",
            "runtime_invocation": "codex exec --sandbox read-only --ephemeral --cd PAI_DIR",
            "pai_dir": "/tmp/pai",
            "adapter_identity_marker": "PAI_CODEX_PEER_BETA_ADAPTER",
            "adapter_status": "peer-beta",
            "upstream_adapter": "claude",
            "agents_router_observed": True,
            "pai_system_prompt_policy_observed": True,
            "memory_write_performed": False,
            "isa_write_performed": False,
            "pulse_probe_performed": False,
            "localhost_31337_called": False,
            "runtime_surface_created": False,
            "evidence_classification": ["runtime proof evidence", "not replacement readiness"],
            "known_limits": ["single contained runtime proof"],
        }
        self._assert_schema_accepts(RUNTIME_SCHEMA, artifact)

    def test_workloop_schema_accepts_required_artifact_shape(self):
        artifact = {
            "milestone_name": "V5-S15B-R1-CODEX-RUNTIME-CONTAINED-WORKLOOP",
            "workloop_kind": "bounded-read-only-adapter-workloop",
            "pai_dir": "/tmp/pai",
            "adapter_identity_marker": "PAI_CODEX_PEER_BETA_ADAPTER",
            "adapter_status": "peer-beta",
            "upstream_adapter": "claude",
            "observed_instruction_sources": ["AGENTS.md"],
            "selected_work_policy": "bounded adapter decision only",
            "memory_write_performed": False,
            "isa_write_performed": False,
            "pulse_probe_performed": False,
            "localhost_31337_called": False,
            "runtime_surface_created": False,
            "proposed_next_action": "Implement a bounded adapter task executor behind the contained launcher.",
            "requires_architect_goal_card": True,
            "evidence_classification": ["runtime workloop evidence", "not replacement readiness"],
            "known_limits": ["single read-only pass"],
        }
        self._assert_schema_accepts(WORKLOOP_SCHEMA, artifact)

    def test_launcher_doctor_passes_on_synthetic_install(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r1.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            result = self._run_launcher(launcher, "doctor", "--pai-dir", str(pai_dir))
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["adapter_status"], "peer-beta")
            self.assertEqual(payload["upstream_adapter"], "claude")

    def test_launcher_doctor_rejects_missing_router_marker(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r1.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            router = pai_dir / "AGENTS.md"
            router.write_text(router.read_text(encoding="utf-8").replace("PAI_CODEX_PEER_BETA_ADAPTER", ""), encoding="utf-8")
            result = self._run_launcher(launcher, "doctor", "--pai-dir", str(pai_dir), check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("adapter identity marker", result.stderr)

    def test_exec_proof_command_uses_codex_exec_read_only_containment(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r1.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            payload = self._dry_run(launcher, "exec-proof", pai_dir, "runtime-proof.json")
            command = payload["command"]
            self.assertEqual(command[0], "codex")
            self.assertIn("exec", command)
            self.assertIn("--ephemeral", command)
            self.assertIn("--ignore-rules", command)
            self.assertEqual(command[command.index("--sandbox") + 1], "read-only")
            self.assertEqual(Path(command[command.index("--cd") + 1]), pai_dir.resolve())
            self.assertEqual(command[command.index("--ask-for-approval") + 1], "never")
            self.assertTrue(str(payload["output"]).endswith("runtime-proof.json"))

    def test_workloop_once_command_uses_codex_exec_read_only_containment(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r1.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            payload = self._dry_run(launcher, "workloop-once", pai_dir, "workloop-once.json")
            command = payload["command"]
            self.assertEqual(command[0], "codex")
            self.assertIn("exec", command)
            self.assertIn("--ephemeral", command)
            self.assertEqual(command[command.index("--sandbox") + 1], "read-only")
            self.assertEqual(Path(command[command.index("--cd") + 1]), pai_dir.resolve())
            self.assertTrue(str(payload["output"]).endswith("workloop-once.json"))

    def test_runtime_outputs_are_limited_to_approved_run_directory(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r1.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            result = self._run_launcher(
                launcher,
                "exec-proof",
                "--pai-dir",
                str(pai_dir),
                "--output",
                str(pai_dir / "runtime-proof.json"),
                "--dry-run",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("adapters/codex/runs/s15b-r1", result.stderr)

    def test_installer_installs_runtime_launcher_and_schemas_to_synthetic_pai_root(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r1.") as tmp:
            pai_dir, backup_root, launcher = self._install_synthetic(tmp)
            self.assertTrue(launcher.is_file())
            self.assertTrue(launcher.stat().st_mode & 0o100)
            self.assertTrue((pai_dir / "adapters" / "codex" / "runtime-proof.schema.json").is_file())
            self.assertTrue((pai_dir / "adapters" / "codex" / "workloop-once.schema.json").is_file())
            result = validate_install(pai_dir, backup_root)
            self.assertEqual(result["adapter_status"], "peer-beta")

    def test_installer_is_idempotent_with_workloop_runtime_payload(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r1.") as tmp:
            pai_dir, backup_root, _ = self._install_synthetic(tmp)
            first = {
                path.relative_to(pai_dir): path.read_bytes()
                for path in (pai_dir / "adapters" / "codex").rglob("*")
                if path.is_file()
            }
            first[Path("AGENTS.md")] = (pai_dir / "AGENTS.md").read_bytes()
            apply_install(pai_dir, backup_root)
            second = {
                path.relative_to(pai_dir): path.read_bytes()
                for path in (pai_dir / "adapters" / "codex").rglob("*")
                if path.is_file()
            }
            second[Path("AGENTS.md")] = (pai_dir / "AGENTS.md").read_bytes()
            self.assertEqual(first, second)

    def test_runtime_harness_does_not_target_memory_isa_or_pulse(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r1.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            proof = self._dry_run(launcher, "exec-proof", pai_dir, "runtime-proof.json")
            workloop = self._dry_run(launcher, "workloop-once", pai_dir, "workloop-once.json")
            combined = json.dumps([proof, workloop])
            for forbidden in [
                "/Memory",
                "Memory/",
                "/ISA",
                "ISA/",
                "/Pulse",
                "Pulse/",
                "localhost:31337",
                "127.0.0.1:31337",
            ]:
                self.assertNotIn(forbidden, combined)

    def test_runtime_harness_does_not_create_repo_root_or_dotcodex_surfaces(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r1.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            before = set(workspace.iterdir())
            self._dry_run(launcher, "exec-proof", pai_dir, "runtime-proof.json")
            self._dry_run(launcher, "workloop-once", pai_dir, "workloop-once.json")
            after = set(workspace.iterdir())
            self.assertEqual(before, after)
            self.assertFalse((workspace / "AGENTS.md").exists())
            self.assertFalse((workspace / ".codex").exists())
            self.assertFalse((pai_dir.parent.parent / ".codex").exists())


if __name__ == "__main__":
    unittest.main()
