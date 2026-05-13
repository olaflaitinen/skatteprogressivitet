# GDPR Compliance

## Lawful Basis

Processing of personal data in production use (real register data accessed under MONA/SAFE)
relies on:

- **Article 6(1)(e)**: Processing necessary for the performance of a task carried out in
  the public interest or in the exercise of official authority.
- **Article 9(2)(j)**: Processing for scientific research purposes subject to appropriate
  safeguards.

## Data Minimisation

Only the variables necessary for tax microsimulation and progressivity estimation are
retained in analysis files. Raw register data (SCB LISA, IoT, FAD) is accessed only in
the SCB MONA/SAFE secure environment and is never exported or committed.

## Security of Processing (Article 32)

- All register data remains within the MONA/SAFE environment.
- No personal data, microdata, personnummer, or organisationsnummer are committed to
  this repository at any time.
- Gitleaks rules in `.gitleaks.toml` enforce PII detection at commit time.

## DPIA Threshold

A Data Protection Impact Assessment (DPIA) is required before accessing real register data
under Etikprövningslagen 2003:460. The DPIA summary is in [dpia-summary.md](dpia-summary.md).

## Research Safeguards (Article 89)

- Results are published only in aggregated, anonymised form.
- Minimum cell-size suppression is applied to distributional outputs.
- No re-identification of individuals is possible from published outputs.
- Data retention follows Riksarkivet RA-FS 2009:1 and SCB archive policy.
