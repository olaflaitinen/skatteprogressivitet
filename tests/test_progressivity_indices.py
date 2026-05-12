"""Tests for progressivity and inequality indices."""

from __future__ import annotations

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from skatteprogressivitet.progressivity.indices import (
    gini, kakwani, suits, residual_progression, theil, atkinson, concentration_index,
)


@pytest.fixture
def uniform_income():
    return np.ones(100)


@pytest.fixture
def progressive_system():
    rng = np.random.default_rng(42)
    y = rng.lognormal(12, 0.7, 500)
    t = np.where(y < 300_000, y * 0.25, y * 0.25 + (y - 300_000) * 0.20)
    return y, t


def test_gini_equal_distribution_is_zero(uniform_income) -> None:
    assert gini(uniform_income) == pytest.approx(0.0, abs=1e-10)


def test_gini_in_range() -> None:
    y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    g = gini(y)
    assert 0.0 <= g <= 1.0


def test_gini_known_value() -> None:
    y = np.array([1.0, 2.0, 3.0, 4.0])
    assert gini(y) == pytest.approx(0.25, abs=1e-6)


def test_kakwani_positive_for_progressive(progressive_system) -> None:
    y, t = progressive_system
    assert kakwani(y, t) > 0


def test_kakwani_zero_proportional() -> None:
    y = np.linspace(10, 100, 100)
    t = y * 0.30
    k = kakwani(y, t)
    assert abs(k) < 0.01


def test_suits_positive_for_progressive(progressive_system) -> None:
    y, t = progressive_system
    assert suits(y, t) > 0


def test_residual_progression_in_range(progressive_system) -> None:
    y, t = progressive_system
    rp = residual_progression(y, y - t)
    assert 0 < rp < 2


def test_theil_positive_unequal() -> None:
    y = np.array([1.0, 10.0, 100.0])
    assert theil(y) > 0


def test_atkinson_in_range() -> None:
    y = np.linspace(1, 100, 50)
    a = atkinson(y, 0.5)
    assert 0 <= a < 1


def test_concentration_index_equals_gini_when_ranked_by_self() -> None:
    y = np.array([10.0, 20.0, 30.0, 40.0])
    g = gini(y)
    c = concentration_index(y, y)
    assert c == pytest.approx(g, abs=1e-8)


@given(st.lists(st.floats(min_value=1, max_value=1e6), min_size=10, max_size=100))
@settings(max_examples=30)
def test_gini_always_in_unit_interval(vals) -> None:
    y = np.array(vals)
    g = gini(y)
    assert -1e-10 <= g <= 1 + 1e-10
