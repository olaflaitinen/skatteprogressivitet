"""Housing allowance computation.

Implements bostadsbidrag (housing allowance for families and young people) and
bostadstillagg (housing supplement for pensioners) entitlements.
"""

from __future__ import annotations

from skatteprogressivitet.legislation.schema import Legislation


def compute_bostadsbidrag(
    annual_income: float,
    housing_cost: float,
    leg: Legislation,
) -> float:
    """Compute bostadsbidrag entitlement.

    The benefit phases out linearly above zero income at the income_taper_rate
    and is capped at the legislative maximum.

    Args:
        annual_income: Annual household income in SEK.
        housing_cost: Annual housing cost in SEK (used for eligibility; simplified).
        leg: Legislation for the year.

    Returns:
        Annual bostadsbidrag entitlement in SEK (non-negative).

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> compute_bostadsbidrag(100000, 60000, leg) >= 0
        True
    """
    if leg.housing_allowance is None:
        return 0.0
    ha = leg.housing_allowance
    taper = ha.income_taper_rate * annual_income
    raw = ha.bostadsbidrag_max - taper
    return max(0.0, min(raw, ha.bostadsbidrag_max))


def compute_bostadstillagg(
    annual_pension_income: float,
    housing_cost: float,
    leg: Legislation,
) -> float:
    """Compute bostadstillagg entitlement for pensioners.

    Args:
        annual_pension_income: Annual pension income in SEK.
        housing_cost: Annual housing cost in SEK.
        leg: Legislation for the year.

    Returns:
        Annual bostadstillagg entitlement in SEK (non-negative).

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> compute_bostadstillagg(120000, 48000, leg) >= 0
        True
    """
    if leg.housing_allowance is None:
        return 0.0
    ha = leg.housing_allowance
    taper = ha.income_taper_rate * annual_pension_income
    raw = ha.bostadstillagg_max - taper
    return max(0.0, min(raw, ha.bostadstillagg_max))
