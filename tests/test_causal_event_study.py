"""Tests for event-study designs."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from skatteprogressivitet.causal.event_study import event_study


@pytest.fixture
def event_df():
    rng = np.random.default_rng(42)
    n_units, n_times = 20, 10
    event_times = np.array([5.0] * 10 + [np.nan] * 10)
    return pd.DataFrame(
        {
            "unit": np.repeat(np.arange(n_units), n_times),
            "time": np.tile(np.arange(n_times), n_units),
            "event_time": np.repeat(event_times, n_times),
            "y": rng.normal(0, 1, n_units * n_times),
        }
    )


def test_event_study_returns_dataframe(event_df) -> None:
    result = event_study(event_df, "y", "event_time", "unit", "time")
    assert isinstance(result, pd.DataFrame)


def test_event_study_has_required_columns(event_df) -> None:
    result = event_study(event_df, "y", "event_time", "unit", "time")
    assert "relative_time" in result.columns
    assert "estimate" in result.columns
    assert "se" in result.columns


def test_base_period_estimate_is_zero(event_df) -> None:
    result = event_study(event_df, "y", "event_time", "unit", "time", base_period=-1)
    base_row = result[result["relative_time"] == -1]
    assert len(base_row) == 1
    assert base_row["estimate"].iloc[0] == pytest.approx(0.0)


def test_pre_trends_close_to_zero(event_df) -> None:
    result = event_study(event_df, "y", "event_time", "unit", "time")
    pre = result[result["relative_time"] < -1]
    for _, row in pre.iterrows():
        assert abs(row["estimate"]) < 2.0
