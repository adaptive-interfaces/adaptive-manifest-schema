# DECISIONS.md (adaptive-manifest-schema)

Design history and rationale for the Adaptive Interfaces manifest schema.
Captures decisions made before any code exists.
This document is the source of truth for why the schema is shaped the way it is.
ACS conformance depends on it.

---

## D-001. Purpose of this repository

**Status:** Accepted

**Context:**
Every Adaptive Interfaces repository includes a `MANIFEST.toml` declaring
its identity, scope, dependencies, and tooling configuration.
Without a canonical schema, these files drift across repos.
Without a validator, errors are caught late or not at all.

**Decision:**
This repository is the single canonical home for the `MANIFEST.toml` schema
and the validator CLI (`adaptive-manifest validate`).
No other repo defines or owns schema field semantics.

**Consequences:**

- All adaptive-interfaces repos depend on this repo.
- This repo has no upstream adaptive-interfaces dependencies.
- Schema changes are versioned and recorded here before taking effect anywhere.

---

## D-002. Analogy to se-manifest-schema

**Status:** Accepted

**Context:**
The Structural Explainability organization built `se-manifest-schema` as the
canonical schema and validator for `SE_MANIFEST.toml` files.
That pattern is mature and working.

**Decision:**
`adaptive-manifest-schema` follows the same architecture:
single schema repo, no upstream dependencies, consumed by all others.
The conventions source for scaffolding is `se-manifest-schema`.

**Consequences:**

- Repo structure, CI, and tooling conform to `se-manifest-schema` patterns.
- The schema format and validator CLI design are informed by SE precedent.
- Divergences from SE patterns are recorded as subsequent decisions.

---

## D-003. Schema versioning

**Status:** Accepted

**Context:**
MANIFEST.toml files currently declare `schema = "adaptive-interfaces-manifest-1"`.
Several proposed extensions (`[package]`, `[docs]`, `[ci]`, `[release]`, `[agent]`,
`[conventions]`) are in use in `ptat-sim` but not yet formally defined.

**Decision:**
Version 1 of the schema documents the fields currently in use across existing repos.
The proposed extensions from `ptat-sim/DECISIONS.md D-007` are formally defined
as part of version 2 (`adaptive-interfaces-manifest-2`).

**Consequences:**

- `schema_url` in all repos points here after this repo is published.
- `ptat-sim` updates from `manifest-1` to `manifest-2` after this schema ships.
- The NOTE in `ptat-sim/MANIFEST.toml` referencing D-007 is resolved.

---

## D-004. CLI command naming

**Status:** Accepted

**Context:**
The SE equivalent uses `se-constitution validate`.
For this ecosystem the validator is general-purpose, not constitution-specific.

**Decision:**
CLI entry point is `adaptive-manifest validate`.
The package name is `adaptive-manifest-schema`.
The Python module name is `adaptive_manifest_schema`.

**Consequences:**

- `[release].validate_step = "uv run adaptive-manifest validate"` in MANIFEST.toml.
- CI E1 step runs `uv run adaptive-manifest validate`.
- Pre-commit E1 hook runs `uv run adaptive-manifest validate`.

---

## D-005. No upstream adaptive-interfaces dependencies

**Status:** Accepted

**Context:**
This repo defines the schema that other repos reference.
If it depended on any of them, circular dependencies would result.

**Decision:**
`[depends].required = []` and `[depends].optional = []`.
This repo is the foundation; nothing in the ecosystem sits below it.

**Consequences:**

- The validator is self-contained.
- Other repos may depend on this repo safely.
- This repo must never import from other adaptive-interfaces packages at runtime.

---

*This document grows with the project. New decisions are appended. Existing decisions
are not edited. Superseding decisions reference the one they replace.*
