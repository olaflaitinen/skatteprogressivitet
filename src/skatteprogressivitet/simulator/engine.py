"""Microsimulation engine.

The :class:`Simulator` class orchestrates the full static simulation pipeline:
loading the legislation, applying tax rules, optionally applying behavioural
responses, and returning a :class:`SimulationResult`.

All floating-point reductions over arrays are performed left-to-right in
deterministic order. Any platform-dependent non-determinism is documented in
docs/reproducibility.md.
"""

from __future__ import annotations

import dataclasses
from typing import Any

import numpy as np
import polars as pl

from skatteprogressivitet.config import Config
from skatteprogressivitet.legislation.ledger import LegislationLedger, TaxOutcome


@dataclasses.dataclass
class SimulationResult:
    """Container for one simulation run's output.

    Attributes:
        year: Legislation year used.
        n_taxpayers: Number of taxpayer records processed.
        outcomes: List of :class:`TaxOutcome` objects, one per taxpayer.
        dataframe: Polars DataFrame with all outcomes as columns.
    """

    year: int
    n_taxpayers: int
    outcomes: list[TaxOutcome]
    dataframe: pl.DataFrame


class Simulator:
    """Static (and optionally behavioural) microsimulator.

    Attributes:
        config: Runtime configuration.
        ledger: Loaded legislation ledger.
    """

    def __init__(self, config: Config | None = None) -> None:
        """Initialise the Simulator.

        Args:
            config: Runtime configuration. Defaults to ``Config()``.
        """
        self.config: Config = config or Config()
        self.ledger: LegislationLedger = LegislationLedger()

    def run(
        self,
        taxpayers: list[dict[str, Any]] | pl.DataFrame,
        year: int | None = None,
        behavioural: str | None = None,
    ) -> SimulationResult:
        """Run the simulation over a population of taxpayers.

        Args:
            taxpayers: Either a list of taxpayer dicts or a polars DataFrame
                with columns ``labour_income``, ``capital_income``, ``age``,
                ``self_employed``.
            year: Legislation year. Defaults to ``config.baseline_year``.
            behavioural: Behavioural mode override. Defaults to ``config.behavioural``.

        Returns:
            A :class:`SimulationResult` with all outcomes.

        Example:
            >>> sim = Simulator()
            >>> tps = [{"labour_income": 300000, "capital_income": 0,
            ...          "age": 40, "self_employed": False}]
            >>> result = sim.run(tps, year=2025)
            >>> result.n_taxpayers
            1
        """
        _year = year or self.config.baseline_year
        _behavioural = behavioural or self.config.behavioural

        records = self._to_records(taxpayers)
        leg = self.ledger.get(_year)

        outcomes: list[TaxOutcome] = []
        for tp in records:
            outcome = self.ledger.apply(_year, tp)
            outcomes.append(outcome)

        if _behavioural in ("eti", "full"):
            outcomes = self._apply_eti(outcomes, records, leg, _behavioural)

        df = self._to_dataframe(outcomes)

        return SimulationResult(
            year=_year,
            n_taxpayers=len(records),
            outcomes=outcomes,
            dataframe=df,
        )

    def _to_records(self, taxpayers: list[dict[str, Any]] | pl.DataFrame) -> list[dict[str, Any]]:
        """Convert input to a list of taxpayer dicts.

        Args:
            taxpayers: Input data.

        Returns:
            List of taxpayer dictionaries.
        """
        if isinstance(taxpayers, pl.DataFrame):
            return taxpayers.to_dicts()
        return list(taxpayers)

    def _apply_eti(
        self,
        outcomes: list[TaxOutcome],
        records: list[dict[str, Any]],
        leg: Any,
        mode: str,
    ) -> list[TaxOutcome]:
        """Apply ETI-based behavioural income responses.

        Args:
            outcomes: Static outcomes list.
            records: Original taxpayer records.
            leg: Legislation for the year.
            mode: ``"eti"`` or ``"full"``.

        Returns:
            Updated outcomes with behavioural responses applied.
        """
        from skatteprogressivitet.behavioural.eti import ETIResponse

        eti = ETIResponse(
            eti_intensive=self.config.eti_intensive,
            eti_extensive=self.config.eti_extensive,
        )
        adjusted: list[TaxOutcome] = []
        for tp, outcome in zip(records, outcomes, strict=False):
            new_income = eti.marginal_response(
                taxpayer=tp,
                marginal_rate=outcome.effective_marginal_rate,
                baseline_marginal_rate=outcome.effective_marginal_rate,
            )
            if new_income != float(tp.get("labour_income", 0)):
                new_tp = dict(tp)
                new_tp["labour_income"] = new_income
                adjusted.append(self.ledger.apply(leg.year, new_tp))
            else:
                adjusted.append(outcome)
        return adjusted

    def _to_dataframe(self, outcomes: list[TaxOutcome]) -> pl.DataFrame:
        """Convert a list of TaxOutcome objects to a Polars DataFrame.

        Args:
            outcomes: List of outcomes.

        Returns:
            Polars DataFrame with one row per taxpayer.
        """
        rows = [o.to_dict() for o in outcomes]
        if not rows:
            return pl.DataFrame()
        # Deterministic column ordering
        cols = list(rows[0].keys())
        data: dict[str, list[float]] = {c: [r[c] for r in rows] for c in cols}
        return pl.DataFrame({c: np.array(v, dtype=np.float64) for c, v in data.items()})
