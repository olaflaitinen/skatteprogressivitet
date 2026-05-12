"""Tests for the legislation YAML loader."""

from __future__ import annotations

import pytest

from skatteprogressivitet.legislation.loader import load_year, load_all
from skatteprogressivitet.legislation.schema import Legislation


EXPECTED_YEARS = [1991, 1995, 2000, 2007, 2015, 2020, 2025]


def test_load_all_returns_expected_years() -> None:
    ledger = load_all()
    assert sorted(ledger.keys()) == EXPECTED_YEARS


@pytest.mark.parametrize("year", EXPECTED_YEARS)
def test_load_year_returns_legislation(year: int) -> None:
    leg = load_year(year)
    assert isinstance(leg, Legislation)
    assert leg.year == year


@pytest.mark.parametrize("year", EXPECTED_YEARS)
def test_legislation_prisbasbelopp_positive(year: int) -> None:
    leg = load_year(year)
    assert leg.prisbasbelopp > 0


@pytest.mark.parametrize("year", EXPECTED_YEARS)
def test_legislation_kommunal_rate_in_range(year: int) -> None:
    leg = load_year(year)
    assert 0.0 < leg.kommunal_skatt.rate < 1.0


@pytest.mark.parametrize("year", EXPECTED_YEARS)
def test_statlig_brackets_monotone(year: int) -> None:
    leg = load_year(year)
    lowers = [b.lower for b in leg.statlig_skatt.brackets]
    for i in range(1, len(lowers)):
        assert lowers[i] > lowers[i - 1]


@pytest.mark.parametrize("year", EXPECTED_YEARS)
def test_statlig_rates_non_negative(year: int) -> None:
    leg = load_year(year)
    for bracket in leg.statlig_skatt.brackets:
        assert 0.0 <= bracket.rate <= 1.0


def test_load_year_missing_raises() -> None:
    with pytest.raises(FileNotFoundError):
        load_year(1900)


def test_jobbskatteavdrag_disabled_before_2007() -> None:
    for year in [1991, 1995, 2000]:
        leg = load_year(year)
        assert not leg.jobbskatteavdrag.enabled


def test_jobbskatteavdrag_enabled_from_2007() -> None:
    for year in [2007, 2015, 2020, 2025]:
        leg = load_year(year)
        assert leg.jobbskatteavdrag.enabled


def test_capital_income_rate_30pct_all_years() -> None:
    for year in EXPECTED_YEARS:
        leg = load_year(year)
        assert leg.kapitalinkomstskatt.standard_rate == pytest.approx(0.30, abs=1e-6)
