"""Tests for the ETI behavioural response module."""

from __future__ import annotations

import pytest

from skatteprogressivitet.behavioural.eti import ETIResponse


def test_no_rate_change_no_response() -> None:
    eti = ETIResponse(eti_intensive=0.3)
    tp = {"labour_income": 500_000}
    result = eti.marginal_response(tp, 0.55, 0.55)
    assert result == pytest.approx(500_000)


def test_lower_rate_increases_income() -> None:
    eti = ETIResponse(eti_intensive=0.3)
    tp = {"labour_income": 500_000}
    result = eti.marginal_response(tp, 0.50, 0.55)
    assert result > 500_000


def test_higher_rate_decreases_income() -> None:
    eti = ETIResponse(eti_intensive=0.3)
    tp = {"labour_income": 500_000}
    result = eti.marginal_response(tp, 0.60, 0.55)
    assert result < 500_000


def test_zero_income_no_change() -> None:
    eti = ETIResponse(eti_intensive=0.3)
    tp = {"labour_income": 0}
    result = eti.marginal_response(tp, 0.50, 0.30)
    assert result == pytest.approx(0.0)


def test_negative_eti_raises() -> None:
    with pytest.raises(ValueError):
        ETIResponse(eti_intensive=-0.1)


def test_participation_response_in_range() -> None:
    eti = ETIResponse(eti_extensive=0.1)
    p = eti.participation_response(0.85, 50_000, 45_000)
    assert 0.0 <= p <= 1.0


def test_result_non_negative() -> None:
    eti = ETIResponse(eti_intensive=1.0)
    tp = {"labour_income": 100_000}
    result = eti.marginal_response(tp, 0.99, 0.50)
    assert result >= 0.0
