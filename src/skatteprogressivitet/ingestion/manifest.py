"""Dataset manifest for ingestion pipelines.

Defines the :class:`Manifest` pydantic model describing an input dataset,
and loaders for reading and validating manifests.
"""

from __future__ import annotations

import pathlib
from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field


class DatasetSpec(BaseModel):
    """Specification for a single input dataset.

    Attributes:
        name: Dataset name.
        path: Relative or absolute path to the dataset file.
        format: File format (``"parquet"``, ``"csv"``, ``"arrow"``).
        sha256: Expected SHA-256 checksum of the file (optional).
        n_rows: Expected number of rows (optional; used for quick validation).
        notes: Optional annotation.
    """

    name: str
    path: str
    format: str = "parquet"
    sha256: Optional[str] = None
    n_rows: Optional[int] = Field(default=None, ge=0)
    notes: str = ""

    model_config = {"frozen": True}


class Manifest(BaseModel):
    """Collection of dataset specifications for an ingestion run.

    Attributes:
        version: Manifest schema version.
        datasets: List of dataset specifications.
        notes: Optional annotation.
    """

    version: str = "1.0"
    datasets: list[DatasetSpec] = Field(default_factory=list)
    notes: str = ""

    model_config = {"frozen": True}


def load_manifest(path: pathlib.Path) -> Manifest:
    """Load and validate a dataset manifest YAML file.

    Args:
        path: Path to the manifest YAML file.

    Returns:
        Validated :class:`Manifest` instance.

    Raises:
        FileNotFoundError: If the file does not exist.
        pydantic.ValidationError: If validation fails.

    Example:
        >>> import pathlib, tempfile, yaml
        >>> data = {"version": "1.0", "datasets": [
        ...     {"name": "lisa", "path": "data/synthetic/lisa_like.parquet"}
        ... ]}
        >>> with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w",
        ...                                  delete=False) as f:
        ...     yaml.dump(data, f)
        ...     p = pathlib.Path(f.name)
        >>> m = load_manifest(p)
        >>> m.datasets[0].name
        'lisa'
    """
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")
    with path.open(encoding="utf-8") as fh:
        data: dict[str, Any] = yaml.safe_load(fh)
    return Manifest.model_validate(data)


def validate_against_schema(manifest: Manifest) -> list[str]:
    """Validate that all datasets in a manifest pass basic checks.

    Args:
        manifest: The manifest to validate.

    Returns:
        List of error strings (empty if all pass).

    Example:
        >>> m = Manifest(datasets=[])
        >>> validate_against_schema(m)
        []
    """
    errors: list[str] = []
    for spec in manifest.datasets:
        p = pathlib.Path(spec.path)
        if not p.is_absolute():
            pass  # Relative paths are resolved at read time
        if spec.sha256 and len(spec.sha256) != 64:
            errors.append(f"{spec.name}: sha256 must be 64 hex characters.")
    return errors
