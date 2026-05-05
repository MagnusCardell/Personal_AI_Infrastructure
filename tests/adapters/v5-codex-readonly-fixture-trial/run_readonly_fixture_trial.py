#!/usr/bin/env python3
"""Validate S10A fixture metadata with a read-only harness.

Codex is not currently proven drop-in for existing local PAI v5 files. This
fixture-only harness reads fixture metadata, prints validation status to stdout,
and does not run Codex, Claude Code, Pulse, network calls, subprocesses, or any
runtime adapter path. Fixture metadata is not a manifest, and harness stdout is
not an audit artifact.
"""

import argparse
import json
import sys
from pathlib import Path


EXPECTED_FIXTURES = {
    "FX-001": "FX-001-release-baseline-static",
    "FX-002": "FX-002-authority-doctrine",
    "FX-003": "FX-003-compact-router-non-installation",
    "FX-004": "FX-004-launcher-inference-static",
    "FX-005": "FX-005-hook-lifecycle-static",
    "FX-006": "FX-006-pulse-static-no-start",
    "FX-007": "FX-007-memory-isa-static-no-write",
    "FX-008": "FX-008-denied-path-negative",
    "FX-009": "FX-009-product-memory-negative",
    "FX-010": "FX-010-unsupported-surface-reporting",
    "FX-011": "FX-011-rollback-no-residue",
    "FX-012": "FX-012-dual-engine-boundary",
}

REQUIRED_FIELDS = {
    "fixture_id",
    "fixture_name",
    "fixture_source_class",
    "pai_version",
    "source_paths",
    "included_surfaces",
    "excluded_surfaces",
    "denied_paths",
    "expected_denials",
    "expected_unsupported_surfaces",
    "expected_no_write_proofs",
    "expected_audit_fields",
    "rollback_expectation",
    "privacy_status",
    "s10a_status",
}

ALLOWED_SOURCE_CLASSES = {
    "release-derived-fixture",
    "synthetic-fixture",
    "negative-safety-fixture",
    "unsupported-surface-fixture",
}

ALLOWED_PRIVACY = {
    "public-release-only",
    "synthetic-only",
    "negative-safety-only",
}

REQUIRED_NO_WRITE_KEYS = {
    "no_release_file_writes",
    "no_root_agents_write",
    "no_codex_surface_write",
    "no_user_local_reads",
    "no_pai_memory_writes",
    "no_isa_writes",
    "no_pulse_start",
    "no_pulse_endpoint_calls",
    "no_product_memory_promotion",
    "no_runtime_invocation",
}

REQUIRED_AUDIT_FIELDS = {
    "fixture_id",
    "files_inspected",
    "files_not_inspected",
    "denied_action_report",
    "unsupported_surface_report",
    "pulse_action_status",
    "memory_write_status",
    "isa_write_status",
    "product_memory_status",
    "rollback_status",
    "residue_status",
    "drop_in_claim_status",
    "provenance",
    "non_promotion_statement",
}

FORBIDDEN_SOURCE_PREFIXES = (
    "~/.claude",
    "~/.codex",
    "/Users/",
    "/home/",
)

REQUIRED_DENIAL_GROUPS = {
    "live private state": ("~/.claude", "~/.codex"),
    "root AGENTS.md": ("AGENTS.md",),
    ".codex surface": (".codex",),
    "Releases writes": ("Releases/ writes",),
    "PAI Memory writes": ("PAI Memory writes",),
    "ISA writes": ("ISA writes",),
    "Pulse startup": ("Pulse startup",),
    "Pulse endpoint calls": ("Pulse endpoint calls", "localhost:31337"),
}


def load_fixture(metadata_path):
    try:
        return json.loads(metadata_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"__load_error__": str(exc)}


