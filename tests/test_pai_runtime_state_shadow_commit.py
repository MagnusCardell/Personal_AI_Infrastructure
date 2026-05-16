from __future__ import annotations

import json
import os
import tempfile
import time
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.pai_runtime_runner.capabilities import (
    CODEX_S16D_PROVIDER_CAPABILITIES,
    STATE_SHADOW_COMMIT_TASK_CAPABILITIES,
    validate_capability_policy,
)
from tools.pai_runtime_runner.state_commit_dry_run import (
    S16C_HUMAN_GATE,
    S16C_MILESTONE,
    S16C_RUN_ID,
)
from tools.pai_runtime_runner.state_proposal import PAI_DIR_LABEL
from tools.pai_runtime_runner.state_shadow_commit import (
    SELECTED_COMMIT_CANDIDATE_NAME,
    SHADOW_APPLY_RESULT_NAME,
    SHADOW_COMMIT_CONTEXT_CAPSULE_NAME,
    SHADOW_COMMIT_EVENTS_NAME,
    SHADOW_COMMIT_STATE_NAME,
    S16D_HUMAN_GATE,
    S16D_MILESTONE,
    S16D_RUN_ID,
    S16D_TASK_ID,
    S16D_TASK_KIND,
    SINGLE_PROPOSAL_POLICY_REVIEW_NAME,
    audit_state_shadow_commit,
    normalize_single_proposal_policy_review,
    select_single_commit_candidate,
    shadow_apply_candidate,
    validate_human_gate,
    validate_selected_commit_candidate,
    validate_shadow_apply_result,
    validate_shadow_commit,
)


def _source_plan() -> dict[str, object]:
    return {
        "milestone_name": S16C_MILESTONE,
        "run_id": S16C_RUN_ID,
        "source_proposal_run_id": "s16a-state-proposal",
        "source_decisions_run_id": "s16b-proposal-review",
        "plan_authority": "pai-policy",
        "plan_mode": "dry-run-only",
        "human_gate": S16C_HUMAN_GATE,
        "candidate_decisions_used": [
            {
                "proposal_id": "memory-0",
                "decision_family": "memory",
                "decision": "approved_for_future_commit_candidate",
                "rationale": "Approved as a future commit candidate.",
                "commit_status": "not_committed",
            },
            {
                "proposal_id": "memory-1",
                "decision_family": "memory",
                "decision": "approved_for_future_commit_candidate",
                "rationale": "Approved as a future commit candidate.",
                "commit_status": "not_committed",
            },
            {
                "proposal_id": "isa-0",
                "decision_family": "isa",
                "decision": "approved_for_future_commit_candidate",
                "rationale": "Approved as a future commit candidate.",
                "commit_status": "not_committed",
            },
        ],
        "planned_memory_writes": [
            {
                "proposal_id": "memory-1",
                "relative_target_path": "Memory/WORK/s16c-dry-run/memory-1-work.md",
                "rendered_content_preview": "# Work\n\nRendered work content.\n",
                "dry_run_status": "not_written",
            },
            {
                "proposal_id": "memory-0",
                "relative_target_path": "Memory/LEARNING/s16c-dry-run/memory-0-learning.md",
                "rendered_content_preview": "# Learning\n\nRendered learning content.\n",
                "dry_run_status": "not_written",
            },
        ],
        "planned_isa_writes": [
            {
                "proposal_id": "isa-0",
                "relative_target_path": "ISA/s16c-dry-run/isa-0-record.md",
                "rendered_content_preview": "# ISA\n\nRendered ISA content.\n",
                "dry_run_status": "not_written",
            }
        ],
        "non_planned_decisions": [
            {
                "proposal_id": "memory-2",
                "decision_family": "memory",
                "decision": "rejected",
                "rationale": "Rejected by PAI policy.",
                "commit_status": "not_committed",
                "non_planned_reason": "rejected",
            }
        ],
        "commit_authority_granted": False,
        "commit_performed": False,
        "memory_files_modified": False,
        "isa_files_modified": False,
        "pulse_files_modified": False,
        "known_limits": ["S16C plan is dry-run only."],
    }


def _capsule(selected: dict[str, object]) -> dict[str, object]:
    return {
        "milestone_name": S16D_MILESTONE,
        "run_id": S16D_RUN_ID,
        "task_id": S16D_TASK_ID,
        "task_kind": S16D_TASK_KIND,
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
        "source_dry_run_plan_run_id": S16C_RUN_ID,
        "human_gate_required": S16D_HUMAN_GATE,
        "source_dry_run_plan_metadata": {
            "candidate_decision_count": 3,
            "planned_memory_write_count": 2,
            "planned_isa_write_count": 1,
            "all_planned_writes_not_written": True,
            "commit_authority_granted": False,
            "commit_performed": False,
        },
        "selected_candidate_metadata": {
            "selected_candidate_count": 1,
            "selected_candidate_kind": selected["selected_candidate_kind"],
            "relative_target_path": selected["relative_target_path"],
            "target_path_family": selected["target_path_family"],
            "selection_policy": selected["selection_policy"],
        },
        "shadow_commit_policy": ["S16D shadow apply is run-directory-only."],
    }


