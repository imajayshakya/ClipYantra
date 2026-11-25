"""Placeholder domain interfaces. No business behavior is implemented."""

from typing import Protocol


class ClipWorkflowPort(Protocol):
    def process_source(self, source_id: str) -> str:
        raise NotImplementedError("Placeholder scaffold.")
