from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json
import os

from redact import redact_obj, safe_preview, sha256_text, text_facts


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def debug_raw_enabled() -> bool:
    return os.environ.get("PAI_CODEX_DEBUG_RAW_LOGS", "").lower() in {"1", "true", "yes", "on"}


def load_json_file(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    if not raw.strip():
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        payload: dict[str, Any] = {
            "_parse_error": str(exc),
            "input_sha256": sha256_text(raw),
            "input_chars": len(raw),
        }
        preview = safe_preview(raw, max_length=240, enabled=debug_raw_enabled())
        if preview is not None:
            payload["redacted_preview"] = preview
        return payload
    if isinstance(value, dict):
        return value
    return {"_non_object_input": True, "input": text_facts(raw)}


def append_jsonl(path: Path, entry: dict[str, Any]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    redacted, meta = redact_obj(entry)
    if isinstance(redacted, dict):
        redacted.setdefault("safe_logging", True)
        redacted.setdefault("redaction", meta)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(redacted, sort_keys=True) + "\n")
    return meta


def safe_error(exc: BaseException) -> dict[str, Any]:
    message = safe_preview(str(exc), max_length=240, enabled=True) or exc.__class__.__name__
    return {"type": exc.__class__.__name__, "message": message}
