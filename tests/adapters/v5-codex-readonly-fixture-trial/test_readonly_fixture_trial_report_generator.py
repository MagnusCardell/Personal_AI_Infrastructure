#!/usr/bin/env python3
"""S11B report-generator negative-control self-test report.

Codex is not currently proven drop-in for existing local PAI v5 files. These
controls validate S11A report-generator path safety and malformed fixture-input
handling only. They do not run Codex, Claude Code, Pulse, network access,
subprocesses, live trials, PAI Memory writes, or ISA writes.
"""

import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path


sys.dont_write_bytecode = True


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
FIXTURE_ROOT = SCRIPT_DIR / "fixtures"
GENERATOR_PATH = SCRIPT_DIR / "generate_readonly_fixture_trial_report.py"
APPROVED_REPORT = SCRIPT_DIR / "reports" / "S11A_RELEASE_FIXTURE_TRIAL_REPORT.json"

REQUIRED_REPORT_FIELDS = {
    "report_id",
    "report_type",
    "report_status",
    "pai_version",
    "engine_under_test",
    "adapter_mode",
    "source_kind",
    "fixture_root",
    "generated_from",
    "fixture_count",
    "case_count",
    "seam_count",
    "coverage_id_count",
    "gate_id_count",
    "denied_category_count",
    "positive_harness_status",
    "negative_control_status",
    "no_residue_status",
    "drop_in_claim_status",
    "pulse_status",
    "memory_status",
    "isa_status",
    "product_memory_status",
    "protected_path_status",
    "live_user_local_state_status",
    "unsupported_surface_report_status",
    "denied_action_report_status",
    "rollback_status",
    "non_promotion_statement",
    "provenance",
    "non_canonical_output_statement",
    "limitations",
}


