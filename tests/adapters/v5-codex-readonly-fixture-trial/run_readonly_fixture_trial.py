#!/usr/bin/env python3
"""Validate S10A fixture metadata with a read-only harness.

Codex is not currently proven drop-in for existing local PAI v5 files. This
fixture-only harness reads fixture metadata, prints validation status to stdout,
and does not run Codex, Claude Code, Pulse, network calls, subprocesses, or any
runtime adapter path. Fixture metadata is not a manifest, and harness stdout is
not an audit artifact. S10D fixture case data is not a manifest, not an audit
artifact, and not runtime payload.
"""

import argparse
import json
import re
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

ALLOWED_SEAMS = {
    "authority seam",
    "compact router seam",
    "launcher seam",
    "inference seam",
    "engine profile/capability seam",
    "hook/lifecycle seam",
    "event/context envelope seam",
    "hook permission/safety seam",
    "Pulse identity seam",
    "Pulse read-only event seam",
    "Pulse observability/audit seam",
    "Memory/ISA single-writer seam",
    "Memory boundary/promotion seam",
    "ISA workflow/state seam",
    "Memory/ISA audit/conflict seam",
    "manifest schema seam",
    "audit schema seam",
    "dry-run validation seam",
    "rollback seam",
    "fixture isolation seam",
    "denied-path seam",
    "unsupported-surface seam",
    "dual-engine boundary seam",
}

ALLOWED_COVERAGE_IDS = {f"CVG-{index:03d}" for index in range(1, 26)}
ALLOWED_GATE_IDS = {f"TG-{index:03d}" for index in range(1, 21)}

REQUIRED_SAFETY_ASSERTIONS = {
    "fixture_only",
    "read_only",
    "no_live_user_local_state",
    "no_existing_local_v5_access",
    "no_root_agents_write",
    "no_codex_surface_write",
    "no_release_file_write",
    "no_claude_file_direct_copy",
    "no_codex_runtime_invocation",
    "no_claude_code_invocation",
    "no_pulse_start",
    "no_pulse_endpoint_call",
    "no_pai_memory_write",
    "no_isa_write",
    "no_product_memory_promotion",
    "no_drop_in_claim",
    "not_manifest",
    "not_audit_artifact",
    "not_runtime_payload",
}

S10C_DENIAL_TERMS = {
    "live user-local state",
    "root AGENTS.md",
    ".codex/",
    "Releases/ write",
    "PAI Memory write",
    "ISA write",
    "Pulse startup",
    "Pulse endpoint call",
    "product memory promotion",
    "Claude file direct-copy",
    "runtime invocation",
    "drop-in claim",
}

SYNTHETIC_SOURCE_PREFIXES = ("synthetic:", "negative:", "unsupported:")
APPROVED_SOURCE_PREFIXES = (
    "Releases/v5.0.0/",
    "docs/adapters/",
    "tests/adapters/v5-codex-readonly-fixture-trial/",
)

REQUIRED_CASE_FIELDS = {
    "case_id",
    "fixture_id",
    "case_name",
    "case_type",
    "case_status",
    "input_symbols",
    "source_references",
    "expected_behaviors",
    "denied_behaviors",
    "unsupported_surface_expectations",
    "no_write_expectations",
    "audit_expectations",
    "rollback_expectations",
    "prohibited_actions",
    "source_policy",
    "drop_in_claim_allowed",
    "codex_runtime_invocation_allowed",
    "claude_code_invocation_allowed",
    "pulse_start_allowed",
    "pulse_endpoint_call_allowed",
    "pai_memory_write_allowed",
    "isa_write_allowed",
    "product_memory_promotion_allowed",
    "existing_local_v5_access_allowed",
}

