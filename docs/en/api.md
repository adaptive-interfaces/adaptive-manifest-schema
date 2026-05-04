# API Reference (adaptive-manifest-schema)

Auto-generated from docstrings in `src/adaptive_manifest_schema/`.

---

## cli

Argument parsing and dispatch. Entry point for `adaptive-manifest validate` and `sync`.

::: adaptive_manifest_schema.cli
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      docstring_style: google

---

## orchestrate

Full validation sequence. Owns `run_validate()`; always syncs before validating.

::: adaptive_manifest_schema.orchestrate
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      docstring_style: google

---

## validate_manifest

Validates any `MANIFEST.toml` against the schema. Importable by downstream consumers.

::: adaptive_manifest_schema.validate_manifest
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      docstring_style: google

---

## validate_schema

Validates internal consistency of `schema/manifest-1.toml`.

::: adaptive_manifest_schema.validate_schema
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      docstring_style: google

---

## validate_contract

Version and tag alignment. Checks `CITATION.cff` version against current git tag.

::: adaptive_manifest_schema.validate_contract
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      docstring_style: google

---

## load

File loading and parsing. Owns `load_manifest()`, `load_schema()`, `get_git_tag()`.

::: adaptive_manifest_schema.load
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      docstring_style: google

---

## sync

Version sync from `CITATION.cff` to `pyproject.toml`.

::: adaptive_manifest_schema.sync
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      docstring_style: google

---

## types.manifest_schema

TypedDict definitions for the manifest schema artifact structure.

::: adaptive_manifest_schema.types.manifest_schema
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      docstring_style: google

---

## types.primitives

Shared primitive type definitions.

::: adaptive_manifest_schema.types.primitives
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      docstring_style: google
