#!/usr/bin/env bash
set -euo pipefail

# Asymmetry is the failure, not absolute counts. If a canonical token is protected on one side/function but missing from its required counterpart, print which side/function lacks which token and exit 1.

SCRIPT_SOURCE="${BASH_SOURCE[0]}"
while [[ -L "$SCRIPT_SOURCE" ]]; do
  SCRIPT_DIR_LINK="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
  SCRIPT_SOURCE="$(readlink "$SCRIPT_SOURCE")"
  [[ "$SCRIPT_SOURCE" != /* ]] && SCRIPT_SOURCE="$SCRIPT_DIR_LINK/$SCRIPT_SOURCE"
done
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
PKG_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

TMP_HOME="$(mktemp -d "${TMPDIR:-/tmp}/pai-codex-lib-parity.XXXXXX")"
cleanup() {
  find "$TMP_HOME" -depth -type f -delete 2>/dev/null || true
  find "$TMP_HOME" -depth -type l -delete 2>/dev/null || true
  find "$TMP_HOME" -depth -type d -empty -delete 2>/dev/null || true
}
trap cleanup EXIT

PYTHON_SRC="${PAI_PARITY_PYTHON_SRC:-$PKG_DIR/hooks/pre-tool-use.sh}"
TS_SRC="${PAI_PARITY_TS_SRC:-$PKG_DIR/../hooks/lib/containment-zones.ts}"

python3 - "$PYTHON_SRC" "$TS_SRC" <<'PY'
from __future__ import annotations

from pathlib import Path
import re
import sys

python_src = Path(sys.argv[1])
ts_src = Path(sys.argv[2])


def fail(message: str) -> None:
    raise SystemExit(message)


def read_text(path: Path, label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        fail(f"could not read {label}: {path} ({exc})")


def extract_def_block(source: str, name: str) -> str:
    lines = source.splitlines()
    start = None
    signature = f"def {name}("
    for index, line in enumerate(lines):
        if line.startswith(signature):
            start = index
            break
    if start is None:
        fail("could not extract python protected tokens")
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        stripped = line.strip()
        if stripped and not line.startswith((" ", "\t")) and not stripped.startswith("#"):
            end = index
            break
    return "\n".join(lines[start:end]) + "\n"


def python_token_set(values: list[object]) -> set[str]:
    tokens: set[str] = set()
    for value in values:
        low = str(value).lower()
        if ".ssh" in low:
            tokens.add("ssh")
        if ".gnupg" in low:
            tokens.add("gnupg")
        if ".aws" in low:
            tokens.add("aws")
        if "config/gcloud" in low:
            tokens.add("config/gcloud")
        if "codex/auth.json" in low:
            tokens.add("codex/auth.json")
        if "claude/.env" in low:
            tokens.add("claude/.env")
    return tokens


def extract_python_tokens(source: str) -> tuple[set[str], set[str]]:
    namespace = {
        "HOME": "/tmp/parity-fake-home",
        "Path": Path,
    }
    try:
        code = extract_def_block(source, "protected_terms") + "\n" + extract_def_block(source, "protected_paths")
        exec(code, namespace)
        protected_terms = namespace["protected_terms"]()
        protected_paths = namespace["protected_paths"]()
    except SystemExit:
        raise
    except Exception:
        fail("could not extract python protected tokens")
    if not isinstance(protected_terms, list) or not isinstance(protected_paths, list):
        fail("could not extract python protected tokens")
    return python_token_set(protected_terms), python_token_set(protected_paths)


def extract_zone_patterns(source: str, zone_name: str) -> list[str]:
    pattern = re.compile(
        r'name:\s*"(?P<name>[^"]+)"\s*,\s*patterns:\s*\[(?P<patterns>.*?)\]\s*,\s*description:',
        re.S,
    )
    for match in pattern.finditer(source):
        if match.group("name").lower() == zone_name:
            return [value.lower() for value in re.findall(r'"([^"]+)"', match.group("patterns"))]
    fail("could not extract typescript protected tokens")


def extract_ts_tokens(source: str) -> set[str]:
    tokens: set[str] = set()
    for raw in extract_zone_patterns(source, "config-secrets"):
        if ".env" in raw:
            tokens.add("env")
        if raw.endswith("settings.json"):
            tokens.add("settings.json")
    for raw in extract_zone_patterns(source, "user-data"):
        if raw == "pai/user/**":
            tokens.add("pai/user/**")
    return tokens


python_source = read_text(python_src, "python source")
ts_source = read_text(ts_src, "typescript source")

terms_tokens, paths_tokens = extract_python_tokens(python_source)
ts_tokens = extract_ts_tokens(ts_source)

shared_tokens = {
    "ssh",
    "gnupg",
    "aws",
    "codex/auth.json",
    "claude/.env",
}

for token in sorted(shared_tokens):
    if token not in terms_tokens:
        fail(f"python protected_terms missing {token}")
    if token not in paths_tokens:
        fail(f"python protected_paths missing {token}")

if "config/gcloud" not in terms_tokens:
    fail("python protected_terms missing config/gcloud")
if "config/gcloud" in paths_tokens:
    fail("python protected_paths unexpectedly contains config/gcloud")

python_has_env = "claude/.env" in (terms_tokens | paths_tokens)
ts_has_env = "env" in ts_tokens
if python_has_env and not ts_has_env:
    fail("typescript config-secrets missing env")
if ts_has_env and not python_has_env:
    fail("python protected terms/paths missing claude/.env")
PY

echo "lib parity test passed"
