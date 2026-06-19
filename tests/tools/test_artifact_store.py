import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from tools.artifact_store import get_artifact_store, LocalArtifactStore, S3ArtifactStore

try:
    import boto3
    from moto import mock_aws
    HAS_S3_DEPS = True
except ImportError:
    HAS_S3_DEPS = False

def test_local_store_file(tmp_path):
    store = LocalArtifactStore(root=tmp_path)
    local_file = tmp_path / "test.txt"
    local_file.write_text("hello")
    
    uri = store.store_file("proj1", "task1", local_file)
    assert uri.startswith("file://")
    assert Path(uri.replace("file://", "")).exists()
    assert Path(uri.replace("file://", "")).read_text() == "hello"

def test_local_store_content(tmp_path):
    store = LocalArtifactStore(root=tmp_path)
    uri = store.store_content("proj1", "task1", "some content", "content.txt")
    assert uri.startswith("file://")
    assert Path(uri.replace("file://", "")).read_text() == "some content"

@pytest.mark.skipif(not HAS_S3_DEPS, reason="boto3 or moto not installed")
@mock_aws
def test_s3_store_file(tmp_path):
    bucket_name = "test-bucket"
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)
    
    store = S3ArtifactStore(bucket=bucket_name, prefix="hermes/")
    local_file = tmp_path / "s3-test.txt"
    local_file.write_text("s3-content")
    
    uri = store.store_file("proj1", "task1", local_file)
    assert uri == f"s3://{bucket_name}/hermes/artifacts/proj1/task1/s3-test.txt"
    
    response = s3.get_object(Bucket=bucket_name, Key="hermes/artifacts/proj1/task1/s3-test.txt")
    assert response["Body"].read().decode("utf-8") == "s3-content"

@pytest.mark.skipif(not HAS_S3_DEPS, reason="boto3 or moto not installed")
@mock_aws
def test_s3_store_content():
    bucket_name = "test-bucket"
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)
    
    store = S3ArtifactStore(bucket=bucket_name)
    uri = store.store_content("proj1", "task1", "raw-content", "raw.txt")
    assert uri == f"s3://{bucket_name}/artifacts/proj1/task1/raw.txt"
    
    response = s3.get_object(Bucket=bucket_name, Key="artifacts/proj1/task1/raw.txt")
    assert response["Body"].read().decode("utf-8") == "raw-content"

def test_factory_local():
    with patch.dict(os.environ, {"HERMES_ARTIFACT_BACKEND": "local"}):
        store = get_artifact_store()
        assert isinstance(store, LocalArtifactStore)

@pytest.mark.skipif(not HAS_S3_DEPS, reason="boto3 not installed")
def test_factory_s3():
    envs = {
        "HERMES_ARTIFACT_BACKEND": "s3",
        "HERMES_S3_BUCKET": "my-bucket",
        "AWS_DEFAULT_REGION": "eu-west-1"
    }
    with patch.dict(os.environ, envs):
        store = get_artifact_store()
        assert isinstance(store, S3ArtifactStore)
        assert store.bucket == "my-bucket"
