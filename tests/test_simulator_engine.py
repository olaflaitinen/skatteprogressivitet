"""Tests for the microsimulation engine."""

from __future__ import annotations

import pytest
import polars as pl

from skatteprogressivitet.simulator.engine import Simulator, SimulationResult
from skatteprogressivitet.config import Config


@pytest.fixture(scope="module")
def sim():
    return Simulator()


@pytest.fixture(scope="module")
def small_population():
    return [
        {"labour_income": i * 100_000, "capital_income": 0, "age": 40, "self_employed": False}
        for i in range(1, 6)
    ]


def test_run_returns_simulation_result(sim, small_population) -> None:
    result = sim.run(small_population, year=2025, behavioural="none")
    assert isinstance(result, SimulationResult)


def test_n_taxpayers_matches_input(sim, small_population) -> None:
    result = sim.run(small_population, year=2025, behavioural="none")
    assert result.n_taxpayers == len(small_population)


def test_dataframe_has_expected_columns(sim, small_population) -> None:
    result = sim.run(small_population, year=2025, behavioural="none")
    assert "total_tax" in result.dataframe.columns
    assert "effective_average_rate" in result.dataframe.columns


def test_all_average_rates_in_range(sim, small_population) -> None:
    result = sim.run(small_population, year=2025, behavioural="none")
    avg_rates = result.dataframe["effective_average_rate"].to_numpy()
    assert (avg_rates >= 0).all()
    assert (avg_rates <= 1).all()


def test_run_accepts_polars_dataframe(sim) -> None:
    df = pl.DataFrame(
        {
            "labour_income": [300_000.0, 500_000.0],
            "capital_income": [0.0, 0.0],
            "age": [35, 50],
            "self_employed": [False, False],
        }
    )
    result = sim.run(df, year=2025, behavioural="none")
    assert result.n_taxpayers == 2


def test_behavioural_mode_eti_runs(sim, small_population) -> None:
    result = sim.run(small_population, year=2025, behavioural="eti")
    assert isinstance(result, SimulationResult)


def test_determinism(small_population) -> None:
    sim1 = Simulator()
    sim2 = Simulator()
    r1 = sim1.run(small_population, year=2025, behavioural="none")
    r2 = sim2.run(small_population, year=2025, behavioural="none")
    t1 = r1.dataframe["total_tax"].to_list()
    t2 = r2.dataframe["total_tax"].to_list()
    assert t1 == pytest.approx(t2)
