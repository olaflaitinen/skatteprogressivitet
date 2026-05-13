"""Figure generation for Skatteprogressivitet reports.

Produces publication-quality PNG, SVG, and PDF/A-2u figures using matplotlib.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

if TYPE_CHECKING:
    import pathlib


def _get_axes() -> tuple[Any, Any]:
    """Import matplotlib and return a new (fig, ax) pair.

    Returns:
        Tuple of (Figure, Axes).
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5))
    return fig, ax


class FigureBuilder:
    """Builder for standard Skatteprogressivitet report figures.

    Attributes:
        output_dir: Directory where figures are written.
    """

    def __init__(self, output_dir: pathlib.Path | None = None) -> None:
        """Initialise FigureBuilder.

        Args:
            output_dir: Output directory. Defaults to ``reports/figures``.
        """
        from skatteprogressivitet.paths import REPORTS_ROOT

        self.output_dir: pathlib.Path = output_dir or (REPORTS_ROOT / "figures")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def effective_rate_profile(
        self,
        incomes: np.ndarray,
        average_rates: np.ndarray,
        marginal_rates: np.ndarray,
        year: int,
        save: bool = True,
    ) -> pathlib.Path:
        """Plot effective average and marginal rate profiles.

        Args:
            incomes: Income array.
            average_rates: Effective average tax rates.
            marginal_rates: Effective marginal tax rates.
            year: Legislation year label.
            save: Whether to save the figure. Default True.

        Returns:
            Path to the saved PNG file.

        Example:
            >>> import numpy as np
            >>> fb = FigureBuilder()
            >>> y = np.linspace(50000, 800000, 100)
            >>> avg = y * 0.0 + 0.30
            >>> mtr = y * 0.0 + 0.52
            >>> p = fb.effective_rate_profile(y, avg, mtr, 2025, save=False)
            >>> isinstance(p, pathlib.Path)
            True
        """
        fig, ax = _get_axes()
        ax.plot(incomes / 1000, average_rates * 100, label="Average rate", linewidth=2)
        ax.plot(
            incomes / 1000, marginal_rates * 100, label="Marginal rate", linewidth=2, linestyle="--"
        )
        ax.set_xlabel("Labour income (kSEK)")
        ax.set_ylabel("Effective tax rate (%)")
        ax.set_title(f"Effective tax rates {year}")
        ax.legend()
        ax.grid(True, alpha=0.3)
        out = self.output_dir / f"effective_rates_{year}.png"
        if save:
            fig.savefig(out, dpi=150, bbox_inches="tight")
        import matplotlib.pyplot as plt

        plt.close(fig)
        return out

    def lorenz_curve(
        self,
        pre_tax_income: np.ndarray,
        post_tax_income: np.ndarray,
        year: int,
        save: bool = True,
    ) -> pathlib.Path:
        """Plot Lorenz curves for pre-tax and post-tax income.

        Args:
            pre_tax_income: Pre-tax income array.
            post_tax_income: Post-tax income array.
            year: Year label.
            save: Whether to save. Default True.

        Returns:
            Path to the saved PNG file.

        Example:
            >>> import numpy as np
            >>> fb = FigureBuilder()
            >>> y = np.linspace(10, 100, 50)
            >>> p = fb.lorenz_curve(y, y * 0.8, 2025, save=False)
            >>> isinstance(p, pathlib.Path)
            True
        """

        def _lorenz(vals: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
            s = np.sort(vals)
            n = len(s)
            cumshare = np.cumsum(s) / np.sum(s)
            pop_share = np.arange(1, n + 1) / n
            return np.concatenate([[0], pop_share]), np.concatenate([[0], cumshare])

        fig, ax = _get_axes()
        px, py = _lorenz(pre_tax_income)
        qx, qy = _lorenz(post_tax_income)
        ax.plot([0, 1], [0, 1], "k--", label="Equality", linewidth=1)
        ax.plot(px, py, label="Pre-tax", linewidth=2)
        ax.plot(qx, qy, label="Post-tax", linewidth=2, linestyle="--")
        ax.set_xlabel("Cumulative population share")
        ax.set_ylabel("Cumulative income share")
        ax.set_title(f"Lorenz curves {year}")
        ax.legend()
        ax.grid(True, alpha=0.3)
        out = self.output_dir / f"lorenz_{year}.png"
        if save:
            fig.savefig(out, dpi=150, bbox_inches="tight")
        import matplotlib.pyplot as plt

        plt.close(fig)
        return out
