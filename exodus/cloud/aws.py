import boto3

def upload_to_s3(region,bucket_name, file_path, object_name=None):
    s3 = boto3.client('s3', region_name=region)
    if object_name is None:
        object_name = file_path
    
    s3.upload_file(file_path, bucket_name, object_name)
    
    
    
def create_s3_bucket(region,bucket_name):
    s3 = boto3.client('s3', region_name=region)
    s3.create_bucket(Bucket=bucket_name)