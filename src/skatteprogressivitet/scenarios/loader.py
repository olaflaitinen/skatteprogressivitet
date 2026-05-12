"""Scenario YAML loader.

Loads counterfactual scenario definitions from ``data/scenarios/`` and
validates them against the scenario schema.
"""

from __future__ import annotations

import pathlib
from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field


class ParameterOverride(BaseModel):
    """A single parameter override within a scenario.

    Attributes:
        path: Dot-separated path into the Legislation model (e.g.
            ``"statlig_skatt.brackets.0.lower"``).
        value: New value to assign at the path.
        notes: Optional annotation.
    """

    path: str
    value: Any
    notes: str = ""

    model_config = {"frozen": True}


class Scenario(BaseModel):
    """A counterfactual scenario definition.

    Attributes:
        scenario_id: Unique identifier for the scenario.
        description: Human-readable description.
        baseline_year: Year from which to start.
        overrides: List of parameter overrides.
        behavioural: Behavioural mode for this scenario run.
        notes: Optional annotation.
    """

    scenario_id: str
    description: str
    baseline_year: int = Field(ge=1991, le=2100)
    overrides: list[ParameterOverride] = Field(default_factory=list)
    behavioural: str = "full"
    notes: str = ""

    model_config = {"frozen": True}


def load_scenario(
    path: pathlib.Path,
) -> Scenario:
    """Load and validate a scenario YAML file.

    Args:
        path: Path to the scenario YAML file.

    Returns:
        Validated :class:`Scenario` instance.

    Raises:
        FileNotFoundError: If the file does not exist.
        pydantic.ValidationError: If the file is invalid.

    Example:
        >>> import pathlib
        >>> from skatteprogressivitet.paths import SCENARIO_ROOT
        >>> p = SCENARIO_ROOT / "raise-brytpunkt.yaml"
        >>> scen = load_scenario(p)
        >>> scen.scenario_id
        'raise-brytpunkt'
    """
    if not path.exists():
        raise FileNotFoundError(f"Scenario file not found: {path}")
    with path.open(encoding="utf-8") as fh:
        data: dict[str, Any] = yaml.safe_load(fh)
    return Scenario.model_validate(data)


def load_all_scenarios(
    root: Optional[pathlib.Path] = None,
) -> dict[str, Scenario]:
    """Load all scenario YAML files from the scenarios directory.

    Args:
        root: Optional override for the scenarios root directory.

    Returns:
        Mapping from ``scenario_id`` to :class:`Scenario`.

    Example:
        >>> scenarios = load_all_scenarios()
        >>> "raise-brytpunkt" in scenarios
        True
    """
    from skatteprogressivitet.paths import SCENARIO_ROOT

    r = root or SCENARIO_ROOT
    result: dict[str, Scenario] = {}
    for p in sorted(r.glob("*.yaml")):
        scen = load_scenario(p)
        result[scen.scenario_id] = scen
    return result
