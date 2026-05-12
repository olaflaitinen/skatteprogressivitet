# Counterfactual Scenarios

Scenarios are defined as YAML files in `data/scenarios/` and validated
against the `Scenario` pydantic model at load time.

## Included scenarios

### `raise-brytpunkt`

Raises the statlig inkomstskatt lower threshold (britpunkt) by 10 percent
from its 2025 level (598 500 SEK to 658 350 SEK).

**Motivation**: model the distributional effect of indexing the threshold
to nominal wage growth rather than price growth, consistent with the
Riksdagen motion 2024/25:Sk123 family.

### `recalibrate-jobbskatteavdrag`

Reduces the jobbskatteavdrag uniformly by 20 percent across all income
segments. Models a partial rollback of the earned-income tax credit as
a fiscal consolidation measure, consistent with SOU 2023:65 menu option C.

### `broaden-capital-base`

Raises the flat capital income tax rate from 30 to 35 percent.
Models a partial move toward a comprehensive income tax, consistent with
the low end of the Dahlberg-Sjoblom (2022) capital tax reform proposals.

### `comprehensive-income`

Sets the capital income tax rate equal to the national average municipal
rate (32.4 percent), effectively abolishing the dual-income tax structure
introduced in 1991.

## Running a scenario

```bash
skatteprogressivitet scenario data/scenarios/raise-brytpunkt.yaml
```

## Writing a custom scenario

Create a YAML file following this schema:

```yaml
scenario_id: "my-scenario"
description: "Description of the reform."
baseline_year: 2025
behavioural: "full"
overrides:
  - path: "statlig_skatt.brackets.1.lower"
    value: 650000.0
    notes: "Raise the britpunkt."
```

The `path` field uses dot notation to address nested fields in the
`Legislation` pydantic model.
