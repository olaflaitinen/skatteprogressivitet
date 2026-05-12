"""Tests for the Config model."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from skatteprogressivitet.config import Config


def test_default_config() -> None:
    c = Config()
    assert c.baseline_year == 2025
    assert c.behavioural == "full"
    assert c.eti_intensive == pytest.approx(0.3)
    assert c.seed == 20251008


def test_config_override() -> None:
    c = Config(baseline_year=2020, behavioural="none", eti_intensive=0.5)  # type: ignore[call-arg]
    assert c.baseline_year == 2020
    assert c.behavioural == "none"
    assert c.eti_intensive == pytest.approx(0.5)


def test_config_negative_eti_raises() -> None:
    with pytest.raises(ValidationError):
        Config(eti_intensive=-0.1)  # type: ignore[call-arg]


def test_config_immutable() -> None:
    c = Config()
    with pytest.raises(Exception):
        c.seed = 42  # type: ignore[misc]


def test_config_bootstrap_replications_positive() -> None:
    with pytest.raises(ValidationError):
        Config(bootstrap_replications=0)  # type: ignore[call-arg]


def test_config_n_jobs_minus_one_allowed() -> None:
    c = Config(n_jobs=-1)  # type: ignore[call-arg]
    assert c.n_jobs == -1
