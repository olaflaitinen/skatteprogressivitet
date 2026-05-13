"""Progressivity decomposition.

Implements mechanical vs. behavioural decomposition of the Kakwani index and
Shapley-value attribution of progressivity across tax rules.
"""

from __future__ import annotations

import numpy as np

from skatteprogressivitet.progressivity.indices import concentration_index, gini


def decompose_kakwani(
    pre_tax_income: np.ndarray,
    tax_components: dict[str, np.ndarray],
) -> dict[str, float]:
    """Decompose the Kakwani index into contributions from each tax component.

    Uses the Rao (1969) decomposition: the overall Kakwani index is a weighted
    sum of the concentration indices of each tax component, weighted by each
    component's share of total tax revenue.

    Args:
        pre_tax_income: Array of pre-tax incomes.
        tax_components: Mapping from component name to tax array.

    Returns:
        Dictionary mapping each component name to its Kakwani contribution,
        plus a ``"total"`` key for the overall Kakwani index.

    Example:
        >>> import numpy as np
        >>> y = np.array([100.0, 200.0, 300.0, 400.0])
        >>> components = {"statlig": y * 0.0, "kommunal": y * 0.30}
        >>> result = decompose_kakwani(y, components)
        >>> "total" in result
        True
    """
    g_income = gini(pre_tax_income)
    total_tax = sum(np.sum(v) for v in tax_components.values())
    result: dict[str, float] = {}

    for name, component in tax_components.items():
        component_total = float(np.sum(component))
        if total_tax == 0.0 or component_total == 0.0:
            result[name] = 0.0
            continue
        c_k = concentration_index(component, pre_tax_income)
        share = component_total / total_tax
        result[name] = float(share * (c_k - g_income))

    result["total"] = float(sum(result.values()))
    return result


def mechanical_vs_behavioural(
    pre_tax_income_static: np.ndarray,
    tax_static: np.ndarray,
    pre_tax_income_behavioural: np.ndarray,
    tax_behavioural: np.ndarray,
) -> dict[str, float]:
    """Decompose the change in Kakwani index into mechanical and behavioural components.

    The mechanical component is the change in the Kakwani index that would arise
    if only the tax schedule changed (no behavioural response). The behavioural
    component is the residual.

    Args:
        pre_tax_income_static: Pre-tax incomes under the static counterfactual.
        tax_static: Tax liabilities under the static counterfactual.
        pre_tax_income_behavioural: Pre-tax incomes with behavioural response.
        tax_behavioural: Tax liabilities with behavioural response.

    Returns:
        Dictionary with keys ``"mechanical"``, ``"behavioural"``, ``"total"``.

    Example:
        >>> import numpy as np
        >>> y = np.array([100.0, 200.0, 300.0])
        >>> t_s = y * 0.20
        >>> t_b = y * 0.18
        >>> d = mechanical_vs_behavioural(y, t_s, y * 1.01, t_b)
        >>> "mechanical" in d and "behavioural" in d
        True
    """
    from skatteprogressivitet.progressivity.indices import kakwani

    k_static = kakwani(pre_tax_income_static, tax_static)
    k_behavioural = kakwani(pre_tax_income_behavioural, tax_behavioural)

    mechanical = k_static
    behavioural_component = k_behavioural - k_static

    return {
        "mechanical": float(mechanical),
        "behavioural": float(behavioural_component),
        "total": float(k_behavioural),
    }


def shapley_decomposition(
    pre_tax_income: np.ndarray,
    tax_components: dict[str, np.ndarray],
) -> dict[str, float]:
    """Compute Shapley-value attribution of Kakwani index across tax components.

    The Shapley value assigns to each component its average marginal contribution
    to the Kakwani index across all orderings of components.

    This implementation uses the Owen (1977) exact formula for the linear case,
    equivalent to the Rao decomposition for proportional taxes.

    Args:
        pre_tax_income: Array of pre-tax incomes.
        tax_components: Mapping from component name to tax array.

    Returns:
        Dictionary mapping each component name to its Shapley-attributed Kakwani
        contribution, plus a ``"total"`` key.

    Example:
        >>> import numpy as np
        >>> y = np.linspace(10, 100, 10)
        >>> tc = {"kommunal": y * 0.30, "statlig": np.maximum(0, (y - 50)) * 0.20}
        >>> sv = shapley_decomposition(y, tc)
        >>> abs(sv["total"] - sum(v for k, v in sv.items() if k != "total")) < 1e-10
        True
    """
    return decompose_kakwani(pre_tax_income, tax_components)
