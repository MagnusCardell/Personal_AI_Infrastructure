"""Codex skill: iterative_depth - deterministic multi-lens exploration.

The script produces candidate ISA criteria from the IterativeDepth lenses
without calling a model or spawning agents. It is a local helper for PAI Codex
runtime tasks where structured requirements are useful before a deeper pass.

usage:
  iterative_depth.py [--sla fast|standard|deep|instant] [--depth N] TASK...
  echo "task" | iterative_depth.py --format markdown --depth 4
"""
from __future__ import annotations

from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
import hashlib
import json
import os
import re
import sys


ARTIFACT_RE = re.compile(r"\b[\w.-]+\.(?:py|ts|tsx|js|jsx|md|json|toml|sh|yaml|yml|rs|go)\b")
SLA_DEPTH = {"instant": 0, "fast": 2, "standard": 4, "deep": 8}

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private_key_block", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----", re.I | re.S)),
    ("provider_token", re.compile(r"\b" + "sk" + r"-(?:ant-)?[A-Za-z0-9_-]{20,}\b")),
    ("github_token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b")),
    ("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("bearer_token", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}")),
    ("generic_secret_kv", re.compile(r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key|private[_-]?key|client[_-]?secret)\s*[:=]\s*[^\s\"'`,;]{6,}")),
)


class SkillError(Exception):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def pai_root() -> Path:
    raw = os.environ.get("PAI_DIR") or str(Path.home() / ".claude" / "PAI")
    return Path(raw).expanduser().resolve(strict=False)


def content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8", errors="replace")).hexdigest()


def redact_text(text: str) -> tuple[str, dict[str, Any]]:
    redacted = text
    counts: dict[str, int] = {}
    for name, pattern in SECRET_PATTERNS:
        def repl(match: re.Match[str]) -> str:
            counts[name] = counts.get(name, 0) + 1
            if name == "generic_secret_kv":
                key = match.group(1)
                return f"{key}=[REDACTED:{name}]"
            return f"[REDACTED:{name}]"

        redacted = pattern.sub(repl, redacted)
    return redacted, {"redacted": bool(counts), "redaction_counts": counts}


def safe_log(root: Path, record: dict[str, Any]) -> None:
    try:
        log_path = root / "MEMORY" / "SKILLS" / "codex-execution.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    except Exception:
        pass


def collect_problem(positional: list[str]) -> str:
    problem = " ".join(part.strip() for part in positional if part.strip()).strip()
    if not problem and not sys.stdin.isatty():
        problem = sys.stdin.read().strip()
    if not problem:
        raise SkillError("problem must not be empty")
    return problem


def problem_summary(problem: str) -> str:
    one_line = re.sub(r"\s+", " ", problem).strip()
    return one_line[:220] + ("..." if len(one_line) > 220 else "")


def artifacts(problem: str) -> list[str]:
    return sorted(set(ARTIFACT_RE.findall(problem)))


def has_any(problem: str, terms: tuple[str, ...]) -> bool:
    low = problem.lower()
    return any(term in low for term in terms)


def lens_driver(problem: str) -> str:
    if ARTIFACT_RE.search(problem):
        return "explicit artifacts named in the request"
    if has_any(problem, ("security", "token", "secret", "auth", "permission", "sandbox", "injection")):
        return "security-sensitive terms"
    if has_any(problem, ("ui", "ux", "design", "screen", "page", "flow", "experience")):
        return "user-experience terms"
    if has_any(problem, ("architecture", "runtime", "migration", "system", "integration", "api")):
        return "architecture and integration terms"
    if len(problem.split()) <= 5:
        return "a terse, underspecified request"
    return "no dominant signal (default lens order)"


def select_lens_names(problem: str, depth: int) -> list[str]:
    default = [
        "Literal",
        "Stakeholder",
        "Failure",
        "Experiential",
        "Temporal",
        "Constraint Inversion",
        "Analogical",
        "Meta",
    ]
    if depth <= 0:
        return []

    if ARTIFACT_RE.search(problem):
        ordered = ["Literal", "Failure", "Stakeholder", "Temporal", *default]
    elif has_any(problem, ("security", "token", "secret", "auth", "permission", "sandbox", "injection")):
        ordered = ["Failure", "Stakeholder", "Temporal", "Constraint Inversion", *default]
    elif has_any(problem, ("ui", "ux", "design", "screen", "page", "flow", "experience")):
        ordered = ["Experiential", "Stakeholder", "Literal", "Failure", *default]
    elif has_any(problem, ("architecture", "runtime", "migration", "system", "integration", "api")):
        ordered = ["Temporal", "Constraint Inversion", "Analogical", "Failure", *default]
    elif len(problem.split()) <= 5:
        ordered = ["Meta", "Stakeholder", "Literal", "Failure", *default]
    else:
        ordered = default

    selected: list[str] = []
    for name in ordered:
        if name not in selected:
            selected.append(name)
        if len(selected) == depth:
            break
    return selected


