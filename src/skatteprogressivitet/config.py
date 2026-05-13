"""Global configuration model for Skatteprogressivitet.

All runtime parameters are encapsulated in the :class:`Config` pydantic v2 model.
Construct one instance per simulation run and pass it explicitly to subsystems.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

BASELINE_YEARS = Literal[1991, 1995, 2000, 2007, 2015, 2020, 2025]
BEHAVIOURAL_MODE = Literal["none", "eti", "full"]


class Config(BaseModel):
    """Runtime configuration for a Skatteprogressivitet simulation.

    Attributes:
        data_root: Path to the data directory. Defaults to the package data root.
        seed: Global random seed. Defaults to MODEL_SEED (20251008).
        baseline_year: Legislation year to use as the baseline.
        scenario_id: Optional scenario identifier. ``None`` means no counterfactual.
        behavioural: Behavioural response mode.
            ``"none"`` = static; ``"eti"`` = ETI only; ``"full"`` = ETI + income shifting.
        eti_intensive: Intensive-margin elasticity of taxable income.
        eti_extensive: Extensive-margin participation elasticity.
        bootstrap_replications: Number of bootstrap replications for standard errors.
        n_jobs: Number of parallel workers (``-1`` = all available cores).
    """

    data_root: str = ""
    seed: int = Field(default=20251008, ge=0)
    baseline_year: BASELINE_YEARS = 2025
    scenario_id: str | None = None
    behavioural: BEHAVIOURAL_MODE = "full"
    eti_intensive: float = Field(default=0.3, ge=0.0, le=5.0)
    eti_extensive: float = Field(default=0.1, ge=0.0, le=5.0)
    bootstrap_replications: int = Field(default=1000, ge=1)
    n_jobs: int = Field(default=1, ge=-1)

    model_config = {"frozen": True}

    @field_validator("eti_intensive", "eti_extensive")
    @classmethod
    def _non_negative(cls, v: float) -> float:
        """Validate that elasticity parameters are non-negative.

        Args:
            v: Elasticity value.

        Returns:
            Validated elasticity value.
        """
        if v < 0:
            raise ValueError("Elasticity parameters must be non-negative.")
        return v
