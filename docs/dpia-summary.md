# DPIA Summary

## Purpose

This document summarises the Data Protection Impact Assessment for the use of Swedish
register data in the Skatteprogressivitet research project.

## Processing Description

- **Data controller**: Department of Economics, Stockholm University.
- **Data processor**: Gustav Olaf Yunus Laitinen-Fredriksson Lundström Imanov.
- **Personal data categories**: Person identifiers (pseudonymised PIDs), income records
  (LISA/IoT), tax records (FAD), employment status, municipality codes, birth year.
- **Data subjects**: Swedish residents present in the LISA panel for the relevant reform
  years covered by the legislative ledger (1991–2025).
- **Legal basis**: Art. 6(1)(e) + 9(2)(j) GDPR; Etikprövningslagen 2003:460.
- **Processing environment**: SCB MONA/SAFE; no export of personal data.

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Re-identification via tax-record linkage | Low | High | Pseudonymisation; MONA/SAFE environment |
| Unauthorised access to register data | Low | High | SCB MONA access controls; gitleaks |
| Output disclosure | Low | Medium | Cell suppression; aggregate publication only |
| Accidental commit of personal data | Low | High | Gitleaks pre-commit hook; `.gitleaks.toml` |

## Outcome

Residual risk is acceptable given SCB MONA/SAFE safeguards. Processing may proceed
subject to ethics approval from Etikprövningsmyndigheten.

## Note on This Repository

This repository contains only synthetic data generated from `SYNTHETIC_SEED = 19960307`.
The DPIA applies to production use with real register data accessed under MONA/SAFE
authorisation.
