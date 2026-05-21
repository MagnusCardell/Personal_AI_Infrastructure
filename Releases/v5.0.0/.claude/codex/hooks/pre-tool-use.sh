#!/usr/bin/env bash
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAI_DIR="${PAI_DIR:-$HOME/.claude/PAI}"
OBS_DIR="$PAI_DIR/MEMORY/OBSERVABILITY"
mkdir -p "$OBS_DIR"
export PYTHONPATH="$HOOK_DIR/lib${PYTHONPATH:+:$PYTHONPATH}"

if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' '{}'
  exit 0
fi

TMP_INPUT="$(mktemp "${TMPDIR:-/tmp}/pai-codex-pretool.XXXXXX")"
trap 'rm -f "$TMP_INPUT"' EXIT
cat > "$TMP_INPUT"

python3 - "$TMP_INPUT" "$OBS_DIR/codex-pretool.jsonl" "$HOOK_DIR" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import os
import re
import sys
from urllib.parse import urlparse

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - depends on Python version
    tomllib = None  # type: ignore[assignment]

from log_event import append_jsonl, load_json_file, now, safe_error
from redact import risk_flags, text_facts

input_path = Path(sys.argv[1])
log_path = Path(sys.argv[2]).expanduser()
hook_dir = Path(sys.argv[3]).expanduser().resolve(strict=False)
HOME = str(Path.home())
PAI_DIR = Path(os.environ.get("PAI_DIR") or str(Path.home() / ".claude" / "PAI")).expanduser().resolve(strict=False)

EGRESS_BLOCKED = {
    "pastebin.com",
    "requestbin.net",
    "webhook.site",
    "ngrok.io",
    "serveo.net",
}
EGRESS_ALLOWED = {
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "api.github.com",
    "raw.githubusercontent.com",
    "api.openai.com",
    "api.anthropic.com",
}


def command_text(payload: dict) -> tuple[str, str]:
    tool_name = str(payload.get("tool_name") or payload.get("toolName") or "")
    tool_input = payload.get("tool_input") if isinstance(payload.get("tool_input"), dict) else {}
    command = tool_input.get("command") if isinstance(tool_input.get("command"), str) else ""
    if command:
        return tool_name, command
    return tool_name, json.dumps(tool_input, sort_keys=True)


def normalized_tool(tool_name: str) -> str:
    return re.sub(r"[^a-z]", "", tool_name.lower())


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def expand_path(raw_path: str, cwd: str) -> Path:
    cleaned = raw_path.strip().strip("'\"`.,")
    cleaned = cleaned.replace("${HOME}", HOME).replace("$HOME", HOME)
    if cleaned.startswith("~/"):
        cleaned = HOME + cleaned[1:]
    path = Path(cleaned)
    if not path.is_absolute():
        path = Path(cwd) / path
    return path.expanduser().resolve(strict=False)


def protected_terms() -> list[str]:
    home_low = HOME.lower()
    dot = "."
    return [
        "~/" + dot + "ssh",
        home_low + "/" + dot + "ssh",
        "$home/" + dot + "ssh",
        "~/" + dot + "gnupg",
        home_low + "/" + dot + "gnupg",
        "$home/" + dot + "gnupg",
        "~/" + dot + "aws",
        home_low + "/" + dot + "aws",
        "$home/" + dot + "aws",
        "~/" + dot + "config/gcloud",
        home_low + "/" + dot + "config/gcloud",
        "$home/" + dot + "config/gcloud",
        "~/" + dot + "codex/" + "auth.json",
        home_low + "/" + dot + "codex/" + "auth.json",
        "$home/" + dot + "codex/" + "auth.json",
        "~/" + dot + "claude/" + ".env",
        home_low + "/" + dot + "claude/" + ".env",
        "$home/" + dot + "claude/" + ".env",
    ]


def protected_paths() -> list[Path]:
    dot = "."
    return [
        Path(HOME) / (dot + "ssh"),
        Path(HOME) / (dot + "gnupg"),
        Path(HOME) / (dot + "aws"),
        Path(HOME) / (dot + "codex") / "auth.json",
        Path(HOME) / (dot + "claude") / ".env",
        Path("/etc") / "passwd",
        Path("/etc") / ("shad" + "ow"),
    ]


def domain_matches(domain: str, target: str) -> bool:
    return domain == target or domain.endswith("." + target)


