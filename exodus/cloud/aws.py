import os
import logging
import boto3
from botocore.exceptions import ClientError
from exodus.utils.neaten import clean_up_failed_backup
from tqdm import tqdm

def upload_folder_to_s3(bucket_name, folder_path, s3_folder_name=None):
    if s3_folder_name is None:
        s3_folder_name = os.path.basename(folder_path)
    
    s3_client = boto3.client('s3')
    
    # Count total files
    total_files = sum([len(files) for r, d, files in os.walk(folder_path)])
    
    with tqdm(total=total_files, desc="Uploading folder to S3") as pbar:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)
                s3_key = os.path.join(s3_folder_name, relative_path)
                
                try:
                    s3_client.upload_file(file_path, bucket_name, s3_key)
                except ClientError as e:
                    logging.error(e)
                    return False
                pbar.update(1)
    
    print("Upload complete")
    return True

def upload_to_s3(bucket_name, file_path, object_name=None):
    
    if object_name is None:
        object_name = os.path.basename(file_path)
        
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_path(), bucket_name, object_name)
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
    
    # Check if bucket already exists
    if check_bucket_exists(s3, bucket_name):
        print(f"Bucket '{bucket_name}' already exists.")
        return False

    try:
        s3.create_bucket(Bucket=bucket_name,
                         CreateBucketConfiguration={
                           'LocationConstraint': region,
                        }
                          )
    except ClientError as e:
        print("Response:",e)
        clean_up_failed_backup()
        return False
    return True
    
    