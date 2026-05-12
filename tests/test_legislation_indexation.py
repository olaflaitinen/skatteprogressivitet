"""Tests for the legislation indexation module."""

from __future__ import annotations

import pytest

from skatteprogressivitet.legislation.indexation import (
    get_basbelopp,
    get_prisbasbelopp,
    get_inkomstbasbelopp,
    index_threshold,
    BASBELOPP_SERIES,
    PRISBASBELOPP_SERIES,
    INKOMSTBASBELOPP_SERIES,
)


def test_get_basbelopp_known_years() -> None:
    assert get_basbelopp(2025) == pytest.approx(52500.0)
    assert get_basbelopp(1991) == pytest.approx(32200.0)


def test_get_prisbasbelopp_known_years() -> None:
    assert get_prisbasbelopp(2020) == pytest.approx(47300.0)


def test_get_inkomstbasbelopp_known_years() -> None:
    assert get_inkomstbasbelopp(2025) == pytest.approx(74300.0)
    assert get_inkomstbasbelopp(2007) == pytest.approx(46200.0)


def test_interpolation_between_years() -> None:
    v_2007 = get_prisbasbelopp(2007)
    v_2015 = get_prisbasbelopp(2015)
    v_mid = get_prisbasbelopp(2011)
    assert v_2007 <= v_mid <= v_2015


def test_extrapolation_below_series_start() -> None:
    v = get_basbelopp(1980)
    assert v == pytest.approx(BASBELOPP_SERIES[1991])


def test_extrapolation_above_series_end() -> None:
    v = get_basbelopp(2099)
    assert v == pytest.approx(BASBELOPP_SERIES[2025])


def test_index_threshold_increases_over_time() -> None:
    t_indexed = index_threshold(170_000, 1991, 2025)
    assert t_indexed > 170_000


def test_index_threshold_same_year_unchanged() -> None:
    t = index_threshold(500_000, 2025, 2025)
    assert t == pytest.approx(500_000)


def test_all_series_values_positive() -> None:
    for val in BASBELOPP_SERIES.values():
        assert val > 0
    for val in PRISBASBELOPP_SERIES.values():
        assert val > 0
    for val in INKOMSTBASBELOPP_SERIES.values():
        assert val > 0
