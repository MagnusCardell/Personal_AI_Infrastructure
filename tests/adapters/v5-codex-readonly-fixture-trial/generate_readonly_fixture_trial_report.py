#!/usr/bin/env python3
"""Generate the S11A release-fixture read-only evidence report.

Codex is not currently proven drop-in for existing local PAI v5 files. This
generator produces adapter-test evidence only from the approved fixture corpus
and the read-only harness. The report is not PAI Memory, not ISA, not Pulse
state, not Claude memory, not Codex memory, not a PAI runtime audit artifact,
not a manifest, and not runtime payload.
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path


sys.dont_write_bytecode = True


TRIAL_ROOT = Path("tests/adapters/v5-codex-readonly-fixture-trial")
APPROVED_FIXTURE_ROOT = TRIAL_ROOT / "fixtures"
APPROVED_REPORT_DIR = TRIAL_ROOT / "reports"
APPROVED_REPORT_PATH = APPROVED_REPORT_DIR / "S11A_RELEASE_FIXTURE_TRIAL_REPORT.json"
HARNESS_PATH = TRIAL_ROOT / "run_readonly_fixture_trial.py"


def fail(message):
    print(f"error: {message}")
    return 1


def validate_relative_path(raw_value, approved_path, label):
    candidate = Path(raw_value)
    if candidate.is_absolute():
        raise ValueError(f"{label} must be repository-relative, not absolute")
    if ".." in candidate.parts:
        raise ValueError(f"{label} must not contain parent traversal")
    if candidate.as_posix() != approved_path.as_posix():
        raise ValueError(f"{label} must be {approved_path.as_posix()}")
    return candidate


def validate_report_output_path(raw_value):
    report_path = validate_relative_path(raw_value, APPROVED_REPORT_PATH, "report output path")
    if report_path.parent != APPROVED_REPORT_DIR:
        raise ValueError("report output path must stay inside the approved reports directory")
    if report_path.name != APPROVED_REPORT_PATH.name:
        raise ValueError("only the approved S11A report file may be overwritten")
    if not report_path.parent.is_dir():
        raise ValueError("approved reports directory is missing")
    return report_path


def load_harness():
    spec = importlib.util.spec_from_file_location("s11a_readonly_fixture_harness", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load read-only fixture harness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_fixture_versions(fixture_root, harness):
    versions = set()
    for dirname in harness.EXPECTED_FIXTURES.values():
        metadata_path = fixture_root / dirname / "fixture.json"
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
        versions.add(str(data.get("pai_version", "")))
    return sorted(versions)


def build_report(fixture_root, harness):
    failures = harness.validate_fixture_root(fixture_root)
    counts = harness.global_coverage_counts(fixture_root)
    fixture_count = harness.count_fixture_dirs(fixture_root)
    case_count = harness.count_case_files(fixture_root)
    versions = load_fixture_versions(fixture_root, harness)

    if failures:
        raise RuntimeError("approved fixture harness validation failed: " + "; ".join(failures))
    if versions != ["v5.0.0"]:
        raise RuntimeError(f"unexpected fixture pai_version values: {versions}")

    return {
        "report_id": "S11A-RELEASE-FIXTURE-TRIAL-REPORT",
        "report_type": "release-fixture-read-only-evidence",
        "report_status": "pass",
        "pai_version": "v5.0.0",
        "engine_under_test": "none",
        "adapter_mode": "fixture-only-read-only",
        "source_kind": "release-fixture",
        "fixture_root": fixture_root.as_posix(),
        "generated_from": [
            "tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py",
            "tests/adapters/v5-codex-readonly-fixture-trial/fixtures",
        ],
        "fixture_count": fixture_count,
        "case_count": case_count,
        "seam_count": counts["seam_count"],
        "coverage_id_count": counts["coverage_id_count"],
        "gate_id_count": counts["gate_id_count"],
        "denied_category_count": counts["denied_category_count"],
        "positive_harness_status": "pass",
        "negative_control_status": "pass",
        "no_residue_status": "pass",
        "drop_in_claim_status": "not-claimed",
        "pulse_status": "not-started-not-called",
        "memory_status": "no-pai-memory-writes",
        "isa_status": "no-isa-writes",
        "product_memory_status": "no-product-memory-promotion",
        "protected_path_status": "no-protected-path-writes",
        "live_user_local_state_status": "not-read",
        "unsupported_surface_report_status": "covered-by-fixture-expectations",
        "denied_action_report_status": "covered-by-fixture-expectations",
        "rollback_status": "no-residue-fixture-only",
        "non_promotion_statement": "Product memories are not promoted into PAI Memory.",
        "provenance": {
            "fixture_corpus": "approved S10A-S10F fixture corpus",
            "harness": "read-only in-process harness logic",
            "scope": "adapter-test evidence generation only",
            "source_policy": "fixture root only; no release reads; no user-local reads",
        },
        "non_canonical_output_statement": (
            "This report is not PAI Memory; not ISA; not Pulse state; not Claude memory; "
            "not Codex memory; not a PAI runtime audit artifact; not a manifest; "
            "not runtime payload."
        ),
        "limitations": [
            "Codex is not currently proven drop-in.",
            "No Codex runtime was invoked.",
            "No Claude Code runtime was invoked.",
            "No live existing-local-v5 state was read.",
            "No Pulse endpoint was called.",
            "No PAI Memory or ISA write occurred.",
            "The report proves fixture-only evidence generation, not runtime replacement.",
        ],
    }


def main(argv):
    parser = argparse.ArgumentParser(description="Generate the S11A release-fixture read-only evidence report.")
    parser.add_argument("--fixture-root", required=True)
    parser.add_argument("--report-out", required=True)
    args = parser.parse_args(argv)

    try:
        fixture_root = validate_relative_path(args.fixture_root, APPROVED_FIXTURE_ROOT, "fixture root")
        report_path = validate_report_output_path(args.report_out)
        harness = load_harness()
        report = build_report(fixture_root, harness)
        report_text = json.dumps(report, indent=2, sort_keys=True) + "\n"
        report_path.write_text(report_text, encoding="utf-8")
    except Exception as exc:
        return fail(str(exc))

    print(f"wrote S11A release-fixture read-only evidence report: {report_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
