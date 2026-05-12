"""Generate and persist the synthetic LISA and tax-register fixtures.

Run once at repo setup:
    uv run python scripts/generate_synthetic_data.py

Outputs:
    data/synthetic/lisa_like.parquet
    data/synthetic/tax_register_like.parquet
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from skatteprogressivitet.ingestion.lisa import synthetic_lisa
from skatteprogressivitet.ingestion.tax_registers import synthetic_tax_register
from skatteprogressivitet.seeds import SYNTHETIC_SEED

SYNTHETIC_ROOT = ROOT / "data" / "synthetic"
SYNTHETIC_ROOT.mkdir(parents=True, exist_ok=True)

YEARS = list(range(1991, 2026))


def main() -> None:
    print(f"Generating synthetic LISA panel (seed={SYNTHETIC_SEED})...")
    lisa_df = synthetic_lisa(n=50_000, years=YEARS, seed=SYNTHETIC_SEED)
    out_lisa = SYNTHETIC_ROOT / "lisa_like.parquet"
    lisa_df.write_parquet(str(out_lisa))
    print(f"  Written: {out_lisa} ({len(lisa_df):,} rows)")

    print(f"Generating synthetic tax register (seed={SYNTHETIC_SEED})...")
    tax_df = synthetic_tax_register(n=50_000, years=YEARS, seed=SYNTHETIC_SEED)
    out_tax = SYNTHETIC_ROOT / "tax_register_like.parquet"
    tax_df.write_parquet(str(out_tax))
    print(f"  Written: {out_tax} ({len(tax_df):,} rows)")

    print("Done.")


if __name__ == "__main__":
    main()
