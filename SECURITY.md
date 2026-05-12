# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x | Yes |

## Reporting a Vulnerability

Report security vulnerabilities by email to **olaf.laitinen@su.se** (primary) or
**olaf.laitinen@gmail.com** (fallback). Do not open a public GitHub issue for security
vulnerabilities.

Include in your report:

- A description of the vulnerability and its potential impact.
- Steps to reproduce or a proof-of-concept.
- Any suggested remediation.

You will receive an acknowledgement within 5 business days. The maintainer commits
to a **90-day responsible disclosure** timeline from initial report to public disclosure.

## NIS2-aligned SDLC

This project implements the following security controls aligned with NIS2 (EU) 2022/2555
and the Cyber Resilience Act:

- **Dependency pinning**: all dependencies are pinned via `uv.lock`.
- **SBOM**: CycloneDX 1.5 JSON SBOM generated at each release.
- **Sigstore signatures**: wheel and sdist are signed via OIDC at release.
- **OpenSSF Scorecard**: weekly automated security posture assessment.
- **CodeQL**: weekly static analysis for Python vulnerabilities.
- **pip-audit**: dependency vulnerability scan in CI.
- **bandit**: static analysis for common Python security issues in CI.
- **gitleaks**: pre-commit hook blocking committed secrets, personnummer, IBAN.
- **Dependabot**: automated dependency update PRs.

## Scope

This repository contains no personal data and no real microdata. The primary
security concern is supply-chain integrity of the software artefacts themselves.
