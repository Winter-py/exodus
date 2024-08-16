import boto3

def upload_to_s3(bucket_name, file_path, object_name=None):
    s3 = boto3.client('s3')
    if object_name is None:
        object_name = file_path
    
    s3.upload_file(file_path, bucket_name, object_name)
    
    
    
def create_s3_bucket(bucket_name):
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=bucket_name)