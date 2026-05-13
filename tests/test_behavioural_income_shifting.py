"""Tests for the income-shifting module."""

from __future__ import annotations

import pytest

from skatteprogressivitet.behavioural.income_shifting import (
    compute_shifted_income,
    shifting_elasticity,
)
from skatteprogressivitet.legislation.loader import load_year


def test_shifting_elasticity_positive_when_differential_positive() -> None:
    e = shifting_elasticity(0.57, 0.20)
    assert e > 0


def test_shifting_elasticity_zero_when_no_differential() -> None:
    e = shifting_elasticity(0.20, 0.20)
    assert e == pytest.approx(0.0)


def test_shifted_income_non_negative() -> None:
    leg = load_year(2025)
    adj_l, cap = compute_shifted_income(800_000, 200_000, 0.57, leg)
    assert adj_l >= 0
    assert cap >= 0


def test_shifted_income_conserved() -> None:
    leg = load_year(2025)
    labour = 800_000.0
    ceiling = 200_000.0
    adj_l, cap = compute_shifted_income(labour, ceiling, 0.57, leg)
    assert adj_l + cap == pytest.approx(labour, rel=1e-6)


def test_no_shifting_when_three_twelve_disabled() -> None:
    leg = load_year(1991)
    if leg.three_twelve is None or not leg.three_twelve.enabled:
        adj_l, cap = compute_shifted_income(500_000, 200_000, 0.50, leg)
        assert cap == pytest.approx(0.0)
