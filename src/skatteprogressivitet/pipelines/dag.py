"""Content-addressed DAG for deterministic pipeline execution.

Implements a minimal directed acyclic graph where each task's output is
identified by a SHA-256 hash of its inputs and parameters.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Callable


class Task:
    """A single node in the pipeline DAG.

    Attributes:
        name: Task name.
        fn: Callable that executes the task.
        inputs: Mapping from parameter name to value.
        output_key: Key under which this task's output is stored.
    """

    def __init__(
        self,
        name: str,
        fn: Callable[..., Any],
        inputs: dict[str, Any],
        output_key: str = "",
    ) -> None:
        """Initialise a Task.

        Args:
            name: Task name.
            fn: Task function.
            inputs: Input parameters.
            output_key: Output storage key.
        """
        self.name = name
        self.fn = fn
        self.inputs = inputs
        self.output_key = output_key or name

    def content_hash(self) -> str:
        """Compute a SHA-256 content-address for this task's inputs.

        Returns:
            Hex-encoded SHA-256 hash string.

        Example:
            >>> t = Task("test", lambda: None, {"a": 1})
            >>> len(t.content_hash())
            64
        """
        payload = json.dumps(
            {"name": self.name, "inputs": str(self.inputs)},
            sort_keys=True,
        ).encode()
        return hashlib.sha256(payload).hexdigest()

    def run(self) -> Any:
        """Execute the task function with the stored inputs.

        Returns:
            Task output.
        """
        return self.fn(**self.inputs)


class DAG:
    """A simple directed acyclic graph of pipeline tasks.

    Attributes:
        tasks: Ordered list of tasks.
    """

    def __init__(self) -> None:
        """Initialise an empty DAG."""
        self.tasks: list[Task] = []
        self._outputs: dict[str, Any] = {}

    def add_task(self, task: Task) -> "DAG":
        """Add a task to the DAG.

        Args:
            task: Task to add.

        Returns:
            Self (for method chaining).

        Example:
            >>> dag = DAG()
            >>> t = Task("noop", lambda: None, {})
            >>> dag.add_task(t) is dag
            True
        """
        self.tasks.append(task)
        return self

    def run_all(self) -> dict[str, Any]:
        """Execute all tasks in order and collect outputs.

        Returns:
            Mapping from output key to task output.
        """
        for task in self.tasks:
            self._outputs[task.output_key] = task.run()
        return dict(self._outputs)

    def get_output(self, key: str) -> Any:
        """Retrieve a stored task output.

        Args:
            key: Output key.

        Returns:
            Stored output value.

        Raises:
            KeyError: If the key has not been computed yet.
        """
        return self._outputs[key]