def load_generator():
    spec = importlib.util.spec_from_file_location("s11b_report_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load S11A report generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_fixture_root(target_root):
    shutil.copytree(FIXTURE_ROOT, target_root)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def fixture_file(temp_root, dirname, name):
    return temp_root / dirname / name


def first_fixture_dir(generator):
    return generator.load_harness().EXPECTED_FIXTURES["FX-001"]


def expect_exception(control_id, description, expected_signal, operation):
    try:
        operation()
    except Exception as exc:
        observed = str(exc)
        passed = expected_signal in observed
        return {
            "negative_id": control_id,
            "description": description,
            "expected_failure_signal": expected_signal,
            "observed_failure_signal": observed,
            "status": "pass" if passed else "fail",
        }
    return {
        "negative_id": control_id,
        "description": description,
        "expected_failure_signal": expected_signal,
        "observed_failure_signal": "no failure",
        "status": "fail",
    }


def expect_impossible(control_id, description, expected_signal, operation):
    try:
        observed = operation()
        passed = expected_signal in observed
    except Exception as exc:
        observed = str(exc)
        passed = False
    return {
        "negative_id": control_id,
        "description": description,
        "expected_failure_signal": expected_signal,
        "observed_failure_signal": observed,
        "status": "pass" if passed else "fail",
    }


def build_temp_report(generator, mutator):
    with tempfile.TemporaryDirectory(prefix="s11b-report-generator-") as temp_dir:
        temp_root = Path(temp_dir) / "fixtures"
        copy_fixture_root(temp_root)
        mutator(temp_root, generator)
        return generator.build_report(temp_root, generator.load_harness())


def validate_positive_control(generator):
    status = generator.main([
        "--fixture-root",
        generator.APPROVED_FIXTURE_ROOT.as_posix(),
        "--report-out",
        generator.APPROVED_REPORT_PATH.as_posix(),
    ])
    if status != 0:
        return "fail"
    data = load_json(APPROVED_REPORT)
    if data.get("report_status") != "pass":
        return "fail"
    if data.get("drop_in_claim_status") != "not-claimed":
        return "fail"
    return "pass"


def make_missing_case(temp_root, generator):
    fixture_file(temp_root, first_fixture_dir(generator), "case.json").unlink()


def make_malformed_fixture(temp_root, generator):
    fixture_file(temp_root, first_fixture_dir(generator), "fixture.json").write_text("{ invalid fixture json", encoding="utf-8")


def make_malformed_case(temp_root, generator):
    fixture_file(temp_root, first_fixture_dir(generator), "case.json").write_text("{ invalid case json", encoding="utf-8")


def make_live_user_local_source(temp_root, generator):
    metadata_path = fixture_file(temp_root, first_fixture_dir(generator), "fixture.json")
    metadata = load_json(metadata_path)
    metadata["source_paths"] = ["~/.claude/PAI"]
    write_json(metadata_path, metadata)


def make_pulse_endpoint_authorized(temp_root, generator):
    case_path = fixture_file(temp_root, first_fixture_dir(generator), "case.json")
    case = load_json(case_path)
    case["pulse_endpoint_call_allowed"] = True
    write_json(case_path, case)


def make_memory_isa_authorized(temp_root, generator):
    case_path = fixture_file(temp_root, first_fixture_dir(generator), "case.json")
    case = load_json(case_path)
    case["pai_memory_write_allowed"] = True
    case["isa_write_allowed"] = True
    write_json(case_path, case)


def make_product_memory_promotion(temp_root, generator):
    case_path = fixture_file(temp_root, first_fixture_dir(generator), "case.json")
    case = load_json(case_path)
    case["product_memory_promotion_allowed"] = True
    write_json(case_path, case)


def report_missing_field_impossible(generator):
    report = generator.build_report(generator.APPROVED_FIXTURE_ROOT, generator.load_harness())
    missing = sorted(REQUIRED_REPORT_FIELDS - set(report.keys()))
    if missing:
        return "missing required report fields: " + ", ".join(missing)
    return "impossible by construction: required report fields present"


def report_wrong_status_impossible(generator):
    report = generator.build_report(generator.APPROVED_FIXTURE_ROOT, generator.load_harness())
    if report.get("report_status") != "pass":
        return f"wrong status observed: {report.get('report_status')}"
    return "impossible by construction: report_status is pass"


def report_drop_in_claim_impossible(generator):
    report = generator.build_report(generator.APPROVED_FIXTURE_ROOT, generator.load_harness())
    if report.get("drop_in_claim_status") != "not-claimed":
        return f"drop-in claim observed: {report.get('drop_in_claim_status')}"
    limitations = " ".join(report.get("limitations", []))
    if "Codex is not currently proven drop-in" not in limitations:
        return "missing non-drop-in limitation"
    return "impossible by construction: drop-in claim is not-claimed"


def report_non_canonical_omission_impossible(generator):
    report = generator.build_report(generator.APPROVED_FIXTURE_ROOT, generator.load_harness())
    statement = report.get("non_canonical_output_statement", "")
    required = [
        "not PAI Memory",
        "not ISA",
        "not Pulse state",
        "not Claude memory",
        "not Codex memory",
        "not a PAI runtime audit artifact",
        "not a manifest",
        "not runtime payload",
    ]
    missing = [term for term in required if term not in statement]
    if missing:
        return "missing non-canonical terms: " + ", ".join(missing)
    return "impossible by construction: non-canonical output statement complete"


def negative_controls(generator):
    def missing_fixture_root():
        with tempfile.TemporaryDirectory(prefix="s11b-report-generator-") as temp_dir:
            generator.build_report(Path(temp_dir) / "missing-fixtures", generator.load_harness())

    return [
        expect_exception(
            "RG-001",
            "absolute report path rejected",
            "absolute",
            lambda: generator.validate_report_output_path("/tmp/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json"),
        ),
        expect_exception(
            "RG-002",
            "parent traversal report path rejected",
            "parent traversal",
            lambda: generator.validate_report_output_path("tests/adapters/v5-codex-readonly-fixture-trial/reports/../S11A_RELEASE_FIXTURE_TRIAL_REPORT.json"),
        ),
        expect_exception(
            "RG-003",
            "output outside reports directory rejected",
            "must be tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json",
            lambda: generator.validate_report_output_path("tests/adapters/v5-codex-readonly-fixture-trial/outside/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json"),
        ),
        expect_exception(
            "RG-004",
            "unexpected report filename rejected",
            "must be tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json",
            lambda: generator.validate_report_output_path("tests/adapters/v5-codex-readonly-fixture-trial/reports/OTHER.json"),
        ),
        expect_exception(
            "RG-005",
            "missing fixture root rejected",
            "missing fixture root",
            missing_fixture_root,
        ),
        expect_exception(
            "RG-006",
            "fixture root with missing case file rejected",
            "missing case.json",
            lambda: build_temp_report(generator, make_missing_case),
        ),
        expect_exception(
            "RG-007",
            "fixture root with malformed fixture metadata rejected",
            "invalid JSON",
            lambda: build_temp_report(generator, make_malformed_fixture),
        ),
        expect_exception(
            "RG-008",
            "fixture root with malformed case data rejected",
            "invalid case JSON",
            lambda: build_temp_report(generator, make_malformed_case),
        ),
        expect_impossible(
            "RG-009",
            "report missing required field rejected or impossible by construction",
            "impossible by construction",
            lambda: report_missing_field_impossible(generator),
        ),
        expect_impossible(
            "RG-010",
            "report with wrong status rejected or impossible by construction",
            "impossible by construction",
            lambda: report_wrong_status_impossible(generator),
        ),
        expect_impossible(
            "RG-011",
            "report with drop-in claim rejected or impossible by construction",
            "impossible by construction",
            lambda: report_drop_in_claim_impossible(generator),
        ),
        expect_impossible(
            "RG-012",
            "non-canonical output statement omission rejected or impossible by construction",
            "impossible by construction",
            lambda: report_non_canonical_omission_impossible(generator),
        ),
        expect_exception(
            "RG-013",
            "live user-local source reference rejected",
            "live/private source path not allowed",
            lambda: build_temp_report(generator, make_live_user_local_source),
        ),
        expect_exception(
            "RG-014",
            "Pulse endpoint-call authorization rejected",
            "pulse_endpoint_call_allowed must be false",
            lambda: build_temp_report(generator, make_pulse_endpoint_authorized),
        ),
        expect_exception(
            "RG-015",
            "PAI Memory or ISA write authorization rejected",
            "isa_write_allowed must be false",
            lambda: build_temp_report(generator, make_memory_isa_authorized),
        ),
        expect_exception(
            "RG-016",
            "product-memory promotion authorization rejected",
            "product_memory_promotion_allowed must be false",
            lambda: build_temp_report(generator, make_product_memory_promotion),
        ),
    ]


def repository_residue_failures():
    failures = []
    for path in REPO_ROOT.rglob("*"):
        path_text = str(path)
        if "__pycache__" in path_text or path.suffix == ".pyc":
            failures.append(path.relative_to(REPO_ROOT).as_posix())
    return sorted(failures)


def main():
    generator = load_generator()
    positive_status = validate_positive_control(generator)
    results = negative_controls(generator)
    residue = repository_residue_failures()

    print("S11B report-generator negative-control self-test report")
    print(f"positive_control_status: {positive_status}")
    print(f"negative_control_count: {len(results)}")
    for result in results:
        print(f"negative_id: {result['negative_id']}")
        print(f"description: {result['description']}")
        print(f"expected_failure_signal: {result['expected_failure_signal']}")
        print(f"observed_failure_signal: {result['observed_failure_signal']}")
        print(f"status: {result['status']}")
    if residue:
        print("repository_residue:")
        for item in residue:
            print(f"- {item}")
    success = positive_status == "pass" and len(results) == 16 and all(result["status"] == "pass" for result in results) and not residue
    print(f"status: {'pass' if success else 'fail'}")
    print("scope: temporary negative-control data only; no live user-local reads; no Pulse calls")
    print("scope: no PAI Memory writes; no ISA writes; evidence output is not PAI Memory, not ISA, not Pulse state")
    print("scope: evidence output is not Claude memory, not Codex memory, not a manifest, and not runtime payload")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
