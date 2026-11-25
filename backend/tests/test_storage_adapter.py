"""Unit tests for storage adapters (ING-002 AC4, AC5)."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock, MagicMock
import hashlib

from app.services.storage_adapter import (
    StorageAdapter,
    LocalFilesystemAdapter,
    StorageConfig,
    create_storage_adapter,
    StorageError,
)
from app.services.s3_adapter import S3Adapter


class TestStorageConfig:
    """Test StorageConfig dataclass."""

    def test_local_config(self):
        """Test local storage configuration."""
        config = StorageConfig(backend="local", local_root="/tmp/storage")

        assert config.backend == "local"
        assert config.local_root == "/tmp/storage"
        assert config.s3_endpoint is None

    def test_s3_config(self):
        """Test S3 storage configuration."""
        config = StorageConfig(
            backend="s3",
            s3_endpoint="https://s3.amazonaws.com",
            s3_bucket="test-bucket",
            s3_access_key="access",
            s3_secret_key="secret",
            s3_region="us-east-1",
        )

        assert config.backend == "s3"
        assert config.s3_endpoint == "https://s3.amazonaws.com"
        assert config.s3_bucket == "test-bucket"
        assert config.s3_access_key == "access"
        assert config.s3_secret_key == "secret"
        assert config.s3_region == "us-east-1"

    def test_s3_config_minio(self):
        """Test S3 config for MinIO (path-style)."""
        config = StorageConfig(
            backend="s3",
            s3_endpoint="http://localhost:9000",
            s3_bucket="test-bucket",
            s3_access_key="minioadmin",
            s3_secret_key="minioadmin",
            s3_force_path_style=True,
        )

        assert config.s3_force_path_style is True


class TestLocalFilesystemAdapter:
    """Test LocalFilesystemAdapter implementation."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def adapter(self, temp_dir):
        """Create adapter with temp directory."""
        config = StorageConfig(backend="local", local_root=str(temp_dir))
        return LocalFilesystemAdapter(config)

    def test_store_file(self, adapter, temp_dir):
        """AC4: Store file to local filesystem."""
        content = b"test file content"
        storage_key = "workspaces/123/sources/456/original/abc123"

        result_key = adapter.store_file(storage_key, content)

        assert result_key == storage_key
        file_path = temp_dir / storage_key
        assert file_path.exists()
        assert file_path.read_bytes() == content

    def test_store_file_creates_directories(self, adapter, temp_dir):
        """Test that nested directories are created."""
        content = b"nested file"
        storage_key = "a/b/c/d/e/file.bin"

        result_key = adapter.store_file(storage_key, content)

        file_path = temp_dir / storage_key
        assert file_path.exists()
        assert file_path.read_bytes() == content

    def test_retrieve_file(self, adapter, temp_dir):
        """AC4: Retrieve file from local filesystem."""
        content = b"retrieve test content"
        storage_key = "test/retrieve/file.bin"
        file_path = temp_dir / storage_key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)

        retrieved = adapter.retrieve_file(storage_key)

        assert retrieved == content

    def test_retrieve_nonexistent_file(self, adapter):
        """Test retrieving nonexistent file raises error."""
        with pytest.raises(StorageError, match="File not found"):
            adapter.retrieve_file("nonexistent/file.bin")

    def test_delete_file(self, adapter, temp_dir):
        """AC4: Delete file from local filesystem."""
        content = b"delete test"
        storage_key = "test/delete/file.bin"
        file_path = temp_dir / storage_key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)

        adapter.delete_file(storage_key)

        assert not file_path.exists()

    def test_delete_nonexistent_file(self, adapter):
        """Test deleting nonexistent file (should not raise)."""
        # Should not raise - idempotent delete
        adapter.delete_file("nonexistent/file.bin")

    def test_get_file_path(self, adapter, temp_dir):
        """AC4: Get absolute file path."""
        storage_key = "test/path/file.bin"
        expected_path = temp_dir / storage_key

        result_path = adapter.get_file_path(storage_key)

        assert result_path == str(expected_path)

    def test_get_presigned_upload_url_local(self, adapter):
        """AC5: Get presigned URL for local (returns file:// URL)."""
        storage_key = "test/presign/file.bin"

        url = adapter.get_presigned_upload_url(storage_key, expires_in=3600)

        assert url.startswith("file://")
        assert storage_key in url

    def test_get_presigned_download_url_local(self, adapter, temp_dir):
        """AC5: Get presigned download URL for local."""
        storage_key = "test/presign/file.bin"
        file_path = temp_dir / storage_key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(b"content")

        url = adapter.get_presigned_download_url(storage_key, expires_in=3600)

        assert url.startswith("file://")
        assert storage_key in url

    def test_file_exists(self, adapter, temp_dir):
        """Test file existence check."""
        storage_key = "test/exists/file.bin"
        file_path = temp_dir / storage_key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(b"content")

        assert adapter.file_exists(storage_key) is True
        assert adapter.file_exists("nonexistent/file.bin") is False

    def test_get_file_size(self, adapter, temp_dir):
        """Test getting file size."""
        content = b"x" * 1000
        storage_key = "test/size/file.bin"
        file_path = temp_dir / storage_key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)

        size = adapter.get_file_size(storage_key)

        assert size == 1000

    def test_get_file_size_nonexistent(self, adapter):
        """Test getting size of nonexistent file."""
        with pytest.raises(StorageError, match="File not found"):
            adapter.get_file_size("nonexistent/file.bin")

    def test_compute_checksum(self, adapter, temp_dir):
        """Test computing SHA-256 checksum."""
        content = b"checksum test content"
        storage_key = "test/checksum/file.bin"
        file_path = temp_dir / storage_key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)

        expected = hashlib.sha256(content).hexdigest()
        result = adapter.compute_checksum(storage_key)

        assert result == expected

    def test_compute_checksum_nonexistent(self, adapter):
        """Test checksum of nonexistent file."""
        with pytest.raises(StorageError, match="File not found"):
            adapter.compute_checksum("nonexistent/file.bin")