ALLOWED_CASE_TYPES = {
    "release-baseline-boundary",
    "authority-boundary",
    "router-non-installation-boundary",
    "launcher-inference-boundary",
    "hook-lifecycle-boundary",
    "pulse-boundary",
    "memory-isa-boundary",
    "denied-path-boundary",
    "product-memory-boundary",
    "unsupported-surface-boundary",
    "rollback-boundary",
    "dual-engine-boundary",
}

REQUIRED_FALSE_CASE_BOOLEANS = {
    "drop_in_claim_allowed",
    "codex_runtime_invocation_allowed",
    "claude_code_invocation_allowed",
    "pulse_start_allowed",
    "pulse_endpoint_call_allowed",
    "pai_memory_write_allowed",
    "isa_write_allowed",
    "product_memory_promotion_allowed",
    "existing_local_v5_access_allowed",
}

REQUIRED_SOURCE_POLICY = {
    "repository_relative_only",
    "synthetic_markers_allowed",
    "no_absolute_paths",
    "no_home_paths",
    "no_parent_traversal",
    "no_protected_root_paths",
    "no_live_user_local_paths",
    "no_release_file_writes",
}

REQUIRED_CASE_LIST_FIELDS = {
    "input_symbols",
    "expected_behaviors",
    "denied_behaviors",
    "unsupported_surface_expectations",
    "no_write_expectations",
    "audit_expectations",
    "rollback_expectations",
    "prohibited_actions",
}

REQUIRED_CASE_DENIED_BEHAVIORS = {
    "root AGENTS.md write",
    ".codex/ write",
    "release file write",
    "Claude file direct-copy",
    "Codex runtime invocation",
    "Claude Code invocation",
    "Pulse startup",
    "Pulse endpoint call",
    "PAI Memory write",
    "ISA write",
    "product memory promotion",
    "existing-local-v5 access",
    "drop-in claim",
}


def load_fixture(metadata_path):
    try:
        return json.loads(metadata_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"__load_error__": str(exc)}


def load_case(case_path):
    try:
        return json.loads(case_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"__case_load_error__": str(exc)}


def validate_source_policy(metadata_path, source_text, failures):
    if source_text.startswith(SYNTHETIC_SOURCE_PREFIXES):
        return

    if source_text.startswith("/") or source_text.startswith("~") or ".." in source_text:
        failures.append(f"{metadata_path}: forbidden source path: {source_text}")
    if source_text.startswith((".codex", ".claude", "PAI/", "AGENTS.md", "CLAUDE.md")):
        failures.append(f"{metadata_path}: protected source path: {source_text}")
    if "/home/" in source_text or "/Users/" in source_text:
        failures.append(f"{metadata_path}: private source path: {source_text}")
    if not source_text.startswith(APPROVED_SOURCE_PREFIXES):
        failures.append(f"{metadata_path}: source path lacks approved repo-relative prefix: {source_text}")


def validate_case_source_policy(case_path, source_text, failures):
    if source_text.startswith(SYNTHETIC_SOURCE_PREFIXES):
        return

    if source_text.startswith("/") or source_text.startswith("~") or ".." in source_text:
        failures.append(f"{case_path}: forbidden source reference: {source_text}")
    if source_text.startswith((".codex", ".claude", "PAI/", "AGENTS.md", "CLAUDE.md")):
        failures.append(f"{case_path}: protected source reference: {source_text}")
    if "/home/" in source_text or "/Users/" in source_text:
        failures.append(f"{case_path}: private source reference: {source_text}")
    if not source_text.startswith(APPROVED_SOURCE_PREFIXES):
        failures.append(f"{case_path}: source reference lacks approved repo-relative prefix: {source_text}")


