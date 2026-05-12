"""Legislation sub-package for Skatteprogressivitet."""

from skatteprogressivitet.legislation.ledger import LegislationLedger, TaxOutcome
from skatteprogressivitet.legislation.loader import load_all, load_year
from skatteprogressivitet.legislation.schema import Legislation

__all__ = [
    "Legislation",
    "LegislationLedger",
    "TaxOutcome",
    "load_all",
    "load_year",
]
