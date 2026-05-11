from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from tools.pai_live_preflight.consent import ConsentValidationError
from tools.pai_live_preflight.path_safety import CONTENT_BODY_READ, PathSafetyError, ensure_allowed_probe, reject_symlink_escape
from tools.pai_live_preflight.preflight import run_fixture_preflight
from tools.pai_live_preflight.report import PreflightReportError, write_report


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "fixtures/s14_live_preflight/roots/valid-pai"
VALID_CONSENT = REPO_ROOT / "fixtures/s14_live_preflight/consent/valid-pai-consent.json"
WRONG_PHRASE = REPO_ROOT / "fixtures/s14_live_preflight/consent/wrong-phrase.json"
WRONG_ROOT = REPO_ROOT / "fixtures/s14_live_preflight/consent/wrong-root.json"
DECLARED_ROOT = "~/.claude/PAI"


class PaiLivePreflightFixtureOnlyTests(unittest.TestCase):
    def test_valid_fixture_preflight_report_is_noncanonical(self):
        report = run_fixture_preflight(
            fixture_root=FIXTURE_ROOT,
            consent_path=VALID_CONSENT,
            declared_source_root=DECLARED_ROOT,
        )

        self.assertEqual(report["consent_status"], "valid")
        self.assertEqual(report["declared_source_root"], DECLARED_ROOT)
        self.assertTrue(report["pulse_not_probed_confirmation"])
        self.assertTrue(report["memory_not_read_confirmation"])
        self.assertTrue(report["isa_not_read_confirmation"])
        classification = report["evidence_classification"]
        self.assertTrue(classification["fixture evidence"])
        self.assertTrue(classification["non-canonical evidence"])
        self.assertTrue(classification["not personal live-state evidence"])

    def test_missing_consent_artifact_rejected(self):
        with tempfile.TemporaryDirectory(prefix="s14c-preflight.") as tmp:
            missing = Path(tmp) / "missing-consent.json"
            with self.assertRaises(ConsentValidationError):
                run_fixture_preflight(
                    fixture_root=FIXTURE_ROOT,
                    consent_path=missing,
                    declared_source_root=DECLARED_ROOT,
                )

    def test_wrong_consent_phrase_rejected(self):
        with self.assertRaises(ConsentValidationError):
            run_fixture_preflight(
                fixture_root=FIXTURE_ROOT,
                consent_path=WRONG_PHRASE,
                declared_source_root=DECLARED_ROOT,
            )

    def test_wrong_declared_source_root_rejected(self):
        with self.assertRaises(ConsentValidationError):
            run_fixture_preflight(
                fixture_root=FIXTURE_ROOT,
                consent_path=WRONG_ROOT,
                declared_source_root=DECLARED_ROOT,
            )
        with self.assertRaises(ConsentValidationError):
            run_fixture_preflight(
                fixture_root=FIXTURE_ROOT,
                consent_path=VALID_CONSENT,
                declared_source_root="~/.claude",
            )

    def test_path_traversal_rejected(self):
        with self.assertRaises(PathSafetyError):
            run_fixture_preflight(
                fixture_root=Path("fixtures/s14_live_preflight/roots/valid-pai/.."),
                consent_path=VALID_CONSENT,
                declared_source_root=DECLARED_ROOT,
            )

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory(prefix="s14c-preflight.") as tmp:
            base = Path(tmp)
            root = base / "root"
            root.mkdir()
            outside = base / "outside"
            outside.mkdir()
            symlink_path = root / "escape"
            try:
                os.symlink(outside, symlink_path)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation is not available on this platform")
            with self.assertRaises(PathSafetyError):
                reject_symlink_escape(root.resolve(), symlink_path)

    def test_forbidden_claude_projects_read_rejected(self):
        with self.assertRaises(PathSafetyError):
            run_fixture_preflight(
                fixture_root=FIXTURE_ROOT,
                consent_path=VALID_CONSENT,
                declared_source_root=DECLARED_ROOT,
                extra_metadata_paths=[".claude/projects"],
            )

    def test_forbidden_codex_memories_read_rejected(self):
        with self.assertRaises(PathSafetyError):
            run_fixture_preflight(
                fixture_root=FIXTURE_ROOT,
                consent_path=VALID_CONSENT,
                declared_source_root=DECLARED_ROOT,
                extra_metadata_paths=[".codex/memories"],
            )

    def test_memory_isa_and_pulse_bodies_do_not_appear_in_report(self):
        report = run_fixture_preflight(
            fixture_root=FIXTURE_ROOT,
            consent_path=VALID_CONSENT,
            declared_source_root=DECLARED_ROOT,
        )
        raw = json.dumps(report, sort_keys=True)
        self.assertNotIn("S14C_SENTINEL_MEMORY_BODY_SHOULD_NOT_APPEAR", raw)
        self.assertNotIn("S14C_SENTINEL_ISA_BODY_SHOULD_NOT_APPEAR", raw)
        self.assertNotIn("S14C_SENTINEL_PULSE_BODY_SHOULD_NOT_APPEAR", raw)
        fixture_root = FIXTURE_ROOT.resolve()
        with self.assertRaises(PathSafetyError):
            ensure_allowed_probe(fixture_root, "Memory/WORK/DO_NOT_READ.md", CONTENT_BODY_READ)
        with self.assertRaises(PathSafetyError):
            ensure_allowed_probe(fixture_root, "ISA/DO_NOT_READ.md", CONTENT_BODY_READ)
        with self.assertRaises(PathSafetyError):
            ensure_allowed_probe(fixture_root, "Pulse/events/DO_NOT_READ.json", CONTENT_BODY_READ)

    def test_output_path_outside_output_root_rejected(self):
        report = run_fixture_preflight(
            fixture_root=FIXTURE_ROOT,
            consent_path=VALID_CONSENT,
            declared_source_root=DECLARED_ROOT,
        )
        with tempfile.TemporaryDirectory(prefix="s14c-preflight.") as tmp:
            output_root = Path(tmp) / "approved"
            outside = Path(tmp) / "outside-report.json"
            with self.assertRaises(PreflightReportError):
                write_report(report, output_root, outside)

    def test_no_pulse_or_runtime_probe_surface(self):
        module_paths = [
            REPO_ROOT / "tools/pai_live_preflight/__init__.py",
            REPO_ROOT / "tools/pai_live_preflight/__main__.py",
            REPO_ROOT / "tools/pai_live_preflight/consent.py",
            REPO_ROOT / "tools/pai_live_preflight/path_safety.py",
            REPO_ROOT / "tools/pai_live_preflight/preflight.py",
            REPO_ROOT / "tools/pai_live_preflight/report.py",
        ]
        forbidden = [
            "import subprocess",
            "import socket",
            "import requests",
            "import urllib",
            "import http.client",
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
