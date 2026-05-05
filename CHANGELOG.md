# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

---

## [0.2.0] - 2026-05-04

### Added

- `AGENT_CONDUCT.md` - org-wide behavioral constraints for AI collaborators
- `SKILL.md` - agent operating guide derived from actual source code
- docs/index.md

### Changed

- `CLAUDE.md` - refactored to thin pointer; reading order only; behavioral content moved to `AGENT_CONDUCT.md`
- `MANIFEST.toml` - `schema_url` corrected;
  `[agent]` safety fields added explicitly;
  `[provides]` updated to reflect three CLI subcommands

### Design decisions recorded

D-009 in `DECISIONS.md` - schema identifier naming:

- `schema` field in downstream `MANIFEST.toml` files:
  - `"adaptive-interfaces-manifest-schema"` (no numeric suffix)

- `manifest_schema_id` field in `manifest-schema.toml`:
  - `"adaptive-interfaces-manifest-schema-1"`
  - numeric suffix retained for migration support

---

## [0.1.0] - 2026-05-03

### Added

- Initial repository scaffold conforming to `se-manifest-schema` conventions
- `DECISIONS.md` - founding design rationale (first artifact, before code)
- `AGENTS.md` - workflow requirements for human and AI contributors
- `CLAUDE.md` - behavioral constraints for AI collaborators
- `MANIFEST.toml` - repository declaration with `[conventions]` source pointer
- `manifest-schema.toml` - canonical schema definition
- `src/adaptive_manifest_schema/` - Python package implementing the validator
- `src/adaptive_manifest_schema/commands/` - CLI subcommands (validate, validate-schema, sync-version)
- `src/adaptive_manifest_schema/validate_manifest.py` - MANIFEST.toml conformance validator; importable
- `src/adaptive_manifest_schema/validate_schema.py` - manifest-schema.toml internal consistency validator
- `src/adaptive_manifest_schema/validate_contract.py` - CITATION.cff version and git tag alignment
- `src/adaptive_manifest_schema/load.py` - TOML file loading primitives
- `src/adaptive_manifest_schema/sync.py` - CITATION.cff version sync to pyproject.toml
- `src/adaptive_manifest_schema/cli.py` - pure CLI dispatcher; no logic
- `tests/` - 62 tests, 86% coverage
- `docs/en/` - docs site with glossary, API reference, scaffold process, and schema evolution guide
- Agent safety fields in `[agent]` section:
  - `permissions`, `checkpoint`, `scope`, `sensitive_paths`, `stop_on_ambiguity`
- Enum validation for `permissions`, `checkpoint`, and `scope` in validator
- Conservative defaults for all agent safety fields (omission never grants permissions)

### Design decisions recorded

- D-001 through D-008 in `DECISIONS.md`
- Key decisions: no upstream dependencies (D-005); agent safety fields (D-006);
  CLI subcommand separation (D-007); schema file location and URL versioning (D-008)

---

## Notes on versioning and releases

- We use **SemVer**:
  - **MAJOR** - breaking changes to schema field definitions or validator semantics
  - **MINOR** - backward-compatible additions (new fields, new validation rules)
  - **PATCH** - fixes, documentation, tooling
- Versions are driven by git tags. Tag `vX.Y.Z` to release.

---

## Release Procedure (Required)

Follow these steps exactly when creating a new release.

### Task 1. Update release metadata (manual edits)

1.1. `CITATION.cff` - update `version` and `date-released`
1.2. `CHANGELOG.md` - add `## [X.Y.Z] - YYYY-MM-DD`, move entries from `[Unreleased]`, update links

### Task 2. Sync Version and Validate

Sync version reads `CITATION.cff` version and
updates `pyproject.toml` fallback-version.

```shell
uv run adaptive-manifest sync-version
uv run adaptive-manifest validate-schema --strict
uv run adaptive-manifest validate --strict

git add -A
uvx pre-commit run --all-files
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build
```

### Task 3. Commit, tag, push

```shell
git add -A
git commit -m "Prep X.Y.Z"
git push -u origin main
```

Verify actions run on GitHub. After success:

```shell
git tag vX.Y.Z -m "X.Y.Z"
git push origin vX.Y.Z
```

### Task 4. Verify tag consistency

Confirm CITATION.cff version matches the pushed git tag.
Run this after `git push origin vX.Y.Z`; it will fail before that point.

```shell
uv run adaptive-manifest validate --strict --require-tag
```

## Only As Needed (delete a tag)

```shell
git tag -d vX.Z.Y
git push origin :refs/tags/vX.Z.Y
```

## Links

[Unreleased]: https://github.com/adaptive-interfaces/adaptive-manifest-schema/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/adaptive-interfaces/adaptive-manifest-schema/releases/tag/v0.2.0
[0.1.0]: https://github.com/adaptive-interfaces/adaptive-manifest-schema/releases/tag/v0.1.0

<!-- markdownlint-enable MD024 -->
