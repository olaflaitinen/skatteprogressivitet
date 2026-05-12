"""Table serialisation utilities.

Writes simulation outputs to CSV (with optional UTF-8 BOM for Excel compatibility),
Parquet, and LaTeX table formats.
"""

from __future__ import annotations

import pathlib

import polars as pl
import pandas as pd


def to_csv_with_bom(df: pl.DataFrame, path: pathlib.Path) -> pathlib.Path:
    """Write a Polars DataFrame to CSV with UTF-8 BOM for Excel compatibility.

    Args:
        df: DataFrame to write.
        path: Output path.

    Returns:
        Path to the written file.

    Example:
        >>> import polars as pl, pathlib, tempfile
        >>> df = pl.DataFrame({"a": [1, 2], "b": [3, 4]})
        >>> with tempfile.TemporaryDirectory() as d:
        ...     p = to_csv_with_bom(df, pathlib.Path(d) / "out.csv")
        ...     p.exists()
        True
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    csv_bytes = df.write_csv().encode("utf-8")
    with path.open("wb") as fh:
        fh.write(b"\xef\xbb\xbf")
        fh.write(csv_bytes)
    return path


def to_parquet(df: pl.DataFrame, path: pathlib.Path) -> pathlib.Path:
    """Write a Polars DataFrame to Parquet.

    Args:
        df: DataFrame to write.
        path: Output path.

    Returns:
        Path to the written file.

    Example:
        >>> import polars as pl, pathlib, tempfile
        >>> df = pl.DataFrame({"a": [1, 2], "b": [3, 4]})
        >>> with tempfile.TemporaryDirectory() as d:
        ...     p = to_parquet(df, pathlib.Path(d) / "out.parquet")
        ...     p.exists()
        True
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(str(path))
    return path


def to_latex_table(
    df: pd.DataFrame,
    path: pathlib.Path,
    caption: str = "",
    label: str = "",
) -> pathlib.Path:
    """Write a pandas DataFrame to a LaTeX table.

    Args:
        df: DataFrame to write.
        path: Output .tex path.
        caption: Table caption.
        label: LaTeX label.

    Returns:
        Path to the written file.

    Example:
        >>> import pandas as pd, pathlib, tempfile
        >>> df = pd.DataFrame({"Metric": ["Kakwani"], "Value": [0.12]})
        >>> with tempfile.TemporaryDirectory() as d:
        ...     p = to_latex_table(df, pathlib.Path(d) / "tbl.tex")
        ...     p.exists()
        True
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    latex = df.to_latex(
        index=False,
        caption=caption or "Results",
        label=label or "tab:results",
        escape=True,
    )
    path.write_text(latex, encoding="utf-8")
    return path
