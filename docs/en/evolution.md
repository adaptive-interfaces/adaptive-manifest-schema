# Schema Evolution (adaptive-manifest-schema)

How changes are made to `adaptive-manifest-schema`.

## Principles

- This repo owns only `schema/manifest-1.toml`
- Changes here affect all downstream repos that declare `MANIFEST.toml`
- Validate before committing
- Tag every release; downstream repos pin by tag
- Record every schema change in `DECISIONS.md` before implementing it

## Standard Workflow

### 1. Add a DECISIONS.md entry

Every schema change requires a recorded decision before any file is modified.
See `DECISIONS.md` for the format.

### 2. Edit `schema/manifest-1.toml`

Changes may include:

- adding or modifying section definitions
- adding or modifying field definitions
- adding or modifying class requirements
- updating validation rules

### 3. Validate

```shell
uv run adaptive-manifest validate
uv run pytest
```

### 4. Commit and tag

```shell
git add -A
git commit -m "Description of change"
git tag vX.Y.Z -m "X.Y.Z"
git push origin main
git push origin vX.Y.Z
```

## Common Tasks

### Add a new section

1. Add `[section.name]` with `allowed_fields` list
2. Add `[field.name.field_name]` for every field in `allowed_fields`
3. Add section to relevant `[class.*]` `optional_sections` or `required_sections`
4. Validate

### Add a new field to an existing section

1. Add field name to `[section.name]` `allowed_fields`
2. Add `[field.section_name.field_name]` with `type` and `required`
3. Validate

### Add a new repository class

1. Add `[class.name]` with `required_sections`, `optional_sections`, `forbidden_sections`
2. Validate

### Fix a validation failure

Always read the error message literally.

Typical causes:

- section referenced in a class definition not declared in `[section.*]`
- field listed in `allowed_fields` has no `[field.section.name]` definition
- field type not in allowed set (`string`, `boolean`, `list[string]`, `integer`)
- class used in `MANIFEST.toml` not declared in `[class.*]`
- enum value for `permissions`, `checkpoint`, or `scope` not in allowed set

## Versioning Policy

Schema changes follow SemVer:

- **MAJOR** - breaking changes to required sections, field types, or validation semantics
- **MINOR** - backward-compatible additions (new optional sections, new fields, new classes)
- **PATCH** - fixes, documentation, tooling

The current schema version is `adaptive-interfaces-manifest-1`.
When breaking changes are required, a new version file (`schema/manifest-2.toml`)
is created and the `schema_allowed` list is updated.
Existing repos migrate at their own pace; both versions are valid during transition.

## Design Constraint

This repo defines structure only.
It does not validate downstream `MANIFEST.toml` files directly.
Downstream repos import `validate_manifest` and run it themselves:

```python
from adaptive_manifest_schema.validate_manifest import validate_manifest
```
