import argparse
import tempfile
from datetime import datetime
from exodus.config.config_loader import ConfigLoader
from exodus.cloud.aws import create_s3_bucket, upload_folder_to_s3, upload_zip_to_s3
from exodus.backup.files import backup_files, compress_files, zip_files_in_directory
from exodus.backup.database import backup_database 

def main():
    #Initialize
    parser = argparse.ArgumentParser(description="Secure application transfer tool")
    parser.add_argument('-exce', '--config', help="Automate the transfer using a config file")
    parser.add_argument('-db', '--Database', help="Back up database", type=str) 
    
    
    #Parsing the argument
    args = parser.parse_args()


    config_loader = ConfigLoader(args.config)
    config = config_loader.load_config()
    
    #datatime 
    # current dateTime
    now = datetime.now()
    # convert to string
    date_time_str = now.strftime("%Y%m%d%H%M%S")

    #Backup files
    backup_dir = tempfile.gettempdir() + f"\\E{date_time_str}"
    backup_files(config['backup']['files'], backup_dir)
    
    #Backup Database
    # backup_database(config['database']['type'],config)
    
    # Compress files 
    zip_file_path = zip_files_in_directory(backup_dir)
    

    #Upload to S3
    region = config['cloud']['region']
    bucket_name = config['cloud']['s3_bucket_name']
    create_s3_bucket(region,bucket_name)
    upload_zip_to_s3(bucket_name, zip_file_path)

    if args.Database:
        print("something happned") 
    
    
if __name__ == "__main__":
    main()