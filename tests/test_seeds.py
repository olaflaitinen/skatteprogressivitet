"""Tests for the seed management module."""

from __future__ import annotations

from skatteprogressivitet.seeds import (
    BOOTSTRAP_SEED,
    MODEL_SEED,
    SYNTHETIC_SEED,
    derive_seed,
    get_global_seed,
    set_global_seed,
)


def test_default_seeds_have_expected_values() -> None:
    assert MODEL_SEED == 20251008
    assert SYNTHETIC_SEED == 19960307
    assert BOOTSTRAP_SEED == 7


def test_set_and_get_global_seed() -> None:
    set_global_seed(42)
    assert get_global_seed() == 42
    set_global_seed(MODEL_SEED)


def test_derive_seed_is_deterministic() -> None:
    set_global_seed(MODEL_SEED)
    s1 = derive_seed("bootstrap", 0)
    s2 = derive_seed("bootstrap", 0)
    assert s1 == s2


def test_derive_seed_different_namespaces_differ() -> None:
    set_global_seed(MODEL_SEED)
    s1 = derive_seed("bootstrap", 0)
    s2 = derive_seed("eti_calibration", 0)
    assert s1 != s2


def test_derive_seed_in_uint32_range() -> None:
    set_global_seed(MODEL_SEED)
    s = derive_seed("bunching_window", 5)
    assert 0 <= s < 2**32


def test_derive_seed_changes_with_global_seed() -> None:
    set_global_seed(1)
    s1 = derive_seed("bootstrap")
    set_global_seed(2)
    s2 = derive_seed("bootstrap")
    assert s1 != s2
    set_global_seed(MODEL_SEED)


def test_derive_seed_changes_with_index() -> None:
    set_global_seed(MODEL_SEED)
    s0 = derive_seed("bootstrap", 0)
    s1 = derive_seed("bootstrap", 1)
    assert s0 != s1
