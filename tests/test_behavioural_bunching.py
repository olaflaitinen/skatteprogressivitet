"""Tests for the bunching estimator."""

from __future__ import annotations

import numpy as np
import pytest

from skatteprogressivitet.behavioural.bunching import (
    count_bin_mass,
    estimate_bunching_eti,
    estimate_counterfactual_density,
)


def test_count_bin_mass_simple() -> None:
    arr = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    assert count_bin_mass(arr, 2.0, 4.0) == 2


def test_count_bin_mass_empty() -> None:
    arr = np.array([1.0, 2.0])
    assert count_bin_mass(arr, 10.0, 20.0) == 0


def test_counterfactual_density_returns_array() -> None:
    rng = np.random.default_rng(42)
    incomes = rng.normal(500_000, 100_000, 2000)
    cf = estimate_counterfactual_density(incomes, 500_000, 50_000, 50_000)
    assert len(cf) > 0
    assert (cf >= 0).all()


def test_bunching_eti_non_negative() -> None:
    rng = np.random.default_rng(7)
    incomes = rng.normal(500_000, 80_000, 3000)
    eti = estimate_bunching_eti(incomes, 500_000, 50_000, 50_000, 0.05)
    assert eti >= 0


def test_bunching_eti_zero_ntr_returns_zero() -> None:
    rng = np.random.default_rng(7)
    incomes = rng.normal(500_000, 80_000, 1000)
    eti = estimate_bunching_eti(incomes, 500_000, 50_000, 50_000, 0.0)
    assert eti == pytest.approx(0.0)
