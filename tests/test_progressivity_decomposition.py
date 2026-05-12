"""Tests for progressivity decomposition."""

from __future__ import annotations

import numpy as np
import pytest

from skatteprogressivitet.progressivity.decomposition import (
    decompose_kakwani,
    mechanical_vs_behavioural,
    shapley_decomposition,
)


@pytest.fixture
def system():
    rng = np.random.default_rng(42)
    y = rng.lognormal(12, 0.7, 200)
    kommunal = y * 0.32
    statlig = np.maximum(0, (y - 500_000)) * 0.20
    jsa = np.minimum(y * 0.05, 15_000)
    return y, {"kommunal": kommunal, "statlig": statlig, "jsa": -jsa}


def test_decompose_kakwani_has_total(system) -> None:
    y, components = system
    result = decompose_kakwani(y, {k: v for k, v in components.items() if k != "jsa"})
    assert "total" in result


def test_decompose_kakwani_components_sum_to_total(system) -> None:
    y, components = system
    pos_components = {k: v for k, v in components.items() if k != "jsa"}
    result = decompose_kakwani(y, pos_components)
    component_sum = sum(v for k, v in result.items() if k != "total")
    assert component_sum == pytest.approx(result["total"], abs=1e-8)


def test_mechanical_vs_behavioural_keys(system) -> None:
    y, components = system
    t = components["kommunal"] + components["statlig"]
    result = mechanical_vs_behavioural(y, t, y * 1.01, t * 0.99)
    assert set(result.keys()) == {"mechanical", "behavioural", "total"}


def test_shapley_equals_rao_decomposition(system) -> None:
    y, components = system
    pos = {k: v for k, v in components.items() if k != "jsa"}
    rao = decompose_kakwani(y, pos)
    shapley = shapley_decomposition(y, pos)
    assert shapley["total"] == pytest.approx(rao["total"], abs=1e-8)
