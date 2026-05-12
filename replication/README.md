# Replication Bundle

## Contents

| File | Purpose |
|------|---------|
| `run_all.sh` | Shell script to reproduce all tables and figures |
| `expected_receipts.json` | SHA-256 hashes of expected output files |
| `host-fingerprint.txt` | Hardware fingerprint at time of reference run |

## Prerequisites

1. Python 3.12 with uv installed.
2. The package installed: `uv sync`.
3. Synthetic data generated: `uv run python scripts/generate_synthetic_data.py`.

## Running

```bash
bash replication/run_all.sh
```

Expected runtime: approximately 5 minutes on a 4-core machine.

## Verifying receipts

```bash
skatteprogressivitet repro
```

## Platform notes

Results are numerically identical on Linux x86-64 (reference platform) and
macOS arm64, except for the bunching estimator output which may differ at the
1e-12 level due to differences in the LAPACK implementation used by NumPy.
