from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.codex_adapter_installer.install import apply_install, read_staged_agents, validate_install
from tools.codex_adapter_installer.runtime_audit import audit_runtime


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SCHEMA = REPO_ROOT / "adapters" / "codex" / "runtime-proof.schema.json"
WORKLOOP_SCHEMA = REPO_ROOT / "adapters" / "codex" / "workloop-once.schema.json"
VALIDATION_SCHEMA = REPO_ROOT / "adapters" / "codex" / "runtime-validation.schema.json"
MILESTONE = "V5-S15B-R2-CODEX-RUNTIME-EVENT-ATTRIBUTED-WORKLOOP"
MARKER = "PAI_CODEX_PEER_BETA_ADAPTER"
RUN_RELATIVE = Path("adapters") / "codex" / "runs" / "s15b-r2"


class CodexAdapterRuntimeEventAttributionTests(unittest.TestCase):
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

    def _dry_run(self, launcher: Path, command: str, pai_dir: Path, output_name: str, events_name: str) -> dict[str, object]:
        run_dir = pai_dir / RUN_RELATIVE
        result = self._run_launcher(
            launcher,
            command,
            "--pai-dir",
            str(pai_dir),
            "--output",
            str(run_dir / output_name),
            "--events-output",
            str(run_dir / events_name),
            "--dry-run",
        )
        return json.loads(result.stdout)

    def _proof(self, pai_dir: Path) -> dict[str, object]:
        return {
            "milestone_name": MILESTONE,
            "runtime_invocation": "codex exec --json --sandbox read-only --ephemeral --cd PAI_DIR",
            "pai_dir": str(pai_dir),
            "adapter_identity_marker": MARKER,
            "adapter_status": "peer-beta",
            "upstream_adapter": "claude",
            "agents_router_observed": True,
            "pai_system_prompt_policy_observed": True,
            "memory_write_performed": False,
            "isa_write_performed": False,
            "pulse_probe_performed": False,
            "localhost_31337_called": False,
            "runtime_surface_created": False,
            "evidence_classification": ["runtime proof evidence", "non-canonical evidence", "not replacement readiness"],
            "known_limits": ["single event-attributed runtime proof"],
        }

    def _workloop(self, pai_dir: Path) -> dict[str, object]:
        return {
            "milestone_name": MILESTONE,
            "workloop_kind": "bounded-read-only-adapter-workloop",
            "pai_dir": str(pai_dir),
            "adapter_identity_marker": MARKER,
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
            "evidence_classification": ["runtime workloop evidence", "non-canonical evidence", "not replacement readiness"],
            "known_limits": ["single read-only work-loop pass"],
        }

    def _write_json(self, path: Path, payload: dict[str, object], after_marker: float) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.utime(path, (after_marker, after_marker))

    def _write_events(self, path: Path, events: list[dict[str, object]], after_marker: float) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(event, sort_keys=True) + "\n" for event in events), encoding="utf-8")
        os.utime(path, (after_marker, after_marker))

    def _audit_fixture(
        self,
        tmp: str,
        *,
        runtime_events: list[dict[str, object]] | None = None,
        workloop_events: list[dict[str, object]] | None = None,
        extra_after_marker: tuple[Path, str] | None = None,
    ) -> dict[str, object]:
        base = Path(tmp)
        pai_dir = base / "home" / ".claude" / "PAI"
        run_dir = pai_dir / RUN_RELATIVE
        repo_root = base / "repo"
        repo_root.mkdir(parents=True)
        pai_dir.mkdir(parents=True)
        marker = base / "marker"
        marker.write_text("marker\n", encoding="utf-8")
        after_marker = marker.stat().st_mtime + 2

        proof_path = run_dir / "runtime-proof.json"
        workloop_path = run_dir / "workloop-once.json"
        runtime_events_path = run_dir / "runtime-events.jsonl"
        workloop_events_path = run_dir / "workloop-events.jsonl"
        self._write_json(proof_path, self._proof(pai_dir), after_marker)
        self._write_json(workloop_path, self._workloop(pai_dir), after_marker)
        self._write_events(runtime_events_path, runtime_events or [{"type": "response.completed"}], after_marker)
        self._write_events(workloop_events_path, workloop_events or [{"type": "response.completed"}], after_marker)

        if extra_after_marker is not None:
            relative, text = extra_after_marker
            extra_path = pai_dir / relative
            extra_path.parent.mkdir(parents=True, exist_ok=True)
            extra_path.write_text(text, encoding="utf-8")
            os.utime(extra_path, (after_marker, after_marker))

        return audit_runtime(
            pai_dir=pai_dir,
            marker=marker,
            runtime_proof=proof_path,
            workloop=workloop_path,
            runtime_events=runtime_events_path,
            workloop_events=workloop_events_path,
            runtime_attempt_number=1,
            repo_root=repo_root,
        )

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

    def test_runtime_audit_accepts_clean_codex_event_stream(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            result = self._audit_fixture(tmp)
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["event_attribution_passed"])
            self.assertFalse(result["forbidden_semantic_writes"])
            self.assertFalse(result["unknown_unclassified_writes"])

    def test_runtime_audit_rejects_codex_file_change_outside_approved_outputs(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            result = self._audit_fixture(
                tmp,
                runtime_events=[{"type": "file_change", "path": "adapters/codex/runs/s15b-r2/extra.json"}],
            )
            self.assertFalse(result["validation_passed"])
            self.assertFalse(result["event_attribution_passed"])
            self.assertTrue(result["codex_file_change_events"])

    def test_runtime_audit_rejects_codex_command_execution_touching_memory(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            result = self._audit_fixture(tmp, runtime_events=[{"type": "exec_command", "cmd": "touch Memory/WORK/item.md"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["memory_write_performed_by_codex"])

    def test_runtime_audit_rejects_codex_command_execution_touching_isa(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            result = self._audit_fixture(tmp, runtime_events=[{"type": "exec_command", "cmd": "python -c 'write ISA/item.md'"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["isa_write_performed_by_codex"])

    def test_runtime_audit_rejects_codex_pulse_probe(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            result = self._audit_fixture(tmp, runtime_events=[{"type": "exec_command", "cmd": "curl http://pai-pulse/status"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["pulse_probe_performed_by_codex"])

    def test_runtime_audit_rejects_localhost_31337(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            result = self._audit_fixture(tmp, runtime_events=[{"type": "exec_command", "cmd": "curl http://localhost:31337/health"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["localhost_31337_called_by_codex"])

    def test_runtime_audit_classifies_known_ambient_pai_state_churn(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            result = self._audit_fixture(tmp, extra_after_marker=(Path("Pulse") / "state" / "cache.json", "{}\n"))
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["ambient_pai_state_churn"])

    def test_runtime_audit_rejects_unknown_unclassified_write(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            result = self._audit_fixture(tmp, extra_after_marker=(Path("unexpected-state.json"), "{}\n"))
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["unknown_unclassified_writes"])

    def test_router_contains_runtime_identity_marker(self):
        router = read_staged_agents()
        for text in [
            "PAI_CODEX_PEER_BETA_ADAPTER",
            "Codex is a peer beta adapter for PAI v5.",
            "Claude remains the official/full-support upstream adapter.",
            "PAI_DIR is the v5 PAI subsystem root, usually ~/.claude/PAI.",
            "AGENTS.md is a router into PAI v5, not a clone of CLAUDE.md.",
        ]:
            self.assertIn(text, router)

    def test_runtime_schema_accepts_required_proof_shape(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            self._assert_schema_accepts(RUNTIME_SCHEMA, self._proof(Path(tmp) / "PAI"))

    def test_workloop_schema_accepts_required_artifact_shape(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            self._assert_schema_accepts(WORKLOOP_SCHEMA, self._workloop(Path(tmp) / "PAI"))

    def test_validation_schema_accepts_required_audit_shape(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            self._assert_schema_accepts(VALIDATION_SCHEMA, self._audit_fixture(tmp))

    def test_launcher_exec_proof_captures_jsonl_events(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            payload = self._dry_run(launcher, "exec-proof", pai_dir, "runtime-proof.json", "runtime-events.jsonl")
            command = payload["command"]
            self.assertEqual(command[0], "codex")
            self.assertIn("exec", command)
            self.assertIn("--json", command)
            self.assertEqual(command[command.index("--sandbox") + 1], "read-only")
            self.assertEqual(Path(command[command.index("--cd") + 1]), pai_dir.resolve())
            self.assertTrue(str(payload["events_output"]).endswith("runtime-events.jsonl"))

    def test_launcher_workloop_once_captures_jsonl_events(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            payload = self._dry_run(launcher, "workloop-once", pai_dir, "workloop-once.json", "workloop-events.jsonl")
            command = payload["command"]
            self.assertEqual(command[0], "codex")
            self.assertIn("exec", command)
            self.assertIn("--json", command)
            self.assertEqual(command[command.index("--sandbox") + 1], "read-only")
            self.assertEqual(Path(command[command.index("--cd") + 1]), pai_dir.resolve())
            self.assertTrue(str(payload["events_output"]).endswith("workloop-events.jsonl"))

    def test_runtime_outputs_are_limited_to_s15b_r2_run_directory(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            result = self._run_launcher(
                launcher,
                "exec-proof",
                "--pai-dir",
                str(pai_dir),
                "--output",
                str(pai_dir / "runtime-proof.json"),
                "--events-output",
                str(pai_dir / RUN_RELATIVE / "runtime-events.jsonl"),
                "--dry-run",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("adapters/codex/runs/s15b-r2", result.stderr)

    def test_installer_installs_event_attributed_runtime_payload_to_synthetic_pai_root(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            pai_dir, backup_root, launcher = self._install_synthetic(tmp)
            self.assertTrue(launcher.is_file())
            self.assertTrue(launcher.stat().st_mode & 0o100)
            self.assertTrue((pai_dir / "adapters" / "codex" / "runtime-proof.schema.json").is_file())
            self.assertTrue((pai_dir / "adapters" / "codex" / "workloop-once.schema.json").is_file())
            self.assertTrue((pai_dir / "adapters" / "codex" / "runtime-validation.schema.json").is_file())
            result = validate_install(pai_dir, backup_root)
            self.assertEqual(result["adapter_status"], "peer-beta")

    def test_installer_is_idempotent_with_event_attributed_runtime_payload(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
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
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            proof = self._dry_run(launcher, "exec-proof", pai_dir, "runtime-proof.json", "runtime-events.jsonl")
            workloop = self._dry_run(launcher, "workloop-once", pai_dir, "workloop-once.json", "workloop-events.jsonl")
            combined = json.dumps([proof, workloop])
            for forbidden in [
                "Memory/WORK",
                "Memory/LEARNING",
                "Memory/KNOWLEDGE",
                "ISA/",
                "Pulse/events",
                "localhost:31337",
                "127.0.0.1:31337",
            ]:
                self.assertNotIn(forbidden, combined)

    def test_runtime_harness_does_not_create_repo_root_or_dotcodex_surfaces(self):
        with tempfile.TemporaryDirectory(prefix="s15b-r2.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            before = set(workspace.iterdir())
            self._dry_run(launcher, "exec-proof", pai_dir, "runtime-proof.json", "runtime-events.jsonl")
            self._dry_run(launcher, "workloop-once", pai_dir, "workloop-once.json", "workloop-events.jsonl")
            after = set(workspace.iterdir())
            self.assertEqual(before, after)
            self.assertFalse((workspace / "AGENTS.md").exists())
            self.assertFalse((workspace / ".codex").exists())
            self.assertFalse((pai_dir.parent.parent / ".codex").exists())


if __name__ == "__main__":
    unittest.main()
