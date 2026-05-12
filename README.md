# Skatteprogressivitet

**Static and behavioural microsimulator for Swedish tax progressivity**

[![CI](https://github.com/olaflaitinen/skatteprogressivitet/actions/workflows/ci.yml/badge.svg)](https://github.com/olaflaitinen/skatteprogressivitet/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/olaflaitinen/skatteprogressivitet/branch/main/graph/badge.svg)](https://codecov.io/gh/olaflaitinen/skatteprogressivitet)
[![REUSE compliant](https://api.reuse.software/badge/github.com/olaflaitinen/skatteprogressivitet)](https://api.reuse.software/info/github.com/olaflaitinen/skatteprogressivitet)
[![License: EUPL-1.2](https://img.shields.io/badge/License-EUPL--1.2-blue.svg)](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/olaflaitinen/skatteprogressivitet/badge)](https://securityscorecards.dev/viewer/?uri=github.com/olaflaitinen/skatteprogressivitet)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](https://www.python.org/)
[![OSOR](https://img.shields.io/badge/OSOR-catalogue-orange)](https://joinup.ec.europa.eu/collection/open-source-observatory-osor)

---

## Abstract

Skatteprogressivitet is a static and behavioural microsimulator for the Swedish
tax-and-transfer system, developed at the Department of Economics, Stockholm University.
It implements the statutory rules governing personal income tax (statlig inkomstskatt and
kommunal inkomstskatt), payroll taxes (arbetsgivaravgifter and egenavgifter), capital-income
taxation including the 3:12 schedule for closely held firms (fåmansföretag), social transfers
(sjukpenning, föräldrapenning, arbetslöshetsersättning), housing allowances (bostadsbidrag
and bostadstillägg), and the earned-income tax credit (jobbskatteavdrag), with a versioned
legislative-parameter ledger covering every major reform episode since the 1991 tax reform.

The engine computes effective marginal and average tax rates across the income distribution
and decomposes progressivity through the Kakwani, Suits, and residual-progression indices,
with bootstrap and influence-function standard errors. Behavioural responses are introduced
through a flexible elasticity-of-taxable-income (ETI) module calibrated against
quasi-experimental estimates from the Swedish reform literature, with separate intensive-margin
and extensive-margin parameterisations and bunching-based identification around statutory
bracket thresholds (brytpunkter). Policy counterfactuals are specified as YAML manifests and
run reproducibly against the synthetic fixture, producing publication-quality tables and
figures consistent with Finansdepartementet revenue baselines.

The repository ships only deterministic synthetic fixtures (CC0-1.0) and the legislative-
parameter ledger (EUPL-1.2). No personal data, no real microdata.

---

## Compliance

| Framework | Status | Reference |
|-----------|--------|-----------|
| EUPL-1.2 | Licensed | LICENSE, LICENSES/EUPL-1.2.txt |
| GDPR (EU) 2016/679 | Compliant - no personal data | docs/gdpr.md |
| OSOR | Registered | docs/osor.md |
| EC OSS Strategy 2020-2023 | Implemented | docs/eu-compliance.md |
| Interoperable Europe Act 2024/903 | Documented | docs/eu-compliance.md |
| REUSE Specification 3.0 | Compliant (DEP5) | .reuse/dep5 |
| FAIR4RS | Self-assessed | docs/fair4rs.md |
| Swedish Legal Basis (OSL 2009:400) | Documented | docs/swedish-legal-basis.md |
| WCAG 2.2 AA | Target conformance | docs/accessibility.md |
| NIS2 (EU) 2022/2555 | SDLC implemented | SECURITY.md |

---

## Installation

Requires Python 3.11 or 3.12 and [uv](https://github.com/astral-sh/uv).

```bash
git clone https://github.com/olaflaitinen/skatteprogressivitet.git
cd skatteprogressivitet
uv sync
```

For development (includes test, lint, type-check tools):

```bash
uv sync --extra dev
```

---

## Quickstart on synthetic fixture

Generate the synthetic fixture (50 000 individuals, 10 years, seed 19960307):

```bash
uv run python scripts/make_synthetic_fixture.py
```

Run the 2025 baseline scenario:

```bash
uv run skatteprogressivitet simulate --year 2025 --behavioural full
```

Compute progressivity indices:

```bash
uv run skatteprogressivitet progressivity --year 2025 --indices kakwani,suits,residual
```

Run a counterfactual (raise the brytpunkt by one percentage point of median earnings):

```bash
uv run skatteprogressivitet scenario --scenario data/scenarios/raise-brytpunkt.yaml
```

Compare baseline and counterfactual results:

```bash
uv run skatteprogressivitet compare --baseline 2025 --scenario raise-brytpunkt
```

---

## Legislation and scenario walkthrough

The legislative-parameter ledger lives in `data/legislation/`. Each YAML file encodes
bracket thresholds, marginal rates, deduction schedules, transfer amounts, and indexation
rules for one reform year. The ledger validates against `data/legislation/schema.json`.

```bash
uv run python scripts/validate_legislation.py --all
```

Scenario YAML files in `data/scenarios/` define counterfactual parameter overrides relative
to a baseline year. See `docs/scenarios.md` for the schema specification.

---

## Data policy

This repository contains no personal data. The synthetic fixture is generated from
`SYNTHETIC_SEED = 19960307` by `scripts/make_synthetic_fixture.py` and is distributed under
CC0-1.0. The legislative-parameter ledger is curated annotation of public statutes (SFS)
and is distributed under EUPL-1.2. Real administrative microdata (SCB LISA, IoT, FAD) are
accessed only within the SCB MONA/SAFE secure environment and are not committed at any time.

---

## Methodology summary

The static engine computes tax liabilities and transfer entitlements by applying the
legislative-parameter ledger to synthetic (or, in the secure environment, real) taxpayer
records. The behavioural module applies ETI-based income responses at each income
quartile, with separate intensive-margin (elasticity 0.3) and extensive-margin (elasticity
0.1) parameterisations. Income shifting under the 3:12 rules is modelled via the
owner-employee margin. Progressivity is measured by the Kakwani, Suits, and residual-
progression indices; inequality by Gini, Theil, and Atkinson. Counterfactual reforms
are revenue-scored and welfare-assessed through compensating and equivalent variation.
See `docs/methodology.md` for full details.

---

## Documentation

Full documentation: https://olaflaitinen.github.io/skatteprogressivitet

---

## Citation

```bibtex
@software{laitinen_fredriksson_lundstrom_imanov_2026_skatteprogressivitet,
  author    = {Laitinen-Fredriksson Lundstr{\"o}m Imanov, Gustav Olaf Yunus},
  title     = {Skatteprogressivitet: behavioural microsimulator of Swedish tax progressivity},
  year      = {2026},
  version   = {0.1.0},
  license   = {EUPL-1.2},
  url       = {https://github.com/olaflaitinen/skatteprogressivitet},
  orcid     = {0009-0006-5184-0810}
}
```

See also `CITATION.cff` and `docs/citation.md`.

---

## Contributing

See `CONTRIBUTING.md`. DCO sign-off and Conventional Commits required.

## Security

See `SECURITY.md`. Report vulnerabilities to olaf.laitinen@su.se.

## Governance

See `GOVERNANCE.md`.

---

## Portfolio cross-references

This is module 3 of a twenty-project portfolio on income, wealth, taxation, inequality,
and intergenerational mobility in Sweden:

- Inkomstprognos, Förmögenhetsanalys, Arvsdynamik, Mobilitetsmodellen, Inkomstklyftan,
  Pensionsrättvisa, Kapitalinkomst, Lönedynamik, Hushållsekonomi, Skattereform,
  Välfärdsmodellen, Generationsskifte, Demografiprognos, Mikrosimulering,
  Toppinkomstandelen, Bolagsskatteanalys, Skatteflyktsdetektor, Förmånsanalys,
  Omfördelningsmodellen.

---

## Maintainer

**Dr. Gustav Olaf Yunus Laitinen-Fredriksson Lundström Imanov, MD, RA, PhD**
ORCID: [0009-0006-5184-0810](https://orcid.org/0009-0006-5184-0810)
Department of Economics, Stockholm University, SE-106 91 Stockholm, Sweden
Email: olaf.laitinen@su.se
GitHub: [@olaflaitinen](https://github.com/olaflaitinen)

Licensed under [EUPL-1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).
Copyright 2024-2026 Gustav Olaf Yunus Laitinen-Fredriksson Lundström Imanov.
