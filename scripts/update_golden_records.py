"""Update golden records after intentional numerical changes.

Run:
    uv run python scripts/update_golden_records.py

This script re-runs the reference simulation, computes SHA-256 checksums of
outputs, and writes them to tests/golden/.

DO NOT run this script unless you have intentionally changed tax rules, seeds,
or legislation files and want to accept the new numerical results.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from skatteprogressivitet.seeds import MODEL_SEED, SYNTHETIC_SEED
from skatteprogressivitet.ingestion.lisa import synthetic_lisa
from skatteprogressivitet.simulator.engine import Simulator
from skatteprogressivitet.config import Config

GOLDEN_DIR = ROOT / "tests" / "golden"
GOLDEN_DIR.mkdir(parents=True, exist_ok=True)


def _sha256_dataframe_bytes(df) -> str:
    """Compute SHA-256 of a Polars DataFrame serialised to IPC bytes."""
    buf = df.write_ipc(None)
    return hashlib.sha256(buf.read()).hexdigest()


def main() -> None:
    print(f"Updating golden records (MODEL_SEED={MODEL_SEED}, SYNTHETIC_SEED={SYNTHETIC_SEED})...")

    df_lisa = synthetic_lisa(n=5_000, years=[2025], seed=SYNTHETIC_SEED)
    tps = df_lisa.to_dicts()

    for year in [1991, 2007, 2020, 2025]:
        config = Config(baseline_year=year, behavioural="none", seed=MODEL_SEED)  # type: ignore[call-arg]
        sim = Simulator(config=config)
        result = sim.run(tps, year=year, behavioural="none")
        checksum = _sha256_dataframe_bytes(result.dataframe)

        record = {
            "description": f"Static simulation year {year}, n=5000, seed={MODEL_SEED}",
            "year": year,
            "seed": MODEL_SEED,
            "n_taxpayers": result.n_taxpayers,
            "checksum": checksum,
            "generated": datetime.now(tz=timezone.utc).isoformat(),
        }
        out = GOLDEN_DIR / f"sim_{year}.json"
        with out.open("w", encoding="utf-8") as fh:
            json.dump(record, fh, indent=2)
        print(f"  Written: {out} (checksum={checksum[:16]}...)")

    print("Done. Commit the updated golden records with a signed DCO commit.")


if __name__ == "__main__":
    main()
