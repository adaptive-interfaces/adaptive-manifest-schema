# adaptive-manifest-schema

<!-- Design for durability; do not introduce drift -->

Canonical `MANIFEST.toml` schema and validator for the Adaptive Interfaces ecosystem.

See the [repository](https://github.com/adaptive-interfaces/adaptive-manifest-schema)
for full documentation.

## Contents

- [Glossary](./glossary.md)
- [API Reference](./api.md)
- [Scaffold Process](./scaffold.md)
- [Schema Evolution](./evolution.md)

## What this repo owns

One file: `schema/manifest-1.toml` at the repository root.

It defines what sections, fields, and class requirements
are valid in any `MANIFEST.toml`.
Downstream repos import `validate_manifest` to check
their own manifests against this schema.
