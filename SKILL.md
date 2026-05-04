# SKILL.md (adaptive-manifest-schema)

Agent operating guide for the `MANIFEST.toml` schema and validator.

This skill operates under the
[Adaptive Conformance Specification (ACS)](https://github.com/adaptive-interfaces/adaptive-conformance-specification).
Apply ACS discovery and conformance steps before executing any domain-specific actions below.

---

## Motivation

Every Adaptive Interfaces repository includes a `MANIFEST.toml` declaring
its identity, scope, dependencies, and tooling configuration.
This repository defines and validates that schema.

It has no upstream Adaptive Interfaces dependencies.
All other repos in the ecosystem depend on it.
It is the foundation layer.

---

## Scope

### Included

- The `validate_manifest` function; importable by downstream repos
- The `validate_schema_internal` function; for this repo only
- The CLI subcommands: `validate`, `validate-schema`, `sync-version`
- Agent safety field enum validation
- Operating rules for agents working in this repo or consuming this API
- Test coverage requirements
- Failure modes and stopping conditions

### Excluded

- Repo scaffolding or generation tools
- Convention file management
- CI workflow templates
- Schemas specific to other organizations

---

## Core Design Constraints

**R-C1. No upstream adaptive-interfaces dependencies.**
This repo imports nothing from other adaptive-interfaces packages at runtime.
This is a hard constraint; see DECISIONS.md D-005.
Any change that introduces such an import is a breaking violation.

**R-C2. Schema changes require a DECISIONS.md entry before implementation.**
Do not add, remove, or rename schema fields without first recording the decision.
See DECISIONS.md for the format and all prior decisions.

**R-C3. Validator changes require test and SKILL.md updates.**
Do not change `validate_manifest.py` or `validate_schema.py` behavior
without updating tests and this document.

---

## Public API

### `validate_manifest(manifest, schema)`

The primary public function. Importable by downstream consumers.

```python
from adaptive_manifest_schema.validate_manifest import validate_manifest
from adaptive_manifest_schema.load import load_manifest, load_schema
from typing import cast
from adaptive_manifest_schema.types.manifest_schema import ManifestSchemaData

manifest = load_manifest()                          # reads ./MANIFEST.toml
schema = cast(ManifestSchemaData, load_schema())    # reads ./manifest-schema.toml
errors = validate_manifest(manifest, schema)

if errors:
    for e in errors:
        print(f"ERROR: {e}")
```

Returns `list[str]`. Empty list means valid.

**What it checks:**

- `schema` field is in `schema_allowed`
- `schema_url` is present
- `[repo].class` is declared and exists in the class registry
- Required sections for the declared class are present
- Forbidden sections for the declared class are absent
- Unknown sections (if `require_known_sections_only` is set)
- Unknown fields within sections (if `require_known_fields_only` is set)
- Required fields within sections are present
- Agent safety field enum values are from the allowed set

### `validate_schema_internal(schema)`

For this repo only. Validates `manifest-schema.toml` internal consistency.

```python
from adaptive_manifest_schema.validate_schema import validate_schema_internal
from adaptive_manifest_schema.load import load_schema
from typing import cast
from adaptive_manifest_schema.types.manifest_schema import ManifestSchemaData

schema = cast(ManifestSchemaData, load_schema())
errors = validate_schema_internal(schema)
```

**What it checks:**

- All sections referenced in class definitions exist in `[section.*]`
- All fields in `allowed_fields` have definitions in `[field.*]`
- All field types are from the allowed set: `string`, `boolean`, `list[string]`, `integer`

### `load_manifest(path)`

```python
from adaptive_manifest_schema.load import load_manifest
from pathlib import Path

manifest = load_manifest()                          # reads ./MANIFEST.toml
manifest = load_manifest(Path("other/MANIFEST.toml"))
```

### `load_schema()`

```python
from adaptive_manifest_schema.load import load_schema

schema = load_schema()    # reads ./manifest-schema.toml
```

Reads `manifest-schema.toml` from the current working directory.
Run from the `adaptive-manifest-schema` repo root, or `chdir` first.

---

## CLI Subcommands

### `adaptive-manifest validate`

Safe to run in any repo. No sync, no schema internal check.

```shell
uv run adaptive-manifest validate
uv run adaptive-manifest validate --strict
uv run adaptive-manifest validate --require-tag
uv run adaptive-manifest validate --path path/to/MANIFEST.toml
```

| Flag            | Effect                                                |
| --------------- | ----------------------------------------------------- |
| `--strict`      | Treat warnings as errors                              |
| `--require-tag` | Require CITATION.cff version to match current git tag |
| `--path`        | Validate a specific file instead of `./MANIFEST.toml` |

Returns 0 on success, 1 on failure.

### `adaptive-manifest validate-schema`

This repo only. Validates `manifest-schema.toml` internal consistency.

```shell
uv run adaptive-manifest validate-schema
uv run adaptive-manifest validate-schema --strict
uv run adaptive-manifest validate-schema --require-tag
```

### `adaptive-manifest sync-version`

This repo only. Syncs `CITATION.cff` version to `pyproject.toml` fallback-version.
Never called automatically; always explicit.

```shell
uv run adaptive-manifest sync-version
```

---

## Agent Safety Fields

The `[agent]` section in `MANIFEST.toml` declares the authorized operation scope
for agents in a repo. The validator enforces allowed values.

| Field               | Allowed values                             | Default when omitted    |
| ------------------- | ------------------------------------------ | ----------------------- |
| `permissions`       | `read-only`, `read-generate`, `read-write` | `read-generate`         |
| `checkpoint`        | `human-review-required`, `automated`       | `human-review-required` |
| `scope`             | `this-repo-only`, `multi-repo`             | `this-repo-only`        |
| `sensitive_paths`   | `list[string]`                             | none                    |
| `stop_on_ambiguity` | `boolean`                                  | `true`                  |

**Critical invariant:** Omitting fields never grants additional permissions.
Conservative defaults apply when any field is absent.
See DECISIONS.md D-006 for full rationale.

---

## Operating Rules

**R-01. Run `validate` before asserting manifest correctness.**
Do not infer conformance from visual inspection of a MANIFEST.toml.
Call `validate_manifest` or `adaptive-manifest validate` and check the return value.

**R-02. Load schema from the repo root, not a hardcoded path.**
`load_schema()` reads `manifest-schema.toml` from the current working directory.
Ensure the working directory is correct before calling it.

**R-03. Do not introduce upstream adaptive-interfaces imports.**
See R-C1. This is a hard constraint, not a preference.

**R-04. Do not call `sync-version` from within `validate`.**
These are explicitly separated. See DECISIONS.md D-007.
`validate` has no version sync side effects.

**R-05. Use `--require-tag` only after pushing a tag.**
`validate --require-tag` checks CITATION.cff version against the current git tag.
It will always fail before the tag exists on the remote.
It belongs in Task 5 of the release procedure, after `git push origin vX.Y.Z`.

**R-06. An empty error list is the only valid conformance signal.**
`validate_manifest` returns `list[str]`.
Do not treat a short list or a list with only warnings as passing.
Empty list means valid; any entry means invalid.

**R-07. Schema changes go in `manifest-schema.toml`, not in Python.**
The schema is defined in `manifest-schema.toml` at the repo root.
Python code reads and enforces the schema; it does not define it.
Agent safety field enum values are defined in `validate_manifest.py`
as Python constants; these are the exception and are documented in D-006.

---

## Test Coverage Requirements

A conforming test suite for a downstream consumer includes at minimum:

| Case type                 | Required                                                     |
| ------------------------- | ------------------------------------------------------------ |
| Valid manifest passes     | Minimal valid manifest with all required sections            |
| Missing required section  | Each required section tested independently                   |
| Unknown class detected    | `[repo].class` set to an unregistered value                  |
| Invalid schema value      | `schema` field set to an unknown string                      |
| Missing schema_url        | `schema_url` field absent                                    |
| Agent safety enum invalid | One test per field: `permissions`, `checkpoint`, `scope`     |
| Agent safety type invalid | `sensitive_paths` not a list; `stop_on_ambiguity` not a bool |
| Agent absent passes       | Omitting `[agent]` entirely is valid                         |
| Own manifest valid        | The repo's own `MANIFEST.toml` must pass `validate_manifest` |

---

## Failure Modes and Stopping Conditions

Stop and report if any of the following are true:

- `validate_manifest` is called without loading `manifest-schema.toml` first
- A downstream import from another adaptive-interfaces package is introduced
- Agent safety fields are validated without checking the allowed value sets
- `sync-version` is called as a side effect of `validate`
- Schema field semantics are changed without a DECISIONS.md entry

Do not proceed to schema modification or validator generation until
the operating rules above are confirmed understood.

---

## Invocation

Skills that require manifest validation include this in their preamble:

> This skill uses `adaptive-manifest-schema` for MANIFEST.toml validation.
> Read `adaptive-manifest-schema/SKILL.md` and apply all operating rules
> before generating any schema definitions or validator logic.

---

## Repository Contents

```text
adaptive-manifest-schema/
  SKILL.md                  this document
  DECISIONS.md              design history and rationale
  MANIFEST.toml             repository declaration
  AGENTS.md                 workflow requirements
  CLAUDE.md                 behavioral constraints for AI collaborators
  manifest-schema.toml      canonical schema definition (source of truth)
  src/adaptive_manifest_schema/
    validate_manifest.py    primary public API; importable by consumers
    validate_schema.py      schema internal consistency; this repo only
    validate_contract.py    tag alignment
    load.py                 file loading primitives
    sync.py                 version sync
    cli.py                  pure CLI dispatcher
    commands/
      validate.py           validate subcommand
      validate_schema.py    validate-schema subcommand
      sync_version.py       sync-version subcommand
    types/
      manifest_schema.py    TypedDict definitions
      primitives.py         shared types
  tests/
```

---

_License: MIT © 2026 [Adaptive Interfaces](https://github.com/adaptive-interfaces)_