def validate_semantic_fields(metadata_path, data, denial_text, failures):
    if "covered_seams" not in data:
        failures.append(f"{metadata_path}: missing covered_seams")
    else:
        seams = data.get("covered_seams")
        if not isinstance(seams, list) or not seams:
            failures.append(f"{metadata_path}: covered_seams must be non-empty list")
        else:
            unknown = sorted(set(str(seam) for seam in seams) - ALLOWED_SEAMS)
            if unknown:
                failures.append(f"{metadata_path}: unknown covered_seams: {unknown}")

    if "coverage_ids" not in data:
        failures.append(f"{metadata_path}: missing coverage_ids")
    else:
        coverage_ids = data.get("coverage_ids")
        if not isinstance(coverage_ids, list) or not coverage_ids:
            failures.append(f"{metadata_path}: coverage_ids must be non-empty list")
        else:
            malformed = [cid for cid in coverage_ids if not re.fullmatch(r"CVG-\d{3}", str(cid))]
            unknown = sorted(set(str(cid) for cid in coverage_ids) - ALLOWED_COVERAGE_IDS)
            if malformed:
                failures.append(f"{metadata_path}: malformed coverage_ids: {malformed}")
            if unknown:
                failures.append(f"{metadata_path}: unknown coverage_ids: {unknown}")

    if "gate_ids" not in data:
        failures.append(f"{metadata_path}: missing gate_ids")
    else:
        gate_ids = data.get("gate_ids")
        if not isinstance(gate_ids, list) or not gate_ids:
            failures.append(f"{metadata_path}: gate_ids must be non-empty list")
        else:
            malformed = [gid for gid in gate_ids if not re.fullmatch(r"TG-\d{3}", str(gid))]
            unknown = sorted(set(str(gid) for gid in gate_ids) - ALLOWED_GATE_IDS)
            if malformed:
                failures.append(f"{metadata_path}: malformed gate_ids: {malformed}")
            if unknown:
                failures.append(f"{metadata_path}: unknown gate_ids: {unknown}")

    if "safety_assertions" not in data:
        failures.append(f"{metadata_path}: missing safety_assertions")
    else:
        safety = data.get("safety_assertions")
        if not isinstance(safety, dict):
            failures.append(f"{metadata_path}: safety_assertions must be an object")
        else:
            missing = sorted(REQUIRED_SAFETY_ASSERTIONS - set(safety.keys()))
            if missing:
                failures.append(f"{metadata_path}: missing safety_assertions keys: {missing}")
            for key in sorted(REQUIRED_SAFETY_ASSERTIONS & set(safety.keys())):
                if safety.get(key) is not True:
                    failures.append(f"{metadata_path}: safety_assertions.{key} must be true")

    if "semantic_status" not in data:
        failures.append(f"{metadata_path}: missing semantic_status")
    elif data.get("semantic_status") != "s10c-semantically-hardened":
        failures.append(f"{metadata_path}: invalid semantic_status: {data.get('semantic_status')}")

    for term in sorted(S10C_DENIAL_TERMS):
        if term not in denial_text:
            failures.append(f"{metadata_path}: missing denied-path coverage term: {term}")

    unsupported = data.get("expected_unsupported_surfaces", [])
    if not isinstance(unsupported, list) or not unsupported:
        failures.append(f"{metadata_path}: expected_unsupported_surfaces must be non-empty")


