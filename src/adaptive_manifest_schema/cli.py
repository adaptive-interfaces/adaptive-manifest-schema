"""cli.py - Command-line interface for adaptive-manifest-schema.

Parses arguments and dispatches to orchestrate.py or sync.py.
Owns nothing except argument parsing and error handling.
All logic lives in orchestrate.py and sync.py.

Entry points:
  uv run adaptive-manifest validate
  uv run adaptive-manifest validate --strict
  uv run adaptive-manifest validate --require-tag
  uv run adaptive-manifest validate --path path/to/MANIFEST.toml
  uv run adaptive-manifest sync

Call chain:
  __main__.py -> cli.main()
              -> orchestrate.run_validate()  (sync called internally)
              -> sync.sync_all()             (sync only, no validation)
"""

import argparse
from pathlib import Path

from adaptive_manifest_schema.orchestrate import run_validate
from adaptive_manifest_schema.sync import sync_all


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="adaptive-manifest",
        description="Validate and sync MANIFEST.toml files for Adaptive Interfaces repos.",
    )
    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser(
        "validate",
        help="Sync and validate MANIFEST.toml against the schema.",
    )
    validate_parser.add_argument(
        "--path",
        type=Path,
        default=None,
        help="Path to MANIFEST.toml (default: ./MANIFEST.toml).",
    )
    validate_parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors.",
    )
    validate_parser.add_argument(
        "--require-tag",
        action="store_true",
        help="Require CITATION.cff version to match current git tag.",
    )

    subparsers.add_parser(
        "sync",
        help="Sync pyproject.toml fallback-version from CITATION.cff version.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface.

    Returns:
        0 on success, 1 on error, 2 if no command given.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "validate":
            return run_validate(
                path=args.path,
                strict=args.strict,
                require_tag=args.require_tag,
            )
        if args.command == "sync":
            sync_all()
            return 0

    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"Error: {e}")  # noqa: T201
        return 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
