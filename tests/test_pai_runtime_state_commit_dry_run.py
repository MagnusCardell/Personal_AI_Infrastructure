from __future__ import annotations

import json
import os
import tempfile
import time
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.pai_runtime_runner.capabilities import (
    CODEX_S16C_PROVIDER_CAPABILITIES,
    STATE_COMMIT_DRY_RUN_TASK_CAPABILITIES,
    validate_capability_policy,
)
from tools.pai_runtime_runner.state_commit_dry_run import (
    COMMIT_DRY_RUN_CONTEXT_CAPSULE_NAME,
    S16C_HUMAN_GATE,
    S16C_MILESTONE,
    S16C_RUN_ID,
    S16C_TASK_ID,
    S16C_TASK_KIND,
    STATE_COMMIT_DRY_RUN_EVENTS_NAME,
    STATE_COMMIT_DRY_RUN_PLAN_NAME,
    STATE_COMMIT_DRY_RUN_REVIEW_NAME,
    STATE_COMMIT_DRY_RUN_STATE_NAME,
    audit_state_commit_dry_run,
    build_commit_dry_run_plan,
    validate_human_gate,
    validate_state_commit_dry_run_plan,
)
from tools.pai_runtime_runner.state_proposal import PAI_DIR_LABEL, S16A_MILESTONE, S16A_RUN_ID
from tools.pai_runtime_runner.state_proposal_review import S16B_MILESTONE, S16B_RUN_ID


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
                "title": "Track commit dry-run policy",
                "rationale": "S16C can plan without writing Memory.",
                "source_context": "accepted S16A proposal artifact",
                "proposed_body": "Dry-run planning remains non-committing.",
                "confidence": 0.8,
                "apply_status": "proposed_only",
            },
            {
                "category": "LEARNING",
                "title": "Deferred learning record",
                "rationale": "This proposal should not be planned when deferred.",
                "source_context": "accepted S16A proposal artifact",
                "proposed_body": "Deferred proposal body.",
                "confidence": 0.8,
                "apply_status": "proposed_only",
            },
        ],
        "isa_proposals": [
            {
                "proposal_type": "work_record",
                "title": "Record dry-run milestone",
                "rationale": "S16C can plan without writing ISA.",
                "proposed_record": "S16C dry-run plan record.",
                "source_context": "accepted S16A proposal artifact",
                "confidence": 0.75,
                "apply_status": "proposed_only",
            },
            {
                "proposal_type": "work_record",
                "title": "Needs revision record",
                "rationale": "This proposal should not be planned when it needs revision.",
                "proposed_record": "Needs revision record.",
                "source_context": "accepted S16A proposal artifact",
                "confidence": 0.75,
                "apply_status": "proposed_only",
            },
        ],
        "proposal_only": True,
        "memory_write_performed": False,
        "isa_write_performed": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
        "evidence_classification": ["proposal-only Memory/ISA semantics"],
        "known_limits": ["S16A does not apply Memory or ISA writes."],
    }


def _decisions(
    *,
    memory_0: str = "approved_for_future_commit_candidate",
    memory_1: str = "deferred",
    isa_0: str = "approved_for_future_commit_candidate",
    isa_1: str = "needs_revision",
) -> dict[str, object]:
    return {
        "milestone_name": S16B_MILESTONE,
        "run_id": S16B_RUN_ID,
        "source_proposal_run_id": S16A_RUN_ID,
        "decision_authority": "pai-policy",
        "decision_mode": "review-only",
        "memory_decisions": [
            {
                "proposal_id": "memory-0",
                "decision": memory_0,
                "rationale": "PAI policy keeps this decision non-committing.",
                "commit_status": "not_committed",
            },
            {
                "proposal_id": "memory-1",
                "decision": memory_1,
                "rationale": "PAI policy keeps this decision non-committing.",
                "commit_status": "not_committed",
            },
        ],
        "isa_decisions": [
            {
                "proposal_id": "isa-0",
                "decision": isa_0,
                "rationale": "PAI policy keeps this decision non-committing.",
                "commit_status": "not_committed",
            },
            {
                "proposal_id": "isa-1",
                "decision": isa_1,
                "rationale": "PAI policy keeps this decision non-committing.",
                "commit_status": "not_committed",
            },
        ],
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_files_modified": False,
        "isa_files_modified": False,
        "pulse_files_modified": False,
        "known_limits": ["S16B decisions are not commits."],
    }


