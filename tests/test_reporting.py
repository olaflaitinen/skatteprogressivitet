"""Tests for reporting utilities."""

from __future__ import annotations

import pathlib
import tempfile

import numpy as np
import pandas as pd
import polars as pl

from skatteprogressivitet.reporting.figures import FigureBuilder
from skatteprogressivitet.reporting.tables import to_csv_with_bom, to_latex_table, to_parquet


def test_to_csv_with_bom_writes_file() -> None:
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4.0, 5.0, 6.0]})
    with tempfile.TemporaryDirectory() as d:
        p = to_csv_with_bom(df, pathlib.Path(d) / "out.csv")
        assert p.exists()
        content = p.read_bytes()
        assert content[:3] == b"\xef\xbb\xbf"


def test_to_parquet_writes_file() -> None:
    df = pl.DataFrame({"x": [1, 2], "y": [3, 4]})
    with tempfile.TemporaryDirectory() as d:
        p = to_parquet(df, pathlib.Path(d) / "out.parquet")
        assert p.exists()
        roundtrip = pl.read_parquet(str(p))
        assert list(roundtrip.columns) == ["x", "y"]


def test_to_latex_table_writes_file() -> None:
    df = pd.DataFrame({"Metric": ["Kakwani", "Suits"], "Value": [0.12, 0.10]})
    with tempfile.TemporaryDirectory() as d:
        p = to_latex_table(df, pathlib.Path(d) / "tbl.tex")
        assert p.exists()
        text = p.read_text(encoding="utf-8")
        assert "tabular" in text


def test_figure_builder_rate_profile() -> None:
    y = np.linspace(50_000, 800_000, 50)
    avg = np.full_like(y, 0.30)
    mtr = np.full_like(y, 0.52)
    with tempfile.TemporaryDirectory() as d:
        fb = FigureBuilder(output_dir=pathlib.Path(d))
        p = fb.effective_rate_profile(y, avg, mtr, 2025, save=True)
        assert p.exists()


def test_figure_builder_lorenz_curve() -> None:
    y = np.linspace(10, 100, 50)
    with tempfile.TemporaryDirectory() as d:
        fb = FigureBuilder(output_dir=pathlib.Path(d))
        p = fb.lorenz_curve(y, y * 0.8, 2025, save=True)
        assert p.exists()
