"""src/adaptive_manifest_schema/commands/validate.py.

Validate any MANIFEST.toml against the schema.
Safe to run in any repo; no sync, no schema internal check.
"""

from pathlib import Path
from typing import cast

from adaptive_manifest_schema.load import load_manifest, load_schema
from adaptive_manifest_schema.types.manifest_schema import ManifestSchemaData
from adaptive_manifest_schema.validate_contract import validate_tag
from adaptive_manifest_schema.validate_manifest import validate_manifest


def run(
    *,
    path: Path | None = None,
    strict: bool = False,
    require_tag: bool = False,
) -> int:
    """Validate a MANIFEST.toml file against the schema.

    Args:
        path: Path to MANIFEST.toml. Defaults to ./MANIFEST.toml.
        strict: Treat warnings as errors.
        require_tag: Require CITATION.cff version to match current git tag.

    Returns:
        0 on success, 1 on failure.
    """
    errors: list[str] = []
    warnings: list[str] = []

    try:
        manifest = load_manifest(path)
        schema = load_schema()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")  # noqa: T201
        return 1

    manifest_label = str(path) if path else "MANIFEST.toml"
    print(f"[validate] {manifest_label}")  # noqa: T201

    if require_tag:
        errors.extend(validate_tag(manifest))

    errors.extend(validate_manifest(manifest, cast(ManifestSchemaData, schema)))

    for e in errors:
        print(f"ERROR: {e}")  # noqa: T201
    for w in warnings:
        print(f"WARNING: {w}")  # noqa: T201

    if errors:
        return 1
    if strict and warnings:
        return 1

    print("Manifest validation passed.")  # noqa: T201
    return 0
