"""Tests for scenario loading and running."""

from __future__ import annotations

import pytest

from skatteprogressivitet.scenarios.loader import load_all_scenarios
from skatteprogressivitet.scenarios.runner import run_scenario

EXPECTED_SCENARIOS = [
    "broaden-capital-base",
    "comprehensive-income",
    "raise-brytpunkt",
    "recalibrate-jobbskatteavdrag",
]


def test_load_all_scenarios() -> None:
    scenarios = load_all_scenarios()
    for sid in EXPECTED_SCENARIOS:
        assert sid in scenarios


@pytest.mark.parametrize("sid", EXPECTED_SCENARIOS)
def test_scenario_has_required_fields(sid: str) -> None:
    scenarios = load_all_scenarios()
    scen = scenarios[sid]
    assert scen.scenario_id == sid
    assert scen.baseline_year >= 1991
    assert len(scen.overrides) >= 0


def test_run_scenario_with_empty_population() -> None:
    scenarios = load_all_scenarios()
    scen = scenarios["raise-brytpunkt"]
    result = run_scenario(scen, [])
    assert result.revenue_change_static == pytest.approx(0.0)


def test_run_scenario_with_taxpayers() -> None:
    scenarios = load_all_scenarios()
    scen = scenarios["raise-brytpunkt"]
    tps = [
        {"labour_income": 700_000, "capital_income": 0, "age": 45, "self_employed": False},
        {"labour_income": 300_000, "capital_income": 0, "age": 35, "self_employed": False},
    ]
    result = run_scenario(scen, tps)
    assert result.baseline.n_taxpayers == 2
    assert result.counterfactual.n_taxpayers == 2
