#!/usr/bin/env bash
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAI_DIR="${PAI_DIR:-$HOME/.claude/PAI}"
OBS_DIR="$PAI_DIR/MEMORY/OBSERVABILITY"
mkdir -p "$OBS_DIR"
export PYTHONPATH="$HOOK_DIR/lib${PYTHONPATH:+:$PYTHONPATH}"

PAI_CODEX_ENV="$HOOK_DIR/pulse.env"
if [[ -f "$PAI_CODEX_ENV" ]]; then
  PAI_CODEX_ENV_VARS=(
    PAI_CODEX_PULSE_ENABLED
    PAI_CODEX_PULSE_URL
    PAI_CODEX_VOICE_ENABLED
    PAI_CODEX_VOICE_ID
    PAI_CODEX_VOICE_EVENTS
    PAI_CODEX_VOICE_MESSAGE_TURN_COMPLETE
    PAI_CODEX_VOICE_MESSAGE_ISA_UPDATED
    PAI_CODEX_LEARNING_ENABLED
    PAI_CODEX_CHECKPOINT_ENABLED
  )
  for name in "${PAI_CODEX_ENV_VARS[@]}"; do
    had_name="__PAI_CODEX_HAD_${name}"
    saved_name="__PAI_CODEX_SAVED_${name}"
    if [[ ${!name+x} ]]; then
      printf -v "$had_name" '%s' "1"
      printf -v "$saved_name" '%s' "${!name}"
    else
      printf -v "$had_name" '%s' "0"
    fi
  done
  set -a
  # shellcheck source=/dev/null
  . "$PAI_CODEX_ENV"
  set +a
  for name in "${PAI_CODEX_ENV_VARS[@]}"; do
    had_name="__PAI_CODEX_HAD_${name}"
    saved_name="__PAI_CODEX_SAVED_${name}"
    if [[ ${!had_name} == "1" ]]; then
      printf -v "$name" '%s' "${!saved_name}"
      export "$name"
    fi
    unset "$had_name" "$saved_name"
  done
  unset PAI_CODEX_ENV_VARS name had_name saved_name
fi

if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' '{}'
  exit 0
fi

TMP_INPUT="$(mktemp "${TMPDIR:-/tmp}/pai-codex-posttool.XXXXXX")"
trap 'command rm "$TMP_INPUT" 2>/dev/null || true' EXIT
cat > "$TMP_INPUT"

python3 - "$TMP_INPUT" "$PAI_DIR" "$OBS_DIR/codex-posttool.jsonl" "$OBS_DIR/codex-isasync.jsonl" <<'PY'
from __future__ import annotations

from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import sys

from log_event import append_jsonl, load_json_file, now, safe_error
from pulse_notify import notify
from redact import risk_flags, text_facts

input_path = Path(sys.argv[1])
pai_dir = Path(sys.argv[2]).expanduser()
tool_log_path = Path(sys.argv[3]).expanduser()
sync_log_path = Path(sys.argv[4]).expanduser()
home = str(Path.home())
checkpoint_log_path = pai_dir / "MEMORY" / "OBSERVABILITY" / "codex-checkpoint.jsonl"
isa_state_path = pai_dir / "MEMORY" / "OBSERVABILITY" / "codex-isa-state.json"


def get_tool(payload: dict) -> tuple[str, dict, str]:
    tool_name = str(payload.get("tool_name") or payload.get("toolName") or "")
    tool_input = payload.get("tool_input") if isinstance(payload.get("tool_input"), dict) else {}
    command = tool_input.get("command") if isinstance(tool_input.get("command"), str) else json.dumps(tool_input, sort_keys=True)
    return tool_name, tool_input, command


def expand_path(raw_path: str, cwd: str) -> Path:
    cleaned = raw_path.strip().strip("'\"`.,")
    cleaned = cleaned.replace("${HOME}", home).replace("$HOME", home)
    if cleaned.startswith("~/"):
        cleaned = home + cleaned[1:]
    path = Path(cleaned)
    if not path.is_absolute():
        path = Path(cwd) / path
    return path


