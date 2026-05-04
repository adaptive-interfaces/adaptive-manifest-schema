# DECISIONS.md (adaptive-manifest-schema)

Design history and rationale for the Adaptive Interfaces manifest schema.
Captures decisions made before any code exists.
This document is the source of truth for why the schema is shaped the way it is.
ACS conformance depends on it.

---

## Append-Only

_This document grows with the project.
New decisions are appended.
Existing decisions are not edited.
Superseding decisions reference the one they replace._

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

## D-006. Agent safety fields in the schema

**Status:** Accepted

**Context:**
AI agents working in codebases can cause serious harm when given
permissions beyond what a task requires.
A known failure mode is an agent that understands a constraint
but overrides it under goal pressure.
The constraint must be architectural, not just instructional.

The `[agent]` section in MANIFEST.toml previously held only
`conformance` and `skill`; it had no way to declare what an agent
is authorized to do or what it must never touch.

**Decision:**
Five safety fields are added to `[section.agent]` and `[field.agent]`:

- `permissions` - authorized operation scope; allowed values: `read-only`,
  `read-generate`, `read-write`
- `checkpoint` - required human review gate; allowed values:
  `human-review-required`, `automated`
- `scope` - filesystem boundary; allowed values: `this-repo-only`, `multi-repo`
- `sensitive_paths` - list of paths the agent must not read or reference
- `stop_on_ambiguity` - boolean; agent stops and reports rather than guessing

All fields are optional.
Omitting any field implies the conservative default:
`read-generate`, `human-review-required`, `this-repo-only`, no sensitive paths,
and `stop_on_ambiguity = true`.

**Rationale:**
Conservative defaults mean a repo that declares no agent section is
no less safe than one that declares all fields explicitly.
Explicit declaration is for documentation and validator enforcement,
not for granting permissions that would otherwise be denied.

The read-generate-review cycle is the architectural checkpoint.
Agents produce artifacts; humans apply them.
No agent in this ecosystem has autonomous write access to production systems.
This is enforced by process, not just by declaration.

**Consequences:**

- `validate_manifest.py` enforces allowed values for `permissions`,
  `checkpoint`, and `scope` as enum validation.
- `test_validate_manifest.py` covers invalid enum values for all three fields.
- `docs/en/index.md` and `README.md` include a Safety section explaining
  the read-generate-review cycle and these fields.
- All repos in the ecosystem are encouraged to declare `[agent]` explicitly
  even when using default values, for documentation clarity.

---

## D-007. CLI subcommand separation

**Status:** Accepted

**Context:**
The original `validate` command called `sync_all()` automatically before validating.
This was inherited from the SE pattern where the repo validates itself.
For downstream consumers, this is wrong: a downstream repo running
`adaptive-manifest validate` should never have its version synced
as a side effect.

The original CLI also conflated three concerns in one command:
schema internal consistency, manifest conformance, and version sync.

**Decision:**
The CLI is separated into distinct subcommands:

- `adaptive-manifest validate` - validates `MANIFEST.toml` against the schema;
  safe for all repos; no sync, no schema internal check
- `adaptive-manifest validate-schema` - validates `schema/manifest-1.toml`
  internal consistency; this repo only
- `adaptive-manifest sync-version` - syncs `CITATION.cff` version to
  `pyproject.toml`; this repo only; never called automatically

Both `validate` and `validate-schema` support:

- `--strict` - treats warnings as errors
- `--require-tag` - confirms `CITATION.cff` version matches current git tag

`validate` additionally supports:

- `--path` - validates a specific file rather than `./MANIFEST.toml`

**Structure:**
`cli.py` becomes a pure dispatcher.
Each subcommand lives in its own module under `commands/`:

```text
commands/
  validate.py
  validate_schema.py
  sync_version.py
```

Each command module is independently testable.

**Consequences:**

- Downstream repos calling `adaptive-manifest validate` get no side effects.
- `orchestrate.py` is refactored; `run_validate()` no longer calls `sync_all()`.
- `test_cli.py` and `test_orchestrate.py` updated to match new structure.
- The pre-commit E1 hook remains `uv run adaptive-manifest validate`.
- The release procedure Task 2 calls `sync-version` explicitly before `validate`.

---

## D-008. Schema file location and schema_url versioning

**Status:** Accepted

**Context:**
Two related questions arose together:
where should the schema TOML file live,
and what should `schema_url` point to in downstream MANIFEST.toml files.

A `schema/` subdirectory was considered and rejected.
There is only one schema file; the subdirectory adds no value.

A versioned filename (`manifest-1.toml`, `manifest-2.toml`) was considered
and rejected.
The version is already carried by the `schema` string field and the git tag.
The filename does not need to duplicate it.

`manifest.toml` was considered and rejected.
Every downstream repo has a file named `MANIFEST.toml` at its root.
A schema definition file with the same base name creates confusion.

For `schema_url`: pointing at `/main/` is a moving target.
Pointing at a git tag is stable and follows the PyPI convention
of depending on a version, not a branch.

**Decision:**
The schema file is named `manifest-schema.toml` and lives at the repo root.
This matches the SE pattern (`manifest-schema.toml` in `se-manifest-schema`),
is unambiguous, and has no collision with downstream instance files.
The filename is stable across all versions.
Versions are carried by the `schema` string field and git tags.

Downstream MANIFEST.toml files use `/main/` during development:

```toml
schema_url = "https://github.com/adaptive-interfaces/adaptive-manifest-schema/blob/main/manifest-schema.toml"
```

After first release, downstream repos pin to a tag:

```toml
schema_url = "https://github.com/adaptive-interfaces/adaptive-manifest-schema/blob/v1.0.0/manifest-schema.toml"
```

Breaking changes increment the `schema` string and ship as a new git tag.
Both schema versions remain valid during transition via `schema_allowed`.

**Consequences:**

- `schema/manifest-1.toml` is renamed to `manifest-schema.toml` at repo root.
- `pyproject.toml` `force-include` updated:
  `"manifest-schema.toml" = "adaptive_manifest_schema/manifest-schema.toml"`
- `load_schema()` in `load.py` updated: `Path("manifest-schema.toml")`
- All downstream repos update `schema_url` to pin to a tag after v1.0.0 ships.
- The validator can optionally warn when `schema_url` points at `/main/`
  and `--require-tag` is passed.

---
