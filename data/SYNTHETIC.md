# Synthetic Data

The `data/synthetic/` directory contains deterministic synthetic fixtures that
mimic the column schema and approximate statistical properties of the Swedish
administrative panel data used in real analyses.

## Files

| File | Description | Rows | Seed |
|------|-------------|------|------|
| `lisa_like.parquet` | Synthetic LISA panel | 50 000 x 35 years | 19960307 |
| `tax_register_like.parquet` | Synthetic IoT panel | 50 000 x 35 years | 19960307 |

## Generating the fixtures

```bash
uv run python scripts/generate_synthetic_data.py
```

## Licence

All files in `data/synthetic/` are dedicated to the public domain under
CC0-1.0. See `data/synthetic/CC0_WAIVER.md`.

## No real data

These files contain no real individuals. The income distributions are
lognormal with parameters calibrated to published SCB aggregate statistics
(Inkomster och skatter, various years). No personnummer or other identifying
information is present.
