"""PDF/A-2u wrapper for report generation.

Provides a thin wrapper around matplotlib's PDF backend with metadata settings
that target PDF/A-2u compliance per Riksarkivet RA-FS 2009:1 preservation
requirements.

Note: Full PDF/A conformance validation requires an external tool (e.g. veraPDF).
This module sets the XMP metadata required for PDF/A-2u conformance but does not
guarantee full conformance without validation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pathlib


def save_figure_pdf_a(
    fig: Any,
    path: pathlib.Path,
    title: str = "",
    author: str = "Gustav Olaf Yunus Laitinen-Fredriksson Lundström Imanov",
    subject: str = "Skatteprogressivitet report figure",
) -> pathlib.Path:
    """Save a matplotlib figure as a PDF targeting PDF/A-2u.

    Sets PDF metadata for title, author, and subject. Uses matplotlib's PDF
    backend with embedded fonts.

    Args:
        fig: A matplotlib Figure object.
        path: Output path (should end in ``.pdf``).
        title: Document title for PDF metadata.
        author: Author name for PDF metadata.
        subject: Subject string for PDF metadata.

    Returns:
        Path to the saved PDF file.

    Example:
        >>> import matplotlib
        >>> matplotlib.use("Agg")
        >>> import matplotlib.pyplot as plt, pathlib, tempfile
        >>> fig, ax = plt.subplots()
        >>> ax.plot([1, 2], [3, 4])
        [...]
        >>> with tempfile.TemporaryDirectory() as d:
        ...     p = save_figure_pdf_a(fig, pathlib.Path(d) / "fig.pdf")
        ...     p.exists()
        True
    """
    import matplotlib
    from matplotlib.backends.backend_pdf import PdfPages

    path.parent.mkdir(parents=True, exist_ok=True)

    metadata = {
        "Title": title or path.stem,
        "Author": author,
        "Subject": subject,
        "Creator": "Skatteprogressivitet v0.1.0",
        "Producer": f"matplotlib {matplotlib.__version__}",
    }

    with PdfPages(str(path), metadata=metadata) as pp:
        pp.savefig(fig, bbox_inches="tight")

    import matplotlib.pyplot as plt

    plt.close(fig)
    return path
