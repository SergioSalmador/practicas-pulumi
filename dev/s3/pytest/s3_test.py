import pytest
from pulumi_aws import s3
from s3.__main__ import create_s3_bucket, set_bucket_lifecycle

@pytest.fixture
def mock_s3_bucket(mocker):
    return mocker.patch.object(s3, 'Bucket')

@pytest.fixture
def mock_s3_lifecycle(mocker):
    return mocker.patch.object(s3, 'BucketLifecycleConfiguration')

def test_create_s3_bucket(mock_s3_bucket):
    create_s3_bucket("test-bucket", "dev", "us-west-2", "mycompany")
    mock_s3_bucket.assert_called_with(
        "test-bucket",
        bucket="test-bucket",
        acl="private",
        tags={
            "Environment": "dev",
            "Region": "us-west-2",
            "Company": "mycompany",
            "Name": "test-bucket"
        }
    )

def test_set_bucket_lifecycle(mock_s3_lifecycle):
    set_bucket_lifecycle("arn:aws:s3:::test-bucket", 30)
    mock_s3_lifecycle.assert_called_with(
        "bucketLifecycleConfiguration",
        bucket="arn:aws:s3:::test-bucket",
        rules=[...]
    )
