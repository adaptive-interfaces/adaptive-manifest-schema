"""Command-line interface for adaptive-manifest-schema.

Usage:
    uv run adaptive-manifest validate
    uv run adaptive-manifest validate --path path/to/MANIFEST.toml
"""

import argparse
from pathlib import Path
import sys


def main() -> None:
    """Entry point for the adaptive-manifest CLI."""
    parser = argparse.ArgumentParser(
        description="Validate MANIFEST.toml files against the adaptive-interfaces schema."
    )
    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser(
        "validate", help="Validate a MANIFEST.toml file."
    )
    validate_parser.add_argument(
        "--path",
        type=Path,
        default=Path("MANIFEST.toml"),
        help="Path to MANIFEST.toml (default: ./MANIFEST.toml).",
    )

    args = parser.parse_args()

    if args.command == "validate":
        _run_validate(args.path)
    else:
        parser.print_help()
        sys.exit(1)


def _run_validate(path: Path) -> None:
    """Run validation against the given MANIFEST.toml path."""
    if not path.exists():
        print(f"Error: {path} not found.")  # noqa: T201
        sys.exit(1)

    # Placeholder: full validation logic implemented in commit 4.
    print(f"Validating {path} ... OK (schema validation not yet implemented)")  # noqa: T201
