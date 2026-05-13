"""Structured logging configuration for Skatteprogressivitet.

Configures structlog to emit JSON in CI environments and human-readable console
output when running interactively. Detect CI by the presence of the ``CI``
environment variable.
"""

from __future__ import annotations

import logging
import os
import sys

import structlog


def configure_logging(level: str = "INFO") -> None:
    """Configure structlog for the current environment.

    Uses JSON rendering when the ``CI`` environment variable is set (truthy),
    and console rendering otherwise.

    Args:
        level: Standard logging level name (e.g. ``"INFO"``, ``"DEBUG"``).

    Example:
        >>> configure_logging("WARNING")
    """
    is_ci = bool(os.environ.get("CI"))

    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if is_ci:
        renderer: structlog.types.Processor = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(level)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Return a bound structlog logger for the given name.

    Args:
        name: Logger name, typically ``__name__``.

    Returns:
        A configured structlog bound logger.

    Example:
        >>> log = get_logger(__name__)
        >>> log is not None
        True
    """
    return structlog.get_logger(name)  # type: ignore[no-any-return]
