"""Tests for the extensive-margin participation model."""

from __future__ import annotations

from skatteprogressivitet.behavioural.extensive_margin import (
    extensive_margin_revenue_effect,
    probit_participation_probability,
)


def test_high_gain_high_participation() -> None:
    p = probit_participation_probability(200_000)
    assert p > 0.9


def test_negative_gain_low_participation() -> None:
    p = probit_participation_probability(-100_000)
    assert p < 0.5


def test_probability_in_range() -> None:
    for gain in [-200_000, 0, 50_000, 200_000]:
        p = probit_participation_probability(gain)
        assert 0.0 <= p <= 1.0


def test_revenue_effect_positive_when_gain_increases() -> None:
    rev = extensive_margin_revenue_effect(1000, 40_000, 50_000, 60_000)
    assert rev > 0


def test_revenue_effect_negative_when_gain_decreases() -> None:
    rev = extensive_margin_revenue_effect(1000, 50_000, 30_000, 60_000)
    assert rev < 0
