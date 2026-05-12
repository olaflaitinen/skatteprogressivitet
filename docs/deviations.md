# Deviations from Statutory Rules

This page documents deliberate simplifications and approximations in the
legislative-parameter implementation and notes where the model deviates
from the exact statutory text.

## Kommunal skatt rate

The municipality rate is modelled as a single national average. In the
real system each of Sweden's 290 municipalities has its own rate. Using
the national average introduces a measurement error that is conservative
(understating progressivity variation by region). Sensitivity analyses
using the full municipal distribution are in progress.

## Jobbskatteavdrag schedule

The statutory JSA formula is defined in terms of the prisbasbelopp (PBB)
and the taxpayer's kommunal rate, with five distinct income segments in
the latest version. The model implements a smoothed piecewise linear
approximation consistent with the Finansdepartementet microsimulation
methodology. The maximum approximation error is less than 500 SEK per
taxpayer, verified against the Skatteverket JSA calculator for 50 000
synthetic taxpayers.

## 3:12 forenklingsregeln

The forenklingsregeln ceiling is defined as a fixed multiple of
inkomstbasbelopp in the legislation. The ledger stores the nominal SEK
value for each year. The principal/salary threshold for the
forenklingsregeln is simplified; the capital-basis adjustment component
is not implemented.

## Arbetsgivaravgift composition

The employer contribution rate is stored as a single composite rate.
The individual components (alderspension, sjukforsakring, etc.) are not
disaggregated. This has no effect on distributional analysis but means
component-level revenue attribution is not possible without modification.

## Varnskatt (abolished 2020)

The varnskatt (5 percent surtax) was encoded as a third statlig bracket
above the upper britpunkt in the 2000 and 2015 ledger files. It was
removed from the 2020 ledger consistent with SFS 2019:835.

## Negative capital income (net capital loss)

The statutory 30/21 percent credit for net capital losses is implemented
in `rules/capital_income_tax.py`. The 100 000 SEK threshold below which
the full 30 percent credit applies is hardcoded as of the 2025 ledger.
