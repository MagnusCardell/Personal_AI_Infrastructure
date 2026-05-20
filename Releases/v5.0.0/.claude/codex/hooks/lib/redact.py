from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import hashlib
import math
import re
from typing import Any


REDACTED = "[REDACTED]"


@dataclass(frozen=True)
class PatternRule:
    name: str
    pattern: re.Pattern[str]


SECRET_DIR_PATTERN = re.compile(
    r"(?i)(?:~|\$HOME|\$\{HOME\}|/home/[A-Za-z0-9_.-]+)/(?:\.(?:ssh|gnupg|aws)|\.config/(?:gcloud)|\.codex/auth\.json|\.claude/\.env)(?:/[^\s\"'`<>]*)?"
)

PATTERNS: tuple[PatternRule, ...] = (
    PatternRule("private_key_block", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----", re.I | re.S)),
    PatternRule("anthropic_token", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b")),
    PatternRule("openai_token", re.compile(r"\bsk-(?!ant-)[A-Za-z0-9_-]{20,}\b")),
    PatternRule("github_token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b")),
    PatternRule("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    PatternRule("bearer_token", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}")),
    PatternRule("authorization_header", re.compile(r"(?im)^(\s*Authorization\s*:\s*)(.+)$")),
    PatternRule("url_credentials", re.compile(r"\b([a-z][a-z0-9+.-]*://)([^/\s:@]{1,128}):([^@\s/]{1,128})@")),
    PatternRule("cookie_session", re.compile(r"(?i)\b(cookie|set-cookie|session(?:id)?|sid)\s*[:=]\s*[^\s;,]{8,}")),
    PatternRule("generic_secret_kv", re.compile(r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key|private[_-]?key|client[_-]?secret)\s*[:=]\s*[^\s\"'`,;]{6,}")),
    PatternRule("ssh_key_material", re.compile(r"\bssh-(?:rsa|ed25519|ecdsa)\s+[A-Za-z0-9+/=]{32,}(?:\s+\S+)?")),
    PatternRule("secret_path", SECRET_DIR_PATTERN),
    PatternRule("email", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
)

HIGH_ENTROPY_PATTERN = re.compile(r"\b[A-Za-z0-9+/=_-]{48,}\b")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def entropy(text: str) -> float:
    if not text:
        return 0.0
    total = len(text)
    counts = {char: text.count(char) for char in set(text)}
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def _replacement(name: str) -> str:
    return f"{REDACTED}:{name}"


def redact_text(text: str | None, *, max_length: int | None = None) -> tuple[str, dict[str, Any]]:
    source = "" if text is None else str(text)
    counts: dict[str, int] = {}
    redacted = source

    for rule in PATTERNS:
        def repl(match: re.Match[str]) -> str:
            counts[rule.name] = counts.get(rule.name, 0) + 1
            if rule.name == "authorization_header":
                return f"{match.group(1)}{_replacement(rule.name)}"
            if rule.name == "url_credentials":
                return f"{match.group(1)}{_replacement(rule.name)}@"
            return _replacement(rule.name)

        redacted = rule.pattern.sub(repl, redacted)

    def entropy_repl(match: re.Match[str]) -> str:
        value = match.group(0)
        if entropy(value) >= 4.0:
            counts["high_entropy"] = counts.get("high_entropy", 0) + 1
            return _replacement("high_entropy")
        return value

    redacted = HIGH_ENTROPY_PATTERN.sub(entropy_repl, redacted)
    truncated = False
    if max_length is not None and len(redacted) > max_length:
        omitted = len(redacted) - max_length
        redacted = redacted[:max_length].rstrip() + f"...[truncated:{omitted}]"
        truncated = True

    return redacted, {
        "input_chars": len(source),
        "output_chars": len(redacted),
        "redacted": bool(counts),
        "redaction_counts": counts,
        "truncated": truncated,
    }


def redact_obj(value: Any) -> tuple[Any, dict[str, Any]]:
    counts: dict[str, int] = {}

    def merge(meta: Mapping[str, Any]) -> None:
        for key, count in dict(meta.get("redaction_counts") or {}).items():
            counts[key] = counts.get(key, 0) + int(count)

    def walk(item: Any) -> Any:
        if isinstance(item, str):
            redacted, meta = redact_text(item)
            merge(meta)
            return redacted
        if isinstance(item, Mapping):
            return {str(key): walk(val) for key, val in item.items()}
        if isinstance(item, Sequence) and not isinstance(item, (bytes, bytearray, str)):
            return [walk(val) for val in item]
        return item

    redacted = walk(value)
    return redacted, {"redacted": bool(counts), "redaction_counts": counts}


def risk_flags(text: str | None) -> dict[str, bool]:
    value = "" if text is None else str(text)
    low = value.lower()
    return {
        "contains_url": bool(re.search(r"\b[a-z][a-z0-9+.-]*://", value, re.I)),
        "contains_url_credentials": bool(re.search(r"\b[a-z][a-z0-9+.-]*://[^/\s:@]+:[^@\s/]+@", value, re.I)),
        "contains_secret_like": redact_text(value)[1]["redacted"],
        "contains_secret_path": bool(SECRET_DIR_PATTERN.search(value)),
        "mentions_pai": ".claude/pai" in low or "/pai/" in low,
        "mentions_memory_work": "memory/work" in low,
        "mentions_isa": "isa.md" in low,
        "mentions_network_fetch": bool(re.search(r"\b(curl|wget|httpie|fetch)\b", low)),
        "mentions_shell_eval": bool(re.search(r"\beval\s+\$\(", low)),
        "mentions_recursive_force_delete": bool(re.search(r"\brm\s+-[^\n;]*r[^\n;]*f", low)),
    }


def text_facts(text: str | None) -> dict[str, Any]:
    value = "" if text is None else str(text)
    _, meta = redact_text(value)
    return {
        "chars": len(value),
        "lines": value.count("\n") + (1 if value else 0),
        "sha256": sha256_text(value) if value else None,
        "redaction": meta,
        "risk_flags": risk_flags(value),
    }


def safe_preview(text: str | None, *, max_length: int = 160, enabled: bool = False) -> str | None:
    if not enabled:
        return None
    preview, _ = redact_text(text or "", max_length=max_length)
    return preview


def prompt_features(prompt: str | None) -> dict[str, Any]:
    value = "" if prompt is None else str(prompt)
    low = re.sub(r"\s+", " ", value.lower()).strip()
    return {
        "chars": len(value),
        "words": len(re.findall(r"\S+", value)),
        "lines": value.count("\n") + (1 if value else 0),
        "sha256": sha256_text(value) if value else None,
        "has_question": "?" in value,
        "risk_flags": risk_flags(value),
        "terms": {
            "identity": any(term in low for term in ("who am i", "my identity", "principal identity")),
            "projects": any(term in low for term in ("active projects", "my projects", "project list")),
            "state": any(term in low for term in ("summarize state", "summarise state", "status", "show", "list", "inspect")),
            "algorithm": any(term in low for term in ("algorithm run", "start an algorithm", "run the algorithm")),
            "execution": any(term in low for term in ("run", "implement", "build", "fix", "design", "investigate", "plan", "verify", "refactor", "ship")),
            "high_stakes": any(term in low for term in ("irreversible", "credential", "secret", "token", "payment", "legal", "medical", "financial")),
            "strategic": any(term in low for term in ("architecture", "migration", "release", "runtime", "cross-system", "strategy")),
        },
    }
