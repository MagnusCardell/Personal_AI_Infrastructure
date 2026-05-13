from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from tools.pai_runtime_runner.audit import audit_run as run_audit
from tools.pai_runtime_runner.providers.codex import build_provider_command, run_codex_provider


MILESTONE = "V5-S15D-PAI-RUNTIME-RUNNER-CODEX"
RUN_ID = "s15d-codex-synthetic-bugfix"
MARKER = "PAI_CODEX_PEER_BETA_ADAPTER"
RUN_RELATIVE = Path("runs") / "s15d" / "codex-synthetic-bugfix"
TASK_RELATIVE = Path("runtime-tasks") / "s15d-codex-synthetic-bugfix.json"


class RunnerError(ValueError):
    pass


def _is_within(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _resolve_pai_dir(value: str | Path) -> Path:
    if str(value) == "":
        raise RunnerError("--pai-dir must not be empty")
    path = Path(value)
    if any(part == ".." for part in path.parts):
        raise RunnerError("--pai-dir must not contain path traversal")
    resolved = path.resolve(strict=True)
    if not resolved.is_dir():
        raise RunnerError("--pai-dir must be a directory")
    return resolved


def _load_json(path: Path, label: str) -> dict[str, object]:
    if not path.is_file():
        raise RunnerError(f"{label} is missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RunnerError(f"{label} is not valid JSON") from exc
    if not isinstance(data, dict):
        raise RunnerError(f"{label} must be a JSON object")
    return data


def _provider_manifest_path(pai_dir: Path, runtime: str) -> Path:
    return pai_dir / "runtimes" / runtime / "provider-manifest.json"


def _validate_codex_manifest(manifest: dict[str, object]) -> None:
    expected = {
        "runtime_name": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "upstream_adapter": "claude",
        "supports_codex_exec": True,
        "supports_jsonl_events": True,
        "supports_structured_output": True,
        "memory_write_policy": "disabled",
        "isa_write_policy": "disabled",
        "pulse_policy": "no-probe",
        "replacement_status": "not-replacement-grade",
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            raise RunnerError(f"codex provider manifest mismatch for {key}")


def _safe_task_card(pai_dir: Path, task_card: str | Path) -> Path:
    path = Path(task_card)
    if str(task_card) == "":
        raise RunnerError("--task-card must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--task-card must not contain path traversal")
    resolved = path.resolve(strict=True)
    expected = (pai_dir / TASK_RELATIVE).resolve(strict=True)
    if resolved != expected:
        raise RunnerError("--task-card must be the installed S15D task card")
    return resolved


def _safe_run_dir(pai_dir: Path, run_dir: str | Path) -> Path:
    path = Path(run_dir)
    if str(run_dir) == "":
        raise RunnerError("--run-dir must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--run-dir must not contain path traversal")
    resolved = path.resolve(strict=False)
    expected = (pai_dir / RUN_RELATIVE).resolve(strict=False)
    if resolved != expected:
        raise RunnerError("PAI runtime run directory must be runs/s15d/codex-synthetic-bugfix")
    if path.exists() and not path.is_dir():
        raise RunnerError("--run-dir target is not a directory")
    if path.is_symlink():
        raise RunnerError("--run-dir target is a symlink")
    return path


def _safe_marker(marker: str | Path) -> Path:
    path = Path(marker)
    if str(marker) == "":
        raise RunnerError("--marker must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--marker must not contain path traversal")
    resolved = path.resolve(strict=True)
    if path.is_symlink():
        raise RunnerError("--marker must not be a symlink")
    return resolved


def _safe_audit_output(run_dir: Path, output: str | Path) -> Path:
    path = Path(output)
    if str(output) == "":
        raise RunnerError("--output must not be empty")
    if any(part == ".." for part in path.parts):
        raise RunnerError("--output must not contain path traversal")
    resolved = path.resolve(strict=False)
    if not _is_within(run_dir.resolve(strict=False), resolved):
        raise RunnerError("--output must stay under runs/s15d/codex-synthetic-bugfix")
    if resolved.name != "run-validation.json":
        raise RunnerError("--output must be named run-validation.json")
    if path.exists() and not path.is_file():
        raise RunnerError("--output target is not a file")
    if path.is_symlink():
        raise RunnerError("--output target is a symlink")
    return path


def doctor(pai_dir: Path) -> dict[str, object]:
    router = pai_dir / "AGENTS.md"
    if not router.is_file():
        raise RunnerError("PAI_DIR/AGENTS.md is missing")
    router_text = router.read_text(encoding="utf-8")
    if MARKER not in router_text:
        raise RunnerError("PAI_DIR/AGENTS.md is missing PAI_CODEX_PEER_BETA_ADAPTER")

    manifest = _load_json(_provider_manifest_path(pai_dir, "codex"), "codex provider manifest")
    _validate_codex_manifest(manifest)
    for path, label in (
        (pai_dir / "bin" / "pai-runtime", "pai-runtime"),
        (pai_dir / "runtime-schemas" / "provider-manifest.schema.json", "provider manifest schema"),
        (pai_dir / "runtime-schemas" / "run-result.schema.json", "run result schema"),
        (pai_dir / "runtime-schemas" / "run-validation.schema.json", "run validation schema"),
        (pai_dir / TASK_RELATIVE, "S15D task card"),
        (pai_dir / "runtime-task-fixtures" / "s15d_bugfix" / "src" / "pai_priority.py", "S15D task fixture"),
        (pai_dir / "adapters" / "codex" / "bin" / "pai-codex", "Codex provider driver"),
    ):
        if not path.is_file():
            raise RunnerError(f"{label} is missing: {path}")
    return {
        "ok": True,
        "pai_dir": str(pai_dir),
        "runtime": "codex",
        "runtime_status": "peer-beta",
        "provider_type": "codex-cli",
        "adapter_identity_marker_observed": True,
    }


def run_runtime(
    pai_dir: Path,
    runtime: str,
    task_card: str | Path,
    run_dir: str | Path,
    dry_run: bool = False,
) -> dict[str, object]:
    # PAI owns the run; Codex is only runtime provider codex.
    doctor(pai_dir)
    if runtime != "codex":
        raise RunnerError(f"unknown runtime provider: {runtime}")
    task_path = _safe_task_card(pai_dir, task_card)
    safe_run_dir = _safe_run_dir(pai_dir, run_dir)
    command = [
        str(pai_dir / "bin" / "pai-runtime"),
        "run",
        "--pai-dir",
        str(pai_dir),
        "--runtime",
        "codex",
        "--task-card",
        str(task_path),
        "--run-dir",
        str(safe_run_dir),
    ]
    provider_command = build_provider_command(pai_dir, task_path, safe_run_dir)
    if dry_run:
        return {
            "dry_run": True,
            "pai_runtime_command": command,
            "provider_command": provider_command,
            "run_dir": str(safe_run_dir),
        }
    safe_run_dir.mkdir(parents=True, exist_ok=True)
    provider_result = run_codex_provider(pai_dir, task_path, safe_run_dir)
    state_path = safe_run_dir / "run-state.json"
    state = _load_json(state_path, "run-state.json") if state_path.exists() else {}
    state["pai_runtime_command"] = command
    state["provider_command"] = provider_result.get("provider_command", provider_command)
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    provider_result["pai_runtime_command"] = command
    provider_result["provider_command"] = state["provider_command"]
    provider_result["pai_owned_run_directory"] = str(safe_run_dir)
    return provider_result


def audit_runtime_run(
    pai_dir: Path,
    marker: str | Path,
    run_dir: str | Path,
    output: str | Path,
    runtime_attempt_number: int,
) -> dict[str, object]:
    doctor(pai_dir)
    marker_path = _safe_marker(marker)
    safe_run_dir = _safe_run_dir(pai_dir, run_dir)
    output_path = _safe_audit_output(safe_run_dir, output)
    result = run_audit(
        pai_dir=pai_dir,
        marker=marker_path,
        run_dir=safe_run_dir,
        result_path=safe_run_dir / "run-result.json",
        events_path=safe_run_dir / "runtime-events.jsonl",
        runtime_attempt_number=runtime_attempt_number,
        repo_root=Path.cwd(),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not result.get("validation_passed"):
        raise RunnerError(f"S15D PAI runtime audit failed; wrote {output_path}")
    return {
        "ok": True,
        "output": str(output_path),
        "event_attribution_passed": result.get("event_attribution_passed"),
        "validation_passed": result.get("validation_passed"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PAI-owned runtime runner.")
    subcommands = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subcommands.add_parser("doctor")
    doctor_parser.add_argument("--pai-dir", required=True)

    run_parser = subcommands.add_parser("run")
    run_parser.add_argument("--pai-dir", required=True)
    run_parser.add_argument("--runtime", required=True)
    run_parser.add_argument("--task-card", required=True)
    run_parser.add_argument("--run-dir", required=True)
    run_parser.add_argument("--dry-run", action="store_true")

    audit_parser = subcommands.add_parser("audit-run")
    audit_parser.add_argument("--pai-dir", required=True)
    audit_parser.add_argument("--marker", required=True)
    audit_parser.add_argument("--run-dir", required=True)
    audit_parser.add_argument("--output", required=True)
    audit_parser.add_argument("--runtime-attempt-number", type=int, default=1)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        pai_dir = _resolve_pai_dir(args.pai_dir)
        if args.command == "doctor":
            result = doctor(pai_dir)
        elif args.command == "run":
            result = run_runtime(pai_dir, args.runtime, args.task_card, args.run_dir, args.dry_run)
        elif args.command == "audit-run":
            result = audit_runtime_run(pai_dir, args.marker, args.run_dir, args.output, args.runtime_attempt_number)
        else:
            raise RunnerError(f"unknown command: {args.command}")
    except (RunnerError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
