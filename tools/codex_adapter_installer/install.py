"""Codex peer beta adapter installer.

The installer copies only the staged adapter payload into approved PAI live
targets. It does not inspect Memory, ISA, Pulse payloads, product memory, or
runtime state, and it does not invoke external runtimes or network services.
"""

from __future__ import annotations

import json
import stat
from pathlib import Path
from typing import Iterable


class InstallerError(ValueError):
    """Raised when installer input, safety validation, or payload validation fails."""


MILESTONE = "V5-S15B-R1-CODEX-RUNTIME-CONTAINED-WORKLOOP"
REPO_ROOT = Path(__file__).resolve().parents[2]
STAGED_ADAPTER_DIR = REPO_ROOT / "adapters" / "codex"

ROUTER_RELATIVE = Path("AGENTS.md")
ADAPTER_DIR_RELATIVE = Path("adapters") / "codex"
INSTALL_STATE_RELATIVE = ADAPTER_DIR_RELATIVE / "install-state.json"
RUNTIME_STATE_RELATIVE = ADAPTER_DIR_RELATIVE / "runtime-state.json"
LAUNCHER_RELATIVE = ADAPTER_DIR_RELATIVE / "bin" / "pai-codex"
RUNTIME_PROOF_SCHEMA_RELATIVE = ADAPTER_DIR_RELATIVE / "runtime-proof.schema.json"
WORKLOOP_SCHEMA_RELATIVE = ADAPTER_DIR_RELATIVE / "workloop-once.schema.json"
RUN_DIR_RELATIVE = ADAPTER_DIR_RELATIVE / "runs" / "s15b-r1"
RUNTIME_PROOF_RELATIVE = RUN_DIR_RELATIVE / "runtime-proof.json"
WORKLOOP_ONCE_RELATIVE = RUN_DIR_RELATIVE / "workloop-once.json"
RUNTIME_VALIDATION_RELATIVE = RUN_DIR_RELATIVE / "runtime-validation.json"

STAGED_TEXT_COPY_TARGETS = {
    "AGENTS.md": ADAPTER_DIR_RELATIVE / "AGENTS.md",
    "README.md": ADAPTER_DIR_RELATIVE / "README.md",
    "adapter-manifest.json": ADAPTER_DIR_RELATIVE / "adapter-manifest.json",
    "runtime-proof.schema.json": RUNTIME_PROOF_SCHEMA_RELATIVE,
    "workloop-once.schema.json": WORKLOOP_SCHEMA_RELATIVE,
}

STAGED_EXECUTABLE_COPY_TARGETS = {
    "bin/pai-codex": LAUNCHER_RELATIVE,
}

INSTALL_REQUIRED_RELATIVES = (
    ROUTER_RELATIVE,
    ADAPTER_DIR_RELATIVE / "AGENTS.md",
    ADAPTER_DIR_RELATIVE / "README.md",
    ADAPTER_DIR_RELATIVE / "adapter-manifest.json",
    INSTALL_STATE_RELATIVE,
    LAUNCHER_RELATIVE,
    RUNTIME_PROOF_SCHEMA_RELATIVE,
    WORKLOOP_SCHEMA_RELATIVE,
    RUNTIME_STATE_RELATIVE,
)

APPROVED_LIVE_RELATIVES = INSTALL_REQUIRED_RELATIVES + (
    RUNTIME_PROOF_RELATIVE,
    WORKLOOP_ONCE_RELATIVE,
    RUNTIME_VALIDATION_RELATIVE,
)

