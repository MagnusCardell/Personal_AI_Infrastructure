from __future__ import annotations

import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.pai_runtime_runner.audit import audit_repo_run
from tools.pai_runtime_runner.install import install_runtime
from tools.pai_runtime_runner.runner import (
    APPROVED_REPOSITORY_WRITE_SET,
    S15E_RUN_RELATIVE,
    S15E_TASK_RELATIVE,
    S15F_RUN_RELATIVE,
    S15F_TASK_RELATIVE,
    run_repo_runtime,
)


MARKER = "PAI_CODEX_PEER_BETA_ADAPTER"


class PaiRuntimeRunnerRepoTaskTests(unittest.TestCase):
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
        task = json.loads((pai_dir / S15E_TASK_RELATIVE).read_text(encoding="utf-8"))
        task["test_command"] = ["python3", "-c", "print('provider registry tests passed')"]
        (pai_dir / S15E_TASK_RELATIVE).write_text(json.dumps(task, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        patch_task = json.loads((pai_dir / S15F_TASK_RELATIVE).read_text(encoding="utf-8"))
        patch_task["test_command"] = ["python3", "-c", "print('patch proposal tests passed')"]
        (pai_dir / S15F_TASK_RELATIVE).write_text(
            json.dumps(patch_task, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return pai_dir

    def _git_repo(self, tmp: str) -> Path:
        repo = Path(tmp) / "repo"
        (repo / "tools" / "pai_runtime_runner").mkdir(parents=True)
        (repo / "tests").mkdir()
        (repo / "tools" / "pai_runtime_runner" / "provider_registry.py").write_text(
            "CODEX_PROVIDER_SEMANTICS = {}\n",
            encoding="utf-8",
        )
        (repo / "tests" / "test_pai_runtime_provider_registry.py").write_text(
            "import unittest\n\nclass RegistryTests(unittest.TestCase):\n    def test_placeholder(self):\n        self.assertTrue(True)\n",
            encoding="utf-8",
        )
        (repo / "tools" / "pai_runtime_runner" / "patch_proposal.py").write_text(
            "def validate_patch_proposal(proposal, approved_write_set):\n    return []\n",
            encoding="utf-8",
        )
        (repo / "tests" / "test_pai_runtime_patch_proposal.py").write_text(
            "import unittest\n\nclass PatchProposalTests(unittest.TestCase):\n    def test_placeholder(self):\n        self.assertTrue(True)\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return repo

    def _fake_codex_bin(self, bin_dir: Path) -> Path:
        codex = bin_dir / "codex"
        codex.write_text(
            """#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

args = sys.argv[1:]
output = Path(args[args.index("-o") + 1])
repo = Path(args[args.index("--cd") + 1])
registry = repo / "tools" / "pai_runtime_runner" / "provider_registry.py"
tests = repo / "tests" / "test_pai_runtime_provider_registry.py"
registry.write_text(registry.read_text(encoding="utf-8") + "\\nEXPECTED_CODEX_SEMANTIC_FIELDS = ('memory_write_policy', 'isa_write_policy', 'pulse_policy', 'replacement_status')\\n", encoding="utf-8")
tests.write_text(tests.read_text(encoding="utf-8") + "\\nclass S15ELiveRegistryTests(unittest.TestCase):\\n    def test_codex_semantic_fields_are_explicit(self):\\n        self.assertTrue(True)\\n", encoding="utf-8")
payload = {
    "milestone_name": "V5-S15E-PAI-RUNTIME-CODEX-REAL-REPO-TASK",
    "run_id": "s15e-provider-registry",
    "runtime": "codex",
    "runtime_status": "peer-beta",
    "provider_type": "codex-cli",
    "pai_dir": "",
    "repo_root": str(repo),
    "task_id": "s15e-provider-registry-repo-task",
    "task_kind": "bounded-real-repository-code-change",
    "adapter_identity_marker": "PAI_CODEX_PEER_BETA_ADAPTER",
    "adapter_status": "peer-beta",
    "upstream_adapter": "claude",
    "agents_router_observed": True,
    "pai_owned_run_directory": True,
    "repository_files_modified": [
        "tools/pai_runtime_runner/provider_registry.py",
        "tests/test_pai_runtime_provider_registry.py",
    ],
    "tests_run": ["python3 -c provider registry tests"],
    "tests_passed": True,
    "memory_write_performed": False,
    "isa_write_performed": False,
    "pulse_probe_performed": False,
    "localhost_31337_called": False,
    "runtime_surface_created": False,
    "result_summary": "Updated provider registry through a bounded repo task.",
    "evidence_classification": [
        "PAI-owned real repository task evidence",
        "runtime provider registry evidence",
        "not replacement readiness"
    ],
    "known_limits": ["synthetic test fake Codex only"],
}
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
print(json.dumps({"type": "file_change", "path": "tools/pai_runtime_runner/provider_registry.py"}))
print(json.dumps({"type": "file_change", "path": "tests/test_pai_runtime_provider_registry.py"}))
print(json.dumps({"type": "exec_command", "cmd": "python3 -m unittest tests.test_pai_runtime_provider_registry"}))
""",
            encoding="utf-8",
        )
        codex.chmod(codex.stat().st_mode | stat.S_IXUSR)
        return codex

    def _fake_codex_patch_bin(self, bin_dir: Path) -> Path:
        codex = bin_dir / "codex"
        codex.write_text(
            """#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

args = sys.argv[1:]
output = Path(args[args.index("-o") + 1])
repo = Path(args[args.index("--cd") + 1])
module_path = repo / "tools" / "pai_runtime_runner" / "patch_proposal.py"
test_path = repo / "tests" / "test_pai_runtime_patch_proposal.py"
module_content = module_path.read_text(encoding="utf-8") + "\\nPATCH_PROPOSAL_TEXT_ENCODING = 'utf-8'\\n"
test_content = test_path.read_text(encoding="utf-8") + "\\nclass S15FPatchApplyTests(unittest.TestCase):\\n    def test_text_encoding_constant_is_explicit(self):\\n        self.assertEqual('utf-8', 'utf-8')\\n"
proposal = {
    "proposal_id": "s15f-patch-proposal",
    "proposal_kind": "full-file-replacement",
    "unified_diff": "--- a/tools/pai_runtime_runner/patch_proposal.py\\n+++ b/tools/pai_runtime_runner/patch_proposal.py\\n",
    "changes": [
        {
            "path": "tools/pai_runtime_runner/patch_proposal.py",
            "mode": "replace-file",
            "content": module_content,
            "unified_diff": "--- a/tools/pai_runtime_runner/patch_proposal.py\\n+++ b/tools/pai_runtime_runner/patch_proposal.py\\n",
        },
        {
            "path": "tests/test_pai_runtime_patch_proposal.py",
            "mode": "replace-file",
            "content": test_content,
            "unified_diff": "--- a/tests/test_pai_runtime_patch_proposal.py\\n+++ b/tests/test_pai_runtime_patch_proposal.py\\n",
        },
    ],
}
payload = {
    "milestone_name": "V5-S15F-PAI-RUNTIME-PATCH-PROPOSAL-APPLIER",
    "run_id": "s15f-patch-proposal",
    "runtime": "codex",
    "runtime_status": "peer-beta",
    "provider_type": "codex-cli",
    "pai_dir": "",
    "repo_root": str(repo),
    "task_id": "s15f-patch-proposal-repo-task",
    "task_kind": "bounded-real-repository-code-change",
    "adapter_identity_marker": "PAI_CODEX_PEER_BETA_ADAPTER",
    "adapter_status": "peer-beta",
    "upstream_adapter": "claude",
    "agents_router_observed": True,
    "pai_owned_run_directory": True,
    "repository_files_modified": [
        "tools/pai_runtime_runner/patch_proposal.py",
        "tests/test_pai_runtime_patch_proposal.py",
    ],
    "tests_run": ["python3 -m unittest tests.test_pai_runtime_patch_proposal"],
    "tests_passed": True,
    "patch_proposal": proposal,
    "patch_proposal_produced": True,
    "patch_proposal_validated": False,
    "patch_proposal_applied_by_pai": False,
    "memory_write_performed": False,
    "isa_write_performed": False,
    "pulse_probe_performed": False,
    "localhost_31337_called": False,
    "runtime_surface_created": False,
    "result_summary": "Proposed patch proposal module replacements.",
    "evidence_classification": [
        "PAI-owned real repository task evidence",
        "patch proposal apply pipeline evidence",
        "not replacement readiness"
    ],
    "known_limits": ["synthetic test fake Codex only"],
}
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
print(json.dumps({"type": "file_change", "path": str(output)}))
print(json.dumps({"type": "exec_command", "cmd": "python3 -m unittest tests.test_pai_runtime_patch_proposal"}))
""",
            encoding="utf-8",
        )
        codex.chmod(codex.stat().st_mode | stat.S_IXUSR)
        return codex

    def _run_with_fake_codex(self, tmp: str) -> tuple[Path, Path, Path]:
        tmp_path = Path(tmp)
        pai_dir = self._install_synthetic(tmp)
        repo = self._git_repo(tmp)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        self._fake_codex_bin(fake_bin)
        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = str(fake_bin) + os.pathsep + old_path
        try:
            run_repo_runtime(
                pai_dir,
                "codex",
                pai_dir / S15E_TASK_RELATIVE,
                repo,
                pai_dir / S15E_RUN_RELATIVE,
            )
        finally:
            os.environ["PATH"] = old_path
        return pai_dir, repo, pai_dir / S15E_RUN_RELATIVE

    def _run_patch_with_fake_codex(self, tmp: str) -> tuple[Path, Path, Path]:
        tmp_path = Path(tmp)
        pai_dir = self._install_synthetic(tmp)
        repo = self._git_repo(tmp)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        self._fake_codex_patch_bin(fake_bin)
        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = str(fake_bin) + os.pathsep + old_path
        try:
            run_repo_runtime(
                pai_dir,
                "codex",
                pai_dir / S15F_TASK_RELATIVE,
                repo,
                pai_dir / S15F_RUN_RELATIVE,
            )
        finally:
            os.environ["PATH"] = old_path
        return pai_dir, repo, pai_dir / S15F_RUN_RELATIVE

    def _repo_run_result(self, pai_dir: Path, repo_root: Path) -> dict[str, object]:
        return {
            "milestone_name": "V5-S15E-PAI-RUNTIME-CODEX-REAL-REPO-TASK",
            "run_id": "s15e-provider-registry",
            "runtime": "codex",
            "runtime_status": "peer-beta",
            "provider_type": "codex-cli",
            "pai_dir": str(pai_dir),
            "repo_root": str(repo_root),
            "task_id": "s15e-provider-registry-repo-task",
            "task_kind": "bounded-real-repository-code-change",
            "adapter_identity_marker": MARKER,
            "adapter_status": "peer-beta",
            "upstream_adapter": "claude",
            "agents_router_observed": True,
            "pai_owned_run_directory": True,
            "repository_files_modified": [
                "tools/pai_runtime_runner/provider_registry.py",
                "tests/test_pai_runtime_provider_registry.py",
            ],
            "tests_run": ["python3 -m unittest tests.test_pai_runtime_provider_registry"],
            "tests_passed": True,
            "memory_write_performed": False,
            "isa_write_performed": False,
            "pulse_probe_performed": False,
            "localhost_31337_called": False,
            "runtime_surface_created": False,
            "result_summary": "Updated provider registry through a bounded repo task.",
            "evidence_classification": [
                "PAI-owned real repository task evidence",
                "runtime provider registry evidence",
                "not replacement readiness",
            ],
            "known_limits": ["fixture evidence only"],
        }

    def _patch_repo_run_result(self, pai_dir: Path, repo_root: Path) -> dict[str, object]:
        return {
            "milestone_name": "V5-S15F-PAI-RUNTIME-PATCH-PROPOSAL-APPLIER",
            "run_id": "s15f-patch-proposal",
            "runtime": "codex",
            "runtime_status": "peer-beta",
            "provider_type": "codex-cli",
            "pai_dir": str(pai_dir),
            "repo_root": str(repo_root),
            "task_id": "s15f-patch-proposal-repo-task",
            "task_kind": "bounded-real-repository-code-change",
            "adapter_identity_marker": MARKER,
            "adapter_status": "peer-beta",
            "upstream_adapter": "claude",
            "agents_router_observed": True,
            "pai_owned_run_directory": True,
            "repository_files_modified": [
                "tools/pai_runtime_runner/patch_proposal.py",
                "tests/test_pai_runtime_patch_proposal.py",
            ],
            "tests_run": [
                "python3 -m unittest tests.test_pai_runtime_patch_proposal tests.test_pai_runtime_runner_repo_task tests.test_pai_runtime_provider_registry"
            ],
            "tests_passed": True,
            "patch_proposal_produced": True,
            "patch_proposal_validated": True,
            "patch_proposal_applied_by_pai": True,
            "memory_write_performed": False,
            "isa_write_performed": False,
            "pulse_probe_performed": False,
            "localhost_31337_called": False,
            "runtime_surface_created": False,
            "result_summary": "Applied a validated patch proposal through PAI.",
            "evidence_classification": [
                "PAI-owned real repository task evidence",
                "patch proposal apply pipeline evidence",
                "not replacement readiness",
            ],
            "known_limits": ["fixture evidence only"],
        }

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
        extra_repo_after_marker: tuple[Path, str] | None = None,
        make_dotcodex: bool = False,
    ) -> dict[str, object]:
        base = Path(tmp)
        pai_dir = base / "home" / ".claude" / "PAI"
        run_dir = pai_dir / S15E_RUN_RELATIVE
        repo_root = base / "repo"
        home = base / "user-home"
        run_dir.mkdir(parents=True)
        repo_root.mkdir(parents=True)
        home.mkdir(parents=True)

        marker = base / "marker"
        marker.write_text("marker\n", encoding="utf-8")
        after_marker = marker.stat().st_mtime + 2

        for relative in (
            Path("tools/pai_runtime_runner/provider_registry.py"),
            Path("tests/test_pai_runtime_provider_registry.py"),
        ):
            target = repo_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("changed\n", encoding="utf-8")
            os.utime(target, (after_marker, after_marker))

        if extra_repo_after_marker is not None:
            relative, text = extra_repo_after_marker
            target = repo_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
            os.utime(target, (after_marker, after_marker))

        if make_dotcodex:
            (repo_root / ".codex").mkdir()

        self._write_json(run_dir / "repo-run-result.json", self._repo_run_result(pai_dir, repo_root), after_marker)
        self._write_events(
            run_dir / "repo-events.jsonl",
            events
            or [
                {"type": "file_change", "path": "tools/pai_runtime_runner/provider_registry.py"},
                {"type": "file_change", "path": "tests/test_pai_runtime_provider_registry.py"},
                {"type": "exec_command", "cmd": "python3 -m unittest tests.test_pai_runtime_provider_registry"},
            ],
            after_marker,
        )
        diff = (
            "--- a/tools/pai_runtime_runner/provider_registry.py\n"
            "+++ b/tools/pai_runtime_runner/provider_registry.py\n"
            "@@ -1 +1 @@\n"
            "-old\n"
            "+new\n"
            "--- a/tests/test_pai_runtime_provider_registry.py\n"
            "+++ b/tests/test_pai_runtime_provider_registry.py\n"
            "@@ -1 +1 @@\n"
            "-old\n"
            "+new\n"
        )
        diff_path = run_dir / "repo-task.diff"
        diff_path.write_text(diff, encoding="utf-8")
        os.utime(diff_path, (after_marker, after_marker))
        self._write_json(
            run_dir / "repo-run-state.json",
            {
                "pai_runtime_command": ["pai-runtime", "run-repo", "--runtime", "codex"],
                "provider_command": ["codex", "exec", "--json", "--sandbox", "workspace-write"],
                "provider_registry_tests_returncode": 0,
            },
            after_marker,
        )

        old_home = os.environ.get("HOME")
        os.environ["HOME"] = str(home)
        try:
            return audit_repo_run(
                pai_dir=pai_dir,
                marker=marker,
                repo_root=repo_root,
                run_dir=run_dir,
                result_path=run_dir / "repo-run-result.json",
                events_path=run_dir / "repo-events.jsonl",
                diff_path=run_dir / "repo-task.diff",
                runtime_attempt_number=1,
            )
        finally:
            if old_home is None:
                os.environ.pop("HOME", None)
            else:
                os.environ["HOME"] = old_home

    def _patch_audit_fixture(
        self,
        tmp: str,
        *,
        validated: bool = True,
    ) -> dict[str, object]:
        base = Path(tmp)
        pai_dir = base / "home" / ".claude" / "PAI"
        run_dir = pai_dir / S15F_RUN_RELATIVE
        repo_root = base / "repo"
        home = base / "user-home"
        run_dir.mkdir(parents=True)
        repo_root.mkdir(parents=True)
        home.mkdir(parents=True)

        marker = base / "marker"
        marker.write_text("marker\n", encoding="utf-8")
        after_marker = marker.stat().st_mtime + 2

        for relative in (
            Path("tools/pai_runtime_runner/patch_proposal.py"),
            Path("tests/test_pai_runtime_patch_proposal.py"),
        ):
            target = repo_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("changed\n", encoding="utf-8")
            os.utime(target, (after_marker, after_marker))

        result = self._patch_repo_run_result(pai_dir, repo_root)
        if not validated:
            result["patch_proposal_validated"] = False
        self._write_json(run_dir / "repo-run-result.json", result, after_marker)
        self._write_events(
            run_dir / "repo-events.jsonl",
            [
                {"type": "file_change", "path": str(run_dir / "patch-proposal.json")},
                {"type": "exec_command", "cmd": "python3 -m unittest tests.test_pai_runtime_patch_proposal"},
            ],
            after_marker,
        )
        proposal = {
            "proposal_id": "s15f-patch-proposal",
            "proposal_kind": "full-file-replacement",
            "changes": [
                {
                    "path": "tools/pai_runtime_runner/patch_proposal.py",
                    "mode": "replace-file",
                    "content": "changed\n",
                    "unified_diff": "--- a/tools/pai_runtime_runner/patch_proposal.py\n+++ b/tools/pai_runtime_runner/patch_proposal.py\n",
                },
                {
                    "path": "tests/test_pai_runtime_patch_proposal.py",
                    "mode": "replace-file",
                    "content": "changed\n",
                    "unified_diff": "--- a/tests/test_pai_runtime_patch_proposal.py\n+++ b/tests/test_pai_runtime_patch_proposal.py\n",
                },
            ],
        }
        self._write_json(run_dir / "patch-proposal.json", proposal, after_marker)
        diff = (
            "--- a/tools/pai_runtime_runner/patch_proposal.py\n"
            "+++ b/tools/pai_runtime_runner/patch_proposal.py\n"
            "@@ -1 +1 @@\n"
            "-old\n"
            "+new\n"
            "--- a/tests/test_pai_runtime_patch_proposal.py\n"
            "+++ b/tests/test_pai_runtime_patch_proposal.py\n"
            "@@ -1 +1 @@\n"
            "-old\n"
            "+new\n"
        )
        diff_path = run_dir / "repo-task.diff"
        diff_path.write_text(diff, encoding="utf-8")
        os.utime(diff_path, (after_marker, after_marker))
        self._write_json(
            run_dir / "repo-run-state.json",
            {
                "pai_runtime_command": ["pai-runtime", "run-repo", "--runtime", "codex"],
                "provider_command": ["codex", "exec", "--json", "--sandbox", "workspace-write"],
                "patch_proposal_produced": True,
                "patch_proposal_validated": validated,
                "patch_proposal_applied_by_pai": True,
                "patch_proposal_tests_returncode": 0,
            },
            after_marker,
        )

        old_home = os.environ.get("HOME")
        os.environ["HOME"] = str(home)
        try:
            return audit_repo_run(
                pai_dir=pai_dir,
                marker=marker,
                repo_root=repo_root,
                run_dir=run_dir,
                result_path=run_dir / "repo-run-result.json",
                events_path=run_dir / "repo-events.jsonl",
                diff_path=run_dir / "repo-task.diff",
                runtime_attempt_number=1,
            )
        finally:
            if old_home is None:
                os.environ.pop("HOME", None)
            else:
                os.environ["HOME"] = old_home

    def test_pai_runtime_run_repo_rejects_unknown_runtime(self):
        with tempfile.TemporaryDirectory(prefix="s15e.repo.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            repo = self._git_repo(tmp)
            with self.assertRaises(ValueError):
                run_repo_runtime(pai_dir, "claude", pai_dir / S15E_TASK_RELATIVE, repo, pai_dir / S15E_RUN_RELATIVE)

    def test_pai_runtime_run_repo_requires_repo_root(self):
        with tempfile.TemporaryDirectory(prefix="s15e.repo.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            with self.assertRaises(ValueError):
                run_repo_runtime(pai_dir, "codex", pai_dir / S15E_TASK_RELATIVE, "", pai_dir / S15E_RUN_RELATIVE)

    def test_pai_runtime_run_repo_rejects_repo_root_outside_git_worktree(self):
        with tempfile.TemporaryDirectory(prefix="s15e.repo.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            outside = Path(tmp) / "not-git"
            outside.mkdir()
            with self.assertRaises(ValueError):
                run_repo_runtime(pai_dir, "codex", pai_dir / S15E_TASK_RELATIVE, outside, pai_dir / S15E_RUN_RELATIVE)

    def test_pai_runtime_run_repo_writes_pai_owned_run_artifacts(self):
        with tempfile.TemporaryDirectory(prefix="s15e.repo.") as tmp:
            _, _, run_dir = self._run_with_fake_codex(tmp)
            self.assertTrue((run_dir / "repo-run-result.json").is_file())
            self.assertTrue((run_dir / "repo-events.jsonl").is_file())
            self.assertTrue((run_dir / "repo-task.diff").is_file())
            self.assertTrue((run_dir / "repo-run-state.json").is_file())

    def test_pai_runtime_run_repo_delegates_to_codex_provider(self):
        with tempfile.TemporaryDirectory(prefix="s15e.repo.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            repo = self._git_repo(tmp)
            payload = run_repo_runtime(
                pai_dir,
                "codex",
                pai_dir / S15E_TASK_RELATIVE,
                repo,
                pai_dir / S15E_RUN_RELATIVE,
                dry_run=True,
            )
            self.assertIn("exec", payload["provider_command"])
            self.assertIn("workspace-write", payload["provider_command"])

    def test_pai_runtime_run_repo_uses_read_only_codex_sandbox_for_patch_proposal(self):
        with tempfile.TemporaryDirectory(prefix="s15f.repo.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            repo = self._git_repo(tmp)
            payload = run_repo_runtime(
                pai_dir,
                "codex",
                pai_dir / S15F_TASK_RELATIVE,
                repo,
                pai_dir / S15F_RUN_RELATIVE,
                dry_run=True,
            )
            self.assertIn("exec", payload["provider_command"])
            self.assertIn("read-only", payload["provider_command"])
            self.assertNotIn("workspace-write", payload["provider_command"])

    def test_repo_run_result_schema_is_codex_structured_output_compatible(self):
        schema = json.loads(Path("pai-runtime/repo-run-result.schema.json").read_text(encoding="utf-8"))
        self.assertNotIn("allOf", schema)
        self.assertIn("patch_proposal", schema["required"])
        self.assertIn("provider_registry_file_content", schema["required"])

    def test_pai_runtime_run_repo_can_use_patch_proposal_apply_mode(self):
        with tempfile.TemporaryDirectory(prefix="s15f.repo.") as tmp:
            _, repo, run_dir = self._run_patch_with_fake_codex(tmp)
            self.assertTrue((run_dir / "patch-proposal.json").is_file())
            self.assertIn(
                "PATCH_PROPOSAL_TEXT_ENCODING",
                (repo / "tools/pai_runtime_runner/patch_proposal.py").read_text(encoding="utf-8"),
            )
            result = json.loads((run_dir / "repo-run-result.json").read_text(encoding="utf-8"))
            self.assertTrue(result["patch_proposal_produced"])
            self.assertTrue(result["patch_proposal_validated"])
            self.assertTrue(result["patch_proposal_applied_by_pai"])

    def test_pai_runtime_audit_repo_accepts_approved_repository_writes(self):
        with tempfile.TemporaryDirectory(prefix="s15e.repo.") as tmp:
            result = self._audit_fixture(tmp)
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["event_attribution_passed"])

    def test_pai_runtime_audit_repo_accepts_pai_applied_patch_proposal(self):
        with tempfile.TemporaryDirectory(prefix="s15f.repo.") as tmp:
            result = self._patch_audit_fixture(tmp)
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["patch_proposal_present"])
            self.assertTrue(result["patch_proposal_valid"])
            self.assertTrue(result["patch_proposal_limited_to_approved_repository_write_set"])
            self.assertTrue(result["patch_proposal_tests_passed"])

    def test_pai_runtime_audit_repo_rejects_unvalidated_patch_proposal(self):
        with tempfile.TemporaryDirectory(prefix="s15f.repo.") as tmp:
            result = self._patch_audit_fixture(tmp, validated=False)
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["forbidden_semantic_writes"])

    def test_pai_runtime_audit_repo_rejects_unapproved_repository_write(self):
        with tempfile.TemporaryDirectory(prefix="s15e.repo.") as tmp:
            result = self._audit_fixture(tmp, extra_repo_after_marker=(Path("README.md"), "no\n"))
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["forbidden_repository_writes"])

    def test_pai_runtime_audit_repo_rejects_root_agents_creation(self):
        with tempfile.TemporaryDirectory(prefix="s15e.repo.") as tmp:
            result = self._audit_fixture(tmp, extra_repo_after_marker=(Path("AGENTS.md"), "no\n"))
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["repo_root_agents_created"])

    def test_pai_runtime_audit_repo_rejects_dotcodex_creation(self):
        with tempfile.TemporaryDirectory(prefix="s15e.repo.") as tmp:
            result = self._audit_fixture(tmp, make_dotcodex=True)
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["repo_dotcodex_created"])

    def test_pai_runtime_audit_repo_rejects_memory_write(self):
        with tempfile.TemporaryDirectory(prefix="s15e.repo.") as tmp:
            result = self._audit_fixture(tmp, events=[{"type": "exec_command", "cmd": "touch Memory/WORK/s15e.txt"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["memory_write_performed_by_codex"])

    def test_pai_runtime_audit_repo_rejects_isa_write(self):
        with tempfile.TemporaryDirectory(prefix="s15e.repo.") as tmp:
            result = self._audit_fixture(tmp, events=[{"type": "exec_command", "cmd": "touch ISA/s15e.md"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["isa_write_performed_by_codex"])

    def test_pai_runtime_audit_repo_rejects_pulse_probe(self):
        with tempfile.TemporaryDirectory(prefix="s15e.repo.") as tmp:
            result = self._audit_fixture(tmp, events=[{"type": "exec_command", "cmd": "curl http://pai/Pulse/events"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["pulse_probe_performed_by_codex"])

    def test_pai_runtime_audit_repo_rejects_localhost_31337(self):
        with tempfile.TemporaryDirectory(prefix="s15e.repo.") as tmp:
            result = self._audit_fixture(tmp, events=[{"type": "exec_command", "cmd": "curl http://localhost:31337"}])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["localhost_31337_called_by_codex"])


if __name__ == "__main__":
    unittest.main()
