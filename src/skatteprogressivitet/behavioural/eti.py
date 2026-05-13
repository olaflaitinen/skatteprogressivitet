"""Elasticity-of-taxable-income (ETI) module.

Implements intensive-margin income responses for individual taxpayers using a
constant-elasticity specification calibrated to the Swedish reform literature.
"""

from __future__ import annotations

from typing import Any


class ETIResponse:
    """ETI-based income response model.

    Attributes:
        eti_intensive: Intensive-margin elasticity of taxable income.
        eti_extensive: Extensive-margin participation elasticity.
    """

    def __init__(
        self,
        eti_intensive: float = 0.3,
        eti_extensive: float = 0.1,
    ) -> None:
        """Initialise the ETIResponse model.

        Args:
            eti_intensive: Intensive-margin ETI. Default 0.3, consistent with
                Blomquist and Selin (2010) and Gelber (2014) for Sweden.
            eti_extensive: Extensive-margin participation elasticity. Default 0.1,
                consistent with Eissa and Liebman (1996) adapted for Sweden.
        """
        if eti_intensive < 0:
            raise ValueError("eti_intensive must be non-negative.")
        if eti_extensive < 0:
            raise ValueError("eti_extensive must be non-negative.")
        self.eti_intensive = eti_intensive
        self.eti_extensive = eti_extensive

    def marginal_response(
        self,
        taxpayer: dict[str, Any],
        marginal_rate: float,
        baseline_marginal_rate: float,
    ) -> float:
        """Compute the behavioural income response to a change in the marginal rate.

        Uses the constant-elasticity specification:

        ``dlogY = -eti * dlog(1 - t)``

        where ``t`` is the marginal tax rate and ``Y`` is taxable income.

        If marginal rates are unchanged (``baseline_marginal_rate == marginal_rate``),
        no response is applied.

        Args:
            taxpayer: Dictionary with at least ``labour_income`` (float).
            marginal_rate: New marginal tax rate (post-reform).
            baseline_marginal_rate: Baseline marginal tax rate (pre-reform).

        Returns:
            Adjusted labour income in SEK.

        Example:
            >>> eti = ETIResponse(eti_intensive=0.3)
            >>> tp = {"labour_income": 500000}
            >>> y = eti.marginal_response(tp, 0.55, 0.57)
            >>> y > 500000
            True
        """
        base_income = float(taxpayer.get("labour_income", 0))
        if base_income <= 0:
            return base_income

        ntr_new = max(1e-6, 1.0 - marginal_rate)
        ntr_base = max(1e-6, 1.0 - baseline_marginal_rate)

        if abs(ntr_new - ntr_base) < 1e-10:
            return base_income

        log_response = self.eti_intensive * (ntr_new / ntr_base - 1.0)
        return max(0.0, base_income * (1.0 + log_response))

    def participation_response(
        self,
        participation_probability: float,
        net_income_gain: float,
        mean_net_income_gain: float,
    ) -> float:
        """Compute the extensive-margin participation probability response.

        Args:
            participation_probability: Baseline participation probability in [0, 1].
            net_income_gain: Net income gain from participation in SEK.
            mean_net_income_gain: Mean net income gain in the reference group.

        Returns:
            Adjusted participation probability in [0, 1].

        Example:
            >>> eti = ETIResponse(eti_extensive=0.1)
            >>> p = eti.participation_response(0.85, 50000, 45000)
            >>> 0 <= p <= 1
            True
        """
        if mean_net_income_gain <= 0:
            return participation_probability
        elasticity_adjustment = self.eti_extensive * (net_income_gain / mean_net_income_gain - 1.0)
        return float(min(1.0, max(0.0, participation_probability * (1.0 + elasticity_adjustment))))