def _capsule() -> dict[str, object]:
    return {
        "milestone_name": S16C_MILESTONE,
        "run_id": S16C_RUN_ID,
        "task_id": S16C_TASK_ID,
        "task_kind": S16C_TASK_KIND,
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
        "source_decisions_run_id": S16B_RUN_ID,
        "human_gate_required": S16C_HUMAN_GATE,
        "source_proposal_metadata": {
            "memory_proposal_count": 2,
            "isa_proposal_count": 2,
            "proposal_only": True,
        },
        "source_decisions_metadata": {
            "memory_decision_count": 2,
            "isa_decision_count": 2,
            "candidate_decision_count": 2,
            "all_decisions_not_committed": True,
            "commit_authority_granted": False,
            "commit_performed": False,
        },
        "dry_run_policy": [
            "Codex may assist a dry-run plan but S16C does not write Memory or ISA.",
        ],
    }


def _review() -> dict[str, object]:
    return {
        "milestone_name": S16C_MILESTONE,
        "run_id": S16C_RUN_ID,
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "task_id": S16C_TASK_ID,
        "task_kind": S16C_TASK_KIND,
        "adapter_identity_marker": "PAI_CODEX_PEER_BETA_ADAPTER",
        "upstream_adapter": "claude",
        "agents_router_observed": True,
        "source_proposal_run_id": S16A_RUN_ID,
        "source_decisions_run_id": S16B_RUN_ID,
        "source_proposal_used": True,
        "source_decisions_used": True,
        "context_capsule_used": True,
        "context_capsule_metadata_only": True,
        "human_gate_observed": True,
        "dry_run_only": True,
        "commit_authority_requested": False,
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_write_performed": False,
        "isa_write_performed": False,
        "pulse_probe_performed": False,
        "localhost_31337_called": False,
        "evidence_classification": ["dry-run-only Memory/ISA commit planning"],
        "known_limits": ["S16C does not commit Memory or ISA proposals."],
    }


def _plan() -> dict[str, object]:
    return build_commit_dry_run_plan(_source_proposal(), _decisions(), S16C_HUMAN_GATE)


def _validation() -> dict[str, object]:
    return {
        "milestone_name": S16C_MILESTONE,
        "run_id": S16C_RUN_ID,
        "runtime": "codex",
        "runtime_attempt_number": 1,
        "pai_runtime_command": [f"{PAI_DIR_LABEL}/bin/pai-runtime", "dry-run-state-commit", "--runtime", "codex"],
        "provider_command": ["codex", "exec", "[sanitized-state-commit-dry-run-prompt]"],
        "source_proposal_present": True,
        "source_proposal_schema_valid": True,
        "source_decisions_present": True,
        "source_decisions_schema_valid": True,
        "human_gate_present": True,
        "human_gate_valid": True,
        "dry_run_context_capsule_present": True,
        "dry_run_context_capsule_metadata_only": True,
        "dry_run_review_present": True,
        "dry_run_review_schema_valid": True,
        "dry_run_plan_present": True,
        "dry_run_plan_schema_valid": True,
        "candidate_decisions_present": True,
        "all_planned_writes_not_written": True,
        "all_target_paths_relative": True,
        "all_target_paths_allowed": True,
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
        "known_limits": ["S16C dry-run-only validation."],
    }


