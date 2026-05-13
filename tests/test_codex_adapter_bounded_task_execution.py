from __future__ import annotations

import json
import os
import stat
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

from tools.codex_adapter_installer.install import apply_install, rollback_install, validate_install
from tools.codex_adapter_installer.task_audit import audit_task


REPO_ROOT = Path(__file__).resolve().parents[1]
TASK_CARD_SCHEMA = REPO_ROOT / "adapters" / "codex" / "task-card.schema.json"
TASK_RESULT_SCHEMA = REPO_ROOT / "adapters" / "codex" / "task-result.schema.json"
TASK_VALIDATION_SCHEMA = REPO_ROOT / "adapters" / "codex" / "task-validation.schema.json"
TASK_CARD = REPO_ROOT / "adapters" / "codex" / "tasks" / "s15c-synthetic-bugfix.json"
TASK_FIXTURE = REPO_ROOT / "adapters" / "codex" / "task-fixtures" / "s15c_bugfix"
MILESTONE = "V5-S15C-CODEX-BOUNDED-TASK-EXECUTION"
TASK_ID = "s15c-synthetic-bugfix"
MARKER = "PAI_CODEX_PEER_BETA_ADAPTER"
RUN_RELATIVE = Path("adapters") / "codex" / "runs" / "s15c"


