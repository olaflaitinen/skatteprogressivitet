# Changelog

All notable changes to Skatteprogressivitet will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-05-12

### Added

- Initial release of Skatteprogressivitet microsimulator.
- Legislative-parameter ledger covering reform years 1991, 1995, 2000, 2007, 2015, 2020, 2025.
- Static tax engine: personal income tax (statlig and kommunal), payroll taxes, capital-income
  tax, jobbskatteavdrag, housing allowances, social transfers.
- 3:12 rules module for closely held firms (fåmansföretag): huvudregeln and förenklingsregeln.
- Behavioural ETI module with intensive-margin (default 0.3) and extensive-margin (default 0.1)
  parameterisations calibrated to Swedish reform literature.
- Bunching-based identification module around brytpunkter.
- Income-shifting module for labour-to-capital reclassification.
- Progressivity indices: Kakwani, Suits, residual progression, Gini, Theil, Atkinson.
- Bootstrap and influence-function standard errors for progressivity indices.
- Shapley-value decomposition of progressivity by tax rule.
- Causal inference modules: two-way FE DiD, Callaway-Sant'Anna, Sun-Abraham,
  de Chaisemartin-D'Haultfoeuille, event study, IV.
- Four counterfactual scenario YAML manifests.
- Deterministic synthetic fixture (50 000 individuals, 10 years, seed 19960307).
- Full test suite with >= 90 percent coverage gate.
- MkDocs Material documentation.
- REUSE 3.0 compliance via DEP5.
- EUPL-1.2 licence.
- CI/CD on ubuntu-22.04, macos-14, windows-2022.
- CycloneDX SBOM generation.
- Sigstore release signing.
- CITATION.cff and Zenodo metadata.

[Unreleased]: https://github.com/olaflaitinen/skatteprogressivitet/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/olaflaitinen/skatteprogressivitet/releases/tag/v0.1.0
