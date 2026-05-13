# Contributing to Skatteprogressivitet

Thank you for considering a contribution. Please read this document in full before
opening a pull request.

## Developer Certificate of Origin (DCO)

All commits must include a DCO sign-off line:

```
Signed-off-by: Your Name <your@email.example>
```

Add it automatically with `git commit -s`. By signing off you certify that you wrote
the contribution and have the right to submit it under EUPL-1.2.

## Commit style

This project follows [Conventional Commits 1.0.0](https://www.conventionalcommits.org/).
Examples:

```
feat(rules): add 2026 statutory bracket parameters
fix(eti): correct intensive-margin elasticity at quartile 4
docs(methodology): clarify residual-progression formula
test(progressivity): add property test for Kakwani monotonicity
```

## Signed commits

All commits must be GPG-signed. Configure with:

```bash
git config --global commit.gpgsign true
```

## EUPL-1.2 compatibility check

Before adding a new dependency, verify that its licence is listed as a compatible
licence in the EUPL-1.2 Appendix, or is otherwise EUPL-compatible per
`docs/eu-compliance.md`. Incompatible licences will be rejected.

## REUSE compliance

This repository uses REUSE Specification 3.0 via DEP5 (`.reuse/dep5`). Do not add
per-file SPDX comment headers. Do not add a `REUSE.toml`. When adding new files,
ensure they are covered by an existing paragraph in `.reuse/dep5`, or add a new
paragraph. Run `uv run reuse lint` before opening a PR.

## GDPR no-PII rule

Do not commit any personal data, real microdata, real tax returns, personnummer,
organisationsnummer, IBAN, or any other personally identifying or financially
sensitive information at any time. Gitleaks is configured to block such commits.

## Legislative-parameter contribution rules

Every new reform episode added to `data/legislation/` must:

1. Include a comment block citing the SFS reference (e.g. `# SFS 2007:346`),
   the proposition reference (e.g. `# Prop. 2006/07:1`), and the effective date.
2. Include an inline diff comment against the prior-year file, listing every
   changed field and its old and new values.
3. Be validated by `python scripts/validate_legislation.py --all` with zero errors.
4. Include at least one unit test in `tests/test_legislation_loader.py` asserting
   backward compatibility on the documented set of 100 taxpayer archetypes.
5. Include a golden-record SHA-256 in `tests/golden/legislation-<year>.sha256`.

## Running checks locally

```bash
uv sync --extra dev
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict src
uv run pytest -x -q --cov=skatteprogressivitet --cov-fail-under=90 --cov-branch
uv run reuse lint
uv run pip-audit --strict
uv run bandit -r src -lll
```

## Pull request checklist

- [ ] DCO sign-off on all commits.
- [ ] Conventional Commits message format.
- [ ] GPG-signed commits.
- [ ] `ruff check` and `ruff format --check` pass.
- [ ] `mypy --strict` passes.
- [ ] `pytest` passes with coverage >= 90 percent.
- [ ] `reuse lint` passes.
- [ ] No personal data or real microdata.
- [ ] If adding a legislation year: SFS citation, inline diff, golden record, unit test.
- [ ] `docs/deviations.md` updated if a requirement is stubbed.
- [ ] `CHANGELOG.md` updated under `[Unreleased]`.