class TestStorageAdapterFactory:
    """Test create_storage_adapter factory function."""

    def test_create_local_adapter(self):
        """Test creating local adapter via factory."""
        config = StorageConfig(backend="local", local_root="/tmp/test")

        adapter = create_storage_adapter(config)

        assert isinstance(adapter, LocalFilesystemAdapter)
        assert adapter.config == config

    def test_create_s3_adapter(self):
        """Test creating S3 adapter via factory."""
        config = StorageConfig(
            backend="s3",
            s3_endpoint="https://s3.amazonaws.com",
            s3_bucket="test-bucket",
            s3_access_key="access",
            s3_secret_key="secret",
        )

        # S3Adapter is imported locally in the factory function, so we patch at import site
        with patch('app.services.s3_adapter.S3Adapter') as mock_s3:
            mock_instance = Mock()
            mock_s3.return_value = mock_instance

            adapter = create_storage_adapter(config)

            assert adapter == mock_instance
            mock_s3.assert_called_once_with(config)

    def test_create_unknown_backend_raises(self):
        """Test unknown backend raises error."""
        config = StorageConfig(backend="unknown")

        with pytest.raises(ValueError, match="Unknown storage backend"):
            create_storage_adapter(config)


class TestS3Adapter:
    """Test S3Adapter implementation (mocked)."""

    @pytest.fixture
    def s3_config(self):
        """Create S3 configuration for testing."""
        return StorageConfig(
            backend="s3",
            s3_endpoint="https://s3.amazonaws.com",
            s3_bucket="test-bucket",
            s3_access_key="test-access",
            s3_secret_key="test-secret",
            s3_region="us-east-1",
        )

    @pytest.fixture
    def s3_adapter(self, s3_config):
        """Create S3 adapter with mocked boto3 client."""
        with patch('app.services.s3_adapter.boto3.client') as mock_client:
            mock_s3 = Mock()
            mock_client.return_value = mock_s3
            adapter = S3Adapter(s3_config)
            adapter._client = mock_s3
            yield adapter, mock_s3

    def test_store_file_s3(self, s3_adapter):
        """Test storing file to S3."""
        adapter, mock_client = s3_adapter
        content = b"s3 test content"
        storage_key = "test/s3/file.bin"

        result = adapter.store_file(storage_key, content)

        assert result == storage_key
        mock_client.put_object.assert_called_once()
        call_args = mock_client.put_object.call_args
        assert call_args.kwargs['Bucket'] == "test-bucket"
        assert call_args.kwargs['Key'] == storage_key
        assert call_args.kwargs['Body'] == content

    def test_retrieve_file_s3(self, s3_adapter):
        """Test retrieving file from S3."""
        adapter, mock_client = s3_adapter
        storage_key = "test/s3/file.bin"
        mock_body = Mock()
        mock_body.read.return_value = b"retrieved content"
        mock_client.get_object.return_value = {'Body': mock_body}

        result = adapter.retrieve_file(storage_key)

        assert result == b"retrieved content"
        mock_client.get_object.assert_called_once_with(
            Bucket="test-bucket",
            Key=storage_key
        )

    def test_delete_file_s3(self, s3_adapter):
        """Test deleting file from S3."""
        adapter, mock_client = s3_adapter
        storage_key = "test/s3/file.bin"

        adapter.delete_file(storage_key)

        mock_client.delete_object.assert_called_once_with(
            Bucket="test-bucket",
            Key=storage_key
        )

    def test_get_presigned_upload_url_s3(self, s3_adapter):
        """AC5: Get presigned upload URL for S3."""
        adapter, mock_client = s3_adapter
        storage_key = "test/s3/file.bin"
        expected_url = "https://s3.amazonaws.com/test-bucket/test/s3/file.bin?X-Amz-Algorithm=..."
        mock_client.generate_presigned_url.return_value = expected_url

        url = adapter.get_presigned_upload_url(storage_key, expires_in=3600)

        assert url == expected_url
        mock_client.generate_presigned_url.assert_called_once()
        call_args = mock_client.generate_presigned_url.call_args
        # boto3 uses keyword arguments
        assert call_args.kwargs['ClientMethod'] == 'put_object'
        assert call_args.kwargs['Params']['Bucket'] == 'test-bucket'
        assert call_args.kwargs['Params']['Key'] == storage_key
        assert call_args.kwargs['ExpiresIn'] == 3600

    def test_get_presigned_download_url_s3(self, s3_adapter):
        """AC5: Get presigned download URL for S3."""
        adapter, mock_client = s3_adapter
        storage_key = "test/s3/file.bin"
        expected_url = "https://s3.amazonaws.com/test-bucket/test/s3/file.bin?X-Amz-Algorithm=..."
        mock_client.generate_presigned_url.return_value = expected_url

        url = adapter.get_presigned_download_url(storage_key, expires_in=3600)

        assert url == expected_url
        mock_client.generate_presigned_url.assert_called_once()
        call_args = mock_client.generate_presigned_url.call_args
        # boto3 uses keyword arguments
        assert call_args.kwargs['ClientMethod'] == 'get_object'
        assert call_args.kwargs['Params']['Bucket'] == 'test-bucket'
        assert call_args.kwargs['Params']['Key'] == storage_key
        assert call_args.kwargs['ExpiresIn'] == 3600

    def test_file_exists_s3(self, s3_adapter):
        """Test file existence check on S3."""
        adapter, mock_client = s3_adapter
        storage_key = "test/s3/file.bin"
        mock_client.head_object.return_value = {}

        result = adapter.file_exists(storage_key)

        assert result is True
        mock_client.head_object.assert_called_once_with(
            Bucket="test-bucket",
            Key=storage_key
        )

    def test_file_exists_s3_not_found(self, s3_adapter):
        """Test file existence check when file doesn't exist."""
        adapter, mock_client = s3_adapter
        storage_key = "test/s3/file.bin"
        from botocore.exceptions import ClientError
        mock_client.head_object.side_effect = ClientError(
            {'Error': {'Code': '404'}}, 'HeadObject'
        )

        result = adapter.file_exists(storage_key)

        assert result is False

    def test_get_file_size_s3(self, s3_adapter):
        """Test getting file size from S3."""
        adapter, mock_client = s3_adapter
        storage_key = "test/s3/file.bin"
        mock_client.head_object.return_value = {'ContentLength': 1024}

        size = adapter.get_file_size(storage_key)

        assert size == 1024

    def test_compute_checksum_s3(self, s3_adapter):
        """Test computing checksum for S3 object (downloads and hashes)."""
        adapter, mock_client = s3_adapter
        storage_key = "test/s3/file.bin"
        mock_body = Mock()
        mock_body.read.return_value = b"checksum content"
        mock_client.get_object.return_value = {'Body': mock_body}

        result = adapter.compute_checksum(storage_key)

        import hashlib
        expected = hashlib.sha256(b"checksum content").hexdigest()
        assert result == expected


