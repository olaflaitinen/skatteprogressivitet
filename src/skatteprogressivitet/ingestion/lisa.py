"""LISA panel data ingestion.

Provides readers for the SCB LISA administrative panel (in the secure
environment) and a deterministic synthetic fixture generator for development
and testing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import polars as pl

if TYPE_CHECKING:
    import pathlib

LISA_SCHEMA: dict[str, type] = {
    "person_id": str,
    "year": int,
    "labour_income": float,
    "capital_income": float,
    "age": int,
    "sex": int,
    "education_level": int,
    "sector": str,
    "region": str,
    "self_employed": bool,
    "n_children": int,
    "n_adults_household": int,
}


def read_lisa(path: pathlib.Path) -> pl.DataFrame:
    """Read a LISA-format Parquet file.

    In the secure environment this reads the real LISA panel. In development
    it reads the synthetic fixture.

    Args:
        path: Path to the Parquet file.

    Returns:
        Polars DataFrame with LISA schema columns.

    Raises:
        FileNotFoundError: If the file does not exist.

    Example:
        >>> from skatteprogressivitet.paths import SYNTHETIC_ROOT
        >>> df = read_lisa(SYNTHETIC_ROOT / "lisa_like.parquet")
        >>> "labour_income" in df.columns
        True
    """
    if not path.exists():
        raise FileNotFoundError(f"LISA file not found: {path}")
    return pl.read_parquet(str(path))


def synthetic_lisa(
    n: int = 50_000,
    years: list[int] | None = None,
    seed: int = 19960307,
) -> pl.DataFrame:
    """Generate a deterministic synthetic LISA-like panel.

    The synthetic data mimics the column schema and approximate statistical
    properties of the real LISA panel (lognormal labour income, age
    distribution, sector mix) but contains no real personal data.

    Args:
        n: Number of individuals (cross-sectional). Default 50 000.
        years: List of years to generate. Defaults to 2015-2024.
        seed: Random seed. Default SYNTHETIC_SEED (19960307).

    Returns:
        Polars DataFrame with the LISA schema.

    Example:
        >>> df = synthetic_lisa(n=100, years=[2025], seed=19960307)
        >>> len(df)
        100
        >>> "labour_income" in df.columns
        True
    """
    _years = years or list(range(2015, 2025))
    rng = np.random.default_rng(seed)

    rows = []
    for year in _years:
        person_ids = [f"SYN{i:07d}" for i in range(n)]
        ages = rng.integers(18, 70, size=n)
        sex = rng.integers(0, 2, size=n)
        edu = rng.integers(1, 5, size=n)
        sector = rng.choice(["private", "public", "self"], size=n, p=[0.65, 0.30, 0.05])
        region = rng.choice(
            ["Stockholm", "Gothenburg", "Malmö", "Other"], size=n, p=[0.25, 0.10, 0.08, 0.57]
        )
        self_emp = sector == "self"
        n_children = rng.integers(0, 4, size=n)
        n_adults = rng.integers(1, 3, size=n)

        labour_raw = np.exp(rng.normal(12.5, 0.7, size=n))
        labour_income = np.where(ages < 22, labour_raw * 0.3, labour_raw)
        labour_income = np.where(self_emp, labour_income * 0.9, labour_income)

        capital_income = np.where(
            rng.random(size=n) < 0.15,
            np.abs(rng.normal(50000, 80000, size=n)),
            0.0,
        )

        rows.append(
            pl.DataFrame(
                {
                    "person_id": person_ids,
                    "year": np.full(n, year, dtype=np.int32),
                    "labour_income": labour_income.astype(np.float64),
                    "capital_income": capital_income.astype(np.float64),
                    "age": ages.astype(np.int32),
                    "sex": sex.astype(np.int32),
                    "education_level": edu.astype(np.int32),
                    "sector": sector.tolist(),
                    "region": region.tolist(),
                    "self_employed": self_emp.tolist(),
                    "n_children": n_children.astype(np.int32),
                    "n_adults_household": n_adults.astype(np.int32),
                }
            )
        )

    return pl.concat(rows)
