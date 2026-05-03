"""Tests for load.py - file loading and parsing."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from adaptive_manifest_schema.load import (
    get_git_tag,
    load_manifest,
    load_schema,
    load_toml,
)


def test_load_toml_valid(tmp_path: Path) -> None:
    f = tmp_path / "test.toml"
    f.write_text('[meta]\nversion = "1.0.0"\n', encoding="utf-8")
    data = load_toml(f)
    assert data["meta"]["version"] == "1.0.0"


def test_load_schema_found(tmp_path: Path) -> None:
    schema_dir = tmp_path / "schema"
    schema_dir.mkdir()
    (schema_dir / "manifest-1.toml").write_text(
        '[meta]\nversion = "1.0.0"\n', encoding="utf-8"
    )
    old = Path.cwd()
    os.chdir(tmp_path)
    try:
        data = load_schema()
        assert "meta" in data
    finally:
        os.chdir(old)


def test_load_schema_missing(tmp_path: Path) -> None:
    old = Path.cwd()
    os.chdir(tmp_path)
    try:
        with pytest.raises(FileNotFoundError, match="manifest-1.toml"):
            load_schema()
    finally:
        os.chdir(old)


def test_load_manifest_found(tmp_path: Path) -> None:
    (tmp_path / "MANIFEST.toml").write_text(
        'schema = "adaptive-interfaces-manifest-1"\n', encoding="utf-8"
    )
    old = Path.cwd()
    os.chdir(tmp_path)
    try:
        data = load_manifest()
        assert data["schema"] == "adaptive-interfaces-manifest-1"
    finally:
        os.chdir(old)


def test_load_manifest_missing(tmp_path: Path) -> None:
    old = Path.cwd()
    os.chdir(tmp_path)
    try:
        with pytest.raises(FileNotFoundError, match="MANIFEST.toml"):
            load_manifest()
    finally:
        os.chdir(old)


def test_load_manifest_explicit_path(tmp_path: Path) -> None:
    p = tmp_path / "OTHER.toml"
    p.write_text('[repo]\nname = "test"\n', encoding="utf-8")
    data = load_manifest(p)
    assert data["repo"]["name"] == "test"


def test_get_git_tag_no_git() -> None:
    with (
        patch("shutil.which", return_value=None),
        pytest.raises(RuntimeError, match="git executable"),
    ):
        get_git_tag()
