"""Capital income tax computation.

Implements the flat kapitalinkomstskatt (standard 30 percent rate) and any
year-specific special schedules defined in the legislation ledger.
"""

from __future__ import annotations

from skatteprogressivitet.legislation.schema import Legislation


def compute_capital_income_tax(net_capital_income: float, leg: Legislation) -> float:
    """Compute capital income tax on net capital income.

    Negative net capital income (a net capital loss) generates a tax reduction
    credit of 30 percent on the first 100 000 SEK and 21 percent on the excess,
    per the Swedish dual income tax rules.

    Args:
        net_capital_income: Net capital income in SEK. May be negative (loss).
        leg: Legislation for the year.

    Returns:
        Tax liability in SEK. Negative means a net tax reduction (credit).

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> compute_capital_income_tax(100000, leg)
        30000.0
        >>> compute_capital_income_tax(-50000, leg)
        -15000.0
    """
    rate = leg.kapitalinkomstskatt.standard_rate

    if net_capital_income >= 0:
        return net_capital_income * rate

    loss = abs(net_capital_income)
    if loss <= 100_000:
        credit = loss * rate
    else:
        credit = 100_000 * rate + (loss - 100_000) * 0.21
    return -credit


def compute_dividend_tax(dividend: float, leg: Legislation) -> float:
    """Compute tax on dividend income (outside 3:12 rules).

    Uses the dividend_rate if specified in the legislation, otherwise falls
    back to the standard capital income rate.

    Args:
        dividend: Dividend income in SEK.
        leg: Legislation for the year.

    Returns:
        Tax liability in SEK.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> compute_dividend_tax(50000, leg)
        15000.0
    """
    rate = leg.kapitalinkomstskatt.dividend_rate or leg.kapitalinkomstskatt.standard_rate
    return max(0.0, dividend) * rate
