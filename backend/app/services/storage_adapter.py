"""ING-002 Storage adapter abstraction for local filesystem and S3-compatible storage."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Optional
import hashlib
import shutil
import os


class StorageError(Exception):
    """Base exception for storage operations."""
    pass


@dataclass
class StorageConfig:
    """Configuration for storage adapter."""
    backend: str  # "local" or "s3"
    local_root: Optional[str] = None
    s3_endpoint: Optional[str] = None
    s3_bucket: Optional[str] = None
    s3_access_key: Optional[str] = None
    s3_secret_key: Optional[str] = None
    s3_region: Optional[str] = None
    s3_force_path_style: bool = False


@dataclass
class UploadResult:
    """Result of a successful upload."""
    storage_key: str
    checksum: str
    size_bytes: int


class StorageAdapter(ABC):
    """Abstract base class for storage adapters."""

    @abstractmethod
    def store_file(self, storage_key: str, content: bytes) -> str:
        """Store a file to storage.
        
        Args:
            storage_key: Storage key (path within bucket/root)
            content: File content as bytes
            
        Returns:
            Storage key
        """
        pass

    @abstractmethod
    def retrieve_file(self, storage_key: str) -> bytes:
        """Retrieve a file from storage.
        
        Args:
            storage_key: Storage key to retrieve
            
        Returns:
            File content as bytes
        """
        pass

    @abstractmethod
    def delete_file(self, storage_key: str) -> bool:
        """Delete a file from storage.
        
        Args:
            storage_key: Storage key to delete
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    def get_file_path(self, storage_key: str) -> str:
        """Get absolute file path for local access (FFprobe).
        
        Args:
            storage_key: Storage key
            
        Returns:
            Absolute file path
        """
        pass

    @abstractmethod
    def get_presigned_upload_url(self, storage_key: str, expires_in: int = 3600) -> str:
        """Get a presigned URL for direct upload.
        
        Args:
            storage_key: Storage key for the upload
            expires_in: URL expiration time in seconds
            
        Returns:
            Presigned upload URL
        """
        pass

    @abstractmethod
    def get_presigned_download_url(self, storage_key: str, expires_in: int = 3600) -> str:
        """Get a presigned URL for direct download.
        
        Args:
            storage_key: Storage key for the download
            expires_in: URL expiration time in seconds
            
        Returns:
            Presigned download URL
        """
        pass

    @abstractmethod
    def file_exists(self, storage_key: str) -> bool:
        """Check if a file exists in storage.
        
        Args:
            storage_key: Storage key to check
            
        Returns:
            True if file exists, False otherwise
        """
        pass

    @abstractmethod
    def get_file_size(self, storage_key: str) -> int:
        """Get file size in bytes.
        
        Args:
            storage_key: Storage key
            
        Returns:
            File size in bytes
        """
        pass

    @abstractmethod
    def compute_checksum(self, storage_key: str) -> str:
        """Compute SHA256 checksum of a file.
        
        Args:
            storage_key: Storage key
            
        Returns:
            SHA256 hex digest
        """
        pass


def compute_checksum(file_path: Path) -> str:
    """Compute SHA256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


class LocalFilesystemAdapter(StorageAdapter):
    """Local filesystem storage adapter for development and single-node deployments."""

    def __init__(self, config: StorageConfig):
        if not config.local_root:
            raise ValueError("local_root is required for LocalFilesystemAdapter")
        self.root = Path(config.local_root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.config = config

    def _resolve_path(self, storage_key: str) -> Path:
        """Resolve storage key to absolute path within root."""
        # Normalize storage key to prevent directory traversal
        normalized_key = storage_key.lstrip("/")
        resolved = (self.root / normalized_key).resolve()
        # Security check: ensure path is within root
        if not str(resolved).startswith(str(self.root)):
            raise ValueError(f"Storage key attempts directory traversal: {storage_key}")
        return resolved

    def store_file(self, storage_key: str, content: bytes) -> str:
        """Store a file to local filesystem."""
        target_path = self._resolve_path(storage_key)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        target_path.write_bytes(content)
        
        return storage_key

    def retrieve_file(self, storage_key: str) -> bytes:
        """Retrieve a file from local filesystem."""
        source_path = self._resolve_path(storage_key)
        if not source_path.exists():
            raise StorageError(f"File not found: {storage_key}")
        return source_path.read_bytes()

    def delete_file(self, storage_key: str) -> bool:
        """Delete a file from local filesystem."""
        target_path = self._resolve_path(storage_key)
        if target_path.exists():
            target_path.unlink()
            # Clean up empty parent directories
            parent = target_path.parent
            while parent != self.root and parent.exists() and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
            return True
        return False

    def get_file_path(self, storage_key: str) -> str:
        """Get absolute file path for local access (FFprobe)."""
        return str(self._resolve_path(storage_key))

    def file_exists(self, storage_key: str) -> bool:
        """Check if a file exists in local filesystem."""
        return self._resolve_path(storage_key).exists()

    def get_file_size(self, storage_key: str) -> int:
        """Get file size in bytes."""
        path = self._resolve_path(storage_key)
        if not path.exists():
            raise StorageError(f"File not found: {storage_key}")
        return path.stat().st_size

    def compute_checksum(self, storage_key: str) -> str:
        """Compute SHA256 checksum of a file."""
        path = self._resolve_path(storage_key)
        if not path.exists():
            raise StorageError(f"File not found: {storage_key}")
        return compute_checksum(path)

    def get_presigned_upload_url(self, storage_key: str, expires_in: int = 3600) -> str:
        """Local filesystem doesn't support presigned URLs - returns file:// URL with storage key."""
        target_path = self._resolve_path(storage_key)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        return f"file://{target_path}?key={storage_key}"

    def get_presigned_download_url(self, storage_key: str, expires_in: int = 3600) -> str:
        """Local filesystem doesn't support presigned URLs - returns file:// URL with storage key."""
        target_path = self._resolve_path(storage_key)
        if not target_path.exists():
            raise StorageError(f"File not found: {storage_key}")
        return f"file://{target_path}?key={storage_key}"


def create_storage_adapter(config: StorageConfig) -> StorageAdapter:
    """Factory function to create storage adapter from config."""
    if config.backend == "local":
        return LocalFilesystemAdapter(config)
    elif config.backend == "s3":
        from .s3_adapter import S3Adapter
        return S3Adapter(config)
    else:
        raise ValueError(f"Unknown storage backend: {config.backend}")
