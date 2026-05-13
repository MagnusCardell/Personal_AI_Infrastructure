from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

from tools.pai_runtime_runner.audit import audit_run
from tools.pai_runtime_runner.install import install_runtime
from tools.pai_runtime_runner.runner import doctor, run_runtime


REPO_ROOT = Path(__file__).resolve().parents[1]
PROVIDER_MANIFEST = REPO_ROOT / "runtimes" / "codex" / "provider-manifest.json"
RUN_RESULT_SCHEMA = REPO_ROOT / "pai-runtime" / "run-result.schema.json"
RUN_VALIDATION_SCHEMA = REPO_ROOT / "pai-runtime" / "run-validation.schema.json"
TASK_CARD = REPO_ROOT / "pai-runtime" / "tasks" / "s15d-codex-synthetic-bugfix.json"
TASK_FIXTURE = REPO_ROOT / "pai-runtime" / "task-fixtures" / "s15d_bugfix"
MILESTONE = "V5-S15D-PAI-RUNTIME-RUNNER-CODEX"
RUN_ID = "s15d-codex-synthetic-bugfix"
MARKER = "PAI_CODEX_PEER_BETA_ADAPTER"
RUN_RELATIVE = Path("runs") / "s15d" / "codex-synthetic-bugfix"


class PaiRuntimeRunnerCodexTests(unittest.TestCase):
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

    def _install_synthetic(self, tmp: str) -> tuple[Path, Path, Path]:
        pai_dir, backup_root = self._synthetic_layout(tmp)
        install_runtime(pai_dir, backup_root)
        return pai_dir, backup_root, pai_dir / "bin" / "pai-runtime"

    def _run_pai_runtime(self, launcher: Path, *args: str, check: bool = True, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(launcher), *args],
            check=check,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
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

    def _repaired_priority_source(self) -> str:
        return """\
ALIASES = {
    "low": {"low", "lo", "l", "minor"},
    "medium": {"medium", "med", "normal", "m"},
    "high": {"high", "hi", "h", "important"},
    "urgent": {"urgent", "critical", "blocker", "p0"},
}


def normalize_priority(value):
    if not isinstance(value, str):
        raise ValueError("priority must be a string")
    text = value.strip().lower()
    for canonical, aliases in ALIASES.items():
        if text in aliases:
            return canonical
    raise ValueError(f"unknown priority: {value!r}")
"""

    def _run_result(self, pai_dir: Path, workspace: Path) -> dict[str, object]:
        return {
            "milestone_name": MILESTONE,
            "run_id": RUN_ID,
            "runtime": "codex",
            "runtime_status": "peer-beta",
            "provider_type": "codex-cli",
            "pai_dir": str(pai_dir),
            "task_id": RUN_ID,
            "task_kind": "bounded-synthetic-code-repair",
            "adapter_identity_marker": MARKER,
            "adapter_status": "peer-beta",
            "upstream_adapter": "claude",
            "agents_router_observed": True,
            "pai_owned_run_directory": True,
            "task_workspace": str(workspace),
            "files_modified": ["src/pai_priority.py"],
            "tests_run": ["python3 -m unittest discover -s tests"],
            "tests_passed": True,
            "memory_write_performed": False,
            "isa_write_performed": False,
            "pulse_probe_performed": False,
            "localhost_31337_called": False,
            "runtime_surface_created": False,
            "result_summary": "Fixed priority alias normalization in the PAI-owned synthetic workspace.",
            "evidence_classification": [
                "PAI-owned runtime task evidence",
                "bounded synthetic task evidence",
                "not replacement readiness",
            ],
            "known_limits": ["synthetic bounded task only"],
            "repair_file_path": "src/pai_priority.py",
            "repair_file_content": self._repaired_priority_source(),
        }

    def _run_validation_shape(self, workspace: Path) -> dict[str, object]:
        return {
            "milestone_name": MILESTONE,
            "run_id": RUN_ID,
            "runtime": "codex",
            "runtime_attempt_number": 1,
            "pai_runtime_command": ["pai-runtime", "run", "--runtime", "codex"],
            "provider_command": ["pai-codex", "provider-run"],
            "task_workspace": str(workspace),
            "task_initially_failed": True,
            "task_tests_passed_after_repair": True,
            "diff_present": True,
            "diff_limited_to_task_workspace": True,
            "event_logs_present": True,
            "event_attribution_passed": True,
            "codex_file_change_events": [],
            "codex_command_execution_events": [],
            "approved_task_workspace_writes": [],
            "approved_pai_run_writes": [],
            "ambient_pai_state_churn": [],
            "forbidden_semantic_writes": [],
            "unknown_unclassified_writes": [],
            "memory_write_performed_by_codex": False,
            "isa_write_performed_by_codex": False,
            "pulse_probe_performed_by_codex": False,
            "localhost_31337_called_by_codex": False,
            "repo_root_agents_created": False,
            "repo_dotcodex_created": False,
            "codex_adapter_files_installed_under_home_codex": False,
            "validation_passed": True,
            "known_limits": ["synthetic bounded task only"],
        }

    def _fake_codex_bin(self, bin_dir: Path) -> Path:
        codex = bin_dir / "codex"
        codex.write_text(
            """#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

args = sys.argv[1:]
output = Path(args[args.index("-o") + 1])
workspace = Path(args[args.index("--cd") + 1])
prompt = args[-1]
match = re.search(r"PAI_DIR is '([^']+)'", prompt)
pai_dir = match.group(1) if match else ""
repair = '''ALIASES = {
    "low": {"low", "lo", "l", "minor"},
    "medium": {"medium", "med", "normal", "m"},
    "high": {"high", "hi", "h", "important"},
    "urgent": {"urgent", "critical", "blocker", "p0"},
}


def normalize_priority(value):
    if not isinstance(value, str):
        raise ValueError("priority must be a string")
    text = value.strip().lower()
    for canonical, aliases in ALIASES.items():
        if text in aliases:
            return canonical
    raise ValueError(f"unknown priority: {value!r}")
'''
payload = {
    "milestone_name": "V5-S15D-PAI-RUNTIME-RUNNER-CODEX",
    "run_id": "s15d-codex-synthetic-bugfix",
    "runtime": "codex",
    "runtime_status": "peer-beta",
    "provider_type": "codex-cli",
    "pai_dir": pai_dir,
    "task_id": "s15d-codex-synthetic-bugfix",
    "task_kind": "bounded-synthetic-code-repair",
    "adapter_identity_marker": "PAI_CODEX_PEER_BETA_ADAPTER",
    "adapter_status": "peer-beta",
    "upstream_adapter": "claude",
    "agents_router_observed": True,
    "pai_owned_run_directory": True,
    "task_workspace": str(workspace),
    "files_modified": ["src/pai_priority.py"],
    "tests_run": ["python3 -m unittest discover -s tests"],
    "tests_passed": True,
    "memory_write_performed": False,
    "isa_write_performed": False,
    "pulse_probe_performed": False,
    "localhost_31337_called": False,
    "runtime_surface_created": False,
    "result_summary": "Fixed priority alias normalization in the PAI-owned synthetic workspace.",
    "evidence_classification": [
        "PAI-owned runtime task evidence",
        "bounded synthetic task evidence",
        "not replacement readiness",
    ],
    "known_limits": ["synthetic bounded task only"],
    "repair_file_path": "src/pai_priority.py",
    "repair_file_content": repair,
}
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
print(json.dumps({"type": "file_change", "path": "src/pai_priority.py"}))
""",
            encoding="utf-8",
        )
        codex.chmod(codex.stat().st_mode | stat.S_IXUSR)
        return codex

    def _with_fake_codex_run(self, tmp: str) -> tuple[Path, Path]:
        tmp_path = Path(tmp)
        pai_dir, _, launcher = self._install_synthetic(tmp)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        self._fake_codex_bin(fake_bin)
        run_dir = pai_dir / RUN_RELATIVE
        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = str(fake_bin) + os.pathsep + old_path
        try:
            result = self._run_pai_runtime(
                launcher,
                "run",
                "--pai-dir",
                str(pai_dir),
                "--runtime",
                "codex",
                "--task-card",
                str(pai_dir / "runtime-tasks" / "s15d-codex-synthetic-bugfix.json"),
                "--run-dir",
                str(run_dir),
            )
        finally:
            os.environ["PATH"] = old_path
        self.assertTrue(json.loads(result.stdout)["ok"])
        return pai_dir, run_dir

    def _write_json(self, path: Path, payload: dict[str, object], mtime: float) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.utime(path, (mtime, mtime))

    def _write_events(self, path: Path, events: list[dict[str, object]], mtime: float) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(event, sort_keys=True) + "\n" for event in events), encoding="utf-8")
        os.utime(path, (mtime, mtime))

    def _audit_fixture(
        self,
        tmp: str,
        *,
        events: list[dict[str, object]] | None = None,
        extra_after_marker: tuple[Path, str] | None = None,
    ) -> dict[str, object]:
        base = Path(tmp)
        pai_dir = base / "home" / ".claude" / "PAI"
        run_dir = pai_dir / RUN_RELATIVE
        workspace = run_dir / "workspace"
        repo_root = base / "repo"
        home = base / "user-home"
        repo_root.mkdir(parents=True)
        home.mkdir(parents=True)
        workspace.mkdir(parents=True)

        marker = base / "marker"
        marker.write_text("marker\n", encoding="utf-8")
        after_marker = marker.stat().st_mtime + 2

        implementation = workspace / "src" / "pai_priority.py"
        implementation.parent.mkdir(parents=True, exist_ok=True)
        implementation.write_text(self._repaired_priority_source(), encoding="utf-8")
        os.utime(implementation, (after_marker, after_marker))

        result_path = run_dir / "run-result.json"
        events_path = run_dir / "runtime-events.jsonl"
        diff_path = run_dir / "task.diff"
        state_path = run_dir / "run-state.json"
        self._write_json(result_path, self._run_result(pai_dir, workspace), after_marker)
        self._write_events(events_path, events or [{"type": "file_change", "path": "src/pai_priority.py"}], after_marker)
        diff_path.write_text("--- a/src/pai_priority.py\n+++ b/src/pai_priority.py\n@@ -1 +1 @@\n-fixed\n+fixed\n", encoding="utf-8")
        os.utime(diff_path, (after_marker, after_marker))
        self._write_json(
            state_path,
            {
                "pai_runtime_command": ["pai-runtime", "run", "--runtime", "codex"],
                "provider_command": ["pai-codex", "provider-run"],
                "codex_exec_command": ["codex", "exec", "--sandbox", "workspace-write"],
                "initial_test_returncode": 1,
                "post_test_returncode": 0,
                "task_workspace": str(workspace),
            },
            after_marker,
        )

        if extra_after_marker is not None:
            relative, text = extra_after_marker
            extra_path = pai_dir / relative
            extra_path.parent.mkdir(parents=True, exist_ok=True)
            extra_path.write_text(text, encoding="utf-8")
            os.utime(extra_path, (after_marker, after_marker))

        old_home = os.environ.get("HOME")
        os.environ["HOME"] = str(home)
        try:
            return audit_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                result_path=result_path,
                events_path=events_path,
                runtime_attempt_number=1,
                repo_root=repo_root,
            )
        finally:
            if old_home is None:
                os.environ.pop("HOME", None)
            else:
                os.environ["HOME"] = old_home

    def test_codex_provider_manifest_is_peer_beta_runtime(self):
        provider = json.loads(PROVIDER_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(provider["runtime_name"], "codex")
        self.assertEqual(provider["runtime_status"], "peer-beta")
        self.assertEqual(provider["provider_type"], "codex-cli")
        self.assertEqual(provider["upstream_adapter"], "claude")
        self.assertTrue(provider["supports_codex_exec"])
        self.assertTrue(provider["supports_jsonl_events"])
        self.assertTrue(provider["supports_structured_output"])
        self.assertEqual(provider["memory_write_policy"], "disabled")
        self.assertEqual(provider["isa_write_policy"], "disabled")
        self.assertEqual(provider["pulse_policy"], "no-probe")
        self.assertEqual(provider["replacement_status"], "not-replacement-grade")

    def test_run_result_schema_accepts_required_shape(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            workspace = Path(tmp) / "workspace"
            self._assert_schema_accepts(RUN_RESULT_SCHEMA, self._run_result(Path(tmp) / "PAI", workspace))

    def test_run_validation_schema_accepts_required_shape(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            self._assert_schema_accepts(RUN_VALIDATION_SCHEMA, self._run_validation_shape(Path(tmp) / "workspace"))

    def test_s15d_fixture_tests_fail_before_repair(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            fixture = Path(tmp) / "fixture"
            shutil.copytree(TASK_FIXTURE, fixture)
            env = dict(os.environ)
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            result = subprocess.run(
                ["python3", "-m", "unittest", "discover", "-s", "tests"],
                cwd=fixture,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )
            self.assertNotEqual(result.returncode, 0)

    def test_pai_runtime_runner_installs_to_synthetic_pai_root(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            self.assertTrue(launcher.is_file())
            self.assertTrue(os.access(launcher, os.X_OK))
            self.assertTrue((pai_dir / "runtimes" / "codex" / "provider-manifest.json").is_file())
            self.assertTrue((pai_dir / "runtime-schemas" / "run-result.schema.json").is_file())
            self.assertTrue((pai_dir / "adapters" / "codex" / "bin" / "pai-codex").is_file())

    def test_pai_runtime_doctor_passes_on_synthetic_install(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            pai_dir, _, _ = self._install_synthetic(tmp)
            result = doctor(pai_dir)
            self.assertTrue(result["ok"])
            self.assertEqual(result["runtime"], "codex")

    def test_pai_runtime_run_creates_pai_owned_run_directory(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            pai_dir, run_dir = self._with_fake_codex_run(tmp)
            self.assertTrue(run_dir.is_dir())
            self.assertTrue((run_dir / "workspace" / "src" / "pai_priority.py").is_file())
            result = json.loads((run_dir / "run-result.json").read_text(encoding="utf-8"))
            self.assertTrue(result["pai_owned_run_directory"])
            self.assertEqual(result["task_id"], RUN_ID)
            self.assertEqual(result["adapter_identity_marker"], MARKER)

    def test_pai_runtime_run_delegates_to_codex_provider(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            pai_dir, _, _ = self._install_synthetic(tmp)
            run_dir = pai_dir / RUN_RELATIVE
            payload = run_runtime(
                pai_dir,
                "codex",
                pai_dir / "runtime-tasks" / "s15d-codex-synthetic-bugfix.json",
                run_dir,
                dry_run=True,
            )
            self.assertIn("provider-run", payload["provider_command"])
            self.assertIn(str(pai_dir / "adapters" / "codex" / "bin" / "pai-codex"), payload["provider_command"])

    def test_pai_runtime_run_rejects_unknown_runtime(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            pai_dir, _, _ = self._install_synthetic(tmp)
            with self.assertRaises(ValueError):
                run_runtime(
                    pai_dir,
                    "claude",
                    pai_dir / "runtime-tasks" / "s15d-codex-synthetic-bugfix.json",
                    pai_dir / RUN_RELATIVE,
                )

    def test_pai_runtime_run_rejects_run_dir_outside_pai_runs(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            pai_dir, _, _ = self._install_synthetic(tmp)
            with self.assertRaises(ValueError):
                run_runtime(
                    pai_dir,
                    "codex",
                    pai_dir / "runtime-tasks" / "s15d-codex-synthetic-bugfix.json",
                    Path(tmp) / "outside",
                )

    def test_pai_runtime_audit_accepts_clean_codex_task_result(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            result = self._audit_fixture(tmp)
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["event_attribution_passed"])

    def test_pai_runtime_audit_rejects_write_outside_pai_owned_run(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            outside = Path(tmp) / "home" / ".claude" / "PAI" / "runtime-state.json"
            result = self._audit_fixture(tmp, events=[{"type": "file_change", "path": str(outside)}])
            self.assertFalse(result["validation_passed"])
            self.assertFalse(result["event_attribution_passed"])

    def test_pai_runtime_audit_rejects_memory_write(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            result = self._audit_fixture(tmp, events=[{"type": "exec_command", "cmd": "touch Memory/WORK/s15d.txt"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["memory_write_performed_by_codex"])

    def test_pai_runtime_audit_rejects_isa_write(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            result = self._audit_fixture(tmp, events=[{"type": "exec_command", "cmd": "touch ISA/s15d.md"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["isa_write_performed_by_codex"])

    def test_pai_runtime_audit_rejects_pulse_probe(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            result = self._audit_fixture(tmp, events=[{"type": "exec_command", "cmd": "curl http://pai/Pulse/events"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["pulse_probe_performed_by_codex"])

    def test_pai_runtime_audit_rejects_localhost_31337(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            result = self._audit_fixture(tmp, events=[{"type": "exec_command", "cmd": "curl http://localhost:31337"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["localhost_31337_called_by_codex"])

    def test_pai_runtime_audit_classifies_known_ambient_pai_churn(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            result = self._audit_fixture(tmp, extra_after_marker=(Path("Memory") / "state" / "cache.json", "{}\n"))
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["ambient_pai_state_churn"])

    def test_pai_runtime_audit_classifies_pulse_observability_churn(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            result = self._audit_fixture(
                tmp,
                extra_after_marker=(Path("PULSE") / "Observability" / ".next" / "BUILD_ID", "build\n"),
            )
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["ambient_pai_state_churn"])

    def test_pai_runtime_audit_rejects_unknown_unclassified_write(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            result = self._audit_fixture(tmp, extra_after_marker=(Path("runtime-unknown.json"), "{}\n"))
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["unknown_unclassified_writes"])

    def test_pai_runtime_runner_does_not_create_repo_root_or_dotcodex_surfaces(self):
        with tempfile.TemporaryDirectory(prefix="s15d.") as tmp:
            tmp_path = Path(tmp)
            pai_dir, _, launcher = self._install_synthetic(tmp)
            fake_bin = tmp_path / "bin"
            fake_bin.mkdir()
            self._fake_codex_bin(fake_bin)
            repo_root = tmp_path / "repo"
            repo_root.mkdir()
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = str(fake_bin) + os.pathsep + old_path
            try:
                self._run_pai_runtime(
                    launcher,
                    "run",
                    "--pai-dir",
                    str(pai_dir),
                    "--runtime",
                    "codex",
                    "--task-card",
                    str(pai_dir / "runtime-tasks" / "s15d-codex-synthetic-bugfix.json"),
                    "--run-dir",
                    str(pai_dir / RUN_RELATIVE),
                    cwd=repo_root,
                )
            finally:
                os.environ["PATH"] = old_path
            self.assertFalse((repo_root / "AGENTS.md").exists())
            self.assertFalse((repo_root / ".codex").exists())


if __name__ == "__main__":
    unittest.main()
