"""validate_manifest.py - Validates any MANIFEST.toml against the schema.

Imported by consumers to validate their own MANIFEST.toml.
Does not know about git tags or version alignment.

Checks:
  - required top-level fields (schema, schema_url)
  - required sections for declared class are present
  - forbidden sections for declared class are absent
  - no unknown sections (if require_known_sections_only is set)
  - no unknown fields within sections (if require_known_fields_only is set)
  - required fields within sections are present
"""

from typing import Any, cast

from adaptive_manifest_schema.types.manifest_schema import ManifestSchemaData


def _get_validation_rules(schema: ManifestSchemaData) -> dict[str, Any]:
    """Extract validation rules from schema."""
    return cast(dict[str, Any], schema.get("validation", {}))


def _get_class_def(
    schema: ManifestSchemaData, class_name: str
) -> dict[str, Any] | None:
    """Return class definition for the given class name, or None."""
    classes = schema.get("class", {})
    value = classes.get(class_name)
    if not isinstance(value, dict):
        return None
    return value  # type: ignore[return-value]


def _get_section_def(
    schema: ManifestSchemaData, section_name: str
) -> dict[str, Any] | None:
    """Return section definition for the given section name, or None."""
    sections = schema.get("section", {})
    value = sections.get(section_name)
    if not isinstance(value, dict):
        return None
    return value  # type: ignore[return-value]


def validate_manifest(
    manifest: dict[str, Any],
    schema: ManifestSchemaData,
) -> list[str]:
    """Validate a manifest dict against the schema.

    Args:
        manifest: Parsed MANIFEST.toml content.
        schema: Parsed schema/manifest-1.toml content.

    Returns:
        List of error strings. Empty list means valid.
    """
    errors: list[str] = []
    rules = _get_validation_rules(schema)

    # top-level identity fields
    manifest_section = schema.get("manifest")
    identity: dict[str, object] = {}
    if isinstance(manifest_section, dict):
        identity_raw = manifest_section.get("identity")
        if isinstance(identity_raw, dict):
            identity = cast(dict[str, object], identity_raw)

    schema_required = identity.get("schema_required")
    if isinstance(schema_required, bool) and schema_required:
        schema_val = manifest.get("schema")
        allowed_raw = identity.get("schema_allowed")
        allowed: list[str] = (
            cast(list[str], allowed_raw) if isinstance(allowed_raw, list) else []
        )
        if schema_val not in allowed:
            errors.append(
                f"manifest.schema: '{schema_val}' not in allowed values {allowed}"
            )

    schema_url_required = identity.get("schema_url_required")
    if (
        isinstance(schema_url_required, bool)
        and schema_url_required
        and not manifest.get("schema_url")
    ):
        errors.append("manifest.schema_url: required but missing")

    # repo section and class
    repo = manifest.get("repo")
    if not isinstance(repo, dict):
        errors.append("manifest missing required [repo] section")
        return errors

    typed_repo = cast(dict[str, object], repo)
    class_name = typed_repo.get("class")
    if not isinstance(class_name, str):
        errors.append("[repo].class: required string field missing")
        return errors

    class_def = _get_class_def(schema, class_name)
    if class_def is None:
        errors.append(f"[repo].class: unknown class '{class_name}'")
        return errors

    known_sections = set(schema.get("section", {}).keys())
    manifest_sections = {k for k in manifest if isinstance(manifest.get(k), dict)}

    # unknown sections
    if rules.get("require_known_sections_only"):
        for section in manifest_sections:
            if section not in known_sections:
                errors.append(f"unknown section '[{section}]'")

    # required sections
    for section in class_def.get("required_sections", []):
        if section not in manifest:
            errors.append(
                f"class '{class_name}' requires section '[{section}]' but it is missing"
            )

    # forbidden sections
    for section in class_def.get("forbidden_sections", []):
        if section in manifest:
            errors.append(
                f"class '{class_name}' forbids section '[{section}]' but it is present"
            )

    # required and unknown fields within sections
    all_fields: dict[str, Any] = cast(dict[str, Any], schema.get("field", {}))
    for section_name in manifest_sections:
        section_def = _get_section_def(schema, section_name)
        if section_def is None:
            continue
        section_data = manifest.get(section_name, {})
        if not isinstance(section_data, dict):
            continue

        allowed_fields = section_def.get("allowed_fields", [])

        if rules.get("require_known_fields_only"):
            section_data_typed = cast(dict[str, object], section_data)
            for field_name in section_data_typed:
                if field_name not in allowed_fields:
                    errors.append(f"[{section_name}].{field_name}: unknown field")

        section_field_defs: dict[str, Any] = cast(
            dict[str, Any], all_fields.get(section_name, {})
        )
        for field_name in allowed_fields:
            field_def = section_field_defs.get(field_name, {})
            if not isinstance(field_def, dict):
                continue
            field_def_typed: dict[str, Any] = cast(dict[str, Any], field_def)
            if field_def_typed.get("required") and field_name not in section_data:
                errors.append(f"[{section_name}].{field_name}: required field missing")

    return errors
