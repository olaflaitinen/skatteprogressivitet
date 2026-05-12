"""Tests for DiD estimators."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from skatteprogressivitet.causal.did import twfe_did, callaway_santanna_att


@pytest.fixture
def panel_df():
    rng = np.random.default_rng(42)
    n_units, n_times = 40, 8
    units = np.repeat(np.arange(n_units), n_times)
    times = np.tile(np.arange(n_times), n_units)
    treat_units = np.arange(20)
    treat_indicator = (
        (np.isin(units, treat_units)) & (times >= 4)
    ).astype(float)
    y = rng.normal(0, 1, n_units * n_times) + treat_indicator * 2.0
    return pd.DataFrame({"unit": units, "time": times, "treat": treat_indicator, "y": y})


def test_twfe_returns_dict(panel_df) -> None:
    result = twfe_did(panel_df, "y", "treat", "unit", "time")
    assert isinstance(result, dict)
    assert "estimate" in result


def test_twfe_estimate_close_to_truth(panel_df) -> None:
    result = twfe_did(panel_df, "y", "treat", "unit", "time")
    assert abs(result["estimate"] - 2.0) < 0.5


def test_callaway_santanna_returns_dataframe() -> None:
    rng = np.random.default_rng(7)
    df = pd.DataFrame(
        {
            "unit": np.repeat(np.arange(30), 5),
            "time": np.tile(np.arange(5), 30),
            "cohort": np.repeat(np.array([2] * 10 + [3] * 10 + [np.nan] * 10), 5),
            "y": rng.normal(0, 1, 150),
        }
    )
    result = callaway_santanna_att(df, "y", "cohort", "time", "unit")
    assert isinstance(result, pd.DataFrame)
    assert "att" in result.columns