def _review() -> dict[str, object]:
    return normalize_single_proposal_policy_review(
        {
            "evidence_classification": ["shadow-apply-only Memory/ISA commit policy"],
            "known_limits": ["S16D does not commit Memory or ISA proposals."],
        },
        {"metadata_only": True},
        S16D_HUMAN_GATE,
    )


def _selected_and_source() -> tuple[dict[str, object], dict[str, object]]:
    return select_single_commit_candidate(_source_plan())


def _shadow_result(tmp: str) -> dict[str, object]:
    selected, source = _selected_and_source()
    return shadow_apply_candidate(Path(tmp) / "run", selected, source)


def _validation() -> dict[str, object]:
    return {
        "milestone_name": S16D_MILESTONE,
        "run_id": S16D_RUN_ID,
        "runtime": "codex",
        "runtime_attempt_number": 1,
        "pai_runtime_command": [f"{PAI_DIR_LABEL}/bin/pai-runtime", "shadow-apply-state-commit", "--runtime", "codex"],
        "provider_command": ["codex", "exec", "[sanitized-state-shadow-commit-prompt]"],
        "source_dry_run_plan_present": True,
        "source_dry_run_plan_schema_valid": True,
        "human_gate_present": True,
        "human_gate_valid": True,
        "shadow_context_capsule_present": True,
        "shadow_context_capsule_metadata_only": True,
        "policy_review_present": True,
        "policy_review_schema_valid": True,
        "selected_candidate_present": True,
        "selected_candidate_schema_valid": True,
        "selected_candidate_count": 1,
        "single_candidate_selected": True,
        "selected_target_path_relative": True,
        "selected_target_path_allowed": True,
        "shadow_apply_result_present": True,
        "shadow_apply_result_schema_valid": True,
        "shadow_target_written": True,
        "shadow_target_under_run_dir": True,
        "shadow_content_hash_recorded": True,
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
        "known_limits": ["S16D shadow validation."],
    }