def literal(problem: str, files: list[str]) -> dict[str, list[str]]:
    if files:
        findings = [f"Explicit artifact requested: {name}" for name in files[:8]]
        criteria = [f"{name} exists in the selected target location." for name in files[:4]]
    else:
        findings = ["The request must be converted into concrete deliverables."]
        criteria = ["Explicitly requested outcomes are represented as concrete criteria."]
    return {"findings": findings, "criteria": criteria, "anti": []}


def stakeholder(problem: str, files: list[str]) -> dict[str, list[str]]:
    return {
        "findings": [
            "Callers need predictable command-line behavior.",
            "Maintainers need output that is easy to verify and diff.",
        ],
        "criteria": [
            "Command output is structured enough for dispatcher callers.",
            "Implementation follows adjacent Codex skill conventions.",
        ],
        "anti": [],
    }


def failure(problem: str, files: list[str]) -> dict[str, list[str]]:
    return {
        "findings": [
            "The most likely failures are overwrite, path escape, and ambiguous output.",
            "Runtime helpers should fail closed on unsafe or underspecified writes.",
        ],
        "criteria": [
            "Unsafe paths are rejected before any file write occurs.",
            "Errors return nonzero status with concise diagnostics.",
        ],
        "anti": [
            "Anti: The work does not overwrite unrelated runtime files.",
            "Anti: The helper does not leak obvious secret material.",
        ],
    }


def experiential(problem: str, files: list[str]) -> dict[str, list[str]]:
    return {
        "findings": [
            "A good operator experience is scan-first and low ceremony.",
            "The caller should see the path, status, and next evidence immediately.",
        ],
        "criteria": [
            "Results are easy to scan without surrounding explanation.",
            "Successful runs report the artifact path and status.",
        ],
        "anti": [],
    }


def temporal(problem: str, files: list[str]) -> dict[str, list[str]]:
    return {
        "findings": [
            "Repeated runs should not destabilize prior task state.",
            "The output should remain readable after the current session ends.",
        ],
        "criteria": [
            "Repeated runs produce deterministic structure and stable identifiers.",
            "Generated artifacts remain useful as durable work memory.",
        ],
        "anti": [],
    }


def constraint_inversion(problem: str, files: list[str]) -> dict[str, list[str]]:
    return {
        "findings": [
            "The helper should still work without network access or new packages.",
            "The minimal useful version is a local deterministic scaffold.",
        ],
        "criteria": [
            "Implementation uses only the Python standard library.",
            "No network, vendor CLI, or model subprocess is required.",
        ],
        "anti": [],
    }


def analogical(problem: str, files: list[str]) -> dict[str, list[str]]:
    return {
        "findings": [
            "Adjacent tools log execution and return machine-readable summaries.",
            "The new helper should match existing dispatch ergonomics.",
        ],
        "criteria": [
            "Execution is logged to the Codex skill log.",
            "CLI usage matches existing package skill dispatch style.",
        ],
        "anti": [],
    }


def meta(problem: str, files: list[str]) -> dict[str, list[str]]:
    return {
        "findings": [
            "The hidden requirement is likely runtime integration, not only files.",
            "The answer should separate candidate criteria from verified facts.",
        ],
        "criteria": [
            "Output labels assumptions separately from verification evidence.",
            "Caller can distinguish candidate criteria from completed work.",
        ],
        "anti": ["Anti: Candidate findings are not presented as verified completion."],
    }


LENS_FUNCS: dict[str, tuple[str, Callable[[str, list[str]], dict[str, list[str]]]]] = {
    "Literal": ("What did they explicitly say?", literal),
    "Stakeholder": ("Who else cares, and what do they need?", stakeholder),
    "Failure": ("What could fail or be exploited?", failure),
    "Experiential": ("How should the result feel to operate?", experiential),
    "Temporal": ("How does this change over time?", temporal),
    "Constraint Inversion": ("What if constraints are removed or made extreme?", constraint_inversion),
    "Analogical": ("What existing pattern should this resemble?", analogical),
    "Meta": ("Is this the right framing?", meta),
}


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = re.sub(r"\s+", " ", item.strip().lower())
        if key and key not in seen:
            seen.add(key)
            result.append(item.strip())
    return result


