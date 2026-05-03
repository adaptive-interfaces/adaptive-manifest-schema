# adaptive-manifest-schema

> Canonical `MANIFEST.toml` schema for the Adaptive Interfaces ecosystem.

Part of the [Adaptive Interfaces](https://github.com/adaptive-interfaces) ecosystem.

## Introduction

Every Adaptive Interfaces repository includes a `MANIFEST.toml` that declares
its identity, scope, dependencies, provided artifacts, and tooling configuration.
This repository defines and validates that schema.

`adaptive-manifest-schema` has no upstream Adaptive Interfaces dependencies.
All other repos in the ecosystem depend on it.
It is the foundation layer.

## Scope: Included

- The canonical `MANIFEST.toml` schema definition
- A CLI tool for validating `MANIFEST.toml` files against the schema
- Field definitions and invariants for all schema sections
- Cross-field validation rules
- A Python library for reading and validating manifests programmatically

## Scope: Excluded

- Repo scaffolding or generation tools
- Convention file management
- CI workflow templates
- Any schema specific to other organizations (SE, civic-interconnect, etc.)

## Quickstart

```shell
uv self update
uv python pin 3.15
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install

uv run adaptive-manifest validate

git add -A
uvx pre-commit run --all-files
# repeat if changes were made
git add -A
uvx pre-commit run --all-files

# do chores
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build

# save progress
git add -A
git commit -m "update"
git push -u origin main
```

## Agent usage

Read [`SKILL.md`](SKILL.md) before generating any artifact that consumes this API.
Read [`DECISIONS.md`](DECISIONS.md) for design rationale.
Read [`AGENTS.md`](AGENTS.md) for workflow requirements.

## Scaffold Process

See SCAFFOLD.md.

Prompt for Commit 4:

```text
Use the SE schema example to build out the project specific logic
needed for this one.
Include our new fields.
Implement it just like we did the SE manifest schema.
```

## License

MIT © 2026 [Adaptive Interfaces](https://github.com/adaptive-interfaces)
