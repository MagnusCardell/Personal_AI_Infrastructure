from __future__ import annotations

import argparse
import json
import sys

from tools.pai_runtime_runner.install import RuntimeInstallError, install_runtime, rollback_runtime


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install or rollback the PAI runtime runner package.")
    parser.add_argument("--pai-dir", required=True)
    parser.add_argument("--backup-root", required=True)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--install", action="store_true")
    action.add_argument("--rollback", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.install:
            result = install_runtime(args.pai_dir, args.backup_root)
            message = f"OK: PAI runtime runner installed to {result['pai_dir']}"
        else:
            result = rollback_runtime(args.pai_dir, args.backup_root)
            message = f"OK: PAI runtime runner rollback completed for {result['pai_dir']}"
    except (RuntimeInstallError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
