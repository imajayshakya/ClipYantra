"""AI/provider port placeholder."""

from typing import Protocol


class ProviderPort(Protocol):
    def execute(self, task: str, payload: dict) -> dict:
        raise NotImplementedError("Placeholder scaffold.")
