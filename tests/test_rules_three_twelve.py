"""Tests for the 3:12 rules computation."""

from __future__ import annotations

import pytest

from skatteprogressivitet.legislation.loader import load_year
from skatteprogressivitet.rules.three_twelve import (
    compute_forenklingsregeln_ceiling,
    compute_huvudregeln_ceiling,
    compute_three_twelve_tax,
)


@pytest.fixture(scope="module")
def leg2025():
    return load_year(2025)


def test_forenklingsregeln_ceiling_positive(leg2025) -> None:
    assert compute_forenklingsregeln_ceiling(leg2025) > 0


def test_huvudregeln_ceiling_positive(leg2025) -> None:
    assert compute_huvudregeln_ceiling(1_000_000, leg2025) > 0


def test_dividend_below_ceiling_qualified_only(leg2025) -> None:
    ceiling = compute_forenklingsregeln_ceiling(leg2025)
    qt, et = compute_three_twelve_tax(ceiling * 0.5, 0, True, leg2025)
    assert qt > 0
    assert et == pytest.approx(0.0)


def test_dividend_above_ceiling_generates_excess(leg2025) -> None:
    ceiling = compute_forenklingsregeln_ceiling(leg2025)
    qt, et = compute_three_twelve_tax(ceiling * 2, 0, True, leg2025)
    assert qt > 0
    assert et > 0


def test_qualified_rate_lower_than_excess_rate(leg2025) -> None:
    assert leg2025.three_twelve is not None
    assert leg2025.three_twelve.dividend_rate_qualified < leg2025.three_twelve.dividend_rate_excess


def test_disabled_legislation_returns_zeros() -> None:
    leg = load_year(1991)
    if leg.three_twelve is None or not leg.three_twelve.enabled:
        qt, et = compute_three_twelve_tax(100_000, 500_000, True, leg)
        assert qt == pytest.approx(0.0)
        assert et == pytest.approx(0.0)
