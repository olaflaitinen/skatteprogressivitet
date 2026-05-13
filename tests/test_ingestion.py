"""Tests for the data ingestion modules."""

from __future__ import annotations

import pathlib
import tempfile

import polars as pl
import pytest

from skatteprogressivitet.ingestion.lisa import read_lisa, synthetic_lisa
from skatteprogressivitet.ingestion.manifest import Manifest, load_manifest, validate_against_schema
from skatteprogressivitet.ingestion.tax_registers import (
    read_tax_register,
    synthetic_tax_register,
)


def test_synthetic_lisa_returns_dataframe() -> None:
    df = synthetic_lisa(n=100, years=[2025], seed=19960307)
    assert isinstance(df, pl.DataFrame)
    assert len(df) == 100


def test_synthetic_lisa_has_expected_columns() -> None:
    df = synthetic_lisa(n=50, years=[2025], seed=19960307)
    for col in ["person_id", "year", "labour_income", "capital_income", "age", "self_employed"]:
        assert col in df.columns


def test_synthetic_lisa_labour_income_positive() -> None:
    df = synthetic_lisa(n=200, years=[2025], seed=19960307)
    assert (df["labour_income"] >= 0).all()


def test_synthetic_lisa_deterministic() -> None:
    df1 = synthetic_lisa(n=100, years=[2025], seed=19960307)
    df2 = synthetic_lisa(n=100, years=[2025], seed=19960307)
    assert df1["labour_income"].to_list() == df2["labour_income"].to_list()


def test_read_lisa_raises_if_missing() -> None:
    with pytest.raises(FileNotFoundError):
        read_lisa(pathlib.Path("/nonexistent/path/lisa.parquet"))


def test_synthetic_tax_register_returns_dataframe() -> None:
    df = synthetic_tax_register(n=50, years=[2025], seed=19960307)
    assert isinstance(df, pl.DataFrame)
    assert "taxable_income" in df.columns


def test_read_tax_register_raises_if_missing() -> None:
    with pytest.raises(FileNotFoundError):
        read_tax_register(pathlib.Path("/nonexistent/tax.parquet"))


def test_load_manifest_from_yaml() -> None:
    import yaml

    data = {
        "version": "1.0",
        "datasets": [
            {"name": "lisa", "path": "data/synthetic/lisa_like.parquet"},
        ],
    }
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
        yaml.dump(data, f)
        p = pathlib.Path(f.name)
    m = load_manifest(p)
    assert m.datasets[0].name == "lisa"
    p.unlink()


def test_validate_manifest_no_errors() -> None:
    m = Manifest(datasets=[])
    errors = validate_against_schema(m)
    assert errors == []


def test_lisa_roundtrip_parquet() -> None:
    df = synthetic_lisa(n=100, years=[2025], seed=19960307)
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "lisa.parquet"
        df.write_parquet(str(p))
        loaded = read_lisa(p)
        assert len(loaded) == len(df)
        assert loaded.columns == df.columns
