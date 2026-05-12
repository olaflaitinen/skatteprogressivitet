# Quickstart

This page walks through a five-minute tour of the main features.

## 1. Validate the legislation ledger

```bash
skatteprogressivitet validate-legislation --all
```

Expected output:
```
Simulating year 2025 ...
1991: OK  (kommunal_rate=0.3100, IBB=32200)
...
2025: OK  (kommunal_rate=0.3240, IBB=74300)
7 file(s) valid.
```

## 2. Compute progressivity indices for 2025

```bash
skatteprogressivitet progressivity --year 2025 --indices kakwani,suits,gini
```

## 3. Run a counterfactual scenario

```bash
skatteprogressivitet scenario data/scenarios/raise-brytpunkt.yaml --year 2025
```

## 4. Full pipeline via Python

```python
from skatteprogressivitet import Simulator, Config

config = Config(baseline_year=2025, behavioural="full")
sim = Simulator(config=config)

taxpayers = [
    {"labour_income": 300_000, "capital_income": 0, "age": 35, "self_employed": False},
    {"labour_income": 700_000, "capital_income": 50_000, "age": 50, "self_employed": False},
]

result = sim.run(taxpayers)
print(result.dataframe)
```

## 5. Generate report figures

```bash
skatteprogressivitet report --year 2025 --output-dir reports/
```

Figures are written to `reports/figures/`.
