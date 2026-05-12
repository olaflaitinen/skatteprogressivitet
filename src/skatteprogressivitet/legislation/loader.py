"""Legislation loader for the per-year YAML parameter files.

Loads YAML files from ``data/legislation/`` and validates them against both the
JSON schema (``data/legislation/schema.json``) and the pydantic :class:`Legislation`
model.
"""

from __future__ import annotations

import json
import pathlib

import yaml

from skatteprogressivitet.legislation.schema import Legislation
from skatteprogressivitet.paths import LEGISLATION_ROOT


def _load_raw(path: pathlib.Path) -> dict:  # type: ignore[type-arg]
    """Read and parse a single YAML file.

    Args:
        path: Absolute path to the YAML file.

    Returns:
        Parsed dictionary.
    """
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)  # type: ignore[no-any-return]


def _validate_json_schema(data: dict, schema: dict) -> None:  # type: ignore[type-arg]
    """Validate data against the JSON schema.

    Args:
        data: Parsed YAML data.
        schema: Parsed JSON schema dict.

    Raises:
        jsonschema.ValidationError: If the data does not conform to the schema.
    """
    import jsonschema

    jsonschema.validate(data, schema)


def load_year(year: int, root: pathlib.Path | None = None) -> Legislation:
    """Load and validate the legislation for a single year.

    Args:
        year: Reform year to load.
        root: Optional override for the legislation root directory.

    Returns:
        A validated :class:`Legislation` instance.

    Raises:
        FileNotFoundError: If no YAML file exists for the given year.
        jsonschema.ValidationError: If the file fails JSON-schema validation.
        pydantic.ValidationError: If the file fails pydantic model validation.

    Example:
        >>> leg = load_year(2025)
        >>> leg.year
        2025
        >>> leg.statlig_skatt.brackets[0].rate
        0.0
    """
    r = root or LEGISLATION_ROOT
    path = r / f"{year}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"No legislation file for year {year}: {path}")

    schema_path = r / "schema.json"
    with schema_path.open(encoding="utf-8") as fh:
        schema = json.load(fh)

    data = _load_raw(path)
    _validate_json_schema(data, schema)
    return Legislation.model_validate(data)


def load_all(root: pathlib.Path | None = None) -> dict[int, Legislation]:
    """Load and validate all legislation YAML files in the given directory.

    Args:
        root: Optional override for the legislation root directory.

    Returns:
        Mapping from year integer to validated :class:`Legislation` instance.

    Example:
        >>> ledger = load_all()
        >>> sorted(ledger.keys())
        [1991, 1995, 2000, 2007, 2015, 2020, 2025]
    """
    r = root or LEGISLATION_ROOT
    result: dict[int, Legislation] = {}
    for yaml_path in sorted(r.glob("*.yaml")):
        try:
            year = int(yaml_path.stem)
        except ValueError:
            continue
        result[year] = load_year(year, root=r)
    return result
