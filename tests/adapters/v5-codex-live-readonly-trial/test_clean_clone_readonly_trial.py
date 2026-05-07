#!/usr/bin/env python3
"""S13B negative controls for the clean-clone read-only trial runner."""

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path


sys.dont_write_bytecode = True

REPO_ROOT = Path.cwd().resolve()
TRIAL_ROOT = Path("tests/adapters/v5-codex-live-readonly-trial")
CONSENT_PATH = TRIAL_ROOT / "consent/S13A_CLEAN_CLONE_CONSENT.json"
PREFLIGHT_OUT = TRIAL_ROOT / "reports/S13A_PREFLIGHT_REPORT.json"
EVIDENCE_OUT = TRIAL_ROOT / "reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json"
RUNNER_PATH = TRIAL_ROOT / "run_clean_clone_readonly_trial.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location("s13a_clean_clone_runner", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not import runner from {RUNNER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


runner = _load_runner()
BASE_CONSENT = json.loads(CONSENT_PATH.read_text(encoding="utf-8"))


def _copy_consent() -> dict:
    return json.loads(json.dumps(BASE_CONSENT))


def _invoke_main(args: list[str]) -> tuple[int, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        rc = runner.main(args)
    return rc, stdout.getvalue() + stderr.getvalue()


def _run_positive_control() -> str:
    rc, output = _invoke_main(
        [
            "--consent",
            str(CONSENT_PATH),
            "--preflight-out",
            str(PREFLIGHT_OUT),
            "--evidence-out",
            str(EVIDENCE_OUT),
        ]
    )
    if rc != 0:
        raise RuntimeError(output.strip() or "positive control failed without output")
    return output


def _expect_trial_failure(case: dict, temp_root: Path) -> dict:
    try:
        case["action"](temp_root)
    except runner.TrialFailure as exc:
        observed = str(exc)
        status = "pass" if case["expected_failure_signal"] in observed else "fail"
    except Exception as exc:  # noqa: BLE001 - report unexpected self-test failures plainly.
        observed = f"unexpected {type(exc).__name__}: {exc}"
        status = "fail"
    else:
        observed = "no failure"
        status = "fail"

    return {
        "negative_id": case["negative_id"],
        "description": case["description"],
        "expected_failure_signal": case["expected_failure_signal"],
        "observed_failure_signal": observed,
        "status": status,
    }


def _validate_consent_case(mutator):
    def action(_temp_root: Path) -> None:
        consent = _copy_consent()
        mutator(consent)
        runner._validate_consent(consent, REPO_ROOT)

    return action


def _remove_list_item(field: str, value: str):
    def mutator(consent: dict) -> None:
        consent[field] = [item for item in consent[field] if item != value]

    return mutator


def _set_field(field: str, value):
    def mutator(consent: dict) -> None:
        consent[field] = value

    return mutator


def _missing_consent_action(temp_root: Path) -> None:
    runner._load_json(temp_root / "missing-consent.json")


def _invalid_json_action(temp_root: Path) -> None:
    path = temp_root / "invalid-consent.json"
    path.write_text("{not valid json", encoding="utf-8")
    runner._load_json(path)


def _missing_field_action(_temp_root: Path) -> None:
    consent = _copy_consent()
    del consent["consent_status"]
    runner._validate_consent(consent, REPO_ROOT)


def _main_failure_action(*, preflight_out: str, evidence_out: str):
    def action(_temp_root: Path) -> None:
        rc, output = _invoke_main(
            [
                "--consent",
                str(CONSENT_PATH),
                "--preflight-out",
                preflight_out,
                "--evidence-out",
                evidence_out,
            ]
        )
        if rc == 0:
            raise RuntimeError("runner unexpectedly passed")
        raise runner.TrialFailure(output.strip())

    return action


def _missing_evidence_action(_temp_root: Path) -> None:
    original = runner.REQUIRED_EVIDENCE
    try:
        runner.REQUIRED_EVIDENCE = ["docs/adapters/S13B_MISSING_REQUIRED_EVIDENCE.md"]
        _files_checked, missing = runner._collect_evidence(REPO_ROOT)
        if not missing:
            raise RuntimeError("missing evidence was not detected")
        raise runner.TrialFailure("missing required clean-clone evidence")
    finally:
        runner.REQUIRED_EVIDENCE = original


NEGATIVE_CASES = [
    {
        "negative_id": "S13B-NC-001",
        "description": "Missing consent artifact is detected.",
        "expected_failure_signal": "missing JSON file",
        "action": _missing_consent_action,
    },
    {
        "negative_id": "S13B-NC-002",
        "description": "Invalid consent JSON is detected.",
        "expected_failure_signal": "invalid JSON",
        "action": _invalid_json_action,
    },
    {
        "negative_id": "S13B-NC-003",
        "description": "Missing required consent field is detected.",
        "expected_failure_signal": "consent missing fields",
        "action": _missing_field_action,
    },
    {
        "negative_id": "S13B-NC-004",
        "description": "Invalid consent_status is detected.",
        "expected_failure_signal": "consent_status mismatch",
        "action": _validate_consent_case(_set_field("consent_status", "approved-for-live-use")),
    },
    {
        "negative_id": "S13B-NC-005",
        "description": "Invalid source_kind is detected.",
        "expected_failure_signal": "source_kind mismatch",
        "action": _validate_consent_case(_set_field("source_kind", "existing-local-v5")),
    },
    {
        "negative_id": "S13B-NC-006",
        "description": "Invalid source_root is detected.",
        "expected_failure_signal": "source_root mismatch",
        "action": _validate_consent_case(_set_field("source_root", "docs/adapters")),
    },
    {
        "negative_id": "S13B-NC-007",
        "description": "Absolute source root is rejected.",
        "expected_failure_signal": "absolute source_root is refused",
        "action": _validate_consent_case(_set_field("source_root", "/tmp/s13b-clean-clone")),
    },
    {
        "negative_id": "S13B-NC-008",
        "description": "Parent traversal source root is rejected.",
        "expected_failure_signal": "parent traversal is forbidden",
        "action": _validate_consent_case(_set_field("source_root", "../outside-repository")),
    },
    {
        "negative_id": "S13B-NC-009",
        "description": "Allowed read root pointing at ~/.claude is rejected.",
        "expected_failure_signal": "user-local path is forbidden",
        "action": _validate_consent_case(_set_field("allowed_read_roots", ["~/.claude"])),
    },
    {
        "negative_id": "S13B-NC-010",
        "description": "Allowed read root pointing at ~/.codex is rejected.",
        "expected_failure_signal": "user-local path is forbidden",
        "action": _validate_consent_case(_set_field("allowed_read_roots", ["~/.codex"])),
    },
    {
        "negative_id": "S13B-NC-011",
        "description": "Allowed read root pointing at /home or /Users is rejected.",
        "expected_failure_signal": "user-local path is forbidden",
        "action": _validate_consent_case(_set_field("allowed_read_roots", ["/home"])),
    },
    {
        "negative_id": "S13B-NC-012",
        "description": "Allowed read root pointing at root AGENTS.md is rejected.",
        "expected_failure_signal": "protected write surface cannot be a read root",
        "action": _validate_consent_case(_set_field("allowed_read_roots", ["AGENTS.md"])),
    },
    {
        "negative_id": "S13B-NC-013",
        "description": "Allowed read root pointing at .codex is rejected.",
        "expected_failure_signal": "protected write surface cannot be a read root",
        "action": _validate_consent_case(_set_field("allowed_read_roots", [".codex"])),
    },
    {
        "negative_id": "S13B-NC-014",
        "description": "Missing forbidden read root for ~/.claude/PAI is detected.",
        "expected_failure_signal": "missing forbidden read root: ~/.claude/PAI",
        "action": _validate_consent_case(_remove_list_item("forbidden_read_roots", "~/.claude/PAI")),
    },
    {
        "negative_id": "S13B-NC-015",
        "description": "Missing forbidden write root for root AGENTS.md is detected.",
        "expected_failure_signal": "missing forbidden write root: AGENTS.md",
        "action": _validate_consent_case(_remove_list_item("forbidden_write_roots", "AGENTS.md")),
    },
    {
        "negative_id": "S13B-NC-016",
        "description": "Missing forbidden write root for .codex is detected.",
        "expected_failure_signal": "missing forbidden write root: .codex",
        "action": _validate_consent_case(_remove_list_item("forbidden_write_roots", ".codex")),
    },
    {
        "negative_id": "S13B-NC-017",
        "description": "Missing no_codex_runtime_invocation prohibition is detected.",
        "expected_failure_signal": "missing runtime prohibition: no_codex_runtime_invocation",
        "action": _validate_consent_case(
            _remove_list_item("runtime_prohibitions", "no_codex_runtime_invocation")
        ),
    },
    {
        "negative_id": "S13B-NC-018",
        "description": "Missing no_claude_code_invocation prohibition is detected.",
        "expected_failure_signal": "missing runtime prohibition: no_claude_code_invocation",
        "action": _validate_consent_case(
            _remove_list_item("runtime_prohibitions", "no_claude_code_invocation")
        ),
    },
    {
        "negative_id": "S13B-NC-019",
        "description": "Missing no_pulse_start prohibition is detected.",
        "expected_failure_signal": "missing runtime prohibition: no_pulse_start",
        "action": _validate_consent_case(_remove_list_item("runtime_prohibitions", "no_pulse_start")),
    },
    {
        "negative_id": "S13B-NC-020",
        "description": "Missing no_pulse_endpoint_calls prohibition is detected.",
        "expected_failure_signal": "missing runtime prohibition: no_pulse_endpoint_calls",
        "action": _validate_consent_case(
            _remove_list_item("runtime_prohibitions", "no_pulse_endpoint_calls")
        ),
    },
    {
        "negative_id": "S13B-NC-021",
        "description": "Consent policy allowing PAI Memory writes is rejected.",
        "expected_failure_signal": "memory_policy mismatch",
        "action": _validate_consent_case(_set_field("memory_policy", "pai-memory-writes-allowed")),
    },
    {
        "negative_id": "S13B-NC-022",
        "description": "Consent policy allowing ISA writes is rejected.",
        "expected_failure_signal": "isa_policy mismatch",
        "action": _validate_consent_case(_set_field("isa_policy", "isa-writes-allowed")),
    },
    {
        "negative_id": "S13B-NC-023",
        "description": "Consent policy allowing product-memory read or promotion is rejected.",
        "expected_failure_signal": "product_memory_policy mismatch",
        "action": _validate_consent_case(
            _set_field("product_memory_policy", "product-memory-read-and-promotion-allowed")
        ),
    },
    {
        "negative_id": "S13B-NC-024",
        "description": "Consent policy allowing drop-in claim is rejected.",
        "expected_failure_signal": "drop_in_claim_policy mismatch",
        "action": _validate_consent_case(_set_field("drop_in_claim_policy", "allowed")),
    },
    {
        "negative_id": "S13B-NC-025",
        "description": "Consent non-canonical statement missing not PAI Memory is rejected.",
        "expected_failure_signal": "consent non-canonical statement missing: not PAI Memory",
        "action": _validate_consent_case(
            _set_field(
                "non_canonical_statement",
                "This artifact is not ISA, not Pulse state, not Claude memory, not Codex memory, "
                "not a manifest, not runtime payload, and not proof that Codex is drop-in.",
            )
        ),
    },
    {
        "negative_id": "S13B-NC-026",
        "description": "Consent non-canonical statement missing not proof that Codex is drop-in is rejected.",
        "expected_failure_signal": "consent non-canonical statement missing: not proof that Codex is drop-in",
        "action": _validate_consent_case(
            _set_field(
                "non_canonical_statement",
                "This artifact is not PAI Memory, not ISA, not Pulse state, not Claude memory, "
                "not Codex memory, not a manifest, and not runtime payload.",
            )
        ),
    },
    {
        "negative_id": "S13B-NC-027",
        "description": "Absolute preflight output path is rejected.",
        "expected_failure_signal": "absolute report path is forbidden",
        "action": _main_failure_action(
            preflight_out="/tmp/S13A_PREFLIGHT_REPORT.json",
            evidence_out=str(EVIDENCE_OUT),
        ),
    },
    {
        "negative_id": "S13B-NC-028",
        "description": "Parent traversal preflight output path is rejected.",
        "expected_failure_signal": "parent traversal in report path is forbidden",
        "action": _main_failure_action(
            preflight_out="../S13A_PREFLIGHT_REPORT.json",
            evidence_out=str(EVIDENCE_OUT),
        ),
    },
    {
        "negative_id": "S13B-NC-029",
        "description": "Preflight output outside S13A reports directory is rejected.",
        "expected_failure_signal": "report path must be",
        "action": _main_failure_action(
            preflight_out="tests/adapters/v5-codex-live-readonly-trial/S13A_PREFLIGHT_REPORT.json",
            evidence_out=str(EVIDENCE_OUT),
        ),
    },
    {
        "negative_id": "S13B-NC-030",
        "description": "Evidence output outside S13A reports directory is rejected.",
        "expected_failure_signal": "report path must be",
        "action": _main_failure_action(
            preflight_out=str(PREFLIGHT_OUT),
            evidence_out="tests/adapters/v5-codex-live-readonly-trial/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json",
        ),
    },
    {
        "negative_id": "S13B-NC-031",
        "description": "Preflight and evidence output paths colliding are rejected.",
        "expected_failure_signal": "report path must be",
        "action": _main_failure_action(
            preflight_out=str(PREFLIGHT_OUT),
            evidence_out=str(PREFLIGHT_OUT),
        ),
    },
    {
        "negative_id": "S13B-NC-032",
        "description": "Missing required clean-clone evidence source is detected.",
        "expected_failure_signal": "missing required clean-clone evidence",
        "action": _missing_evidence_action,
    },
    {
        "negative_id": "S13B-NC-033",
        "description": "Personal-clone-like source path is rejected.",
        "expected_failure_signal": "parent traversal is forbidden",
        "action": _validate_consent_case(
            _set_field("source_root", "../Personal_AI_Infrastructure_personal_clone")
        ),
    },
    {
        "negative_id": "S13B-NC-034",
        "description": "Runtime invocation pressure is rejected.",
        "expected_failure_signal": "consent_scope mismatch",
        "action": _validate_consent_case(
            _set_field(
                "consent_scope",
                "clean-clone repository-local read-only adapter-test preflight with runtime invocation",
            )
        ),
    },
    {
        "negative_id": "S13B-NC-035",
        "description": "Pulse endpoint-call pressure is rejected.",
        "expected_failure_signal": "pulse_policy mismatch",
        "action": _validate_consent_case(_set_field("pulse_policy", "pulse-endpoint-calls-allowed")),
    },
    {
        "negative_id": "S13B-NC-036",
        "description": "Report attempting to become canonical state is rejected or impossible by construction.",
        "expected_failure_signal": "reporting_policy mismatch",
        "action": _validate_consent_case(_set_field("reporting_policy", "canonical PAI Memory state")),
    },
]


def main() -> int:
    failures = []
    positive_status = "fail"

    try:
        _run_positive_control()
        positive_status = "pass"
    except Exception as exc:  # noqa: BLE001 - self-test should report any unexpected positive failure.
        failures.append(f"positive control failed: {type(exc).__name__}: {exc}")

    results = []
    with tempfile.TemporaryDirectory(prefix="s13b-clean-clone-negative-") as temp_name:
        temp_root = Path(temp_name)
        for case in NEGATIVE_CASES:
            result = _expect_trial_failure(case, temp_root)
            results.append(result)
            if result["status"] != "pass":
                failures.append(f"{result['negative_id']}: {result['observed_failure_signal']}")

    print("S13B clean-clone negative-control self-test report")
    print(f"positive_control_status: {positive_status}")
    print(f"negative_control_count: {len(results)}")
    for result in results:
        print(f"negative_id: {result['negative_id']}")
        print(f"description: {result['description']}")
        print(f"expected_failure_signal: {result['expected_failure_signal']}")
        print(f"observed_failure_signal: {result['observed_failure_signal']}")
        print(f"status: {result['status']}")
    print("scope: negative-control data is temporary only; no committed negative fixtures")
    print("scope: no live user-local reads; no personal-clone access; no Pulse calls")
    print("scope: no PAI Memory writes; no ISA writes; no product-memory read or promotion")
    print("scope: S13B does not prove Codex is drop-in")
    print(f"status: {'pass' if positive_status == 'pass' and not failures and len(results) == 36 else 'fail'}")

    if positive_status != "pass" or failures or len(results) != 36:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
