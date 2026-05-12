"""Benchmarks for the microsimulation engine.

Run with:
    uv run pytest benchmarks/ --benchmark-only
"""

from __future__ import annotations

import pytest

from skatteprogressivitet.simulator.engine import Simulator
from skatteprogressivitet.ingestion.lisa import synthetic_lisa
from skatteprogressivitet.seeds import SYNTHETIC_SEED


@pytest.fixture(scope="module")
def population_1k():
    df = synthetic_lisa(n=1000, years=[2025], seed=SYNTHETIC_SEED)
    return df.to_dicts()


@pytest.fixture(scope="module")
def population_10k():
    df = synthetic_lisa(n=10_000, years=[2025], seed=SYNTHETIC_SEED)
    return df.to_dicts()


def test_bench_simulate_1k_static(benchmark, population_1k) -> None:
    sim = Simulator()
    benchmark(sim.run, population_1k, year=2025, behavioural="none")


def test_bench_simulate_1k_eti(benchmark, population_1k) -> None:
    sim = Simulator()
    benchmark(sim.run, population_1k, year=2025, behavioural="eti")


def test_bench_simulate_10k_static(benchmark, population_10k) -> None:
    sim = Simulator()
    benchmark(sim.run, population_10k, year=2025, behavioural="none")