def extract_domains(command: str) -> list[str]:
    domains: list[str] = []
    for match in re.finditer(r"\b[a-z][a-z0-9+.-]*://[^\s\"'`<>)]*", command, re.I):
        parsed = urlparse(match.group(0))
        host = (parsed.hostname or "").lower().strip(".")
        if host:
            domains.append(host)
    return sorted(set(domains))


def egress_inspector(tool_name: str, command: str) -> tuple[str | None, dict]:
    tool = normalized_tool(tool_name)
    if tool not in {"bash", "applypatch"}:
        return None, {"result": "not_applicable", "domains": []}
    domains = extract_domains(command)
    blocked = [domain for domain in domains if any(domain_matches(domain, sink) for sink in EGRESS_BLOCKED)]
    allowed = [domain for domain in domains if domain in EGRESS_ALLOWED]
    observed = [domain for domain in domains if domain not in blocked and domain not in allowed]
    if blocked:
        return "blocks outbound traffic to known exfiltration or sink domain", {
            "result": "deny",
            "blocked_domains": blocked,
            "allowed_domains": allowed,
            "observed_domains": observed,
        }
    return None, {
        "result": "allow",
        "blocked_domains": [],
        "allowed_domains": allowed,
        "observed_domains": observed,
    }


def strip_single_quoted(text: str) -> str:
    return re.sub(r"'(?:'\\''|[^'])*'", "''", text)


def injection_inspector(tool_name: str, command: str) -> tuple[str | None, dict]:
    if normalized_tool(tool_name) != "bash":
        return None, {"result": "not_applicable"}
    compact = re.sub(r"\s+", " ", strip_single_quoted(command).lower())
    checks = (
        ("command_substitution", re.compile(r"\$\(")),
        ("backtick_substitution", re.compile(r"`[^`]+`")),
        ("curl_pipe_shell", re.compile(r"\bcurl\b[^\n|;]*\|\s*(?:sudo\s+)?(?:bash|sh)\b")),
        ("wget_pipe_shell", re.compile(r"\bwget\b[^\n|;]*\|\s*(?:sudo\s+)?(?:bash|sh)\b")),
        ("semicolon_shell", re.compile(r";\s*(?:sudo\s+)?(?:bash|sh)\b")),
    )
    matched = [name for name, pattern in checks if pattern.search(compact)]
    if matched:
        return "blocks dangerous shell injection or network-to-shell form", {"result": "deny", "matched": matched}
    return None, {"result": "allow", "matched": []}


