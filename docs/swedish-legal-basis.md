# Swedish Legal Basis

## OSL 2009:400 Chapter 24 (Offentlighets- och sekretesslag)

Chapter 24 of OSL governs confidentiality for statistical data held by public authorities
such as SCB. Access to LISA, IoT, and FAD registers requires a formal data access agreement
(dataavtal) under OSL 24:8, granted through SCB MONA/SAFE.

## Lag 2001:99 (Registerlag för Statistik)

Lag 2001:99 regulates the processing of personal data in Swedish official statistics.
Research use under this act requires ethical approval from Etikprövningsmyndigheten.

## Inkomstskattelagen (IL) 1999:1229

The Income Tax Act (IL) is the primary statutory basis for the legislative-parameter ledger.
All bracket thresholds, rates, deduction schedules, and 3:12 parameters encoded in
`data/legislation/` are derived from IL and annual SFS amendments.

## SCB MONA/SAFE

The Microdata Online Access (MONA) system and the SAFE remote execution environment are
SCB's secure infrastructure for research access to linked register data (LISA, IoT, FAD).
All production processing must occur within these environments.

## Etikprövningslagen 2003:460

Swedish law on ethical review requires approval from Etikprövningsmyndigheten before
research that processes sensitive personal data about identifiable individuals may begin.

## Riksarkivet RA-FS 2009:1

Research data must be preserved in accordance with Riksarkivet regulations. Synthetic
fixtures and analysis code are archived via Zenodo; real register data remains within
SCB controlled infrastructure.

## SND FAIR Principles

The Swedish National Data Service (SND) FAIR data principles apply to published
research outputs and metadata from this project.

## SFS References in the Legislative Ledger

Each file in `data/legislation/` includes inline comments citing:

- The SFS number of the governing statute (e.g. `# SFS 2007:346`).
- The Riksdag proposition reference (e.g. `# Prop. 2006/07:1`).
- The effective date of the parameters.
