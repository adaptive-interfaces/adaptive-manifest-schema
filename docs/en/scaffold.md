# Scaffold Process (adaptive-manifest-schema)

<!-- Design for durability; do not introduce drift -->

How this repository was created and how to create a new repo using this schema.

## Reference

[adaptive-playbook: scaffold-new-repo](https://github.com/adaptive-interfaces/adaptive-playbook/blob/main/patterns/scaffold-new-repo.md)

The full process is defined there.
This page records what was done during the creation of this repo.

## How this repo was created

Followed the first four commits from the scaffold process.

### Commit 1. Founding documents

- `.gitignore`
- `DECISIONS.md`
- `LICENSE`
- `MANIFEST.toml`
- `README.md`

Critical information is documented in `DECISIONS.md` and encoded in `MANIFEST.toml`.
See the current repo or the commit log for file contents.

### Commit 2. Agent files

- `AGENTS.md`
- `CLAUDE.md`

### Commit 3. Agent scaffold from manifest

The prompt for Commit 3 was:

```text
Scaffold https://github.com/adaptive-interfaces/adaptive-manifest-schema
following MANIFEST.toml, AGENTS.md, and CLAUDE.md in the repo.
Generate all convention files, pyproject.toml, CI workflows, src stubs,
and any other files derived from the manifest.
Package as a zip using: cd <output-folder> && zip -r ../output.zip .
so it extracts correctly on Windows, Mac, and Linux.
```

The manifest points to the
[SE Manifest Schema repository](https://github.com/structural-explainability/se-manifest-schema)
as the conventions source.

### Commit 4. Project-specific logic

The prompt for Commit 4 was:

```text
Use the SE schema example to build out the project-specific logic
needed for this one.
Include our new fields.
Implement it just like we did the SE manifest schema.
```

Source: `https://github.com/structural-explainability/se-manifest-schema`