class TestStorageAdapterInterface:
    """Test that adapters implement the abstract interface correctly."""

    def test_local_adapter_implements_interface(self):
        """Verify LocalFilesystemAdapter implements StorageAdapter."""
        config = StorageConfig(backend="local", local_root="/tmp")
        adapter = LocalFilesystemAdapter(config)

        assert isinstance(adapter, StorageAdapter)
        # Check all abstract methods are implemented
        assert hasattr(adapter, 'store_file')
        assert hasattr(adapter, 'retrieve_file')
        assert hasattr(adapter, 'delete_file')
        assert hasattr(adapter, 'get_file_path')
        assert hasattr(adapter, 'get_presigned_upload_url')
        assert hasattr(adapter, 'get_presigned_download_url')
        assert hasattr(adapter, 'file_exists')
        assert hasattr(adapter, 'get_file_size')
        assert hasattr(adapter, 'compute_checksum')

    def test_s3_adapter_implements_interface(self):
        """Verify S3Adapter implements StorageAdapter."""
        config = StorageConfig(
            backend="s3",
            s3_endpoint="https://s3.amazonaws.com",
            s3_bucket="test",
            s3_access_key="access",
            s3_secret_key="secret",
        )
        with patch('app.services.s3_adapter.boto3.client'):
            adapter = S3Adapter(config)

        assert isinstance(adapter, StorageAdapter)
        assert hasattr(adapter, 'store_file')
        assert hasattr(adapter, 'retrieve_file')
        assert hasattr(adapter, 'delete_file')
        assert hasattr(adapter, 'get_file_path')
        assert hasattr(adapter, 'get_presigned_upload_url')
        assert hasattr(adapter, 'get_presigned_download_url')
        assert hasattr(adapter, 'file_exists')
        assert hasattr(adapter, 'get_file_size')
        assert hasattr(adapter, 'compute_checksum')