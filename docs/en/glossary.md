# Glossary (adaptive-manifest-schema)

Key terms for understanding `MANIFEST.toml` structure, schema validation,
and agent safety constraints.

---

## MANIFEST.toml

The repository declaration file present in every Adaptive Interfaces repo.
Declares identity, scope, dependencies, provided artifacts, and tooling configuration.
Machine-readable, human-legible, and reviewable.
Validated by `adaptive-manifest validate`.

## schema

The top-level string field in `MANIFEST.toml` that declares which schema version
the file conforms to.
Current value: `"adaptive-interfaces-manifest-1"`.
The validator checks this against `schema_allowed` in `schema/manifest-1.toml`.

## schema_url

The top-level string field pointing to the schema definition document.
Required alongside `schema`.
Allows tooling and humans to locate the canonical field definitions.

## Section

A TOML table within `MANIFEST.toml`, declared as `[section_name]`.
Sections are either required or optional depending on the repo class.
The schema defines which sections are allowed and what fields each may contain.

## Required section

A section that must be present for a given repo class.
The validator reports an error if it is absent.
Core required sections for all classes: `meta`, `repo`, `layer`, `depends`,
`provides`, `scope`, `citation`.

## Optional section

A section that may be present but is not required.
Proposed sections (`package`, `docs`, `ci`, `release`, `agent`, `conventions`)
are all optional.

## Forbidden section

A section that must not be present for a given repo class.
The validator reports an error if it is found.
Currently no sections are forbidden for any defined class.

## Field

A key-value pair within a section.
Each field has a declared type (`string`, `boolean`, `list[string]`, `integer`)
and a required status.
The validator checks unknown fields and missing required fields.

## Repo class

The declared category of a repository, set in `[repo].class`.
Drives which sections are required, optional, or forbidden.
Defined classes: `library`, `simulation`, `schema`, `guide`, `example`, `skill`, `lab`.

## Layer

The declared position of a repository in the ecosystem layer model.
Set in `[layer].space` and `[layer].role`.
Describes where the repo sits conceptually, not technically.

## Conservative default

The behavior applied when an agent safety field is omitted from `[agent]`.
Omitting a field never grants additional permissions.
Defaults: `permissions = read-generate`, `checkpoint = human-review-required`,
`scope = this-repo-only`, `stop_on_ambiguity = true`.

## Read-generate-review cycle

The architectural checkpoint for all agent operations in this ecosystem.
Agents read files and produce artifacts.
Humans review before anything is applied.
No agent has autonomous write access to production systems.
Declared in `[agent]` and enforced as a process constraint, not only a schema field.

## permissions

An `[agent]` field declaring the authorized operation scope for agents in a repo.
Allowed values:

| Value | Meaning |
| ----- | ------- |
| `read-only` | inspect and analyze; no artifact generation |
| `read-generate` | read files and produce new artifacts; no direct writes (default) |
| `read-write` | modify existing files; requires a DECISIONS.md entry |

## checkpoint

An `[agent]` field declaring the required human review gate before agent output is applied.
Allowed values:

| Value | Meaning |
| ----- | ------- |
| `human-review-required` | all output reviewed before applying (default) |
| `automated` | CI-gated; no human review required |

## scope

An `[agent]` field declaring the filesystem boundary for agent operations.
Allowed values:

| Value | Meaning |
| ----- | ------- |
| `this-repo-only` | agent operates only within this repository (default) |
| `multi-repo` | cross-repo operations permitted; target repos must be named in the task |

## sensitive_paths

An `[agent]` field listing paths the agent must not read, reproduce, or reference.
The agent must stop and request human guidance if a task requires access to these paths.
Example: `["data/", ".env", "secrets/"]`.

## stop_on_ambiguity

An `[agent]` boolean field.
When `true`, the agent must stop and report rather than guess
when task scope is unclear or evidence is insufficient.
Default: `true`.

## conformance

An `[agent]` field pointing to the behavioral protocol the agent must apply
before generating any artifact.
Typically points to the Adaptive Conformance Specification (ACS).

## skill

An `[agent]` field pointing to the domain operating guide (`SKILL.md`).
The agent reads this after ACS conformance is complete.

## conventions.source

The `[conventions]` field declaring the conformance source for repo scaffolding.
An agent clones this repo, observes its convention files, and conforms to them
when generating a scaffold for the current repo.

## validate_manifest

The public Python function importable by downstream consumers to validate
their own `MANIFEST.toml` against the schema.
Returns a list of error strings; empty list means valid.

```python
from adaptive_manifest_schema.validate_manifest import validate_manifest
```

## adaptive-manifest validate

The CLI command that runs the full validation sequence:
sync, schema internal consistency check, and manifest conformance check.

```shell
uv run adaptive-manifest validate
uv run adaptive-manifest validate --strict
uv run adaptive-manifest validate --path path/to/MANIFEST.toml
```
