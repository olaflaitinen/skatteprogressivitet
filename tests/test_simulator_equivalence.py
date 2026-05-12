"""Tests for equivalence scale utilities."""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from skatteprogressivitet.simulator.equivalence import (
    oecd_modified_scale,
    square_root_scale,
    equivalise,
)


def test_single_adult_no_children_oecd() -> None:
    assert oecd_modified_scale(1, 0) == pytest.approx(1.0)


def test_two_adults_two_children_oecd() -> None:
    assert oecd_modified_scale(2, 2) == pytest.approx(2.1)


def test_single_household_sqrt() -> None:
    assert square_root_scale(1) == pytest.approx(1.0)


def test_four_member_sqrt() -> None:
    assert square_root_scale(4) == pytest.approx(2.0, abs=1e-10)


def test_equivalise_reduces_income() -> None:
    equiv = equivalise(200_000, 2, 1, "oecd_modified")
    assert equiv < 200_000


def test_equivalise_single_unchanged() -> None:
    equiv = equivalise(200_000, 1, 0, "oecd_modified")
    assert equiv == pytest.approx(200_000)


def test_equivalise_unknown_method_raises() -> None:
    with pytest.raises(ValueError):
        equivalise(100_000, 2, 0, "unknown")


def test_oecd_scale_invalid_adults_raises() -> None:
    with pytest.raises(ValueError):
        oecd_modified_scale(0, 0)


@given(
    n_adults=st.integers(min_value=1, max_value=10),
    n_children=st.integers(min_value=0, max_value=10),
)
@settings(max_examples=50)
def test_oecd_scale_monotone_in_size(n_adults: int, n_children: int) -> None:
    s1 = oecd_modified_scale(n_adults, n_children)
    s2 = oecd_modified_scale(n_adults + 1, n_children)
    assert s2 > s1
