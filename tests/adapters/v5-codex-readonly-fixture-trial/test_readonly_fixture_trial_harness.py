#!/usr/bin/env python3
"""S10D fixture case negative-control self-tests for the read-only harness.

Codex is not currently proven drop-in for existing local PAI v5 files. These
negative-control tests prove only fixture harness behavior. They do not run
Codex, Claude Code, Pulse, network calls, subprocesses, or runtime adapter code.
Temporary negative-control data is not a fixture corpus, not a manifest, not an
audit artifact, and not runtime payload. S10D extends negative-control coverage
for fixture case data, expected behavior, denied_behaviors,
unsupported_surface_expectations, no_write_expectations, audit_expectations,
rollback_expectations, prohibited_actions, and non-drop-in posture.
"""

import importlib.util
import json
import sys
import tempfile
from pathlib import Path


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
APPROVED_FIXTURE_ROOT = HERE / "fixtures"
HARNESS_PATH = HERE / "run_readonly_fixture_trial.py"


def import_harness():
    spec = importlib.util.spec_from_file_location("s10a_readonly_fixture_harness", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to import harness from {HARNESS_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HARNESS = import_harness()


def fixture_dir(root, fixture_id):
    return root / HARNESS.EXPECTED_FIXTURES[fixture_id]


def metadata_path(root, fixture_id):
    return fixture_dir(root, fixture_id) / "fixture.json"


def case_path(root, fixture_id):
    return fixture_dir(root, fixture_id) / "case.json"


def read_metadata(root, fixture_id):
    return json.loads(metadata_path(root, fixture_id).read_text(encoding="utf-8"))


def read_case(root, fixture_id):
    return json.loads(case_path(root, fixture_id).read_text(encoding="utf-8"))


def store_metadata(root, fixture_id, data):
    metadata_path(root, fixture_id).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def store_case(root, fixture_id, data):
    case_path(root, fixture_id).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_valid_temp_corpus(root, omit_fixture_id=None):
    root.mkdir(parents=True)
    for fixture_id, dirname in HARNESS.EXPECTED_FIXTURES.items():
        if fixture_id == omit_fixture_id:
            continue
        source_dir = APPROVED_FIXTURE_ROOT / dirname
        target_dir = root / dirname
        target_dir.mkdir()
        for filename in ("README.md", "fixture.json", "case.json"):
            (target_dir / filename).write_text(
                (source_dir / filename).read_text(encoding="utf-8"),
                encoding="utf-8",
            )


def mutate_metadata(root, fixture_id, mutator):
    data = read_metadata(root, fixture_id)
    mutator(data)
    store_metadata(root, fixture_id, data)


def mutate_case(root, fixture_id, mutator):
    data = read_case(root, fixture_id)
    mutator(data)
    store_case(root, fixture_id, data)


def remove_list_entries(data, field, forbidden_tokens):
    data[field] = [
        item
        for item in data.get(field, [])
        if not any(token in str(item) for token in forbidden_tokens)
    ]


def case_missing_fixture_directory(root):
    write_valid_temp_corpus(root, omit_fixture_id="FX-012")


def case_extra_file(root):
    write_valid_temp_corpus(root)
    (fixture_dir(root, "FX-001") / "extra.txt").write_text("temporary negative-control file\n", encoding="utf-8")


def case_missing_required_field(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.pop("fixture_name", None))


def case_invalid_source_class(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.update({"fixture_source_class": "invalid-source-class"}))


def case_sanitized_user_fixture(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.update({"fixture_source_class": "sanitized-user-fixture"}))


def case_private_source_path(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.update({"source_paths": ["~/.claude/PAI"]}))


def case_missing_no_write_key(root):
    write_valid_temp_corpus(root)

    def mutate(data):
        data["expected_no_write_proofs"].pop("no_isa_writes", None)

    mutate_metadata(root, "FX-001", mutate)


def case_false_no_write_value(root):
    write_valid_temp_corpus(root)

    def mutate(data):
        data["expected_no_write_proofs"]["no_isa_writes"] = False

    mutate_metadata(root, "FX-001", mutate)


def case_missing_audit_field(root):
    write_valid_temp_corpus(root)

    def mutate(data):
        data["expected_audit_fields"] = [
            field for field in data.get("expected_audit_fields", []) if field != "provenance"
        ]

    mutate_metadata(root, "FX-001", mutate)


def case_missing_pulse_endpoint_denial(root):
    write_valid_temp_corpus(root)

    def mutate(data):
        tokens = ("Pulse endpoint calls", "localhost:31337")
        remove_list_entries(data, "denied_paths", tokens)
        remove_list_entries(data, "expected_denials", tokens)

    mutate_metadata(root, "FX-001", mutate)


def case_invalid_privacy_status(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.update({"privacy_status": "live-private"}))


def case_invalid_s10a_status(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.update({"s10a_status": "runtime-fixture"}))


def case_invalid_json(root):
    write_valid_temp_corpus(root)
    metadata_path(root, "FX-001").write_text("{ invalid json\n", encoding="utf-8")


def case_unexpected_directory(root):
    write_valid_temp_corpus(root)
    (root / "FX-999-unexpected").mkdir()


def case_missing_readme(root):
    write_valid_temp_corpus(root)
    (fixture_dir(root, "FX-001") / "README.md").unlink()


def case_missing_covered_seams(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.pop("covered_seams", None))


def case_unknown_seam(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.update({"covered_seams": ["unknown seam"]}))


def case_missing_coverage_ids(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.pop("coverage_ids", None))


def case_malformed_coverage_id(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.update({"coverage_ids": ["BAD-001"]}))


def case_missing_gate_ids(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.pop("gate_ids", None))


def case_malformed_gate_id(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.update({"gate_ids": ["BAD-001"]}))


def case_missing_safety_assertions(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.pop("safety_assertions", None))


def case_false_safety_assertion(root):
    write_valid_temp_corpus(root)

    def mutate(data):
        data["safety_assertions"]["no_isa_write"] = False

    mutate_metadata(root, "FX-001", mutate)


def case_missing_semantic_status(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.pop("semantic_status", None))


def case_invalid_semantic_status(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.update({"semantic_status": "runtime-ready"}))


def case_parent_traversal_source_path(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.update({"source_paths": ["docs/adapters/../secret.md"]}))


def case_absolute_source_path(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.update({"source_paths": ["/tmp/private"]}))


def case_missing_denied_path_category(root):
    write_valid_temp_corpus(root)

    def mutate(data):
        tokens = ("drop-in claim",)
        remove_list_entries(data, "denied_paths", tokens)
        remove_list_entries(data, "expected_denials", tokens)

    mutate_metadata(root, "FX-001", mutate)


def case_missing_unsupported_surface(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.update({"expected_unsupported_surfaces": []}))


def case_protected_source_path(root):
    write_valid_temp_corpus(root)
    mutate_metadata(root, "FX-001", lambda data: data.update({"source_paths": [".codex/config.toml"]}))


def case_missing_case_json(root):
    write_valid_temp_corpus(root)
    case_path(root, "FX-001").unlink()


def case_invalid_case_json(root):
    write_valid_temp_corpus(root)
    case_path(root, "FX-001").write_text("{ invalid case json\n", encoding="utf-8")


def case_fixture_id_mismatch(root):
    write_valid_temp_corpus(root)
    mutate_case(root, "FX-001", lambda data: data.update({"fixture_id": "FX-999"}))


def case_missing_required_case_field(root):
    write_valid_temp_corpus(root)
    mutate_case(root, "FX-001", lambda data: data.pop("case_name", None))


def case_invalid_case_type(root):
    write_valid_temp_corpus(root)
    mutate_case(root, "FX-001", lambda data: data.update({"case_type": "runtime-boundary"}))


def case_invalid_case_status(root):
    write_valid_temp_corpus(root)
    mutate_case(root, "FX-001", lambda data: data.update({"case_status": "runtime-ready"}))


def case_empty_input_symbols(root):
    write_valid_temp_corpus(root)
    mutate_case(root, "FX-001", lambda data: data.update({"input_symbols": []}))


def case_empty_expected_behaviors(root):
    write_valid_temp_corpus(root)
    mutate_case(root, "FX-001", lambda data: data.update({"expected_behaviors": []}))


def case_missing_case_denied_behavior(root):
    write_valid_temp_corpus(root)

    def mutate(data):
        data["denied_behaviors"] = [
            behavior for behavior in data.get("denied_behaviors", []) if "drop-in claim" not in str(behavior)
        ]

    mutate_case(root, "FX-001", mutate)


def case_empty_unsupported_surface_expectations(root):
    write_valid_temp_corpus(root)
    mutate_case(root, "FX-001", lambda data: data.update({"unsupported_surface_expectations": []}))


def case_empty_no_write_expectations(root):
    write_valid_temp_corpus(root)
    mutate_case(root, "FX-001", lambda data: data.update({"no_write_expectations": []}))


def case_false_source_policy(root):
    write_valid_temp_corpus(root)

    def mutate(data):
        data["source_policy"]["no_home_paths"] = False

    mutate_case(root, "FX-001", mutate)


def case_forbidden_source_reference(root):
    write_valid_temp_corpus(root)
    mutate_case(root, "FX-001", lambda data: data.update({"source_references": ["~/.claude/PAI"]}))


def case_prohibited_boolean_true(root):
    write_valid_temp_corpus(root)
    mutate_case(root, "FX-001", lambda data: data.update({"pulse_start_allowed": True}))


def case_s10d_extra_fixture_file(root):
    write_valid_temp_corpus(root)
    (fixture_dir(root, "FX-001") / "extra-case.txt").write_text(
        "temporary S10D negative-control file\n",
        encoding="utf-8",
    )


NEGATIVE_CASES = [
    {
        "negative_id": "NC-001",
        "description": "Missing fixture directory is detected.",
        "expected_failure_signal": "missing fixture directory",
        "builder": case_missing_fixture_directory,
    },
    {
        "negative_id": "NC-002",
        "description": "Extra file inside a fixture directory is detected.",
        "expected_failure_signal": "expected exactly README.md, case.json, fixture.json",
        "builder": case_extra_file,
    },
    {
        "negative_id": "NC-003",
        "description": "Missing required metadata field is detected.",
        "expected_failure_signal": "missing fields",
        "builder": case_missing_required_field,
    },
    {
        "negative_id": "NC-004",
        "description": "Invalid fixture_source_class is detected.",
        "expected_failure_signal": "invalid fixture_source_class",
        "builder": case_invalid_source_class,
    },
    {
        "negative_id": "NC-005",
        "description": "Forbidden sanitized-user-fixture source class is detected.",
        "expected_failure_signal": "sanitized-user-fixture is not allowed",
        "builder": case_sanitized_user_fixture,
    },
    {
        "negative_id": "NC-006",
        "description": "Forbidden live/private source path such as ~/.claude/PAI is detected.",
        "expected_failure_signal": "live/private source path not allowed",
        "builder": case_private_source_path,
    },
    {
        "negative_id": "NC-007",
        "description": "Missing expected_no_write_proofs key is detected.",
        "expected_failure_signal": "missing expected_no_write_proofs keys",
        "builder": case_missing_no_write_key,
    },
    {
        "negative_id": "NC-008",
        "description": "False expected_no_write_proofs value is detected.",
        "expected_failure_signal": "expected_no_write_proofs.no_isa_writes must be true",
        "builder": case_false_no_write_value,
    },
    {
        "negative_id": "NC-009",
        "description": "Missing expected_audit_fields value is detected.",
        "expected_failure_signal": "missing expected_audit_fields",
        "builder": case_missing_audit_field,
    },
    {
        "negative_id": "NC-010",
        "description": "Missing denied-path coverage for Pulse endpoint calls is detected.",
        "expected_failure_signal": "missing denial coverage for Pulse endpoint calls",
        "builder": case_missing_pulse_endpoint_denial,
    },
    {
        "negative_id": "NC-011",
        "description": "Invalid privacy_status is detected.",
        "expected_failure_signal": "invalid privacy_status",
        "builder": case_invalid_privacy_status,
    },
    {
        "negative_id": "NC-012",
        "description": "Invalid s10a_status is detected.",
        "expected_failure_signal": "invalid s10a_status",
        "builder": case_invalid_s10a_status,
    },
    {
        "negative_id": "NC-013",
        "description": "Invalid JSON in fixture.json is detected.",
        "expected_failure_signal": "invalid JSON",
        "builder": case_invalid_json,
    },
    {
        "negative_id": "NC-014",
        "description": "Unexpected fixture directory is detected.",
        "expected_failure_signal": "unexpected fixture directories",
        "builder": case_unexpected_directory,
    },
    {
        "negative_id": "NC-015",
        "description": "Missing README is detected.",
        "expected_failure_signal": "expected exactly README.md, case.json, fixture.json",
        "builder": case_missing_readme,
    },
    {
        "negative_id": "NC-016",
        "description": "Missing covered_seams is detected.",
        "expected_failure_signal": "missing covered_seams",
        "builder": case_missing_covered_seams,
    },
    {
        "negative_id": "NC-017",
        "description": "Unknown seam value is detected.",
        "expected_failure_signal": "unknown covered_seams",
        "builder": case_unknown_seam,
    },
    {
        "negative_id": "NC-018",
        "description": "Missing coverage_ids is detected.",
        "expected_failure_signal": "missing coverage_ids",
        "builder": case_missing_coverage_ids,
    },
    {
        "negative_id": "NC-019",
        "description": "Malformed coverage ID is detected.",
        "expected_failure_signal": "malformed coverage_ids",
        "builder": case_malformed_coverage_id,
    },
    {
        "negative_id": "NC-020",
        "description": "Missing gate_ids is detected.",
        "expected_failure_signal": "missing gate_ids",
        "builder": case_missing_gate_ids,
    },
    {
        "negative_id": "NC-021",
        "description": "Malformed gate ID is detected.",
        "expected_failure_signal": "malformed gate_ids",
        "builder": case_malformed_gate_id,
    },
    {
        "negative_id": "NC-022",
        "description": "Missing safety_assertions is detected.",
        "expected_failure_signal": "missing safety_assertions",
        "builder": case_missing_safety_assertions,
    },
    {
        "negative_id": "NC-023",
        "description": "False safety_assertions value is detected.",
        "expected_failure_signal": "safety_assertions.no_isa_write must be true",
        "builder": case_false_safety_assertion,
    },
    {
        "negative_id": "NC-024",
        "description": "Missing semantic_status is detected.",
        "expected_failure_signal": "missing semantic_status",
        "builder": case_missing_semantic_status,
    },
    {
        "negative_id": "NC-025",
        "description": "Invalid semantic_status is detected.",
        "expected_failure_signal": "invalid semantic_status",
        "builder": case_invalid_semantic_status,
    },
    {
        "negative_id": "NC-026",
        "description": "Forbidden parent traversal in source_paths is detected.",
        "expected_failure_signal": "forbidden source path",
        "builder": case_parent_traversal_source_path,
    },
    {
        "negative_id": "NC-027",
        "description": "Forbidden absolute path in source_paths is detected.",
        "expected_failure_signal": "forbidden source path",
        "builder": case_absolute_source_path,
    },
    {
        "negative_id": "NC-028",
        "description": "Missing denied-path category is detected.",
        "expected_failure_signal": "missing denied-path coverage term: drop-in claim",
        "builder": case_missing_denied_path_category,
    },
    {
        "negative_id": "NC-029",
        "description": "Missing unsupported-surface coverage is detected.",
        "expected_failure_signal": "expected_unsupported_surfaces must be non-empty",
        "builder": case_missing_unsupported_surface,
    },
    {
        "negative_id": "NC-030",
        "description": "Source path to .codex/ or root AGENTS.md is detected.",
        "expected_failure_signal": "protected source path",
        "builder": case_protected_source_path,
    },
    {
        "negative_id": "NC-031",
        "description": "Missing case.json is detected.",
        "expected_failure_signal": "missing case.json",
        "builder": case_missing_case_json,
    },
    {
        "negative_id": "NC-032",
        "description": "Invalid JSON in case.json is detected.",
        "expected_failure_signal": "invalid case JSON",
        "builder": case_invalid_case_json,
    },
    {
        "negative_id": "NC-033",
        "description": "Fixture ID mismatch in case.json is detected.",
        "expected_failure_signal": "fixture_id mismatch between directory, fixture.json, and case.json",
        "builder": case_fixture_id_mismatch,
    },
    {
        "negative_id": "NC-034",
        "description": "Missing required case field is detected.",
        "expected_failure_signal": "missing required case fields",
        "builder": case_missing_required_case_field,
    },
    {
        "negative_id": "NC-035",
        "description": "Invalid case_type is detected.",
        "expected_failure_signal": "invalid case_type",
        "builder": case_invalid_case_type,
    },
    {
        "negative_id": "NC-036",
        "description": "Invalid case_status is detected.",
        "expected_failure_signal": "invalid case_status",
        "builder": case_invalid_case_status,
    },
    {
        "negative_id": "NC-037",
        "description": "Empty input_symbols is detected.",
        "expected_failure_signal": "input_symbols must be a non-empty list",
        "builder": case_empty_input_symbols,
    },
    {
        "negative_id": "NC-038",
        "description": "Empty expected_behaviors is detected.",
        "expected_failure_signal": "expected_behaviors must be a non-empty list",
        "builder": case_empty_expected_behaviors,
    },
    {
        "negative_id": "NC-039",
        "description": "Missing denied behavior category is detected.",
        "expected_failure_signal": "missing denied behavior: drop-in claim",
        "builder": case_missing_case_denied_behavior,
    },
    {
        "negative_id": "NC-040",
        "description": "Empty unsupported_surface_expectations is detected.",
        "expected_failure_signal": "unsupported_surface_expectations must be a non-empty list",
        "builder": case_empty_unsupported_surface_expectations,
    },
    {
        "negative_id": "NC-041",
        "description": "Empty no_write_expectations is detected.",
        "expected_failure_signal": "no_write_expectations must be a non-empty list",
        "builder": case_empty_no_write_expectations,
    },
    {
        "negative_id": "NC-042",
        "description": "False or missing source_policy key is detected.",
        "expected_failure_signal": "source_policy.no_home_paths must be true",
        "builder": case_false_source_policy,
    },
    {
        "negative_id": "NC-043",
        "description": "Forbidden source reference such as ~/.claude/PAI is detected.",
        "expected_failure_signal": "forbidden source reference",
        "builder": case_forbidden_source_reference,
    },
    {
        "negative_id": "NC-044",
        "description": "Prohibited action boolean set to true is detected.",
        "expected_failure_signal": "pulse_start_allowed must be false",
        "builder": case_prohibited_boolean_true,
    },
    {
        "negative_id": "NC-045",
        "description": "Extra unexpected file in fixture directory is detected after S10D file-set rules.",
        "expected_failure_signal": "expected exactly README.md, case.json, fixture.json",
        "builder": case_s10d_extra_fixture_file,
    },
]


def run_positive_control():
    failures = HARNESS.validate_fixture_root(APPROVED_FIXTURE_ROOT)
    return {
        "status": "pass" if not failures else "fail",
        "failures": failures,
    }


def run_negative_case(case):
    with tempfile.TemporaryDirectory(prefix="s10d-harness-negative-control-") as temp_dir:
        temp_root = Path(temp_dir) / "fixtures"
        case["builder"](temp_root)
        failures = HARNESS.validate_fixture_root(temp_root)

    expected = case["expected_failure_signal"]
    observed = next((failure for failure in failures if expected in failure), failures[0] if failures else "")
    status = "pass" if failures and expected in observed else "fail"
    return {
        "negative_id": case["negative_id"],
        "description": case["description"],
        "expected_failure_signal": expected,
        "observed_failure_signal": observed,
        "status": status,
    }


def main():
    positive = run_positive_control()
    results = [run_negative_case(case) for case in NEGATIVE_CASES]
    overall_pass = positive["status"] == "pass" and all(result["status"] == "pass" for result in results)

    print("S10D fixture case negative-control self-test report")
    print(f"positive_control_status: {positive['status']}")
    if positive["failures"]:
        for failure in positive["failures"]:
            print(f"positive_control_failure: {failure}")
    print(f"negative_control_count: {len(results)}")

    for result in results:
        print(f"negative_id: {result['negative_id']}")
        print(f"description: {result['description']}")
        print(f"expected_failure_signal: {result['expected_failure_signal']}")
        print(f"observed_failure_signal: {result['observed_failure_signal']}")
        print(f"status: {result['status']}")

    print(f"status: {'pass' if overall_pass else 'fail'}")
    print("scope: negative-control temporary data only; no live user-local reads; no Pulse calls")
    print("scope: no PAI Memory writes; no ISA writes; not PAI Memory; product memories are not promoted")
    print("scope: PAI_SYSTEM_PROMPT.md remains high-authority; CLAUDE.md and AGENTS.md must not be copied directly")
    print("scope: rollback posture remains temporary-directory cleanup and no repository no-residue artifacts")
    print("scope: case.json is fixture case data only, not a manifest, not an audit artifact, and not runtime payload")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
