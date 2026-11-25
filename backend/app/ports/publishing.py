"""Publishing port placeholder."""

from typing import Protocol


class PublishingPort(Protocol):
    def reconcile(self, attempt_id: str) -> dict:
        raise NotImplementedError("Placeholder scaffold.")
