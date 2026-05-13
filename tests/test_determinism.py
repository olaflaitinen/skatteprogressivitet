"""Determinism tests: identical inputs must produce identical outputs."""

from __future__ import annotations

import numpy as np
import pytest

from skatteprogressivitet.progressivity.indices import gini, kakwani
from skatteprogressivitet.seeds import MODEL_SEED, set_global_seed
from skatteprogressivitet.simulator.engine import Simulator

POPULATION = [
    {
        "labour_income": float(i * 50_000),
        "capital_income": 0.0,
        "age": 30 + i % 20,
        "self_employed": False,
    }
    for i in range(1, 21)
]


def test_simulator_deterministic_across_runs() -> None:
    set_global_seed(MODEL_SEED)
    sim1 = Simulator()
    r1 = sim1.run(POPULATION, year=2025, behavioural="none")

    set_global_seed(MODEL_SEED)
    sim2 = Simulator()
    r2 = sim2.run(POPULATION, year=2025, behavioural="none")

    t1 = r1.dataframe["total_tax"].to_list()
    t2 = r2.dataframe["total_tax"].to_list()
    assert t1 == pytest.approx(t2)


def test_progressivity_indices_deterministic() -> None:
    rng = np.random.default_rng(19960307)
    y = rng.lognormal(12, 0.7, 200)
    t = y * 0.28

    k1 = kakwani(y, t)
    k2 = kakwani(y, t)
    assert k1 == pytest.approx(k2)

    g1 = gini(y)
    g2 = gini(y)
    assert g1 == pytest.approx(g2)


def test_behavioural_simulation_deterministic() -> None:
    set_global_seed(MODEL_SEED)
    sim1 = Simulator()
    r1 = sim1.run(POPULATION, year=2025, behavioural="eti")

    set_global_seed(MODEL_SEED)
    sim2 = Simulator()
    r2 = sim2.run(POPULATION, year=2025, behavioural="eti")

    t1 = r1.dataframe["total_tax"].to_list()
    t2 = r2.dataframe["total_tax"].to_list()
    assert t1 == pytest.approx(t2)
