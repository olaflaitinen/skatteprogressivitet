"""Tests for the jobbskatteavdrag (EITC) computation."""

from __future__ import annotations

import pytest

from skatteprogressivitet.legislation.loader import load_year
from skatteprogressivitet.rules.jobbskatteavdrag import compute_jobbskatteavdrag


def test_disabled_before_2007() -> None:
    for year in [1991, 1995, 2000]:
        leg = load_year(year)
        credit = compute_jobbskatteavdrag(400_000, 40, leg)
        assert credit == pytest.approx(0.0)


def test_enabled_from_2007() -> None:
    for year in [2007, 2015, 2020, 2025]:
        leg = load_year(year)
        credit = compute_jobbskatteavdrag(300_000, 40, leg)
        assert credit > 0


def test_zero_income_zero_credit() -> None:
    leg = load_year(2025)
    assert compute_jobbskatteavdrag(0, 40, leg) == pytest.approx(0.0)


def test_over_65_enhanced_credit() -> None:
    leg = load_year(2025)
    young = compute_jobbskatteavdrag(300_000, 40, leg)
    senior = compute_jobbskatteavdrag(300_000, 67, leg)
    if leg.jobbskatteavdrag.age_65_plus_enhanced:
        assert senior > young


def test_credit_non_negative() -> None:
    leg = load_year(2025)
    for income in [0, 10_000, 100_000, 500_000, 2_000_000]:
        assert compute_jobbskatteavdrag(income, 40, leg) >= 0
