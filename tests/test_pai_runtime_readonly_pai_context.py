from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator, ValidationError

from tools.pai_runtime_runner.audit import audit_pai_context_run
from tools.pai_runtime_runner.capabilities import CapabilityPolicyError
from tools.pai_runtime_runner.install import (
    INSTALL_TEXT_TARGETS,
    RuntimeInstallError,
    S15I_MUTABLE_INSTALL_RELATIVES,
    _validate_schema_file,
    install_runtime,
    validate_staged_payload,
)
from tools.pai_runtime_runner.pai_context import (
    S15I_MILESTONE,
    S15I_RUN_ID,
    context_report_from_capsule,
    collect_pai_context_metadata,
    normalize_context_report,
    validate_context_capsule,
    validate_context_report,
)
from tools.pai_runtime_runner.providers.codex import build_pai_context_provider_command
from tools.pai_runtime_runner.runner import (
    RunnerError,
    S15I_RUN_RELATIVE,
    S15I_TASK_RELATIVE,
    audit_pai_context_runtime_run,
    main as runner_main,
    run_pai_context_runtime,
)


class PaiRuntimeReadOnlyPaiContextTests(unittest.TestCase):
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

    def _add_context_dirs(self, pai_dir: Path) -> None:
        for relative in (
            Path("Memory") / "WORK",
            Path("Memory") / "LEARNING",
            Path("Memory") / "KNOWLEDGE",
            Path("ISA"),
            Path("Pulse") / "events",
        ):
            (pai_dir / relative).mkdir(parents=True, exist_ok=True)
        (pai_dir / "Memory" / "WORK" / "secret.md").write_text("memory body must stay unread\n", encoding="utf-8")
        (pai_dir / "ISA" / "secret.md").write_text("isa body must stay unread\n", encoding="utf-8")
        (pai_dir / "Pulse" / "events" / "event.json").write_text('{"payload": "unread"}\n', encoding="utf-8")

    def _fake_codex_bin(self, bin_dir: Path) -> Path:
        codex = bin_dir / "codex"
        codex.write_text(
            """#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

args = sys.argv[1:]
output = Path(args[args.index("-o") + 1])
payload = {
    "milestone_name": "V5-S15I-PAI-RUNTIME-READONLY-PAI-CONTEXT-TASK",
    "run_id": "s15i-read-only-pai-context",
    "runtime": "codex",
    "runtime_status": "peer-beta",
    "provider_type": "codex-cli",
    "pai_dir_label": "~/.claude/PAI",
    "task_id": "s15i-readonly-pai-context-task",
    "task_kind": "readonly-pai-metadata-context",
    "adapter_identity_marker": "PAI_CODEX_PEER_BETA_ADAPTER",
    "upstream_adapter": "claude",
    "agents_router_observed": True,
    "context_capsule_used": True,
    "context_capsule_metadata_only": True,
    "runtime_provider_count": 1,
    "runtime_provider_names": ["codex"],
    "codex_provider_status": "peer-beta",
    "codex_capabilities_observed": ["pai.context.read.metadata"],
    "memory_categories_observed": ["WORK"],
    "memory_body_read": False,
    "isa_body_read": False,
    "pulse_event_payload_read": False,
    "claude_project_memory_read": False,
    "codex_memory_read": False,
    "pulse_probe_performed": False,
    "localhost_31337_called": False,
    "context_summary": "Fake Codex mentioned localhost:31337." if os.environ.get("PAI_FAKE_CONTEXT_FORBIDDEN_TEXT") == "1" else "Fake Codex consumed the sanitized capsule.",
    "evidence_classification": ["read-only PAI metadata context evidence"],
    "known_limits": ["synthetic fake Codex mentioned /home/example"] if os.environ.get("PAI_FAKE_CONTEXT_FORBIDDEN_TEXT") == "1" else ["synthetic fake Codex only"],
}
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
print(json.dumps({"type": "message", "message": "context report emitted"}))
""",
            encoding="utf-8",
        )
        codex.chmod(codex.stat().st_mode | stat.S_IXUSR)
        return codex

    def _run_with_fake_codex(self, tmp: str, forbidden_report_text: bool = False) -> tuple[Path, Path]:
        tmp_path = Path(tmp)
        pai_dir = self._install_synthetic(tmp)
        self._add_context_dirs(pai_dir)
        marker = tmp_path / "marker"
        marker.write_text("marker\n", encoding="utf-8")
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        self._fake_codex_bin(fake_bin)
        old_path = os.environ.get("PATH", "")
        old_forbidden = os.environ.get("PAI_FAKE_CONTEXT_FORBIDDEN_TEXT")
        os.environ["PATH"] = str(fake_bin) + os.pathsep + old_path
        if forbidden_report_text:
            os.environ["PAI_FAKE_CONTEXT_FORBIDDEN_TEXT"] = "1"
        else:
            os.environ.pop("PAI_FAKE_CONTEXT_FORBIDDEN_TEXT", None)
        try:
            run_pai_context_runtime(
                pai_dir,
                "codex",
                pai_dir / S15I_TASK_RELATIVE,
                pai_dir / S15I_RUN_RELATIVE,
            )
        finally:
            os.environ["PATH"] = old_path
            if old_forbidden is None:
                os.environ.pop("PAI_FAKE_CONTEXT_FORBIDDEN_TEXT", None)
            else:
                os.environ["PAI_FAKE_CONTEXT_FORBIDDEN_TEXT"] = old_forbidden
        return pai_dir, marker

    def _write_clean_context_artifacts(self, pai_dir: Path, run_dir: Path) -> None:
        run_dir.mkdir(parents=True, exist_ok=True)
        capsule = collect_pai_context_metadata(pai_dir)
        report = context_report_from_capsule(capsule)
        (run_dir / "pai-context-capsule.json").write_text(
            json.dumps(capsule, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (run_dir / "pai-context-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        state = {
            "pai_runtime_command": [
                str(pai_dir / "bin" / "pai-runtime"),
                "run-pai-context",
                "--pai-dir",
                str(pai_dir),
                "--runtime",
                "codex",
                "--task-card",
                str(pai_dir / S15I_TASK_RELATIVE),
                "--run-dir",
                str(run_dir),
            ],
            "provider_command": [
                "codex",
                "--ask-for-approval",
                "never",
                "exec",
                "--skip-git-repo-check",
                "--ephemeral",
                "--json",
                "--sandbox",
                "read-only",
                "--cd",
                str(run_dir),
                "--add-dir",
                str(run_dir),
                "--output-schema",
                str(run_dir / "pai-context-report.schema.json"),
                "-o",
                str(run_dir / "pai-context-report.json"),
                "[sanitized-pai-context-prompt]",
            ],
        }
        (run_dir / "pai-context-state.json").write_text(
            json.dumps(state, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def _audit_with_event(self, tmp: str, event: dict[str, object]) -> dict[str, object]:
        pai_dir = self._install_synthetic(tmp)
        self._add_context_dirs(pai_dir)
        run_dir = pai_dir / S15I_RUN_RELATIVE
        marker = Path(tmp) / "marker"
        marker.write_text("marker\n", encoding="utf-8")
        self._write_clean_context_artifacts(pai_dir, run_dir)
        (run_dir / "pai-context-events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
        return audit_pai_context_run(
            pai_dir=pai_dir,
            marker=marker,
            run_dir=run_dir,
            capsule_path=run_dir / "pai-context-capsule.json",
            report_path=run_dir / "pai-context-report.json",
            events_path=run_dir / "pai-context-events.jsonl",
        )

    def test_context_collector_includes_runtime_provider_metadata(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            capsule = collect_pai_context_metadata(pai_dir)
            self.assertEqual(capsule["runtime_provider_names"], ["codex"])
            self.assertEqual(capsule["runtime_providers"][0]["runtime_status"], "peer-beta")
            self.assertIn("pai.context.read.metadata", capsule["runtime_providers"][0]["capabilities"])

    def test_install_runtime_live_mode_writes_only_s15i_mutable_targets(self):
        with tempfile.TemporaryDirectory(prefix="s15i.live-install.") as tmp:
            home = Path(tmp) / "home"
            pai_dir = home / ".claude" / "PAI"
            backup_root = Path(tmp) / "backup"
            pai_dir.mkdir(parents=True)
            (backup_root / ".claude" / "PAI").mkdir(parents=True)

            for relative in INSTALL_TEXT_TARGETS.values():
                if relative in S15I_MUTABLE_INSTALL_RELATIVES:
                    continue
                target = pai_dir / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("pre-s15i live runtime payload\n", encoding="utf-8")

            with mock.patch("tools.pai_runtime_runner.install.Path.home", return_value=home):
                result = install_runtime(pai_dir, backup_root)

            changed = {Path(item).relative_to(pai_dir) for item in result["changed_targets"]}
            self.assertTrue(changed)
            self.assertLessEqual(changed, S15I_MUTABLE_INSTALL_RELATIVES)

    def test_context_collector_includes_runtime_state_metadata(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            capsule = collect_pai_context_metadata(pai_dir)
            self.assertIn("milestone_name", capsule["runtime_state"]["summary_keys"])
            self.assertIn("supports_pai_context_metadata", capsule["runtime_state"]["summary_keys"])
            self.assertNotIn("scalar_summary", capsule["runtime_state"])

    def test_context_collector_includes_top_level_pai_structure_metadata(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            capsule = collect_pai_context_metadata(pai_dir)
            self.assertIn("runtimes", capsule["top_level_pai_structure"]["directories"])
            self.assertIn("AGENTS.md", capsule["top_level_pai_structure"]["files"])

    def test_context_collector_includes_memory_category_presence_without_bodies(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            self._add_context_dirs(pai_dir)
            capsule = collect_pai_context_metadata(pai_dir)
            work = next(item for item in capsule["memory_categories"] if item["category"] == "WORK")
            self.assertTrue(work["present"])
            self.assertEqual(work["file_count"], 1)
            self.assertFalse(work["body_read"])
            self.assertNotIn("memory body must stay unread", json.dumps(capsule))

    def test_context_collector_does_not_count_isa_or_pulse_payload_files(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            self._add_context_dirs(pai_dir)
            capsule = collect_pai_context_metadata(pai_dir)
            self.assertTrue(capsule["isa"]["present"])
            self.assertIsNone(capsule["isa"]["file_count"])
            self.assertEqual(capsule["isa"]["file_count_scope"], "not-collected")
            self.assertTrue(capsule["pulse"]["present"])
            self.assertIsNone(capsule["pulse"]["file_count"])
            self.assertEqual(capsule["pulse"]["file_count_scope"], "not-collected")
            raw = json.dumps(capsule, sort_keys=True)
            self.assertNotIn("secret.md", raw)
            self.assertNotIn("event.json", raw)

    def test_context_collector_ignores_symlinked_metadata_entries(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            self._add_context_dirs(pai_dir)
            outside = Path(tmp) / "outside-secret.md"
            outside.write_text("outside body must stay unread\n", encoding="utf-8")
            os.symlink(outside, pai_dir / "Memory" / "WORK" / "outside-link.md")
            os.symlink(pai_dir / "Pulse", pai_dir / "PulseLink", target_is_directory=True)
            shutil.rmtree(pai_dir / "Memory" / "LEARNING")
            outside_learning = Path(tmp) / "outside-learning"
            outside_learning.mkdir()
            (outside_learning / "leaked.md").write_text("symlinked memory body must stay unread\n", encoding="utf-8")
            os.symlink(outside_learning, pai_dir / "Memory" / "LEARNING", target_is_directory=True)

            capsule = collect_pai_context_metadata(pai_dir)
            work = next(item for item in capsule["memory_categories"] if item["category"] == "WORK")
            learning = next(item for item in capsule["memory_categories"] if item["category"] == "LEARNING")
            self.assertEqual(work["file_count"], 1)
            self.assertFalse(learning["present"])
            self.assertEqual(learning["file_count"], 0)
            self.assertNotIn("PulseLink", capsule["top_level_pai_structure"]["directories"])
            raw = json.dumps(capsule, sort_keys=True)
            self.assertNotIn("outside-link.md", raw)
            self.assertNotIn("leaked.md", raw)
            self.assertNotIn("outside body must stay unread", raw)
            self.assertNotIn("symlinked memory body must stay unread", raw)

    def test_context_collector_rejects_memory_body_reads(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            result = self._audit_with_event(
                tmp,
                {"type": "exec_command", "cmd": "cat ~/.claude/PAI/Memory/WORK/secret.md"},
            )
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["memory_body_read_by_codex"])

    def test_context_collector_rejects_isa_body_reads(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            result = self._audit_with_event(tmp, {"type": "exec_command", "cmd": "cat ~/.claude/PAI/ISA/secret.md"})
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["isa_body_read_by_codex"])

    def test_context_collector_rejects_pulse_event_payload_reads(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            result = self._audit_with_event(
                tmp,
                {"type": "exec_command", "cmd": "cat ~/.claude/PAI/Pulse/events/event.json"},
            )
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["pulse_event_payload_read_by_codex"])

    def test_context_capsule_uses_redacted_paths(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            capsule = collect_pai_context_metadata(pai_dir)
            raw = json.dumps(capsule, sort_keys=True)
            self.assertEqual(capsule["pai_dir_label"], "~/.claude/PAI")
            self.assertNotIn(tmp, raw)
            self.assertNotIn("/home/", raw)

    def test_context_capsule_schema_accepts_metadata_only_capsule(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            capsule = collect_pai_context_metadata(pai_dir)
            self.assertEqual(validate_context_capsule(capsule), [])
            schema = json.loads(Path("pai-runtime/pai-context-capsule.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(capsule)

    def test_context_capsule_schema_requires_codex_provider_metadata(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            capsule = collect_pai_context_metadata(pai_dir)
            schema = json.loads(Path("pai-runtime/pai-context-capsule.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)

            capsule["runtime_provider_names"] = []
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(capsule)

            capsule = collect_pai_context_metadata(pai_dir)
            capsule["runtime_providers"] = []
            capsule["runtime_provider_count"] = 0
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(capsule)

            capsule = collect_pai_context_metadata(pai_dir)
            capsule["runtime_providers"][0]["capabilities"] = []
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(capsule)

    def test_context_capsule_schema_rejects_unredacted_nested_metadata(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            capsule = collect_pai_context_metadata(pai_dir)
            schema = json.loads(Path("pai-runtime/pai-context-capsule.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)

            provider_leak = json.loads(json.dumps(capsule))
            provider_leak["runtime_providers"][0]["runtime_name"] = "/home/example/provider"
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(provider_leak)

            provider_case_leak = json.loads(json.dumps(capsule))
            provider_case_leak["runtime_providers"][0]["runtime_name"] = "/Home/example/provider"
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(provider_case_leak)

            runtime_state_leak = json.loads(json.dumps(capsule))
            runtime_state_leak["runtime_state"]["summary_keys"].append("localhost:31337")
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(runtime_state_leak)

            endpoint_case_leak = json.loads(json.dumps(capsule))
            endpoint_case_leak["collection_policy"].append("Do not expose LocalHost:31337.")
            self.assertTrue(validate_context_capsule(endpoint_case_leak))
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(endpoint_case_leak)

            codex_home_leak = json.loads(json.dumps(capsule))
            codex_home_leak["collection_policy"].append("Do not expose ~/.codex memory.")
            self.assertTrue(validate_context_capsule(codex_home_leak))
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(codex_home_leak)

            claude_project_leak = json.loads(json.dumps(capsule))
            claude_project_leak["collection_policy"].append("Do not expose ~/.Claude/Projects/demo/memory.")
            self.assertTrue(validate_context_capsule(claude_project_leak))
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(claude_project_leak)

            policy_leak = json.loads(json.dumps(capsule))
            policy_leak["collection_policy"].append("Do not expose auth.json.")
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(policy_leak)

            policy_case_leak = json.loads(json.dumps(capsule))
            policy_case_leak["collection_policy"].append("Do not expose Auth.JSON or Claude.md Contents.")
            self.assertTrue(validate_context_capsule(policy_case_leak))
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(policy_case_leak)

            run_artifact_leak = json.loads(json.dumps(capsule))
            run_artifact_leak["run_artifact_index"].append(
                {"run_id": "s15i/read-only-pai-context", "artifact_names": ["/home/example/raw.txt"], "artifact_count": 1}
            )
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(run_artifact_leak)

    def test_context_capsule_schema_rejects_body_read_flag(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            capsule = collect_pai_context_metadata(pai_dir)
            capsule["forbidden_body_reads"]["memory_body_read"] = True
            schema = json.loads(Path("pai-runtime/pai-context-capsule.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(capsule)

    def test_context_capsule_schema_rejects_unknown_top_level_fields(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            capsule = collect_pai_context_metadata(pai_dir)
            capsule["unexpected_raw_content"] = "raw body must not be accepted"
            schema = json.loads(Path("pai-runtime/pai-context-capsule.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(capsule)

    def test_context_capsule_schema_rejects_isa_or_pulse_file_counts(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            self._add_context_dirs(pai_dir)
            capsule = collect_pai_context_metadata(pai_dir)
            schema = json.loads(Path("pai-runtime/pai-context-capsule.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)

            capsule["isa"]["file_count"] = 1
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(capsule)

            capsule = collect_pai_context_metadata(pai_dir)
            capsule["pulse"]["file_names"] = ["event.json"]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(capsule)

    def test_context_task_schema_accepts_task_card(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            task = json.loads((pai_dir / S15I_TASK_RELATIVE).read_text(encoding="utf-8"))
            schema = json.loads(Path("pai-runtime/pai-context-task.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(task)

    def test_context_task_schema_rejects_direct_live_traversal(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            task = json.loads((pai_dir / S15I_TASK_RELATIVE).read_text(encoding="utf-8"))
            schema = json.loads(Path("pai-runtime/pai-context-task.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)

            task["codex_direct_live_pai_traversal_allowed"] = True
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(task)

            task = json.loads((pai_dir / S15I_TASK_RELATIVE).read_text(encoding="utf-8"))
            task["required_capabilities"] = ["memory.write"]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(task)

            task = json.loads((pai_dir / S15I_TASK_RELATIVE).read_text(encoding="utf-8"))
            task["forbidden_read_surfaces"] = ["PAI Memory bodies"]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(task)

            task = json.loads((pai_dir / S15I_TASK_RELATIVE).read_text(encoding="utf-8"))
            task["task_summary"] = "Do not include /Home/example, Auth.JSON, or LocalHost:31337."
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(task)

    def test_run_pai_context_rejects_installed_task_card_schema_violation(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            task_path = pai_dir / S15I_TASK_RELATIVE
            task = json.loads(task_path.read_text(encoding="utf-8"))
            task["codex_direct_live_pai_traversal_allowed"] = True
            task_path.write_text(json.dumps(task, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(RunnerError, "task card schema validation failed"):
                run_pai_context_runtime(
                    pai_dir,
                    "codex",
                    task_path,
                    pai_dir / S15I_RUN_RELATIVE,
                    dry_run=True,
                )

    def test_install_schema_preflight_rejects_invalid_schema(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            schema_path = Path(tmp) / "invalid.schema.json"
            schema_path.write_text(json.dumps({"type": 123}) + "\n", encoding="utf-8")
            with self.assertRaises(RuntimeInstallError):
                _validate_schema_file(schema_path, "invalid.schema.json")

    def test_install_preflight_requires_context_metadata_capability(self):
        manifest = json.loads(Path("runtimes/codex/provider-manifest.json").read_text(encoding="utf-8"))
        manifest["capabilities"] = [item for item in manifest["capabilities"] if item != "pai.context.read.metadata"]
        with mock.patch("tools.pai_runtime_runner.install._load_provider_manifest", return_value=manifest):
            with self.assertRaisesRegex(RuntimeInstallError, "capabilities do not match"):
                validate_staged_payload()

    def test_context_report_schema_accepts_capsule_derived_report(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            capsule = collect_pai_context_metadata(pai_dir)
            report = context_report_from_capsule(capsule)
            schema = json.loads(Path("pai-runtime/pai-context-report.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(report)

    def test_context_report_schema_requires_codex_provider_capability(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            capsule = collect_pai_context_metadata(pai_dir)
            report = context_report_from_capsule(capsule)
            schema = json.loads(Path("pai-runtime/pai-context-report.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(report)

            report["runtime_provider_names"] = []
            Draft202012Validator(schema).validate(report)
            self.assertTrue(validate_context_report(report))

            report = context_report_from_capsule(capsule)
            report["runtime_provider_count"] = 0
            Draft202012Validator(schema).validate(report)
            self.assertTrue(validate_context_report(report))

            report = context_report_from_capsule(capsule)
            report["codex_capabilities_observed"] = []
            Draft202012Validator(schema).validate(report)
            self.assertTrue(validate_context_report(report))

    def test_context_report_schema_rejects_unredacted_text(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            capsule = collect_pai_context_metadata(pai_dir)
            report = context_report_from_capsule(capsule)
            schema = json.loads(Path("pai-runtime/pai-context-report.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)

            report["context_summary"] = "Report mentioned localhost:31337."
            Draft202012Validator(schema).validate(report)
            self.assertTrue(validate_context_report(report))

            report = context_report_from_capsule(capsule)
            report["context_summary"] = "Report mentioned LocalHost:31337."
            self.assertTrue(validate_context_report(report))
            Draft202012Validator(schema).validate(report)

            report = context_report_from_capsule(capsule)
            report["known_limits"] = ["Report mentioned ~/.codex memory."]
            self.assertTrue(validate_context_report(report))
            Draft202012Validator(schema).validate(report)

            report = context_report_from_capsule(capsule)
            report["known_limits"] = ["Report mentioned ~/.Claude/Projects/demo/memory."]
            self.assertTrue(validate_context_report(report))
            Draft202012Validator(schema).validate(report)

            report = context_report_from_capsule(capsule)
            report["known_limits"] = ["Report mentioned /home/example."]
            self.assertTrue(validate_context_report(report))
            Draft202012Validator(schema).validate(report)

            report = context_report_from_capsule(capsule)
            report["known_limits"] = ["Report mentioned /users/example and C:\\users\\example."]
            self.assertTrue(validate_context_report(report))
            Draft202012Validator(schema).validate(report)

            report = context_report_from_capsule(capsule)
            report["evidence_classification"] = ["Report mentioned auth.json."]
            self.assertTrue(validate_context_report(report))
            Draft202012Validator(schema).validate(report)

            report = context_report_from_capsule(capsule)
            report["evidence_classification"] = ["Report mentioned Auth.JSON and Claude.md Contents."]
            self.assertTrue(validate_context_report(report))
            Draft202012Validator(schema).validate(report)

    def test_context_report_normalization_ignores_provider_free_text(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            capsule = collect_pai_context_metadata(pai_dir)
            report = normalize_context_report(
                {
                    "context_summary": "Provider free text mentioned localhost:31337.",
                    "known_limits": ["Provider free text mentioned /home/example."],
                    "evidence_classification": ["provider supplied"],
                },
                capsule,
            )
            raw = json.dumps(report, sort_keys=True)
            self.assertNotIn("localhost:31337", raw)
            self.assertNotIn("/home/example", raw)
            self.assertEqual(report["context_summary"], context_report_from_capsule(capsule)["context_summary"])

    def test_run_pai_context_requires_pai_context_read_metadata_capability(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            result = run_pai_context_runtime(
                pai_dir,
                "codex",
                pai_dir / S15I_TASK_RELATIVE,
                pai_dir / S15I_RUN_RELATIVE,
                dry_run=True,
            )
            self.assertEqual(result["required_capabilities"], ["pai.context.read.metadata"])

    def test_run_pai_context_dry_run_redacts_context_prompt(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            self._add_context_dirs(pai_dir)
            result = run_pai_context_runtime(
                pai_dir,
                "codex",
                pai_dir / S15I_TASK_RELATIVE,
                pai_dir / S15I_RUN_RELATIVE,
                dry_run=True,
            )
            command = result["provider_command"]
            self.assertEqual(command[-1], "[sanitized-pai-context-prompt]")
            serialized = json.dumps(command)
            self.assertNotIn("Sanitized PAI context capsule JSON", serialized)
            self.assertNotIn("runtime_providers", serialized)
            self.assertNotIn("memory body must stay unread", serialized)

    def test_pai_context_provider_prompt_omits_forbidden_endpoint_literal(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            task = json.loads((pai_dir / S15I_TASK_RELATIVE).read_text(encoding="utf-8"))
            capsule = collect_pai_context_metadata(pai_dir)
            command = build_pai_context_provider_command(
                pai_dir,
                task,
                capsule,
                pai_dir / S15I_RUN_RELATIVE,
                pai_dir / S15I_RUN_RELATIVE / "pai-context-report.json",
            )
            prompt = command[-1]
            self.assertNotIn("localhost:31337", prompt)
            self.assertNotIn("127.0.0.1:31337", prompt)
            self.assertNotIn("~/.codex", prompt)
            self.assertNotIn("~/.claude/projects", prompt)
            self.assertIn("Pulse local control endpoint", prompt)

    def test_run_pai_context_rejects_installed_capsule_schema_mismatch(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            schema_path = pai_dir / "runtime-schemas" / "pai-context-capsule.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["metadata_only"]["const"] = False
            schema_path.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            with self.assertRaises(RunnerError):
                run_pai_context_runtime(
                    pai_dir,
                    "codex",
                    pai_dir / S15I_TASK_RELATIVE,
                    pai_dir / S15I_RUN_RELATIVE,
                    dry_run=True,
                )

    def test_run_pai_context_rejects_runtime_without_context_capability(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            manifest_path = pai_dir / "runtimes" / "codex" / "provider-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["capabilities"] = [item for item in manifest["capabilities"] if item != "pai.context.read.metadata"]
            manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            with self.assertRaises(CapabilityPolicyError):
                run_pai_context_runtime(
                    pai_dir,
                    "codex",
                    pai_dir / S15I_TASK_RELATIVE,
                    pai_dir / S15I_RUN_RELATIVE,
                    dry_run=True,
                )

    def test_run_pai_context_writes_only_pai_owned_run_artifacts(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, _ = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            self.assertTrue((run_dir / "pai-context-capsule.json").is_file())
            self.assertTrue((run_dir / "pai-context-report.schema.json").is_file())
            self.assertTrue((run_dir / "pai-context-report.json").is_file())
            self.assertTrue((run_dir / "pai-context-events.jsonl").is_file())
            self.assertFalse((Path(tmp) / "home" / ".codex" / "adapters" / "codex").exists())

    def test_run_pai_context_normalizes_provider_forbidden_free_text(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp, forbidden_report_text=True)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            report_raw = (run_dir / "pai-context-report.json").read_text(encoding="utf-8")
            self.assertNotIn("localhost:31337", report_raw)
            self.assertNotIn("/home/example", report_raw)
            report = json.loads(report_raw)
            schema = json.loads((run_dir / "pai-context-report.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator(schema).validate(report)
            self.assertEqual(validate_context_report(report), [])
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            self.assertTrue(result["validation_passed"])

    def test_run_pai_context_rejects_installed_report_schema_mismatch(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            tmp_path = Path(tmp)
            pai_dir = self._install_synthetic(tmp)
            self._add_context_dirs(pai_dir)
            schema_path = pai_dir / "runtime-schemas" / "pai-context-report.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["codex_provider_status"]["enum"] = ["not-peer-beta"]
            schema_path.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            fake_bin = tmp_path / "bin"
            fake_bin.mkdir()
            self._fake_codex_bin(fake_bin)
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = str(fake_bin) + os.pathsep + old_path
            try:
                with self.assertRaises(RunnerError):
                    run_pai_context_runtime(
                        pai_dir,
                        "codex",
                        pai_dir / S15I_TASK_RELATIVE,
                        pai_dir / S15I_RUN_RELATIVE,
                    )
            finally:
                os.environ["PATH"] = old_path

    def test_audit_pai_context_accepts_clean_metadata_only_run(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["context_capsule_metadata_only"])
            self.assertEqual(result["unknown_unclassified_writes"], [])
            self.assertTrue(
                any(path.endswith("pai-context-report.schema.json") for path in result["approved_pai_run_writes"])
            )

    def test_audit_pai_context_rejects_missing_command_evidence(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            (run_dir / "pai-context-state.json").write_text(
                json.dumps(
                    {
                        "pai_runtime_command": ["pai-runtime", "doctor"],
                        "provider_command": ["codex", "exec"],
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            self.assertFalse(result["event_attribution_passed"])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["runtime_warnings"])

            (run_dir / "pai-context-state.json").write_text(
                json.dumps(
                    {
                        "pai_runtime_command": [
                            "pai-runtime",
                            "run-pai-context",
                            "--pai-dir",
                            str(pai_dir),
                            "--runtime",
                            "codex",
                            "--task-card",
                            str(pai_dir / S15I_TASK_RELATIVE),
                            "--run-dir",
                            str(run_dir),
                        ],
                        "provider_command": [
                            "codex",
                            "--ask-for-approval",
                            "never",
                            "exec",
                            "--skip-git-repo-check",
                            "--ephemeral",
                            "--json",
                            "--sandbox",
                            "read-only",
                            "--cd",
                            str(run_dir),
                            "--add-dir",
                            str(run_dir),
                            "--output-schema",
                            str(run_dir / "pai-context-report.schema.json"),
                            "-o",
                            str(run_dir / "pai-context-report.json"),
                            "[sanitized-pai-context-prompt]",
                        ],
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            self.assertFalse(result["event_attribution_passed"])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["runtime_warnings"])

            wrong_run_dir = pai_dir / "runs" / "s15i" / "wrong-context"
            (run_dir / "pai-context-state.json").write_text(
                json.dumps(
                    {
                        "pai_runtime_command": [
                            str(pai_dir / "bin" / "pai-runtime"),
                            "run-pai-context",
                            "--pai-dir",
                            str(pai_dir),
                            "--runtime",
                            "codex",
                            "--task-card",
                            str(pai_dir / S15I_TASK_RELATIVE),
                            "--run-dir",
                            str(run_dir),
                        ],
                        "provider_command": [
                            "codex",
                            "--ask-for-approval",
                            "never",
                            "exec",
                            "--skip-git-repo-check",
                            "--ephemeral",
                            "--json",
                            "--sandbox",
                            "read-only",
                            "--cd",
                            str(wrong_run_dir),
                            "--add-dir",
                            str(wrong_run_dir),
                            "--output-schema",
                            str(wrong_run_dir / "pai-context-report.schema.json"),
                            "-o",
                            str(wrong_run_dir / "pai-context-report.json"),
                            "[sanitized-pai-context-prompt]",
                        ],
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            self.assertFalse(result["event_attribution_passed"])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["runtime_warnings"])

    def test_audit_pai_context_rejects_capsule_schema_violation(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            marker = Path(tmp) / "marker"
            marker.write_text("marker\n", encoding="utf-8")
            self._write_clean_context_artifacts(pai_dir, run_dir)
            capsule_path = run_dir / "pai-context-capsule.json"
            capsule = json.loads(capsule_path.read_text(encoding="utf-8"))
            capsule["forbidden_body_reads"]["unexpected_body_read"] = False
            capsule_path.write_text(json.dumps(capsule, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            (run_dir / "pai-context-events.jsonl").write_text("", encoding="utf-8")
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=capsule_path,
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            self.assertFalse(result["context_capsule_schema_valid"])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["forbidden_semantic_writes"])

    def test_context_validation_schema_accepts_clean_audit(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            schema = json.loads(Path("pai-runtime/pai-context-validation.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(result)

            result["runtime_warnings"] = [
                {
                    "classification": "codex_event_runtime_warning",
                    "path": "~/.claude/PAI/runs/s15i/read-only-pai-context/pai-context-events.jsonl",
                    "reason": "event log contains forbidden context text",
                }
            ]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

    def test_audit_pai_context_runtime_run_validates_validation_schema(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            schema_path = pai_dir / "runtime-schemas" / "pai-context-validation.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["runtime"]["const"] = "not-codex"
            schema_path.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(RunnerError, "validation artifact schema validation failed"):
                audit_pai_context_runtime_run(
                    pai_dir=pai_dir,
                    marker=marker,
                    run_dir=run_dir,
                    output=run_dir / "pai-context-validation.json",
                    runtime_attempt_number=1,
                )

    def test_audit_pai_context_cli_defaults_runtime_attempt_number(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            output = run_dir / "pai-context-validation.json"
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = runner_main(
                    [
                        "audit-pai-context",
                        "--pai-dir",
                        str(pai_dir),
                        "--marker",
                        str(marker),
                        "--run-dir",
                        str(run_dir),
                        "--output",
                        str(output),
                    ]
                )

            self.assertEqual(code, 0)
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result["runtime_attempt_number"], 1)
            self.assertTrue(result["validation_passed"])

    def test_audit_pai_context_runtime_run_rejects_output_escape(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            with self.assertRaisesRegex(RunnerError, "output must stay under"):
                audit_pai_context_runtime_run(
                    pai_dir=pai_dir,
                    marker=marker,
                    run_dir=run_dir,
                    output=pai_dir / "runs" / "s15i" / "pai-context-validation.json",
                    runtime_attempt_number=1,
                )
            with self.assertRaisesRegex(RunnerError, "output must be named pai-context-validation.json"):
                audit_pai_context_runtime_run(
                    pai_dir=pai_dir,
                    marker=marker,
                    run_dir=run_dir,
                    output=run_dir / "unexpected-validation.json",
                    runtime_attempt_number=1,
                )

    def test_context_validation_schema_rejects_forbidden_or_unknown_writes(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            schema = json.loads(Path("pai-runtime/pai-context-validation.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            result["unknown_unclassified_writes"] = ["unexpected-live-write.txt"]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

    def test_context_validation_schema_rejects_invalid_runtime_attempt_number(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            schema = json.loads(Path("pai-runtime/pai-context-validation.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            result["runtime_attempt_number"] = 0
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

    def test_context_validation_schema_requires_command_evidence(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            schema = json.loads(Path("pai-runtime/pai-context-validation.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)

            result["pai_runtime_command"] = []
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["pai_runtime_command"] = ["pai-runtime", "doctor"]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["pai_runtime_command"] = ["pai-runtime", "run-pai-context"]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            redacted_run_dir = "~/.claude/PAI/runs/s15i/read-only-pai-context"
            wrong_redacted_run_dir = "~/.claude/PAI/runs/s15i/wrong-context"
            result["pai_runtime_command"] = [
                "~/.claude/PAI/bin/pai-runtime",
                "run-pai-context",
                "--pai-dir",
                "~/.claude/PAI",
                "--runtime",
                "codex",
                "--task-card",
                "~/.claude/PAI/runtime-tasks/s15i-readonly-pai-context-task.json",
                "--run-dir",
                wrong_redacted_run_dir,
            ]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["pai_runtime_command"] = [
                "pai-runtime",
                "run-pai-context",
                "--pai-dir",
                "~/.claude/PAI",
                "--runtime",
                "codex",
                "--task-card",
                "~/.claude/PAI/runtime-tasks/s15i-readonly-pai-context-task.json",
                "--run-dir",
                redacted_run_dir,
            ]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["pai_runtime_command"] = [
                "~/.claude/PAI/bin/pai-runtime",
                "run-pai-context",
                "--pai-dir",
                "~/.claude/PAI",
                "--runtime",
                "codex",
                "--task-card",
                "~/.claude/PAI/runtime-tasks/s15i-readonly-pai-context-task.json",
                "--run-dir",
                redacted_run_dir,
            ]
            result["provider_command"] = []
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["provider_command"] = ["codex", "exec"]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["provider_command"] = ["codex", "exec", "[sanitized-pai-context-prompt]"]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["provider_command"] = [
                "codex",
                "--ask-for-approval",
                "never",
                "exec",
                "--skip-git-repo-check",
                "--ephemeral",
                "--json",
                "--sandbox",
                "workspace-write",
                "--cd",
                redacted_run_dir,
                "--add-dir",
                redacted_run_dir,
                "--output-schema",
                f"{redacted_run_dir}/pai-context-report.schema.json",
                "-o",
                f"{redacted_run_dir}/pai-context-report.json",
                "[sanitized-pai-context-prompt]",
            ]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["provider_command"] = [
                "codex",
                "--ask-for-approval",
                "never",
                "exec",
                "--skip-git-repo-check",
                "--ephemeral",
                "--json",
                "--sandbox",
                "read-only",
                "--cd",
                wrong_redacted_run_dir,
                "--add-dir",
                wrong_redacted_run_dir,
                "--output-schema",
                f"{wrong_redacted_run_dir}/pai-context-report.schema.json",
                "-o",
                f"{wrong_redacted_run_dir}/pai-context-report.json",
                "[sanitized-pai-context-prompt]",
            ]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["provider_command"] = [
                "codex",
                "--ask-for-approval",
                "never",
                "exec",
                "--skip-git-repo-check",
                "--ephemeral",
                "--json",
                "--sandbox",
                "read-only",
                "--cd",
                redacted_run_dir,
                "--add-dir",
                redacted_run_dir,
                "--output-schema",
                f"{redacted_run_dir}/pai-context-report.schema.json",
                "-o",
                f"{redacted_run_dir}/pai-context-report.json",
                "[sanitized-pai-context-prompt]",
            ]
            Draft202012Validator(schema).validate(result)

    def test_context_validation_schema_rejects_unknown_top_level_fields(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            schema = json.loads(Path("pai-runtime/pai-context-validation.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            result["unexpected_raw_content"] = "raw body must not be accepted"
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

    def test_context_validation_schema_rejects_unredacted_absolute_paths(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            schema = json.loads(Path("pai-runtime/pai-context-validation.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            result["provider_command"] = [str(pai_dir / "bin" / "pai-runtime")]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["provider_command"] = ["codex", "exec", "CLAUDE.md contents"]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["provider_command"] = ["codex", "exec", "[sanitized-pai-context-prompt]"]
            result["known_limits"] = ["Known limit mentioned auth.json."]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["known_limits"] = ["Known limit mentioned /Home/example and C:\\users\\example."]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["known_limits"] = ["Known limit mentioned Auth.JSON and Claude.md Contents."]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["known_limits"] = ["Known limit mentioned LocalHost:31337."]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["known_limits"] = ["Known limit mentioned ~/.codex memory."]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["known_limits"] = ["Known limit mentioned ~/.Claude/Projects/demo/memory."]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

    def test_context_validation_schema_rejects_unredacted_nested_event_paths(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            schema = json.loads(Path("pai-runtime/pai-context-validation.schema.json").read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            result["codex_command_execution_events"] = [
                {
                    "classification": "codex_event_command_execution",
                    "command": f"cat {pai_dir / 'Memory' / 'WORK' / 'secret.md'}",
                    "event_type": "exec_command",
                }
            ]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["codex_command_execution_events"] = [{"classification": "codex_event_command_execution"}]
            result["codex_file_change_events"] = []
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["codex_command_execution_events"] = []
            result["codex_file_change_events"] = [
                {
                    "classification": "codex_event_file_change",
                    "approved": True,
                    "paths": [str(run_dir / "pai-context-report.json")],
                    "event_type": "file_change",
                }
            ]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

            result["codex_file_change_events"] = [
                {
                    "classification": "codex_event_file_change",
                    "approved": False,
                    "paths": ["~/.claude/PAI/runs/s15i/read-only-pai-context/pai-context-report.json"],
                    "event_type": "file_change",
                }
            ]
            with self.assertRaises(ValidationError):
                Draft202012Validator(schema).validate(result)

    def test_context_validation_artifact_omits_forbidden_endpoint_literals(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp, forbidden_report_text=True)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            raw = json.dumps(result, sort_keys=True)
            self.assertTrue(result["validation_passed"])
            self.assertNotIn("localhost:31337", raw)
            self.assertNotIn("127.0.0.1:31337", raw)

    def test_context_validation_artifact_redacts_pai_absolute_paths(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir, marker = self._run_with_fake_codex(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            raw = json.dumps(result, sort_keys=True)
            self.assertTrue(result["validation_passed"])
            self.assertNotIn(str(pai_dir), raw)
            self.assertIn("~/.claude/PAI", raw)

    def test_audit_pai_context_rejects_memory_body_read(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            result = self._audit_with_event(tmp, {"type": "exec_command", "cmd": "cat Memory/WORK/secret.md"})
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["memory_body_read_by_codex"])

    def test_audit_pai_context_rejects_isa_body_read(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            result = self._audit_with_event(tmp, {"type": "exec_command", "cmd": "cat ISA/secret.md"})
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["isa_body_read_by_codex"])

    def test_audit_pai_context_rejects_pulse_payload_read(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            result = self._audit_with_event(tmp, {"type": "exec_command", "cmd": "cat Pulse/events/event.json"})
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["pulse_event_payload_read_by_codex"])

    def test_audit_pai_context_rejects_codex_memory_read(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            result = self._audit_with_event(tmp, {"type": "exec_command", "cmd": "cat ~/.codex/memories/profile.md"})
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["codex_memory_read_by_codex"])

    def test_audit_pai_context_rejects_claude_project_memory_read(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            result = self._audit_with_event(
                tmp,
                {"type": "exec_command", "cmd": "cat ~/.claude/projects/demo/memory"},
            )
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["claude_project_memory_read_by_codex"])

    def test_audit_pai_context_rejects_pulse_probe(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            result = self._audit_with_event(
                tmp,
                {"type": "exec_command", "cmd": "curl http://localhost:31337/status"},
            )
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["pulse_probe_performed_by_codex"])
            self.assertTrue(result["localhost_31337_called_by_codex"])

    def test_audit_pai_context_rejects_forbidden_event_text(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            result = self._audit_with_event(
                tmp,
                {
                    "type": "message",
                    "message": (
                        "Model mentioned LocalHost:31337, /Home/example, C:\\Users\\example, ~/.codex, "
                        "~/.Claude/Settings, Auth.JSON, and Claude.md Contents."
                    ),
                },
            )
            raw = json.dumps(result, sort_keys=True)
            self.assertFalse(result["event_attribution_passed"])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["runtime_warnings"])
            self.assertTrue(
                any(
                    warning.get("reason") == "event log contains forbidden context text"
                    for warning in result["runtime_warnings"]
                )
            )
            self.assertTrue(all(str(warning.get("path", "")).startswith("~/.claude/PAI/") for warning in result["runtime_warnings"]))
            self.assertNotIn("LocalHost:31337", raw)
            self.assertNotIn("/Home/example", raw)
            self.assertNotIn("C:\\Users\\example", raw)
            self.assertNotIn("~/.codex", raw)
            self.assertNotIn("Auth.JSON", raw)
            self.assertNotIn("Claude.md Contents", raw)

    def test_audit_pai_context_rejects_unknown_unclassified_write(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            marker = Path(tmp) / "marker"
            marker.write_text("marker\n", encoding="utf-8")
            self._write_clean_context_artifacts(pai_dir, run_dir)
            (run_dir / "pai-context-events.jsonl").write_text("", encoding="utf-8")
            (pai_dir / "unexpected-live-write.txt").write_text("unexpected\n", encoding="utf-8")
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["unknown_unclassified_writes"])

    def test_audit_pai_context_rejects_symlink_write(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            marker = Path(tmp) / "marker"
            marker.write_text("marker\n", encoding="utf-8")
            self._write_clean_context_artifacts(pai_dir, run_dir)
            (run_dir / "pai-context-events.jsonl").write_text(
                json.dumps({"type": "message", "message": "context report emitted"}) + "\n",
                encoding="utf-8",
            )
            outside = Path(tmp) / "outside-artifact.txt"
            outside.write_text("outside\n", encoding="utf-8")
            os.symlink(outside, run_dir / "escape-link")
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            self.assertFalse(result["validation_passed"])
            self.assertTrue(any("escape-link" in item for item in result["unknown_unclassified_writes"]))

    def test_audit_pai_context_rejects_empty_event_log(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            marker = Path(tmp) / "marker"
            marker.write_text("marker\n", encoding="utf-8")
            self._write_clean_context_artifacts(pai_dir, run_dir)
            (run_dir / "pai-context-events.jsonl").write_text("", encoding="utf-8")
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            self.assertFalse(result["event_logs_present"])
            self.assertFalse(result["validation_passed"])

    def test_audit_pai_context_rejects_malformed_event_log(self):
        with tempfile.TemporaryDirectory(prefix="s15i.context.") as tmp:
            pai_dir = self._install_synthetic(tmp)
            run_dir = pai_dir / S15I_RUN_RELATIVE
            marker = Path(tmp) / "marker"
            marker.write_text("marker\n", encoding="utf-8")
            self._write_clean_context_artifacts(pai_dir, run_dir)
            (run_dir / "pai-context-events.jsonl").write_text("{not json}\n", encoding="utf-8")
            result = audit_pai_context_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                capsule_path=run_dir / "pai-context-capsule.json",
                report_path=run_dir / "pai-context-report.json",
                events_path=run_dir / "pai-context-events.jsonl",
            )
            self.assertTrue(result["event_logs_present"])
            self.assertFalse(result["event_attribution_passed"])
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["runtime_warnings"])

    def test_report_identity_constants_match_milestone(self):
        self.assertEqual(S15I_MILESTONE, "V5-S15I-PAI-RUNTIME-READONLY-PAI-CONTEXT-TASK")
        self.assertEqual(S15I_RUN_ID, "s15i-read-only-pai-context")


if __name__ == "__main__":
    unittest.main()
