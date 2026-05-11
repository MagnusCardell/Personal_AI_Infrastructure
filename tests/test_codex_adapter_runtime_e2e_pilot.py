from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.codex_adapter_installer.install import apply_install, read_staged_agents, validate_install


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "adapters/codex/runtime-proof.schema.json"


class CodexAdapterRuntimeE2EPilotTests(unittest.TestCase):
    def _synthetic_layout(self, tmp: str) -> tuple[Path, Path]:
        base = Path(tmp)
        pai_dir = base / "home" / ".claude" / "PAI"
        pai_dir.mkdir(parents=True)
        backup_root = base / "backup"
        (backup_root / ".claude" / "PAI").mkdir(parents=True)
        return pai_dir, backup_root

    def _install(self, tmp: str) -> tuple[Path, Path]:
        pai_dir, backup_root = self._synthetic_layout(tmp)
        apply_install(pai_dir, backup_root)
        validate_install(pai_dir, backup_root)
        return pai_dir, backup_root

    def _run_launcher(self, pai_dir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        launcher = pai_dir / "adapters" / "codex" / "bin" / "pai-codex"
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [str(launcher), *args],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )

    def _dry_run(self, pai_dir: Path) -> dict[str, object]:
        output = pai_dir / "adapters" / "codex" / "runs" / "s15b" / "runtime-proof.json"
        result = self._run_launcher(
            pai_dir,
            "exec-proof",
            "--pai-dir",
            str(pai_dir),
            "--output",
            str(output),
            "--dry-run",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_router_contains_runtime_identity_marker(self):
        self.assertIn("PAI_CODEX_PEER_BETA_ADAPTER", read_staged_agents())

    def test_runtime_schema_accepts_required_proof_shape(self):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        sample = {
            "milestone_name": "V5-S15B-CODEX-RUNTIME-E2E-PILOT",
            "runtime_invocation": {
                "command": "codex exec",
                "mode": "non-interactive",
                "working_directory": "/tmp/pai",
            },
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
            "evidence_classification": [
                "runtime proof evidence",
                "non-canonical evidence",
                "not replacement readiness",
                "not Claude equivalence",
            ],
            "known_limits": ["bounded runtime proof only"],
        }
        self.assertEqual(set(schema["required"]), set(sample))
        self.assertEqual(schema["properties"]["runtime_invocation"]["type"], "object")
        self.assertEqual(schema["properties"]["adapter_identity_marker"]["type"], "string")

    def test_launcher_doctor_passes_on_synthetic_install(self):
        with tempfile.TemporaryDirectory(prefix="s15b-runtime.") as tmp:
            pai_dir, _ = self._install(tmp)
            result = self._run_launcher(pai_dir, "doctor", "--pai-dir", str(pai_dir))
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["adapter_status"], "peer-beta")
            self.assertEqual(payload["upstream_adapter"], "claude")
            self.assertTrue(payload["identity_marker_present"])

    def test_launcher_doctor_rejects_missing_router_marker(self):
        with tempfile.TemporaryDirectory(prefix="s15b-runtime.") as tmp:
            pai_dir, _ = self._install(tmp)
            router = pai_dir / "AGENTS.md"
            router.write_text(router.read_text(encoding="utf-8").replace("PAI_CODEX_PEER_BETA_ADAPTER\n\n", ""), encoding="utf-8")
            result = self._run_launcher(pai_dir, "doctor", "--pai-dir", str(pai_dir))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("identity marker", result.stderr)

    def test_launcher_doctor_rejects_replacement_status(self):
        with tempfile.TemporaryDirectory(prefix="s15b-runtime.") as tmp:
            pai_dir, _ = self._install(tmp)
            manifest_path = pai_dir / "adapters" / "codex" / "adapter-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["adapter_status"] = "replacement-grade"
            manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
            result = self._run_launcher(pai_dir, "doctor", "--pai-dir", str(pai_dir))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("peer-beta", result.stderr)

    def test_exec_proof_command_uses_codex_exec(self):
        with tempfile.TemporaryDirectory(prefix="s15b-runtime.") as tmp:
            pai_dir, _ = self._install(tmp)
            payload = self._dry_run(pai_dir)
            command = payload["command"]
            self.assertEqual(command[0], "codex")
            self.assertIn("exec", command)
            self.assertIn("--ephemeral", command)
            self.assertIn("--sandbox", command)
            self.assertIn("workspace-write", command)
            self.assertIn("--output-schema", command)
            self.assertIn("-o", command)

    def test_exec_proof_command_uses_pai_dir_as_working_directory(self):
        with tempfile.TemporaryDirectory(prefix="s15b-runtime.") as tmp:
            pai_dir, _ = self._install(tmp)
            payload = self._dry_run(pai_dir)
            command = payload["command"]
            self.assertEqual(payload["cwd"], str(pai_dir.resolve()))
            self.assertEqual(command[command.index("--cd") + 1], str(pai_dir.resolve()))

    def test_exec_proof_command_writes_only_approved_run_output(self):
        with tempfile.TemporaryDirectory(prefix="s15b-runtime.") as tmp:
            pai_dir, _ = self._install(tmp)
            payload = self._dry_run(pai_dir)
            expected = pai_dir / "adapters" / "codex" / "runs" / "s15b" / "runtime-proof.json"
            self.assertEqual(payload["planned_writes"], [str(expected)])
            self.assertEqual(payload["approved_run_dir"], str(expected.parent))

    def test_installer_installs_runtime_launcher_to_synthetic_pai_root(self):
        with tempfile.TemporaryDirectory(prefix="s15b-runtime.") as tmp:
            pai_dir, _ = self._install(tmp)
            launcher = pai_dir / "adapters" / "codex" / "bin" / "pai-codex"
            schema = pai_dir / "adapters" / "codex" / "runtime-proof.schema.json"
            runtime_state = pai_dir / "adapters" / "codex" / "runtime-state.json"
            self.assertTrue(launcher.is_file())
            self.assertTrue(os.access(launcher, os.X_OK))
            self.assertTrue(schema.is_file())
            self.assertTrue(runtime_state.is_file())

    def test_installer_is_idempotent_with_runtime_launcher(self):
        with tempfile.TemporaryDirectory(prefix="s15b-runtime.") as tmp:
            pai_dir, backup_root = self._install(tmp)
            launcher = pai_dir / "adapters" / "codex" / "bin" / "pai-codex"
            before = launcher.read_bytes()
            apply_install(pai_dir, backup_root)
            validate_install(pai_dir, backup_root)
            self.assertEqual(before, launcher.read_bytes())

    def test_runtime_harness_does_not_target_memory_isa_or_pulse(self):
        with tempfile.TemporaryDirectory(prefix="s15b-runtime.") as tmp:
            pai_dir, _ = self._install(tmp)
            payload = self._dry_run(pai_dir)
            raw = json.dumps(payload, sort_keys=True)
            for token in [
                "Memory/WORK",
                "Memory/LEARNING",
                "Memory/KNOWLEDGE",
                "ISA/",
                "Pulse/events",
                "localhost:31337",
                "127.0.0.1:31337",
            ]:
                self.assertNotIn(token, raw)
            self.assertNotIn("PAI_CODEX_PEER_BETA_ADAPTER", payload["prompt"])

    def test_runtime_harness_does_not_create_repo_root_or_dotcodex_surfaces(self):
        with tempfile.TemporaryDirectory(prefix="s15b-runtime.") as tmp:
            pai_dir, _ = self._install(tmp)
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            before = set(workspace.iterdir())
            self._dry_run(pai_dir)
            after = set(workspace.iterdir())
            self.assertEqual(before, after)
            self.assertFalse((workspace / "AGENTS.md").exists())
            self.assertFalse((workspace / ".codex").exists())


if __name__ == "__main__":
    unittest.main()
