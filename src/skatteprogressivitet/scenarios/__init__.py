"""Scenarios sub-package for Skatteprogressivitet."""

from skatteprogressivitet.scenarios.loader import Scenario, load_scenario
from skatteprogressivitet.scenarios.runner import ScenarioResult, run_scenario

__all__ = ["Scenario", "ScenarioResult", "load_scenario", "run_scenario"]