def validate_case_file(case_path, fixture_id, metadata_fixture_id, failures):
    if not case_path.is_file():
        failures.append(f"{case_path}: missing case.json")
        return

    case = load_case(case_path)
    if "__case_load_error__" in case:
        failures.append(f"{case_path}: invalid case JSON: {case['__case_load_error__']}")
        return

    missing_fields = sorted(REQUIRED_CASE_FIELDS - set(case.keys()))
    if missing_fields:
        failures.append(f"{case_path}: missing required case fields: {missing_fields}")

    case_fixture_id = case.get("fixture_id")
    if case_fixture_id != fixture_id or case_fixture_id != metadata_fixture_id:
        failures.append(
            f"{case_path}: fixture_id mismatch between directory, fixture.json, and case.json"
        )

    case_type = case.get("case_type")
    if case_type not in ALLOWED_CASE_TYPES:
        failures.append(f"{case_path}: invalid case_type: {case_type}")

    case_status = case.get("case_status")
    if case_status != "s10d-fixture-case-data-only":
        failures.append(f"{case_path}: invalid case_status: {case_status}")

    for field in sorted(REQUIRED_CASE_LIST_FIELDS):
        value = case.get(field)
        if not isinstance(value, list) or not value:
            failures.append(f"{case_path}: {field} must be a non-empty list")

    denied_behaviors = case.get("denied_behaviors", [])
    denied_text = "\n".join(str(value) for value in denied_behaviors) if isinstance(denied_behaviors, list) else ""
    for term in sorted(REQUIRED_CASE_DENIED_BEHAVIORS):
        if term not in denied_text:
            failures.append(f"{case_path}: missing denied behavior: {term}")

    source_policy = case.get("source_policy")
    if not isinstance(source_policy, dict):
        failures.append(f"{case_path}: source_policy must be an object")
        source_policy = {}
    missing_policy = sorted(REQUIRED_SOURCE_POLICY - set(source_policy.keys()))
    if missing_policy:
        failures.append(f"{case_path}: missing source_policy keys: {missing_policy}")
    for key in sorted(REQUIRED_SOURCE_POLICY & set(source_policy.keys())):
        if source_policy.get(key) is not True:
            failures.append(f"{case_path}: source_policy.{key} must be true")

    source_references = case.get("source_references", [])
    if not isinstance(source_references, list):
        failures.append(f"{case_path}: source_references must be a list")
        source_references = []
    for source_reference in source_references:
        validate_case_source_policy(case_path, str(source_reference), failures)

    for field in sorted(REQUIRED_FALSE_CASE_BOOLEANS):
        if case.get(field) is not False:
            failures.append(f"{case_path}: {field} must be false")


def validate_fixture(root, fixture_id, dirname, failures):
    directory = root / dirname
    if not directory.is_dir():
        failures.append(f"{fixture_id}: missing fixture directory {directory}")
        return

    children = sorted(child.name for child in directory.iterdir())
    if children != ["README.md", "case.json", "fixture.json"]:
        failures.append(f"{dirname}: expected exactly README.md, case.json, fixture.json, got {children}")

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
        validate_source_policy(metadata_path, source_text, failures)

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
    validate_semantic_fields(metadata_path, data, denial_text, failures)
    validate_case_file(directory / "case.json", fixture_id, data.get("fixture_id"), failures)


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


def count_case_files(root):
    if not root.is_dir():
        return 0
    return sum(1 for dirname in EXPECTED_FIXTURES.values() if (root / dirname / "case.json").is_file())


def main(argv):
    parser = argparse.ArgumentParser(description="Validate S10D read-only fixture metadata and case data.")
    parser.add_argument("--fixture-root", required=True, help="Approved S10A fixture root.")
    args = parser.parse_args(argv)

    fixture_root = Path(args.fixture_root)
    failures = validate_fixture_root(fixture_root)

    print("S10A read-only fixture validation report")
    print("S10C semantic validation")
    print("S10D fixture case validation")
    print(f"fixture_root: {fixture_root}")
    print(f"expected_fixture_count: {len(EXPECTED_FIXTURES)}")
    print(f"fixture_count: {len(EXPECTED_FIXTURES)}")
    print(f"case_count: {count_case_files(fixture_root)}")
    print("semantic_status: s10c-semantically-hardened")
    print("case_status: s10d-fixture-case-data-only")

    if failures:
        print("status: fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("status: pass")
    print("validated: fixture-only metadata, read-only harness posture, denied_action_report coverage")
    print("validated: unsupported_surface_report coverage, rollback/no-residue posture, no live user-local paths")
    print("validated: no PAI Memory writes, no ISA writes, no Pulse startup, no Pulse endpoint calls")
    print("validated: fixture case expected behaviors, denied_behaviors, no_write_expectations, audit_expectations")
    print("note: this harness does not prove Codex drop-in behavior or official upstream engine status")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
