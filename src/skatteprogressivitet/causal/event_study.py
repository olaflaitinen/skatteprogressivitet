"""Event-study designs around Swedish tax reform episodes.

Implements event-study regressions that trace the dynamic treatment effects
of reform episodes by interacting a treatment indicator with relative-time
dummies, normalising to the period immediately before the reform.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def event_study(
    df: pd.DataFrame,
    outcome: str,
    event_time: str,
    unit_id: str,
    time_id: str,
    pre_periods: int = 4,
    post_periods: int = 6,
    base_period: int = -1,
) -> pd.DataFrame:
    """Run an event-study regression using relative-time indicators.

    Estimates:
    ``Y_it = alpha_i + gamma_t + sum_{k != base} beta_k * 1[s_it = k] + eps``

    where ``s_it = t - event_time_i`` is the relative time to treatment.

    Args:
        df: Panel DataFrame.
        outcome: Outcome column name.
        event_time: Column containing the calendar period of first treatment
            (``NaN`` for never-treated units).
        unit_id: Unit fixed-effect column.
        time_id: Time column.
        pre_periods: Number of pre-event periods to include (negative relative time).
        post_periods: Number of post-event periods to include.
        base_period: Relative period to normalise to zero (excluded from regression).

    Returns:
        DataFrame with columns ``relative_time``, ``estimate``, ``se``.

    Example:
        >>> import pandas as pd, numpy as np
        >>> rng = np.random.default_rng(42)
        >>> n_units, n_times = 20, 10
        >>> event_times = np.array([5]*10 + [np.nan]*10)
        >>> df = pd.DataFrame({
        ...     "unit": np.repeat(np.arange(n_units), n_times),
        ...     "time": np.tile(np.arange(n_times), n_units),
        ...     "event_time": np.repeat(event_times, n_times),
        ...     "y": rng.normal(0, 1, n_units * n_times),
        ... })
        >>> result = event_study(df, "y", "event_time", "unit", "time")
        >>> isinstance(result, pd.DataFrame)
        True
    """
    data = df.copy()
    data["_rel_time"] = data[time_id] - data[event_time]

    relative_periods = list(range(-pre_periods, post_periods + 1))
    relative_periods = [k for k in relative_periods if k != base_period]

    results = []
    for k in relative_periods:
        subset = data[data["_rel_time"].isin([k, base_period]) | data[event_time].isna()].copy()
        subset["_indicator"] = (subset["_rel_time"] == k).astype(float)

        subset["_y_dm"] = (
            subset[outcome]
            - subset.groupby(unit_id)[outcome].transform("mean")
            - subset.groupby(time_id)[outcome].transform("mean")
            + subset[outcome].mean()
        )
        subset["_d_dm"] = (
            subset["_indicator"]
            - subset.groupby(unit_id)["_indicator"].transform("mean")
            - subset.groupby(time_id)["_indicator"].transform("mean")
            + subset["_indicator"].mean()
        )

        d_vals = subset["_d_dm"].values
        y_vals = subset["_y_dm"].values
        dd = float(np.sum(d_vals**2))
        if dd == 0.0:
            results.append({"relative_time": k, "estimate": 0.0, "se": np.nan})
            continue

        beta = float(np.dot(d_vals, y_vals) / dd)
        resid = y_vals - beta * d_vals
        n = len(y_vals)
        sigma2 = float(np.sum(resid**2) / max(n - 2, 1))
        se = float(np.sqrt(sigma2 / dd))
        results.append({"relative_time": k, "estimate": beta, "se": se})

    result_df = pd.DataFrame(results).sort_values("relative_time").reset_index(drop=True)
    base_row = pd.DataFrame([{"relative_time": base_period, "estimate": 0.0, "se": 0.0}])
    return (
        pd.concat([result_df, base_row], ignore_index=True)
        .sort_values("relative_time")
        .reset_index(drop=True)
    )
