from __future__ import annotations

import argparse
import sys

from .install import InstallerError, apply_install, rollback_install, validate_install


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install, validate, or rollback the S15A Codex adapter.")
    parser.add_argument("--pai-dir", required=True, help="PAI subsystem root, normally ~/.claude/PAI.")
    parser.add_argument("--backup-root", help="Backup root created before live writes.")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--apply", action="store_true", help="Apply the staged Codex adapter payload.")
    action.add_argument("--validate", action="store_true", help="Validate the installed Codex adapter payload.")
    action.add_argument("--rollback", action="store_true", help="Rollback approved adapter targets from backup.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.apply:
            result = apply_install(args.pai_dir, args.backup_root)
            print(f"OK: Codex adapter applied to {result['pai_dir']}")
        elif args.validate:
            result = validate_install(args.pai_dir, args.backup_root)
            print(f"OK: Codex adapter validation passed for {result['pai_dir']}")
        elif args.rollback:
            result = rollback_install(args.pai_dir, args.backup_root)
            print(f"OK: Codex adapter rollback completed for {result['pai_dir']}")
    except InstallerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
