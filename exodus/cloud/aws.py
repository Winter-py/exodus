import os
import logging
import boto3
import shutil
import tempfile
import zipfile
from botocore.exceptions import ClientError
from exodus.utils.neaten import clean_up_failed_backup
from tqdm import tqdm

def upload_zipfile_to_s3(bucket_name, zip_file_path, s3_key=None):
    """
    Upload a ZIP file to an S3 bucket with progress tracking.

    :param bucket_name: The name of the S3 bucket.
    :param zip_file_path: The local path to the ZIP file to upload.
    :param s3_key: The S3 key (path in the bucket). Defaults to the ZIP file name.
    :return: True if upload was successful, False otherwise.
    """
    s3_client = boto3.client('s3')

    # Use the ZIP file's name as the S3 key if not provided
    if s3_key is None:
        s3_key = os.path.basename(zip_file_path)

    try:
        # Get the size of the file to upload
        file_size = os.path.getsize(zip_file_path)

        # Open the file in binary mode
        with open(zip_file_path, 'rb') as f:
            # Create a tqdm progress bar
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Uploading {s3_key}") as pbar:
                # Define a callback to update tqdm
                def progress_callback(bytes_transferred):
                    pbar.update(bytes_transferred)

                # Use upload_fileobj to provide a callback for progress tracking
                s3_client.upload_fileobj(f, bucket_name, s3_key, Callback=progress_callback)

        print(f"Uploaded {zip_file_path} to s3://{bucket_name}/{s3_key}")
        return True
    except ClientError as e:
        logging.error(f"Failed to upload {zip_file_path} to S3: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False

def upload_to_s3(bucket_name, file_path, object_name=None):
    
    if object_name is None:
        object_name = file_path.split('/')[-1]
        
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
    
    
    
def upload_zip_to_s3(bucket_name, zip_file_path, s3_folder_name=None):
    # Use the system's temporary directory
    temp_dir = tempfile.gettempdir()

    # Create a unique subdirectory in the temp directory
    extracted_dir = os.path.join(temp_dir, "exodus_backup.zip")
    os.makedirs(extracted_dir, exist_ok=True)

    # Extract the ZIP file into the temporary directory
    with zipfile.ZipFile(zip_file_path, 'r') as zipf:
        zipf.extractall(extracted_dir)
    
    # Upload the extracted contents to S3
    result = upload_zipfile_to_s3(bucket_name, zip_file_path, s3_folder_name)

    # Cleanup
    shutil.rmtree(extracted_dir, ignore_errors=True)
    return result