class CodexAdapterBoundedTaskExecutionTests(unittest.TestCase):
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

    def _task_dry_run(self, launcher: Path, pai_dir: Path, run_dir: Path | None = None) -> dict[str, object]:
        target_run_dir = run_dir or (pai_dir / RUN_RELATIVE)
        result = self._run_launcher(
            launcher,
            "task-run",
            "--pai-dir",
            str(pai_dir),
            "--task-card",
            str(pai_dir / "adapters" / "codex" / "tasks" / "s15c-synthetic-bugfix.json"),
            "--run-dir",
            str(target_run_dir),
            "--result",
            str(target_run_dir / "task-result.json"),
            "--events-output",
            str(target_run_dir / "task-events.jsonl"),
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

    def _task_result(self, pai_dir: Path, workspace: Path) -> dict[str, object]:
        return {
            "milestone_name": MILESTONE,
            "task_id": TASK_ID,
            "task_kind": "bounded-synthetic-code-repair",
            "pai_dir": str(pai_dir),
            "adapter_identity_marker": MARKER,
            "adapter_status": "peer-beta",
            "upstream_adapter": "claude",
            "agents_router_observed": True,
            "task_workspace": str(workspace),
            "files_modified": ["src/pai_priority.py"],
            "tests_run": ["python3 -m unittest discover -s tests"],
            "tests_passed": True,
            "memory_write_performed": False,
            "isa_write_performed": False,
            "pulse_probe_performed": False,
            "localhost_31337_called": False,
            "runtime_surface_created": False,
            "result_summary": "Fixed priority alias normalization in the synthetic workspace.",
            "evidence_classification": [
                "bounded task execution evidence",
                "synthetic task evidence",
                "not replacement readiness",
            ],
            "known_limits": ["synthetic bounded task only"],
            "repair_file_path": "src/pai_priority.py",
            "repair_file_content": self._repaired_priority_source(),
        }

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

    def _task_validation_shape(self, workspace: Path) -> dict[str, object]:
        return {
            "milestone_name": MILESTONE,
            "task_id": TASK_ID,
            "runtime_attempt_number": 1,
            "codex_exec_command": ["codex", "exec"],
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
            "approved_adapter_writes": [],
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

    def _write_json(self, path: Path, payload: dict[str, object], mtime: float) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.utime(path, (mtime, mtime))

    def _write_events(self, path: Path, events: list[dict[str, object]], mtime: float) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(event, sort_keys=True) + "\n" for event in events), encoding="utf-8")
        os.utime(path, (mtime, mtime))

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
    "milestone_name": "V5-S15C-CODEX-BOUNDED-TASK-EXECUTION",
    "task_id": "s15c-synthetic-bugfix",
    "task_kind": "bounded-synthetic-code-repair",
    "pai_dir": pai_dir,
    "adapter_identity_marker": "PAI_CODEX_PEER_BETA_ADAPTER",
    "adapter_status": "peer-beta",
    "upstream_adapter": "claude",
    "agents_router_observed": True,
    "task_workspace": str(workspace),
    "files_modified": ["src/pai_priority.py"],
    "tests_run": ["python3 -m unittest discover -s tests"],
    "tests_passed": True,
    "memory_write_performed": False,
    "isa_write_performed": False,
    "pulse_probe_performed": False,
    "localhost_31337_called": False,
    "runtime_surface_created": False,
    "result_summary": "Fixed priority alias normalization in the synthetic workspace.",
    "evidence_classification": [
        "bounded task execution evidence",
        "synthetic task evidence",
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

    def _audit_fixture(
        self,
        tmp: str,
        *,
        events: list[dict[str, object]] | None = None,
        extra_after_marker: tuple[Path, str] | None = None,
        repo_extra_after_marker: tuple[Path, str] | None = None,
        home_extra_after_marker: tuple[Path, str] | None = None,
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
        implementation.write_text("def normalize_priority(value):\n    return 'low'\n", encoding="utf-8")
        os.utime(implementation, (after_marker, after_marker))

        result_path = run_dir / "task-result.json"
        events_path = run_dir / "task-events.jsonl"
        diff_path = run_dir / "task.diff"
        state_path = run_dir / "task-run-state.json"
        self._write_json(result_path, self._task_result(pai_dir, workspace), after_marker)
        self._write_events(events_path, events or [{"type": "file_change", "path": "src/pai_priority.py"}], after_marker)
        diff_path.write_text("--- a/src/pai_priority.py\n+++ b/src/pai_priority.py\n@@ -1 +1 @@\n-fixed\n+fixed\n", encoding="utf-8")
        os.utime(diff_path, (after_marker, after_marker))
        self._write_json(
            state_path,
            {
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

        if repo_extra_after_marker is not None:
            relative, text = repo_extra_after_marker
            extra_path = repo_root / relative
            extra_path.parent.mkdir(parents=True, exist_ok=True)
            extra_path.write_text(text, encoding="utf-8")
            os.utime(extra_path, (after_marker, after_marker))

        if home_extra_after_marker is not None:
            relative, text = home_extra_after_marker
            extra_path = home / relative
            extra_path.parent.mkdir(parents=True, exist_ok=True)
            extra_path.write_text(text, encoding="utf-8")
            os.utime(extra_path, (after_marker, after_marker))

        old_home = os.environ.get("HOME")
        os.environ["HOME"] = str(home)
        try:
            return audit_task(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                task_result=result_path,
                task_events=events_path,
                runtime_attempt_number=1,
                repo_root=repo_root,
            )
        finally:
            if old_home is None:
                os.environ.pop("HOME", None)
            else:
                os.environ["HOME"] = old_home

    def test_task_card_schema_accepts_s15c_task(self):
        self._assert_schema_accepts(TASK_CARD_SCHEMA, json.loads(TASK_CARD.read_text(encoding="utf-8")))

    def test_task_result_schema_accepts_required_shape(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            workspace = Path(tmp) / "workspace"
            self._assert_schema_accepts(TASK_RESULT_SCHEMA, self._task_result(Path(tmp) / "PAI", workspace))

    def test_task_result_schema_is_strict_output_compatible(self):
        schema = json.loads(TASK_RESULT_SCHEMA.read_text(encoding="utf-8"))
        self.assertFalse(schema.get("additionalProperties"))
        self.assertEqual(set(schema["properties"]), set(schema["required"]))

    def test_task_validation_schema_accepts_required_shape(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            self._assert_schema_accepts(TASK_VALIDATION_SCHEMA, self._task_validation_shape(Path(tmp) / "workspace"))

    def test_s15c_fixture_tests_fail_before_repair(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
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

    def test_task_runner_copies_fixture_to_isolated_workspace(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            payload = self._task_dry_run(launcher, pai_dir)
            workspace = Path(payload["task_workspace"])
            self.assertTrue((workspace / "README.md").is_file())
            self.assertTrue((workspace / "src" / "pai_priority.py").is_file())
            self.assertGreater(payload["initial_test_returncode"], 0)

    def test_task_runner_constructs_codex_exec_workspace_write_command(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            payload = self._task_dry_run(launcher, pai_dir)
            command = payload["workspace_write_command"]
            self.assertEqual(command[0], "codex")
            self.assertIn("exec", command)
            self.assertIn("--json", command)
            self.assertIn("--ephemeral", command)
            self.assertEqual(command[command.index("--sandbox") + 1], "workspace-write")
            self.assertEqual(Path(command[command.index("--cd") + 1]), Path(payload["task_workspace"]))
            self.assertIn("--output-schema", command)
            actual_command = payload["command"]
            self.assertEqual(actual_command[actual_command.index("--sandbox") + 1], "read-only")

    def test_task_runner_materializes_codex_repair_and_generates_diff(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            tmp_path = Path(tmp)
            pai_dir, _, launcher = self._install_synthetic(tmp)
            fake_bin = tmp_path / "bin"
            fake_bin.mkdir()
            self._fake_codex_bin(fake_bin)

            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = str(fake_bin) + os.pathsep + old_path
            try:
                run_dir = pai_dir / RUN_RELATIVE
                result = self._run_launcher(
                    launcher,
                    "task-run",
                    "--pai-dir",
                    str(pai_dir),
                    "--task-card",
                    str(pai_dir / "adapters" / "codex" / "tasks" / "s15c-synthetic-bugfix.json"),
                    "--run-dir",
                    str(run_dir),
                    "--result",
                    str(run_dir / "task-result.json"),
                    "--events-output",
                    str(run_dir / "task-events.jsonl"),
                )
            finally:
                os.environ["PATH"] = old_path

            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            workspace = run_dir / "workspace"
            self.assertTrue((run_dir / "task-result.json").is_file())
            self.assertTrue((run_dir / "task-events.jsonl").is_file())
            diff = (run_dir / "task.diff").read_text(encoding="utf-8")
            self.assertIn("src/pai_priority.py", diff)
            repaired = (workspace / "src" / "pai_priority.py").read_text(encoding="utf-8")
            self.assertIn("urgent", repaired)

    def test_task_runner_output_passes_launcher_audit_task(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            tmp_path = Path(tmp)
            pai_dir, _, launcher = self._install_synthetic(tmp)
            fake_bin = tmp_path / "bin"
            fake_bin.mkdir()
            self._fake_codex_bin(fake_bin)
            run_dir = pai_dir / RUN_RELATIVE
            marker = tmp_path / "marker"
            marker.write_text("marker\n", encoding="utf-8")
            old_marker_time = time.time() - 10
            os.utime(marker, (old_marker_time, old_marker_time))

            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = str(fake_bin) + os.pathsep + old_path
            try:
                self._run_launcher(
                    launcher,
                    "task-run",
                    "--pai-dir",
                    str(pai_dir),
                    "--task-card",
                    str(pai_dir / "adapters" / "codex" / "tasks" / "s15c-synthetic-bugfix.json"),
                    "--run-dir",
                    str(run_dir),
                    "--result",
                    str(run_dir / "task-result.json"),
                    "--events-output",
                    str(run_dir / "task-events.jsonl"),
                )
            finally:
                os.environ["PATH"] = old_path

            result = self._run_launcher(
                launcher,
                "audit-task",
                "--pai-dir",
                str(pai_dir),
                "--marker",
                str(marker),
                "--run-dir",
                str(run_dir),
                "--task-result",
                str(run_dir / "task-result.json"),
                "--task-events",
                str(run_dir / "task-events.jsonl"),
                "--output",
                str(run_dir / "task-validation.json"),
            )
            payload = json.loads(result.stdout)
            self.assertTrue(payload["validation_passed"])
            validation_path = run_dir / "task-validation.json"
            self.assertTrue(validation_path.is_file())
            validation = json.loads(validation_path.read_text(encoding="utf-8"))
            self.assertTrue(validation["task_initially_failed"])
            self.assertTrue(validation["task_tests_passed_after_repair"])
            self.assertTrue(validation["diff_present"])
            self.assertTrue(validation["event_attribution_passed"])

    def test_task_runner_rejects_workspace_outside_s15c_run_dir(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            outside = Path(tmp) / "outside"
            result = self._run_launcher(
                launcher,
                "task-run",
                "--pai-dir",
                str(pai_dir),
                "--task-card",
                str(pai_dir / "adapters" / "codex" / "tasks" / "s15c-synthetic-bugfix.json"),
                "--run-dir",
                str(outside),
                "--result",
                str(outside / "task-result.json"),
                "--events-output",
                str(outside / "task-events.jsonl"),
                "--dry-run",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("adapters/codex/runs/s15c", result.stderr)

    def test_task_runner_rejects_result_outside_s15c_run_dir(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            run_dir = pai_dir / RUN_RELATIVE
            outside = Path(tmp) / "task-result.json"
            result = self._run_launcher(
                launcher,
                "task-run",
                "--pai-dir",
                str(pai_dir),
                "--task-card",
                str(pai_dir / "adapters" / "codex" / "tasks" / "s15c-synthetic-bugfix.json"),
                "--run-dir",
                str(run_dir),
                "--result",
                str(outside),
                "--events-output",
                str(run_dir / "task-events.jsonl"),
                "--dry-run",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--result must stay under adapters/codex/runs/s15c", result.stderr)

    def test_task_runner_rejects_events_output_outside_s15c_run_dir(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            run_dir = pai_dir / RUN_RELATIVE
            outside = Path(tmp) / "task-events.jsonl"
            result = self._run_launcher(
                launcher,
                "task-run",
                "--pai-dir",
                str(pai_dir),
                "--task-card",
                str(pai_dir / "adapters" / "codex" / "tasks" / "s15c-synthetic-bugfix.json"),
                "--run-dir",
                str(run_dir),
                "--result",
                str(run_dir / "task-result.json"),
                "--events-output",
                str(outside),
                "--dry-run",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--events-output must stay under adapters/codex/runs/s15c", result.stderr)

    def test_task_runner_rejects_result_symlink_escape(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            run_dir = pai_dir / RUN_RELATIVE
            run_dir.mkdir(parents=True)
            outside = Path(tmp) / "task-result.json"
            symlink = run_dir / "task-result.json"
            symlink.symlink_to(outside)
            result = self._run_launcher(
                launcher,
                "task-run",
                "--pai-dir",
                str(pai_dir),
                "--task-card",
                str(pai_dir / "adapters" / "codex" / "tasks" / "s15c-synthetic-bugfix.json"),
                "--run-dir",
                str(run_dir),
                "--result",
                str(symlink),
                "--events-output",
                str(run_dir / "task-events.jsonl"),
                "--dry-run",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--result must stay under adapters/codex/runs/s15c", result.stderr)

    def test_task_runner_rejects_events_output_symlink_escape(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            run_dir = pai_dir / RUN_RELATIVE
            run_dir.mkdir(parents=True)
            outside = Path(tmp) / "task-events.jsonl"
            symlink = run_dir / "task-events.jsonl"
            symlink.symlink_to(outside)
            result = self._run_launcher(
                launcher,
                "task-run",
                "--pai-dir",
                str(pai_dir),
                "--task-card",
                str(pai_dir / "adapters" / "codex" / "tasks" / "s15c-synthetic-bugfix.json"),
                "--run-dir",
                str(run_dir),
                "--result",
                str(run_dir / "task-result.json"),
                "--events-output",
                str(symlink),
                "--dry-run",
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--events-output must stay under adapters/codex/runs/s15c", result.stderr)

    def test_audit_task_rejects_result_outside_s15c_run_dir(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            tmp_path = Path(tmp)
            pai_dir, _, launcher = self._install_synthetic(tmp)
            run_dir = pai_dir / RUN_RELATIVE
            run_dir.mkdir(parents=True)
            marker = tmp_path / "marker"
            marker.write_text("marker\n", encoding="utf-8")
            outside_result = tmp_path / "task-result.json"
            outside_result.write_text("{}\n", encoding="utf-8")
            result = self._run_launcher(
                launcher,
                "audit-task",
                "--pai-dir",
                str(pai_dir),
                "--marker",
                str(marker),
                "--run-dir",
                str(run_dir),
                "--task-result",
                str(outside_result),
                "--task-events",
                str(run_dir / "task-events.jsonl"),
                "--output",
                str(run_dir / "task-validation.json"),
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--task-result must stay under adapters/codex/runs/s15c", result.stderr)

    def test_audit_task_rejects_events_outside_s15c_run_dir(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            tmp_path = Path(tmp)
            pai_dir, _, launcher = self._install_synthetic(tmp)
            run_dir = pai_dir / RUN_RELATIVE
            run_dir.mkdir(parents=True)
            marker = tmp_path / "marker"
            marker.write_text("marker\n", encoding="utf-8")
            result_path = run_dir / "task-result.json"
            result_path.write_text("{}\n", encoding="utf-8")
            outside_events = tmp_path / "task-events.jsonl"
            outside_events.write_text("{}\n", encoding="utf-8")
            result = self._run_launcher(
                launcher,
                "audit-task",
                "--pai-dir",
                str(pai_dir),
                "--marker",
                str(marker),
                "--run-dir",
                str(run_dir),
                "--task-result",
                str(result_path),
                "--task-events",
                str(outside_events),
                "--output",
                str(run_dir / "task-validation.json"),
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--task-events must stay under adapters/codex/runs/s15c", result.stderr)

    def test_task_audit_accepts_clean_task_workspace_writes(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            result = self._audit_fixture(tmp)
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["event_attribution_passed"])
            self.assertTrue(result["approved_task_workspace_writes"])

    def test_task_audit_rejects_write_outside_task_workspace(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            pai_dir = Path(tmp) / "home" / ".claude" / "PAI"
            result = self._audit_fixture(tmp, events=[{"type": "file_change", "path": str(pai_dir / "AGENTS.md")}])
            self.assertFalse(result["validation_passed"])
            self.assertFalse(result["event_attribution_passed"])

    def test_task_audit_rejects_memory_write(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            result = self._audit_fixture(tmp, events=[{"type": "exec_command", "cmd": "touch Memory/WORK/item.md"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["memory_write_performed_by_codex"])

    def test_task_audit_rejects_isa_write(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            result = self._audit_fixture(tmp, events=[{"type": "exec_command", "cmd": "python -c 'write ISA/item.md'"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["isa_write_performed_by_codex"])

    def test_task_audit_rejects_pulse_probe(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            result = self._audit_fixture(tmp, events=[{"type": "exec_command", "cmd": "curl http://pai-pulse/status"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["pulse_probe_performed_by_codex"])

    def test_task_audit_rejects_localhost_31337(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            result = self._audit_fixture(tmp, events=[{"type": "exec_command", "cmd": "curl http://localhost:31337/health"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["localhost_31337_called_by_codex"])

    def test_task_audit_classifies_known_ambient_pai_churn(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            result = self._audit_fixture(tmp, extra_after_marker=(Path("Pulse") / "state" / "cache.json", "{}\n"))
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["ambient_pai_state_churn"])

    def test_task_audit_rejects_unknown_unclassified_write(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            result = self._audit_fixture(tmp, extra_after_marker=(Path("unexpected-state.json"), "{}\n"))
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["unknown_unclassified_writes"])

    def test_task_audit_rejects_repo_root_agents_creation(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            result = self._audit_fixture(tmp, repo_extra_after_marker=(Path("AGENTS.md"), "not approved\n"))
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["repo_root_agents_created"])

    def test_task_audit_rejects_repo_dotcodex_creation(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            result = self._audit_fixture(tmp, repo_extra_after_marker=(Path(".codex") / "config.toml", "# no\n"))
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["repo_dotcodex_created"])

    def test_task_audit_rejects_home_codex_adapter_surface(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            result = self._audit_fixture(tmp, home_extra_after_marker=(Path(".codex") / "AGENTS.md", "not approved\n"))
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["codex_adapter_files_installed_under_home_codex"])

    def test_installer_installs_task_payload_to_synthetic_pai_root(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            pai_dir, backup_root, launcher = self._install_synthetic(tmp)
            self.assertTrue(launcher.is_file())
            self.assertTrue((pai_dir / "adapters" / "codex" / "task-card.schema.json").is_file())
            self.assertTrue((pai_dir / "adapters" / "codex" / "task-result.schema.json").is_file())
            self.assertTrue((pai_dir / "adapters" / "codex" / "task-validation.schema.json").is_file())
            self.assertTrue((pai_dir / "adapters" / "codex" / "tasks" / "s15c-synthetic-bugfix.json").is_file())
            self.assertTrue((pai_dir / "adapters" / "codex" / "task-fixtures" / "s15c_bugfix" / "src" / "pai_priority.py").is_file())
            result = validate_install(pai_dir, backup_root)
            self.assertEqual(result["adapter_status"], "peer-beta")

    def test_installer_is_idempotent_with_task_payload(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
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

    def test_installer_rollback_removes_s15c_run_directory(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            pai_dir, backup_root, _ = self._install_synthetic(tmp)
            run_dir = pai_dir / RUN_RELATIVE
            run_dir.mkdir(parents=True)
            artifact = run_dir / "task-result.json"
            artifact.write_text("{}\n", encoding="utf-8")

            result = rollback_install(pai_dir, backup_root)

            self.assertFalse(run_dir.exists())
            self.assertIn(str(run_dir), result["changed_targets"])

    def test_task_harness_does_not_create_repo_root_or_dotcodex_surfaces(self):
        with tempfile.TemporaryDirectory(prefix="s15c.") as tmp:
            pai_dir, _, launcher = self._install_synthetic(tmp)
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            before = set(workspace.iterdir())
            self._task_dry_run(launcher, pai_dir)
            after = set(workspace.iterdir())
            self.assertEqual(before, after)
            self.assertFalse((workspace / "AGENTS.md").exists())
            self.assertFalse((workspace / ".codex").exists())


if __name__ == "__main__":
    unittest.main()
