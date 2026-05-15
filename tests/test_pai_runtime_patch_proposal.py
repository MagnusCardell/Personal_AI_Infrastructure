from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.pai_runtime_runner.patch_proposal import (
    PATCH_PROPOSAL_TEXT_ENCODING,
    PatchProposalError,
    load_patch_proposal,
    materialize_patch_proposal,
    validate_patch_proposal,
)


APPROVED = {
    "tools/pai_runtime_runner/patch_proposal.py",
    "tests/test_pai_runtime_patch_proposal.py",
}


class PaiRuntimePatchProposalTests(unittest.TestCase):
    def _proposal(self, path: str = "tools/pai_runtime_runner/patch_proposal.py", content: str = "value = 1\n") -> dict[str, object]:
        return {
            "proposal_id": "s15f-patch-proposal",
            "proposal_kind": "full-file-replacement",
            "changes": [
                {
                    "path": path,
                    "mode": "replace-file",
                    "content": content,
                    "unified_diff": "--- a/file\n+++ b/file\n",
                }
            ],
        }

    def test_patch_proposal_text_encoding_is_explicit(self):
        self.assertEqual(PATCH_PROPOSAL_TEXT_ENCODING, "utf-8")

    def test_patch_proposal_accepts_full_file_replacement_inside_write_set(self):
        self.assertEqual(validate_patch_proposal(self._proposal(), APPROVED), [])

    def test_patch_proposal_rejects_absolute_path(self):
        errors = validate_patch_proposal(self._proposal("/tmp/outside.py"), APPROVED)
        self.assertTrue(any("absolute" in error for error in errors))

    def test_patch_proposal_rejects_path_traversal(self):
        errors = validate_patch_proposal(self._proposal("../outside.py"), APPROVED)
        self.assertTrue(any("path traversal" in error for error in errors))

    def test_patch_proposal_rejects_unapproved_repository_path(self):
        errors = validate_patch_proposal(self._proposal("README.md"), APPROVED)
        self.assertTrue(any("approved_write_set" in error for error in errors))

    def test_patch_proposal_rejects_root_agents(self):
        errors = validate_patch_proposal(self._proposal("AGENTS.md"), APPROVED | {"AGENTS.md"})
        self.assertTrue(any("AGENTS.md" in error for error in errors))

    def test_patch_proposal_rejects_dotcodex(self):
        errors = validate_patch_proposal(self._proposal(".codex/config.toml"), APPROVED | {".codex/config.toml"})
        self.assertTrue(any(".codex" in error for error in errors))

    def test_patch_proposal_materializes_only_approved_files(self):
        with tempfile.TemporaryDirectory(prefix="s15f.patch.") as tmp:
            repo = Path(tmp)
            applied = materialize_patch_proposal(self._proposal(), repo, APPROVED)
            self.assertEqual(applied, ["tools/pai_runtime_runner/patch_proposal.py"])
            self.assertEqual((repo / "tools/pai_runtime_runner/patch_proposal.py").read_text(encoding="utf-8"), "value = 1\n")
            self.assertFalse((repo / "README.md").exists())

    def test_patch_proposal_records_applied_paths(self):
        with tempfile.TemporaryDirectory(prefix="s15f.patch.") as tmp:
            repo = Path(tmp)
            proposal = self._proposal("tests/test_pai_runtime_patch_proposal.py", "import unittest\n")
            applied = materialize_patch_proposal(proposal, repo, APPROVED)
            self.assertEqual(applied, ["tests/test_pai_runtime_patch_proposal.py"])

    def test_patch_proposal_rejects_binary_content(self):
        errors = validate_patch_proposal(self._proposal(content="abc\x00def"), APPROVED)
        self.assertTrue(any("binary" in error for error in errors))

    def test_load_patch_proposal_reads_json_object(self):
        with tempfile.TemporaryDirectory(prefix="s15f.patch.") as tmp:
            path = Path(tmp) / "patch-proposal.json"
            path.write_text(json.dumps(self._proposal()) + "\n", encoding="utf-8")
            self.assertEqual(load_patch_proposal(path)["proposal_id"], "s15f-patch-proposal")

    def test_materialize_rejects_invalid_proposal(self):
        with tempfile.TemporaryDirectory(prefix="s15f.patch.") as tmp:
            with self.assertRaises(PatchProposalError):
                materialize_patch_proposal(self._proposal("README.md"), Path(tmp), APPROVED)


if __name__ == "__main__":
    unittest.main()
