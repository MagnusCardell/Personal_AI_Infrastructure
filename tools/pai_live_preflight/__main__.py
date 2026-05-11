"""CLI entry point for fixture-only S14C preflight evidence generation."""

from __future__ import annotations

import argparse
import sys

from .preflight import run_fixture_preflight
from .report import write_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the fixture-only S14C PAI preflight.")
    parser.add_argument("--fixture-root", required=True)
    parser.add_argument("--consent", required=True)
    parser.add_argument("--declared-source-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--output", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    report = run_fixture_preflight(
        fixture_root=args.fixture_root,
        consent_path=args.consent,
        declared_source_root=args.declared_source_root,
    )
    output = write_report(report, args.output_root, args.output)
    print(f"fixture-only preflight report written: {output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
