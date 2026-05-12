"""Shared pytest fixtures for the Skatteprogressivitet test suite."""

from __future__ import annotations

import numpy as np
import pytest

from skatteprogressivitet.legislation.loader import load_year
from skatteprogressivitet.legislation.schema import Legislation


@pytest.fixture(scope="session")
def leg_1991() -> Legislation:
    """Load the 1991 legislation."""
    return load_year(1991)


@pytest.fixture(scope="session")
def leg_2007() -> Legislation:
    """Load the 2007 legislation."""
    return load_year(2007)


@pytest.fixture(scope="session")
def leg_2025() -> Legislation:
    """Load the 2025 legislation."""
    return load_year(2025)


@pytest.fixture(scope="session")
def sample_taxpayers() -> list[dict]:
    """Return a small fixed set of taxpayer archetypes."""
    return [
        {"labour_income": 100_000, "capital_income": 0, "age": 25, "self_employed": False},
        {"labour_income": 300_000, "capital_income": 0, "age": 35, "self_employed": False},
        {"labour_income": 500_000, "capital_income": 0, "age": 45, "self_employed": False},
        {"labour_income": 700_000, "capital_income": 0, "age": 55, "self_employed": False},
        {"labour_income": 1_000_000, "capital_income": 50_000, "age": 50, "self_employed": False},
        {"labour_income": 250_000, "capital_income": 0, "age": 67, "self_employed": False},
        {"labour_income": 200_000, "capital_income": 0, "age": 30, "self_employed": True},
        {"labour_income": 0, "capital_income": 100_000, "age": 40, "self_employed": False},
    ]


@pytest.fixture(scope="session")
def income_array() -> np.ndarray:
    """Return a reproducible lognormal income array."""
    rng = np.random.default_rng(19960307)
    return rng.lognormal(12.5, 0.7, 500)


@pytest.fixture(scope="session")
def tax_array(income_array: np.ndarray) -> np.ndarray:
    """Return a simple proportional-progressive tax array."""
    y = income_array
    t = np.where(y < 300_000, y * 0.30, y * 0.30 + (y - 300_000) * 0.20)
    return t
