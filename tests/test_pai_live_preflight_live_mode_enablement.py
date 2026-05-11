from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from tools.pai_live_preflight.consent import ConsentValidationError
from tools.pai_live_preflight.path_safety import PathSafetyError, reject_symlink_escape
from tools.pai_live_preflight.preflight import run_fixture_preflight, run_installed_pai_preflight
from tools.pai_live_preflight.report import write_report


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "fixtures/s14_live_preflight/roots/valid-pai"
VALID_CONSENT = REPO_ROOT / "fixtures/s14_live_preflight/consent/valid-pai-consent.json"
WRONG_PHRASE = REPO_ROOT / "fixtures/s14_live_preflight/consent/wrong-phrase.json"
WRONG_ROOT = REPO_ROOT / "fixtures/s14_live_preflight/consent/wrong-root.json"
DECLARED_ROOT = "~/.claude/PAI"


def _make_synthetic_installed_root(base: Path) -> Path:
    root = base / "synthetic-installed-pai"
    for directory in [
        root / "Memory/WORK",
        root / "Memory/LEARNING",
        root / "Memory/KNOWLEDGE",
        root / "ISA",
        root / "Pulse/events",
    ]:
        directory.mkdir(parents=True, exist_ok=True)
    (root / "PAI_SYSTEM_PROMPT.md").write_text("", encoding="utf-8")
    (root / "Memory/WORK/DO_NOT_READ.md").write_text(
        "S14D_SENTINEL_MEMORY_BODY_SHOULD_NOT_APPEAR\n", encoding="utf-8"
    )
    (root / "ISA/DO_NOT_READ.md").write_text("S14D_SENTINEL_ISA_BODY_SHOULD_NOT_APPEAR\n", encoding="utf-8")
    (root / "Pulse/events/DO_NOT_READ.json").write_text(
        "S14D_SENTINEL_PULSE_BODY_SHOULD_NOT_APPEAR\n", encoding="utf-8"
    )
    return root