def extract_isa_paths(payload: dict, tool_name: str, tool_input: dict, command: str) -> list[Path]:
    cwd = str(payload.get("cwd") or os.getcwd())
    candidates: set[Path] = set()
    search_text = command or ""

    for key in ("file_path", "path"):
        value = tool_input.get(key)
        if isinstance(value, str):
            search_text += "\n" + value

    for line in command.splitlines():
        match = re.match(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", line.strip())
        if match:
            candidates.add(expand_path(match.group(1), cwd))

    token_pattern = r"(?P<path>(?:/|~|\$HOME|\$\{HOME\}|[A-Za-z0-9_.-]+/)[^\s\"'`;|<>]*MEMORY/WORK/[^\s\"'`;|<>]*ISA\.md)"
    for match in re.finditer(token_pattern, search_text):
        candidates.add(expand_path(match.group("path"), cwd))

    if tool_name == "Bash":
        expanded = search_text.replace("${HOME}", home).replace("$HOME", home).replace("~/", home + "/")
        for match in re.finditer(r"(?:>|>>)\s*(?P<path>[^\s;|]+ISA\.md)", expanded):
            candidates.add(expand_path(match.group("path"), cwd))
        for match in re.finditer(r"\btee\s+(?:-a\s+)?(?P<path>[^\s;|]+ISA\.md)", expanded):
            candidates.add(expand_path(match.group("path"), cwd))

    work_root = pai_dir / "MEMORY" / "WORK"
    resolved: list[Path] = []
    for candidate in candidates:
        try:
            real_candidate = candidate.expanduser().resolve(strict=False)
            real_work = work_root.expanduser().resolve(strict=False)
            if real_candidate.name == "ISA.md" and real_work in real_candidate.parents:
                resolved.append(real_candidate)
        except Exception:
            continue
    return sorted(set(resolved), key=str)


def env_enabled(name: str) -> bool:
    return os.environ.get(name, "").lower() in {"1", "true", "yes", "on"}


def parse_isc_state(isa_path: Path) -> dict[str, bool]:
    try:
        text = isa_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    states: dict[str, bool] = {}
    pattern = re.compile(r"^-\s+\[(?P<mark>[ xX])\]\s+(?P<id>ISC-[0-9]+(?:\.[0-9]+)?):", re.M)
    for match in pattern.finditer(text):
        states[match.group("id")] = match.group("mark").lower() == "x"
    return states


def load_isa_state() -> dict:
    if not isa_state_path.exists():
        return {"version": 1, "isas": {}}
    try:
        value = json.loads(isa_state_path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {"version": 1, "isas": {}}
    if not isinstance(value, dict):
        return {"version": 1, "isas": {}}
    if not isinstance(value.get("isas"), dict):
        value["isas"] = {}
    value.setdefault("version", 1)
    return value


def write_isa_state(state: dict) -> None:
    isa_state_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = isa_state_path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp_path.replace(isa_state_path)


def git_run(args: list[str], cwd: Path, *, timeout: int = 8) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def claude_git_root() -> Path:
    return Path(home) / ".claude"


def is_claude_git_repo(root: Path) -> bool:
    if not (root / ".git").exists():
        return False
    proc = git_run(["rev-parse", "--is-inside-work-tree"], root)
    return proc.returncode == 0 and proc.stdout.strip() == "true"


def rel_to_claude(path: Path, root: Path) -> str | None:
    try:
        return str(path.resolve(strict=False).relative_to(root.resolve(strict=False)))
    except ValueError:
        return None


def git_status_paths(root: Path) -> list[str]:
    proc = git_run(["status", "--porcelain", "--untracked-files=all"], root)
    if proc.returncode != 0:
        return []
    paths: list[str] = []
    for line in proc.stdout.splitlines():
        if len(line) < 4:
            continue
        item = line[3:]
        if " -> " in item:
            item = item.split(" -> ", 1)[1]
        paths.append(item.strip())
    return paths


def is_runtime_observability_path(path: str) -> bool:
    return path.startswith("PAI/MEMORY/OBSERVABILITY/codex-") and path.endswith(".jsonl")


def checkpoint_git_commit(isa_path: Path, state: dict, isc_ids: list[str]) -> dict:
    root = claude_git_root()
    if not is_claude_git_repo(root):
        write_isa_state(state)
        return {"status": "skipped", "reason": "claude git repo unavailable", "git_repo": str(root)}

    isa_rel = rel_to_claude(isa_path, root)
    state_rel = rel_to_claude(isa_state_path, root)
    if isa_rel is None or state_rel is None:
        write_isa_state(state)
        return {"status": "skipped", "reason": "ISA or state path outside claude git repo", "git_repo": str(root)}

    allowed_dirty = {isa_rel, state_rel}
    dirty = git_status_paths(root)
    unrelated = [path for path in dirty if path not in allowed_dirty and not is_runtime_observability_path(path)]
    if unrelated:
        return {"status": "skipped", "reason": "claude git repo has unrelated dirty paths", "dirty_paths": unrelated}

    write_isa_state(state)
    add_proc = git_run(["add", "--", isa_rel, state_rel], root)
    if add_proc.returncode != 0:
        return {
            "status": "failed",
            "reason": "git add failed",
            "exit_code": add_proc.returncode,
            "stdout": text_facts(add_proc.stdout),
            "stderr": text_facts(add_proc.stderr),
        }

    message = f"ISC checkpoint: {isa_path.parent.name} \u2014 {', '.join(isc_ids)}"
    commit_proc = git_run(["commit", "--no-gpg-sign", "-m", message], root)
    if commit_proc.returncode != 0:
        return {
            "status": "failed",
            "reason": "git commit failed",
            "exit_code": commit_proc.returncode,
            "stdout": text_facts(commit_proc.stdout),
            "stderr": text_facts(commit_proc.stderr),
        }
    return {
        "status": "committed",
        "message": message,
        "stdout": text_facts(commit_proc.stdout),
        "stderr": text_facts(commit_proc.stderr),
    }


def checkpoint_isa(isa_path: Path) -> dict:
    if not env_enabled("PAI_CODEX_CHECKPOINT_ENABLED"):
        return {"status": "disabled", "isa_path": str(isa_path)}

    current = parse_isc_state(isa_path)
    if not current:
        return {"status": "skipped", "reason": "no ISC checkbox state found", "isa_path": str(isa_path)}

    state = load_isa_state()
    isas = state.setdefault("isas", {})
    key = str(isa_path)
    previous_record = isas.get(key) if isinstance(isas.get(key), dict) else {}
    previous = previous_record.get("checked") if isinstance(previous_record.get("checked"), dict) else {}
    transitions = sorted(isc_id for isc_id, checked in current.items() if checked and previous.get(isc_id) is False)

    isas[key] = {
        "slug": isa_path.parent.name,
        "isa_path": key,
        "checked": current,
        "updated": now(),
    }

    if not transitions:
        write_isa_state(state)
        return {"status": "no_transition", "isa_path": key, "checked_count": sum(1 for checked in current.values() if checked)}

    result = checkpoint_git_commit(isa_path, state, transitions)
    result.update({"isa_path": key, "isa_slug": isa_path.parent.name, "isc_ids": transitions})
    return result


def run_isasync(isa_path: Path, payload: dict) -> dict:
    bun = shutil.which("bun")
    if not bun:
        return {"status": "absent", "reason": "bun unavailable", "isa_path": str(isa_path)}

    tool_sync = pai_dir / "TOOLS" / "ISASync.ts"
    hook_sync = Path(home) / ".claude" / "hooks" / "ISASync.hook.ts"
    if tool_sync.exists():
        cmd = [bun, str(tool_sync), str(isa_path)]
        input_text = None
        kind = "PAI/TOOLS/ISASync.ts"
    elif hook_sync.exists():
        cmd = [bun, str(hook_sync)]
        synthetic = {
            "hook_event_name": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": str(isa_path)},
            "session_id": payload.get("session_id") or payload.get("sessionId"),
            "turn_id": payload.get("turn_id") or payload.get("turnId"),
            "cwd": payload.get("cwd") or os.getcwd(),
        }
        input_text = json.dumps(synthetic)
        kind = "~/.claude/hooks/ISASync.hook.ts"
    else:
        return {"status": "absent", "reason": "no ISASync implementation found", "isa_path": str(isa_path)}

    try:
        proc = subprocess.run(
            cmd,
            input=input_text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=8,
            check=False,
        )
    except Exception as exc:
        return {"status": "failed", "kind": kind, "isa_path": str(isa_path), "error": safe_error(exc)}

    return {
        "status": "ran" if proc.returncode == 0 else "failed",
        "kind": kind,
        "isa_path": str(isa_path),
        "exit_code": proc.returncode,
        "stdout": text_facts(proc.stdout),
        "stderr": text_facts(proc.stderr),
    }


try:
    payload = load_json_file(input_path)
    tool_name, tool_input, command = get_tool(payload)
    flags = risk_flags(command)
    isa_paths = extract_isa_paths(payload, tool_name, tool_input, command)

    append_jsonl(
        tool_log_path,
        {
            "timestamp": now(),
            "hook_event_name": "PostToolUse",
            "tool_name": tool_name,
            "cwd": payload.get("cwd") or os.getcwd(),
            "turn_id": payload.get("turn_id") or payload.get("turnId"),
            "tool_use_id": payload.get("tool_use_id") or payload.get("toolUseId"),
            "mentions_pai_dir": flags["mentions_pai"],
            "mentions_memory_work": flags["mentions_memory_work"],
            "mentions_isa": flags["mentions_isa"],
            "detected_isa_paths": [str(path) for path in isa_paths],
            "command": text_facts(command),
        },
    )

    for isa_path in isa_paths:
        checkpoint_result = checkpoint_isa(isa_path)
        if checkpoint_result.get("status") != "disabled":
            checkpoint_result["timestamp"] = now()
            append_jsonl(checkpoint_log_path, checkpoint_result)

        result = run_isasync(isa_path, payload)
        result["timestamp"] = now()
        append_jsonl(sync_log_path, result)
        if result.get("status") in {"ran", "failed"}:
            pulse_result = notify(
                "codex.algorithm.isa_updated",
                "PAI Codex ISA updated",
                details={
                    "isa_slug": isa_path.parent.name,
                    "isasync_status": result.get("status"),
                    "isasync_attempted": True,
                },
            )
            if pulse_result.get("attempted"):
                append_jsonl(
                    sync_log_path,
                    {
                        "timestamp": now(),
                        "hook_event_name": "PostToolUse",
                        "isa_slug": isa_path.parent.name,
                        "pulse": pulse_result,
                    },
                )
except Exception as exc:
    try:
        append_jsonl(tool_log_path, {"timestamp": now(), "hook_event_name": "PostToolUse", "error": safe_error(exc)})
    except Exception:
        pass
print("{}")
PY
