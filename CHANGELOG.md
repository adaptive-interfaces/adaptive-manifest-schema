# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

## [Unreleased]

### Added

- Initial repository scaffold conforming to `se-manifest-schema` conventions
- `DECISIONS.md` - founding design rationale (first artifact, before code)
- `AGENTS.md` - workflow requirements for human and AI contributors
- `CLAUDE.md` - behavioral constraints for AI collaborators
- `MANIFEST.toml` - repository declaration with `[conventions]` source pointer
- `schema/manifest-1.toml` - stub for canonical manifest-1 schema definition

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

1.1. `CHANGELOG.md`

- Add `## [X.Y.Z] - YYYY-MM-DD`
- Move entries from `[Unreleased]`
- Update comparison links at bottom of file

### Task 2. Validate

Read `MANIFEST.toml` `[release].validate_step` for the repo-specific step.

```shell
uvx pre-commit run --all-files
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build
uv run adaptive-manifest validate
```

### Task 3. Commit, tag, push

```shell
git add .
git commit -m "Release X.Y.Z"
git tag vX.Y.Z -m "X.Y.Z"
git push origin main
git push origin vX.Y.Z
```

Sample commands:

```shell
# delete and recreate a tag if needed
git tag -d v0.1.0
git push origin :refs/tags/v0.1.0

# new tag / release
git tag v0.1.0 -m "0.1.0"
git push origin v0.1.0
```

## Links

[Unreleased]: https://github.com/adaptive-interfaces/adaptive-manifest-schema/compare/HEAD
