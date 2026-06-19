"""
Artifact Storage System for Hermes Agent.

Provides a unified interface for storing task-related artifacts (files, logs,
checkpoints) either on the local filesystem or in a remote S3-compatible bucket.

Configuration:
- HERMES_ARTIFACT_BACKEND: 'local' (default) or 's3'
- HERMES_S3_BUCKET: S3 bucket name
- HERMES_S3_PREFIX: Global prefix (e.g., 'hermes/')
- HERMES_S3_REGION: AWS region
"""

import os
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from hermes_constants import get_hermes_home

logger = logging.getLogger(__name__)

class ArtifactStore(ABC):
    """Abstract base class for task artifact storage."""

    @abstractmethod
    def store_file(self, project: str, task_id: str, local_path: Path, remote_filename: Optional[str] = None) -> str:
        """Store a local file and return its storage URI (file:// or s3://)."""
        pass

    @abstractmethod
    def store_content(self, project: str, task_id: str, content: str, filename: str) -> str:
        """Store raw string content as a file and return its storage URI."""
        pass

class LocalArtifactStore(ArtifactStore):
    """Stores artifacts in the local HERMES_HOME/artifacts directory."""

    def __init__(self, root: Optional[Path] = None):
        self.root = root or (get_hermes_home() / "artifacts")
        self.root.mkdir(parents=True, exist_ok=True)

    def _get_path(self, project: str, task_id: str) -> Path:
        p = self.root / project / task_id
        p.mkdir(parents=True, exist_ok=True)
        return p

    def store_file(self, project: str, task_id: str, local_path: Path, remote_filename: Optional[str] = None) -> str:
        target_dir = self._get_path(project, task_id)
        filename = remote_filename or local_path.name
        target_path = target_dir / filename
        
        import shutil
        shutil.copy2(local_path, target_path)
        return f"file://{target_path.absolute()}"

    def store_content(self, project: str, task_id: str, content: str, filename: str) -> str:
        target_dir = self._get_path(project, task_id)
        target_path = target_dir / filename
        target_path.write_text(content, encoding="utf-8")
        return f"file://{target_path.absolute()}"

class S3ArtifactStore(ArtifactStore):
    """Stores artifacts in an S3 bucket."""

    def __init__(self, bucket: str, prefix: str = "", region: Optional[str] = None):
        import boto3
        from botocore.config import Config
        
        self.bucket = bucket
        self.prefix = prefix.strip("/")
        
        s3_config = Config(region_name=region) if region else None
        self.client = boto3.client("s3", config=s3_config)

    def _get_key(self, project: str, task_id: str, filename: str) -> str:
        parts = []
        if self.prefix:
            parts.append(self.prefix)
        parts.extend(["artifacts", project, task_id, filename])
        return "/".join(parts)

    def store_file(self, project: str, task_id: str, local_path: Path, remote_filename: Optional[str] = None) -> str:
        filename = remote_filename or local_path.name
        key = self._get_key(project, task_id, filename)
        
        self.client.upload_file(str(local_path), self.bucket, key)
        return f"s3://{self.bucket}/{key}"

    def store_content(self, project: str, task_id: str, content: str, filename: str) -> str:
        key = self._get_key(project, task_id, filename)
        
        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=content.encode("utf-8"),
            ContentType="text/plain"
        )
        return f"s3://{self.bucket}/{key}"

def get_artifact_store() -> ArtifactStore:
    """Factory to create the configured artifact store."""
    backend = os.getenv("HERMES_ARTIFACT_BACKEND", "local").lower()
    
    if backend == "s3":
        bucket = os.getenv("HERMES_S3_BUCKET")
        if not bucket:
            logger.warning("HERMES_S3_BUCKET not set, falling back to local artifact store")
            return LocalArtifactStore()
            
        prefix = os.getenv("HERMES_S3_PREFIX", "")
        region = os.getenv("AWS_DEFAULT_REGION") or os.getenv("AWS_REGION")
        
        try:
            return S3ArtifactStore(bucket=bucket, prefix=prefix, region=region)
        except ImportError:
            logger.error("boto3 not installed, cannot use S3ArtifactStore. Falling back to local.")
            return LocalArtifactStore()
    
    return LocalArtifactStore()
