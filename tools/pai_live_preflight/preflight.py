"""Fixture-only preflight metadata checks.

The module performs shallow metadata probes only. It does not read file bodies,
does not inspect live installed state, and does not invoke runtime services.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from .consent import APPROVED_DECLARED_SOURCE_ROOT, validate_consent_artifact
from .path_safety import HIGH_LEVEL_STRUCTURAL_METADATA_CHECK, ensure_allowed_probe, redact_path, resolve_fixture_root


STRUCTURAL_METADATA_PROBES = (
    ("PAI_SYSTEM_PROMPT.md", "file"),
    ("Memory", "directory"),
    ("Memory/WORK", "directory"),
    ("Memory/LEARNING", "directory"),
    ("Memory/KNOWLEDGE", "directory"),
    ("ISA", "directory"),
    ("Pulse", "directory"),
    ("Pulse/events", "directory"),
)


def _metadata_result(root: Path, relative_path: str, expected_type: str) -> dict[str, object]:
    candidate = ensure_allowed_probe(root, relative_path, HIGH_LEVEL_STRUCTURAL_METADATA_CHECK)
    exists = candidate.exists()
    if expected_type == "directory":
        type_ok = candidate.is_dir()
    elif expected_type == "file":
        type_ok = candidate.is_file()
    else:
        type_ok = False
    return {
        "relative_path": relative_path,
        "expected_type": expected_type,
        "exists": exists,
        "type_matches": bool(exists and type_ok),
        "readable_metadata_only": bool(exists and os.access(candidate, os.R_OK)),
    }


def run_fixture_preflight(
    *,
    fixture_root: str | Path,
    consent_path: str | Path,
    declared_source_root: str,
    extra_metadata_paths: Iterable[str] = (),
) -> dict[str, object]:
    consent = validate_consent_artifact(consent_path, declared_source_root)
    resolved_root = resolve_fixture_root(fixture_root)

    structural_check_results = [
        _metadata_result(resolved_root, relative_path, expected_type)
        for relative_path, expected_type in STRUCTURAL_METADATA_PROBES
    ]

    for relative_path in extra_metadata_paths:
        ensure_allowed_probe(resolved_root, relative_path, HIGH_LEVEL_STRUCTURAL_METADATA_CHECK)

    pai_prompt = next(
        result for result in structural_check_results if result["relative_path"] == "PAI_SYSTEM_PROMPT.md"
    )
    pai_dir_candidate_result = {
        "declared_future_live_source_root": APPROVED_DECLARED_SOURCE_ROOT,
        "fixture_root_label": "fixture-root-redacted",
        "fixture_root_is_not_live_installed_state": True,
        "candidate_supported_by_fixture_metadata": bool(pai_prompt["type_matches"]),
    }

    return {
        "milestone_name": "V5-S14C-LIVE-PREFLIGHT-FIXTURE-IMPLEMENTATION",
        "consent_status": consent.consent_status,
        "source_root_label": "fixture-root-redacted",
        "source_root_redacted_display_path": redact_path(resolved_root),
        "declared_source_root": declared_source_root,
        "pai_dir_candidate_result": pai_dir_candidate_result,
        "structural_check_results": structural_check_results,
        "forbidden_target_exclusion_results": {
            "status": "pass-no-forbidden-targets-read",
            "checked_without_content_body_reads": True,
            "forbidden_targets": [
                "~/.claude/projects/**",
                "~/.claude/projects/**/memory",
                "~/.codex/**",
                "~/.codex/memories/**",
                "PAI Memory content bodies",
                "ISA content bodies",
                "Pulse event payload bodies",
            ],
        },
        "pulse_not_probed_confirmation": True,
        "memory_not_read_confirmation": True,
        "isa_not_read_confirmation": True,
        "no_residue_result": {
            "fixture_preflight_writes": "none",
            "live_installed_state_touched": False,
            "runtime_surfaces_created": False,
        },
        "abort_status": "not-aborted",
        "known_risks": [
            "fixture-only evidence cannot prove live installed PAI readability",
            "fixture-only evidence is not replacement readiness evidence",
        ],
        "evidence_classification": {
            "fixture evidence": True,
            "non-canonical evidence": True,
            "not personal live-state evidence": True,
            "not proof of runtime adapter correctness": True,
            "not proof of Claude equivalence": True,
            "not proof of replacement readiness": True,
            "not proof that Codex can replace Claude": True,
            "not proof that installed PAI state is safe to migrate": True,
        },
    }
