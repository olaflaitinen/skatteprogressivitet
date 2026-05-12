"""Canonical filesystem paths for Skatteprogressivitet.

All path constants resolve relative to the repository root detected at import
time.  Downstream modules should import from here rather than constructing
paths ad-hoc.
"""

from __future__ import annotations

import pathlib

_REPO_ROOT: pathlib.Path = pathlib.Path(__file__).parent.parent.parent

DATA_ROOT: pathlib.Path = _REPO_ROOT / "data"
LEGISLATION_ROOT: pathlib.Path = DATA_ROOT / "legislation"
SCENARIO_ROOT: pathlib.Path = DATA_ROOT / "scenarios"
SYNTHETIC_ROOT: pathlib.Path = DATA_ROOT / "synthetic"
REPORTS_ROOT: pathlib.Path = _REPO_ROOT / "reports"


def ensure_reports_root() -> pathlib.Path:
    """Create the reports directory if it does not exist.

    Returns:
        The resolved reports root path.

    Example:
        >>> p = ensure_reports_root()
        >>> p.exists()
        True
    """
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    return REPORTS_ROOT
