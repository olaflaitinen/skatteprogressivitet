"""Tests for capital income tax computation."""

from __future__ import annotations

import pytest

from skatteprogressivitet.legislation.loader import load_year
from skatteprogressivitet.rules.capital_income_tax import (
    compute_capital_income_tax,
    compute_dividend_tax,
)


@pytest.fixture(scope="module")
def leg2025():
    return load_year(2025)


def test_positive_capital_income_30pct(leg2025) -> None:
    assert compute_capital_income_tax(100_000, leg2025) == pytest.approx(30_000.0)


def test_zero_capital_income(leg2025) -> None:
    assert compute_capital_income_tax(0, leg2025) == pytest.approx(0.0)


def test_small_loss_credit(leg2025) -> None:
    credit = compute_capital_income_tax(-50_000, leg2025)
    assert credit == pytest.approx(-15_000.0)


def test_large_loss_reduced_rate_above_100k(leg2025) -> None:
    credit = compute_capital_income_tax(-150_000, leg2025)
    expected = -(100_000 * 0.30 + 50_000 * 0.21)
    assert credit == pytest.approx(expected, rel=1e-6)


def test_dividend_tax_30pct(leg2025) -> None:
    assert compute_dividend_tax(50_000, leg2025) == pytest.approx(15_000.0)


def test_negative_dividend_zero_tax(leg2025) -> None:
    assert compute_dividend_tax(-1000, leg2025) == pytest.approx(0.0)
