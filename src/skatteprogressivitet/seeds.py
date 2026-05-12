"""Deterministic seed management for Skatteprogressivitet.

All randomness in the package flows through this module. Use
:func:`set_global_seed` to initialise the global seed at process startup and
:func:`derive_seed` to obtain a deterministic child seed for a named sub-task.
"""

from __future__ import annotations

import hashlib

SYNTHETIC_SEED: int = 19960307
MODEL_SEED: int = 20251008
BOOTSTRAP_SEED: int = 7
SCENARIO_SEED: int = 1991

_NAMESPACES: frozenset[str] = frozenset(
    ["bootstrap", "eti_calibration", "bunching_window", "scenario_perturbation"]
)

_global_seed: int = MODEL_SEED


def set_global_seed(seed: int) -> None:
    """Set the module-level global seed.

    Args:
        seed: Integer seed value.

    Example:
        >>> set_global_seed(42)
        >>> get_global_seed()
        42
    """
    global _global_seed  # noqa: PLW0603
    _global_seed = seed


def get_global_seed() -> int:
    """Return the current global seed.

    Returns:
        Current global seed integer.

    Example:
        >>> set_global_seed(MODEL_SEED)
        >>> get_global_seed() == MODEL_SEED
        True
    """
    return _global_seed


def derive_seed(namespace: str, index: int = 0) -> int:
    """Derive a deterministic child seed from the global seed and a namespace.

    Uses SHA-256 to hash the concatenation of the global seed, namespace, and
    index, returning a 32-bit integer. This ensures that different sub-tasks
    receive independent, reproducible seeds without manual management.

    Args:
        namespace: Named sub-task namespace. Should be one of the documented
            namespaces: ``bootstrap``, ``eti_calibration``, ``bunching_window``,
            ``scenario_perturbation``.
        index: Optional integer to further differentiate seeds within a namespace.

    Returns:
        A 32-bit non-negative integer seed.

    Example:
        >>> set_global_seed(MODEL_SEED)
        >>> s = derive_seed("bootstrap", 0)
        >>> isinstance(s, int)
        True
        >>> 0 <= s < 2**32
        True
    """
    payload = f"{_global_seed}:{namespace}:{index}".encode()
    digest = hashlib.sha256(payload).digest()
    return int.from_bytes(digest[:4], byteorder="big")
