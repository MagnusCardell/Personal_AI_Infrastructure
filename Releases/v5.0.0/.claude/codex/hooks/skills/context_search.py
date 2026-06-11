"""Codex skill: context_search — Phase-1 scan of prior PAI work.

Mirrors the ContextSearch skill's fast index scan: session registry,
session names, work directory names, and ISA title grep. Read-only.

usage: context_search.py TERM [TERM...]
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import os
import sys

MAX_PER_SOURCE = 5


def pai_dir() -> Path:
    configured = os.environ.get("PAI_DIR", "").strip()
    if configured:
        return Path(configured)
    return Path.home() / ".claude" / "PAI"


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None


def matches(text: str, terms: list[str]) -> bool:
    low = text.lower()
    return any(term in low for term in terms)


def scan_work_registry(root: Path, terms: list[str]) -> list[dict]:
    data = load_json(root / "MEMORY" / "STATE" / "work.json")
    results: list[dict] = []
    if not isinstance(data, dict):
        return results
    for slug, entry in data.items():
        if not isinstance(entry, dict):
            continue
        haystack = " ".join(
            str(entry.get(key, "")) for key in ("task", "sessionName", "phase")
        ) + " " + str(slug)
        if matches(haystack, terms):
            results.append(
                {
                    "slug": str(slug),
                    "task": str(entry.get("task", ""))[:120],
                    "phase": str(entry.get("phase", "")),
                    "progress": str(entry.get("progress", "")),
                }
            )
    return results[-MAX_PER_SOURCE:]


def scan_session_names(root: Path, terms: list[str]) -> list[dict]:
    data = load_json(root / "MEMORY" / "STATE" / "session-names.json")
    results: list[dict] = []
    entries = data.items() if isinstance(data, dict) else []
    for session_id, name in entries:
        if matches(str(name), terms):
            results.append({"sessionId": str(session_id), "name": str(name)[:120]})
    return results[-MAX_PER_SOURCE:]


def scan_work_dirs(root: Path, terms: list[str]) -> list[dict]:
    work = root / "MEMORY" / "WORK"
    results: list[dict] = []
    if not work.is_dir():
        return results
    try:
        names = sorted(p.name for p in work.iterdir() if p.is_dir())
    except OSError:
        return results
    for name in names:
        if matches(name, terms):
            isa = work / name / "ISA.md"
            results.append({"dir": name, "isa": str(isa) if isa.is_file() else ""})
    return results[-MAX_PER_SOURCE:]


def scan_isa_titles(root: Path, terms: list[str]) -> list[dict]:
    work = root / "MEMORY" / "WORK"
    results: list[dict] = []
    if not work.is_dir():
        return results
    try:
        isa_paths = sorted(work.glob("*/ISA.md"))
    except OSError:
        return results
    for isa in isa_paths:
        try:
            head = isa.read_text(encoding="utf-8", errors="replace")[:2000]
        except OSError:
            continue
        title = ""
        for line in head.splitlines():
            if line.startswith("task:"):
                title = line[len("task:"):].strip().strip('"')
                break
        if title and matches(title, terms):
            results.append({"isa": str(isa), "task": title[:120]})
        if len(results) >= MAX_PER_SOURCE:
            break
    return results


def log_execution(root: Path, terms: list[str], counts: dict) -> None:
    try:
        log_path = root / "MEMORY" / "SKILLS" / "codex-execution.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "skill": "context_search",
            "terms": terms[:8],
            "counts": counts,
            "status": "ok",
        }
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")
    except Exception:
        pass


def main(argv: list[str]) -> int:
    terms = [arg.strip().lower() for arg in argv if arg.strip()]
    if not terms:
        print("usage: context_search.py TERM [TERM...]", file=sys.stderr)
        return 2
    root = pai_dir()
    report = {
        "query": terms,
        "sessions": scan_work_registry(root, terms),
        "session_names": scan_session_names(root, terms),
        "work_dirs": scan_work_dirs(root, terms),
        "isa_titles": scan_isa_titles(root, terms),
    }
    counts = {key: len(value) for key, value in report.items() if isinstance(value, list)}
    log_execution(root, terms, counts)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
