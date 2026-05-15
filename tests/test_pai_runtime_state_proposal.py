from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.pai_runtime_runner.capabilities import (
    CODEX_PROVIDER_CAPABILITIES,
    CODEX_S16A_PROVIDER_CAPABILITIES,
    STATE_PROPOSAL_TASK_CAPABILITIES,
    validate_capability_policy,
)
from tools.pai_runtime_runner.state_proposal import (
    PAI_DIR_LABEL,
    S16A_MILESTONE,
    S16A_RUN_ID,
    S16A_TASK_ID,
    S16A_TASK_KIND,
    STATE_CONTEXT_CAPSULE_NAME,
    STATE_PROPOSAL_EVENTS_NAME,
    STATE_PROPOSAL_NAME,
    STATE_PROPOSAL_STATE_NAME,
    audit_state_proposal_run,
    validate_state_proposal,
)


def _proposal() -> dict[str, object]:
    return {
        "milestone_name": S16A_MILESTONE,
        "run_id": S16A_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "pai_dir_label": PAI_DIR_LABEL,
        "task_id": S16A_TASK_ID,
        "task_kind": S16A_TASK_KIND,
        "adapter_identity_marker": "PAI_CODEX_PEER_BETA_ADAPTER",
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": True,
        "memory_proposals": [
            {
                "category": "WORK",
                "title": "Track proposal-only runtime state follow-up",
                "rationale": "The capsule shows a peer-beta runtime can produce bounded proposals.",
                "source_context": "sanitized metadata capsule",
                "proposed_body": "Proposal-only note; not applied to Memory in S16A.",
                "confidence": 0.8,
                "apply_status": "proposed_only",
            }
        ],
        "isa_proposals": [
            {
                "proposal_type": "work_record",
                "title": "Record proposal-only state task",
                "rationale": "The capsule supports documenting proposal-only semantics.",
                "proposed_record": "S16A proposal-only state update record.",
                "source_context": "sanitized metadata capsule",
                "confidence": 0.75,
                "apply_status": "proposed_only",
            }
        ],
        "proposal_only": True,
        "memory_write_performed": False,
        "isa_write_performed": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
        "evidence_classification": ["proposal-only Memory/ISA semantics"],
        "known_limits": ["S16A does not apply Memory or ISA writes."],
    }


def _capsule() -> dict[str, object]:
    return {
        "milestone_name": S16A_MILESTONE,
        "run_id": S16A_RUN_ID,
        "task_id": S16A_TASK_ID,
        "task_kind": S16A_TASK_KIND,
        "pai_dir_label": PAI_DIR_LABEL,
        "metadata_only": True,
        "redacted_paths": True,
        "runtime_providers": [],
        "runtime_provider_names": ["codex"],
        "runtime_provider_count": 1,
        "memory_categories": [],
        "isa": {"present": False, "body_read": False},
        "pulse": {"present": False, "body_read": False},
        "forbidden_body_reads": {
            "memory_body_read": False,
            "isa_body_read": False,
            "pulse_event_payload_read": False,
            "claude_project_memory_read": False,
            "codex_memory_read": False,
        },
        "proposal_policy": [
            "Codex may propose Memory updates but S16A does not write Memory.",
        ],
    }


def _validation() -> dict[str, object]:
    return {
        "milestone_name": S16A_MILESTONE,
        "run_id": S16A_RUN_ID,
        "runtime": "codex",
        "runtime_attempt_number": 1,
        "pai_runtime_command": [
            f"{PAI_DIR_LABEL}/bin/pai-runtime",
            "propose-state",
            "--runtime",
            "codex",
        ],
        "provider_command": ["codex", "exec", "[sanitized-state-proposal-prompt]"],
        "state_context_capsule_present": True,
        "state_context_capsule_metadata_only": True,
        "state_proposal_present": True,
        "state_proposal_schema_valid": True,
        "state_proposal_semantically_valid": True,
        "all_memory_proposals_proposed_only": True,
        "all_isa_proposals_proposed_only": True,
        "memory_files_modified": False,
        "isa_files_modified": False,
        "pulse_files_modified": False,
        "event_logs_present": True,
        "event_attribution_passed": True,
        "codex_file_change_events": [],
        "codex_command_execution_events": [],
        "approved_pai_run_writes": [],
        "ambient_pai_state_churn": [],
        "forbidden_semantic_writes": [],
        "unknown_unclassified_writes": [],
        "memory_body_read_by_codex": False,
        "isa_body_read_by_codex": False,
        "pulse_event_payload_read_by_codex": False,
        "memory_write_performed_by_codex": False,
        "isa_write_performed_by_codex": False,
        "pulse_probe_performed_by_codex": False,
        "localhost_31337_called_by_codex": False,
        "repo_root_agents_created": False,
        "repo_dotcodex_created": False,
        "codex_adapter_files_installed_under_home_codex": False,
        "validation_passed": True,
        "known_limits": ["S16A proposal-only validation."],
    }


