"""Explicitly disabled adapters. No external services are contacted."""


class DisabledStorageAdapter:
    def put_object(self, key: str, source_path: str) -> str:
        raise NotImplementedError("Storage adapter not implemented.")

    def get_object(self, key: str) -> str:
        raise NotImplementedError("Storage adapter not implemented.")


class DisabledProviderAdapter:
    def execute(self, task: str, payload: dict) -> dict:
        raise NotImplementedError("Provider adapter not implemented.")


class DisabledPublishingAdapter:
    def reconcile(self, attempt_id: str) -> dict:
        raise NotImplementedError("Publishing adapter not implemented.")
