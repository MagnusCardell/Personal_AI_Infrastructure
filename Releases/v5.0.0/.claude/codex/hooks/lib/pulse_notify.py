from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import json
import os
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_PULSE_URL = "http://localhost:31337"
NOTIFY_ENDPOINT = "/notify"
TIMEOUT_SECONDS = 0.5


def pulse_enabled() -> bool:
    value = os.environ.get("PAI_CODEX_PULSE_ENABLED", "")
    return value.lower() in {"1", "true", "yes", "on"}


def pulse_url() -> str:
    value = os.environ.get("PAI_CODEX_PULSE_URL", "").strip()
    return value or DEFAULT_PULSE_URL


def _safe_url(base_url: str) -> str:
    parsed = urllib.parse.urlsplit(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Pulse URL must be http(s)")
    if "@" in parsed.netloc:
        raise ValueError("Pulse URL must not contain credentials")
    clean = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", ""))
    return clean.rstrip("/") + NOTIFY_ENDPOINT


def _payload(event: str, message: str, *, source: str, details: dict[str, Any] | None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "source": source,
        "event": event,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if details:
        payload["details"] = details
    return payload


def notify(event: str, message: str, *, source: str = "pai-codex", details: dict[str, Any] | None = None) -> dict[str, Any]:
    if not pulse_enabled():
        return {"enabled": False, "attempted": False, "success": False, "reason": "disabled"}

    try:
        endpoint = _safe_url(pulse_url())
        body = json.dumps(_payload(event, message, source=source, details=details), sort_keys=True).encode("utf-8")
        request = urllib.request.Request(
            endpoint,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return {
                "enabled": True,
                "attempted": True,
                "success": 200 <= int(response.status) < 300,
                "status": int(response.status),
            }
    except (OSError, TimeoutError, ValueError, urllib.error.URLError, urllib.error.HTTPError) as exc:
        return {
            "enabled": True,
            "attempted": True,
            "success": False,
            "error_type": exc.__class__.__name__,
        }
