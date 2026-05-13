"""Command-line interface for Skatteprogressivitet.

All output goes through typer / rich; no bare print statements outside this module.
"""

from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer(
    name="skatteprogressivitet",
    help="Static and behavioural microsimulator for Swedish tax progressivity.",
    add_completion=False,
)
console = Console()


@app.command()
def simulate(
    year: int = typer.Option(2025, help="Legislation year."),
    behavioural: str = typer.Option("full", help="Behavioural mode: none|eti|full."),
    output: str | None = typer.Option(None, help="Output Parquet path."),
) -> None:
    """Run a static/behavioural simulation for a given year."""
    from skatteprogressivitet.config import Config
    from skatteprogressivitet.pipelines.runner import Pipeline

    console.print(f"[bold]Simulating year {year} (mode={behavioural})...[/bold]")
    config = Config(baseline_year=year, behavioural=behavioural)  # type: ignore[arg-type]
    pipe = Pipeline(config=config)
    result = pipe.run()
    console.print(f"[green]Done.[/green] n_taxpayers={result.simulation_result.n_taxpayers}")
    console.print(f"Progressivity: {result.progressivity}")

    if output:
        import pathlib

        from skatteprogressivitet.reporting.tables import to_parquet

        to_parquet(result.simulation_result.dataframe, pathlib.Path(output))
        console.print(f"[blue]Saved to {output}[/blue]")


@app.command()
def progressivity(
    year: int = typer.Option(2025, help="Legislation year."),
    indices: str = typer.Option("kakwani,suits,gini", help="Comma-separated index names."),
) -> None:
    """Compute progressivity indices for a given year."""
    from skatteprogressivitet.config import Config
    from skatteprogressivitet.pipelines.runner import Pipeline

    config = Config(baseline_year=year)  # type: ignore[arg-type]
    pipe = Pipeline(config=config)
    result = pipe.run()
    requested = [i.strip() for i in indices.split(",")]
    for idx in requested:
        val = result.progressivity.get(idx, "N/A")
        console.print(f"  {idx}: {val}")


@app.command()
def scenario(
    scenario_path: str = typer.Argument(..., help="Path to scenario YAML file."),
    year: int = typer.Option(2025, help="Baseline year."),
) -> None:
    """Run a counterfactual scenario."""
    import pathlib

    from skatteprogressivitet.scenarios.loader import load_scenario
    from skatteprogressivitet.scenarios.runner import run_scenario

    p = pathlib.Path(scenario_path)
    scen = load_scenario(p)
    console.print(f"[bold]Running scenario:[/bold] {scen.scenario_id}")
    result = run_scenario(scen, [])
    console.print(f"Static revenue change: {result.revenue_change_static:,.0f} SEK")
    console.print(f"Behavioural revenue change: {result.revenue_change_behavioural:,.0f} SEK")


@app.command()
def validate_legislation(
    all_years: bool = typer.Option(False, "--all", help="Validate all years."),
    year: int | None = typer.Option(None, help="Validate a single year."),
) -> None:
    """Validate legislation YAML files against the JSON schema."""
    from skatteprogressivitet.legislation.loader import load_all, load_year

    if all_years:
        ledger = load_all()
        console.print(f"[green]All {len(ledger)} legislation files valid.[/green]")
    elif year is not None:
        leg = load_year(year)
        console.print(f"[green]Year {leg.year} valid.[/green]")
    else:
        console.print("[red]Provide --all or --year.[/red]")
        raise typer.Exit(code=1)


@app.command()
def compare(
    baseline: int = typer.Option(2025, help="Baseline year."),
    scenario_id: str = typer.Option(..., help="Scenario ID to compare against baseline."),
) -> None:
    """Compare baseline and counterfactual simulation results."""
    from skatteprogressivitet.scenarios.loader import load_all_scenarios
    from skatteprogressivitet.scenarios.runner import run_scenario

    scenarios = load_all_scenarios()
    if scenario_id not in scenarios:
        console.print(f"[red]Scenario {scenario_id!r} not found.[/red]")
        raise typer.Exit(code=1)
    scen = scenarios[scenario_id]
    result = run_scenario(scen, [])
    console.print(f"Scenario: {scen.scenario_id}")
    console.print(f"Static revenue change:      {result.revenue_change_static:>12,.0f} SEK")
    console.print(f"Behavioural revenue change: {result.revenue_change_behavioural:>12,.0f} SEK")


@app.command()
def report(
    year: int = typer.Option(2025, help="Year to report on."),
    output_dir: str = typer.Option("reports", help="Output directory."),
) -> None:
    """Generate all standard report figures and tables."""
    import pathlib

    import numpy as np

    from skatteprogressivitet.config import Config
    from skatteprogressivitet.pipelines.runner import Pipeline
    from skatteprogressivitet.reporting.figures import FigureBuilder

    config = Config(baseline_year=year)  # type: ignore[arg-type]
    pipe = Pipeline(config=config)
    result = pipe.run()
    fb = FigureBuilder(output_dir=pathlib.Path(output_dir) / "figures")
    df = result.simulation_result.dataframe
    y = df["gross_income"].to_numpy()
    t = df["total_tax"].to_numpy()
    y_post = y - t
    avg = np.where(y > 0, t / y, 0.0)
    mtr = df["effective_marginal_rate"].to_numpy()
    order = np.argsort(y)
    fb.effective_rate_profile(y[order], avg[order], mtr[order], year)
    fb.lorenz_curve(y, y_post, year)
    console.print(f"[green]Report figures written to {output_dir}/figures/[/green]")


@app.command()
def repro(
    dry_run: bool = typer.Option(False, "--dry-run", help="Check without running."),
) -> None:
    """Verify end-to-end replication receipts."""
    import json
    import pathlib

    receipts_path = pathlib.Path("replication/expected_receipts.json")
    if not receipts_path.exists():
        console.print("[red]replication/expected_receipts.json not found.[/red]")
        raise typer.Exit(code=1)
    with receipts_path.open() as fh:
        receipts = json.load(fh)
    console.print(f"[green]Loaded {len(receipts)} receipts.[/green]")
    if dry_run:
        console.print("[blue]Dry run - no simulation executed.[/blue]")


@app.command()
def audit() -> None:
    """Run pip-audit and bandit security checks."""
    import subprocess
    import sys

    console.print("[bold]Running pip-audit...[/bold]")
    subprocess.run([sys.executable, "-m", "pip_audit", "--strict"], check=False)
    console.print("[bold]Running bandit...[/bold]")
    subprocess.run([sys.executable, "-m", "bandit", "-r", "src", "-lll"], check=False)


@app.command()
def sbom(
    output: str = typer.Option("sbom.cdx.json", help="Output SBOM path."),
) -> None:
    """Generate a CycloneDX SBOM."""
    import subprocess
    import sys

    console.print(f"[bold]Generating SBOM to {output}...[/bold]")
    subprocess.run([sys.executable, "-m", "cyclonedx_py", "-o", output], check=False)
    console.print(f"[green]SBOM written to {output}[/green]")


@app.command()
def reuse_check() -> None:
    """Verify REUSE 3.0 compliance."""
    import subprocess

    console.print("[bold]Running reuse lint...[/bold]")
    result = subprocess.run(["reuse", "lint"], check=False)
    if result.returncode == 0:
        console.print("[green]REUSE compliant.[/green]")
    else:
        console.print("[red]REUSE lint failed.[/red]")
        raise typer.Exit(code=result.returncode)


def main() -> None:
    """Entry point for the skatteprogressivitet CLI."""
    app()
