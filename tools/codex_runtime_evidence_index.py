#!/usr/bin/env python3
"""Print a sanitized index of Codex PAI runtime evidence paths.

The index reports existence and file metadata only. It deliberately does not
read or print evidence file bodies, because live PAI evidence can contain
private runtime context.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class EvidenceItem:
    phase: str
    label: str
    path: str
    kind: str = "pai"


EVIDENCE_ITEMS = [
    EvidenceItem("S17A0", "Native hook probe", "MEMORY/OBSERVABILITY/codex-runtime-probe-summary.md"),
    EvidenceItem("S17A", "Runtime MVP evidence", "MEMORY/OBSERVABILITY/s17a-runtime-mvp-evidence.md"),
    EvidenceItem("S17B", "Live ISA write evidence", "MEMORY/OBSERVABILITY/s17b-live-write-evidence.md"),
    EvidenceItem("S17C", "Full Algorithm evidence", "MEMORY/OBSERVABILITY/s17c-full-algorithm-evidence.md"),
    EvidenceItem("S17C", "Full Algorithm learning", "MEMORY/LEARNING/ALGORITHM/2026-05/2026-05-19-085500_LEARNING_s17c-codex-native-runtime.md"),
    EvidenceItem("S17D0", "Baseline manifest", "MEMORY/OBSERVABILITY/s17d0-runtime-baseline-manifest.json"),
    EvidenceItem("S17D0", "Regression evidence", "MEMORY/OBSERVABILITY/s17d0-regression-evidence.md"),
    EvidenceItem("S17D1", "Skills evidence", "MEMORY/OBSERVABILITY/s17d-skills-evidence.md"),
    EvidenceItem("S17D2", "Read-only agents evidence", "MEMORY/OBSERVABILITY/s17d-subagents-evidence.md"),
    EvidenceItem("S17E0", "Baseline manifest", "MEMORY/OBSERVABILITY/s17e0-runtime-baseline-manifest.json"),
    EvidenceItem("S17E0", "Regression evidence", "MEMORY/OBSERVABILITY/s17e0-regression-evidence.md"),
    EvidenceItem("S17E1", "Prompt privacy evidence", "MEMORY/OBSERVABILITY/s17e1-prompt-privacy-evidence.md"),
    EvidenceItem("S17E2", "Redaction evidence", "MEMORY/OBSERVABILITY/s17e2-redaction-evidence.md"),
    EvidenceItem("S17E3", "Writable-root evidence", "MEMORY/OBSERVABILITY/s17e3-writable-root-evidence.md"),
    EvidenceItem("S17E3", "Profile C ISA", "MEMORY/WORK/s17e3-profile-c-privacy-containment/ISA.md"),
    EvidenceItem("S17E4", "Read-only agent enforcement", "MEMORY/OBSERVABILITY/s17e4-readonly-agent-enforcement.md"),
    EvidenceItem("S17E5", "Hook coverage matrix", "MEMORY/OBSERVABILITY/s17e5-hook-coverage-matrix.md"),
    EvidenceItem("S18A0", "Baseline check", "MEMORY/OBSERVABILITY/s18a0-baseline-check.md"),
    EvidenceItem("S18A1", "E1 trial evidence", "MEMORY/OBSERVABILITY/s18a1-e1-trial.md"),
    EvidenceItem("S18A2", "E2 trial evidence", "MEMORY/OBSERVABILITY/s18a2-e2-trial.md"),
    EvidenceItem("S18A2", "E2 trial ISA", "MEMORY/WORK/20260520-082915_s18a2-codex-evidence-index/ISA.md"),
    EvidenceItem("S18A3", "E3 trial evidence", "MEMORY/OBSERVABILITY/s18a3-e3-trial.md"),
    EvidenceItem("S18A4", "Replacement-grade evaluation", "MEMORY/OBSERVABILITY/s18a-replacement-grade-evaluation.md"),
    EvidenceItem("S17", "Runtime architecture doc", "docs/architecture/V5-S17-CODEX-AS-PAI-RUNTIME.md", "repo"),
    EvidenceItem("S17D", "Skills and agents architecture doc", "docs/architecture/V5-S17D-CODEX-NATIVE-SKILLS-AND-SUBAGENTS.md", "repo"),
    EvidenceItem("S17E", "Hardening architecture doc", "docs/architecture/V5-S17E-CODEX-RUNTIME-HARDENING.md", "repo"),
    EvidenceItem("S18A", "Primary runtime trial architecture doc", "docs/architecture/V5-S18A-CODEX-PRIMARY-RUNTIME-TRIAL.md", "repo"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    parser.add_argument(
        "--phase",
        action="append",
        default=[],
        help="filter by exact phase prefix, for example S17E or S18A",
    )
    parser.add_argument(
        "--pai-dir",
        default=os.environ.get("PAI_DIR", str(Path.home() / ".claude" / "PAI")),
        help="live PAI root; defaults to $PAI_DIR or ~/.claude/PAI",
    )
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="repository root for repo documentation paths",
    )
    return parser.parse_args()


def select_items(items: Iterable[EvidenceItem], phase_filters: list[str]) -> list[EvidenceItem]:
    if not phase_filters:
        return list(items)
    return [item for item in items if any(item.phase.startswith(prefix) for prefix in phase_filters)]


def resolve_path(item: EvidenceItem, pai_dir: Path, repo_root: Path) -> Path:
    if item.kind == "repo":
        return repo_root / item.path
    return pai_dir / item.path


def display_path(item: EvidenceItem, pai_dir: Path) -> str:
    if item.kind == "repo":
        return item.path
    return "~/.claude/PAI/" + item.path


def stat_item(item: EvidenceItem, pai_dir: Path, repo_root: Path) -> dict[str, object]:
    actual_path = resolve_path(item, pai_dir, repo_root)
    exists = actual_path.exists()
    metadata: dict[str, object] = {
        "phase": item.phase,
        "label": item.label,
        "kind": item.kind,
        "path": display_path(item, pai_dir),
        "exists": exists,
    }
    if exists:
        stat = actual_path.stat()
        metadata.update(
            {
                "bytes": stat.st_size,
                "mtime_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc)
                .replace(microsecond=0)
                .isoformat()
                .replace("+00:00", "Z"),
            }
        )
    return metadata


def emit_markdown(rows: list[dict[str, object]]) -> None:
    print("# Codex PAI Runtime Evidence Index")
    print()
    print("This index reports paths and file metadata only. It does not read evidence bodies.")
    print()
    print("| phase | label | exists | bytes | mtime UTC | path |")
    print("| --- | --- | --- | ---: | --- | --- |")
    for row in rows:
        bytes_value = row.get("bytes", "")
        mtime = row.get("mtime_utc", "")
        print(
            f"| {row['phase']} | {row['label']} | {str(row['exists']).lower()} | "
            f"{bytes_value} | {mtime} | `{row['path']}` |"
        )


def main() -> int:
    args = parse_args()
    pai_dir = Path(args.pai_dir).expanduser()
    repo_root = Path(args.repo_root).expanduser()
    items = select_items(EVIDENCE_ITEMS, args.phase)
    rows = [stat_item(item, pai_dir, repo_root) for item in items]
    payload = {
        "schema": "pai.codex_runtime_evidence_index.v1",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "pai_dir": "~/.claude/PAI" if pai_dir == Path.home() / ".claude" / "PAI" else str(pai_dir),
        "repo_root": str(repo_root),
        "items": rows,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        emit_markdown(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
