"""Storage port placeholder."""

from typing import Protocol


class StoragePort(Protocol):
    def put_object(self, key: str, source_path: str) -> str:
        raise NotImplementedError("Placeholder scaffold.")

    def get_object(self, key: str) -> str:
        raise NotImplementedError("Placeholder scaffold.")
