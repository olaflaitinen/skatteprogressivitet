"""Tests for the legislation pydantic schema."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from skatteprogressivitet.legislation.schema import (
    Bracket,
    KommunalSkatt,
    Legislation,
    StatligSkatt,
)


def _minimal_legislation_dict() -> dict:
    return {
        "year": 2025,
        "kommunal_skatt": {"rate": 0.32},
        "statlig_skatt": {
            "brackets": [
                {"lower": 0, "upper": 598500, "rate": 0.0},
                {"lower": 598500, "upper": None, "rate": 0.20},
            ]
        },
        "kapitalinkomstskatt": {"standard_rate": 0.30},
        "arbetsgivaravgift": {"rate": 0.3142},
        "egenavgift": {"rate": 0.2871},
        "jobbskatteavdrag": {"enabled": True},
        "basbelopp": 52500,
        "prisbasbelopp": 52500,
        "inkomstbasbelopp": 74300,
    }


def test_legislation_valid() -> None:
    data = _minimal_legislation_dict()
    leg = Legislation.model_validate(data)
    assert leg.year == 2025


def test_bracket_rate_out_of_range() -> None:
    with pytest.raises(ValidationError):
        Bracket(lower=0, upper=100, rate=1.5)


def test_statlig_non_monotone_brackets_raises() -> None:
    with pytest.raises(ValidationError):
        StatligSkatt(
            brackets=[
                Bracket(lower=100, upper=200, rate=0.0),
                Bracket(lower=50, upper=300, rate=0.20),
            ]
        )


def test_kommunal_rate_out_of_range() -> None:
    with pytest.raises(ValidationError):
        KommunalSkatt(rate=1.5)


def test_legislation_year_below_minimum() -> None:
    data = _minimal_legislation_dict()
    data["year"] = 1800
    with pytest.raises(ValidationError):
        Legislation.model_validate(data)


def test_legislation_immutable() -> None:
    data = _minimal_legislation_dict()
    leg = Legislation.model_validate(data)
    with pytest.raises(Exception):
        leg.year = 2000  # type: ignore[misc]
