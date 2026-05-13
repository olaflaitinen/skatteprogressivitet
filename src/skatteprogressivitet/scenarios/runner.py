"""Scenario runner.

Applies a :class:`Scenario`'s parameter overrides to a baseline
:class:`Legislation`, runs the simulator, and returns a
:class:`ScenarioResult` with both baseline and counterfactual outcomes.
"""

from __future__ import annotations

import copy
import dataclasses
from typing import TYPE_CHECKING, Any

from skatteprogressivitet.config import Config
from skatteprogressivitet.legislation.ledger import LegislationLedger
from skatteprogressivitet.simulator.engine import SimulationResult, Simulator

if TYPE_CHECKING:
    import polars as pl

    from skatteprogressivitet.scenarios.loader import Scenario


@dataclasses.dataclass
class ScenarioResult:
    """Results of a counterfactual scenario run.

    Attributes:
        scenario: The scenario definition that was run.
        baseline: SimulationResult for the baseline.
        counterfactual: SimulationResult for the counterfactual.
        revenue_change_static: Static revenue change in SEK (counterfactual - baseline).
        revenue_change_behavioural: Behavioural revenue change in SEK.
    """

    scenario: Scenario
    baseline: SimulationResult
    counterfactual: SimulationResult
    revenue_change_static: float
    revenue_change_behavioural: float


def _apply_overrides(
    legislation_dict: dict[str, Any],
    overrides: list[Any],
) -> dict[str, Any]:
    """Apply a list of parameter overrides to a legislation dictionary.

    Uses dot-notation paths to set nested values.

    Args:
        legislation_dict: Mutable copy of the legislation as a plain dict.
        overrides: List of :class:`~skatteprogressivitet.scenarios.loader.ParameterOverride`.

    Returns:
        Modified dictionary.
    """
    result = copy.deepcopy(legislation_dict)
    for override in overrides:
        parts = override.path.split(".")
        node: Any = result
        for part in parts[:-1]:
            if isinstance(node, dict):
                node = node[part]
            elif isinstance(node, list):
                node = node[int(part)]
        last = parts[-1]
        if isinstance(node, dict):
            node[last] = override.value
        elif isinstance(node, list):
            node[int(last)] = override.value
    return result


def run_scenario(
    scenario: Scenario,
    taxpayers: list[dict[str, Any]] | pl.DataFrame,
    config: Config | None = None,
) -> ScenarioResult:
    """Run a counterfactual scenario against the baseline.

    Args:
        scenario: The scenario to run.
        taxpayers: Taxpayer population.
        config: Optional runtime configuration override.

    Returns:
        A :class:`ScenarioResult` with baseline and counterfactual outcomes.

    Example:
        >>> from skatteprogressivitet.scenarios.loader import load_scenario
        >>> from skatteprogressivitet.paths import SCENARIO_ROOT
        >>> scen = load_scenario(SCENARIO_ROOT / "raise-brytpunkt.yaml")
        >>> tps = [{"labour_income": 500000, "capital_income": 0,
        ...          "age": 40, "self_employed": False}]
        >>> result = run_scenario(scen, tps)
        >>> result.baseline.n_taxpayers == 1
        True
    """
    _config = config or Config(baseline_year=scenario.baseline_year)  # type: ignore[call-arg]
    ledger = LegislationLedger()
    sim = Simulator(config=_config)

    baseline = sim.run(taxpayers, year=scenario.baseline_year, behavioural="none")

    leg = ledger.get(scenario.baseline_year)
    leg_dict = leg.model_dump()
    modified_dict = _apply_overrides(leg_dict, scenario.overrides)

    from skatteprogressivitet.legislation.schema import Legislation

    modified_leg = Legislation.model_validate(modified_dict)

    from skatteprogressivitet.legislation.ledger import TaxOutcome
    from skatteprogressivitet.rules.personal_income_tax import compute_personal_income_tax

    records = taxpayers if isinstance(taxpayers, list) else taxpayers.to_dicts()
    cf_outcomes: list[TaxOutcome] = [
        compute_personal_income_tax(tp, modified_leg) for tp in records
    ]
    cf_df = sim._to_dataframe(cf_outcomes)

    counterfactual = SimulationResult(
        year=scenario.baseline_year,
        n_taxpayers=len(records),
        outcomes=cf_outcomes,
        dataframe=cf_df,
    )

    base_revenue = float(sum(o.total_tax for o in baseline.outcomes))
    cf_revenue_static = float(sum(o.total_tax for o in cf_outcomes))
    revenue_change_static = cf_revenue_static - base_revenue

    if scenario.behavioural in ("eti", "full"):
        cf_behavioural = sim.run(
            taxpayers, year=scenario.baseline_year, behavioural=scenario.behavioural
        )
        cf_rev_beh = float(sum(o.total_tax for o in cf_behavioural.outcomes))
        revenue_change_behavioural = cf_rev_beh - base_revenue
    else:
        revenue_change_behavioural = revenue_change_static

    return ScenarioResult(
        scenario=scenario,
        baseline=baseline,
        counterfactual=counterfactual,
        revenue_change_static=revenue_change_static,
        revenue_change_behavioural=revenue_change_behavioural,
    )
