"""load.py - Loading and parsing for adaptive-manifest-schema.

Owns:
  - load_toml()        - read any TOML file
  - load_schema()      - read schema/manifest-1.toml
  - load_manifest()    - read MANIFEST.toml
  - get_git_tag()      - read current exact git tag
"""

from pathlib import Path
import shutil
import subprocess
import tomllib
from typing import Any


def load_toml(path: Path) -> dict[str, Any]:
    """Load and return TOML data from the specified path."""
    return tomllib.loads(path.read_text(encoding="utf-8"))


def load_schema() -> dict[str, Any]:
    """Load schema/manifest-1.toml from repo root."""
    path = Path("schema") / "manifest-1.toml"
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {path}")
    return load_toml(path)


def load_manifest(path: Path | None = None) -> dict[str, Any]:
    """Load MANIFEST.toml from the given path or repo root."""
    target = path if path is not None else Path("MANIFEST.toml")
    if not target.exists():
        raise FileNotFoundError(f"MANIFEST.toml not found: {target}")
    return load_toml(target)


def get_git_tag() -> str:
    """Return the current git tag (exact match required)."""
    git = shutil.which("git")
    if git is None:
        raise RuntimeError("git executable not found on PATH")
    try:
        return (
            subprocess.check_output(  # noqa: S603
                [git, "describe", "--tags", "--exact-match"],
                stderr=subprocess.DEVNULL,
            )
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Repository is not on a tagged commit") from exc
