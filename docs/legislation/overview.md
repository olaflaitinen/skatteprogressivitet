# Legislation Ledger Overview

## Structure

The legislative-parameter ledger consists of per-year YAML files in
`data/legislation/`, one for each major reform year. Each file is
validated against `data/legislation/schema.json` (JSON Schema 2020-12)
and the pydantic `Legislation` model.

## Reform years

| Year | Key reform | SFS reference |
|------|-----------|---------------|
| 1991 | Den stora skattereformen (dual income tax) | SFS 1990:651 |
| 1995 | State tax rate raised to 25%; budget consolidation | SFS 1994:1744 |
| 2000 | Inkomstskattelagen (IL); varnskatt introduced | SFS 1999:1230 |
| 2007 | Jobbskatteavdrag step 1 | SFS 2006:1340 |
| 2015 | Youth payroll-tax reduction phased out | SFS 2014:1468 |
| 2020 | Varnskatt abolished | SFS 2019:835 |
| 2025 | Jobbskatteavdrag expansion; updated thresholds | SFS 2024:875 |

## Adding a new year

1. Create `data/legislation/<year>.yaml` following the existing format.
2. Add the `# SFS ...` and `# Prop. ...` header comments.
3. Validate: `skatteprogressivitet validate-legislation --year <year>`.
4. Update `docs/legislation/overview.md`.
5. Sign and push with DCO sign-off per `CONTRIBUTING.md`.

## Accessing parameters programmatically

```python
from skatteprogressivitet.legislation.loader import load_year

leg = load_year(2025)
print(leg.statlig_skatt.brackets)
print(leg.jobbskatteavdrag.enabled)
```
