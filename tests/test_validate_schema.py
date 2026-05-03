"""Tests for validate_schema.py - schema internal consistency."""

from typing import cast

from adaptive_manifest_schema.types.manifest_schema import ManifestSchemaData
from adaptive_manifest_schema.validate_schema import validate_schema_internal


def _valid_schema() -> ManifestSchemaData:
    return cast(
        ManifestSchemaData,
        {
            "section": {
                "repo": {"allowed_fields": ["name", "class"]},
            },
            "field": {
                "repo": {
                    "name": {"type": "string", "required": True},
                    "class": {"type": "string", "required": True},
                },
            },
            "class": {
                "library": {
                    "required_sections": ["repo"],
                    "optional_sections": [],
                    "forbidden_sections": [],
                }
            },
        },
    )


def test_valid_schema_passes() -> None:
    errors = validate_schema_internal(_valid_schema())
    assert errors == []


def test_class_references_unknown_section() -> None:
    schema = _valid_schema()
    schema["class"]["library"]["required_sections"] = ["repo", "nonexistent"]  # type: ignore[index]
    errors = validate_schema_internal(schema)
    assert any("nonexistent" in e for e in errors)


def test_section_field_missing_definition() -> None:
    schema = cast(
        ManifestSchemaData,
        {
            "section": {
                "repo": {"allowed_fields": ["name", "undocumented"]},
            },
            "field": {
                "repo": {
                    "name": {"type": "string", "required": True},
                },
            },
            "class": {},
        },
    )
    errors = validate_schema_internal(schema)
    assert any("undocumented" in e for e in errors)


def test_invalid_field_type_detected() -> None:
    schema = cast(
        ManifestSchemaData,
        {
            "section": {
                "repo": {"allowed_fields": ["name"]},
            },
            "field": {
                "repo": {
                    "name": {"type": "unknown_type", "required": True},
                },
            },
            "class": {},
        },
    )
    errors = validate_schema_internal(schema)
    assert any("unknown_type" in e for e in errors)
