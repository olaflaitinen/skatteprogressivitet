"""Tests for housing allowance computation."""

from __future__ import annotations

import pytest

from skatteprogressivitet.legislation.loader import load_year
from skatteprogressivitet.rules.housing_allowance import (
    compute_bostadsbidrag,
    compute_bostadstillagg,
)


@pytest.fixture(scope="module")
def leg2025():
    return load_year(2025)


def test_bostadsbidrag_low_income(leg2025) -> None:
    assert compute_bostadsbidrag(0, 60_000, leg2025) > 0


def test_bostadsbidrag_non_negative(leg2025) -> None:
    for income in [0, 50_000, 200_000, 1_000_000]:
        assert compute_bostadsbidrag(income, 60_000, leg2025) >= 0


def test_bostadsbidrag_tapers_with_income(leg2025) -> None:
    low = compute_bostadsbidrag(50_000, 60_000, leg2025)
    high = compute_bostadsbidrag(200_000, 60_000, leg2025)
    assert low >= high


def test_bostadstillagg_non_negative(leg2025) -> None:
    for income in [0, 100_000, 300_000]:
        assert compute_bostadstillagg(income, 48_000, leg2025) >= 0
