"""Progressivity and inequality indices.

Implements Kakwani, Suits, residual-progression, Gini, Theil, and Atkinson
indices over arrays of pre-tax income and tax liability.
"""

from __future__ import annotations

import numpy as np


def gini(values: np.ndarray) -> float:
    """Compute the Gini coefficient of an array of non-negative values.

    Uses the formula based on the covariance between values and their
    rank, which is numerically stable for large arrays.

    Args:
        values: Array of non-negative values (e.g. incomes).

    Returns:
        Gini coefficient in [0, 1].

    Example:
        >>> import numpy as np
        >>> gini(np.array([1.0, 2.0, 3.0, 4.0]))
        0.25
    """
    n = len(values)
    if n == 0:
        return 0.0
    sorted_v = np.sort(values)
    total = np.sum(sorted_v)
    if total == 0.0:
        return 0.0
    ranks = np.arange(1, n + 1)
    return float((2.0 * np.sum(ranks * sorted_v) / (n * total)) - (n + 1) / n)


def concentration_index(tax: np.ndarray, income: np.ndarray) -> float:
    """Compute the concentration index of tax with respect to income.

    The concentration index is defined analogously to the Gini coefficient but
    ranks observations by income rather than by the tax variable itself.

    Args:
        tax: Array of tax liabilities.
        income: Array of pre-tax incomes (used for ranking).

    Returns:
        Concentration index in [-1, 1].

    Example:
        >>> import numpy as np
        >>> t = np.array([0.0, 1.0, 2.0, 3.0])
        >>> y = np.array([10.0, 20.0, 30.0, 40.0])
        >>> concentration_index(t, y)
        0.25
    """
    n = len(tax)
    if n == 0:
        return 0.0
    order = np.argsort(income)
    tax_sorted = tax[order]
    total_tax = np.sum(tax_sorted)
    if total_tax == 0.0:
        return 0.0
    ranks = np.arange(1, n + 1)
    return float((2.0 * np.sum(ranks * tax_sorted) / (n * total_tax)) - (n + 1) / n)


def kakwani(pre_tax_income: np.ndarray, tax: np.ndarray) -> float:
    """Compute the Kakwani progressivity index.

    The Kakwani index equals the concentration index of tax liabilities
    (ranked by pre-tax income) minus the Gini coefficient of pre-tax income.
    A positive value indicates a progressive tax schedule.

    Args:
        pre_tax_income: Array of pre-tax incomes.
        tax: Array of tax liabilities.

    Returns:
        Kakwani index.

    Example:
        >>> import numpy as np
        >>> y = np.array([10.0, 20.0, 30.0, 40.0])
        >>> t = y * np.array([0.10, 0.15, 0.20, 0.25])
        >>> k = kakwani(y, t)
        >>> k > 0
        True
    """
    g_income = gini(pre_tax_income)
    c_tax = concentration_index(tax, pre_tax_income)
    return float(c_tax - g_income)


def suits(pre_tax_income: np.ndarray, tax: np.ndarray) -> float:
    """Compute the Suits progressivity index.

    The Suits index measures progressivity as twice the area between the
    diagonal and the Lorenz-like curve of cumulative tax shares vs cumulative
    income shares. Range [-1, 1]; positive = progressive.

    Args:
        pre_tax_income: Array of pre-tax incomes.
        tax: Array of tax liabilities.

    Returns:
        Suits index.

    Example:
        >>> import numpy as np
        >>> y = np.array([10.0, 20.0, 30.0, 40.0])
        >>> t = y * np.array([0.10, 0.15, 0.20, 0.25])
        >>> s = suits(y, t)
        >>> s > 0
        True
    """
    n = len(pre_tax_income)
    if n == 0:
        return 0.0
    order = np.argsort(pre_tax_income)
    y_sorted = pre_tax_income[order]
    t_sorted = tax[order]

    cum_income = np.cumsum(y_sorted) / np.sum(y_sorted)
    cum_tax = np.cumsum(t_sorted)
    total_tax = np.sum(t_sorted)
    if total_tax == 0.0:
        return 0.0
    cum_tax_share = cum_tax / total_tax

    # Area under the Lorenz-type curve (trapezoid rule)
    area = float(np.trapz(cum_tax_share, cum_income))
    return float(1.0 - 2.0 * area)


def residual_progression(
    pre_tax_income: np.ndarray,
    post_tax_income: np.ndarray,
) -> float:
    """Compute the average residual progression index.

    Residual progression at income y is defined as:
    ``rp(y) = (1 - marginal_rate) / (1 - average_rate)``

    This function returns the population mean of this ratio.

    Args:
        pre_tax_income: Array of pre-tax incomes.
        post_tax_income: Array of post-tax incomes.

    Returns:
        Mean residual progression (scalar).

    Example:
        >>> import numpy as np
        >>> y = np.array([100.0, 200.0, 300.0, 400.0])
        >>> y_post = y - y * np.array([0.10, 0.15, 0.20, 0.25])
        >>> rp = residual_progression(y, y_post)
        >>> 0 < rp < 1.1
        True
    """
    if len(pre_tax_income) < 2:
        return 1.0
    order = np.argsort(pre_tax_income)
    y = pre_tax_income[order]
    y_post = post_tax_income[order]

    avg_rate = 1.0 - y_post / np.maximum(y, 1.0)
    dy = np.diff(y)
    dy_post = np.diff(y_post)
    marginal_rate = 1.0 - dy_post / np.maximum(dy, 1.0)

    denom = 1.0 - avg_rate[:-1]
    safe_denom = np.where(np.abs(denom) > 1e-10, denom, np.nan)
    rp = (1.0 - marginal_rate) / safe_denom
    return float(np.nanmean(rp))


def theil(values: np.ndarray) -> float:
    """Compute the Theil T inequality index.

    Args:
        values: Array of positive income values.

    Returns:
        Theil T index (>= 0).

    Example:
        >>> import numpy as np
        >>> theil(np.array([1.0, 2.0, 3.0, 4.0])) > 0
        True
    """
    v = values[values > 0]
    if len(v) == 0:
        return 0.0
    mu = np.mean(v)
    if mu <= 0:
        return 0.0
    return float(np.mean((v / mu) * np.log(v / mu)))


def atkinson(values: np.ndarray, epsilon: float = 0.5) -> float:
    """Compute the Atkinson inequality index.

    Args:
        values: Array of positive income values.
        epsilon: Inequality aversion parameter. Default 0.5.

    Returns:
        Atkinson index in [0, 1).

    Example:
        >>> import numpy as np
        >>> 0 < atkinson(np.array([1.0, 2.0, 3.0, 4.0])) < 1
        True
    """
    v = values[values > 0]
    if len(v) == 0:
        return 0.0
    mu = np.mean(v)
    if mu <= 0:
        return 0.0
    if abs(epsilon - 1.0) < 1e-10:
        ede = np.exp(np.mean(np.log(v)))
    else:
        ede = np.mean(v ** (1.0 - epsilon)) ** (1.0 / (1.0 - epsilon))
    return float(1.0 - ede / mu)
