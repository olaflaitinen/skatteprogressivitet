"""Tests for the CLI entry points."""

from __future__ import annotations

from typer.testing import CliRunner

from skatteprogressivitet.cli import app

runner = CliRunner()


def test_validate_legislation_all() -> None:
    result = runner.invoke(app, ["validate-legislation", "--all"])
    assert result.exit_code == 0
    assert "valid" in result.output.lower()


def test_validate_legislation_single_year() -> None:
    result = runner.invoke(app, ["validate-legislation", "--year", "2025"])
    assert result.exit_code == 0


def test_validate_legislation_missing_year() -> None:
    result = runner.invoke(app, ["validate-legislation", "--year", "1900"])
    assert result.exit_code != 0


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "microsimulator" in result.output.lower()


def test_simulate_command() -> None:
    result = runner.invoke(app, ["simulate", "--year", "2025", "--behavioural", "none"])
    assert result.exit_code == 0
