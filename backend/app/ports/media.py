"""Media pipeline port placeholder."""

from typing import Protocol


class MediaPort(Protocol):
    def validate_media(self, source_path: str) -> dict:
        raise NotImplementedError("Placeholder scaffold.")
