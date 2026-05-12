"""Skatteprogressivitet: static and behavioural microsimulator for Swedish tax progressivity.

This package implements the statutory rules governing the Swedish tax-and-transfer
system and computes effective marginal and average tax rates, progressivity indices,
and counterfactual policy reforms.

Licence: EUPL-1.2
Author: Gustav Olaf Yunus Laitinen-Fredriksson Lundström Imanov
ORCID: 0009-0006-5184-0810
Affiliation: Department of Economics, Stockholm University
"""

from __future__ import annotations

from skatteprogressivitet._version import __version__
from skatteprogressivitet.config import Config
from skatteprogressivitet.scenarios.loader import Scenario
from skatteprogressivitet.seeds import set_global_seed
from skatteprogressivitet.simulator.engine import Simulator

__author__ = "Gustav Olaf Yunus Laitinen-Fredriksson Lundström Imanov"
__license__ = "EUPL-1.2"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "Config",
    "Scenario",
    "Simulator",
    "set_global_seed",
]
