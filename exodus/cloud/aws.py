import boto3
from botocore.exceptions import ClientError

def upload_to_s3(bucket_name, file_path, object_name=None):
    s3 = boto3.client('s3')
    if object_name is None:
        object_name = file_path
    try:
        s3.upload_file(file_path, bucket_name, object_name)
    except ClientError as e:
        print(e)
        return False
    return True
    
    
    
def create_s3_bucket(region,bucket_name):
    s3 = boto3.client('s3', region_name=region)
    try:
        s3.create_bucket(Bucket=bucket_name,
                         CreateBucketConfiguration={
                           'LocationConstraint': region,
                        }
                          )
    except ClientError as e:
        print("Response:",e)
        return False
    return True
    
    