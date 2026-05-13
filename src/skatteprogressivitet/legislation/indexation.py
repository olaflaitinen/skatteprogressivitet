"""Indexation series for statutory amounts.

Provides the basbelopp, prisbasbelopp, and inkomstbasbelopp series derived from
the committed legislation YAML files, and utility methods for indexing bracket
thresholds and transfer ceilings across years.
"""

from __future__ import annotations

BASBELOPP_SERIES: dict[int, float] = {
    1991: 32200,
    1995: 35700,
    2000: 36900,
    2007: 41000,
    2015: 44500,
    2020: 47300,
    2025: 52500,
}

PRISBASBELOPP_SERIES: dict[int, float] = {
    1991: 32200,
    1995: 35700,
    2000: 36900,
    2007: 41000,
    2015: 44500,
    2020: 47300,
    2025: 52500,
}

INKOMSTBASBELOPP_SERIES: dict[int, float] = {
    1991: 32200,
    1995: 35700,
    2000: 38800,
    2007: 46200,
    2015: 58100,
    2020: 66800,
    2025: 74300,
}


def get_basbelopp(year: int) -> float:
    """Return the basbelopp for the given year.

    Interpolates linearly between known reference years if the exact year is
    not in the series.

    Args:
        year: Calendar year.

    Returns:
        Basbelopp in SEK.

    Example:
        >>> get_basbelopp(2025)
        52500.0
    """
    return _interpolate(BASBELOPP_SERIES, year)


def get_prisbasbelopp(year: int) -> float:
    """Return the prisbasbelopp for the given year.

    Args:
        year: Calendar year.

    Returns:
        Prisbasbelopp in SEK.

    Example:
        >>> get_prisbasbelopp(2025)
        52500.0
    """
    return _interpolate(PRISBASBELOPP_SERIES, year)


def get_inkomstbasbelopp(year: int) -> float:
    """Return the inkomstbasbelopp for the given year.

    Args:
        year: Calendar year.

    Returns:
        Inkomstbasbelopp in SEK.

    Example:
        >>> get_inkomstbasbelopp(2025)
        74300.0
    """
    return _interpolate(INKOMSTBASBELOPP_SERIES, year)


def index_threshold(threshold: float, base_year: int, target_year: int) -> float:
    """Scale a statutory threshold from base_year to target_year using prisbasbelopp.

    Args:
        threshold: Threshold value in SEK at base_year prices.
        base_year: Reference year for the threshold.
        target_year: Target year to index to.

    Returns:
        Indexed threshold in SEK at target_year prices.

    Example:
        >>> t = index_threshold(170000, 1991, 2025)
        >>> t > 170000
        True
    """
    base_pbb = get_prisbasbelopp(base_year)
    target_pbb = get_prisbasbelopp(target_year)
    return threshold * (target_pbb / base_pbb)


def _interpolate(series: dict[int, float], year: int) -> float:
    """Linear interpolation within a known series.

    Args:
        series: Mapping from year to value.
        year: Target year.

    Returns:
        Interpolated or exact value.
    """
    if year in series:
        return float(series[year])
    years = sorted(series.keys())
    if year <= years[0]:
        return float(series[years[0]])
    if year >= years[-1]:
        return float(series[years[-1]])
    for i in range(len(years) - 1):
        y0, y1 = years[i], years[i + 1]
        if y0 < year < y1:
            v0, v1 = series[y0], series[y1]
            alpha = (year - y0) / (y1 - y0)
            return float(v0 + alpha * (v1 - v0))
    return float(series[years[-1]])
