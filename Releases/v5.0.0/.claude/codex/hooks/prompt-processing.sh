#!/usr/bin/env bash
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAI_DIR="${PAI_DIR:-$HOME/.claude/PAI}"
OBS_DIR="$PAI_DIR/MEMORY/OBSERVABILITY"
mkdir -p "$OBS_DIR"
export PYTHONPATH="$HOOK_DIR/lib${PYTHONPATH:+:$PYTHONPATH}"

TMP_INPUT="$(mktemp "${TMPDIR:-/tmp}/pai-codex-prompt.XXXXXX")"
trap 'rm -f "$TMP_INPUT"' EXIT
cat > "$TMP_INPUT"

python3 - "$TMP_INPUT" "$OBS_DIR/codex-prompt-classification.jsonl" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import os
import re
import sys

from log_event import append_jsonl, load_json_file, now, safe_error
from redact import prompt_features

input_path = Path(sys.argv[1])
log_path = Path(sys.argv[2]).expanduser()
MODES = {"MINIMAL", "NATIVE", "ALGORITHM"}
TIERS = {"E1", "E2", "E3", "E4", "E5"}


def extract_prompt(payload: dict) -> str:
    for key in ("prompt", "user_prompt", "input", "text"):
        value = payload.get(key)
        if isinstance(value, str):
            return value
    message = payload.get("message")
    if isinstance(message, dict) and isinstance(message.get("content"), str):
        return message["content"]
    return ""


def classify_local(prompt: str) -> tuple[str, str, str]:
    compact = re.sub(r"\s+", " ", prompt.strip().lower()).strip()
    minimal_patterns = [
        r"^(hi|hello|hey|thanks|thank you|thx|ok|okay|yep|yes|no|nice|cool)[!.? ]*$",
        r"^(what\?|why\?|how\?|which one\?|say more|clarify|can you clarify)[!.? ]*$",
    ]
    if len(compact) <= 80 and any(re.match(pattern, compact) for pattern in minimal_patterns):
        return "MINIMAL", "E1", "short conversational prompt"

    native_terms = [
        "who am i",
        "what are my projects",
        "active projects",
        "my active projects",
        "summarize state",
        "summarise state",
        "status",
        "list",
        "show",
        "inspect",
        "what is my",
        "tell me about my",
        "telos",
        "learning entry",
    ]
    algorithm_terms = [
        "run",
        "implement",
        "build",
        "fix",
        "design",
        "investigate",
        "debug",
        "plan",
        "start an algorithm run",
        "algorithm run",
        "execute",
        "create",
        "write",
        "modify",
        "edit",
        "refactor",
        "verify",
        "test",
        "ship",
    ]

    if any(term in compact for term in algorithm_terms):
        mode = "ALGORITHM"
        reason = "execution or implementation intent"
    elif any(term in compact for term in native_terms):
        mode = "NATIVE"
        reason = "live PAI state or status query"
    elif compact.endswith("?") and len(compact) < 240:
        mode = "NATIVE"
        reason = "bounded informational question"
    else:
        mode = "ALGORITHM"
        reason = "non-trivial request by default"

    high_stakes = [
        "irreversible",
        "credential",
        "secret",
        "token",
        "payment",
        "legal",
        "medical",
        "financial",
        "delete",
        "destroy",
    ]
    strategic = ["strategy", "architecture", "cross-system", "migration", "release", "replace", "runtime", "multi-repo", "external"]
    simple = ["pwd", "single file", "one file", "tiny", "small", "quick", "e1", "harmless"]
    bounded = ["bounded", "multi-step", "couple", "few files", "e2"]

    if mode in {"MINIMAL", "NATIVE"}:
        tier = "E1"
    elif any(term in compact for term in high_stakes):
        tier = "E5" if any(term in compact for term in ["irreversible", "credential", "secret", "token", "payment"]) else "E4"
    elif any(term in compact for term in strategic):
        tier = "E4"
    elif any(term in compact for term in simple):
        tier = "E1"
    elif any(term in compact for term in bounded):
        tier = "E2"
    else:
        tier = "E3"
    return mode, tier, reason


try:
    payload = load_json_file(input_path)
    prompt = extract_prompt(payload)
    mode, tier, reason = classify_local(prompt)
    if mode not in MODES or tier not in TIERS:
        mode, tier, reason = "ALGORITHM", "E3", "classifier invariant fallback"

    classifier = "local_deterministic"
    privacy = "raw_prompt_not_logged_or_forwarded"
    additional = "\n".join(
        [
            f"PAI_MODE={mode}",
            f"PAI_TIER={tier}",
            f"PAI_CLASSIFIER={classifier}",
            f"PAI_PRIVACY={privacy}",
            f"PAI_REASON={reason}",
            "",
        ]
    )

    append_jsonl(
        log_path,
        {
            "timestamp": now(),
            "hook_event_name": "UserPromptSubmit",
            "cwd": payload.get("cwd") or os.getcwd(),
            "turn_id": payload.get("turn_id") or payload.get("turnId"),
            "mode": mode,
            "tier": tier,
            "reason": reason,
            "classifier": classifier,
            "privacy": privacy,
            "prompt_features": prompt_features(prompt),
            "model_inference_used": False,
            "raw_prompt_forwarded": False,
        },
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": additional}}))
except Exception as exc:
    try:
        append_jsonl(
            log_path,
            {
                "timestamp": now(),
                "hook_event_name": "UserPromptSubmit",
                "error": safe_error(exc),
                "mode": "ALGORITHM",
                "tier": "E3",
                "classifier": "local_deterministic_error_fallback",
                "privacy": "raw_prompt_not_logged_or_forwarded",
            },
        )
    except Exception:
        pass
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "PAI_MODE=ALGORITHM\nPAI_TIER=E3\nPAI_CLASSIFIER=local_deterministic_error_fallback\nPAI_PRIVACY=raw_prompt_not_logged_or_forwarded\nPAI_REASON=classifier error fallback\n"}}))
PY
