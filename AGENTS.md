# AGENTS.md (adaptive-manifest-schema)

## Scope

This repository provides the canonical `MANIFEST.toml` schema definition
and validator CLI for the Adaptive Interfaces ecosystem.
Changes must preserve:

- schema stability (field names and semantics are depended on by all other repos)
- validator correctness (false positives and false negatives both break downstream trust)
- zero upstream adaptive-interfaces dependencies (this repo is the foundation layer)

Do not add or remove schema fields without a corresponding DECISIONS.md entry.
Do not change validator behavior without updating tests and SKILL.md.

## WHY

This repo uses a uniform, reproducible workflow based on `uv` and `pyproject.toml`.
These instructions exist to prevent tool drift and OS mismatch.

## Requirements

Use `uv` for all environment, dependency, and run commands in this repo.
Do not recommend or use `pip install` as the primary workflow.
The canonical Python version is defined in `.python-version`.
Commands and guidance must work on Windows, macOS, and Linux.
If shell-specific commands are unavoidable, provide both:

- PowerShell (Windows)
- bash/zsh (macOS/Linux)

## Quickstart

```shell
uv self update
uv python pin 3.15
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install
```

## Common Tasks

Lint and format:

```shell
uv run python -m ruff format .
uv run python -m ruff check . --fix
```

Run tests:

```shell
uv run pytest
```

Validate:

```shell
uv run adaptive-manifest validate
```

## Formatting Conventions

Document titles use the filename and repo name in parentheses:
`# DECISIONS.md (adaptive-manifest-schema)`

Numbered decision sections use periods:
`## D-001. Purpose of this repository`

Avoid emdashes.
Avoid endashes.
Prefer semicolons, commas, or starting a new sentence.
Start each sentence on a new line to assist diffs.
Keep line length to 100 characters wherever possible.

## Agent Task Assignment

Before generating any schema definition, validator logic, or consuming code:

1. Read `SKILL.md`; it is the operating guide, not optional documentation.
2. Read `DECISIONS.md`; it explains why the schema is shaped the way it is.
3. Confirm understanding of the schema versioning policy (see D-003).
4. Confirm that no upstream adaptive-interfaces imports are introduced (see D-005).

## pre-commit

```shell
uvx pre-commit run --all-files
```
