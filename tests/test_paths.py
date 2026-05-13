"""Tests for canonical path management."""

from __future__ import annotations

from typing import TYPE_CHECKING

from skatteprogressivitet.paths import (
    DATA_ROOT,
    LEGISLATION_ROOT,
    REPORTS_ROOT,
    SCENARIO_ROOT,
    SYNTHETIC_ROOT,
    ensure_reports_root,
)

if TYPE_CHECKING:
    import pathlib


def test_data_root_exists() -> None:
    assert DATA_ROOT.exists()


def test_legislation_root_exists() -> None:
    assert LEGISLATION_ROOT.exists()


def test_scenario_root_exists() -> None:
    assert SCENARIO_ROOT.exists()


def test_paths_are_absolute() -> None:
    for p in [DATA_ROOT, LEGISLATION_ROOT, SCENARIO_ROOT, SYNTHETIC_ROOT, REPORTS_ROOT]:
        assert p.is_absolute()


def test_ensure_reports_root_creates_dir(tmp_path: pathlib.Path) -> None:
    import skatteprogressivitet.paths as paths_module

    original = paths_module.REPORTS_ROOT
    paths_module.REPORTS_ROOT = tmp_path / "reports"
    try:
        result = ensure_reports_root()
        assert result.exists()
    finally:
        paths_module.REPORTS_ROOT = original
