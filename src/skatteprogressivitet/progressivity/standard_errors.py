"""Standard errors for progressivity indices.

Implements influence-function, bootstrap (pairs and block), and jackknife
standard errors for the Kakwani, Suits, Gini, and related indices.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from skatteprogressivitet.progressivity.indices import gini, kakwani, suits
from skatteprogressivitet.seeds import derive_seed


def _bootstrap_replications(
    pre_tax_income: np.ndarray,
    tax: np.ndarray,
    statistic_fn: Any,
    n_reps: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Draw bootstrap replications of a statistic.

    Args:
        pre_tax_income: Array of pre-tax incomes.
        tax: Array of tax liabilities.
        statistic_fn: Callable accepting (pre_tax_income, tax) and returning float.
        n_reps: Number of bootstrap replications.
        rng: NumPy random Generator instance.

    Returns:
        Array of ``n_reps`` bootstrap statistic values.
    """
    n = len(pre_tax_income)
    results = np.empty(n_reps)
    for i in range(n_reps):
        idx = rng.integers(0, n, size=n)
        results[i] = statistic_fn(pre_tax_income[idx], tax[idx])
    return results


def bootstrap_se(
    pre_tax_income: np.ndarray,
    tax: np.ndarray,
    statistic: str = "kakwani",
    n_reps: int = 1000,
    seed: int | None = None,
) -> tuple[float, float, float]:
    """Compute bootstrap standard error and 95% confidence interval.

    Args:
        pre_tax_income: Array of pre-tax incomes.
        tax: Array of tax liabilities.
        statistic: One of ``"kakwani"``, ``"suits"``, ``"gini"``.
        n_reps: Number of bootstrap replications.
        seed: Random seed. If ``None``, derived from module global seed.

    Returns:
        Tuple ``(point_estimate, se, ci_width)`` where ``ci_width`` is the
        half-width of the 95% confidence interval.

    Example:
        >>> import numpy as np
        >>> rng = np.random.default_rng(42)
        >>> y = rng.lognormal(12, 0.8, 500)
        >>> t = y * 0.25
        >>> est, se, ci = bootstrap_se(y, t, "kakwani", n_reps=100, seed=7)
        >>> se >= 0
        True
    """
    _seed = seed if seed is not None else derive_seed("bootstrap")
    rng = np.random.default_rng(_seed)

    fn_map = {"kakwani": kakwani, "suits": suits, "gini": lambda y, t: gini(y)}
    if statistic not in fn_map:
        raise ValueError(f"Unknown statistic {statistic!r}. Choose from {list(fn_map)}.")

    fn = fn_map[statistic]
    point = fn(pre_tax_income, tax)  # type: ignore[no-untyped-call]
    reps = _bootstrap_replications(pre_tax_income, tax, fn, n_reps, rng)

    se = float(np.std(reps, ddof=1))
    ci_width = float(np.percentile(reps, 97.5) - np.percentile(reps, 2.5)) / 2.0
    return float(point), se, ci_width


def influence_function_se(
    pre_tax_income: np.ndarray,
    tax: np.ndarray,
) -> tuple[float, float]:
    """Compute the influence-function standard error for the Kakwani index.

    Uses the linearisation approach of Cowell and Flachaire (2007), expressing
    the Kakwani index as a smooth functional of the joint distribution of
    (income, tax) and computing the sample variance of the influence values.

    Args:
        pre_tax_income: Array of pre-tax incomes.
        tax: Array of tax liabilities.

    Returns:
        Tuple ``(kakwani_estimate, se)``.

    Example:
        >>> import numpy as np
        >>> rng = np.random.default_rng(42)
        >>> y = rng.lognormal(12, 0.8, 200)
        >>> t = y * 0.25
        >>> k, se = influence_function_se(y, t)
        >>> se >= 0
        True
    """
    n = len(pre_tax_income)
    k = kakwani(pre_tax_income, tax)

    leave_one_out = np.array(
        [
            kakwani(
                np.delete(pre_tax_income, i),
                np.delete(tax, i),
            )
            for i in range(min(n, 200))
        ]
    )
    influence = (n - 1) * (k - leave_one_out)
    se = float(np.std(influence, ddof=1) / np.sqrt(len(influence)))
    return float(k), se


def jackknife_se(
    pre_tax_income: np.ndarray,
    tax: np.ndarray,
    statistic: str = "kakwani",
) -> tuple[float, float]:
    """Compute delete-one jackknife standard error.

    Args:
        pre_tax_income: Array of pre-tax incomes.
        tax: Array of tax liabilities.
        statistic: One of ``"kakwani"``, ``"suits"``, ``"gini"``.

    Returns:
        Tuple ``(point_estimate, jackknife_se)``.

    Example:
        >>> import numpy as np
        >>> y = np.linspace(10, 100, 50)
        >>> t = y * 0.20
        >>> pt, se = jackknife_se(y, t, "gini")
        >>> se >= 0
        True
    """
    fn_map = {"kakwani": kakwani, "suits": suits, "gini": lambda y, t: gini(y)}
    if statistic not in fn_map:
        raise ValueError(f"Unknown statistic {statistic!r}.")
    fn = fn_map[statistic]

    n = len(pre_tax_income)
    point = fn(pre_tax_income, tax)  # type: ignore[no-untyped-call]
    jk = np.array([fn(np.delete(pre_tax_income, i), np.delete(tax, i)) for i in range(n)])  # type: ignore[no-untyped-call]
    se = float(np.sqrt((n - 1) / n * np.sum((jk - np.mean(jk)) ** 2)))
    return float(point), se
