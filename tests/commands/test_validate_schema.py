"""tests/commands/test_validate_schema.py.

Tests for commands/validate_schema.py - schema internal consistency command.
"""

import os
from pathlib import Path
from unittest.mock import patch

from adaptive_manifest_schema.commands.validate_schema import run


def test_validate_schema_passes() -> None:
    """run() against this repo's own manifest-schema.toml must return 0."""
    repo_root = Path(__file__).parent.parent.parent
    old = Path.cwd()
    os.chdir(repo_root)
    try:
        result = run()
        assert result == 0
    finally:
        os.chdir(old)


def test_validate_schema_strict_passes_when_no_warnings() -> None:
    repo_root = Path(__file__).parent.parent.parent
    old = Path.cwd()
    os.chdir(repo_root)
    try:
        result = run(strict=True)
        assert result == 0
    finally:
        os.chdir(old)


def test_validate_schema_missing_schema_file_returns_1(tmp_path: Path) -> None:
    old = Path.cwd()
    os.chdir(tmp_path)
    try:
        result = run()
        assert result == 1
    finally:
        os.chdir(old)


def test_validate_schema_require_tag_fails_when_not_on_tag() -> None:
    repo_root = Path(__file__).parent.parent.parent
    old = Path.cwd()
    os.chdir(repo_root)
    try:
        with patch(
            "adaptive_manifest_schema.validate_contract.get_git_tag",
            side_effect=RuntimeError("not on a tagged commit"),
        ):
            result = run(require_tag=True)
            assert result == 1
    finally:
        os.chdir(old)


def test_validate_schema_strict_and_require_tag_together() -> None:
    """--strict and --require-tag can be combined."""
    repo_root = Path(__file__).parent.parent.parent
    old = Path.cwd()
    os.chdir(repo_root)
    try:
        with patch(
            "adaptive_manifest_schema.validate_contract.get_git_tag",
            side_effect=RuntimeError("not on a tagged commit"),
        ):
            result = run(strict=True, require_tag=True)
            assert result == 1
    finally:
        os.chdir(old)


def test_validate_schema_invalid_schema_returns_1(tmp_path: Path) -> None:
    """A schema file with an invalid field type should fail."""
    (tmp_path / "manifest-schema.toml").write_text(
        """
[section.repo]
allowed_fields = ["name"]

[field.repo]
name = {type = "not-a-valid-type", required = true}

[class]

[validation]
""",
        encoding="utf-8",
    )
    old = Path.cwd()
    os.chdir(tmp_path)
    try:
        result = run()
        assert result == 1
    finally:
        os.chdir(old)