def _schema(name: str) -> dict[str, object]:
    schema = json.loads(Path("pai-runtime", name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


class PaiRuntimeStateCommitDryRunTests(unittest.TestCase):
    def _write_json(self, path: Path, payload: dict[str, object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def _write_clean_run(self, tmp: str) -> tuple[Path, Path, Path, Path, Path]:
        pai_dir = Path(tmp) / "home" / ".claude" / "PAI"
        run_dir = pai_dir / "runs" / "s16c" / "commit-dry-run"
        source_proposal_path = pai_dir / "runs" / "s16a" / "state-proposal" / "state-proposal.json"
        source_decisions_path = pai_dir / "runs" / "s16b" / "proposal-review" / "state-proposal-decisions.json"
        (pai_dir / "runtime-schemas").mkdir(parents=True)
        for name in (
            "state-proposal.schema.json",
            "state-proposal-decisions.schema.json",
            "state-commit-dry-run-review.schema.json",
            "state-commit-dry-run-plan.schema.json",
        ):
            (pai_dir / "runtime-schemas" / name).write_text(
                Path("pai-runtime", name).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        self._write_json(source_proposal_path, _source_proposal())
        self._write_json(source_decisions_path, _decisions())
        time.sleep(0.01)
        marker = Path(tmp) / "marker"
        marker.write_text("marker\n", encoding="utf-8")
        time.sleep(0.01)
        self._write_json(run_dir / COMMIT_DRY_RUN_CONTEXT_CAPSULE_NAME, _capsule())
        self._write_json(run_dir / STATE_COMMIT_DRY_RUN_REVIEW_NAME, _review())
        self._write_json(run_dir / STATE_COMMIT_DRY_RUN_PLAN_NAME, _plan())
        (run_dir / STATE_COMMIT_DRY_RUN_EVENTS_NAME).write_text(
            json.dumps({"type": "message", "message": "dry-run review emitted"}) + "\n",
            encoding="utf-8",
        )
        self._write_json(
            run_dir / STATE_COMMIT_DRY_RUN_STATE_NAME,
            {
                "pai_runtime_command": [
                    str(pai_dir / "bin" / "pai-runtime"),
                    "dry-run-state-commit",
                    "--runtime",
                    "codex",
                ],
                "provider_command": ["codex", "exec", "[sanitized-state-commit-dry-run-prompt]"],
                "source_proposal_path": str(source_proposal_path),
                "source_decisions_path": str(source_decisions_path),
                "human_gate": S16C_HUMAN_GATE,
                "commit_authority_granted": False,
                "commit_performed": False,
            },
        )
        return pai_dir, run_dir, source_proposal_path, source_decisions_path, marker

    def _audit(
        self,
        pai_dir: Path,
        run_dir: Path,
        source_proposal_path: Path,
        source_decisions_path: Path,
        marker: Path,
    ) -> dict[str, object]:
        repo_root = run_dir.parents[4] / "repo"
        repo_root.mkdir(parents=True, exist_ok=True)
        home = run_dir.parents[4] / "isolated-home"
        home.mkdir(parents=True, exist_ok=True)
        old_home = os.environ.get("HOME")
        os.environ["HOME"] = str(home)
        try:
            return audit_state_commit_dry_run(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                source_proposal_path=source_proposal_path,
                source_decisions_path=source_decisions_path,
                capsule_path=run_dir / COMMIT_DRY_RUN_CONTEXT_CAPSULE_NAME,
                review_path=run_dir / STATE_COMMIT_DRY_RUN_REVIEW_NAME,
                plan_path=run_dir / STATE_COMMIT_DRY_RUN_PLAN_NAME,
                events_path=run_dir / STATE_COMMIT_DRY_RUN_EVENTS_NAME,
                repo_root=repo_root,
            )
        finally:
            if old_home is None:
                os.environ.pop("HOME", None)
            else:
                os.environ["HOME"] = old_home

    def test_state_commit_dry_run_review_schema_accepts_required_shape(self):
        Draft202012Validator(_schema("state-commit-dry-run-review.schema.json")).validate(_review())

    def test_state_commit_dry_run_plan_schema_accepts_required_shape(self):
        Draft202012Validator(_schema("state-commit-dry-run-plan.schema.json")).validate(_plan())

    def test_state_commit_dry_run_validation_schema_accepts_required_shape(self):
        Draft202012Validator(_schema("state-commit-dry-run-validation.schema.json")).validate(_validation())

    def test_dry_run_requires_exact_human_gate(self):
        with self.assertRaisesRegex(ValueError, "S16C_DRY_RUN_ONLY_NO_MEMORY_ISA_WRITE"):
            validate_human_gate("WRONG")

    def test_dry_run_rejects_missing_human_gate(self):
        with self.assertRaisesRegex(ValueError, "S16C_DRY_RUN_ONLY_NO_MEMORY_ISA_WRITE"):
            validate_human_gate(None)

    def test_dry_run_selects_only_approved_future_commit_candidates(self):
        plan = build_commit_dry_run_plan(
            _source_proposal(),
            _decisions(memory_0="approved_for_future_commit_candidate", memory_1="rejected", isa_0="deferred", isa_1="needs_revision"),
            S16C_HUMAN_GATE,
        )
        self.assertEqual([item["proposal_id"] for item in plan["candidate_decisions_used"]], ["memory-0"])
        self.assertEqual(len(plan["planned_memory_writes"]), 1)
        self.assertEqual(plan["planned_isa_writes"], [])

    def test_dry_run_ignores_rejected_deferred_and_needs_revision(self):
        plan = build_commit_dry_run_plan(
            _source_proposal(),
            _decisions(memory_0="rejected", memory_1="deferred", isa_0="approved_for_future_commit_candidate", isa_1="needs_revision"),
            S16C_HUMAN_GATE,
        )
        self.assertEqual([item["proposal_id"] for item in plan["candidate_decisions_used"]], ["isa-0"])
        self.assertEqual(
            {item["non_planned_reason"] for item in plan["non_planned_decisions"]},
            {"rejected", "deferred", "needs_revision"},
        )

    def test_dry_run_requires_candidate_decisions(self):
        with self.assertRaisesRegex(ValueError, "no approved_for_future_commit_candidate decisions"):
            build_commit_dry_run_plan(
                _source_proposal(),
                _decisions(memory_0="rejected", memory_1="deferred", isa_0="rejected", isa_1="needs_revision"),
                S16C_HUMAN_GATE,
            )

    def test_dry_run_rejects_absolute_target_path(self):
        plan = _plan()
        plan["planned_memory_writes"][0]["relative_target_path"] = "/Memory/WORK/bad.md"
        self.assertTrue(validate_state_commit_dry_run_plan(plan))

    def test_dry_run_rejects_path_traversal_target_path(self):
        plan = _plan()
        plan["planned_memory_writes"][0]["relative_target_path"] = "Memory/WORK/../bad.md"
        self.assertTrue(validate_state_commit_dry_run_plan(plan))

    def test_dry_run_rejects_target_outside_memory_or_isa(self):
        plan = _plan()
        plan["planned_memory_writes"][0]["relative_target_path"] = "Memory/STATE/bad.md"
        self.assertTrue(validate_state_commit_dry_run_plan(plan))

    def test_dry_run_rejects_pulse_target(self):
        plan = _plan()
        plan["planned_memory_writes"][0]["relative_target_path"] = "Pulse/events/bad.jsonl"
        self.assertTrue(validate_state_commit_dry_run_plan(plan))

    def test_dry_run_rejects_commit_authority_granted(self):
        plan = _plan()
        plan["commit_authority_granted"] = True
        self.assertIn("state commit dry-run plan mismatch for commit_authority_granted", validate_state_commit_dry_run_plan(plan))

    def test_dry_run_rejects_commit_performed(self):
        plan = _plan()
        plan["commit_performed"] = True
        self.assertIn("state commit dry-run plan mismatch for commit_performed", validate_state_commit_dry_run_plan(plan))

    def test_dry_run_rejects_memory_file_modified(self):
        plan = _plan()
        plan["memory_files_modified"] = True
        self.assertIn("state commit dry-run plan mismatch for memory_files_modified", validate_state_commit_dry_run_plan(plan))

    def test_dry_run_rejects_isa_file_modified(self):
        plan = _plan()
        plan["isa_files_modified"] = True
        self.assertIn("state commit dry-run plan mismatch for isa_files_modified", validate_state_commit_dry_run_plan(plan))

    def test_capabilities_allow_memory_commit_dry_run(self):
        manifest = {"capabilities": list(CODEX_S16C_PROVIDER_CAPABILITIES)}
        self.assertEqual(validate_capability_policy(manifest, ["memory.commit.dry_run"]), [])

    def test_capabilities_allow_isa_commit_dry_run(self):
        manifest = {"capabilities": list(CODEX_S16C_PROVIDER_CAPABILITIES)}
        self.assertEqual(validate_capability_policy(manifest, STATE_COMMIT_DRY_RUN_TASK_CAPABILITIES), [])

    def test_capabilities_reject_memory_write_commit(self):
        manifest = {"capabilities": list(CODEX_S16C_PROVIDER_CAPABILITIES)}
        self.assertTrue(validate_capability_policy(manifest, ["memory.write.commit"]))

    def test_capabilities_reject_isa_write_commit(self):
        manifest = {"capabilities": list(CODEX_S16C_PROVIDER_CAPABILITIES)}
        self.assertTrue(validate_capability_policy(manifest, ["isa.write.commit"]))

    def test_audit_state_commit_dry_run_accepts_clean_dry_run(self):
        with tempfile.TemporaryDirectory(prefix="s16c.dryrun.") as tmp:
            pai_dir, run_dir, source_proposal_path, source_decisions_path, marker = self._write_clean_run(tmp)
            result = self._audit(pai_dir, run_dir, source_proposal_path, source_decisions_path, marker)
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["all_planned_writes_not_written"])

    def test_audit_state_commit_dry_run_rejects_unknown_unclassified_write(self):
        with tempfile.TemporaryDirectory(prefix="s16c.dryrun.") as tmp:
            pai_dir, run_dir, source_proposal_path, source_decisions_path, marker = self._write_clean_run(tmp)
            (pai_dir / "unknown.txt").write_text("unexpected\n", encoding="utf-8")
            result = self._audit(pai_dir, run_dir, source_proposal_path, source_decisions_path, marker)
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["unknown_unclassified_writes"])


if __name__ == "__main__":
    unittest.main()
