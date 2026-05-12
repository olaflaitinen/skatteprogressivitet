"""Nox sessions for Skatteprogressivitet."""

from __future__ import annotations

import nox

nox.options.sessions = ["lint", "type", "test", "cov"]
nox.options.reuse_existing_virtualenvs = True

PYTHON_VERSIONS = ["3.11", "3.12"]
SRC = "src/skatteprogressivitet"


@nox.session(python=PYTHON_VERSIONS)
def lint(session: nox.Session) -> None:
    """Run ruff linter and formatter check."""
    session.install("ruff>=0.5")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session(python=PYTHON_VERSIONS)
def type(session: nox.Session) -> None:
    """Run mypy strict type checking."""
    session.install(".[dev]")
    session.run("mypy", "--strict", SRC)


@nox.session(python=PYTHON_VERSIONS)
def test(session: nox.Session) -> None:
    """Run the test suite."""
    session.install(".[dev]")
    session.run(
        "pytest",
        "-x",
        "-q",
        "--import-mode=importlib",
        *session.posargs,
    )


@nox.session(python="3.12")
def cov(session: nox.Session) -> None:
    """Run tests with coverage gate."""
    session.install(".[dev]")
    session.run(
        "pytest",
        "-x",
        "-q",
        "--cov=skatteprogressivitet",
        "--cov-fail-under=90",
        "--cov-branch",
        "--cov-report=xml",
        "--import-mode=importlib",
        *session.posargs,
    )


@nox.session(python="3.12")
def docs(session: nox.Session) -> None:
    """Build documentation with mkdocs."""
    session.install(".[docs]")
    session.run("mkdocs", "build", "--strict")


@nox.session(python="3.12")
def build(session: nox.Session) -> None:
    """Build sdist and wheel."""
    session.install("hatchling")
    session.run("python", "-m", "hatchling", "build")


@nox.session(python="3.12")
def audit(session: nox.Session) -> None:
    """Run pip-audit and bandit security checks."""
    session.install(".[dev]")
    session.run("pip-audit", "--strict")
    session.run("bandit", "-r", SRC, "-lll")


@nox.session(python="3.12")
def reuse(session: nox.Session) -> None:
    """Verify REUSE compliance."""
    session.install("reuse>=4")
    session.run("reuse", "lint")


@nox.session(python="3.12")
def sbom(session: nox.Session) -> None:
    """Generate CycloneDX SBOM."""
    session.install("cyclonedx-bom>=4")
    session.run("cyclonedx-py", "-o", "sbom.cdx.json")


@nox.session(python="3.12")
def release(session: nox.Session) -> None:
    """Full release pipeline: build, audit, sbom, reuse."""
    session.install(".[dev]")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")
    session.run("mypy", "--strict", SRC)
    session.run("pytest", "-x", "-q", "--cov=skatteprogressivitet", "--cov-fail-under=90")
    session.run("reuse", "lint")
    session.run("pip-audit", "--strict")
    session.run("bandit", "-r", SRC, "-lll")
    session.run("cyclonedx-py", "-o", "sbom.cdx.json")
    session.run("python", "-m", "hatchling", "build")
