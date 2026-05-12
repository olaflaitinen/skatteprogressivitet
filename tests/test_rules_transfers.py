"""Tests for social transfer computations."""

from __future__ import annotations

import pytest

from skatteprogressivitet.legislation.loader import load_year
from skatteprogressivitet.rules.transfers import (
    compute_sjukpenning,
    compute_foraldrapenning,
    compute_a_kassa,
)


@pytest.fixture(scope="module")
def leg2025():
    return load_year(2025)


def test_sjukpenning_positive(leg2025) -> None:
    assert compute_sjukpenning(400_000, 30, leg2025) > 0


def test_sjukpenning_zero_days(leg2025) -> None:
    assert compute_sjukpenning(400_000, 0, leg2025) == pytest.approx(0.0)


def test_foraldrapenning_positive(leg2025) -> None:
    assert compute_foraldrapenning(350_000, 90, leg2025) > 0


def test_a_kassa_positive(leg2025) -> None:
    assert compute_a_kassa(350_000, 60, leg2025) > 0


def test_higher_income_higher_benefit(leg2025) -> None:
    low = compute_sjukpenning(200_000, 30, leg2025)
    high = compute_sjukpenning(400_000, 30, leg2025)
    assert high >= low


def test_benefit_capped(leg2025) -> None:
    low_income = compute_a_kassa(200_000, 30, leg2025)
    very_high_income = compute_a_kassa(10_000_000, 30, leg2025)
    assert very_high_income < 10 * low_income
