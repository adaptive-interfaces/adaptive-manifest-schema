"""Tests for validate_manifest.py - MANIFEST.toml conformance."""

import os
from pathlib import Path
from typing import Any, cast

from adaptive_manifest_schema.load import load_manifest, load_schema
from adaptive_manifest_schema.types.manifest_schema import ManifestSchemaData
from adaptive_manifest_schema.validate_manifest import validate_manifest


def _minimal_schema() -> ManifestSchemaData:
    return cast(
        ManifestSchemaData,
        {
            "manifest": {
                "identity": {
                    "schema_required": True,
                    "schema_allowed": ["adaptive-interfaces-manifest-1"],
                    "schema_url_required": True,
                }
            },
            "section": {
                "repo": {"required": True, "allowed_fields": ["name", "class"]},
                "scope": {"required": True, "allowed_fields": ["includes", "excludes"]},
            },
            "field": {
                "repo": {
                    "name": {"type": "string", "required": True},
                    "class": {"type": "string", "required": True},
                },
                "scope": {
                    "includes": {"type": "list[string]", "required": True},
                    "excludes": {"type": "list[string]", "required": True},
                },
            },
            "class": {
                "library": {
                    "required_sections": ["repo", "scope"],
                    "optional_sections": [],
                    "forbidden_sections": [],
                }
            },
            "validation": {
                "require_known_sections_only": True,
                "require_known_fields_only": True,
            },
        },
    )


def _minimal_manifest() -> dict[str, Any]:
    return {
        "schema": "adaptive-interfaces-manifest-1",
        "schema_url": "https://example.com",
        "repo": {"name": "test-repo", "class": "library"},
        "scope": {"includes": ["something"], "excludes": []},
    }


def test_own_manifest_is_valid(tmp_path: Path) -> None:
    """The shipped MANIFEST.toml must conform to the schema."""
    repo_root = Path(__file__).parent.parent
    manifest = load_manifest(repo_root / "MANIFEST.toml")
    old = Path.cwd()
    os.chdir(repo_root)
    try:
        schema = cast(ManifestSchemaData, load_schema())
    finally:
        os.chdir(old)
    errors = validate_manifest(manifest, schema)
    assert errors == [], "\n".join(errors)


def test_valid_manifest_passes() -> None:
    errors = validate_manifest(_minimal_manifest(), _minimal_schema())
    assert errors == []


def test_missing_required_section_detected() -> None:
    manifest = _minimal_manifest()
    del manifest["scope"]
    errors = validate_manifest(manifest, _minimal_schema())
    assert any("scope" in e for e in errors)


def test_forbidden_section_detected() -> None:
    schema = cast(
        ManifestSchemaData,
        {
            **_minimal_schema(),
            "class": {
                "library": {
                    "required_sections": ["repo", "scope"],
                    "optional_sections": [],
                    "forbidden_sections": ["scope"],
                }
            },
        },
    )
    errors = validate_manifest(_minimal_manifest(), schema)
    assert any("forbids" in e for e in errors)


def test_unknown_section_detected() -> None:
    manifest = _minimal_manifest()
    manifest["surprise"] = {"key": "value"}
    errors = validate_manifest(manifest, _minimal_schema())
    assert any("surprise" in e for e in errors)


def test_unknown_field_detected() -> None:
    manifest = _minimal_manifest()
    manifest["repo"]["unknown_field"] = "value"
    errors = validate_manifest(manifest, _minimal_schema())
    assert any("unknown_field" in e for e in errors)


def test_invalid_schema_value_detected() -> None:
    manifest = _minimal_manifest()
    manifest["schema"] = "wrong-schema"
    errors = validate_manifest(manifest, _minimal_schema())
    assert any("wrong-schema" in e for e in errors)


def test_missing_schema_url_detected() -> None:
    manifest = _minimal_manifest()
    del manifest["schema_url"]
    errors = validate_manifest(manifest, _minimal_schema())
    assert any("schema_url" in e for e in errors)


def test_unknown_class_detected() -> None:
    manifest = _minimal_manifest()
    manifest["repo"]["class"] = "nonexistent"
    errors = validate_manifest(manifest, _minimal_schema())
    assert any("nonexistent" in e for e in errors)


def test_missing_repo_section_detected() -> None:
    manifest = _minimal_manifest()
    del manifest["repo"]
    errors = validate_manifest(manifest, _minimal_schema())
    assert any("repo" in e for e in errors)
