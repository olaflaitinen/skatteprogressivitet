"""Equivalence scale utilities.

Implements the OECD-modified and square-root equivalence scales for adjusting
household income to per-equivalent-adult income.
"""

from __future__ import annotations


def oecd_modified_scale(n_adults: int, n_children: int) -> float:
    """Compute the OECD-modified equivalence scale.

    Assigns weight 1.0 to the first adult, 0.5 to each additional adult,
    and 0.3 to each child.

    Args:
        n_adults: Number of adults in the household (>= 1).
        n_children: Number of children (>= 0).

    Returns:
        Equivalence scale factor (>= 1.0).

    Example:
        >>> oecd_modified_scale(1, 0)
        1.0
        >>> oecd_modified_scale(2, 2)
        2.1
    """
    if n_adults < 1:
        raise ValueError("n_adults must be >= 1.")
    return 1.0 + (n_adults - 1) * 0.5 + n_children * 0.3


def square_root_scale(household_size: int) -> float:
    """Compute the square-root equivalence scale.

    Divides household income by the square root of household size.

    Args:
        household_size: Total number of household members (>= 1).

    Returns:
        Equivalence scale factor (>= 1.0).

    Example:
        >>> square_root_scale(1)
        1.0
        >>> abs(square_root_scale(4) - 2.0) < 1e-10
        True
    """
    if household_size < 1:
        raise ValueError("household_size must be >= 1.")
    return float(household_size) ** 0.5


def equivalise(
    income: float,
    n_adults: int,
    n_children: int,
    method: str = "oecd_modified",
) -> float:
    """Equivalise household income.

    Args:
        income: Household income in SEK.
        n_adults: Number of adults.
        n_children: Number of children.
        method: One of ``"oecd_modified"`` or ``"square_root"``.

    Returns:
        Equivalised income per adult equivalent in SEK.

    Example:
        >>> equivalise(200000, 2, 0, "square_root")
        141421.35623730953
    """
    if method == "oecd_modified":
        scale = oecd_modified_scale(n_adults, n_children)
    elif method == "square_root":
        household_size = n_adults + n_children
        scale = square_root_scale(max(1, household_size))
    else:
        raise ValueError(f"Unknown equivalence method: {method!r}")
    return income / scale
