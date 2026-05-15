from __future__ import annotations

import json
import time
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.pai_runtime_runner.capabilities import (
    CODEX_S16B_PROVIDER_CAPABILITIES,
    STATE_PROPOSAL_REVIEW_TASK_CAPABILITIES,
    validate_capability_policy,
)
from tools.pai_runtime_runner.state_proposal import PAI_DIR_LABEL, S16A_MILESTONE, S16A_RUN_ID
from tools.pai_runtime_runner.state_proposal_review import (
    REVIEW_CONTEXT_CAPSULE_NAME,
    S16B_MILESTONE,
    S16B_RUN_ID,
    S16B_TASK_ID,
    S16B_TASK_KIND,
    STATE_PROPOSAL_DECISIONS_NAME,
    STATE_PROPOSAL_REVIEW_EVENTS_NAME,
    STATE_PROPOSAL_REVIEW_NAME,
    STATE_PROPOSAL_REVIEW_STATE_NAME,
    audit_state_proposal_review_run,
    validate_state_proposal_decisions,
)


def _source_proposal() -> dict[str, object]:
    return {
        "milestone_name": S16A_MILESTONE,
        "run_id": S16A_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "pai_dir_label": PAI_DIR_LABEL,
        "task_id": "s16a-state-proposal-task",
        "task_kind": "proposal-only-memory-isa-state-update",
        "adapter_identity_marker": "PAI_CODEX_PEER_BETA_ADAPTER",
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": True,
        "memory_proposals": [
            {
                "category": "WORK",
                "title": "Track proposal review policy",
                "rationale": "S16B reviews S16A proposals without commit authority.",
                "source_context": "accepted S16A proposal artifact",
                "proposed_body": "Review policy remains non-committing.",
                "confidence": 0.8,
                "apply_status": "proposed_only",
            }
        ],
        "isa_proposals": [
            {
                "proposal_type": "work_record",
                "title": "Record review-only milestone",
                "rationale": "The proposal can be reviewed without writing ISA.",
                "proposed_record": "S16B review-only decision record.",
                "source_context": "accepted S16A proposal artifact",
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
        "milestone_name": S16B_MILESTONE,
        "run_id": S16B_RUN_ID,
        "task_id": S16B_TASK_ID,
        "task_kind": S16B_TASK_KIND,
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
        "source_proposal_run_id": S16A_RUN_ID,
        "source_proposal_metadata": {
            "memory_proposal_count": 1,
            "isa_proposal_count": 1,
            "all_memory_apply_status_proposed_only": True,
            "all_isa_apply_status_proposed_only": True,
        },
        "review_policy": [
            "Codex may review Memory proposals but S16B does not write Memory.",
        ],
    }


def _review(decision: str = "approved_for_future_commit_candidate") -> dict[str, object]:
    return {
        "milestone_name": S16B_MILESTONE,
        "run_id": S16B_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "task_id": S16B_TASK_ID,
        "task_kind": S16B_TASK_KIND,
        "adapter_identity_marker": "PAI_CODEX_PEER_BETA_ADAPTER",
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "source_proposal_run_id": S16A_RUN_ID,
        "source_proposal_used": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": True,
        "memory_proposal_reviews": [
            {
                "proposal_id": "memory-0",
                "title": "Track proposal review policy",
                "review_summary": "The proposal is bounded and can remain a future candidate.",
                "rationale": "S16B does not grant commit authority.",
                "recommended_decision": decision,
                "commit_status": "not_committed",
            }
        ],
        "isa_proposal_reviews": [
            {
                "proposal_id": "isa-0",
                "title": "Record review-only milestone",
                "review_summary": "The proposal is reviewable without ISA mutation.",
                "rationale": "S16B decisions remain run artifacts.",
                "recommended_decision": decision,
                "commit_status": "not_committed",
            }
        ],
        "commit_authority_requested": False,
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_write_performed": False,
        "isa_write_performed": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
        "evidence_classification": ["review-only Memory/ISA proposal policy"],
        "known_limits": ["S16B does not commit Memory or ISA proposals."],
    }


def _decisions(decision: str = "approved_for_future_commit_candidate") -> dict[str, object]:
    return {
        "milestone_name": S16B_MILESTONE,
        "run_id": S16B_RUN_ID,
        "source_proposal_run_id": S16A_RUN_ID,
        "decision_authority": "pai-policy",
        "decision_mode": "review-only",
        "memory_decisions": [
            {
                "proposal_id": "memory-0",
                "decision": decision,
                "rationale": "PAI policy keeps this decision non-committing.",
                "commit_status": "not_committed",
            }
        ],
        "isa_decisions": [
            {
                "proposal_id": "isa-0",
                "decision": decision,
                "rationale": "PAI policy keeps this decision non-committing.",
                "commit_status": "not_committed",
            }
        ],
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_files_modified": False,
        "isa_files_modified": False,
        "pulse_files_modified": False,
        "known_limits": ["S16B decisions are not commits."],
    }


def _validation() -> dict[str, object]:
    return {
        "milestone_name": S16B_MILESTONE,
        "run_id": S16B_RUN_ID,
        "runtime": "codex",
        "runtime_attempt_number": 1,
        "pai_runtime_command": [f"{PAI_DIR_LABEL}/bin/pai-runtime", "review-state-proposal", "--runtime", "codex"],
        "provider_command": ["codex", "exec", "[sanitized-state-proposal-review-prompt]"],
        "source_proposal_present": True,
        "source_proposal_schema_valid": True,
        "review_context_capsule_present": True,
        "review_context_capsule_metadata_only": True,
        "state_proposal_review_present": True,
        "state_proposal_review_schema_valid": True,
        "state_proposal_decisions_present": True,
        "state_proposal_decisions_schema_valid": True,
        "all_decisions_non_committing": True,
        "commit_authority_granted": False,
        "commit_performed": False,
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
        "known_limits": ["S16B review-only validation."],
    }


def _schema(name: str) -> dict[str, object]:
    schema = json.loads(Path("pai-runtime", name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


class PaiRuntimeStateProposalReviewTests(unittest.TestCase):
    def _write_clean_run(self, tmp: str) -> tuple[Path, Path, Path, Path]:
        pai_dir = Path(tmp) / "home" / ".claude" / "PAI"
        run_dir = pai_dir / "runs" / "s16b" / "proposal-review"
        source_path = pai_dir / "runs" / "s16a" / "state-proposal" / "state-proposal.json"
        (pai_dir / "runtime-schemas").mkdir(parents=True)
        run_dir.mkdir(parents=True)
        source_path.parent.mkdir(parents=True)
        for name in (
            "state-proposal.schema.json",
            "state-proposal-review.schema.json",
            "state-proposal-decisions.schema.json",
        ):
            (pai_dir / "runtime-schemas" / name).write_text(
                Path("pai-runtime", name).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        source_path.write_text(json.dumps(_source_proposal()) + "\n", encoding="utf-8")
        time.sleep(0.01)
        marker = Path(tmp) / "marker"
        marker.write_text("marker\n", encoding="utf-8")
        time.sleep(0.01)
        (run_dir / REVIEW_CONTEXT_CAPSULE_NAME).write_text(json.dumps(_capsule()) + "\n", encoding="utf-8")
        (run_dir / STATE_PROPOSAL_REVIEW_NAME).write_text(json.dumps(_review()) + "\n", encoding="utf-8")
        (run_dir / STATE_PROPOSAL_DECISIONS_NAME).write_text(json.dumps(_decisions()) + "\n", encoding="utf-8")
        (run_dir / STATE_PROPOSAL_REVIEW_EVENTS_NAME).write_text(
            json.dumps({"type": "message", "message": "review emitted"}) + "\n",
            encoding="utf-8",
        )
        (run_dir / STATE_PROPOSAL_REVIEW_STATE_NAME).write_text(
            json.dumps(
                {
                    "pai_runtime_command": [
                        str(pai_dir / "bin" / "pai-runtime"),
                        "review-state-proposal",
                        "--runtime",
                        "codex",
                    ],
                    "provider_command": ["codex", "exec", "[sanitized-state-proposal-review-prompt]"],
                    "source_proposal_path": str(source_path),
                }
            )
            + "\n",
            encoding="utf-8",
        )
        return pai_dir, run_dir, source_path, marker

    def _audit(self, pai_dir: Path, run_dir: Path, source_path: Path, marker: Path) -> dict[str, object]:
        return audit_state_proposal_review_run(
            pai_dir=pai_dir,
            marker=marker,
            run_dir=run_dir,
            source_proposal_path=source_path,
            capsule_path=run_dir / REVIEW_CONTEXT_CAPSULE_NAME,
            review_path=run_dir / STATE_PROPOSAL_REVIEW_NAME,
            decisions_path=run_dir / STATE_PROPOSAL_DECISIONS_NAME,
            events_path=run_dir / STATE_PROPOSAL_REVIEW_EVENTS_NAME,
            repo_root=Path.cwd(),
        )

    def test_state_proposal_review_schema_accepts_required_shape(self):
        Draft202012Validator(_schema("state-proposal-review.schema.json")).validate(_review())

    def test_state_proposal_decisions_schema_accepts_required_shape(self):
        Draft202012Validator(_schema("state-proposal-decisions.schema.json")).validate(_decisions())
        self.assertEqual(validate_state_proposal_decisions(_decisions()), [])

    def test_state_proposal_review_validation_schema_accepts_required_shape(self):
        Draft202012Validator(_schema("state-proposal-review-validation.schema.json")).validate(_validation())

    def test_review_decisions_require_non_committing_status(self):
        decisions = _decisions()
        decisions["memory_decisions"][0]["commit_status"] = "committed"
        self.assertIn("memory_decisions[0].commit_status must be not_committed", validate_state_proposal_decisions(decisions))

    def test_review_decisions_reject_commit_performed(self):
        decisions = _decisions()
        decisions["commit_performed"] = True
        self.assertIn("state proposal decisions mismatch for commit_performed", validate_state_proposal_decisions(decisions))

    def test_review_decisions_reject_commit_authority_granted(self):
        decisions = _decisions()
        decisions["commit_authority_granted"] = True
        self.assertIn(
            "state proposal decisions mismatch for commit_authority_granted",
            validate_state_proposal_decisions(decisions),
        )

    def test_review_decisions_accept_approved_for_future_commit_candidate(self):
        self.assertEqual(validate_state_proposal_decisions(_decisions("approved_for_future_commit_candidate")), [])

    def test_review_decisions_accept_rejected(self):
        self.assertEqual(validate_state_proposal_decisions(_decisions("rejected")), [])

    def test_review_decisions_accept_deferred(self):
        self.assertEqual(validate_state_proposal_decisions(_decisions("deferred")), [])

    def test_review_decisions_accept_needs_revision(self):
        self.assertEqual(validate_state_proposal_decisions(_decisions("needs_revision")), [])

    def test_capabilities_allow_memory_proposal_review(self):
        manifest = {"capabilities": list(CODEX_S16B_PROVIDER_CAPABILITIES)}
        self.assertEqual(validate_capability_policy(manifest, ["memory.proposal.review"]), [])

    def test_capabilities_allow_isa_proposal_review(self):
        manifest = {"capabilities": list(CODEX_S16B_PROVIDER_CAPABILITIES)}
        self.assertEqual(validate_capability_policy(manifest, STATE_PROPOSAL_REVIEW_TASK_CAPABILITIES), [])

    def test_capabilities_reject_memory_write_commit(self):
        manifest = {"capabilities": list(CODEX_S16B_PROVIDER_CAPABILITIES)}
        self.assertTrue(validate_capability_policy(manifest, ["memory.write.commit"]))

    def test_capabilities_reject_isa_write_commit(self):
        manifest = {"capabilities": list(CODEX_S16B_PROVIDER_CAPABILITIES)}
        self.assertTrue(validate_capability_policy(manifest, ["isa.write.commit"]))

    def test_audit_state_proposal_review_accepts_clean_review_only_run(self):
        with tempfile.TemporaryDirectory(prefix="s16b.review.") as tmp:
            pai_dir, run_dir, source_path, marker = self._write_clean_run(tmp)
            result = self._audit(pai_dir, run_dir, source_path, marker)
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["all_decisions_non_committing"])

    def test_audit_state_proposal_review_rejects_memory_file_modified(self):
        with tempfile.TemporaryDirectory(prefix="s16b.review.") as tmp:
            pai_dir, run_dir, source_path, marker = self._write_clean_run(tmp)
            target = pai_dir / "Memory" / "WORK" / "bad.md"
            target.parent.mkdir(parents=True)
            target.write_text("must not be written\n", encoding="utf-8")
            result = self._audit(pai_dir, run_dir, source_path, marker)
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["memory_files_modified"])

    def test_audit_state_proposal_review_rejects_isa_file_modified(self):
        with tempfile.TemporaryDirectory(prefix="s16b.review.") as tmp:
            pai_dir, run_dir, source_path, marker = self._write_clean_run(tmp)
            target = pai_dir / "ISA" / "bad.md"
            target.parent.mkdir(parents=True)
            target.write_text("must not be written\n", encoding="utf-8")
            result = self._audit(pai_dir, run_dir, source_path, marker)
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["isa_files_modified"])

    def test_audit_state_proposal_review_rejects_pulse_file_modified(self):
        with tempfile.TemporaryDirectory(prefix="s16b.review.") as tmp:
            pai_dir, run_dir, source_path, marker = self._write_clean_run(tmp)
            target = pai_dir / "Pulse" / "state.json"
            target.parent.mkdir(parents=True)
            target.write_text("{}\n", encoding="utf-8")
            result = self._audit(pai_dir, run_dir, source_path, marker)
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["pulse_files_modified"])

    def test_audit_state_proposal_review_rejects_unknown_unclassified_write(self):
        with tempfile.TemporaryDirectory(prefix="s16b.review.") as tmp:
            pai_dir, run_dir, source_path, marker = self._write_clean_run(tmp)
            (pai_dir / "unknown.txt").write_text("unexpected\n", encoding="utf-8")
            result = self._audit(pai_dir, run_dir, source_path, marker)
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["unknown_unclassified_writes"])


if __name__ == "__main__":
    unittest.main()