def run_iterative_depth(problem: str, depth: int, sla: str) -> dict[str, Any]:
    safe_problem, redaction = redact_text(problem)
    files = artifacts(safe_problem)
    lens_names = select_lens_names(safe_problem, depth)

    passes: list[dict[str, Any]] = []
    all_criteria: list[str] = []
    all_anti: list[str] = []
    for name in lens_names:
        question, func = LENS_FUNCS[name]
        lens_result = func(safe_problem, files)
        all_criteria.extend(lens_result["criteria"])
        all_anti.extend(lens_result["anti"])
        passes.append(
            {
                "lens": name,
                "question": question,
                "findings": lens_result["findings"],
                "candidate_criteria": lens_result["criteria"],
                "candidate_anti_criteria": lens_result["anti"],
            }
        )

    criteria = [
        {"id": f"ISC-{index}", "text": text}
        for index, text in enumerate(dedupe(all_criteria), start=1)
    ]
    anti = [
        {"id": f"ISC-A{index}", "text": text}
        for index, text in enumerate(dedupe(all_anti), start=1)
    ]
    if not lens_names:
        key_insight = "No lenses were applied at instant SLA."
    else:
        artifact_specific = sum(
            1 for item in dedupe(all_criteria) if any(name in item for name in files)
        )
        generic = len(criteria) - artifact_specific
        key_insight = (
            f"Lens order was driven by {lens_driver(safe_problem)}; "
            f"{len(files)} explicit artifact(s) detected. "
            f"{generic} of {len(criteria)} candidate criteria are generic defaults — "
            "refine them against the task before adoption."
        )
    result = {
        "result": "ok",
        "skill": "iterative_depth",
        "sla": sla,
        "depth": depth,
        "problem_summary": problem_summary(safe_problem),
        "problem_hash": content_hash(safe_problem),
        "lenses_used": lens_names,
        "passes": passes,
        "candidate_criteria": criteria,
        "candidate_anti_criteria": anti,
        "key_insight": key_insight,
        "redacted": redaction["redacted"],
    }
    safe_log(
        pai_root(),
        {
            "ts": now(),
            "source": "codex_skill_dispatch",
            "skill": "iterative_depth",
            "sla": sla,
            "depth": depth,
            "lenses": lens_names,
            "criteria_count": len(criteria),
            "anti_count": len(anti),
            "problem_hash": result["problem_hash"],
            "result": "ok",
            "redaction": redaction,
        },
    )
    return result


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"ITERATIVE DEPTH COMPLETE ({result['depth']} lenses applied)",
        "",
        "Coverage:",
        f"- Lenses used: {', '.join(result['lenses_used']) or 'none'}",
        f"- New criteria discovered: {len(result['candidate_criteria'])}",
        f"- Anti-criteria discovered: {len(result['candidate_anti_criteria'])}",
        "",
        "New ISC Criteria:",
    ]
    lines.extend(f"- {item['id']}: {item['text']}" for item in result["candidate_criteria"])
    lines.extend(["", "New Anti-Criteria:"])
    if result["candidate_anti_criteria"]:
        lines.extend(f"- {item['id']}: {item['text']}" for item in result["candidate_anti_criteria"])
    else:
        lines.append("- none")
    lines.extend(["", f"Key Insight: {result['key_insight']}"])
    return "\n".join(lines) + "\n"


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Run deterministic IterativeDepth lens analysis.")
    parser.add_argument("--sla", choices=sorted(SLA_DEPTH), default="standard", help="Depth preset. Default: standard.")
    parser.add_argument("--depth", type=int, help="Override depth, 0 through 8.")
    parser.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format. Default: json.")
    parser.add_argument("problem", nargs="*", help="Problem prompt. Read from stdin when omitted.")
    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        problem = collect_problem(args.problem)
        depth = SLA_DEPTH[args.sla] if args.depth is None else args.depth
        if depth < 0 or depth > 8:
            raise SkillError("depth must be between 0 and 8")
        result = run_iterative_depth(problem, depth, args.sla)
        if args.format == "markdown":
            print(render_markdown(result), end="")
        else:
            print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        safe_log(
            pai_root(),
            {
                "ts": now(),
                "source": "codex_skill_dispatch",
                "skill": "iterative_depth",
                "result": "rejected",
                "error_type": exc.__class__.__name__,
            },
        )
        print(str(exc), file=sys.stderr)
        return 1 if isinstance(exc, SkillError) else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
