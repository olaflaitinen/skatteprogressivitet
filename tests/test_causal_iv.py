"""Tests for IV estimators."""

from __future__ import annotations

import numpy as np

from skatteprogressivitet.causal.iv import bunching_iv, tsls


def test_tsls_consistent_estimate() -> None:
    rng = np.random.default_rng(42)
    n = 500
    z = rng.normal(0, 1, n)
    x = 0.8 * z + rng.normal(0, 0.5, n)
    y = 1.5 * x + rng.normal(0, 1, n)
    result = tsls(y, x, z)
    assert abs(result["estimate"] - 1.5) < 0.4


def test_tsls_returns_dict() -> None:
    rng = np.random.default_rng(7)
    n = 200
    z = rng.normal(0, 1, n)
    x = z + rng.normal(0, 0.3, n)
    y = x + rng.normal(0, 1, n)
    result = tsls(y, x, z)
    assert "estimate" in result
    assert "se" in result
    assert "f_first_stage" in result
    assert "n_obs" in result


def test_tsls_f_statistic_strong_instrument() -> None:
    rng = np.random.default_rng(42)
    n = 1000
    z = rng.normal(0, 1, n)
    x = 2.0 * z + rng.normal(0, 0.1, n)
    y = x + rng.normal(0, 1, n)
    result = tsls(y, x, z)
    assert result["f_first_stage"] > 10


def test_bunching_iv_returns_dict() -> None:
    rng = np.random.default_rng(42)
    incomes = rng.normal(500_000, 80_000, 1000)
    outcomes = incomes * 0.9 + rng.normal(0, 5_000, 1000)
    result = bunching_iv(incomes, outcomes, threshold=500_000)
    assert "estimate" in result
    assert "n_obs" in result
