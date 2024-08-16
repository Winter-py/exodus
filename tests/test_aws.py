import unittest
from unittest.mock import patch
import boto3
from moto import mock_s3
from exodus.cloud.aws import upload_to_s3, create_s3_bucket  # Replace 'my_module' with your actual module name

class TestS3Functions(unittest.TestCase):

    @mock_s3
    def test_create_s3_bucket(self):
        region = "us-west-1"
        bucket_name = "test-bucket"

        # Call the function to create the bucket
        create_s3_bucket(region, bucket_name)

        # Assert that the bucket exists
        s3 = boto3.client('s3', region_name=region)
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        self.assertIn(bucket_name, buckets)

    @mock_s3
    def test_upload_to_s3(self):
        region = "us-west-1"
        bucket_name = "test-bucket"
        file_path = "test.txt"
        object_name = "uploaded_test.txt"

        # Create the bucket first
        s3 = boto3.client('s3', region_name=region)
        s3.create_bucket(Bucket=bucket_name)

        # Mock the open function to simulate a file
        with patch("builtins.open", unittest.mock.mock_open(read_data="data")) as mock_file:
            # Call the function to upload the file
            upload_to_s3(region, bucket_name, file_path, object_name)

        # Assert that the file was uploaded
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = [obj['Key'] for obj in response.get('Contents', [])]
        self.assertIn(object_name, objects)

if __name__ == '__main__':
    unittest.main()
