"""CLI entry point for consent-gated preflight evidence generation."""

from __future__ import annotations

import argparse
import sys

from .preflight import RUN_CONTEXT_FIXTURE, RUN_CONTEXT_INSTALLED_PAI, run_fixture_preflight, run_installed_pai_preflight
from .report import write_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the S14 PAI preflight in an explicit context.")
    parser.add_argument("--run-context", choices=[RUN_CONTEXT_FIXTURE, RUN_CONTEXT_INSTALLED_PAI], default=RUN_CONTEXT_FIXTURE)
    parser.add_argument("--fixture-root")
    parser.add_argument("--installed-source-root")
    parser.add_argument("--consent", required=True)
    parser.add_argument("--declared-source-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--output", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.run_context == RUN_CONTEXT_FIXTURE:
        if not args.fixture_root:
            parser.error("--fixture-root is required for fixture run context")
        report = run_fixture_preflight(
            fixture_root=args.fixture_root,
            consent_path=args.consent,
            declared_source_root=args.declared_source_root,
        )
    elif args.run_context == RUN_CONTEXT_INSTALLED_PAI:
        if not args.installed_source_root:
            parser.error("--installed-source-root is required for installed-pai run context")
        report = run_installed_pai_preflight(
            installed_source_root=args.installed_source_root,
            consent_path=args.consent,
            declared_source_root=args.declared_source_root,
        )
    else:
        parser.error("unsupported run context")
    output = write_report(report, args.output_root, args.output)
    print(f"{args.run_context} preflight report written: {output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
