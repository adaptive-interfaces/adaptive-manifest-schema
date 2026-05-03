"""types/primitives.py - Shared primitive type definitions."""

from typing import Any, TypedDict

# One parsed TOML document is the broad boundary type returned by loaders.
TomlData = dict[str, Any]

# Artifact names are stable string keys used in collections of loaded data.
ArtifactName = str

# A repository-level loaded data set is a mapping of artifact name to TOML document.
ArtifactCollection = dict[ArtifactName, TomlData]


class ArtifactMeta(TypedDict, total=False):
    """Common metadata header present in all schema artifact files."""

    version: str
    status: str
    title: str
