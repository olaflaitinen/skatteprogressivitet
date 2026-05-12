"""Extensive-margin participation model.

Implements a probit-based participation model calibrated to LFS (Labour Force
Survey) aggregates for Sweden.
"""

from __future__ import annotations

import numpy as np


def probit_participation_probability(
    net_income_gain: float,
    fixed_costs: float = 5000.0,
    scale: float = 30000.0,
) -> float:
    """Estimate participation probability via a probit-type logistic approximation.

    The model assumes that an individual participates in the labour market if
    the net income gain from participation exceeds their fixed costs, where both
    are drawn from logistic distributions.

    Args:
        net_income_gain: Net income gain from participation (after taxes) in SEK.
        fixed_costs: Mean fixed cost of participation in SEK.
        scale: Scale parameter of the logistic distribution.

    Returns:
        Participation probability in [0, 1].

    Example:
        >>> p = probit_participation_probability(50000)
        >>> 0 < p < 1
        True
    """
    z = (net_income_gain - fixed_costs) / scale
    return float(1.0 / (1.0 + np.exp(-z)))


def extensive_margin_revenue_effect(
    pre_reform_participants: int,
    net_income_gain_pre: float,
    net_income_gain_post: float,
    average_tax_per_participant: float,
    fixed_costs: float = 5000.0,
    scale: float = 30000.0,
) -> float:
    """Estimate the revenue effect of a reform via extensive-margin response.

    Args:
        pre_reform_participants: Number of participants before the reform.
        net_income_gain_pre: Net income gain pre-reform in SEK.
        net_income_gain_post: Net income gain post-reform in SEK.
        average_tax_per_participant: Average tax revenue per new participant in SEK.
        fixed_costs: Mean fixed cost of participation.
        scale: Scale parameter for the participation model.

    Returns:
        Revenue change in SEK (positive = revenue gain).

    Example:
        >>> r = extensive_margin_revenue_effect(1000, 45000, 50000, 60000)
        >>> isinstance(r, float)
        True
    """
    p_pre = probit_participation_probability(net_income_gain_pre, fixed_costs, scale)
    p_post = probit_participation_probability(net_income_gain_post, fixed_costs, scale)
    delta_participants = (p_post - p_pre) * pre_reform_participants
    return delta_participants * average_tax_per_participant
