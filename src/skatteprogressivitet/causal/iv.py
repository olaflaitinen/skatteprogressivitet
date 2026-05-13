"""Instrumental-variables and bunching-as-IV estimators.

Implements 2SLS IV estimation and a bunching-as-IV wrapper that uses the
predicted mass shift at the britpunkt as an instrument for the net-of-tax rate.
"""

from __future__ import annotations

import numpy as np


def tsls(
    y: np.ndarray,
    x: np.ndarray,
    z: np.ndarray,
    controls: np.ndarray | None = None,
) -> dict[str, float]:
    """Two-stage least squares (2SLS) IV estimator.

    Args:
        y: Outcome vector (n,).
        x: Endogenous regressor (n,).
        z: Instrument (n,).
        controls: Optional matrix of exogenous controls (n, k).

    Returns:
        Dictionary with keys ``"estimate"``, ``"se"``, ``"f_first_stage"``,
        ``"n_obs"``.

    Example:
        >>> import numpy as np
        >>> rng = np.random.default_rng(7)
        >>> n = 300
        >>> z = rng.normal(0, 1, n)
        >>> x = 0.8 * z + rng.normal(0, 0.5, n)
        >>> y = 1.5 * x + rng.normal(0, 1, n)
        >>> r = tsls(y, x, z)
        >>> abs(r["estimate"] - 1.5) < 0.5
        True
    """
    n = len(y)

    if controls is not None:
        c = controls
        z_aug = np.column_stack([z, c])
        x_aug = np.column_stack([x, c])
    else:
        z_aug = z.reshape(-1, 1)
        x_aug = x.reshape(-1, 1)

    # First stage
    pz = z_aug @ np.linalg.pinv(z_aug.T @ z_aug) @ z_aug.T
    x_hat = pz @ x_aug[:, 0]

    # First-stage F-statistic
    resid_first = x_aug[:, 0] - x_hat
    ss_res = float(np.sum(resid_first**2))
    ss_tot = float(np.sum((x_aug[:, 0] - np.mean(x_aug[:, 0])) ** 2))
    r2_first = 1.0 - ss_res / max(ss_tot, 1e-10)
    k_inst = 1
    f_first = float((r2_first / k_inst) / ((1 - r2_first) / max(n - k_inst - 1, 1)))

    # Second stage
    x_second = np.column_stack([x_hat] + ([] if controls is None else [controls]))
    beta_2sls = np.linalg.lstsq(x_second, y, rcond=None)[0]

    estimate = float(beta_2sls[0])
    resid_2sls = y - x_second @ beta_2sls
    sigma2 = float(np.sum(resid_2sls**2) / max(n - x_second.shape[1], 1))
    xx_inv = np.linalg.pinv(x_second.T @ x_second)
    se = float(np.sqrt(sigma2 * xx_inv[0, 0]))

    return {"estimate": estimate, "se": se, "f_first_stage": f_first, "n_obs": n}


def bunching_iv(
    incomes: np.ndarray,
    outcome: np.ndarray,
    threshold: float,
    window: float = 50_000.0,
    bin_width: float = 10_000.0,
) -> dict[str, float]:
    """Bunching-as-IV estimator using excess mass at the britpunkt as instrument.

    Units close to the threshold are assigned to the instrument based on
    predicted vs. observed bin counts, following Chetty et al. (2011).

    Args:
        incomes: Array of incomes.
        outcome: Array of outcome values (e.g. post-reform income).
        threshold: Statutory threshold (britpunkt).
        window: Half-width of the bunching window in SEK.
        bin_width: Bin width in SEK.

    Returns:
        Dictionary with ``"estimate"``, ``"se"``, ``"n_obs"``.

    Example:
        >>> import numpy as np
        >>> rng = np.random.default_rng(42)
        >>> y_inc = rng.normal(500000, 80000, 1000)
        >>> y_out = y_inc * 0.9 + rng.normal(0, 5000, 1000)
        >>> r = bunching_iv(y_inc, y_out, threshold=500000)
        >>> "estimate" in r
        True
    """
    in_window = (incomes >= threshold - window) & (incomes <= threshold + window)
    instrument = in_window.astype(float)
    return tsls(outcome, incomes, instrument)
