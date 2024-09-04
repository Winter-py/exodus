import os
import logging
import boto3
from botocore.exceptions import ClientError

def upload_to_s3(bucket_name, file_path, object_name=None):
    
    if object_name is None:
        object_name = os.path.basename(file_path)
        
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    
    
def check_bucket_exists(s3_client, bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            return False
        else:
            raise e
    
    
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
    
    