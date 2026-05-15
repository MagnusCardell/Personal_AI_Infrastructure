from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.pai_runtime_runner.beta_readiness import (
    ACCEPTED_S15_COMMITS,
    PAI_DIR_LABEL,
    REQUIRED_RESULT_VALUES,
    REQUIRED_VALIDATION_VALUES,
    S15J_MILESTONE,
    S15J_RUN_ID,
    validate_beta_readiness_result,
    validate_beta_readiness_validation,
    validate_evidence_index,
)


def _sample_result() -> dict[str, object]:
    return {
        **REQUIRED_RESULT_VALUES,
        "evidence_classification": [
            "S15 executable closeout evidence",
            "Codex peer-beta runtime provider evidence",
            "not replacement readiness",
        ],
        "known_limits": [
            "S15J is a closeout gate and does not add Memory, ISA, or Pulse authority.",
        ],
    }


def _sample_validation() -> dict[str, object]:
    return {
        **REQUIRED_VALIDATION_VALUES,
        "runtime_attempt_number": 1,
        "pai_runtime_command": [
            f"{PAI_DIR_LABEL}/bin/pai-runtime",
            "beta-readiness",
            "--pai-dir",
            PAI_DIR_LABEL,
            "--runtime",
            "codex",
            "--run-dir",
            f"{PAI_DIR_LABEL}/runs/s15j/codex-beta-readiness",
        ],
        "provider_commands_run": [
            f"{PAI_DIR_LABEL}/bin/pai-runtime providers list --pai-dir {PAI_DIR_LABEL}",
            f"{PAI_DIR_LABEL}/bin/pai-runtime providers status codex --pai-dir {PAI_DIR_LABEL}",
            f"{PAI_DIR_LABEL}/bin/pai-runtime providers doctor codex --pai-dir {PAI_DIR_LABEL}",
            f"{PAI_DIR_LABEL}/bin/pai-runtime providers validate codex --pai-dir {PAI_DIR_LABEL}",
        ],
        "evidence_artifacts_checked": [],
        "evidence_artifacts_missing": [],
        "evidence_artifacts_regenerated": [],
        "approved_pai_run_writes": [
            f"{PAI_DIR_LABEL}/runs/s15j/codex-beta-readiness/beta-readiness-result.json",
            f"{PAI_DIR_LABEL}/runs/s15j/codex-beta-readiness/beta-readiness-events.jsonl",
            f"{PAI_DIR_LABEL}/runs/s15j/codex-beta-readiness/beta-readiness-validation.json",
            f"{PAI_DIR_LABEL}/runs/s15j/codex-beta-readiness/evidence-index.json",
        ],
        "ambient_pai_state_churn": [],
        "forbidden_semantic_writes": [],
        "unknown_unclassified_writes": [],
        "known_limits": [
            "S15J validates peer-beta readiness only; it is not replacement readiness.",
        ],
    }


def _sample_evidence_index() -> dict[str, object]:
    return {
        "milestone_name": S15J_MILESTONE,
        "run_id": S15J_RUN_ID,
        "accepted_commits": list(ACCEPTED_S15_COMMITS),
        "live_artifacts_checked": [],
        "live_artifacts_regenerated": [],
        "runtime_provider_status": {
            "runtime_name": "codex",
            "runtime_status": "peer-beta",
            "provider_type": "codex-cli",
            "upstream_adapter": "claude",
            "supports_codex_exec": True,
            "supports_jsonl_events": True,
            "supports_structured_output": True,
            "memory_write_policy": "disabled",
            "isa_write_policy": "disabled",
            "pulse_policy": "no-probe",
            "replacement_status": "not-replacement-grade",
        },
        "capability_summary": {
            "provider_capabilities": [
                "repo.read",
                "repo.write.proposal",
                "repo.write.apply",
                "pai.context.read.metadata",
                "memory.write.disabled",
                "isa.write.disabled",
                "pulse.no-probe",
            ],
            "required_peer_beta_capabilities": [],
            "forbidden_capabilities": ["memory.write", "isa.write", "pulse.probe"],
        },
        "protected_surface_summary": {
            "repo_root_agents_created": False,
            "repo_dotcodex_created": False,
            "codex_adapter_files_installed_under_home_codex": False,
        },
        "s15_closeout_summary": [
            "Codex is peer beta.",
            "Claude remains official/full-support upstream.",
            "Codex replacement readiness is not claimed.",
            "Claude equivalence is not claimed.",
        ],
        "recommended_s16_direction": "controlled real PAI-context task execution with proposal-only Memory/ISA semantics",
    }


