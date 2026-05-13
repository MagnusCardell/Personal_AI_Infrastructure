from __future__ import annotations

import json
import subprocess
from pathlib import Path


RUN_ID = "s15d-codex-synthetic-bugfix"
RUN_RESULT_NAME = "run-result.json"
EVENTS_NAME = "runtime-events.jsonl"


class CodexProviderError(ValueError):
    pass


def provider_driver(pai_dir: Path) -> Path:
    return pai_dir / "adapters" / "codex" / "bin" / "pai-codex"


def build_provider_command(pai_dir: Path, task_card: Path, run_dir: Path) -> list[str]:
    driver = provider_driver(pai_dir)
    return [
        str(driver),
        "provider-run",
        "--pai-dir",
        str(pai_dir),
        "--task-card",
        str(task_card),
        "--run-dir",
        str(run_dir),
        "--result",
        str(run_dir / RUN_RESULT_NAME),
        "--events-output",
        str(run_dir / EVENTS_NAME),
    ]


def run_codex_provider(pai_dir: Path, task_card: Path, run_dir: Path, dry_run: bool = False) -> dict[str, object]:
    """Run Codex as a PAI runtime provider.

    PAI owns the run. The provider driver only performs the bounded Codex
    execution step for the PAI-owned run directory.
    """

    driver = provider_driver(pai_dir)
    if not driver.is_file():
        raise CodexProviderError(f"Codex provider driver is missing: {driver}")
    command = build_provider_command(pai_dir, task_card, run_dir)
    if dry_run:
        return {
            "dry_run": True,
            "provider_command": command,
            "driver_path": str(driver),
            "run_dir": str(run_dir),
        }

    completed = subprocess.run(
        command,
        cwd=Path.cwd(),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise CodexProviderError(f"Codex provider failed: {completed.stderr.strip()}")
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise CodexProviderError("Codex provider did not return JSON") from exc
    if not isinstance(payload, dict):
        raise CodexProviderError("Codex provider response must be a JSON object")
    payload["provider_command"] = command
    return payload
