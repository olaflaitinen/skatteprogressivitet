"""Pipeline runner composing the full end-to-end simulation workflow.

Composes: ingest -> legislation -> simulate -> behavioural -> progressivity
-> scenarios -> report.
"""

from __future__ import annotations

import dataclasses
from typing import Any

import polars as pl

from skatteprogressivitet.config import Config
from skatteprogressivitet.pipelines.dag import DAG, Task


@dataclasses.dataclass
class PipelineResult:
    """Container for a full pipeline run.

    Attributes:
        config: Runtime configuration used.
        simulation_result: Output from the simulator.
        progressivity: Dictionary of progressivity index values.
        scenario_results: Mapping from scenario_id to ScenarioResult.
    """

    config: Config
    simulation_result: Any
    progressivity: dict[str, float]
    scenario_results: dict[str, Any]


class Pipeline:
    """Full end-to-end simulation pipeline.

    Attributes:
        config: Runtime configuration.
    """

    def __init__(self, config: Config | None = None) -> None:
        """Initialise the Pipeline.

        Args:
            config: Runtime configuration. Defaults to ``Config()``.
        """
        self.config: Config = config or Config()

    def run(
        self,
        taxpayers: list[dict[str, Any]] | pl.DataFrame | None = None,
        scenarios: list[str] | None = None,
    ) -> PipelineResult:
        """Execute the full pipeline.

        Args:
            taxpayers: Taxpayer population. If ``None``, loads the synthetic fixture.
            scenarios: List of scenario IDs to run. If ``None``, runs all.

        Returns:
            A :class:`PipelineResult` with all outputs.

        Example:
            >>> pipe = Pipeline()
            >>> result = pipe.run(taxpayers=[
            ...     {"labour_income": 300000, "capital_income": 0,
            ...      "age": 35, "self_employed": False}
            ... ])
            >>> "kakwani" in result.progressivity
            True
        """
        from skatteprogressivitet.simulator.engine import Simulator
        from skatteprogressivitet.progressivity.indices import (
            kakwani, suits, gini, theil, atkinson,
        )
        from skatteprogressivitet.scenarios.loader import load_all_scenarios
        from skatteprogressivitet.scenarios.runner import run_scenario
        import numpy as np

        _taxpayers = taxpayers or self._load_synthetic()

        sim = Simulator(config=self.config)
        sim_result = sim.run(_taxpayers, year=self.config.baseline_year)

        df = sim_result.dataframe
        y = df["gross_income"].to_numpy()
        t = df["total_tax"].to_numpy()
        y_post = y - t

        prog: dict[str, float] = {
            "kakwani": float(kakwani(y, t)),
            "suits": float(suits(y, t)),
            "gini_pre": float(gini(y)),
            "gini_post": float(gini(y_post)),
            "theil": float(theil(y)),
            "atkinson_05": float(atkinson(y, 0.5)),
        }

        all_scenarios = load_all_scenarios()
        if scenarios is not None:
            all_scenarios = {k: v for k, v in all_scenarios.items() if k in scenarios}

        scen_results: dict[str, Any] = {}
        for sid, scen in all_scenarios.items():
            scen_results[sid] = run_scenario(scen, _taxpayers, config=self.config)

        return PipelineResult(
            config=self.config,
            simulation_result=sim_result,
            progressivity=prog,
            scenario_results=scen_results,
        )

    def _load_synthetic(self) -> list[dict[str, Any]]:
        """Load the synthetic fixture as a list of taxpayer dicts.

        Returns:
            List of taxpayer dictionaries.
        """
        from skatteprogressivitet.paths import SYNTHETIC_ROOT
        import pyarrow.parquet as pq

        path = SYNTHETIC_ROOT / "lisa_like.parquet"
        if path.exists():
            tbl = pq.read_table(str(path))
            return tbl.to_pydict_list() if hasattr(tbl, "to_pydict_list") else (
                pl.from_arrow(tbl).to_dicts()
            )
        return [
            {"labour_income": 300000.0, "capital_income": 0.0, "age": 40, "self_employed": False}
        ]