def _schema(name: str) -> dict[str, object]:
    schema = json.loads(Path("pai-runtime", name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


class PaiRuntimeStateShadowCommitTests(unittest.TestCase):
    def _write_json(self, path: Path, payload: dict[str, object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def _write_clean_run(self, tmp: str) -> tuple[Path, Path, Path, Path]:
        pai_dir = Path(tmp) / "home" / ".claude" / "PAI"
        run_dir = pai_dir / "runs" / "s16d" / "single-proposal-shadow-commit"
        source_plan_path = pai_dir / "runs" / "s16c" / "commit-dry-run" / "state-commit-dry-run-plan.json"
        (pai_dir / "runtime-schemas").mkdir(parents=True)
        for name in (
            "state-commit-dry-run-plan.schema.json",
            "single-proposal-policy-review.schema.json",
            "selected-commit-candidate.schema.json",
            "shadow-apply-result.schema.json",
        ):
            (pai_dir / "runtime-schemas" / name).write_text(
                Path("pai-runtime", name).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        self._write_json(source_plan_path, _source_plan())
        time.sleep(0.01)
        marker = Path(tmp) / "marker"
        marker.write_text("marker\n", encoding="utf-8")
        time.sleep(0.01)
        selected, source_candidate = _selected_and_source()
        self._write_json(run_dir / SHADOW_COMMIT_CONTEXT_CAPSULE_NAME, _capsule(selected))
        self._write_json(run_dir / SINGLE_PROPOSAL_POLICY_REVIEW_NAME, _review())
        self._write_json(run_dir / SELECTED_COMMIT_CANDIDATE_NAME, selected)
        shadow = shadow_apply_candidate(run_dir, selected, source_candidate)
        self._write_json(run_dir / SHADOW_APPLY_RESULT_NAME, shadow)
        (run_dir / SHADOW_COMMIT_EVENTS_NAME).write_text(
            json.dumps({"type": "message", "message": "shadow policy review emitted"}) + "\n",
            encoding="utf-8",
        )
        self._write_json(
            run_dir / SHADOW_COMMIT_STATE_NAME,
            {
                "pai_runtime_command": [
                    str(pai_dir / "bin" / "pai-runtime"),
                    "shadow-apply-state-commit",
                    "--runtime",
                    "codex",
                ],
                "provider_command": ["codex", "exec", "[sanitized-state-shadow-commit-prompt]"],
                "source_dry_run_plan_path": str(source_plan_path),
                "human_gate": S16D_HUMAN_GATE,
                "commit_authority_granted": False,
                "commit_performed": False,
            },
        )
        return pai_dir, run_dir, source_plan_path, marker

    def _audit(self, pai_dir: Path, run_dir: Path, source_plan_path: Path, marker: Path) -> dict[str, object]:
        repo_root = run_dir.parents[4] / "repo"
        repo_root.mkdir(parents=True, exist_ok=True)
        home = run_dir.parents[4] / "isolated-home"
        home.mkdir(parents=True, exist_ok=True)
        old_home = os.environ.get("HOME")
        os.environ["HOME"] = str(home)
        try:
            return audit_state_shadow_commit(
                pai_dir=pai_dir,
                marker=marker,
                run_dir=run_dir,
                source_dry_run_plan_path=source_plan_path,
                capsule_path=run_dir / SHADOW_COMMIT_CONTEXT_CAPSULE_NAME,
                review_path=run_dir / SINGLE_PROPOSAL_POLICY_REVIEW_NAME,
                selected_path=run_dir / SELECTED_COMMIT_CANDIDATE_NAME,
                shadow_apply_path=run_dir / SHADOW_APPLY_RESULT_NAME,
                events_path=run_dir / SHADOW_COMMIT_EVENTS_NAME,
                repo_root=repo_root,
            )
        finally:
            if old_home is None:
                os.environ.pop("HOME", None)
            else:
                os.environ["HOME"] = old_home

    def test_shadow_commit_review_schema_accepts_required_shape(self):
        Draft202012Validator(_schema("single-proposal-policy-review.schema.json")).validate(_review())

    def test_selected_commit_candidate_schema_accepts_required_shape(self):
        selected, _ = _selected_and_source()
        Draft202012Validator(_schema("selected-commit-candidate.schema.json")).validate(selected)

    def test_shadow_apply_result_schema_accepts_required_shape(self):
        with tempfile.TemporaryDirectory(prefix="s16d.shadow.") as tmp:
            Draft202012Validator(_schema("shadow-apply-result.schema.json")).validate(_shadow_result(tmp))

    def test_shadow_commit_validation_schema_accepts_required_shape(self):
        Draft202012Validator(_schema("shadow-commit-validation.schema.json")).validate(_validation())

    def test_shadow_commit_requires_exact_human_gate(self):
        with self.assertRaisesRegex(ValueError, "S16D_SHADOW_APPLY_ONLY_NO_LIVE_MEMORY_ISA_WRITE"):
            validate_human_gate("WRONG")

    def test_shadow_commit_rejects_missing_human_gate(self):
        with self.assertRaisesRegex(ValueError, "S16D_SHADOW_APPLY_ONLY_NO_LIVE_MEMORY_ISA_WRITE"):
            validate_human_gate(None)

    def test_shadow_commit_selects_single_candidate(self):
        selected, _ = _selected_and_source()
        self.assertEqual(selected["selected_candidate_count"], 1)
        self.assertEqual(selected["selection_status"], "selected_for_shadow_apply_only")

    def test_shadow_commit_prefers_memory_before_isa_by_policy(self):
        plan = _source_plan()
        plan["planned_memory_writes"] = [
            {
                "proposal_id": "memory-9",
                "relative_target_path": "Memory/WORK/z-memory.md",
                "rendered_content_preview": "memory",
                "dry_run_status": "not_written",
            }
        ]
        plan["planned_isa_writes"] = [
            {
                "proposal_id": "isa-0",
                "relative_target_path": "ISA/a-isa.md",
                "rendered_content_preview": "isa",
                "dry_run_status": "not_written",
            }
        ]
        selected, _ = select_single_commit_candidate(plan)
        self.assertEqual(selected["selected_candidate_kind"], "memory")
        self.assertEqual(selected["relative_target_path"], "Memory/WORK/z-memory.md")

    def test_shadow_commit_rejects_no_candidates(self):
        plan = _source_plan()
        plan["planned_memory_writes"] = []
        plan["planned_isa_writes"] = []
        with self.assertRaisesRegex(ValueError, "no planned Memory or ISA writes"):
            select_single_commit_candidate(plan)

    def test_shadow_commit_rejects_absolute_target_path(self):
        plan = _source_plan()
        plan["planned_memory_writes"][0]["relative_target_path"] = "/Memory/WORK/bad.md"
        with self.assertRaisesRegex(ValueError, "relative_target_path must be relative"):
            select_single_commit_candidate(plan)

    def test_shadow_commit_rejects_path_traversal_target_path(self):
        plan = _source_plan()
        plan["planned_memory_writes"][0]["relative_target_path"] = "Memory/WORK/../bad.md"
        with self.assertRaisesRegex(ValueError, "traversal"):
            select_single_commit_candidate(plan)

    def test_shadow_commit_rejects_target_outside_memory_or_isa(self):
        plan = _source_plan()
        plan["planned_memory_writes"][0]["relative_target_path"] = "Memory/STATE/bad.md"
        with self.assertRaisesRegex(ValueError, "outside allowed"):
            select_single_commit_candidate(plan)

    def test_shadow_commit_rejects_pulse_target(self):
        plan = _source_plan()
        plan["planned_memory_writes"][0]["relative_target_path"] = "Pulse/events/bad.jsonl"
        with self.assertRaisesRegex(ValueError, "outside allowed"):
            select_single_commit_candidate(plan)

    def test_shadow_commit_writes_shadow_target_under_run_dir(self):
        with tempfile.TemporaryDirectory(prefix="s16d.shadow.") as tmp:
            run_dir = Path(tmp) / "run"
            selected, source = _selected_and_source()
            result = shadow_apply_candidate(run_dir, selected, source)
            target = run_dir / result["shadow_target_path_relative_to_run"]
            self.assertTrue(target.is_file())
            self.assertTrue(str(target.resolve()).startswith(str(run_dir.resolve()) + os.sep))

    def test_shadow_commit_rejects_commit_authority_granted(self):
        plan = _source_plan()
        plan["commit_authority_granted"] = True
        with self.assertRaisesRegex(ValueError, "commit_authority_granted"):
            select_single_commit_candidate(plan)

    def test_shadow_commit_rejects_commit_performed(self):
        plan = _source_plan()
        plan["commit_performed"] = True
        with self.assertRaisesRegex(ValueError, "commit_performed"):
            select_single_commit_candidate(plan)

    def test_shadow_commit_rejects_memory_file_modified(self):
        result = _shadow_result(tempfile.mkdtemp(prefix="s16d.shadow."))
        result["memory_files_modified"] = True
        self.assertIn("shadow apply result mismatch for memory_files_modified", validate_shadow_apply_result(result))

    def test_shadow_commit_rejects_isa_file_modified(self):
        result = _shadow_result(tempfile.mkdtemp(prefix="s16d.shadow."))
        result["isa_files_modified"] = True
        self.assertIn("shadow apply result mismatch for isa_files_modified", validate_shadow_apply_result(result))

    def test_capabilities_allow_memory_commit_shadow_apply(self):
        manifest = {"capabilities": list(CODEX_S16D_PROVIDER_CAPABILITIES)}
        self.assertEqual(validate_capability_policy(manifest, ["memory.commit.shadow_apply"]), [])

    def test_capabilities_allow_isa_commit_shadow_apply(self):
        manifest = {"capabilities": list(CODEX_S16D_PROVIDER_CAPABILITIES)}
        self.assertEqual(validate_capability_policy(manifest, STATE_SHADOW_COMMIT_TASK_CAPABILITIES), [])

    def test_capabilities_reject_memory_write_commit(self):
        manifest = {"capabilities": list(CODEX_S16D_PROVIDER_CAPABILITIES)}
        self.assertTrue(validate_capability_policy(manifest, ["memory.write.commit"]))

    def test_capabilities_reject_isa_write_commit(self):
        manifest = {"capabilities": list(CODEX_S16D_PROVIDER_CAPABILITIES)}
        self.assertTrue(validate_capability_policy(manifest, ["isa.write.commit"]))

    def test_audit_state_shadow_commit_accepts_clean_shadow_apply(self):
        with tempfile.TemporaryDirectory(prefix="s16d.shadow.") as tmp:
            pai_dir, run_dir, source_plan_path, marker = self._write_clean_run(tmp)
            result = self._audit(pai_dir, run_dir, source_plan_path, marker)
            self.assertTrue(result["validation_passed"])
            self.assertTrue(result["single_candidate_selected"])
            self.assertTrue(result["shadow_target_under_run_dir"])

    def test_audit_state_shadow_commit_rejects_unknown_unclassified_write(self):
        with tempfile.TemporaryDirectory(prefix="s16d.shadow.") as tmp:
            pai_dir, run_dir, source_plan_path, marker = self._write_clean_run(tmp)
            (pai_dir / "unknown.txt").write_text("unexpected\n", encoding="utf-8")
            result = self._audit(pai_dir, run_dir, source_plan_path, marker)
            self.assertFalse(result["validation_passed"])
            self.assertTrue(result["unknown_unclassified_writes"])


if __name__ == "__main__":
    unittest.main()
