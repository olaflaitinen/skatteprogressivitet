"""Tests for personal income tax computation."""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from skatteprogressivitet.legislation.loader import load_year
from skatteprogressivitet.rules.personal_income_tax import (
    compute_personal_income_tax,
    _compute_statlig,
    _compute_kommunal,
    _compute_marginal_rate,
)


@pytest.fixture(scope="module")
def leg2025():
    return load_year(2025)


def test_zero_income_zero_statlig(leg2025) -> None:
    assert _compute_statlig(0, leg2025) == pytest.approx(0.0)


def test_below_brytpunkt_zero_statlig(leg2025) -> None:
    assert _compute_statlig(500_000, leg2025) == pytest.approx(0.0)


def test_above_brytpunkt_positive_statlig(leg2025) -> None:
    tax = _compute_statlig(700_000, leg2025)
    assert tax > 0


def test_kommunal_proportional(leg2025) -> None:
    t1 = _compute_kommunal(200_000, leg2025)
    t2 = _compute_kommunal(400_000, leg2025)
    assert t2 == pytest.approx(2 * t1, rel=1e-6)


def test_kommunal_rate_range(leg2025) -> None:
    rate = leg2025.kommunal_skatt.rate
    assert 0.25 < rate < 0.45


def test_compute_pit_returns_outcome(leg2025) -> None:
    tp = {"labour_income": 400_000, "capital_income": 0, "age": 40, "self_employed": False}
    outcome = compute_personal_income_tax(tp, leg2025)
    assert outcome.total_tax > 0
    assert 0 < outcome.effective_average_rate < 1


def test_higher_income_higher_average_rate(leg2025) -> None:
    tp_low = {"labour_income": 200_000, "capital_income": 0, "age": 40, "self_employed": False}
    tp_high = {"labour_income": 800_000, "capital_income": 0, "age": 40, "self_employed": False}
    r_low = compute_personal_income_tax(tp_low, leg2025)
    r_high = compute_personal_income_tax(tp_high, leg2025)
    assert r_high.effective_average_rate > r_low.effective_average_rate


def test_jsa_reduces_tax_vs_1991(leg2025) -> None:
    leg1991 = load_year(1991)
    tp = {"labour_income": 300_000, "capital_income": 0, "age": 40, "self_employed": False}
    outcome_2025 = compute_personal_income_tax(tp, leg2025)
    outcome_1991 = compute_personal_income_tax(tp, leg1991)
    assert outcome_2025.jobbskatteavdrag > outcome_1991.jobbskatteavdrag


def test_capital_income_taxed_at_30pct(leg2025) -> None:
    tp = {"labour_income": 0, "capital_income": 100_000, "age": 40, "self_employed": False}
    outcome = compute_personal_income_tax(tp, leg2025)
    assert outcome.kapitalinkomstskatt == pytest.approx(30_000, rel=1e-3)


@given(
    labour=st.floats(min_value=0, max_value=2_000_000, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=50)
def test_tax_monotone_in_income(labour: float) -> None:
    leg = load_year(2025)
    tp1 = {"labour_income": labour, "capital_income": 0, "age": 40, "self_employed": False}
    tp2 = {
        "labour_income": labour + 1000,
        "capital_income": 0,
        "age": 40,
        "self_employed": False,
    }
    o1 = compute_personal_income_tax(tp1, leg)
    o2 = compute_personal_income_tax(tp2, leg)
    assert o2.total_tax >= o1.total_tax - 1e-6


@given(
    labour=st.floats(min_value=1000, max_value=2_000_000, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=50)
def test_marginal_rate_bounded(labour: float) -> None:
    leg = load_year(2025)
    rate = _compute_marginal_rate(labour, leg)
    assert 0.0 <= rate <= 1.0