REQUIRED_ROUTER_CONCEPTS = (
    "PAI_CODEX_PEER_BETA_ADAPTER",
    "Codex is a peer beta adapter for PAI v5.",
    "Claude remains the official/full-support upstream adapter.",
    "PAI v5 is a Life OS, not just Claude config.",
    "PAI_DIR is the v5 PAI subsystem root, usually ~/.claude/PAI.",
    "PAI_SYSTEM_PROMPT.md is a high-authority instruction layer.",
    "Pulse is the central daemon/dashboard/event surface on localhost:31337.",
    "ISA replaces PRD as the work/system-of-record primitive.",
    "Memory v7.6 has WORK, LEARNING, and KNOWLEDGE.",
    "Codex must not write PAI Memory unless a later architect-approved policy allows it.",
    "Codex must not write ISA unless a later architect-approved policy allows it.",
    "Codex must not start, probe, or call Pulse.",
    "AGENTS.md is a router into PAI v5, not a clone of CLAUDE.md.",
    "When operating in a PAI workspace, identify PAI_DIR, read PAI_SYSTEM_PROMPT.md if available, then follow Codex adapter constraints.",
)

EXPECTED_MANIFEST_VALUES = {
    "adapter_name": "codex",
    "adapter_status": "peer-beta",
    "upstream_adapter": "claude",
    "payload_type": "live-installable-router",
    "install_target": "~/.claude/PAI/AGENTS.md",
    "live_install_status": "installed-by-installer-only",
}

REQUIRED_MANIFEST_KEYS = (
    "adapter_name",
    "adapter_status",
    "upstream_adapter",
    "payload_type",
    "install_target",
    "live_install_status",
    "authority_layers",
    "memory_policy",
    "isa_policy",
    "pulse_policy",
    "runtime_surface_policy",
    "rollback_policy",
    "runtime_launcher_policy",
)

FORBIDDEN_ROUTER_MARKERS = (
    "You are Claude Code",
    "# CLAUDE.md",
    "Claude Code configuration",
    "MCP servers",
    "slash commands",
    "Codex is replacement-grade",
    "Codex replaces Claude",
    "Codex may write Memory",
    "Codex may write ISA",
    "Codex may probe Pulse",
    "repo root AGENTS.md approved",
    ".codex/ approved",
    "~/.codex approved",
)

NOT_APPROVED_SURFACES = (
    "repo root AGENTS.md",
    "repo .codex/",
    "~/.codex adapter files",
    "Codex hooks",
    "Codex rules",
    "Codex skills",
    "Codex agents",
    "Codex commands",
    "Codex launchers outside ~/.claude/PAI/adapters/codex/bin/",
    "Pulse bridge",
    "Memory writer",
    "ISA writer",
)

RUNTIME_SCHEMA_REQUIRED_FIELDS = (
    "milestone_name",
    "runtime_invocation",
    "pai_dir",
    "adapter_identity_marker",
    "adapter_status",
    "upstream_adapter",
    "agents_router_observed",
    "pai_system_prompt_policy_observed",
    "memory_write_performed",
    "isa_write_performed",
    "pulse_probe_performed",
    "localhost_31337_called",
    "runtime_surface_created",
    "evidence_classification",
    "known_limits",
)

WORKLOOP_SCHEMA_REQUIRED_FIELDS = (
    "milestone_name",
    "workloop_kind",
    "pai_dir",
    "adapter_identity_marker",
    "adapter_status",
    "upstream_adapter",
    "observed_instruction_sources",
    "selected_work_policy",
    "memory_write_performed",
    "isa_write_performed",
    "pulse_probe_performed",
    "localhost_31337_called",
    "runtime_surface_created",
    "proposed_next_action",
    "requires_architect_goal_card",
    "evidence_classification",
    "known_limits",
)


def _reject_path_value(path_value: str | Path | None, label: str) -> Path:
    if path_value is None:
        raise InstallerError(f"{label} is required")
    text = str(path_value)
    if text == "":
        raise InstallerError(f"{label} must not be empty")
    if "\x00" in text:
        raise InstallerError(f"{label} contains a NUL byte")
    candidate = Path(text)
    if any(part == ".." for part in candidate.parts):
        raise InstallerError("path traversal is detected")
    return candidate


