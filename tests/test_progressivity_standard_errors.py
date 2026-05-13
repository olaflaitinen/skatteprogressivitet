"""Tests for progressivity standard error estimators."""

from __future__ import annotations

import numpy as np
import pytest

from skatteprogressivitet.progressivity.standard_errors import (
    bootstrap_se,
    influence_function_se,
    jackknife_se,
)


@pytest.fixture
def sample_system():
    rng = np.random.default_rng(42)
    y = rng.lognormal(12, 0.7, 200)
    t = np.where(y < 300_000, y * 0.25, y * 0.25 + (y - 300_000) * 0.10)
    return y, t


def test_bootstrap_se_returns_tuple(sample_system) -> None:
    y, t = sample_system
    point, se, ci = bootstrap_se(y, t, statistic="kakwani", n_reps=50, seed=7)
    assert isinstance(point, float)
    assert se >= 0
    assert ci >= 0


def test_bootstrap_se_point_matches_direct(sample_system) -> None:
    from skatteprogressivitet.progressivity.indices import kakwani

    y, t = sample_system
    point, _, _ = bootstrap_se(y, t, statistic="kakwani", n_reps=50, seed=7)
    direct = kakwani(y, t)
    assert point == pytest.approx(direct, abs=1e-8)


def test_bootstrap_se_unknown_statistic(sample_system) -> None:
    y, t = sample_system
    with pytest.raises(ValueError):
        bootstrap_se(y, t, statistic="unknown", n_reps=10)


def test_jackknife_se_returns_tuple(sample_system) -> None:
    y, t = sample_system
    point, se = jackknife_se(y[:30], t[:30], statistic="gini")
    assert isinstance(point, float)
    assert se >= 0


def test_influence_function_se_returns_tuple(sample_system) -> None:
    y, t = sample_system
    point, se = influence_function_se(y[:50], t[:50])
    assert isinstance(point, float)
    assert se >= 0


def test_bootstrap_se_suits(sample_system) -> None:
    y, t = sample_system
    point, se, ci = bootstrap_se(y, t, statistic="suits", n_reps=50, seed=7)
    assert se >= 0
