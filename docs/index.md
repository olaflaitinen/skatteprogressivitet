# Skatteprogressivitet

**Static and behavioural microsimulator for Swedish tax progressivity (1991-2025)**

Skatteprogressivitet is an open-source research software package that implements
the full statutory tax-and-transfer rules of the Swedish dual income tax system
and computes effective marginal and average tax rates, progressivity indices
(Kakwani, Suits, Gini, Theil, Atkinson), and revenue and distributional effects
of counterfactual policy reforms.

## Quick start

```bash
pip install skatteprogressivitet
skatteprogressivitet simulate --year 2025 --behavioural full
skatteprogressivitet progressivity --year 2025
```

## Documentation structure

- [Installation](installation.md) - how to install the package
- [Quickstart](quickstart.md) - a five-minute tour
- [Methodology](methodology/progressivity.md) - index definitions and estimation
- [Legislation](legislation/overview.md) - the statutory parameter ledger
- [Scenarios](scenarios.md) - counterfactual reform scenarios
- [Replication](reproducibility.md) - how to reproduce published results
- [API reference](api/index.md) - auto-generated module documentation

## Licence and citation

This software is released under the [EUPL-1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).
If you use it in research, please cite it as described in [CITATION.cff](https://github.com/olaflaitinen/skatteprogressivitet/blob/main/CITATION.cff).
