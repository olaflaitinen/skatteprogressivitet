"""LegislationLedger: aggregate access to all reform years.

Provides a single object that holds all loaded :class:`Legislation` instances
and exposes methods to compute tax outcomes for individual taxpayers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from skatteprogressivitet.legislation.loader import load_all

if TYPE_CHECKING:
    import pathlib

    from skatteprogressivitet.legislation.schema import Legislation


class TaxOutcome:
    """Result of applying legislation to a single taxpayer.

    Attributes:
        statlig_skatt: State income tax liability in SEK.
        kommunal_skatt: Municipal income tax liability in SEK.
        kapitalinkomstskatt: Capital income tax liability in SEK.
        arbetsgivaravgift: Employer payroll tax in SEK.
        jobbskatteavdrag: Earned-income tax credit in SEK (negative reduces tax).
        total_tax: Sum of all tax components minus credits.
        effective_average_rate: Total tax divided by gross income.
        effective_marginal_rate: Marginal tax rate at the given income level.
    """

    def __init__(
        self,
        statlig_skatt: float,
        kommunal_skatt: float,
        kapitalinkomstskatt: float,
        arbetsgivaravgift: float,
        jobbskatteavdrag: float,
        gross_income: float,
        marginal_rate: float,
    ) -> None:
        """Initialise a TaxOutcome.

        Args:
            statlig_skatt: State income tax in SEK.
            kommunal_skatt: Municipal income tax in SEK.
            kapitalinkomstskatt: Capital income tax in SEK.
            arbetsgivaravgift: Employer payroll tax in SEK.
            jobbskatteavdrag: EITC credit in SEK (reduces tax when positive).
            gross_income: Gross income in SEK.
            marginal_rate: Effective marginal rate at this income level.
        """
        self.statlig_skatt = statlig_skatt
        self.kommunal_skatt = kommunal_skatt
        self.kapitalinkomstskatt = kapitalinkomstskatt
        self.arbetsgivaravgift = arbetsgivaravgift
        self.jobbskatteavdrag = jobbskatteavdrag
        self.total_tax = statlig_skatt + kommunal_skatt + kapitalinkomstskatt - jobbskatteavdrag
        self.gross_income = gross_income
        self.effective_average_rate = self.total_tax / gross_income if gross_income > 0 else 0.0
        self.effective_marginal_rate = marginal_rate

    def to_dict(self) -> dict[str, float]:
        """Serialise to a plain dictionary.

        Returns:
            Dictionary with all numeric fields.

        Example:
            >>> outcome = TaxOutcome(0, 0, 0, 0, 0, 100000, 0.32)
            >>> "total_tax" in outcome.to_dict()
            True
        """
        return {
            "statlig_skatt": self.statlig_skatt,
            "kommunal_skatt": self.kommunal_skatt,
            "kapitalinkomstskatt": self.kapitalinkomstskatt,
            "arbetsgivaravgift": self.arbetsgivaravgift,
            "jobbskatteavdrag": self.jobbskatteavdrag,
            "total_tax": self.total_tax,
            "gross_income": self.gross_income,
            "effective_average_rate": self.effective_average_rate,
            "effective_marginal_rate": self.effective_marginal_rate,
        }


class LegislationLedger:
    """Aggregate holder for all committed reform-year legislation.

    Attributes:
        years: Sorted list of available reform years.
    """

    def __init__(self, root: pathlib.Path | None = None) -> None:
        """Initialise by loading all YAML files from the legislation root.

        Args:
            root: Optional override for the legislation root directory.
        """
        self._data: dict[int, Legislation] = load_all(root=root)
        self.years: list[int] = sorted(self._data.keys())

    def get(self, year: int) -> Legislation:
        """Return the :class:`Legislation` for a given year.

        Args:
            year: Reform year.

        Returns:
            Validated legislation object.

        Raises:
            KeyError: If the year is not in the ledger.

        Example:
            >>> ledger = LegislationLedger()
            >>> ledger.get(2025).year
            2025
        """
        if year not in self._data:
            raise KeyError(f"No legislation for year {year}. Available: {self.years}")
        return self._data[year]

    def apply(self, year: int, taxpayer: dict[str, Any]) -> TaxOutcome:
        """Compute tax outcome for a taxpayer under the given year's legislation.

        This is a thin dispatch wrapper. Full computation is delegated to the
        individual rule modules in ``skatteprogressivitet.rules``.

        Args:
            year: Legislation year to apply.
            taxpayer: Dictionary with keys ``labour_income``, ``capital_income``,
                ``age``, ``self_employed`` (bool).

        Returns:
            A :class:`TaxOutcome` with all components computed.

        Example:
            >>> ledger = LegislationLedger()
            >>> tp = {"labour_income": 400000, "capital_income": 0, "age": 40,
            ...       "self_employed": False}
            >>> outcome = ledger.apply(2025, tp)
            >>> outcome.kommunal_skatt > 0
            True
        """
        from skatteprogressivitet.rules.personal_income_tax import (
            compute_personal_income_tax,
        )

        leg = self.get(year)
        return compute_personal_income_tax(taxpayer, leg)
