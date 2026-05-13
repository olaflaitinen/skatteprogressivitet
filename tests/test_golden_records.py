"""Golden-record regression tests.

Compares simulation outputs against stored SHA-256 checksums in
``tests/golden/``. Fails if the checksum does not match, alerting to
unintended numerical changes.

Mark: ``--mark golden`` to run only these tests.
"""

from __future__ import annotations

import hashlib
import json
import pathlib

import pytest

from skatteprogressivitet.config import Config
from skatteprogressivitet.ingestion.lisa import synthetic_lisa
from skatteprogressivitet.seeds import MODEL_SEED, SYNTHETIC_SEED
from skatteprogressivitet.simulator.engine import Simulator

GOLDEN_DIR = pathlib.Path(__file__).parent / "golden"


def _sha256_dataframe_bytes(df) -> str:
    buf = df.write_ipc(None)
    return hashlib.sha256(buf.read()).hexdigest()


def _load_record(year: int) -> dict | None:
    p = GOLDEN_DIR / f"sim_{year}.json"
    if not p.exists():
        return None
    with p.open(encoding="utf-8") as fh:
        return json.load(fh)


@pytest.mark.golden
@pytest.mark.parametrize("year", [1991, 2007, 2020, 2025])
def test_golden_simulation(year: int) -> None:
    record = _load_record(year)
    if record is None:
        pytest.skip(f"No golden record for year {year}; run update_golden_records.py first.")

    df_lisa = synthetic_lisa(n=5_000, years=[year], seed=SYNTHETIC_SEED)
    tps = df_lisa.to_dicts()

    config = Config(baseline_year=year, behavioural="none", seed=MODEL_SEED)  # type: ignore[call-arg]
    sim = Simulator(config=config)
    result = sim.run(tps, year=year, behavioural="none")

    checksum = _sha256_dataframe_bytes(result.dataframe)
    assert checksum == record["checksum"], (
        f"Golden record mismatch for year {year}.\n"
        f"  Expected: {record['checksum']}\n"
        f"  Got:      {checksum}\n"
        "Run scripts/update_golden_records.py if the change is intentional."
    )
