"""Income-shifting module for 3:12 reclassification.

Models the labour-to-capital income reclassification by closely held firm
owners (fåmansföretag) under the 3:12 rules, following the identification
strategy in Alstadsaeter and Jacob (2016) and Blomqvist (2018).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from skatteprogressivitet.legislation.schema import Legislation


def shifting_elasticity(
    marginal_labour_rate: float,
    dividend_rate_qualified: float,
) -> float:
    """Estimate the income-shifting elasticity from the tax-rate differential.

    The shifting incentive is proportional to the tax-rate differential between
    labour income and qualified dividends. A simple linear approximation is used:

    ``elasticity = kappa * (tau_labour - tau_dividend)``

    where ``kappa = 0.5`` is a calibration constant consistent with Alstadsaeter
    and Jacob (2016).

    Args:
        marginal_labour_rate: Effective marginal rate on labour income.
        dividend_rate_qualified: Tax rate on qualified 3:12 dividends.

    Returns:
        Estimated income-shifting elasticity (non-negative).

    Example:
        >>> e = shifting_elasticity(0.57, 0.20)
        >>> e > 0
        True
    """
    kappa = 0.5
    differential = max(0.0, marginal_labour_rate - dividend_rate_qualified)
    return kappa * differential


def compute_shifted_income(
    labour_income: float,
    capital_ceiling: float,
    marginal_labour_rate: float,
    leg: Legislation,
) -> tuple[float, float]:
    """Compute adjusted labour and capital income after income shifting.

    Given a taxpayer who can shift income between labour and capital up to
    the qualified dividend ceiling, estimate how much they will shift.

    Args:
        labour_income: Pre-shifting labour income in SEK.
        capital_ceiling: Qualified dividend ceiling in SEK (from 3:12 rules).
        marginal_labour_rate: Effective marginal labour income tax rate.
        leg: Legislation for the year.

    Returns:
        A tuple (adjusted_labour_income, shifted_capital_income) in SEK.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> adj_l, cap = compute_shifted_income(800000, 200000, 0.57, leg)
        >>> cap >= 0 and adj_l >= 0
        True
    """
    if leg.three_twelve is None or not leg.three_twelve.enabled:
        return labour_income, 0.0

    drate = leg.three_twelve.dividend_rate_qualified
    elast = shifting_elasticity(marginal_labour_rate, drate)

    max_shift = min(labour_income, capital_ceiling)
    shifted = max_shift * elast

    adjusted_labour = labour_income - shifted
    shifted_capital = shifted

    return max(0.0, adjusted_labour), max(0.0, shifted_capital)