class PaiLivePreflightLiveModeEnablementTests(unittest.TestCase):
    def test_fixture_mode_preserves_s14c_evidence_classification(self):
        report = run_fixture_preflight(
            fixture_root=FIXTURE_ROOT,
            consent_path=VALID_CONSENT,
            declared_source_root=DECLARED_ROOT,
        )
        classification = report["evidence_classification"]
        self.assertTrue(classification["fixture evidence"])
        self.assertTrue(classification["non-canonical evidence"])
        self.assertTrue(classification["not personal live-state evidence"])
        self.assertEqual(report["run_context"], "fixture")

    def test_installed_pai_mode_requires_exact_consent(self):
        with tempfile.TemporaryDirectory(prefix="s14d-preflight.") as tmp:
            root = _make_synthetic_installed_root(Path(tmp))
            with self.assertRaises(ConsentValidationError):
                run_installed_pai_preflight(
                    installed_source_root=root,
                    consent_path=WRONG_PHRASE,
                    declared_source_root=DECLARED_ROOT,
                )

    def test_installed_pai_mode_requires_declared_pai_root(self):
        with tempfile.TemporaryDirectory(prefix="s14d-preflight.") as tmp:
            root = _make_synthetic_installed_root(Path(tmp))
            with self.assertRaises(ConsentValidationError):
                run_installed_pai_preflight(
                    installed_source_root=root,
                    consent_path=WRONG_ROOT,
                    declared_source_root=DECLARED_ROOT,
                )
            with self.assertRaises(ConsentValidationError):
                run_installed_pai_preflight(
                    installed_source_root=root,
                    consent_path=VALID_CONSENT,
                    declared_source_root="~/.claude",
                )

    def test_installed_pai_mode_uses_explicit_source_root_argument(self):
        with self.assertRaises(PathSafetyError):
            run_installed_pai_preflight(
                installed_source_root="",
                consent_path=VALID_CONSENT,
                declared_source_root=DECLARED_ROOT,
            )

    def test_installed_pai_mode_rejects_tilde_source_root_path(self):
        with self.assertRaises(PathSafetyError):
            run_installed_pai_preflight(
                installed_source_root="~/.claude/PAI",
                consent_path=VALID_CONSENT,
                declared_source_root=DECLARED_ROOT,
            )

    def test_installed_pai_mode_rejects_home_variable_source_root_path(self):
        with self.assertRaises(PathSafetyError):
            run_installed_pai_preflight(
                installed_source_root="$HOME/.claude/PAI",
                consent_path=VALID_CONSENT,
                declared_source_root=DECLARED_ROOT,
            )

    def test_installed_pai_mode_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory(prefix="s14d-preflight.") as tmp:
            base = Path(tmp)
            root = _make_synthetic_installed_root(base)
            with self.assertRaises(PathSafetyError):
                run_installed_pai_preflight(
                    installed_source_root=root / "..",
                    consent_path=VALID_CONSENT,
                    declared_source_root=DECLARED_ROOT,
                )

    def test_installed_pai_mode_rejects_symlink_escape(self):
        with tempfile.TemporaryDirectory(prefix="s14d-preflight.") as tmp:
            base = Path(tmp)
            root = _make_synthetic_installed_root(base)
            outside = base / "outside"
            outside.mkdir()
            symlink_path = root / "escape"
            try:
                os.symlink(outside, symlink_path)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation is not available on this platform")
            with self.assertRaises(PathSafetyError):
                reject_symlink_escape(root.resolve(), symlink_path)
            with self.assertRaises(PathSafetyError):
                run_installed_pai_preflight(
                    installed_source_root=root,
                    consent_path=VALID_CONSENT,
                    declared_source_root=DECLARED_ROOT,
                    extra_metadata_paths=["escape"],
                )

    def test_installed_pai_mode_report_is_redacted_and_noncanonical(self):
        with tempfile.TemporaryDirectory(prefix="s14d-preflight.") as tmp:
            base = Path(tmp)
            root = _make_synthetic_installed_root(base)
            output_root = base / "out"
            report = run_installed_pai_preflight(
                installed_source_root=root,
                consent_path=VALID_CONSENT,
                declared_source_root=DECLARED_ROOT,
            )
            output = write_report(report, output_root, output_root / "report.json")
            raw = output.read_text(encoding="utf-8")
            persisted = json.loads(raw)
            classification = persisted["evidence_classification"]
            self.assertTrue(classification["personal live-state evidence"])
            self.assertTrue(classification["non-canonical evidence"])
            self.assertTrue(classification["synthetic validation only"])
            self.assertNotIn(str(root.resolve()), raw)
            self.assertIn("<redacted>", persisted["source_root_redacted_display_path"])

    def test_installed_pai_mode_does_not_leak_memory_isa_or_pulse_sentinels(self):
        with tempfile.TemporaryDirectory(prefix="s14d-preflight.") as tmp:
            root = _make_synthetic_installed_root(Path(tmp))
            report = run_installed_pai_preflight(
                installed_source_root=root,
                consent_path=VALID_CONSENT,
                declared_source_root=DECLARED_ROOT,
            )
            raw = json.dumps(report, sort_keys=True)
            self.assertNotIn("S14D_SENTINEL_MEMORY_BODY_SHOULD_NOT_APPEAR", raw)
            self.assertNotIn("S14D_SENTINEL_ISA_BODY_SHOULD_NOT_APPEAR", raw)
            self.assertNotIn("S14D_SENTINEL_PULSE_BODY_SHOULD_NOT_APPEAR", raw)

    def test_installed_pai_mode_does_not_introduce_runtime_probe_surface(self):
        module_paths = [
            REPO_ROOT / "tools/pai_live_preflight/__main__.py",
            REPO_ROOT / "tools/pai_live_preflight/consent.py",
            REPO_ROOT / "tools/pai_live_preflight/path_safety.py",
            REPO_ROOT / "tools/pai_live_preflight/preflight.py",
            REPO_ROOT / "tools/pai_live_preflight/report.py",
        ]
        forbidden = [
            "import subprocess",
            "from subprocess",
            "import socket",
            "from socket",
            "import requests",
            "from requests",
            "import urllib",
            "from urllib",
            "import http.client",
            "from http.client",
            "import ftplib",
            "from ftplib",
            "import telnetlib",
            "from telnetlib",
            "import webbrowser",
            "from webbrowser",
            "localhost:31337",
            "127.0.0.1:31337",
            "Path.home(",
            ".expanduser(",
            "os.path.expanduser",
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in module_paths)
        for token in forbidden:
            self.assertNotIn(token, combined)


if __name__ == "__main__":
    unittest.main()
