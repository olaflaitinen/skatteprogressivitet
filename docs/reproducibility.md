# Reproducibility

## Seeds

All randomness in Skatteprogressivitet flows through the three canonical seeds:

| Constant | Value | Purpose |
|----------|-------|---------|
| `SYNTHETIC_SEED` | 19960307 | Synthetic data generation |
| `MODEL_SEED` | 20251008 | Global simulation seed |
| `BOOTSTRAP_SEED` | 7 | Standard error bootstrap |

Child seeds for named sub-tasks are derived deterministically via SHA-256
from the global seed and task namespace (see `skatteprogressivitet.seeds`).

## Floating-point determinism

All array reductions use left-to-right summation over deterministically
sorted arrays. NumPy operations use `np.random.default_rng` (PCG64) seeded
from the derived seeds. Polars operations are single-threaded in CI.

Known platform-specific non-determinism:

- `np.polyfit` may differ at the last ULP between macOS (Accelerate) and
  Linux (OpenBLAS). The bunching estimator uses `np.polyfit` internally;
  results may differ at the 1e-12 level across platforms.

## Locked dependencies

`uv.lock` pins every transitive dependency. Run `uv sync` to reproduce
the exact environment.

## Verification

```bash
# Run all tests and check against golden records
make test
skatteprogressivitet repro
```

## Archival

Each release is deposited to Zenodo with a DOI. The `CITATION.cff` and
`.zenodo.json` at the repository root contain the full deposition metadata.