def _schema(name: str) -> dict[str, object]:
    schema = json.loads(Path("pai-runtime", name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


class PaiRuntimeStateProposalTests(unittest.TestCase):
    def _write_clean_run(self, tmp: str) -> tuple[Path, Path, Path]:
        pai_dir = Path(tmp) / "home" / ".claude" / "PAI"
        run_dir = pai_dir / "runs" / "s16a" / "state-proposal"
        (pai_dir / "runtime-schemas").mkdir(parents=True)
        run_dir.mkdir(parents=True)
        marker = Path(tmp) / "marker"
        marker.write_text("marker\n", encoding="utf-8")
        (pai_dir / "runtime-schemas" / "state-proposal.schema.json").write_text(
            Path("pai-runtime/state-proposal.schema.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (run_dir / STATE_CONTEXT_CAPSULE_NAME).write_text(json.dumps(_capsule()) + "\n", encoding="utf-8")
        (run_dir / STATE_PROPOSAL_NAME).write_text(json.dumps(_proposal()) + "\n", encoding="utf-8")
        (run_dir / STATE_PROPOSAL_EVENTS_NAME).write_text(
            json.dumps({"type": "message", "message": "proposal emitted"}) + "\n",
            encoding="utf-8",
        )
        (run_dir / STATE_PROPOSAL_STATE_NAME).write_text(
            json.dumps(
                {
                    "pai_runtime_command": [
                        str(pai_dir / "bin" / "pai-runtime"),
                        "propose-state",
                        "--runtime",
                        "codex",
                    ],
                    "provider_command": ["codex", "exec", "[sanitized-state-proposal-prompt]"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        return pai_dir, run_dir, marker

    def _audit(self, pai_dir: Path, run_dir: Path, marker: Path) -> dict[str, object]:
        return audit_state_proposal_run(
            pai_dir=pai_dir,
            marker=marker,
            run_dir=run_dir,
            capsule_path=run_dir / STATE_CONTEXT_CAPSULE_NAME,
            proposal_path=run_dir / STATE_PROPOSAL_NAME,
            events_path=run_dir / STATE_PROPOSAL_EVENTS_NAME,
            repo_root=Path.cwd(),
        )

    def test_state_proposal_schema_accepts_required_shape(self):
        schema = _schema("state-proposal.schema.json")
        Draft202012Validator(schema).validate(_proposal())
        self.assertEqual(validate_state_proposal(_proposal()), [])

    def test_state_proposal_validation_schema_accepts_required_shape(self):
        schema = _schema("state-proposal-validation.schema.json")
        Draft202012Validator(schema).validate(_validation())

    def test_state_proposal_requires_proposal_only_true(self):
        proposal = _proposal()
        proposal["proposal_only"] = False
        self.assertIn("state proposal mismatch for proposal_only", validate_state_proposal(proposal))

    def test_state_proposal_requires_memory_apply_status_proposed_only(self):
        proposal = _proposal()
        proposal["memory_proposals"][0]["apply_status"] = "applied"
        self.assertIn("memory_proposals[0].apply_status must be proposed_only", validate_state_proposal(proposal))

    def test_state_proposal_requires_isa_apply_status_proposed_only(self):
        proposal = _proposal()
        proposal["isa_proposals"][0]["apply_status"] = "applied"
        self.assertIn("isa_proposals[0].apply_status must be proposed_only", validate_state_proposal(proposal))

    def test_state_proposal_rejects_memory_write_performed(self):
        proposal = _proposal()
        proposal["memory_write_performed"] = True
        self.assertIn("state proposal mismatch for memory_write_performed", validate_state_proposal(proposal))

    def test_state_proposal_rejects_isa_write_performed(self):
        proposal = _proposal()
        proposal["isa_write_performed"] = True
        self.assertIn("state proposal mismatch for isa_write_performed", validate_state_proposal(proposal))

    def test_state_proposal_rejects_pulse_probe(self):
        proposal = _proposal()
        proposal["pulse_probe_performed"] = True
        self.assertIn("state proposal mismatch for pulse_probe_performed", validate_state_proposal(proposal))

    def test_capabilities_allow_memory_write_proposal(self):
        manifest = {"capabilities": list(CODEX_S16A_PROVIDER_CAPABILITIES)}
        self.assertEqual(validate_capability_policy(manifest, ["memory.write.proposal"]), [])

    def test_capabilities_allow_isa_write_proposal(self):
        manifest = {"capabilities": list(CODEX_S16A_PROVIDER_CAPABILITIES)}
        self.assertEqual(validate_capability_policy(manifest, STATE_PROPOSAL_TASK_CAPABILITIES), [])

    def test_capabilities_reject_memory_write_commit(self):
        manifest = {"capabilities": list(CODEX_PROVIDER_CAPABILITIES)}
        errors = validate_capability_policy(manifest, ["memory.write.commit"])
        self.assertTrue(errors)

    def test_capabilities_reject_isa_write_commit(self):
        manifest = {"capabilities": list(CODEX_PROVIDER_CAPABILITIES)}
        errors = validate_capability_policy(manifest, ["isa.write.commit"])
        self.assertTrue(errors)

    def test_capabilities_reject_pulse_probe(self):
        manifest = {"capabilities": list(CODEX_PROVIDER_CAPABILITIES)}
        errors = validate_capability_policy(manifest, ["pulse.probe"])
        self.assertTrue(errors)

    def test_audit_state_proposal_accepts_clean_proposal_only_run(self):
        with tempfile.TemporaryDirectory(prefix="s16a.state.") as tmp:
            pai_dir, run_dir, marker = self._write_clean_run(tmp)
            result = self._audit(pai_dir, run_dir, marker)
            self.assertTrue(result["validation_passed"])
            self.assertFalse(result["memory_files_modified"])
            self.assertFalse(result["isa_files_modified"])

    def test_audit_state_proposal_rejects_memory_file_modified(self):
        with tempfile.TemporaryDirectory(prefix="s16a.state.") as tmp:
            pai_dir, run_dir, marker = self._write_clean_run(tmp)
            target = pai_dir / "Memory" / "WORK" / "bad.md"
            target.parent.mkdir(parents=True)
            target.write_text("must not be written\n", encoding="utf-8")
            result = self._audit(pai_dir, run_dir, marker)
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["memory_files_modified"])

    def test_audit_state_proposal_rejects_isa_file_modified(self):
        with tempfile.TemporaryDirectory(prefix="s16a.state.") as tmp:
            pai_dir, run_dir, marker = self._write_clean_run(tmp)
            target = pai_dir / "ISA" / "bad.md"
            target.parent.mkdir(parents=True)
            target.write_text("must not be written\n", encoding="utf-8")
            result = self._audit(pai_dir, run_dir, marker)
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["isa_files_modified"])

    def test_audit_state_proposal_rejects_pulse_file_modified(self):
        with tempfile.TemporaryDirectory(prefix="s16a.state.") as tmp:
            pai_dir, run_dir, marker = self._write_clean_run(tmp)
            target = pai_dir / "Pulse" / "state.json"
            target.parent.mkdir(parents=True)
            target.write_text("{}\n", encoding="utf-8")
            result = self._audit(pai_dir, run_dir, marker)
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["pulse_files_modified"])

    def test_audit_state_proposal_rejects_unknown_unclassified_write(self):
        with tempfile.TemporaryDirectory(prefix="s16a.state.") as tmp:
            pai_dir, run_dir, marker = self._write_clean_run(tmp)
            (pai_dir / "unknown.txt").write_text("unexpected\n", encoding="utf-8")
            result = self._audit(pai_dir, run_dir, marker)
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["unknown_unclassified_writes"])


if __name__ == "__main__":
    unittest.main()
