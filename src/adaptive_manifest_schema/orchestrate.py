"""orchestrate.py - Validation orchestrator for adaptive-manifest-schema.

Owns run_validate(). Called by cli.py. Always syncs before validating.
This is the only file that knows the full validation order.

Validation order:
  1. sync_all()                  - align CITATION.cff and pyproject.toml
  2. validate_tag()              - CITATION.cff version matches git tag (--require-tag only)
  3. validate_schema_internal()  - schema/manifest-1.toml is self-consistent
  4. validate_manifest()         - MANIFEST.toml conforms to the schema

Consumers in other repos do not call run_validate here.
They import validate_manifest directly:
  from adaptive_manifest_schema.validate_manifest import validate_manifest
"""

from pathlib import Path
from typing import cast

from adaptive_manifest_schema.load import load_manifest, load_schema
from adaptive_manifest_schema.sync import sync_all
from adaptive_manifest_schema.types.manifest_schema import ManifestSchemaData
from adaptive_manifest_schema.validate_contract import validate_tag
from adaptive_manifest_schema.validate_manifest import validate_manifest
from adaptive_manifest_schema.validate_schema import validate_schema_internal


def run_validate(
    *,
    path: Path | None = None,
    require_tag: bool = False,
    strict: bool = False,
) -> int:
    """Sync and validate schema/manifest-1.toml and MANIFEST.toml.

    Args:
        path: Path to MANIFEST.toml (default: ./MANIFEST.toml).
        require_tag: If True, verify CITATION.cff version matches current git tag.
        strict: If True, treat warnings as errors.

    Returns:
        0 on success, 1 on failure.
    """
    sync_all()

    errors: list[str] = []
    warnings: list[str] = []

    try:
        manifest = load_manifest(path)
        schema = load_schema()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")  # noqa: T201
        return 1

    manifest_label = str(path) if path else "MANIFEST.toml"
    print("[validate] schema/manifest-1.toml")  # noqa: T201
    print(f"[validate] {manifest_label}")  # noqa: T201

    if require_tag:
        errors.extend(validate_tag(manifest))

    errors.extend(validate_schema_internal(cast(ManifestSchemaData, schema)))
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
