"""Social transfer entitlement computation.

Implements sjukpenning (sickness benefit), föräldrapenning (parental benefit),
arbetslöshetsersättning (unemployment benefit), and sjukersättning
(disability benefit) for a single taxpayer.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from skatteprogressivitet.legislation.schema import Legislation


def _daily_rate(annual_income: float, replacement_rate: float, ceiling_sek: float) -> float:
    """Convert annual income to a daily benefit rate respecting a ceiling.

    Args:
        annual_income: Annual labour income in SEK.
        replacement_rate: Replacement rate as a fraction.
        ceiling_sek: Annual income ceiling for the benefit.

    Returns:
        Daily benefit rate in SEK.
    """
    capped_income = min(annual_income, ceiling_sek)
    return capped_income * replacement_rate / 365.0


def compute_sjukpenning(
    labour_income: float,
    sick_days: int,
    leg: Legislation,
) -> float:
    """Compute sjukpenning entitlement.

    Args:
        labour_income: Annual labour income in SEK.
        sick_days: Number of qualifying sick days (excluding the first carensdag).
        leg: Legislation for the year.

    Returns:
        Total sjukpenning entitlement in SEK.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> compute_sjukpenning(400000, 30, leg) > 0
        True
    """
    if leg.transfers is None:
        return 0.0
    t = leg.transfers
    ceiling = t.a_kassa_ceiling_ibb_fraction * leg.inkomstbasbelopp * 7.5
    daily = _daily_rate(labour_income, t.sjukpenning_rate, ceiling)
    return daily * max(0, sick_days)


def compute_foraldrapenning(
    labour_income: float,
    parental_days: int,
    leg: Legislation,
) -> float:
    """Compute föräldrapenning entitlement.

    Args:
        labour_income: Annual labour income in SEK.
        parental_days: Number of qualifying parental leave days at SGI-based rate.
        leg: Legislation for the year.

    Returns:
        Total föräldrapenning entitlement in SEK.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> compute_foraldrapenning(400000, 90, leg) > 0
        True
    """
    if leg.transfers is None:
        return 0.0
    t = leg.transfers
    ceiling = t.a_kassa_ceiling_ibb_fraction * leg.inkomstbasbelopp * 7.5
    daily = _daily_rate(labour_income, t.foraldrapenning_rate, ceiling)
    return daily * max(0, parental_days)


def compute_a_kassa(
    labour_income: float,
    unemployment_days: int,
    leg: Legislation,
) -> float:
    """Compute arbetslöshetsersättning (a-kassa) entitlement.

    Args:
        labour_income: Annual labour income in SEK (prior to unemployment).
        unemployment_days: Number of qualifying unemployment days.
        leg: Legislation for the year.

    Returns:
        Total a-kassa entitlement in SEK.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> compute_a_kassa(350000, 60, leg) > 0
        True
    """
    if leg.transfers is None:
        return 0.0
    t = leg.transfers
    ceiling = t.a_kassa_ceiling_ibb_fraction * leg.inkomstbasbelopp
    daily = _daily_rate(labour_income, t.a_kassa_rate, ceiling)
    return daily * max(0, unemployment_days)
