"""Tax register (IoT) ingestion.

Provides readers for the SCB IoT (Inkomst- och taxeringsregistret) and a
deterministic synthetic tax-register fixture generator.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import polars as pl

if TYPE_CHECKING:
    import pathlib


def read_tax_register(path: pathlib.Path) -> pl.DataFrame:
    """Read a tax-register-format Parquet file.

    Args:
        path: Path to the Parquet file.

    Returns:
        Polars DataFrame with tax register columns.

    Raises:
        FileNotFoundError: If the file does not exist.

    Example:
        >>> from skatteprogressivitet.paths import SYNTHETIC_ROOT
        >>> df = read_tax_register(SYNTHETIC_ROOT / "tax_register_like.parquet")
        >>> "taxable_income" in df.columns
        True
    """
    if not path.exists():
        raise FileNotFoundError(f"Tax register file not found: {path}")
    return pl.read_parquet(str(path))


def synthetic_tax_register(
    n: int = 50_000,
    years: list[int] | None = None,
    seed: int = 19960307,
) -> pl.DataFrame:
    """Generate a deterministic synthetic tax-register-like panel.

    Args:
        n: Number of individuals. Default 50 000.
        years: List of years. Defaults to 2015-2024.
        seed: Random seed. Default SYNTHETIC_SEED (19960307).

    Returns:
        Polars DataFrame with tax register schema.

    Example:
        >>> df = synthetic_tax_register(n=100, years=[2025], seed=19960307)
        >>> "taxable_income" in df.columns
        True
    """
    _years = years or list(range(2015, 2025))
    rng = np.random.default_rng(seed + 1)

    rows = []
    for year in _years:
        person_ids = [f"SYN{i:07d}" for i in range(n)]
        labour = np.exp(rng.normal(12.5, 0.7, size=n))
        capital = np.where(rng.random(size=n) < 0.15, np.abs(rng.normal(50000, 80000, size=n)), 0.0)
        deductions = np.abs(rng.normal(5000, 8000, size=n))
        taxable = np.maximum(0.0, labour - deductions)
        assessed = taxable + capital

        rows.append(
            pl.DataFrame(
                {
                    "person_id": person_ids,
                    "year": np.full(n, year, dtype=np.int32),
                    "labour_income": labour.astype(np.float64),
                    "capital_income": capital.astype(np.float64),
                    "deductions": deductions.astype(np.float64),
                    "taxable_income": taxable.astype(np.float64),
                    "assessed_income": assessed.astype(np.float64),
                }
            )
        )

    return pl.concat(rows)
