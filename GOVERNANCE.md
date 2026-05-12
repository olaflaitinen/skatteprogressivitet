# Governance

## Model

Skatteprogressivitet uses a **lead-maintainer model**. A single maintainer holds
merge rights, release rights, and final decision authority. Community contributors
participate via pull requests and issue discussions.

## Lead Maintainer

Dr. Gustav Olaf Yunus Laitinen-Fredriksson Lundström Imanov, MD, RA, PhD
ORCID: https://orcid.org/0009-0006-5184-0810
Department of Economics, Stockholm University
Email: olaf.laitinen@su.se

## Decision process

1. **Bug fixes and documentation**: merged by the lead maintainer after CI passes.
2. **New features and legislative-parameter additions**: require a GitHub issue
   describing the change, a linked pull request with full test coverage, and
   approval by the lead maintainer.
3. **Breaking changes** (API, data schema, golden-record reset): require a
   CHANGELOG entry, a version bump, and explicit documentation of the change
   in `docs/deviations.md` or the methodology pages.
4. **Licence changes**: require a formal amendment process and cannot be made
   unilaterally.

## Succession

If the lead maintainer is unavailable for more than 90 days, the Department of
Economics at Stockholm University nominates a successor via the institutional
GitHub organisation.

## Transparency

All decisions are recorded in commit history, GitHub issues, and pull request
discussions. The CHANGELOG documents every user-visible change.
