"""ING-002 S3-compatible storage adapter for production deployments."""

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from .storage_adapter import StorageAdapter, StorageConfig, StorageError


@dataclass
class S3Config:
    """S3-specific configuration."""
    endpoint_url: str
    bucket: str
    access_key: str
    secret_key: str
    region: str = "us-east-1"


class S3Adapter(StorageAdapter):
    """S3-compatible storage adapter (AWS S3, MinIO, etc.)."""

    def __init__(self, config: StorageConfig):
        if not all([config.s3_endpoint, config.s3_bucket, config.s3_access_key, config.s3_secret_key]):
            raise ValueError("S3 config requires endpoint, bucket, access_key, and secret_key")
        
        self.config = S3Config(
            endpoint_url=config.s3_endpoint,
            bucket=config.s3_bucket,
            access_key=config.s3_access_key,
            secret_key=config.s3_secret_key,
            region=config.s3_region or "us-east-1",
        )
        
        self.client = boto3.client(
            "s3",
            endpoint_url=self.config.endpoint_url,
            aws_access_key_id=self.config.access_key,
            aws_secret_access_key=self.config.secret_key,
            region_name=self.config.region,
            config=Config(signature_version="s3v4"),
        )
        
        # Ensure bucket exists
        self._ensure_bucket()

    def _ensure_bucket(self) -> None:
        """Create bucket if it doesn't exist."""
        try:
            self.client.head_bucket(Bucket=self.config.bucket)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                self.client.create_bucket(Bucket=self.config.bucket)
            else:
                raise

    def _compute_checksum(self, content: bytes) -> str:
        """Compute SHA256 checksum of bytes."""
        sha256 = hashlib.sha256()
        sha256.update(content)
        return sha256.hexdigest()

    def store_file(self, storage_key: str, content: bytes) -> str:
        """Store a file to S3."""
        self.client.put_object(
            Bucket=self.config.bucket,
            Key=storage_key,
            Body=content
        )
        return storage_key

    def retrieve_file(self, storage_key: str) -> bytes:
        """Retrieve a file from S3."""
        try:
            response = self.client.get_object(Bucket=self.config.bucket, Key=storage_key)
            return response['Body'].read()
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise StorageError(f"File not found: {storage_key}")
            raise

    def delete_file(self, storage_key: str) -> bool:
        """Delete a file from S3."""
        try:
            self.client.delete_object(Bucket=self.config.bucket, Key=storage_key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise

    def get_file_path(self, storage_key: str) -> str:
        """Get absolute file path for local access (FFprobe).
        
        S3 doesn't support local file paths. This raises NotImplementedError.
        For FFprobe validation, download to temp file first.
        """
        raise NotImplementedError("S3Adapter does not support local file paths. Download to temp file for FFprobe.")

    def file_exists(self, storage_key: str) -> bool:
        """Check if a file exists in S3."""
        try:
            self.client.head_object(Bucket=self.config.bucket, Key=storage_key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise

    def get_file_size(self, storage_key: str) -> int:
        """Get file size in bytes."""
        try:
            response = self.client.head_object(Bucket=self.config.bucket, Key=storage_key)
            return response['ContentLength']
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                raise StorageError(f"File not found: {storage_key}")
            raise

    def compute_checksum(self, storage_key: str) -> str:
        """Compute SHA256 checksum of a file in S3."""
        try:
            response = self.client.get_object(Bucket=self.config.bucket, Key=storage_key)
            content = response['Body'].read()
            return self._compute_checksum(content)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                raise StorageError(f"File not found: {storage_key}")
            raise

    def get_presigned_upload_url(self, storage_key: str, expires_in: int = 3600) -> str:
        """Get a presigned URL for direct upload to S3."""
        return self.client.generate_presigned_url(
                ClientMethod="put_object",
            Params={"Bucket": self.config.bucket, "Key": storage_key},
            ExpiresIn=expires_in,
        )

    def get_presigned_download_url(self, storage_key: str, expires_in: int = 3600) -> str:
        """Get a presigned URL for direct download from S3."""
        return self.client.generate_presigned_url(
                ClientMethod="get_object",
            Params={"Bucket": self.config.bucket, "Key": storage_key},
            ExpiresIn=expires_in,
        )