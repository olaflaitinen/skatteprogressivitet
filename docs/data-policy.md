# Data Policy

## GDPR compliance

This repository contains **no personal data** and **no real microdata** of any
kind. The following data types are explicitly excluded:

- SCB LISA panel microdata (real)
- Skatteverket IoT (tax register) microdata (real)
- Any personnummer, name, address, or other directly identifying information
- Any indirectly identifying combination of variables

All empirical analysis in this project is conducted inside the SCB secure
research environment (Microdata Online Access, MONA) and no microdata are
committed to this repository.

## Synthetic data

The synthetic LISA-like and tax-register-like fixtures in `data/synthetic/`
are generated deterministically from the SYNTHETIC_SEED (19960307) using
lognormal income distributions with parameters calibrated to published SCB
aggregate statistics. They contain no real individuals. The synthetic data
are licensed under CC0-1.0 (see `data/synthetic/CC0_WAIVER.md`).

## Legislative data

The YAML files in `data/legislation/` contain exclusively public statutory
parameters from Swedish government legislation (SFS) and government
propositions (Prop.), which are in the public domain under Swedish law.

## Research environment

Access to real microdata for academic replication is available through the
SCB MONA system. The institutional data access agreement (DAA) and
processing records are maintained at the Department of Economics,
Stockholm University, and are not committed to this repository.

## Legal basis

Data processing in the secure environment relies on the legal basis of
Article 89(1) GDPR (scientific research purpose), implemented in Sweden
via Lag (2018:218) med kompletterande bestammelser till EU:s
dataskyddsforordning.
