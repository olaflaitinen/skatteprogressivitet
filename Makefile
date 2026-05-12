.PHONY: all lint type test cov docs build audit reuse sbom release sync clean

all: lint type test

sync:
	uv sync

lint:
	uv run nox -s lint

type:
	uv run nox -s type

test:
	uv run nox -s test

cov:
	uv run nox -s cov

docs:
	uv run nox -s docs

build:
	uv run nox -s build

audit:
	uv run nox -s audit

reuse:
	uv run nox -s reuse

sbom:
	uv run nox -s sbom

release:
	uv run nox -s release

validate-legislation:
	uv run python scripts/validate_legislation.py --all

synthetic-fixture:
	uv run python scripts/make_synthetic_fixture.py

clean:
	rm -rf dist/ build/ site/ htmlcov/ .coverage .mypy_cache .ruff_cache .pytest_cache sbom.cdx.json
