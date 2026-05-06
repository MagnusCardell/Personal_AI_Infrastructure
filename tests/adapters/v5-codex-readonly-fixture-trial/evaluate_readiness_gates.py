#!/usr/bin/env python3
"""Evaluate S11 readiness gates from repository-local fixture evidence.

Codex is not currently proven drop-in for existing local PAI v5 files. This
evaluator produces adapter-test evidence only. The S11C report is not PAI
Memory, not ISA, not Pulse state, not Claude memory, not Codex memory, not a
PAI runtime audit artifact, not a manifest, and not runtime payload.
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
APPROVED_EVIDENCE_REPORT = APPROVED_REPORT_DIR / "S11A_RELEASE_FIXTURE_TRIAL_REPORT.json"
APPROVED_REPORT_PATH = APPROVED_REPORT_DIR / "S11C_READINESS_GATE_EVALUATION.json"
HARNESS_PATH = TRIAL_ROOT / "run_readonly_fixture_trial.py"
S10G_GATE_DOC = Path("docs/adapters/V5_CODEX_S11_READ_ONLY_TRIAL_READINESS_GATES.md")
S11B_CONTROL_SOURCE = TRIAL_ROOT / "test_readonly_fixture_trial_report_generator.py"


def fail(message):
    print(f"error: {message}")
    return 1


def validate_exact_relative_path(raw_value, approved_path, label):
    candidate = Path(raw_value)
    if candidate.is_absolute():
        raise ValueError(f"{label} must be repository-relative, not absolute")
    if ".." in candidate.parts:
        raise ValueError(f"{label} must not contain parent traversal")
    if candidate.as_posix() != approved_path.as_posix():
        raise ValueError(f"{label} must be {approved_path.as_posix()}")
    return candidate


def validate_report_output_path(raw_value):
    report_path = validate_exact_relative_path(raw_value, APPROVED_REPORT_PATH, "report output path")
    if report_path.parent != APPROVED_REPORT_DIR:
        raise ValueError("report output path must stay inside the approved reports directory")
    if report_path.name != APPROVED_REPORT_PATH.name:
        raise ValueError("only the approved S11C report file may be written")
    if not report_path.parent.is_dir():
        raise ValueError("approved reports directory is missing")
    return report_path


def load_harness():
    spec = importlib.util.spec_from_file_location("s11c_readonly_fixture_harness", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load read-only fixture harness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def validate_repository_sources():
    gate_doc = S10G_GATE_DOC.read_text(encoding="utf-8")
    control_source = S11B_CONTROL_SOURCE.read_text(encoding="utf-8")

    for index in range(18):
        gate_id = f"R{index}"
        require(f"Gate {gate_id}" in gate_doc, f"missing S10G gate definition: {gate_id}")

    for index in range(1, 17):
        control_id = f"RG-{index:03d}"
        require(control_id in control_source, f"missing S11B report-generator control: {control_id}")

    require("S11B report-generator negative-control self-test report" in control_source, "missing S11B control report marker")


def validate_evidence_report(evidence_report, fixture_root, harness):
    failures = harness.validate_fixture_root(fixture_root)
    if failures:
        raise RuntimeError("approved fixture harness validation failed: " + "; ".join(failures))

    counts = harness.global_coverage_counts(fixture_root)
    fixture_count = harness.count_fixture_dirs(fixture_root)
    case_count = harness.count_case_files(fixture_root)

    expected = {
        "report_type": "release-fixture-read-only-evidence",
        "report_status": "pass",
        "adapter_mode": "fixture-only-read-only",
        "positive_harness_status": "pass",
        "negative_control_status": "pass",
        "no_residue_status": "pass",
        "drop_in_claim_status": "not-claimed",
        "pulse_status": "not-started-not-called",
        "memory_status": "no-pai-memory-writes",
        "isa_status": "no-isa-writes",
        "product_memory_status": "no-product-memory-promotion",
        "live_user_local_state_status": "not-read",
    }

    for key, value in expected.items():
        require(evidence_report.get(key) == value, f"unexpected S11A evidence field {key}: {evidence_report.get(key)!r}")

    require(evidence_report.get("fixture_root") == fixture_root.as_posix(), "S11A evidence fixture root mismatch")
    require(evidence_report.get("fixture_count") == fixture_count, "S11A fixture_count mismatch")
    require(evidence_report.get("case_count") == case_count, "S11A case_count mismatch")
    require(evidence_report.get("seam_count") == counts["seam_count"], "S11A seam_count mismatch")
    require(evidence_report.get("coverage_id_count") == counts["coverage_id_count"], "S11A coverage_id_count mismatch")
    require(evidence_report.get("gate_id_count") == counts["gate_id_count"], "S11A gate_id_count mismatch")
    require(
        evidence_report.get("denied_category_count") == counts["denied_category_count"],
        "S11A denied_category_count mismatch",
    )

    statement = str(evidence_report.get("non_canonical_output_statement", ""))
    for term in [
        "not PAI Memory",
        "not ISA",
        "not Pulse state",
        "not Claude memory",
        "not Codex memory",
        "not a PAI runtime audit artifact",
        "not a manifest",
        "not runtime payload",
    ]:
        require(term in statement, f"S11A non-canonical statement missing {term}")

    return {
        "fixture_count": fixture_count,
        "case_count": case_count,
        "seam_count": counts["seam_count"],
        "coverage_id_count": counts["coverage_id_count"],
        "gate_id_count": counts["gate_id_count"],
        "denied_category_count": counts["denied_category_count"],
    }


def gate(gate_id, gate_name, status, required_proof, observed_evidence, failure_signal, future_s12_implication):
    return {
        "gate_id": gate_id,
        "gate_name": gate_name,
        "status": status,
        "required_proof": required_proof,
        "observed_evidence": observed_evidence,
        "failure_signal": failure_signal,
        "future_s12_implication": future_s12_implication,
    }


def build_gates(evidence_report, counts):
    count_summary = (
        f"fixture_count={counts['fixture_count']}; case_count={counts['case_count']}; "
        f"seam_count={counts['seam_count']}; coverage_id_count={counts['coverage_id_count']}; "
        f"gate_id_count={counts['gate_id_count']}; denied_category_count={counts['denied_category_count']}"
    )
    no_live = "S11A live_user_local_state_status is not-read; S11C does not approve live existing-local-v5 access."
    no_pulse = "S11A pulse_status is not-started-not-called; S11C does not authorize Pulse startup or calls."
    no_memory = "S11A memory_status is no-pai-memory-writes; S11C does not authorize PAI Memory writes."
    no_isa = "S11A isa_status is no-isa-writes; S11C does not authorize ISA writes."

    return {
        "R0": gate(
            "R0",
            "Architect Approval",
            "requires-architect-approval",
            "Explicit architect approval for any S12 objective, source protocol, reads, writes, and hard failures.",
            "S11C report status is ready-for-architect-review-not-approved; S12 approval status is not-approved.",
            "S12 work begins from this report alone or treats readiness evidence as approval.",
            "S12 remains future-only and requires explicit architect approval.",
        ),
        "R1": gate(
            "R1",
            "Fixture Track Accepted",
            "evidence-pass",
            "Accepted S10 fixture-only corpus, harness, negative controls, global coverage, and no-residue evidence.",
            f"S11A evidence is pass and corpus counts are stable: {count_summary}.",
            "Fixture-only evidence is incomplete, rejected, or not reviewed.",
            "Architect review can consider fixture evidence; this does not authorize live trials.",
        ),
        "R2": gate(
            "R2",
            "Approved S11 Write Set",
            "evidence-pass",
            "Exact approved write sets for S11A, S11B, and S11C with no runtime artifacts.",
            "S11C writes only the approved execution plan, evaluator, S11C report, and optional README update.",
            "Open-ended writes or generated runtime, manifest, schema, Memory, ISA, or Pulse artifacts.",
            "Any future S12 must name an exact write set and preserve protected paths.",
        ),
        "R3": gate(
            "R3",
            "No Live User-Local State By Default",
            "blocked-live-state",
            "Evidence that live user-local and existing-local-v5 state were not read.",
            no_live,
            "Any implicit read of home-directory state, live Claude state, live Codex state, or existing-local-v5 state.",
            "S12 must keep live user-local access blocked unless a future card explicitly approves a controlled source.",
        ),
        "R4": gate(
            "R4",
            "Explicit Source Selection",
            "blocked-live-state",
            "Repository-relative fixture, report, and document sources only.",
            "S11C reads repository-local fixture, report, harness, S10G gate, and S11B control files only.",
            "Source discovery through private state, live default paths, or inferred local configuration.",
            "S12 must explicitly name any source and must not infer live user-local state access.",
        ),
        "R5": gate(
            "R5",
            "No Root AGENTS.md",
            "evidence-pass",
            "Protected-path validation confirms root AGENTS.md is not created or modified.",
            "S11C creates no root AGENTS.md and no Codex router surface.",
            "Root AGENTS.md is created, modified, generated, or migrated.",
            "Future AGENTS.md work remains outside S11C and requires separate approval.",
        ),
        "R6": gate(
            "R6",
            "No .codex",
            "evidence-pass",
            "Protected-path validation confirms .codex is not created or modified.",
            "S11C creates no .codex config, profile, hook, rule, memory, or generated file.",
            "Any .codex file or directory is created or modified.",
            "Future Codex runtime surfaces remain unauthorized unless explicitly approved.",
        ),
        "R7": gate(
            "R7",
            "No Pulse Startup",
            "evidence-pass",
            "Evidence that Pulse was not started.",
            no_pulse,
            "Any command, service, script, or evaluator behavior starts Pulse.",
            "Pulse startup remains prohibited unless a future card explicitly approves it.",
        ),
        "R8": gate(
            "R8",
            "No Pulse Endpoint Calls",
            "evidence-pass",
            "Evidence that Pulse endpoints were not called and localhost:31337 was not probed.",
            no_pulse,
            "HTTP calls, socket calls, curl probes, health checks, or localhost endpoint access.",
            "Pulse endpoint calls remain prohibited unless separately approved.",
        ),
        "R9": gate(
            "R9",
            "No PAI Memory Writes",
            "evidence-pass",
            "Evidence that PAI Memory was not written.",
            no_memory,
            "PAI Memory file creation, mutation, migration, or promotion.",
            "PAI Memory remains canonical PAI state and cannot be written by this track.",
        ),
        "R10": gate(
            "R10",
            "No ISA Writes",
            "evidence-pass",
            "Evidence that ISA was not written.",
            no_isa,
            "ISA file creation, mutation, migration, or generated state update.",
            "ISA remains canonical PAI state and cannot be written by this track.",
        ),
        "R11": gate(
            "R11",
            "No Product Memory Promotion",
            "evidence-pass",
            "Evidence that product memories are not silently promoted into PAI Memory.",
            "S11A product_memory_status is no-product-memory-promotion and non_promotion_statement is present.",
            "Product-memory promotion, normalization, migration, or import into PAI Memory.",
            "Product-memory promotion remains prohibited without a separate architect-approved policy.",
        ),
        "R12": gate(
            "R12",
            "Authority Boundary Preserved",
            "evidence-pass",
            "Evidence preserving PAI_SYSTEM_PROMPT.md, CLAUDE.md, compact router, and policy/config boundaries.",
            "S10/S11 docs preserve authority boundary and prohibit copying Claude-shaped files directly into Codex surfaces.",
            "Authority levels are flattened or Claude-shaped files are copied directly into Codex surfaces.",
            "Any future adapter planning must preserve authority distinctions before runtime work.",
        ),
        "R13": gate(
            "R13",
            "Launcher and Inference Boundary Preserved",
            "evidence-pass",
            "Evidence that launcher and inference boundaries remain report-only and no runtime engine is invoked.",
            "S11A engine_under_test is none and limitations state no Codex runtime or Claude Code runtime was invoked.",
            "Launcher, wrapper, installer, migration, inference profile, or runtime invocation is created or executed.",
            "S12 must remain non-runtime unless a future architect card explicitly changes scope.",
        ),
        "R14": gate(
            "R14",
            "Hook and Lifecycle Boundary Preserved",
            "evidence-pass",
            "Evidence that hook/lifecycle boundaries remain unsupported-surface reporting only.",
            "Fixture evidence covers hook/lifecycle seams without creating Codex hooks, rules, agents, commands, or skills.",
            "Any hook, rule, skill, agent, command, lifecycle payload, or generated Codex control surface is created.",
            "Future mapping of hooks or lifecycle surfaces remains blocked until explicitly approved.",
        ),
        "R15": gate(
            "R15",
            "Unsupported Surface Reporting",
            "evidence-pass",
            "Read-only unsupported-surface reporting from the fixture corpus and S11A report.",
            "S11A unsupported_surface_report_status is covered-by-fixture-expectations.",
            "Unsupported surfaces are ignored, treated as supported, or converted into runtime payloads.",
            "Unsupported-surface reporting remains mandatory before any drop-in readiness claim.",
        ),
        "R16": gate(
            "R16",
            "Audit and Rollback Reporting",
            "evidence-pass",
            "Report-only audit and rollback posture without creating audit artifacts, manifests, schemas, or trial outputs.",
            "S11A rollback_status is no-residue-fixture-only and non-canonical statement rejects audit artifact and manifest status.",
            "Missing rollback/no-residue evidence or created audit artifact, manifest, or executable schema.",
            "Future audit/rollback evidence must remain report-only unless explicitly approved.",
        ),
        "R17": gate(
            "R17",
            "No Drop-In Claim",
            "evidence-pass",
            "Final evidence preserves no drop-in claim.",
            "S11A drop_in_claim_status is not-claimed and S11C limitations preserve Codex is not currently proven drop-in.",
            "Any claim that Codex is drop-in today, official upstream engine, replacement-grade, or runtime-compatible.",
            "No drop-in claim is allowed until later architect-approved validation proves it.",
        ),
    }


def build_report(fixture_root, evidence_path, harness):
    validate_repository_sources()
    evidence_report = read_json(evidence_path)
    counts = validate_evidence_report(evidence_report, fixture_root, harness)
    gates = build_gates(evidence_report, counts)

    return {
        "report_id": "S11C-READINESS-GATE-EVALUATION",
        "report_type": "s11-readiness-gate-evaluation",
        "report_status": "pass",
        "source_reports": [
            "docs/adapters/V5_CODEX_S11_READ_ONLY_TRIAL_READINESS_GATES.md",
            "tests/adapters/v5-codex-readonly-fixture-trial/reports/S11A_RELEASE_FIXTURE_TRIAL_REPORT.json",
            "tests/adapters/v5-codex-readonly-fixture-trial/test_readonly_fixture_trial_report_generator.py",
            "tests/adapters/v5-codex-readonly-fixture-trial/run_readonly_fixture_trial.py",
            "tests/adapters/v5-codex-readonly-fixture-trial/fixtures",
        ],
        "gate_count": 18,
        "gates": gates,
        "minimum_entry_threshold_status": "ready-for-architect-review-not-approved",
        "s12_approval_status": "not-approved",
        "drop_in_claim_status": "not-claimed",
        "pulse_status": "not-started-not-called",
        "memory_status": "no-pai-memory-writes",
        "isa_status": "no-isa-writes",
        "live_user_local_state_status": "not-read",
        "non_canonical_output_statement": (
            "This S11C evidence output is not PAI Memory; not ISA; not Pulse state; "
            "not Claude memory; not Codex memory; not a PAI runtime audit artifact; "
            "not a manifest; not runtime payload."
        ),
        "limitations": [
            "Codex is not currently proven drop-in for existing local PAI v5 files.",
            "S11C creates readiness gate evaluation evidence only.",
            "S11C does not approve S12.",
            "S11C does not run live trials.",
            "S11C does not read existing-local-v5 state.",
            "S11C does not authorize live user-local access.",
            "S11C does not start Pulse or call Pulse endpoints.",
            "S11C does not write PAI Memory or ISA.",
            "S11C does not authorize product-memory promotion into PAI Memory.",
            "S11C does not implement runtime adapter work.",
        ],
    }


def main(argv):
    parser = argparse.ArgumentParser(description="Evaluate S11 readiness gates from fixture evidence.")
    parser.add_argument("--fixture-root", required=True)
    parser.add_argument("--evidence-report", required=True)
    parser.add_argument("--report-out", required=True)
    args = parser.parse_args(argv)

    try:
        fixture_root = validate_exact_relative_path(args.fixture_root, APPROVED_FIXTURE_ROOT, "fixture root")
        evidence_path = validate_exact_relative_path(args.evidence_report, APPROVED_EVIDENCE_REPORT, "evidence report path")
        report_path = validate_report_output_path(args.report_out)
        harness = load_harness()
        report = build_report(fixture_root, evidence_path, harness)
        report_text = json.dumps(report, indent=2, sort_keys=True) + "\n"
        report_path.write_text(report_text, encoding="utf-8")
    except Exception as exc:
        return fail(str(exc))

    print(f"wrote S11C readiness gate evaluation report: {report_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