def _load_schema(name: str) -> dict[str, object]:
    schema = json.loads(Path("pai-runtime", name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


class PaiRuntimeBetaReadinessTests(unittest.TestCase):
    def test_beta_readiness_result_schema_accepts_required_shape(self):
        schema = _load_schema("beta-readiness-result.schema.json")
        Draft202012Validator(schema).validate(_sample_result())
        self.assertEqual(validate_beta_readiness_result(_sample_result()), [])

    def test_beta_readiness_validation_schema_accepts_required_shape(self):
        schema = _load_schema("beta-readiness-validation.schema.json")
        Draft202012Validator(schema).validate(_sample_validation())
        self.assertEqual(validate_beta_readiness_validation(_sample_validation()), [])

    def test_evidence_index_schema_accepts_required_shape(self):
        schema = _load_schema("evidence-index.schema.json")
        index = _sample_evidence_index()
        Draft202012Validator(schema).validate(index)
        self.assertEqual(validate_evidence_index(index), [])

    def test_beta_readiness_gate_requires_codex_peer_beta(self):
        result = _sample_result()
        result["runtime_status"] = "full-support"
        self.assertIn("beta-readiness result mismatch for runtime_status", validate_beta_readiness_result(result))

    def test_beta_readiness_gate_rejects_replacement_status(self):
        result = _sample_result()
        result["replacement_readiness_claimed"] = True
        self.assertIn(
            "beta-readiness result mismatch for replacement_readiness_claimed",
            validate_beta_readiness_result(result),
        )

    def test_beta_readiness_gate_rejects_claude_equivalence_claim(self):
        result = _sample_result()
        result["claude_equivalence_claimed"] = True
        self.assertIn(
            "beta-readiness result mismatch for claude_equivalence_claimed",
            validate_beta_readiness_result(result),
        )

    def test_beta_readiness_gate_requires_provider_lifecycle_pass(self):
        result = _sample_result()
        result["provider_lifecycle_passed"] = False
        self.assertIn(
            "beta-readiness result mismatch for provider_lifecycle_passed",
            validate_beta_readiness_result(result),
        )

    def test_beta_readiness_gate_requires_capability_policy_pass(self):
        result = _sample_result()
        result["capability_policy_passed"] = False
        self.assertIn(
            "beta-readiness result mismatch for capability_policy_passed",
            validate_beta_readiness_result(result),
        )

    def test_beta_readiness_gate_requires_patch_proposal_policy_pass(self):
        result = _sample_result()
        result["patch_proposal_policy_passed"] = False
        self.assertIn(
            "beta-readiness result mismatch for patch_proposal_policy_passed",
            validate_beta_readiness_result(result),
        )

    def test_beta_readiness_gate_requires_readonly_pai_context_policy_pass(self):
        result = _sample_result()
        result["readonly_pai_context_policy_passed"] = False
        self.assertIn(
            "beta-readiness result mismatch for readonly_pai_context_policy_passed",
            validate_beta_readiness_result(result),
        )

    def test_beta_readiness_gate_rejects_memory_write(self):
        result = _sample_result()
        result["memory_write_performed"] = True
        self.assertIn("beta-readiness result mismatch for memory_write_performed", validate_beta_readiness_result(result))

    def test_beta_readiness_gate_rejects_isa_write(self):
        result = _sample_result()
        result["isa_write_performed"] = True
        self.assertIn("beta-readiness result mismatch for isa_write_performed", validate_beta_readiness_result(result))

    def test_beta_readiness_gate_rejects_memory_body_read(self):
        result = _sample_result()
        result["memory_body_read"] = True
        self.assertIn("beta-readiness result mismatch for memory_body_read", validate_beta_readiness_result(result))

    def test_beta_readiness_gate_rejects_isa_body_read(self):
        result = _sample_result()
        result["isa_body_read"] = True
        self.assertIn("beta-readiness result mismatch for isa_body_read", validate_beta_readiness_result(result))

    def test_beta_readiness_gate_rejects_pulse_payload_read(self):
        result = _sample_result()
        result["pulse_event_payload_read"] = True
        self.assertIn(
            "beta-readiness result mismatch for pulse_event_payload_read",
            validate_beta_readiness_result(result),
        )

    def test_beta_readiness_gate_rejects_pulse_probe(self):
        result = _sample_result()
        result["pulse_probe_performed"] = True
        self.assertIn("beta-readiness result mismatch for pulse_probe_performed", validate_beta_readiness_result(result))

    def test_beta_readiness_gate_rejects_root_agents(self):
        result = _sample_result()
        result["repo_root_agents_created"] = True
        self.assertIn("beta-readiness result mismatch for repo_root_agents_created", validate_beta_readiness_result(result))

    def test_beta_readiness_gate_rejects_dotcodex(self):
        result = _sample_result()
        result["repo_dotcodex_created"] = True
        self.assertIn("beta-readiness result mismatch for repo_dotcodex_created", validate_beta_readiness_result(result))

    def test_beta_readiness_gate_rejects_home_codex_adapter_install(self):
        result = _sample_result()
        result["codex_adapter_files_installed_under_home_codex"] = True
        self.assertIn(
            "beta-readiness result mismatch for codex_adapter_files_installed_under_home_codex",
            validate_beta_readiness_result(result),
        )


if __name__ == "__main__":
    unittest.main()