def _resolve_existing_dir(path_value: str | Path | None, label: str) -> Path:
    candidate = _reject_path_value(path_value, label)
    try:
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError as exc:
        raise InstallerError(f"{label} must exist") from exc
    except RuntimeError as exc:
        raise InstallerError(f"{label} has ambiguous path resolution") from exc
    if not resolved.is_dir():
        raise InstallerError(f"{label} must be a directory")
    return resolved


def _is_within(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _resolve_pai_dir(pai_dir: str | Path | None) -> Path:
    return _resolve_existing_dir(pai_dir, "--pai-dir")


def _resolve_backup_root(backup_root: str | Path | None) -> Path:
    resolved = _resolve_existing_dir(backup_root, "--backup-root")
    if resolved == REPO_ROOT or _is_within(REPO_ROOT, resolved):
        raise InstallerError("--backup-root must not be inside the repository")
    if not (resolved / ".claude").is_dir():
        raise InstallerError("--backup-root must contain a .claude backup directory")
    return resolved


def _safe_live_path(pai_dir: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute() or any(part == ".." for part in relative_path.parts):
        raise InstallerError("path traversal is detected")
    target = pai_dir / relative_path
    try:
        resolved_target = target.resolve(strict=False)
    except RuntimeError as exc:
        raise InstallerError("install target has ambiguous path resolution") from exc
    if not _is_within(pai_dir, resolved_target):
        raise InstallerError("symlink escape is detected for install target")
    if target.is_symlink():
        raise InstallerError("install target is a symlink")
    return target


def approved_live_targets(pai_dir: Path) -> tuple[Path, ...]:
    return tuple(_safe_live_path(pai_dir, relative_path) for relative_path in APPROVED_LIVE_RELATIVES)


def _read_staged_text(filename: str) -> str:
    path = STAGED_ADAPTER_DIR / filename
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise InstallerError(f"staged adapter payload is missing: {path}") from exc


def load_staged_manifest() -> dict[str, object]:
    try:
        manifest = json.loads(_read_staged_text("adapter-manifest.json"))
    except json.JSONDecodeError as exc:
        raise InstallerError("adapter manifest is not valid JSON") from exc
    if not isinstance(manifest, dict):
        raise InstallerError("adapter manifest must be a JSON object")
    return manifest


def read_staged_agents() -> str:
    return _read_staged_text("AGENTS.md")


def _load_staged_schema(filename: str, required_fields: tuple[str, ...]) -> dict[str, object]:
    try:
        schema = json.loads(_read_staged_text(filename))
    except json.JSONDecodeError as exc:
        raise InstallerError(f"{filename} is not valid JSON") from exc
    if not isinstance(schema, dict):
        raise InstallerError(f"{filename} must be a JSON object")
    schema_text = json.dumps(schema, sort_keys=True)
    missing = [field for field in required_fields if field not in schema_text]
    if missing:
        raise InstallerError(f"{filename} is missing required fields: " + ", ".join(missing))
    return schema


def validate_router_text(text: str) -> None:
    missing = [concept for concept in REQUIRED_ROUTER_CONCEPTS if concept not in text]
    if missing:
        raise InstallerError("AGENTS router is missing required PAI v5 concepts: " + ", ".join(missing))
    if len(text.encode("utf-8")) > 12000:
        raise InstallerError("AGENTS router is too large for compact-router requirement")
    if text.count("Claude") > 8:
        raise InstallerError("AGENTS router over-emphasizes Claude and looks like a Claude-facing file")
    forbidden = [marker for marker in FORBIDDEN_ROUTER_MARKERS if marker in text]
    if forbidden:
        raise InstallerError("AGENTS router contains forbidden clone or approval markers: " + ", ".join(forbidden))


def validate_manifest(manifest: dict[str, object]) -> None:
    missing = [key for key in REQUIRED_MANIFEST_KEYS if key not in manifest]
    if missing:
        raise InstallerError("adapter manifest is missing required keys: " + ", ".join(missing))

    for key, expected in EXPECTED_MANIFEST_VALUES.items():
        actual = manifest.get(key)
        if actual != expected:
            raise InstallerError(f"adapter manifest mismatch for {key}: expected {expected!r}, got {actual!r}")

    launcher_policy = manifest.get("runtime_launcher_policy")
    if not isinstance(launcher_policy, dict):
        raise InstallerError("runtime_launcher_policy must be an object")
    if launcher_policy.get("launcher_target") != "~/.claude/PAI/adapters/codex/bin/pai-codex":
        raise InstallerError("runtime_launcher_policy must target the approved adapter launcher")
    if launcher_policy.get("run_directory") != "~/.claude/PAI/adapters/codex/runs/s15b-r1/":
        raise InstallerError("runtime_launcher_policy must target the approved S15B-R1 run directory")

    runtime_policy = manifest.get("runtime_surface_policy")
    if not isinstance(runtime_policy, dict):
        raise InstallerError("runtime_surface_policy must be an object")
    not_approved = runtime_policy.get("not_approved_by_this_milestone")
    if not isinstance(not_approved, list):
        raise InstallerError("runtime_surface_policy.not_approved_by_this_milestone must be a list")
    missing_not_approved = [surface for surface in NOT_APPROVED_SURFACES if surface not in not_approved]
    if missing_not_approved:
        raise InstallerError(
            "adapter manifest is missing not-approved surfaces: " + ", ".join(missing_not_approved)
        )


def validate_launcher_text(text: str) -> None:
    missing = [token for token in ("doctor", "exec-proof", "workloop-once", "codex", "exec", "read-only") if token not in text]
    if missing:
        raise InstallerError("runtime launcher is missing required tokens: " + ", ".join(missing))


def validate_staged_payload() -> None:
    validate_router_text(read_staged_agents())
    validate_manifest(load_staged_manifest())
    _read_staged_text("README.md")
    validate_launcher_text(_read_staged_text("bin/pai-codex"))
    _load_staged_schema("runtime-proof.schema.json", RUNTIME_SCHEMA_REQUIRED_FIELDS)
    _load_staged_schema("workloop-once.schema.json", WORKLOOP_SCHEMA_REQUIRED_FIELDS)


def _install_state_json() -> str:
    state = {
        "adapter_name": "codex",
        "adapter_status": "peer-beta",
        "installed": True,
        "install_target": "~/.claude/PAI/AGENTS.md",
        "managed_live_targets": [str(path) for path in APPROVED_LIVE_RELATIVES],
        "milestone": MILESTONE,
        "rollback_source": "backup-root/.claude/PAI",
        "upstream_adapter": "claude",
    }
    return json.dumps(state, indent=2, sort_keys=True) + "\n"


def _runtime_state_json() -> str:
    state = {
        "adapter_name": "codex",
        "adapter_status": "peer-beta",
        "launcher": "~/.claude/PAI/adapters/codex/bin/pai-codex",
        "milestone": MILESTONE,
        "runtime_mode": "contained-read-only",
        "run_directory": "~/.claude/PAI/adapters/codex/runs/s15b-r1/",
        "upstream_adapter": "claude",
    }
    return json.dumps(state, indent=2, sort_keys=True) + "\n"


def _write_text_if_changed(path: Path, text: str) -> bool:
    if path.exists():
        if not path.is_file():
            raise InstallerError(f"install target is not a file: {path}")
        if path.read_text(encoding="utf-8") == text:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def _mark_executable(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _copy_payload_to_live(pai_dir: Path) -> list[Path]:
    changed: list[Path] = []
    router = read_staged_agents()
    if _write_text_if_changed(_safe_live_path(pai_dir, ROUTER_RELATIVE), router):
        changed.append(pai_dir / ROUTER_RELATIVE)

    for filename, relative_target in STAGED_TEXT_COPY_TARGETS.items():
        text = _read_staged_text(filename)
        target = _safe_live_path(pai_dir, relative_target)
        if _write_text_if_changed(target, text):
            changed.append(target)

    for filename, relative_target in STAGED_EXECUTABLE_COPY_TARGETS.items():
        text = _read_staged_text(filename)
        target = _safe_live_path(pai_dir, relative_target)
        if _write_text_if_changed(target, text):
            changed.append(target)
        _mark_executable(target)

    for relative_target, text in (
        (INSTALL_STATE_RELATIVE, _install_state_json()),
        (RUNTIME_STATE_RELATIVE, _runtime_state_json()),
    ):
        target = _safe_live_path(pai_dir, relative_target)
        if _write_text_if_changed(target, text):
            changed.append(target)
    return changed


def apply_install(pai_dir: str | Path | None, backup_root: str | Path | None) -> dict[str, object]:
    resolved_pai_dir = _resolve_pai_dir(pai_dir)
    _resolve_backup_root(backup_root)
    validate_staged_payload()
    approved_live_targets(resolved_pai_dir)
    changed = _copy_payload_to_live(resolved_pai_dir)
    validate_install(resolved_pai_dir)
    return {
        "pai_dir": str(resolved_pai_dir),
        "changed_targets": [str(path) for path in changed],
    }


def _validate_live_text_matches(pai_dir: Path, relative_path: Path, expected: str) -> None:
    target = _safe_live_path(pai_dir, relative_path)
    if not target.exists():
        raise InstallerError(f"installed file is missing: {target}")
    if not target.is_file():
        raise InstallerError(f"installed target is not a file: {target}")
    actual = target.read_text(encoding="utf-8")
    if actual != expected:
        raise InstallerError(f"installed file does not match staged payload: {target}")


def _validate_live_json(path: Path, label: str) -> dict[str, object]:
    if not path.exists():
        raise InstallerError(f"{label} is missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise InstallerError(f"{label} is not valid JSON") from exc
    if not isinstance(data, dict):
        raise InstallerError(f"{label} must be a JSON object")
    return data


def validate_install(
    pai_dir: str | Path | None,
    backup_root: str | Path | None = None,
) -> dict[str, object]:
    resolved_pai_dir = _resolve_pai_dir(pai_dir)
    if backup_root is not None:
        _resolve_backup_root(backup_root)
    validate_staged_payload()
    approved_live_targets(resolved_pai_dir)

    staged_agents = read_staged_agents()
    _validate_live_text_matches(resolved_pai_dir, ROUTER_RELATIVE, staged_agents)
    _validate_live_text_matches(resolved_pai_dir, ADAPTER_DIR_RELATIVE / "AGENTS.md", staged_agents)
    _validate_live_text_matches(resolved_pai_dir, ADAPTER_DIR_RELATIVE / "README.md", _read_staged_text("README.md"))
    _validate_live_text_matches(resolved_pai_dir, RUNTIME_PROOF_SCHEMA_RELATIVE, _read_staged_text("runtime-proof.schema.json"))
    _validate_live_text_matches(resolved_pai_dir, WORKLOOP_SCHEMA_RELATIVE, _read_staged_text("workloop-once.schema.json"))

    launcher_target = _safe_live_path(resolved_pai_dir, LAUNCHER_RELATIVE)
    _validate_live_text_matches(resolved_pai_dir, LAUNCHER_RELATIVE, _read_staged_text("bin/pai-codex"))
    if not launcher_target.stat().st_mode & stat.S_IXUSR:
        raise InstallerError("installed runtime launcher is not executable")

    manifest_target = _safe_live_path(resolved_pai_dir, ADAPTER_DIR_RELATIVE / "adapter-manifest.json")
    installed_manifest = _validate_live_json(manifest_target, "installed adapter manifest")
    if installed_manifest != load_staged_manifest():
        raise InstallerError("installed adapter manifest does not match staged manifest")
    validate_manifest(installed_manifest)

    state_target = _safe_live_path(resolved_pai_dir, INSTALL_STATE_RELATIVE)
    state = _validate_live_json(state_target, "install-state.json")
    if state.get("installed") is not True:
        raise InstallerError("install-state.json does not record installed=true")
    if state.get("adapter_status") != "peer-beta":
        raise InstallerError("install-state.json does not preserve adapter_status=peer-beta")
    if state.get("upstream_adapter") != "claude":
        raise InstallerError("install-state.json does not preserve upstream_adapter=claude")

    runtime_state_target = _safe_live_path(resolved_pai_dir, RUNTIME_STATE_RELATIVE)
    runtime_state = _validate_live_json(runtime_state_target, "runtime-state.json")
    if runtime_state.get("runtime_mode") != "contained-read-only":
        raise InstallerError("runtime-state.json does not record contained-read-only mode")
    if runtime_state.get("adapter_status") != "peer-beta":
        raise InstallerError("runtime-state.json does not preserve adapter_status=peer-beta")
    if runtime_state.get("upstream_adapter") != "claude":
        raise InstallerError("runtime-state.json does not preserve upstream_adapter=claude")

    return {
        "pai_dir": str(resolved_pai_dir),
        "adapter_status": installed_manifest["adapter_status"],
        "upstream_adapter": installed_manifest["upstream_adapter"],
        "launcher": str(launcher_target),
    }


def _backup_pai_dir(backup_root: Path) -> Path:
    backup_pai = backup_root / ".claude" / "PAI"
    if not backup_pai.is_dir():
        raise InstallerError("backup root does not contain .claude/PAI")
    return backup_pai


def _restore_or_remove_file(pai_dir: Path, backup_pai: Path, relative_path: Path) -> bool:
    live_target = _safe_live_path(pai_dir, relative_path)
    backup_source = backup_pai / relative_path

    if backup_source.exists():
        if backup_source.is_symlink():
            raise InstallerError(f"backup source for rollback is a symlink: {backup_source}")
        if not backup_source.is_file():
            raise InstallerError(f"backup source for rollback is not a file: {backup_source}")
        text = backup_source.read_text(encoding="utf-8")
        changed = _write_text_if_changed(live_target, text)
        if live_target.name == "pai-codex":
            _mark_executable(live_target)
        return changed

    if live_target.exists():
        if not live_target.is_file():
            raise InstallerError(f"rollback target is not a file: {live_target}")
        live_target.unlink()
        return True
    return False


def _remove_empty_dirs(paths: Iterable[Path]) -> None:
    for path in paths:
        try:
            path.rmdir()
        except FileNotFoundError:
            continue
        except OSError:
            continue


def rollback_install(pai_dir: str | Path | None, backup_root: str | Path | None) -> dict[str, object]:
    resolved_pai_dir = _resolve_pai_dir(pai_dir)
    resolved_backup_root = _resolve_backup_root(backup_root)
    approved_live_targets(resolved_pai_dir)
    backup_pai = _backup_pai_dir(resolved_backup_root)

    changed: list[Path] = []
    for relative_path in APPROVED_LIVE_RELATIVES:
        if _restore_or_remove_file(resolved_pai_dir, backup_pai, relative_path):
            changed.append(resolved_pai_dir / relative_path)

    _remove_empty_dirs(
        (
            resolved_pai_dir / RUN_DIR_RELATIVE,
            resolved_pai_dir / ADAPTER_DIR_RELATIVE / "runs",
            resolved_pai_dir / ADAPTER_DIR_RELATIVE / "bin",
            resolved_pai_dir / ADAPTER_DIR_RELATIVE,
            resolved_pai_dir / "adapters",
        )
    )

    return {
        "pai_dir": str(resolved_pai_dir),
        "changed_targets": [str(path) for path in changed],
    }
