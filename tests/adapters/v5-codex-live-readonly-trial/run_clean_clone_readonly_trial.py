#!/usr/bin/env python3
"""S13A clean-clone read-only trial runner."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


sys.dont_write_bytecode = True

CONSENT_STATUS = "approved-for-clean-clone-preflight-only"
SOURCE_KIND = "clean-clone-read-only"
SOURCE_ROOT = "."
CONSENT_SCOPE = "clean-clone repository-local read-only adapter-test preflight"

ALLOWED_READ_ROOTS = [
    "docs/adapters",
    "tests/adapters/v5-codex-readonly-fixture-trial",
    "Releases/v5.0.0",
]

FORBIDDEN_READ_ROOTS = [
    "~/.claude",
    "~/.claude/PAI",
    "~/.claude/projects",
    "~/.codex",
    "~/.codex/memories",
    "/home",
    "/Users",
]

FORBIDDEN_WRITE_ROOTS = [
    "Releases",
    ".claude",
    "PAI",
    "CLAUDE.md",
    "AGENTS.md",
    ".codex",
    "install.sh",
    "settings.json",
    "hooks",
    "skills",
    "subagents",
    "agents",
    "commands",
    ".github",
    ".agents",
    "PAI_SYSTEM_PROMPT.md",
]

RUNTIME_PROHIBITIONS = [
    "no_codex_runtime_invocation",
    "no_claude_code_invocation",
    "no_pulse_start",
    "no_pulse_endpoint_calls",
    "no_installers",
    "no_import_or_migration_tooling",
    "no_hook_rule_or_execpolicy_commands",
]

NON_CANONICAL_STATEMENT = (
    "This S13A adapter-test artifact is not PAI Memory, not ISA, not Pulse state, "
    "not Claude memory, not Codex memory, not a manifest, not runtime payload, "
    "and not proof that Codex is drop-in."
)

REQUIRED_EVIDENCE = [
    "docs/adapters/V5_CODEX_S12_READINESS_CLOSEOUT_REPORT.md",
    "docs/adapters/V5_CODEX_S13_LIVE_READ_ONLY_TRIAL_GATES.md",
    "docs/adapters/V5_CODEX_S13_PROPOSED_WRITE_SET_AND_COMPLETION_CONTRACT.md",
    "docs/adapters/V5_CODEX_S13_RISK_REGISTER.md",
    "docs/adapters/V5_CODEX_S12_TO_S13_DECISION_LOG.md",
    "tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py",
    "tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_harness.py",
    "tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_no_residue.py",
    "tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json",
    "tests/adapters/v5-codex-readonly-fixture-trial/reports/S11C_READINESS_GATE_EVALUATION.json",
    "tests/adapters/v5-codex-readonly-fixture-trial/fixtures",
    "Releases/v5.0.0/.claude/CLAUDE.md",
    "Releases/v5.0.0/.claude/PAI/PAI_SYSTEM_PROMPT.md",
]

EXPECTED_CONSENT_KEYS = {
    "consent_id",
    "consent_status",
    "consent_scope",
    "source_kind",
    "source_root",
    "allowed_read_roots",
    "forbidden_read_roots",
    "forbidden_write_roots",
    "runtime_prohibitions",
    "product_memory_policy",
    "pulse_policy",
    "memory_policy",
    "isa_policy",
    "reporting_policy",
    "retention_policy",
    "rollback_no_residue_policy",
    "drop_in_claim_policy",
    "non_canonical_statement",
    "limitations",
}

EXPECTED_POLICY_FIELDS = {
    "consent_scope": CONSENT_SCOPE,
    "reporting_policy": "non-canonical adapter-test evidence only",
    "retention_policy": "retain only as repository-local S13A adapter-test artifact in the approved write set",
    "rollback_no_residue_policy": "no writes outside approved S13A artifact paths; reports may be regenerated deterministically",
}


class TrialFailure(Exception):
    """Raised for fail-closed S13A trial validation errors."""


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise TrialFailure(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise TrialFailure(f"invalid JSON in {path}: {exc}") from exc


def _is_user_local_text(value: str) -> bool:
    return (
        value.startswith("~")
        or value == "/home"
        or value.startswith("/home/")
        or value == "/Users"
        or value.startswith("/Users/")
    )


def _assert_safe_relative_root(value: str, repo_root: Path, *, read_root: bool) -> Path:
    if not value:
        raise TrialFailure("empty path is not allowed")
    if _is_user_local_text(value):
        raise TrialFailure(f"user-local path is forbidden: {value}")

    path = Path(value)
    if path.is_absolute():
        resolved = path.resolve()
        if resolved == repo_root:
            return resolved
        raise TrialFailure(f"absolute path is forbidden: {value}")

    if ".." in path.parts:
        raise TrialFailure(f"parent traversal is forbidden: {value}")

    if read_root:
        forbidden_read_roots = {
            ".codex",
            ".claude",
            "PAI",
            "AGENTS.md",
            "CLAUDE.md",
            "install.sh",
            "settings.json",
            "hooks",
            "skills",
            "subagents",
            "agents",
            "commands",
            ".github",
            ".agents",
        }
        if value in forbidden_read_roots:
            raise TrialFailure(f"protected write surface cannot be a read root: {value}")
        if value == "Releases":
            raise TrialFailure("release root cannot be a broad read root")

    resolved = (repo_root / path).resolve()
    try:
        resolved.relative_to(repo_root)
    except ValueError as exc:
        raise TrialFailure(f"path escapes repository root: {value}") from exc
    return resolved


def _validate_consent(consent: dict, repo_root: Path) -> None:
    missing = sorted(EXPECTED_CONSENT_KEYS - set(consent))
    if missing:
        raise TrialFailure(f"consent missing fields: {missing}")

    checks = {
        **EXPECTED_POLICY_FIELDS,
        "consent_status": CONSENT_STATUS,
        "source_kind": SOURCE_KIND,
        "drop_in_claim_policy": "not-allowed",
        "product_memory_policy": "no-product-memory-read-or-promotion",
        "pulse_policy": "not-started-not-called",
        "memory_policy": "no-pai-memory-writes",
        "isa_policy": "no-isa-writes",
    }
    for key, expected in checks.items():
        if consent.get(key) != expected:
            raise TrialFailure(f"{key} mismatch: expected {expected!r}, got {consent.get(key)!r}")

    allowed_read_roots = consent.get("allowed_read_roots")
    if not isinstance(allowed_read_roots, list):
        raise TrialFailure("allowed_read_roots must be a list")

    for root in allowed_read_roots:
        resolved = _assert_safe_relative_root(root, repo_root, read_root=True)
        if not resolved.exists():
            raise TrialFailure(f"approved read root does not exist: {root}")

    if allowed_read_roots != ALLOWED_READ_ROOTS:
        raise TrialFailure("allowed_read_roots must match the approved S13A roots exactly")

    for required in FORBIDDEN_READ_ROOTS:
        if required not in consent.get("forbidden_read_roots", []):
            raise TrialFailure(f"missing forbidden read root: {required}")

    for required in FORBIDDEN_WRITE_ROOTS:
        if required not in consent.get("forbidden_write_roots", []):
            raise TrialFailure(f"missing forbidden write root: {required}")

    for required in RUNTIME_PROHIBITIONS:
        if required not in consent.get("runtime_prohibitions", []):
            raise TrialFailure(f"missing runtime prohibition: {required}")

    statement = consent.get("non_canonical_statement", "")
    for term in [
        "not PAI Memory",
        "not ISA",
        "not Pulse state",
        "not Claude memory",
        "not Codex memory",
        "not a manifest",
        "not runtime payload",
        "not proof that Codex is drop-in",
    ]:
        if term not in statement:
            raise TrialFailure(f"consent non-canonical statement missing: {term}")

    source_root = consent.get("source_root", "")
    source_root_path = Path(source_root)
    if source_root_path.is_absolute() and source_root_path.resolve() != repo_root:
        raise TrialFailure("absolute source_root is refused unless it is the normalized repository root")
    _assert_safe_relative_root(source_root, repo_root, read_root=False)
    if source_root != SOURCE_ROOT:
        raise TrialFailure(f"source_root mismatch: expected {SOURCE_ROOT!r}, got {source_root!r}")


def _validate_output_path(path: Path, expected: str, repo_root: Path) -> Path:
    if path.is_absolute():
        raise TrialFailure(f"absolute report path is forbidden: {path}")
    if ".." in path.parts:
        raise TrialFailure(f"parent traversal in report path is forbidden: {path}")
    if str(path) != expected:
        raise TrialFailure(f"report path must be {expected}, got {path}")
    resolved = (repo_root / path).resolve()
    try:
        resolved.relative_to(repo_root)
    except ValueError as exc:
        raise TrialFailure(f"report path escapes repository root: {path}") from exc
    if not resolved.parent.exists():
        raise TrialFailure(f"report directory does not exist: {resolved.parent}")
    return resolved


def _collect_evidence(repo_root: Path) -> tuple[list[dict], list[str]]:
    files_checked = []
    missing = []
    for item in REQUIRED_EVIDENCE:
        _assert_safe_relative_root(item, repo_root, read_root=False)
        path = repo_root / item
        exists = path.exists()
        files_checked.append({"path": item, "status": "present" if exists else "missing"})
        if not exists:
            missing.append(item)
    return files_checked, missing


def _base_status_fields() -> dict:
    return {
        "pulse_status": "not-started-not-called",
        "memory_status": "no-pai-memory-writes",
        "isa_status": "no-isa-writes",
        "product_memory_status": "no-product-memory-read-or-promotion",
        "runtime_invocation_status": "no-codex-or-claude-runtime-invocation",
        "drop_in_claim_status": "not-claimed",
    }


def _build_preflight(consent: dict, missing: list[str]) -> dict:
    report = {
        "abort_reasons": [],
        "abort_required": False,
        "allowed_read_roots": ALLOWED_READ_ROOTS,
        "consent_status": consent["consent_status"],
        "forbidden_read_roots": consent["forbidden_read_roots"],
        "forbidden_write_roots": consent["forbidden_write_roots"],
        "limitations": [
            "S13A is a clean-clone read-only trial only.",
            "S13A is not an existing-local-v5 trial.",
            "S13A is not a personal-clone trial.",
            "S13A does not inspect user-local state or arbitrary home directories.",
            "Codex is not currently proven drop-in for existing local PAI v5 files.",
        ],
        "non_canonical_statement": NON_CANONICAL_STATEMENT,
        "preflight_status": "pass-read-only-clean-clone",
        "protected_path_status": "no-protected-path-writes",
        "report_id": "S13A-PREFLIGHT-REPORT",
        "report_status": "pass",
        "report_type": "clean-clone-read-only-preflight",
        "source_kind": SOURCE_KIND,
        "source_root": SOURCE_ROOT,
        **_base_status_fields(),
    }
    if missing:
        report["abort_required"] = True
        report["abort_reasons"] = [f"missing required evidence: {item}" for item in missing]
        report["preflight_status"] = "abort-required"
        report["report_status"] = "fail"
    return report


def _build_evidence(files_checked: list[dict], missing: list[str]) -> dict:
    return {
        "files_checked": files_checked,
        "limitations": [
            "S13A validates clean-clone repository-local evidence only.",
            "S13A does not validate existing-local-v5 user state.",
            "S13A does not validate a personal clone.",
            "S13A does not validate Codex runtime adapter behavior.",
            "Codex is not currently proven drop-in for existing local PAI v5 files.",
        ],
        "missing_evidence": missing,
        "non_canonical_statement": NON_CANONICAL_STATEMENT,
        "personal_clone_access_status": "not-accessed",
        "protected_paths_modified": False,
        "release_files_modified": False,
        "report_id": "S13A-CLEAN-CLONE-READONLY-EVIDENCE",
        "report_status": "pass" if not missing else "fail",
        "report_type": "clean-clone-read-only-evidence",
        "required_evidence": REQUIRED_EVIDENCE,
        "source_kind": SOURCE_KIND,
        "source_root": SOURCE_ROOT,
        "user_local_access_status": "not-accessed",
        **_base_status_fields(),
    }


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the S13A clean-clone read-only trial.")
    parser.add_argument("--consent", required=True)
    parser.add_argument("--preflight-out", required=True)
    parser.add_argument("--evidence-out", required=True)
    args = parser.parse_args(argv)

    repo_root = Path.cwd().resolve()

    try:
        consent_path = _assert_safe_relative_root(args.consent, repo_root, read_root=False)
        expected_consent = "tests/adapters/v5-codex-live-readonly-trial/consent/S13A_CLEAN_CLONE_CONSENT.json"
        if str(Path(args.consent)) != expected_consent:
            raise TrialFailure(f"consent path must be {expected_consent}")

        preflight_out = _validate_output_path(
            Path(args.preflight_out),
            "tests/adapters/v5-codex-live-readonly-trial/reports/S13A_PREFLIGHT_REPORT.json",
            repo_root,
        )
        evidence_out = _validate_output_path(
            Path(args.evidence_out),
            "tests/adapters/v5-codex-live-readonly-trial/reports/S13A_CLEAN_CLONE_READONLY_EVIDENCE.json",
            repo_root,
        )

        consent = _load_json(consent_path)
        _validate_consent(consent, repo_root)
        files_checked, missing = _collect_evidence(repo_root)

        preflight = _build_preflight(consent, missing)
        evidence = _build_evidence(files_checked, missing)
        _write_json(preflight_out, preflight)
        _write_json(evidence_out, evidence)

        if missing:
            raise TrialFailure("missing required clean-clone evidence")

        generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        print("S13A clean-clone read-only trial")
        print(f"generated_at: {generated_at}")
        print("source_kind: clean-clone-read-only")
        print("preflight_status: pass-read-only-clean-clone")
        print("report_status: pass")
        print("user_local_access_status: not-accessed")
        print("personal_clone_access_status: not-accessed")
        print("pulse_status: not-started-not-called")
        print("memory_status: no-pai-memory-writes")
        print("isa_status: no-isa-writes")
        print("product_memory_status: no-product-memory-read-or-promotion")
        print("runtime_invocation_status: no-codex-or-claude-runtime-invocation")
        print("drop_in_claim_status: not-claimed")
        return 0
    except TrialFailure as exc:
        print(f"S13A clean-clone read-only trial failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
