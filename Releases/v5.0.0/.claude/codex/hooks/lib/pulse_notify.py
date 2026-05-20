from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_PULSE_URL = "http://localhost:31337"
NOTIFY_ENDPOINT = "/notify"
TIMEOUT_SECONDS = 0.5
TRUE_VALUES = {"1", "true", "yes", "on"}
DEFAULT_VOICE_EVENTS = {"turn_complete"}
EVENT_ALIASES: dict[str, set[str]] = {
    "codex.turn.complete": {"codex.turn.complete", "codex_turn_complete", "turn_complete"},
    "codex.algorithm.isa_updated": {
        "codex.algorithm.isa_updated",
        "codex_algorithm_isa_updated",
        "algorithm_isa_updated",
        "isa_updated",
    },
}
DEFAULT_VOICE_MESSAGES = {
    "codex.turn.complete": "PAI Codex turn complete.",
    "codex.algorithm.isa_updated": "PAI Codex ISA updated.",
}
VOICE_MESSAGE_ENV = {
    "codex.turn.complete": "PAI_CODEX_VOICE_MESSAGE_TURN_COMPLETE",
    "codex.algorithm.isa_updated": "PAI_CODEX_VOICE_MESSAGE_ISA_UPDATED",
}
SECRET_LIKE = (
    re.compile(r"\b" + "sk" + r"-(?:ant-)?[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{12,}\b"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key|client[_-]?secret)\s*[:=]\s*[^\s\"'`,;]{6,}"),
    re.compile(r"\b([a-z][a-z0-9+.-]*://)([^/\s:@]{1,128}):([^@\s/]{1,128})@"),
)


def pulse_enabled() -> bool:
    value = os.environ.get("PAI_CODEX_PULSE_ENABLED", "")
    return value.lower() in TRUE_VALUES


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


def _normal_event_token(value: str) -> str:
    return value.strip().lower().replace("-", "_")


def _voice_enabled() -> bool:
    value = os.environ.get("PAI_CODEX_VOICE_ENABLED", "")
    return value.lower() in TRUE_VALUES


def _voice_event_tokens() -> set[str]:
    raw = os.environ.get("PAI_CODEX_VOICE_EVENTS", "").strip()
    if not raw:
        return set(DEFAULT_VOICE_EVENTS)
    return {_normal_event_token(token) for token in re.split(r"[\s,]+", raw) if token.strip()}


def _event_tokens(event: str) -> set[str]:
    aliases = set(EVENT_ALIASES.get(event, {event}))
    aliases.add(_normal_event_token(event))
    return aliases


def _safe_voice_id() -> str | None:
    raw = os.environ.get("PAI_CODEX_VOICE_ID", "").strip()
    if not raw:
        return None
    if re.fullmatch(r"[A-Za-z0-9_-]{1,128}", raw):
        return raw
    return None


def _safe_voice_message(event: str, fallback: str) -> str:
    raw = os.environ.get(VOICE_MESSAGE_ENV.get(event, ""), "").strip()
    message = raw or DEFAULT_VOICE_MESSAGES.get(event, fallback)
    if any(pattern.search(message) for pattern in SECRET_LIKE):
        return DEFAULT_VOICE_MESSAGES.get(event, fallback)
    message = re.sub(r"\s+", " ", message).strip()
    return message[:180] if message else DEFAULT_VOICE_MESSAGES.get(event, fallback)


def _voice_intent(event: str, fallback_message: str) -> dict[str, Any]:
    if not _voice_enabled():
        return {"voice_enabled": False}
    selected = _voice_event_tokens()
    if "*" not in selected and "all" not in selected and not (_event_tokens(event) & selected):
        return {"voice_enabled": False}
    intent: dict[str, Any] = {
        "voice_enabled": True,
        "message": _safe_voice_message(event, fallback_message),
    }
    voice_id = _safe_voice_id()
    if voice_id:
        intent["voice_id"] = voice_id
    return intent


def _payload(event: str, message: str, *, source: str, details: dict[str, Any] | None) -> dict[str, Any]:
    voice = _voice_intent(event, message)
    payload: dict[str, Any] = {
        "source": source,
        "event": event,
        "message": str(voice.get("message") or message),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "voice_enabled": bool(voice["voice_enabled"]),
    }
    if voice.get("voice_id"):
        payload["voice_id"] = voice["voice_id"]
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
