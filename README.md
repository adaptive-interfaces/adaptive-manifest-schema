# adaptive-manifest-schema

[![Adaptive Interfaces](https://img.shields.io/badge/adaptive--interfaces-compliant-blue?logo=github)](https://github.com/adaptive-interfaces)
[![PyPI](https://img.shields.io/pypi/v/adaptive-manifest-schema?logo=pypi&label=pypi)](https://pypi.org/project/adaptive-manifest-schema/)
[![Docs Site](https://img.shields.io/badge/docs-site-blue?logo=github)](https://adaptive-interfaces.github.io/adaptive-manifest-schema/)
[![Repo](https://img.shields.io/badge/repo-GitHub-black?logo=github)](https://github.com/adaptive-interfaces/adaptive-manifest-schema)
[![Python 3.15+](https://img.shields.io/badge/python-3.15%2B-blue?logo=python)](https://github.com/adaptive-interfaces/adaptive-manifest-schema/blob/main/pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](https://github.com/adaptive-interfaces/adaptive-manifest-schema/blob/main/LICENSE)

[![CI](https://github.com/adaptive-interfaces/adaptive-manifest-schema/actions/workflows/ci-python-zensical.yml/badge.svg?branch=main)](https://github.com/adaptive-interfaces/adaptive-manifest-schema/actions/workflows/ci-python-zensical.yml)
[![Docs](https://github.com/adaptive-interfaces/adaptive-manifest-schema/actions/workflows/deploy-zensical.yml/badge.svg?branch=main)](https://github.com/adaptive-interfaces/adaptive-manifest-schema/actions/workflows/deploy-zensical.yml)
[![Links](https://github.com/adaptive-interfaces/adaptive-manifest-schema/actions/workflows/links.yml/badge.svg?branch=main)](https://github.com/adaptive-interfaces/adaptive-manifest-schema/actions/workflows/links.yml)

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

- The canonical `MANIFEST.toml` schema definition (`schema/manifest-1.toml`)
- A CLI validator (`adaptive-manifest validate`)
- Field definitions, types, and invariants for all schema sections
- Cross-field validation rules including agent safety field enum enforcement
- A Python library for reading and validating manifests programmatically

## Scope: Excluded

- Repo scaffolding or generation tools
- Convention file management
- CI workflow templates
- Schemas specific to other organizations (SE, civic-interconnect, etc.)

## Safety

Agents working in codebases can cause serious harm when given permissions
beyond what a task requires.
A known failure mode is an agent that understands a constraint
but overrides it under goal pressure.
The constraint must be architectural, not just instructional.

This schema encodes a **read-generate-review cycle** as the architectural checkpoint:

- Agents read files and produce artifacts.
- Humans review before anything is applied.
- No agent has autonomous write access to production systems.

The `[agent]` section in every `MANIFEST.toml` declares this posture explicitly:

```toml
[agent]
conformance = "https://github.com/adaptive-interfaces/adaptive-conformance-specification"
skill = "SKILL.md"
permissions = "read-generate"
checkpoint = "human-review-required"
scope = "this-repo-only"
stop_on_ambiguity = true
```

The validator enforces allowed values for `permissions`, `checkpoint`, and `scope`.
Conservative defaults apply when fields are omitted.
Omitting `[agent]` entirely does not grant additional permissions.
See `DECISIONS.md D-006` for full rationale.

## Contents

- [API Reference](api.md) - auto-generated from `src/adaptive_manifest_schema/`

## Command Reference

<details>
<summary>Show command reference</summary>

### In a machine terminal

Open a machine terminal where you want the project:

```shell
git clone https://github.com/structural-explainability/se-manifest-schema

cd se-manifest-schema
code .
```

### In a VS Code terminal

```shell
uv self update
uv python pin 3.15
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install

git add -A
uvx pre-commit run --all-files
# repeat if changes were made
git add -A
uvx pre-commit run --all-files

uv run adaptive-manifest validate-schema --strict
uv run adaptive-manifest validate --strict

# do chores
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build

# save progress
git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Agent Usage

This repository is structured for agent consumption.
Read these files in order before generating any artifact:

1. [`MANIFEST.toml`](./MANIFEST.toml) - repository contract and agent configuration
2. [`SKILL.md`](./SKILL.md) - operating guide and interface contract
3. [`DECISIONS.md`](./DECISIONS.md) - design rationale
4. [`AGENTS.md`](./AGENTS.md) - workflow requirements
5. [`AGENT_CONDUCT.md`](./AGENT_CONDUCT.md) - behavioral constraints

## Working with Agents

Agents may accumulate context drift over long sessions.
Rereading may anchor them back to the repo's constraints.
On long context windows, asking the agent to reread key documents may help.

```text
Please reread MANIFEST.toml, SKILL.md, and AGENTS.md
before continuing.
```

## Documentation

[Documentation Site](https://adaptive-interfaces.github.io/adaptive-manifest-schema/)

## See also

- [CHANGELOG.md](./CHANGELOG.md)
- [CITATION.cff](./CITATION.cff)

## License

MIT © 2026 [Adaptive Interfaces](https://github.com/adaptive-interfaces)
