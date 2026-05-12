"""Filing-unit construction utilities.

Constructs individual, joint, and household filing units from a polars DataFrame
row or a plain dictionary.
"""

from __future__ import annotations

from typing import Any


class FilingUnit:
    """Represents a single tax-filing unit.

    Attributes:
        unit_id: Unique identifier for the filing unit.
        unit_type: One of ``"individual"``, ``"joint"``, or ``"household"``.
        members: List of member taxpayer dicts.
        aggregated: Aggregated income and demographics dict.
    """

    def __init__(
        self,
        unit_id: str,
        unit_type: str,
        members: list[dict[str, Any]],
    ) -> None:
        """Initialise a FilingUnit.

        Args:
            unit_id: Unique identifier.
            unit_type: Filing unit type.
            members: List of member taxpayer dictionaries.
        """
        self.unit_id = unit_id
        self.unit_type = unit_type
        self.members = members
        self.aggregated = self._aggregate()

    def _aggregate(self) -> dict[str, Any]:
        """Aggregate member-level fields to filing-unit level.

        Returns:
            Dictionary with summed income fields and primary-member demographics.
        """
        total_labour = sum(float(m.get("labour_income", 0)) for m in self.members)
        total_capital = sum(float(m.get("capital_income", 0)) for m in self.members)
        primary = self.members[0] if self.members else {}
        return {
            "labour_income": total_labour,
            "capital_income": total_capital,
            "age": int(primary.get("age", 40)),
            "self_employed": bool(primary.get("self_employed", False)),
            "n_members": len(self.members),
        }


def make_individual_unit(taxpayer: dict[str, Any], uid: str = "") -> FilingUnit:
    """Create an individual filing unit from a single taxpayer dict.

    Args:
        taxpayer: Taxpayer data dictionary.
        uid: Unit identifier.

    Returns:
        A :class:`FilingUnit` with one member.

    Example:
        >>> tp = {"labour_income": 300000, "age": 35, "self_employed": False}
        >>> unit = make_individual_unit(tp, uid="u1")
        >>> unit.unit_type
        'individual'
    """
    return FilingUnit(unit_id=uid, unit_type="individual", members=[taxpayer])
