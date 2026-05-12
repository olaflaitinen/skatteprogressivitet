"""Payroll tax computation.

Implements arbetsgivaravgifter (employer payroll taxes) and egenavgifter
(self-employed social contributions) for a single worker.
"""

from __future__ import annotations

from skatteprogressivitet.legislation.schema import Legislation


def compute_arbetsgivaravgift(
    labour_income: float,
    age: int,
    self_employed: bool,
    leg: Legislation,
) -> float:
    """Compute employer payroll tax (arbetsgivaravgift) or self-employed contribution.

    For employees (``self_employed=False``) this is the employer's cost on top
    of gross salary. For the self-employed it is the egenavgift.

    Age-based reduced rates are applied when specified in the legislation.

    Args:
        labour_income: Gross labour income in SEK.
        age: Worker's age in years.
        self_employed: Whether the worker is self-employed.
        leg: Legislation for the year.

    Returns:
        Payroll tax in SEK.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> compute_arbetsgivaravgift(400000, 35, False, leg) > 0
        True
    """
    if self_employed:
        rate = leg.egenavgift.rate
        ceiling = leg.egenavgift.ceiling
        base = min(labour_income, ceiling) if ceiling else labour_income
        return max(0.0, base * rate)

    aa = leg.arbetsgivaravgift
    if age < 26 and aa.reduced_rate_under_26 is not None:
        rate = aa.reduced_rate_under_26
    elif age > 65 and aa.reduced_rate_over_65 is not None:
        rate = aa.reduced_rate_over_65
    else:
        rate = aa.rate

    ceiling = aa.ceiling
    base = min(labour_income, ceiling) if ceiling else labour_income
    return max(0.0, base * rate)


def compute_egenavgift(labour_income: float, leg: Legislation) -> float:
    """Compute self-employed social contribution (egenavgift).

    Args:
        labour_income: Self-employment income in SEK.
        leg: Legislation for the year.

    Returns:
        Egenavgift in SEK.

    Example:
        >>> from skatteprogressivitet.legislation.loader import load_year
        >>> leg = load_year(2025)
        >>> compute_egenavgift(300000, leg) > 0
        True
    """
    ea = leg.egenavgift
    ceiling = ea.ceiling
    base = min(labour_income, ceiling) if ceiling else labour_income
    return max(0.0, base * ea.rate)
