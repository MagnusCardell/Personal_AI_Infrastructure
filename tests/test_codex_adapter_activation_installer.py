from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from tools.codex_adapter_installer.install import (
    EXPECTED_MANIFEST_VALUES,
    InstallerError,
    apply_install,
    load_staged_manifest,
    read_staged_agents,
    rollback_install,
    validate_install,
    validate_router_text,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class CodexAdapterActivationInstallerTests(unittest.TestCase):
    def _synthetic_layout(self, tmp: str) -> tuple[Path, Path]:
        base = Path(tmp)
        pai_dir = base / "home" / ".claude" / "PAI"
        pai_dir.mkdir(parents=True)
        backup_root = base / "backup"
        backup_pai = backup_root / ".claude" / "PAI"
        backup_pai.mkdir(parents=True)
        return pai_dir, backup_root

    def test_manifest_is_valid_peer_beta_codex_adapter(self):
        manifest = load_staged_manifest()
        for key, expected in EXPECTED_MANIFEST_VALUES.items():
            self.assertEqual(manifest[key], expected)
        runtime_policy = manifest["runtime_surface_policy"]
        not_approved = runtime_policy["not_approved_by_this_milestone"]
        for surface in [
            "repo root AGENTS.md",
            "repo .codex/",
            "~/.codex/",
            "Codex hooks",
            "Codex rules",
            "Codex skills",
            "Codex agents",
            "Codex commands",
            "Codex launchers",
            "Pulse bridge",
            "Memory writer",
            "ISA writer",
        ]:
            self.assertIn(surface, not_approved)

    def test_agents_router_contains_required_pai_v5_concepts(self):
        text = read_staged_agents()
        for concept in [
            "Codex is a peer beta adapter for PAI v5.",
            "Claude remains the official/full-support upstream adapter.",
            "PAI v5 is a Life OS, not just Claude config.",
            "PAI_DIR is the v5 PAI subsystem root, usually ~/.claude/PAI.",
            "PAI_SYSTEM_PROMPT.md is a high-authority instruction layer.",
            "Pulse is the central daemon/dashboard/event surface on localhost:31337.",
            "ISA replaces PRD as the work/system-of-record primitive.",
            "Memory v7.6 has WORK, LEARNING, and KNOWLEDGE.",
            "AGENTS.md is a router into PAI v5, not a clone of CLAUDE.md.",
        ]:
            self.assertIn(concept, text)

    def test_agents_router_is_not_claude_md_clone(self):
        text = read_staged_agents()
        validate_router_text(text)
        self.assertLess(len(text.encode("utf-8")), 12000)
        self.assertNotIn("You are Claude Code", text)
        self.assertNotIn("# CLAUDE.md", text)
        self.assertLessEqual(text.count("Claude"), 8)

    def test_installer_applies_to_synthetic_pai_root(self):
        with tempfile.TemporaryDirectory(prefix="s15a-install.") as tmp:
            pai_dir, backup_root = self._synthetic_layout(tmp)
            result = apply_install(pai_dir, backup_root)
            self.assertEqual(Path(result["pai_dir"]), pai_dir.resolve())
            self.assertEqual((pai_dir / "AGENTS.md").read_text(encoding="utf-8"), read_staged_agents())
            self.assertTrue((pai_dir / "adapters" / "codex" / "install-state.json").is_file())

    def test_installer_validate_passes_after_apply(self):
        with tempfile.TemporaryDirectory(prefix="s15a-install.") as tmp:
            pai_dir, backup_root = self._synthetic_layout(tmp)
            apply_install(pai_dir, backup_root)
            result = validate_install(pai_dir, backup_root)
            self.assertEqual(result["adapter_status"], "peer-beta")
            self.assertEqual(result["upstream_adapter"], "claude")

    def test_installer_is_idempotent(self):
        with tempfile.TemporaryDirectory(prefix="s15a-install.") as tmp:
            pai_dir, backup_root = self._synthetic_layout(tmp)
            apply_install(pai_dir, backup_root)
            first = {
                path.relative_to(pai_dir): path.read_bytes()
                for path in (pai_dir / "adapters" / "codex").glob("*")
                if path.is_file()
            }
            first[Path("AGENTS.md")] = (pai_dir / "AGENTS.md").read_bytes()
            apply_install(pai_dir, backup_root)
            second = {
                path.relative_to(pai_dir): path.read_bytes()
                for path in (pai_dir / "adapters" / "codex").glob("*")
                if path.is_file()
            }
            second[Path("AGENTS.md")] = (pai_dir / "AGENTS.md").read_bytes()
            self.assertEqual(first, second)
            validate_install(pai_dir, backup_root)

    def test_installer_rejects_empty_pai_dir(self):
        with tempfile.TemporaryDirectory(prefix="s15a-install.") as tmp:
            _, backup_root = self._synthetic_layout(tmp)
            with self.assertRaises(InstallerError):
                apply_install("", backup_root)

    def test_installer_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory(prefix="s15a-install.") as tmp:
            pai_dir, backup_root = self._synthetic_layout(tmp)
            with self.assertRaises(InstallerError):
                apply_install(pai_dir / ".." / "PAI", backup_root)

    def test_installer_rejects_symlink_escape(self):
        with tempfile.TemporaryDirectory(prefix="s15a-install.") as tmp:
            pai_dir, backup_root = self._synthetic_layout(tmp)
            outside = Path(tmp) / "outside"
            outside.mkdir()
            adapters = pai_dir / "adapters"
            try:
                os.symlink(outside, adapters)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation is not available on this platform")
            with self.assertRaises(InstallerError):
                apply_install(pai_dir, backup_root)

    def test_installer_rollback_restores_synthetic_previous_agents(self):
        with tempfile.TemporaryDirectory(prefix="s15a-install.") as tmp:
            pai_dir, backup_root = self._synthetic_layout(tmp)
            previous = "# Previous PAI router\n"
            (pai_dir / "AGENTS.md").write_text(previous, encoding="utf-8")
            backup_agents = backup_root / ".claude" / "PAI" / "AGENTS.md"
            backup_agents.write_text(previous, encoding="utf-8")

            apply_install(pai_dir, backup_root)
            self.assertNotEqual((pai_dir / "AGENTS.md").read_text(encoding="utf-8"), previous)
            rollback_install(pai_dir, backup_root)
            self.assertEqual((pai_dir / "AGENTS.md").read_text(encoding="utf-8"), previous)

    def test_installer_does_not_create_codex_or_repo_root_surfaces(self):
        with tempfile.TemporaryDirectory(prefix="s15a-install.") as tmp:
            pai_dir, backup_root = self._synthetic_layout(tmp)
            cwd = Path(tmp) / "workspace"
            cwd.mkdir()
            before = set(cwd.iterdir())
            apply_install(pai_dir, backup_root)
            after = set(cwd.iterdir())
            self.assertEqual(before, after)
            self.assertFalse((cwd / "AGENTS.md").exists())
            self.assertFalse((cwd / ".codex").exists())
            self.assertFalse((pai_dir.parent.parent / ".codex").exists())

    def test_install_state_is_valid_json(self):
        with tempfile.TemporaryDirectory(prefix="s15a-install.") as tmp:
            pai_dir, backup_root = self._synthetic_layout(tmp)
            apply_install(pai_dir, backup_root)
            state_path = pai_dir / "adapters" / "codex" / "install-state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertTrue(state["installed"])


if __name__ == "__main__":
    unittest.main()
