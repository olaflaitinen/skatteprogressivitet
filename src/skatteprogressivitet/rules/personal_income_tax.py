"""Personal income tax computation.

Implements statlig inkomstskatt and kommunal inkomstskatt for a single taxpayer
under a given year's :class:`Legislation`.
"""

from __future__ import annotations

from typing import Any

from skatteprogressivitet.legislation.schema import Legislation
from skatteprogressivitet.rules.jobbskatteavdrag import compute_jobbskatteavdrag


def _compute_statlig(labour_income: float, leg: Legislation) -> float:
    """Apply the state income tax bracket schedule.

    Args:
        labour_income: Taxable labour income in SEK.
        leg: Legislation for the year.

    Returns:
        State income tax liability in SEK.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> _compute_statlig(700000, leg) > 0
        True
    """
    tax = 0.0
    brackets = leg.statlig_skatt.brackets
    for i, bracket in enumerate(brackets):
        lower = bracket.lower
        upper = bracket.upper if bracket.upper is not None else float("inf")
        if labour_income <= lower:
            break
        taxable_in_bracket = min(labour_income, upper) - lower
        tax += taxable_in_bracket * bracket.rate
    return tax


def _compute_kommunal(labour_income: float, leg: Legislation) -> float:
    """Apply the proportional municipal income tax.

    Args:
        labour_income: Taxable labour income in SEK.
        leg: Legislation for the year.

    Returns:
        Municipal income tax liability in SEK.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> _compute_kommunal(400000, leg) > 0
        True
    """
    return labour_income * leg.kommunal_skatt.rate


def _compute_marginal_rate(labour_income: float, leg: Legislation) -> float:
    """Compute the effective marginal labour income tax rate at a given income.

    The marginal rate is the sum of kommunal_skatt.rate and the statlig bracket
    rate that applies at the given income level, minus the marginal jobbskatteavdrag
    relief.

    Args:
        labour_income: Labour income level in SEK.
        leg: Legislation for the year.

    Returns:
        Marginal rate as a fraction between 0 and 1.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> 0 < _compute_marginal_rate(700000, leg) < 1
        True
    """
    kommunal_rate = leg.kommunal_skatt.rate
    statlig_rate = 0.0
    for bracket in leg.statlig_skatt.brackets:
        lower = bracket.lower
        upper = bracket.upper if bracket.upper is not None else float("inf")
        if lower < labour_income <= upper:
            statlig_rate = bracket.rate
            break
        if labour_income > upper:
            statlig_rate = bracket.rate
    return min(kommunal_rate + statlig_rate, 1.0)


def compute_personal_income_tax(
    taxpayer: dict[str, Any],
    leg: Legislation,
) -> "TaxOutcome":
    """Compute full personal income tax outcome for a single taxpayer.

    Args:
        taxpayer: Dictionary with keys:
            - ``labour_income``: float, SEK.
            - ``capital_income``: float, SEK.
            - ``age``: int.
            - ``self_employed``: bool.
        leg: Legislation for the year.

    Returns:
        A :class:`~skatteprogressivitet.legislation.ledger.TaxOutcome`.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> tp = {"labour_income": 500000, "capital_income": 0,
        ...       "age": 45, "self_employed": False}
        >>> outcome = compute_personal_income_tax(tp, leg)
        >>> outcome.total_tax > 0
        True
    """
    from skatteprogressivitet.legislation.ledger import TaxOutcome
    from skatteprogressivitet.rules.capital_income_tax import compute_capital_income_tax
    from skatteprogressivitet.rules.payroll_tax import compute_arbetsgivaravgift

    labour_income: float = float(taxpayer.get("labour_income", 0))
    capital_income: float = float(taxpayer.get("capital_income", 0))
    age: int = int(taxpayer.get("age", 40))
    self_employed: bool = bool(taxpayer.get("self_employed", False))

    statlig = _compute_statlig(labour_income, leg)
    kommunal = _compute_kommunal(labour_income, leg)
    kapital = compute_capital_income_tax(capital_income, leg)
    jsa = compute_jobbskatteavdrag(labour_income, age, leg)
    arbetsgivar = compute_arbetsgivaravgift(labour_income, age, self_employed, leg)
    marginal = _compute_marginal_rate(labour_income, leg)

    gross = labour_income + capital_income

    return TaxOutcome(
        statlig_skatt=statlig,
        kommunal_skatt=kommunal,
        kapitalinkomstskatt=kapital,
        arbetsgivaravgift=arbetsgivar,
        jobbskatteavdrag=jsa,
        gross_income=gross,
        marginal_rate=marginal,
    )
