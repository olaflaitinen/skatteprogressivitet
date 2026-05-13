"""Tests for the pipeline runner."""

from __future__ import annotations

import pytest

from skatteprogressivitet.pipelines.runner import Pipeline, PipelineResult


@pytest.fixture
def small_pop():
    return [
        {"labour_income": 300_000.0, "capital_income": 0.0, "age": 35, "self_employed": False},
        {"labour_income": 600_000.0, "capital_income": 0.0, "age": 50, "self_employed": False},
    ]


def test_pipeline_returns_result(small_pop) -> None:
    pipe = Pipeline()
    result = pipe.run(taxpayers=small_pop, scenarios=[])
    assert isinstance(result, PipelineResult)


def test_pipeline_progressivity_keys(small_pop) -> None:
    pipe = Pipeline()
    result = pipe.run(taxpayers=small_pop, scenarios=[])
    for key in ["kakwani", "suits", "gini_pre", "gini_post"]:
        assert key in result.progressivity


def test_pipeline_progressivity_finite(small_pop) -> None:
    pipe = Pipeline()
    result = pipe.run(taxpayers=small_pop, scenarios=[])
    import math

    for val in result.progressivity.values():
        assert math.isfinite(val)


def test_pipeline_scenario_results_dict(small_pop) -> None:
    pipe = Pipeline()
    result = pipe.run(taxpayers=small_pop, scenarios=["raise-brytpunkt"])
    assert isinstance(result.scenario_results, dict)
