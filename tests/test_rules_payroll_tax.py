"""Tests for payroll tax computation."""

from __future__ import annotations

import pytest

from skatteprogressivitet.legislation.loader import load_year
from skatteprogressivitet.rules.payroll_tax import compute_arbetsgivaravgift, compute_egenavgift


@pytest.fixture(scope="module")
def leg2025():
    return load_year(2025)


def test_employer_payroll_positive(leg2025) -> None:
    tax = compute_arbetsgivaravgift(400_000, 35, False, leg2025)
    assert tax > 0


def test_employer_payroll_proportional(leg2025) -> None:
    t1 = compute_arbetsgivaravgift(200_000, 35, False, leg2025)
    t2 = compute_arbetsgivaravgift(400_000, 35, False, leg2025)
    assert t2 == pytest.approx(2 * t1, rel=1e-6)


def test_reduced_rate_under_26(leg2025) -> None:
    t_young = compute_arbetsgivaravgift(400_000, 22, False, leg2025)
    t_normal = compute_arbetsgivaravgift(400_000, 35, False, leg2025)
    if leg2025.arbetsgivaravgift.reduced_rate_under_26 is not None:
        assert t_young <= t_normal


def test_reduced_rate_over_65(leg2025) -> None:
    t_senior = compute_arbetsgivaravgift(400_000, 70, False, leg2025)
    t_normal = compute_arbetsgivaravgift(400_000, 35, False, leg2025)
    if leg2025.arbetsgivaravgift.reduced_rate_over_65 is not None:
        assert t_senior <= t_normal


def test_self_employed_uses_egenavgift(leg2025) -> None:
    t_emp = compute_arbetsgivaravgift(300_000, 40, False, leg2025)
    t_self = compute_arbetsgivaravgift(300_000, 40, True, leg2025)
    assert t_emp != t_self


def test_egenavgift_positive(leg2025) -> None:
    assert compute_egenavgift(300_000, leg2025) > 0


def test_zero_income_zero_tax(leg2025) -> None:
    assert compute_arbetsgivaravgift(0, 35, False, leg2025) == pytest.approx(0.0)
    assert compute_egenavgift(0, leg2025) == pytest.approx(0.0)
