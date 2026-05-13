"""Bunching-based identification around statutory bracket thresholds.

Implements a Chetty/Saez-style bunching estimator for identifying the
elasticity of taxable income from excess mass at the brytpunkt (the state
income tax bracket threshold).
"""

from __future__ import annotations

import numpy as np


def count_bin_mass(
    incomes: np.ndarray,
    bin_lower: float,
    bin_upper: float,
) -> int:
    """Count the number of observations in an income bin.

    Args:
        incomes: Array of income values.
        bin_lower: Lower bound of the bin (inclusive).
        bin_upper: Upper bound of the bin (exclusive).

    Returns:
        Count of observations in the bin.

    Example:
        >>> import numpy as np
        >>> arr = np.array([100, 200, 300, 400, 500])
        >>> count_bin_mass(arr, 150, 350)
        2
    """
    return int(np.sum((incomes >= bin_lower) & (incomes < bin_upper)))


def estimate_counterfactual_density(
    incomes: np.ndarray,
    threshold: float,
    window_lower: float,
    window_upper: float,
    bin_width: float = 10_000.0,
    poly_degree: int = 5,
) -> np.ndarray:
    """Estimate the counterfactual income density around a threshold.

    Fits a polynomial to the observed income distribution, excluding the
    bunching window ``[threshold - window_lower, threshold + window_upper]``,
    and returns the fitted density at each bin centre.

    Args:
        incomes: Array of income values.
        threshold: Statutory threshold (brytpunkt) in SEK.
        window_lower: Width of the exclusion window below the threshold.
        window_upper: Width of the exclusion window above the threshold.
        bin_width: Bin width in SEK. Default 10 000.
        poly_degree: Degree of the polynomial fit. Default 5.

    Returns:
        Array of counterfactual bin densities.

    Example:
        >>> import numpy as np
        >>> rng = np.random.default_rng(42)
        >>> incomes = rng.normal(500000, 100000, 5000)
        >>> cf = estimate_counterfactual_density(incomes, 500000, 50000, 50000)
        >>> len(cf) > 0
        True
    """
    lo = threshold - window_lower - bin_width * 20
    hi = threshold + window_upper + bin_width * 20
    bins = np.arange(lo, hi + bin_width, bin_width)
    centres = (bins[:-1] + bins[1:]) / 2.0

    counts = np.array([count_bin_mass(incomes, bins[i], bins[i + 1]) for i in range(len(centres))])

    exclude = (centres >= threshold - window_lower) & (centres <= threshold + window_upper)
    fit_centres = centres[~exclude]
    fit_counts = counts[~exclude]

    if len(fit_centres) < poly_degree + 1:
        return counts.astype(float)

    coeffs = np.polyfit(fit_centres, fit_counts, poly_degree)
    counterfactual = np.polyval(coeffs, centres)
    return np.maximum(counterfactual, 0.0)


def estimate_bunching_eti(
    incomes: np.ndarray,
    threshold: float,
    window_lower: float,
    window_upper: float,
    delta_log_ntr: float,
    bin_width: float = 10_000.0,
) -> float:
    """Estimate ETI from excess bunching mass at a statutory threshold.

    Uses the Chetty et al. (2011) formula:
    ``eti = (B / h_0(z*)) / (z* * delta_log(1-t))``

    where ``B`` is excess bunching, ``h_0(z*)`` is the counterfactual density
    at the threshold, and ``z*`` is the threshold income.

    Args:
        incomes: Array of income values.
        threshold: Statutory threshold in SEK.
        window_lower: Exclusion window width below threshold in SEK.
        window_upper: Exclusion window width above threshold in SEK.
        delta_log_ntr: Change in log net-of-tax rate at the kink.
        bin_width: Bin width in SEK.

    Returns:
        ETI estimate (non-negative float).

    Example:
        >>> import numpy as np
        >>> rng = np.random.default_rng(7)
        >>> incomes = rng.normal(500000, 100000, 10000)
        >>> eti = estimate_bunching_eti(incomes, 500000, 50000, 50000, 0.05)
        >>> eti >= 0
        True
    """
    counterfactual = estimate_counterfactual_density(
        incomes, threshold, window_lower, window_upper, bin_width
    )

    lo = threshold - window_lower - bin_width * 20
    bins = np.arange(lo, threshold + window_upper + bin_width * 21, bin_width)
    centres = (bins[:-1] + bins[1:]) / 2.0

    observed_at_threshold = count_bin_mass(
        incomes, threshold - bin_width / 2, threshold + bin_width / 2
    )

    idx = np.searchsorted(centres, threshold)
    if idx >= len(counterfactual):
        return 0.0

    h0_z_star = counterfactual[idx]
    if h0_z_star <= 0 or delta_log_ntr <= 0 or threshold <= 0:
        return 0.0

    excess_mass = (observed_at_threshold - h0_z_star) / h0_z_star
    eti = excess_mass / (threshold * delta_log_ntr / bin_width)
    return float(max(0.0, eti))
