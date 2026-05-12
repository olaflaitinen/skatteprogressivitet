# Golden Records

This directory stores SHA-256 checksums of key simulation outputs used
to detect unintended regressions in numerical results.

Golden records are generated on the reference platform (Linux x86-64,
Python 3.12) using the canonical seeds:
- `SYNTHETIC_SEED` = 19960307
- `MODEL_SEED` = 20251008

## Format

Each `.json` file contains:
```json
{
  "description": "...",
  "year": 2025,
  "seed": 20251008,
  "n_taxpayers": 50000,
  "checksum": "<sha256 of the serialised output>",
  "generated": "ISO-8601 date"
}
```

## Updating golden records

Golden records must be updated intentionally when:
- Legislation YAML files change
- Tax rule implementations change
- Seeds change

Update procedure:
```bash
uv run python scripts/update_golden_records.py
```

Any accidental numerical change will cause `test_determinism.py` to fail.
