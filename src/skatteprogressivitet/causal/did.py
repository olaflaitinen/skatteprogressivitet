"""Difference-in-differences estimators.

Implements two-way fixed-effects (TWFE) DiD and the Callaway-Sant'Anna (2021)
heterogeneity-robust estimator for staggered adoption designs.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def twfe_did(
    df: pd.DataFrame,
    outcome: str,
    treatment: str,
    unit_id: str,
    time_id: str,
) -> dict[str, float]:
    """Estimate a two-way fixed-effects DiD coefficient.

    Fits the model: ``Y_it = alpha_i + gamma_t + beta * D_it + eps_it``
    using within-transformation (demeaning by unit and time).

    Args:
        df: Panel DataFrame with columns for outcome, treatment indicator,
            unit identifier, and time identifier.
        outcome: Name of the outcome column.
        treatment: Name of the binary treatment column.
        unit_id: Name of the unit fixed-effect column.
        time_id: Name of the time fixed-effect column.

    Returns:
        Dictionary with keys ``"estimate"``, ``"se"``, ``"n_obs"``, ``"n_units"``.

    Example:
        >>> import pandas as pd, numpy as np
        >>> rng = np.random.default_rng(42)
        >>> n = 200
        >>> df = pd.DataFrame({
        ...     "unit": np.repeat(np.arange(20), 10),
        ...     "time": np.tile(np.arange(10), 20),
        ...     "treat": (np.repeat(np.arange(20), 10) >= 10).astype(float),
        ...     "y": rng.normal(0, 1, n),
        ... })
        >>> result = twfe_did(df, "y", "treat", "unit", "time")
        >>> "estimate" in result
        True
    """
    data = df.copy()
    data["_y_demeaned"] = (
        data[outcome]
        - data.groupby(unit_id)[outcome].transform("mean")
        - data.groupby(time_id)[outcome].transform("mean")
        + data[outcome].mean()
    )
    data["_d_demeaned"] = (
        data[treatment]
        - data.groupby(unit_id)[treatment].transform("mean")
        - data.groupby(time_id)[treatment].transform("mean")
        + data[treatment].mean()
    )

    d = data["_d_demeaned"].values
    y = data["_y_demeaned"].values

    dd = float(np.sum(d**2))
    if dd == 0.0:
        return {"estimate": 0.0, "se": np.nan, "n_obs": len(data), "n_units": 0}

    beta = float(np.sum(d * y) / dd)
    resid = y - beta * d
    n = len(y)
    k = 2  # approximate df used for unit + time FE
    sigma2 = float(np.sum(resid**2) / max(n - k, 1))
    se = float(np.sqrt(sigma2 / dd))

    return {
        "estimate": beta,
        "se": se,
        "n_obs": n,
        "n_units": int(data[unit_id].nunique()),
    }


def callaway_santanna_att(
    df: pd.DataFrame,
    outcome: str,
    cohort: str,
    time_id: str,
    unit_id: str,
    control_group: str = "never_treated",
) -> pd.DataFrame:
    """Compute group-time average treatment effects (ATT(g,t)).

    This is a simplified implementation of the Callaway-Sant'Anna (2021)
    estimator for staggered DiD. Each cohort g is compared to the specified
    control group in each post-treatment period.

    Args:
        df: Panel DataFrame.
        outcome: Outcome column name.
        cohort: Column indicating the first treated period (0 or NaN for never-treated).
        time_id: Time column name.
        unit_id: Unit column name.
        control_group: Either ``"never_treated"`` or ``"not_yet_treated"``.

    Returns:
        DataFrame with columns ``group``, ``time``, ``att``, ``n_treated``,
        ``n_control``.

    Example:
        >>> import pandas as pd, numpy as np
        >>> rng = np.random.default_rng(7)
        >>> df = pd.DataFrame({
        ...     "unit": np.repeat(np.arange(30), 5),
        ...     "time": np.tile(np.arange(5), 30),
        ...     "cohort": np.repeat(
        ...         np.array([2]*10 + [3]*10 + [np.nan]*10), 5),
        ...     "y": rng.normal(0, 1, 150),
        ... })
        >>> result = callaway_santanna_att(df, "y", "cohort", "time", "unit")
        >>> isinstance(result, pd.DataFrame)
        True
    """
    records = []
    cohorts = sorted(c for c in df[cohort].dropna().unique() if not np.isnan(c))

    for g in cohorts:
        treated_units = df.loc[df[cohort] == g, unit_id].unique()
        if control_group == "never_treated":
            ctrl_units = df.loc[df[cohort].isna(), unit_id].unique()
        else:
            ctrl_units = df.loc[
                df[cohort].isna() | (df[cohort] > g), unit_id
            ].unique()

        pre_period = g - 1
        post_periods = sorted(t for t in df[time_id].unique() if t >= g)

        for t in post_periods:
            y_treat_post = df.loc[
                (df[unit_id].isin(treated_units)) & (df[time_id] == t), outcome
            ].mean()
            y_treat_pre = df.loc[
                (df[unit_id].isin(treated_units)) & (df[time_id] == pre_period), outcome
            ].mean()
            y_ctrl_post = df.loc[
                (df[unit_id].isin(ctrl_units)) & (df[time_id] == t), outcome
            ].mean()
            y_ctrl_pre = df.loc[
                (df[unit_id].isin(ctrl_units)) & (df[time_id] == pre_period), outcome
            ].mean()

            att = (y_treat_post - y_treat_pre) - (y_ctrl_post - y_ctrl_pre)
            records.append(
                {
                    "group": g,
                    "time": t,
                    "att": att,
                    "n_treated": len(treated_units),
                    "n_control": len(ctrl_units),
                }
            )

    return pd.DataFrame(records)
