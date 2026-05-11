"""Report writer for fixture-only S14C preflight evidence."""

from __future__ import annotations

import json
from pathlib import Path

from .path_safety import is_within_root, reject_path_traversal


class PreflightReportError(ValueError):
    """Raised when the fixture-only report path is outside the approved output root."""


def write_report(report: dict[str, object], output_root: str | Path, output_path: str | Path) -> Path:
    approved_output_root = Path(output_root)
    report_path = Path(output_path)

    reject_path_traversal(approved_output_root, allow_absolute=True)
    reject_path_traversal(report_path, allow_absolute=True)

    resolved_output_root = approved_output_root.resolve(strict=False)
    resolved_report_path = report_path.resolve(strict=False)
    if not is_within_root(resolved_output_root, resolved_report_path):
        raise PreflightReportError("writes outside an explicitly approved output root are rejected")

    resolved_output_root.mkdir(parents=True, exist_ok=True)
    resolved_report_path.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(report)
    payload.setdefault("report_mode", "fixture-only non-canonical")
    payload["source_root_redacted_display_path"] = str(payload.get("source_root_redacted_display_path", "<redacted>"))
    resolved_report_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return resolved_report_path
