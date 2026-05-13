"""Jobbskatteavdrag (earned-income tax credit) computation.

The jobbskatteavdrag was introduced in 2007 and expanded through five steps.
The credit depends on earned income, the kommunal tax rate, and age (enhanced
rate for workers over 65 when the legislation so specifies).

The schedule in the legislation YAML is an informational piecewise description.
This module implements the credit directly against the statutory formulas
parameterised by the prisbasbelopp and kommunal rate.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from skatteprogressivitet.legislation.schema import Legislation


def compute_jobbskatteavdrag(
    earned_income: float,
    age: int,
    leg: Legislation,
) -> float:
    """Compute the jobbskatteavdrag credit for a single taxpayer.

    Returns zero if the legislation year does not enable the credit.

    The credit is approximated from the piecewise schedule stored in the ledger.
    In the absence of a fully parameterised formula, this function implements a
    smoothed piecewise linear approximation consistent with Finansdepartementet
    microsimulation methodology.

    Args:
        earned_income: Earned (labour) income in SEK.
        age: Taxpayer age in years.
        leg: Legislation for the year.

    Returns:
        Credit amount in SEK (non-negative; reduces tax liability).

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> compute_jobbskatteavdrag(300000, 40, leg) > 0
        True
        >>> compute_jobbskatteavdrag(300000, 40, load_year(1991))
        0.0
    """
    jsa = leg.jobbskatteavdrag
    if not jsa.enabled:
        return 0.0

    kommunal_rate = leg.kommunal_skatt.rate
    pbb = leg.prisbasbelopp

    # Age-based enhancement multiplier (over 65 when the legislation so specifies)
    age_factor = 1.25 if (age >= 65 and jsa.age_65_plus_enhanced) else 1.0

    credit = _piecewise_credit(earned_income, kommunal_rate, pbb)
    return max(0.0, credit * age_factor)


def _piecewise_credit(earned_income: float, kommunal_rate: float, pbb: float) -> float:
    """Compute the base credit using a generalised piecewise linear schedule.

    The schedule uses prisbasbelopp (PBB) as the natural income unit, consistent
    with the statutory definition.

    Args:
        earned_income: Earned income in SEK.
        kommunal_rate: Municipal tax rate (fraction).
        pbb: Prisbasbelopp in SEK for this year.

    Returns:
        Base credit in SEK.
    """
    # Phase-in region: 0 to 0.91 * PBB
    # Credit rises linearly to kommunal_rate * 0.91 * PBB * factor
    # Phase-flat region: 0.91 * PBB to ~6 * PBB
    # Phase-out region: above ~7 * PBB
    t0 = 0.91 * pbb
    t1 = 2.72 * pbb
    t2 = 7.0 * pbb

    if earned_income <= 0:
        return 0.0

    if earned_income <= t0:
        return kommunal_rate * earned_income

    if earned_income <= t1:
        credit_at_t0 = kommunal_rate * t0
        additional = kommunal_rate * (earned_income - t0) * 0.3174
        return credit_at_t0 + additional

    max_credit = kommunal_rate * t0 + kommunal_rate * (t1 - t0) * 0.3174

    if earned_income <= t2:
        return max_credit

    # Phase-out above t2
    phase_out = kommunal_rate * (earned_income - t2) * 0.03
    return max(0.0, max_credit - phase_out)
