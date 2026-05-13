"""3:12 rules for closely held firms (fåmansföretag).

Implements the two main methods for computing the qualified dividend ceiling
under the Swedish 3:12 rules: förenklingsregeln (the simplified rule) and
huvudregeln (the main rule).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from skatteprogressivitet.legislation.schema import Legislation


def compute_forenklingsregeln_ceiling(leg: Legislation) -> float:
    """Compute the qualified dividend ceiling under förenklingsregeln.

    Förenklingsregeln allows a flat dividend ceiling regardless of the salary
    paid by the company. The ceiling equals the base amount defined in the
    legislation, indexed to inkomstbasbelopp.

    Args:
        leg: Legislation for the year.

    Returns:
        Maximum qualified dividend in SEK under förenklingsregeln.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> compute_forenklingsregeln_ceiling(leg) > 0
        True
    """
    if leg.three_twelve is None or not leg.three_twelve.enabled:
        return 0.0
    return leg.three_twelve.forenklingsregeln_base


def compute_huvudregeln_ceiling(anskaffningsvarde: float, leg: Legislation) -> float:
    """Compute the qualified dividend ceiling under huvudregeln.

    Huvudregeln sets the qualified dividend ceiling as a required return on the
    acquisition cost of shares (anskaffningsvarde) multiplied by the statutory
    return rate plus an IBB-based salary component.

    Args:
        anskaffningsvarde: Acquisition cost (omkostnadsbelopp) of shares in SEK.
        leg: Legislation for the year.

    Returns:
        Maximum qualified dividend in SEK under huvudregeln.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> compute_huvudregeln_ceiling(1_000_000, leg) > 0
        True
    """
    if leg.three_twelve is None or not leg.three_twelve.enabled:
        return 0.0
    return_rate = leg.three_twelve.huvudregeln_return_rate
    ibb_component = leg.inkomstbasbelopp * 0.5
    return anskaffningsvarde * return_rate + ibb_component


def compute_three_twelve_tax(
    dividend: float,
    anskaffningsvarde: float,
    use_forenklingsregeln: bool,
    leg: Legislation,
) -> tuple[float, float]:
    """Compute tax on dividends from a closely held firm under 3:12 rules.

    Dividends up to the qualified ceiling are taxed at the reduced qualified
    rate (currently 20 percent). Dividends above the ceiling are reclassified
    as labour income and taxed at the excess rate.

    Args:
        dividend: Total dividend amount in SEK.
        anskaffningsvarde: Acquisition cost of shares, used for huvudregeln.
        use_forenklingsregeln: If True, use förenklingsregeln; else huvudregeln.
        leg: Legislation for the year.

    Returns:
        A tuple (qualified_tax, excess_tax) in SEK.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> qt, et = compute_three_twelve_tax(300000, 2000000, False, leg)
        >>> qt >= 0 and et >= 0
        True
    """
    if leg.three_twelve is None or not leg.three_twelve.enabled:
        return 0.0, 0.0

    if use_forenklingsregeln:
        ceiling = compute_forenklingsregeln_ceiling(leg)
    else:
        ceiling = compute_huvudregeln_ceiling(anskaffningsvarde, leg)

    qualified = min(dividend, ceiling)
    excess = max(0.0, dividend - ceiling)

    qualified_tax = qualified * leg.three_twelve.dividend_rate_qualified
    excess_tax = excess * leg.three_twelve.dividend_rate_excess

    return qualified_tax, excess_tax