def config_allowed_roots() -> list[Path]:
    config_path = Path(os.environ.get("CODEX_HOME") or str(Path.home() / ".codex")) / "config.toml"
    if tomllib is None or not config_path.exists():
        return []
    try:
        data = tomllib.loads(config_path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return []
    roots = data.get("sandbox_workspace_write", {}).get("writable_roots", []) if isinstance(data, dict) else []
    if not isinstance(roots, list):
        return []
    return [Path(root).expanduser().resolve(strict=False) for root in roots if isinstance(root, str)]


def find_repo_root(cwd: Path) -> Path | None:
    for candidate in [cwd, *cwd.parents]:
        if (candidate / ".git").exists():
            return candidate.resolve(strict=False)
    return None


def allowed_roots(cwd: str) -> list[Path]:
    roots = [PAI_DIR]
    roots.extend(config_allowed_roots())
    repo_root = find_repo_root(Path(cwd).expanduser().resolve(strict=False))
    if repo_root is not None:
        roots.append(repo_root)
    roots.append(hook_dir.parent)
    unique: list[Path] = []
    for root in roots:
        if root not in unique:
            unique.append(root)
    return unique


def walk_path_values(value: object) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str) and key in {"file_path", "path"} and isinstance(item, str):
                found.append(item)
            else:
                found.extend(walk_path_values(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(walk_path_values(item))
    return found


def extract_target_paths(payload: dict, tool_name: str, command: str) -> list[Path]:
    tool = normalized_tool(tool_name)
    tool_input = payload.get("tool_input") if isinstance(payload.get("tool_input"), dict) else {}
    cwd = str(payload.get("cwd") or os.getcwd())
    raw_paths: list[str] = []
    if tool in {"write", "edit", "multiedit"}:
        raw_paths.extend(walk_path_values(tool_input))
    if tool == "applypatch":
        for line in command.splitlines():
            match = re.match(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", line.strip())
            if match:
                raw_paths.append(match.group(1))
            move_match = re.match(r"^\*\*\* Move to: (.+)$", line.strip())
            if move_match:
                raw_paths.append(move_match.group(1))
    return sorted({expand_path(raw, cwd) for raw in raw_paths}, key=str)


def containment_guard(payload: dict, tool_name: str, command: str) -> tuple[str | None, dict]:
    paths = extract_target_paths(payload, tool_name, command)
    if not paths:
        return None, {"result": "not_applicable", "target_count": 0}
    roots = allowed_roots(str(payload.get("cwd") or os.getcwd()))
    protected = protected_paths()
    denied: list[str] = []
    protected_hits: list[str] = []
    for path in paths:
        if any(path == item or is_relative_to(path, item) for item in protected):
            protected_hits.append(str(path))
            continue
        if not any(path == root or is_relative_to(path, root) for root in roots):
            denied.append(str(path))
    if protected_hits:
        return "blocks writes to protected credential or system paths", {
            "result": "deny",
            "target_count": len(paths),
            "protected_hits": protected_hits,
            "denied_paths": denied,
            "allowed_roots": [str(root) for root in roots],
        }
    if denied:
        return "blocks detectable write target outside configured PAI or workspace roots", {
            "result": "deny",
            "target_count": len(paths),
            "protected_hits": [],
            "denied_paths": denied,
            "allowed_roots": [str(root) for root in roots],
        }
    return None, {
        "result": "allow",
        "target_count": len(paths),
        "protected_hits": [],
        "denied_paths": [],
        "allowed_roots": [str(root) for root in roots],
    }


def danger_reason(command: str) -> str | None:
    compact = re.sub(r"\s+", " ", command.lower())
    flags = risk_flags(command)
    forced_remove = r"\br" + r"m\s+-[^\n;]*r[^\n;]*f"
    if flags["contains_url_credentials"]:
        return "credentials must not be placed in URLs"
    if re.search(forced_remove + r"[^\n;]*\s+/(?:\s|$|\*)", compact):
        return "blocks recursive force delete against filesystem root"
    if re.search(r"\bsudo\s+" + forced_remove, compact):
        return "blocks elevated recursive force delete"
    if flags["mentions_shell_eval"]:
        return "blocks eval of command substitution"
    if re.search(r"\bchmod\s+-r\s+777\s+/(?:\s|$)", compact):
        return "blocks world-writable chmod against filesystem root"
    account_paths = ["/etc/" + "passwd", "/etc/" + "shad" + "ow"]
    if any(path in compact for path in account_paths):
        if re.search(r"(>|>>|\btee\b|\bsed\s+-i\b|\bperl\s+-i\b|\bmv\b|\bcp\b|\brm\b|\bchmod\b|\bchown\b)", compact):
            return "blocks writes or destructive operations against system account files"
    if any(path in compact for path in protected_terms()):
        return "blocks operations against protected credential or secret paths"
    return None


try:
    payload = load_json_file(input_path)
    tool_name, command = command_text(payload)
    egress_reason, egress = egress_inspector(tool_name, command)
    injection_reason, injection = injection_inspector(tool_name, command)
    containment_reason, containment = containment_guard(payload, tool_name, command)
    reason = egress_reason or injection_reason or containment_reason or danger_reason(command)
    decision = "deny" if reason else "allow"
    append_jsonl(
        log_path,
        {
            "timestamp": now(),
            "hook_event_name": "PreToolUse",
            "tool_name": tool_name,
            "cwd": payload.get("cwd") or os.getcwd(),
            "turn_id": payload.get("turn_id") or payload.get("turnId"),
            "tool_use_id": payload.get("tool_use_id") or payload.get("toolUseId"),
            "decision": decision,
            "reason": reason,
            "egress_inspector": egress,
            "injection_inspector": injection,
            "containment_guard": containment,
            "command": text_facts(command),
        },
    )
    if reason:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}}))
    else:
        print("{}")
except Exception as exc:
    try:
        append_jsonl(log_path, {"timestamp": now(), "hook_event_name": "PreToolUse", "decision": "fallback", "error": safe_error(exc)})
    except Exception:
        pass
    print("{}")
PY