def validate_fixture(root, fixture_id, dirname, failures):
    directory = root / dirname
    if not directory.is_dir():
        failures.append(f"{fixture_id}: missing fixture directory {directory}")
        return

    children = sorted(child.name for child in directory.iterdir())
    if children != ["README.md", "fixture.json"]:
        failures.append(f"{dirname}: expected exactly README.md and fixture.json, got {children}")

    metadata_path = directory / "fixture.json"
    data = load_fixture(metadata_path)
    if "__load_error__" in data:
        failures.append(f"{metadata_path}: invalid JSON: {data['__load_error__']}")
        return

    missing_fields = sorted(REQUIRED_FIELDS - set(data.keys()))
    if missing_fields:
        failures.append(f"{metadata_path}: missing fields: {missing_fields}")

    if data.get("fixture_id") != fixture_id:
        failures.append(f"{metadata_path}: fixture_id mismatch: {data.get('fixture_id')} != {fixture_id}")

    source_class = data.get("fixture_source_class")
    if source_class not in ALLOWED_SOURCE_CLASSES:
        failures.append(f"{metadata_path}: invalid fixture_source_class: {source_class}")
    if source_class == "sanitized-user-fixture":
        failures.append(f"{metadata_path}: sanitized-user-fixture is not allowed in S10A")

    privacy_status = data.get("privacy_status")
    if privacy_status not in ALLOWED_PRIVACY:
        failures.append(f"{metadata_path}: invalid privacy_status: {privacy_status}")

    if data.get("s10a_status") != "implemented-fixture-metadata-only":
        failures.append(f"{metadata_path}: invalid s10a_status: {data.get('s10a_status')}")

    source_paths = data.get("source_paths", [])
    if not isinstance(source_paths, list):
        failures.append(f"{metadata_path}: source_paths must be a list")
        source_paths = []
    for source_path in source_paths:
        source_text = str(source_path)
        if source_text.startswith(FORBIDDEN_SOURCE_PREFIXES):
            failures.append(f"{metadata_path}: live/private source path not allowed: {source_text}")

    no_write = data.get("expected_no_write_proofs", {})
    if not isinstance(no_write, dict):
        failures.append(f"{metadata_path}: expected_no_write_proofs must be an object")
        no_write = {}
    missing_no_write = sorted(REQUIRED_NO_WRITE_KEYS - set(no_write.keys()))
    if missing_no_write:
        failures.append(f"{metadata_path}: missing expected_no_write_proofs keys: {missing_no_write}")
    for key in sorted(REQUIRED_NO_WRITE_KEYS & set(no_write.keys())):
        if no_write.get(key) is not True:
            failures.append(f"{metadata_path}: expected_no_write_proofs.{key} must be true")

    audit_fields = data.get("expected_audit_fields", [])
    if not isinstance(audit_fields, list):
        failures.append(f"{metadata_path}: expected_audit_fields must be a list")
        audit_fields = []
    missing_audit = sorted(REQUIRED_AUDIT_FIELDS - set(audit_fields))
    if missing_audit:
        failures.append(f"{metadata_path}: missing expected_audit_fields: {missing_audit}")

    denial_values = []
    for key in ("denied_paths", "expected_denials"):
        values = data.get(key, [])
        if isinstance(values, list):
            denial_values.extend(str(value) for value in values)
        else:
            failures.append(f"{metadata_path}: {key} must be a list")
    denial_text = "\n".join(denial_values)
    for label, tokens in REQUIRED_DENIAL_GROUPS.items():
        if not any(token in denial_text for token in tokens):
            failures.append(f"{metadata_path}: missing denial coverage for {label}")


def validate_fixture_root(root):
    failures = []

    if not root.is_dir():
        return [f"missing fixture root: {root}"]

    actual_dirs = sorted(item.name for item in root.iterdir() if item.is_dir())
    expected_dirs = sorted(EXPECTED_FIXTURES.values())
    if actual_dirs != expected_dirs:
        failures.append(f"unexpected fixture directories: expected {expected_dirs}, got {actual_dirs}")

    for fixture_id, dirname in EXPECTED_FIXTURES.items():
        validate_fixture(root, fixture_id, dirname, failures)

    return failures


def main(argv):
    parser = argparse.ArgumentParser(description="Validate S10A read-only fixture metadata.")
    parser.add_argument("--fixture-root", required=True, help="Approved S10A fixture root.")
    args = parser.parse_args(argv)

    fixture_root = Path(args.fixture_root)
    failures = validate_fixture_root(fixture_root)

    print("S10A read-only fixture validation report")
    print(f"fixture_root: {fixture_root}")
    print(f"expected_fixture_count: {len(EXPECTED_FIXTURES)}")

    if failures:
        print("status: fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("status: pass")
    print("validated: fixture-only metadata, read-only harness posture, denied_action_report coverage")
    print("validated: unsupported_surface_report coverage, rollback/no-residue posture, no live user-local paths")
    print("validated: no PAI Memory writes, no ISA writes, no Pulse startup, no Pulse endpoint calls")
    print("note: this harness does not prove Codex drop-in behavior or official upstream engine status")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
